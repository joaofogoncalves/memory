---
argument-hint: [urls and/or notes about what to write]
description: Write a LinkedIn post using your style guide and voice profile, and generate 3 AI image prompts
allowed-tools: AskUserQuestion, WebFetch, Write, Read, Glob
---

Write a LinkedIn post based on the user's input and generate AI image prompts for it.

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

## Step 3: Draft the post

### Auto-detect post template

Based on input type and chosen angle, select the template:
- **Source is a tweet, LinkedIn post, or someone's hot take** → Short-form commentary (150-250 words)
- **Source is an article the user wrote or wants to promote** → Article promotion (100-200 words)
- **Source is an article/data + user has a thesis** → Long-form thought piece (250-400 words, only if the argument needs the space)
- **No URL, just text notes with a thesis** → Long-form thought piece (250-400 words, only if the argument needs the space)
- **No URL, brief reaction to an event/trend** → Short-form commentary (150-250 words)

### Write the draft

Follow `writing_style.md` as the primary style authority — its rules on voice, tone, structure, signature moves, language, length, and anti-patterns are all mandatory.

Supplement with `profile.md` for:
- Vocabulary: use the "Use naturally" words, avoid the "Avoid" words
- Recurring topics and the specific angles taken on each
- Rhetorical devices and deeper voice patterns not covered by `writing_style.md`

Where `profile.md` and `writing_style.md` conflict, `writing_style.md` wins.

Additional rules:
- Emoji: zero by default
- Hashtags: 2-4 at the very end
- No engagement asks, no self-promotion
- If using the "ps:" aside device, keep it lowercase and casual

### Show draft and iterate

IMPORTANT: Always output the full draft as regular text in your response BEFORE asking for feedback. Never put the draft inside the `preview` field of AskUserQuestion — previews don't render reliably. The user must be able to read the draft directly in the conversation.

Format: output the draft text between horizontal rules (`---`) so it's visually distinct, then use AskUserQuestion with options:
- "Looks good" — proceed to image prompts
- "Needs changes" — user provides feedback in the notes field
- "Try a different angle" — go back to Step 2
- "Scrap and start over" — ask for new input

If the user selects "Needs changes," revise the draft, output the full revised text again, and ask once more. Continue iterating until they approve.

## Step 4: Decide whether the post needs an image

Before generating prompts, make a judgement call: does this post actually benefit from an image?

**Skip images when:**
- The post is a short, punchy take that stands on its own (the text IS the content)
- Adding an image would feel like decoration, not evidence
- The post is a personal story or admission where an image would dilute the rawness
- There's no natural visual (no source to screenshot, no framework to diagram, no concept that needs illustration)

**Include images when:**
- The source material is a tweet/post worth screenshotting (the screenshot IS the hook)
- The argument has a visual structure (comparison, framework, data) that a diagram would clarify
- The concept is abstract enough that an illustration gives the reader an anchor

If you decide the post doesn't need an image, tell the user: "This post works better without an image — the text carries itself." Offer to generate prompts anyway if they want, then skip to Step 5.

If the post does benefit from an image, proceed below.

## Step 4b: Generate image prompts

Generate **3 image prompts** following the visual taste profile from `taste.md`.

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

Use these LinkedIn-optimized defaults:
- **Diagrams/infographics**: 1200x1200px (1:1) · PNG (sharp text, no compression artifacts)
- **AI illustrations**: 1200x627px (1.91:1) · PNG or JPG (landscape fills the feed well)
- **Screenshots**: capture at native resolution, crop to content · PNG (lossless)

Override the defaults when the content demands it (e.g., a tall flowchart might need 1080x1350 portrait).

### Show prompts and iterate

Present the 3 image prompts to the user using AskUserQuestion with options:
- "All good" — proceed to save
- "Revise prompts" — user provides feedback
- "Skip images" — save post without image prompts

If revising, iterate until approved.

## Step 5: Save draft

1. Check if a `drafts/` directory exists at the project root. If not, note that it will be created.
2. Generate a slug from the post's opening line: first 5-8 words, lowercased, hyphenated, max 50 chars.
3. Save to `drafts/YYYY-MM-DD-slug.md` using today's date.

### File format

```markdown
---
date: [today's date, YYYY-MM-DD]
source_urls:
  - [url1]
  - [url2]
angle: [one-line description of the chosen angle]
template: [short-form | long-form | article-promotion]
---

## Post

[the approved post text, exactly as approved — ready to copy-paste to LinkedIn]

## Image Prompts

### Option 1: [type — e.g., "Screenshot of source tweet"]
[prompt or screenshot instructions]

### Option 2: [type — e.g., "Diagram"]
[prompt]

### Option 3: [type — e.g., "AI illustration"]
[prompt]
```

If no URLs were used, omit the `source_urls` field.
If the user skipped images, omit the `## Image Prompts` section entirely.

## Step 6: Confirm completion

Tell the user:
- The draft has been saved to `drafts/[filename].md`
- Remind them the post text is ready to copy-paste
- If image prompts were included, remind them to generate the images
