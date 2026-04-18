"""Generate clean markdown files for LinkedIn posts."""

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

from scraper.models import LinkedInPost
from scraper.utils import format_datetime


logger = logging.getLogger('linkedin_scraper.markdown')


class MarkdownGenerator:
    """Generate markdown files from LinkedIn posts."""

    def __init__(self, config: dict):
        """
        Initialize markdown generator.

        Args:
            config: Configuration dictionary
        """
        self.config = config

    def generate_post_markdown(self, post: LinkedInPost) -> str:
        """
        Generate complete markdown content for a post.

        Args:
            post: LinkedInPost object

        Returns:
            Markdown content as string
        """
        sections = []

        # Add frontmatter
        sections.append(self._format_header(post))

        # Add date heading
        date_str = post.created_at.strftime('%B %d, %Y')
        sections.append(f"# {date_str}\n")

        # Handle reposts differently
        if post.is_repost():
            sections.append(self._format_repost(post))
        else:
            sections.append(self._format_content(post.content))

        # Add hashtags if present
        if post.hashtags:
            hashtags_str = ' '.join([f'#{tag}' for tag in post.hashtags])
            sections.append(f"\n**Hashtags:** {hashtags_str}\n")

        # Add media section
        if post.has_media():
            sections.append(self._format_media(post.media))

        # Add footer with original link
        sections.append(self._format_footer(post))

        return '\n'.join(sections)

    def _format_header(self, post: LinkedInPost) -> str:
        """
        Format YAML frontmatter.

        Args:
            post: LinkedInPost object

        Returns:
            YAML frontmatter string
        """
        archived_at = datetime.now().strftime('%Y-%m-%d')

        header = [
            '---',
            f'date: {post.created_at.strftime("%Y-%m-%d")}',
            f'post_url: {post.post_url}',
            f'post_type: {post.post_type}',
            f'archived_at: {archived_at}',
        ]

        if post.hashtags:
            tags = ', '.join(post.hashtags)
            header.append(f'tags: [{tags}]')

        if post.reactions:
            header.append(f'reactions: {post.reactions}')
        if post.comments:
            header.append(f'comments: {post.comments}')

        header.append('---\n')

        return '\n'.join(header)

    def _format_content(self, text: str) -> str:
        """
        Format post content, preserving formatting.

        Args:
            text: Post content text

        Returns:
            Formatted content
        """
        if not text:
            return "_[No text content]_\n"

        # Preserve line breaks
        formatted = text.strip()

        # Ensure proper paragraph spacing
        formatted = formatted.replace('\n\n\n', '\n\n')

        return formatted + '\n'

    def _format_repost(self, post: LinkedInPost) -> str:
        """
        Format repost with special handling.

        Args:
            post: LinkedInPost object (must be repost)

        Returns:
            Formatted repost content
        """
        sections = []

        sections.append('## 🔄 Repost\n')

        if post.original_post_url:
            sections.append(f'**Original post:** {post.original_post_url}\n')

        if post.repost_commentary:
            sections.append('**My commentary:**\n')
            sections.append(self._format_content(post.repost_commentary))

        return '\n'.join(sections)

    def _format_media(self, media_list: list) -> str:
        """
        Format media references.

        Args:
            media_list: List of Media objects

        Returns:
            Formatted media section
        """
        if not media_list:
            return ''

        sections = ['\n---\n', '## Media\n']

        for media in media_list:
            if media.local_path:
                if media.type == 'image':
                    # Use markdown image syntax
                    sections.append(f'![{media.filename}]({media.local_path})\n')
                elif media.type == 'video':
                    # Use link for videos
                    sections.append(f'📹 [{media.filename}]({media.local_path})\n')
                elif media.type == 'document':
                    # Use link for documents
                    sections.append(f'📄 [{media.filename}]({media.local_path})\n')
            else:
                # Media download failed, show URL
                sections.append(f'⚠️ _Media not available locally_\n')

        return '\n'.join(sections)

    def _format_footer(self, post: LinkedInPost) -> str:
        """
        Format footer with link to original post.

        Args:
            post: LinkedInPost object

        Returns:
            Formatted footer
        """
        footer = [
            '\n---\n',
            f'[View original post on LinkedIn]({post.post_url})',
        ]

        return '\n'.join(footer)

    def save_post_markdown(self, post: LinkedInPost, output_path: Path) -> bool:
        """
        Generate and save markdown file for post.

        Args:
            post: LinkedInPost object
            output_path: Path to save markdown file

        Returns:
            True if successful
        """
        try:
            markdown_content = self.generate_post_markdown(post)

            # Ensure parent directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write markdown file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            logger.info(f"Saved markdown: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save markdown for post {post.id}: {e}")
            return False

    def update_engagement(
        self,
        md_path: Path,
        reactions: int,
        comments: int,
        post_url: Optional[str] = None,
    ) -> bool:
        """Update reactions/comments (and optionally fill empty post_url) in an existing post.md.

        Uses surgical line-level updates to preserve frontmatter formatting and
        minimize git diffs. Only writes when a value actually changes. Never
        touches the post body.

        Args:
            md_path: Path to the existing post.md file.
            reactions: Latest reaction count from the scraper.
            comments: Latest comment count from the scraper.
            post_url: If provided and the existing frontmatter has an empty
                post_url, fill it in (useful the first time an authored post
                is seen on LinkedIn).

        Returns:
            True if the file was updated or already up-to-date; False on error.
        """
        try:
            text = md_path.read_text(encoding='utf-8')
            if not text.startswith('---'):
                logger.warning(f"No frontmatter in {md_path}, skipping engagement update")
                return False

            parts = text.split('---', 2)
            if len(parts) < 3:
                logger.warning(f"Malformed frontmatter in {md_path}, skipping")
                return False

            fm_text = parts[1]
            body = parts[2]
            fm = yaml.safe_load(fm_text) or {}

            lines = fm_text.strip('\n').split('\n')
            new_fields = []
            changed = False

            def replace_line(key: str, new_val) -> bool:
                pattern = re.compile(rf'^{re.escape(key)}\s*:.*$')
                for i, line in enumerate(lines):
                    if pattern.match(line):
                        lines[i] = f'{key}: {new_val}'
                        return True
                return False

            existing_reactions = int(fm.get('reactions', 0) or 0)
            existing_comments = int(fm.get('comments', 0) or 0)
            existing_post_url = (fm.get('post_url') or '').strip('"\' ')

            if reactions and reactions != existing_reactions:
                if not replace_line('reactions', reactions):
                    new_fields.append(f'reactions: {reactions}')
                changed = True

            if comments and comments != existing_comments:
                if not replace_line('comments', comments):
                    new_fields.append(f'comments: {comments}')
                changed = True

            if post_url and not existing_post_url:
                if not replace_line('post_url', post_url):
                    new_fields.append(f'post_url: {post_url}')
                changed = True

            if not changed:
                return True

            if new_fields:
                lines.extend(new_fields)

            new_text = '---\n' + '\n'.join(lines) + '\n---' + body
            md_path.write_text(new_text, encoding='utf-8')
            logger.info(
                f"Updated engagement for {md_path.parent.name}: "
                f"reactions {existing_reactions}→{reactions}, "
                f"comments {existing_comments}→{comments}"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to update engagement for {md_path}: {e}", exc_info=True)
            return False

    def generate_index(self, posts: list, output_path: Path) -> bool:
        """
        Generate an index file listing all posts.

        Args:
            posts: List of LinkedInPost objects
            output_path: Path to save index file

        Returns:
            True if successful
        """
        try:
            sections = [
                '# LinkedIn Posts Archive\n',
                f'**Total posts:** {len(posts)}',
                f'**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n',
                '---\n',
                '## Posts by Year\n'
            ]

            # Group posts by year
            posts_by_year = {}
            for post in sorted(posts, key=lambda p: p.created_at, reverse=True):
                year = post.created_at.year
                if year not in posts_by_year:
                    posts_by_year[year] = []
                posts_by_year[year].append(post)

            # Generate index entries
            for year in sorted(posts_by_year.keys(), reverse=True):
                sections.append(f'### {year}\n')
                for post in posts_by_year[year]:
                    date_str = post.created_at.strftime('%B %d')
                    preview = post.content[:100] if post.content else '[No content]'
                    if len(post.content) > 100:
                        preview += '...'

                    # Generate relative path to post
                    post_path = f"{post.created_at.strftime('%Y/%m')}/{post.slug}/post.md"

                    sections.append(f'- **{date_str}**: [{preview}]({post_path})')

                sections.append('')

            # Write index file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(sections))

            logger.info(f"Generated index: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to generate index: {e}")
            return False
