"""Main entry point for LinkedIn Post Archiver."""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

import re

from scraper.utils import (
    setup_logging,
    load_config,
    load_env_vars,
    slugify_post,
    get_unique_slug,
    create_directory
)
from scraper.media_downloader import MediaDownloader
from scraper.markdown_generator import MarkdownGenerator
from scraper.export_parser import LinkedInExportParser


logger = logging.getLogger('linkedin_scraper')


class LinkedInArchiver:
    """Main orchestrator for LinkedIn post archiving."""

    def __init__(self, config_path: str = 'config/config.yaml'):
        """
        Initialize the archiver.

        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path)
        self.logger = setup_logging(self.config)

        self.base_dir = Path(self.config['output']['base_dir'])
        self.media_downloader = MediaDownloader(self.config)
        self.markdown_generator = MarkdownGenerator(self.config)

        # API-related state (lazy init)
        self.env_vars = None
        self.authenticator = None
        self.client = None
        self.post_fetcher = None

    def authenticate(self, force_reauth: bool = False):
        """
        Perform OAuth authentication.

        Args:
            force_reauth: Force new authentication flow
        """
        from scraper.auth import LinkedInAuthenticator
        from scraper.linkedin_client import LinkedInClient
        from scraper.post_fetcher import PostFetcher

        logger.info("Starting authentication...")

        if not self.env_vars:
            self.env_vars = load_env_vars()

        self.authenticator = LinkedInAuthenticator(
            client_id=self.env_vars['client_id'],
            client_secret=self.env_vars['client_secret'],
            redirect_uri=self.env_vars['redirect_uri']
        )

        if force_reauth:
            self.authenticator.clear_cache()
            logger.info("Cleared cached token, forcing re-authentication")

        try:
            access_token = self.authenticator.get_access_token(force_refresh=force_reauth)
            logger.info("Authentication successful!")

            # Initialize client
            self.client = LinkedInClient(access_token, self.config)
            self.post_fetcher = PostFetcher(self.client)

            return True

        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False

    @staticmethod
    def _content_fingerprint(text: str) -> str:
        """Normalize post text into a fingerprint for duplicate detection."""
        text = text.lower()
        text = re.sub(r'http\S+', '', text)       # remove URLs
        text = re.sub(r'#\w+', '', text)           # remove hashtags
        text = re.sub(r'@\w+', '', text)           # remove mentions
        text = re.sub(r'[^\w\s]', '', text)        # remove punctuation
        text = re.sub(r'\s+', ' ', text).strip()   # collapse whitespace
        return text

    def _archive_posts(self, posts: list, desc: str = "Archiving posts") -> dict:
        """
        Archive a list of LinkedInPost objects to disk.

        Args:
            posts: List of LinkedInPost objects
            desc: Progress bar description

        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_posts': len(posts),
            'successful': 0,
            'failed': 0,
            'skipped_self_reposts': 0,
            'media_downloaded': 0,
        }

        # Pre-populate with slugs already on disk to prevent duplicates
        existing_slugs = []
        for d in self.base_dir.rglob('post.md'):
            existing_slugs.append(d.parent.name)
        # Track content fingerprints to detect self-reposts
        content_fingerprints: set = set()

        for post in tqdm(posts, desc=desc):
            try:
                fingerprint = self._content_fingerprint(post.content)

                # If this is a repost and we already have the original content, skip it
                if post.is_repost() and fingerprint in content_fingerprints:
                    logger.debug(f"Skipping self-repost: {post.content[:60]}...")
                    stats['skipped_self_reposts'] += 1
                    continue

                content_fingerprints.add(fingerprint)

                # Generate slug
                base_slug = slugify_post(post.content, post.created_at)
                slug = get_unique_slug(base_slug, existing_slugs)
                existing_slugs.append(slug)
                post.slug = slug

                # Create post directory
                post_date_path = post.created_at.strftime(self.config['output']['date_format'])
                post_dir = self.base_dir / post_date_path / slug
                create_directory(post_dir)

                # Check if post already exists
                md_path = post_dir / 'post.md'
                if md_path.exists():
                    logger.debug(f"Post already archived: {slug}")
                    stats['successful'] += 1
                    continue

                # Download media
                if post.has_media():
                    downloaded = self.media_downloader.download_media_for_post(post, post_dir)
                    stats['media_downloaded'] += len(downloaded)

                # Generate markdown
                success = self.markdown_generator.save_post_markdown(post, md_path)

                if success:
                    stats['successful'] += 1
                else:
                    stats['failed'] += 1

            except Exception as e:
                logger.error(f"Failed to archive post {post.id}: {e}")
                stats['failed'] += 1
                continue

        # Generate index
        logger.info("Generating index file...")
        index_path = self.base_dir / 'INDEX.md'
        self.markdown_generator.generate_index(posts, index_path)

        return stats

    def fetch_and_archive_posts(self, limit: int = None) -> dict:
        """
        Fetch all posts via API and archive them.

        Args:
            limit: Maximum number of posts to fetch (None = all)

        Returns:
            Dictionary with statistics
        """
        if not self.client:
            logger.error("Not authenticated. Run authentication first.")
            return {}

        logger.info("Fetching user profile...")
        profile = self.client.get_user_profile()

        if not profile:
            logger.error("Failed to fetch user profile")
            return {}

        user_name = profile.get('name', 'Unknown')
        logger.info(f"Archiving posts for: {user_name}")

        # Get person URN
        person_urn = self.client.get_person_urn(profile)
        if not person_urn:
            logger.error("Could not determine person URN")
            return {}

        logger.info(f"Person URN: {person_urn}")

        # Fetch posts
        logger.info("Fetching posts from LinkedIn...")
        posts = self.post_fetcher.fetch_all_posts(person_urn, limit=limit)

        if not posts:
            logger.warning("No posts found")
            return {'total_posts': 0}

        logger.info(f"Found {len(posts)} posts to archive")

        stats = self._archive_posts(posts, desc="Archiving posts")
        stats['api_requests'] = self.client.get_request_count()
        return stats

    def import_and_archive_export(self, export_path: str) -> dict:
        """
        Import LinkedIn data export and archive posts.

        Args:
            export_path: Path to LinkedIn export ZIP file or directory

        Returns:
            Dictionary with statistics
        """
        logger.info(f"Importing LinkedIn data export from: {export_path}")

        parser = LinkedInExportParser(export_path)
        posts = parser.parse_export()

        if not posts:
            logger.warning("No posts found in export")
            return {'total_posts': 0}

        logger.info(f"Found {len(posts)} posts in export")
        return self._archive_posts(posts, desc="Archiving posts from export")

    def crawl_and_archive_posts(
        self, profile_url: str, limit: int = None, headed: bool = False
    ) -> dict:
        """
        Crawl posts via browser automation and archive them.

        Args:
            profile_url: LinkedIn profile URL
            limit: Maximum number of posts to crawl
            headed: Run browser in visible mode

        Returns:
            Dictionary with statistics
        """
        from scraper.browser_crawler import BrowserCrawler

        logger.info("Starting browser-based crawl...")
        crawler = BrowserCrawler(self.config)

        posts = crawler.crawl_posts(
            profile_url=profile_url,
            limit=limit,
            headed=headed,
        )

        if not posts:
            logger.warning("No posts crawled")
            return {'total_posts': 0}

        logger.info(f"Crawled {len(posts)} posts, archiving...")
        stats = self._archive_posts(posts, desc="Archiving crawled posts")
        self._refresh_featured_posts()
        return stats

    def _refresh_featured_posts(self) -> None:
        """Re-compute and persist the featured_posts list in site.yaml.

        Reads the full post archive (engagement data from frontmatter), picks
        the top performers from the last 90 days, and overwrites featured_posts
        in config/site.yaml so the next build picks them up automatically.
        """
        try:
            from web.build import parse_all_posts, compute_featured_posts, update_site_yaml_featured
            all_posts = parse_all_posts()
            slugs = compute_featured_posts(all_posts, days=90, top_n=6)
            if slugs:
                update_site_yaml_featured(slugs)
                logger.info(f"Updated featured posts: {slugs}")
            else:
                logger.debug("No engagement data yet — featured_posts not updated.")
        except Exception as e:
            logger.warning(f"Could not refresh featured posts: {e}")

    def _print_stats(self, stats: dict, label: str = "Archival") -> None:
        """Print summary statistics."""
        logger.info("\n" + "=" * 60)
        logger.info(f"{label} Complete!")
        logger.info("=" * 60)
        logger.info(f"Total posts: {stats.get('total_posts', 0)}")
        logger.info(f"Successfully archived: {stats.get('successful', 0)}")
        logger.info(f"Failed: {stats.get('failed', 0)}")
        if stats.get('skipped_self_reposts'):
            logger.info(f"Skipped self-reposts: {stats['skipped_self_reposts']}")
        logger.info(f"Media files downloaded: {stats.get('media_downloaded', 0)}")
        if stats.get('api_requests'):
            logger.info(f"API requests made: {stats['api_requests']}")
        logger.info(f"\nArchive location: {self.base_dir}")
        logger.info("=" * 60)

    def run(self, args):
        """
        Run the archiver based on command-line arguments.

        Args:
            args: Parsed command-line arguments
        """
        logger.info("=" * 60)
        logger.info("LinkedIn Post Archiver")
        logger.info("=" * 60)

        # Handle import-export mode (no authentication needed)
        if args.import_export:
            logger.info("\nImporting from LinkedIn data export...\n")
            stats = self.import_and_archive_export(args.import_export)
            self._print_stats(stats, "Import")
            return

        # Handle browser login mode
        if args.browser_login:
            from scraper.browser_crawler import BrowserCrawler
            crawler = BrowserCrawler(self.config)
            success = crawler.manual_login()
            if success:
                logger.info("Browser login successful! Session saved.")
                logger.info("You can now run with --crawl to archive your posts.")
            else:
                logger.error("Browser login failed.")
                sys.exit(1)
            return

        # Handle crawl mode (browser-based, no API needed)
        if args.crawl:
            if not args.profile_url:
                logger.error("--profile-url is required with --crawl")
                logger.error("Example: --crawl --profile-url https://www.linkedin.com/in/username")
                sys.exit(1)

            logger.info("\nStarting browser-based crawl...\n")
            stats = self.crawl_and_archive_posts(
                profile_url=args.profile_url,
                limit=args.limit,
                headed=args.headed,
            )
            self._print_stats(stats, "Crawl")
            return

        # Handle authentication-only mode (API)
        if args.auth:
            success = self.authenticate(force_reauth=args.reauth)
            if success:
                logger.info("Authentication complete!")
                logger.info("You can now run with --fetch to archive your posts")
            else:
                logger.error("Authentication failed")
                sys.exit(1)
            return

        # API fetch mode
        if args.fetch:
            success = self.authenticate(force_reauth=args.reauth)
            if not success:
                logger.error("Authentication failed. Exiting.")
                sys.exit(1)

            logger.info("\nStarting post archival...\n")
            stats = self.fetch_and_archive_posts(limit=args.limit)
            self._print_stats(stats, "Archival")

            requests_made = stats.get('api_requests', 0)
            if requests_made > 400:
                logger.warning(f"High API usage: {requests_made}/~500 daily limit")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Archive your LinkedIn posts locally',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Browser crawl (recommended - no API needed):
  python -m scraper.main --browser-login
  python -m scraper.main --crawl --profile-url https://www.linkedin.com/in/username
  python -m scraper.main --crawl --profile-url https://www.linkedin.com/in/username --limit 50

  # Import from LinkedIn data export:
  python -m scraper.main --import-export /path/to/linkedin-export.zip

  # API method (if you have API access):
  python -m scraper.main --auth
  python -m scraper.main --fetch
        """
    )

    # Browser crawl options
    crawl_group = parser.add_argument_group('Browser crawl (recommended)')
    crawl_group.add_argument(
        '--browser-login',
        action='store_true',
        help='Open browser for manual LinkedIn login (do this first)'
    )
    crawl_group.add_argument(
        '--crawl',
        action='store_true',
        help='Crawl posts via browser automation (no API needed)'
    )
    crawl_group.add_argument(
        '--profile-url',
        type=str,
        metavar='URL',
        help='LinkedIn profile URL (e.g. https://www.linkedin.com/in/username)'
    )
    crawl_group.add_argument(
        '--headed',
        action='store_true',
        help='Run browser in visible mode (for debugging)'
    )

    # Import options
    import_group = parser.add_argument_group('Data export import')
    import_group.add_argument(
        '--import-export',
        type=str,
        metavar='PATH',
        help='Import from LinkedIn data export (ZIP file or directory)'
    )

    # API options
    api_group = parser.add_argument_group('API method (requires LinkedIn API access)')
    api_group.add_argument(
        '--auth',
        action='store_true',
        help='Run OAuth authentication flow'
    )
    api_group.add_argument(
        '--fetch',
        action='store_true',
        help='Fetch and archive all posts via API'
    )
    api_group.add_argument(
        '--reauth',
        action='store_true',
        help='Force re-authentication'
    )

    # Common options
    parser.add_argument(
        '--limit',
        type=int,
        metavar='N',
        help='Maximum number of posts to process'
    )
    parser.add_argument(
        '--config',
        default='config/config.yaml',
        help='Path to configuration file (default: config/config.yaml)'
    )

    args = parser.parse_args()

    # If no action specified, show help
    if not any([args.auth, args.fetch, args.crawl, args.browser_login, args.import_export]):
        parser.print_help()
        sys.exit(0)

    try:
        archiver = LinkedInArchiver(config_path=args.config)
        archiver.run(args)
    except KeyboardInterrupt:
        logger.info("\n\nInterrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
