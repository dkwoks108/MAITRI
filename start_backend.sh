#!/bin/bash

# MAITRI Backend Startup Script

echo "=================================="
echo "MAITRI Backend Startup"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/.installed" ]; then
    echo "Installing dependencies..."
    echo "This may take several minutes on first run..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/.installed
    echo "✓ Dependencies installed"
    echo ""
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "✓ .env created"
    echo ""
fi

# Create data directories
mkdir -p data/sessions data/alerts

echo "Starting MAITRI backend server..."
echo "API will be available at: http://localhost:8000"
echo "Documentation at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python main.py
