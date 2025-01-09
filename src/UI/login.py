import requests

import streamlit as st

from config.ui_config import API_URL
from config.ui_config import STYLES_DIR
from UI.style_loader import load_page_config, load_css


load_page_config()        
load_css(f"{STYLES_DIR}/base.css", f"{STYLES_DIR}/login.css")

SETUP_ENDPOINT = f"{API_URL}/setup"

st.title("Database Connection 🔗")

dbms = st.selectbox(
    "⚙️ Database management system",
    ["MySQL", "PostgreSQL", "SQLite", "MongoDB", "Redis"],
    placeholder="Search"
)

DEFAULT_PORT = (
    3306 if dbms == "MySQL" else
    5432 if dbms == "PostgreSQL" else
    27017 if dbms == "MongoDB" else
    6379
)

form = st.form(key="db_connection_form")
inputs = {"dbms": dbms}
if dbms == "SQLite":
    sqlite_mode = form.radio("Select mode", ["Local file", "Volume"], index=0)
    if sqlite_mode == "Local file":
        inputs["file_path"] = form.text_input(
            "📤 Upload SQLite file (.sqlite or .db)", 
            placeholder="Provide the path to your SQLite database file 📁"
        )
    else:
        inputs["file_path"] = "Volume selected. Ensure proper configuration."
else:
    inputs.update({
        "user": form.text_input("🧑 User"),
        "password": form.text_input("🔒 Password", type="password"),
        "host": form.text_input("🖥️ Host"),
        "port": form.number_input("🔌 Port", min_value=0, value=DEFAULT_PORT, step=1),
        "database": form.text_input("🗄️ Database")
    })

    if dbms == "PostgreSQL":
        inputs["db_schema"] = form.text_input("📄 Schema", placeholder="public")

submit = form.form_submit_button("Connect")

if submit:
    missing_fields = [key for key, value in inputs.items() if not value]
    if not missing_fields:
        response = requests.post(SETUP_ENDPOINT, json=inputs)
        if response.status_code == 200:
            inputs.clear()
            st.switch_page("pages/query.py")
        else:
            st.error(response.json()["detail"])
    else:
        st.error("All fields are required.")