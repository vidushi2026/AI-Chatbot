import sys
from indexer import SimpleIndexer

def verify_search(query):
    indexer = SimpleIndexer("processed_chunks.json")
    results = indexer.search(query)
    
    print(f"--- Verification for Query: '{query}' ---")
    if not results:
        print("No results found.")
        return

    for i, res in enumerate(results[:3]): # Show top 3
        print(f"[{i+1}] Content: {res['content']}")
        print(f"    Source URL: {res['metadata']['source']}")
    print("-" * 40)

if __name__ == "__main__":
    queries = [
        "Motilal Midcap expense ratio",
        "ELSS lock-in",
        "How to download capital gains",
        "Nifty 500 exit load"
    ]
    for q in queries:
        verify_search(q)
