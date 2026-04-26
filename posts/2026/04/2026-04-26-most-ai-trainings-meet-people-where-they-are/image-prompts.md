# Image Prompts

## Option 1 (chosen): Diagram — visible vs actual curriculum

Rendered via `charts/` (`feature-compare` template, horizontal). Spec lives at `media/training-vs-requires.json`. Re-render command:

```bash
node charts/render.mjs --template feature-compare \
  --data posts/2026/04/2026-04-26-most-ai-trainings-meet-people-where-they-are/media/training-vs-requires.json \
  --output posts/2026/04/2026-04-26-most-ai-trainings-meet-people-where-they-are/media/image-1.webp \
  --width 900 --height 600
```

Output: `media/image-1.webp` (1800x1278 landscape, denser cards).

## Option 2: Editorial illustration — small task, vast invisible problem-space

An editorial illustration in painterly digital style. A person sits at a small desk in the foreground, brightly lit, working on a single visible task on their laptop screen. Behind them, vast and dimly lit, stretches an enormous abstract problem-space: branching decision trees, layered diagrams, half-built structures, all rendered in muted blues, grays, and deep indigos. The person is unaware of it. The contrast between the small lit foreground and the vast dim background is the point. Mood: NYT Magazine long-read opener, contemplative, slightly melancholy. No text in the image. No floating 3D icons, no glowing screens, no split-layout banners.

Format: 1440x900px (16:10) · PNG.

## Option 3: Editorial illustration — the amplifier metaphor

An editorial illustration in painterly digital style. A small figure in a warmly lit foreground speaks calmly into a microphone. The microphone connects to a colossal speaker stack that towers behind them, rendered in cool blues and deep teals. The sound coming out of the speakers is visualized as large, warped, distorted waveforms — the input was simple, but the amplification has made the output strange and unwieldy. The figure looks small, contained, and unbothered. Mood: editorial, painterly, slightly surreal, like a Wired feature opener. No text in the image. No floating 3D icons, no bright pastels.

Format: 1440x900px (16:10) · PNG.
