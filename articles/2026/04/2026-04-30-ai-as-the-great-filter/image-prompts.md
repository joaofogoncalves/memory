# Image Prompts

## Hero Image

Wide cinematic landscape photograph of a long narrow mountain pass at late dusk, shot from elevation looking down the length of the corridor. The pass cuts a single thin channel between two enormous walls of weathered rock that rise sharply on both sides; the cliff faces are dark, geological, layered, deeply shadowed. The corridor floor is a pale dry-riverbed strip of cracked earth and stone running into the distance, narrowing toward a single small opening at the vanishing point where the last cold daylight breaks through. Threading along the riverbed, small and unhurried, is a thin scattered line of human silhouettes walking forward — perhaps eight or ten figures spaced unevenly, dignified in posture, none in groups. Some are mid-stride, one or two have stopped. They are tiny against the scale of the cliffs. Faint dust hangs in the air. The sky is a slate-blue gradient deepening toward indigo at the top of the frame, with a single cool sliver of pale gold light at the far end of the pass.

Cinematic colour grade: deep cold slate-blue and bluish-grey across the cliff walls, warm gold-amber pinhole at the far vanishing point, the riverbed neutral with cool shadows. Wide-angle lens (equivalent ~24–28mm) to emphasise the scale of the walls and the smallness of the figures. Sharp focus along the corridor; the cliff tops fall into atmospheric haze. Subtle film grain, slight lens compression, no lens flare. The composition is centred and symmetrical so the pass and its single end-of-tunnel light land cleanly in the centre of the frame across 16:10 spotlight, full-width × 220px archive cards, and 300×175 list cards.

References: Sebastião Salgado *Genesis*-era monumental landscape photography, Edward Burtynsky industrial-scale geological work, Reuben Wu's *Lux Noctis* night-landscape series, Roger Deakins cinematography (*Sicario* desert sequences, *Blade Runner 2049* canyon shots), Andreas Gursky's *Rhine II*-style horizontal calm. Documentary, not painterly. Real place, photographed with intent.

Avoid: glowing portals, neon or cyberpunk palettes, sci-fi overlays, painterly or illustrated rendering, hand-drawn look, 3D render gloss, motivational colour grading, lens flare kitsch, hero figures in the foreground, faces, recognisable clothing details, modern signage, AI-generated "glowing tech" aesthetic, anything that reads as fantasy concept art. The image should feel like a photograph of a real geological pass at the moment of selection — quiet, vast, indifferent.

Communicates: the Great Filter as a real geological narrowing — most never make it through, the survivors are unremarkable in the moment, and the selection is silent.

Format: 1440×900px (16:10) · JPG
Target path: `media/hero.jpg`

## Inline Visual (line chart)

The conceptual heart of the piece — two engineer trajectories using AI, identical output for ~6 months, then divergence — rendered as a `line` chart.

- Template: `line`
- Spec: `media/two-trajectories.json`
- Output: `media/two-trajectories.webp`
- Title: "The selection happens in the gap"
- Subtitle: "Two engineers using AI — output looks identical, until it doesn't."
- Series 1 (cyan `#44d8f1`): "AI as force multiplier on depth" — climbs steadily through Month 13.
- Series 2 (coral `#ff8a9e`): "AI as substitute for depth" — tracks identically through Month 7, peaks at Month 9, collapses by Month 13.
- Caption: clarifies the y-axis is illustrative ("real value shipped — code the engineer can defend, debug, and extend").
- Anchor: inside **The filter is selection, not extinction**, immediately after "And only one of them can fix it."

Render command:

```bash
node charts/render.mjs --template line \
  --data articles/2026/04/2026-04-30-ai-as-the-great-filter/media/two-trajectories.json \
  --output articles/2026/04/2026-04-30-ai-as-the-great-filter/media/two-trajectories.webp \
  --width 1600 --height 900
```

Why this chart, not a sycophancy stat-compare: the sycophancy data lands fine in prose with citations. The two-trajectories shape is the thesis — externalising it as a single image gives the piece a screenshot-shareable visual that does work the prose can't. Distinct from the hero (canyon = the filter; chart = the divergence inside it).
