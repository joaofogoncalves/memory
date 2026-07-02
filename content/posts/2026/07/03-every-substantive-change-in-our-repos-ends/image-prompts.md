# Image Prompts

## Option 1: Chart — feature-compare (CHOSEN, rendered to media/image-1.webp)

Spec at `media/feature-compare.json`, rendered via:

```bash
node charts/render.mjs --template feature-compare \
  --data content/posts/2026/07/03-every-substantive-change-in-our-repos-ends/media/feature-compare.json \
  --output content/posts/2026/07/03-every-substantive-change-in-our-repos-ends/media/image-1.webp \
  --width 1150 --height 780
```

## Option 2: Terminal-log visual (evidence-style, not used)

A dark terminal window, tightly cropped with no browser chrome, showing the tail of a coding session: a few dimmed lines of diff/commit output, then the highlighted final prompt line in teal monospace: `> update the docs this change just made stale`. Below it, faint repeated instances of the same line from previous sessions scrolling into the dark, suggesting the habit. Deep navy background (#0e131e-adjacent), single teal accent on the live prompt line, monospace throughout, medium text density. Avoid fake UI clutter, emoji, or glowing sci-fi effects.
Format: 1200x1200px (1:1) · PNG

## Option 3: Painterly editorial illustration (not used)

A cinematic, painterly scene of a scaffolded building under construction at dusk, where a second, smaller structure of paper and bound volumes grows alongside it at exactly the same height, storey for storey — the archive rising with the building rather than being stacked afterward. Muted warm-and-slate palette, soft directional light, visible brushwork, NYT-Magazine register. No text in the image, no glossy 3D render, no cyberpunk neon, subject centered with breathing room for cropping.
Format: 1440x900px (16:10) · PNG or JPG
