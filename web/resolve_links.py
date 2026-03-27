#!/usr/bin/env python3
"""Resolve lnkd.in shortened URLs to their actual destinations.

LinkedIn's shortener uses a JS-based interstitial page. The real URL is
embedded as an href in the HTML body. We fetch the page and extract it.

Usage: python web/resolve_links.py
       python web/resolve_links.py --dry-run   # preview without writing
"""

import re
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / 'posts'
LNKD_PATTERN = re.compile(r'https://lnkd\.in/[a-zA-Z0-9_-]+')

# URLs that are part of LinkedIn's chrome, not the actual redirect target
IGNORE_DOMAINS = {
    'www.linkedin.com',
    'static.licdn.com',
    'linkedin.com',
}

resolved_cache: dict[str, str] = {}


def resolve_url(short_url: str) -> str | None:
    """Fetch the lnkd.in page and extract the real URL from the HTML."""
    if short_url in resolved_cache:
        return resolved_cache[short_url]

    try:
        resp = requests.get(short_url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        })
        resp.raise_for_status()

        # Extract all hrefs from the page
        hrefs = re.findall(r'href="(https?://[^"]+)"', resp.text)

        # Find the first href that's not LinkedIn's own chrome
        for href in hrefs:
            # Skip LinkedIn's own URLs
            domain = href.split('/')[2] if len(href.split('/')) > 2 else ''
            if domain in IGNORE_DOMAINS:
                continue
            # Skip tracking/help links
            if 'linkedin.com/help' in href:
                continue
            # This is our target
            resolved_cache[short_url] = href
            return href

        # If all hrefs are LinkedIn, check if it redirects to a LinkedIn post
        for href in hrefs:
            if 'linkedin.com/feed/update' in href or 'linkedin.com/pulse' in href:
                resolved_cache[short_url] = href
                return href

        resolved_cache[short_url] = short_url
        return short_url

    except Exception as e:
        print(f'  FAILED: {short_url} → {e}')
        return None


def process_file(post_file: Path, dry_run: bool = False) -> int:
    """Process a single post.md file. Returns number of links resolved."""
    text = post_file.read_text(encoding='utf-8')
    short_urls = LNKD_PATTERN.findall(text)

    if not short_urls:
        return 0

    count = 0
    new_text = text

    for short_url in set(short_urls):
        real_url = resolve_url(short_url)
        if real_url and real_url != short_url:
            new_text = new_text.replace(short_url, real_url)
            print(f'  {short_url} → {real_url}')
            count += 1
        elif real_url == short_url:
            print(f'  {short_url} → (could not resolve)')
        time.sleep(0.5)  # Be polite to LinkedIn

    if count > 0 and not dry_run:
        post_file.write_text(new_text, encoding='utf-8')

    return count


def main():
    dry_run = '--dry-run' in sys.argv

    if dry_run:
        print('DRY RUN — no files will be modified\n')

    post_files = sorted(POSTS_DIR.rglob('post.md'))
    total_resolved = 0
    files_changed = 0

    for pf in post_files:
        text = pf.read_text(encoding='utf-8')
        if 'lnkd.in' not in text:
            continue

        rel = pf.relative_to(ROOT)
        print(f'{rel}')
        resolved = process_file(pf, dry_run=dry_run)
        if resolved > 0:
            total_resolved += resolved
            files_changed += 1

    print(f'\nDone. Resolved {total_resolved} links in {files_changed} files.')
    if dry_run:
        print('(dry run — no files were changed)')


if __name__ == '__main__':
    main()
