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

X rewards: thread structure, hook on tweet 1, a landing tweet that closes the loop. 280 chars per tweet (soft — Premium users have more but write for the base limit).

**Default to a thread, but pack each tweet.** Use the full 280-char budget. Group related beats into a single dense tweet rather than spinning every short sentence off into its own. Splitting a setup line and its punchline into two tweets just because they read as two beats is wrong — keep them together if they both fit.

Thread construction rules:
- **Tweet 1**: the hook + first beat. Pack toward 280 chars — typically the canonical post's opener AND the next paragraph or two if they fit. Must stand alone as a reason to read more.
- **Tweets 2-N**: continue packing toward 280 chars per tweet. Break on major argument shifts, not minor rhythm beats. Avoid "1/", "2/" numbering — X displays thread position natively.
- **Last tweet**: the landing. Either the closing line from the canonical post, or a reframe that recontextualizes the thread. Often combined with the prior beat into one dense tweet.
- **Target 3-4 tweets** for a typical short-form post. 5 only if the argument genuinely needs the space. 6+ is almost always over-fragmented — go back and combine.
- If the canonical post has a link (e.g. to an article), put the link in the **last tweet**, not the first — X throttles reach on posts with links, and first-tweet links hurt thread performance especially.
- No hashtags (X culture — feels spammy). Optional handle mentions if quoting someone.

**Char-count sanity check before showing the variant:** if any tweet is under ~180 chars, ask whether it can be combined with the next one. The default failure mode is over-splitting, not under-splitting.

**Single-tweet exception**: only for genuinely one-line observations under ~240 chars. Almost everything else is a thread.

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

If skipping, jump to Step 7. If including a visual, decide **single image or a sequence** next.

### Single image or a sequence?

LinkedIn supports carousels up to 9 images. X allows up to 4 images per tweet. Substack Notes accepts multiple inline images. A sequence is worth it when the argument unfolds across beats — a carousel narrative, a before/after, a framework broken out slide by slide, a thread where specific tweets benefit from their own supporting visual.

**Default: single image.** Choose a sequence only when you can name what each slot carries. If you can't articulate what slide 2 adds beyond slide 1, you don't have a sequence — you have one image with extras.

If choosing a sequence, use AskUserQuestion to decide the count:
- 2-3 images: tight narrative, works on all three platforms cleanly
- 4 images: fits X per-tweet max; fine on LinkedIn carousel and Substack
- 5-9 images: LinkedIn carousel only — too many for X threads and Substack Notes start to feel cluttered

For a sequence, briefly sketch what each slot carries (e.g. "slide 1: the claim; slide 2: the contrast; slide 3: the landing data") before moving to Step 6. This sketch feeds the prompts.

### Chart is always one of the visual options

**Always include a chart spec as one of the 3 visual options in Step 6** — never offer 3 AI image prompts. Charts render as crisp, on-brand visuals via the `charts/` module and consistently outperform generic AI illustrations for posts with any structural argument.

Available chart templates (see `charts/README.md`): `bar`, `stat-compare`, `quadrant`, `line`, `feature-compare`, `grid-diff`, `flow` (horizontal or vertical), `timeline`, `article-card`, `quote-card`, `quote-classic`.

The chart should fit the post's actual argument. Some natural pairings:
- Single number / ranking → `bar`
- Two numbers contrasted → `stat-compare`
- Two-by-two framing → `quadrant`
- Two paths / before vs. after → `feature-compare`
- Old vs. new with overlap → `grid-diff`
- Process / pipeline / sequence → `flow`
- Trend over time → `line`
- Events on a time axis → `timeline`
- Article-promo post (pointing readers to a published article) → `article-card` (hero + title + subtitle + auto logo/URL — replaces Substack's auto-card so the canonical visual lives in the repo). Pass the hero via `--asset hero=<path-to-article-hero>`.
- Internet / personal quote (yours or someone else's tweet/post) when no clean source screenshot is available → `quote-card` (X-style avatar + name + @handle header above the quote). Pass the avatar via `--asset avatar=<path>` (defaults to `web/img/headshot.jpg` for your own quotes).
- Famous / editorial quote (historical, classic literature, Stanford-commencement-style) → `quote-classic` (big curly-quote glyph, attribution with thin rule, optional source line). No avatar.

**If no existing template fits the argument,** add a new template to `charts/` rather than dropping the chart option. Use AskUserQuestion to confirm: "Add a new `<name>` template to `charts/`" vs. "Use a different existing template." Include a one-paragraph sketch of the proposed template (data shape + visual layout) so the user can decide.

For a chart spec, produce the JSON payload inline in the conversation alongside the other two image prompts so the user sees all three options together. If the user picks the chart, render it via the `charts/` module before saving.

## Step 6: Generate image prompts (or chart spec)

Two modes depending on Step 5. Single-image mode is the default; sequence mode produces one prompt per slot.

### Single-image mode (default)

Produce **3 image prompts** as alternatives for one slot — user picks one. If you decided above to offer a chart, the 3 options become: 1 chart spec + 2 AI image prompts.

#### Three different visual approaches

Each prompt should target a **different image type** from the taste profile:
1. **Screenshot or evidence-based visual** — if the source material came from a URL (especially a tweet, LinkedIn post, or article), the FIRST option should be a **screenshot suggestion** instead of a generation prompt. Describe exactly what to screenshot (the tweet, the article headline, the key quote), specify dark mode if it's a Twitter/X screenshot, note whether to crop to a specific section or capture full-width. If the source isn't screenshot-worthy, replace this with a third generation prompt.
2. **Diagram or infographic** — visualize a framework, comparison, or data point from the post. Dark background preferred, deep blues/teals, readable text labels.
3. **AI-generated conceptual illustration** — for the abstract concept in the post. Non-threatening, stylized. Dark palette. No split-layout banners, no floating 3D icons, no bright pastels.

#### Show prompts and iterate

Present the 3 prompts to the user using AskUserQuestion with options:
- "All good" — proceed to save
- "Revise prompts" — user provides feedback
- "Skip images" — save post without image prompts

If revising, iterate until approved.

### Sequence mode (multi-image posts)

Produce **exactly N prompts — one per slot, in narrative order.** No 3-alternative ceremony per slot; a sequence is already a larger commitment and each slot needs a clear role, not three options. User reviews all N prompts together and targets revisions by slot index.

Each prompt must explicitly name its role in the sequence — e.g. "Slide 1/4 — the opening claim," "Slide 2/4 — the contrast setup," "Slide 4/4 — the landing number." Slots should build on each other visually (consistent palette, consistent type treatment) unless a deliberate visual shift is part of the argument.

#### Sequence mixing

A sequence can mix types (e.g. slot 1 is a screenshot, slots 2-3 are diagrams, slot 4 is an illustration). Don't force the same type across every slot — the right tool per beat wins. The constraint is narrative coherence, not visual uniformity.

#### Show prompts and iterate

Output all N prompts as regular text in the response, clearly labeled by slot, then use AskUserQuestion:
- "All good" — proceed to save
- "Revise slot X" — user names the slot and provides feedback in notes
- "Skip images" — save post without image prompts

If revising, regenerate only the named slot(s), re-output the full sequence, and ask again. Iterate until approved.

### Chart rendering

When rendering a chart (single-image mode or as one slot of a sequence), save the spec next to the post under the post's `media/` folder and render to `.webp`:

```bash
node charts/render.mjs --template <name> \
  --data posts/YYYY/MM/YYYY-MM-DD-slug/media/<name>.json \
  --output posts/YYYY/MM/YYYY-MM-DD-slug/media/<name>.webp \
  --width <w> --height <h>
```

LinkedIn crops to ~1:1 in feed. For square-favorable charts use `--width 1200 --height 1200`; for wide editorial charts use the defaults from `charts/README.md`.

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

For a sequence, pick a dimension per slot and keep it consistent across the sequence unless the argument demands otherwise — a LinkedIn carousel with mixed aspect ratios reads as sloppy. Default to 1200×1200 square for carousels (LinkedIn renders all carousel images at the same crop).

Override the defaults when the content demands it (e.g., a tall flowchart might need 1080×1350 portrait).

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

**For sequence posts (2+ images):** append a `## Media` section after the hashtags line with one markdown reference per image, in sequence order. This matches the scraper's existing convention and makes all images render stacked on the individual post page.

```markdown
**Hashtags:** #Tag1 #Tag2 #Tag3

---

## Media

![image-1.webp](media/image-1.webp)

![image-2.webp](media/image-2.webp)

![image-3.webp](media/image-3.webp)
```

Single-image posts don't need the `## Media` section — the builder picks up `media[0]` as the card thumbnail and OG image automatically, and the individual post page reads fine without an inline hero.

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

**Attach image:** media/image-1.webp

---

**After posting:** copy the LinkedIn permalink and paste it into `post.md` as `post_url:`.
```

**For sequence posts (2+ images):** replace the single-image attach line with a carousel attach block:

```markdown
**Attach as a carousel (in order):**
- media/image-1.webp
- media/image-2.webp
- media/image-3.webp

LinkedIn renders 2+ images as a swipeable carousel. Order matters — image-1 is the feed thumbnail, and readers swipe left in sequence.
```

If the post has no image, omit the attach block entirely.

### 7c. `x-thread.md` — X thread paste-ready variant

```markdown
# X thread — [slug]

Paste each tweet into X manually as a reply chain, OR load into Typefully / similar scheduler. No hashtags, no numbering.

---

**Tweet 1 (hook):**
[text, under 280 chars]
*Attach: media/image-1.webp*

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

**Image-per-tweet rules:**
- **Single-image post:** attach `media/image-1.webp` to tweet 1 (the hook). Its visibility in the feed matters most.
- **Sequence post (2-4 images):** distribute one image per tweet across the tweets that best carry them. Default: image-1 on tweet 1, then subsequent images on the tweets whose argument they anchor. X allows up to 4 images in a single tweet, but one-per-tweet reads cleaner for a narrative thread.
- **Sequence post (5-9 images):** X doesn't fit this cleanly — pick the 3-4 strongest images for the thread, note the rest are LinkedIn-carousel-only.

Use `*Attach: media/image-N.webp*` as an italic line directly under the relevant tweet's body. If a tweet has no image, omit the attach line.

If the X variant is a single tweet (short-but-complete exception), use a single `**Tweet:**` block with the attach line underneath.

### 7d. `substack-note.md` — Substack Note paste-ready variant

```markdown
# Substack Note — [slug]

Paste into Substack Notes (substack.com/notes). No hashtags. Links welcome.

---

[Substack Note body, adapted from the LinkedIn variant — no hashtags, softer hook, link welcomed if applicable]

---

**Attach image:** media/image-1.webp

---

**After posting:** copy the Note URL and paste it into `post.md` as `substack_note_url:`.
```

**For sequence posts (2+ images):** replace the single-image attach line with an inline attach block:

```markdown
**Attach inline (in order):**
- media/image-1.webp (primary — shown above the fold)
- media/image-2.webp
- media/image-3.webp

Substack Notes supports multiple inline images. Paste the text first, then drag each image in at the cursor position where it should appear in the flow. If you want all images at the top (simplest), drag them in as a block before the first paragraph.
```

If the post has no image, omit the attach block entirely.

### 7e. `image-prompts.md` — if images were generated

**Single-image mode (3 alternatives, user picked one):**

```markdown
# Image Prompts

## Option 1: [type — e.g., "Screenshot of source tweet"]
[prompt or screenshot instructions]

## Option 2: [type — e.g., "Diagram"]
[prompt]

## Option 3: [type — e.g., "AI illustration"]
[prompt]
```

**Sequence mode (N slots, one prompt per slot):**

```markdown
# Image Prompts — sequence

## Slide 1/N: [role — e.g., "the opening claim"]
[prompt]

## Slide 2/N: [role — e.g., "the contrast setup"]
[prompt]

## Slide 3/N: [role — e.g., "the landing data"]
[prompt]
```

The final image file written to `media/` for each slot should be named `image-1.webp`, `image-2.webp`, ..., `image-N.webp` in the same order as the slides appear here.

If the user skipped images, omit this file entirely.

### 7f. Chart specs (if a chart was chosen)

Chart JSON spec and rendered `.webp` go in the post's `media/` subdirectory (already created when rendering in Step 6).

## Step 8: Confirm completion

Tell the user:
- **Site canonical post saved:** `posts/YYYY/MM/YYYY-MM-DD-slug/post.md`
- **LinkedIn variant:** `posts/YYYY/MM/YYYY-MM-DD-slug/linkedin.md` — paste into LinkedIn's native composer
- **X thread variant:** `posts/YYYY/MM/YYYY-MM-DD-slug/x-thread.md` — paste into X or Typefully
- **Substack Note variant:** `posts/YYYY/MM/YYYY-MM-DD-slug/substack-note.md` — paste into substack.com/notes
- If image prompts: `image-prompts.md` in the same directory. Generate each image and save to `media/` as `image-1.webp` (single-image posts) or `image-1.webp` through `image-N.webp` in sequence order (multi-image posts).
- Remind: "After posting on each surface, fill in `post_url:`, `x_url:`, and `substack_note_url:` in `post.md` frontmatter."
- Remind: "To publish the site post: `bash pipeline.sh --skip-scrape`"
- Remind: "Later runs of the scraper will pick up engagement counts (reactions, comments) from LinkedIn and merge them into this post automatically — no duplicate will be created because `authored: true` is set."
- Suggested posting order: site (auto-deployed via pipeline) → LinkedIn (broadest cold reach) → X (parallel cold reach) → Substack Note (warm conversion to subscribers).
