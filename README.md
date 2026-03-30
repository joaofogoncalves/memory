# LinkedIn Post Archiver

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Archive your LinkedIn posts as clean markdown files with media downloads, and optionally publish them as a static website. Keep a permanent, offline backup of your content that you control.

## Features

- **Browser Crawler** (primary) — Playwright-based automation, no API limits
- **LinkedIn API** (fallback) — OAuth 2.0 for programmatic access
- **Media Downloads** — Images, videos, and documents saved locally
- **Clean Markdown** — Readable files with YAML frontmatter, organized by date
- **Static Site Generator** — Dark-themed personal website from your archive
- **Idempotent** — Safe to re-run; skips already archived posts
- **Resume Support** — Automatic checkpointing to resume interrupted crawls

## Quick Start

### Prerequisites

- Python 3.9+
- A LinkedIn account

### 1. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/linkedin-post-archiver.git
cd linkedin-post-archiver

python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
python -m playwright install
```

### 2. Configure credentials

```bash
cp .env.example .env
```

Edit `.env` and add your LinkedIn API credentials (only needed for the API path):

```env
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:8080/callback
```

> **API credentials are optional** if you only use the browser crawler. To create
> them, go to [LinkedIn Developers](https://www.linkedin.com/developers/apps),
> create an app, enable "Sign In with LinkedIn using OpenID Connect" and
> "Share on LinkedIn", then copy the Client ID and Secret.

### 3. Archive your posts

**Browser crawler (recommended):**

```bash
# First time — opens a browser window to log in
python scraper/main.py --browser-login

# Fetch all posts
python scraper/main.py --fetch

# Or limit to the most recent N posts
python scraper/main.py --limit 50
```

**API path (alternative):**

```bash
python scraper/main.py --auth    # authenticate via OAuth
python scraper/main.py --fetch   # fetch posts
```

### 4. Verify setup (optional)

```bash
python verify_setup.py
```

## Publishing a Website (Optional)

The site generator turns your archive into a static personal website with a dark, brutalist theme.

### 1. Configure your site

```bash
cp config/site.yaml.example config/site.yaml
```

Edit `config/site.yaml` with your name, bio, and social links.

### 2. Add your CV (optional)

Create a `cv.md` in the project root for the About page (see `cv.md.example` for the format). If omitted, the About page shows a placeholder.

### 3. Add a headshot (optional)

Place a `headshot.jpg` in `web/img/` to display on the About page.

### 4. Build

```bash
python web/build.py
```

Output goes to `web/dist/`. Open `web/dist/index.html` to preview locally.

### 5. Deploy

The included deploy script uses rsync over SSH (configured for Opalstack):

```bash
bash web/deploy.sh
```

For other hosts (GitHub Pages, Netlify, Vercel), point the build to `python web/build.py` and publish the `web/dist/` directory. See comments in `web/deploy.sh` for details.

## Output Structure

```
posts/
└── 2024/
    └── 01/
        └── 2024-01-15-first-post-about-ai/
            ├── post.md          # Markdown with YAML frontmatter
            └── media/
                ├── image-1.jpg
                └── image-2.jpg
```

See `examples/sample-post/post.md` for the full format.

## Configuration

### `config/config.yaml` — Scraper settings

Controls crawl behavior, rate limiting, media downloads, and logging. All options are commented inline.

### `config/site.yaml` — Website personalization

Your name, bio, social links, and footer text. Copy from `config/site.yaml.example`.

### `.env` — Credentials

LinkedIn API keys, Google Analytics ID, and deployment credentials. Copy from `.env.example`.

## Rate Limits

The browser crawler is not subject to API rate limits (it scrolls the feed like a regular user). It uses configurable delays between actions to avoid detection.

The API path has a ~500 requests/day limit. Most users can archive everything in one run. See [RATE_LIMITS.md](RATE_LIMITS.md) for detailed information on batching, automation, and monitoring.

## Troubleshooting

### Browser crawler

- **Hangs or gets detected:** Increase `scroll_delay_min`/`scroll_delay_max` in `config/config.yaml`
- **Session expired:** Clear the browser profile with `rm -rf cache/browser_profile` and re-login with `--browser-login`
- **No posts found:** Verify login worked, check `logs/scraper.log`

### API path

- **Authentication failed:** Verify Client ID and Secret in `.env`, check redirect URI matches exactly
- **Port 8080 in use:** Run `lsof -i :8080` and free the port
- **No posts fetched:** Re-authenticate with `--reauth`, check app permissions

### General

- **Media download failed:** URLs may be temporary; check internet connection and disk space
- **Logs:** Always check `logs/scraper.log` for detailed error messages

## Project Structure

```
├── scraper/                    # Post archiver
│   ├── main.py                 # CLI entry point
│   ├── browser_crawler.py      # Playwright crawler (primary)
│   ├── auth.py                 # OAuth 2.0 (API fallback)
│   ├── linkedin_client.py      # API wrapper
│   ├── post_fetcher.py         # API response parsing
│   ├── export_parser.py        # LinkedIn data export parser
│   ├── media_downloader.py     # Media downloads
│   ├── markdown_generator.py   # Markdown output
│   ├── models.py               # Data models
│   └── utils.py                # Helpers + checkpointing
│
├── web/                        # Static site generator
│   ├── build.py                # Markdown → HTML
│   ├── deploy.sh               # Rsync deployment
│   ├── resolve_links.py        # Resolve lnkd.in URLs
│   ├── css/, js/, img/         # Site assets
│   └── dist/                   # Build output (gitignored)
│
├── config/
│   ├── config.yaml             # Scraper config
│   └── site.yaml.example       # Site identity template
│
├── examples/
│   └── sample-post/post.md     # Example archived post
│
├── .env.example                # Credentials template
├── cv.md.example               # CV template for About page
├── requirements.txt            # Python dependencies
├── verify_setup.py             # Setup checker
├── CONTRIBUTING.md             # Contribution guidelines
├── RATE_LIMITS.md              # API rate limit details
├── LICENSE                     # MIT
└── CLAUDE.md                   # Claude Code instructions
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License. See [LICENSE](LICENSE).

This tool is for personal archiving of your own content. Respect LinkedIn's Terms of Service.
