# Image Prompts

User selected Option 3 — quote-card (self-quote of the closing line).

## Option 1: Chart (`bar`) — release category breakdown

Render category breakdown of v1.2.0 changes (dependency bumps, security/CVEs, features, fixes, docs). JSON spec:

```json
{
  "title": "Bridgeport v1.2.0 — what shipped",
  "subtitle": "Most of it is the unsexy stuff",
  "unit": " items",
  "yMax": 14,
  "highlightIndex": 0,
  "bars": [
    {"label": "Dependency bumps", "value": 13},
    {"label": "Security / CVEs", "value": 4},
    {"label": "Features", "value": 3},
    {"label": "Fixes", "value": 3},
    {"label": "Docs", "value": 2}
  ]
}
```

Format: 1200×1200px (1:1) · WebP.

## Option 2: Custom diagram — image channel discipline

A minimalist diagram on a deep navy background (#0e131e), composed of three labeled columns from left to right: `:edge` (subtitle: "master builds"), `:latest` / `:stable` (subtitle: "tagged releases", highlighted in teal #44d8f1 as the focal change), and `:vX.Y.Z` / `:YYYYMMDDHH-sha` (subtitle: "immutable"). Title at top in clean sans-serif: "Bridgeport v1.2.0 — image channel discipline". Use monospace for tag names, sans-serif for descriptions. One thin teal connector line under the `:latest`/`:stable` column with a small label "now means released, not master". Bottom-right wordmark: "JG joaofogoncalves.com" in small mono. Sparse, lots of whitespace.

Format: 1200×1200px (1:1) · PNG.

## Option 3: `quote-card` — self-quote (SELECTED)

Rendered via `charts/render.mjs` with the JSON below. Avatar is `web/img/headshot.jpg`. Output written to `media/image-1.webp`.

```json
{
  "name": "João Gonçalves",
  "handle": "joaofogoncalves",
  "quote": "Open source tools live or die on whether someone keeps tightening the rough edges once the launch dopamine wears off."
}
```

Render command:

```bash
node charts/render.mjs --template quote-card \
  --data posts/2026/05/2026-05-21-shipped-bridgeport-v1-2-0-today/media/quote-card.json \
  --asset avatar=web/img/headshot.jpg \
  --output posts/2026/05/2026-05-21-shipped-bridgeport-v1-2-0-today/media/image-1.webp \
  --width 1600 --height 900
```

Format: 1600×900px (16:9) · WebP.
