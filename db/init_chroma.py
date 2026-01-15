import chromadb
from chromadb.config import Settings

# Initialize Chroma client with persistent storage
def init_chroma_client(persist_directory="./chroma_db"):
    """Initialize Chroma client with local persistent storage."""
    client = chromadb.PersistentClient(path=persist_directory)
    return client

def create_collection(client, collection_name="kb_const_docs"):
    """Create or get a collection for storing documents and embeddings."""
    collection = client.get_or_create_collection(name=collection_name)
    return collection

def add_documents(collection, documents, embeddings=None, metadatas=None, ids=None):
    """Add documents and their embeddings to the collection."""
    if ids is None:
        ids = [f"doc_{i}" for i in range(len(documents))]
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

def query_collection(collection, query_embeddings, n_results=5):
    """Query the collection using pre-computed embeddings."""
    results = collection.query(
        query_embeddings=query_embeddings,
        n_results=n_results
    )
    return results

if __name__ == "__main__":
    # Example usage
    client = init_chroma_client()
    collection = create_collection(client)
    print(f"Chroma collection '{collection.name}' initialized.")
    print(f"Collection count: {collection.count()}")