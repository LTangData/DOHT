import streamlit as st

from UI.pages.database_login import login
from UI.pages.query_executor import query
from config.ui_config import STYLES_DIR


st.set_page_config(
    page_title="Get Rid of Query"
)

def load_css(file_name: str) -> None:
    """
    Loads CSS from a specified file into a Streamlit application.

    This function reads the contents of a CSS file and injects it into the Streamlit app as a style tag. This allows for custom styling of the Streamlit app directly from an external CSS file.

    Args:
        file_name (str): The path to the CSS file to be loaded.

    Raises:
        FileNotFoundError: If the CSS file does not exist at the specified path.
    """
    try:
        with open(file_name, "r") as file:
            css_content = file.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_name} does not exist.")

load_css(f"{STYLES_DIR}/UI.css")

# Database credentials input
if "db_info" not in st.session_state:
    st.session_state["db_info"] = {}

current_page = st.query_params.get("page", "login")

if current_page == "login":
    login()
elif current_page == "query":
    query()
else:
    st.error("Page not found.")