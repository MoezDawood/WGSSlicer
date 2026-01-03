#!/bin/bash

# SSH Tunnel Script for WGS Slicer Access
# Run this script to create an SSH tunnel and open the app in your browser

echo "🔗 Creating SSH tunnel to WGS Slicer..."
echo ""
echo "This will:"
echo "  1. Create an SSH tunnel to the BCM server"
echo "  2. Forward port 8501 to access the app"
echo "  3. Open the app in your browser"
echo ""
echo "Keep this terminal open while using the app!"
echo "Press Ctrl+C to close the tunnel when done."
echo ""

# Check if port 8501 is already in use locally
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port 8501 is already in use on your computer."
    echo "Using port 8502 instead..."
    LOCAL_PORT=8502
    URL="http://localhost:8502"
else
    LOCAL_PORT=8501
    URL="http://localhost:8501"
fi

# Create SSH tunnel
echo "Creating tunnel on port $LOCAL_PORT..."
ssh -L ${LOCAL_PORT}:localhost:8501 mdawood@10.66.4.211 &
SSH_PID=$!

# Wait a moment for tunnel to establish
sleep 2

# Check if tunnel is working
if ps -p $SSH_PID > /dev/null; then
    echo "✅ SSH tunnel created successfully!"
    echo ""
    echo "🌐 Opening app in your browser..."
    echo "   URL: $URL"
    echo ""
    echo "📝 Keep this terminal open while using the app!"
    echo "   Press Ctrl+C to close the tunnel when done."
    echo ""
    
    # Open browser (works on macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$URL" 2>/dev/null || echo "Please open $URL in your browser"
    else
        echo "Please open $URL in your browser"
    fi
    
    # Wait for user to press Ctrl+C
    wait $SSH_PID
else
    echo "❌ Failed to create SSH tunnel"
    echo "Make sure you can SSH to the BCM server"
    exit 1
fi

