# Use Port 80 or 443 (Already Open!)

Great news! Ports **80** (HTTP) and **443** (HTTPS) are already open and listening on the server. These are standard web ports that are likely already allowed through the firewall.

## ✅ Solution: Switch to Port 80 or 443

### Option 1: Use Port 80 (HTTP) - Easiest

On your BCM server:

```bash
# Stop current instance
pkill -f streamlit

# Restart on port 80
cd ~/SlicerToWebsite/WGSSlicer
source ~/anaconda3/etc/profile.d/conda.sh
conda activate wgs-slicer
streamlit run WGS_Slicer_v2.py --server.port=80 --server.address=0.0.0.0
```

**Note**: Port 80 may require root privileges. If you get a permission error, use port 8080 instead (also open).

### Option 2: Use Port 8080 (Also Open)

```bash
# Stop current instance
pkill -f streamlit

# Restart on port 8080
cd ~/SlicerToWebsite/WGSSlicer
source ~/anaconda3/etc/profile.d/conda.sh
conda activate wgs-slicer
streamlit run WGS_Slicer_v2.py --server.port=8080 --server.address=0.0.0.0
```

### Option 3: Use Port 443 (HTTPS) - Most Secure

Port 443 is also open, but you'd need SSL certificates. Port 8080 is probably easiest.

## 🌐 Access Your App

After switching to port 80 or 8080:

- **Port 80**: `http://10.66.4.211`
- **Port 8080**: `http://10.66.4.211:8080`

## ⚠️ Note About Port 80

Port 80 (and 443) are "privileged ports" and may require root to bind. If you get a "Permission denied" error, use port 8080 instead - it's also open and doesn't require root.

## Quick Test

After switching ports, test from your MacBook:

```bash
# For port 80
nc -zv 10.66.4.211 80

# For port 8080
nc -zv 10.66.4.211 8080
```

If either works, you're all set! 🎉

