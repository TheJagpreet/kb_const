"""
Graph builder module.

This module defines and compiles the LangGraph workflow.
"""

from langgraph.graph import StateGraph, START, END

from .data_fetching import fetch_and_clone_repos, collect_documents
from .keywords import read_keywords
from .embeddings import create_embeddings
from .db_operations import store_embeddings, retrieve_data
from .reranking import rerank_documents
from .llm_generation import generate_constitution
from .state import State


def build_graph():
    """
    Builds and compiles the LangGraph workflow.

    Defines the nodes and edges for the knowledge base constitution generation process.

    Returns:
        The compiled LangGraph application.
    """
    graph = StateGraph(State)
    graph.add_node("fetch_and_clone_repos", fetch_and_clone_repos)
    graph.add_node("read_keywords", read_keywords)
    graph.add_node("collect_documents", collect_documents)
    graph.add_node("create_embeddings", create_embeddings)
    graph.add_node("store_embeddings", store_embeddings)
    graph.add_node("retrieve_data", retrieve_data)
    graph.add_node("rerank_documents", rerank_documents)
    graph.add_node("generate_constitution", generate_constitution)
    graph.add_edge(START, "fetch_and_clone_repos")
    graph.add_edge("fetch_and_clone_repos", "read_keywords")
    graph.add_edge("read_keywords", "collect_documents")
    graph.add_edge("collect_documents", "create_embeddings")
    graph.add_edge("create_embeddings", "store_embeddings")
    graph.add_edge("store_embeddings", "retrieve_data")
    graph.add_edge("retrieve_data", "rerank_documents")
    graph.add_edge("rerank_documents", "generate_constitution")
    graph.add_edge("generate_constitution", END)

    app = graph.compile()
    return app