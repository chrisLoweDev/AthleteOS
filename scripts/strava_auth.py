"""
One-time Strava OAuth setup for Athlete OS.

Usage:
    python scripts/strava_auth.py

This script:
1. Reads STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET from .env
2. Opens browser to Strava authorization page
3. Starts a local HTTP server to capture the OAuth callback
4. Exchanges the auth code for tokens
5. Writes STRAVA_REFRESH_TOKEN to .env
"""

import os
import sys
import webbrowser
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import requests
from dotenv import load_dotenv, set_key

# Path to .env — one directory up from this script
ENV_PATH = os.path.join(os.path.dirname(__file__), '..', '.env')

CALLBACK_PORT = 8080
REDIRECT_URI = f'http://localhost:{CALLBACK_PORT}/callback'
TOKEN_URL = 'https://www.strava.com/oauth/token'
AUTH_URL = 'https://www.strava.com/oauth/authorize'
SCOPE = 'activity:read_all'

# Will be set by the callback handler
_auth_code = None


class CallbackHandler(BaseHTTPRequestHandler):
    """Handles the OAuth redirect from Strava."""

    def do_GET(self):
        global _auth_code
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if 'code' in params:
            _auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html><body>
                <h2>Authorization successful!</h2>
                <p>You can close this tab and return to the terminal.</p>
                </body></html>
            """)
        elif 'error' in params:
            error = params.get('error', ['unknown'])[0]
            self.send_response(400)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(f'<html><body><h2>Authorization failed: {error}</h2></body></html>'.encode())
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress default request logging
        pass


def main():
    global _auth_code

    # Load credentials
    load_dotenv(dotenv_path=ENV_PATH)
    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')

    if not client_id or not client_secret:
        print("ERROR: STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET must be set in .env")
        print(f"  .env path: {os.path.abspath(ENV_PATH)}")
        sys.exit(1)

    # Build authorization URL
    auth_url = (
        f"{AUTH_URL}"
        f"?client_id={client_id}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={SCOPE}"
        f"&approval_prompt=auto"
    )

    print("\nAthleteOS — Strava Authorization Setup")
    print("=" * 40)
    print(f"\nOpening browser to authorize Strava access...")
    print(f"If the browser doesn't open, visit this URL manually:\n\n  {auth_url}\n")

    webbrowser.open(auth_url)

    # Start local server to capture callback
    server = HTTPServer(('localhost', CALLBACK_PORT), CallbackHandler)
    print(f"Waiting for authorization callback on port {CALLBACK_PORT}...")

    while _auth_code is None:
        server.handle_request()

    server.server_close()

    # Exchange auth code for tokens
    print("\nExchanging authorization code for tokens...")
    resp = requests.post(TOKEN_URL, data={
        'client_id': client_id,
        'client_secret': client_secret,
        'code': _auth_code,
        'grant_type': 'authorization_code',
    })

    if resp.status_code != 200:
        print(f"ERROR: Token exchange failed ({resp.status_code})")
        print(resp.text)
        sys.exit(1)

    data = resp.json()
    refresh_token = data.get('refresh_token')
    athlete = data.get('athlete', {})
    athlete_name = f"{athlete.get('firstname', '')} {athlete.get('lastname', '')}".strip()

    if not refresh_token:
        print("ERROR: No refresh token in response")
        print(json.dumps(data, indent=2))
        sys.exit(1)

    # Write refresh token to .env
    set_key(ENV_PATH, 'STRAVA_REFRESH_TOKEN', refresh_token)

    print(f"\nSuccess! Authorized as: {athlete_name or 'Unknown athlete'}")
    print(f"Refresh token saved to .env")
    print("\nNext steps:")
    print("  1. Fill in athlete/profile.md with your FTP, HR zones, and goals")
    print("  2. Open Claude Code in this directory: claude")
    print("  3. Run /plan-workouts to create your first training block")


if __name__ == '__main__':
    main()
