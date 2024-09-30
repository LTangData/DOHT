from pathlib import Path
from loguru import logger

def configure_logging(file: str) -> None:
    """
    Configures logging for the application using loguru, creating log files in the 'backend/logs/' directory.

    Args:
        file (str): The file name where the logging is being configured (usually __file__).

    This function ensures that logs are saved in a directory structure, with each log file named after the script.
    """
    # Define the logs directory path
    logs_dir = Path("logs/")
    
    # Create the logs directory if it does not exist
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract the base name (without extension) from the provided file
    file_name = Path(file).stem
    
    # Add a new log file configuration with a specified format and log level
    logger.add(logs_dir / f'{file_name}.log', 
               format='{time:YYYY-MM-DD HH:mm:ss} {level} {message}', 
               level='INFO')

    # Log success for setting up logging (optional)
    logger.success(f"Logging configured for {file_name}.")
