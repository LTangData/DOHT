from pydantic import BaseModel


class DatabaseConnectionRequest(BaseModel):
    """
    Data model representing the credentials and configuration for establishing a database connection.

    Attributes:
        dbms (str | None): The type of database management system.
        file_path (str | None): The path to the database file (for connecting to SQLite databases using local file path).
        file_name (str | None): The name of the database file inside sqlite_dbs folder (for connecting to SQLite databases through Docker 
                                or deployed services).
        user (str | None): The username used for authenticating the database connection.
        password (str | None): The password used for authenticating the database connection.
        host (str | None): The hostname or IP address of the database server.
        port (int | None): The port number to connect to the database (e.g., 3306 for MySQL, 5432 for PostgreSQL).
        database (str | None): The name of the database to connect to.
        db_schema (str | None): The schema to use within the database (specifically for PostgresQL).

    By default, all attributes have their value set to None.
    """
    dbms: str | None = None
    file_path: str | None = None
    file_name: str | None = None
    user: str | None = None
    password: str | None = None
    host: str | None = None
    port: int | None = None
    database: str | None = None
    db_schema: str | None = None

class QueryRequest(BaseModel):
    """
    Data model representing a request to process a query or question.

    Attributes:
        input (str): The query or question provided by the user for processing.
    """
    input: str

class QueryResponse(BaseModel):
    """
    Data model representing the response generated for a given query.

    Attributes:
        output (str): The result or answer generated in response to the user's query.
    """
    output: str
