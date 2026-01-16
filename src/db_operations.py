"""
Database operations module.

This module handles storing embeddings in ChromaDB and retrieving data based on keywords.
"""

import os
import shutil
import time

from sentence_transformers import SentenceTransformer

from db.init_chroma import init_chroma_client, create_collection, add_documents, query_collection
from .state import State

PERSIST_DB = False  # Set to True to persist the database across runs


def store_embeddings(state: State) -> State:
    """
    Stores the embeddings and documents in ChromaDB.

    Initializes the Chroma client, creates a collection, and adds documents with their embeddings.
    If PERSIST_DB is False, deletes the existing database folder first.

    Args:
        state (State): The current workflow state containing documents and embeddings.

    Returns:
        State: Updated state with stored_count.
    """
    start = time.time()
    print("Starting store_embeddings")
    if not PERSIST_DB:
        chroma_dir = "./chroma_db"
        if os.path.exists(chroma_dir):
            shutil.rmtree(chroma_dir)
            print("Deleted existing chroma_db folder.")
    client = init_chroma_client()
    collection_name = "kb_const_docs"
    try:
        client.delete_collection(collection_name)
    except:
        pass  # Collection might not exist
    collection = create_collection(client, collection_name)
    contents = [doc[0] for doc in state['documents']]
    names = [doc[1] for doc in state['documents']]
    metadatas = [{'name': name} for name in names]
    add_documents(collection, contents, state['embeddings'], metadatas)
    stored_count = len(state['documents'])
    end = time.time()
    elapsed = end - start
    print(f"Finished store_embeddings in {elapsed:.2f} seconds")
    return {"stored_count": stored_count}


def retrieve_data(state: State) -> State:
    """
    Retrieves relevant documents for each keyword using vector search.

    For each keyword, encodes it and queries the ChromaDB collection for the top matching document.

    Args:
        state (State): The current workflow state containing keywords.

    Returns:
        State: Updated state with retrieved_data dictionary.
    """
    start = time.time()
    print("Starting retrieve_data")
    model = SentenceTransformer('BAAI/bge-m3')
    client = init_chroma_client()
    collection = create_collection(client, "kb_const_docs")
    results = {}
    for keyword in state['keywords']:
        keyword_embedding = model.encode([keyword]).tolist()[0]
        query_result = query_collection(collection, [keyword_embedding], n_results=5)
        results[keyword] = query_result
    end = time.time()
    elapsed = end - start
    print(f"Finished retrieve_data in {elapsed:.2f} seconds")
    return {"retrieved_data": results}