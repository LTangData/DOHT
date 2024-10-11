from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_openai import OpenAIEmbeddings

examples = [
    {
        "Question": "Total population in a random place",
        "SQLQuery": "SELECT COUNT(*) FROM customers WHERE perfume_purchased = 'true'",
        "SQLResult": "12345"
    }
]

to_vectorize = [' '.join(example.values()) for example in examples]
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)

class CustomSemanticSimilarityExampleSelector(SemanticSimilarityExampleSelector):
    similarity_threshold: float = 0.8

    def select_examples(self, input_variables):
        query = ' '.join(input_variables.values())
        # Get the k most similar examples
        examples_with_scores = self.vectorstore.similarity_search_with_relevance_scores(query, k=self.k)
        # Filter examples based on the similarity threshold
        filtered_examples = [
            example for example, score in examples_with_scores
            if score >= self.similarity_threshold
        ]
        # Extract the examples (without scores) to return
        return [example.metadata for example in filtered_examples]

example_selector = CustomSemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=1,
    similarity_threshold=0.8
)

example_prompt = ChatPromptTemplate(
    messages=['''
    Question: {Question}
    SQL Query: {SQLQuery}
    SQL Result: {SQLResult}
    '''],
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    input_variables=['question', 'query', 'result'], # These are passed to example_selector
    example_selector=example_selector,
    example_prompt=example_prompt,
)

prefix = SystemMessage(content='''
        You are an expert SQL assistant.
        Only use the above examples as guidance or when you find user question that matches OVER 90%, otherwise prioritize over answering the user's question accurately on your own.
        These examples are just meant to support you when you are facing complex questions, which have already been provided with solutions in guidance.
        If you find user question that matches perfectly to any of the above examples, then you should use the result of the example since it is 100% correct answer that has been manually written by human.
        If you face INSERT, UPDATE or DELETE requests, your answers should be really simple and insightful. Just answer users using the exact "SQL Result" provided.
        Since you are just an assistant, you are NOT allowed to provide any further instructions to users. You just tell them whether their request was valid and successfully executed or not.
        If the request failed, you should concisely and clearly explain ONLY the ONE MAIN problem. It is crucial for you to avoid lengthy responses and confusion for users.
        You are NOT allowed to tell user to execute the query in MySQL environment or anything else. The query has already been executed before that, your only job is to tell if the request was successfully executed.
''')

final_prompt = ChatPromptTemplate.from_messages(
    [
        few_shot_prompt,
        prefix,
        ('user', '''
        Now, Given the following user question, corresponding SQL query, and SQL result, answer the user question.
                            
        Question: {question}
        SQL Query: {query}
        SQL Result: {result}

        Please provide concise answer to avoid confusion to users and lengthy responses.
''')
    ]
)
