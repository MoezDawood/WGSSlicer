# Solution: SSH Connection Issue on Streamlit Cloud

## 🔴 The Problem

Streamlit Cloud servers **cannot** access your BCM internal server (`10.66.4.211`) because:
- Streamlit Cloud runs on their own servers (not on BCM network)
- Your VPN only affects YOUR computer, not Streamlit's servers
- The BCM server IP (`10.66.4.211`) is only accessible from within the BCM network

## ✅ Solution Options

### Option 1: Deploy on BCM Server (RECOMMENDED - Best Solution)

Deploy the app directly on a BCM server that has access to the data server.

#### Steps:

1. **SSH into a BCM server** (one that can access `10.66.4.211`):
   ```bash
   ssh your-username@bcm-server.bcm.edu
   ```

2. **Clone your repository**:
   ```bash
   git clone https://github.com/MoezDawood/WGSSlicer.git
   cd WGSSlicer
   ```

3. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the app**:
   ```bash
   streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
   ```

5. **Access via BCM network**:
   - If on BCM network: `http://bcm-server-ip:8501`
   - If outside: Connect to BCM VPN first, then access

#### Advantages:
- ✅ Direct access to BCM server
- ✅ No network restrictions
- ✅ Full control
- ✅ Free (uses BCM resources)

#### Setup for Production (Optional):

Use a process manager to keep it running:

```bash
# Install PM2
npm install -g pm2

# Create ecosystem.config.js
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'wgs-slicer',
    script: 'streamlit',
    args: 'run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0',
    interpreter: 'python3',
    autorestart: true,
    watch: false
  }]
}
EOF

# Start the app
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

---

### Option 2: Use Railway.app (May Work)

Railway sometimes allows SSH connections. Worth trying:

1. Go to https://railway.app
2. Sign in with GitHub
3. Create new project from GitHub repo
4. Select `MoezDawood/WGSSlicer`
5. Railway will auto-detect and deploy
6. Test if SSH works

**Note**: This may still fail if Railway blocks SSH or can't reach internal IPs.

---

### Option 3: Modify App Architecture (Advanced)

Create a proxy/tunnel solution, but this is complex and may not be worth it.

---

### Option 4: Use Streamlit Cloud with Different Approach

If the data files could be:
- Copied to a publicly accessible location (S3, GitHub, etc.)
- Or accessed via a public API

Then modify the app to use that instead of SSH. But this requires changing your data infrastructure.

---

## 🎯 Recommended Action Plan

**Best approach**: Deploy on BCM server (Option 1)

1. **Contact BCM IT** or your lab's system administrator
2. **Ask for**:
   - Access to a server that can run Streamlit apps
   - Port 8501 (or another port) opened for web access
   - Or use an existing web server infrastructure

3. **Deploy using the steps in Option 1 above**

---

## 📝 Quick Deploy Script for BCM Server

I'll create a deployment script you can run on the BCM server:

```bash
#!/bin/bash
# deploy-on-bcm.sh

echo "🚀 Deploying WGS Slicer on BCM Server..."

# Clone/update repository
if [ -d "WGSSlicer" ]; then
    cd WGSSlicer
    git pull
else
    git clone https://github.com/MoezDawood/WGSSlicer.git
    cd WGSSlicer
fi

# Install dependencies
pip3 install -r requirements.txt

# Run the app
echo "✅ Starting Streamlit app on port 8501..."
streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
```

---

## 🔍 Testing the Connection

To verify if a platform can reach your BCM server, you can add a test function to your app or run this Python script:

```python
import paramiko
import sys

def test_ssh_connection():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect("10.66.4.211", username="test", password="test", timeout=5)
        print("✅ SSH connection successful!")
        client.close()
        return True
    except Exception as e:
        print(f"❌ SSH connection failed: {e}")
        return False

if __name__ == "__main__":
    test_ssh_connection()
```

---

## 💡 Alternative: Keep Streamlit Cloud for Demo, Use BCM for Production

You could:
- Keep the Streamlit Cloud version as a demo (with a note about VPN requirement)
- Deploy the working version on BCM server for actual use
- Users on BCM network/VPN can use the BCM-hosted version

---

## Need Help?

- Contact BCM IT for server access
- Check with your lab's system administrator
- Consider asking if BCM has a web hosting service for research apps

