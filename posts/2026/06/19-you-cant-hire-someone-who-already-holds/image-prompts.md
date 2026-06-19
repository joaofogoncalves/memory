# Image options

Single-image post. Chosen: **Option 1 — article-card** (rendered to `media/image-1.webp`).

## Option 1 (chosen): article-card — promo card for the article
Real painterly hero from the article + title + subtitle + auto JG/URL wordmark. Canonical article-promo visual that replaces Substack's auto-card.

Spec: `media/article-card.json`
Render:
```bash
node charts/render.mjs --template article-card \
  --data posts/2026/06/19-you-cant-hire-someone-who-already-holds/media/article-card.json \
  --asset hero=articles/2026/06/14-the-moat-that-walks-out-the-door/media/hero.jpg \
  --output posts/2026/06/19-you-cant-hire-someone-who-already-holds/media/image-1.webp \
  --width 1440 --height 900
```

## Option 2 (not used): line chart — "Same start. Different slope."
Two hires, identical résumés, both at zero on day one; one steep (high absorption rate), one shallow. One teal accent on the fast line. The angle rendered literally as shape.
```json
{
  "template": "line",
  "title": "Same start. Different slope.",
  "subtitle": "How much of your team's judgment a new hire holds, by month.",
  "unit": "%",
  "caption": "Illustrative. Identical résumés, different absorption rate.",
  "labels": ["Day 1", "Month 1", "Month 3", "Month 6", "Month 12"],
  "series": [
    { "label": "High slope (absorbs fast)", "values": [0, 25, 55, 80, 95], "color": "#44d8f1" },
    { "label": "Low slope (absorbs slow)",  "values": [0, 8, 18, 30, 45], "color": "#5b6b7a" }
  ]
}
```
1200×1200

## Option 3 (not used): feature-compare — "Inventory vs Slope"
Left card "Inventory — what loops score" (deep judgment about systems that aren't yours · reads fast because it's recognition · sits on the résumé). Right card, teal-accented, "Slope — what compounds the moat" (absorbs your ledger in weeks · re-derives as the model moves · gets faster on your surface). Arrow left→right.
1200×1200
