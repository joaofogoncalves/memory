---
argument-hint: [optional: variant name] (empty = regenerate all)
description: Generate elevator pitches, talk abstracts, speaker bios, LinkedIn copy — all variants in one living file
allowed-tools: Read, Write, Glob, AskUserQuestion
---

Generate self-pitch variants — the surface-tailored ways you describe yourself when the conversation isn't about a specific job. Saved to `pitches.md` at the project root as a single living document containing all variants.

Use this for: networking events, recruiter calls before there's a JD, conference proposals, podcast intros, founder/VC chats, fast LinkedIn or X bio refreshes.

The voice operationalizes "Lead with proof, not promises" across surfaces of varying length. Same underlying narrative, surface-tailored compression.

## Arguments

`$ARGUMENTS` may be:

- **Empty** → regenerate ALL variants (default)
- **A variant name** → regenerate just that one in place. Accepted variant names:
  - `30s` — Elevator 30-second
  - `60s` — Elevator 60-second
  - `2min` — Elevator 2-minute
  - `linkedin-headline` — LinkedIn headline (160 chars)
  - `linkedin-about` — LinkedIn About summary (≤2,600 chars)
  - `talk-abstract` — Conference talk abstract (200–300 words)
  - `bio-short` — Speaker bio short (~50 words)
  - `bio-medium` — Speaker bio medium (~100 words)
  - `bio-long` — Speaker bio long (~200 words)

If a variant name is given but doesn't match, use AskUserQuestion to clarify.

## Step 1: Read inputs

In parallel:

1. `cv.md` — proof bank (required)
2. `pitch_style.md` — primary style authority
3. `profile.md` — voice reference (vocabulary, recurring patterns)
4. `writing_style.md` — format hygiene
5. `config/site.yaml` — name, links, current title
6. Recent articles via `Glob articles/**/article.md` — read the 3 most recent for thesis material (titles, subtitles, opening claims)
7. Existing `pitches.md` if present — preserve any user edits when regenerating only one variant

## Step 2: Build the through-line

Before writing any variant, draft the **single through-line sentence** — the one claim that all variants compress or expand from. It should:

- Lead with a present-tense action ("I run," "I build," not "I have experience in")
- Contain at least one number or named system
- Reference the contrast / through-line across roles (15 years of engineering leadership ↔ now operating at agent-velocity)

Example: *"I'm a Founding Engineer at BRIDGE IN running a 14-agent AI orchestration system, after 15 years scaling engineering teams through one $20M acquisition."*

This through-line is internal scaffolding — it doesn't appear verbatim in every variant.

## Step 3: Generate the requested variant(s)

For each variant, follow these specs precisely. Length targets are from `pitch_style.md`.

### `30s` — Elevator 30-second (~75 words)

Format: 3–4 sentences, spoken aloud cleanly in 30 seconds.

Structure:
1. What you do now (one sentence with a number).
2. What you did before (one sentence — the through-line).
3. What you're looking for / why this conversation (one sentence).

Use case: networking events, intros at meetups.

### `60s` — Elevator 60-second (~150 words)

Adds: one specific story or accomplishment that makes the proof concrete.

Structure:
1. What you do now (one sentence).
2. **One concrete example** — what shipped, what changed (2–3 sentences).
3. The through-line / pattern across your career (1–2 sentences).
4. Why this conversation (one sentence).

Use case: first call with a recruiter, intro chat with a founder, "tell me about yourself" early in an interview.

### `2min` — Elevator 2-minute (~300 words)

Adds: the thesis (your POV on engineering / AI / leadership) and a second concrete example.

Structure:
1. Hook: what you do now, a number, and a single observation that's surprising.
2. One example from current work (BRIDGE IN), with specifics.
3. One example from a prior role (acquisition, scale-up, or platform work), with specifics.
4. The thesis: what your career taught you that's useful in this conversation.
5. Why this conversation specifically.

Use case: panel intros, substantive interview "tell me about yourself," podcast intro.

### `linkedin-headline` — LinkedIn headline (≤160 chars)

The single hardest-working sentence in the entire kit. Constraints:
- Must contain: current role + one keyword recruiters search.
- Must contain: a number or a named system.
- Must NOT contain: "passionate," "thought leader," any vague positioning words.
- ≤160 characters (LinkedIn's hard cap).

Generate 3 candidate headlines, then pick the strongest. Show all 3 to the user with a one-line note on which is recommended and why.

### `linkedin-about` — LinkedIn About summary (1,500–2,500 chars; hard cap 2,600)

LinkedIn's About section. Critical: the **first 220 characters** are the hook (LinkedIn truncates with "...see more" around there).

Structure:
- **Hook (first 220 chars)**: a proof-led one-paragraph claim. The user should be willing to be reduced to just these 220 chars on a phone preview.
- **Body (3–5 short paragraphs)**: lift the cv.md `## Thesis` and `## Building` sections; compress them into a flowing self-narrative. Use single-line emphasis beats.
- **Bullet block at the bottom**: 3–5 lines with key proof points. Format each: `→ {Proof}` or use a clean dash.
- No "Let's connect" / "Open to opportunities" footer — those signals belong in the LinkedIn `Open to work` setting, not in the prose.

### `talk-abstract` — Conference talk abstract (200–300 words)

Use when proposing a talk to a conference, podcast, or event.

Structure:
1. **Title** (one line, claim or question — same patterns as `article_style.md`).
2. **Hook paragraph** (~80 words): the surprising observation, the data point, or the contrarian framing.
3. **Body paragraph** (~100 words): what the talk argues, with one specific example you'd walk through.
4. **Takeaway block** (3 bullets): what attendees leave with.
5. **Speaker line** (~30 words): one sentence using the `bio-short` content.

Tone: same as articles — a take, not a summary.

### `bio-short` (~50 words)

One sentence. Format: `{Name} is a {role} at {company}. {one notable artifact / outcome}. {one prior credit if it strengthens the line}.`

Use case: end of a talk abstract, podcast show notes byline.

### `bio-medium` (~100 words)

Adds: the through-line across roles + one thesis sentence.

Use case: conference speaker page, panel host bio.

### `bio-long` (~200 words)

Adds: the thesis paragraph (lifted/compressed from cv.md `## Thesis`) and one or two specific career credits.

Use case: keynote bio, magazine interview byline, a deep-link About on an external site.

## Step 4: Voice check

For every variant, confirm:

- [ ] Lead with proof, not "I am a"
- [ ] At least one number or named system in the first sentence
- [ ] No "passionate," "leverage," "thought leader," "results-driven"
- [ ] No "open to," "Let's connect," "looking forward to hearing"
- [ ] No em-dashes inside sentences
- [ ] Within length band

If any fail, rewrite that variant before saving.

## Step 5: Save

`pitches.md` lives at the project root. Structure:

```markdown
# Pitches

Through-line: *{the through-line sentence from Step 2}*

Last updated: {YYYY-MM-DD}

---

## Elevator 30-second (~75 words)

{variant body}

---

## Elevator 60-second (~150 words)

{variant body}

---

## Elevator 2-minute (~300 words)

{variant body}

---

## LinkedIn headline (≤160 chars)

**Recommended:** {strongest of the 3 candidates}

Alternates:
1. {alt 1}
2. {alt 2}

---

## LinkedIn About (≤2,600 chars)

{variant body}

---

## Talk abstract (200–300 words)

**Title:** {title}

{variant body}

---

## Speaker bio — short (~50 words)

{variant body}

---

## Speaker bio — medium (~100 words)

{variant body}

---

## Speaker bio — long (~200 words)

{variant body}
```

When `$ARGUMENTS` specifies a single variant, **only replace that variant's block**, leaving all others untouched. Use the existing `pitches.md` (if any) to preserve user edits to other variants.

## Step 6: Confirm

Tell the user:

- Path to `pitches.md`
- Which variant(s) were generated or regenerated
- For LinkedIn headline: show all 3 candidates and which is recommended (the user picks)
- The through-line sentence (so they can sanity-check the foundation)

The user is expected to lightly edit `pitches.md` after generation — voice always benefits from a human pass. The next time `/pitch` runs (with a single-variant arg), it preserves the edits to other variants.
