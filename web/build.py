#!/usr/bin/env python3
"""Static site builder for a LinkedIn post archive.

Reads markdown posts from posts/ and optional cv.md, generates a static HTML
site following the 'Brutalist Compiler' design system.

Site identity is configured in config/site.yaml (see config/site.yaml.example).

Usage: python web/build.py
"""

import hashlib
import json
import os
import re
import shutil
from datetime import datetime, timezone
from email.utils import format_datetime as _fmt_rfc2822
from html import escape
from pathlib import Path
from typing import Optional

import markdown
import yaml
from dotenv import load_dotenv
from PIL import Image

load_dotenv(Path(__file__).resolve().parent.parent / '.env')

# ============================================================
# Brand constants
# ============================================================

# BRIDGE IN always renders in brand red — never changes without explicit consent
_BRIDGE_IN_HTML = '<span style="color:#cc0000;font-weight:600">BRIDGE IN</span>'


def style_bridge_in(html: str) -> str:
    """Apply red brand styling to every occurrence of 'BRIDGE IN' in HTML."""
    return html.replace('BRIDGE IN', _BRIDGE_IN_HTML)


# ============================================================
# Configuration
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / 'posts'
CV_FILE = ROOT / 'cv.md'
CV_PDF = ROOT / 'cv_joaofogoncalves.pdf'
NOW_FILE = ROOT / 'now.md'
ARTICLES_DIR = ROOT / 'articles'
WEB_DIR = Path(__file__).resolve().parent
DIST_DIR = WEB_DIR / 'dist'
CSS_SRC = WEB_DIR / 'css'
JS_SRC = WEB_DIR / 'js'
IMG_SRC = WEB_DIR / 'img'

SITE_CONFIG_FILE = ROOT / 'config' / 'site.yaml'

def _load_site_config() -> dict:
    """Load site identity from config/site.yaml, falling back to env vars."""
    cfg = {}
    if SITE_CONFIG_FILE.exists():
        cfg = yaml.safe_load(SITE_CONFIG_FILE.read_text(encoding='utf-8')) or {}
    return {
        'site_name': cfg.get('site_name', os.environ.get('SITE_NAME', 'My Site')),
        'site_description': cfg.get('site_description', os.environ.get('SITE_DESCRIPTION', '')),
        'linkedin': cfg.get('linkedin', ''),
        'github': cfg.get('github', ''),
        'twitter': cfg.get('twitter', ''),
        'twitter_handle': cfg.get('twitter_handle', ''),
        'substack': cfg.get('substack', ''),
        'hero_title': cfg.get('hero_title', cfg.get('site_name', 'My Site')),
        'hero_subline': cfg.get('hero_subline', ''),
        'about_teaser': cfg.get('about_teaser', ''),
        'footer_text': cfg.get('footer_text', cfg.get('site_name', 'My Site')),
        'speaking_text': cfg.get('speaking_text', ''),
        'thesis': cfg.get('thesis', ''),
        'newsletter_url': cfg.get('newsletter_url', ''),
        'featured_posts': cfg.get('featured_posts', []) or [],
        'topics': cfg.get('topics', []) or [],
    }

SITE = _load_site_config()
SITE_NAME = SITE['site_name']
SITE_URL = os.environ.get('SITE_URL', '').rstrip('/')
SITE_DESCRIPTION = SITE['site_description']
LINKEDIN = SITE['linkedin']
GITHUB = SITE['github']
TWITTER = SITE['twitter']
TWITTER_HANDLE = SITE['twitter_handle']
SUBSTACK = SITE['substack']

md_renderer = markdown.Markdown(
    extensions=['fenced_code', 'codehilite', 'tables', 'smarty', 'md_in_html'],
    extension_configs={
        'codehilite': {
            'css_class': 'highlight',
            'guess_lang': False,
            'linenums': False,
        },
    },
    output_format='html',
)


def _asset_hash(path: Path, length: int = 8) -> str:
    """Return a short SHA-256 hash of a file's contents for cache-busting."""
    if not path.exists():
        return '0'
    return hashlib.sha256(path.read_bytes()).hexdigest()[:length]


# Compute once at build time so every page gets the same version strings
_CSS_VER = _asset_hash(CSS_SRC / 'style.css')
_JS_VER = _asset_hash(JS_SRC / 'posts.js')
_HOME_JS_VER = _asset_hash(JS_SRC / 'home.js')

# Read critical CSS for inlining (above-the-fold styles)
_CRITICAL_CSS_PATH = CSS_SRC / 'critical.css'
_CRITICAL_CSS = _CRITICAL_CSS_PATH.read_text(encoding='utf-8') if _CRITICAL_CSS_PATH.exists() else ''


def minify_css(text: str) -> str:
    """Lightweight CSS minifier — strip comments and collapse whitespace."""
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s*([{}:;,])\s*', r'\1', text)
    text = text.replace(';}', '}')
    return text.strip()


def autolink_urls(html: str) -> str:
    """Convert bare URLs in HTML text nodes into clickable links."""
    def replace_url(m):
        prefix = m.group(1)
        url = m.group(2)
        # Skip if already inside an href or src attribute
        if prefix in ('="', "='"):
            return m.group(0)
        return f'{prefix}<a href="{url}" target="_blank" rel="noopener">{url}</a>'

    return re.sub(
        r'(="|=\'|>|^|\s)(https?://[^\s<>"\']+)',
        replace_url,
        html
    )


def externalize_links(html: str) -> str:
    """Add target="_blank" rel="noopener" to external <a> tags that lack it."""
    def repl(m):
        attrs = m.group(1)
        if 'target=' in attrs:
            return m.group(0)
        # Preserve existing rel (e.g. rel="nofollow") and append noopener
        if 'rel=' in attrs:
            new_attrs = re.sub(
                r'rel=(["\'])([^"\']*)\1',
                lambda r: f'rel={r.group(1)}{r.group(2)} noopener{r.group(1)}' if 'noopener' not in r.group(2) else r.group(0),
                attrs,
            )
            return f'<a{new_attrs} target="_blank">'
        return f'<a{attrs} target="_blank" rel="noopener">'

    return re.sub(r'<a([^>]*\shref="https?://[^"]*"[^>]*)>', repl, html)


def expand_wide_fences(md_text: str) -> str:
    """Convert `::: wide` / `::: full` / `:::` fences into div wrappers.

    Used in articles to opt inline images or tables out of the 720px content
    column. Inner markdown is processed via the `md_in_html` extension.
    """
    pattern = re.compile(
        r'^:::[ \t]*(wide|full)[ \t]*\r?\n(.*?)\r?\n^:::[ \t]*\r?\n?',
        re.DOTALL | re.MULTILINE,
    )
    def repl(m):
        cls = m.group(1)
        inner = m.group(2)
        return f'<div class="breakout breakout--{cls}" markdown="1">\n\n{inner}\n\n</div>\n'
    return pattern.sub(repl, md_text)


# ============================================================
# Post Parsing
# ============================================================

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from markdown content."""
    if not text.startswith('---'):
        return {}, text
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}, text
    fm = yaml.safe_load(parts[1]) or {}
    content = parts[2].strip()
    return fm, content


def clean_content(content: str) -> str:
    """Remove noise from post content for rendering."""
    # Remove the date heading (# Month DD, YYYY)
    content = re.sub(r'^#\s+\w+\s+\d{1,2},\s+\d{4}\s*\n', '', content)

    # Remove raw hashtag lines (hashtag\n#Tag patterns)
    content = re.sub(r'(?m)^hashtag\s*\n', '', content)

    # Remove standalone hashtag lines like "#AI " that were part of raw format
    # But keep the **Hashtags:** line and ## headings
    content = re.sub(r'(?m)^#(?!#)(\w+)\s*$', '', content)

    # Remove the **Hashtags:** line (we show tags separately)
    content = re.sub(r'\*\*Hashtags?:\*\*[^\n]*\n?', '', content)

    # Remove the "View original post" link at the bottom (we add our own)
    content = re.sub(r'\[View original post on LinkedIn\]\([^)]+\)\s*$', '', content)

    # Remove trailing separators
    content = re.sub(r'---\s*$', '', content.rstrip())

    # Clean up excessive blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.strip()


def extract_title(content: str) -> str:
    """Get the first meaningful line as the post title."""
    # Remove date heading first
    text = re.sub(r'^#\s+\w+\s+\d{1,2},\s+\d{4}\s*\n', '', content)

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        # Skip markdown headings that are just "Media" or formatting
        if line.startswith('## ') and line.strip('# ').lower() in ('media', 'repost'):
            continue
        if line.startswith('---'):
            continue
        if line.startswith('!['):
            continue
        if line.startswith('hashtag'):
            continue
        if line.startswith('#') and not line.startswith('## '):
            # A hashtag line like #AI
            continue
        if line.startswith('**Hashtags'):
            continue
        if line.startswith('[View original'):
            continue
        # Strip markdown bold/italic
        clean = re.sub(r'[*_`]', '', line)
        # Strip repost emoji
        clean = clean.replace('🔄 Repost', '').strip()
        if clean:
            return clean[:120]
    return 'Untitled'


def extract_preview(content: str, max_chars: int = 250) -> str:
    """Extract preview text (first ~250 chars of body after title)."""
    text = re.sub(r'^#\s+\w+\s+\d{1,2},\s+\d{4}\s*\n', '', content)

    lines = []
    found_title = False
    for line in text.split('\n'):
        stripped = line.strip()
        if not stripped:
            if found_title:
                continue
            continue
        if not found_title:
            # Skip the title line
            if stripped.startswith('##') or stripped.startswith('![') or stripped.startswith('---'):
                continue
            if stripped.startswith('hashtag') or stripped.startswith('**Hashtag'):
                continue
            if stripped.startswith('[View original'):
                continue
            found_title = True
            continue
        # Now collect body lines
        if stripped.startswith('##') or stripped.startswith('![') or stripped.startswith('---'):
            break
        if stripped.startswith('hashtag') or stripped.startswith('**Hashtag'):
            break
        if stripped.startswith('[View original'):
            break
        if stripped.startswith('#') and len(stripped) < 30:
            continue  # likely a hashtag
        clean = re.sub(r'[*_`]', '', stripped)
        if clean:
            lines.append(clean)
        if len(' '.join(lines)) > max_chars:
            break

    preview = ' '.join(lines)
    if len(preview) > max_chars:
        preview = preview[:max_chars].rsplit(' ', 1)[0] + '...'
    return preview


def has_media(post_dir: Path) -> list[str]:
    """Return list of renderable media filenames in post's media/ dir.

    Excludes non-renderable build artifacts like chart spec JSON files.
    """
    media_dir = post_dir / 'media'
    if not media_dir.exists():
        return []
    renderable_exts = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.mp4', '.mov', '.svg')
    return [
        f.name for f in sorted(media_dir.iterdir())
        if f.is_file() and f.suffix.lower() in renderable_exts
    ]


def parse_all_posts() -> list[dict]:
    """Scan all posts, parse, filter to original + article."""
    posts = []

    for post_file in POSTS_DIR.rglob('post.md'):
        text = post_file.read_text(encoding='utf-8')
        fm, content = parse_frontmatter(text)

        post_type = fm.get('post_type', '')
        if post_type not in ('original', 'article'):
            continue

        date_val = fm.get('date', '')
        if hasattr(date_val, 'strftime'):
            date_str = date_val.strftime('%Y-%m-%d')
        else:
            date_str = str(date_val)

        # Build the slug from directory name
        post_dir = post_file.parent
        slug = post_dir.name
        year = date_str[:4]
        month = date_str[5:7]

        title = extract_title(content)
        preview = extract_preview(content)
        media_files = has_media(post_dir)

        # URL path for this post
        url_path = f'/posts/{year}/{month}/{slug}/'

        read_time = reading_time(content)

        try:
            mtime_iso = datetime.fromtimestamp(
                post_file.stat().st_mtime, tz=timezone.utc
            ).date().isoformat()
        except Exception:
            mtime_iso = date_str
        date_modified = mtime_iso if mtime_iso > date_str else date_str

        word_count = len(content.split())

        posts.append({
            'date': date_str,
            'date_modified': date_modified,
            'year': year,
            'month': month,
            'slug': slug,
            'title': title,
            'description': str(fm.get('description', '') or '').strip(),
            'preview': preview,
            'reading_time': read_time,
            'word_count': word_count,
            'tags': [str(t) for t in (fm.get('tags', []) or [])],
            'post_type': post_type,
            'post_url': fm.get('post_url', ''),
            'x_url': fm.get('x_url', ''),
            'substack_note_url': fm.get('substack_note_url', ''),
            'url': url_path,
            'media': media_files,
            'source_dir': str(post_dir),
            'content': content,
            'reactions': int(fm.get('reactions', 0) or 0),
            'comments': int(fm.get('comments', 0) or 0),
        })

    # Sort by date descending
    posts.sort(key=lambda p: p['date'], reverse=True)
    return posts


def parse_all_articles() -> list[dict]:
    """Scan articles/ directory, parse article.md files."""
    if not ARTICLES_DIR.exists():
        return []
    articles = []

    for article_file in ARTICLES_DIR.rglob('article.md'):
        text = article_file.read_text(encoding='utf-8')
        fm, content = parse_frontmatter(text)

        title = fm.get('title', 'Untitled')
        subtitle = fm.get('subtitle', '')

        date_val = fm.get('date', '')
        if hasattr(date_val, 'strftime'):
            date_str = date_val.strftime('%Y-%m-%d')
        else:
            date_str = str(date_val)

        article_dir = article_file.parent
        slug = article_dir.name
        year = date_str[:4]
        month = date_str[5:7]

        # Preview from first paragraph of content
        preview = ''
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('!'):
                continue
            preview = re.sub(r'[*_`\[\]]', '', line)[:250]
            break

        media_files = has_media(article_dir)
        hero_image = fm.get('hero_image', '')

        # Reading time from frontmatter or computed
        rt = fm.get('reading_time')
        if rt:
            read_time = f'{rt} min read'
        else:
            read_time = reading_time(content)

        # Draft handling: drafts get an obfuscated URL and are excluded from
        # listings, feeds, sitemap, and topics. The token is stable per article
        # so review links don't change between builds.
        is_draft = bool(fm.get('draft', False))
        draft_token = ''
        if is_draft:
            explicit = fm.get('draft_token', '')
            if explicit:
                draft_token = str(explicit).strip()
            else:
                draft_token = hashlib.sha256(slug.encode('utf-8')).hexdigest()[:16]
            url_path = f'/articles/drafts/{draft_token}/'
        else:
            url_path = f'/articles/{year}/{month}/{slug}/'

        # dateModified from file mtime if newer than the publish date
        try:
            mtime_iso = datetime.fromtimestamp(
                article_file.stat().st_mtime, tz=timezone.utc
            ).date().isoformat()
        except Exception:
            mtime_iso = date_str
        date_modified = mtime_iso if mtime_iso > date_str else date_str

        word_count = len(content.split())

        articles.append({
            'date': date_str,
            'date_modified': date_modified,
            'year': year,
            'month': month,
            'slug': slug,
            'title': title,
            'subtitle': subtitle,
            'description': str(fm.get('description', '') or '').strip(),
            'preview': preview,
            'reading_time': read_time,
            'word_count': word_count,
            'tags': [str(t) for t in (fm.get('tags', []) or [])],
            'substack_url': fm.get('substack_url', ''),
            'hero_image': hero_image,
            'url': url_path,
            'media': media_files,
            'source_dir': str(article_dir),
            'content': content,
            'draft': is_draft,
            'draft_token': draft_token,
        })

    articles.sort(key=lambda a: a['date'], reverse=True)
    return articles


# ============================================================
# HTML Templates
# ============================================================

_GFONTS_URL = (
    'https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300..900;1,300..700&'
    'family=JetBrains+Mono:wght@400;500&family=Newsreader:ital,wght@0,400;0,600;0,700;1,400&'
    'family=Space+Grotesk:wght@400;500;600&display=swap'
)

GOOGLE_FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    f'<link rel="stylesheet" href="{_GFONTS_URL}" media="print" onload="this.media=\'all\'">'
    f'<noscript><link rel="stylesheet" href="{_GFONTS_URL}"></noscript>'
)


def ga_snippet() -> str:
    """Return deferred Google Analytics snippet (loads after page is interactive)."""
    ga_id = os.environ.get('GA_MEASUREMENT_ID', '').strip()
    if not ga_id:
        return ''
    return (
        f'<script>\n'
        f'  window.addEventListener("load", function() {{\n'
        f'    setTimeout(function() {{\n'
        f'      var s = document.createElement("script");\n'
        f'      s.src = "https://www.googletagmanager.com/gtag/js?id={ga_id}";\n'
        f'      document.head.appendChild(s);\n'
        f'      s.onload = function() {{\n'
        f'        window.dataLayer = window.dataLayer || [];\n'
        f'        function gtag(){{dataLayer.push(arguments);}}\n'
        f"        gtag('js', new Date());\n"
        f"        gtag('config', '{ga_id}');\n"
        f'      }};\n'
        f'    }}, 100);\n'
        f'  }});\n'
        f'  </script>'
    )


FAVICON = (
    '<link rel="icon" type="image/x-icon" href="{prefix}img/favicon.ico">\n'
    '  <link rel="icon" type="image/png" sizes="192x192" href="{prefix}img/favicon-192.png">\n'
    '  <link rel="apple-touch-icon" href="{prefix}img/apple-touch-icon.png">'
)


def reading_time(text: str) -> str:
    """Estimate reading time from word count."""
    words = len(text.split())
    minutes = max(1, round(words / 230))
    return f'{minutes} min read'


def og_tags(title: str, description: str = '', og_type: str = 'website',
            og_image: str = '', depth: int = 0, large_image: bool = False,
            canonical_url: str = '') -> str:
    """Generate Open Graph and Twitter Card meta tags.

    `large_image` switches the Twitter card to summary_large_image — use it
    whenever the og_image is a real hero (not the default headshot fallback).
    """
    prefix = '../' * depth
    desc = escape(description or SITE_DESCRIPTION)
    has_real_image = bool(og_image)
    img = og_image or f'{prefix}img/headshot.jpg'
    if SITE_URL and not img.startswith('http'):
        img = f'{SITE_URL}/{img.lstrip("/")}'
    card_type = 'summary_large_image' if (large_image and has_real_image) else 'summary'
    lines = [
        f'<meta property="og:title" content="{escape(title)}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:image" content="{img}">',
    ]
    if large_image and has_real_image:
        # Standard hero dims used by /article (1440×900). Helps platforms that
        # respect og:image:width/height for layout decisions.
        lines.append('<meta property="og:image:width" content="1440">')
        lines.append('<meta property="og:image:height" content="900">')
    if canonical_url:
        lines.append(f'<meta property="og:url" content="{canonical_url}">')
    lines.append(f'<meta name="twitter:card" content="{card_type}">')
    lines.append(f'<meta name="twitter:site" content="{TWITTER_HANDLE}">')
    if has_real_image:
        lines.append(f'<meta name="twitter:image" content="{img}">')
    if SITE_URL:
        lines.append(f'<meta property="og:site_name" content="{SITE_NAME}">')
    return '\n  '.join(lines)


def head_html(title: str, depth: int = 0, extra_head: str = '',
              description: str = '', og_type: str = 'website', og_image: str = '',
              jsonld: str = '', noindex: bool = False,
              large_image: bool = False, canonical_path: str = '') -> str:
    """Generate <head> with proper relative paths.

    `canonical_path` is the site-root-relative path of the current page
    (e.g. "/articles/2026/05/foo/"). When SITE_URL is set, it produces a
    <link rel="canonical"> and a matching og:url.
    """
    prefix = '../' * depth
    ga = ga_snippet()
    desc = escape(description or SITE_DESCRIPTION)
    canonical_url = ''
    canonical_link = ''
    if SITE_URL and canonical_path:
        canonical_url = f'{SITE_URL}{canonical_path}'
        canonical_link = f'<link rel="canonical" href="{canonical_url}">'
    og = og_tags(title, description, og_type, og_image, depth,
                 large_image=large_image, canonical_url=canonical_url)
    rss_link = f'<link rel="alternate" type="application/rss+xml" title="{escape(SITE_NAME)}" href="{prefix}feed.xml">'
    robots = '<meta name="robots" content="noindex, nofollow">' if noindex else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#0e131e">
  <title>{escape(title)} — {SITE_NAME}</title>
  <meta name="description" content="{desc}">
  {robots}
  {canonical_link}
  {FAVICON.format(prefix=prefix)}
  {rss_link}
  {og}
  {ga}
  <style>{minify_css(_CRITICAL_CSS)}</style>
  {GOOGLE_FONTS}
  <link rel="stylesheet" href="{prefix}css/style.css?v={_CSS_VER}" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="{prefix}css/style.css?v={_CSS_VER}"></noscript>
  <script src="{prefix}js/posts.js?v={_JS_VER}" defer></script>
  {extra_head}
  {jsonld}
</head>'''


def _has_public_articles() -> bool:
    """True if at least one non-draft article.md exists."""
    if not ARTICLES_DIR.exists():
        return False
    for f in ARTICLES_DIR.rglob('article.md'):
        try:
            fm, _ = parse_frontmatter(f.read_text(encoding='utf-8'))
            if not fm.get('draft', False):
                return True
        except Exception:
            continue
    return False


def nav_html(active: str = '', depth: int = 0, transparent: bool = False) -> str:
    prefix = '../' * depth
    cls = lambda name: ' active' if active == name else ''
    articles_link = (
        f'<a href="{prefix}articles/"{cls("articles")}>Articles</a>'
        if _has_public_articles() else ''
    )
    now_link = (
        f'<a href="{prefix}now/"{cls("now")}>Now</a>'
        if NOW_FILE.exists() else ''
    )
    subscribe_link = (
        f'<a href="{SITE["newsletter_url"]}" target="_blank" rel="noopener" class="nav-cta">Subscribe</a>'
        if SITE.get('newsletter_url') else ''
    )
    nav_cls = 'nav nav--transparent' if transparent else 'nav'
    return f'''<nav class="{nav_cls}">
  <div class="nav-inner">
    <a href="{prefix}" class="nav-logo-link"><img src="{prefix}img/logo.webp" alt="JG" class="nav-logo" width="24" height="24"></a>
    <div class="nav-links">
      <a href="{prefix}about/"{cls("about")}>About</a>
      {articles_link}
      <a href="{prefix}posts/"{cls("posts")}>Posts</a>
      {now_link}
      {subscribe_link}
    </div>
  </div>
</nav>
<main>'''


SVG_LINKEDIN = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>'
SVG_GITHUB = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>'
SVG_X = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>'
SVG_SUBSTACK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M22.539 8.242H1.46V5.406h21.08v2.836zM1.46 10.812V24L12 18.11 22.54 24V10.812H1.46zM22.54 0H1.46v2.836h21.08V0z"/></svg>'
SVG_RSS = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M6.18 15.64a2.18 2.18 0 010 4.36 2.18 2.18 0 010-4.36M4 4.44A15.56 15.56 0 0119.56 20h-2.83A12.73 12.73 0 004 7.27V4.44m0 5.66a9.9 9.9 0 019.9 9.9h-2.83A7.07 7.07 0 004 12.93V10.1z"/></svg>'


def footer_html() -> str:
    social_links = ''
    if LINKEDIN:
        social_links += f'<a href="{LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn">{SVG_LINKEDIN}</a>'
    if GITHUB:
        social_links += f'<a href="{GITHUB}" target="_blank" rel="noopener" aria-label="GitHub">{SVG_GITHUB}</a>'
    if TWITTER:
        social_links += f'<a href="{TWITTER}" target="_blank" rel="noopener" aria-label="X">{SVG_X}</a>'
    if SUBSTACK:
        social_links += f'<a href="{SUBSTACK}" target="_blank" rel="noopener" aria-label="Substack">{SVG_SUBSTACK}</a>'
    social_links += f'<a href="/feed.xml" aria-label="RSS feed">{SVG_RSS}</a>'
    links_div = f'<div class="footer-links">{social_links}</div>' if social_links else ''

    return f'''</main>
<button class="scroll-top" id="scroll-top" aria-label="Scroll to top">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>
</button>
<footer class="footer">
  <div class="footer-inner">
    <span>{escape(SITE['footer_text'])}</span>
    {links_div}
  </div>
</footer>'''


def render_tags_html(tags: list, limit: int = 5) -> str:
    """Render tag pills."""
    return ''.join(
        f'<span class="tag">{escape(str(t))}</span>'
        for t in tags[:limit]
    )


def compute_featured_posts(posts: list[dict], days: int = 90, top_n: int = 6) -> list[str]:
    """Rank posts by engagement score in the last `days` days, return top slug list.

    Score = reactions + (comments * 3). Comments weighted higher as a stronger signal.
    Only considers posts with at least some engagement data captured.
    """
    from datetime import date as _date, timedelta
    cutoff = (_date.today() - timedelta(days=days)).isoformat()
    candidates = [
        p for p in posts
        if p['date'] >= cutoff and (p['reactions'] > 0 or p['comments'] > 0)
    ]
    candidates.sort(key=lambda p: p['reactions'] + p['comments'] * 3, reverse=True)
    return [p['slug'] for p in candidates[:top_n]]


def update_site_yaml_featured(slugs: list[str]) -> None:
    """Overwrite the featured_posts list in config/site.yaml in-place."""
    if not SITE_CONFIG_FILE.exists():
        return
    text = SITE_CONFIG_FILE.read_text(encoding='utf-8')
    slug_lines = '\n'.join(f'  - "{s}"' for s in slugs)
    new_block = f'featured_posts:\n{slug_lines}'
    # Replace existing featured_posts block (handles both populated and empty list)
    text = re.sub(
        r'featured_posts:.*?(?=\n\S|\Z)',
        new_block,
        text,
        flags=re.DOTALL,
    )
    SITE_CONFIG_FILE.write_text(text, encoding='utf-8')


def newsletter_cta_html() -> str:
    """Render a minimal newsletter subscription prompt if configured."""
    url = SITE.get('newsletter_url', '')
    if not url:
        return ''
    return (
        f'<div class="newsletter-cta">'
        f'<span class="newsletter-cta-text">If this resonates →</span>'
        f'<a href="{url}" target="_blank" rel="noopener" class="newsletter-cta-link">Subscribe for more</a>'
        f'</div>'
    )


def jsonld_person() -> str:
    """Generate JSON-LD Person schema for the About page."""
    same_as = [u for u in [LINKEDIN, GITHUB, TWITTER] if u]
    data: dict = {
        '@context': 'https://schema.org',
        '@type': 'Person',
        'name': SITE_NAME,
        'description': SITE_DESCRIPTION,
        'url': SITE_URL or '/',
    }
    if same_as:
        data['sameAs'] = same_as
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def jsonld_article(post: dict, image_url: str = '') -> str:
    """Generate JSON-LD Article schema for a post or article page.

    Accepts an absolute `image_url` (the article hero or post media). When
    omitted, falls back to the site headshot so the schema still validates.
    """
    url = f'{SITE_URL}{post["url"]}' if SITE_URL else post['url']
    description = (
        post.get('description')
        or post.get('subtitle')
        or post.get('preview', '')
    )[:200]

    same_as = [u for u in [LINKEDIN, GITHUB, TWITTER] if u]
    author: dict = {
        '@type': 'Person',
        'name': SITE_NAME,
        'url': SITE_URL or '/',
    }
    if same_as:
        author['sameAs'] = same_as

    publisher: dict = {
        '@type': 'Person',
        'name': SITE_NAME,
        'url': SITE_URL or '/',
    }

    if not image_url and SITE_URL:
        image_url = f'{SITE_URL}/img/headshot.jpg'

    data: dict = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': post['title'][:110],
        'description': description,
        'url': url,
        'datePublished': post['date'],
        'dateModified': post.get('date_modified', post['date']),
        'inLanguage': 'en',
        'mainEntityOfPage': {'@type': 'WebPage', '@id': url},
        'author': author,
        'publisher': publisher,
    }
    if image_url:
        data['image'] = image_url
    if post.get('word_count'):
        data['wordCount'] = post['word_count']
    if post.get('tags'):
        data['keywords'] = ', '.join(post['tags'])
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


_FAQ_HEADING_RE = re.compile(
    r'^##\s+(?:FAQ|Frequently asked questions|Common questions)\s*$',
    re.IGNORECASE | re.MULTILINE,
)


def _extract_faq_pairs(content: str) -> list[tuple[str, str]]:
    """Pull (question, answer) pairs out of a markdown FAQ section.

    Looks for a heading like `## FAQ` (or `## Frequently asked questions`)
    and treats every following H3 (`### …?`) as a question, with the
    paragraphs underneath it as the answer. Stops at the next H2.
    """
    match = _FAQ_HEADING_RE.search(content)
    if not match:
        return []

    section = content[match.end():]
    next_h2 = re.search(r'^##\s+\S', section, re.MULTILINE)
    if next_h2:
        section = section[:next_h2.start()]

    pairs: list[tuple[str, str]] = []
    current_q: Optional[str] = None
    answer_lines: list[str] = []

    def _flush() -> None:
        if current_q is None:
            return
        answer = '\n'.join(answer_lines).strip()
        # Strip markdown emphasis/links/inline-code lightly so the answer reads
        # cleanly when surfaced as a Google FAQ snippet.
        answer = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', answer)
        answer = re.sub(r'[*_`]', '', answer)
        if current_q and answer:
            pairs.append((current_q, answer))

    for line in section.split('\n'):
        h3 = re.match(r'^###\s+(.+?)\s*$', line)
        if h3:
            _flush()
            q = h3.group(1).strip()
            current_q = q if q.endswith('?') else None
            answer_lines = []
            continue
        if current_q is not None:
            answer_lines.append(line)
    _flush()

    return pairs


def jsonld_faq(content: str) -> str:
    """Generate FAQPage JSON-LD if the article has a recognizable FAQ section."""
    pairs = _extract_faq_pairs(content)
    if not pairs:
        return ''
    data = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': q,
                'acceptedAnswer': {'@type': 'Answer', 'text': a},
            }
            for q, a in pairs
        ],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def generate_rss(articles: list[dict]) -> str:
    """Generate RSS 2.0 feed XML for the last 20 articles."""
    items_sorted = sorted(articles, key=lambda a: a['date'], reverse=True)
    base = SITE_URL or ''
    items = []
    for a in items_sorted[:20]:
        url = f'{base}{a["url"]}'
        try:
            dt = datetime.strptime(a['date'], '%Y-%m-%d').replace(tzinfo=timezone.utc)
            pub_date = _fmt_rfc2822(dt)
        except Exception:
            pub_date = a['date']

        cleaned = clean_content(a['content'])
        md_renderer.reset()
        content_html = md_renderer.convert(expand_wide_fences(cleaned))

        # Hero image and subtitle live in frontmatter, not the body, so they
        # don't reach RSS readers via the normal markdown render. Prepend them
        # to the description so feeds carry the same lead-in as the page.
        prefix_parts = []
        if a.get('hero_image'):
            prefix_parts.append(
                f'<p><img src="{_webp_name(a["hero_image"])}" alt=""></p>'
            )
        if a.get('subtitle'):
            prefix_parts.append(
                f'<p><em>{escape(a["subtitle"])}</em></p>'
            )
        content_html = ''.join(prefix_parts) + content_html

        content_html = _rewrite_img_to_webp(content_html)
        # Article URL ends with /, so relative media/foo.webp resolves correctly
        content_html = _absolutize_img_src(content_html, url if url.endswith('/') else url + '/')
        # Escape CDATA end sequence within content
        content_html = content_html.replace(']]>', ']]]]><![CDATA[>')

        items.append(
            f'  <item>\n'
            f'    <title>{escape(a["title"])}</title>\n'
            f'    <link>{url}</link>\n'
            f'    <guid isPermaLink="true">{url}</guid>\n'
            f'    <pubDate>{pub_date}</pubDate>\n'
            f'    <description><![CDATA[{content_html}]]></description>\n'
            f'  </item>'
        )

    site_url = base or '/'
    feed_url = f'{base}/feed.xml' if base else '/feed.xml'
    items_xml = '\n'.join(items)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        '  <channel>\n'
        f'    <title>{escape(SITE_NAME)}</title>\n'
        f'    <link>{site_url}/</link>\n'
        f'    <description>{escape(SITE_DESCRIPTION)}</description>\n'
        '    <language>en</language>\n'
        f'    <atom:link href="{feed_url}" rel="self" type="application/rss+xml"/>\n'
        f'{items_xml}\n'
        '  </channel>\n'
        '</rss>'
    )


def generate_sitemap(posts: list[dict], articles: Optional[list[dict]] = None) -> str:
    """Generate sitemap.xml with all pages."""
    base = SITE_URL or ''
    static_pages = [
        (f'{base}/', '1.0', ''),
        (f'{base}/about/', '0.7', ''),
        (f'{base}/posts/', '0.8', ''),
    ]
    if articles:
        static_pages.append((f'{base}/articles/', '0.8', ''))
    url_entries = []
    for loc, priority, lastmod in static_pages:
        entry = f'  <url>\n    <loc>{loc}</loc>\n    <priority>{priority}</priority>\n  </url>'
        url_entries.append(entry)
    for p in posts:
        loc = f'{base}{p["url"]}'
        entry = (
            f'  <url>\n'
            f'    <loc>{loc}</loc>\n'
            f'    <lastmod>{p["date"]}</lastmod>\n'
            f'    <priority>0.8</priority>\n'
            f'  </url>'
        )
        url_entries.append(entry)
    for a in (articles or []):
        loc = f'{base}{a["url"]}'
        entry = (
            f'  <url>\n'
            f'    <loc>{loc}</loc>\n'
            f'    <lastmod>{a["date"]}</lastmod>\n'
            f'    <priority>0.9</priority>\n'
            f'  </url>'
        )
        url_entries.append(entry)
    body = '\n'.join(url_entries)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{body}\n'
        '</urlset>'
    )


def render_card(post: dict, depth: int = 0) -> str:
    """Render a post card for the home/posts page."""
    prefix = '../' * depth
    url = prefix + post['url'].lstrip('/')
    if not url.endswith('/'):
        url += '/'
    tags_html = render_tags_html(post['tags'])

    thumb = ''
    if post.get('media'):
        thumb_fname = _webp_name(post['media'][0])
        thumb_src = prefix + f"posts/{post['year']}/{post['month']}/{post['slug']}/media/{thumb_fname}"
        thumb = f'<img class="card-thumb" src="{thumb_src}" alt="" loading="lazy">'

    card_cls = 'card card-with-thumb' if thumb else 'card'

    return f'''<div class="{card_cls}">
  <div class="card-body">
    <div class="card-title"><a href="{url}">{escape(post['title'])}</a></div>
    <div class="card-preview">{escape(post['preview'])}</div>
    <div class="card-footer"><div class="card-tags">{tags_html}</div><div class="card-meta"><span class="card-date">{post['date']}</span><span class="card-reading-time">{post['reading_time']}</span></div></div>
  </div>
  {thumb}
</div>'''


def render_featured_card(post: dict, depth: int = 0) -> str:
    """Render a larger featured post card."""
    prefix = '../' * depth
    url = prefix + post['url'].lstrip('/')
    if not url.endswith('/'):
        url += '/'
    tags_html = render_tags_html(post['tags'])

    image = ''
    if post.get('media'):
        img_fname = _webp_name(post['media'][0])
        img_src = prefix + f"posts/{post['year']}/{post['month']}/{post['slug']}/media/{img_fname}"
        image = f'<img class="card-image" src="{img_src}" alt="" loading="lazy">'

    return f'''<div class="card-featured">
  {image}
  <div class="card-title"><a href="{url}">{escape(post['title'])}</a></div>
  <div class="card-preview">{escape(post['preview'])}</div>
  <div class="card-footer"><div class="card-tags">{tags_html}</div><div class="card-meta"><span class="card-date">{post['date']}</span><span class="card-reading-time">{post['reading_time']}</span></div></div>
</div>'''


# ============================================================
# Page Generators
# ============================================================

def _hero_links_html() -> str:
    """Build social links for the hero section.

    Wraps social handles and the role line in separate spans so the role line
    can break to its own row on small screens via CSS.
    """
    links = []
    if LINKEDIN:
        links.append(f'<a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>')
    if GITHUB:
        links.append(f'<a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>')
    if TWITTER:
        links.append(f'<a href="{TWITTER}" target="_blank" rel="noopener">X</a>')
    if SUBSTACK:
        links.append(f'<a href="{SUBSTACK}" target="_blank" rel="noopener">Substack</a>')
    sep = '<span class="sep">·</span>'
    social = sep.join(links)
    return (
        f'<div class="hero-links">'
        f'<span class="hero-links-social">{social}</span>'
        f'<span class="sep hero-links-sep">·</span>'
        f'<span class="hero-links-role">'
        f'Founding Engineer at <a href="https://www.bridgein.pt/" target="_blank" rel="noopener" class="logo-strip-name logo-strip-name--bridgein">BRIDGE IN</a>'
        f'<span class="sep">·</span>'
        f'Previously at: <a href="https://www.altium.com/" target="_blank" rel="noopener" class="logo-strip-name logo-strip-name--altium">Altium</a>'
        f' and <a href="https://www.valispace.com/" target="_blank" rel="noopener" class="logo-strip-name logo-strip-name--valispace">Valispace</a>'
        f'</span>'
        f'</div>'
    )


def assign_post_topics(post: dict, topics: list[dict]) -> list[dict]:
    """Return topics that match this post's tags."""
    post_tags = {t.lower() for t in post.get('tags', [])}
    return [
        t for t in topics
        if post_tags & {tag.lower() for tag in (t.get('tags') or [])}
    ]


def _now_badges(content: str) -> str:
    """Extract h2 section titles from now.md and render as status badges."""
    headings = re.findall(r'^## (.+)$', content, re.MULTILINE)
    if not headings:
        return ''
    badges = ''.join(
        f'<span class="now-badge"><span class="now-badge-value">{escape(h)}</span></span>'
        for h in headings
    )
    return f'<div class="now-badges">{badges}</div>'


def generate_now(posts: list[dict] = None, topics: list[dict] = None) -> str:
    """Generate the /now page from now.md."""
    if NOW_FILE.exists():
        _, content = parse_frontmatter(NOW_FILE.read_text(encoding='utf-8'))
        md_renderer.reset()
        body_html = style_bridge_in(autolink_urls(md_renderer.convert(content)))
        badges_html = _now_badges(content)
        last_mod = ''
        # Extract "last updated" line if present
        m = re.search(r'_[Ll]ast updated[^_]*_', content)
        if m:
            last_mod = f'<p class="post-stats">{escape(m.group(0).strip("_"))}</p>'
    else:
        body_html = '<p class="muted">Add a <code>now.md</code> file in the project root to populate this page.</p>'
        badges_html = ''
        last_mod = ''

    topics_section = _topics_home_html(posts or [], topics or [])

    return f'''{head_html("Now", depth=1, description=f"What {SITE_NAME} is doing now.", canonical_path='/now/')}
<body>
<div class="noise-overlay" aria-hidden="true"></div>
{nav_html(active='now', depth=1)}

<div class="page-container">
  <div class="about-header">
    <h1>Now</h1>
    {last_mod}
    {badges_html}
  </div>
  <div class="post-content now-content">
    {body_html}
  </div>
  {topics_section}
</div>

{footer_html()}
</body>
</html>'''


def generate_topics_index(posts: list[dict], topics: list[dict]) -> str:
    """Generate the /topics/ index page."""
    cards_html = ''
    for topic in topics:
        topic_posts = [p for p in posts if any(t['slug'] == topic['slug'] for t in p.get('topics', []))]
        count = len(topic_posts)
        if count == 0:
            continue
        url = f'{topic["slug"]}/'
        desc = escape(topic.get('description', ''))
        cards_html += f'''<a href="{url}" class="topic-card reveal">
  <div class="topic-card-name">{escape(topic["name"])}</div>
  <div class="topic-card-desc">{desc}</div>
  <div class="topic-card-count">{count} posts</div>
</a>\n'''

    return f'''{head_html("Topics", depth=1, description=f"Writing themes by {SITE_NAME}.", canonical_path='/topics/')}
<body>
<div class="noise-overlay" aria-hidden="true"></div>
{nav_html(active='topics', depth=1)}

<div class="page-container">
  <div class="about-header">
    <h1>Topics</h1>
  </div>
  <div class="topics-grid">
    {cards_html}
  </div>
</div>

{footer_html()}
</body>
</html>'''


def generate_topic_page(topic: dict, posts: list[dict]) -> str:
    """Generate a /topics/{slug}/ page listing all posts in that topic."""
    topic_posts = [p for p in posts if any(t['slug'] == topic['slug'] for t in p.get('topics', []))]
    total = len(topic_posts)

    archive_html = ''
    current_year = ''
    for p in topic_posts:
        if p['year'] != current_year:
            current_year = p['year']
            archive_html += f'<div class="archive-year-header">{current_year}</div>\n'
        tags = render_tags_html(p['tags'], limit=3)
        url = f"../../posts/{p['year']}/{p['month']}/{p['slug']}/"
        archive_html += f'''<div class="archive-row reveal">
  <span class="archive-date">{p['date']}</span>
  <span class="archive-title"><a href="{url}">{escape(p['title'])}</a></span>
  <span class="archive-tags">{tags}</span>
</div>\n'''

    desc = escape(topic.get('description', ''))
    return f'''{head_html(topic["name"], depth=2, description=topic.get("description", ""), canonical_path=f'/topics/{topic["slug"]}/')}
<body>
<div class="noise-overlay" aria-hidden="true"></div>
{nav_html(active='topics', depth=2)}

<div class="page-container">
  <div class="about-header">
    <div class="topic-breadcrumb"><a href="../../topics/">Topics</a> /</div>
    <h1>{escape(topic["name"])}</h1>
    <p class="muted">{desc}</p>
    <p class="post-stats">{total} posts</p>
  </div>
  <div class="archive-list">
    {archive_html}
  </div>
</div>

{footer_html()}
</body>
</html>'''


def render_article_card(article: dict, depth: int = 0) -> str:
    """Render an article card with hero image, title, and subtitle."""
    prefix = '../' * depth
    url = prefix + article['url'].lstrip('/')
    if not url.endswith('/'):
        url += '/'
    tags_html = render_tags_html(article['tags'])

    hero = ''
    if article.get('hero_image'):
        hero_fname = _webp_name(article['hero_image'])
        hero_src = prefix + f"articles/{article['year']}/{article['month']}/{article['slug']}/{hero_fname}"
        hero = f'<img class="article-card-hero" src="{hero_src}" alt="" loading="lazy">'

    subtitle_html = ''
    if article.get('subtitle'):
        subtitle_html = f'<div class="article-card-subtitle">{escape(article["subtitle"])}</div>'

    return f'''<a href="{url}" class="article-card">
  {hero}
  <div class="article-card-body">
    <div class="article-card-title">{escape(article['title'])}</div>
    {subtitle_html}
    <div class="card-footer"><div class="card-tags">{tags_html}</div><div class="card-meta"><span class="card-date">{article['date']}</span><span class="card-reading-time">{article['reading_time']}</span></div></div>
  </div>
</a>'''


def generate_articles_archive(articles: list[dict], topics: list[dict]) -> str:
    """Generate the /articles/ archive page."""
    total = len(articles)

    cards_html = '\n'.join(render_article_card(a, depth=1) for a in articles)

    return f'''{head_html("Articles", depth=1, description=f"Long-form writing by {SITE_NAME}.", canonical_path='/articles/')}
<body>
<div class="noise-overlay" aria-hidden="true"></div>
{nav_html(active='articles', depth=1)}

<div class="page-container">
  <div class="posts-header">
    <h1>Articles</h1>
    <span class="posts-count">{total} articles</span>
    <p class="posts-description">Long-form essays on AI, engineering, and the judgment that doesn't automate.</p>
  </div>

  <div class="articles-grid">
    {cards_html}
  </div>

  {newsletter_cta_html()}
</div>

{footer_html()}
</body>
</html>'''


def generate_article_page(article: dict, topics: list[dict], depth: Optional[int] = None) -> str:
    """Generate an individual article page."""
    is_draft = bool(article.get('draft'))
    # Public articles live at /articles/YYYY/MM/slug/ (depth=4).
    # Drafts live at /articles/drafts/{token}/ (depth=3).
    if depth is None:
        depth = 3 if is_draft else 4

    md_renderer.reset()
    body_html = externalize_links(_rewrite_img_to_webp(style_bridge_in(autolink_urls(md_renderer.convert(expand_wide_fences(article['content']))))))

    tags_html = render_tags_html(article['tags'])

    # Topic badges
    article_topics = article.get('topics', [])
    topics_html = ''
    if article_topics:
        prefix_topics = '../' * depth
        topics_html = ''.join(
            f'<a href="{prefix_topics}topics/{t["slug"]}/" class="topic-badge">{escape(t["name"])}</a>'
            for t in article_topics
        )
        topics_html = f'<div class="post-topics">{topics_html}</div>'

    # Hero image
    hero_html = ''
    if article.get('hero_image'):
        hero_html = f'<img class="article-hero" src="{_webp_name(article["hero_image"])}" alt="" loading="lazy">'

    # Substack link
    substack_link = ''
    if article.get('substack_url'):
        substack_link = f'<a href="{article["substack_url"]}" class="post-original-link" target="_blank" rel="noopener">Also published on Substack →</a>'

    # Subtitle
    subtitle_html = ''
    if article.get('subtitle'):
        subtitle_html = f'<p class="article-subtitle">{escape(article["subtitle"])}</p>'

    # Draft banner — visual reminder that the page is unlisted
    draft_banner = ''
    if is_draft:
        draft_banner = (
            '<div class="draft-banner" style="background:#2a1a1a;border:1px solid #cc0000;'
            'color:#ffb3b3;padding:12px 16px;margin-top:80px;margin-bottom:24px;'
            'font-family:JetBrains Mono,monospace;font-size:13px;border-radius:2px;">'
            'DRAFT — unlisted review link. Do not share publicly.'
            '</div>'
        )

    # OG image (relative path used for the meta tag; absolute used for JSON-LD)
    og_image = ''
    image_url_abs = ''
    if article.get('hero_image'):
        hero_fname = _webp_name(article['hero_image'])
        if is_draft:
            og_image = f"articles/drafts/{article['draft_token']}/{hero_fname}"
        else:
            og_image = f"articles/{article['year']}/{article['month']}/{article['slug']}/{hero_fname}"
        if SITE_URL and not is_draft:
            image_url_abs = f'{SITE_URL}/{og_image.lstrip("/")}'

    description = (
        article.get('description')
        or article.get('subtitle')
        or article.get('preview', '')
    )[:160]

    canonical_path = '' if is_draft else article['url']

    article_jsonld = ''
    if not is_draft:
        article_jsonld = jsonld_article(article, image_url=image_url_abs)
        faq_jsonld = jsonld_faq(article['content'])
        if faq_jsonld:
            article_jsonld = article_jsonld + '\n  ' + faq_jsonld

    return f'''{head_html(article['title'][:60], depth=depth,
        description=description,
        og_type='article',
        og_image=og_image,
        large_image=bool(og_image),
        canonical_path=canonical_path,
        jsonld=article_jsonld,
        noindex=is_draft)}
<body>
<div class="noise-overlay" aria-hidden="true"></div>
<div id="reading-progress" class="reading-progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-hidden="true"></div>
{nav_html(active='articles', depth=depth)}

<div class="page-container article-page">
  {draft_banner}
  <div class="post-header"{ ' style="padding-top:0"' if is_draft else ''}>
    <h1 class="article-title">{escape(article['title'])}</h1>
    {subtitle_html}
    <div class="post-meta">
      <span class="post-date">{article['date']}</span>
      <span class="post-reading-time">{article['reading_time']}</span>
    </div>
    <div class="post-tags">{tags_html}</div>
  </div>

  {hero_html}

  <div class="post-content article-content">
    {body_html}
  </div>

  <div class="post-footer">
    {topics_html}
    <div class="post-actions">
      {substack_link}
      <button class="copy-link-btn" aria-label="Copy link">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg>
        <span>Copy link</span>
      </button>
    </div>
    {newsletter_cta_html()}
  </div>
</div>

{footer_html()}
<script>
document.querySelector('.copy-link-btn')?.addEventListener('click', function() {{
  navigator.clipboard.writeText(window.location.href).then(() => {{
    this.querySelector('span').textContent = 'Copied!';
    setTimeout(() => this.querySelector('span').textContent = 'Copy link', 2000);
  }});
}});
</script>
</body>
</html>'''


def _articles_home_section(articles: list[dict]) -> str:
    """Render a 'Latest Articles' section for the home page."""
    if not articles:
        return ''
    cards = '\n'.join(render_article_card(a, depth=0) for a in articles[:3])
    return f'''<section class="section">
    <div class="section-title">Articles</div>
    <div class="articles-grid">
      {cards}
    </div>
    <a href="articles/" class="view-all">All articles &rarr;</a>
  </section>'''


def _featured_spotlight_html(items: list[dict]) -> str:
    """Render the featured spotlight section with auto-rotating slides.

    Accepts articles (uses `hero_image`) or posts (uses first `media`).
    """
    if not items:
        return ''
    # Limit to 5 to keep dots manageable
    items = items[:5]

    slides_html = ''
    for i, p in enumerate(items):
        url = p['url'].lstrip('/')
        if not url.endswith('/'):
            url += '/'
        tags_html = render_tags_html(p['tags'])
        active = ' active' if i == 0 else ''

        image_html = ''
        text_only = ' spotlight-slide--text-only'
        img_src = None
        if p.get('hero_image'):
            hero_fname = _webp_name(p['hero_image'])
            img_src = f"articles/{p['year']}/{p['month']}/{p['slug']}/{hero_fname}"
        elif p.get('media'):
            thumb_fname = _webp_name(p['media'][0])
            img_src = f"posts/{p['year']}/{p['month']}/{p['slug']}/media/{thumb_fname}"
        if img_src:
            image_html = f'<div class="spotlight-image"><img src="{img_src}" alt="" loading="lazy"></div>'
            text_only = ''

        preview_text = p.get('subtitle') or p.get('preview') or ''

        slides_html += f'''<div class="spotlight-slide{active}{text_only}" data-index="{i}">
      <div class="spotlight-content">
        <h2 class="spotlight-title"><a href="{url}">{escape(p['title'])}</a></h2>
        <p class="spotlight-preview">{escape(preview_text)}</p>
        <div class="card-footer"><div class="card-tags">{tags_html}</div><div class="card-meta"><span class="card-date">{p['date']}</span><span class="card-reading-time">{p['reading_time']}</span></div></div>
      </div>
      {image_html}
    </div>\n'''

    dots_html = ''
    if len(items) > 1:
        dots = ''.join(
            f'<button class="spotlight-dot{" active" if i == 0 else ""}" data-index="{i}" aria-label="Slide {i+1}"></button>'
            for i in range(len(items))
        )
        dots_html = f'<div class="spotlight-dots">{dots}</div>'

    return f'''<section class="section" aria-label="Featured writing">
    <div class="section-title">Start Here</div>
    <div class="spotlight-viewport">
      <div class="spotlight-slides">
        {slides_html}
      </div>
      {dots_html}
    </div>
  </section>'''


def _recent_notes_html(posts: list[dict], limit: int = 6) -> str:
    """Render a compact strip of the most recent short-form posts."""
    if not posts:
        return ''
    recent = sorted(posts, key=lambda p: p['date'], reverse=True)[:limit]
    rows = []
    for p in recent:
        url = p['url'].lstrip('/')
        if not url.endswith('/'):
            url += '/'
        rows.append(
            f'<a class="note-row" href="{url}">'
            f'<span class="note-date">{p["date"]}</span>'
            f'<span class="note-title">{escape(p["title"])}</span>'
            f'</a>'
        )
    rows_html = '\n'.join(rows)
    return f'''<section class="section" aria-label="Recent notes">
    <div class="section-header">
      <div class="section-title">Recent notes</div>
      <a href="posts/" class="view-all">All posts &rarr;</a>
    </div>
    <div class="recent-notes">
      {rows_html}
    </div>
  </section>'''


def _topics_home_html(posts: list[dict], topics: list[dict]) -> str:
    """Render the top 3 topics (by post count) as cards on the home page."""
    if not topics:
        return ''
    scored = []
    for topic in topics:
        count = sum(
            1 for p in posts
            if any(t['slug'] == topic['slug'] for t in p.get('topics', []))
        )
        if count:
            scored.append((count, topic))
    if not scored:
        return ''
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:3]

    cards_html = ''
    for count, topic in top:
        url = f'/topics/{topic["slug"]}/'
        desc = escape(topic.get('description', ''))
        cards_html += f'''<a href="{url}" class="topic-card reveal">
      <div class="topic-card-name">{escape(topic["name"])}</div>
      <div class="topic-card-desc">{desc}</div>
      <div class="topic-card-count">{count} posts</div>
    </a>\n'''

    return f'''<section class="section" aria-label="Topics">
    <div class="section-header">
      <div class="section-title">Topics</div>
      <a href="topics/" class="view-all">All topics &rarr;</a>
    </div>
    <div class="topics-grid">
      {cards_html}
    </div>
  </section>'''


def _newsletter_section_html() -> str:
    """Render a full-width newsletter CTA section for the home page."""
    url = SITE.get('newsletter_url', '')
    if not url:
        return ''
    return f'''<section class="newsletter-section section">
    <div class="newsletter-section-inner">
      <p class="newsletter-section-heading">Stay in the loop</p>
      <p class="newsletter-section-text">Writing about engineering leadership, AI, and the craft of building software.</p>
      <a href="{url}" target="_blank" rel="noopener" class="newsletter-section-btn">Subscribe &rarr;</a>
    </div>
  </section>'''


def generate_home(posts: list[dict], articles: Optional[list[dict]] = None) -> str:
    """Generate the home page HTML."""
    all_articles = articles or []
    articles_by_date = sorted(all_articles, key=lambda a: a['date'], reverse=True)
    # Spotlight the 5 newest articles (rotating carousel).
    spotlight_articles = articles_by_date[:5]

    # Thesis text for the hero
    thesis_html = ''
    thesis_text = SITE.get('thesis', '')
    if thesis_text:
        # Allow natural line break after first sentence for readability
        thesis_escaped = escape(thesis_text)
        thesis_escaped = thesis_escaped.replace('when you do.', 'when you do.<br>', 1)
        thesis_html = f'<p class="hero-thesis">{thesis_escaped}</p>'

    home_script = f'<script src="js/home.js?v={_HOME_JS_VER}" defer></script>'

    return f'''{head_html("Home", depth=0, description=SITE_DESCRIPTION, extra_head=home_script, canonical_path='/')}
<body>
<div class="noise-overlay" aria-hidden="true"></div>
{nav_html(depth=0, transparent=True)}

<canvas id="hero-canvas" aria-hidden="true"></canvas>

<div class="hero-fullscreen">
  <div class="hero-fullscreen-content page-container">
    <h1>{escape(SITE['hero_title'])}</h1>
    {thesis_html}
    {_hero_links_html()}
  </div>
</div>

<div class="page-container">
  {_featured_spotlight_html(spotlight_articles)}

  {_recent_notes_html(posts)}

  {_topics_home_html(posts, SITE.get('topics', []))}

  {_newsletter_section_html()}
</div>

{footer_html()}
</body>
</html>'''


def _fmt_date_range(date_str: str) -> str:
    """Convert 'January 2024 – November 2025' → 'JAN 2024 — NOV 2025'."""
    parts = re.split(r'\s*[–—]\s*', date_str.strip())
    out = []
    for p in parts:
        p = p.strip()
        if p.lower() == 'present':
            out.append('PRESENT')
        else:
            m = re.match(r'^(\w+)\s+(\d{4})$', p)
            if m:
                out.append(f'{m.group(1)[:3].upper()} {m.group(2)}')
            else:
                out.append(p.upper())
    return ' — '.join(out)


def _parse_cv_sections(content: str) -> dict:
    """Split cv.md body into a dict of section_name → section_text."""
    sections: dict = {}
    current: Optional[str] = None
    buf: list = []

    for line in content.split('\n'):
        if line.startswith('## '):
            if current is not None:
                sections[current] = '\n'.join(buf).strip()
            current = line[3:].strip()
            buf = []
        elif current is None:
            # Pre-section content (title, tagline…) goes under '_intro'
            sections.setdefault('_intro', [])
            sections['_intro'].append(line)  # type: ignore[union-attr]
        else:
            buf.append(line)

    if current is not None:
        sections[current] = '\n'.join(buf).strip()
    if '_intro' in sections and isinstance(sections['_intro'], list):
        sections['_intro'] = '\n'.join(sections['_intro']).strip()
    return sections


def _parse_experience_entries(text: str) -> list[dict]:
    """Parse the Experience section text into a list of entry dicts.

    Recognized lines beneath the `### Company — Role` header:
      - `**Date Range** · Location` — date and location
      - `[badges] item · item · item` — pill row rendered under bullets
      - `- bullet` — highlight bullets
    """
    entries = []
    for raw in re.split(r'\n---\n', text):
        raw = raw.strip()
        if not raw:
            continue
        lines = raw.split('\n')

        # Header line: ### Company — Role
        m = re.match(r'^###\s+(.+?)\s+[—–]\s+(.+)$', lines[0])
        if not m:
            continue
        company = m.group(1).strip()
        role = m.group(2).strip()

        date_str = location = ''
        badges: list[str] = []
        for line in lines[1:]:
            stripped = line.strip()
            if not stripped:
                continue
            dm = re.match(r'^\*\*(.+?)\*\*\s*[·•]\s*(.+)$', stripped)
            if dm and not date_str:
                date_str = _fmt_date_range(dm.group(1))
                location = dm.group(2).strip()
                continue
            bm = re.match(r'^\[badges\]\s*(.+)$', stripped, re.IGNORECASE)
            if bm:
                badges = [b.strip() for b in re.split(r'\s*[·•]\s*', bm.group(1)) if b.strip()]
                continue

        bullets = [ln[2:].strip() for ln in lines if ln.startswith('- ')]

        entries.append({
            'company': company,
            'role': role,
            'date': date_str,
            'location': location,
            'bullets': bullets,
            'badges': badges,
        })
    return entries


def _render_timeline(entries: list[dict]) -> str:
    """Render .timeline HTML from parsed experience entries."""
    nodes = []
    for e in entries:
        company_html = style_bridge_in(escape(e['company']))
        bullets_html = ''
        if e['bullets']:
            items = ''.join(f'<li>{escape(b)}</li>' for b in e['bullets'])
            bullets_html = f'\n      <ul class="timeline-highlights">{items}</ul>'
        badges_html = ''
        if e.get('badges'):
            pills = ''.join(
                f'<span class="timeline-badge">{escape(b)}</span>' for b in e['badges']
            )
            badges_html = f'\n      <div class="timeline-badges">{pills}</div>'
        nodes.append(
            f'    <div class="timeline-node">\n'
            f'      <div class="timeline-date">{escape(e["date"])}</div>\n'
            f'      <div class="timeline-company">{company_html}</div>\n'
            f'      <div class="timeline-role">{escape(e["role"])}</div>\n'
            f'      <div class="timeline-location">{escape(e["location"])}</div>'
            f'{bullets_html}'
            f'{badges_html}\n'
            f'    </div>'
        )
    return '<div class="timeline">\n\n' + '\n\n'.join(nodes) + '\n\n  </div>'


def _render_skills(text: str) -> str:
    """Render .skills-section HTML from the Top Skills list."""
    rows = []
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('- '):
            skill = escape(line[2:].strip())
            rows.append(
                f'<div class="skill-row"><span class="skill-label">{skill}</span></div>'
            )
    if not rows:
        return ''
    return '<div class="skills-section">\n    ' + '\n    '.join(rows) + '\n  </div>'


def _parse_about_section(text: str) -> dict:
    """Parse a section into italic sub-headline, body markdown, and badges.

    Recognized lines:
      - `*italic concept line*` — single-line italic header (first one wins)
      - `[badges] item · item · item` — pill row
      - `[stats] value / label · value / label` — stat-pair row (hero only)
    Everything else is body markdown.
    """
    italic = ''
    badges: list[str] = []
    body_lines: list[str] = []

    seen_body = False
    for line in (text or '').split('\n'):
        stripped = line.strip()
        m = re.match(r'^\*([^*]+?)\*$', stripped)
        if m and not italic and not seen_body:
            italic = m.group(1).strip()
            continue
        bm = re.match(r'^\[(?:badges|stats)\]\s*(.+)$', stripped, re.IGNORECASE)
        if bm:
            badges = [b.strip() for b in re.split(r'\s*[·•]\s*', bm.group(1)) if b.strip()]
            continue
        if stripped:
            seen_body = True
        body_lines.append(line)

    body_md = '\n'.join(body_lines).strip()
    return {'italic': italic, 'body_md': body_md, 'badges': badges}


def _render_hero(name: str, parsed: dict, summary_md: str) -> str:
    """Render the about-page hero: name, italic headline, stat callouts, context."""
    headline = parsed.get('italic', '')
    stat_pairs = parsed.get('badges', [])

    headline_html = (
        f'  <p class="about-hero-headline">{escape(headline)}</p>\n' if headline else ''
    )

    stats_html = ''
    if stat_pairs:
        items = []
        for pair in stat_pairs:
            if '/' in pair:
                value, label = [p.strip() for p in pair.split('/', 1)]
            else:
                value, label = pair, ''
            items.append(
                '<div class="about-hero-stat">'
                f'<div class="about-hero-stat-value">{escape(value)}</div>'
                f'<div class="about-hero-stat-label">{escape(label)}</div>'
                '</div>'
            )
        stats_html = '  <div class="about-hero-stats">' + ''.join(items) + '</div>\n'

    context_html = ''
    if summary_md:
        md_renderer.reset()
        rendered = style_bridge_in(autolink_urls(md_renderer.convert(summary_md)))
        context_html = f'  <div class="about-hero-context">{rendered}</div>\n'

    return (
        '<section class="about-hero">\n'
        f'  <h1 class="about-hero-name">{escape(name)}</h1>\n'
        f'{headline_html}{stats_html}{context_html}'
        '</section>'
    )


def _render_about_section(num: str, label: str, parsed: dict,
                         body_html_override: Optional[str] = None,
                         extra_class: str = '') -> str:
    """Render a numbered about-page section."""
    italic_html = ''
    if parsed.get('italic'):
        italic_html = (
            f'\n  <div class="about-section-italic">{escape(parsed["italic"])}</div>'
        )

    if body_html_override is not None:
        body_inner = body_html_override
    elif parsed.get('body_md'):
        md_renderer.reset()
        body_inner = style_bridge_in(autolink_urls(md_renderer.convert(parsed['body_md'])))
    else:
        body_inner = ''

    badges_html = ''
    if parsed.get('badges'):
        pills = ''.join(
            f'<span class="about-badge">{escape(b)}</span>' for b in parsed['badges']
        )
        badges_html = f'\n  <div class="about-badges">{pills}</div>'

    cls = 'about-section' + (f' {extra_class}' if extra_class else '')
    return (
        f'<section class="{cls}">\n'
        '  <div class="about-section-header">\n'
        f'    <span class="about-section-num">{escape(num)}</span>\n'
        f'    <span class="about-section-label">{escape(label)}</span>\n'
        '  </div>'
        f'{italic_html}\n'
        f'  <div class="about-section-body">{body_inner}</div>'
        f'{badges_html}\n'
        '</section>'
    )


def _extract_name_from_intro(intro: str, fallback: str) -> str:
    """Pull the name from cv.md `# Name` header; fall back to provided default."""
    for line in (intro or '').split('\n'):
        stripped = line.strip()
        if stripped.startswith('# '):
            return stripped[2:].strip()
    return fallback


def generate_about() -> str:
    """Generate the about page HTML from cv.md (if present).

    Structure:
      Hero (name, italic headline, 3 stat callouts, context paragraph)
      01 — Thesis
      02 — What I'm Building
      03 — How I Got Here  (timeline with metric badges)
      04 — Open To  (soft-pitch CTA)
      Footer CTA (social links + Download CV + small Education/Languages strip)
    """
    # Social links
    social_parts = []
    if LINKEDIN:
        social_parts.append(f'<a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>')
    if GITHUB:
        social_parts.append(f'<a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>')
    if TWITTER:
        social_parts.append(f'<a href="{TWITTER}" target="_blank" rel="noopener">X</a>')
    if SUBSTACK:
        social_parts.append(f'<a href="{SUBSTACK}" target="_blank" rel="noopener">Substack</a>')
    if CV_PDF.exists():
        social_parts.append('<a href="cv_joaofogoncalves.pdf" download>Download CV</a>')

    sep = '<span class="muted" style="margin:0 0.75rem">&middot;</span>'
    social_html = sep.join(social_parts)

    if not CV_FILE.exists():
        body = (
            '<p class="muted">Add a <code>cv.md</code> file in the project root '
            'to populate this page.</p>'
        )
        return f'''{head_html("About", depth=1, jsonld=jsonld_person(), canonical_path='/about/')}
<body>
<div class="noise-overlay" aria-hidden="true"></div>
{nav_html(active='about', depth=1)}

<div class="page-container">
  <div class="about-header">
    <h1>About</h1>
  </div>
  {body}
  <div class="about-cta">
    <div class="about-cta-links">{social_html}</div>
  </div>
</div>

{footer_html()}
</body>
</html>'''

    cv_text = CV_FILE.read_text(encoding='utf-8')
    _, cv_content = parse_frontmatter(cv_text)
    sections = _parse_cv_sections(cv_content)

    name = _extract_name_from_intro(sections.get('_intro', ''), SITE_NAME)

    hero_parsed = _parse_about_section(sections.get('Hero', ''))
    summary_md = sections.get('Summary', '').strip()
    thesis_parsed = _parse_about_section(sections.get('Thesis', ''))
    building_parsed = _parse_about_section(sections.get('Building', ''))
    open_to_parsed = _parse_about_section(sections.get('Open To', ''))

    hero_html = _render_hero(name, hero_parsed, summary_md)

    thesis_html = (
        _render_about_section('01', 'Thesis', thesis_parsed)
        if thesis_parsed['body_md']
        else ''
    )

    building_html = (
        _render_about_section('02', "What I'm Building", building_parsed)
        if building_parsed['body_md']
        else ''
    )

    # 03 — How I Got Here: render the timeline as the section body
    experience_text = sections.get('Experience', '')
    entries = _parse_experience_entries(experience_text)
    history_html = ''
    if entries:
        timeline_html = _render_timeline(entries)
        history_parsed = {
            'italic': 'Fifteen years before BRIDGE IN.',
            'body_md': '',
            'badges': [],
        }
        history_html = _render_about_section(
            '03',
            'How I Got Here',
            history_parsed,
            body_html_override=timeline_html,
        )

    # 04 — Open To: stronger CTA styling via .about-pitch variant
    open_to_html = (
        _render_about_section(
            '04',
            'Open To',
            open_to_parsed,
            extra_class='about-pitch',
        )
        if open_to_parsed['body_md']
        else ''
    )

    # Footer metadata strip: Education + Languages
    edu_text = ''
    edu_raw = sections.get('Education', '').strip()
    if edu_raw:
        edu_lines = [l for l in edu_raw.split('\n') if l.strip()]
        if edu_lines:
            uni = edu_lines[0].lstrip('#').strip()
            degree = ''
            if len(edu_lines) > 1:
                degree = edu_lines[1].split('·')[0].split('(')[0].strip()
            edu_text = uni + (f' — {degree}' if degree else '')

    languages_text = ''
    lang_raw = sections.get('Languages', '').strip()
    if lang_raw:
        langs = []
        for line in lang_raw.split('\n'):
            line = line.strip()
            if line.startswith('- '):
                lang = line[2:].split('(')[0].strip()
                if lang:
                    langs.append(lang)
        if langs:
            languages_text = ' · '.join(langs)

    meta_lines = []
    if edu_text:
        meta_lines.append(f'<div>{escape(edu_text)}</div>')
    if languages_text:
        meta_lines.append(f'<div>{escape(languages_text)}</div>')
    meta_block = ''
    if meta_lines:
        meta_block = (
            '\n  <div class="about-cta-meta">\n    '
            + '\n    '.join(meta_lines)
            + '\n  </div>'
        )

    cta_html = (
        '<div class="about-cta">\n'
        f'  <div class="about-cta-links">{social_html}</div>'
        f'{meta_block}\n'
        '</div>'
    )

    return f'''{head_html("About", depth=1, jsonld=jsonld_person(), canonical_path='/about/')}
<body>
<div class="noise-overlay" aria-hidden="true"></div>
{nav_html(active='about', depth=1)}

<div class="page-container about-page">
  {hero_html}
  {thesis_html}
  {building_html}
  {history_html}
  {open_to_html}
  {cta_html}
</div>

{footer_html()}
</body>
</html>'''


def _render_list_card(post: dict, depth: int = 0) -> str:
    """Render a post as a full-width list row (spotlight-style)."""
    prefix = '../' * depth
    url = prefix + post['url'].lstrip('/')
    if not url.endswith('/'):
        url += '/'
    tags_html = render_tags_html(post['tags'])

    thumb = ''
    if post.get('media'):
        thumb_fname = _webp_name(post['media'][0])
        thumb_src = prefix + f"posts/{post['year']}/{post['month']}/{post['slug']}/media/{thumb_fname}"
        thumb = f'<div class="list-card-image"><img src="{thumb_src}" alt="" loading="lazy"></div>'

    return f'''<a href="{url}" class="list-card">
  <div class="list-card-body">
    <div class="list-card-title">{escape(post['title'])}</div>
    <div class="list-card-preview">{escape(post['preview'])}</div>
    <div class="card-footer"><div class="card-tags">{tags_html}</div><div class="card-meta"><span class="card-date">{post['date']}</span><span class="card-reading-time">{post['reading_time']}</span></div></div>
  </div>
  {thumb}
</a>'''


def generate_posts_archive(posts: list[dict]) -> str:
    """Generate the posts archive page with JS-powered filtering."""
    total = len(posts)

    # Server-render the first page for no-JS fallback
    fallback_cards = '\n'.join(_render_list_card(p, depth=1) for p in posts[:20])

    return f'''{head_html("Posts", depth=1, canonical_path='/posts/')}
<body>
<div class="noise-overlay" aria-hidden="true"></div>
{nav_html(active='posts', depth=1)}

<div class="page-container">
  <div class="posts-header">
    <h1>Posts</h1>
    <span class="posts-count" id="posts-count">{total} posts</span>
    <p class="posts-description">Short-form notes on AI, engineering, and the work in flight.</p>
  </div>

  <div class="filters">
    <input type="text" class="search-input" id="search-input" placeholder="Search posts...">
    <div class="year-filters" id="year-filters"></div>
    <div class="tag-filters" id="tag-filters"></div>
    <div class="filter-status" id="filter-status"></div>
  </div>

  <section id="archive-section">
    <div class="posts-list" id="archive-list">
      {fallback_cards}
    </div>
    <div class="empty-state" id="empty-state">No posts match that filter.</div>
    <div class="load-more-container" id="load-more-container">
      <button class="load-more-btn" id="load-more-btn">Load more</button>
    </div>
  </section>
</div>

{footer_html()}
</body>
</html>'''


def generate_post_page(post: dict, prev_post: Optional[dict], next_post: Optional[dict], depth: int = 4) -> str:
    """Generate an individual post page."""
    # Clean and render content. Strip inline media/ image refs — they render in the
    # bottom gallery instead so the body stays text-first.
    cleaned = clean_content(post['content'])
    cleaned = re.sub(r'!\[[^\]]*\]\(media/[^)]+\)\s*', '', cleaned).strip()
    md_renderer.reset()
    body_html = md_renderer.convert(cleaned)
    body_html = externalize_links(_rewrite_img_to_webp(autolink_urls(body_html)))

    tags_html = render_tags_html(post['tags'])
    read_time = reading_time(cleaned)

    # Topic badges
    post_topics = post.get('topics', [])
    topics_html = ''
    if post_topics:
        prefix_topics = '../../../../'
        topics_html = ''.join(
            f'<a href="{prefix_topics}topics/{t["slug"]}/" class="topic-badge">{escape(t["name"])}</a>'
            for t in post_topics
        )
        topics_html = f'<div class="post-topics">{topics_html}</div>'

    # OG image: use first media if available, else headshot
    post_og_image = ''
    post_image_abs = ''
    if post.get('media'):
        media_fname = _webp_name(post['media'][0])
        post_og_image = f"posts/{post['year']}/{post['month']}/{post['slug']}/media/{media_fname}"
        if SITE_URL:
            post_image_abs = f'{SITE_URL}/{post_og_image.lstrip("/")}'

    # Fix media paths — they reference media/image-1.jpg, which is correct
    # since media/ is copied into the same directory

    # Build prev/next nav
    prefix = '../../../../'
    prev_link = ''
    next_link = ''
    if prev_post:
        prev_url = prefix + prev_post['url'].lstrip('/')
        prev_link = f'<a href="{prev_url}">← Previous</a>'
    if next_post:
        next_url = prefix + next_post['url'].lstrip('/')
        next_link = f'<a href="{next_url}">Next →</a>'

    # Media gallery: render all images at the bottom (inline refs already stripped above)
    image_exts = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
    gallery_html = ''
    if post.get('media'):
        gallery_items = []
        for fname in post['media']:
            if not fname.lower().endswith(image_exts):
                continue
            src = _webp_name(fname)
            gallery_items.append(
                f'<a class="post-media-item" href="media/{src}" target="_blank" rel="noopener">'
                f'<img src="media/{src}" alt="" loading="lazy">'
                f'</a>'
            )
        if gallery_items:
            gallery_html = f'<div class="post-media-gallery">{"".join(gallery_items)}</div>'

    backlinks = []
    if post.get('post_url'):
        backlinks.append(f'<a href="{post["post_url"]}" class="post-original-link" target="_blank" rel="noopener">View on LinkedIn →</a>')
    if post.get('x_url'):
        backlinks.append(f'<a href="{post["x_url"]}" class="post-original-link" target="_blank" rel="noopener">View on X →</a>')
    if post.get('substack_note_url'):
        backlinks.append(f'<a href="{post["substack_note_url"]}" class="post-original-link" target="_blank" rel="noopener">View on Substack →</a>')
    original_link = ''.join(backlinks)

    description = (post.get('description') or post.get('preview', ''))[:160]

    return f'''{head_html(post['title'][:60], depth=depth,
        description=description,
        og_type='article',
        og_image=post_og_image,
        large_image=bool(post_og_image),
        canonical_path=post['url'],
        jsonld=jsonld_article(post, image_url=post_image_abs))}
<body>
<div class="noise-overlay" aria-hidden="true"></div>
<div id="reading-progress" class="reading-progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-hidden="true"></div>
{nav_html(active='posts', depth=depth)}

<div class="page-container">
  <div class="post-header">
    <div class="post-meta">
      <span class="post-date">{post['date']}</span>
      <span class="post-reading-time">{read_time}</span>
    </div>
    <div class="post-tags">{tags_html}</div>
  </div>

  <div class="post-content">
    {body_html}
  </div>

  {gallery_html}

  <div class="post-footer">
    {topics_html}
    <div class="post-actions">
      {original_link}
      <button class="copy-link-btn" aria-label="Copy link">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg>
        <span>Copy link</span>
      </button>
    </div>
    {newsletter_cta_html()}
    <div class="post-nav">
      {prev_link}
      <span></span>
      {next_link}
    </div>
  </div>
</div>

{footer_html()}
<script>
document.querySelector('.copy-link-btn')?.addEventListener('click', function() {{
  navigator.clipboard.writeText(window.location.href).then(() => {{
    this.querySelector('span').textContent = 'Copied!';
    setTimeout(() => this.querySelector('span').textContent = 'Copy link', 2000);
  }});
}});
</script>
</body>
</html>'''


# ============================================================
# Build Pipeline
# ============================================================

def generate_posts_json(posts: list[dict]) -> str:
    """Generate JSON index for client-side search/filter."""
    entries = []
    for p in posts:
        entries.append({
            'date': p['date'],
            'title': p['title'],
            'preview': p['preview'],
            'reading_time': p['reading_time'],
            'tags': p['tags'],
            'url': p['url'],
            'slug': p['slug'],
            'year': p['year'],
            'month': p['month'],
            'type': p['post_type'],
            'media': _webp_name(p['media'][0]) if p['media'] else '',
        })
    return json.dumps(entries, ensure_ascii=False, indent=None)


def _webp_name(fname: str) -> str:
    """Return the WebP filename for a given image, or the original if not convertible."""
    stem, suffix = os.path.splitext(fname)
    if suffix.lower() in ('.jpg', '.jpeg', '.png'):
        return stem + '.webp'
    return fname


def _rewrite_img_to_webp(html: str) -> str:
    """Rewrite img src references from .jpg/.png to .webp in rendered HTML."""
    def _replace(m):
        prefix = m.group(1)
        stem = m.group(2)
        return f'{prefix}{stem}.webp"'
    return re.sub(
        r'(<img[^>]+src="[^"]*?)([^"/]+)\.(jpg|jpeg|png)"',
        _replace,
        html,
    )


def _absolutize_img_src(html: str, base_url: str) -> str:
    """Resolve relative <img src> paths against base_url. Used for RSS where
    feed readers can't resolve paths relative to the article page."""
    def _replace(m):
        prefix = m.group(1)
        src = m.group(2)
        if src.startswith(('http://', 'https://', '//', '/', 'data:')):
            return m.group(0)
        return f'{prefix}{base_url}{src}"'
    return re.sub(r'(<img[^>]+src=")([^"]+)"', _replace, html)


def _optimize_image(src: Path, dst_dir: Path) -> None:
    """Copy image to dst_dir, converting JPG/PNG to WebP when beneficial."""
    suffix = src.suffix.lower()
    if suffix in ('.jpg', '.jpeg', '.png'):
        webp_dst = dst_dir / (src.stem + '.webp')
        if not webp_dst.exists():
            try:
                img = Image.open(src)
                img.save(webp_dst, 'WEBP', quality=82)
                # Only keep WebP if it's actually smaller
                if webp_dst.stat().st_size >= src.stat().st_size:
                    webp_dst.unlink()
                    shutil.copy2(src, dst_dir / src.name)
            except Exception:
                # Fall back to plain copy on any image error
                if webp_dst.exists():
                    webp_dst.unlink()
                shutil.copy2(src, dst_dir / src.name)
    else:
        shutil.copy2(src, dst_dir / src.name)


def copy_media(posts: list[dict]):
    """Copy media directories from source posts into dist, optimizing images."""
    for p in posts:
        if not p['media']:
            continue
        src_media = Path(p['source_dir']) / 'media'
        dst_media = DIST_DIR / 'posts' / p['year'] / p['month'] / p['slug'] / 'media'
        if dst_media.exists():
            continue
        dst_media.mkdir(parents=True, exist_ok=True)
        for fname in p['media']:
            src = src_media / fname
            if src.exists():
                _optimize_image(src, dst_media)


def copy_article_media(articles: list[dict]):
    """Copy media directories from source articles into dist, optimizing images."""
    for a in articles:
        if not a['media']:
            continue
        src_media = Path(a['source_dir']) / 'media'
        if a.get('draft'):
            dst_media = DIST_DIR / 'articles' / 'drafts' / a['draft_token'] / 'media'
        else:
            dst_media = DIST_DIR / 'articles' / a['year'] / a['month'] / a['slug'] / 'media'
        if dst_media.exists():
            continue
        dst_media.mkdir(parents=True, exist_ok=True)
        for fname in a['media']:
            src = src_media / fname
            if src.exists():
                _optimize_image(src, dst_media)


def build():
    """Main build function."""
    print('Parsing posts...')
    posts = parse_all_posts()
    print(f'  Found {len(posts)} original/article posts')

    print('Parsing articles...')
    all_articles = parse_all_articles()
    articles = [a for a in all_articles if not a.get('draft')]
    draft_articles = [a for a in all_articles if a.get('draft')]
    print(f'  Found {len(articles)} articles ({len(draft_articles)} drafts)')

    # Assign topics to each post and article
    topics = SITE.get('topics', [])
    for post in posts:
        post['topics'] = assign_post_topics(post, topics)
    for article in all_articles:
        article['topics'] = assign_post_topics(article, topics)

    # Clean dist
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)

    # Copy static assets (minify CSS)
    print('Copying assets...')
    (DIST_DIR / 'css').mkdir(parents=True)
    css_text = (CSS_SRC / 'style.css').read_text(encoding='utf-8')
    (DIST_DIR / 'css' / 'style.css').write_text(minify_css(css_text), encoding='utf-8')
    shutil.copytree(JS_SRC, DIST_DIR / 'js')
    if IMG_SRC.exists():
        shutil.copytree(IMG_SRC, DIST_DIR / 'img')

    # Generate home page
    print('Generating home page...')
    (DIST_DIR / 'index.html').write_text(generate_home(posts, articles), encoding='utf-8')

    # Generate about page
    print('Generating about page...')
    about_dir = DIST_DIR / 'about'
    about_dir.mkdir(parents=True)
    (about_dir / 'index.html').write_text(generate_about(), encoding='utf-8')
    if CV_PDF.exists():
        shutil.copy2(CV_PDF, about_dir / 'cv_joaofogoncalves.pdf')

    # Generate /now page
    if NOW_FILE.exists():
        print('Generating /now page...')
        now_dir = DIST_DIR / 'now'
        now_dir.mkdir(parents=True)
        (now_dir / 'index.html').write_text(generate_now(posts, topics), encoding='utf-8')

    # Generate /topics pages
    if topics:
        print(f'Generating /topics pages ({len(topics)} topics)...')
        topics_dir = DIST_DIR / 'topics'
        topics_dir.mkdir(parents=True)
        (topics_dir / 'index.html').write_text(generate_topics_index(posts, topics), encoding='utf-8')
        for topic in topics:
            topic_dir = topics_dir / topic['slug']
            topic_dir.mkdir(parents=True)
            (topic_dir / 'index.html').write_text(generate_topic_page(topic, posts), encoding='utf-8')

    # Generate articles section
    if articles or draft_articles:
        articles_dir = DIST_DIR / 'articles'
        articles_dir.mkdir(parents=True, exist_ok=True)

        if articles:
            print(f'Generating articles section ({len(articles)} articles)...')
            (articles_dir / 'index.html').write_text(
                generate_articles_archive(articles, topics), encoding='utf-8')

            for article in articles:
                article_dir = articles_dir / article['year'] / article['month'] / article['slug']
                article_dir.mkdir(parents=True, exist_ok=True)
                html = generate_article_page(article, topics)
                (article_dir / 'index.html').write_text(html, encoding='utf-8')

        if draft_articles:
            print(f'Generating draft articles ({len(draft_articles)} drafts, unlisted)...')
            drafts_root = articles_dir / 'drafts'
            drafts_root.mkdir(parents=True, exist_ok=True)
            for article in draft_articles:
                draft_dir = drafts_root / article['draft_token']
                draft_dir.mkdir(parents=True, exist_ok=True)
                html = generate_article_page(article, topics)
                (draft_dir / 'index.html').write_text(html, encoding='utf-8')
                print(f'  Draft: /articles/drafts/{article["draft_token"]}/  ({article["slug"]})')

        print('Copying article media...')
        copy_article_media(articles + draft_articles)

    # Generate posts archive
    print('Generating posts archive...')
    posts_dir = DIST_DIR / 'posts'
    posts_dir.mkdir(parents=True)
    (posts_dir / 'index.html').write_text(generate_posts_archive(posts), encoding='utf-8')

    # Generate posts.json
    (posts_dir / 'posts.json').write_text(generate_posts_json(posts), encoding='utf-8')

    # Generate individual post pages
    print(f'Generating {len(posts)} post pages...')
    for i, post in enumerate(posts):
        prev_post = posts[i - 1] if i > 0 else None
        next_post = posts[i + 1] if i < len(posts) - 1 else None

        post_dir = posts_dir / post['year'] / post['month'] / post['slug']
        post_dir.mkdir(parents=True, exist_ok=True)
        html = generate_post_page(post, prev_post, next_post)
        (post_dir / 'index.html').write_text(html, encoding='utf-8')

    # Copy media files
    print('Copying media...')
    copy_media(posts)

    # Generate RSS feed
    print('Generating RSS feed...')
    (DIST_DIR / 'feed.xml').write_text(generate_rss(articles), encoding='utf-8')

    # Generate sitemap
    print('Generating sitemap...')
    (DIST_DIR / 'sitemap.xml').write_text(generate_sitemap(posts, articles), encoding='utf-8')

    # Generate robots.txt — disallow drafts tree (noindex meta also set per-page)
    robots = 'User-agent: *\nAllow: /\nDisallow: /articles/drafts/\n'
    if SITE_URL:
        robots += f'Sitemap: {SITE_URL}/sitemap.xml\n'
    (DIST_DIR / 'robots.txt').write_text(robots, encoding='utf-8')

    # Generate .htaccess for cache and compression headers
    htaccess = '''\
# Cache static assets aggressively (CSS/JS use ?v= cache busters)
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/x-icon "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType application/pdf "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType text/html "access plus 0 seconds"
  ExpiresByType application/xml "access plus 1 hour"
  ExpiresByType application/json "access plus 1 hour"
</IfModule>

# Gzip compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json application/xml text/xml image/svg+xml
</IfModule>
'''
    (DIST_DIR / '.htaccess').write_text(htaccess, encoding='utf-8')

    print(f'\nBuild complete! Output in {DIST_DIR}')
    print(f'  {len(posts)} post pages')
    print(f'  {len(articles)} article pages')
    print(f'  Global files: home, about, posts, articles, posts.json, feed.xml, sitemap.xml')


if __name__ == '__main__':
    build()
