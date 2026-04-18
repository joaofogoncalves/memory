---
argument-hint: (no args) — always scrapes with --limit 10
description: Scrape recent LinkedIn posts to refresh engagement counts and catch any posts made outside the /post workflow
allowed-tools: AskUserQuestion, Bash, Glob, Grep, Read
---

Scrape the 10 most recent LinkedIn posts and reconcile them with the local archive.

**In the authored-first model**, the site is canonical for posts. You write with `/post`, which saves to `posts/YYYY/MM/YYYY-MM-DD-slug/post.md` and generates paste-ready LinkedIn and X variants that you post natively. The scraper's job here is two-fold:

1. **Refresh engagement** — for every scraped post that matches a local post (by `post_url` or by content fingerprint within 14 days), update `reactions:` and `comments:` in the frontmatter. Body is never touched. This is handled automatically by the scraper.
2. **Catch stragglers** — anything you posted manually on LinkedIn without running `/post` gets picked up as a genuinely new post. Most of the time this catches noise (quick replies, milestones, follow-thanks) rather than substantive content. That's what this skill curates.

Self-article-promo filtering (the old main job of this skill) is no longer needed — in the new model, when you promote an article on LinkedIn the promo is authored via `/post` and already exists as a canonical site post. Scraping it just updates its engagement.

## Step 1: Snapshot existing posts

Before scraping, capture the current set of post directories so you can diff new additions after the run:

```bash
find posts -type d -name "2*" -mindepth 3 -maxdepth 3 | sort > /tmp/sync_before.txt
wc -l < /tmp/sync_before.txt
```

Report the count to the user: "Found N archived posts. Scraping the last 10 from LinkedIn..."

## Step 2: Run the scraper

```bash
python -m scraper.main --crawl --limit 10
```

This uses `LINKEDIN_PROFILE_URL` from `.env` automatically. The scraper may take a minute and requires a valid browser session (from a prior `--browser-login`). Capture stdout so you can report the engagement-update count to the user in Step 5.

If the scraper fails (login expired, network error, etc.), surface the error and stop — don't fake curation on stale data.

## Step 3: Resolve shortened links on new posts

LinkedIn posts often contain `lnkd.in/...` shortened URLs. Resolve them in-place:

```bash
python web/resolve_links.py
```

This is idempotent and only touches `post.md` files that still have unresolved links.

## Step 4: Identify genuinely-new posts

Compute the diff:

```bash
find posts -type d -name "2*" -mindepth 3 -maxdepth 3 | sort > /tmp/sync_after.txt
comm -13 /tmp/sync_before.txt /tmp/sync_after.txt
```

The output is the list of new post directories. Anything that matched an existing post (via URL or fingerprint) was merged and will NOT appear here — that's the scraper's job, not yours.

If zero new posts, skip to Step 6 and report the engagement-update count to the user.

For each new post, Read the full `post.md` file. Extract:
- Frontmatter: `date`, `post_type`
- Body text (between `# Date` heading and `---` footer)

Parallelize the Read calls where possible.

## Step 5: Flag low-value noise

For each genuinely-new post, decide whether to flag it for removal. The new model has a much narrower scope here — authored content doesn't need flagging, so you're only looking at LinkedIn activity that happened outside the `/post` workflow.

### Low-value noise (flag for drop)

Flag if any of these apply:

- **Milestone posts**: "1,000 followers!", "Thanks for the follows", "Celebrating X years"
- **Empty / placeholder posts**: body < 50 chars, or obviously a draft/test
- **Pure reposts without commentary**: the scraper already filters these, but double-check — a body that's just a repost header with no meaningful user text is noise
- **One-line reactions**: "Great point!", "Love this", "Agreed" — short engagement comments that happen to be standalone posts

Reason format: `Low-value: <short description>` (e.g., "Low-value: milestone post", "Low-value: one-line reaction")

### Keep by default

- Original takes with substance (even if brief)
- Real reactions to external events, tweets, articles — anything with a point of view
- Reposts WITH meaningful user commentary (actual paragraphs of your own thinking)
- Book/article recommendations that aren't your own work

### When in doubt, keep

Unlike the old flow, the bar for dropping is now higher — these are posts you actually wrote, just informally. Only flag content that clearly isn't worth preserving. Flag with a reason, the user confirms in Step 6, and the default should skew toward keeping.

## Step 6: Present candidates and confirm

### If there are engagement updates (most common case)

Parse the scraper's stdout for the "Engagement updated on existing" stat. Report it:

```
Scraped 10 posts. Engagement updated on N existing posts (reactions + comments refreshed in-place).

No new posts to curate — everything matched an existing authored or scraped post.
```

Suggest a rebuild + deploy and stop.

### If there are genuinely-new posts

Print a summary block, then ask for confirmation.

```
Scraped 10 posts. Engagement updated on N existing posts.
Found M genuinely-new posts since last sync:

FLAGGED FOR DROP (Y):
  • 2026-04-10-thanks-for-the-follows
    Low-value: milestone post

KEEP (Z):
  • 2026-04-13-this-take-from-yegor-bugayenko-is-directionally-r — original commentary
  ...
```

### Confirmation

- If **0 flagged**: tell the user nothing to drop, suggest rebuild, stop.
- If **1-4 flagged**: use AskUserQuestion with `multiSelect: true`, one option per flagged post (label = short slug, description = reason). User checks the ones to drop.
- If **5+ flagged**: first ask "Drop all X flagged posts?" with options `["Drop all", "Review in batches", "Keep all"]`. If "Review in batches", loop through flagged posts 4 at a time with multiSelect questions.

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
- Engagement updated on N existing posts
- K genuinely-new posts found; J dropped as noise, (K-J) kept
- Next step: "Rebuild the site with `python web/build.py` — or run `bash pipeline.sh --skip-scrape` to rebuild and deploy."

## Notes on the shifted model

The old sync skill had to detect self-promo posts (LinkedIn posts that only existed to link to your own article). That's no longer a thing — in the authored-first flow, those posts are either intentional short-form takes (authored via `/post`, saved to the site as canonical) or they don't exist at all.

The new job here is much simpler: let the scraper do its merge work silently, and curate only the rare posts that slipped in outside `/post`. Most runs will find nothing to curate and only report engagement updates — that's the expected steady state.
