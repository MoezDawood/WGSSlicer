# BCM Server Deployment Guide

Complete guide for deploying WGS Slicer on a BCM server.

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ SSH access to a BCM server
- ✅ Python 3.7+ installed on the server
- ✅ Git installed on the server
- ✅ Port access (typically 8501 or another port approved by BCM IT)
- ✅ Permissions to install Python packages

## 🚀 Quick Start (Simple Deployment)

### Step 1: Connect to BCM Server

```bash
ssh your-username@bcm-server.bcm.edu
# Or use the specific server name/IP provided by BCM IT
```

### Step 2: Clone and Deploy

```bash
# Navigate to your preferred directory (e.g., /home/your-username or /var/www)
cd ~

# Clone the repository
git clone https://github.com/MoezDawood/WGSSlicer.git
cd WGSSlicer

# Install dependencies
pip3 install --user -r requirements.txt
# Or if you have sudo: sudo pip3 install -r requirements.txt

# Run the app
streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
```

### Step 3: Access the App

- **From BCM network**: `http://bcm-server-ip:8501`
- **From outside**: Connect to BCM VPN first, then access

**Note**: Replace `bcm-server-ip` with the actual IP address or hostname of your server.

---

## 🔧 Production Deployment (Recommended)

For a production setup that runs continuously and restarts automatically:

### Option A: Using systemd (Linux servers)

#### 1. Create systemd service file

```bash
sudo nano /etc/systemd/system/wgs-slicer.service
```

Copy this content:

```ini
[Unit]
Description=WGS Slicer Streamlit Application
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/WGSSlicer
Environment="PATH=/usr/bin:/usr/local/bin:/home/your-username/.local/bin"
ExecStart=/usr/bin/streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Important**: Replace:
- `your-username` with your actual username
- `/home/your-username/WGSSlicer` with the actual path to your app

#### 2. Enable and start the service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable wgs-slicer

# Start the service
sudo systemctl start wgs-slicer

# Check status
sudo systemctl status wgs-slicer

# View logs
sudo journalctl -u wgs-slicer -f
```

#### 3. Useful Commands

```bash
# Stop the service
sudo systemctl stop wgs-slicer

# Restart the service
sudo systemctl restart wgs-slicer

# Disable auto-start on boot
sudo systemctl disable wgs-slicer

# View recent logs
sudo journalctl -u wgs-slicer -n 50
```

---

### Option B: Using PM2 (Node.js process manager)

#### 1. Install PM2

```bash
# Install Node.js if not already installed
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 globally
sudo npm install -g pm2
```

#### 2. Use the provided ecosystem file

The repository includes `ecosystem.config.js`. Just run:

```bash
cd ~/WGSSlicer
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

#### 3. Useful PM2 Commands

```bash
# View status
pm2 status

# View logs
pm2 logs wgs-slicer

# Restart
pm2 restart wgs-slicer

# Stop
pm2 stop wgs-slicer

# Delete
pm2 delete wgs-slicer
```

---

## 🌐 Setting Up Reverse Proxy (Optional but Recommended)

If you want to access the app via a domain name or port 80/443:

### Using Nginx

#### 1. Install Nginx

```bash
sudo apt-get update
sudo apt-get install nginx
```

#### 2. Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/wgs-slicer
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.bcm.edu;  # Or use IP address

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

#### 3. Enable the Site

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/wgs-slicer /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

#### 4. Access via Domain

Now you can access the app at: `http://your-domain.bcm.edu`

---

## 🔒 Security Considerations

### 1. Firewall Configuration

```bash
# Allow port 8501 (or your chosen port)
sudo ufw allow 8501/tcp

# Or if using Nginx on port 80
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp  # If using HTTPS
```

### 2. Add Authentication (Optional)

Consider adding authentication to your Streamlit app or using Nginx basic auth:

```bash
# Install apache2-utils
sudo apt-get install apache2-utils

# Create password file
sudo htpasswd -c /etc/nginx/.htpasswd username

# Add to Nginx config
auth_basic "Restricted Access";
auth_basic_user_file /etc/nginx/.htpasswd;
```

### 3. Use HTTPS (Recommended for Production)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.bcm.edu
```

---

## 📝 Updating the App

When you push updates to GitHub:

```bash
cd ~/WGSSlicer
git pull origin main

# If using systemd
sudo systemctl restart wgs-slicer

# If using PM2
pm2 restart wgs-slicer
```

---

## 🐛 Troubleshooting

### App won't start

1. **Check Python and dependencies**:
   ```bash
   python3 --version
   pip3 list | grep streamlit
   ```

2. **Check if port is in use**:
   ```bash
   sudo netstat -tulpn | grep 8501
   # Or
   sudo lsof -i :8501
   ```

3. **Check logs**:
   ```bash
   # systemd
   sudo journalctl -u wgs-slicer -n 100
   
   # PM2
   pm2 logs wgs-slicer
   ```

### Can't connect from browser

1. **Check firewall**:
   ```bash
   sudo ufw status
   ```

2. **Check if app is running**:
   ```bash
   # systemd
   sudo systemctl status wgs-slicer
   
   # PM2
   pm2 status
   ```

3. **Test locally on server**:
   ```bash
   curl http://localhost:8501
   ```

### Permission errors

1. **Check file permissions**:
   ```bash
   ls -la ~/WGSSlicer
   chmod +x ~/WGSSlicer/*.py
   ```

2. **Check user permissions**:
   ```bash
   whoami
   # Make sure service runs as correct user
   ```

---

## 📞 Getting Help

### Contact BCM IT

If you need:
- Server access
- Port opening
- Domain name setup
- SSL certificates
- Firewall configuration

Contact: BCM IT Support

### Check Logs

Always check logs first when troubleshooting:
- Application logs (systemd/PM2)
- Nginx logs: `/var/log/nginx/error.log`
- System logs: `journalctl -xe`

---

## ✅ Deployment Checklist

- [ ] SSH access to BCM server
- [ ] Python 3.7+ installed
- [ ] Git installed
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] App tested locally on server
- [ ] Port opened in firewall
- [ ] Service configured (systemd or PM2)
- [ ] Service starts on boot
- [ ] App accessible from network
- [ ] (Optional) Nginx reverse proxy configured
- [ ] (Optional) SSL certificate installed
- [ ] Documentation updated with access URL

---

## 🎯 Quick Reference

**Start app manually:**
```bash
cd ~/WGSSlicer
streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
```

**Start with systemd:**
```bash
sudo systemctl start wgs-slicer
```

**Start with PM2:**
```bash
pm2 start ecosystem.config.js
```

**View logs:**
```bash
# systemd
sudo journalctl -u wgs-slicer -f

# PM2
pm2 logs wgs-slicer
```

**Update app:**
```bash
cd ~/WGSSlicer
git pull
sudo systemctl restart wgs-slicer  # or pm2 restart wgs-slicer
```

