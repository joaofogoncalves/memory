"""Main entry point for LinkedIn Post Archiver."""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

from scraper.utils import (
    setup_logging,
    load_config,
    load_env_vars,
    slugify_post,
    get_unique_slug,
    create_directory
)
from scraper.auth import LinkedInAuthenticator
from scraper.linkedin_client import LinkedInClient
from scraper.post_fetcher import PostFetcher
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
        self.env_vars = load_env_vars()

        self.base_dir = Path(self.config['output']['base_dir'])
        self.authenticator = None
        self.client = None
        self.post_fetcher = None
        self.media_downloader = MediaDownloader(self.config)
        self.markdown_generator = MarkdownGenerator(self.config)

    def authenticate(self, force_reauth: bool = False):
        """
        Perform OAuth authentication.

        Args:
            force_reauth: Force new authentication flow
        """
        logger.info("Starting authentication...")

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

    def fetch_and_archive_posts(self, limit: int = None) -> dict:
        """
        Fetch all posts and archive them.

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

        # Archive each post
        stats = {
            'total_posts': len(posts),
            'successful': 0,
            'failed': 0,
            'media_downloaded': 0,
            'api_requests': self.client.get_request_count()
        }

        existing_slugs = []

        for post in tqdm(posts, desc="Archiving posts"):
            try:
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

    def import_and_archive_export(self, export_path: str) -> dict:
        """
        Import LinkedIn data export and archive posts.

        Args:
            export_path: Path to LinkedIn export ZIP file or directory

        Returns:
            Dictionary with statistics
        """
        logger.info(f"Importing LinkedIn data export from: {export_path}")

        # Parse export
        parser = LinkedInExportParser(export_path)
        posts = parser.parse_export()

        if not posts:
            logger.warning("No posts found in export")
            return {'total_posts': 0}

        logger.info(f"Found {len(posts)} posts in export")

        # Archive posts (reuse existing logic)
        stats = {
            'total_posts': len(posts),
            'successful': 0,
            'failed': 0,
            'media_downloaded': 0,
            'api_requests': 0
        }

        existing_slugs = []

        for post in tqdm(posts, desc="Archiving posts from export"):
            try:
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

                # Download media (if any)
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

            # Print summary
            logger.info("\n" + "=" * 60)
            logger.info("Import Complete!")
            logger.info("=" * 60)
            logger.info(f"Total posts: {stats.get('total_posts', 0)}")
            logger.info(f"Successfully archived: {stats.get('successful', 0)}")
            logger.info(f"Failed: {stats.get('failed', 0)}")
            logger.info(f"Media files downloaded: {stats.get('media_downloaded', 0)}")
            logger.info(f"\nArchive location: {self.base_dir}")
            logger.info("=" * 60)
            return

        # Handle authentication-only mode
        if args.auth:
            success = self.authenticate(force_reauth=args.reauth)
            if success:
                logger.info("✓ Authentication complete!")
                logger.info("You can now run with --fetch to archive your posts")
            else:
                logger.error("✗ Authentication failed")
                sys.exit(1)
            return

        # Authenticate
        success = self.authenticate(force_reauth=args.reauth)
        if not success:
            logger.error("Authentication failed. Exiting.")
            sys.exit(1)

        # Fetch and archive posts
        if args.fetch or args.limit:
            logger.info("\nStarting post archival...\n")
            stats = self.fetch_and_archive_posts(limit=args.limit)

            # Print summary
            logger.info("\n" + "=" * 60)
            logger.info("Archival Complete!")
            logger.info("=" * 60)
            logger.info(f"Total posts: {stats.get('total_posts', 0)}")
            logger.info(f"Successfully archived: {stats.get('successful', 0)}")
            logger.info(f"Failed: {stats.get('failed', 0)}")
            logger.info(f"API requests made: {stats.get('api_requests', 0)}")
            logger.info(f"Media files downloaded: {stats.get('media_downloaded', 0)}")
            logger.info(f"\nArchive location: {self.base_dir}")

            # Rate limit warning
            requests_made = stats.get('api_requests', 0)
            if requests_made > 400:
                logger.warning(f"⚠️  High API usage: {requests_made}/~500 daily limit")

            logger.info("=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Archive your LinkedIn posts locally',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Import from LinkedIn data export (no API needed!)
  python -m scraper.main --import-export /path/to/linkedin-export.zip

  # Authenticate with LinkedIn API
  python -m scraper.main --auth

  # Fetch and archive all posts via API
  python -m scraper.main --fetch

  # Fetch only the last 50 posts via API
  python -m scraper.main --limit 50

  # Force re-authentication and fetch posts
  python -m scraper.main --reauth --fetch
        """
    )

    parser.add_argument(
        '--import-export',
        type=str,
        metavar='PATH',
        help='Import from LinkedIn data export (ZIP file or directory)'
    )

    parser.add_argument(
        '--auth',
        action='store_true',
        help='Run authentication flow only (for API method)'
    )

    parser.add_argument(
        '--fetch',
        action='store_true',
        help='Fetch and archive all posts (via API - requires auth)'
    )

    parser.add_argument(
        '--limit',
        type=int,
        metavar='N',
        help='Fetch only the last N posts'
    )

    parser.add_argument(
        '--reauth',
        action='store_true',
        help='Force re-authentication (clear cached token)'
    )

    parser.add_argument(
        '--config',
        default='config/config.yaml',
        help='Path to configuration file (default: config/config.yaml)'
    )

    args = parser.parse_args()

    # If no action specified, show help
    if not any([args.auth, args.fetch, args.limit]):
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
