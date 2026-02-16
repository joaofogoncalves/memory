"""Parse LinkedIn data export files and convert to Post objects."""

import json
import logging
import zipfile
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict
from scraper.models import LinkedInPost, Media
from scraper.utils import extract_hashtags


logger = logging.getLogger('linkedin_scraper.export_parser')


class LinkedInExportParser:
    """Parse LinkedIn's data export JSON files."""

    def __init__(self, export_path: str):
        """
        Initialize parser with path to LinkedIn export.

        Args:
            export_path: Path to LinkedIn export ZIP file or extracted directory
        """
        self.export_path = Path(export_path)
        self.temp_dir = None

    def parse_export(self) -> List[LinkedInPost]:
        """
        Parse LinkedIn export and return list of posts.

        Returns:
            List of LinkedInPost objects
        """
        # Check if it's a ZIP file or directory
        if self.export_path.is_file() and self.export_path.suffix == '.zip':
            return self._parse_zip()
        elif self.export_path.is_dir():
            return self._parse_directory(self.export_path)
        else:
            raise ValueError(f"Invalid export path: {self.export_path}")

    def _parse_zip(self) -> List[LinkedInPost]:
        """Extract and parse ZIP file."""
        import tempfile
        import shutil

        logger.info(f"Extracting ZIP file: {self.export_path}")

        # Create temporary directory
        self.temp_dir = Path(tempfile.mkdtemp())

        try:
            # Extract ZIP
            with zipfile.ZipFile(self.export_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)

            logger.info(f"Extracted to: {self.temp_dir}")

            # Parse extracted directory
            return self._parse_directory(self.temp_dir)

        finally:
            # Cleanup temporary directory
            if self.temp_dir and self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)

    def _parse_directory(self, directory: Path) -> List[LinkedInPost]:
        """
        Parse LinkedIn export directory.

        Args:
            directory: Path to extracted export directory

        Returns:
            List of LinkedInPost objects
        """
        posts = []

        # LinkedIn export typically has these files:
        # - Posts.csv or Posts.json
        # - Share.csv or Shares.json
        # Look for posts files
        posts_files = [
            'Posts.json',
            'posts.json',
            'Share.json',
            'share.json',
            'Posts.csv',
            'Shares.csv'
        ]

        for filename in posts_files:
            file_path = directory / filename
            if file_path.exists():
                logger.info(f"Found posts file: {filename}")

                if filename.endswith('.json'):
                    posts.extend(self._parse_json_file(file_path))
                elif filename.endswith('.csv'):
                    posts.extend(self._parse_csv_file(file_path))

        logger.info(f"Parsed {len(posts)} posts from export")
        return posts

    def _parse_json_file(self, file_path: Path) -> List[LinkedInPost]:
        """Parse JSON posts file."""
        posts = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # LinkedIn export format can vary
            # Try different structures
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict) and 'elements' in data:
                items = data['elements']
            else:
                logger.warning(f"Unknown JSON structure in {file_path}")
                return posts

            for item in items:
                post = self._parse_post_item(item)
                if post:
                    posts.append(post)

        except Exception as e:
            logger.error(f"Failed to parse JSON file {file_path}: {e}")

        return posts

    def _parse_csv_file(self, file_path: Path) -> List[LinkedInPost]:
        """Parse CSV posts file."""
        import csv

        posts = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    post = self._parse_csv_row(row)
                    if post:
                        posts.append(post)

        except Exception as e:
            logger.error(f"Failed to parse CSV file {file_path}: {e}")

        return posts

    def _parse_post_item(self, item: Dict) -> Optional[LinkedInPost]:
        """
        Parse a single post item from JSON.

        Args:
            item: Dictionary containing post data

        Returns:
            LinkedInPost object or None
        """
        try:
            # Extract fields (LinkedIn export format)
            post_id = item.get('id', item.get('ID', ''))
            content = item.get('text', item.get('commentary', item.get('Text', '')))

            # Parse date
            date_str = item.get('date', item.get('Date', item.get('createdAt', '')))
            created_at = self._parse_date(date_str)

            # Generate URL (if available)
            post_url = item.get('url', item.get('URL', item.get('link', '')))
            if not post_url:
                post_url = f"https://www.linkedin.com/feed/update/{post_id}/"

            # Extract hashtags
            hashtags = extract_hashtags(content)

            # Determine post type
            post_type = 'original'
            if item.get('resharedPost') or item.get('isReshare'):
                post_type = 'repost'

            # Extract media (if present)
            media = self._extract_media_from_item(item)

            # Create post object
            post = LinkedInPost(
                id=post_id or f"export-{hash(content)}",
                post_url=post_url,
                content=content,
                created_at=created_at,
                post_type=post_type,
                media=media,
                hashtags=hashtags
            )

            return post

        except Exception as e:
            logger.error(f"Failed to parse post item: {e}")
            return None

    def _parse_csv_row(self, row: Dict) -> Optional[LinkedInPost]:
        """Parse a single CSV row."""
        try:
            # CSV format from LinkedIn export
            content = row.get('ShareCommentary', row.get('Text', row.get('Content', '')))
            date_str = row.get('Date', row.get('CreatedAt', ''))
            link = row.get('ShareLink', row.get('Link', ''))

            created_at = self._parse_date(date_str)

            post = LinkedInPost(
                id=f"csv-{hash(content + date_str)}",
                post_url=link or f"https://www.linkedin.com/feed/",
                content=content,
                created_at=created_at,
                post_type='original',
                media=[],
                hashtags=extract_hashtags(content)
            )

            return post

        except Exception as e:
            logger.error(f"Failed to parse CSV row: {e}")
            return None

    def _parse_date(self, date_str: str) -> datetime:
        """
        Parse date string from various formats.

        Args:
            date_str: Date string

        Returns:
            datetime object
        """
        if not date_str:
            return datetime.now()

        # Try common formats
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d/%m/%Y'
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        # If all formats fail, try timestamp
        try:
            timestamp = int(date_str) / 1000  # Milliseconds to seconds
            return datetime.fromtimestamp(timestamp)
        except (ValueError, TypeError):
            logger.warning(f"Could not parse date: {date_str}")
            return datetime.now()

    def _extract_media_from_item(self, item: Dict) -> List[Media]:
        """Extract media URLs from post item."""
        media = []

        # Look for media in various fields
        media_fields = ['media', 'images', 'attachments', 'content']

        for field in media_fields:
            if field in item and item[field]:
                media_data = item[field]

                if isinstance(media_data, list):
                    for media_item in media_data:
                        if isinstance(media_item, str):
                            # Direct URL
                            media.append(Media(type='image', url=media_item))
                        elif isinstance(media_item, dict):
                            # Object with URL
                            url = media_item.get('url', media_item.get('URL', ''))
                            if url:
                                media_type = media_item.get('type', 'image')
                                media.append(Media(type=media_type, url=url))

        return media
