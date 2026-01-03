# 🎉 Your App is Running!

## ✅ Current Status

Your WGS Slicer app is now running on port **1199**!

## 🌐 How to Access It

### Find Your Server IP:
```bash
hostname -I
```

### Access the App:
- **From BCM network**: `http://[your-server-ip]:1199`
- **From outside**: Connect to BCM VPN first, then access `http://[your-server-ip]:1199`

Replace `[your-server-ip]` with the actual IP address from `hostname -I`.

## ⚠️ Note About the Warning

The CORS/XSRF warning is just informational - your app will work fine. I've updated the config file to fix it for future runs.

## 🔄 Keep It Running

### Option 1: Keep Terminal Open
The app will run as long as your SSH session is active. If you disconnect, it will stop.

### Option 2: Run in Background (nohup)
Press `Ctrl+C` to stop the current instance, then:

```bash
cd ~/SlicerToWebsite/WGSSlicer
source ~/anaconda3/etc/profile.d/conda.sh
conda activate wgs-slicer
nohup streamlit run WGS_Slicer_v2.py --server.port=1199 --server.address=0.0.0.0 > streamlit.log 2>&1 &
```

This will:
- Run in the background
- Keep running after you disconnect
- Log output to `streamlit.log`

To check if it's running:
```bash
ps aux | grep streamlit
```

To stop it:
```bash
pkill -f streamlit
```

### Option 3: Set Up as Systemd Service (Recommended for Production)

I can help you set this up so it:
- Starts automatically on server boot
- Restarts if it crashes
- Runs in the background

Let me know if you want help with this!

## 📝 Quick Commands

**Check if app is running:**
```bash
ps aux | grep streamlit
```

**View logs (if using nohup):**
```bash
tail -f ~/SlicerToWebsite/WGSSlicer/streamlit.log
```

**Stop the app:**
```bash
pkill -f streamlit
```

**Restart the app:**
```bash
cd ~/SlicerToWebsite/WGSSlicer
source ~/anaconda3/etc/profile.d/conda.sh
conda activate wgs-slicer
streamlit run WGS_Slicer_v2.py --server.port=1199 --server.address=0.0.0.0
```

## 🎯 Next Steps

1. **Test the app**: Access it in your browser and try logging in
2. **Set up background service**: If you want it to run automatically
3. **Configure firewall**: Make sure port 1199 is open if needed

Your app is live! 🚀

