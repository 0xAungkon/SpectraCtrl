#!/bin/bash

echo "Starting the application..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment '.venv' not found."
    echo "Please run ./setup.sh first to create the environment and install dependencies."
    exit 1
fi

# Activate virtual environment
# Note: 'source' might behave differently depending on how the script is run.
# For direct execution (./start.sh), this works to bring venv paths into current shell.
# If this script were sourced itself, then the calling shell would be affected.
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if activation was successful (e.g., by checking if a venv command is available)
if ! command -v uvicorn &> /dev/null; then
    echo "Error: Failed to activate virtual environment, or uvicorn is not installed correctly in .venv."
    echo "Please ensure ./setup.sh ran successfully and try sourcing manually: 'source .venv/bin/activate'"
    exit 1
fi
echo "Virtual environment activated."

# Launch the FastAPI application with Uvicorn, wrapped in xvfb-run
echo "Launching FastAPI application with Uvicorn on http://0.0.0.0:8000..."
echo "Press CTRL+C to stop the server."

xvfb-run uvicorn src.main:app --host 0.0.0.0 --port 8000

# Check Uvicorn exit status (though usually it's killed with CTRL+C)
if [ $? -ne 0 ]; then
    echo "Error: Uvicorn server failed to start or exited with an error."
    # Deactivate might be useful here if we had more cleanup
    # deactivate
    exit 1
fi

echo "Application stopped."
# Deactivate might be useful here if we had more cleanup
# deactivate
exit 0
