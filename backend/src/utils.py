import re

def extract_sql_from_query(response: str) -> str:
    """
    Extracts an SQL query from a GPT-4 response formatted with SQL code blocks.

    The expected response format is:
    ```sql
    {SQL query goes here}
    ```

    Args:
        response (str): The full response containing the SQL query.

    Returns:
        str: The extracted SQL query. If no query is found, returns an empty string.
    """
    # Use regex to match SQL code block between ```sql and ```
    match = re.search(r'```sql(.*?)```', response, re.DOTALL)
    
    if match:
        # Return the stripped SQL query if a match is found
        return match.group(1).strip()
    
    # Return an empty string if no match is found
    return ''