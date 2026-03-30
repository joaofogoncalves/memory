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
from html import escape
from pathlib import Path

import markdown
import yaml
from dotenv import load_dotenv

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
        'hero_title': cfg.get('hero_title', cfg.get('site_name', 'My Site')),
        'hero_subline': cfg.get('hero_subline', ''),
        'about_teaser': cfg.get('about_teaser', ''),
        'footer_text': cfg.get('footer_text', cfg.get('site_name', 'My Site')),
        'speaking_text': cfg.get('speaking_text', ''),
    }

SITE = _load_site_config()
SITE_NAME = SITE['site_name']
SITE_URL = os.environ.get('SITE_URL', '').rstrip('/')
SITE_DESCRIPTION = SITE['site_description']
LINKEDIN = SITE['linkedin']
GITHUB = SITE['github']
TWITTER = SITE['twitter']
TWITTER_HANDLE = SITE['twitter_handle']

md_renderer = markdown.Markdown(extensions=['fenced_code', 'tables', 'smarty'], output_format='html')


def _asset_hash(path: Path, length: int = 8) -> str:
    """Return a short SHA-256 hash of a file's contents for cache-busting."""
    if not path.exists():
        return '0'
    return hashlib.sha256(path.read_bytes()).hexdigest()[:length]


# Compute once at build time so every page gets the same version strings
_CSS_VER = _asset_hash(CSS_SRC / 'style.css')
_JS_VER = _asset_hash(JS_SRC / 'posts.js')


def autolink_urls(html: str) -> str:
    """Convert bare URLs in HTML text nodes into clickable links."""
    def replace_url(m):
        prefix = m.group(1)
        url = m.group(2)
        # Skip if already inside an href or src attribute
        if prefix in ('="', "='", '>'):
            return m.group(0)
        return f'{prefix}<a href="{url}" target="_blank" rel="noopener">{url}</a>'

    return re.sub(
        r'(="|=\'|>|^|\s)(https?://[^\s<>"\']+)',
        replace_url,
        html
    )


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
    """Return list of media filenames in post's media/ dir."""
    media_dir = post_dir / 'media'
    if not media_dir.exists():
        return []
    return [f.name for f in sorted(media_dir.iterdir()) if f.is_file()]


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

        posts.append({
            'date': date_str,
            'year': year,
            'month': month,
            'slug': slug,
            'title': title,
            'preview': preview,
            'reading_time': read_time,
            'tags': [str(t) for t in (fm.get('tags', []) or [])],
            'post_type': post_type,
            'post_url': fm.get('post_url', ''),
            'url': url_path,
            'media': media_files,
            'source_dir': str(post_dir),
            'content': content,
        })

    # Sort by date descending
    posts.sort(key=lambda p: p['date'], reverse=True)
    return posts


# ============================================================
# HTML Templates
# ============================================================

GOOGLE_FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&'
    'family=JetBrains+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">'
)


def ga_snippet() -> str:
    """Return Google Analytics gtag.js snippet if GA_MEASUREMENT_ID is set."""
    ga_id = os.environ.get('GA_MEASUREMENT_ID', '').strip()
    if not ga_id:
        return ''
    return (
        f'<script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>\n'
        f'  <script>\n'
        f'    window.dataLayer = window.dataLayer || [];\n'
        f'    function gtag(){{dataLayer.push(arguments);}}\n'
        f"    gtag('js', new Date());\n"
        f"    gtag('config', '{ga_id}');\n"
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
            og_image: str = '', depth: int = 0) -> str:
    """Generate Open Graph and Twitter Card meta tags."""
    prefix = '../' * depth
    desc = escape(description or SITE_DESCRIPTION)
    img = og_image or f'{prefix}img/headshot.jpg'
    if SITE_URL and not img.startswith('http'):
        img = f'{SITE_URL}/{img.lstrip("/")}'
    lines = [
        f'<meta property="og:title" content="{escape(title)}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:image" content="{img}">',
        f'<meta name="twitter:card" content="summary">',
        f'<meta name="twitter:site" content="{TWITTER_HANDLE}">',
    ]
    if SITE_URL:
        lines.append(f'<meta property="og:site_name" content="{SITE_NAME}">')
    return '\n  '.join(lines)


def head_html(title: str, depth: int = 0, extra_head: str = '',
              description: str = '', og_type: str = 'website', og_image: str = '') -> str:
    """Generate <head> with proper relative paths."""
    prefix = '../' * depth
    ga = ga_snippet()
    desc = escape(description or SITE_DESCRIPTION)
    og = og_tags(title, description, og_type, og_image, depth)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#0e131e">
  <title>{escape(title)} — {SITE_NAME}</title>
  <meta name="description" content="{desc}">
  {FAVICON.format(prefix=prefix)}
  {og}
  {ga}
  {GOOGLE_FONTS}
  <link rel="stylesheet" href="{prefix}css/style.css?v={_CSS_VER}">
  <script src="{prefix}js/posts.js?v={_JS_VER}" defer></script>
  {extra_head}
</head>'''


def nav_html(active: str = '', depth: int = 0) -> str:
    prefix = '../' * depth
    about_cls = ' active' if active == 'about' else ''
    posts_cls = ' active' if active == 'posts' else ''
    return f'''<nav class="nav">
  <div class="nav-inner">
    <a href="{prefix}" class="nav-logo-link"><img src="{prefix}img/logo.png" alt="JG" class="nav-logo" width="24" height="24"></a>
    <div class="nav-links">
      <a href="{prefix}about/" class="{about_cls}">About</a>
      <a href="{prefix}posts/" class="{posts_cls}">Posts</a>
    </div>
  </div>
</nav>'''


SVG_LINKEDIN = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>'
SVG_GITHUB = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>'
SVG_X = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>'


def footer_html() -> str:
    social_links = ''
    if LINKEDIN:
        social_links += f'<a href="{LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn">{SVG_LINKEDIN}</a>'
    if GITHUB:
        social_links += f'<a href="{GITHUB}" target="_blank" rel="noopener" aria-label="GitHub">{SVG_GITHUB}</a>'
    if TWITTER:
        social_links += f'<a href="{TWITTER}" target="_blank" rel="noopener" aria-label="X">{SVG_X}</a>'
    links_div = f'<div class="footer-links">{social_links}</div>' if social_links else ''
    return f'''<button class="scroll-top" id="scroll-top" aria-label="Scroll to top">
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


def render_card(post: dict, depth: int = 0) -> str:
    """Render a post card for the home/posts page."""
    prefix = '../' * depth
    url = prefix + post['url'].lstrip('/')
    if not url.endswith('/'):
        url += '/'
    tags_html = render_tags_html(post['tags'])

    thumb = ''
    if post.get('media'):
        thumb_src = prefix + f"posts/{post['year']}/{post['month']}/{post['slug']}/media/{post['media'][0]}"
        thumb = f'<img class="card-thumb" src="{thumb_src}" alt="" loading="lazy">'

    card_cls = 'card card-with-thumb' if thumb else 'card'

    return f'''<div class="{card_cls}">
  <div class="card-body">
    <div class="card-meta"><span class="card-date">{post['date']}</span><span class="card-reading-time">{post['reading_time']}</span></div>
    <div class="card-title"><a href="{url}">{escape(post['title'])}</a></div>
    <div class="card-preview">{escape(post['preview'])}</div>
    <div class="card-tags">{tags_html}</div>
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
        img_src = prefix + f"posts/{post['year']}/{post['month']}/{post['slug']}/media/{post['media'][0]}"
        image = f'<img class="card-image" src="{img_src}" alt="" loading="lazy">'

    return f'''<div class="card-featured">
  {image}
  <div class="card-meta"><span class="card-date">{post['date']}</span><span class="card-reading-time">{post['reading_time']}</span></div>
  <div class="card-title"><a href="{url}">{escape(post['title'])}</a></div>
  <div class="card-preview">{escape(post['preview'])}</div>
  <div class="card-tags">{tags_html}</div>
</div>'''


# ============================================================
# Page Generators
# ============================================================

def _hero_links_html() -> str:
    """Build social links for the hero section."""
    links = []
    if LINKEDIN:
        links.append(f'<a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>')
    if GITHUB:
        links.append(f'<a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>')
    if TWITTER:
        links.append(f'<a href="{TWITTER}" target="_blank" rel="noopener">X</a>')
    if not links:
        return ''
    sep = '<span class="sep">·</span>'
    return f'<div class="hero-links">{sep.join(links)}</div>'


def generate_home(posts: list[dict]) -> str:
    """Generate the home page HTML."""
    recent = posts[:6]
    cards = '\n'.join(render_card(p, depth=0) for p in recent)

    hero_subline = ''
    if SITE['hero_subline']:
        # hero_subline from site.yaml may already contain styled BRIDGE IN markup
        hero_subline = f'<p class="hero-subline">{SITE["hero_subline"]}</p>'

    about_teaser = ''
    if SITE['about_teaser']:
        about_teaser = f'''<div class="about-teaser">
    <div class="about-teaser-inner">
      <p>{escape(SITE['about_teaser'])}</p>
      <a href="about/" class="view-all">More about me &rarr;</a>
    </div>
  </div>'''

    return f'''{head_html("Home", depth=0, description=SITE_DESCRIPTION)}
<body>
<div class="noise-overlay" aria-hidden="true"></div>
{nav_html(depth=0)}

<div class="page-container">
  <section class="hero">
    <h1>{escape(SITE['hero_title'])}</h1>
    {hero_subline}
    {_hero_links_html()}
  </section>

  {about_teaser}

  <section class="section">
    <div class="section-title">Recent</div>
    <div class="cards-grid">
      {cards}
    </div>
    <a href="posts/" class="view-all">All posts &rarr;</a>
  </section>
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
    current: str | None = None
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
    """Parse the Experience section text into a list of entry dicts."""
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
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            dm = re.match(r'^\*\*(.+?)\*\*\s*[·•]\s*(.+)$', line)
            if dm:
                date_str = _fmt_date_range(dm.group(1))
                location = dm.group(2).strip()
            break

        bullets = [ln[2:].strip() for ln in lines if ln.startswith('- ')]

        entries.append({
            'company': company,
            'role': role,
            'date': date_str,
            'location': location,
            'bullets': bullets,
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
        nodes.append(
            f'    <div class="timeline-node">\n'
            f'      <div class="timeline-date">{escape(e["date"])}</div>\n'
            f'      <div class="timeline-company">{company_html}</div>\n'
            f'      <div class="timeline-role">{escape(e["role"])}</div>\n'
            f'      <div class="timeline-location">{escape(e["location"])}</div>'
            f'{bullets_html}\n'
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


def generate_about() -> str:
    """Generate the about page HTML from cv.md (if present)."""
    headshot = ''
    headshot_path = IMG_SRC / 'headshot.jpg'
    if headshot_path.exists():
        headshot = f'<img src="../img/headshot.jpg" alt="{escape(SITE_NAME)}" class="headshot">'

    # Social links
    social_parts = []
    if LINKEDIN:
        social_parts.append(f'<a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>')
    if GITHUB:
        social_parts.append(f'<a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>')
    if TWITTER:
        social_parts.append(f'<a href="{TWITTER}" target="_blank" rel="noopener">X</a>')
    sep = '<span class="muted" style="margin:0 0.75rem">&middot;</span>'
    social_html = sep.join(social_parts)

    speaking_text = SITE.get('speaking_text', '')
    speaking_p = f'<p>{escape(speaking_text)}</p>\n    ' if speaking_text else ''

    if not CV_FILE.exists():
        intro_html = (
            '<p class="muted">Add a <code>cv.md</code> file in the project root '
            'to populate this page.</p>'
        )
        timeline_html = skills_html = education_html = ''
    else:
        cv_text = CV_FILE.read_text(encoding='utf-8')
        _, cv_content = parse_frontmatter(cv_text)
        sections = _parse_cv_sections(cv_content)

        # Intro from Summary section
        summary_md = sections.get('Summary', '')
        md_renderer.reset()
        intro_html = style_bridge_in(autolink_urls(md_renderer.convert(summary_md))) if summary_md else ''

        # Experience timeline
        experience_text = sections.get('Experience', '')
        entries = _parse_experience_entries(experience_text)
        timeline_html = _render_timeline(entries) if entries else ''

        # Skills
        skills_text = sections.get('Top Skills', '')
        skills_html = _render_skills(skills_text)

        # Education — "### University\nDegree · Date"
        edu_raw = sections.get('Education', '').strip()
        edu_html_inner = ''
        if edu_raw:
            edu_lines = [l for l in edu_raw.split('\n') if l.strip()]
            uni = edu_lines[0].lstrip('#').strip()
            degree = ''
            if len(edu_lines) > 1:
                degree = edu_lines[1].split('·')[0].split('(')[0].strip()
            edu_html_inner = escape(uni) + (f' — {escape(degree)}' if degree else '')
        education_html = f'<div class="education">{edu_html_inner}</div>' if edu_html_inner else ''

    experience_block = ''
    if timeline_html:
        experience_block = f'''
  <div class="section-title">Experience</div>

  {timeline_html}
'''

    skills_block = ''
    if skills_html:
        skills_block = f'''
  <div class="section-title">Skills</div>

  {skills_html}
'''

    return f'''{head_html("About", depth=1)}
<body>
<div class="noise-overlay" aria-hidden="true"></div>
{nav_html(active='about', depth=1)}

<div class="page-container">
  <div class="about-header">
    <h1>About</h1>
  </div>

  <div class="about-intro-row">
    <div class="about-intro">
      {intro_html}
    </div>
    {headshot}
  </div>
{experience_block}{skills_block}
  <div class="speaking-cta">
    {speaking_p}{social_html}
  </div>

  {education_html}
</div>

{footer_html()}
</body>
</html>'''


def generate_posts_archive(posts: list[dict]) -> str:
    """Generate the posts archive page with JS-powered filtering."""
    total = len(posts)
    featured = posts[:6]
    featured_html = '\n'.join(render_featured_card(p, depth=1) for p in featured)

    # Server-render the first page of the archive for no-JS fallback
    archive_html = ''
    current_year = ''
    for p in posts[:20]:
        if p['year'] != current_year:
            current_year = p['year']
            archive_html += f'<div class="archive-year-header">{current_year}</div>\n'
        tags = render_tags_html(p['tags'], limit=3)
        url = f"{p['year']}/{p['month']}/{p['slug']}/"
        archive_html += f'''<div class="archive-row">
  <span class="archive-date">{p['date']}</span>
  <span class="archive-title"><a href="{url}">{escape(p['title'])}</a></span>
  <span class="archive-tags">{tags}</span>
</div>\n'''

    return f'''{head_html("Posts", depth=1)}
<body>
<div class="noise-overlay" aria-hidden="true"></div>
{nav_html(active='posts', depth=1)}

<div class="page-container">
  <div class="posts-header">
    <h1>Posts</h1>
    <span class="posts-count" id="posts-count">{total} posts</span>
    <p class="posts-description">Archived from LinkedIn. Originals only.</p>
  </div>

  <div class="filters">
    <input type="text" class="search-input" id="search-input" placeholder="Search posts...">
    <div class="year-filters" id="year-filters"></div>
    <div class="tag-filters" id="tag-filters"></div>
    <div class="filter-status" id="filter-status"></div>
  </div>

  <section id="recent-section">
    <div class="section-title">Recent</div>
    <div class="featured-grid">
      {featured_html}
    </div>
    <div style="height:calc(var(--spacing-unit)*2)"></div>
  </section>

  <section id="archive-section">
    <div class="section-title"></div>
    <div class="archive-list" id="archive-list">
      {archive_html}
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


def generate_post_page(post: dict, prev_post: dict | None, next_post: dict | None, depth: int = 4) -> str:
    """Generate an individual post page."""
    # Clean and render content
    cleaned = clean_content(post['content'])
    md_renderer.reset()
    body_html = md_renderer.convert(cleaned)
    body_html = autolink_urls(body_html)

    tags_html = render_tags_html(post['tags'])
    read_time = reading_time(cleaned)

    # OG image: use first media if available, else headshot
    post_og_image = ''
    if post.get('media'):
        post_og_image = f"posts/{post['year']}/{post['month']}/{post['slug']}/media/{post['media'][0]}"

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

    original_link = ''
    if post.get('post_url'):
        original_link = f'<a href="{post["post_url"]}" class="post-original-link" target="_blank" rel="noopener">View original on LinkedIn →</a>'

    return f'''{head_html(post['title'][:60], depth=depth,
        description=post['preview'][:160],
        og_type='article',
        og_image=post_og_image)}
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

  <div class="post-footer">
    <div class="post-actions">
      {original_link}
      <button class="copy-link-btn" aria-label="Copy link">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg>
        <span>Copy link</span>
      </button>
    </div>
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
            'type': p['post_type'],
            'media': bool(p['media']),
        })
    return json.dumps(entries, ensure_ascii=False, indent=None)


def copy_media(posts: list[dict]):
    """Copy media directories from source posts into dist."""
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
            dst = dst_media / fname
            if src.exists() and not dst.exists():
                shutil.copy2(src, dst)


def build():
    """Main build function."""
    print('Parsing posts...')
    posts = parse_all_posts()
    print(f'  Found {len(posts)} original/article posts')

    # Clean dist
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)

    # Copy static assets
    print('Copying assets...')
    shutil.copytree(CSS_SRC, DIST_DIR / 'css')
    shutil.copytree(JS_SRC, DIST_DIR / 'js')
    if IMG_SRC.exists():
        shutil.copytree(IMG_SRC, DIST_DIR / 'img')

    # Generate home page
    print('Generating home page...')
    (DIST_DIR / 'index.html').write_text(generate_home(posts), encoding='utf-8')

    # Generate about page
    print('Generating about page...')
    about_dir = DIST_DIR / 'about'
    about_dir.mkdir(parents=True)
    (about_dir / 'index.html').write_text(generate_about(), encoding='utf-8')

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

    print(f'\nBuild complete! Output in {DIST_DIR}')
    print(f'  {len(posts)} post pages')
    print(f'  4 main pages (home, about, posts archive, posts.json)')


if __name__ == '__main__':
    build()
