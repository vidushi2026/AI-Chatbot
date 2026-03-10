import json
import os

class SimpleIndexer:
    def __init__(self, chunks_file):
        with open(chunks_file, 'r') as f:
            self.chunks = json.load(f)
            
    def search(self, query):
        """
        Improved keyword matching: Scores based on keyword matches and exact fund name presence.
        """
        stopwords = {"what", "is", "the", "of", "for", "a", "an", "and", "in", "on", "at", "to", "with"}
        query_lower = query.lower()
        keywords = [kw for kw in query_lower.split() if kw not in stopwords]
        
        results = []
        for chunk in self.chunks:
            content_lower = chunk['content'].lower()
            metadata = chunk.get('metadata', {})
            fund_name = metadata.get('fund_name', '').lower()
            
            # Base score: number of keyword matches
            score = sum(1 for kw in keywords if kw in content_lower)
            
            # Boost for matching fund name exactly in the query
            if fund_name and fund_name in query_lower:
                score += 10 # Massive boost
            
            # Boost if chunk content starts with the fund name (common in our chunks)
            if fund_name and content_lower.startswith(f"the {fund_name}"):
                score += 2
                
            if score > 0:
                results.append((score, chunk))
        
        # Sort by score descending
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results]
if __name__ == "__main__":
    chunks_path = "processed_chunks.json"
    if os.path.exists(chunks_path):
        indexer = SimpleIndexer(chunks_path)
        # Test search
        test_queries = ["expense ratio", "lock-in", "minimum SIP"]
        for q in test_queries:
            results = indexer.search(q)
            print(f"\nQuery: {q}")
            print(f"Found {len(results)} results.")
            if results:
                print(f"Sample Result: {results[0]['content']}")
                print(f"Source: {results[0]['metadata']['source']}")
    else:
        print(f"Error: {chunks_path} not found. Run processor.py first.")
