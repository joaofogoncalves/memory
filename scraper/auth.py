"""OAuth 2.0 authentication for LinkedIn API."""

import json
import logging
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, urlparse, parse_qs
from pathlib import Path
from typing import Optional, Dict
import requests


logger = logging.getLogger('linkedin_scraper.auth')


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler to catch OAuth callback."""

    auth_code = None

    def do_GET(self):
        """Handle GET request from OAuth callback."""
        # Parse query parameters
        query_components = parse_qs(urlparse(self.path).query)

        if 'code' in query_components:
            CallbackHandler.auth_code = query_components['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <body>
                    <h1>Authentication Successful!</h1>
                    <p>You can close this window and return to the terminal.</p>
                    <script>window.close();</script>
                </body>
                </html>
            """)
        elif 'error' in query_components:
            error = query_components.get('error', ['Unknown error'])[0]
            error_desc = query_components.get('error_description', [''])[0]
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"""
                <html>
                <body>
                    <h1>Authentication Failed</h1>
                    <p>Error: {error}</p>
                    <p>{error_desc}</p>
                </body>
                </html>
            """.encode())
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


class LinkedInAuthenticator:
    """Handle OAuth 2.0 authentication flow for LinkedIn."""

    AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
    TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
    SCOPES = ['openid', 'profile', 'email', 'w_member_social']

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str,
                 token_cache_path: str = 'cache/token.json'):
        """
        Initialize authenticator.

        Args:
            client_id: LinkedIn app client ID
            client_secret: LinkedIn app client secret
            redirect_uri: OAuth redirect URI (must match app settings)
            token_cache_path: Path to store cached access token
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_cache_path = Path(token_cache_path)
        self.access_token = None

        # Ensure cache directory exists
        self.token_cache_path.parent.mkdir(parents=True, exist_ok=True)

    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        Get valid access token, using cache or triggering new OAuth flow.

        Args:
            force_refresh: Force new OAuth flow even if token is cached

        Returns:
            Valid access token
        """
        if not force_refresh:
            cached_token = self._load_cached_token()
            if cached_token:
                logger.info("Using cached access token")
                self.access_token = cached_token
                return cached_token

        logger.info("Starting OAuth 2.0 authentication flow...")
        auth_code = self._start_oauth_flow()

        if not auth_code:
            raise Exception("Failed to obtain authorization code")

        logger.info("Exchanging authorization code for access token...")
        token = self._exchange_code_for_token(auth_code)

        self._save_token(token)
        self.access_token = token['access_token']

        return self.access_token

    def _start_oauth_flow(self) -> Optional[str]:
        """
        Start OAuth flow by opening browser and running local server.

        Returns:
            Authorization code or None
        """
        # Build authorization URL
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.SCOPES)
        }
        auth_url = f"{self.AUTH_URL}?{urlencode(params)}"

        logger.info(f"Opening browser for authentication...")
        logger.info(f"If browser doesn't open, visit: {auth_url}")

        # Open browser
        webbrowser.open(auth_url)

        # Start local server to catch callback
        port = int(urlparse(self.redirect_uri).port or 8080)
        server = HTTPServer(('localhost', port), CallbackHandler)

        logger.info(f"Waiting for callback on http://localhost:{port}/callback ...")

        # Wait for one request (the callback)
        server.handle_request()

        auth_code = CallbackHandler.auth_code
        return auth_code

    def _exchange_code_for_token(self, auth_code: str) -> Dict:
        """
        Exchange authorization code for access token.

        Args:
            auth_code: Authorization code from OAuth callback

        Returns:
            Token response dictionary
        """
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        try:
            response = requests.post(self.TOKEN_URL, data=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to exchange code for token: {e}")
            raise

    def _save_token(self, token: Dict):
        """Save token to cache file."""
        try:
            with open(self.token_cache_path, 'w') as f:
                json.dump(token, f, indent=2)
            logger.info(f"Token saved to {self.token_cache_path}")
        except Exception as e:
            logger.warning(f"Failed to save token to cache: {e}")

    def _load_cached_token(self) -> Optional[str]:
        """Load token from cache file if it exists."""
        if not self.token_cache_path.exists():
            return None

        try:
            with open(self.token_cache_path, 'r') as f:
                token_data = json.load(f)
                return token_data.get('access_token')
        except Exception as e:
            logger.warning(f"Failed to load cached token: {e}")
            return None

    def clear_cache(self):
        """Clear cached token."""
        if self.token_cache_path.exists():
            self.token_cache_path.unlink()
            logger.info("Token cache cleared")
