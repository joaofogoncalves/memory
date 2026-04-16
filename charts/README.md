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

## CLI flags

| flag | default | notes |
|---|---|---|
| `--template` | — | Template name (`bar`, `stat-compare`, `quadrant`, `line`) or path to `.html` |
| `--data`     | — | Path to JSON file |
| `--output`   | — | `.webp` → quality 95, `.png` → lossless |
| `--width`    | 1600 | Viewport width |
| `--height`   | 900 | Viewport height |
| `--scale`    | 2 | `deviceScaleFactor` (retina) |

## Theme

Shared palette, typography, and spacing live in `theme.js`. Import it from Node:

```js
import theme, { toCSSVars } from './charts/theme.js';
```

Or inline `toCSSVars()` into new templates to stay visually consistent.
