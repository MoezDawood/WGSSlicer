# Isolated Python Environment Setup

This guide explains how to set up a dedicated Python environment for WGS Slicer with a newer Python version, isolated from the system Python.

## 🎯 Why Use an Isolated Environment?

- ✅ **Newer Python version**: Install Python 3.9+ even if system has Python 3.6
- ✅ **Isolated dependencies**: No conflicts with system packages
- ✅ **Reproducible**: Same environment every time
- ✅ **Clean**: Easy to remove and recreate

## 🚀 Quick Setup

Run the automated setup script:

```bash
cd ~/SlicerToWebsite/WGSSlicer
git pull origin main
bash setup-bcm-server-env.sh
```

This script will:
1. Check for Conda (preferred for HPC clusters)
2. Create a Python 3.9 environment
3. Install all dependencies
4. Set up a service to run automatically

## 📋 Manual Setup Options

### Option 1: Using Conda (Recommended for HPC Clusters)

Conda is often available on HPC clusters and makes it easy to install different Python versions.

```bash
# Check if conda is available
conda --version

# If not in PATH, try:
source ~/anaconda3/etc/profile.d/conda.sh
# or
source ~/miniconda3/etc/profile.d/conda.sh

# Create environment with Python 3.9
conda create -n wgs-slicer python=3.9 -y

# Activate environment
conda activate wgs-slicer

# Install dependencies
cd ~/SlicerToWebsite/WGSSlicer
pip install -r requirements.txt

# Test
streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
```

**To use conda environment in systemd service:**

```ini
[Service]
ExecStart=/bin/bash -c "source $(conda info --base)/etc/profile.d/conda.sh && conda activate wgs-slicer && streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0"
```

### Option 2: Using Python venv

If conda is not available, use Python's built-in venv:

```bash
# Check for Python 3.9+
python3.9 --version
# or
python3.10 --version

# If available, create venv
cd ~/SlicerToWebsite/WGSSlicer
python3.9 -m venv venv

# Activate environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Test
streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
```

**To use venv in systemd service:**

```ini
[Service]
Environment="PATH=/storage/lupski/home/mdawood/SlicerToWebsite/WGSSlicer/venv/bin:$PATH"
ExecStart=/storage/lupski/home/mdawood/SlicerToWebsite/WGSSlicer/venv/bin/streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
```

### Option 3: Install Python 3.9+ via Conda/Miniconda

If your system only has Python 3.6, install Miniconda first:

```bash
# Download Miniconda
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install (follow prompts)
bash Miniconda3-latest-Linux-x86_64.sh

# Add to PATH
source ~/.bashrc

# Now use Option 1 above
```

## 🔧 Using the Environment

### Activate Environment

**Conda:**
```bash
conda activate wgs-slicer
```

**Venv:**
```bash
source ~/SlicerToWebsite/WGSSlicer/venv/bin/activate
```

### Run the App

```bash
cd ~/SlicerToWebsite/WGSSlicer
streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
```

### Deactivate Environment

```bash
# Conda
conda deactivate

# Venv
deactivate
```

## 🔄 Updating the Environment

### Update Dependencies

```bash
# Activate environment first
conda activate wgs-slicer  # or source venv/bin/activate

# Update from requirements.txt
pip install --upgrade -r requirements.txt
```

### Recreate Environment

If something goes wrong, you can easily recreate:

**Conda:**
```bash
conda env remove -n wgs-slicer
conda create -n wgs-slicer python=3.9 -y
conda activate wgs-slicer
pip install -r requirements.txt
```

**Venv:**
```bash
rm -rf ~/SlicerToWebsite/WGSSlicer/venv
python3.9 -m venv ~/SlicerToWebsite/WGSSlicer/venv
source ~/SlicerToWebsite/WGSSlicer/venv/bin/activate
pip install -r requirements.txt
```

## 📝 Environment Information

### Check Python Version

```bash
# In activated environment
python --version
```

### List Installed Packages

```bash
# In activated environment
pip list
```

### Export Environment

**Conda:**
```bash
conda env export > environment.yml
```

**Venv:**
```bash
pip freeze > requirements-frozen.txt
```

## 🐛 Troubleshooting

### "conda: command not found"

```bash
# Try to find conda
find ~ -name conda 2>/dev/null

# If found, add to PATH
export PATH="$HOME/anaconda3/bin:$PATH"
# or
export PATH="$HOME/miniconda3/bin:$PATH"

# Add to ~/.bashrc for persistence
echo 'export PATH="$HOME/anaconda3/bin:$PATH"' >> ~/.bashrc
```

### "python3.9: command not found"

- Install Python 3.9+ via conda (recommended)
- Or ask system administrator to install Python 3.9+
- Or use the system Python 3.6 with `requirements-py36.txt`

### Environment not activating in systemd

Make sure the service file uses the full path or proper activation command. See the service file examples above.

### Permission errors

```bash
# Make sure you own the environment directory
chown -R $USER ~/SlicerToWebsite/WGSSlicer/venv
# or for conda
chown -R $USER ~/.conda/envs/wgs-slicer
```

## ✅ Benefits Summary

- ✅ **Isolated**: No conflicts with system Python
- ✅ **Modern**: Python 3.9+ with latest features
- ✅ **Reproducible**: Same setup every time
- ✅ **Portable**: Easy to move or recreate
- ✅ **Clean**: Easy to remove when done

