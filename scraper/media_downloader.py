"""Download and manage media files from LinkedIn posts."""

import os
import logging
import hashlib
from pathlib import Path
from typing import List, Optional
import requests
from PIL import Image
from tqdm import tqdm
from scraper.models import LinkedInPost, Media
from scraper.utils import sanitize_filename


logger = logging.getLogger('linkedin_scraper.media')


class MediaDownloader:
    """Handle downloading of images, videos, and documents."""

    def __init__(self, config: dict):
        """
        Initialize media downloader.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.download_images = config.get('media', {}).get('download_images', True)
        self.download_videos = config.get('media', {}).get('download_videos', True)
        self.download_documents = config.get('media', {}).get('download_documents', True)
        self.max_video_size_mb = config.get('media', {}).get('max_video_size_mb', 500)
        self.timeout = config.get('linkedin', {}).get('timeout', 30)

    def download_media_for_post(self, post: LinkedInPost, output_dir: Path) -> List[str]:
        """
        Download all media for a post.

        Args:
            post: LinkedInPost object
            output_dir: Directory to save media files

        Returns:
            List of successfully downloaded file paths
        """
        if not post.has_media():
            return []

        # Create media subdirectory
        media_dir = output_dir / 'media'
        media_dir.mkdir(parents=True, exist_ok=True)

        downloaded_files = []

        for idx, media in enumerate(post.media, start=1):
            try:
                # Check if we should download this media type
                if media.type == 'image' and not self.download_images:
                    continue
                elif media.type == 'video' and not self.download_videos:
                    continue
                elif media.type == 'document' and not self.download_documents:
                    continue

                # Determine file extension
                ext = self._get_file_extension(media.url, media.type)

                # Generate filename
                filename = f"{media.type}-{idx}{ext}"
                filename = sanitize_filename(filename)
                output_path = media_dir / filename

                # Skip if already downloaded
                if output_path.exists():
                    logger.debug(f"Media already exists: {filename}")
                    media.local_path = str(output_path.relative_to(output_dir))
                    media.filename = filename
                    downloaded_files.append(str(output_path))
                    continue

                # Download based on media type
                success = False
                if media.type == 'image':
                    success = self._download_image(media.url, output_path)
                elif media.type == 'video':
                    success = self._download_video(media.url, output_path)
                elif media.type == 'document':
                    success = self._download_document(media.url, output_path)

                if success:
                    media.local_path = str(output_path.relative_to(output_dir))
                    media.filename = filename
                    downloaded_files.append(str(output_path))
                    logger.info(f"Downloaded: {filename}")

            except Exception as e:
                logger.error(f"Failed to download media {idx} for post {post.id}: {e}")
                continue

        return downloaded_files

    def _download_image(self, url: str, output_path: Path) -> bool:
        """
        Download and validate image file.

        Args:
            url: Image URL
            output_path: Local path to save

        Returns:
            True if successful
        """
        try:
            response = requests.get(url, stream=True, timeout=self.timeout)
            response.raise_for_status()

            # Save image
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            # Validate image with PIL
            try:
                with Image.open(output_path) as img:
                    img.verify()
                return True
            except Exception as e:
                logger.warning(f"Image validation failed: {e}")
                output_path.unlink()
                return False

        except Exception as e:
            logger.error(f"Failed to download image from {url}: {e}")
            return False

    def _download_video(self, url: str, output_path: Path) -> bool:
        """
        Download video file with progress bar.

        Args:
            url: Video URL
            output_path: Local path to save

        Returns:
            True if successful
        """
        try:
            # Get file size first
            response = requests.head(url, timeout=self.timeout)
            file_size = int(response.headers.get('content-length', 0))

            # Check size limit
            size_mb = file_size / (1024 * 1024)
            if size_mb > self.max_video_size_mb:
                logger.warning(
                    f"Video too large ({size_mb:.1f}MB > {self.max_video_size_mb}MB), skipping"
                )
                return False

            # Download with progress bar
            response = requests.get(url, stream=True, timeout=self.timeout)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                with tqdm(total=file_size, unit='B', unit_scale=True, desc=output_path.name) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))

            return True

        except Exception as e:
            logger.error(f"Failed to download video from {url}: {e}")
            if output_path.exists():
                output_path.unlink()
            return False

    def _download_document(self, url: str, output_path: Path) -> bool:
        """
        Download document file.

        Args:
            url: Document URL
            output_path: Local path to save

        Returns:
            True if successful
        """
        try:
            response = requests.get(url, stream=True, timeout=self.timeout)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            return True

        except Exception as e:
            logger.error(f"Failed to download document from {url}: {e}")
            return False

    def _get_file_extension(self, url: str, media_type: str) -> str:
        """
        Determine file extension from URL or media type.

        Args:
            url: Media URL
            media_type: Type of media

        Returns:
            File extension with dot (e.g., '.jpg')
        """
        # Try to get extension from URL
        path = url.split('?')[0]  # Remove query params
        if '.' in path:
            ext = os.path.splitext(path)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4', '.mov', '.avi', '.pdf', '.doc', '.docx']:
                return ext

        # Default extensions by type
        defaults = {
            'image': '.jpg',
            'video': '.mp4',
            'document': '.pdf'
        }

        return defaults.get(media_type, '')

    def calculate_checksum(self, file_path: Path) -> str:
        """
        Calculate MD5 checksum of file.

        Args:
            file_path: Path to file

        Returns:
            MD5 checksum string
        """
        md5_hash = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
