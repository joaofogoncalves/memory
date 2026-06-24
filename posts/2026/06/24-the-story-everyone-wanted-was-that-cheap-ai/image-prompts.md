# Image Prompts

Chosen visual: **two of Anthropic's own study figures**, fetched directly from the announcement CDN and kept in their native palette (taste.md category 3 — external charts, untouched). Resized to 1440px long edge, saved as WebP:
- `media/image-1.webp` (lead / site thumbnail) — **Figure 5 "Expertise and how sessions end"** (verified success 15% novice → 33% expert; the gap held). Source: `https://www-cdn.anthropic.com/images/4zrzovbb/website/140578bc2523d4945c016d72e69628d2692228c8-1920x1080.png`
- `media/image-2.webp` — **Figure 3 "Claude does more per prompt for more expert users"** (4.9 actions/607 words → 11.7/3.2k). Source: `https://www-cdn.anthropic.com/images/4zrzovbb/website/a72b63aceab4eadb0baa5799a69cc3ff211e7462-1920x1080.png`

Original single-screenshot capture instructions retained below for reference.

## Option 1 (chosen): Screenshot of Anthropic's success-rate figure
Open https://www.anthropic.com/research/claude-code-expertise and find the figure showing verified session success rate by user expertise (novice ~15%, intermediate/expert ~28-33%). Screenshot just that chart.
- Crop tight to the figure itself: no browser chrome, no tab bar, no surrounding body text, no nav.
- Keep Anthropic's native palette — do NOT restyle into navy/teal. It's someone else's chart; share it as-is.
- If the figure is natively light-mode (Anthropic announcement cards usually are), leave it light-mode. Don't force dark mode on a light source.
- Center the chart with a little breathing room so the site's thumbnail crops don't clip axis labels.
- Save as `media/image-1.webp` (or PNG, lossless, then convert). Target ~1200px on the long edge.

## Option 2 (not chosen): Chart (bar) — success rate by expertise tier
On-brand bar chart, navy background + teal highlight on the expert bar. Spec:
```json
{
  "title": "The gap held",
  "subtitle": "Verified Claude Code session success rate, by user expertise (Anthropic, 400k sessions)",
  "unit": "%",
  "yMax": 40,
  "highlightIndex": 2,
  "bars": [
    { "label": "Novice", "value": 15 },
    { "label": "Intermediate", "value": 28 },
    { "label": "Expert", "value": 33 }
  ]
}
```
Render: `node charts/render.mjs --template bar --data media/bar.json --output media/image-1.webp --width 1200 --height 1200`

## Option 3 (not chosen): AI conceptual illustration
A painterly, editorial-register image of a rising skill-curve ridge where the distance between two climbers stays fixed even as the slope gets easier underfoot — "the tool got cheaper, the gap held." Muted, cinematic, NYT-Magazine register, dark base. No glossy-3D, no Midjourney-cyberpunk, no floating icons, no stock-photo aesthetic.
Format: 1440x900px (16:10) · PNG
