import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Root directory
PROJ_ROOT = Path(__file__).resolve().parents[2]

SRC_DIR = PROJ_ROOT / "src"

API_DIR = SRC_DIR / "API"

DATA_DIR = API_DIR / "data"
LOGS_DIR = API_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True) # Ensure the logs directory exists
