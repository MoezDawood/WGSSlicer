# Quick BCM Server Deployment

Fastest way to get your app running on a BCM server.

## 🚀 One-Command Setup

```bash
# On your BCM server, run:
bash <(curl -s https://raw.githubusercontent.com/MoezDawood/WGSSlicer/main/setup-bcm-server.sh)
```

Or manually:

```bash
# 1. Clone the repo
git clone https://github.com/MoezDawood/WGSSlicer.git
cd WGSSlicer

# 2. Run setup script
bash setup-bcm-server.sh
```

## 📋 What the Script Does

1. ✅ Checks Python and Git installation
2. ✅ Clones/updates the repository
3. ✅ Installs all dependencies
4. ✅ Sets up a service (systemd or PM2)
5. ✅ Starts the application

## 🎯 After Setup

Your app will be running at:
```
http://your-server-ip:8501
```

**To find your server IP:**
```bash
hostname -I
```

## 🔧 Quick Commands

**Check if app is running:**
```bash
# If using systemd
sudo systemctl status wgs-slicer

# If using PM2
pm2 status
```

**View logs:**
```bash
# systemd
sudo journalctl -u wgs-slicer -f

# PM2
pm2 logs wgs-slicer
```

**Restart app:**
```bash
# systemd
sudo systemctl restart wgs-slicer

# PM2
pm2 restart wgs-slicer
```

## ⚠️ Important Notes

1. **Port Access**: Make sure port 8501 is open:
   ```bash
   sudo ufw allow 8501/tcp
   ```

2. **BCM Network**: The app needs to be on the BCM network to access `10.66.4.211`

3. **VPN Access**: Users outside BCM network need VPN to access the app

## 📖 Full Documentation

See `BCM_SERVER_DEPLOYMENT.md` for complete instructions including:
- Nginx reverse proxy setup
- SSL/HTTPS configuration
- Security hardening
- Troubleshooting

