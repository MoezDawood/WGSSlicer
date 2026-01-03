# Simple Test Commands

## Test Imports (without special characters)

```bash
python -c "import streamlit; import paramiko; import pandas; import pyarrow; print('All packages work')"
```

Or test individually:
```bash
python -c "import streamlit; print('streamlit OK')"
python -c "import paramiko; print('paramiko OK')"
python -c "import pandas; print('pandas OK')"
python -c "import pyarrow; print('pyarrow OK')"
```

## Run the App

```bash
cd ~/SlicerToWebsite/WGSSlicer
streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
```

