from pathlib import Path

from loguru import logger

from config.server_config import LOGS_DIR


def configure_logging(file: str) -> None:
    """
    Sets up application logging using Loguru.

    This function creates the logs directory (if not already present) under API directory and configures Loguru to write logs to a file 
    named after the script. The logs are formatted with timestamps, log levels, and messages, with a default log level of "INFO."

    Args:
        file (str): The name of the script file where logging is configured (typically __file__).
    """
    logs_dir = Path(LOGS_DIR)
    logs_dir.mkdir(parents=True, exist_ok=True)
    # Extract the base name (without extension) from the provided file
    file_name = Path(file).stem
    # Add configuration with the specified format and log level
    logger.add(logs_dir / f"{file_name}.log", 
               format="{time:YYYY-MM-DD HH:mm:ss} {level} {message}", 
               level="INFO")
    
    logger.success(f"Logging configured for {file_name}.")
