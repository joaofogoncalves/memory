# Image Prompts

## Hero Image

A photorealistic wide shot of a working craftsman's tool wall at the end of the day: a French-cleat wall hung with dozens of well-used hand tools, each in its own painted outline so the empty spaces read as clearly as the filled ones. One outline near the center is empty, its tool still in use off-frame. Low warm work-lamp light rakes across from the left, catching worn wooden handles, steel, and brass, deep shadows pooling between the tools. Shot on a 35mm lens at f/2, shallow depth of field falling off toward the edges, documentary register, muted warm palette of aged wood and metal, matte finish, no glossy sheen. The wall reads as a system someone built and maintains, not a store display. No text, no logos, no people, no hands. Centered composition with breathing room at the edges for thumbnail cropping.

Format: 1440x900px (16:10) · JPG

Concept: the owned, maintained layer. Every tool earned its outline (the skills-as-a-ledger-of-failures idea); the empty slot is the gate currently in your hand (the re-derivation cadence). Off-palette and warm, contrasting the rented, disposable loop. Heroes are not bound by the site's navy + teal scheme.

---

## Section diagram (already rendered — flow chart)

The §4 visual ("The week a model ships") is a rendered chart, not an AI image:
`media/re-derivation-cadence.webp` (spec: `media/re-derivation-cadence.json`, template `flow`).

Five-stage horizontal flow — Model ships → Audit the bets → Delete dead gates → Hunt the new edge → Re-baseline — with "Hunt the new edge" as the single teal-highlighted stage. No AI image needed for this slot.

```bash
node charts/render.mjs --template flow \
  --data articles/2026/06/2026-06-08-rent-the-loop-build-the-moat/media/re-derivation-cadence.json \
  --output articles/2026/06/2026-06-08-rent-the-loop-build-the-moat/media/re-derivation-cadence.webp \
  --width 1900 --height 600 --scale 2
```
