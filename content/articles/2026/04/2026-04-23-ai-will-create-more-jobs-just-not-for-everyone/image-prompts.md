# Image Prompts

## Hero Image

Wide cinematic architectural photograph of a monumental corporate lobby at night, shot head-on from the far end of the atrium. The space is vast: double-height ceiling, polished stone floor reflecting overhead downlights, brushed steel columns flanking the frame. Stretching horizontally across the mid-ground is a long row of ten to twelve identical turnstile gates — the kind of waist-high optical barriers used in secure office buildings. Every gate except one is dark and inactive, their indicator panels unlit, their transparent glass wings closed. A single turnstile near the centre of the frame is lit: cool teal-white light glowing from its panels, wings open. A short, orderly queue of three or four silhouetted figures in business attire is passing through it — one mid-stride on the far side, one at the reader, one waiting. The figures are in soft shadow, dignified, unhurried. Beyond the turnstile bank, the lobby continues into a glass-walled interior where a few more distant silhouettes are visible moving through a lit corridor.

Cinematic colour grade: cold slate-blue and desaturated steel ambient across the lobby, a precise pool of cool white-teal light only at the one active gate, warm tungsten accents in the deep background corridor. Slight wide-angle lens (equivalent ~24–28mm) to capture the scale of the turnstile row; sharp focus on the lit gate and the figures passing through; the dark gates and the polished floor fall into shallow focus. Faint haze or glass reflection for atmosphere. Dominant lines: the horizontal rhythm of the turnstile row, the vanishing-point perspective of the floor tiles, the vertical steel columns framing the edges.

Keep the composition symmetrical around the lit turnstile so 16:10 and square thumbnail crops both preserve the one-gate-lit moment. No signage, no text, no company logos, no glowing sci-fi overlays, no visible security guards, no UI elements.

References: Andreas Gursky architectural panoramas (Prada, 99 Cent, Paris Montparnasse), Michael Mann night-interior cinematography (*Heat*, *Collateral*, *The Insider*), Lynne Cohen institutional interiors, Thomas Struth museum/atrium photography. Avoid: painterly brushwork, illustration style, watercolour texture, hand-drawn look, 3D render gloss, bright sci-fi neon, tech-startup corporate palettes, lens-flare kitsch, any hint of digital-painting aesthetic.

Format: 1440x900px (16:10) · PNG

Target path: `media/hero-door-policy.jpg` (generated and wired into frontmatter)

## Inline charts (rendered)

- `media/wage-premium-trajectory.webp` — line chart anchoring "The part nobody prices in" (0% → 25% → 56% over 2022–2024)
- `media/cohort-divergence.webp` — stat-compare anchoring "The part nobody prices in" (senior cohort +9% vs entry cohort −6%)
- `media/two-doors.webp` — feature-compare anchoring "Who gets the new jobs" (leverage vs judgment)
- `media/adaptation-window.webp` — stat-compare anchoring "But isn't this just reskilling panic?" (PC era 5–15 yr productivity diffusion lag vs AI era 10 mo of task-coverage growth 36% → 49%). **Regenerated** from Solow-paradox sources (David 1990, Brynjolfsson & Hitt 2003) and AEI data after the original's factually-wrong PC wage premium claim (0 → 15% over 15 years) was corrected — Krueger (1993) found a 10–15% PC-user wage premium already in 1984 CPS data; Autor/Katz/Krueger (1998) measured 17% → 22% over 1984–1993. Rendered via Playwright from JSON spec at `media/adaptation-window.json`.
- `media/quality-debt-gitclear.webp` — stat-compare anchoring "But doesn't AI code rot?" (4× clone growth vs +54% bugs/developer). Rendered via Playwright from JSON spec at `media/quality-debt-gitclear.json`.

The old `wage-premium-jump.webp` stat-compare is superseded by the trajectory line chart and can be deleted once the article body is updated.
