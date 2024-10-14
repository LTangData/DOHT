import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import QueryRequest, QueryResponse
from database import setup_initial_database
from llm import setup_openai_api
from chain import create_chain
from log_config import configure_logging

from typing import Generator

from loguru import logger


def lifespan(app: FastAPI) -> Generator[None, None, None]:
    '''
    Initializes resources like the database and LLM during application startup.

    Args:
        app (FastAPI): The FastAPI instance.

    Yields:
        None: Used to manage application lifespan (setup and teardown).
    '''
    global MySQL_database, GPT4o_model, chain
    
    # Configure application logging
    configure_logging(__file__)
    
    # Setup the initial database connection
    MySQL_database = setup_initial_database()
    
    # Setup OpenAI GPT-4o model through the OpenAI API
    GPT4o_model = setup_openai_api()
    
    # Create the processing chain to handle queries
    chain = create_chain(GPT4o_model, MySQL_database)

    logger.success('Resources initialized successfully.')
    
    yield  # This pauses here while the app runs and resumes when the app is shutting down

    # Cleanup code and finalize logs after application stops
    logger.info('Shutting down the application...')
    logger.info('Logs finalized.')

# Initialize FastAPI app with a lifespan handler
app = FastAPI(lifespan=lifespan)

# List of allowed origins (frontend URL will be included inside this)
origins = ['http://localhost:8501']

# Middleware to enable Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allow all origins for simplicity
    allow_credentials=True,
    allow_methods=['*'],  # Allow all HTTP methods
    allow_headers=['*'],  # Allow all HTTP headers
)

@app.post('/query', response_model=QueryResponse)
async def query_endpoint(request: QueryRequest) -> QueryResponse:
    '''
    Endpoint to handle user queries and return processed answers.

    Args:
        request (QueryRequest): The incoming question from the user.

    Returns:
        QueryResponse: The processed answer based on the LLM and database.
    
    Raises:
        HTTPException: If any error occurs during query processing.
    '''
    try:
        # Invoke the chain with the provided question
        answer = chain.invoke({'question': request.question})
        return QueryResponse(answer=answer)
    except Exception as e:
        # Handle any exceptions that occur and return a 500 HTTP error
        raise HTTPException(status_code=500, detail=f'{e}')

if __name__ == '__main__':
    # Start the FastAPI app with Uvicorn
    uvicorn.run('server:app', host='0.0.0.0', port=8000, reload=True)
