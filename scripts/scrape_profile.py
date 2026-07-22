"""Dump the LinkedIn profile About + Experience sections as plain text.

One-off helper for syncing the website/CV with the live LinkedIn profile.
Designed to run in CI (GitHub Actions) where LINKEDIN_LI_AT provides the
session cookie — same auth mechanism as scraper/browser_crawler.py.

Usage:
    LINKEDIN_LI_AT=<cookie> LINKEDIN_PROFILE_URL=<url> \
        uv run python scripts/scrape_profile.py
"""

import os
import sys

from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

PROFILE_URL = os.environ.get(
    'LINKEDIN_PROFILE_URL', 'https://www.linkedin.com/in/joaofogoncalves'
).rstrip('/')


def expand_see_more(page) -> None:
    """Click every inline "see more" toggle so truncated text is captured."""
    selectors = [
        'button.inline-show-more-text__button',
        'button:has-text("see more")',
        'button:has-text("Show more")',
    ]
    for selector in selectors:
        for button in page.locator(selector).all():
            try:
                button.click(timeout=1500)
                page.wait_for_timeout(400)
            except Exception:
                pass


def dump(page, url: str, label: str) -> str:
    page.goto(url, wait_until='domcontentloaded', timeout=60_000)
    page.wait_for_timeout(6_000)
    if any(marker in page.url for marker in ('authwall', '/login', 'checkpoint')):
        print(f"NOT LOGGED IN or challenged at {label}: {page.url}")
        sys.exit(1)
    expand_see_more(page)
    try:
        text = page.locator('main').inner_text(timeout=10_000)
    except Exception:
        text = page.evaluate('document.body.innerText')
    print(f"\n===== {label} START =====")
    print(text)
    print(f"===== {label} END =====")
    return text


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled'],
        )
        context = browser.new_context(
            viewport={'width': 1280, 'height': 1600},
            locale='en-US',
        )
        li_at = os.environ.get('LINKEDIN_LI_AT', '').strip()
        if li_at:
            context.add_cookies([{
                'name': 'li_at',
                'value': li_at,
                'domain': '.linkedin.com',
                'path': '/',
                'httpOnly': True,
                'secure': True,
                'sameSite': 'None',
            }])
        else:
            print("WARNING: LINKEDIN_LI_AT not set — expecting authwall")

        page = context.new_page()
        Stealth().apply_stealth_sync(page)

        dump(page, PROFILE_URL + '/', 'PROFILE (headline + About)')
        dump(page, PROFILE_URL + '/details/experience/', 'EXPERIENCE')

        browser.close()


if __name__ == '__main__':
    main()
