from pydantic import BaseModel


class DatabaseConnectionRequest(BaseModel):
    """
    Request model for establishing a database connection.

    Attributes:
        user (str): The username for authenticating the database connection.
        password (str): The password for authenticating the database connection.
        host (str): The hostname or IP address of the database server.
        port (int): The port number to connect to the database (default is 3306).
        database (str): The name of the database to connect to.
    """
    user: str
    password: str
    host: str
    port: int = 3306
    database: str

class QueryRequest(BaseModel):
    """
    Request model for sending a query.

    Attributes:
        input (str): The query or question to be processed.
    """
    input: str

class QueryResponse(BaseModel):
    """
    Response model for returning query results.

    Attributes:
        output (str): The generated response or answer to the query.
    """
    output: str
