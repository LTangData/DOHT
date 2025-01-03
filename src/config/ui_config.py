from pathlib import Path

import streamlit as st


# Environment variables
if "API_URL" in st.secrets:  # Check if running in Streamlit Cloud
    API_URL = st.secrets["API_URL"]
else:  # Fallback for local development
    API_URL = "http://localhost:8000"

# Root directory
PROJ_ROOT = Path(__file__).resolve().parents[2]

SRC_DIR = PROJ_ROOT / "src"

UI_DIR = SRC_DIR / "UI"

STYLES_DIR = UI_DIR / "styles"
