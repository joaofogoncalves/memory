---
argument-hint: [job description URL or text] [optional: company URL]
description: Generate interview prep — talking points, STAR-shaped behavioral answers, technical talking points, questions to ask back
allowed-tools: Read, WebFetch, Write, Bash, AskUserQuestion, Glob
---

Generate a focused interview prep document for a specific role. Saved to `applications/{company-slug}/interview-prep.md`.

Output is **proof-led, not study-guide**: it pulls real material from cv.md and recent articles rather than producing generic answers. Designed to read in 30 minutes the night before, not in three hours over a weekend.

## Arguments

`$ARGUMENTS` may contain:
- A JD URL or text (required)
- Optionally a company URL or domain (e.g. `https://acme.com`)
- Optionally a stage hint (e.g. "first call with recruiter", "panel with eng team", "founder chat")

If `$ARGUMENTS` is empty, use AskUserQuestion to gather: JD URL/text, company URL (optional), interview stage (optional).

If a URL is provided, distinguish JD vs company URL by content type / path heuristics. If ambiguous, ask.

## Step 1: Read inputs

In parallel:

1. `cv.md` — proof bank (required)
2. `pitch_style.md` — for the "Tell me about yourself" pitch tone
3. `profile.md` — voice reference
4. `writing_style.md` — format hygiene
5. `config/site.yaml` — site identity
6. Recent articles via `Glob articles/**/article.md` — pick the 3 most recent for thesis material to surface in answers
7. JD (fetch URL or use inline text)
8. Company URL if provided (fetch)

## Step 2: Parse the JD

Extract:
- Company name + slug
- Role title and seniority signals
- Top 5 explicit requirements
- 3 unstated problems the role exists to solve (read between lines: scope of team, recent funding, growth stage, mentioned pain points)
- Stack / tools / methodologies
- Stage signals (what stage the company is in — pre-seed, Series A, scale-up, mature)

## Step 3: Research the company (if URL provided)

If a company URL was provided, capture:
- One-line "what they do"
- Stage / funding / team size signals
- Recent news (product launches, pivots, hires, raises)
- Engineering culture signals (if their site or blog reveals any)
- Leadership names that might appear in interview rounds

If no URL was provided, skip this section (do not fabricate).

## Step 4: Generate the prep document

Save to `applications/{company-slug}/interview-prep.md` with these sections, in this order:

### Section 1 — TL;DR (the night-before refresher)

Three bullets at the very top:
- The one-sentence company summary
- The role's biggest unstated problem (your read)
- The proof you're going to lead with

### Section 2 — "Tell me about yourself" pitch (60–90 seconds spoken / ~150 words)

A specific pitch tailored to *this* role, drawing from `pitch_style.md` rules and the user's actual cv.md content. Lead with what they're doing now (BRIDGE IN, the agents) and the most relevant one or two prior roles. Close with a one-sentence reason this conversation specifically. Do NOT lead with "I have X years of experience."

### Section 3 — Behavioral questions (5–7)

Predict the most likely behavioral questions for this role/stage. For each:
- The question (one line)
- A **STAR-shaped answer** drawn from real cv.md content. Format: `Situation → Task → Action → Result`. Each is one or two sentences max — these are talking-point notes, not memorized answers.

Bias toward questions about:
- Scaling teams / managing through change (if cv.md shows that)
- AI integration / engineering tooling (always relevant given current role)
- Acquisition / due diligence (if Valispace experience maps)
- Hiring / firing / coaching (if the role is leadership)
- Failure mode + recovery (universal)
- Decision-making under ambiguity (universal)
- A specific question pulled from the JD's stated values or pain points

Pick the 5–7 that are most likely for *this specific role/stage*.

### Section 4 — Technical / role-specific (5–7)

Predict the technical or scope-of-role questions. Examples for an engineering leadership role: how do you split planning vs implementation between agents and humans, what's your CI/CD philosophy, how do you do code review at the velocity AI enables, how have you handled production incidents at AI-speed.

For each:
- The question
- 3–5 talking-point bullets — what to say, what specific examples to draw from cv.md or articles, what to avoid

### Section 5 — Questions to ask back (5–7)

Substantive, specific questions that signal you've read about the company and thought about the role. Categories to draw from:
- **Engineering culture**: "How do you currently split human vs AI-generated code in review? What's the bar?"
- **AI strategy**: "Where on the spectrum from 'AI as autocomplete' to 'AI as a teammate' is your team operating today, and where do you want it in 12 months?"
- **Scaling / hiring**: questions specific to their stage
- **Decision-making**: how do they reverse decisions, what's the cadence
- **Day-in-the-life of the person they last hired into this role**

Avoid: questions that could be answered by their About page or recent press. Avoid: salary, perks, WLB at the first round (push to later rounds).

### Section 6 — Company research (if URL was provided)

A focused dump of what you found — facts, not editorializing. Useful as a 5-minute pre-call refresher.

### Section 7 — Failure-mode list

Three things to avoid in this specific interview:
- Specific phrases / words that would land badly given the JD's culture signals
- Topics where overclaiming would be tempting but wrong
- A subtle anti-pattern from `pitch_style.md` that's most relevant here (e.g., "Watch for hedging — this role looks like it wants opinionated.")

## Step 5: Voice check

The prep doc itself should NOT be in pitch-voice — it's working notes. Plain, direct, scannable.

But the embedded artifacts (the "Tell me about yourself" pitch, sample STAR phrasing) MUST follow `pitch_style.md`:
- Lead with proof
- No "passionate," "leverage," etc.
- No marketing CTAs

## Step 6: Save

```bash
mkdir -p applications/{company-slug}/
```

Frontmatter:

```yaml
---
company: {Company Name}
role: {Role Title}
stage: {Interview stage if provided}
date: {YYYY-MM-DD}
jd_source: {URL or "pasted text"}
company_url: {URL or empty}
---
```

## Step 7: Confirm

Tell the user:

- Path to the saved file
- The 3 unstated problems you identified in the JD (one-liners)
- The single proof you'd lead with for "Tell me about yourself"
- Whether company research was included (depends on URL availability)

If the user has not yet generated a tailored CV (`/pdf {JD URL}`) or cover letter (`/cover-letter {JD URL}`) for this role, mention they can — but don't auto-run.
