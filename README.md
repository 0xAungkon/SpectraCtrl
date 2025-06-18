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
