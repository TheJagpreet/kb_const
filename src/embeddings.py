"""
Embeddings module.

This module handles creating embeddings for the collected documents.
"""

import time

from sentence_transformers import SentenceTransformer

from .state import State


def create_embeddings(state: State) -> State:
    """
    Creates embeddings for the collected documents using SentenceTransformers.

    Uses the BAAI/bge-m3 model to encode document contents into vectors.

    Args:
        state (State): The current workflow state containing documents.

    Returns:
        State: Updated state with embeddings list.
    """
    start = time.time()
    print("Starting create_embeddings")
    model = SentenceTransformer('BAAI/bge-m3')
    contents = [doc[0] for doc in state['documents']]
    embeddings = model.encode(contents).tolist()
    end = time.time()
    elapsed = end - start
    print(f"Finished create_embeddings in {elapsed:.2f} seconds")
    return {"embeddings": embeddings}