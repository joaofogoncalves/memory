Analyze the user's LinkedIn post images and generate a visual taste profile. Uses batch processing with cached descriptions to handle large image sets efficiently.

## Arguments

Parse `$ARGUMENTS` for:
1. **Day window**: first number found (default: 60)
2. **Batch size**: number after `--batch` flag (default: 10)

Examples: `$ARGUMENTS` = "" -> 60 days, 10 batch. "90" -> 90 days, 10 batch. "60 --batch 20" -> 60 days, 20 batch. "--batch 5" -> 60 days, 5 batch.

## Step 1: Discover posts with images

1. Glob `posts/**/post.md` to find all posts.
2. Glob `posts/**/media/image-*.jpg` to find all images.
3. Read each post's YAML frontmatter to get `date`, `post_type`, and check for existing `media_descriptions`.
4. **Filter posts** the same way as `/profile`:
   - Include: `post_type: original` or `post_type: article`
   - Include: reposts only if they have user commentary (text before `## Repost`)
   - Exclude: pure reposts, empty posts
5. Match images to their qualifying posts (images live in `media/` subdirectory of each post).
6. Build two lists:
   - `already_described`: images whose post has a `media_descriptions` entry for that filename
   - `needs_description`: images without a cached description

Apply tiered recency (same cutoff as `/profile`): prioritize Tier 1 (current window) images in the `needs_description` queue.

**Report the inventory** to the user: "Found X images across Y qualifying posts. Z already have cached descriptions, W need processing."

## Step 2: Batch process uncached images

If `needs_description` is empty, skip to Step 4.

Take the first `--batch N` images from `needs_description` (Tier 1 images first, then Tier 2 by date descending).

For each image:
1. **Read the image file** using the Read tool (it supports images natively).
2. Also read the corresponding post's text content for context.
3. **Generate a description** (2-3 sentences) covering:
   - What the image depicts (subject, context)
   - Visual style (screenshot, chart, infographic, photo, meme, diagram, etc.)
   - Composition (text-heavy, image-heavy, mixed, aspect ratio feel)
   - Notable visual characteristics (colors, branding, platform UI if screenshot)
   - If text is visible in the image, note what it says (briefly)

Process images in parallel where possible (read multiple images in one turn).

## Step 3: Write descriptions to frontmatter

For each processed image, update the corresponding post's YAML frontmatter to add or extend the `media_descriptions` field.

**Before:**
```yaml
---
date: 2026-03-26
post_url: https://...
post_type: original
archived_at: 2026-03-27
---
```

**After:**
```yaml
---
date: 2026-03-26
post_url: https://...
post_type: original
archived_at: 2026-03-27
media_descriptions:
  image-1.jpg: >-
    Screenshot of a LinkedIn post about AI adoption by a tech CEO.
    Dark mode interface showing text-heavy content with engagement
    metrics visible. Corporate tone, no images within the post.
---
```

**Important:**
- Use YAML block scalar `>-` for multi-line descriptions
- Preserve ALL existing frontmatter fields exactly as they are
- If `media_descriptions` already exists (from a previous run), add new entries without overwriting existing ones
- Use the Edit tool to modify only the frontmatter section of each post

## Step 4: Report progress or generate taste.md

Count how many images now have descriptions (cached + just processed) vs total.

**If less than 80% of images are described:**
Report to the user:
- "Processed [N] images this run. Total: [described]/[total] images have descriptions ([percent]%)."
- "Run `/taste` again to process more. Or `/taste --batch 50` to process more at once."
- Do NOT generate taste.md yet — not enough data.

**If 80% or more are described:**
Proceed to synthesis.

## Step 5: Generate taste.md (only when >= 80% described)

Read all cached `media_descriptions` from qualifying posts (re-read the frontmatter).

Apply tiered recency weighting:
- Calculate cutoff date from the day window argument
- Tier 1 (current window) descriptions get priority in the analysis
- If a visual pattern appears only in Tier 2, note it as "historical"

Analyze the descriptions for patterns and write `taste.md` to the project root.

**Output structure:**

```markdown
# Visual Taste Profile

You share images on LinkedIn that follow these patterns. Use this guide when selecting or creating images for posts.

## Image Types
[Distribution and preference: what percentage are screenshots, charts, photos, etc.]
[Which types appear most in recent posts]

## Visual Composition
[Text density: heavy, moderate, minimal]
[Layout patterns: full-width screenshots, cropped sections, etc.]
[Color tendencies: dark mode, light mode, branded colors]

## Subject Matter
[What the images depict — match content topics]
[Relationship between image and post text]

## Platform and Source Patterns
[Where screenshots come from: LinkedIn, Twitter, articles, etc.]
[Any recurring sources or formats]

## Branding and Consistency
[Recurring visual elements if any]
[Consistency level: highly curated vs organic/varied]

## What NOT To Share
[Anti-patterns: generic stock photos, AI-generated art, overly polished graphics, etc.]
[Visual styles that would feel off-brand]

---
Generated from [N] image descriptions ([M] in current window of [X] days)
[P] images unprocessed (if any)
Last updated: [today's date]
```

**Rules:**
- Every line is a directive ("Share screenshots of real conversations, not polished graphics")
- Keep under ~100 lines
- Include anti-patterns section
- Note the generation metadata

## Step 6: Confirm completion

Tell the user:
- How many images were processed this run
- Total description coverage (described / total)
- Whether taste.md was generated or more runs needed
- If taste.md was generated, suggest combining it with profile.md for a complete profile
