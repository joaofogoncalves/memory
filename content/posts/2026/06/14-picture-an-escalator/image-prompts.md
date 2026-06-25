# Image Prompts

Chosen visual: **Option 1 — quadrant chart** (rendered via the charts module to `media/image-1.webp`).

## Option 1: Quadrant chart (CHOSEN — rendered, 1600x900 wide)
Template: `quadrant`. Effort (x) × the escalator / AI (y). Per-quadrant `tone` set in the
spec: Climbing = `good` (teal, the only way ahead), Refusing = `bad` (coral, the worst
corner), Standing and The stairs = `neutral`. Subtitle dropped for mobile legibility; the
template now centers each quadrant's title + description and auto-hides an empty subtitle.
Spec saved at `media/escalator-quadrant.json`.

Render command:
```bash
node charts/render.mjs \
  --template quadrant \
  --data posts/2026/06/14-picture-an-escalator/media/escalator-quadrant.json \
  --output posts/2026/06/14-picture-an-escalator/media/image-1.webp \
  --width 1600 --height 900 --scale 2
```

## Option 2: "Standing vs Climbing" compare card (not used)
Template: `feature-compare`. Drops the full taxonomy and zeroes in on the post's landing —
the two options that matter once everyone is already on the escalator. Two cards (STAND |
CLIMB) with outcome bullets and an arrow labelled "the gap that matters". On-brand alternative.

## Option 3: Editorial illustration (not used — off the usual post-taste)
`taste.md` reserves AI illustrations for article heroes, so this was the weakest fit for a post.
Prompt, if ever wanted: A long escalator rising through a dark, cavernous transit hall,
cinematic wide frame. Most figures stand passively on the moving steps, evenly spaced, faces
lit by a cool ambient glow, all rising at the same rate. One lone figure climbs the steps two
at a time, caught mid-stride with a touch of motion blur, pulling clearly ahead of the standers
and the few people trudging up the static stairs to the side. Muted, moody palette: deep
blue-grey shadows with a single warm shaft of light from the top falling on the climber.
Painterly editorial style, Wired / NYT-Magazine long-read register, fine grain, soft focus at
the edges. No text, no logos, no signage. Avoid glossy 3D renders, neon cyberpunk, and clean
stock-photo lighting.
Format: 1440x900px (16:10) · JPG
