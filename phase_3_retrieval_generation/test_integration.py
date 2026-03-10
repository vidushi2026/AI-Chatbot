import sys
import os

# Add relevant directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'phase_3_retrieval_generation'))
from chatbot import GrowwChatbot

def test_integration():
    bot = GrowwChatbot()
    
    # User's specific test case
    query = "What is the expense ratio of Motilal Oswal Midcap Fund Direct Growth?"
    print(f"Testing Query: {query}")
    
    # We will check if the indexer finds the right chunk first
    results = bot.indexer.search(query)
    if results:
        print(f"Indexer found {len(results)} relevant chunks.")
        print(f"Top result: {results[0]['content']}")
        print(f"Source URL: {results[0]['metadata']['source']}")
    else:
        print("Indexer failed to find relevant chunks.")
        return

    # Simulate or run the chat
    response = bot.chat(query)
    print(f"\nChatbot Response:\n{response}")

    # Validation
    expected_value = "0.82%"
    expected_url = "https://groww.in/mutual-funds/motilal-oswal-most-focused-midcap-30-fund-direct-growth"
    
    if expected_value in response and expected_url in response:
        print("\nTEST PASSED: Correct value and URL found in response.")
    else:
        print("\nTEST FAILED: Missing expected value or URL.")

if __name__ == "__main__":
    test_integration()
