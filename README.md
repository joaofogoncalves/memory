# LinkedIn Post Archiver

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python tool to archive your LinkedIn posts locally as clean, readable markdown files with media downloads. Keep a permanent, offline backup of your content that you control.

## Features

- **OAuth 2.0 Authentication** - Secure authentication with LinkedIn API
- **Complete Post Archive** - Fetch all your LinkedIn posts (original, reposts, articles, polls)
- **Media Downloads** - Download images, videos, and documents locally
- **Clean Markdown** - Generate readable markdown files organized by date
- **Organized Structure** - Posts organized in `YYYY/MM/post-slug/` folders
- **Rate Limiting** - Respectful API usage with automatic rate limiting
- **Idempotent** - Safe to re-run; skips already archived posts

## Prerequisites

### 1. Create a LinkedIn Developer App

Before using this tool, you need to create a LinkedIn Developer App:

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps)
2. Click **"Create app"**
3. Fill in the required details:
   - App name: "LinkedIn Post Archiver" (or any name)
   - LinkedIn Page: Select or create a page
   - App logo: Upload any image
4. Click **"Create app"**

### 2. Configure OAuth Settings

1. In your app settings, go to **"Auth"** tab
2. Under **"OAuth 2.0 settings"**:
   - Add redirect URL: `http://localhost:8080/callback`
3. Under **"Products"**, request access to:
   - **"Sign In with LinkedIn using OpenID Connect"**
   - **"Share on LinkedIn"**
4. Copy your **Client ID** and **Client Secret**

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/joaofogoncalves/linkedin-post-archiver.git
cd linkedin-post-archiver
```

Or download and extract the ZIP file from GitHub.

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Credentials

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:8080/callback
```

## Usage

### Authenticate

Run authentication first to get an access token:

```bash
python scraper/main.py --auth
```

This will:
1. Open your browser to LinkedIn login
2. Ask you to authorize the app
3. Redirect back to localhost and save the token

### Archive All Posts

After authentication, fetch and archive all your posts:

```bash
python scraper/main.py --fetch
```

### Archive Recent Posts

Fetch only the last N posts (e.g., 50):

```bash
python scraper/main.py --limit 50
```

### Force Re-authentication

If your token expires or you want to re-authenticate:

```bash
python scraper/main.py --reauth --fetch
```

## Output Structure

Posts are organized in the following structure:

```
posts/
├── 2024/
│   ├── 01/
│   │   ├── 2024-01-15-first-post-about-ai/
│   │   │   ├── post.md
│   │   │   └── media/
│   │   │       ├── image-1.jpg
│   │   │       └── image-2.jpg
│   │   └── 2024-01-20-thoughts-on-web-development/
│   │       └── post.md
│   └── 02/
│       └── 2024-02-10-exciting-project-launch/
│           ├── post.md
│           └── media/
│               └── video-1.mp4
└── INDEX.md  # Generated index of all posts
```

## Markdown Format

Each post is saved as a clean markdown file:

```markdown
---
date: 2024-01-15
post_url: https://linkedin.com/posts/...
post_type: original
archived_at: 2024-02-16
tags: [AI, technology, innovation]
---

# January 15, 2024

This is the content of my LinkedIn post. It preserves
all the original formatting and line breaks.

Multiple paragraphs are maintained properly.

**Hashtags:** #AI #technology #innovation

---

## Media

![image-1.jpg](media/image-1.jpg)
![image-2.jpg](media/image-2.jpg)

---

[View original post on LinkedIn](https://linkedin.com/posts/...)
```

## Configuration

Edit `config/config.yaml` to customize behavior:

```yaml
linkedin:
  rate_limit_delay: 1.5  # Seconds between API requests
  max_retries: 3         # Max retry attempts
  timeout: 30            # Request timeout in seconds

media:
  download_images: true
  download_videos: true
  download_documents: true
  max_video_size_mb: 500

logging:
  level: INFO
  file: logs/scraper.log
```

## Understanding Rate Limits

### Quick Facts

- **Daily Limit:** ~500 API requests per day
- **Per Request:** Up to 50 posts
- **Your Capacity:** 25,000 posts per day

**Bottom Line:** Most users can archive all their posts in one run!
- 1,000 posts = ~20 requests (4% of daily limit)
- The script is **idempotent** - safe to run daily for updates

**📖 See [RATE_LIMITS.md](RATE_LIMITS.md) for detailed information about:**
- Automated daily updates
- Setting up cron jobs / Task Scheduler
- Batch processing strategies
- Request tracking and monitoring

### What If I Have Many Posts?

**Option 1: Run in batches** (recommended for 10,000+ posts)
```bash
# Day 1: First 5,000 posts (~100 requests)
python scraper/main.py --limit 5000

# Day 2: Next batch (automatically skips existing)
python scraper/main.py --fetch
```

**Option 2: Single run** (works for most users)
```bash
# Fetches everything (idempotent - safe to re-run)
python scraper/main.py --fetch
```

### Automated Daily Updates

Set up a cron job to automatically archive new posts:

**macOS/Linux:**
```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 2 AM)
0 2 * * * cd /path/to/linkedin-post-archiver && source venv/bin/activate && python scraper/main.py --fetch >> logs/cron.log 2>&1
```

**Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 2:00 AM
4. Action: Start a program
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `scraper/main.py --fetch`
   - Start in: `C:\path\to\linkedin-post-archiver`

### Rate Limit Monitoring

The script shows request count after completion:
```
Archival Complete!
Total posts: 150
Successfully archived: 150
API requests made: 3
Media files downloaded: 45
```

If you hit rate limits (rare), wait 24 hours and re-run - the script will resume where it left off.

## Troubleshooting

### Authentication Failed

- Verify your Client ID and Client Secret in `.env`
- Check that the redirect URI matches: `http://localhost:8080/callback`
- Ensure port 8080 is not in use by another application

### No Posts Fetched

- Check logs in `logs/scraper.log`
- Verify your LinkedIn app has the required permissions
- Try re-authenticating with `--reauth`

### Media Download Failed

- Some media URLs may be temporary or expired
- Check your internet connection
- Large videos may fail due to size limits (adjust in config)

### Rate Limiting

If you see rate limit warnings:
- The tool automatically handles this with exponential backoff
- Increase `rate_limit_delay` in config if needed
- LinkedIn API has daily request limits

## Important Notes

### LinkedIn API Limitations

- **Rate Limits**: LinkedIn has rate limits on API requests (~500/day for developer apps)
- **Data Access**: You can only access your own posts, not others'
- **Historical Data**: Access depends on when you created your developer app
- **Media URLs**: Some media URLs may be temporary and should be downloaded immediately

### Privacy & Security

- Never commit your `.env` file with credentials
- The `.gitignore` is configured to exclude sensitive files
- Access tokens are cached in `cache/token.json` (git-ignored)
- Media files are excluded from git by default

### Storage Considerations

- Videos can be large (500MB+ each)
- Consider available disk space before archiving
- You can disable video downloads in `config.yaml`

## Development

### Project Structure

```
scraper/
├── __init__.py              # Package initialization
├── main.py                  # Main entry point
├── auth.py                  # OAuth 2.0 authentication
├── linkedin_client.py       # LinkedIn API wrapper
├── post_fetcher.py          # Post parsing logic
├── media_downloader.py      # Media download handling
├── markdown_generator.py    # Markdown generation
├── models.py                # Data models
└── utils.py                 # Helper functions
```

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-cov

# Run tests (when available)
pytest tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Note:** This tool is for personal use to archive your own content. LinkedIn's Terms of Service apply to API usage.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Suggesting features
- Submitting pull requests

## Support

For issues or questions:
1. Check `logs/scraper.log` for detailed error messages
2. Review LinkedIn API documentation: https://docs.microsoft.com/en-us/linkedin/
3. Search [existing issues](https://github.com/YOUR_USERNAME/linkedin-post-archiver/issues)
4. Open a new issue with detailed information

## Roadmap

Future improvements:
- [ ] Incremental updates (fetch only new posts)
- [ ] Comment thread archiving
- [ ] Export to HTML/PDF formats
- [ ] Search functionality
- [ ] Engagement metrics tracking

---

**Note**: This tool is designed for personal archiving of your own content. Respect LinkedIn's Terms of Service and API usage policies.
