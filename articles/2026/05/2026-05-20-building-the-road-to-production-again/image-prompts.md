# Image Prompts

## Hero Image

Wide aerial shot of a major highway interchange under construction at golden hour. The road's skeleton is visible: concrete piers, exposed rebar, half-poured ramps curving away into a hazy landscape. Empty of people but full of the marks of work just done — construction equipment parked along the edges, formwork still in place around the unfinished bridge deck. Documentary photography style, shot from a high angle with a wide-angle lens. Warm earth tones and amber light, low sun raking across the structures, slight atmospheric haze in the distance giving depth.

Composition: keep the interchange centered with breathing room around it so thumbnail crops at multiple aspect ratios still read cleanly.

Avoid: any text or signage, painterly brushwork, illustration aesthetic, AI-art cyberpunk lighting, glossy 3D-render look, stock photography of workers in hard hats pointing at clipboards. Real construction site, real light, documentary register.

Format: 1440x900px (16:10) · PNG or JPG

## Section diagram (already rendered)

The `Four patterns map. One breaks.` feature-compare chart is rendered at `media/road-then-now.webp` from `media/road-then-now.json`. No image prompt needed — it's a chart, not an AI image.

The cycle row uses the per-item `{text, status: "breaks"}` shape (template extension added 2026-05-20) which renders the row in coral with a small "BREAKS" badge. Used to visually mark the asymmetry on both sides of the compare.

To re-render after editing the JSON:

```bash
node charts/render.mjs \
  --template feature-compare \
  --data articles/2026/05/2026-05-20-building-the-road-to-production-again/media/road-then-now.json \
  --output articles/2026/05/2026-05-20-building-the-road-to-production-again/media/road-then-now.webp \
  --width 1600 --height 720 --scale 2
```
