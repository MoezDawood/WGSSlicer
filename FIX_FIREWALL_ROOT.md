# Fix Firewall with Root Access

Since you have root access but not sudo, here are your options:

## Option 1: Switch to Root User

```bash
# Switch to root
su -

# Check firewall
firewall-cmd --list-all
# or
ufw status
# or
iptables -L -n | grep 1199

# Open port 1199
firewall-cmd --permanent --add-port=1199/tcp
firewall-cmd --reload

# Or for ufw:
ufw allow 1199/tcp

# Exit root when done
exit
```

## Option 2: Contact System Administrator

If you prefer not to use root, contact BCM IT or your system administrator and ask them to:
- Open port 1199/tcp in the firewall
- Or verify if there are any network restrictions

## Option 3: Check if Firewall is the Issue First

Before using root, let's verify the firewall is actually blocking:

### On BCM Server:
```bash
# Test if app responds locally
curl http://localhost:1199
```

### On Your MacBook:
```bash
# Test if you can reach the server at all
ping 10.66.4.211

# Test if port is blocked
nc -zv 10.66.4.211 1199
```

If `ping` works but `nc` fails, it's definitely the firewall.

## Alternative: Use a Different Port

If you can't modify firewall, you could try using a port that's already open (like 80, 443, or 8080), but you'd need to check with your admin which ports are open.

