import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from agent import create_agent
from custom_exceptions import (
    DatabaseURIError,
    AuthenticationError,
    HostPermissionError,
    UnknownDatabaseError,
    InvalidAPIKey,
    APIKeyNotFound,
    AgentError
)
from database import setup_initial_database
from llm import setup_openai_api
from log_config import configure_logging
from models import (
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

@app.post("/setup")
async def initial_resources_setup(credentials: DatabaseConnectionRequest) -> str:
    """
    Sets up the database and LLM resources.

    Args:
        credentials (DatabaseConnectionRequest): Database connection details.

    Returns:
        str: "Success" if setup is completed.

    Raises:
        HTTPException: If setup fails due to database, LLM or agent issues.
    """
    global agent_executor
    input = dict(credentials)
    db_user = input["user"]
    db_password = input["password"]
    db_host = input["host"]
    db_port = input["port"]
    db_name = input["database"]

    configure_logging(__file__)

    try:
        MySQL_database = setup_initial_database(db_user, db_password, db_host, db_port, db_name)
    except (DatabaseURIError, AuthenticationError, HostPermissionError, UnknownDatabaseError) as db_error:
        raise HTTPException(
            status_code=(500 if type(db_error) == DatabaseURIError else 400),
            detail=str(db_error)
        )

    try:
        GPT4o_model = setup_openai_api()
    except (InvalidAPIKey, APIKeyNotFound) as api_error:
        raise HTTPException(
            status_code=400,
            detail=str(api_error)
        )

    try:
        agent_executor = create_agent(GPT4o_model, MySQL_database)
        logger.success("Successfully connected to GROQ.")
        return "Success"
    except AgentError as agent_error:
        raise HTTPException(
            status_code=500,
            detail=str(agent_error)
        )

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest) -> QueryResponse:
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
    except NameError as setup_error:
        logger.error(f"Failed to process query. Details:\n {setup_error}")
        raise HTTPException(
            status_code=500,
            detail="Database connection and LLM were not set up properly. Please ensure to run initial setup first."
        )

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
