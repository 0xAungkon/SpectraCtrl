#!/bin/bash

echo "Starting the setup process..."
echo "This script requires sudo privileges for installing system packages."

# Update package list
echo "Updating package list..."
if ! sudo apt-get update; then
    echo "Error: Failed to update package list. Please check your internet connection and sudo privileges."
    exit 1
fi

# Install pip and xvfb
echo "Installing python3-pip and xvfb..."
if ! sudo apt-get install -y python3-pip xvfb; then
    echo "Error: Failed to install python3-pip or xvfb. Please check sudo privileges and package availability."
    exit 1
fi
echo "python3-pip and xvfb installed successfully."

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not found in PATH. Please install Python 3."
    exit 1
fi
echo "Python 3 found."

# Create Python virtual environment
echo "Creating Python virtual environment '.venv'..."
if ! python3 -m venv .venv; then
    echo "Error: Failed to create Python virtual environment. Check Python 3 installation and permissions."
    exit 1
fi
echo "Virtual environment '.venv' created successfully."

# Install Python packages from requirements.txt
echo "Installing Python packages from requirements.txt into '.venv'..."
if ! .venv/bin/pip install -r requirements.txt; then
    echo "Error: Failed to install packages from requirements.txt. Check the file and your internet connection."
    # Consider removing .venv if install fails to allow a clean retry
    # rm -rf .venv
    exit 1
fi
echo "Python packages installed successfully."

echo ""
echo "---------------------------------------------------------------------"
echo "Setup completed successfully!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "After activating the environment, you can run the application using:"
echo "  ./start.sh  (You might need to create start.sh first or run uvicorn directly)"
echo "---------------------------------------------------------------------"

exit 0
