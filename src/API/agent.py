from langchain.agents.agent import AgentExecutor
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from loguru import logger

from API.custom_exceptions import AgentError
from API.FSL_prompt import get_final_prompt


def create_agent(llm: ChatOpenAI, toolkit: SQLDatabaseToolkit) -> AgentExecutor:
    """
    Constructs a SQL query agent to translate natural language into executable database operations.

    This method initializes an agent that leverages a Large Language Model to:
    - Interpret natural language questions
    - Generate appropriate SQL statements
    - Execute queries in the database
    - Return comprehensive query results

    Args:
        llm (ChatOpenAI): Language model for query generation.
        toolkit (SQLDatabaseToolkit): A collection of database tools that provide methods and utilities for query execution 
            and database interaction.

    Returns:
        AgentExecutor: Configured agent for SQL operations.

    Raises:
        AgentError: Raised when the agent creation process fails due to configuration errors.

    Note:
        The agent operates with verbose logging to provide transparency into its decision-making process.
    """
    full_prompt = get_final_prompt()

    try:
        agent_executor = create_sql_agent(
            llm,
            toolkit,
            agent_type="openai-tools",
            verbose=True,
            prompt=full_prompt,
        )
    except Exception as agent_error:
        logger.error(f"Failed to create agent. Details:\n{agent_error}")
        raise AgentError(
            "An uenxpected technical problem has occured. This feature may not be available right now. We apologize for such inconvenience."
        ) from agent_error

    return agent_executor