---
argument-hint: [topic, thesis, or source URLs]
description: Write a long-form article for the website, with image prompts
allowed-tools: AskUserQuestion, WebFetch, WebSearch, Write, Read, Glob, Edit, Bash
---

Write a long-form article based on the user's input, following the established article style.

## Arguments

`$ARGUMENTS` contains free text: URLs, notes, topics, theses, or any combination. Parse it to separate:
- **URLs**: anything starting with `http://` or `https://`
- **Text notes**: everything else (topic, thesis, angle, raw material)

If `$ARGUMENTS` is empty, use AskUserQuestion to ask what the article is about.

## Step 1: Gather source material

1. Read `article_style.md` from the project root. This is the long-form style supplement.
2. Read `writing_style.md` from the project root. This is the primary style authority for voice, tone, and language rules.
3. Read `profile.md` from the project root. This provides vocabulary, topic expertise, and voice patterns.
4. Read `taste.md` from the project root. This is the visual taste profile for image prompts.
5. If URLs were found in the arguments:
   - Fetch each URL using WebFetch
   - Extract: headline, author, main argument, notable quotes, data points
6. Summarize all source material in a brief internal note (do not show to user yet).

## Step 2: Research

If the topic would benefit from supporting data or citations:
1. Use WebSearch to find 3-5 relevant sources: industry reports, academic studies, data points, expert opinions
2. Fetch the most promising results with WebFetch
3. Extract key findings, statistics, and quotable insights
4. Note the sources for inline citation in the article

Articles should be grounded in evidence where possible. The voice is practitioner-first, but data strengthens the argument.

## Step 3: Propose angles and structure

Based on the source material, text notes, and research, propose **2-3 angles** for the article. Each angle should:
- Be 2-3 sentences describing the thesis and approach
- Map to recurring topics from profile.md
- Represent genuinely different perspectives

Use AskUserQuestion to present the angles.

After the user picks an angle, propose a **section-by-section outline**:
- Title + subtitle
- 4-7 section headers with 1-sentence description each
- Expected length range (e.g., "~2,000 words, 8 min read")

Present the outline with AskUserQuestion. Options:
- "Looks good" — proceed to draft
- "Needs changes" — user provides feedback on structure
- "Try different angles" — go back to angle selection

Iterate until the outline is approved.

## Step 4: Draft the article

### Style hierarchy

1. `writing_style.md` — primary authority for voice, tone, language rules
2. `article_style.md` — long-form-specific patterns (section headers, citations, pacing, opening/closing patterns)
3. `profile.md` — vocabulary, rhetorical devices, topic-specific angles

Where any conflict exists, writing_style.md wins. article_style.md supplements, never overrides.

### Writing rules

Follow `article_style.md` for:
- Opening pattern: scene, thesis, or provocative question (never a generic framing)
- Section headers: short, thematic, questions or declarations (never "Introduction" / "Conclusion")
- Closing pattern: return to the opening, reframe with everything the reader now knows
- Citations: inline, conversational, 3-5 sources
- Pacing: let sections breathe, alternate analytical paragraphs with punchy emphasis beats

Follow `writing_style.md` for:
- Zero emojis
- No em dashes, no hyperbole, no corporate speak
- Plain words over fancy ones
- Trust the reader

Follow `profile.md` for:
- Vocabulary: use the "Use naturally" words, avoid the "Avoid" words
- Rhetorical devices: "both things are probably true", implicit comparison, explanatory cascade
- Topic-specific angles and framing

### Show draft and iterate

Output the full draft as regular text between horizontal rules (`---`). Then use AskUserQuestion with options:
- "Looks good" — proceed to image prompts
- "Needs changes" — user provides feedback
- "Rewrite section [N]" — user specifies which section needs work
- "Scrap and start over" — back to Step 3

Continue iterating until approved.

## Step 5: Decide whether the article needs images or charts

Every article visual is either a **chart** (rendered from data via `charts/`) or an **AI-generated image** (prompt for a separate diffusion pass). Choose per visual.

**Charts beat images when the visual communicates concrete structure or data:**
- A number-heavy comparison (funnel %, before/after, two headline stats)
- A 2×2 framing, quadrant, or ranking
- A trend over time (single or multi-series)
- A pipeline, workflow, or architecture (horizontal flow, vertical flow, stacked tracks)
- A timeline of events (by time of day or by date)

**AI images beat charts when the visual is:**
- A hero / mood setter
- An abstract metaphor with no structured data
- A scene or illustration

**Always generate a hero.** Hero is nearly always an AI image (it's the mood piece), but if the article's thesis is a single chart-like shape (e.g. one stat contrast that carries the whole piece), the chart can be the hero.

### Available chart templates

Before proposing a section visual, scan `charts/templates/` and consider if any fit:

- `bar` — descending / ascending categorical comparison, funnel
- `stat-compare` — two big numbers with an arrow (access vs maturity, before vs after)
- `quadrant` — 2×2 framing with labeled regions
- `line` — multi-series trend over time
- `flow` — horizontal or vertical pipeline with optional parallel tracks, gate labels, highlighted stage (set `orientation: "vertical"` for narrow columns / vertical reading)
- `timeline` — stacked tracks with point or span events along a time-of-day or date axis

If a planned section visual maps to one of these, generate a **chart spec** (see Step 5b).

**If the visual doesn't fit any existing template:** describe the diagram you want, and surface it to the user with AskUserQuestion:
- Options: "Add a new `<name>` template to `charts/`" · "Fall back to AI image prompt" · "Drop the visual"
- Include a one-paragraph sketch of the template (geometry, data shape, sample JSON). Do not silently fall back to an AI image without asking — the whole point of `charts/` is to grow as patterns repeat.

**Skip the visual when:**
- The article is mostly personal narrative
- The diagram would feel forced

## Step 5b: Generate chart specs and image prompts

For each visual decided in Step 5, produce **either** a chart spec (if it maps to a template) **or** an image prompt (if it's mood/metaphor).

### Chart specs

For each chart, save a JSON spec to `articles/YYYY/MM/YYYY-MM-DD-slug/media/<name>.json`. The JSON must set `template` to the template name and match the shape documented in `charts/README.md`.

Default dimensions when rendering (documented in `charts/README.md`):
- `flow` horizontal — `--width 1800 --height 620`
- `flow` vertical — `--width 1200 --height 900`
- `timeline` — `--width 1800 --height 620` (shorter if few tracks)
- `bar` / `line` — `--width 1600 --height 900`
- `stat-compare` — `--width 1600 --height 900`
- `quadrant` — `--width 1600 --height 900`

After saving each spec, render it:

```bash
node charts/render.mjs \
  --template <name> \
  --data articles/YYYY/MM/YYYY-MM-DD-slug/media/<name>.json \
  --output articles/YYYY/MM/YYYY-MM-DD-slug/media/<name>.webp \
  --width <w> --height <h>
```

Reference the rendered `.webp` in the article body as a standard markdown image.

**If a section visual has no matching template**, do NOT silently fall back. Surface it to the user with AskUserQuestion:
- "Add a new `<name>` template to `charts/`" — describe the proposed geometry, data shape, and sample JSON in the question body
- "Fall back to an AI image prompt" — generate a prompt instead
- "Drop this visual" — skip the section image entirely

### AI image prompts

Generate prompts following the visual taste profile from `taste.md`.

### Website image specs

All article images display on the site at **720px content width** (2x retina = 1440px). Thumbnails are cropped via `object-fit: cover` at various ratios (16:10 spotlight, full-width × 220px archive cards). To work everywhere, **keep subjects centered with breathing room for cropping**.

| Image type | Dimensions | Ratio | Format | Usage |
|-----------|-----------|-------|--------|-------|
| Hero image | **1440×900px** | 16:10 | PNG or JPG | Article page hero, archive card thumbnail, homepage spotlight |
| Section diagram | **1440×900px** | 16:10 | PNG | Inline content image, sharp text |
| Square diagram | **1200×1200px** | 1:1 | PNG | When content demands square (flowcharts, comparisons) |

### Hero image prompt
- Should capture the article's core tension or theme
- Dimensions: **1440×900px (16:10)** — 2x retina for 720px display, crops cleanly for all thumbnail contexts
- **Heroes are NOT bound by the site color scheme.** Unlike inline diagrams/charts (which follow the dark navy + teal palette from taste.md), the hero is the mood piece for the article. Use whatever palette, medium, and style best serves the concept — painterly editorial illustrations, warm tones, photography-like scenes, whatever fits. Think NYT Magazine / Wired long-read opener, not infographic.
- Inline section images (diagrams, comparisons, schematics) DO follow taste.md / the site palette — only the hero is free.

### Section image prompts (1-2, if needed)
- Diagrams, infographics, or conceptual illustrations
- Dimensions: **1440×900px (16:10)** for illustrations, **1200×1200px (1:1)** for square diagrams
- Reference the specific section content they accompany

### Prompt format
Write each prompt as 2-4 sentences covering:
- Subject and composition (**keep subject centered** — thumbnails crop edges)
- Visual style and mood
- Color palette
- What text (if any) should appear
- What to avoid (reference taste.md anti-patterns)

End each prompt with: `Format: [width]x[height]px ([aspect ratio]) · [file type]`

### Show prompts and iterate
Present both chart specs and image prompts together with AskUserQuestion:
- "All good" — proceed to save
- "Revise" — user provides feedback on either
- "Skip images" — save without images or charts

## Step 6: Save the article

1. Generate a slug from the title: key words, lowercased, hyphenated, max 60 chars
2. Create the directory: `articles/YYYY/MM/YYYY-MM-DD-slug/`
3. Save `article.md` with this format:

```markdown
---
title: "[Article title]"
subtitle: "[Subtitle]"
date: [today's date, YYYY-MM-DD]
tags: [tag1, tag2, tag3]
medium_url:
hero_image:
reading_time: [computed from word count]
draft: true
---

[Full article content as approved]
```

4. Chart specs (`media/<name>.json`) and rendered `.webp` files are already saved from Step 5b. Include inline references (`![caption](media/<name>.webp)`) in the article body at the relevant sections.
5. If AI image prompts were generated, save them as `articles/YYYY/MM/YYYY-MM-DD-slug/image-prompts.md`:

```markdown
# Image Prompts

## Hero Image
[prompt]

## Section: [section name]
[prompt]
```

**Notes:**
- `medium_url` is left empty — fill in after publishing to Medium
- `hero_image` is left empty — fill in after generating and saving the image
- `reading_time` is computed: word count / 230, rounded to nearest minute
- `draft: true` is set by default — new articles always start as drafts. They build at `/articles/drafts/<stable-token>/` only, not listed on home, archive, topics, RSS, or sitemap. Page is served with `noindex, nofollow` and the drafts tree is disallowed in `robots.txt`. Use this URL to share review links. To publish, run `/publish <slug-or-path>` (or remove the `draft` line manually and update the date).

## Step 7: Wrap up

Tell the user:
- The article has been saved to `articles/[path]/article.md`
- Image prompts saved to `articles/[path]/image-prompts.md` (if generated)
- Remind: "To rebuild the site with this article: `python web/build.py`"
- Remind: "When ready to promote on LinkedIn, run `/write [article-url]`"
- Remind: "After publishing to Medium, update `medium_url` in the article frontmatter"
- Remind: "After generating images, save hero to `media/` folder and update `hero_image` in frontmatter"
