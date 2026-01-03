# Fix: Conda Command Not Found

Conda is installed but not in your PATH. Here's how to fix it:

## Quick Fix - Run These Commands:

```bash
# Source conda (add it to PATH)
source ~/anaconda3/etc/profile.d/conda.sh

# Now activate the environment
conda activate wgs-slicer

# Install pyarrow via conda (pre-built binary)
conda install pyarrow -y

# Install streamlit and paramiko
pip install streamlit paramiko
```

## Make It Permanent (Optional):

Add conda to your PATH permanently by adding this to your `~/.bashrc`:

```bash
echo 'source ~/anaconda3/etc/profile.d/conda.sh' >> ~/.bashrc
source ~/.bashrc
```

Then you can use `conda activate wgs-slicer` directly in new sessions.

## Test After Installation:

```bash
conda activate wgs-slicer
python -c "import streamlit; import paramiko; import pandas; import pyarrow; print('✅ All packages work!')"
```

