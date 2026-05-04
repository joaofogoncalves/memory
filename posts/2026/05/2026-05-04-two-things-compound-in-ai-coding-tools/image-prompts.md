# Image Prompts

## Option 1: Article-card (chart spec) — chosen

Standard article-promo card with the canyon hero, title, subtitle, and auto-stamped logo & URL signature. Spec saved to `media/image-1.json`. Rendered to `media/image-1.webp`.

Render command:

```bash
node charts/render.mjs --template article-card \
  --data posts/2026/05/2026-05-04-two-things-compound-in-ai-coding-tools/media/image-1.json \
  --asset hero=articles/2026/05/2026-05-04-ai-as-the-great-filter/media/hero.png \
  --output posts/2026/05/2026-05-04-two-things-compound-in-ai-coding-tools/media/image-1.webp \
  --width 1440 --height 900
```

## Option 2: feature-compare diagram (not chosen)

Two-mechanism side-by-side: sycophancy vs variable-ratio reinforcement, with a "Compound" arrow between them. Lands the post's argument visually.

## Option 3: AI illustration — slot machine with code on the reels (not chosen)

Tech-noir editorial illustration: vintage three-reel slot machine with code fragments on the reels, late-night dimly-lit room, dark navy and deep teal lighting, film-noir aesthetic. References Edward Hopper and Roger Deakins.
