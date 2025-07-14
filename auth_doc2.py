import base64
import os
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

USERNAME = "sager"
PASSWORD = "sager"
DOCS_DIR = os.path.abspath("docs/build/html")  # Adjust if needed
SOURCE_DIR = os.path.abspath("docs/source")


class AuthHandler(SimpleHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Sager Docs"')
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        auth_header = self.headers.get("Authorization")
        if auth_header is None:
            self.do_AUTHHEAD()
            return
        method, encoded = auth_header.split(" ", 1)
        if method != "Basic":
            self.do_AUTHHEAD()
            return
        decoded = base64.b64decode(encoded).decode()
        username, password = decoded.split(":", 1)
        if username == USERNAME and password == PASSWORD:
            return super().do_GET()
        else:
            self.do_AUTHHEAD()
            return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def run():
    print(f"[🚀] Launching sphinx-autobuild at http://localhost:8000")
    subprocess.run([
        "sphinx-autobuild",
        SOURCE_DIR,
        DOCS_DIR,
        "--port", "8000",
        "--open-browser"
    ])

if __name__ == "__main__":
    run()
