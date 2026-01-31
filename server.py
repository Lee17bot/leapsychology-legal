"""
Simple static file server for LeaPsychology legal pages.
Designed for Railway deployment.
"""

import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Change to the directory where the script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class LegalPagesHandler(SimpleHTTPRequestHandler):
    """Custom handler for serving legal pages."""

    def do_GET(self):
        # Route handling
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        elif self.path == '/terms':
            self.path = '/terms.html'
        elif self.path == '/privacy':
            self.path = '/privacy.html'

        return SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):
        print(f"[REQUEST] {args[0]}", flush=True)


def run_server():
    port = int(os.environ.get('PORT', 8080))

    print(f"========================================", flush=True)
    print(f"LeaPsychology Legal Pages Server", flush=True)
    print(f"========================================", flush=True)
    print(f"Port: {port}", flush=True)
    print(f"Working directory: {os.getcwd()}", flush=True)
    print(f"Files: {os.listdir('.')}", flush=True)
    print(f"", flush=True)
    print(f"Routes:", flush=True)
    print(f"  /        -> Home", flush=True)
    print(f"  /terms   -> Terms of Service", flush=True)
    print(f"  /privacy -> Privacy Policy", flush=True)
    print(f"========================================", flush=True)

    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, LegalPagesHandler)

    print(f"Server running on http://0.0.0.0:{port}", flush=True)
    sys.stdout.flush()

    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
