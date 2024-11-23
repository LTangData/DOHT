from langchain_community.utilities import SQLDatabase
from loguru import logger

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


def setup_initial_database() -> SQLDatabase:
    """
    Establishes a connection to the MySQL database using credentials from the configuration.

    Returns:
        SQLDatabase: A LangChain SQLDatabase instance connected to the MySQL database.

    Raises:
        Exception: If the connection to the database fails.
    """
    try:
        db_uri = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        db = SQLDatabase.from_uri(db_uri)
        logger.success("MySQL connection successfully established.")
    except Exception as e:
        logger.error(f"MySQL connection failed: {e}")
        raise
    
    return db
