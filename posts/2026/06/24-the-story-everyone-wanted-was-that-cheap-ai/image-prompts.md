# Image Prompts

Chosen visual: **screenshot** of Anthropic's own success-rate-by-expertise figure (taste.md category 3 — external chart in its native palette, kept untouched). Save the final crop to `media/image-1.webp`.

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
