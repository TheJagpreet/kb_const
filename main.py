import json
import os
import subprocess
from pathlib import Path
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    config: list[dict]
    keywords: list[str]
    downloaded_paths: list[str]
    constitution: str

def read_config(state: State) -> State:
    with open('config.json', 'r') as f:
        config = json.load(f)
    return {"config": config}

def download_data(state: State) -> State:
    paths = []
    os.makedirs('data', exist_ok=True)
    for repo in state['config']:
        url = repo['url']
        branch = repo['branch']
        repo_name = url.split('/')[-1]
        path = f'data/{repo_name}'
        if os.path.exists(path):
            subprocess.run(['git', 'pull'], cwd=path, check=True)
        else:
            subprocess.run(['git', 'clone', '--branch', branch, url, path], check=True)
        paths.append(path)
    return {"downloaded_paths": paths}

def read_keywords(state: State) -> State:
    with open('base_kb.md', 'r') as f:
        keywords = [line.strip() for line in f if line.strip()]
    return {"keywords": keywords}

def create_constitution(state: State) -> State:
    relevant_snippets = []
    for path in state['downloaded_paths']:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(('.md', '.txt', '.py')):  # Assuming relevant file types
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if any(keyword.lower() in content.lower() for keyword in state['keywords']):
                                snippet = content[:500]  # Take first 500 chars as snippet
                                relevant_snippets.append(f"From {file_path}:\n{snippet}\n")
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
    constitution = "Created as per github speckit constitution agent guidelines\n\n" + "\n".join(relevant_snippets)
    with open('base_constitution.md', 'w') as f:
        f.write(constitution)
    return {"constitution": constitution}

graph = StateGraph(State)
graph.add_node("read_config", read_config)
graph.add_node("download_data", download_data)
graph.add_node("read_keywords", read_keywords)
graph.add_node("create_constitution", create_constitution)
graph.add_edge(START, "read_config")
graph.add_edge("read_config", "download_data")
graph.add_edge("download_data", "read_keywords")
graph.add_edge("read_keywords", "create_constitution")
graph.add_edge("create_constitution", END)

app = graph.compile()

result = app.invoke({})
print("Constitution created:", result['constitution'][:200])  # Print first 200 chars