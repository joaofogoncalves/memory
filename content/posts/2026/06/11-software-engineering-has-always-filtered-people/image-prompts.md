# Image Prompts

All three options were on-brand `charts/` renders rather than AI illustrations — `taste.md` reserves AI-generated imagery for editorial article heroes only, and this is a thesis post.

## Option 1 (USED): `feature-compare` — the two filters, side by side
Rendered to `media/image-1.webp` from `media/the-filter-moved.json`.

```bash
node charts/render.mjs --template feature-compare \
  --data posts/2026/06/2026-06-11-software-engineering-has-always-filtered-people/media/the-filter-moved.json \
  --output posts/2026/06/2026-06-11-software-engineering-has-always-filtered-people/media/image-1.webp \
  --width 1360 --height 720
```

Rendered horizontal at 1360×720. Uses asymmetric card widths via `leftFlex: 0.62` / `rightFlex: 1.0` in the spec (new optional fields added to `charts/templates/feature-compare.html` — default stays 1fr/1fr, so other charts are unaffected). The narrow left card hugs its short bullets; the wider right card fits "Can you reason about the whole system?" on one line.

Left card "OLD FILTER / Can you write the code?" (syntax fluency, compile/run, framework recall, debug line by line) → arrow "moved" → right card "NEW FILTER / Can you reason about the whole system?" (idea to running, deploy/scale/fail at 3am, attack surface & blast radius, taste & product sense). Note: the last left-card item was changed from "the part the models close" to "Debug it line by line" so the old filter lists concrete manual craft, not meta-commentary about models.

## Option 2 (not used): `grid-diff` — what the models close vs what they don't
Two columns: "MODELS CLOSE THIS" (writing syntax, compile, run, framework recall) vs "THEY DON'T CLOSE THIS" (idea to production, deploy/scale/fail, attack surface/blast radius, taste & product sense — all flagged `isNew`). Render `--width 1600 --height 900`.

## Option 3 (not used): `quote-card` — the closing line as a branded pull-quote
Quote: "The field still sorts people. It just stopped sorting on the part that got cheap." Name João Gonçalves, handle @joaofogoncalves, avatar `web/img/headshot.jpg`. Render `--width 1440 --height 900`. Text-forward, no diagram.
