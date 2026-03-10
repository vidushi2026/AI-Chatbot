import http.server
import socketserver
import json
import os
import sys
from urllib.parse import urlparse, parse_qs

# Add project root to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from phase_3_retrieval_generation.chatbot import GrowwChatbot

PORT = 8000
DIRECTORY = os.path.join(os.path.dirname(__file__), "static")

class GrowwHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            query = data.get('query', '')
            
            try:
                chatbot = GrowwChatbot()
                response = chatbot.chat(query)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                res_body = json.dumps({'response': response})
                self.wfile.write(res_body.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
        else:
            super().do_POST()

if __name__ == "__main__":
    # Ensure static directory exists
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
        
    print(f"Starting server at http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), GrowwHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server...")
            httpd.shutdown()
