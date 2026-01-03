# Find Available Port

Port 8080 is in use. Let's find what's using it and find an available port.

## Check What's Using Port 8080

```bash
# See what process is using port 8080
ss -tulpn | grep 8080
# or
netstat -tulpn | grep 8080
# or
lsof -i :8080
```

## Find an Available Port

Try these common web ports that might be available:

```bash
# Check which ports are available
for port in 8501 3000 5000 8000 9000 8888 5001; do
    if ! ss -tuln | grep -q ":$port "; then
        echo "Port $port is AVAILABLE"
    else
        echo "Port $port is IN USE"
    fi
done
```

## Use an Available Port

Once you find an available port (let's say 8501), run:

```bash
cd ~/SlicerToWebsite/WGSSlicer
source ~/anaconda3/etc/profile.d/conda.sh
conda activate wgs-slicer
streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
```

## Or Use Port 80 (Might Need Root)

Port 80 is open. You could try it, but it might require root:

```bash
# Try port 80 (might need root)
streamlit run WGS_Slicer_v2.py --server.port=80 --server.address=0.0.0.0
```

If you get "Permission denied", you'll need root or use a different port.

