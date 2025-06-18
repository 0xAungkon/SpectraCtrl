import subprocess
import re
import json

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
        
        window_name = parts[9].strip()
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
