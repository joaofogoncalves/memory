# Image Prompts

All images follow the visual taste profile: dark palette (deep navy / near-black background #0e131e, teal accents #44d8f1), high text density, flat vector style, no floating icons, no 3D gloss, no gradient corporate banners. Every diagram should look like a precise technical schematic, not a marketing slide. Keep subjects centered with breathing room because thumbnails crop the edges.

---

## Hero Image — Pipeline vs Nervous System

A two-panel comparison diagram on a dark navy background (#0e131e). Left panel titled "Pipeline" in clean sans-serif at the top: a straight horizontal chain of five labeled rectangles reading "Spec → Plan → Build → Test → Review → Merge", connected by simple arrows. The whole chain is a flat neutral gray, contained inside a thin circular border labeled "One system, one input, one output." Right panel titled "Nervous System": concentric rings. Outer ring labeled "Sensors" with three small pill labels around its circumference (Sentry, Slack, Backlog). Middle ring labeled "Reflexes" with four pill labels (/heartbeat, /pick, /build, /ci-fix). Inner core labeled "Memory" with two small labels (gist state, weekly review). Teal arrows loop between the rings in both directions to show bidirectional flow. The nervous system side should visually feel alive compared to the static pipeline. Minimal ornamentation. Mono-width readable sans-serif labels throughout. No icons, no gradients, no floating 3D elements. Centered composition, generous margins.

Format: 1440x900px (16:10) · PNG

---

## Section 3 — The Three Organs · `::: wide` (displays at 1080px)

A clean three-column diagram on the same dark navy background. Each column is a tall rounded rectangle with a teal header bar. Column 1 header: "SENSORS" — below it, stacked labeled blocks: "Sentry feed", "Slack: #product", "Slack: #product-monitoring", "Slack: #eng-team", "Slack: #product-development", "GitHub @mentions". Column 2 header: "REFLEXES" — below: "/heartbeat", "/pick", "/build", "/ship", "/ci-fix", "/fix-dependabot". Column 3 header: "MEMORY" — below: "gist state (timestamps, pending threads, nudge budgets)", "/weekly-agent-review", "agent definitions (.claude/agents/)". Thin teal arrows connect the columns in a loop: sensors → reflexes (straight), reflexes → memory (down-curving), memory → sensors (long return arrow across the top, labeled "tunes"). Labels crisp and readable. No icons inside the blocks, just text. The diagram should feel like an architecture schematic, not a marketing graphic.

Format: 2160x1080px (2:1) · PNG — wider aspect to match the three-column layout at 1080px display width

---

## Section 4 — Agent Roster Evolution · `::: wide` (displays at 1080px)

A side-by-side before/after grid on a dark navy background. Left side header: "February 2026 · 12 agents". Below it, a 3-column × 4-row grid of small labeled cards, each card showing a single agent name in monospaced sans-serif: project-manager, product-manager, architect, ui-designer, backend-developer, frontend-developer, code-optimizer, code-simplifier, test-writer, quality-checker, code-reviewer, documentation-expert. All cards in a muted slate gray. Right side header: "April 2026 · 14 agents". Same grid but with 14 cards in a 3-column × 5-row layout (14 total, one cell empty). The four new agents (ci-fixer, conflict-resolver, github-actions-expert, tester) are highlighted in teal (#44d8f1) with a teal outline glow. Each new card has a tiny right-side annotation label in smaller text: ci-fixer → "CI drift", conflict-resolver → "merge conflicts", github-actions-expert → "supply chain", tester → "test writing (split from test-writer)". A thin horizontal separator between left and right halves with a small "→" in the center. Readable sans-serif throughout, no icons, no decorative flourishes.

Format: 2160x1080px (2:1) · PNG — wider aspect suits the before/after side-by-side grid comparison

---

## Section 5 — Autonomy Dial

A centered diagram of a three-position rotary dial on a dark navy background. The dial itself is a flat circular shape with a teal pointer. Three tick marks around the top half of the dial, each with a label: left tick "--auto" (green indicator dot), center tick "--guided" (yellow/amber indicator dot), right tick "--review" (red indicator dot). Below the dial, a compact three-column table (rendered as flat text, not spreadsheet grid). Column headers: "Mode", "Use for", "Auto-merge". Rows: "--auto | Bug, Improvement, Typo | yes" — "--guided | Medium feature, light refactor | no" — "--review | Architecture, migration, security | no". To the right of the dial, a small annotation arrow pointing to the pointer with the label "Chosen by issue complexity. Human can override." Minimal, flat vector style. No 3D dial rendering, no chrome, no bevels — the dial should read as a schematic diagram, not a physical object.

Format: 1200x1200px (1:1) · PNG

---

## Section 6 — Day-in-the-Life Timeline · `::: full` (displays at 1200px, edge-to-edge of page)

A horizontal timeline diagram on a dark navy background. Title at the top: "A Tuesday, April 2026". The timeline runs left to right across the canvas, spanning 08:00 to 18:00, with thin vertical hour markers. Four horizontal tracks stacked vertically, each labeled on the left:

Track 1 — "SENSORS (/heartbeat)" — teal blocks at 08:14 (creates #2847) and 14:00 (mentions sweep).
Track 2 — "REFLEXES (/pick + /build)" — a longer teal block from 09:02 to 09:43 labeled "/pick → /build --auto → PR ready", and a second block at 17:30 labeled "/pick next".
Track 3 — "SPECIALISTS" — a small teal block at 09:33 labeled "ci-fixer patches flaky migration".
Track 4 — "HUMAN" — just two small dots, one at 10:11 labeled "👍 approve" (use a simple checkmark, not an emoji graphic) and a second tiny dot at the end of the day.

Below the main timeline, a smaller separate row labeled "FRIDAY" with one teal block labeled "/weekly-agent-review → proposes 'secrets expert' agent" and a dashed arrow curving back to the start of the main timeline to indicate the feedback loop into next week.

Readable sans-serif labels, teal accent color on all active blocks, thin white/gray baseline for the timeline itself. No icons beyond the checkmark. Clean schematic feel.

Format: 2400x900px (8:3) · PNG — extra-wide aspect for edge-to-edge timeline display at 1200px

---

## Optional bonus — Evolution Timeline (Feb → Apr)

If you want one more diagram, use this between sections 3 and 4: a horizontal timeline from Feb 17, 2026 to Apr 16, 2026 with event markers showing: "Feb 23 — agents upgraded to Opus", "Feb 28 — parallel quality checks", "Mar 1 — weekly-agent-review", "Mar 8 — ci-fixer + /ci-fix", "Mar 25 — conflict-resolver", "Apr 7 — MCP retry + persistent gist state", "Apr 10 — research as issue type", "Apr 15 — reaction-based approvals". Dark navy background, teal markers, each with a short caption. Flat schematic style.

Format: 1440x900px (16:10) · PNG
