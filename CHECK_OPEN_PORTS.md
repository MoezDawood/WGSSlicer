# Check Open Ports on BCM Server

Safe commands to check which ports are open/listening (no root needed):

## Check Listening Ports

### Method 1: Using netstat
```bash
# Show all listening TCP ports
netstat -tuln | grep LISTEN

# Show listening ports with process names (if you have permissions)
netstat -tulpn | grep LISTEN

# Show only listening ports (cleaner output)
netstat -tuln | grep LISTEN | awk '{print $4}' | cut -d: -f2 | sort -n | uniq
```

### Method 2: Using ss (modern alternative)
```bash
# Show all listening TCP ports
ss -tuln | grep LISTEN

# Show with process names
ss -tulpn | grep LISTEN

# Show just port numbers
ss -tuln | grep LISTEN | awk '{print $5}' | cut -d: -f2 | sort -n | uniq
```

### Method 3: Using lsof (if available)
```bash
# Show listening ports
lsof -i -P -n | grep LISTEN
```

## Check Firewall Rules (Read-Only)

### Check firewalld status
```bash
# Check if firewalld is running
systemctl status firewalld

# List current firewall rules (read-only, may need root)
firewall-cmd --list-all 2>/dev/null || echo "Need root or firewalld not active"
```

### Check iptables (read-only)
```bash
# List current iptables rules (read-only)
iptables -L -n 2>/dev/null || echo "Need root to view"
```

### Check ufw status
```bash
# Check ufw status (read-only)
ufw status 2>/dev/null || echo "ufw not installed or need root"
```

## Common Open Ports to Look For

Look for these common web service ports:
- **22** - SSH (definitely open)
- **80** - HTTP
- **443** - HTTPS
- **8080** - Alternative HTTP
- **8443** - Alternative HTTPS
- **8501** - Streamlit default
- **3000** - Node.js apps
- **5000** - Flask default
- **8000** - Django/alternative

## Quick Command to Find Common Web Ports

```bash
# Check for common web ports
for port in 80 443 8080 8443 8501 3000 5000 8000; do
    if netstat -tuln | grep -q ":$port "; then
        echo "Port $port is LISTENING"
    else
        echo "Port $port is NOT listening"
    fi
done
```

## Check What Services Are Running

```bash
# See what services are listening
ss -tulpn | grep LISTEN | awk '{print $1, $5, $7}'
```

This shows: protocol, address:port, and process name.

## Find Available Ports

To find a port that's NOT in use:
```bash
# Check if a specific port is available
netstat -tuln | grep -q ":8080 " && echo "Port 8080 is in use" || echo "Port 8080 is available"
```

## Recommended: Run This Complete Check

```bash
echo "=== Listening Ports ==="
ss -tuln | grep LISTEN | awk '{print $5}' | cut -d: -f2 | sort -n | uniq

echo ""
echo "=== Common Web Ports Status ==="
for port in 80 443 8080 8443 8501 3000 5000 8000; do
    if ss -tuln | grep -q ":$port "; then
        echo "Port $port: IN USE"
    else
        echo "Port $port: AVAILABLE"
    fi
done
```

