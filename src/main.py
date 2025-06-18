import os
import asyncio
import base64
from io import BytesIO
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import mss
import mss.tools

# Ensure src directory exists, though FastAPI typically runs from root
# and paths for StaticFiles are relative to where uvicorn is run.
os.makedirs("src/static", exist_ok=True)

app = FastAPI()

# Mount static files directory (for index.html)
# Ensure this path is correct relative to where Uvicorn is started.
# If Uvicorn runs from repo root, 'src/static' is correct.
app.mount("/ui", StaticFiles(directory="src/static", html=True), name="ui")

# --- Screen Capture Logic ---
def capture_screen_region_to_bytes():
    """Captures a predefined region of the screen and returns it as bytes in PNG format."""
    try:
        with mss.mss() as sct:
            monitor = {"top": 100, "left": 100, "width": 500, "height": 400} # Predefined region
            sct_img = sct.grab(monitor)

            # Save to BytesIO buffer instead of a file
            img_byte_arr = BytesIO()
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=img_byte_arr)
            img_byte_arr.seek(0) # Go to the beginning of the BytesIO buffer
            return img_byte_arr.getvalue()
    except Exception as e:
        print(f"An error occurred during screen capture for WebSocket: {e}")
        raise # Re-raise to be handled by the WebSocket endpoint

# Kept for compatibility or direct access if needed, saves to file
def capture_screen_region_for_file():
    """Captures a predefined region of the screen and saves it as screenshot.png."""
    try:
        with mss.mss() as sct:
            monitor = {"top": 100, "left": 100, "width": 500, "height": 400}
            sct_img = sct.grab(monitor)
            output_file = "screenshot.png" # Static filename
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_file)
            return output_file
    except Exception as e:
        print(f"An error occurred during screen capture for file: {e}")
        raise

@app.get("/capture")
async def capture_and_send_image_file():
    """
    Captures a screen region and returns it as an image file.
    Relies on xvfb-run for the environment.
    """
    try:
        image_path = capture_screen_region_for_file()
        if os.path.exists(image_path):
            return FileResponse(image_path, media_type="image/png", filename="screenshot.png")
        else:
            return {"error": "Screenshot file not found after capture attempt."}, 500
    except Exception as e:
        return {"error": f"Failed to capture screen for file: {e}"}, 500

@app.websocket("/ws")
async def websocket_streaming_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"Client connected: {websocket.client}")
    try:
        while True:
            # Capture screen region
            img_bytes = capture_screen_region_to_bytes()

            # Encode image bytes to base64 string
            base64_image = base64.b64encode(img_bytes).decode('utf-8')

            # Send base64 string over WebSocket
            await websocket.send_text(f"data:image/png;base64,{base64_image}")

            await asyncio.sleep(0.1)  # For ~10 FPS

    except WebSocketDisconnect:
        print(f"Client disconnected: {websocket.client}")
    except Exception as e:
        print(f"Error in WebSocket for {websocket.client}: {e}")
        await websocket.close(code=1011, reason=f"Internal server error: {e}")
    finally:
        print(f"Closing WebSocket connection for: {websocket.client}")


if __name__ == "__main__":
    print("Starting Uvicorn server. Run with: xvfb-run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload (optional for dev)")
    # This block is not typically run directly for FastAPI apps with Uvicorn.
    # Uvicorn should be started from the command line as instructed.
    pass
