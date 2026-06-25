# Image Prompts

## Option 1 (chosen): article-card chart

Rendered via the `article-card` template from `charts/`. Surfaces the article's hero image (construction-site golden-hour photo) with title, subtitle, JG wordmark, and URL signature.

Spec: `media/article-card.json` · rendered to `media/image-1.webp`.

Re-render command:

```bash
node charts/render.mjs \
  --template article-card \
  --data posts/2026/05/2026-05-20-a-bad-deploy-is-legible/media/article-card.json \
  --asset hero=articles/2026/05/2026-05-20-building-the-road-to-production-again/media/hero.jpg \
  --output posts/2026/05/2026-05-20-a-bad-deploy-is-legible/media/image-1.webp \
  --width 1440 --height 900
```

## Option 2 (not used): painterly editorial illustration — mineral deposit in the pipes

Wide editorial scene of the inside of an industrial water main, lit by a single warm work lamp. Mineral scale encrusts the inner surface in thick, uneven layers — pale yellow and rust-colored deposits narrowing the bore visibly. One section cut away to reveal the cross-section. Painterly, slightly muted palette. Warm tungsten light against cool steel-blue shadows. No text overlay, no figures.

Avoid: cyberpunk lighting, glossy 3D-render, AI-art aesthetic, neon, brain-with-circuits, robot-arm imagery.

Format: 1440x900px (16:10) · PNG or JPG

## Option 3 (not used): re-use of road-then-now.webp

The article's existing feature-compare chart already shows the four-map / one-breaks asymmetry on-brand. Cheapest option, but duplicates what readers see inside the article.

Source: `articles/2026/05/2026-05-20-building-the-road-to-production-again/media/road-then-now.webp`
