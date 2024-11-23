from typing import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from agent import create_agent
from database import setup_initial_database
from llm import setup_openai_api
from log_config import configure_logging
from models import QueryRequest, QueryResponse


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Initializes resources like the database and LLM during application startup.

    Args:
        app (FastAPI): The FastAPI instance.

    Yields:
        None: Used to manage application lifespan (startup and shutdown).
    """
    configure_logging(__file__)
    global MySQL_database, GPT4o_model, agent_executor
    MySQL_database = setup_initial_database()
    GPT4o_model = setup_openai_api()
    agent_executor = create_agent(GPT4o_model, MySQL_database)

    logger.success("Resources initialized successfully.")

    yield

    logger.info("Shutting down the application...")
    logger.info("Logs finalized.")

app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:8501"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest) -> QueryResponse:
    """
    Endpoint to handle user queries and return processed answers.

    Args:
        request (QueryRequest): The incoming question from the user.

    Returns:
        QueryResponse: The processed answer based on the LLM and database.
    
    Raises:
        HTTPException: If any error occurs during query processing.
    """
    try:
        answer = agent_executor.invoke({"input": request.question})
        return QueryResponse(answer=answer["output"])
    except Exception as e:
        logger.error(f"Failed to process query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
