from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.chains import create_sql_query_chain
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

from src.utils import extract_sql_from_query

def create_chain(db, llm) -> RunnablePassthrough:
    """
    Creates a chain to generate and execute SQL queries and provide answers based on the SQL results.
    
    This chain performs the following steps:
    1. Uses the LLM to write an SQL query based on a user question.
    2. Executes the SQL query on the database.
    3. Generates a natural language answer based on the query result.
    
    Args:
        db: An instance of the database (SQLDatabase) to query.
        llm: The language model (LLM) to generate SQL queries and responses.

    Returns:
        RunnablePassthrough: A chain object that takes a user question, generates an SQL query,
                             executes it, and returns an answer based on the result.
    """
    
    # Tool to execute SQL queries on the provided database
    execute_query = QuerySQLDataBaseTool(db=db)
    
    # Chain to generate SQL queries based on user input using the LLM
    write_query = create_sql_query_chain(llm, db)
    
    # Prompt template for answering user questions based on SQL query and result
    answer_prompt = PromptTemplate.from_template(
        '''Given the following user question, corresponding SQL query, and SQL result, answer the user question.
        Question: {question}
        SQL Query: {query}
        SQL Result: {result}
        Answer: '''
    )

    # Create the chain: 
    # 1. Generate SQL query
    # 2. Execute SQL query
    # 3. Return the result formatted with the answer prompt, parsed into a final answer
    chain = (
        # Pass user data through and assign generated query
        RunnablePassthrough.assign(query=write_query)
        # Assign SQL execution result after extracting the query from the data
        .assign(result=lambda data: execute_query.invoke({'query': extract_sql_from_query(itemgetter('query')(data))}))
        # Apply the prompt template
        | answer_prompt
        # Use the LLM to answer the question based on query and result
        | llm
        # Parse the final output as a string
        | StrOutputParser()
    )

    return chain
