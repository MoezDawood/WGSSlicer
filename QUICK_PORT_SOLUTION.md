# Quick Solution: Find and Use Available Port

Port 8080 is in use. Let's find an available port quickly.

## Quick Check for Available Ports

Run this on BCM server:

```bash
# Check common web ports
for port in 8501 3000 5000 8000 9000 8888 5001 8502; do
    if ! ss -tuln | grep -q ":$port "; then
        echo "✅ Port $port is AVAILABLE"
    else
        echo "❌ Port $port is IN USE"
    fi
done
```

## Recommended: Use Port 8501

Port 8501 is the Streamlit default and is likely available. Try it:

```bash
cd ~/SlicerToWebsite/WGSSlicer
source ~/anaconda3/etc/profile.d/conda.sh
conda activate wgs-slicer
streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
```

Then access at: `http://10.66.4.211:8501`

## Alternative Ports to Try

If 8501 doesn't work, try these in order:
- 8501 (Streamlit default)
- 3000 (common web port)
- 5000 (Flask default)
- 8000 (Django default)
- 9000 (alternative)
- 8888 (Jupyter-like)

## Test After Starting

From your MacBook:
```bash
nc -zv 10.66.4.211 8501
```

If it works, access `http://10.66.4.211:8501` in your browser.

