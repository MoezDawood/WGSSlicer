# Fix: Pandas Build Error

The error occurs because pandas is trying to compile from source, but the system GCC (4.8.5) is too old.

## Quick Fix

Install pandas via conda instead of pip (conda has pre-built binaries):

```bash
# Activate the conda environment
conda activate wgs-slicer

# Install pandas via conda (pre-built binary)
conda install pandas -y

# Then install the rest via pip
pip install streamlit paramiko
```

## Alternative: Use Older Pandas Version

If conda install doesn't work, use an older pandas version with pre-built wheels:

```bash
conda activate wgs-slicer
pip install streamlit paramiko "pandas<2.0"
```

## Complete Fix Command

Run this on your BCM server:

```bash
cd ~/SlicerToWebsite/WGSSlicer
conda activate wgs-slicer
conda install pandas -y
pip install streamlit paramiko
```

