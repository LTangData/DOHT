import requests

import streamlit as st

from config.ui_config import API_URL
from config.ui_config import STYLES_DIR
from UI.style_loader import load_page_config, load_css


load_page_config()        
load_css(f"{STYLES_DIR}/base.css", f"{STYLES_DIR}/query.css")

QUERY_ENDPOINT = f"{API_URL}/query"
DISCONNECTION_ENDPOINT = f"{API_URL}/close-connection"

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Carter+One&display=swap');
    </style>
            
    <h1 style="font-family: 'Carter One'">DOHT</h1>    
""",
unsafe_allow_html=True)

user_question = st.text_input(
    "❓ Question goes here:",
    placeholder="Clear and proper word choices result in more accurate results 📈"
)
status_message = st.empty()
retrieve = st.button("Retrieve")
disconnect = st.button("Disconnect and Return")

# Either click on Retrieve button or hit Enter to submit question
if retrieve or (user_question and user_question != st.session_state.get("last_query")):
    st.session_state["last_query"] = user_question
    if user_question:
        status_message.markdown("<p class=\"process-msg\">⏳ LLM is processing data...</p>", unsafe_allow_html=True)
        question_response = requests.post(QUERY_ENDPOINT, json={"input": user_question})
        result = question_response.json()
        if question_response.status_code == 200:
            status_message.markdown("<p class=\"success-msg\">✅ Data processed successfully.</p>", unsafe_allow_html=True)
            st.write(result["output"])
        else:
            status_message.markdown("<p class=\"error-msg\">❌ Error occurred while processing data.</p>", unsafe_allow_html=True)
            st.error(result["detail"])
    else:
        st.warning("Please enter a question.")

if disconnect:
    disc_response = requests.post(DISCONNECTION_ENDPOINT)
    if disc_response.status_code == 200:
            st.switch_page("login.py")
    else:
        st.error(disc_response.json()["detail"])