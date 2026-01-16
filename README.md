# KB Const

A Python project for generating knowledge base constitutions using LangGraph, ChromaDB, and Azure AI Foundry.

## Overview

This project automates the creation of a "constitution" (a synthesized specification document) from domain-specific knowledge files. It:

- Clones GitHub repositories containing knowledge base content.
- Collects and processes documents (Markdown, text, Python files).
- Creates embeddings using SentenceTransformers (BAAI/bge-m3).
- Stores embeddings in ChromaDB for vector search.
- Retrieves relevant documents based on keywords from `config/keywords.md`.
- Re-ranks retrieved documents using cross-encoder for better relevance.
- Generates a comprehensive constitution using Azure AI Foundry's LLM models.

## Project Structure

The codebase is organized into modular components for maintainability:

- `src/`: Main source code directory
  - `__init__.py`: Package initialization
  - `state.py`: Defines the LangGraph state TypedDict
  - `data_fetching.py`: Handles repository cloning and document collection
  - `keywords.py`: Reads keywords from config/keywords.md
  - `embeddings.py`: Creates embeddings using SentenceTransformers
  - `db_operations.py`: Manages ChromaDB storage and retrieval
  - `reranking.py`: Re-ranks retrieved documents for better relevance
  - `llm_generation.py`: Generates constitution using Azure OpenAI
  - `graph_builder.py`: Defines and compiles the LangGraph workflow
- `main.py`: Entry point that builds and runs the workflow
- `config/`: Configuration files directory
  - `config.json`: Repository configuration
  - `keywords.md`: Keywords for retrieval
  - `.env.example`: Sample environment variables file

## Configuration

- **config/config.json**: Define repositories to clone with URLs and branches.
- **config/keywords.md**: List keywords (one per line) for retrieval.
- **.env**: Set Azure AI Foundry credentials in root directory (copy from `config/.env.example`):
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
- Re-rank documents for relevance.
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