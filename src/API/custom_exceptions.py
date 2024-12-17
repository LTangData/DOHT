# Base classes
class DatabaseConnectionError(Exception):
    """Base exception for database connection errors."""
    pass

class LLMError(Exception):
    """Base exception for LLM errors."""
    pass

class AgentError(Exception):
    """Base exception for agent errors."""
    pass


# Custom classes
class DatabaseURIError(DatabaseConnectionError):
    """Raised when the database URI is invalid."""
    pass

class AuthenticationError(DatabaseConnectionError):
    """Raised for incorrect user or password."""
    pass

class HostPermissionError(DatabaseConnectionError):
    """Raised when there are problems related to user permission on host and port."""
    pass

class UnknownDatabaseError(DatabaseConnectionError):
    """Raised when there are problems related to user permission on database and tables."""
    pass

class NonexistentConnectionError(DatabaseConnectionError):
    """Raised when a database connection is already established."""
    pass

class InvalidAPIKey(LLMError):
    """Raised when the provided API key is invalid."""
    pass

class APIKeyNotFound(LLMError):
    """Raised when the API key is not provided."""
    pass