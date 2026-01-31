"""
Simple static file server for LeaPsychology legal pages.
Designed for Railway deployment.
"""

import os
from http.server import HTTPServer, SimpleHTTPRequestHandler


class LegalPagesHandler(SimpleHTTPRequestHandler):
    """Custom handler for serving legal pages."""

    def do_GET(self):
        # Route handling
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/terms':
            self.path = '/terms.html'
        elif self.path == '/privacy':
            self.path = '/privacy.html'

        return SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")


def run_server():
    port = int(os.environ.get('PORT', 8080))
    server_address = ('', port)

    httpd = HTTPServer(server_address, LegalPagesHandler)
    print(f"LeaPsychology Legal Pages Server")
    print(f"Running on port {port}")
    print(f"Routes:")
    print(f"  / -> Home")
    print(f"  /terms -> Terms of Service")
    print(f"  /privacy -> Privacy Policy")

    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
