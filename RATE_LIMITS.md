# Rate Limits & Automation Guide

## Understanding LinkedIn API Rate Limits

### The Numbers

- **Daily Limit:** ~500 API requests per day (for developer apps)
- **Per Request:** Up to 50 posts
- **Total Capacity:** 500 × 50 = **25,000 posts per day**

### What This Means for You

**Most users won't hit the limit!**

| Your Post Count | Requests Needed | % of Daily Limit |
|----------------|-----------------|------------------|
| 100 posts      | 2 requests      | 0.4%            |
| 500 posts      | 10 requests     | 2%              |
| 1,000 posts    | 20 requests     | 4%              |
| 2,500 posts    | 50 requests     | 10%             |
| 10,000 posts   | 200 requests    | 40%             |

**Bottom line:** Unless you have 10,000+ posts, you can archive everything in one run.

---

## How the Script Works

### Request Tracking

The script now tracks and displays API requests:

```bash
python scraper/main.py --fetch
```

**Output:**
```
Archival Complete!
═══════════════════════════════════════════════════════
Total posts: 150
Successfully archived: 150
Failed: 0
API requests made: 3          ← This shows your usage
Media files downloaded: 45
═══════════════════════════════════════════════════════
```

### Rate Limit Protection

Built-in protections:
1. **1.5 second delay** between requests (configurable)
2. **Automatic retry** with exponential backoff on errors
3. **Warning at 400+ requests** to alert you before hitting limit
4. **Idempotent** - safe to re-run if interrupted

---

## Usage Strategies

### Strategy 1: Single Run (Recommended for Most)

**Best for:** Users with <5,000 posts

```bash
# Just run it once - fetches everything
python scraper/main.py --fetch
```

**Why this works:**
- 5,000 posts = ~100 requests (well under 500 limit)
- Takes 2-3 minutes with rate limiting
- Gets everything in one go

---

### Strategy 2: Batched Approach

**Best for:** Users with 10,000+ posts (rare)

```bash
# Day 1: First 5,000 posts
python scraper/main.py --limit 5000

# Day 2: Next 5,000 posts
python scraper/main.py --limit 10000

# Or just let it resume
python scraper/main.py --fetch
```

**How it works:**
- Script skips already-archived posts
- Each run continues where you left off
- No duplicates created

---

### Strategy 3: Automated Daily Updates (Set & Forget)

**Best for:** Keeping archive up-to-date with new posts

The script is **idempotent** - running it repeatedly:
- ✅ Skips existing posts
- ✅ Only archives new posts
- ✅ Uses minimal API requests
- ✅ No risk of duplicates

#### Setup on macOS/Linux

**Option A: Using Cron**

```bash
# Edit your crontab
crontab -e

# Add this line (runs daily at 2 AM)
0 2 * * * cd /path/to/linkedin-post-archiver && source venv/bin/activate && python scraper/main.py --fetch >> logs/cron.log 2>&1
```

**Schedule options:**
```bash
# Every day at 2 AM
0 2 * * *

# Every Monday at 9 AM
0 9 * * 1

# First day of every month at midnight
0 0 1 * *
```

**Option B: Using launchd (macOS)**

Create `~/Library/LaunchAgents/com.linkedin.archiver.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.linkedin.archiver</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/linkedin-post-archiver/venv/bin/python</string>
        <string>/path/to/linkedin-post-archiver/scraper/main.py</string>
        <string>--fetch</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/path/to/linkedin-post-archiver/logs/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/linkedin-post-archiver/logs/launchd.error.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.linkedin.archiver.plist
```

#### Setup on Windows

**Using Task Scheduler:**

1. Open **Task Scheduler** (search in Start menu)
2. Click **"Create Basic Task"**
3. Name: "LinkedIn Post Archiver"
4. Trigger: **Daily**
5. Time: **2:00 AM**
6. Action: **Start a program**
   - Program: `C:\path\to\linkedin-post-archiver\venv\Scripts\python.exe`
   - Arguments: `scraper/main.py --fetch`
   - Start in: `C:\path\to\linkedin-post-archiver`
7. Check **"Open Properties dialog when I click Finish"**
8. In Properties:
   - General tab: Check **"Run whether user is logged on or not"**
   - Settings tab: Uncheck **"Stop the task if it runs longer than"**

**PowerShell Script (Alternative):**

Create `run_archiver.ps1`:
```powershell
Set-Location "C:\path\to\linkedin-post-archiver"
& "venv\Scripts\python.exe" "scraper\main.py" "--fetch" | Out-File -Append "logs\scheduled.log"
```

Schedule this script in Task Scheduler.

---

## Monitoring Your Usage

### Check Request Count

After each run, the script shows:
```
API requests made: 15
```

### Track Over Time

Check your logs:
```bash
grep "API requests made" logs/scraper.log
```

Output:
```
2024-01-15 14:23:45 - INFO - API requests made: 15
2024-01-16 14:23:45 - INFO - API requests made: 1
2024-01-17 14:23:45 - INFO - API requests made: 2
```

### Rate Limit Warning

If you're approaching the limit:
```
⚠️  High API usage: 450/~500 daily limit
```

**What to do:**
- Wait 24 hours for reset
- Script will resume from where it stopped

---

## What If You Hit the Limit?

**Symptoms:**
- HTTP 429 errors in logs
- "Rate limited" warning messages
- Script pauses and retries

**Solution:**
1. **Wait 24 hours** - LinkedIn resets daily limits
2. **Re-run the script:**
   ```bash
   python scraper/main.py --fetch
   ```
3. Script automatically **resumes** from where it stopped (idempotent)

**The script handles this automatically:**
- Exponential backoff: 1s → 2s → 4s → 8s
- Max 3 retry attempts
- Logs the error for your review

---

## Real-World Scenarios

### Scenario 1: New User with 500 Posts

```bash
python scraper/main.py --fetch
```

**Result:**
- Requests: ~10
- Time: 1-2 minutes
- ✅ All posts archived in one run

---

### Scenario 2: Active User with 2,000 Posts

```bash
python scraper/main.py --fetch
```

**Result:**
- Requests: ~40
- Time: 5 minutes
- ✅ All posts archived in one run

---

### Scenario 3: Power User with 15,000 Posts

```bash
# First run
python scraper/main.py --fetch
# ... runs for 20 minutes, hits 450 requests
# ... gets first ~22,500 posts
```

If interrupted or hitting limits:
```bash
# Next day or after waiting
python scraper/main.py --fetch
# ... resumes, gets remaining posts
# ... only makes ~50 more requests
```

**Result:**
- Day 1: 450 requests, 22,500 posts
- Day 2: 50 requests, remaining posts
- ✅ Complete archive in 2 days

---

### Scenario 4: Daily Updates (Automated)

Set up cron job:
```bash
0 2 * * * cd /path/to/archiver && source venv/bin/activate && python scraper/main.py --fetch
```

**What happens each day:**
- Checks for new posts since last run
- Archives 0-5 new posts (typical)
- Uses 0-1 API request
- ✅ Archive stays current with near-zero effort

---

## Best Practices

### ✅ Do This

1. **Run the script fully once** to get your complete archive
2. **Set up automation** for daily/weekly updates
3. **Monitor logs** occasionally to catch issues
4. **Let it run uninterrupted** - it's designed to handle long runs
5. **Trust the idempotency** - safe to re-run anytime

### ⚠️ Avoid This

1. **Don't manually interrupt** unless necessary
2. **Don't run multiple instances** simultaneously
3. **Don't worry about exact post counts** - script handles pagination
4. **Don't manually manage batches** unless you have 20,000+ posts

---

## FAQs

### Q: How do I know how many posts I have?

**A:** Just run the script! It will tell you:
```
Found 1,247 posts to archive
```

### Q: Will running it daily waste API requests?

**A:** No! It skips existing posts and only fetches new ones:
```
# Day 1: 500 posts
API requests made: 10

# Day 2: 2 new posts
API requests made: 1

# Day 3: 0 new posts
API requests made: 0
```

### Q: What if I stop the script mid-run?

**A:** Just re-run it! It will:
- Skip already-archived posts
- Continue from where you stopped
- Not create duplicates

### Q: Can I run this on a schedule automatically?

**A:** Yes! That's the recommended approach:
- Set up cron (Linux/macOS) or Task Scheduler (Windows)
- Run daily or weekly
- Your archive stays current automatically

### Q: Does it count media downloads as API requests?

**A:** No! Only these count as API requests:
- Fetching user profile: 1 request
- Fetching each page of 50 posts: 1 request per page
- Media downloads use direct URLs (no API call)

---

## Summary

**For 99% of users:**
```bash
# Just do this once
python scraper/main.py --fetch

# Then set up automation for updates
# (optional but recommended)
```

**You won't hit rate limits unless:**
- You have 20,000+ posts (very rare)
- You run the script 10+ times per day (unnecessary)

**The script is designed to be run daily without issues!**

---

_Last updated: 2024-02-16_
