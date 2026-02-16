# Quick Start Guide

Get your LinkedIn posts archived in 5 minutes!

## Prerequisites

✅ Python 3.9 or higher
✅ LinkedIn Developer App (instructions below)

---

## Step 1: Create LinkedIn Developer App (5 minutes)

1. **Go to LinkedIn Developers**
   - Visit: https://www.linkedin.com/developers/apps
   - Click **"Create app"**

2. **Fill in App Details**
   - App name: `LinkedIn Post Archiver`
   - LinkedIn Page: Select any page (create one if needed)
   - App logo: Upload any image
   - Click **"Create app"**

3. **Configure OAuth**
   - Go to **"Auth"** tab
   - Add redirect URL: `http://localhost:8080/callback`
   - Click **"Update"**

4. **Request Products**
   - Go to **"Products"** tab
   - Request: **"Sign In with LinkedIn using OpenID Connect"**
   - Request: **"Share on LinkedIn"**

5. **Get Credentials**
   - Go to **"Auth"** tab
   - Copy your **Client ID**
   - Copy your **Client Secret**

---

## Step 2: Install & Configure

```bash
# Navigate to project directory
cd linkedin-post-archiver  # Or wherever you cloned the project

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

**Edit `.env` file:**

```bash
# Open .env in your text editor
nano .env  # or use any text editor
```

**Add your credentials:**

```env
LINKEDIN_CLIENT_ID=your_actual_client_id_here
LINKEDIN_CLIENT_SECRET=your_actual_client_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:8080/callback
```

Save and close.

---

## Step 3: Verify Setup

```bash
python verify_setup.py
```

If everything is ✓ green, you're ready!

---

## Step 4: Authenticate

```bash
python scraper/main.py --auth
```

**What happens:**
1. Browser opens to LinkedIn
2. Click **"Allow"** to authorize
3. You'll see "Authentication Successful!"
4. Close browser, return to terminal

---

## Step 5: Archive Your Posts

```bash
python scraper/main.py --fetch
```

**What happens:**
1. Fetches all your LinkedIn posts
2. Downloads images and videos
3. Generates clean markdown files
4. Saves to `posts/` directory

**Progress shows:**
```
Fetching posts from LinkedIn...
Retrieved 50 posts
Archiving posts: 100%|██████████| 50/50

Archival Complete!
Total posts: 50
Successfully archived: 50
Media files downloaded: 25
```

---

## Step 6: View Your Archive

```bash
# Open the posts directory
open posts/  # macOS
# OR
explorer posts  # Windows
# OR
xdg-open posts  # Linux

# View the index
cat posts/INDEX.md
```

**Directory structure:**
```
posts/
├── 2024/
│   ├── 01/
│   │   └── 2024-01-15-my-first-post/
│   │       ├── post.md
│   │       └── media/
│   │           └── image-1.jpg
│   └── 02/
└── INDEX.md
```

---

## Common Commands

### Fetch only recent posts
```bash
python scraper/main.py --limit 10
```

### Re-authenticate
```bash
python scraper/main.py --reauth --fetch
```

### Update archive (fetch new posts)
```bash
python scraper/main.py --fetch
```
(Skips already archived posts)

---

## Troubleshooting

### "Authentication failed"
- Check your Client ID and Secret in `.env`
- Verify redirect URI: `http://localhost:8080/callback`
- Make sure port 8080 is available

### "No posts found"
- Verify your LinkedIn app has required permissions
- Try re-authenticating: `--reauth`

### "Rate limit exceeded"
- Wait a few minutes and try again
- LinkedIn has API rate limits (~500 requests/day)

---

## Next Steps

✅ **Backup your archive**
   - Copy `posts/` directory to cloud storage
   - Commit markdown files to git (media excluded by default)

✅ **Customize settings**
   - Edit `config/config.yaml` for advanced options

✅ **Schedule regular archives**
   - Run monthly to keep archive updated

---

## Need Help?

📖 **Full documentation:** See `README.md`
📋 **Check logs:** `logs/scraper.log`
🐛 **Issues:** Check GitHub issues or create new one

---

**That's it!** Your LinkedIn posts are now safely archived. 🎉
