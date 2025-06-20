from fastapi import Response
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import base64
import subprocess


class OsBasicAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
    
    def check_password(self, username, password):
        system_username = subprocess.check_output("whoami", shell=True).decode().strip()
        if system_username != username:
            return False

        try:
            proc = subprocess.run(
                ['su', '-', username, '-c', 'echo OK'],
                input=password + '\n',
                text=True,
                capture_output=True
            )
            return proc.stdout.strip() == 'OK'
        except Exception:
            return False
    
    async def dispatch(self, request: Request, call_next):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Basic "):
            return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})
        encoded = auth.split(" ")[1]
        decoded = base64.b64decode(encoded).decode("utf-8")
        req_username, req_password = decoded.split(":", 1)
            
        if self.check_password(req_username, req_password) is False:
            return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})
    
        return await call_next(request)
