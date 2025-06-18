import subprocess
import io
import time
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def capture(window_id: str) -> bytes:
    try:
        cmd = f"xwd -silent -id {window_id} | convert xwd:- -resize 50% -quality 50 webp:-"
        return subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        return b''

def stream_frames(window_id: str):
    while True:
        img = capture(window_id)
        if img:
            yield (b"--frame\r\nContent-Type: image/webp\r\n\r\n" + img + b"\r\n")
        time.sleep(0.05)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>WEBP Stream</title></head>
    <body class="bg-black flex items-center justify-center min-h-screen">
      <img id="stream" src="/stream" style="max-width:100%; height:auto; border:1px solid white;" />
    </body>
    </html>
    """

@app.get("/stream")
def stream():
    return StreamingResponse(stream_frames("0x02c00075"), media_type="multipart/x-mixed-replace; boundary=frame")
