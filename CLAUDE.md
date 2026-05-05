# LinkedIn Post Archiver - Claude Code Instructions

## Project Overview

This is a Python application that archives LinkedIn posts locally as clean markdown files with media downloads, and publishes them as a static website. It uses a **Playwright browser crawler** (primary method) or OAuth 2.0 API (legacy fallback) to fetch posts and preserve them in an organized folder structure. A static site generator converts the archive into a deployable website.

**Purpose:** Create a permanent, offline archive of the user's LinkedIn content that they control - focusing on what they wrote, not engagement metrics. Optionally publish as a personal website positioned for thought leadership.

**Status:** Production-ready. Archiving, site generation, and deployment all working.

---

## Technology Stack

- **Python 3.14+** (managed by [uv](https://docs.astral.sh/uv/) — see `pyproject.toml`)
- **Playwright** - Browser automation for crawling LinkedIn (primary method)
- **LinkedIn API v2** - OAuth 2.0 (legacy fallback, limited by API restrictions)
- **Static Site** - Vanilla HTML/CSS/JS, no frameworks
- **Core Libraries:**
  - `playwright` / `playwright-stealth` - Browser-based post crawling
  - `requests` - HTTP client for API calls and media downloads
  - `requests-oauthlib` - OAuth 2.0 implementation (legacy)
  - `PyYAML` - Configuration management
  - `Pillow` - Image validation and processing
  - `python-slugify` - URL-safe slug generation
  - `python-dateutil` - Date parsing
  - `python-dotenv` - Environment variable loading
  - `reportlab` - Native PDF generation (CV PDF)
  - `tqdm` - Progress bars
  - `coloredlogs` - Enhanced console output

---

## Directory Structure

```
linkedin-post-archiver/  # Project root
├── scraper/                          # Main application package
│   ├── __init__.py                   # Package initialization
│   ├── main.py                       # CLI entry point & orchestration
│   ├── browser_crawler.py            # Playwright browser crawler (primary)
│   ├── auth.py                       # OAuth 2.0 authentication flow (legacy)
│   ├── linkedin_client.py            # LinkedIn API wrapper (legacy)
│   ├── post_fetcher.py               # Parse API responses into Post objects
│   ├── export_parser.py              # Import from LinkedIn data export
│   ├── media_downloader.py           # Download and validate media files
│   ├── markdown_generator.py         # Generate markdown output
│   ├── models.py                     # Data models (LinkedInPost, Media)
│   └── utils.py                      # Helper functions + checkpoint management
│
├── web/                              # Static site generator
│   ├── build.py                      # Site generator (posts → HTML)
│   ├── resolve_links.py              # Resolve lnkd.in shortened URLs
│   ├── deploy.sh                     # Deploy to Opalstack via rsync
│   ├── css/
│   │   ├── style.css                 # Brutalist dark theme styles
│   │   └── critical.css              # Inlined above-the-fold CSS
│   ├── js/
│   │   ├── posts.js                  # Client-side search/filter (posts page)
│   │   └── home.js                   # Homepage: particle canvas, spotlight, tabs
│   ├── img/
│   │   ├── headshot.jpg              # Author photo for About page
│   │   └── logo.webp                 # Site logo for nav bar
│   └── dist/                         # Generated site output (git-ignored)
│
├── config/
│   ├── config.yaml                   # Scraper configuration (tracked)
│   ├── site.yaml                     # Site personalization (git-ignored)
│   └── site.yaml.example             # Site config template (tracked)
│
├── examples/
│   └── sample-post/post.md           # Example archived post format
│
├── posts/                            # Short-form posts (tracked; mix of authored via /post and historical scrape)
│   └── YYYY/MM/post-slug/
│       ├── post.md                   # Markdown file
│       └── media/                    # Downloaded images/videos
│
├── articles/                         # Long-form articles (tracked in git)
│   └── YYYY/MM/YYYY-MM-DD-slug/
│       ├── article.md                # Article markdown with frontmatter
│       ├── image-prompts.md          # AI image generation prompts (optional)
│       └── media/                    # Article images (hero, diagrams)
│
├── cv/                               # CV PDF generator (self-contained)
│   ├── generate.py                   # reportlab-based PDF builder
│   └── fonts/                        # Bundled fonts (Inter, JetBrains Mono)
│
├── .claude/
│   ├── settings.json                 # Plugin configuration
│   └── commands/                     # Claude Code custom skills
│       ├── article.md                # /article - long-form article writer
│       ├── cover-letter.md           # /cover-letter - tailored cover letter for a JD
│       ├── interview-prep.md         # /interview-prep - prep doc for a specific interview
│       ├── outreach.md               # /outreach - recruiter / HM / founder DMs + emails
│       ├── pdf.md                    # /pdf - CV PDF generator (generic + JD-tailored)
│       ├── pitch.md                  # /pitch - elevator/talk/bio/LinkedIn variants
│       ├── post.md                   # /post - LinkedIn post writer
│       ├── profile.md                # /profile - voice profile generator
│       ├── publish.md                # /publish - promote draft to published
│       ├── sync.md                   # /sync - scrape + curate recent posts
│       └── taste.md                  # /taste - visual taste profile generator
│
├── applications/                     # Job-search artifacts (git-ignored; see "Job-Search Toolkit")
│   └── {company-slug}/
│       ├── cover-letter.md           # /cover-letter output
│       ├── outreach.md               # /outreach output (3 variants)
│       ├── interview-prep.md         # /interview-prep output
│       ├── notes.md                  # User-maintained: JD copy, contacts, dates
│       └── cv.pdf                    # /pdf tailored mode output (was cv-{slug}.pdf at root)
│
├── cache/                            # Browser profile + token cache (git-ignored)
├── logs/                             # Application logs (git-ignored)
├── .venv/                            # uv-managed virtual environment (git-ignored)
│
├── pipeline.sh                       # Full pipeline: scrape → resolve → build → deploy
├── pyproject.toml                    # Python project metadata + dependencies (uv)
├── uv.lock                           # Resolved dependency lockfile (uv)
├── .python-version                   # Pins Python 3.14 for uv
├── .env                              # Credentials (git-ignored, created by user)
├── .env.example                      # Credentials template
├── .gitignore                        # Git exclusions
│
├── cv.md                             # Professional CV + About-page narrative sections (tracked)
├── cv_joaofogoncalves.pdf                            # Generated CV PDF (tracked, persistent asset)
├── now.md                            # /now page content (tracked)
├── now.md.example                    # /now template (tracked)
├── article_style.md                  # Long-form article style supplement (tracked)
├── writing_style.md                  # LinkedIn writing style guide (tracked)
├── pitch_style.md                    # Self-positioning style guide (tracked) — used by /cover-letter, /outreach, /interview-prep, /pitch and the About page
├── profile.md                        # Voice profile for AI writing (tracked)
├── taste.md                          # Visual taste profile (tracked)
├── pitches.md                        # /pitch output: living doc with all pitch variants (tracked)
│
├── README.md                         # Full documentation
├── CONTRIBUTING.md                   # Contribution guidelines
├── RATE_LIMITS.md                    # LinkedIn API rate limit docs
├── LICENSE                           # MIT License
├── verify_setup.py                   # Setup verification script
└── CLAUDE.md                         # This file
```

---

## Key Design Decisions

### 1. Browser Crawler (Primary Method)
- Playwright-based browser automation replaces LinkedIn API as the primary crawling method
- Uses `playwright-stealth` to avoid LinkedIn bot detection
- Manual login with headed browser; session saved to `cache/browser_profile`
- Intelligent scrolling with random delays (5-12s, configurable)
- Post extraction via DOM selectors
- Automatic checkpointing to resume interrupted crawls
- Filters out self-reposts to avoid duplicates
- `--profile-url` falls back to `LINKEDIN_PROFILE_URL` from `.env` if not passed
- **Why:** LinkedIn API is too restrictive (limited scopes, rate limits, restricted historical access)

### 2. OAuth 2.0 Flow (Legacy Fallback)
- Uses local HTTP server on port 8080 to catch OAuth callback
- Token cached in `cache/token.json` for reuse
- Browser automatically opens for user authorization
- Supports re-authentication with `--reauth` flag

### 3. Rate Limiting (API path)
- 1.5 second delay between API requests (configurable)
- Exponential backoff on 429 rate limit errors: 1s → 2s → 4s → 8s
- Max 3 retries per request
- All rate limiting handled in `linkedin_client.py`

### 4. Post Organization (authored-first model)
- Structure: `posts/YYYY/MM/YYYY-MM-DD-slug/`
- Slug format: `YYYY-MM-DD-first-words-of-post` (max 60 chars)
- Duplicate slugs handled with numeric suffixes (-2, -3, etc.)
- Media stored in `media/` subdirectory per post
- **Site is canonical for short-form posts.** Authored via `/post`, which saves `post.md` (canonical body) plus `linkedin.md` and `x-thread.md` (paste-ready variants for manual posting). `posts/` is tracked in git — these are authored artifacts the user owns, not just a scraped mirror.
- The historical `posts/` archive (scraped from LinkedIn before this model existed) lives alongside newly-authored posts; both are rendered the same way by the site builder.
- **Authored-post frontmatter** differs slightly from scraped: `authored: true`, empty `post_url:` and `x_url:` initially (filled in after posting manually), `source_urls:`, `angle:`, `template:`.

### 5. Idempotent Operation with Merge Mode
- Safe to re-run; the scraper never overwrites existing post bodies.
- On re-crawl, scraped posts are matched to existing local posts by (a) exact `post_url` match or (b) content fingerprint within ±14 days. Matched posts get **engagement-only updates**: `reactions:` and `comments:` are refreshed in-place; an empty `post_url:` on an authored post is filled in with the LinkedIn permalink.
- Posts with no match are added as new. This catches anything posted manually on LinkedIn outside the `/post` workflow.
- Media downloads still skip existing files.

### 6. Error Handling
- All errors logged to `logs/scraper.log`
- Failed posts logged but don't stop the entire process
- Media download failures noted in logs but don't fail post creation

### 7. Static Site Generator
- `web/build.py` reads markdown posts and generates a complete static site
- Site identity (name, bio, social links) loaded from `config/site.yaml`
- About page rendered from `cv.md` (markdown → HTML), with placeholder if missing
- Brutalist dark theme ("senior engineer's personal site")
- **Layout**: `--max-page: 1280px` (page container), `--max-content: 720px` (readable text width for posts/articles, centered)
- Pages: Home, About, Posts (searchable), Articles, /topics index, /topics/{slug}, /now
- Only shows `post_type: original` or `article` (filters out reposts)
- Client-side search and tag filtering via `web/js/posts.js`
- Homepage interactivity via `web/js/home.js` (particle canvas, spotlight rotation, tabs)
- Critical CSS (`web/css/critical.css`) inlined in `<head>` for fast above-the-fold rendering
- Output to `web/dist/` (git-ignored)
- Also generates: `feed.xml` (RSS 2.0), `sitemap.xml`, `robots.txt`
- JSON-LD structured data on every post page (Article schema) and About page (Person schema)
- RSS autodiscovery `<link>` in every page `<head>`

### 8. Homepage Design
- **Hero section**: Compact hero (not full-viewport) with animated particle network canvas background (`web/js/home.js`). Teal-colored nodes drift, form connections, and react to mouse movement. Name with glitch animation + blinking cursor, thesis statement with teal left border, social links.
- **Transparent nav**: On the homepage, the nav bar starts fully transparent so particles flow behind it, then gains a frosted-glass background on scroll (`.nav--transparent` class).
- **Featured Spotlight ("Start Here")**: Auto-rotating display of the newest articles — one at a time with text on left and hero image on right. Crossfades every 12s with dot indicators. Pauses on hover for accessibility. Article-only (not posts) — the site positions long-form as primary.
- **Recent notes**: Compact text-only strip of the 6 most recent short-form posts (date + title, one row each). Sits below the spotlight as secondary activity. Links to `/posts/` for the full archive.
- **Topics section**: Topic cards with post counts (if topics configured in `site.yaml`)
- **Newsletter CTA**: Centered section with teal glow button (if `newsletter_url` configured)

### 9. Thought Leadership Features
- **Featured posts ("Start Here")**: configured slugs or auto-computed from engagement
  - Auto-computation: `reactions + comments×3` score, top 3 from last 90 days
  - Auto-updates `featured_posts` in `site.yaml` after each scrape
- **Topics**: tag-to-theme mapping generates `/topics/` index and `/topics/{slug}/` pages
  - Topic badges shown on individual post pages
  - Topics nav link appears automatically when `topics:` is configured in `site.yaml`
- **Now page**: `/now/` generated from `now.md` (git-ignored personal content)
  - Nav link appears automatically when `now.md` exists
- **Newsletter CTA**: optional subscribe prompt on home + post pages (`newsletter_url` in site.yaml)
- **Engagement capture**: browser crawler extracts reaction/comment counts into post frontmatter

### 9. Deployment (Opalstack)
- `web/deploy.sh` builds the site and deploys via rsync over SSH
- Credentials loaded from `.env` (OPAL_* variables)
- Deletes stale files on remote

### 10. Full Pipeline Automation
- `pipeline.sh` runs the complete workflow: scrape → resolve links → build → deploy
- Requires `LINKEDIN_PROFILE_URL` in `.env`
- Flags: `--skip-scrape` (rebuild/deploy only), `--dry-run` (no deploy)
- After scrape, `featured_posts` in `site.yaml` is auto-updated with top performers

### 11. CV PDF Generator
- `cv/generate.py` — self-contained reportlab script that generates `cv_joaofogoncalves.pdf` from `cv.md`
- Brutalist dark theme matching the website: `#0e131e` background, `#44d8f1` teal accents, `#dee2f2` text
- Fonts bundled in `cv/fonts/` (Inter, JetBrains Mono); Helvetica-Bold as fallback for Space Grotesk (OTF not supported by reportlab)
- A4 layout, 18mm margins, targets 2 pages max
- Recent roles get full bullet detail; older roles ("Earlier Career") are compact single-line descriptions
- The `/pdf` skill supports tailored mode: pass a job description URL/text and the CV is reframed for that role
- `cv_joaofogoncalves.pdf` is tracked in git as a persistent asset; `build.py` copies it to `dist/about/` during build
- **Why:** Native PDF generation avoids Playwright/browser dependency and is faster and more portable

### 12. Writing Style Guide
- `writing_style.md` — authoritative style guide for LinkedIn post writing
- Defines structure, tone, language rules, length targets, and anti-patterns
- The `/post` skill uses it as primary reference (takes precedence over `profile.md` where they conflict)
- `profile.md` supplements with vocabulary, topic expertise, and deeper voice patterns

### 13. Articles Section
- `articles/` directory stores original long-form content (tracked in git, same as `posts/` now)
- Structure: `articles/YYYY/MM/YYYY-MM-DD-slug/article.md` with `media/` subdirectory
- Article frontmatter: `title`, `subtitle`, `date`, `tags`, `medium_url`, `hero_image`, `reading_time`, `draft` (default true on creation)
- Draft mode: **new articles always start with `draft: true`** (set by `/article`). Drafts publish at an obfuscated `/articles/drafts/<token>/` URL (stable sha256 of slug, 16 chars), excluded from home, archive, topics, RSS, and sitemap; pages carry `noindex, nofollow` and the drafts tree is disallowed in `robots.txt`.
- To promote a draft: run `/publish <slug>` — removes `draft: true`, updates `date:` to today, and renames the directory to match the new date so the path stays `articles/YYYY/MM/YYYY-MM-DD-slug/`.
- `article_style.md` — supplements `writing_style.md` with long-form patterns (section headers, citations, pacing)
- Same core voice as LinkedIn posts, scaled up for longer format
- Build workflow: write article locally → build site → deploy → optionally cross-post to Substack / Medium → update `substack_url` / `medium_url`
- The `/article` skill handles drafting; the `/publish` skill promotes a draft AND produces the `substack-paste.md` artifact ready to paste into Substack (with canonical URL pointing back to the site). Generating Substack paste only at publish time avoids wasted token churn during the draft loop. `/post` handles the LinkedIn + X promotion posts (decoupled).
- Articles appear on: home page (Start Here spotlight + Essays grid — articles are the primary content on the home page), `/articles/` archive, `/articles/YYYY/MM/slug/` pages, RSS feed, sitemap
- **Distribution stack**: site is canonical (SEO + long-term home) → Substack for email + discovery (via `substack-paste.md` for articles, `substack-note.md` for short-form Notes) → LinkedIn + X for short-form cold reach (via `/post`). Each surface gets a surface-native artifact; no platform sees a generic cross-post.
- **Why separate from posts:** articles are long-form authored content with different frontmatter (title, subtitle, hero_image, reading_time). Short-form posts now also live in the site as canonical, but have their own structure optimized for short-form rhythm.

### 14. Image Specs
All images display on the site at **720px content width** (2x retina = 1440px source). Thumbnails are cropped via `object-fit: cover` at various aspect ratios. **Keep subjects centered with breathing room** for safe cropping.

| Context | Display Size | Crop |
|---------|-------------|------|
| Homepage card thumb (tab grid) | 140 × 100px | cover |
| Homepage spotlight | full-width, max-h 220px | cover, 16:10 |
| Posts page list card | 300 × 175px | cover |
| Article archive card | full-width × 220px | cover |
| Article/post hero (inline) | 720px × auto | no crop |

**Standard source sizes** (used by `/post` and `/article` skills):
- **Hero/illustration**: 1440×900px (16:10) · PNG or JPG — works everywhere
- **Square diagram**: 1200×1200px (1:1) · PNG — sharp text
- **Screenshots**: native resolution, crop to content · PNG

**Hero images are NOT bound by the site color scheme.** Heroes are mood pieces — use whatever palette, medium, and style best serves the article's concept (painterly editorial illustrations, warm tones, cinematic photography-like scenes, etc.). Think NYT Magazine / Wired long-read opener. Only inline diagrams, charts, and schematics follow `taste.md` and the dark navy + teal palette.

### 15. Job-Search Toolkit (soft-hunt-shaped)

The user is in a soft-hunt posture (open to conversations, not actively job-hunting). The toolkit is shaped around four operating principles borrowed from James Gardner's "817 Applications" site:

- **Lead with proof, not promises** — every artifact opens with a specific accomplishment, never an introduction
- **Target conversations, not applications** — outreach is substantive and low-volume, not blast
- **Build in public** — the site itself is the proof; artifacts link back to it
- **Quiet ask, not marketing CTA** — closes invite a conversation, never sell

**The toolkit:**

| Surface | Skill | Output | Notes |
|---|---|---|---|
| Personal narrative (always-on) | n/a (manual) | About page (rendered from `cv.md` Hero/Thesis/Building/Open To sections) | Replaces conventional bio + timeline. Numbered sections, metric callouts, soft pitch at bottom. |
| Generic CV (always-on) | `/pdf` (no args) | `cv_joaofogoncalves.pdf` at root | Reads `cv.md` as source of truth; tracked in git. |
| Self-pitch variants (always-on) | `/pitch` (optional variant arg) | `pitches.md` at root (tracked) | 9 variants in one file: 30s/60s/2min elevator, LinkedIn headline + About, talk abstract, 3 speaker bios. |
| Tailored CV (per JD) | `/pdf {JD URL}` | `applications/{slug}/cv.pdf` | Reframes existing proofs for the specific role; never fabricates. |
| Cover letter (per JD) | `/cover-letter {JD URL}` | `applications/{slug}/cover-letter.md` | 250–350 words, three paragraphs, proof-led opener. |
| Recruiter / HM / founder outreach | `/outreach {recipient}` | `applications/{slug}/outreach.md` | LinkedIn DM (~80w) + email cold (~150w) + follow-up (~50w). Requires a specific hook about the recipient. |
| Interview prep | `/interview-prep {JD URL} [company URL]` | `applications/{slug}/interview-prep.md` | TL;DR + tailored "tell me about yourself" + behavioral STARs + technical talking points + questions to ask back + company research |

**The canonical content flow:**

`cv.md` is the source of truth for everything. Its sections split into two audiences:

- **CV-only sections** (`Summary`, `Experience`, `Education`, `Languages`, `Top Skills`, `Certifications`) — render in `cv_joaofogoncalves.pdf` and `applications/{slug}/cv.pdf`.
- **About-only sections** (`Hero`, `Thesis`, `Building`, `Open To`) — render only on the website's About page. The `/pdf` skill and `cv/generate.py` explicitly skip them.
- **Both** — the Experience section is read by both. Rich `[badges] item · item · item` lines under each role render as pills on the About page; they're skipped in the PDF.

**Experience grouping in PDF**: roles with 2+ bullets → detailed `EXPERIENCE` section. Roles with 1 bullet → compact `EARLIER CAREER` section. The user controls grouping by editing bullet counts in `cv.md`.

**Style guides:**

- `pitch_style.md` — primary authority for any artifact where João is the subject (About page, cover letters, outreach, interview prep, pitches). Codifies the four principles above plus length targets per surface and an anti-pattern checklist.
- `writing_style.md` — for LinkedIn posts (still primary for `/post`)
- `article_style.md` — for long-form essays (still primary for `/article`)

**Why `applications/` is git-ignored**: cover letters and outreach often contain confidential JD text and recipient contact details; tailored CVs reference specific company contexts. Default-ignored to keep them local. The user can override per-folder if they want a tracked record.

---

## Code Conventions

### Imports
- Standard library imports first
- Third-party imports second
- Local imports last
- Alphabetical within each group

### Logging
- Use module-level logger: `logger = logging.getLogger('linkedin_scraper.module_name')`
- Log levels:
  - DEBUG: Detailed debugging info
  - INFO: Progress updates and success messages
  - WARNING: Non-critical issues (e.g., media download failed)
  - ERROR: Critical failures that prevent operation

### Type Hints
- All function parameters and return types annotated
- Use `Optional[Type]` for nullable values
- Use `List[Type]`, `Dict[Key, Value]` for collections

### Docstrings
- Google-style docstrings for all public functions
- Include Args, Returns, and Raises sections where applicable

### Error Messages
- User-facing errors: Clear, actionable messages
- Debug errors: Include technical details and stack traces
- Always log exceptions with `logger.error(f"...", exc_info=True)`

---

## Working with the Code

### Environment (uv)

The project uses [`uv`](https://docs.astral.sh/uv/) to manage Python and dependencies. Configuration is in `pyproject.toml`; the resolved env lives in `.venv/` (auto-created on first `uv sync` or `uv run`).

**First-time setup:**
```bash
uv sync                                  # install Python 3.14 env + deps
uv run playwright install chromium       # install Playwright browser
```

**Run any script via `uv run` — no manual venv activation needed:**
```bash
uv run python -m scraper.main --crawl
uv run python web/build.py
```

If you prefer to activate the venv directly: `source .venv/bin/activate`.

### Running the Application

**Browser login (first time):**
```bash
uv run python -m scraper.main --browser-login
```

**Archive all posts (browser crawler):**
```bash
uv run python -m scraper.main --crawl
# Uses LINKEDIN_PROFILE_URL from .env automatically
# Or pass explicitly: --profile-url https://www.linkedin.com/in/username
```

**Test with limited posts:**
```bash
uv run python -m scraper.main --crawl --limit 10
```

**Legacy API authentication:**
```bash
uv run python -m scraper.main --auth
```

**Force re-authentication (API):**
```bash
uv run python -m scraper.main --reauth --fetch
```

### Static Site Workflow

**Build the website:**
```bash
uv run python web/build.py
```

**Resolve lnkd.in shortened URLs in posts:**
```bash
uv run python web/resolve_links.py          # apply changes
uv run python web/resolve_links.py --dry-run  # preview only
```

**Deploy to Opalstack:**
```bash
bash web/deploy.sh
```

### Full Pipeline (automated)

```bash
# One command — scrape + resolve + build + deploy
bash pipeline.sh

# Rebuild and deploy without scraping (e.g. after editing now.md or site.yaml)
bash pipeline.sh --skip-scrape

# Scrape and resolve but don't deploy (safe for testing)
bash pipeline.sh --dry-run
```

### Manual Pipeline (step by step)

```bash
# 1. Crawl new posts (also auto-updates featured_posts in site.yaml)
uv run python -m scraper.main --crawl --profile-url https://www.linkedin.com/in/yourprofile

# 2. Resolve shortened URLs
uv run python web/resolve_links.py

# 3. Build and deploy website
bash web/deploy.sh
```

### Development Workflow

1. **Make code changes** in appropriate module
2. **Test changes** with `--limit 5` for quick validation
3. **Check logs** in `logs/scraper.log` for debugging
4. **Verify output** in `posts/` directory
5. **Update documentation** if adding features

### Adding New Features

**To add a new post type:**
1. Update `models.py` - Add to `post_type` enum
2. Update `post_fetcher.py` - Add parsing logic in `_determine_post_type()`
3. Update `markdown_generator.py` - Add formatting logic if needed

**To add new media type:**
1. Update `models.py` - Add to Media `type` validation
2. Update `media_downloader.py` - Add download method
3. Update `markdown_generator.py` - Add markdown formatting

**To add new CLI option:**
1. Update `main.py` - Add argument to parser
2. Update `LinkedInArchiver.run()` - Handle new option
3. Update `README.md` - Document new option

---

## Configuration Management

### config/config.yaml

**LinkedIn API Settings (legacy):**
```yaml
linkedin:
  api_version: v2
  rate_limit_delay: 1.5    # Increase if hitting rate limits
  max_retries: 3           # Number of retry attempts
  timeout: 30              # HTTP request timeout
```

**Browser Crawler Settings:**
```yaml
browser:
  profile_dir: cache/browser_profile
  scroll_delay_min: 5.0    # Min seconds between scrolls
  scroll_delay_max: 12.0   # Max seconds between scrolls
  action_delay_min: 1.5    # Min seconds between actions
  action_delay_max: 4.0    # Max seconds between actions
  max_stale_scrolls: 10    # Stop after N scrolls with no new posts
```

**Output Settings:**
```yaml
output:
  base_dir: posts          # Relative to project root, or absolute path
  date_format: "%Y/%m"     # Directory structure format
```

**Media Settings:**
```yaml
media:
  download_images: true
  download_videos: true
  download_documents: true
  max_video_size_mb: 500   # Skip videos larger than this
```

**Logging:**
```yaml
logging:
  level: INFO              # DEBUG for verbose output
  file: logs/scraper.log
```

### config/site.yaml (git-ignored)

Site identity for the static site generator. Copy from `config/site.yaml.example`:

```yaml
# Identity
site_name: "Your Name"
site_description: "Your tagline."
linkedin: "https://linkedin.com/in/your-profile"
github: "https://github.com/your-username"
twitter: "https://x.com/your-handle"
twitter_handle: "@your-handle"

# Home page
hero_title: "Your Name"
hero_subline: "Your tagline here."
footer_text: "Your Name · Your City"

# Thought leadership features (all optional)
thesis: "Your 2-3 sentence POV statement shown as a callout on the home page."
newsletter_url: ""              # Substack/Beehiiv URL — shows subscribe CTA if set
speaking_text: ""               # Short blurb shown on About page

# Featured posts — auto-updated after each scrape from top engagement (last 90 days)
# Override with explicit slugs to pin specific posts
featured_posts:
  - "YYYY-MM-DD-post-slug"

# Topics — generates /topics/ index and /topics/{slug}/ pages
# Nav link appears automatically when this is configured
# Tags must match post frontmatter tags (lowercase)
topics:
  - name: "Theme Name"
    slug: theme-slug
    description: "One sentence description."
    tags: [tag1, tag2, tag3]
```

**Note:** `about_teaser` in old site.yaml configs is ignored — the homepage now uses `thesis` (rendered in the hero section). The About page link appears in the hero social links row.

### now.md (git-ignored)

Content for the `/now` page. Copy from `now.md.example` and fill in:
- What you're currently building
- What you're thinking about
- What you're reading
- What changed recently

The `/now` nav link appears automatically when `now.md` exists.

### .env File

**Pipeline (required for `bash pipeline.sh`):**
```env
LINKEDIN_PROFILE_URL=https://www.linkedin.com/in/yourprofile
```

**LinkedIn API credentials (required for API path, optional for browser crawler):**
```env
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:8080/callback
```

**Website (optional):**
```env
SITE_URL=https://yoursite.com
GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

**Opalstack deployment (optional):**
```env
OPAL_SSH_USER=your_opalstack_username
OPAL_SSH_HOST=opal1.opalstack.com
OPAL_SSH_PORT=22
OPAL_APP_PATH=/home/your_user/apps/your_app_name
```

**Important:** Never commit `.env` file. It's git-ignored.

---

## LinkedIn API Integration (Legacy)

### Authentication Endpoints

- **Authorization:** `https://www.linkedin.com/oauth/v2/authorization`
- **Token Exchange:** `https://www.linkedin.com/oauth/v2/accessToken`

### Required OAuth Scopes

- `openid` - OpenID Connect authentication
- `profile` - User profile data
- `email` - User email (optional)
- `w_member_social` - Access to posts and shares

### API Endpoints Used

1. **User Profile:** `GET /v2/userinfo`
   - Returns: name, sub (person ID), email

2. **User Posts:** `GET /v2/ugcPosts?q=authors&authors=List({personURN})`
   - Pagination: `start` and `count` parameters
   - Max 50 posts per request

### Rate Limits

- **Developer Apps:** ~500 requests per day
- **Official Limit:** Not publicly documented
- **Best Practice:** 1-2 second delay between requests

### Common API Errors

- **401 Unauthorized:** Token expired, re-authenticate
- **403 Forbidden:** Insufficient permissions
- **404 Not Found:** Invalid URN or endpoint
- **429 Too Many Requests:** Rate limited, exponential backoff
- **500 Internal Server Error:** LinkedIn issue, retry

---

## Data Models

### LinkedInPost

```python
@dataclass
class LinkedInPost:
    id: str                              # LinkedIn post URN
    post_url: str                        # Public post URL
    content: str                         # Post text content
    created_at: datetime                 # Publication timestamp
    post_type: str                       # 'original', 'repost', 'article', 'poll'
    media: List[Media]                   # Attached media files
    hashtags: List[str]                  # Extracted hashtags
    original_post_url: Optional[str]     # For reposts
    repost_commentary: Optional[str]     # User's repost comment
    slug: Optional[str]                  # URL-safe identifier
    reactions: int                       # LinkedIn reaction count at scrape time
    comments: int                        # LinkedIn comment count at scrape time
```

Engagement fields (`reactions`, `comments`) are captured by the browser crawler from the LinkedIn feed DOM and written to post frontmatter. They drive the auto-featured posts computation.

### Media

```python
@dataclass
class Media:
    type: str                    # 'image', 'video', 'document'
    url: str                     # Remote media URL
    local_path: Optional[str]    # Relative path to downloaded file
    filename: Optional[str]      # Local filename
```

---

## Claude Code Custom Skills

### /article - Long-Form Article Writer
- Writes long-form articles (1,000-3,500 words) for the website's articles section
- Follows `article_style.md` (supplement) + `writing_style.md` (primary) + `profile.md` (voice)
- Workflow: gather input → research sources → pick target audience → propose angles → outline → draft → image prompts → save → generate critique prompt. (Substack paste artifact is generated at publish time by `/publish`, not here.)
- Asks for **target audience** up front (engineering leaders, product/business, generalists, mixed) — threads through angle selection, drafting depth, and visual choices
- Saves to `articles/YYYY/MM/YYYY-MM-DD-slug/article.md`
- Generates image prompts (hero + section diagrams) following `taste.md`
- Generates a **critique prompt** (`critique-prompt.md`) — user pastes into another AI for a sharp second-opinion review before publishing
- Does NOT generate the Substack paste artifact — that's moved to `/publish` so it's only created when a draft is promoted (saves tokens during the draft iteration loop)
- Decoupled from LinkedIn/X: reminds user to run `/post` for the short-form promo on LinkedIn and X after article is finalized
- Article frontmatter: title, subtitle, date, tags, medium_url, substack_url, hero_image, reading_time, draft (always true on creation)

### /publish - Promote Draft to Published
- Removes `draft: true` from an article's frontmatter and updates `date:` to today
- Renames the directory (`articles/YYYY/MM/YYYY-MM-DD-slug/`) via `git mv` so the new date is reflected in the path
- Generates the **Substack paste artifact** (`substack-paste.md`) — reformats the article body for Substack's editor with posting checklist (title, subtitle, canonical URL pointing back to the site, image re-upload reminders). Only generated at publish time to avoid token churn during the draft loop.
- Pass a slug fragment as arg, or run with no args to pick from a list of drafts
- Reminds user to rebuild after

### /pdf - CV PDF Generator
- Generates a styled PDF version of the CV matching the site's brutalist dark theme
- Generic mode (no args): renders `cv.md` as-is → `cv_joaofogoncalves.pdf`
- Tailored mode (JD URL or text): reframes CV for a specific role → `cv-{company-slug}.pdf`
- Uses `document-skills:pdf` skill for native PDF creation (no HTML/browser)
- Design spec defined in `.claude/commands/pdf.md`

### /profile - Voice Profile Generator
- Analyzes recent LinkedIn posts (60-day window by default)
- Filters to `post_type: original` or `article` only
- Extracts writing patterns: opening hooks, sentence rhythm, vocabulary, rhetorical devices
- Generates `profile.md` — a voice profile system prompt for AI-assisted writing
- Uses tiered recency weighting (recent posts weighted higher)

### /taste - Visual Taste Profile Generator
- Analyzes images attached to posts
- Batch processes uncached images (describes them, stores descriptions in post frontmatter)
- Generates `taste.md` — a visual taste profile for image selection
- Requires 80%+ of images described before generating
- Uses tiered recency weighting for visual patterns

### /post - Short-Form Post Authoring
- Authors short-form content with the site as canonical home, and generates LinkedIn + X + Substack Note variants for manual posting
- Writes four artifacts under `posts/YYYY/MM/YYYY-MM-DD-slug/`:
  - `post.md` — canonical site version (with `authored: true` in frontmatter, empty `post_url`/`x_url`/`substack_note_url` fields filled in later after posting)
  - `linkedin.md` — LinkedIn paste-ready variant (hook-first, intentional line breaks, 2-4 hashtags, no emojis)
  - `x-thread.md` — X paste-ready variant (single long post by default — X allows long-form now; for posts with an external URL, append one short reply tweet with just the link; no hashtags)
  - `substack-note.md` — Substack Note paste-ready variant (~90% of LinkedIn copy: no hashtags, softer hook, link welcomed since Notes don't throttle them)
- Uses `writing_style.md` (primary) and `profile.md` (supplementary) for voice
- Fetches source material from URLs, proposes 2-3 angles, drafts after user picks one
- Auto-detects template: short-form commentary, article reaction, or long-form thought piece
- Thread-bias: defaults to X threads unless the idea is genuinely a single one-liner
- Image-default: posts ship with a visual unless there's an explicit reason to skip (data shows ~5x engagement uplift)
- Length target: 100-150 words is the peak engagement zone; 100-250 acceptable; under 100 underperforms
- Generates 3 image prompts (or chart spec) based on `taste.md` if images add value
- After posting manually on each surface, the user fills in `post_url:`, `x_url:`, and `substack_note_url:` in `post.md` frontmatter. On the next scraper run, engagement counts (reactions, comments) are merged in automatically via the scraper's merge mode.
- Suggested posting order: site → LinkedIn (cold reach) → X (parallel cold reach) → Substack Note (warm conversion to subscribers)

### /sync - Refresh Engagement + Catch Stragglers
- Runs the browser crawler with `--limit 10` to refresh engagement counts on existing posts (handled silently by the scraper's merge mode) and surface any genuinely-new posts that were written outside `/post`
- **Merge-mode** means re-scraping does not duplicate posts — matched posts (by `post_url` or content fingerprint within 14 days) only get `reactions:` and `comments:` refreshed; bodies are never overwritten
- For genuinely-new posts (things posted manually on LinkedIn without running `/post`), applies light noise curation: milestone posts, empty/placeholder posts, one-line reactions, pure reposts — flags each with a reason, user confirms drops via AskUserQuestion
- **No longer does self-article-promo detection** — in the authored-first model, promo posts for articles are authored via `/post` and are canonical site content, not noise
- Run before `pipeline.sh --skip-scrape` to keep engagement data fresh and catch stragglers

### /cover-letter - Tailored Cover Letter
- Generates a 250–350 word cover letter for a specific job description (URL or text)
- Reads `cv.md`, `pitch_style.md`, `profile.md`, `writing_style.md`, `config/site.yaml`
- **Lead-with-proof discipline**: opens with a specific accomplishment that maps to the role, not a generic introduction. Anti-patterns (passionate, leverage, "I would bring…") are explicitly rejected by a voice-check step.
- Saves to `applications/{company-slug}/cover-letter.md` with frontmatter (company, role, contact, date, jd_source)
- Optional: also produce a styled PDF via `document-skills:pdf` matching the brutalist theme
- Recommended companion runs: `/pdf {JD URL}` for tailored CV, `/outreach` for the recruiter DM

### /outreach - Recruiter / Hiring Manager / Founder Outreach
- Drafts three length-tiered variants of cold outreach for one specific recipient: LinkedIn DM (~80 words), email cold (~150 words), follow-up (~50 words for 5–7 days later)
- Operationalizes "Target conversations, not applications": each variant must lead with relevance to the recipient (a specific hook — their work, their post, their thesis), not with a request
- LinkedIn URLs are usually blocked by WebFetch — falls back to asking the user for the recipient's context if so
- Saves to `applications/{company-slug}/outreach.md`
- The hook is a hard requirement: if the user can't supply something specific about the recipient, the skill stops and asks. Generic outreach is worse than no outreach.

### /interview-prep - Interview Prep Document
- Given a JD (URL or text) and optional company URL, generates a focused prep doc designed to read in 30 minutes the night before
- Sections: TL;DR refresher, "Tell me about yourself" pitch tailored to the role, 5–7 behavioral questions with STAR-shaped answer notes pulled from cv.md, 5–7 technical/role questions with talking points, 5–7 substantive questions to ask back, optional company research summary, failure-mode list (specific things to avoid in this interview)
- Reads recent `articles/*` for thesis material to surface in answers
- Saves to `applications/{company-slug}/interview-prep.md`
- The embedded "Tell me about yourself" pitch follows `pitch_style.md`; the prep doc itself is plain working notes

### /pitch - Self-Pitch Variants (Living Document)
- Generates surface-tailored ways to describe yourself when there's no specific JD: elevator pitches (30s/60s/2min), LinkedIn headline + About summary, conference talk abstract, speaker bios (short/medium/long)
- Default (no args): regenerates ALL variants. Pass a variant name (`30s`, `60s`, `2min`, `linkedin-headline`, `linkedin-about`, `talk-abstract`, `bio-short`, `bio-medium`, `bio-long`) to refresh just one in place — preserves user edits to the others.
- Saves to `pitches.md` at project root (single living document with all variants under headers)
- Builds an internal **through-line sentence** first — the one claim every variant compresses or expands from — so the variants stay coherent across surfaces
- LinkedIn headline mode: generates 3 candidates and recommends the strongest; user picks

---

## Testing & Debugging

### Setup Verification

```bash
uv run python verify_setup.py
```

Checks:
- Python version (3.14+)
- All dependencies installed
- Directory structure exists
- Configuration files present
- `.env` file configured

### Debug Mode

Enable verbose logging in `config/config.yaml`:
```yaml
logging:
  level: DEBUG
```

Or set environment variable:
```bash
export LOG_LEVEL=DEBUG
uv run python -m scraper.main --fetch
```

### Testing Browser Crawler

```bash
# Login (opens headed browser)
uv run python -m scraper.main --browser-login

# Crawl with limit
uv run python -m scraper.main --limit 5

# Check logs for errors
tail -f logs/scraper.log
```

### Testing API Authentication (Legacy)

```bash
# Test OAuth flow
uv run python -m scraper.main --auth

# Check token cache
cat cache/token.json

# Force re-authentication
uv run python -m scraper.main --reauth
```

### Common Issues

**Browser crawler hangs or gets detected:**
- Increase scroll delays in `config.yaml` (`scroll_delay_min`/`scroll_delay_max`)
- Clear browser profile: `rm -rf cache/browser_profile` and re-login
- Check if LinkedIn UI has changed (DOM selectors may need updating)

**Port 8080 in use (API auth):**
- Check: `lsof -i :8080`
- Kill process: `kill -9 <PID>`
- Or change port in auth.py (also update .env redirect URI)

**Authentication fails (API):**
- Verify credentials in `.env`
- Check redirect URI matches app settings exactly
- Ensure app has required permissions approved

**No posts fetched:**
- Check logs: `cat logs/scraper.log`
- For browser crawler: verify login session is still valid
- For API: verify permissions, try `--reauth`

**Media downloads fail:**
- Check internet connection
- LinkedIn media URLs may expire (temporary signed URLs)
- Increase timeout in config.yaml
- Check disk space

**Site build fails:**
- Ensure posts exist in `posts/` directory
- Check that `cv.md` exists (used for About page)
- Run with Python 3.9+ from venv

---

## Important Notes

### Security Considerations

1. **Never commit `.env` file** - Contains sensitive credentials
2. **Token/browser cache** - Stored in `cache/` (git-ignored)
3. **API credentials** - Keep Client ID and Secret secure
4. **Browser profile** - Contains LinkedIn session cookies (git-ignored)
5. **SSH credentials** - Opalstack deploy vars in `.env` only

### Git Strategy

**Tracked:**
- All Python code (scraper + web + cv generator)
- Documentation (README, CONTRIBUTING, RATE_LIMITS, CLAUDE.md)
- Configuration templates (`config/config.yaml`, `config/site.yaml.example`)
- Example files (`now.md.example`, `examples/`)
- Website source (CSS, JS, favicons)
- Claude Code skills (`.claude/commands/`) and settings (`.claude/settings.json`)
- CV PDF generator (`cv/generate.py`, `cv/fonts/`)
- `cv_joaofogoncalves.pdf` (persistent generated asset)
- `cv.md`, `profile.md`, `taste.md`, `now.md` (personal content the user owns)
- `writing_style.md`, `article_style.md`, `pitch_style.md` (style guides feeding the skills)
- `articles/` directory (original long-form articles — authored content, not scraped)
- `posts/` directory (short-form posts — authored via `/post` and historical scrape; the authored-first model treats these as canonical site content the user owns)

**Ignored (runtime + per-application artifacts):**
- `config/site.yaml` (site identity — copy `config/site.yaml.example` to start)
- `web/img/headshot.jpg` (personal photo)
- `.env` file (credentials)
- `.venv/`, `cache/`, `logs/`, `web/dist/`, `drafts/`
- `applications/` (per-application artifacts — cover letters, outreach, interview prep, tailored CVs; often contain confidential JD text and recipient details)

### Performance Considerations

1. **Browser crawl** - Takes 10-30+ minutes depending on post count and scroll delays
2. **Rate limiting (API)** - Adds 1.5s per request
3. **Video downloads** - Can be slow for large files
4. **Site build** - Fast (seconds), reads markdown files
5. **Deploy** - Depends on rsync delta size

---

## Maintenance Tasks

### Update Dependencies

```bash
uv lock --upgrade        # bump lockfile to latest compatible versions
uv sync                  # apply the new lockfile to .venv
uv tree --outdated       # show what's still out of date
```

### Update Playwright Browsers

```bash
uv run playwright install
```

### Clear Cache

```bash
# Clear API token
rm -rf cache/token.json

# Clear browser session (will need to re-login)
rm -rf cache/browser_profile

# Re-login
uv run python -m scraper.main --browser-login
```

### Clean Logs

```bash
rm logs/scraper.log
# Logs auto-recreate on next run
```

### Re-archive Posts

```bash
# Safe to re-run, skips existing
uv run python -m scraper.main --fetch
```

### Rebuild & Deploy Website

```bash
bash web/deploy.sh
```

---

## Future Enhancement Ideas

### Potential Improvements (Not Implemented)

1. **Incremental updates** - Track last fetch date, only get new posts
2. **Comment archiving** - Preserve comment threads on posts
3. **Engagement metrics** - Store likes/comments/shares over time
4. **Analytics** - Post frequency, popular topics, etc.
5. **Scheduled archiving** - Cron job for automatic updates
6. **Multi-user support** - Archive multiple LinkedIn accounts

### Implementation Guidelines for Additions

- Maintain backward compatibility with existing archives
- Add new features as optional flags
- Update all documentation when adding features
- Keep configuration in `config.yaml`
- Follow existing code conventions

---

## When Working with Claude Code

### Modifying Code

**Before making changes:**
1. Read the relevant module first
2. Check `logs/scraper.log` for error context
3. Understand the data flow through the system

**After making changes:**
1. Test with `--limit 5` for quick validation
2. Check logs for errors or warnings
3. Verify output in `posts/` directory
4. Update documentation if needed

### Common Requests

**"Add support for X feature":**
1. Check if feature aligns with project scope (post archiving + publishing)
2. Identify affected modules (usually 2-3)
3. Update data models if needed
4. Add configuration options
5. Update documentation

**"Fix bug with Y":**
1. Read logs in `logs/scraper.log`
2. Identify which module has the issue
3. Add more logging if needed for debugging
4. Test fix with `--limit 5`
5. Verify fix doesn't break existing functionality

**"Update documentation":**
1. Identify which doc needs update (README vs QUICKSTART vs this file)
2. Keep examples concrete and tested
3. Update all relevant docs consistently

### Project Philosophy

- **Simplicity:** Keep it simple and maintainable
- **Reliability:** Prefer robustness over features
- **User control:** User owns their data completely
- **Privacy:** Everything stored locally (publishing is opt-in)
- **Idempotent:** Safe to re-run operations
- **Fail gracefully:** One error shouldn't stop entire process

---

## Module Responsibilities

### scraper/main.py
- CLI argument parsing
- Application orchestration (browser crawler or API path)
- User-facing output and statistics
- Error handling at top level

### scraper/browser_crawler.py
- Playwright browser automation
- LinkedIn feed scrolling and post extraction
- DOM parsing for post content, media, links
- Session management (login, profile persistence)
- Checkpoint save/resume for interrupted crawls
- Repost detection and filtering

### scraper/auth.py
- OAuth 2.0 authorization flow (legacy)
- Browser-based authentication
- Token caching and retrieval
- Re-authentication handling

### scraper/linkedin_client.py
- Low-level LinkedIn API wrapper (legacy)
- HTTP request handling
- Rate limiting implementation
- Retry logic and error handling

### scraper/post_fetcher.py
- Parse LinkedIn API responses
- Convert raw data to LinkedInPost objects
- Extract media URLs from posts
- Determine post types

### scraper/export_parser.py
- Import posts from LinkedIn data export files
- Parse exported data format into LinkedInPost objects

### scraper/media_downloader.py
- Download images, videos, documents
- File validation (especially images)
- Progress bars for large downloads
- Size limit enforcement

### scraper/markdown_generator.py
- Generate markdown from LinkedInPost
- Format reposts specially
- Embed media references
- Create index files

### scraper/models.py
- Data class definitions
- Input validation
- Type safety

### scraper/utils.py
- Slug generation
- Filename sanitization
- Hashtag extraction
- Configuration loading
- Logging setup
- Checkpoint save/load for crawler resume

### web/build.py
- Static site generator
- Loads site identity from `config/site.yaml` (name, bio, social links, footer, topics, thesis, etc.)
- Reads markdown posts from `posts/`, articles from `articles/`, About content from `cv.md`, Now content from `now.md`
- Generates HTML pages: Home, About, Articles archive, Posts archive, /topics index, /topics/{slug}, /now, individual posts, individual articles
- Also generates: `feed.xml` (RSS 2.0, last 20 articles — articles only, no short-form posts), `sitemap.xml`, `robots.txt`
- JSON-LD structured data: Person schema on About, Article schema on each post and article
- Topics are assigned at build time by matching post/article tags against `topics[].tags` in site.yaml
- `compute_featured_posts(posts, days=90, top_n=3)` — engagement-ranked featured posts
- `update_site_yaml_featured(slugs)` — overwrites `featured_posts` in site.yaml in-place
- `parse_all_articles()` — scans `articles/` for `article.md` files, extracts frontmatter (title, subtitle, hero_image, medium_url, reading_time)
- Nav links for Articles, Topics, and Now appear automatically when content exists; no dead links
- **Homepage helpers**: `_featured_spotlight_html()` (auto-rotating spotlight, accepts articles or posts), `_recent_notes_html()` (compact recent-posts strip), `_topics_home_html()` (topic cards), `_newsletter_section_html()` (CTA section)
- **Posts page**: Single continuous list of spotlight-style row cards (`_render_list_card()` + `.list-card` CSS). Full-width rows with text left, thumbnail right (300×175). JS renders same format dynamically via `posts.js`.
- Articles section: `/articles/` archive with hero image cards, `/articles/YYYY/MM/slug/` individual pages
- Post/article content: 720px (`--max-content`) centered with `margin: 0 auto` within the 1280px page container
- About page gracefully handles missing `cv.md` with placeholder
- `nav_html()` accepts `transparent=True` for homepage (particles visible behind nav)
- Outputs to `web/dist/`

### web/resolve_links.py
- Resolves `lnkd.in` shortened URLs in archived posts
- Fetches real destination URLs
- Updates post.md files in-place
- Supports `--dry-run` mode

### web/deploy.sh
- Builds site via `build.py` then deploys via rsync over SSH
- Loads credentials from `.env`

### pipeline.sh
- Full automation: scrape → resolve links → build → deploy
- `--skip-scrape`: rebuild/deploy only (use after editing `now.md` or `site.yaml`)
- `--dry-run`: scrape + resolve but do not deploy

### cv/generate.py
- Self-contained reportlab script that generates `cv_joaofogoncalves.pdf` from hardcoded CV content
- Brutalist dark theme: `#0e131e` background, `#44d8f1` teal accents, Inter + JetBrains Mono fonts
- Fonts bundled in `cv/fonts/` — no external downloads needed at runtime
- Run: `uv run python cv/generate.py` → outputs `cv_joaofogoncalves.pdf` in project root

---

## Contact & Support

**Documentation:**
- README.md - Comprehensive guide
- QUICKSTART.md - Quick setup
- PROJECT_SUMMARY.md - Technical details
- CONTRIBUTING.md - Contribution guidelines
- RATE_LIMITS.md - API rate limit details

**Debugging:**
- Check `logs/scraper.log` first
- Run with `--limit 5` for testing
- Use DEBUG log level for verbose output

**LinkedIn API:**
- Docs: https://docs.microsoft.com/en-us/linkedin/
- Developer Portal: https://www.linkedin.com/developers/

---

_Last updated: 2026-04-18_
_Project version: 2.1.0_
