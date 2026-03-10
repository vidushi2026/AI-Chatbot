import sys
import os
import json

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from phase_2_processing_indexing.indexer import SimpleIndexer

def run_health_check():
    print("--- Running Post-Update Health Check ---")
    
    # Paths
    processed_data_path = os.path.join(os.path.dirname(__file__), '..', 'phase_2_processing_indexing', 'processed_data.json')
    vector_index_path = os.path.join(os.path.dirname(__file__), '..', 'phase_2_processing_indexing', 'vector_index.json')

    # 1. Verify files exist
    for path in [processed_data_path, vector_index_path]:
        if not os.path.exists(path):
            print(f"FAILED: File missing at {path}")
            return False
        
    # 2. Verify JSON integrity and source links
    try:
        with open(processed_data_path, 'r') as f:
            chunks = json.load(f)
            print(f"INFO: Found {len(chunks)} chunks in knowledge base.")
            
            if not chunks:
                print("FAILED: Knowledge base is empty.")
                return False
                
            # Check for source links in every chunk
            for i, chunk in enumerate(chunks):
                if 'metadata' not in chunk or 'source' not in chunk['metadata'] or not chunk['metadata']['source'].startswith('http'):
                    print(f"FAILED: Chunk {i} is missing a valid source link.")
                    return False
            print("PASS: Source link verification complete.")
    except Exception as e:
        print(f"FAILED: Could not validate data integrity. {str(e)}")
        return False

    # 3. Verify core retrieval
    indexer = SimpleIndexer(vector_index_path)
    test_queries = ["Motilal Midcap", "ELSS lock-in", "exit load"]
    for query in test_queries:
        results = indexer.search(query)
        if not results:
            print(f"FAILED: No results for critical query '{query}'.")
            return False
        # Verify result has content and source
        if not results[0].get('content') or not results[0]['metadata'].get('source'):
             print(f"FAILED: Malformed result for query '{query}'.")
             return False
        print(f"PASS: Query '{query}' returned valid, attributed results.")

    print("--- Health Check PASSED ---")
    return True

if __name__ == "__main__":
    success = run_health_check()
    sys.exit(0 if success else 1)
