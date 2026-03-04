# server.py — A tiny web server to test port forwarding
from http.server import HTTPServer, SimpleHTTPRequestHandler

print("Server running at http://localhost:8000")
HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler).serve_forever()
