#!/bin/bash

# BCM Server Setup Script for WGS Slicer with Isolated Python Environment
# This script creates a dedicated Python environment for the project

set -e  # Exit on error

echo "🚀 WGS Slicer - BCM Server Setup with Isolated Environment"
echo "=========================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
ENV_DIR="$APP_DIR/venv"
PYTHON_VERSION="3.9"  # Target Python version

echo -e "${GREEN}✓${NC} Running as user: $USERNAME"
echo -e "${GREEN}✓${NC} Home directory: $HOME_DIR"
echo -e "${BLUE}ℹ${NC} Will create isolated Python $PYTHON_VERSION environment"
echo ""

# Check Git
echo "Checking Git installation..."
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed${NC}"
    exit 1
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

# Check for Conda (preferred for HPC clusters)
CONDA_AVAILABLE=false
if command -v conda &> /dev/null; then
    CONDA_AVAILABLE=true
    echo -e "${GREEN}✓${NC} Conda is available"
elif [ -f "$HOME/anaconda3/bin/conda" ] || [ -f "$HOME/miniconda3/bin/conda" ]; then
    CONDA_AVAILABLE=true
    if [ -f "$HOME/anaconda3/bin/conda" ]; then
        export PATH="$HOME/anaconda3/bin:$PATH"
    else
        export PATH="$HOME/miniconda3/bin:$PATH"
    fi
    echo -e "${GREEN}✓${NC} Conda found in home directory"
fi

# Create Python environment
if [ "$CONDA_AVAILABLE" = true ]; then
    echo ""
    echo "Creating Conda environment with Python $PYTHON_VERSION..."
    
    # Remove existing environment if it exists
    if conda env list | grep -q "^wgs-slicer "; then
        echo -e "${YELLOW}⚠${NC} Existing conda environment found. Removing..."
        conda env remove -n wgs-slicer -y
    fi
    
    # Create new conda environment
    conda create -n wgs-slicer python=$PYTHON_VERSION -y
    
    echo -e "${GREEN}✓${NC} Conda environment created"
    echo ""
    echo "Installing dependencies in conda environment..."
    
    # Activate and install
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate wgs-slicer
    
    # Install pip packages
    pip install -r requirements.txt
    
    echo -e "${GREEN}✓${NC} Dependencies installed in conda environment"
    
    # Get the Python path from the environment
    PYTHON_PATH=$(which python)
    STREAMLIT_PATH=$(which streamlit)
    
else
    echo ""
    echo "Conda not available. Using Python venv..."
    
    # Check if Python 3.9+ is available
    PYTHON_CMD=""
    for version in python3.9 python3.10 python3.11 python3.12 python3; do
        if command -v $version &> /dev/null; then
            PYTHON_VER=$($version --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
            MAJOR=$(echo $PYTHON_VER | cut -d'.' -f1)
            MINOR=$(echo $PYTHON_VER | cut -d'.' -f2)
            if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 7 ]; then
                PYTHON_CMD=$version
                echo -e "${GREEN}✓${NC} Found $version ($PYTHON_VER)"
                break
            fi
        fi
    done
    
    if [ -z "$PYTHON_CMD" ]; then
        echo -e "${RED}❌ No suitable Python version (3.7+) found${NC}"
        echo ""
        echo "Options:"
        echo "1. Install Python 3.9+ manually"
        echo "2. Use conda/miniconda (recommended for HPC clusters)"
        echo "3. Contact system administrator"
        exit 1
    fi
    
    # Remove existing venv if it exists
    if [ -d "$ENV_DIR" ]; then
        echo -e "${YELLOW}⚠${NC} Removing existing virtual environment..."
        rm -rf "$ENV_DIR"
    fi
    
    # Create virtual environment
    echo "Creating virtual environment with $PYTHON_CMD..."
    $PYTHON_CMD -m venv "$ENV_DIR"
    
    echo -e "${GREEN}✓${NC} Virtual environment created"
    echo ""
    echo "Installing dependencies in virtual environment..."
    
    # Activate and install
    source "$ENV_DIR/bin/activate"
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo -e "${GREEN}✓${NC} Dependencies installed in virtual environment"
    
    # Get the Python path from the environment
    PYTHON_PATH="$ENV_DIR/bin/python"
    STREAMLIT_PATH="$ENV_DIR/bin/streamlit"
fi

echo ""
echo "=================================="
echo -e "${GREEN}✅ Environment Setup Complete!${NC}"
echo ""
echo "Python environment location:"
if [ "$CONDA_AVAILABLE" = true ]; then
    echo "  Type: Conda environment"
    echo "  Name: wgs-slicer"
    echo "  Python: $PYTHON_PATH"
    echo ""
    echo "To activate: conda activate wgs-slicer"
else
    echo "  Type: Python venv"
    echo "  Location: $ENV_DIR"
    echo "  Python: $PYTHON_PATH"
    echo ""
    echo "To activate: source $ENV_DIR/bin/activate"
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
        if [ "$CONDA_AVAILABLE" = true ]; then
            echo "  conda activate wgs-slicer"
            echo "  cd $APP_DIR"
            echo "  streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0"
        else
            echo "  source $ENV_DIR/bin/activate"
            echo "  cd $APP_DIR"
            echo "  streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0"
        fi
        ;;
    2)
        echo ""
        echo "Setting up systemd service..."
        
        # Create service file
        SERVICE_FILE="/tmp/wgs-slicer.service"
        
        if [ "$CONDA_AVAILABLE" = true ]; then
            # Conda service file
            cat > "$SERVICE_FILE" << EOF
[Unit]
Description=WGS Slicer Streamlit Application
After=network.target

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$APP_DIR
Environment="PATH=$HOME/anaconda3/bin:$HOME/miniconda3/bin:\$PATH"
ExecStart=/bin/bash -c "source \$(conda info --base)/etc/profile.d/conda.sh && conda activate wgs-slicer && streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0"
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
        else
            # Venv service file
            cat > "$SERVICE_FILE" << EOF
[Unit]
Description=WGS Slicer Streamlit Application
After=network.target

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$APP_DIR
Environment="PATH=$ENV_DIR/bin:\$PATH"
ExecStart=$STREAMLIT_PATH run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
        fi
        
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
        
        # Update ecosystem config with correct paths
        if [ "$CONDA_AVAILABLE" = true ]; then
            cat > "$APP_DIR/ecosystem.config.js" << EOF
module.exports = {
  apps: [{
    name: 'wgs-slicer',
    script: 'streamlit',
    args: 'run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0',
    interpreter: '/bin/bash',
    interpreter_args: '-c "source \$(conda info --base)/etc/profile.d/conda.sh && conda activate wgs-slicer &&',
    cwd: '$APP_DIR',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G'
  }]
};
EOF
        else
            cat > "$APP_DIR/ecosystem.config.js" << EOF
module.exports = {
  apps: [{
    name: 'wgs-slicer',
    script: '$STREAMLIT_PATH',
    args: 'run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0',
    cwd: '$APP_DIR',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G'
  }]
};
EOF
        fi
        
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
echo -e "${GREEN}✅ Complete Setup Finished!${NC}"
echo ""
echo "Next steps:"
echo "1. Make sure port 8501 is open: sudo ufw allow 8501/tcp"
echo "2. Test the app: http://$(hostname -I | awk '{print $1}'):8501"
echo "3. See BCM_SERVER_DEPLOYMENT.md for more configuration options"
echo ""

