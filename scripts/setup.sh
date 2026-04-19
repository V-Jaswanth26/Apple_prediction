#!/bin/bash

# Apple Stock Prediction - Setup Script
# This script sets up the project structure and dependencies

echo "Setting up Apple Stock Prediction Project..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Create necessary directories if they don't exist
echo "Creating project directories..."
mkdir -p logs
mkdir -p tests/backend
mkdir -p tests/frontend
mkdir -p config
mkdir -p assets/images
mkdir -p assets/icons
mkdir -p assets/fonts

# Set up configuration files
echo "Setting up configuration files..."
if [ ! -f "config/development.json" ]; then
    echo '{"FLASK_ENV": "development", "DEBUG": true}' > config/development.json
fi

if [ ! -f "config/production.json" ]; then
    echo '{"FLASK_ENV": "production", "DEBUG": false}' > config/production.json
fi

# Set up log files
echo "Setting up log files..."
touch logs/app.log
touch logs/error.log
touch logs/access.log

echo "Setup complete!"
echo "To start the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Start backend: cd backend && python api/simple_app.py"
echo "3. Start frontend: cd frontend && npm start"
echo "Or use Docker: docker-compose up --build"
