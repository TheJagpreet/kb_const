"""
LLM generation module.

This module handles generating the constitution using Azure OpenAI.
"""

import datetime
import os
import time

from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

from .state import State

load_dotenv()  # Load environment variables from .env


def generate_constitution(state: State) -> State:
    """
    Generates a constitution document based on retrieved data using Azure OpenAI.

    Formats the retrieved documents into a prompt, calls the LLM, and saves the response to a file.

    Args:
        state (State): The current workflow state containing retrieved_data.

    Returns:
        State: Updated state with constitution text.
    """
    start = time.time()
    print("Starting generate_constitution")

    # Initialize Azure OpenAI client
    llm = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        temperature=0.7,
        max_tokens=2000
    )

    # Format the retrieved data into a prompt
    retrieved = state['retrieved_data']
    prompt_parts = []
    for keyword, data in retrieved.items():
        docs = data.get('documents', [[]])[0]
        metas = data.get('metadatas', [[]])[0]
        for doc, meta in zip(docs, metas):
            name = meta.get('name', 'Unknown')
            prompt_parts.append(f"Keyword: {keyword}\nSource: {name}\nContent:\n{doc}\n")

    full_prompt = "Based on the following retrieved knowledge documents, generate a comprehensive constitution or specification document that synthesizes the key concepts, best practices, and guidelines from all the provided content. Structure it clearly with sections, headings, and actionable insights.\n\n" + "\n".join(prompt_parts)

    # Call the LLM
    response = llm.invoke(full_prompt)
    constitution = response.content if hasattr(response, 'content') else str(response)

    # Save to file
    os.makedirs('constitution', exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"constitution_{timestamp}.md"
    filepath = os.path.join('constitution', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(constitution)
    print(f"Constitution saved to: {filepath}")

    end = time.time()
    elapsed = end - start
    print(f"Finished generate_constitution in {elapsed:.2f} seconds")
    return {"constitution": constitution, "constitution_path": filepath}