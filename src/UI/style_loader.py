import streamlit as st


def load_page_config() -> None:
    """
    Configures the Streamlit application page settings, including the title and icon.

    Loads the application icon from a file and sets the page title and icon for the Streamlit app.

    Raises:
        FileNotFoundError: If the icon file cannot be found.
    """
    with open("assets/DOHT Icon.png", "rb") as f:
        icon = f.read()
    
    st.set_page_config(
        page_title="DOHT",
        page_icon=icon
    )

def load_css(*files: str) -> None:
    """
    Loads custom CSS files and injects the styles into the Streamlit application.

    Args:
        files (Tuple[str, ...]): One or more file paths to CSS files.

    Raises:
        FileNotFoundError: If any of the specified CSS files cannot be found.
    """
    try:
        css_content = ""
        for file in files:
            with open(file, "r") as f:
                css_content += f.read() + "\n"
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file} does not exist.")
