# charts/

Generate article visuals as `.webp` / `.png` files from JSON data.

Templates are standalone HTML that read their payload from `window.__DATA__`. A Playwright renderer injects the data, waits for fonts + Chart.js to settle, then screenshots `#chart-container`.

## Setup

```bash
npm install
npx playwright install chromium
```

## Render a chart

```bash
node charts/render.mjs \
  --template bar \
  --data charts/examples/adoption-gap.json \
  --output charts/out/adoption-gap.webp \
  --width 1600 --height 900 --scale 2
```

Or via the npm script:

```bash
npm run chart -- --template bar \
  --data charts/examples/adoption-gap.json \
  --output charts/out/adoption-gap.webp
```

## Templates

### `bar` — adoption funnel / descending comparison

```bash
node charts/render.mjs \
  --template bar \
  --data charts/examples/adoption-gap.json \
  --output charts/out/adoption-gap.webp
```

Data shape: `{ title, subtitle, unit, yMax, highlightIndex, bars: [{label, value}] }`

### `stat-compare` — two big numbers with arrow

```bash
node charts/render.mjs \
  --template stat-compare \
  --data charts/examples/access-vs-maturity.json \
  --output charts/out/access-vs-maturity.webp
```

Data shape: `{ title, subtitle, arrowLabel, left: {label, value, description}, right: {...} }`

### `quadrant` — 2×2 framing diagram (inline SVG)

```bash
node charts/render.mjs \
  --template quadrant \
  --data charts/examples/quadrant-ai-maturity.json \
  --output charts/out/quadrant-ai-maturity.webp
```

Data shape: `{ title, subtitle, xAxis: {low, high, title}, yAxis: {...}, quadrants: {tl, tr, bl, br} }`

### `feature-compare` — two cards with label + bullet list, optional arrow

```bash
node charts/render.mjs --template feature-compare \
  --data <spec>.json --output <name>.webp --width 1600 --height 720
```

Data shape: `{ title, subtitle, arrowLabel, left: {label, title, items: [...]}, right: {...} }`

### `grid-diff` — before/after grid of labeled cards, new items highlighted

```bash
node charts/render.mjs --template grid-diff \
  --data <spec>.json --output <name>.webp --width 1800 --height 900
```

Data shape: `{ title, subtitle, columns, left: {header, count, items: [...]}, right: {...} }`. Items are strings or `{label, note?, isNew?}`.

### `flow` — horizontal pipeline with optional parallel tracks and gate labels

```bash
node charts/render.mjs \
  --template flow \
  --data charts/examples/pipeline-flow.json \
  --output charts/out/pipeline-flow.webp \
  --width 2160 --height 900
```

Data shape: `{ title, subtitle, tracks: [{label, stages: [...]}], gates: [{afterIndex, label}], highlightStageIndex }`

### `timeline` — stacked tracks with point or span events along a time or date axis

```bash
node charts/render.mjs \
  --template timeline \
  --data charts/examples/day-in-life.json \
  --output charts/out/day-in-life.webp \
  --width 2400 --height 900
```

Data shape:
```jsonc
{
  "title": "...",
  "timeAxis": {
    "type": "time",              // or "date"
    "start": "08:00",            // HH:MM for time, YYYY-MM-DD for date
    "end": "18:00",
    "ticks": [{ "at": "10:00", "label": "10:00" }, ...]
  },
  "tracks": [{
    "label": "Sensors",
    "color": "#44d8f1",
    "events": [
      { "at": "08:14", "label": "creates #2847", "timeLabel": "08:14" },
      { "from": "09:02", "to": "09:43", "label": "/pick → /build" },
      { "at": "10:11", "label": "approve", "shape": "check" }
    ]
  }]
}
```

For few-track timelines, drop `--height` to ~500 to avoid large vertical whitespace.

### `line` — multi-series trend

```bash
node charts/render.mjs \
  --template line \
  --data charts/examples/adoption-over-time.json \
  --output charts/out/adoption-over-time.webp
```

Data shape: `{ title, subtitle, unit, labels: [...], series: [{label, values, color}] }`

### `article-card` — promo card for article launches (hero + title + subtitle)

Substack-style social card. Hero image as background with a darkening scrim, eyebrow tag + title + subtitle bottom-left, logo + URL signature bottom-right (auto-stamped by the renderer). Render at **1440×900** (16:10) to match the site's universal hero ratio so the card crops cleanly across LinkedIn, X, and the homepage spotlight.

```bash
node charts/render.mjs \
  --template article-card \
  --data charts/examples/article-card-experience-tax.json \
  --asset hero=articles/2026/04/2026-04-28-experience-isnt-the-tax-identity-is/media/hero.jpg \
  --output charts/out/article-card-experience-tax.webp \
  --width 1440 --height 900
```

Data shape: `{ eyebrow?, title, subtitle? }`. The hero image is passed via `--asset hero=<path>` (the renderer inlines it as a data URL, so the path resolves at render time, not in the data file). Title font size auto-adapts to length (3 stops). Use this for short-form promo posts that drive readers to a published article — replaces Substack's auto-generated card so the canonical visual lives in the repo.

### `quote-card` — original pull-quote card

Use when the post is a quote and you don't have a clean source screenshot (your own line, or someone else's line you don't want to screenshot). Big display-font pull-quote with attribution, optional eyebrow context, faint quote-mark glyph as a visual anchor. **1440×900** to fit the site ratio.

```bash
node charts/render.mjs \
  --template quote-card \
  --data charts/examples/quote-card-identity-weight.json \
  --output charts/out/quote-card-identity-weight.webp \
  --width 1440 --height 900
```

Data shape: `{ quote, attribution?, source?, context? }`. Quote font size auto-adapts to length across 5 stops (≤80, ≤140, ≤220, ≤320, longer). Wrap your quote in straight `"..."` if you want to override the auto-applied curly quotes. `source` is the small fade after the attribution name — use it for venue/url (e.g. `joaofogoncalves.com`, `On X · 2026-04`).

## CLI flags

| flag | default | notes |
|---|---|---|
| `--template` | — | Template name (`bar`, `stat-compare`, `quadrant`, `line`, `article-card`, `quote-card`, ...) or path to `.html` |
| `--data`     | — | Path to JSON file |
| `--output`   | — | `.webp` → quality 95, `.png` → lossless |
| `--width`    | 1600 | Viewport width |
| `--height`   | 900 | Viewport height |
| `--scale`    | 2 | `deviceScaleFactor` (retina) |
| `--transparent` | false | Drops the dark surface. Charts render with transparent background (text stays light — use only over dark composites). |
| `--no-signature` | false | Skip the auto-stamped logo + URL in the bottom-right. |
| `--asset`    | — | Inline a file as a data URL under `window.__DATA__.assets[KEY]`. Format: `KEY=PATH` (repeatable). Used by `article-card` for the hero image. |

## Theme

Shared palette, typography, and spacing live in `theme.js`. Import it from Node:

```js
import theme, { toCSSVars } from './charts/theme.js';
```

Or inline `toCSSVars()` into new templates to stay visually consistent.
