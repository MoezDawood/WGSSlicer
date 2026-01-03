# Troubleshooting Connection Issues

## Issue: "Connection Refused" when accessing the app

### Step 1: Verify App is Running on BCM Server

On your **BCM server** (SSH session), check:

```bash
# Check if streamlit process is running
ps aux | grep streamlit

# Check if port 1199 is listening
netstat -tulpn | grep 1199
# or
ss -tulpn | grep 1199
```

### Step 2: Check Firewall

On the **BCM server**, check if firewall is blocking:

```bash
# Check firewall status
sudo firewall-cmd --list-all
# or
sudo iptables -L -n | grep 1199
# or
sudo ufw status
```

If firewall is active, allow port 1199:
```bash
sudo firewall-cmd --permanent --add-port=1199/tcp
sudo firewall-cmd --reload
# or for ufw:
sudo ufw allow 1199/tcp
```

### Step 3: Verify Network Access

**Important**: You must be on the BCM network to access `10.66.4.211`:

1. **Are you on BCM WiFi?** - If yes, you should be able to access it
2. **Are you on BCM VPN?** - If working from home, connect to BCM VPN first
3. **Is `10.66.4.211` the correct server IP?** - Verify on the server:

```bash
# On BCM server, find its IP
hostname -I
# or
ip addr show | grep "inet " | grep -v 127.0.0.1
```

### Step 4: Restart App with Correct Binding

If the app isn't listening on the external interface, restart it:

```bash
# On BCM server
cd ~/SlicerToWebsite/WGSSlicer
source ~/anaconda3/etc/profile.d/conda.sh
conda activate wgs-slicer

# Stop any existing instance
pkill -f streamlit

# Start with explicit binding
streamlit run WGS_Slicer_v2.py --server.port=1199 --server.address=0.0.0.0
```

### Step 5: Test Connection from Server

On the **BCM server**, test if the app responds:

```bash
curl http://localhost:1199
# or
curl http://10.66.4.211:1199
```

If this works on the server but not from your Mac, it's a network/firewall issue.

### Step 6: Check from Your Mac

On your **MacBook**, verify you can reach the server:

```bash
# Test if you can reach the server
ping 10.66.4.211

# Test if port 1199 is accessible
nc -zv 10.66.4.211 1199
# or
telnet 10.66.4.211 1199
```

If ping works but port doesn't, it's a firewall issue.

## Common Solutions

### Solution 1: Connect to BCM VPN
If you're not on BCM network, connect to VPN first.

### Solution 2: Open Firewall Port
```bash
# On BCM server
sudo firewall-cmd --permanent --add-port=1199/tcp
sudo firewall-cmd --reload
```

### Solution 3: Use Server's Actual IP
The server might have a different IP. Check with:
```bash
hostname -I
```

### Solution 4: Check App is Actually Running
```bash
ps aux | grep streamlit
# Should show a running process
```

## Quick Diagnostic Commands

Run these on **BCM server**:

```bash
# 1. Is app running?
ps aux | grep streamlit

# 2. Is port listening?
netstat -tulpn | grep 1199

# 3. What's the server IP?
hostname -I

# 4. Test locally
curl http://localhost:1199
```

Run these on **your Mac**:

```bash
# 1. Can you ping the server?
ping 10.66.4.211

# 2. Can you reach the port?
nc -zv 10.66.4.211 1199
```

