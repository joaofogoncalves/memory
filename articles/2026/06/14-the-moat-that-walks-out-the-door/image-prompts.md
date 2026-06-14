# Image Prompts

## Hero Image — "the handover" (continues the engine-rig series)

Series continuity: part 1 = the gas-turbine engine alone in its steel test-rig; part 2 = the same rig with one technician working it; part 3 = the same rig with two technicians, knowledge passing between them. Same engine, same cool brushed-steel palette with a single warm amber work light, same cinematic-industrial photography.

Photorealistic industrial photograph, same series as the prior two: the same gas-turbine engine mounted in its steel test-rig, cool brushed-steel tones with a single warm amber work light. Two technicians work at the engine together — an older, experienced one standing slightly back, one hand gesturing at a component as he explains; a younger one leaning in with a tool, following the point. Plain work clothes, focused, mid-conversation. Shallow depth of field, 35mm, cinematic color grade, documentary style, the warm light falling on the handoff between them. Keep both figures centered with breathing room for cropping. Avoid: text or logos, clearly identifiable faces, glossy 3D-render look, neon/cyberpunk, illustration or painterly texture.

Format: 1440x900px (16:10) · JPG

After generating, save as `media/hero.jpg` and set `hero_image: media/hero.jpg` in the article frontmatter.

## Section: "What a runbook can't hold" — rendered chart (no AI generation)

Already rendered via the `charts/` module (feature-compare template), not an AI image:
- Spec: `media/runbook-vs-judgment.json`
- Output: `media/runbook-vs-judgment.webp` (referenced inline in the article)

To re-render after edits:

```bash
node charts/render.mjs --template feature-compare \
  --data articles/2026/06/12-the-moat-that-walks-out-the-door/media/runbook-vs-judgment.json \
  --output articles/2026/06/12-the-moat-that-walks-out-the-door/media/runbook-vs-judgment.webp \
  --width 1600 --height 720
```
