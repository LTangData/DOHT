import os
import requests

import streamlit as st

from config.ui_config import API_URL
from config.ui_config import STYLES_DIR
from UI.style_loader import load_page_config, load_css


load_page_config()        
load_css(f"{STYLES_DIR}/base.css", f"{STYLES_DIR}/login.css")

SETUP_ENDPOINT = f"{API_URL}/setup"

st.title("Database Connection 🔗")

# DBMS Selection
dbms = st.selectbox(
    "⚙️ Database management system",
    ["MySQL", "PostgreSQL", "SQLite"],
    placeholder="Search"
)
if dbms == "SQLite":
    sqlite_mode = st.radio("Select mode", ["Local file", "Volume"], index=0)


inputs = {"dbms": dbms}

DEFAULT_PORT = (
    3306 if dbms == "MySQL" else
    5432
)

# Main form
form = st.form(key="db_connection_form")
# SQLITE
if dbms == "SQLite":
    if sqlite_mode == "Local file":
        inputs["file_path"] = form.text_input(
            "📤 Upload SQLite file path (.sqlite or .db)", 
            placeholder="Provide the path to your SQLite database file 📁"
        )
        form.caption("""
            This mode is unavailable if you are accessing the app through `Docker` or public service (`ltang-doht.streamlit.app`).
            If you need to proceed with `Docker`, please switch to the `Volume` mode.
        """)
    else:
        files = [f for f in os.listdir("sqlite_dbs") if os.path.isfile(os.path.join("sqlite_dbs", f))]
        files.sort()
        inputs["file_name"] = form.selectbox("🏷️ Name of the SQLite database file (.sqlite or .db)", files)
        form.caption("""
            This mode is unavailable if you are accessing the app through public service (`ltang-doht.streamlit.app`).
            This mode requires you to have your database files (at least one) inside `sqlite_dbs` folder, which you will need to create manually.
            All the options available here in the select box are the name of all files present inside `sqlite_dbs`.
        """)
# MYSQL, POSTGRESQL
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