---
argument-hint: [recruiter/HM LinkedIn URL] OR [Company, Role, Person] OR [recipient context as text]
description: Draft proof-led outreach (LinkedIn DM, email cold, follow-up) for a specific recipient
allowed-tools: Read, WebFetch, Write, Bash, AskUserQuestion
---

Draft cold outreach to a recruiter, hiring manager, founder, or someone interesting in your space. Saved to `applications/{company-slug}/outreach.md` with three length-tiered variants.

The voice operationalizes "Target conversations, not applications": substantive, specific, low-volume. One thoughtful message beats a hundred portal applications. Each variant must lead with relevance to the recipient — not with a request.

## Arguments

`$ARGUMENTS` describes the recipient. Parse flexibly:

- **LinkedIn URL** (`https://linkedin.com/in/...`) — attempt WebFetch; if blocked (LinkedIn usually is), fall back to asking the user for context.
- **Company, Role, Person** triplet (`"Acme Corp, VP Eng, Jane Doe"`) — most common form.
- **Free-text context** — pull what you can.
- **Empty** — use AskUserQuestion to gather: company name, recipient name, recipient role, why this person specifically (anything you know about their work / what they've shipped / what they've written).

## Step 1: Read inputs

Read these in parallel:

1. `cv.md` — proof bank
2. `pitch_style.md` — primary style guide for self-positioning
3. `profile.md` — voice reference
4. `writing_style.md` — format hygiene
5. `config/site.yaml` — your site URL, LinkedIn, GitHub

## Step 2: Build recipient context

From the arguments and any fetched data, capture:

- **Recipient name** (and how to address them — first name unless they're a formal company)
- **Recipient role** (recruiter, hiring manager, founder, IC at a target team)
- **Company** (slug it: lowercase hyphenated)
- **Specific hook** — something concrete about *them* that justifies the outreach. Their public work, a post they wrote, a system they shipped, a hire they're making, a thesis they've publicly stated. **If you don't have this, stop and ask the user for it.** Generic outreach is worse than no outreach.

If the arguments lacked a hook and you can't infer one, use AskUserQuestion to ask: "What specifically about this person makes you want to reach out — something they wrote, shipped, or said publicly?"

## Step 3: Pick a proof

Identify ONE proof point from cv.md that aligns with the recipient's likely interest. Different proofs work for different recipient types:

- **Recruiter/TA**: 2–3 metrics that show level + recency (current role + scope)
- **Hiring manager**: a system or accomplishment that maps to what their team builds
- **Founder/CEO**: an outcome that matches their stage (e.g., 0→1 → BRIDGE IN; scale → Valispace acquisition)
- **IC at a target team**: a technical artifact that's interesting to them as a peer

The proof should be one sentence — it goes near the top of every variant.

## Step 4: Draft three variants

All three appear in the same file under separate headings. Length and tone differ.

### Variant 1 — LinkedIn DM (~80 words)

- One-line hook: connects to *them*, not to you.
- One-line proof: what you do, with a number.
- One-line ask: a specific question, not a request to "connect" or "chat."
- No external link. Mobile-first. No salutation block needed.

**Example shape:**

```
Hey {firstname} — saw your piece on {specific thing}. Hit something I keep running into: {one-sentence elaboration that shows you actually read it}.

Currently running {your one-line proof at BRIDGE IN}. Curious how you're {specific question that connects their work to your work}?
```

### Variant 2 — Email cold (~150 words, 130–180 acceptable)

- Subject line: 5–8 words, specific, no clickbait. Examples: `"on {their thing} — quick note"`, `"agent orchestration / 14 in production"`, `"{role title} role — proof of fit"`.
- Salutation: `Hi {firstname},` (always first name; `Hello,` if unknown).
- Three short paragraphs:
  1. **Hook** (~30 words) — relevance to them
  2. **Proof + fit** (~70 words) — what you do + why it maps to what they need
  3. **Quiet ask** (~30 words) — one specific question or 20-minute call invitation
- Sign-off: `João\n{site URL}` — site link is welcome here (unlike the LinkedIn DM).

### Variant 3 — Follow-up (~50 words)

For 5–7 days after no reply. Gentle, no guilt.

- Reference the original message in one clause, not a recap.
- One short proof or update (something new since last message).
- Reaffirm the ask in one sentence — usually narrowed (`"if a 20-minute call this or next week works…"`).
- No "just bumping this up" or "circling back."

## Step 5: Voice check

For each variant, confirm:

- [ ] Opens with relevance to the recipient, not "I'm reaching out because…"
- [ ] One named proof (system, number, or artifact)
- [ ] No "Let's connect," "I'd love to discuss," "looking forward to hearing back"
- [ ] No "I came across your profile" / "I noticed that you" framing
- [ ] No em-dashes inside sentences
- [ ] No emojis (unless the recipient's own style would warrant exactly one — rare)
- [ ] Variant within its length band (80 / 150 / 50 words ±20%)

If any fail, rewrite before saving.

## Step 6: Save

```bash
mkdir -p applications/{company-slug}/
```

Save to `applications/{company-slug}/outreach.md`. Use this layout:

```markdown
---
recipient: {Name}
role: {Their role}
company: {Company}
hook: {One-line description of why this person specifically}
date: {YYYY-MM-DD}
---

# Outreach — {Recipient Name} ({Company})

## LinkedIn DM (~80 words)

{variant 1 body}

---

## Email cold (~150 words)

**Subject:** {subject line}

{variant 2 body}

---

## Follow-up (~50 words, send after 5–7 days of silence)

{variant 3 body}
```

## Step 7: Confirm

Tell the user:

- Path to the saved file
- The hook you used (one line)
- The proof you led with
- Word counts for each variant

Note: LinkedIn frequently blocks WebFetch. If that happened, the message is built from the user-supplied context only — flag this so the user can review extra carefully before sending.
