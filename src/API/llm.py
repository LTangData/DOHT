import os

from langchain_openai import ChatOpenAI
from loguru import logger
from openai import OpenAIError

from config import OPENAI_API_KEY
from custom_exceptions import (
    InvalidAPIKey,
    APIKeyNotFound
)


def setup_openai_api() -> ChatOpenAI:
    """
    Configures and initializes LLM using OpenAI GPT-4o chat model.

    Returns:
        ChatOpenAI: The configured LLM.

    Raises:
        APIKeyNotFound: If the OpenAI API key is missing or not provided.
        InvalidAPIKey: If the API connection fails due to an invalid API key, network issues, or other API-related errors.
    """
    if not OPENAI_API_KEY:
        logger.error(f"OpenAI API connection failed. API Key was not provided.")
        raise APIKeyNotFound(
            "Failed to connect to OpenAI API. Please ensure that you have provided your API Key before running the setup."
        ) from None
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    try:
        # Initiliaze LLM
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0  # Control response randomness
        )
        # Test the API connection with a simple request
        response = llm.invoke("Say Hello")
        logger.success("OpenAI API successfully initialized.")
    except OpenAIError as api_error:
        logger.error(f"OpenAI API connection failed. Details: \n{api_error}")
        raise InvalidAPIKey(
            "Failed to connect to OpenAI API. Check the validity of your API key and network settings."
        ) from api_error
    
    return llm
