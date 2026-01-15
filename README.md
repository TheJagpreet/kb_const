# KB Const

A Python project for generating knowledge base constitutions using LangGraph, ChromaDB, and Azure AI Foundry.

## Overview

This project automates the creation of a "constitution" (a synthesized specification document) from domain-specific knowledge files. It:

- Clones GitHub repositories containing knowledge base content.
- Collects and processes documents (Markdown, text, Python files).
- Creates embeddings using SentenceTransformers (BAAI/bge-m3).
- Stores embeddings in ChromaDB for vector search.
- Retrieves relevant documents based on keywords from `base_kb.md`.
- Generates a comprehensive constitution using Azure AI Foundry's LLM models.

## Setup

Use uv to manage the environment.

```bash
uv venv --python 3.13
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -r requirements.txt
```

## Configuration

- **config.json**: Define repositories to clone with URLs and branches.
- **base_kb.md**: List keywords (one per line) for retrieval.
- **.env**: Set Azure AI Foundry credentials:
  - `AZURE_OPENAI_API_KEY`
  - `AZURE_OPENAI_ENDPOINT`
  - `AZURE_OPENAI_API_VERSION`
  - `AZURE_OPENAI_DEPLOYMENT_NAME`

## Run

```bash
uv run python main.py
```

The script will:
- Clone/update repos.
- Process documents.
- Generate embeddings.
- Store in ChromaDB.
- Retrieve top documents per keyword.
- Generate and save constitution to `constitution/` folder.

## Output

- Console logs with timing and retrieved filenames.
- Constitution saved as `constitution/constitution_YYYYMMDD_HHMMSS.md`.

## Dependencies

- LangGraph for workflow orchestration.
- SentenceTransformers for embeddings.
- ChromaDB for vector storage.
- LangChain OpenAI for Azure AI integration.
- GitPython for repo handling.