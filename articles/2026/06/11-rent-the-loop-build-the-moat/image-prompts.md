# Image Prompts

## Hero Image

A photorealistic wide shot inside the same dim industrial engine test cell as part one ("The Harness Is the Moat"): the jet turbine still clamped in its steel test rig, but now a single technician in work clothes is mid-task on the scaffolding, reaching into the cabling, reading an instrumentation panel, adjusting a mount. The rig and the person are the subject. The engine sits behind them, unchanged. 35mm lens, shallow depth of field, cold blue-grey industrial light with one warm sodium work-lamp raking across the worker's hands and the panel. Edward Burtynsky / Wired documentary mood, muted desaturated palette, matte finish, no glossy CGI sheen. Face away or obscured, not a portrait. No text, no logos. Subject centered with breathing room for thumbnail cropping.

Format: 1440x900px (16:10) · JPG

Concept: deliberate series continuity with part one's hero. Same engine test cell, same Burtynsky / Wired register, same cold-blue plus warm-lamp lighting. Part one showed the engine dwarfed by the rig (the system); part two shifts focus to the human working the rig, which is the re-derivation cadence and the close, "it lives in the team, not the repo." Introducing a figure in part two is the intended progression from part one's empty cell. Hero is off the site's navy + teal palette by design.

(Superseded: the earlier draft prompt for this slot was a craftsman's tool-wall. Replaced for series visual continuity with part one.)

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
