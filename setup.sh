#!/bin/bash
# Quick setup script for Calectra Dashboard

echo "=================================="
echo "Calectra Dashboard Setup"
echo "=================================="

# Check Python
echo "Checking Python..."
python --version

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv
source venv/Scripts/activate

# Install Python dependencies
echo "Installing Python packages..."
pip install pandas openpyxl

# Process data
echo "Processing data..."
python process_data.py

# Install Node dependencies
echo "Installing Node dependencies..."
cd dashboard
npm install

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "To start the dashboard:"
echo "  cd dashboard"
echo "  npm run dev"
echo ""
