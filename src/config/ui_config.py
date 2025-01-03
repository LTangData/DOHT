import os
from pathlib import Path

from dotenv import load_dotenv


# Environment variables
load_dotenv()
API_URL = os.getenv("API_URL")

# Root directory
PROJ_ROOT = Path(__file__).resolve().parents[2]

SRC_DIR = PROJ_ROOT / "src"

UI_DIR = SRC_DIR / "UI"

STYLES_DIR = UI_DIR / "styles"
