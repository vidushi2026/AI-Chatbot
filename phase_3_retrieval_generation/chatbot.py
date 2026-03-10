import json
import os
import urllib.request
import sys

# Add current and phase 2 directories to path for imports
curr_dir = os.path.dirname(__file__)
sys.path.append(curr_dir)
sys.path.append(os.path.join(curr_dir, '..', 'phase_2_processing_indexing'))
from indexer import SimpleIndexer
from prompt_template import SYSTEM_PROMPT

def get_env_variable(var_name):
    """Simple .env loader for standard library usage."""
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith(f"{var_name}="):
                    return line.split("=")[1].strip()
    return os.environ.get(var_name)

class GrowwChatbot:
    def __init__(self):
        chunks_path = os.path.join(os.path.dirname(__file__), '..', 'phase_2_processing_indexing', 'vector_index.json')
        # Fallback to processed_chunks if vector_index hasn't been created yet
        if not os.path.exists(chunks_path):
            chunks_path = os.path.join(os.path.dirname(__file__), '..', 'phase_2_processing_indexing', 'processed_chunks.json')
        
        self.indexer = SimpleIndexer(chunks_path)
        self.api_key = get_env_variable("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def chat(self, user_query):
        # 1. Retrieve Context
        results = self.indexer.search(user_query)
        context = ""
        source_url = "https://groww.in/" # Default if no specific results
        
        if results:
            context_list = []
            for r in results[:5]:
                context_list.append(f"Content: {r['content']}\nSource URL: {r['metadata']['source']}")
            context = "\n---\n".join(context_list)
            source_url = results[0]['metadata']['source']
        else:
            context = "No relevant information found in the database."

        # 2. Prepare Prompt
        prompt = SYSTEM_PROMPT.format(context=context, query=user_query)

        # 3. Call Groq API
        if not self.api_key or self.api_key == "your_key_here":
            # Better simulation for testing: extract the answer from context if available
            if results:
                # Simplistic extraction for simulation
                answer = results[0]['content']
                return f"{answer}\nSource: {source_url}"
            return f"[SIMULATED RESPONSE - NO API KEY]\nI'm sorry, I don't have information about that in my records.\nSource: {source_url}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; GrowwBot/1.0)"
        }
        
        # Using a supported modern model
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a helpful Groww assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.0
        }

        try:
            req = urllib.request.Request(self.api_url, data=json.dumps(data).encode(), headers=headers)
            with urllib.request.urlopen(req) as response:
                resp_data = json.loads(response.read().decode())
                return resp_data['choices'][0]['message']['content']
        except urllib.error.HTTPError as e:
            error_msg = e.read().decode()
            try:
                error_json = json.loads(error_msg)
                return f"Groq API Error: {error_json.get('error', {}).get('message', error_msg)}"
            except:
                return f"Groq API Error: {error_msg}"
        except Exception as e:
            return f"Error connecting to Groq: {str(e)}"

if __name__ == "__main__":
    bot = GrowwChatbot()
    print("Groww RAG Chatbot initialized (Phase 3). Type your query below.")
    while True:
        try:
            query = input("\nUser: ")
            if query.lower() in ["exit", "quit"]: break
            response = bot.chat(query)
            print(f"\nBot: {response}")
        except KeyboardInterrupt:
            break
