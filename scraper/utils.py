"""Utility functions for the LinkedIn scraper."""

import json
import os
import re
import logging
import yaml
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from slugify import slugify as make_slug
from dotenv import load_dotenv


def setup_logging(config: dict) -> logging.Logger:
    """Configure and return logger with file and console handlers."""
    import coloredlogs

    log_level = config.get('logging', {}).get('level', 'INFO')
    log_file = config.get('logging', {}).get('file', 'logs/scraper.log')

    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    # Configure root logger
    logger = logging.getLogger('linkedin_scraper')
    logger.setLevel(getattr(logging, log_level))

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, log_level))
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler with colors
    coloredlogs.install(
        level=log_level,
        logger=logger,
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    return logger


def load_config(config_path: str = 'config/config.yaml') -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def load_env_vars():
    """Load environment variables from .env file."""
    load_dotenv()

    client_id = os.getenv('LINKEDIN_CLIENT_ID')
    client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
    redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')

    if not all([client_id, client_secret, redirect_uri]):
        raise ValueError(
            "Missing required environment variables. "
            "Please set LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, and LINKEDIN_REDIRECT_URI in .env file."
        )

    return {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri
    }


def slugify_post(content: str, date: datetime, max_length: int = 60) -> str:
    """
    Generate a URL-safe slug from post content and date.

    Format: DD-first-words-of-post (zero-padded day prefix). Year and month
    live in the directory path (posts/YYYY/MM/) and the full date in
    frontmatter, so only the day is carried in the leaf directory name.
    """
    # Format day prefix (zero-padded, e.g. "08", "11")
    date_prefix = date.strftime('%d')

    # Clean content: remove URLs, hashtags, mentions, and extra whitespace
    clean_content = re.sub(r'http\S+', '', content)
    clean_content = re.sub(r'#\w+', '', clean_content)
    clean_content = re.sub(r'@\w+', '', clean_content)
    clean_content = re.sub(r'\s+', ' ', clean_content).strip()

    # Get first few words
    words = clean_content.split()[:8]
    content_part = ' '.join(words)

    # Create slug
    slug = make_slug(content_part, max_length=max_length - len(date_prefix) - 1)

    return f"{date_prefix}-{slug}" if slug else date_prefix


def sanitize_filename(filename: str) -> str:
    """Remove or replace characters that are unsafe for filenames."""
    # Remove or replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with hyphens
    filename = filename.replace(' ', '-')
    # Remove multiple hyphens
    filename = re.sub(r'-+', '-', filename)
    # Trim and limit length
    return filename[:255].strip('-')


def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from text."""
    if not text:
        return []

    hashtags = re.findall(r'#(\w+)', text)
    return list(set(hashtags))  # Remove duplicates


def create_directory(path: str) -> Path:
    """Create directory if it doesn't exist and return Path object."""
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_unique_slug(base_slug: str, existing_slugs: List[str]) -> str:
    """
    Generate a unique slug by appending a number if necessary.

    Example: post-title -> post-title-2 -> post-title-3
    """
    if base_slug not in existing_slugs:
        return base_slug

    counter = 2
    while f"{base_slug}-{counter}" in existing_slugs:
        counter += 1

    return f"{base_slug}-{counter}"


def format_datetime(dt: datetime, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """Format datetime object to string."""
    return dt.strftime(format_str)


def parse_linkedin_date(date_str: str) -> Optional[datetime]:
    """Parse LinkedIn API date string to datetime object."""
    try:
        # LinkedIn typically uses Unix timestamp in milliseconds
        timestamp = int(date_str) / 1000
        return datetime.fromtimestamp(timestamp)
    except (ValueError, TypeError):
        return None


def decode_linkedin_timestamp(url_or_id: str) -> Optional[datetime]:
    """Decode a post's exact creation time from its LinkedIn activity/share ID.

    LinkedIn's 64-bit post IDs encode the creation time in their high bits: the
    first 41 bits are the Unix timestamp in milliseconds, so ``id >> 22`` yields
    milliseconds since the Unix epoch. The numeric ID appears in both URL forms
    the scraper handles:
      - activity URN: ``.../feed/update/urn:li:activity:<id>/``
      - share URL:    ``.../posts/<slug>-share-<id>-<suffix>/``

    This is exact (to the second) and works retroactively, unlike the relative
    timestamp ("2w", "1mo") the feed shows, which only yields an approximate date.

    Args:
        url_or_id: A LinkedIn post URL or the bare numeric ID.

    Returns:
        A timezone-aware UTC datetime, or None if no plausible ID is found.
    """
    if not url_or_id:
        return None
    text = str(url_or_id)
    match = re.search(r'urn:li:activity:(\d+)', text) or re.search(r'(\d{15,})', text)
    if not match:
        return None
    try:
        ms = int(match.group(1)) >> 22
        dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    except (ValueError, OverflowError, OSError):
        return None
    # Sanity bound: reject IDs that decode to an implausible year.
    if not (2010 <= dt.year <= 2035):
        return None
    return dt


def parse_relative_date(text: str) -> Optional[datetime]:
    """
    Parse LinkedIn relative date strings to datetime.

    Examples: '2h', '3d', '1w', '2mo', '1yr', '30m', '5s',
              '2 hours', '3 days ago', '1 week'
    """
    text = text.strip().lower().rstrip('.')
    text = text.replace(' ago', '')

    patterns = [
        (r'(\d+)\s*s(?:ec(?:ond)?s?)?$', 'seconds'),
        (r'(\d+)\s*m(?:in(?:ute)?s?)?$', 'minutes'),
        (r'(\d+)\s*h(?:(?:ou)?rs?)?$', 'hours'),
        (r'(\d+)\s*d(?:ays?)?$', 'days'),
        (r'(\d+)\s*w(?:(?:ee)?ks?)?$', 'weeks'),
        (r'(\d+)\s*mo(?:nths?)?$', 'months'),
        (r'(\d+)\s*yr?(?:(?:ea)?rs?)?$', 'years'),
    ]

    for pattern, unit in patterns:
        match = re.match(pattern, text)
        if match:
            value = int(match.group(1))
            now = datetime.now()
            if unit == 'seconds':
                return now - timedelta(seconds=value)
            elif unit == 'minutes':
                return now - timedelta(minutes=value)
            elif unit == 'hours':
                return now - timedelta(hours=value)
            elif unit == 'days':
                return now - timedelta(days=value)
            elif unit == 'weeks':
                return now - timedelta(weeks=value)
            elif unit == 'months':
                return now - timedelta(days=value * 30)
            elif unit == 'years':
                return now - timedelta(days=value * 365)

    return None


def load_checkpoint(path: str = 'cache/crawl_checkpoint.json') -> Optional[Dict]:
    """Load crawl checkpoint from disk."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_checkpoint(data: Dict, path: str = 'cache/crawl_checkpoint.json') -> None:
    """Save crawl checkpoint to disk."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, default=str)
