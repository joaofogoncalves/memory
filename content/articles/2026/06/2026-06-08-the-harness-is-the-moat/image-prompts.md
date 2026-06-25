# Image Prompts

## Hero Image

A photorealistic wide shot inside a dim industrial engine test cell: a single jet turbine engine mounted and clamped into an elaborate steel test rig, wrapped in sensor cabling, hydraulic lines, restraint bars, and instrumentation. The engine sits dead center, polished and powerful, but it is dwarfed by the scaffolding, mounts, and wiring that hold it and measure it. Shot on a 35mm lens, shallow depth of field falling off toward the edges, cold blue-grey industrial light with one warm sodium work-lamp raking across the rig. Documentary register, Edward Burtynsky / Wired-feature mood, muted desaturated palette, matte finish, no glossy CGI sheen. The structure around the engine is the subject, not the engine. No text, no logos, no people.

Format: 1440x900px (16:10) · JPG

Concept: the engine is the model (the impressive commodity everyone benchmarks); the rig that holds, restrains, and measures it is the harness (the thing that actually makes it usable). Keep the engine centered with breathing room so thumbnail crops stay clean.

---

## Section diagrams (rendered charts, not AI images)

All three section visuals are rendered charts from JSON specs via `charts/render.mjs`, in the navy + teal studio palette with the JG wordmark. No AI image needed for any of these slots.

### §2 "What a harness actually is" — `model-one-stage.webp` (template `flow`)

The model is the single teal-highlighted stage ("Model writes code"); the surrounding stages and gate labels are the harness.

### §6 "Won't the model just eat the harness?" — `harness-depreciation.webp` (template `line`)

Two lines cross: as model capability rises across Opus 4.5 → 4.6 → 4.8, the scaffolding the model still needs falls away (teal). Illustrative; the documented anchor is the 4.5 → 4.6 step (context resets + sprint decomposition removed, $200 → $124). Carries the depreciation thesis as a shape.

```bash
node charts/render.mjs --template line \
  --data articles/2026/06/2026-06-05-the-harness-is-the-moat/media/harness-depreciation.json \
  --output articles/2026/06/2026-06-05-the-harness-is-the-moat/media/harness-depreciation.webp \
  --width 1600 --height 900 --scale 2
```

### §6 payoff (before "What you actually own") — `rented-vs-owned.webp` (template `feature-compare`)

Left card (muted): the rented, commoditizing generic loop — agent loop, sandboxes, session state — now sold as Managed Agents. Right card (teal): the owned half that is the moat — your deploy gates, domain verification, failure history, and the skill of re-deriving the harness when the model moves. Arrow labelled "where the moat sits" points right.

```bash
node charts/render.mjs --template feature-compare \
  --data articles/2026/06/2026-06-05-the-harness-is-the-moat/media/rented-vs-owned.json \
  --output articles/2026/06/2026-06-05-the-harness-is-the-moat/media/rented-vs-owned.webp \
  --width 1600 --height 820 --scale 2
```
