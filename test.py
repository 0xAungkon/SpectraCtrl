import subprocess

def check_password(username, password):
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
        
print(check_password('amd','7530'))