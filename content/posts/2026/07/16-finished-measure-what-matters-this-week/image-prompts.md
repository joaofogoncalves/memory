# Image Prompts

**Chosen: Option 2 (evidence photo).** Take the photo and save it as `media/image-1.jpg` in this directory before posting. The other options are kept below as fallbacks.

## Option 1: Chart — feature-compare (fallback)
Render via: `node charts/render.mjs --template feature-compare --data <spec>.json --output media/image-1.webp --width 1600 --height 720`

```json
{
  "title": "OKRs are half a system",
  "subtitle": "What teams copy from Measure What Matters vs. what it runs on",
  "arrowLabel": "runs on",
  "left": {
    "label": "THE HALF TEAMS COPY",
    "title": "OKRs",
    "items": [
      "Quarterly objectives",
      "Measurable key results",
      "Public scoring",
      "Cascading alignment"
    ]
  },
  "right": {
    "label": "THE HALF TEAMS SKIP",
    "title": "CFRs",
    "items": [
      "Conversations: regular one-on-ones",
      "Feedback: while it's still useful",
      "Recognition: specific, never ceremonial",
      "The human system underneath"
    ]
  }
}
```

## Option 2: Evidence photo — your copy of the book (CHOSEN)
A phone photo of your physical copy of "Measure What Matters" — cover up, natural light, on your desk or next to your laptop. Crop tight to the book with breathing room for thumbnail crops, no clutter in frame. Unbranded, no overlay.
Format: native resolution, crop to content · JPG

## Option 3: AI editorial illustration (fallback)
A painterly editorial scene: a large, precise measuring instrument (a vintage balance scale or gauge) in the foreground, and behind it, softly lit, two figures in conversation at a small table. The machinery sharp, the humans warm. Muted moody palette, cinematic side light, NYT-Magazine register. No text in the image. Avoid glossy 3D renders, floating icons, bright pastels, and the default LinkedIn-AI aesthetic.
Format: 1440x900px (16:10) · PNG
