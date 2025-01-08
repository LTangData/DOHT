from langchain_community.utilities import SQLDatabase
from loguru import logger
from sqlalchemy.exc import OperationalError

from API.custom_exceptions import (
    DatabaseURIError,
    AuthenticationError,
    HostPermissionError,
    UnknownDatabaseError
)
from API.models import DatabaseConnectionRequest


def connect_to_db(credentials: DatabaseConnectionRequest) -> SQLDatabase:
    """
    Establishes a connection to a database using the provided credentials and configuration.

    Args:
        credentials (DatabaseConnectionRequest): An object containing the necessary credentials for database 
            connection. Expected attributes include:
            - dbms (str): The type of database management system.
            - user (str): The username for database authentication.
            - password (str): The password for database authentication.
            - host (str): The host address of the database server.
            - port (int): The port number to connect to the database server.
            - database (str): The name of the target database.
            - db_schema (str, optional): The schema to use inside database (specifically for PostgresQL).

    Returns:
        SQLDatabase: An instance of LangChain's `SQLDatabase` connected to the specified database.

    Raises:
        DatabaseURIError: If the database URI is invalid or improperly formatted.
        AuthenticationError: If authentication fails due to incorrect credentials.
        HostPermissionError: If access is denied due to insufficient host or port permissions.
        UnknownDatabaseError: If the specified database does not exist or another unknown error occurs.

    Notes:
        - Supported DBMS values include "MySQL", "PostgreSQL", "SQLite", "MongoDB" and "Redis".
        - Connection errors are logged with detailed information for troubleshooting.
    """
    inputs = dict(credentials)
    dbms = inputs["dbms"]
    db_user = inputs["user"]
    db_password = inputs["password"]
    db_host = inputs["host"]
    db_port = inputs["port"]
    db_name = inputs["database"]
    db_schema = inputs["db_schema"]

    match dbms:
        case "MySQL":
            # Consistency across both deployment and local development: pymysql
            # Best performance: mysqlclient (requires libmysqlclient and a C compiler)
            db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        case "PostgreSQL":
            # Consistency across both deployment and local development: psycopg2-binary
            # Best performance: psycopg2 (requires a C compiler, Python header files and PostgreSQL development files)
            db_uri = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        case "MongoDB":
            db_uri = f"mongodb://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    db = None

    try:
        db = SQLDatabase.from_uri(db_uri)
        if dbms == "PostgreSQL":
            db._execute(f"SET search_path TO {db_schema}")
        logger.success("Database connection successfully established.")
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
    except Exception as e:
        logger.error(f"Failed to establish connection. Details:\n{e}")
        raise UnknownDatabaseError(
            "An unexpected error occurred while connecting to the MySQL database. Please ensure that the database is running and accessible."
        ) from e

    return db
