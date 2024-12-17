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

from config.server_config import DATA_DIR
from API.data_loader import load_message_from_file, load_json_from_file


def create_fs_prompt() -> FewShotPromptTemplate:
    """
    Configures a few-shot prompt template with semantic similarity-based example selection.

    This few-shot prompt is designed for the RAG application to dynamically select the most relevant examples according to user questions
    for generating accurate and context-aware responses. In simplicity, this technique is used to "teach" or fine-tune the model to be able to
    handle highly complex questions and fully understand the nature of our database.
     
    Semantic similarity search is a search algorithm used to match user question with examples based on meaning rather than exact words. In order to
    utilize this algorithm, vector database is also used in this application (ChromaDB in our case).

    Returns:
        FewShotPromptTemplate: A dynamic prompt template using selected examples.
    """
    examples = load_json_from_file(f"{DATA_DIR}/examples.json")
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        OpenAIEmbeddings(),
        Chroma,
        k=3,
        input_keys=["input"],
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
    Converts a few-shot prompt template into a chat-ready format.

    Args:
        few_shot_prompt (FewShotPromptTemplate): The base prompt to enhance.

    Returns:
        ChatPromptTemplate: A complete template for chat-based interactions.
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
    Assembles the final chat prompt template by integrating a few-shot prompt.

    Returns:
        ChatPromptTemplate: A complete template for chat-based interactions.
    """
    few_shot_prompt = create_fs_prompt()

    return create_final_prompt(few_shot_prompt)
