import os
from pathlib import Path


# Environment variables
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Root directory
PROJ_ROOT = Path(__file__).resolve().parents[2]

SRC_DIR = PROJ_ROOT / "src"

UI_DIR = SRC_DIR / "UI"

STYLES_DIR = UI_DIR / "styles"
