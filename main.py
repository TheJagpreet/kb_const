"""
Main entry point for the KB Const application.

This script builds the LangGraph workflow and executes it to generate a knowledge base constitution.
"""

from src.graph_builder import build_graph

if __name__ == "__main__":
    app = build_graph()
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
    constitution_path = result.get('constitution_path', '')
    if constitution:
        print(f"\n--- Generated Constitution ---")
        print(f"Constitution saved to: {constitution_path}")
    else:
        print("No constitution generated.")
    print("------------------------------------------------------")