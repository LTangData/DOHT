import os
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables for OpenAI and database credentials
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]

SRC_DIR = PROJ_ROOT / "src"
LOGS_DIR = PROJ_ROOT / "logs"

DATA_DIR = SRC_DIR / "data"
STYLES_DIR = SRC_DIR / "styles"

# Ensure the logs directory exists
LOGS_DIR.mkdir(parents=True, exist_ok=True)