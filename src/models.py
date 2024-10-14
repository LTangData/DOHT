from pydantic import BaseModel


class QueryRequest(BaseModel):
    '''
    Request model for the query endpoint.

    Attributes:
        question (str): The question being asked in the query.
    '''
    question: str

class QueryResponse(BaseModel):
    '''
    Response model for the query endpoint.

    Attributes:
        answer (str): The answer generated in response to the query.
    '''
    answer: str
