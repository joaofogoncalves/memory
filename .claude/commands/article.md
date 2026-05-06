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

## Step 2.5: Identify the target audience

The audience shapes angle, depth, vocabulary, and visual choices. If the user's notes already specify an audience (e.g., "for engineering leaders", "for PMs"), use it and skip the question.

Otherwise, use AskUserQuestion with these options:
- **Engineering leaders / technical decision-makers** — CTOs, VPs Eng, staff+ engineers. Assume technical depth, skip the 101, lead with architectural tradeoffs and failure modes.
- **Product & business leaders** — PMs, founders, execs. Frame in outcomes, use metaphors over jargon, fewer code details.
- **Generalists / curious professionals** — mixed backgrounds. Explain more, use analogies, avoid unexplained acronyms.
- **Mixed / broad audience** — default LinkedIn reach. Write for the smart non-specialist; technical asides in context, never as the centerpiece.

Remember this choice — it informs angles (Step 3), depth (Step 4), and visuals (Step 5).

## Step 2.6: SERP reality check

Before proposing angles, do a quick SERP read for the topic. The goal is **not** to pick the angle by what ranks — it's to make sure the angle isn't accidentally indistinguishable from what's already on page 1.

1. Pick 1–3 likely search queries a reader interested in this topic might type. Frame them as the reader would, not as the author. Calibrate vocabulary to the audience from Step 2.5.
2. Use WebSearch on each query. Skim the top ~10 results.
3. Capture, in an internal note (not shown to the user yet):
   - **Dominant format**: listicle, how-to, explainer, comparison, opinion essay, case study, news. Which formats own the SERP?
   - **Recurring framings**: what angle does almost every result take? Where do they all agree?
   - **Format gap**: what shape of piece is *missing*? (e.g. all listicles, no opinion piece; all how-tos, no skeptical take.)
   - **Proof gap**: what concrete evidence, examples, or numbers do top results lack?
   - **People Also Ask / related questions** if visible — surface them as candidate FAQ entries later (Step 6 will emit FAQPage JSON-LD if you include a `## FAQ` section).

Carry this into Step 3. The angle should either fill a real gap (format or proof) or earn its place by being a sharper, more specific take than the SERP consensus. If every top result already says what you were going to say, the angle is wrong — pick a different one.

This is a sanity check, not an SEO playbook. Don't warp the voice to match SERP norms; warp the *positioning* so the piece is genuinely additive.

## Step 3: Propose angles and structure

Based on the source material, text notes, research, and the target audience from Step 2.5, propose **2-3 angles** for the article. Each angle should:
- Be 2-3 sentences describing the thesis and approach
- Map to recurring topics from profile.md
- Represent genuinely different perspectives
- Land with the chosen audience — pick a thesis they'll care about, framed in their vocabulary

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

## Step 3.5: Plan internal links

After the outline is approved and **before drafting**, identify 2–4 candidate internal links the article should weave in naturally. Internal linking is one of the cheapest discoverability levers and is much harder to retrofit cleanly.

1. **Scan existing articles**: list all non-draft article slugs and titles from `articles/YYYY/MM/*/article.md`. Glob is fine. For each, read the title and subtitle from frontmatter — that's enough to judge thematic fit.
2. **Scan recent posts**: glob `posts/YYYY/MM/*/post.md` from the last ~12 months. Many short-form posts contain the seed of an idea this article expands on; linking back gives them a second life.
3. **Check for matching topic pages**: read `config/site.yaml` `topics:` list. If the article fits one (or two), the topic page is a natural cross-link.
4. **Pick 2–4 candidates** with a one-sentence reason each. Favor links that:
   - Expand on a claim made in passing in this article (so the link adds something the reader will actually click)
   - Connect to a piece on the *same* theme that approaches it differently (cluster signal)
   - Point to a topic page when this article belongs to a recurring theme

**Decide where each link belongs in the outline.** Specify section + anchor phrase. The link should fit a sentence the article would naturally write — never bolt one on for SEO.

**Skip if the article is genuinely standalone.** A link that has to be forced is worse than no link at all. Two strong internal links beat four weak ones.

Carry the chosen links + their anchor placements into the draft prompt — the writer should reach for them as it goes, not retrofit them at the end. External citations (the 3–5 source links from Step 2) are separate; this step is only about *internal* linking.

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

### Calibrate depth to audience

Use the audience from Step 2.5:
- **Engineering leaders**: assume technical literacy; skip 101-level explanations; go deeper on tradeoffs, specific implementations, failure modes. Code and architecture allowed.
- **Product & business leaders**: frame in outcomes, not implementation. Analogies for technical concepts. Jargon only when defining it. Heavier on "why it matters."
- **Generalists**: define technical terms on first use. Prefer concrete stories over abstractions. Analogies carry the explanation.
- **Mixed**: lead with the broadly accessible frame. One or two technical asides for specialists are fine — don't lose the generalist reader.

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

**Match visuals to audience (Step 2.5):** engineering audiences often value technical diagrams (flow, architecture, timeline); business audiences prefer outcome-framed comparisons (stat-compare, bar, quadrant); generalists lean on narrative hero images over technical diagrams.

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
- **Heroes are NOT bound by the site color scheme.** Unlike inline diagrams/charts (which follow the dark navy + teal palette from taste.md), the hero is the mood piece for the article. Choose palette and lighting that serve the concept.
- **Default to cinematic photography, not painting.** The heroes that land on this site look like photographs or photo-real renders: architectural interiors, documentary-style scenes, real objects with real light. Think *The New Yorker* photo essays, Wired feature photography, Apple product-site art direction, Edward Burtynsky, Gregory Crewdson — a real place or object, shot with intent. Not an illustration of one.
- **Avoid language that invites painterly output:** "editorial painting," "painterly brushwork," "visible texture," "illustration," "digital painting," "artist's rendering." These consistently produce soft, watercolor-flavored images that read as generic AI art. Instead, write the prompt as a photograph: lens, lighting, camera distance, time of day.
- **Prompt scaffolding that works** (mix and match): photorealistic wide shot · architectural/interior photography · shallow depth of field · natural window light · golden hour · overhead perspective · long exposure · 35mm / 50mm / wide-angle · cinematic color grade · documentary style · muted saturation · matte finish (not glossy).
- **When the concept resists photography** (a metaphor with no physical referent), prefer a real object or scene that stands in for the idea over an illustration of the idea. A quiet workshop photographed at dawn beats a painting of industriousness.
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
3. **Write a meta description** (140–160 characters) for the `description:` frontmatter field. This is what shows up in Google SERP snippets and link previews — it must earn the click on its own. Rules:
   - Distinct from the subtitle (different phrasing, different beat — they sit next to each other in the preview)
   - Lead with the punch, not throat-clearing ("Most teams… X. Here's why."), not "This article explores…"
   - Concrete enough that someone scanning a SERP knows what they're getting
   - No keyword stuffing, no clickbait, voice consistent with the article
   - Include 1–2 of the article's key terms naturally (queries it would plausibly rank for)
4. Save `article.md` with this format:

```markdown
---
title: "[Article title]"
subtitle: "[Subtitle]"
description: "[140–160 char meta description — earns the click in the SERP]"
date: [today's date, YYYY-MM-DD]
tags: [tag1, tag2, tag3]
substack_url:
hero_image:
reading_time: [computed from word count]
draft: true
---

[Full article content as approved]
```

**Optional — FAQ section for snippet eligibility.** If the article naturally answers 3+ recurring questions about its topic (often surfaced by the People Also Ask box in Step 2.6), add a `## FAQ` section near the bottom with `### Question?` H3s and a short paragraph answer under each. The build pipeline auto-emits FAQPage JSON-LD when it detects this pattern, which can earn rich-result placement. Don't fabricate questions to game it — the FAQ has to read as a genuine extension of the piece, not a tacked-on SEO tail.

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
- `substack_url` is left empty — fill in after publishing to Substack
- `hero_image` is left empty — fill in after generating and saving the image
- `reading_time` is computed: word count / 230, rounded to nearest minute
- `draft: true` is set by default — new articles always start as drafts. They build at `/articles/drafts/<stable-token>/` only, not listed on home, archive, topics, RSS, or sitemap. Page is served with `noindex, nofollow` and the drafts tree is disallowed in `robots.txt`. Use this URL to share review links. To publish, run `/publish <slug-or-path>` (or remove the `draft` line manually and update the date).

## Step 7: Generate critique prompt for external review

Save a copy-pasteable critique prompt the user can take to another AI (ChatGPT, Claude.ai, Gemini) for a second-opinion review. This is the main defense against the polish-after-publish loop — catching weak spots while the draft is still a draft.

Write to `articles/YYYY/MM/YYYY-MM-DD-slug/critique-prompt.md`. **Do not embed the article text** — pass the draft URL instead, so the reviewing AI fetches the live draft page directly. This keeps the prompt short and ensures the reviewer sees the rendered article (images, formatting) rather than raw markdown.

Compute the draft URL:
- Token: `sha256(slug)[:16]` (same method `web/build.py` uses for draft routing)
- URL: `{SITE_URL}/articles/drafts/{token}/`
- Read `SITE_URL` from `.env`; fall back to `yoursite.com` if missing.
- Use `python -c "import hashlib; print(hashlib.sha256('<slug>'.encode()).hexdigest()[:16])"` to compute the token.

Template (substitute `{AUDIENCE}` with the audience from Step 2.5, and `{DRAFT_URL}` with the computed URL):

```markdown
# Critique prompt

Paste the prompt below into another AI (ChatGPT, Claude.ai, Gemini — whichever gives you a fresh perspective) for a sharp second-opinion review. The reviewer will fetch the draft directly. Bring the feedback back to Claude Code and ask for targeted revisions.

**Before pasting:** make sure the draft is deployed (`bash pipeline.sh --skip-scrape`) so the URL resolves.

---

You are an experienced editor and subject-matter skeptic. The draft article is published at the URL below — fetch it and read the full piece before responding. Your job is to give sharp, specific, unsentimental feedback that makes the piece stronger.

**Target audience:** {AUDIENCE}

**Draft article URL:** {DRAFT_URL}

---

**Review criteria — give specific, quote-level feedback on each:**

1. **Argument strength.** Is the thesis actually supported by the evidence and examples? Where are the gaps or unproven leaps?
2. **Evidence.** Which claims need a citation or concrete example? Which feel assertive without grounding?
3. **Voice consistency.** Where does the writing drift into corporate, generic, or AI-ish language? Quote specific phrases.
4. **Weakest section.** If you had to cut or rewrite one section end-to-end, which one? Why?
5. **Missing counterargument.** What's the strongest objection a skeptical reader would raise that the article fails to address?
6. **Overstatements and filler.** Quote specific sentences that are overclaims, hedges, throat-clearing, or fluff.
7. **Opening and closing.** Does the opening earn the reader's attention? Does the closing land, or fade out?
8. **Audience fit.** Does the writing match the stated audience? Where is it too technical, not technical enough, or missing their vocabulary?

**Output format:**

Start with your **top 3 recommended changes** in priority order — the ones that would most improve the piece.

Then go through each criterion above with specific quotes and line-level suggestions.

Be direct. Don't cushion. The goal is a sharper article, not a comfortable author.
```

## Step 8: Wrap up

Tell the user:
- The article has been saved to `articles/[path]/article.md`
- Critique prompt saved to `articles/[path]/critique-prompt.md` — paste it into another AI before publishing to catch weak spots
- Image prompts saved to `articles/[path]/image-prompts.md` (if generated)
- Remind: "To rebuild the site with this article: `python web/build.py`"
- Remind: "When ready to promote on LinkedIn and X, run `/post [article-url]`"
- Remind: "When ready to publish, run `/publish [slug]` — it flips the draft flag and generates the Substack paste-in artifact"
- Remind: "After publishing to Substack, update `substack_url` in the article frontmatter"
- Remind: "After generating images, save hero to `media/` folder and update `hero_image` in frontmatter"
