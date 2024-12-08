import subprocess

from invoke import task
import inspect


if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec

FASTAPI_SERVER = "src/API/server.py"
STREAMLIT_UI = "src/UI/app.py"

@task
def app(ctx):
    fastapi = subprocess.Popen(["python", FASTAPI_SERVER])
    streamlit = subprocess.Popen(["streamlit", "run", STREAMLIT_UI])

    fastapi.wait()
    streamlit.wait()