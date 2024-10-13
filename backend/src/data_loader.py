import json 
from typing import List, Dict


def load_message_from_file(file_path: str) -> str:
    """
    Loads a message from a text file.

    Args:
        file_path (str): Path to the text file.

    Returns:
        str: The content of the file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def load_json_from_file(file_path: str) -> List[Dict[str, str]]:
    """
    Loads examples from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        List[Dict[str, str]]: A list of example dictionaries.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)