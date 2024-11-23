from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import OpenAIEmbeddings

from config import DATA_DIR
from data_loader import load_message_from_file, load_json_from_file


def create_fs_prompt() -> FewShotPromptTemplate:
    """
    Initializes a few-shot prompt template using semantic similarity for example selection.

    Loads examples from JSON and constructs a template with dynamic elements based on the provided data.
    
    Returns:
<<<<<<< HEAD
        Configured few-shot prompt template.
    """
    examples = load_json_from_file(f"{DATA_DIR}/examples.json")
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        OpenAIEmbeddings(),
        Chroma,
        k=3,
        input_keys=["input"],
=======
        Chroma: A Chroma vector store containing the vectorized examples.
    '''
    # Prepare examples for vectorization
    to_vectorize = [' '.join(example.values()) for example in examples]
    
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings()
    
    # Create Chroma vector store
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)
    return vectorstore


class CustomExampleSelector(SemanticSimilarityExampleSelector):
    '''
    Custom example selector using semantic similarity to find the closest examples for the query.

    Attributes:
        similarity_threshold (float): The minimum similarity score to consider an example relevant.
    '''
    
    similarity_threshold: float = 0.8

    def select_examples(self, input_variables: Dict[str, str]) -> List[Dict[str, str]]:
        '''
        Selects examples based on their semantic similarity to the input query.

        Args:
            input_variables (Dict[str, str]): The input query in the form of a dictionary with variable names and values.

        Returns:
            List[Dict[str, str]]: A list of the most relevant examples matching the input query.
        '''
        query = ' '.join(input_variables.values())
        # Get the k most similar examples
        examples_with_scores = self.vectorstore.similarity_search_with_relevance_scores(query, k=self.k)
        
        # Filter examples based on the similarity threshold
        filtered_examples = [
            example for example, score in examples_with_scores
            if score >= self.similarity_threshold
        ]
        
        return [example.metadata for example in filtered_examples]


def create_fs_prompt(vectorstore: Chroma) -> FewShotChatMessagePromptTemplate:
    '''
    Creates a few-shot chat message prompt template using semantic similarity example selection.

    Args:
        vectorstore (Chroma): The vector store used for selecting relevant examples.

    Returns:
        FewShotChatMessagePromptTemplate: A few-shot prompt template that selects examples and prepares the final prompt.
    '''
    # Load the example prompt from external file
    example_prompt_message = load_message_from_file(f'{DATA_DIR}/example_prompt.txt')

    # Define the example prompt template
    example_prompt = ChatPromptTemplate(
        messages=[example_prompt_message]
>>>>>>> 0d568717a4fd3b802ab26004c36609590e016e9a
    )
    system_prefix = load_message_from_file(f"{DATA_DIR}/prefix.txt")
    example_prompt = load_message_from_file(f"{DATA_DIR}/example_prompt.txt")

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=PromptTemplate.from_template(example_prompt),
        input_variables=["input", "dialect", "top_k"],
        prefix=system_prefix,
        suffix="",
    )

    return few_shot_prompt


def create_final_prompt(few_shot_prompt: FewShotPromptTemplate) -> ChatPromptTemplate:
    """
    Combines a few-shot prompt with a message placeholder to form a chat prompt template.

    Args:
        few_shot_prompt: Few-shot prompt to wrap into a chat template.

    Returns:
        Complete chat prompt template.
    """
    full_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=few_shot_prompt),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    return full_prompt


def get_final_prompt() -> ChatPromptTemplate:
    """
    Generates a chat prompt template using a few-shot configured prompt.

    Orchestrates the creation of few-shot and chat prompts to be used for model interactions.

    Returns:
        Finalized chat prompt template.
    """
    few_shot_prompt = create_fs_prompt()

    return create_final_prompt(few_shot_prompt)
