import subprocess
import os


def start() -> None:
    cmd = ['poetry', 'run', 'streamlit', 'run', 'lct/auth.py', '--server.port', os.environ.get('STREAMLIT_PORT', 7464)]
    subprocess.run(cmd)

