# SpectraCtrl

SpectraCtrl is a Python-based web application that allows you to view a Linux desktop screen in real-time through a web browser using WebSockets. It also provides basic (currently non-interactive with the web UI) mouse and keyboard control demonstrations.

## Features

- Real-time screen viewing via web browser using WebSockets.
- Predefined region screen capture.
- Basic demonstration scripts for mouse and keyboard control using `pynput` (not yet integrated into the web UI).
- FastAPI backend server.
- Simple HTML/JavaScript frontend.

## Technology Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Screen Capture:** `mss`
- **Input Control (Demo):** `pynput`
- **Real-time Communication:** WebSockets
- **Frontend:** HTML, CSS, JavaScript
- **Environment Management:** `venv`, `pip`
- **System Dependencies:** `xvfb` (for headless screen capture)

## Setup

### Prerequisites

- A Linux system with an X server environment (Xorg). `xvfb` will be used to create a virtual display.
- `sudo` privileges are required to run the setup script for installing system packages.
- Python 3 and `git`.

### Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory_name>
    ```

2.  **Run the setup script:**
    Make sure the script is executable: `chmod +x setup.sh`
    Then run it:
    ```bash
    ./setup.sh
    ```
    This script will:
    - Update your system's package list.
    - Install `python3-pip` (if not already present) and `xvfb`.
    - Create a Python virtual environment named `.venv`.
    - Install all required Python packages from `requirements.txt` into the virtual environment.

## Running the Application

1.  **Ensure `setup.sh` has been completed successfully.**

2.  **Run the start script:**
    Make sure the script is executable: `chmod +x start.sh`
    Then run it:
    ```bash
    ./start.sh
    ```
    This script will:
    - Activate the Python virtual environment.
    - Start the FastAPI server using Uvicorn, wrapped with `xvfb-run` to provide a virtual display.
    - The server will listen on `http://0.0.0.0:8000`.

3.  **Access the web interface:**
    Open your web browser and navigate to:
    ```
    http://localhost:8000/ui/index.html
    ```
    You should see a live stream of the predefined screen region.

## Stopping the Application

To stop the server, press `Ctrl+C` in the terminal where `start.sh` is running.

## Development Notes
- The `pynput` script `src/input_control.py` is a standalone demonstration and not currently integrated with the web UI for interactive control.
- The screen capture region is predefined in `src/main.py`.
- The application relies on `xvfb` for running in headless environments or environments where direct display access is problematic for capture.
