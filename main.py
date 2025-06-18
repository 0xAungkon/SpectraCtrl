from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Query
from includes.utils import list_monitors_and_windows
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

@app.get("/fetch")
async def fetch_data():
    return list_monitors_and_windows()

@app.post("/share")
async def share(type: str = Query(..., description="Type of data to share (e.g., 'monitor', 'window')"), id: str = Query(..., description="ID of the monitor or window to share")):
    return True

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
