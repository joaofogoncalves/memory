"""Fetch and parse LinkedIn posts from API responses."""

import logging
import re
from datetime import datetime
from typing import List, Optional, Dict
from scraper.models import LinkedInPost, Media
from scraper.utils import extract_hashtags, parse_linkedin_date


logger = logging.getLogger('linkedin_scraper.fetcher')


class PostFetcher:
    """Parse LinkedIn API responses into Post objects."""

    def __init__(self, linkedin_client):
        """
        Initialize post fetcher.

        Args:
            linkedin_client: LinkedInClient instance
        """
        self.client = linkedin_client

    def fetch_all_posts(self, author_urn: str, limit: Optional[int] = None) -> List[LinkedInPost]:
        """
        Fetch and parse all posts for a user.

        Args:
            author_urn: LinkedIn person URN
            limit: Maximum number of posts to fetch

        Returns:
            List of LinkedInPost objects
        """
        logger.info(f"Fetching posts for {author_urn}...")
        raw_posts = self.client.get_all_posts(author_urn, limit=limit)

        parsed_posts = []
        for raw_post in raw_posts:
            try:
                post = self._parse_post(raw_post)
                if post:
                    parsed_posts.append(post)
            except Exception as e:
                post_id = raw_post.get('id', 'unknown')
                logger.error(f"Failed to parse post {post_id}: {e}")
                continue

        logger.info(f"Successfully parsed {len(parsed_posts)} posts")
        return parsed_posts

    def _parse_post(self, raw_data: Dict) -> Optional[LinkedInPost]:
        """
        Parse raw API response into LinkedInPost object.

        Args:
            raw_data: Raw post data from LinkedIn API

        Returns:
            LinkedInPost object or None
        """
        try:
            # Extract basic fields
            post_id = raw_data.get('id', '')
            if not post_id:
                logger.warning("Post missing ID, skipping")
                return None

            # Get post content
            specific_content = raw_data.get('specificContent', {})
            share_content = specific_content.get('com.linkedin.ugc.ShareContent', {})

            # Extract text content
            share_commentary = share_content.get('shareCommentary', {})
            content = share_commentary.get('text', '')

            # Get creation timestamp
            created = raw_data.get('created', {})
            created_at = parse_linkedin_date(str(created.get('time', 0)))
            if not created_at:
                created_at = datetime.now()

            # Generate post URL
            post_url = self._generate_post_url(post_id)

            # Determine post type and extract media
            post_type = self._determine_post_type(raw_data)
            media = self._extract_media(raw_data)

            # Extract hashtags
            hashtags = extract_hashtags(content)

            # Handle reposts
            original_post_url = None
            repost_commentary = None
            if post_type == 'repost':
                reshare_context = raw_data.get('reshareContext', {})
                if reshare_context:
                    parent_post = reshare_context.get('parent')
                    if parent_post:
                        original_post_url = self._generate_post_url(parent_post)
                    repost_commentary = content

            # Get author info if available
            author = raw_data.get('author', '')
            author_name = None
            author_headline = None

            # Create LinkedInPost object
            post = LinkedInPost(
                id=post_id,
                post_url=post_url,
                content=content,
                created_at=created_at,
                post_type=post_type,
                media=media,
                hashtags=hashtags,
                original_post_url=original_post_url,
                repost_commentary=repost_commentary,
                author_name=author_name,
                author_headline=author_headline
            )

            return post

        except Exception as e:
            logger.error(f"Error parsing post: {e}")
            return None

    def _determine_post_type(self, raw_data: Dict) -> str:
        """
        Determine the type of post.

        Args:
            raw_data: Raw post data

        Returns:
            Post type string
        """
        # Check if it's a reshare/repost
        if 'reshareContext' in raw_data and raw_data['reshareContext']:
            return 'repost'

        # Check for article
        specific_content = raw_data.get('specificContent', {})
        share_content = specific_content.get('com.linkedin.ugc.ShareContent', {})

        if 'article' in share_content or 'shareMediaCategory' in share_content:
            media_category = share_content.get('shareMediaCategory', '')
            if media_category == 'ARTICLE':
                return 'article'

        # Check for poll
        if 'poll' in share_content:
            return 'poll'

        # Default to original post
        return 'original'

    def _extract_media(self, raw_data: Dict) -> List[Media]:
        """
        Extract media attachments from post.

        Args:
            raw_data: Raw post data

        Returns:
            List of Media objects
        """
        media_list = []

        try:
            specific_content = raw_data.get('specificContent', {})
            share_content = specific_content.get('com.linkedin.ugc.ShareContent', {})

            # Get media array
            media_array = share_content.get('media', [])

            for idx, media_item in enumerate(media_array):
                # Get media URL
                media_data = media_item.get('media')
                if not media_data:
                    continue

                # Determine media type
                media_type = 'image'  # Default

                # Try to get download URL
                download_url = media_item.get('originalUrl', '')

                if not download_url:
                    # Try alternative fields
                    thumbnails = media_item.get('thumbnails', [])
                    if thumbnails:
                        download_url = thumbnails[0].get('url', '')

                if download_url:
                    media_obj = Media(
                        type=media_type,
                        url=download_url,
                        filename=f"{media_type}-{idx + 1}"
                    )
                    media_list.append(media_obj)

        except Exception as e:
            logger.warning(f"Failed to extract media: {e}")

        return media_list

    def _generate_post_url(self, post_id: str) -> str:
        """
        Generate LinkedIn post URL from post ID.

        Args:
            post_id: LinkedIn post ID (URN)

        Returns:
            Full LinkedIn post URL
        """
        # Extract activity ID from URN
        # Format: urn:li:share:7012345678901234567 or urn:li:ugcPost:7012345678901234567
        activity_id = post_id.split(':')[-1]
        return f"https://www.linkedin.com/feed/update/urn:li:activity:{activity_id}/"

    def _is_repost(self, raw_data: Dict) -> bool:
        """
        Check if post is a repost/reshare.

        Args:
            raw_data: Raw post data

        Returns:
            True if repost, False otherwise
        """
        return 'reshareContext' in raw_data and bool(raw_data['reshareContext'])
