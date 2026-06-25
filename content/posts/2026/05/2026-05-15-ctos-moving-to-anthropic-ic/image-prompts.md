# Image Prompts

User picked: **Option 1 — `timeline` chart** (rendered natively via `charts/render.mjs`).

Rendered to `media/image-1.webp` from `media/timeline-cto-moves.json` using the `timeline` template at 1600×600. The March cluster (McCann + Bailis) is rendered as a span to avoid label collision; Krieger sits on a parallel "Internal" track since his move was Anthropic CPO → MTS rather than external CTO → MTS.

Re-render command:
```bash
node charts/render.mjs --template timeline \
  --data posts/2026/05/2026-05-15-ctos-moving-to-anthropic-ic/media/timeline-cto-moves.json \
  --output posts/2026/05/2026-05-15-ctos-moving-to-anthropic-ic/media/image-1.webp \
  --width 1600 --height 600
```

---

## Option 2 (not used): "Gradient of proximity" diagram

Custom dark-mode brand diagram visualizing the second-half thesis. Concentric rings on a deep navy (#0e131e) background. Innermost ring small and labeled "FRONTIER LAB" (the densest point). Around it, a second ring labeled "DEPLOYMENT-ADJACENT" (operators deploying frontier AI in production at large enterprises). Outside that, a fainter third ring labeled "AI-ASSISTED SaaS." Furthest out, a barely-visible fourth ring labeled "DEFAULT INDUSTRY." A single teal accent (#44d8f1) glows on the innermost ring; the others fade toward navy-grey. Monospace labels for the ring tags. Small sans-serif title at top: "PROXIMITY TO THE FRONTIER." Subtitle: "The gradient extends outward." JG joaofogoncalves.com wordmark bottom right in small mono. No people, no icons, no glossy 3D render, no neural-network background. Style: flat editorial diagram, like a Wired sidebar graphic.
Format: 1200x1200px (1:1) · PNG

## Option 3 (not used): "The wave" transition list diagram

Custom dark-mode brand diagram listing the five moves as transitions. Deep navy (#0e131e) background. Five horizontal rows: "[Former Title @ Company]" on the left, thin teal (#44d8f1) arrow in the middle, "MTS @ Anthropic" on the right. Order top to bottom: "Niki Parmar — Co-founder/CTO, Adept" (Dec 2024), "Henry Shi — Co-founder/CTO/COO, Super.com" (Jul 2025), "Mike Krieger — CPO, Anthropic" (Jan 2026), "Bryan McCann — Co-founder/CTO, You.com" (Mar 2026), "Peter Bailis — CTO, Workday" (Mar 2026). Dates in small monospace to the right of each row in muted grey. Title at top in bold sans-serif: "C-SUITE → MTS." Subtitle in mono: "Five moves in fifteen months." JG wordmark bottom right. No portraits, no logos, no glossy effects. One teal accent on the most recent row arrow only; the rest muted grey-blue. Flat, dense, brand-consistent.
Format: 1200x1200px (1:1) · PNG
