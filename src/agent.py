from langchain.agents.agent import AgentExecutor
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI

from FSL_prompt import get_final_prompt


def create_agent(llm: ChatOpenAI, db: SQLDatabase) -> AgentExecutor:
    """
    Create an agent that executes SQL queries using a language model.

    This function configures a SQL agent that connects a language model to a SQL database
    allowing the model to autonomously generate and execute SQL queries based on user input.

    Args:
        llm (ChatOpenAI): The language model agent from OpenAI.
        db (SQLDatabase): The SQL database configuration used by the agent.

    Returns:
        AgentExecutor: An executable agent that can run SQL queries.
    """
    # Generate the final prompt from a predefined function
    full_prompt = get_final_prompt()

    # Create the SQL agent with verbose output to trace operations
    agent_executor = create_sql_agent(
        llm,
        db=db,
        prompt=full_prompt,
        agent_type="openai-tools",
        verbose=True
    )

    return agent_executor