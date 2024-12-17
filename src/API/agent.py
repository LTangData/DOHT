from langchain.agents.agent import AgentExecutor
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from loguru import logger

from API.custom_exceptions import AgentError
from API.FSL_prompt import get_final_prompt


def create_agent(llm: ChatOpenAI, db: SQLDatabase) -> AgentExecutor:
    """
    Initializes an agent to process natural language inputs and execute SQL queries.

    Args:
        llm (ChatOpenAI): Language model for query generation.
        db (SQLDatabase): Database connection for query execution.

    Returns:
        AgentExecutor: Configured agent for SQL operations.

    Raises:
        AgentError: If agent creation fails.
    """
    # Generate the final prompt from a predefined function
    full_prompt = get_final_prompt()

    try:
        # Create the SQL agent with verbose output to trace operations
        agent_executor = create_sql_agent(
            llm,
            db=db,
            prompt=full_prompt,
            agent_type="openai-tools",
            verbose=True
        )
    except Exception as agent_error:
        logger.error(f"Failed to create agent. Details:\n{agent_error}")
        raise AgentError(
            "If you are seeing this message, it means that there has been a technical problem from our side. " +
            "Please contact us so that we can resolve the issue as soon as possible. We apologize for such inconvenience."
        ) from agent_error

    return agent_executor