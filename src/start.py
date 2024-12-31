import os
import sys
import subprocess
import signal


FASTAPI = "src/API/server.py"
STREAMLIT = "src/UI/app.py"

processes = []

def shutdown():
    """Terminate all subprocesses."""
    print("Shutting down...")
    for process in processes:
        process.terminate()
    sys.exit(0)

def start_backend():
    """Start the backend"""
    subprocess.run([sys.executable, FASTAPI])

def start_frontend():
    """Start the frontend"""
    # Default to 8000 if PORT is not set. This is needed for Heroku deployment
    subprocess.run(["streamlit", "run", STREAMLIT, f"--server.port={int(os.getenv("PORT", 8501))}"])

def main():
    """Start the full application"""
    try:
        backend = subprocess.Popen([sys.executable, FASTAPI])
        frontend = subprocess.Popen(["streamlit", "run", STREAMLIT])
        processes.extend([backend, frontend])
    except Exception as e:
        print(e)
        sys.exit(1)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    backend.wait()
    frontend.wait()

if __name__ == "__main__":
    main()
