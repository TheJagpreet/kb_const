"""
Keywords module.

This module handles reading keywords from the base_kb.md file.
"""

import time

from .state import State


def read_keywords(state: State) -> State:
    """
    Reads keywords from base_kb.md.

    Each non-empty line in the file is treated as a keyword.

    Args:
        state (State): The current workflow state.

    Returns:
        State: Updated state with keywords list.
    """
    start = time.time()
    print("Starting read_keywords")
    with open('config/keywords.md', 'r') as f:
        keywords = [line.strip() for line in f if line.strip()]
    end = time.time()
    elapsed = end - start
    print(f"Finished read_keywords in {elapsed:.2f} seconds")
    return {"keywords": keywords}