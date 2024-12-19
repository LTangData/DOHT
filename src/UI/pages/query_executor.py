import requests

import streamlit as st


QUERY_ENDPOINT = "http://localhost:8000/query"
DISCONNECTION_ENDPOINT = "http://localhost:8000/close-connection"
def query():
    st.markdown("<h1 class=\"query-title\">GROQ (Get Rid of Queries)</h1>", unsafe_allow_html=True)

    user_question = st.text_input("Question goes here:")
    status_message = st.empty()

    # Either click on Submit button or hit Enter to submit question
    if st.button("Submit") or (user_question and user_question != st.session_state.get("last_query")):
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

    if st.button("Disconnect and Return"):
        disc_response = requests.post(DISCONNECTION_ENDPOINT)
        if disc_response.status_code == 200:
                st.query_params.update({"page": "login"})
                st.rerun()
                st.stop()
        else:
            st.error(disc_response.json()["detail"])