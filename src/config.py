import os
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables for OpenAI and database credentials
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]

SRC_DIR = PROJ_ROOT / "src"
LOGS_DIR = PROJ_ROOT / "logs"

DATA_DIR = SRC_DIR / "data"
STYLES_DIR = SRC_DIR / "styles"

# Ensure the logs directory exists
LOGS_DIR.mkdir(parents=True, exist_ok=True)