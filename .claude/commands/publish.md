---
argument-hint: [article slug, path, or leave empty to pick]
description: Promote a draft article to published — remove draft flag, update date, generate Substack paste artifact
allowed-tools: AskUserQuestion, Glob, Read, Edit, Write, Bash
---

Promote a draft article to published state by removing `draft: true` from frontmatter, updating `date:` to today, and generating the Substack paste-in artifact.

## Step 1: Locate the draft

If `$ARGUMENTS` is non-empty:
- Treat it as a slug fragment or path. Use Glob with `articles/**/*$ARGUMENTS*/article.md` to find matches.
- If multiple matches, use AskUserQuestion to disambiguate.

If `$ARGUMENTS` is empty:
- Glob `articles/**/article.md`, read each frontmatter, collect those with `draft: true`.
- If zero drafts, tell the user and stop.
- If one draft, use it.
- If multiple, use AskUserQuestion listing each by title + date.

## Step 2: Update frontmatter

Read today's date with `date +%Y-%m-%d`.

Edit the article.md:
- Remove the `draft: true` line entirely.
- Replace the `date:` value with today's date.

Leave `title`, `subtitle`, `tags`, `medium_url`, `hero_image`, `reading_time` untouched.

## Step 3: Rename directory and file paths to match new date (if date changed)

Articles live at `articles/YYYY/MM/YYYY-MM-DD-slug/article.md`. If the new date differs from the old one, the directory path needs to match:

1. Compute new path: `articles/<new-YYYY>/<new-MM>/<new-YYYY-MM-DD>-<slug>/`
2. If different from current path, `mkdir -p` the new parent and `git mv` the directory so history is preserved.
3. If the parent month/year directory is now empty, remove it.

The slug portion (everything after the date prefix) stays the same.

## Step 4: Generate Substack paste artifact

Substack is a distribution surface for the article — email delivery + discovery network — with the article's canonical home on the user's site. Substack has no public API for publishing, so this step produces a paste-ready file the user can drop into Substack's editor in ~2 minutes.

Generate this only at publish time (not at draft creation) to save tokens during the draft loop.

Save to `articles/<new-path>/substack-paste.md`. The file has two parts: a posting checklist and the article body reformatted for Substack paste.

### Preparation

1. Read the published `article.md` (post-Step-3 path). Extract from frontmatter:
   - `title`, `subtitle`, `tags`, `hero_image`
2. Read `SITE_URL` from `.env` — fall back to `yoursite.com` if missing.
3. Scan the article body for inline images: `![caption](media/filename.ext)`. Collect each filename for the checklist.
4. Transform the body for paste: replace every `![caption](media/filename.ext)` with `[IMAGE: caption — upload media/filename.ext here]`. This makes missed images impossible to overlook since local paths don't resolve in Substack.

### Template

```markdown
# Substack paste-in — [article title]

## Posting checklist (do these in Substack's editor)

1. **Title:** [article title from frontmatter]
2. **Subtitle:** [article subtitle from frontmatter]
3. **Canonical URL** (Post settings → SEO → Canonical URL): `{SITE_URL}/articles/YYYY/MM/slug/` — this keeps SEO pointed at your site, not Substack.
4. **Hero image:** upload `media/[hero-image-filename]` at the top of the post (Substack strips local paths on paste; you have to upload through their UI).
5. **Inline images:** re-upload any of these as you reach them in the body:
   - `media/[image-1]`
   - `media/[image-2]`
6. **Tags:** [comma-separated tags from frontmatter]
7. At the end of the post, add this canonical-pointer line so readers who found you on Substack know where the piece actually lives:

   > Originally published at [yoursite.com/articles/YYYY/MM/slug](SITE_URL/articles/YYYY/MM/slug/).

## Body to paste

Everything below the `---` line is the article body. Select all and paste into Substack's editor after you've set title and subtitle.

---

[TRANSFORMED ARTICLE BODY — everything below the frontmatter, with `![caption](media/*)` replaced by `[IMAGE: caption — upload media/* here]`]

---

## After posting

- Grab the Substack post URL.
- Add a `substack_url:` field to the article frontmatter (alongside `medium_url`).
- Optional: share the Substack URL in a Notes post on Substack itself for an extra discovery pass.
```

**Do NOT modify `article.md`** — Substack is downstream; the site article is canonical.

## Step 5: Confirm

Tell the user:
- Article title + new path
- Old draft URL is now dead; new public URL will be `/articles/YYYY/MM/slug/` after rebuild
- Substack paste-in saved to `articles/<path>/substack-paste.md`
- Remind: "Rebuild with `python web/build.py` (or `bash pipeline.sh --skip-scrape` to deploy)"
- Remind: "After publishing to Substack, grab the URL and add `substack_url:` to the article frontmatter"
