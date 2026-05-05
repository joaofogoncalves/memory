---
argument-hint: [job description URL or text]
description: Generate a proof-led cover letter tailored to a specific job, in your voice
allowed-tools: Read, WebFetch, Write, Bash, AskUserQuestion, Skill
---

Generate a tailored cover letter for a specific job. Saved to `applications/{company-slug}/cover-letter.md`. Optionally also produces a styled PDF.

The cover letter must **lead with proof, not promises** — it opens with a specific accomplishment that maps to the role, not a generic introduction.

## Arguments

`$ARGUMENTS` is required: either a URL to the job description, or the JD text pasted inline.

- If `$ARGUMENTS` starts with `http`, fetch the JD via WebFetch.
- Otherwise treat `$ARGUMENTS` as the JD text.
- If `$ARGUMENTS` is empty, use AskUserQuestion to ask for the JD URL or text.

## Step 1: Read inputs

Read these files in parallel:

1. `cv.md` — proof bank (required; abort if missing)
2. `pitch_style.md` — primary style authority for self-positioning artifacts
3. `profile.md` — secondary voice reference (vocabulary, recurring patterns)
4. `writing_style.md` — for format hygiene rules (em-dashes, anti-pattern phrases)
5. `config/site.yaml` — name, links, current title

Then fetch / read the JD as described above.

## Step 2: Parse the JD

From the JD, extract:

- **Company name** (and slug it: lowercase, hyphenated, e.g. `acme-corp`)
- **Role title**
- **Hiring contact** (if named — used for the salutation)
- **Top 3-5 stated requirements**, ranked by emphasis in the JD
- **Top 3 problems the role exists to solve** — read between the lines (e.g. "scaling our infra team from 5 to 20 in 12 months" implies a hiring/scaling problem)
- **Tone signals** — formal vs casual, startup vs enterprise, technical vs business
- **Stack / tools mentioned** — for surface-level keyword resonance only; do not stuff

## Step 3: Build the proof map

For each of the top 3 problems the role is hiring against, identify ONE specific proof point from `cv.md` that maps to it. The proof must be a real, named thing (a system, a number, a delta, a shipped artifact).

If you can't find a real proof for a stated problem, say so to the user. Do NOT fabricate. A short, honest cover letter beats a long one with hand-waved fits.

## Step 4: Draft the cover letter

Length: **250–350 words.** Three paragraphs.

### Paragraph 1 — proof opener (60–90 words)

Open with ONE specific proof point. Not a framing. Not "I'm writing to apply for…" Lead with what you did and what changed because of it. Tie it to the role's biggest stated problem in the second sentence.

**Anti-patterns to avoid:**
- "I am writing to express my interest in the [role] position at [Company]."
- "I came across this role and was excited to…"
- "With X years of experience in Y, I am confident I would…"
- Any opener that delays the proof past the second sentence.

### Paragraph 2 — fit (100–150 words)

Map 2–3 specific proofs from cv.md to specific aspects of the role. One sentence per proof. The structure for each: *what you did → quantified outcome → how it transfers.*

Use the company's named systems / language where relevant — but don't keyword-stuff. Two surface-level references is plenty.

### Paragraph 3 — quiet ask (50–80 words)

Close with a specific question or invitation. Not a marketing CTA.

**Good closers:**
- "Happy to talk through how I'd approach the [specific problem from JD] in the first 90 days, if useful."
- "If you're sizing the role this quarter, worth a 20-minute call?"
- A pointed question about how they're currently structuring the work.

**Anti-patterns to avoid:**
- "I look forward to hearing from you."
- "Thank you for your consideration."
- "I would love the opportunity to discuss further."
- "Feel free to reach out at your earliest convenience."

## Step 5: Voice check

Before saving, run the cover letter through these filters:

- [ ] Opens with a proof point, not an introduction
- [ ] Every sentence has a specific noun (system, company, number) — no abstract claims
- [ ] No em-dashes inside sentences (per `writing_style.md`)
- [ ] No "passionate," "leverage," "results-driven," "thought leader"
- [ ] No "I would bring…" — only "I've done…"
- [ ] Closes with a question or specific invitation, not a marketing CTA
- [ ] 250–350 words total
- [ ] BRIDGE IN appears verbatim where used (rendered red+bold via the site's styling later)

If any fail, rewrite that section before saving.

## Step 6: Save

Create the directory if missing and write the cover letter:

```bash
mkdir -p applications/{company-slug}/
```

Save to `applications/{company-slug}/cover-letter.md` with this frontmatter:

```yaml
---
company: {Company Name}
role: {Role Title}
contact: {Hiring contact name, or empty}
date: {YYYY-MM-DD}
jd_source: {URL or "pasted text"}
---
```

Followed by the cover letter body. Include a properly formatted salutation (`Dear {name},` if known, else `Hello,`) and a sign-off (`João`).

## Step 7: Confirm

Tell the user:

- Path to the saved file
- Word count
- Which 3 proof points you led with (one-liner each)
- The two specific JD problems you mapped them to

Offer to also generate a styled PDF version (matching the brutalist theme of the CV) using `document-skills:pdf`. Only do so if the user confirms — they may not need it. If they say yes, save to `applications/{company-slug}/cover-letter.pdf`.

After this skill, the user typically also wants to run `/outreach` for the recruiter DM and `/pdf "{JD URL}"` for a tailored CV. Mention this lightly so they know the toolkit is there, but don't auto-run them.
