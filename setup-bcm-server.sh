#!/bin/bash

# BCM Server Setup Script for WGS Slicer
# Run this script on your BCM server to set up the application

set -e  # Exit on error

echo "🚀 WGS Slicer - BCM Server Setup"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo -e "${RED}❌ Please do not run this script as root${NC}"
   echo "Run as your regular user. Sudo will be prompted when needed."
   exit 1
fi

USERNAME=$(whoami)
HOME_DIR="$HOME"
APP_DIR="$HOME_DIR/WGSSlicer"

echo -e "${GREEN}✓${NC} Running as user: $USERNAME"
echo -e "${GREEN}✓${NC} Home directory: $HOME_DIR"
echo ""

# Check Python
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.7 or higher first"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓${NC} Python version: $PYTHON_VERSION"
echo ""

# Check Git
echo "Checking Git installation..."
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}⚠${NC} Git is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y git
fi
echo -e "${GREEN}✓${NC} Git is installed"
echo ""

# Clone or update repository
if [ -d "$APP_DIR" ]; then
    echo "Repository already exists. Updating..."
    cd "$APP_DIR"
    git pull origin main
    echo -e "${GREEN}✓${NC} Repository updated"
else
    echo "Cloning repository..."
    cd "$HOME_DIR"
    git clone https://github.com/MoezDawood/WGSSlicer.git
    cd "$APP_DIR"
    echo -e "${GREEN}✓${NC} Repository cloned"
fi
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --user -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Dependencies installed"
else
    echo -e "${YELLOW}⚠${NC} Some dependencies may have failed. Trying with sudo..."
    sudo pip3 install -r requirements.txt
fi
echo ""

# Test the application
echo "Testing application..."
if python3 -c "import streamlit; import paramiko; import pandas" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} All required packages are installed"
else
    echo -e "${RED}❌ Some packages are missing. Please check the installation${NC}"
    exit 1
fi
echo ""

# Ask about deployment method
echo "Choose deployment method:"
echo "1) Run manually (for testing)"
echo "2) Set up systemd service (recommended for production)"
echo "3) Set up PM2 (alternative process manager)"
echo "4) Just install, I'll set up later"
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}✓${NC} Setup complete!"
        echo ""
        echo "To run the app manually:"
        echo "  cd $APP_DIR"
        echo "  streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0"
        ;;
    2)
        echo ""
        echo "Setting up systemd service..."
        
        # Create service file
        SERVICE_FILE="/tmp/wgs-slicer.service"
        cat > "$SERVICE_FILE" << EOF
[Unit]
Description=WGS Slicer Streamlit Application
After=network.target

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$APP_DIR
Environment="PATH=/usr/bin:/usr/local/bin:$HOME_DIR/.local/bin"
ExecStart=$(which streamlit) run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
        
        # Copy to systemd directory
        sudo cp "$SERVICE_FILE" /etc/systemd/system/wgs-slicer.service
        sudo systemctl daemon-reload
        sudo systemctl enable wgs-slicer
        sudo systemctl start wgs-slicer
        
        echo -e "${GREEN}✓${NC} Systemd service created and started"
        echo ""
        echo "Service commands:"
        echo "  sudo systemctl status wgs-slicer  # Check status"
        echo "  sudo systemctl restart wgs-slicer  # Restart"
        echo "  sudo journalctl -u wgs-slicer -f  # View logs"
        ;;
    3)
        echo ""
        echo "Setting up PM2..."
        
        # Check if Node.js is installed
        if ! command -v node &> /dev/null; then
            echo "Installing Node.js..."
            curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
            sudo apt-get install -y nodejs
        fi
        
        # Install PM2
        if ! command -v pm2 &> /dev/null; then
            sudo npm install -g pm2
        fi
        
        # Create logs directory
        mkdir -p "$APP_DIR/logs"
        
        # Start with PM2
        cd "$APP_DIR"
        pm2 start ecosystem.config.js
        pm2 save
        pm2 startup
        
        echo -e "${GREEN}✓${NC} PM2 setup complete"
        echo ""
        echo "PM2 commands:"
        echo "  pm2 status  # Check status"
        echo "  pm2 logs wgs-slicer  # View logs"
        echo "  pm2 restart wgs-slicer  # Restart"
        ;;
    4)
        echo ""
        echo -e "${GREEN}✓${NC} Setup complete!"
        echo "You can set up the service later using the instructions in BCM_SERVER_DEPLOYMENT.md"
        ;;
    *)
        echo -e "${YELLOW}⚠${NC} Invalid choice. Setup complete, but no service configured."
        ;;
esac

echo ""
echo "=================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Make sure port 8501 is open: sudo ufw allow 8501/tcp"
echo "2. Test the app: http://$(hostname -I | awk '{print $1}'):8501"
echo "3. See BCM_SERVER_DEPLOYMENT.md for more configuration options"
echo ""

