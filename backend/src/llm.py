import os
from langchain_openai import ChatOpenAI
from loguru import logger
from src.config import OPENAI_API_KEY

def setup_openai_api() -> ChatOpenAI:
    """
    Sets up the OpenAI API using the provided secret key from environment variables.

    Returns:
        ChatOpenAI: An instance of the ChatOpenAI client configured to use GPT-4.

    Raises:
        ValueError: If the OpenAI API key is not found.
        Exception: If an unexpected error occurs during the API test call.
    """
    # Check if the OpenAI API key is available
    if not OPENAI_API_KEY:
        logger.error('OpenAI API Key not found in environment variables')
        raise ValueError('OpenAI API credentials are missing.')

    # Set the OpenAI API key in the environment
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

    # Initialize the OpenAI LLM with the chosen model and temperature settings
    llm = ChatOpenAI(
        model='gpt-4o',
        temperature=0  # Control response randomness
    )

    try:
        # Test the API connection by sending a simple request
        response = llm.invoke("Say Hello")
        logger.success("OpenAI API call successful.")
    except Exception as e:
        # Log and raise an exception if the API call fails
        logger.error(f"API call failed. An unexpected error occurred: {e}")
        raise

    return llm
