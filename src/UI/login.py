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
    ["MySQL", "PostgreSQL", "SQLite", "MongoDB", "Redis"],
    placeholder="Search"
)
inputs = {"dbms": dbms}
if dbms == "SQLite":
    sqlite_mode = st.radio("Select mode", ["Local file", "Volume"], index=0)
elif dbms == "MongoDB":
    inputs["mongodb_connection_type"] = st.radio("Select connection type", ["Local/Custom", "SRV-Compatible"], index=0)
    st.caption("""
        `SRV-compatible` connections use the `mongodb+srv` protocol, which simplifies configuration by automatically handling replica sets and load balancing.
        Note that NOT all cloud platforms support SRV, please verify with your provider if they utilize SRV protocol.
    """)

DEFAULT_PORT = (
    3306 if dbms == "MySQL" else
    5432 if dbms == "PostgreSQL" else
    27017 if dbms == "MongoDB" else
    6379
)

# Main form
form = st.form(key="db_connection_form")
form_inputs = {}
# SQLITE
if dbms == "SQLite":
    if sqlite_mode == "Local file":
        form_inputs["file_path"] = form.text_input(
            "📤 Upload SQLite file path (.sqlite or .db)", 
            placeholder="Provide the path to your SQLite database file 📁"
        )
        form.caption("""
            This mode is unavailable if you are accessing the app through `Docker` or public service (`ltang-doht.streamlit.app`).
            If you need to proceed with `Docker`, please switch to the `Volume` option.
        """)
    else:
        files = [f for f in os.listdir("sqlite_dbs") if os.path.isfile(os.path.join("sqlite_dbs", f))]
        files.sort()
        form_inputs["file_name"] = form.selectbox("🏷️ Name of the SQLite database file (.sqlite or .db)", files)
        form.caption("""
            This mode requires you to have your database files (at least one) located inside `sqlite_dbs` folder.
            All the options available here in the select box are the name of all files present inside `sqlite_dbs`.
        """)
# MYSQL, POSTGRESQL, MONGODB, REDIS
else:
    form_inputs.update({
        "user": form.text_input("🧑 User"),
        "password": form.text_input("🔒 Password", type="password")
    })
    if dbms == "MongoDB" and inputs["mongodb_connection_type"] == "SRV-Compatible":
        form_inputs["cluster"] = form.text_input("🕸️ Cluster URL/Hostname/SRV Record")
    else:
        form_inputs.update({
            "host": form.text_input("🖥️ Host"),
            "port": form.number_input("🔌 Port", min_value=0, value=DEFAULT_PORT, step=1)
        })
    form_inputs["database"] = form.text_input("🗄️ Database")
    if dbms == "PostgreSQL":
        form_inputs["db_schema"] = form.text_input("📄 Schema", placeholder="public")
    elif dbms == "MongoDB":
        form_inputs["db_collection"] = form.text_input("📚 Collection")

inputs.update(form_inputs)

submit = form.form_submit_button("Connect")

if submit:
    missing_fields = [key for key, value in inputs.items() if not value]
    if not missing_fields:
        response = requests.post(SETUP_ENDPOINT, json=inputs)
        if response.status_code == 200:
            form_inputs.clear()
            inputs.clear()
            st.switch_page("pages/query.py")
        else:
            st.error(response.json()["detail"])
    else:
        st.error("All fields are required.")