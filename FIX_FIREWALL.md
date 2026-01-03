# Fix Firewall for Port 1199

Your app is running correctly! The issue is likely the firewall blocking port 1199.

## Quick Fix - Run on BCM Server:

```bash
# Check firewall status
sudo firewall-cmd --list-all
# or
sudo iptables -L -n | grep 1199
# or
sudo ufw status

# If firewall is active, allow port 1199:
sudo firewall-cmd --permanent --add-port=1199/tcp
sudo firewall-cmd --reload

# Or for ufw:
sudo ufw allow 1199/tcp
```

## Test After Opening Firewall:

From your MacBook:
```bash
nc -zv 10.66.4.211 1199
```

If that works, try accessing `http://10.66.4.211:1199` in your browser.

