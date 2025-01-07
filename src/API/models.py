from pydantic import BaseModel


class DatabaseConnectionRequest(BaseModel):
    """
    Data model representing the credentials and configuration for establishing a database connection.

    Attributes:
        dbms (str): The type of database management system (e.g., "MySQL", "PostgreSQL", "MongoDB").
        user (str): The username used for authenticating the database connection.
        password (str): The password used for authenticating the database connection.
        host (str): The hostname or IP address of the database server.
        port (int): The port number to connect to the database (e.g., 3306 for MySQL, 5432 for PostgreSQL).
        database (str): The name of the database to connect to.
        db_schema (str | None): The schema to use within the database (specifically for PostgresQL). Defaults to None.
    """
    dbms: str
    user: str
    password: str
    host: str
    port: int
    database: str
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
