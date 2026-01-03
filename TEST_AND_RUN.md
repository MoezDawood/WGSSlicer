# Test and Run Your App

## Step 1: Verify Installation

```bash
# Make sure you're in the conda environment
source ~/anaconda3/etc/profile.d/conda.sh
conda activate wgs-slicer

# Test all imports
python -c "import streamlit; import paramiko; import pandas; import pyarrow; print('✅ All packages imported successfully!')"
```

## Step 2: Run the App

```bash
# Navigate to your app directory
cd ~/SlicerToWebsite/WGSSlicer

# Run the Streamlit app
streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
```

## Step 3: Access the App

Once running, you'll see output like:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://10.66.4.211:8501
```

Access it at: `http://your-server-ip:8501`

To find your server IP:
```bash
hostname -I
```

## Step 4: Set Up as a Service (Optional - For Production)

If you want the app to run automatically in the background:

### Option A: Using systemd

```bash
# Create service file
sudo nano /etc/systemd/system/wgs-slicer.service
```

Paste this (update paths as needed):
```ini
[Unit]
Description=WGS Slicer Streamlit Application
After=network.target

[Service]
Type=simple
User=mdawood
WorkingDirectory=/storage/lupski/home/mdawood/SlicerToWebsite/WGSSlicer
Environment="PATH=/storage/lupski/home/mdawood/anaconda3/bin:/usr/bin:/usr/local/bin"
ExecStart=/bin/bash -c "source /storage/lupski/home/mdawood/anaconda3/etc/profile.d/conda.sh && conda activate wgs-slicer && streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0"
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable wgs-slicer
sudo systemctl start wgs-slicer
sudo systemctl status wgs-slicer
```

### Option B: Run in Background with nohup

```bash
cd ~/SlicerToWebsite/WGSSlicer
source ~/anaconda3/etc/profile.d/conda.sh
conda activate wgs-slicer
nohup streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0 > streamlit.log 2>&1 &
```

## Troubleshooting

### App won't start
- Check if port 8501 is in use: `netstat -tulpn | grep 8501`
- Check logs if using systemd: `sudo journalctl -u wgs-slicer -f`

### Can't access from browser
- Make sure firewall allows port 8501: `sudo ufw allow 8501/tcp`
- Verify app is running: `ps aux | grep streamlit`
- Check server IP: `hostname -I`

### Import errors
- Make sure conda environment is activated
- Verify packages: `conda list` and `pip list`

