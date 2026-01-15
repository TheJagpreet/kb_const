import json
import os
import shutil
import subprocess
import time
import datetime
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from sentence_transformers import SentenceTransformer
from db.init_chroma import init_chroma_client, create_collection, add_documents, query_collection
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

PERSIST_DB = False  # Set to True to persist the database across runs

class State(TypedDict):
    downloaded_paths: list[str]
    keywords: list[str]
    documents: list[tuple[str, str]]  # (content, name)
    embeddings: list[list[float]]
    stored_count: int
    retrieved_data: dict
    constitution: str

def fetch_and_clone_repos(state: State) -> State:
    start = time.time()
    print("Starting fetch_and_clone_repos")
    with open('config.json', 'r') as f:
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

def read_keywords(state: State) -> State:
    start = time.time()
    print("Starting read_keywords")
    with open('base_kb.md', 'r') as f:
        keywords = [line.strip() for line in f if line.strip()]
    end = time.time()
    elapsed = end - start
    print(f"Finished read_keywords in {elapsed:.2f} seconds")
    return {"keywords": keywords}

def collect_documents(state: State) -> State:
    start = time.time()
    print("Starting collect_documents")
    documents = []
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

def create_embeddings(state: State) -> State:
    start = time.time()
    print("Starting create_embeddings")
    model = SentenceTransformer('BAAI/bge-m3')
    contents = [doc[0] for doc in state['documents']]
    embeddings = model.encode(contents).tolist()
    end = time.time()
    elapsed = end - start
    print(f"Finished create_embeddings in {elapsed:.2f} seconds")
    return {"embeddings": embeddings}

def store_embeddings(state: State) -> State:
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
    start = time.time()
    print("Starting retrieve_data")
    model = SentenceTransformer('BAAI/bge-m3')
    client = init_chroma_client()
    collection = create_collection(client, "kb_const_docs")
    results = {}
    for keyword in state['keywords']:
        keyword_embedding = model.encode([keyword]).tolist()[0]
        query_result = query_collection(collection, [keyword_embedding], n_results=1)
        results[keyword] = query_result
    end = time.time()
    elapsed = end - start
    print(f"Finished retrieve_data in {elapsed:.2f} seconds")
    return {"retrieved_data": results}

def generate_constitution(state: State) -> State:
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
    return {"constitution": constitution}

graph = StateGraph(State)
graph.add_node("fetch_and_clone_repos", fetch_and_clone_repos)
graph.add_node("read_keywords", read_keywords)
graph.add_node("collect_documents", collect_documents)
graph.add_node("create_embeddings", create_embeddings)
graph.add_node("store_embeddings", store_embeddings)
graph.add_node("retrieve_data", retrieve_data)
graph.add_node("generate_constitution", generate_constitution)
graph.add_edge(START, "fetch_and_clone_repos")
graph.add_edge("fetch_and_clone_repos", "read_keywords")
graph.add_edge("read_keywords", "collect_documents")
graph.add_edge("collect_documents", "create_embeddings")
graph.add_edge("create_embeddings", "store_embeddings")
graph.add_edge("store_embeddings", "retrieve_data")
graph.add_edge("retrieve_data", "generate_constitution")
graph.add_edge("generate_constitution", END)

app = graph.compile()

result = app.invoke({})
print("------------Summary of operations:--------------------")
print("Downloaded repositories to:", result['downloaded_paths'])
print("Keywords:", result['keywords'])
print("Number of documents:", len(result.get('documents', [])))
print("Number of embeddings:", len(result.get('embeddings', [])))
print("Stored count:", result.get('stored_count', 0))
retrieved = result.get('retrieved_data', {})
if retrieved:
    print("Retrieved documents for each keyword:")
    for keyword, data in retrieved.items():
        print(f"\n--- Keyword: {keyword} ---")
        metas = data.get('metadatas', [[]])[0]
        for i, meta in enumerate(metas, 1):
            name = meta.get('name', 'Unknown')
            print(f"{i}. {name}")
else:
    print("No retrieved data.")
constitution = result.get('constitution', '')
if constitution:
    print("\n--- Generated Constitution ---")
    print(constitution)
else:
    print("No constitution generated.")
print("------------------------------------------------------")