# SSH Tunnel Access Guide

This allows users to access the app through an SSH tunnel, bypassing the firewall.

## How It Works

1. User creates an SSH tunnel from their computer to the BCM server
2. The tunnel forwards local port 8501 to the server's port 8501
3. User accesses `http://localhost:8501` in their browser
4. Traffic goes through the SSH tunnel securely

## For Users: How to Access

### Step 1: Create SSH Tunnel

**On your MacBook/computer:**

```bash
ssh -L 8501:localhost:8501 mdawood@10.66.4.211
```

This will:
- Connect to the BCM server
- Forward your local port 8501 to the server's port 8501
- Keep the connection open

### Step 2: Keep Terminal Open

**Important**: Keep this terminal window open while using the app. The tunnel stays active as long as the SSH session is open.

### Step 3: Access the App

Open your browser and go to:
```
http://localhost:8501
```

You should see the WGS Slicer login page!

### Step 4: Use the App

- Enter your BCM username and password in the web form
- The app will connect to the BCM data server
- Use the app normally

### Step 5: Close Tunnel

When done, press `Ctrl+C` in the terminal to close the SSH tunnel.

## Alternative: Background SSH Tunnel

If you want the tunnel to run in the background:

```bash
# Create tunnel in background
ssh -f -N -L 8501:localhost:8501 mdawood@10.66.4.211

# Check if it's running
ps aux | grep "ssh.*8501"

# Kill the tunnel when done
pkill -f "ssh.*8501"
```

## For Different Ports

If the app is on a different port (e.g., 1199), adjust the command:

```bash
ssh -L 1199:localhost:1199 mdawood@10.66.4.211
```

Then access `http://localhost:1199`

## Troubleshooting

### "Port already in use"
If port 8501 is already in use on your Mac:

```bash
# Use a different local port
ssh -L 8502:localhost:8501 mdawood@10.66.4.211
```

Then access `http://localhost:8502`

### "Connection refused"
- Make sure the app is running on the server
- Check: `ps aux | grep streamlit` on the server

### Tunnel keeps disconnecting
- Check your network connection
- The tunnel will close if SSH disconnects
- Re-run the SSH command to reconnect

## Advantages

✅ No firewall changes needed
✅ Secure (encrypted through SSH)
✅ Works from anywhere (just need SSH access)
✅ No root/sudo needed

## Disadvantages

⚠️ Users need SSH access to BCM server
⚠️ Must keep terminal/SSH session open
⚠️ Each user needs to create their own tunnel

