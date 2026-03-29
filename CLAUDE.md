# LinkedIn Post Archiver - Claude Code Instructions

## Project Overview

This is a Python application that archives LinkedIn posts locally as clean markdown files with media downloads, and publishes them as a static website. It uses a **Playwright browser crawler** (primary method) or OAuth 2.0 API (legacy fallback) to fetch posts and preserve them in an organized folder structure. A static site generator converts the archive into a deployable website.

**Purpose:** Create a permanent, offline archive of the user's LinkedIn content that they control - focusing on what they wrote, not engagement metrics. Optionally publish as a personal website.

**Status:** Production-ready. Archiving, site generation, and deployment all working.

---

## Technology Stack

- **Python 3.9+** (currently running on 3.14)
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
│   │   └── style.css                 # Brutalist dark theme styles
│   ├── js/
│   │   └── posts.js                  # Client-side search/filter
│   ├── img/
│   │   └── headshot.jpg              # Author photo for About page
│   └── dist/                         # Generated site output (git-ignored)
│
├── config/
│   └── config.yaml                   # Application configuration
│
├── posts/                            # Archived posts output
│   └── YYYY/MM/post-slug/
│       ├── post.md                   # Markdown file (tracked)
│       └── media/                    # Downloaded images/videos (git-ignored)
│
├── .claude/
│   └── commands/                     # Claude Code custom skills
│       ├── profile.md                # /profile - voice profile generator
│       └── taste.md                  # /taste - visual taste profile generator
│
├── cache/                            # Browser profile + token cache (git-ignored)
├── logs/                             # Application logs (git-ignored)
├── venv/                             # Virtual environment (git-ignored)
│
├── requirements.txt                  # Python dependencies
├── .env                              # Credentials (git-ignored, created by user)
├── .env.example                      # Credentials template
├── .gitignore                        # Git exclusions
│
├── cv.md                             # Professional CV (used by site generator)
├── profile.md                        # Voice profile for AI-assisted writing
├── taste.md                          # Visual taste profile for image selection
├── stitch-prompt.md                  # Website design spec for Stitch mockups
│
├── README.md                         # Full documentation
├── QUICKSTART.md                     # 5-minute setup guide
├── PROJECT_SUMMARY.md                # Technical implementation details
├── CONTRIBUTING.md                   # Contribution guidelines
├── PUBLISH_CHECKLIST.md              # GitHub publishing checklist
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

### 4. Post Organization
- Structure: `posts/YYYY/MM/post-slug/`
- Slug format: `YYYY-MM-DD-first-words-of-post` (max 60 chars)
- Duplicate slugs handled with numeric suffixes (-2, -3, etc.)
- Media stored in `media/` subdirectory per post

### 5. Idempotent Operation
- Safe to re-run; skips posts that already exist
- Checks for `post.md` file before archiving
- Media downloads skip existing files

### 6. Error Handling
- All errors logged to `logs/scraper.log`
- Failed posts logged but don't stop the entire process
- Media download failures noted in logs but don't fail post creation

### 7. Static Site Generator
- `web/build.py` reads markdown posts and generates a complete static site
- Brutalist dark theme ("senior engineer's personal site")
- 3 pages: Home (hero + recent posts), About (CV timeline), Posts (searchable archive)
- Only shows `post_type: original` or `article` (filters out reposts)
- Client-side search and tag filtering via `web/js/posts.js`
- Output to `web/dist/` (git-ignored)

### 8. Deployment (Opalstack)
- `web/deploy.sh` builds the site and deploys via rsync over SSH
- Credentials loaded from `.env` (OPAL_* variables)
- Deletes stale files on remote

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

### Virtual Environment

**Always activate venv before working:**
```bash
source venv/bin/activate  # macOS/Linux
```

**Check current environment:**
```bash
which python  # Should point to venv/bin/python
```

### Running the Application

**Browser login (first time):**
```bash
python scraper/main.py --browser-login
```

**Archive all posts (browser crawler):**
```bash
python scraper/main.py --fetch
```

**Test with limited posts:**
```bash
python scraper/main.py --limit 10
```

**Legacy API authentication:**
```bash
python scraper/main.py --auth
```

**Force re-authentication (API):**
```bash
python scraper/main.py --reauth --fetch
```

### Static Site Workflow

**Build the website:**
```bash
python web/build.py
```

**Resolve lnkd.in shortened URLs in posts:**
```bash
python web/resolve_links.py          # apply changes
python web/resolve_links.py --dry-run  # preview only
```

**Deploy to Opalstack:**
```bash
bash web/deploy.sh
```

### Full Pipeline

```bash
# 1. Crawl new posts
python scraper/main.py --fetch

# 2. Resolve shortened URLs
python web/resolve_links.py

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

### .env File

**Required environment variables:**
```env
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:8080/callback
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
```

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

### /profile - Voice Profile Generator
- Analyzes recent LinkedIn posts (60-day window by default)
- Filters to `post_type: original` or `article` only
- Extracts writing patterns: opening hooks, sentence rhythm, vocabulary, rhetorical devices
- Generates `profile.md` - a voice profile system prompt for AI-assisted writing
- Uses tiered recency weighting (recent posts weighted higher)

### /taste - Visual Taste Profile Generator
- Analyzes images attached to posts
- Batch processes uncached images (describes them, stores descriptions in post frontmatter)
- Generates `taste.md` - a visual taste profile for image selection
- Requires 80%+ of images described before generating
- Uses tiered recency weighting for visual patterns

---

## Testing & Debugging

### Setup Verification

```bash
python verify_setup.py
```

Checks:
- Python version (3.9+)
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
python scraper/main.py --fetch
```

### Testing Browser Crawler

```bash
# Login (opens headed browser)
python scraper/main.py --browser-login

# Crawl with limit
python scraper/main.py --limit 5

# Check logs for errors
tail -f logs/scraper.log
```

### Testing API Authentication (Legacy)

```bash
# Test OAuth flow
python scraper/main.py --auth

# Check token cache
cat cache/token.json

# Force re-authentication
python scraper/main.py --reauth
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
- All Python code (scraper + web)
- Documentation files
- Configuration templates
- Markdown post files
- Post images in `posts/**/media/`
- Website source (CSS, JS, images)

**Ignored:**
- `.env` file
- `venv/` directory
- `cache/` directory (browser profile + tokens)
- `logs/` directory
- `web/dist/` (generated site output)
- Large video files (*.mp4, *.mov)

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
source venv/bin/activate
pip install --upgrade -r requirements.txt
pip list --outdated
```

### Update Playwright Browsers

```bash
python -m playwright install
```

### Clear Cache

```bash
# Clear API token
rm -rf cache/token.json

# Clear browser session (will need to re-login)
rm -rf cache/browser_profile

# Re-login
python scraper/main.py --browser-login
```

### Clean Logs

```bash
rm logs/scraper.log
# Logs auto-recreate on next run
```

### Re-archive Posts

```bash
# Safe to re-run, skips existing
python scraper/main.py --fetch
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
- Reads markdown posts from `posts/` and `cv.md`
- Generates HTML pages (Home, About, Posts)
- Markdown-to-HTML conversion with frontmatter parsing
- Outputs to `web/dist/`

### web/resolve_links.py
- Resolves `lnkd.in` shortened URLs in archived posts
- Fetches real destination URLs
- Updates post.md files in-place
- Supports `--dry-run` mode

### web/deploy.sh
- Builds site via `build.py`
- Deploys to Opalstack via rsync over SSH
- Loads credentials from `.env`

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

_Last updated: 2026-03-27_
_Project version: 2.0.0_
