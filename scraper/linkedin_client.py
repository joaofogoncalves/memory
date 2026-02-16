"""LinkedIn API client with rate limiting and error handling."""

import time
import logging
from typing import Dict, List, Optional
import requests
from requests.exceptions import RequestException


logger = logging.getLogger('linkedin_scraper.client')


class LinkedInClient:
    """Client for interacting with LinkedIn API v2."""

    BASE_URL = 'https://api.linkedin.com/v2'
    REST_BASE_URL = 'https://api.linkedin.com/rest'

    def __init__(self, access_token: str, config: dict):
        """
        Initialize LinkedIn API client.

        Args:
            access_token: OAuth 2.0 access token
            config: Configuration dictionary with rate limits and timeouts
        """
        self.access_token = access_token
        self.config = config
        self.rate_limit_delay = config.get('linkedin', {}).get('rate_limit_delay', 1.5)
        self.max_retries = config.get('linkedin', {}).get('max_retries', 3)
        self.timeout = config.get('linkedin', {}).get('timeout', 30)
        self.last_request_time = 0
        self.request_count = 0  # Track API requests

    def _get_headers(self) -> Dict[str, str]:
        """Get standard headers for API requests."""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0',
            'LinkedIn-Version': '202401'
        }

    def _wait_for_rate_limit(self):
        """Implement rate limiting delay."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()

    def _make_request(self, method: str, url: str, **kwargs) -> Optional[Dict]:
        """
        Make HTTP request with retries and error handling.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Full URL to request
            **kwargs: Additional arguments for requests

        Returns:
            Response JSON or None if failed
        """
        self._wait_for_rate_limit()

        headers = self._get_headers()
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))

        kwargs['timeout'] = kwargs.get('timeout', self.timeout)

        for attempt in range(self.max_retries):
            try:
                response = requests.request(method, url, headers=headers, **kwargs)

                if response.status_code == 429:
                    # Rate limited - exponential backoff
                    wait_time = (2 ** attempt) * 2
                    logger.warning(f"Rate limited (429). Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                self.request_count += 1  # Increment request counter
                return response.json() if response.content else {}

            except RequestException as e:
                logger.error(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}")

                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.info(f"Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Max retries reached for {url}")
                    return None

        return None

    def get_user_profile(self) -> Optional[Dict]:
        """
        Get authenticated user's profile information.

        Returns:
            User profile data or None
        """
        url = 'https://api.linkedin.com/v2/userinfo'
        logger.info("Fetching user profile...")

        profile = self._make_request('GET', url)
        if profile:
            logger.info(f"Retrieved profile for: {profile.get('name', 'Unknown')}")
        return profile

    def get_user_posts(self, author_urn: str, start: int = 0, count: int = 50) -> Optional[Dict]:
        """
        Fetch user's posts with pagination.

        Args:
            author_urn: LinkedIn URN for the author (e.g., 'urn:li:person:XXXXX')
            start: Pagination start index
            count: Number of posts to fetch (max 50 per request)

        Returns:
            Posts data or None
        """
        # LinkedIn UGC Posts API endpoint
        url = f"{self.BASE_URL}/ugcPosts"

        params = {
            'q': 'authors',
            'authors': f'List({author_urn})',
            'start': start,
            'count': min(count, 50)  # LinkedIn max is 50 per request
        }

        logger.info(f"Fetching posts (start={start}, count={count})...")
        response = self._make_request('GET', url, params=params)

        if response and 'elements' in response:
            logger.info(f"Retrieved {len(response['elements'])} posts")

        return response

    def get_person_urn(self, profile: Dict) -> Optional[str]:
        """
        Extract person URN from profile data.

        Args:
            profile: User profile dictionary

        Returns:
            Person URN string or None
        """
        # Try to get from 'sub' field (OpenID Connect)
        sub = profile.get('sub')
        if sub:
            return f"urn:li:person:{sub}"

        logger.error("Could not extract person URN from profile")
        return None

    def download_media(self, url: str, output_path: str) -> bool:
        """
        Download media file from URL.

        Args:
            url: Media URL
            output_path: Local path to save file

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.debug(f"Downloading media from {url}")
            response = requests.get(url, stream=True, timeout=self.timeout)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            logger.debug(f"Media saved to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to download media from {url}: {e}")
            return False

    def get_all_posts(self, author_urn: str, limit: Optional[int] = None) -> List[Dict]:
        """
        Fetch all posts from user with pagination.

        Args:
            author_urn: LinkedIn URN for the author
            limit: Maximum number of posts to fetch (None = all)

        Returns:
            List of all posts
        """
        all_posts = []
        start = 0
        count = 50

        while True:
            response = self.get_user_posts(author_urn, start=start, count=count)

            if not response or 'elements' not in response:
                break

            posts = response['elements']
            if not posts:
                break

            all_posts.extend(posts)

            # Check if we've hit the limit
            if limit and len(all_posts) >= limit:
                all_posts = all_posts[:limit]
                break

            # Check if there are more posts
            paging = response.get('paging', {})
            if 'links' not in paging or not any(link.get('rel') == 'next' for link in paging['links']):
                break

            start += count
            logger.info(f"Fetched {len(all_posts)} posts so far...")

        logger.info(f"Total posts fetched: {len(all_posts)}")
        logger.info(f"API requests made: {self.request_count}")
        return all_posts

    def get_request_count(self) -> int:
        """
        Get the number of API requests made in this session.

        Returns:
            Number of requests made
        """
        return self.request_count
