import requests

import streamlit as st


API_URL = "http://localhost:8000/setup"
def login():
    st.title("Database Connection")

    form = st.form(key="db_connection_form")
    user = form.text_input("User")
    password = form.text_input("Password", type="password")
    host = form.text_input("Host")
    port = form.number_input("Port", value=3306)
    db_name = form.text_input("Database")
    submit = form.form_submit_button("Connect")

    if submit:
        if user and password and host and port and db_name:
            st.session_state["db_info"] = {
                "user": user,
                "password": password,
                "host": host,
                "port": port,
                "database": db_name
            }
            
            response = requests.post(API_URL, json=st.session_state["db_info"])
            if response.status_code == 200:
                st.query_params.page = "executor"
                st.rerun()
                st.stop()
            else:
                st.error(response.json()["detail"])
        else:
            st.error("All fields are required.")