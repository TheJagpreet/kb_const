#!/usr/bin/env python3

import chromadb
from chromadb.config import Settings

def run_chroma_server(host="127.0.0.1", port=8000, persist_directory="./chroma_db"):
    """Run Chroma server locally."""
    # Note: Chroma server mode requires additional setup
    # For embedded mode, use init_chroma.py instead
    print("For local Chroma usage, use the embedded client in init_chroma.py")
    print("To run a server, install chroma and run: chroma run --host 127.0.0.1 --port 8000")

    # Alternative: Use HTTP client to connect to a running server
    # client = chromadb.HttpClient(host=host, port=port)
    # But for local lite db, embedded is preferred

if __name__ == "__main__":
    run_chroma_server()