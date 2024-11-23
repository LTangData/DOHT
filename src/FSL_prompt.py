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
        Configured few-shot prompt template.
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
