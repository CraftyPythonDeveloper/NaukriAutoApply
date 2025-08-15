#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print error and wait for user input
error_exit() {
    echo "Error: $1"
    read -p "Press Enter to exit..."
    exit 1
}

# Check if Python is installed
if ! command_exists python3; then
    error_exit "Python is not installed. Please install Python 3.9 or higher."
fi

# Check Python version
python3 -c "import sys; sys.exit(0) if sys.version_info >= (3, 9) else sys.exit(1)" >/dev/null 2>&1
if [ $? -ne 0 ]; then
    error_exit "Python version 3.9 or higher is required."
fi

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "Virtual environment found, activating..."
    source .venv/bin/activate || error_exit "Failed to activate virtual environment."
else
    echo "Creating new virtual environment..."
    python3 -m venv .venv || error_exit "Failed to create virtual environment."
    
    echo "Activating virtual environment..."
    source .venv/bin/activate || error_exit "Failed to activate virtual environment."
    
    echo "Installing dependencies..."
    python -m pip install -r requirements.txt || error_exit "Failed to install dependencies."
fi

# Check for required files
if [ ! -f ".env" ]; then
    error_exit ".env file not found. Please create .env file with GEMINI_API_KEY."
fi

if [ ! -f "resume_data.txt" ]; then
    error_exit "resume_data.txt not found. Please add your resume data."
fi

# Run the automation script
echo "Starting Naukri Automation..."
python naukri_automation.py
if [ $? -ne 0 ]; then
    error_exit "An error occurred while running the script."
fi

# Deactivate virtual environment
deactivate

echo "Script completed successfully."
read -p "Press Enter to exit..."
exit 0
