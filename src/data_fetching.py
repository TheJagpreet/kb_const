"""
Data fetching and document collection module.

This module handles cloning repositories and collecting documents from them.
"""

import json
import os
import subprocess
import time
from typing import List, Tuple

from .state import State


def fetch_and_clone_repos(state: State) -> State:
    """
    Fetches and clones repositories specified in config.json.

    For each repository in the config, it clones or pulls the specified branch.
    Updates the state with the list of downloaded paths.

    Args:
        state (State): The current workflow state.

    Returns:
        State: Updated state with downloaded_paths.
    """
    start = time.time()
    print("Starting fetch_and_clone_repos")
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    paths = []
    os.makedirs('data', exist_ok=True)
    for repo in config:
        url = repo['url']
        branch = repo['branch']
        repo_name = url.split('/')[-1].replace('.git', '')
        path = f'data/{repo_name}_{branch}'
        if os.path.exists(path):
            subprocess.run(['git', 'pull'], cwd=path, check=True)
        else:
            subprocess.run(['git', 'clone', '--branch', branch, url, path], check=True)
        paths.append(path)
    end = time.time()
    elapsed = end - start
    print(f"Finished fetch_and_clone_repos in {elapsed:.2f} seconds")
    return {"downloaded_paths": paths}


def collect_documents(state: State) -> State:
    """
    Collects documents from the cloned repositories.

    Walks through each downloaded path and collects content from .md, .txt, .py files.
    Updates the state with the list of documents as (content, name) tuples.

    Args:
        state (State): The current workflow state.

    Returns:
        State: Updated state with documents.
    """
    start = time.time()
    print("Starting collect_documents")
    documents: List[Tuple[str, str]] = []
    for path in state['downloaded_paths']:
        folder_name = os.path.basename(path)  # e.g., kb_const_kb_1
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(('.md', '.txt', '.py')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if content.strip():
                                name = f"{folder_name}_{file}"
                                documents.append((content, name))
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
    end = time.time()
    elapsed = end - start
    print(f"Finished collect_documents in {elapsed:.2f} seconds")
    return {"documents": documents}