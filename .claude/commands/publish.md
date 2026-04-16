---
argument-hint: [article slug, path, or leave empty to pick]
description: Promote a draft article to published — remove draft flag and update date to today
allowed-tools: AskUserQuestion, Glob, Read, Edit, Bash
---

Promote a draft article to published state by removing `draft: true` from frontmatter and updating `date:` to today.

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

## Step 4: Confirm

Tell the user:
- Article title + new path
- Old draft URL is now dead; new public URL will be `/articles/YYYY/MM/slug/` after rebuild
- Remind: "Rebuild with `python web/build.py` (or `bash pipeline.sh --skip-scrape` to deploy)"
