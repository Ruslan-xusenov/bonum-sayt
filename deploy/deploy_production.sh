#!/bin/bash

# =========================================
#  Bonum-Sayt Production Deployment Script
# =========================================

set -e

# --- Configuration ---
PROJECT_NAME="bonum-sayt"
DOMAIN="bonumm.uz"
GITHUB_REPO="https://github.com/Ruslan-xusenov/bonum-sayt.git"
PROJECT_DIR="/var/www/$PROJECT_NAME"
VENV_DIR="$PROJECT_DIR/venv"
USER=$(whoami)
GROUP="www-data"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

echo "1. Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y
print_status "System updated"

echo ""
echo "2. Installing required packages..."
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    postgresql \
    postgresql-contrib \
    nginx \
    redis-server \
    git \
    certbot \
    python3-certbot-nginx \
    ufw \
    curl \
    libpq-dev
print_status "Packages installed"

echo ""
echo "3. Setting up PostgreSQL..."
# Variables for DB
DB_NAME="bonum_sayt_db"
DB_USER="bonum_sayt_user"
DB_PASS=$(openssl rand -base64 12)

# Check if DB exists
if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    sudo -u postgres psql << EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\q
EOF
    print_status "PostgreSQL database and user created"
else
    print_warning "Database $DB_NAME already exists. Skipping creation."
    DB_PASS="ALREADY_SET_DURING_INITIAL_SETUP"
fi

echo ""
echo "4. Setting up project directory..."
if [ ! -d "$PROJECT_DIR" ]; then
    sudo mkdir -p /var/www
    sudo git clone $GITHUB_REPO $PROJECT_DIR
    sudo chown -R $USER:$GROUP $PROJECT_DIR
    print_status "Repository cloned"
else
    print_warning "Directory $PROJECT_DIR already exists. Updating code..."
    cd $PROJECT_DIR
    git pull origin main
    print_status "Code updated"
fi

mkdir -p $PROJECT_DIR/logs
mkdir -p $PROJECT_DIR/staticfiles
mkdir -p $PROJECT_DIR/media
print_status "Directories created"

echo ""
echo "5. Setting up virtual environment..."
cd $PROJECT_DIR
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn daphne uvicorn channels-redis dj-database-url django-redis whitenoise psycopg2-binary
print_status "Virtual environment ready"

echo ""
echo "6. Django setup (.env and migrations)..."
if [ ! -f ".env" ]; then
    cat <<EOF > .env
DJANGO_SECRET_KEY=$(openssl rand -base64 32)
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=$DOMAIN,91.99.1.216
DATABASE_URL=postgres://$DB_USER:$DB_PASS@localhost:5432/$DB_NAME
REDIS_URL=redis://127.0.0.1:6379/1
CORS_ALLOWED_ORIGINS=https://$DOMAIN
DJANGO_CSRF_TRUSTED_ORIGINS=https://$DOMAIN,https://91.99.1.216
# Add your Cloudinary and Telegram tokens here
# CLOUDINARY_CLOUD_NAME=...
EOF
    print_status ".env file created"
else
    print_warning ".env file already exists. Skipping creation."
fi

python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput
print_status "Django migrations and static files configured"

echo ""
echo "7. Setting permissions..."
sudo chown -R $USER:$GROUP $PROJECT_DIR
sudo chmod -R 755 $PROJECT_DIR
# Media directory needs write access for www-data if uploading files via app
sudo chmod -R 775 $PROJECT_DIR/media
print_status "Permissions set"

echo ""
echo "8. Setting up Systemd service (Daphne)..."
cat <<EOF | sudo tee /etc/systemd/system/daphne-$PROJECT_NAME.service
[Unit]
Description=Daphne service for $PROJECT_NAME
After=network.target

[Service]
User=$USER
Group=$GROUP
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/daphne -u $PROJECT_DIR/daphne.sock config.asgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable daphne-$PROJECT_NAME
sudo systemctl restart daphne-$PROJECT_NAME
print_status "Daphne systemd service (daphne-$PROJECT_NAME) configured"

echo ""
echo "9. Setting up Nginx..."
cat <<EOF | sudo tee /etc/nginx/sites-available/$PROJECT_NAME.conf
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

sudo ln -sf /etc/nginx/sites-available/$PROJECT_NAME.conf /etc/nginx/sites-enabled/
# sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx
print_status "Nginx configured"

echo ""
echo "10. Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
print_status "Firewall configured"

echo ""
echo "11. Configuring Redis..."
sudo systemctl enable redis-server
sudo systemctl start redis-server
print_status "Redis configured"

echo ""
echo "12. Creating Django superuser..."
print_warning "If this is the first time, you may want to create a superuser."
print_warning "Run: source venv/bin/activate && python manage.py createsuperuser"

echo ""
echo "========================================="
echo -e "${GREEN}  Deployment Complete!${NC}"
echo "========================================="
echo ""
echo "Key information:"
echo "1. Domain: https://$DOMAIN"
echo "2. Project Dir: $PROJECT_DIR"
echo "3. To enable SSL (HTTPS), run:"
echo "   sudo certbot --nginx -d $DOMAIN"
echo ""
echo "Next steps:"
echo "- Update .env with your actual Telegram/Cloudinary credentials"
echo "- Run SSL setup manually"
echo ""
print_status "All done!"
