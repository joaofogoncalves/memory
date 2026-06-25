# Image Prompts — sequence

## Slide 1/2: the Google chart (Pichai's trajectory)

User-provided editorial chart showing % of new code at Google written by AI over time, with annotated callouts (Pichai Q3 '24: 25%, Q1 '25: 30%, Ashkenazi Q3 '25: 50%, Q4 '25: 50%, today/Cloud Next: 75%). Saved as `media/image-1.png`. No regeneration — used as-is.

## Slide 2/2: BRIDGE IN AI authorship trend

Rendered via the `charts/` line template using `media/bios-ai-authorship.json`:

```bash
node charts/render.mjs --template line \
  --data posts/2026/04/2026-04-27-at-cloud-next-pichai-showed-this-chart/media/bios-ai-authorship.json \
  --output posts/2026/04/2026-04-27-at-cloud-next-pichai-showed-this-chart/media/image-2.webp \
  --width 1200 --height 1200
```

Spec: single series ("AI-authored share") plotting [0, 0, 19, 75, 98, 99.9] across [Nov '25 → Apr '26]. Title: "% of new code at BRIDGE IN written by AI". Subtitle: "Greenfield repo, Nov 2025 – Apr 2026." Color: teal `#44d8f1`. Square 1200×1200 to carousel cleanly with slide 1.

Methodology note (for if anyone asks): figures derived from `git log` on the bios repo. AI-authored = commits authored by `aiBerto` / `Claude` accounts OR commits with `Co-Authored-By: Claude` in the body. Dependabot commits excluded. Lines added used as the proxy for "share of new code" — matches the Pichai metric framing.
