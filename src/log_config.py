from pathlib import Path
from loguru import logger


def configure_logging(file: str) -> None:
    '''
    Configures logging for the application using loguru, creating log files in the 'logs' directory (outside of the 'src' directory).

    Args:
        file (str): The file name where the logging is being configured (usually __file__).

    This function creates the logs directory if it does not exist and ensures that logs are saved in a file named 
    after the script with a standard log format and log level.
    '''
    # Define the logs directory path
    logs_dir = Path('../logs')
    
    # Create the logs directory if it does not exist
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract the base name (without extension) from the provided file
    file_name = Path(file).stem
    
    # Add a new log file configuration with the specified format and log level
    logger.add(logs_dir / f'{file_name}.log', 
               format='{time:YYYY-MM-DD HH:mm:ss} {level} {message}', 
               level='INFO')

    # Log success for setting up logging
    logger.success(f'Logging configured for {file_name}.')
