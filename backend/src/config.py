import os
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger


# Load environment variables from .env file if it exists
load_dotenv()

# Retrieve environment variables for OpenAI and database credentials
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f'Project root path is: {PROJ_ROOT}')

SRC_DIR = PROJ_ROOT / 'src'
LOGS_DIR = PROJ_ROOT / 'logs'

DAtA_DIR = SRC_DIR / 'data'

# Ensure the logs directory exists
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# If tqdm is installed, configure loguru to integrate with tqdm for progress bars
try:
    from tqdm import tqdm

    # Remove the default loguru handler
    logger.remove(0)

    # Add a new handler to use tqdm's write function for log messages, ensuring compatibility with progress bars
    logger.add(lambda msg: tqdm.write(msg, end=''), colorize=True)
    logger.success("tqdm integration enabled for logging.")
except ModuleNotFoundError:
    logger.warning("tqdm is not installed. Proceeding without tqdm integration.")