#!/usr/bin/env python3
"""Static site builder for João Gonçalves' personal website.

Reads markdown posts from posts/ and cv.md, generates static HTML
following the 'Brutalist Compiler' design system.

Usage: python web/build.py
"""

import json
import re
import shutil
from html import escape
from pathlib import Path

import markdown
import yaml

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

SITE_NAME = 'João Gonçalves'
SITE_URL = ''  # Set to deployed URL if needed
LINKEDIN = 'https://linkedin.com/in/joaofogoncalves'
GITHUB = 'https://github.com/joaofogoncalves'
TWITTER = 'https://x.com/joaofogoncalves'

md_renderer = markdown.Markdown(extensions=['fenced_code', 'tables', 'smarty'], output_format='html')


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

        posts.append({
            'date': date_str,
            'year': year,
            'month': month,
            'slug': slug,
            'title': title,
            'preview': preview,
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


def head_html(title: str, depth: int = 0, extra_head: str = '') -> str:
    """Generate <head> with proper relative paths."""
    prefix = '../' * depth
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)} — {SITE_NAME}</title>
  <meta name="description" content="Engineering leader &amp; AI coding practitioner. Founding Engineer at BRIDGE IN.">
  {GOOGLE_FONTS}
  <link rel="stylesheet" href="{prefix}css/style.css">
  {extra_head}
</head>'''


def nav_html(active: str = '', depth: int = 0) -> str:
    prefix = '../' * depth
    about_cls = ' active' if active == 'about' else ''
    posts_cls = ' active' if active == 'posts' else ''
    return f'''<nav class="nav">
  <div class="nav-inner">
    <a href="{prefix}index.html" class="nav-name">João Gonçalves</a>
    <div class="nav-links">
      <a href="{prefix}about/index.html" class="{about_cls}">About</a>
      <a href="{prefix}posts/index.html" class="{posts_cls}">Posts</a>
    </div>
  </div>
</nav>'''


def footer_html() -> str:
    return f'''<footer class="footer">
  <div class="footer-inner">
    <span>João Gonçalves · Lisbon</span>
    <div class="footer-links">
      <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
      <a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>
      <a href="{TWITTER}" target="_blank" rel="noopener">X</a>
    </div>
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
    url += 'index.html'
    tags_html = render_tags_html(post['tags'])

    thumb = ''
    if post.get('media'):
        thumb_src = prefix + f"posts/{post['year']}/{post['month']}/{post['slug']}/media/{post['media'][0]}"
        thumb = f'<img class="card-thumb" src="{thumb_src}" alt="" loading="lazy">'

    card_cls = 'card card-with-thumb' if thumb else 'card'

    return f'''<div class="{card_cls}">
  <div class="card-body">
    <div class="card-date">{post['date']}</div>
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
    url += 'index.html'
    tags_html = render_tags_html(post['tags'])

    image = ''
    if post.get('media'):
        img_src = prefix + f"posts/{post['year']}/{post['month']}/{post['slug']}/media/{post['media'][0]}"
        image = f'<img class="card-image" src="{img_src}" alt="" loading="lazy">'

    return f'''<div class="card-featured">
  {image}
  <div class="card-date">{post['date']}</div>
  <div class="card-title"><a href="{url}">{escape(post['title'])}</a></div>
  <div class="card-preview">{escape(post['preview'])}</div>
  <div class="card-tags">{tags_html}</div>
</div>'''


# ============================================================
# Page Generators
# ============================================================

def generate_home(posts: list[dict]) -> str:
    """Generate the home page HTML."""
    recent = posts[:6]
    cards = '\n'.join(render_card(p, depth=0) for p in recent)

    return f'''{head_html("Home", depth=0)}
<body>
{nav_html(depth=0)}

<div class="page-container">
  <section class="hero">
    <h1>João Gonçalves</h1>
    <p class="hero-subline">
      Founding Engineer at <a href="https://www.bridgein.pt/" target="_blank" rel="noopener" style="color:#cc0000;font-weight:500;text-decoration:none">BRIDGE IN</a>. Previously Director of Engineering at
      Altium/Valispace. Building things with AI, not just talking about it.
    </p>
    <div class="hero-links">
      <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
      <span class="sep">·</span>
      <a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>
      <span class="sep">·</span>
      <a href="{TWITTER}" target="_blank" rel="noopener">X</a>
    </div>
  </section>

  <div class="about-teaser">
    <div class="about-teaser-inner">
      <p>15+ years building software and teams. Steered an engineering org through a $20M acquisition.
         Now building from scratch again. Currently writing about what happens when AI changes how we build.</p>
      <a href="about/index.html" class="view-all">More about me →</a>
    </div>
  </div>

  <section class="section">
    <div class="section-title">Recent</div>
    <div class="cards-grid">
      {cards}
    </div>
    <a href="posts/index.html" class="view-all">All posts →</a>
  </section>
</div>

{footer_html()}
</body>
</html>'''


def generate_about() -> str:
    """Generate the about page HTML."""
    return f'''{head_html("About", depth=1)}
<body>
{nav_html(active='about', depth=1)}

<div class="page-container">
  <div class="about-header">
    <h1>About</h1>
  </div>

  <div class="about-intro-row">
    <div class="about-intro">
      I'm an engineering leader who still writes code daily. 15+ years of building teams and shipping
      products across SaaS, engineering software, and IoT — from a 4-person startup to a 25-person
      department through a $20M acquisition. Based in Lisbon, currently building <a href="https://www.bridgein.pt/" target="_blank" rel="noopener" style="color:#cc0000;text-decoration:none">BRIDGE IN</a> from scratch.
      I write about AI tooling, software craft, and what it actually takes to lead engineering teams.
    </div>
    <img src="../img/headshot.jpg" alt="João Gonçalves" class="headshot">
  </div>

  <div class="section-title">Experience</div>

  <div class="timeline">

    <div class="timeline-node">
      <div class="timeline-date">NOV 2025 — PRESENT</div>
      <div class="timeline-company"><a href="https://www.bridgein.pt/" target="_blank" rel="noopener" style="color:#cc0000;text-decoration:none">BRIDGE IN</a></div>
      <div class="timeline-role">Founding Engineer</div>
      <div class="timeline-location">Lisbon, Portugal</div>
    </div>

    <div class="timeline-node">
      <div class="timeline-date">JAN 2024 — NOV 2025</div>
      <div class="timeline-company">Altium</div>
      <div class="timeline-role">Director of Software Engineering</div>
      <div class="timeline-location">Lisbon, Portugal</div>
      <ul class="timeline-highlights">
        <li>Integrated Valispace as an Altium 365 app, ensuring continuity and merging capabilities in the aftermath of a high-profile $20M acquisition</li>
        <li>Doubled the engineering department's size and coached new team leads to own all operations — project management, system architecture, and software development</li>
        <li>Interfaced cross-departmentally to identify and implement technology solutions that directly impact business growth, notably equipping DevOps with improved Kubernetes infrastructure to accommodate a surge in demand</li>
        <li>Cultivated a healthy, productive, and meritocratic department culture that retained 90% of staff post-merger, despite the temptation of a generous shareholder payout</li>
      </ul>
    </div>

    <div class="timeline-node">
      <div class="timeline-date">AUG 2022 — FEB 2024</div>
      <div class="timeline-company">Valispace</div>
      <div class="timeline-role">Head of Technology &amp; Interim CTO</div>
      <div class="timeline-location">Lisbon, Portugal</div>
      <ul class="timeline-highlights">
        <li>Positioned Valispace, a fast-growing startup, as an attractive asset for a $20M acquisition by Altium, and directed all due diligence to ensure a frictionless transaction and transition to new ownership</li>
        <li>Partnered with the CEO &amp; CPO to orient the company's strategic direction and pioneered AI's early adoption</li>
        <li>Orchestrated an engineering department of 25+ staff across three teams to implement cloud computing and emerging technologies, operating a complex global cloud environment with only three engineers</li>
        <li>Implemented ISO-27001 to access highly regulated opportunities in aerospace — Airbus, Clearspace, and iSpace</li>
      </ul>
    </div>

    <div class="timeline-node">
      <div class="timeline-date">OCT 2020 — AUG 2022</div>
      <div class="timeline-company">Valispace</div>
      <div class="timeline-role">Head of DevOps</div>
      <div class="timeline-location">Lisbon, Portugal</div>
      <ul class="timeline-highlights">
        <li>Oversaw an operations team of four responsible for 100+ cloud-based &amp; on-premise deployments with maintenance and support</li>
        <li>Owned a robust CI/CD pipeline that accelerated time-to-market for software releases by 89%</li>
        <li>Established and maintained strong relationships with external vendors and stakeholders to ensure successful integration of third-party tools and services</li>
      </ul>
    </div>

    <div class="timeline-node">
      <div class="timeline-date">AUG 2018 — OCT 2020</div>
      <div class="timeline-company">Valispace</div>
      <div class="timeline-role">Senior Developer</div>
      <div class="timeline-location">Lisbon, Portugal</div>
      <ul class="timeline-highlights">
        <li>Performed in-depth code reviews, amplified team productivity, reduced software defects, and streamlined development processes by introducing Agile and automated testing frameworks</li>
        <li>Developed, maintained, and improved both the backend REST API and the frontend application</li>
      </ul>
    </div>

    <div class="timeline-node">
      <div class="timeline-date">JAN 2016 — AUG 2018</div>
      <div class="timeline-company">Quidgest</div>
      <div class="timeline-role">R&amp;D Software Engineer</div>
      <div class="timeline-location">Lisbon, Portugal</div>
      <ul class="timeline-highlights">
        <li>Built and continuously improved a low-code tool ahead of its time — enabling non-technical users to assemble complex software solutions like ERPs, HR portals, and document management systems</li>
        <li>Clients included Portugal's government &amp; armed forces</li>
      </ul>
    </div>

    <div class="timeline-node">
      <div class="timeline-date">JAN 2015 — OCT 2017</div>
      <div class="timeline-company">Sources.pt</div>
      <div class="timeline-role">Co-Founder &amp; Lead Developer</div>
      <div class="timeline-location">Lisbon, Portugal</div>
      <ul class="timeline-highlights">
        <li>Conceived an IoT modular platform, built its working prototype, and marketed its unique merits as a cost-saving sensor solution accessible to the consumer market</li>
        <li>Pitched the project to a bigger tech company to secure stable financing and merge capabilities</li>
      </ul>
    </div>

    <div class="timeline-node">
      <div class="timeline-date">APR 2013 — JAN 2015</div>
      <div class="timeline-company">Inova Software</div>
      <div class="timeline-role">Senior Mobile Developer</div>
      <div class="timeline-location">Lisbon, Portugal</div>
      <ul class="timeline-highlights">
        <li>Project management of the app "Partnering Place Mobile"</li>
        <li>Architecture design of UI render engine based on descriptive models, built with Phonegap and JavaScript frameworks (Underscore.js, Backbone.js, Angular.js)</li>
      </ul>
    </div>

    <div class="timeline-node">
      <div class="timeline-date">MAY 2011 — APR 2013</div>
      <div class="timeline-company">Quidgest</div>
      <div class="timeline-role">R&amp;D Software Engineer</div>
      <div class="timeline-location">Lisbon, Portugal</div>
      <ul class="timeline-highlights">
        <li>Built and improved a low-code platform enabling non-technical users to assemble complex software solutions; clients included Portugal's government &amp; armed forces</li>
      </ul>
    </div>

    <div class="timeline-node">
      <div class="timeline-date">JAN 2011 — MAY 2011</div>
      <div class="timeline-company">EmergeIT</div>
      <div class="timeline-role">Developer</div>
      <div class="timeline-location">Lisbon, Portugal</div>
      <ul class="timeline-highlights">
        <li>Development of remote management applications for mobile devices and web-based administration tools</li>
      </ul>
    </div>

    <div class="timeline-node">
      <div class="timeline-date">SEP 2009 — DEC 2010</div>
      <div class="timeline-company">NAD / Design Solutions</div>
      <div class="timeline-role">Developer</div>
      <div class="timeline-location">Lisbon, Portugal</div>
      <ul class="timeline-highlights">
        <li>Websites, intranets, database systems, and multimedia applications using HTML, CSS, JavaScript, Python, Django, SQL, and ActionScript</li>
      </ul>
    </div>

  </div>

  <div class="section-title">Skills &amp; Domains</div>

  <div class="skills-section">
    <div class="skill-row">
      <span class="skill-label">Engineering Leadership</span>
      <span class="skill-desc">Scaling teams from 4 to 25+, coaching leads, M&amp;A integration</span>
    </div>
    <div class="skill-row">
      <span class="skill-label">AI &amp; Tooling</span>
      <span class="skill-desc">Claude Code, AI-assisted development, GenAI strategy</span>
    </div>
    <div class="skill-row">
      <span class="skill-label">Infrastructure</span>
      <span class="skill-desc">Kubernetes, cloud architecture, CI/CD, ISO-27001</span>
    </div>
    <div class="skill-row">
      <span class="skill-label">Languages</span>
      <span class="skill-desc">Python, JavaScript/TypeScript, full-stack SaaS</span>
    </div>
  </div>

  <div class="speaking-cta">
    <p>Available for speaking, podcasts, and conversations about engineering leadership and AI in practice.</p>
    <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
    <span class="muted" style="margin:0 0.75rem">·</span>
    <a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>
    <span class="muted" style="margin:0 0.75rem">·</span>
    <a href="{TWITTER}" target="_blank" rel="noopener">X</a>
  </div>

  <div class="education">
    Universidade de Évora — Computer Science
  </div>
</div>

{footer_html()}
</body>
</html>'''


def generate_posts_archive(posts: list[dict]) -> str:
    """Generate the posts archive page with JS-powered filtering."""
    total = len(posts)
    featured = posts[:2]
    featured_html = '\n'.join(render_featured_card(p, depth=1) for p in featured)

    # Server-render the first page of the archive for no-JS fallback
    archive_html = ''
    current_year = ''
    for p in posts[:20]:
        if p['year'] != current_year:
            current_year = p['year']
            archive_html += f'<div class="archive-year-header">{current_year}</div>\n'
        tags = render_tags_html(p['tags'], limit=3)
        url = f"{p['year']}/{p['month']}/{p['slug']}/index.html"
        archive_html += f'''<div class="archive-row">
  <span class="archive-date">{p['date']}</span>
  <span class="archive-title"><a href="{url}">{escape(p['title'])}</a></span>
  <span class="archive-tags">{tags}</span>
</div>\n'''

    return f'''{head_html("Posts", depth=1, extra_head='<script src="../js/posts.js" defer></script>')}
<body>
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
    <div class="section-title">Archive</div>
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

    # Fix media paths — they reference media/image-1.jpg, which is correct
    # since media/ is copied into the same directory

    # Build prev/next nav
    prefix = '../../../../'
    prev_link = ''
    next_link = ''
    if prev_post:
        prev_url = prefix + prev_post['url'].lstrip('/') + 'index.html'
        prev_link = f'<a href="{prev_url}">← Previous</a>'
    if next_post:
        next_url = prefix + next_post['url'].lstrip('/') + 'index.html'
        next_link = f'<a href="{next_url}">Next →</a>'

    original_link = ''
    if post.get('post_url'):
        original_link = f'<a href="{post["post_url"]}" class="post-original-link" target="_blank" rel="noopener">View original on LinkedIn →</a>'

    return f'''{head_html(post['title'][:60], depth=depth)}
<body>
{nav_html(active='posts', depth=depth)}

<div class="page-container">
  <div class="post-header">
    <div class="post-date">{post['date']}</div>
    <div class="post-tags">{tags_html}</div>
  </div>

  <div class="post-content">
    {body_html}
  </div>

  <div class="post-footer">
    {original_link}
    <div class="post-nav">
      {prev_link}
      <span></span>
      {next_link}
    </div>
  </div>
</div>

{footer_html()}
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
            'tags': p['tags'],
            'url': p['url'] + 'index.html',
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
