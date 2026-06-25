---
argument-hint: [article slug, path, or leave empty to pick]
description: Promote a draft article to published — remove draft flag, update date, rename directory to match
allowed-tools: AskUserQuestion, Glob, Read, Edit, Bash
---

Promote a draft article to published state by removing `draft: true` from frontmatter, updating `date:` to today, and renaming the directory to match the new date.

## Step 1: Locate the draft

If `$ARGUMENTS` is non-empty:
- Treat it as a slug fragment or path. Use Glob with `content/articles/**/*$ARGUMENTS*/article.md` to find matches.
- If multiple matches, use AskUserQuestion to disambiguate.

If `$ARGUMENTS` is empty:
- Glob `content/articles/**/article.md`, read each frontmatter, collect those with `draft: true`.
- If zero drafts, tell the user and stop.
- If one draft, use it.
- If multiple, use AskUserQuestion listing each by title + date.

## Step 2: Update frontmatter

Read today's date with `date +%Y-%m-%d`.

Edit the article.md:
- Remove the `draft: true` line entirely.
- Replace the `date:` value with today's date.

Leave `title`, `subtitle`, `tags`, `substack_url`, `hero_image`, `reading_time` untouched.

## Step 3: Rename directory and file paths to match new date (if date changed)

Articles live at `content/articles/YYYY/MM/DD-slug/article.md` — `YYYY/MM` come from the frontmatter `date:`, and the directory name is the zero-padded **day** plus the slug (e.g. `content/articles/2026/06/11-rent-the-loop-build-the-moat/`). `build.py` derives year/month/date from frontmatter and uses the directory name verbatim as the URL slug, so the path only needs to carry the day. If the new date differs from the old one, the directory name needs to match:

1. Compute new path: `content/articles/<new-YYYY>/<new-MM>/<new-DD>-<slug>/` — zero-pad `<new-DD>` (e.g. `08`, `11`) so directories sort chronologically.
2. If different from current path, `mkdir -p` the new parent and `git mv` the directory so history is preserved.
3. If the parent month/year directory is now empty, remove it.

The slug portion (everything after the `DD-` prefix) stays the same.

No Substack paste file is generated. Substack's Import tool pulls a published post straight from its canonical URL — body, formatting, and images — so a hand-formatted paste artifact is redundant once the site is deployed. The cross-post happens after the rebuild, driven by the live URL (see the confirm step).

**Do NOT modify `article.md`** for any downstream surface — the site article is canonical; Substack is downstream.

## Step 4: Confirm

Compute the live URL: read `SITE_URL` from `.env` (fall back to `yoursite.com`), and join it with the new public path `/articles/YYYY/MM/slug/`.

Tell the user:
- Article title + new path
- Old draft URL is now dead; new public URL will be `{SITE_URL}/articles/YYYY/MM/slug/` after rebuild
- Remind: "Rebuild and deploy first: `bash scripts/pipeline.sh --skip-scrape` (or `python web/build.py` to build only). Substack's import reads the live page, so it has to be deployed before you import."
- Remind: "To cross-post to Substack: use its **Import** tool (New post → Import) and point it at the live URL `{SITE_URL}/articles/YYYY/MM/slug/`. It pulls in the body, formatting, and images. Then set the post's canonical URL (Settings → SEO) to that same URL so SEO stays pointed at your site."
- Remind: "After publishing to Substack, grab the URL and add `substack_url:` to the article frontmatter."
