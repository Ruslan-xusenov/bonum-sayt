#!/bin/bash

# --- Configuration ---
PROJECT_NAME="nextmarket"
DOMAIN="nextmarket.ruslandev.uz"
GITHUB_REPO="https://github.com/Ruslan-xusenov/bonum-sayt.git"
USER_NAME=$(whoami)
PROJECT_DIR="/home/$USER_NAME/$PROJECT_NAME"
VENV_PATH="$PROJECT_DIR/venv"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}NextMarket Deployment Script${NC}"
echo "---------------------------"

show_menu() {
    echo "1) Full Initial Setup (New Server)"
    echo "2) Update Project (Pull & Restart)"
    echo "3) Exit"
}

initial_setup() {
    echo -e "${GREEN}[1/8] Updating System Packages...${NC}"
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y python3-pip python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl redis-server git

    echo -e "${GREEN}[2/8] Setting up PostgreSQL...${NC}"
    # Create DB and User if they don't exist
    DB_NAME="nextmarket_db"
    DB_USER="nextmarket_user"
    DB_PASS=$(openssl rand -base64 12)
    
    sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
    sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
    sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
    sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
    sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'UTC';"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

    echo -e "${GREEN}[3/8] Cloning Repository...${NC}"
    if [ ! -d "$PROJECT_DIR" ]; then
        git clone $GITHUB_REPO $PROJECT_DIR
    else
        echo "Directory $PROJECT_DIR already exists. Skipping clone."
    fi
    cd $PROJECT_DIR

    echo -e "${GREEN}[4/8] Setting up Virtual Environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install gunicorn daphne uvicorn channels-redis dj-database-url django-redis whitenoise

    echo -e "${GREEN}[5/8] Creating .env file...${NC}"
    cat <<EOF > .env
DJANGO_SECRET_KEY=$(openssl rand -base64 32)
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=$DOMAIN,91.99.1.216
DATABASE_URL=postgres://$DB_USER:$DB_PASS@localhost:5432/$DB_NAME
REDIS_URL=redis://127.0.0.1:6379/1
CORS_ALLOWED_ORIGINS=https://$DOMAIN
DJANGO_CSRF_TRUSTED_ORIGINS=https://$DOMAIN
EOF
    echo "Done. Please update .env with Cloudinary and Telegram credentials manually."

    echo -e "${GREEN}[6/8] Migrations and Static Files...${NC}"
    python3 manage.py migrate
    python3 manage.py collectstatic --noinput

    echo -e "${GREEN}[7/8] Configuring Systemd (Daphne)...${NC}"
    cat <<EOF | sudo tee /etc/systemd/system/daphne.service
[Unit]
Description=Daphne service for $PROJECT_NAME
After=network.target

[Service]
User=$USER_NAME
Group=www-data
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/daphne -u $PROJECT_DIR/daphne.sock config.asgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl start daphne
    sudo systemctl enable daphne

    echo -e "${GREEN}[8/8] Configuring Nginx...${NC}"
    cat <<EOF | sudo tee /etc/nginx/sites-available/$PROJECT_NAME
server {
    listen 80;
    server_name $DOMAIN 91.99.1.216;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
    }

    location /media/ {
        alias $PROJECT_DIR/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$PROJECT_DIR/daphne.sock;
    }

    location /ws/ {
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_redirect off;
        proxy_pass http://unix:$PROJECT_DIR/daphne.sock;
    }
}
EOF

    sudo ln -s /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/
    sudo nginx -t && sudo systemctl restart nginx

    echo -e "${YELLOW}Setup Complete! Site should be live at http://$DOMAIN${NC}"
    echo -e "${YELLOW}To enable SSL (HTTPS), run: sudo apt install certbot python3-certbot-nginx && sudo certbot --nginx -d $DOMAIN${NC}"
}

update_project() {
    echo -e "${GREEN}Updating Project...${NC}"
    cd $PROJECT_DIR
    git pull origin main
    source venv/bin/activate
    pip install -r requirements.txt
    python3 manage.py migrate
    python3 manage.py collectstatic --noinput
    sudo systemctl restart daphne
    sudo systemctl restart nginx
    echo -e "${GREEN}Update Complete!${NC}"
}

while true; do
    show_menu
    read -p "Choose an option: " choice
    case $choice in
        1) initial_setup ;;
        2) update_project ;;
        3) exit 0 ;;
        *) echo -e "${RED}Invalid option${NC}" ;;
    esac
done
