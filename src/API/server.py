import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from API.agent import create_agent
from API.custom_exceptions import (
    DatabaseURIError,
    AuthenticationError,
    HostPermissionError,
    UnknownDatabaseError,
    NonexistentConnectionError,
    InvalidAPIKey,
    APIKeyNotFound,
    AgentError
)
from API.database import connect_to_db
from API.llm import setup_openai_api
from API.log_config import configure_logging
from API.models import (
    DatabaseConnectionRequest,
    QueryRequest,
    QueryResponse,
)


app = FastAPI()

origins = [
    "http://localhost:8501", # Development
    "https://ltang-doht.streamlit.app/" # Production
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HOST = "0.0.0.0"
PORT = 8000
connection_exists = False

@app.post("/setup")
async def initialize_resources(db_credentials: DatabaseConnectionRequest) -> str:
    """
    Initializes and sets up the database connection, LLM resources, and query agent.

    Args:
        db_credentials (DatabaseConnectionRequest): Credentials and configuration for database connection.

    Returns:
        str: "Success" if the setup is completed successfully.

    Raises:
        HTTPException: Raised if there are issues with the database connection, LLM initialization, or agent setup.
    """
    configure_logging(__file__)

    global connection_exists, database, GPT4o_model, agent_executor

    try:
        database = connect_to_db(db_credentials)
        connection_exists = True
        GPT4o_model = setup_openai_api()
        agent_executor = create_agent(GPT4o_model, database)
        logger.success("Successfully connected to GROQ.")
        return "Success"
    except (DatabaseURIError, AuthenticationError, HostPermissionError, UnknownDatabaseError) as db_error:
        raise HTTPException(
            status_code=(500 if type(db_error) == DatabaseURIError else 400),
            detail=str(db_error)
        )
    except (InvalidAPIKey, APIKeyNotFound) as api_error:
        raise HTTPException(
            status_code=400,
            detail=str(api_error)
        )
    except AgentError as agent_error:
        raise HTTPException(
            status_code=500,
            detail=str(agent_error)
        )

@app.post("/query", response_model=QueryResponse)
async def process_user_query(request: QueryRequest) -> QueryResponse:
    """
    Handles user queries by passing the input to the query agent and returning the result.

    Args:
        request (QueryRequest): Contains the user's query or question.

    Returns:
        QueryResponse: The generated answer or output from the query agent.

    Raises:
        HTTPException: Raised if the query cannot be processed due to incomplete setup or unexpected errors.
    """
    try:
        answer = agent_executor.invoke({"input": request.input})
        return QueryResponse(output=answer["output"])
    except Exception as setup_error:
        logger.error(f"Failed to process query. Details:\n {setup_error}")
        raise HTTPException(
            status_code=500,
            detail="Database connection and LLM were not set up properly. Please ensure to run initial setup first."
        )
    
@app.post("/close-connection")
async def terminate_database_connection() -> str:
    """
    Safely closes the active database connection and resets global resources.

    Terminates the MySQL database connection and clears related global variables. 
    Logs an error and raises an HTTP exception if no connection exists.

    Returns:
        str: "Success" if the database connection is closed successfully.

    Raises:
        HTTPException: Raised if no active connection exists or if an error occurs during termination.
    """
    global connection_exists, database, GPT4o_model, agent_executor

    try:
        if not connection_exists:
            raise NonexistentConnectionError
        database = None
        connection_exists = False
        agent_executor = None
        logger.success("Database connection closed.")
        return "Success"
    except NonexistentConnectionError as nxt_conn_error:
        logger.error(f"Error while closing the database connection: {nxt_conn_error}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while closing the database connection. Please ensure you have a connection available to be closed."
        )

if __name__ == "__main__":
    uvicorn.run("server:app", host=HOST, port=PORT, reload=True)
