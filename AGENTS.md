# Agent instructions (Cursor / Grok Bot)

Writing and content agents for João Gonçalves should treat this repo as the source of truth for voice, archive layout, and publish workflows.

Claude Code users: keep using [`CLAUDE.md`](CLAUDE.md) and the skills under [`.claude/commands/`](.claude/commands/). This file is additive for Cursor / Grok agents — it does not replace Claude Code.

## Repo

- GitHub: `https://github.com/joaofogoncalves/memory`
- Prefer the GitHub connector / API for reads and PR-based writes. Do not invent a parallel style guide outside this repo.

## Style hierarchy (mandatory)

1. [`style/writing_style.md`](style/writing_style.md) — primary authority for voice, tone, language, length, anti-patterns
2. [`style/article_style.md`](style/article_style.md) — long-form supplement (articles only)
3. [`style/profile.md`](style/profile.md) — vocabulary and topic patterns; defer to `writing_style.md` on conflict
4. [`style/taste.md`](style/taste.md) — visuals and image prompts
5. [`style/pitch_style.md`](style/pitch_style.md) — self-positioning / about-your-work only

Always re-read these from the repo before drafting. Do not cache a private paraphrase as policy.

## Workflows

Do **not** re-implement the full procedures here. Open and follow the matching skill file end-to-end:

| Task | Follow |
|------|--------|
| Short-form post (site + LinkedIn / X / Substack Note) | [`.claude/commands/post.md`](.claude/commands/post.md) |
| Long-form article | [`.claude/commands/article.md`](.claude/commands/article.md) |
| Strip AI tells | [`.claude/commands/humanize.md`](.claude/commands/humanize.md) |
| Promote draft → published | [`.claude/commands/publish.md`](.claude/commands/publish.md) |
| Scrape + curate recent posts | [`.claude/commands/sync.md`](.claude/commands/sync.md) |
| Pitch / bio variants | [`.claude/commands/pitch.md`](.claude/commands/pitch.md) |
| Voice / taste refresh | [`.claude/commands/profile.md`](.claude/commands/profile.md), [`.claude/commands/taste.md`](.claude/commands/taste.md) |

Where a skill says `AskUserQuestion`, use your host’s question UI (e.g. a choice widget). Where it says `WebFetch` / `WebSearch` / `Write` / `Read`, use the equivalent tools available to you.

## Save locations

- Posts: `content/posts/YYYY/MM/DD-slug/` (`post.md`, platform variants, optional `media/`)
- Articles: `content/articles/YYYY/MM/DD-slug/` (`article.md` with `draft: true` by default, optional `media/`, prompts)

Preserve frontmatter conventions from the skill files (`authored: true` on posts, draft routing for articles, empty permalink fields until after manual posting).

## Standing rules

1. Propose **2–3 angles** before drafting; wait for João’s pick.
2. Show the **full draft in chat** before asking for approval.
3. Run the full **humanize** skill after approval and **before** platform variants or publish.
4. Never create, overwrite, or force-push authored content without explicit approval for the mutation.
5. Zero emojis by default; no em dashes; no corporate LinkedIn-speak; bias short.
6. Visuals default **on** for posts unless you can state a clear reason to skip (see `post.md`).
7. LinkedIn: no external URLs in the post body. Put the source/article link in the **first comment**, posted immediately after the main post (see `.claude/commands/post.md`).

## Site pipeline (when publishing)

After content is approved and saved: `bash scripts/pipeline.sh --skip-scrape` (or the steps documented in `README.md`) to rebuild/deploy. Do not run scrape/deploy unless João asks.

## Collaboration

Chief of Staff may route writing briefs here. Speak as João’s writing partner. Pull him in for angle choice, draft approval, and publish decisions only.
