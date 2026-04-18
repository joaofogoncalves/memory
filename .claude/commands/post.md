---
argument-hint: [urls and/or notes about what to write]
description: Author a short-form post — saves canonical version to the site and generates LinkedIn + X + Substack Note variants for manual posting
allowed-tools: AskUserQuestion, WebFetch, Write, Read, Glob, Bash
---

Author a short-form post. The site is canonical — the post is saved to `posts/YYYY/MM/YYYY-MM-DD-slug/post.md`. LinkedIn, X thread, and Substack Note variants are generated as paste-ready artifacts for manual posting on each platform.

## Arguments

`$ARGUMENTS` contains free text: URLs, notes, angles, or any combination. Parse it to separate:
- **URLs**: anything starting with `http://` or `https://`
- **Text notes**: everything else (the user's thoughts, angles, or raw material)

If `$ARGUMENTS` is empty, use AskUserQuestion to ask what they want to write about.

## Step 1: Gather source material

1. Read `writing_style.md` from the project root. This is the authoritative style guide — it defines structure, tone, language rules, length targets, and anti-patterns. Always follow it as the primary reference when drafting.
2. Read `profile.md` from the project root. This is the auto-generated voice profile — it provides vocabulary, topic expertise, and deeper voice patterns. Where it conflicts with `writing_style.md`, defer to `writing_style.md`.
3. Read `taste.md` from the project root. This is the visual taste profile — follow it when generating image prompts.
4. If URLs were found in the arguments:
   - Fetch each URL using WebFetch
   - Extract the key content: headline, author, main argument, notable quotes, data points
   - Identify the source type: tweet/X post, LinkedIn post, article, blog post, research paper, other
5. Summarize all source material in a brief internal note (do not show to user yet).

## Step 2: Propose angles

Based on the source material and text notes, propose **2-3 angles** for the post. Each angle should:
- Be 1-2 sentences describing the take
- Map to one of the recurring topics from profile.md
- Represent a genuinely different perspective, not just rewordings

If the user already provided a clear angle/thesis in their text notes, still propose it as the first option but offer 1-2 alternatives.

Use AskUserQuestion to present the angles. Format:
- Each option label is a short name for the angle (e.g., "The adoption gap angle")
- Each option description is the 1-2 sentence take

## Step 3: Draft the canonical post (site version)

### Auto-detect post template

Based on input type and chosen angle, select the template. Word counts below reflect engagement data: posts in the 100-150 word range score ~3-4x posts in the 150-200 range, which still beat 200+. Bias short.

- **Source is a tweet, LinkedIn post, or someone's hot take** → Short-form commentary (**100-150 words**, hard upper bound 200)
- **Source is an article (yours or someone else's) you want to riff on** → Article reaction / promotion (**100-180 words**)
- **Source is an article/data + user has a thesis** → Long-form thought piece (**200-300 words**, only if the argument genuinely needs the space — and it usually doesn't)
- **No URL, just text notes with a thesis** → Long-form thought piece (**200-300 words**, same caveat)
- **No URL, brief reaction to an event/trend** → Short-form commentary (**100-150 words**)

**Hard floor:** 100 words. Posts under 100 underperform across the archive.
**Hard ceiling default:** 250 words. Going past requires the argument to earn it; cut anything restating what's already said.

### Write the draft

Follow `writing_style.md` as the primary style authority — its rules on voice, tone, structure, signature moves, language, length, and anti-patterns are all mandatory.

Supplement with `profile.md` for:
- Vocabulary: use the "Use naturally" words, avoid the "Avoid" words
- Recurring topics and the specific angles taken on each
- Rhetorical devices and deeper voice patterns not covered by `writing_style.md`

Where `profile.md` and `writing_style.md` conflict, `writing_style.md` wins.

Additional rules:
- Emoji: zero by default
- Hashtags: 2-4 at the very end of the body (LinkedIn convention — the site strips them before rendering)
- No engagement asks, no self-promotion
- If using the "ps:" aside device, keep it lowercase and casual

This is the **canonical** draft. LinkedIn and X variants will be adapted from it in Step 4 — keep this version clean, platform-neutral, and suitable for the site. The canonical post may contain a link (e.g., to an article you're reacting to), but avoid LinkedIn-specific or X-specific phrasing.

### Show draft and iterate

IMPORTANT: Always output the full draft as regular text in your response BEFORE asking for feedback. Never put the draft inside the `preview` field of AskUserQuestion — previews don't render reliably. The user must be able to read the draft directly in the conversation.

Format: output the draft text between horizontal rules (`---`) so it's visually distinct, then use AskUserQuestion with options:
- "Looks good" — proceed to platform variants
- "Needs changes" — user provides feedback in the notes field
- "Try a different angle" — go back to Step 2
- "Scrap and start over" — ask for new input

If the user selects "Needs changes," revise the draft, output the full revised text again, and ask once more. Continue iterating until they approve.

## Step 4: Generate platform variants

Once the canonical post is approved, produce three platform-adapted artifacts (LinkedIn, X thread, Substack Note). Each surface has different mechanics and audience — don't just paste the same text to all three.

### LinkedIn variant

LinkedIn rewards: a sharp hook in the first 1-2 lines (shown above "see more"), intentional paragraph breaks, conversational rhythm, hashtags at the end, zero emojis (per style guide).

- Usually very close to the canonical draft — often identical
- Double-check: first 2 lines MUST earn the expand click
- Keep paragraph breaks generous (single-sentence paragraphs work well here)
- Hashtags at the end, 2-4 tags
- Length: 150-300 words comfortable; longer is fine if the argument earns it

### X variant

X rewards: thread structure, hook on tweet 1, short sentences, one idea per tweet, a landing tweet that closes the loop. 280 chars per tweet (soft — Premium users have more but write for the base limit).

**Default to a thread.** Single tweets are only for genuinely one-line observations (under ~240 chars with room for the point to breathe). Even short ideas often read better as a 2-3 tweet thread with rhythm.

Thread construction rules:
- **Tweet 1**: the hook. Sharpest line from the post. Must stand alone as a reason to read more.
- **Tweets 2-N**: one idea per tweet. Break on natural beats, not mid-thought. Avoid "1/", "2/" numbering — it feels mechanical and X displays thread position natively. Let the rhythm carry it.
- **Last tweet**: the landing. Either the closing line from the canonical post, or a reframe that recontextualizes the thread.
- **Target 3-7 tweets** for a typical short-form post. Longer threads (8+) only if the argument genuinely needs the space.
- If the canonical post has a link (e.g. to an article), put the link in the **last tweet**, not the first — X throttles reach on posts with links, and first-tweet links hurt thread performance especially.
- No hashtags (X culture — feels spammy). Optional handle mentions if quoting someone.

**Short-but-thread-fits judgment call**: if the canonical post is 150-200 words but has a natural rhythm break (setup → turn → landing), still write a 3-tweet thread. Single-tweet output is the exception, not the default.

### Substack Note variant

Substack Notes is a different beast from LinkedIn and X — the audience is already inside the newsletter ecosystem and one click from subscribing. Notes is mid-funnel (conversion), not top-of-funnel (cold reach). Adapt the LinkedIn variant with these moves:

- **Strip the hashtags.** Notes culture doesn't use them.
- **Soften the hook.** LinkedIn's first line has to earn the expand-click against a noisy feed; Notes readers are more receptive. The opener can be conversational rather than punchy. A flat first sentence is fine.
- **Welcome the link.** Unlike X, Substack Notes don't throttle posts with links. If this is an article-promo post or a riff on a source, include the link inline near the close (or as a final standalone line for click prominence).
- **Length:** roughly the same as LinkedIn — 100-250 words. Notes can go longer than tweets, but shorter feels native.
- **No Subscribe CTA.** The Subscribe button shows up automatically on every Note for non-subscribers; don't ask explicitly.

For most posts the Note is ~90% of the LinkedIn copy with these adjustments — a fast transform, not a fresh write. If the LinkedIn variant is also link-free and tag-light, the Note can be nearly identical.

### Show variants and iterate

Output all three variants (LinkedIn, X thread, Substack Note) clearly separated in the response, then use AskUserQuestion:
- "All look good" — proceed to images
- "Revise LinkedIn" — feedback on LinkedIn variant
- "Revise X thread" — feedback on X thread
- "Revise Substack Note" — feedback on Note variant
- "Revise multiple" — feedback on more than one

Iterate until approved.

## Step 5: Choose a visual (default: yes)

Archive analysis shows posts with media average ~6.5x the comment engagement of text-only posts (11.2 vs 1.7 comments). **Default to including a visual** — skipping should be the exception, and you should be able to state the reason out loud.

**Include a visual (the default) when any of these apply — which is most posts:**
- There's source material worth screenshotting: tweet, LinkedIn post, article, research figure. The screenshot is often the sharpest hook.
- The argument has a visual structure (comparison, framework, funnel, timeline, stat contrast) a chart or diagram would clarify.
- The concept is abstract and benefits from an editorial illustration as an anchor.
- In short: if you can imagine a reasonable visual, include one.

**Skip only when:**
- The post is a raw personal admission and a visual would dilute the directness (e.g. "I got this wrong, here's what I learned").
- Forcing an image would genuinely feel like decoration — there's no concept to anchor, and no external artifact to show.
- The prose rhythm is the whole point and an image would break the read.

These are rare cases. If you skip, state the reason explicitly in the conversation: "Skipping visual — this post is [raw personal admission / rhythm-driven / ...], and adding an image would hurt the point." Do not skip silently.

If the post includes a visual, proceed to Step 6. If skipping, jump to Step 7.

### Chart as an alternative to AI image

Some posts — especially ones built around a single stat, contrast, or comparison — are better served by a **chart** than a generated image. A crisp chart with the headline number often out-performs a stylized illustration for this style of post.

Consider a chart (not an AI image) when:
- The post pivots on one or two numbers ("88% have access, 1% have maturity")
- The post contrasts two paths / before-after / pipeline vs. nervous system
- The hook is a ranking or funnel
- The post already cites a stat the reader should see, not just read

Available chart templates (see `charts/README.md`): `bar`, `stat-compare`, `quadrant`, `line`, `flow` (horizontal or vertical), `timeline`.

If a chart fits, offer it as one of the 3 visual options in Step 6 — alongside two AI image prompts — rather than producing three AI prompts. Produce a chart **spec** (template name + sample JSON payload) and, if the user picks it, render it via the `charts/` module.

**If the visual you want doesn't match any existing template,** ask the user with AskUserQuestion: "Add a new `<name>` template to `charts/`" vs. "Use an AI image prompt instead." Include a one-paragraph sketch of the proposed template.

## Step 6: Generate image prompts (or chart spec)

If you decided above to offer a chart, the 3 options become: 1 chart spec + 2 AI image prompts. Otherwise produce **3 image prompts** following the visual taste profile from `taste.md`.

When rendering a chart, save the spec next to the post under the post's `media/` folder and render to `.webp`:

```bash
node charts/render.mjs --template <name> \
  --data posts/YYYY/MM/YYYY-MM-DD-slug/media/<name>.json \
  --output posts/YYYY/MM/YYYY-MM-DD-slug/media/<name>.webp \
  --width <w> --height <h>
```

LinkedIn crops to ~1:1 in feed. For square-favorable charts use `--width 1200 --height 1200`; for wide editorial charts use the defaults from `charts/README.md`.

### Screenshot suggestion

If the source material came from a URL (especially a tweet, LinkedIn post, or article), the FIRST option should be a **screenshot suggestion** instead of a generation prompt. Format:
- Describe exactly what to screenshot (the tweet, the article headline, the key quote)
- Specify dark mode if it's a Twitter/X screenshot
- Note whether to crop to a specific section or capture full-width

If the source isn't screenshot-worthy, replace this with a third generation prompt.

### Three different visual approaches

Each prompt should target a **different image type** from the taste profile:
1. **Screenshot or evidence-based visual** (if applicable — see above)
2. **Diagram or infographic** — visualize a framework, comparison, or data point from the post. Dark background preferred, deep blues/teals, readable text labels.
3. **AI-generated conceptual illustration** — for the abstract concept in the post. Non-threatening, stylized. Dark palette. No split-layout banners, no floating 3D icons, no bright pastels.

### Prompt format

Write each prompt as detailed natural language (for Nano Banana or similar generators). Each prompt should be 2-4 sentences covering:
- Subject and composition
- Visual style and mood
- Color palette
- What text (if any) should appear in the image
- What to avoid (reference taste.md anti-patterns)

End each prompt with a **specs line** in this format:
`Format: [width]x[height]px ([aspect ratio]) · [file type]`

### Image dimensions

Posts appear on both LinkedIn and the personal website. Use these defaults:

| Image type | Dimensions | Ratio | Format | Notes |
|-----------|-----------|-------|--------|-------|
| **AI illustrations** | **1440×900px** | 16:10 | PNG or JPG | Works on both LinkedIn (landscape) and the website (2x retina at 720px, crops cleanly for all thumbnail contexts: spotlight 16:10, list cards 300×175, card thumbs 140×100) |
| **Diagrams/infographics** | **1200×1200px** | 1:1 | PNG | Sharp text, no compression artifacts. Square works on LinkedIn and website. |
| **Screenshots** | native resolution, crop to content | — | PNG | Lossless |

**Important**: Keep the main subject **centered with breathing room** — the website crops images via `object-fit: cover` at different ratios depending on context (homepage spotlight, post list thumbnails, card grids).

Override the defaults when the content demands it (e.g., a tall flowchart might need 1080x1350 portrait).

### Show prompts and iterate

Present the 3 image prompts to the user using AskUserQuestion with options:
- "All good" — proceed to save
- "Revise prompts" — user provides feedback
- "Skip images" — save post without image prompts

If revising, iterate until approved.

## Step 7: Save all artifacts

1. Generate a slug from the canonical post's opening line: first 5-8 words, lowercased, hyphenated, max 50 chars.
2. Compute the post directory path: `posts/YYYY/MM/YYYY-MM-DD-slug/` using today's date.
3. If the directory already exists (rare, but possible if re-running), append `-2`, `-3`, etc. to the slug.
4. Create the directory and write the following files:

### 7a. `post.md` — canonical site version

```markdown
---
date: YYYY-MM-DD
post_type: original
authored: true
post_url: ""
x_url: ""
substack_note_url: ""
tags: [tag1, tag2, tag3]
source_urls:
  - [url1]
angle: [one-line description of the chosen angle]
template: [short-form | long-form | article-reaction]
---

[the canonical post body, exactly as approved]

**Hashtags:** #Tag1 #Tag2 #Tag3
```

Notes:
- `authored: true` distinguishes this from scraped posts. The scraper will respect this flag and only update engagement counts, never overwrite the body.
- `post_url` starts empty — fill in with the LinkedIn permalink after posting manually.
- `x_url` starts empty — fill in with the X permalink after posting.
- `substack_note_url` starts empty — fill in with the Substack Note permalink after posting.
- `source_urls` — omit if the post has no external sources.
- `tags` — lowercase tags extracted from the hashtags or the topic (match `site.yaml` topics where relevant).

### 7b. `linkedin.md` — LinkedIn paste-ready variant

```markdown
# LinkedIn post — [slug]

Paste this directly into LinkedIn's composer. Zero emojis, 2-4 hashtags at the end.

---

[LinkedIn variant body, exactly as approved]

#Tag1 #Tag2 #Tag3

---

**After posting:** copy the LinkedIn permalink and paste it into `post.md` as `post_url:`.
```

### 7c. `x-thread.md` — X thread paste-ready variant

```markdown
# X thread — [slug]

Paste each tweet into X manually as a reply chain, OR load into Typefully / similar scheduler. No hashtags, no numbering.

---

**Tweet 1 (hook):**
[text, under 280 chars]

**Tweet 2:**
[text]

**Tweet 3:**
[text]

...

**Tweet N (landing):**
[text, may include the link if this is an article reaction]

---

**After posting:** copy the X permalink (of tweet 1) and paste it into `post.md` as `x_url:`.
```

If the X variant is a single tweet (short-but-complete exception), use a single `**Tweet:**` block with the same structure.

### 7d. `substack-note.md` — Substack Note paste-ready variant

```markdown
# Substack Note — [slug]

Paste into Substack Notes (substack.com/notes). No hashtags. Links welcome.

---

[Substack Note body, adapted from the LinkedIn variant — no hashtags, softer hook, link welcomed if applicable]

---

**After posting:** copy the Note URL and paste it into `post.md` as `substack_note_url:`.
```

### 7e. `image-prompts.md` — if images were generated

```markdown
# Image Prompts

## Option 1: [type — e.g., "Screenshot of source tweet"]
[prompt or screenshot instructions]

## Option 2: [type — e.g., "Diagram"]
[prompt]

## Option 3: [type — e.g., "AI illustration"]
[prompt]
```

If the user skipped images, omit this file entirely.

### 7f. Chart specs (if a chart was chosen)

Chart JSON spec and rendered `.webp` go in the post's `media/` subdirectory (already created when rendering in Step 6).

## Step 8: Confirm completion

Tell the user:
- **Site canonical post saved:** `posts/YYYY/MM/YYYY-MM-DD-slug/post.md`
- **LinkedIn variant:** `posts/YYYY/MM/YYYY-MM-DD-slug/linkedin.md` — paste into LinkedIn's native composer
- **X thread variant:** `posts/YYYY/MM/YYYY-MM-DD-slug/x-thread.md` — paste into X or Typefully
- **Substack Note variant:** `posts/YYYY/MM/YYYY-MM-DD-slug/substack-note.md` — paste into substack.com/notes
- If image prompts: `image-prompts.md` in the same directory, generate images and save hero to `media/`
- Remind: "After posting on each surface, fill in `post_url:`, `x_url:`, and `substack_note_url:` in `post.md` frontmatter."
- Remind: "To publish the site post: `bash pipeline.sh --skip-scrape`"
- Remind: "Later runs of the scraper will pick up engagement counts (reactions, comments) from LinkedIn and merge them into this post automatically — no duplicate will be created because `authored: true` is set."
- Suggested posting order: site (auto-deployed via pipeline) → LinkedIn (broadest cold reach) → X (parallel cold reach) → Substack Note (warm conversion to subscribers).
