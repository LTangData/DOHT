import requests

import streamlit as st

from config.ui_config import API_URL


SETUP_ENDPOINT = f"{API_URL}/setup"
def login():
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
    if dbms == "SQLite":
        pass
    else:
        inputs = {
            "dbms": dbms,
            "user": form.text_input("🧑 User"),
            "password": form.text_input("🔒 Password", type="password"),
            "host": form.text_input("🖥️ Host"),
            "port": form.number_input("🔌 Port", min_value=0, value=DEFAULT_PORT, step=1),
            "database": form.text_input("💾 Database")
        }

        if dbms == "PostgreSQL":
            inputs["db_schema"] = form.text_input("🗂️ Schema", placeholder="public")

    submit = form.form_submit_button("Connect")

    if submit:
        missing_fields = [key for key, value in inputs.items() if not value]
        if not missing_fields:
            response = requests.post(SETUP_ENDPOINT, json=inputs)
            if response.status_code == 200:
                st.query_params.update({"page": "query"})
                st.rerun()
                st.stop()
            else:
                st.error(response.json()["detail"])
        else:
            st.error("All fields are required.")