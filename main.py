from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Query
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query, HTTPException
from includes.utils import list_monitors_and_windows , capture , stream_frames , setup
from includes.middlewares import OsBasicAuthMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends
from fastapi.middleware import Middleware


setup()  # Ensure necessary utilities are set up

app = FastAPI(middleware=[Middleware(OsBasicAuthMiddleware)])

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

@app.get("/fetch")
async def fetch_data():
    return list_monitors_and_windows()

@app.get("/stream")
def stream(id: str = Query(...), type: str = Query(...)):
    if type not in ("monitor", "window"):
        raise HTTPException(status_code=400, detail="type must be 'monitor' or 'window'")
    return StreamingResponse(stream_frames(type, id), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
