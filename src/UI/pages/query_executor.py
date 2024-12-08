import requests

import streamlit as st


API_URL = "http://localhost:8000/query"
def executor():
    st.markdown("<h1 style=\"font-family:Montserrat; color:#5e6f80; font-size:48px;\">GROQ (Get Rid of Queries)</h1>", unsafe_allow_html=True)

    user_question = st.text_input("Question goes here:")
    status_message = st.empty()

    if st.button("Submit") or (user_question and user_question != st.session_state.get("last_query")):
        st.session_state["last_query"] = user_question
        if user_question:
            status_message.markdown("<p style=\"font-family:Arial; font-size:16px; color:orange;\">⏳ LLM is processing data...</p>", unsafe_allow_html=True)
            response = requests.post(API_URL, json={"input": user_question})
            if response.status_code == 200:
                result = response.json()["output"]
                st.write(result)
                status_message.markdown("<p style=\"font-family:Arial; font-size:16px; color:green;\">✅ Data processed successfully.</p>", unsafe_allow_html=True)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                status_message.markdown("<p style=\"font-family:Arial; font-size:16px; color:red;\">❌ Error occurred while processing data.</p>", unsafe_allow_html=True)
        else:
            st.warning("Please enter a question.")

    if st.button("Disconnect and Return"):
        st.session_state["login_completed"] = False
        st.session_state["db_info"] = {}
        st.rerun()