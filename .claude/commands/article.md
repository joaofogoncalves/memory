---
argument-hint: [topic, thesis, or source URLs]
description: Write a long-form article for the website, with image prompts
allowed-tools: AskUserQuestion, WebFetch, WebSearch, Write, Read, Glob, Edit
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

## Step 5: Decide whether the article needs images

Make a judgement call. Most articles benefit from at least a hero image.

**Always generate prompts for:**
- A hero image (the main visual, shown at top of article and in cards)

**Also generate prompts when:**
- The article has a framework, comparison, or data that a diagram would clarify
- There's an abstract concept that needs a visual anchor
- A section would benefit from breaking up long text

**Skip additional images when:**
- The article is mostly personal narrative
- Diagrams would feel forced

## Step 5b: Generate image prompts

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
- Style: follow taste.md patterns (dark palette, conceptual, non-generic)

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
Present with AskUserQuestion:
- "All good" — proceed to save
- "Revise prompts" — user provides feedback
- "Skip images" — save without image prompts

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
# draft: true   # optional — uncomment to publish at obfuscated /articles/drafts/<token>/ URL only
---

[Full article content as approved]
```

4. If image prompts were generated, save them as a separate file `articles/YYYY/MM/YYYY-MM-DD-slug/image-prompts.md`:

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
- `draft: true` (optional) builds the article at `/articles/drafts/<stable-token>/` only — not listed on home, archive, topics, RSS, or sitemap. Page is served with `noindex, nofollow` and the drafts tree is disallowed in `robots.txt`. Use this to share review links. To publish, remove the `draft` line and rebuild — the URL will change to the standard `/articles/YYYY/MM/slug/` path.

## Step 7: Wrap up

Tell the user:
- The article has been saved to `articles/[path]/article.md`
- Image prompts saved to `articles/[path]/image-prompts.md` (if generated)
- Remind: "To rebuild the site with this article: `python web/build.py`"
- Remind: "When ready to promote on LinkedIn, run `/write [article-url]`"
- Remind: "After publishing to Medium, update `medium_url` in the article frontmatter"
- Remind: "After generating images, save hero to `media/` folder and update `hero_image` in frontmatter"
