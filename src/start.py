import sys
import subprocess
import signal


FASTAPI = "src/API/server.py"
STREAMLIT = "src/UI/login.py"

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
    subprocess.run(["streamlit", "run", STREAMLIT])

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
