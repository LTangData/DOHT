import os

from langchain_openai import ChatOpenAI
from loguru import logger
from openai import OpenAIError

from config.server_config import OPENAI_API_KEY
from API.custom_exceptions import (
    InvalidAPIKey,
    APIKeyNotFound
)


def setup_openai_api() -> ChatOpenAI:
    """
    Initializes and configures the OpenAI GPT-4o chat model for use.

    Returns:
        ChatOpenAI: An instance of the configured OpenAI GPT-4o model.

    Raises:
        APIKeyNotFound: If the OpenAI API key is not provided or missing from the environment.
        InvalidAPIKey: If the connection to the OpenAI API fails due to an invalid API key, network issues, or other API-related errors.
    """
    if not OPENAI_API_KEY:
        logger.error(f"OpenAI API connection failed. API Key was not provided.")
        raise APIKeyNotFound(
            "Failed to connect to OpenAI API. Please ensure that you have provided your API Key before running the setup."
        ) from None
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    try:
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0  # Control response randomness
        )
        # Test the API connection with a simple request
        response = llm.invoke("Say Hello")
        logger.success("OpenAI API successfully accessed.")
    except OpenAIError as api_error:
        logger.error(f"OpenAI API connection failed. Details: \n{api_error}")
        raise InvalidAPIKey(
            "Failed to connect to OpenAI API. Check the validity of your API key and network settings."
        ) from api_error
    
    return llm
