"""
Flask server for LeaPsychology legal pages.
"""

import os
from flask import Flask, send_file, request, jsonify

app = Flask(__name__)

# Get the directory where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def home():
    return send_file(os.path.join(BASE_DIR, 'index.html'))


@app.route('/terms')
@app.route('/terms.html')
def terms():
    return send_file(os.path.join(BASE_DIR, 'terms.html'))


@app.route('/privacy')
@app.route('/privacy.html')
def privacy():
    return send_file(os.path.join(BASE_DIR, 'privacy.html'))


@app.route('/callback')
def callback():
    code = request.args.get('code', '')
    error = request.args.get('error', '')
    error_desc = request.args.get('error_description', '')

    if error:
        return f"""<!DOCTYPE html>
<html><head><title>Error</title></head>
<body style="font-family: sans-serif; padding: 50px; text-align: center;">
<h1>Authorization Error</h1>
<p>Error: {error}</p>
<p>{error_desc}</p>
</body></html>"""

    if code:
        return f"""<!DOCTYPE html>
<html><head><title>Success</title></head>
<body style="font-family: sans-serif; padding: 50px; text-align: center;">
<h1>Authorization Successful!</h1>
<p>Your authorization code is:</p>
<div style="background: #f0f0f0; padding: 20px; margin: 20px; border-radius: 10px; word-break: break-all;">
<code style="font-size: 18px;">{code}</code>
</div>
<p>Copy this code and send it to complete the setup.</p>
</body></html>"""

    return """<!DOCTYPE html>
<html><head><title>Callback</title></head>
<body style="font-family: sans-serif; padding: 50px; text-align: center;">
<h1>OAuth Callback</h1>
<p>Waiting for authorization...</p>
</body></html>"""


@app.route('/health')
@app.route('/ping')
def health():
    return jsonify({"status": "ok", "service": "leapsychology-legal"})


@app.route('/robots.txt')
def robots():
    return "User-agent: *\nAllow: /", 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting LeaPsychology Legal Pages on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
