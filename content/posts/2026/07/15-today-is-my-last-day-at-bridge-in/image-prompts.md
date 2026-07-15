# Image Prompts

Recommendation: **Option 1**. A farewell post is a raw personal post — a real photo carries it better than anything generated. Options 2 and 3 are fallbacks if no photo exists.

## Option 1: Real photo (recommended)

Not a generation prompt. Attach a genuine photo: the team, the office, the last-day desk, or the whiteboard from the handover sessions. Candid beats posed; the post's directness is the point and a real photo matches it. Crop to landscape if possible.
Format: native resolution, crop to content · JPG/PNG

## Option 2: Article card (chart renderer — fallback, spec saved)

Render the on-brand article card for the linked piece (spec at `media/article-card.json`), using the article's hero as the card image:

```bash
node charts/render.mjs --template article-card \
  --data content/posts/2026/07/15-today-is-my-last-day-at-bridge-in/media/article-card.json \
  --asset hero=content/articles/2026/07/15-i-offboarded-myself-with-ai/media/hero.jpg \
  --output content/posts/2026/07/15-today-is-my-last-day-at-bridge-in/media/image-1.webp
```

Format: template default (wide) · WEBP

## Option 3: AI illustration (conceptual)

A painterly editorial illustration of a figure walking out of a dim, warm-lit office at dusk carrying nothing, while behind them a wall of small glowing teal terminal windows keeps working — dozens of tiny processes still running in an otherwise empty room. Mood: quiet, unsentimental, slightly wry; think NYT Magazine long-read opener, muted navy and amber palette with teal accents from the screens. No text in the image, no floating 3D icons, no split-layout banner composition, no bright pastels.
Format: 1440x900px (16:10) · PNG
