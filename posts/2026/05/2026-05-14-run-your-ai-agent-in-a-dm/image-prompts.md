# Image Prompts

## Option 1 (chosen): Article-card chart

Renders via `charts/` module — on-brand article-promo card with the article's hero image, title, subtitle, JG wordmark and canonical URL. Replaces Substack/LinkedIn auto-cards so the canonical visual lives in the repo.

Spec: `media/article-card.json`
Hero asset: `articles/2026/05/2026-05-14-lead-time-is-the-wrong-half/media/hero.png`
Output: `media/image-1.webp` (1440x900px, 16:10, webp — matches the site's universal hero ratio so the card crops cleanly across LinkedIn, X, and the homepage spotlight)

Render command:
```bash
node charts/render.mjs --template article-card \
  --data posts/2026/05/2026-05-14-run-your-ai-agent-in-a-dm/media/article-card.json \
  --output posts/2026/05/2026-05-14-run-your-ai-agent-in-a-dm/media/image-1.webp \
  --asset hero=articles/2026/05/2026-05-14-lead-time-is-the-wrong-half/media/hero.png \
  --width 1440 --height 900
```

## Option 2 (not chosen): Feature-compare chart

Private agent vs public agent contrast — the post's actual argument as a side-by-side. Left column: "DM, IDE sidebar, Cursor session" with rows on individual gain; right column: "Slack channel, no DMs" with rows on org-level compounding. Format: 1200x1200px (1:1) · webp.

## Option 3 (not chosen): Tobi/River tweet screenshot

Tight dark-mode crop of Tobi Lütke's tweet about Shopify's River agent (https://x.com/tobi/status/2053121182044451016). No browser chrome, no UI overlays. Anchors the "Shopify built theirs at 5000 engineers" line. Format: native resolution, cropped to content · PNG.
