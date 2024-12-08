import os
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables for OpenAI and database credentials
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]

LOGS_DIR = PROJ_ROOT / "logs"
SRC_DIR = PROJ_ROOT / "src"

ASSETS_DIR = SRC_DIR / "assets"
API_DIR = SRC_DIR / "API"
UI_DIR = SRC_DIR / "UI"

DATA_DIR = API_DIR / "data"
STYLES_DIR = UI_DIR / "styles"

# Ensure the logs directory exists
LOGS_DIR.mkdir(parents=True, exist_ok=True)