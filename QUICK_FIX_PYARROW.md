# Quick Fix for PyArrow Error

The error occurs because pyarrow is trying to compile from source but `cmake` is not installed.

## ✅ Quick Fix - Run This Now:

```bash
# Make sure you're in the conda environment
conda activate wgs-slicer

# Install pyarrow via conda (pre-built binary, no compilation needed)
conda install pyarrow -y

# Then install streamlit and paramiko
pip install streamlit paramiko
```

That's it! PyArrow will be installed as a pre-built binary, so no compilation is needed.

## Why This Works:

- Conda provides pre-built pyarrow binaries (no cmake needed)
- Avoids compilation issues
- Much faster installation
- More reliable on older systems

## Test It:

```bash
conda activate wgs-slicer
python -c "import pyarrow; print('PyArrow version:', pyarrow.__version__)"
```

If that works, you're all set!

