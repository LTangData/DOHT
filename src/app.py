import streamlit as st
import requests

from config import STYLES_DIR

# Define the FastAPI backend URL
API_URL = 'http://localhost:8000/query'

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the external CSS file
load_css(f'{STYLES_DIR}/UI.css')

# Streamlit UI with custom title styling
st.markdown('<h1 style="font-family:Montserrat; color:#3d4960; font-size:48px;">GROQ (Get Rid Of Queries)</h1>', unsafe_allow_html=True)

# Text input for user to ask question
user_question = st.text_input('Quesion goes here:')

# Placeholder for status message just under the text input
status_message = st.empty()

# Click 'Submit' or simply hit 'Enter' inside the textbox to submit the query
if st.button('Submit') or user_question:
    if user_question:
        # Display 'LLM is extracting data...' while processing
        status_message.markdown('<p style="font-family:Arial; font-size:16px; color:orange;">⏳ LLM is extracting data...</p>', unsafe_allow_html=True)

        # Send the user question to FastAPI backend
        response = requests.post(API_URL, json={'question': user_question})

        if response.status_code == 200:
            # Display the response answer from backend
            result = response.json()['answer']
            st.write(result)
            # Update the status message to success
            status_message.markdown('<p style="font-family:Arial; font-size:16px; color:green;">✅ Data extracted successfully.</p>', unsafe_allow_html=True)
        else:
            st.error(f'Error: {response.status_code} - {response.text}')
            status_message.markdown('<p style="font-family:Arial; font-size:16px; color:red;">❌ Error occurred while retrieving data.</p>', unsafe_allow_html=True)
    else:
        st.warning('Please enter a question.')
