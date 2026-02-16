# LinkedIn Post Archiver - Claude Code Instructions

## Project Overview

This is a Python application that archives LinkedIn posts locally as clean markdown files with media downloads. It uses OAuth 2.0 authentication with the LinkedIn API to fetch posts and preserve them in an organized folder structure.

**Purpose:** Create a permanent, offline archive of the user's LinkedIn content that they control - focusing on what they wrote, not engagement metrics.

**Status:** Production-ready, fully implemented and tested.

---

## Technology Stack

- **Python 3.9+** (currently running on 3.14)
- **LinkedIn API v2** (OAuth 2.0 with OpenID Connect)
- **Core Libraries:**
  - `requests` - HTTP client for API calls
  - `requests-oauthlib` - OAuth 2.0 implementation
  - `PyYAML` - Configuration management
  - `Pillow` - Image validation and processing
  - `tqdm` - Progress bars
  - `coloredlogs` - Enhanced console output

---

## Directory Structure

```
linkedin-post-archiver/  # Project root
├── scraper/                          # Main application package
│   ├── __init__.py                   # Package initialization
│   ├── main.py                       # CLI entry point & orchestration
│   ├── auth.py                       # OAuth 2.0 authentication flow
│   ├── linkedin_client.py            # LinkedIn API wrapper with rate limiting
│   ├── post_fetcher.py               # Parse API responses into Post objects
│   ├── media_downloader.py           # Download and validate media files
│   ├── markdown_generator.py         # Generate markdown output
│   ├── models.py                     # Data models (LinkedInPost, Media)
│   └── utils.py                      # Helper functions
│
├── config/
│   └── config.yaml                   # Application configuration
│
├── posts/                            # Archived posts output (git-ignored media)
│   └── YYYY/MM/post-slug/
│       ├── post.md                   # Markdown file
│       └── media/                    # Downloaded images/videos
│
├── cache/                            # OAuth token cache (git-ignored)
├── logs/                             # Application logs (git-ignored)
├── venv/                             # Virtual environment (git-ignored)
│
├── requirements.txt                  # Python dependencies
├── .env                              # Credentials (git-ignored, created by user)
├── .env.example                      # Credentials template
├── .gitignore                        # Git exclusions
│
├── README.md                         # Full documentation
├── QUICKSTART.md                     # 5-minute setup guide
├── PROJECT_SUMMARY.md                # Technical implementation details
├── verify_setup.py                   # Setup verification script
└── CLAUDE.md                         # This file
```

---

## Key Design Decisions

### 1. OAuth 2.0 Flow
- Uses local HTTP server on port 8080 to catch OAuth callback
- Token cached in `cache/token.json` for reuse
- Browser automatically opens for user authorization
- Supports re-authentication with `--reauth` flag

### 2. Rate Limiting
- 1.5 second delay between API requests (configurable)
- Exponential backoff on 429 rate limit errors: 1s → 2s → 4s → 8s
- Max 3 retries per request
- All rate limiting handled in `linkedin_client.py`

### 3. Post Organization
- Structure: `posts/YYYY/MM/post-slug/`
- Slug format: `YYYY-MM-DD-first-words-of-post` (max 60 chars)
- Duplicate slugs handled with numeric suffixes (-2, -3, etc.)
- Media stored in `media/` subdirectory per post

### 4. Idempotent Operation
- Safe to re-run; skips posts that already exist
- Checks for `post.md` file before archiving
- Media downloads skip existing files

### 5. Error Handling
- All API errors logged to `logs/scraper.log`
- Failed posts logged but don't stop the entire process
- Media download failures noted in logs but don't fail post creation

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

**Authentication:**
```bash
python scraper/main.py --auth
```

**Archive all posts:**
```bash
python scraper/main.py --fetch
```

**Test with limited posts:**
```bash
python scraper/main.py --limit 10
```

**Force re-authentication:**
```bash
python scraper/main.py --reauth --fetch
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

**LinkedIn API Settings:**
```yaml
linkedin:
  api_version: v2
  rate_limit_delay: 1.5    # Increase if hitting rate limits
  max_retries: 3           # Number of retry attempts
  timeout: 30              # HTTP request timeout
```

**Output Settings:**
```yaml
output:
  base_dir: /path/to/posts  # Archive output directory
  date_format: "%Y/%m"      # Directory structure format
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

**Important:** Never commit `.env` file. It's git-ignored.

---

## LinkedIn API Integration

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

### Testing Authentication

```bash
# Test OAuth flow
python scraper/main.py --auth

# Check token cache
cat cache/token.json

# Force re-authentication
python scraper/main.py --reauth
```

### Testing Post Fetching

```bash
# Fetch only 5 posts for testing
python scraper/main.py --limit 5

# Check logs for errors
tail -f logs/scraper.log

# Verify output structure
ls -R posts/
```

### Common Issues

**Port 8080 in use:**
- Check: `lsof -i :8080`
- Kill process: `kill -9 <PID>`
- Or change port in auth.py (also update .env redirect URI)

**Authentication fails:**
- Verify credentials in `.env`
- Check redirect URI matches app settings exactly
- Ensure app has required permissions approved

**No posts fetched:**
- Check logs: `cat logs/scraper.log`
- Verify API permissions in LinkedIn app
- Try re-authentication: `--reauth`

**Media downloads fail:**
- Check internet connection
- LinkedIn media URLs may expire (temporary signed URLs)
- Increase timeout in config.yaml
- Check disk space

---

## Important Notes

### Security Considerations

1. **Never commit `.env` file** - Contains sensitive credentials
2. **Token cache** - Stored in `cache/token.json` (git-ignored)
3. **API credentials** - Keep Client ID and Secret secure
4. **Access tokens** - Expire after ~60 days (varies)

### LinkedIn API Limitations

1. **Rate limits** - Respect 1.5s delay between requests
2. **Data access** - Can only fetch your own posts
3. **Historical data** - Depends on when app was created
4. **Media URLs** - May be temporary/signed, download immediately

### Git Strategy

**Tracked:**
- All Python code
- Documentation files
- Configuration templates
- Markdown output files

**Ignored:**
- `.env` file
- `venv/` directory
- `cache/` directory
- `logs/` directory
- Media files in `posts/**/media/`
- Large video files (*.mp4, *.mov)

### Performance Considerations

1. **Initial archive** - May take 10-30 minutes depending on post count
2. **Rate limiting** - Adds 1.5s per request (necessary)
3. **Video downloads** - Can be slow for large files
4. **Disk space** - Videos can be 500MB+ each

---

## Maintenance Tasks

### Update Dependencies

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
pip list --outdated
```

### Clear Cache

```bash
rm -rf cache/token.json
python scraper/main.py --auth
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

### Backup Archive

```bash
# Backup posts (markdown only)
tar -czf posts-backup-$(date +%Y%m%d).tar.gz posts/**/*.md posts/**/INDEX.md

# Include media (large!)
tar -czf posts-full-backup-$(date +%Y%m%d).tar.gz posts/
```

---

## Future Enhancement Ideas

### Potential Improvements (Not Implemented)

1. **Incremental updates** - Track last fetch date, only get new posts
2. **Comment archiving** - Preserve comment threads on posts
3. **Engagement metrics** - Store likes/comments/shares over time
4. **HTML export** - Generate browsable HTML version
5. **Search functionality** - Full-text search across archive
6. **Analytics** - Post frequency, popular topics, etc.
7. **Scheduled archiving** - Cron job for automatic updates
8. **Multi-user support** - Archive multiple LinkedIn accounts

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
1. Check if feature aligns with project scope (post archiving)
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
- **Privacy:** Everything stored locally
- **Idempotent:** Safe to re-run operations
- **Fail gracefully:** One error shouldn't stop entire process

---

## Module Responsibilities

### main.py
- CLI argument parsing
- Application orchestration
- User-facing output and statistics
- Error handling at top level

### auth.py
- OAuth 2.0 authorization flow
- Browser-based authentication
- Token caching and retrieval
- Re-authentication handling

### linkedin_client.py
- Low-level LinkedIn API wrapper
- HTTP request handling
- Rate limiting implementation
- Retry logic and error handling

### post_fetcher.py
- Parse LinkedIn API responses
- Convert raw data to LinkedInPost objects
- Extract media URLs from posts
- Determine post types

### media_downloader.py
- Download images, videos, documents
- File validation (especially images)
- Progress bars for large downloads
- Size limit enforcement

### markdown_generator.py
- Generate markdown from LinkedInPost
- Format reposts specially
- Embed media references
- Create index files

### models.py
- Data class definitions
- Input validation
- Type safety

### utils.py
- Slug generation
- Filename sanitization
- Hashtag extraction
- Configuration loading
- Logging setup

---

## Contact & Support

**Documentation:**
- README.md - Comprehensive guide
- QUICKSTART.md - Quick setup
- PROJECT_SUMMARY.md - Technical details

**Debugging:**
- Check `logs/scraper.log` first
- Run with `--limit 5` for testing
- Use DEBUG log level for verbose output

**LinkedIn API:**
- Docs: https://docs.microsoft.com/en-us/linkedin/
- Developer Portal: https://www.linkedin.com/developers/

---

_Last updated: 2026-02-16_
_Project version: 1.0.0_
