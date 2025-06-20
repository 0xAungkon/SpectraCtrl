import shutil
import subprocess
import re
import json
import time 
import mss
import io
from PIL import Image
from loguru import logger

def setup():
    if shutil.which("xwd") is None:
        subprocess.run(["sudo", "apt-get", "update"])
        subprocess.run(["sudo", "apt-get", "install", "-y", "x11-utils"])
        subprocess.run(["sudo", "apt-get", "install", "-y", "x11-apps"])
    
    if shutil.which("xwd") is None:
        raise RuntimeError("xwd command not found. Please install x11-utils and x11-apps.")

def get_monitor_info():
    monitors_raw = subprocess.check_output(["xrandr", "--listmonitors"], text=True).strip().split('\n')[1:]
    monitors = []
    for line in monitors_raw:
        parts = re.split(r'\s+', line.strip())
        monitor_id = parts[1].lstrip('+*')
        width_px = int(parts[2].split('+')[0].split('x')[0].split('/')[0])
        height_px = int(parts[2].split('+')[0].split('x')[1].split('/')[0])
        aspect_ratio = round(width_px / height_px, 2) if height_px else None
        monitors.append({
            "monitor_id": monitor_id,
            "resolution": f"{width_px}x{height_px}",
            "aspect_ratio": aspect_ratio,
        })
    return monitors

def get_window_info():
    windows_raw = subprocess.check_output(["wmctrl", "-lGx"], text=True).strip().split('\n')
    windows = []
    for line in windows_raw:
        parts = line.split(None, 9)
        if len(parts) < 10:
            continue
        window_id = parts[0]
        x, y, w, h = map(int, parts[2:6])
        wm_class = parts[6]  # e.g. 'google-chrome.Google-chrome'

        
        window_name =  ' '.join(parts[8:]).strip()
        aspect_ratio = round(w / h, 2) if h else None
        app_name = wm_class.split('.')[0] if wm_class else None
        windows.append({
            "window_id": window_id,
            "window_name": window_name,
            "application": app_name,
            "resolution": f"{w}x{h}",
            "aspect_ratio": aspect_ratio,
        })
    return windows

def list_monitors_and_windows():
    monitors = get_monitor_info()
    windows = get_window_info()
    return {"monitors": monitors, "windows": windows}


def get_monitor_geometry(name):
    output = subprocess.check_output(['xrandr']).decode()
    match = re.search(rf'^{name} connected.*?(\d+)x(\d+)\+(\d+)\+(\d+)', output, re.MULTILINE)
    if match:
        width, height, x, y = map(int, match.groups())
        return {"width": width, "height": height, "x": x, "y": y}
    return None

def capture(mtype: str, mid: str, monitor_info: dict) -> bytes:
    response = b''
    if mtype == "monitor":
        with mss.mss() as sct:
            monitor = {"top": monitor_info['y'], "left": monitor_info['x'], "width": monitor_info['width'], "height": monitor_info['height']}
            img = sct.grab(monitor)
            buffer = io.BytesIO()
            png_bytes = mss.tools.to_png(img.rgb, img.size)
            buffer.write(png_bytes)
            response = buffer.getvalue()
    elif mtype == "window":
        cmd = f"xwd -silent -id {mid} | convert xwd:- -quality 50 webp:-"
        response= subprocess.check_output(cmd, shell=True)
    else:
        raise ValueError("Invalid type")
    return response

def stream_frames(mtype: str, mid: str):
    if mtype not in ["monitor", "window"]:
        raise ValueError("Invalid type, must be 'monitor' or 'window'")
    monitor_info=False
    if mtype == "monitor":
        monitor_info = get_monitor_geometry(mid)
        if not monitor_info:
            raise ValueError(f"Monitor {mid} not found")
    prev_img=None
    while True:
        try:
            img = capture(mtype, mid, monitor_info)
            if img != prev_img:
                prev_img = img
            else:
                pass
                logger.info("No change in image, skipping frame")
            
            yield (b"--frame\r\nContent-Type: image/webp\r\n\r\n" + img + b"\r\n")
        except subprocess.CalledProcessError:
            break
