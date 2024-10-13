from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from operator import itemgetter

from utils import extract_sql_from_query
from FSL_prompt import get_final_prompt


def create_sql_query_chain(llm: ChatOpenAI, db: SQLDatabase) -> StrOutputParser:
    """
    Creates a chain to generate an SQL query based on user input, using the database table structure for reference.

    Args:
        llm (ChatOpenAI): The language model used to generate SQL queries.
        db (SQLDatabase): The database object containing table information.

    Returns:
        StrOutputParser: A parser that processes the LLM's response and returns it as a string.
    """
    
    # Get the database table information
    table_info = db.get_table_info()

    # Create a prompt template that includes the table structure and user question
    prompt = PromptTemplate.from_template(f'''
    You are an expert SQL assistant. You have access to the following table structure:
    {table_info}
    
    Based on the user question, generate an accurate SQL query, ensuring the query is correct. 

    Question: {{question}}

    Your answer should be just like the format below. You are not allowed to provide any further information.

    Your answer goes here

    If there is no answer, then simply say

    "Invalid question. No SQL query generated"
    ''')

    # Chain the prompt with the LLM and output parser
    return prompt | llm | StrOutputParser()

def create_chain(llm: ChatOpenAI, db: SQLDatabase) -> RunnablePassthrough:
    """
    Creates a chain to generate and execute SQL queries and provide answers based on the SQL results.

    Args:
        db (SQLDatabase): The database instance to query.
        llm (LLM): The language model to generate SQL queries and responses.

    Returns:
        RunnablePassthrough: A chain object that generates an SQL query, executes it, 
                             and provides an answer based on the query result.
    """
    
    # Tool to execute SQL queries on the provided database
    execute_query = QuerySQLDataBaseTool(db=db)
    
    # Chain to generate SQL queries based on user input using the LLM
    write_query = create_sql_query_chain(llm, db)

    # Prompt template for answering user questions based on SQL query and result
    prompt = get_final_prompt()

    # print(prompt.invoke({
    #     'question': 'hmm I wonder who donald trump is?',
    #     'query': 'Invalid question. No SQL query generated',
    #     'result': ''
    # }).to_string())

    # Create the chain to:
    # 1. Generate SQL query
    # 2. Execute SQL query
    # 3. Return the result formatted with the answer prompt, parsed into a final answer
    chain = (
        # Pass user data through and assign generated query
        RunnablePassthrough.assign(query=write_query)
        # Assign SQL execution result after extracting the query from the data
        .assign(result=lambda data: execute_query.invoke({'query': extract_sql_from_query(itemgetter('query')(data))}))
        # Apply the prompt template
        | prompt
        # Use the LLM to answer the question based on query and result
        | llm
        # Parse the final output as a string
        | StrOutputParser()
    )

    return chain
