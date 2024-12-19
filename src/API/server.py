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
from API.database import setup_initial_database
from API.llm import setup_openai_api
from API.log_config import configure_logging
from API.models import (
    DatabaseConnectionRequest,
    QueryRequest,
    QueryResponse,
)

app = FastAPI()

origins = ["http://localhost:8501"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection_exists = False

@app.post("/setup")
async def initialize_resources(credentials: DatabaseConnectionRequest) -> str:
    """
    Sets up the database and LLM resources.

    Args:
        credentials (DatabaseConnectionRequest): Database connection details.

    Returns:
        str: "Success" if setup is completed.

    Raises:
        HTTPException: If setup fails due to database, LLM or agent issues.
    """
    input = dict(credentials)
    db_user = input["user"]
    db_password = input["password"]
    db_host = input["host"]
    db_port = input["port"]
    db_name = input["database"]

    configure_logging(__file__)

    # Used for closing connection
    global connection_exists, MySQL_database, GPT4o_model, agent_executor

    try:
        MySQL_database = setup_initial_database(db_user, db_password, db_host, db_port, db_name)
        connection_exists = True
        GPT4o_model = setup_openai_api()
        agent_executor = create_agent(GPT4o_model, MySQL_database)
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
    Processes user queries and returns answers.

    Args:
        request (QueryRequest): User query input.

    Returns:
        QueryResponse: Generated answer.

    Raises:
        HTTPException: If query processing fails or setup is incomplete.
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
    Closes the active database connection and resets global resources.

    Terminates the MySQL database connection and clears related global variables. 
    Logs an error and raises an HTTP exception if no connection exists.

    Returns:
        str: Success message when the connection is closed.

    Raises:
        HTTPException: If no active connection exists or an error occurs.
    """
    global connection_exists, MySQL_database, GPT4o_model, agent_executor

    try:
        if not connection_exists:
            raise NonexistentConnectionError
        MySQL_database = None
        connection_exists = False
        agent_executor = None
        logger.success("Database connection closed.")
        return "Success"
    except NonexistentConnectionError as nxt_conn_error:
        logger.error(f"Error while closing the database connection: {nxt_conn_error}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while closing the database connection. Please ensure you have a connection available to be closed."
        )

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
