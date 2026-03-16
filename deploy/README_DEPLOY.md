# Deploying Bonum-Sayt

This project is configured for deployment using **Daphne** (ASGI), **Nginx**, **PostgreSQL**, and **Redis**.

## Files created:
- `deploy/deploy.sh`: Main deployment and update script.
- `deploy/nginx_template.conf`: Template for Nginx configuration.

## Prerequisites
1. A Ubuntu/Debian server with root access.
2. Domain pointed to the server IP (`91.99.1.216`).
3. GitHub repository pushed and accessible.

## How to use the script:

### 1. Initial Setup
On your server, run these commands:
```bash
git clone https://github.com/Ruslan-xusenov/bonum-sayt.git bonum-sayt
cd bonum-sayt/deploy
chmod +x deploy.sh
./deploy.sh
```
Select **Option 1** for the first-time setup. It will:
- Install all necessary system packages.
- Setup PostgreSQL database and user.
- Setup Virtual Environment and install Python packages.
- Create a `.env` file with secure keys.
- Run migrations and collect static files.
- Configure Daphne as a systemd service.
- Configure Nginx.

### 2. Updating the Project
Whenever you push changes to GitHub, run:
```bash
cd /var/www/bonum-sayt/deploy
./deploy.sh
```
Select **Option 2**. It will:
- Pull latest changes from Git.
- Install new requirements.
- Run migrations.
- Collect static files.
- Restart Daphne and Nginx.

## Post-Setup Actions
1. **Enable SSL (HTTPS):**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d bonumm.uz
   ```
2. **Update Environments:**
   Edit the `.env` file in the project root to add your Cloudinary and Telegram credentials.
   ```bash
   nano ../.env
   ```
3. **Check Logs:**
   If something is wrong, check Daphne logs:
   ```bash
   sudo journalctl -u daphne-bonum-sayt -f
   ```
   Or Nginx logs:
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```