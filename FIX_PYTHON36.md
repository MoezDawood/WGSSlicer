# Fix for Python 3.6 Compatibility Issue

Your BCM server has Python 3.6.8, but newer versions of Streamlit require Python 3.7+.

## Solution Options

### Option 1: Use Older Streamlit Version (Quick Fix)

The setup script detected Python 3.6. Use the Python 3.6 compatible requirements:

```bash
cd ~/SlicerToWebsite/WGSSlicer
pip3 install --user -r requirements-py36.txt
```

This installs Streamlit 0.84.2 which works with Python 3.6.

### Option 2: Use Python 3.7+ (Recommended)

Check if Python 3.7+ is available:

```bash
# Check for Python 3.7
python3.7 --version
# Or
python3.8 --version
# Or
python3.9 --version
```

If available, use it:

```bash
# Install with Python 3.7+
python3.7 -m pip install --user -r requirements.txt

# Run with Python 3.7+
python3.7 -m streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
```

### Option 3: Install Python 3.7+ (If you have sudo)

```bash
# On CentOS/RHEL
sudo yum install python37 python37-pip

# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.7 python3.7-pip

# Then use it
python3.7 -m pip install --user -r requirements.txt
```

### Option 4: Use Conda/Miniconda (Recommended for BCM servers)

Many BCM servers have conda available:

```bash
# Check if conda is available
which conda

# If available, create a new environment
conda create -n wgs-slicer python=3.9
conda activate wgs-slicer
pip install -r requirements.txt
```

## Quick Fix Command

Run this on your BCM server right now:

```bash
cd ~/SlicerToWebsite/WGSSlicer
pip3 install --user streamlit==0.84.2 paramiko pandas
```

Then test:

```bash
streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
```

