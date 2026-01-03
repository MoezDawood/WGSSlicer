#!/bin/bash

# Deploy WGS Slicer on BCM Server
# Run this script on a BCM server that has access to 10.66.4.211

echo "🚀 Deploying WGS Slicer on BCM Server..."
echo ""

# Check if we're in the right directory
if [ ! -f "WGS_Slicer_v2.py" ]; then
    echo "📦 Cloning repository..."
    if [ -d "WGSSlicer" ]; then
        cd WGSSlicer
        echo "🔄 Updating existing repository..."
        git pull
    else
        git clone https://github.com/MoezDawood/WGSSlicer.git
        cd WGSSlicer
    fi
else
    echo "✅ Already in WGSSlicer directory"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✅ Dependencies installed successfully!"
echo ""
echo "🚀 Starting Streamlit app..."
echo "   The app will be available at: http://$(hostname -I | awk '{print $1}'):8501"
echo "   Or: http://localhost:8501"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""

# Run the app
streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0

