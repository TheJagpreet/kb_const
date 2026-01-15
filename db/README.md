# Database Setup for KB Const

This folder contains helper scripts to set up a PostgreSQL database with pgvector extension using Podman.

## Prerequisites
- Podman installed
- Python environment with required packages

## Setup Steps

1. **Start the Database Container:**
   ```bash
   ./run_db.sh
   ```
   This will start a PostgreSQL container with pgvector on port 5432.

2. **Initialize the Database:**
   ```bash
   python init_db.py
   ```
   This will enable the vector extension and create necessary tables.

## Usage
- Connect to the database using the config in `init_db.py`.
- The `documents` table is set up to store content with vector embeddings.
- Adjust vector dimensions in `init_db.py` based on your embedding model (e.g., 1536 for OpenAI text-embedding-ada-002).

## Cleanup
To stop and remove the container:
```bash
podman stop kb_const_pgvector
podman rm kb_const_pgvector
```

## Alternative: Chroma Lite DB

For a simpler local vector database, you can use Chroma in embedded mode.

### Setup Steps

1. **Initialize Chroma:**
   ```bash
   python init_chroma.py
   ```
   This will create a persistent Chroma database in `./chroma_db`.

2. **Usage in Code:**
   Use the functions in `init_chroma.py` to add documents and query embeddings.

### Features
- Lightweight and easy to set up.
- Persistent storage on disk.
- No external dependencies like containers.

### Cleanup
To reset the Chroma database, delete the `./chroma_db` folder.