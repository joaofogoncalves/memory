---
argument-hint: (no args) — always scrapes with --limit 10
description: Scrape recent LinkedIn posts and curate — drop promo-posts for your own articles and other low-value noise
allowed-tools: AskUserQuestion, Bash, Glob, Grep, Read
---

Scrape the 10 most recent LinkedIn posts with the browser crawler, then apply subjective judgment to remove posts that shouldn't be in the archive. The canonical case: you published an article, wrote a LinkedIn post to promote it, and both got scraped — the article itself is the real content, the promo post is noise. Cleaning these up before they propagate to the website and RSS feed is the job.

## Step 1: Snapshot existing posts

Before scraping, capture the current set of post directories so you can diff later:

```bash
find posts -type d -name "2*" -mindepth 3 -maxdepth 3 | sort > /tmp/sync_before.txt
wc -l < /tmp/sync_before.txt
```

Report the count to the user: "Found N archived posts. Scraping the last 10 from LinkedIn..."

## Step 2: Run the scraper

```bash
python -m scraper.main --crawl --limit 10
```

This uses `LINKEDIN_PROFILE_URL` from `.env` automatically. The scraper may take a minute and requires a valid browser session (from a prior `--browser-login`).

If the scraper fails (login expired, network error, etc.), surface the error and stop — don't fake curation on stale data.

## Step 3: Resolve shortened links on new posts

LinkedIn posts often contain `lnkd.in/...` shortened URLs. Resolve them in-place so the self-promo detection in Step 4 has real destinations to inspect:

```bash
python web/resolve_links.py
```

This is idempotent and only touches `post.md` files that still have unresolved links.

## Step 4: Identify newly-added posts

Compute the diff:

```bash
find posts -type d -name "2*" -mindepth 3 -maxdepth 3 | sort > /tmp/sync_after.txt
comm -13 /tmp/sync_before.txt /tmp/sync_after.txt
```

The output is the list of new post directories. If zero new posts, tell the user "No new posts since last sync — nothing to curate." and stop.

Also gather context you'll need for judgment:

1. Read `.env` to get `SITE_URL` (the user's domain — any post linking here is self-promo).
2. Glob `articles/**/article.md`, read each frontmatter to build a list of:
   - slug (from directory name)
   - title
   - medium_url (may be empty for unpublished-to-Medium articles)
3. For each new post, Read the full `post.md` file. Extract:
   - Frontmatter: `date`, `post_type`
   - Body text (between `# Date` heading and `---` footer)
   - Any URLs in the body

Parallelize the Read calls where possible.

## Step 5: Apply judgment — flag likely drops

For each new post, decide whether to flag it for removal. Use these categories:

### Self-article promotion (highest-confidence drop)

Flag if ANY of the following is true:
- Body contains a URL matching `SITE_URL` (after stripping trailing slash)
- Body contains a URL matching any `medium_url` from the local articles list
- Body contains a URL whose path slug matches a local article slug (e.g., post links to `/articles/2026/04/every-company-is-three-things` and we have a local article with that slug)
- Body has strong promo language AND a link: phrases like "wrote about this", "full article", "published", "dig into this", "more in the article", "read the full piece"

Reason format: `Self-promo: links to articles/YYYY/MM/<slug>` (be specific about which article).

### Low-value noise

Flag if any:
- Thanks-for-follows / milestone posts ("1,000 followers!", "Thanks everyone")
- Empty or placeholder posts (body < 50 chars)
- Pure reposts with no user commentary (scraper should already filter these, but double-check — look for a body that's just a repost header with no user text above it)
- Obvious test posts

Reason format: `Low-value: <short description>` (e.g., "Low-value: milestone post")

### Keep by default

- Original takes with substance
- Reactions to external events, tweets, articles (not your own)
- Reposts WITH meaningful user commentary (actual paragraphs of your own thinking)
- Book/article recommendations that aren't your own work

### When in doubt

Flag it. Over-flagging with a good reason is fine — the user confirms in Step 6 and can keep anything you got wrong. Silently keeping noise is the failure mode to avoid.

## Step 6: Present candidates and confirm

Print a summary block to the conversation, then ask for confirmation.

### Summary format

```
Scraped X new posts since last sync.

FLAGGED FOR DROP (Y):
  • 2026-04-14-ask-any-executive-what-their-company-does-and
    Self-promo: links to articles/2026/04/every-company-is-three-things-ai-just-made-that-obvious
  • 2026-04-10-thanks-for-the-follows
    Low-value: milestone post

KEEP (Z):
  • 2026-04-13-this-take-from-yegor-bugayenko-is-directionally-r — original commentary
  • 2026-04-15-this-take-has-a-hidden-assumption-that-trust — original commentary
  ...
```

### Confirmation

- If **0 flagged**: tell the user nothing to drop, suggest rebuild, stop.
- If **1-4 flagged**: use AskUserQuestion with `multiSelect: true`, one option per flagged post (label = short slug, description = reason). User checks the ones to drop.
- If **5+ flagged**: first ask "Drop all X flagged posts?" with options `["Drop all", "Review in batches", "Keep all"]`. If "Review in batches", loop through flagged posts 4 at a time with multiSelect questions.

Always give the user a chance to override — let them add notes via the "Other" option if they want to explain a keep/drop override.

## Step 7: Delete confirmed drops

For each post the user confirmed:

```bash
rm -rf posts/YYYY/MM/<slug>/
```

Delete the whole directory (post + media). Do NOT touch:
- `site.yaml` featured_posts — the scraper regenerates this on each run
- The articles themselves — they're in `articles/`, untouched by this skill
- Any post not in the confirmed-drop list

## Step 8: Clean up temp files and confirm

```bash
rm -f /tmp/sync_before.txt /tmp/sync_after.txt
```

Tell the user:
- How many new posts were scraped
- How many were dropped (list slugs)
- How many were kept
- Next step: "Rebuild the site with `python web/build.py` — or run `bash pipeline.sh --skip-scrape` to rebuild and deploy."

## Notes on subjective judgment

The whole point of this skill is judgment the scraper itself can't do. The scraper is literal; you're the editor. When the line is fuzzy — "is this a promo or a substantive take on my own piece?" — flag it, explain your reasoning in the flag reason, and let the user decide.

Don't flag for personal opinion on quality ("this post isn't very good"). Only flag for the specific categories above: self-promo for existing local articles, and low-value noise.
