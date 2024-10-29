from invoke import task
import subprocess
import inspect

if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec

@task
def app(ctx) -> None:
    """
    Starts the server script `server.py` and the Streamlit app `app.py` from the `src` directory.
    It handles KeyboardInterrupt to gracefully terminate both processes if the user interrupts the execution.

    Args:
        ctx (Context): The context instance (automatically provided by Invoke).

    Example:
        invoke app  # This will start both the server and the client applications.
    """
    # Start the server
    server = subprocess.Popen(['python', 'src/server.py'])
    # Start the client
    client = subprocess.Popen(['streamlit', 'run', 'src/app.py'])

    try:
        # Wait for both processes to complete, or handle interruption
        server.wait()
        client.wait()
    except KeyboardInterrupt:
        # Ensure both processes are terminated gracefully
        server.terminate()
        client.terminate()

