from langchain_community.utilities import SQLDatabase
from src.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from loguru import logger

def setup_initial_database() -> SQLDatabase:
    """
    Establishes a connection to the MySQL database using credentials from the configuration.

    Returns:
        SQLDatabase: A LangChain SQLDatabase instance connected to the MySQL database.
    
    Raises:
        Exception: If the connection to the database fails.
    """
    try:
        # Build the database URI for MySQL connection using pymysql as the driver
        db_uri = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
        
        # Establish connection to the MySQL database
        db = SQLDatabase.from_uri(db_uri)
        
        # Log success message if the connection is successful
        logger.success('MySQL connection successfully established.')
    except Exception as e:
        # Log error message if connection fails and re-raise the exception
        logger.error(f'MySQL connection failed: {e}')
        raise
    
    # Return the established database instance
    return db

