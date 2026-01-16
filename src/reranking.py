"""
Re-ranking module.

This module handles re-ranking of retrieved documents for better relevance.
"""

import time

from sentence_transformers import CrossEncoder

from .state import State


def rerank_documents(state: State) -> State:
    """
    Re-ranks the retrieved documents using a cross-encoder for better relevance.

    Uses a cross-encoder model to score the relevance of each retrieved document
    to its corresponding keyword and selects the top result.

    Args:
        state (State): The current workflow state containing retrieved_data.

    Returns:
        State: Updated state with re-ranked retrieved_data.
    """
    start = time.time()
    print("Starting rerank_documents")

    model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    reranked_results = {}

    for keyword, data in state['retrieved_data'].items():
        docs = data.get('documents', [[]])[0]
        metas = data.get('metadatas', [[]])[0]

        if docs:
            # Prepare pairs for cross-encoder
            pairs = [(keyword, doc) for doc in docs]
            scores = model.predict(pairs)

            # Get the index of the highest score
            best_idx = scores.argmax()
            best_doc = docs[best_idx]
            best_meta = metas[best_idx]

            reranked_results[keyword] = {
                'documents': [[best_doc]],
                'metadatas': [[best_meta]]
            }
        else:
            reranked_results[keyword] = data

    end = time.time()
    elapsed = end - start
    print(f"Finished rerank_documents in {elapsed:.2f} seconds")
    return {"retrieved_data": reranked_results}