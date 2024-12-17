from langchain_community.utilities import SQLDatabase
from loguru import logger
from sqlalchemy.exc import OperationalError

from API.custom_exceptions import (
    DatabaseURIError,
    AuthenticationError,
    HostPermissionError,
    UnknownDatabaseError
)


def setup_initial_database(db_user: str, db_password: str, db_host: str, db_port: int, db_name: str) -> SQLDatabase:
    """
    Establishes a connection to a MySQL database using the provided credentials and configuration.

    Args:
        db_user (str): The username for database authentication.
        db_password (str): The password for database authentication.
        db_host (str): The host address of the MySQL server.
        db_port (int): The port number for the MySQL server.
        db_name (str): The name of the target database.

    Returns:
        SQLDatabase: An instance of LangChain's `SQLDatabase` connected to the specified MySQL database.

    Raises:
        DatabaseURIError: If the database URI format is invalid or malformed.
        AuthenticationError: If authentication fails due to incorrect credentials.
        HostPermissionError: If the connection fails due to insufficient host or port permissions.
        UnknownDatabaseError: If the specified database does not exist or is inaccessible.
    """
    db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?connect_timeout=10"
    db = None

    try:
        db = SQLDatabase.from_uri(db_uri)
        logger.success("MySQL connection successfully established.")
    except ValueError as value_error:
        logger.error(f"Invalid database URI format: {db_uri}. Details:\n{value_error}")
        raise DatabaseURIError(
            "There is an error in the database URI format. Please contact us through leotang.prof@gmail.com or (672)-999-2497 so that we can resolve the issue ASAP."
        ) from value_error
    except OperationalError as opr_error:   
        opr_error_msg = opr_error.args[0]
        if "1045" in opr_error_msg:
            logger.error(f"Authentication failed. Details:\n{opr_error_msg}")
            raise AuthenticationError(
                "Authentication failed. Please ensure that username and password are correct."
            ) from None
        if "2003" in opr_error_msg:
            logger.error(f"Unable to connect to MySQL server at {db_host}:{db_port}. Details:\n{opr_error_msg}")
            raise HostPermissionError(
                "User does not have privilege to establish connection using the specified host and port. " + 
                "Please check privileges of current user or check if host and port are both valid and input correctly."
            ) from None
        if "1049" in opr_error_msg:
            logger.error(f"Invalid database specified. Details:\n{opr_error_msg}")
            raise UnknownDatabaseError(
                "Database not found. Please ensure that the database name is correct or check privileges of current user."
            ) from None

    return db
