"""Browser-based LinkedIn post crawler using Playwright."""

import logging
import random
import re
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright, Page, Locator, TimeoutError as PlaywrightTimeout
from playwright_stealth import Stealth

from scraper.models import LinkedInPost, Media
from scraper.utils import (
    extract_hashtags,
    parse_relative_date,
    load_checkpoint,
    save_checkpoint,
)

logger = logging.getLogger('linkedin_scraper.browser_crawler')


class BrowserCrawler:
    """Crawl LinkedIn posts using browser automation."""

    def __init__(self, config: dict):
        self.config = config
        browser_cfg = config.get('browser', {})
        self.profile_dir = browser_cfg.get('profile_dir', 'cache/browser_profile')
        self.scroll_delay_min = browser_cfg.get('scroll_delay_min', 3.0)
        self.scroll_delay_max = browser_cfg.get('scroll_delay_max', 8.0)
        self.action_delay_min = browser_cfg.get('action_delay_min', 1.0)
        self.action_delay_max = browser_cfg.get('action_delay_max', 3.0)
        self.max_stale_scrolls = browser_cfg.get('max_stale_scrolls', 5)

        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    def _launch_browser(self, headed: bool = False) -> Page:
        """Launch browser with persistent context."""
        Path(self.profile_dir).mkdir(parents=True, exist_ok=True)

        self._playwright = sync_playwright().start()

        # Always use the full chromium binary (not the headless shell)
        # so that headed login and headless crawl share the same profile
        chromium_path = self._playwright.chromium.executable_path
        self._context = self._playwright.chromium.launch_persistent_context(
            user_data_dir=self.profile_dir,
            headless=not headed,
            executable_path=chromium_path,
            viewport={'width': 1280, 'height': 900},
            locale='en-US',
            args=[
                '--disable-blink-features=AutomationControlled',
            ],
        )
        self._page = self._context.new_page()
        Stealth().apply_stealth_sync(self._page)
        return self._page

    def manual_login(self) -> bool:
        """
        Open headed browser for manual LinkedIn login.

        User logs in manually. Session is saved to persistent profile.
        Returns True if login was detected.
        """
        logger.info("Opening browser for manual LinkedIn login...")
        logger.info("Please log in to LinkedIn in the browser window.")
        logger.info("The browser will close automatically once login is detected.")

        page = self._launch_browser(headed=True)

        try:
            page.goto('https://www.linkedin.com/login', wait_until='domcontentloaded')

            # Wait for user to complete login (detected by URL change to feed/main page)
            # Give them up to 5 minutes
            logger.info("Waiting for login (up to 5 minutes)...")
            try:
                page.wait_for_url(
                    re.compile(r'linkedin\.com/(feed|in/|mynetwork)'),
                    timeout=300_000,
                )
                logger.info("Login detected! Session saved.")
                self._random_delay(2, 3)
                return True
            except PlaywrightTimeout:
                logger.error("Login timed out after 5 minutes.")
                return False

        finally:
            self.close()

    def is_logged_in(self) -> bool:
        """Check if saved session is still valid."""
        page = self._page
        if not page:
            return False

        try:
            page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=20_000)
            self._random_delay(2, 3)

            url = page.url
            logger.debug(f"Login check URL: {url}")

            # If redirected to login/auth page, session is invalid
            if '/login' in url or '/authwall' in url or '/signup' in url or '/checkpoint' in url:
                logger.debug(f"Redirected to auth page: {url}")
                return False

            # If we're still on linkedin.com/feed or similar, we're logged in
            if 'linkedin.com/feed' in url or 'linkedin.com/in/' in url or 'linkedin.com/mynetwork' in url:
                return True

            # Fallback: check page title doesn't indicate login
            title = page.title().lower()
            logger.debug(f"Page title: {title}")
            if 'sign in' in title or 'log in' in title or 'join' in title:
                return False

            return True
        except Exception as e:
            logger.warning(f"Login check failed: {e}")
            return False

    def crawl_posts(
        self,
        profile_url: str,
        limit: Optional[int] = None,
        headed: bool = False,
    ) -> List[LinkedInPost]:
        """
        Crawl posts from a LinkedIn profile.

        Args:
            profile_url: LinkedIn profile URL (e.g. https://www.linkedin.com/in/username)
            limit: Max posts to crawl (None = all)
            headed: Run in visible browser mode

        Returns:
            List of LinkedInPost objects (most recent first)
        """
        page = self._launch_browser(headed=headed)

        # Check login
        if not self.is_logged_in():
            logger.error(
                "Not logged in. Run with --browser-login first to authenticate."
            )
            self.close()
            return []

        # Navigate to activity page
        activity_url = profile_url.rstrip('/') + '/recent-activity/all/'
        logger.info(f"Navigating to: {activity_url}")
        page.goto(activity_url, wait_until='domcontentloaded', timeout=30_000)
        self._random_delay(2, 4)

        # Check for valid page
        if '/login' in page.url or '/authwall' in page.url:
            logger.error("Redirected to login. Session may have expired.")
            self.close()
            return []

        posts: List[LinkedInPost] = []
        seen_urns: set = set()
        stale_count = 0

        logger.info("Starting scroll and extract loop...")

        try:
            while True:
                # Find all post containers
                post_elements = page.locator(
                    'div.feed-shared-update-v2'
                ).all()

                new_count = 0
                for el in post_elements:
                    try:
                        urn = el.get_attribute('data-urn') or ''
                        if not urn or urn in seen_urns:
                            continue

                        seen_urns.add(urn)
                        new_count += 1

                        # Extract post data
                        post = self._extract_post(el, urn, page)
                        if post:
                            posts.append(post)
                            logger.debug(
                                f"Extracted post {len(posts)}: {post.content[:60]}..."
                            )

                            # Check limit
                            if limit and len(posts) >= limit:
                                logger.info(f"Reached limit of {limit} posts.")
                                stale_count = self.max_stale_scrolls
                                break

                    except Exception as e:
                        logger.warning(f"Failed to extract post {urn}: {e}")
                        continue

                # Show progress with oldest post date
                oldest_date = ''
                if posts:
                    oldest_date = f", oldest: {posts[-1].created_at.strftime('%Y-%m-%d')}"

                # Check stale
                if new_count == 0:
                    stale_count += 1
                    logger.info(
                        f"No new posts this scroll (stale {stale_count}/{self.max_stale_scrolls}, total: {len(posts)}{oldest_date})"
                    )
                else:
                    stale_count = 0
                    logger.info(
                        f"Found {new_count} new posts (total: {len(posts)}{oldest_date})"
                    )

                if stale_count >= self.max_stale_scrolls:
                    logger.info("No more new posts found. Done scrolling.")
                    break

                # Scroll down
                self._scroll_down(page)
                self._random_delay(self.scroll_delay_min, self.scroll_delay_max)

        except KeyboardInterrupt:
            logger.info("Interrupted by user. Saving progress...")
        except Exception as e:
            logger.error(f"Crawl error: {e}", exc_info=True)
        finally:
            # Save checkpoint with the first (most recent) post
            if posts:
                first_post = posts[0]
                save_checkpoint({
                    'last_post_id': first_post.id,
                    'last_post_date': first_post.created_at.isoformat(),
                    'last_crawl_timestamp': datetime.now().isoformat(),
                    'posts_crawled': len(posts),
                    'profile_url': profile_url,
                })

            self.close()

        logger.info(f"Crawled {len(posts)} posts total.")
        return posts

    def _extract_post(self, el: Locator, urn: str, page: Page) -> Optional[LinkedInPost]:
        """Extract a LinkedInPost from a post DOM element."""
        try:
            # Click "see more" to expand truncated text
            self._expand_post_text(el)

            content = self._extract_text(el)
            if not content:
                content = "(no text content)"

            created_at = self._extract_date(el)
            media = self._extract_media(el)
            post_type = self._determine_post_type(el)
            hashtags = extract_hashtags(content)
            post_url = self._extract_post_url(urn)

            # For reposts, try to extract commentary
            repost_commentary = None
            original_post_url = None
            if post_type == 'repost':
                repost_commentary, original_post_url = self._extract_repost_info(el)

            return LinkedInPost(
                id=urn,
                post_url=post_url,
                content=content,
                created_at=created_at,
                post_type=post_type,
                media=media,
                hashtags=hashtags,
                original_post_url=original_post_url,
                repost_commentary=repost_commentary,
            )
        except Exception as e:
            logger.warning(f"Failed to parse post {urn}: {e}")
            return None

    def _expand_post_text(self, el: Locator) -> None:
        """Click 'see more' button if present to expand truncated text."""
        try:
            see_more = el.locator('button.feed-shared-inline-show-more-text__button').first
            if see_more.is_visible(timeout=500):
                see_more.click()
                self._random_delay(0.3, 0.8)
        except (PlaywrightTimeout, Exception):
            pass

    def _extract_text(self, el: Locator) -> str:
        """Extract post text content."""
        # Try multiple selectors for the text content
        selectors = [
            'div.feed-shared-update-v2__description span.break-words',
            'div.feed-shared-update-v2__description',
            'span.break-words',
            'div.update-components-text',
        ]

        for selector in selectors:
            try:
                text_el = el.locator(selector).first
                if text_el.is_visible(timeout=500):
                    text = text_el.inner_text(timeout=2_000)
                    if text and text.strip():
                        return text.strip()
            except (PlaywrightTimeout, Exception):
                continue

        return ''

    def _extract_date(self, el: Locator) -> datetime:
        """Extract post creation date."""
        # LinkedIn shows relative dates in a span near the author info
        # Look for the time element or date-like span
        try:
            # Try aria-label on time-related elements
            time_selectors = [
                'span.update-components-actor__sub-description span[aria-hidden="true"]',
                'span.feed-shared-actor__sub-description span[aria-hidden="true"]',
                'a.app-aware-link time',
            ]

            for selector in time_selectors:
                try:
                    time_el = el.locator(selector).first
                    if time_el.is_visible(timeout=500):
                        date_text = time_el.inner_text(timeout=1_000).strip()
                        # Remove trailing bullet and extra text (e.g. "2d \u2022 Edited")
                        date_text = date_text.split('\u2022')[0].strip()
                        date_text = date_text.split('•')[0].strip()
                        parsed = parse_relative_date(date_text)
                        if parsed:
                            return parsed
                except (PlaywrightTimeout, Exception):
                    continue

        except Exception as e:
            logger.debug(f"Date extraction failed: {e}")

        return datetime.now()

    def _extract_media(self, el: Locator) -> List[Media]:
        """Extract media attachments from post."""
        media = []

        # Images
        try:
            images = el.locator(
                'div.update-components-image img, '
                'div.feed-shared-image img, '
                'div.update-components-linkedin-video__container img'
            ).all()
            for img in images:
                try:
                    src = img.get_attribute('src') or ''
                    if src and 'data:image' not in src and 'static.licdn' not in src:
                        media.append(Media(type='image', url=src))
                except Exception:
                    continue
        except Exception:
            pass

        # Videos (poster/thumbnail - actual video URLs are in data attributes or require API)
        try:
            videos = el.locator(
                'video, div.update-components-linkedin-video'
            ).all()
            for vid in videos:
                try:
                    # Try to get video source
                    src = vid.get_attribute('src') or vid.get_attribute('data-src') or ''
                    poster = vid.get_attribute('poster') or ''
                    if src and 'data:' not in src:
                        media.append(Media(type='video', url=src))
                    elif poster:
                        media.append(Media(type='image', url=poster))
                except Exception:
                    continue
        except Exception:
            pass

        # Documents/carousels
        try:
            docs = el.locator(
                'div.update-components-document, '
                'div.feed-shared-document'
            ).all()
            for doc in docs:
                try:
                    # Documents often have preview images
                    doc_imgs = doc.locator('img').all()
                    for doc_img in doc_imgs:
                        src = doc_img.get_attribute('src') or ''
                        if src and 'data:image' not in src:
                            media.append(Media(type='document', url=src))
                except Exception:
                    continue
        except Exception:
            pass

        return media

    def _determine_post_type(self, el: Locator) -> str:
        """Determine if post is original, repost, article, or poll."""
        try:
            outer_html = el.inner_html(timeout=2_000)

            # Check for repost indicators
            if 'reposted this' in outer_html.lower() or 'reshared' in outer_html.lower():
                return 'repost'

            # Check for article
            if 'update-components-article' in outer_html or 'feed-shared-article' in outer_html:
                return 'article'

            # Check for poll
            if 'update-components-poll' in outer_html or 'feed-shared-poll' in outer_html:
                return 'poll'

        except Exception:
            pass

        return 'original'

    def _extract_post_url(self, urn: str) -> str:
        """Build LinkedIn post URL from URN."""
        # URN format: urn:li:activity:1234567890
        activity_id = urn.split(':')[-1] if ':' in urn else urn
        return f"https://www.linkedin.com/feed/update/urn:li:activity:{activity_id}/"

    def _extract_repost_info(self, el: Locator) -> tuple:
        """Extract repost commentary and original post URL."""
        commentary = None
        original_url = None

        try:
            # The user's commentary on a repost is usually in a separate div
            # above the shared content
            commentary_el = el.locator(
                'div.feed-shared-update-v2__description-wrapper span.break-words'
            ).first
            if commentary_el.is_visible(timeout=500):
                commentary = commentary_el.inner_text(timeout=1_000).strip()
        except (PlaywrightTimeout, Exception):
            pass

        try:
            # Original post link
            link_el = el.locator(
                'a.feed-shared-mini-update-v2__link, '
                'a.update-components-mini-update-v2__link'
            ).first
            if link_el.is_visible(timeout=500):
                original_url = link_el.get_attribute('href')
        except (PlaywrightTimeout, Exception):
            pass

        return commentary, original_url

    def _scroll_down(self, page: Page) -> None:
        """Scroll down with human-like behavior, then wait for content to load."""
        # Multiple small scrolls to mimic human behavior
        total = random.randint(800, 1500)
        scrolled = 0
        while scrolled < total:
            chunk = random.randint(100, 300)
            page.evaluate(f'window.scrollBy(0, {chunk})')
            time.sleep(random.uniform(0.1, 0.4))
            scrolled += chunk

        # Wait for network to settle (new posts loading)
        try:
            page.wait_for_load_state('networkidle', timeout=10_000)
        except PlaywrightTimeout:
            pass

    def _random_delay(self, min_sec: float, max_sec: float) -> None:
        """Sleep for a random duration."""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def close(self) -> None:
        """Close browser and clean up."""
        try:
            if self._context:
                self._context.close()
                self._context = None
            if self._playwright:
                self._playwright.stop()
                self._playwright = None
            self._page = None
        except Exception as e:
            logger.debug(f"Browser cleanup: {e}")
