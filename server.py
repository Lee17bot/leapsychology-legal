"""
Simple static file server for LeaPsychology legal pages.
Designed for Railway deployment with TikTok verification support.
"""

import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Change to the directory where the script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class LegalPagesHandler(BaseHTTPRequestHandler):
    """Custom handler for serving legal pages with TikTok support."""

    def send_html_response(self, content, status=200):
        """Send HTML response with proper headers."""
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(content.encode('utf-8')))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def send_json_response(self, data, status=200):
        """Send JSON response."""
        content = json.dumps(data)
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(content.encode('utf-8')))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        # Route handling
        if path == '/' or path == '':
            self.serve_file('index.html')
        elif path == '/terms' or path == '/terms.html':
            self.serve_file('terms.html')
        elif path == '/privacy' or path == '/privacy.html':
            self.serve_file('privacy.html')
        elif path == '/callback':
            # TikTok OAuth callback
            code = query.get('code', [''])[0]
            error = query.get('error', [''])[0]

            if error:
                html = f"""<!DOCTYPE html>
<html><head><title>Error</title></head>
<body style="font-family: sans-serif; padding: 50px; text-align: center;">
<h1>Authorization Error</h1>
<p>Error: {error}</p>
<p>{query.get('error_description', [''])[0]}</p>
</body></html>"""
            elif code:
                html = f"""<!DOCTYPE html>
<html><head><title>Success</title></head>
<body style="font-family: sans-serif; padding: 50px; text-align: center;">
<h1>Authorization Successful!</h1>
<p>Your authorization code is:</p>
<div style="background: #f0f0f0; padding: 20px; margin: 20px; border-radius: 10px; word-break: break-all;">
<code style="font-size: 18px;">{code}</code>
</div>
<p>Copy this code and send it to complete the setup.</p>
</body></html>"""
            else:
                html = """<!DOCTYPE html>
<html><head><title>Callback</title></head>
<body style="font-family: sans-serif; padding: 50px; text-align: center;">
<h1>OAuth Callback</h1>
<p>Waiting for authorization...</p>
</body></html>"""

            self.send_html_response(html)
        elif path == '/health' or path == '/ping':
            # Health check endpoint
            self.send_json_response({"status": "ok", "service": "leapsychology-legal"})
        elif path == '/robots.txt':
            content = "User-agent: *\nAllow: /"
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            self.send_error(404, "Page not found")

    def do_HEAD(self):
        """Handle HEAD requests for URL verification."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path in ['/', '/terms', '/privacy', '/callback', '/terms.html', '/privacy.html']:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def serve_file(self, filename):
        """Serve a static HTML file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_html_response(content)
        except FileNotFoundError:
            self.send_error(404, f"File {filename} not found")

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}", flush=True)


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
    print(f"  /         -> Home", flush=True)
    print(f"  /terms    -> Terms of Service", flush=True)
    print(f"  /privacy  -> Privacy Policy", flush=True)
    print(f"  /callback -> OAuth Callback", flush=True)
    print(f"  /health   -> Health Check", flush=True)
    print(f"========================================", flush=True)

    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, LegalPagesHandler)

    print(f"Server running on http://0.0.0.0:{port}", flush=True)
    sys.stdout.flush()

    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
