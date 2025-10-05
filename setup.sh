#!/bin/bash

echo "========================================"
echo "   Therapist Companion Setup Script"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.8+ using your package manager"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "macOS: brew install python3"
    exit 1
fi

echo -e "${GREEN}✅ Python found${NC}"
python3 --version

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is not available${NC}"
    echo "Please install pip3 using your package manager"
    exit 1
fi

echo -e "${GREEN}✅ pip found${NC}"

# Create virtual environment
echo
echo "🔧 Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to create virtual environment${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Virtual environment created${NC}"

# Activate virtual environment
echo
echo "🚀 Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Upgrade pip
echo
echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

# Install system dependencies for pygame (Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo
    echo "🔧 Installing system dependencies for pygame..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libportmidi-dev libjpeg-dev
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-devel SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel freetype-devel portmidi-devel libjpeg-turbo-devel
    else
        echo -e "${YELLOW}⚠️  Please install pygame dependencies manually for your Linux distribution${NC}"
    fi
fi

# Install requirements
echo
echo "📦 Installing requirements..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install requirements${NC}"
    echo "Please check requirements.txt and try again"
    exit 1
fi

echo -e "${GREEN}✅ Requirements installed successfully${NC}"

# Create assets directory if it doesn't exist
if [ ! -d "assets" ]; then
    echo
    echo "📁 Creating assets directory..."
    mkdir assets
    echo -e "${YELLOW}⚠️  Please place your therapist expression images in the 'assets' directory${NC}"
    echo "   Required files: neutral.jpeg, smiling.jpeg, concerned.jpeg, etc."
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo
    echo "🔑 Creating .env file..."
    echo "API=YOUR_GOOGLE_GEMINI_API_KEY_HERE" > .env
    echo
    echo -e "${YELLOW}⚠️  IMPORTANT: Please edit .env file and add your Google Gemini API key${NC}"
    echo "   You can get an API key from: https://makersuite.google.com/app/apikey"
    echo
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

echo
echo "========================================"
echo "   Setup Complete! 🎉"
echo "========================================"
echo
echo "To run the application:"
echo "  1. Make sure you've added your API key to .env file"
echo "  2. Activate venv: source venv/bin/activate"
echo "  3. Run: python main.py"
echo
echo "To build executable for distribution:"
echo "  Run: python build_executable.py"
echo
echo "For deployment options, see: DEPLOYMENT.md"
echo