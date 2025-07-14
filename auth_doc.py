import base64
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys

USERNAME = "sager"
PASSWORD = "sager"

class AuthHandler(SimpleHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Sager Area"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        auth_header = self.headers.get('Authorization')
        if auth_header is None:
            self.do_AUTHHEAD()
            # Return here to stop further processing
            return
        method, encoded = auth_header.split(' ', 1)
        if method != 'Basic':
            self.do_AUTHHEAD()
            return
        decoded = base64.b64decode(encoded).decode()
        username, password = decoded.split(':', 1)
        if username == USERNAME and password == PASSWORD:
            super().do_GET()
        else:
            self.do_AUTHHEAD()
            return

if __name__ == '__main__':
    webdir = '/Users/Omar/dev/SagerFirstTask/docss/_build/html'
    # webdir = '/Users/Omar/dev/SagerFirstTask/docs/build/html'
    if not os.path.isdir(webdir):
        print(f"Error: directory does not exist: {webdir}")
        sys.exit(1)
    os.chdir(webdir)
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, AuthHandler)
    print(f"Serving {webdir} on http://localhost:8080 with basic auth")
    httpd.serve_forever()
