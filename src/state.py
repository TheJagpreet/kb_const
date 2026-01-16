"""
State definitions for the KB Const application.

This module defines the TypedDict for the LangGraph state used throughout the workflow.
"""

from typing import TypedDict


class State(TypedDict):
    """
    Represents the state of the LangGraph workflow.

    Attributes:
        downloaded_paths (list[str]): List of paths to downloaded/cloned repositories.
        keywords (list[str]): List of keywords read from base_kb.md.
        documents (list[tuple[str, str]]): List of tuples containing (content, name) for each document.
        embeddings (list[list[float]]): List of embedding vectors for the documents.
        stored_count (int): Number of documents stored in the database.
        retrieved_data (dict): Retrieved data from the database for each keyword.
        constitution (str): The generated constitution text.
        constitution_path (str): The file path where the constitution is saved.
    """
    downloaded_paths: list[str]
    keywords: list[str]
    documents: list[tuple[str, str]]  # (content, name)
    embeddings: list[list[float]]
    stored_count: int
    retrieved_data: dict
    constitution: str
    constitution_path: str