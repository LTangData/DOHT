from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_openai import OpenAIEmbeddings

from data_loader import load_message_from_file, load_json_from_file
from config import DAtA_DIR

from typing import List, Dict


def create_vectorstore(examples: List[Dict[str, str]]) -> Chroma:
    """
    Creates a vector store from the provided examples for semantic similarity search.

    Args:
        examples (List[Dict[str, str]]): List of example dictionaries containing 'Question', 'SQLQuery', and 'SQLResult'.

    Returns:
        Chroma: A Chroma vector store containing the vectorized examples.
    """
    # Prepare examples for vectorization
    to_vectorize = [' '.join(example.values()) for example in examples]
    
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings()
    
    # Create Chroma vector store
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)
    return vectorstore


class CustomExampleSelector(SemanticSimilarityExampleSelector):
    """
    Custom example selector using semantic similarity to find the closest examples for the query.

    Attributes:
        similarity_threshold (float): The minimum similarity score to consider an example relevant.
    """
    
    similarity_threshold: float = 0.4

    def select_examples(self, input_variables: Dict[str, str]) -> List[Dict[str, str]]:
        """
        Selects examples based on their semantic similarity to the input query.

        Args:
            input_variables (Dict[str, str]): The input query in the form of a dictionary with variable names and values.

        Returns:
            List[Dict[str, str]]: A list of the most relevant examples matching the input query.
        """
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
    """
    Creates a few-shot chat message prompt template using semantic similarity example selection.

    Args:
        vectorstore (Chroma): The vector store used for selecting relevant examples.

    Returns:
        FewShotChatMessagePromptTemplate: A few-shot prompt template that selects examples and prepares the final prompt.
    """
    # Load the example prompt from external file
    example_prompt_message = load_message_from_file(f'{DAtA_DIR}/example_prompt.txt')

    # Define the example prompt template
    example_prompt = ChatPromptTemplate(
        messages=[example_prompt_message],
    )
    
    # Create an instance of the custom semantic similarity example selector
    example_selector = CustomExampleSelector(vectorstore=vectorstore, 
                                             k=2,
                                             input_keys=['question'])
    
    # Return a few-shot prompt template
    return FewShotChatMessagePromptTemplate(
        input_variables=['question', 'query', 'result'],  # Variables passed to example_selector
        example_selector=example_selector,
        example_prompt=example_prompt,
    )


def create_final_prompt(few_shot_prompt: FewShotChatMessagePromptTemplate) -> ChatPromptTemplate:
    """
    Creates the final prompt template by combining a few-shot prompt and system message.

    Args:
        few_shot_prompt (FewShotChatMessagePromptTemplate): The few-shot prompt template for providing examples.

    Returns:
        ChatPromptTemplate: The final prompt template ready to be used for processing queries.
    """
    # Load the prefix and user messages from external files
    prefix_message = load_message_from_file(f'{DAtA_DIR}/prefix.txt')
    user_message = load_message_from_file(f'{DAtA_DIR}/user_message.txt')

    # Define the system message for the assistant's behavior
    prefix = SystemMessage(content=prefix_message)

    # Combine few-shot prompt and system message into the final prompt
    return ChatPromptTemplate.from_messages(
        [
            few_shot_prompt,
            prefix,
            ('user', user_message)
        ]
    )


def get_final_prompt() -> ChatPromptTemplate:
    """
    Entry point to create and return the final prompt template.

    Returns:
        ChatPromptTemplate: The final prompt template that can be used for processing user queries.
    """
    examples = load_json_from_file(f'{DAtA_DIR}/examples.json')
    
    # Create vectorstore from examples
    vectorstore = create_vectorstore(examples)
    
    # Create few-shot prompt template
    few_shot_prompt = create_fs_prompt(vectorstore)
    
    # Return the final prompt template
    return create_final_prompt(few_shot_prompt)
