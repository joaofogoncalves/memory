---
argument-hint: [pasted text, a file path, or a post/article slug — empty to be prompted]
description: Strip AI tells from a draft and rewrite in your voice — runs a two-pass audit (detect, then verify) calibrated to your style guides
allowed-tools: AskUserQuestion, Read, Edit, Write, Glob
---

Strip the characteristic "AI writing" tells from a piece of text and rewrite it in João's voice. This is an **editing pass**, not a rewrite — it preserves the meaning, structure, register, and argument of the input. It only removes the patterns that make prose read as machine-generated.

This skill is the authoritative home for the AI-tell catalogue below. `/post` and `/article` run the same audit inline during drafting and reference this file.

## What this is for

- Cleaning a draft you wrote elsewhere (a Substack draft, an email, a doc) and pasted in.
- A targeted scrub of an existing `post.md` or `article.md` that reads a little machine-made.
- A final-polish pass when something is "fine but stiff."

It is **not** a content edit. It won't restructure your argument, add evidence, or change your thesis. If the draft has a substance problem, that's a different job (use the `/article` critique prompt for that).

## Arguments

`$ARGUMENTS` can be one of:
- **Pasted text** — the prose to clean, inline.
- **A file path** — e.g. `content/posts/2026/06/14-foo/post.md` or any `.md` file.
- **A slug fragment** — locate the file with `Glob` (`content/posts/**/*$ARGUMENTS*/post.md`, then `content/articles/**/*$ARGUMENTS*/article.md`). If multiple match, disambiguate with AskUserQuestion.

If `$ARGUMENTS` is empty, ask the user to paste the text or name a file.

When the input is a file with frontmatter, operate **only on the body** — never touch frontmatter, hashtags, or media references.

## Step 1: Calibrate to the voice

Read these before auditing — they ARE the voice calibration (don't ask the user for a writing sample; their style guides are more precise than a 2-paragraph sample):

1. `style/writing_style.md` — primary authority. Note which tells it already bans (em dashes, hyperbole, "not X but Y", corporate-speak, filler phrases). These are non-negotiable.
2. `style/profile.md` — vocabulary ("use naturally" vs "avoid" lists), rhetorical devices, and the deliberate signature moves to **preserve** (see below).
3. If the input is an article, also read `style/article_style.md`.

## Step 2: Detect — audit against the AI-tell catalogue

Read the input and flag the patterns below. Most are phrase-level — flag every instance and quote the offending phrase. The **cadence tells** are different: they're judged by *density across the whole piece*, so count them rather than flagging each one (see that subsection). Don't fix yet.

### Hard tells (always fix)

These read as AI to anyone and have no legitimate use in this voice:

- **Em / en dashes** — `—` or `–` anywhere. Convert to a period, comma, colon, or restructure. Non-negotiable; this is the single most reliable AI fingerprint and `writing_style.md` already bans it.
- **Trailing `-ing` "analysis" clauses** — a participial tail bolted onto a sentence to editorialize: "…, *highlighting the importance of* X", "…, *underscoring the need for* Y", "…, *reflecting a broader shift toward* Z", "…, *showcasing its ability to* W". Cut the tail, or turn the point into a direct sentence. This is the most common LLM tell and is *not* yet named in the style guides.
- **Copula avoidance / inflation verbs** — dodging plain "is/does" with "*serves as*", "*stands as a testament to*", "*plays a pivotal role in*", "*acts as a cornerstone of*", "*represents a significant*". Replace with plain "is", "does", or the specific fact.
- **Significance inflation** — "game-changing", "revolutionary", "transformative", "a landmark", "groundbreaking", "in an era of". Cut, or replace with the concrete thing that's actually notable. Already banned by `writing_style.md`.
- **"Not X, but Y" correction frames** — "It's not just a tool, it's a philosophy." Restructure to a direct claim. Already banned. (Do NOT confuse with the *deliberate* "same X, completely different Y" contrast — see Preserve.)
- **Filler / throat-clearing** — "It's worth noting that", "In today's landscape", "At the end of the day", "Needless to say", "When it comes to", "In order to" (→ "to"). Cut. Already banned.

### Soft tells (fix unless deliberate)

These can be legitimate occasionally; the tell is *reflexive overuse*. Use judgment and the Preserve list:

- **Elegant variation / synonym cycling** — renaming one thing three ways to avoid repeating the noun ("the system… the platform… the framework" all meaning the same thing). Just repeat the noun. Repetition reads as human; variation reads as a thesaurus.
- **False ranges** — "from startups to enterprises", "from code to culture", "from X to Y" when it isn't a real spectrum, just padding to imply scope. Name the actual scope or cut.
- **Compulsive rule-of-three** — tricolons everywhere ("faster, cheaper, and more reliable"). Keep the *earned* ones; cut the reflexive ones. (João's deliberate closing tricolons are a signature — see Preserve.)
- **Vague attribution** — "experts say", "studies show", "many believe", "it's widely understood". Name the source or cut. (`article_style.md` already requires named citations.)
- **Excessive signposting** — two forms. The transitional ("Now let's turn to", "As we discussed above", "In the next section") and the imperative/declarative ("Make it concrete.", "Here is the trap.", "Here is the strongest objection."). The second is subtler — it reads as a model announcing its own next beat — and slips past the `article_style.md` ban, which only names the transitional form. Cut both, or fold the setup into the sentence that follows.
- **Title-case headings** — "The Future Of Work". Use sentence-case thematic headers ("What actually dies").
- **Boldface / emoji overuse** — bold sprinkled mid-sentence for emphasis; any emoji. Strip both.

### Cadence tells (density-gated — the hardest call)

These are rhythm patterns, not phrases. Any single instance is fine — often it *is* the signature voice. The tell is **density**: the same device firing over and over across a piece. You cannot audit these phrase-by-phrase; a per-instance "is this one earned?" answers yes every time and never notices it's the fifth. **Count each across the whole piece**, then judge the rate against a small budget (≈2–3 in a long article, 1 in a short post). This is exactly the class of tell a corpus-level reviewer catches and a per-draft pass misses most.

- **Antithesis / staccato cadence** — short declarative, its opposition, terse resolution: "The model was fine." / "True. Also useless on a Monday." / "It resigns. It takes a better offer." One or two land hard. A dozen reads as a tic.
- **Aphorism-formula closers** — balanced abstract-noun couplets used to end sections: "The harness, you can lose to a better model. The judgment, you can only lose to a worse manager." / "One compounds the moat. The other borrows against it." Powerful once or twice per piece; mechanical when every section closes this way.
- **Anaphora** — repeated sentence-openers for rhythm: "It coordinates state… It handles permissions… It recovers…" Deliberate when it builds to something; a tell when it's just cadence.

When a device is over budget, the fix is **not** to delete it — keep the one or two strongest instances and rewrite the rest as ordinary sentences. The target is sparse-and-deliberate, not zero.

### Communication tells (mostly for pasted external drafts)

Rare in `post.md`/`article.md`, common in pasted chatbot output:

- **Chatbot closings** — "I hope this helps!", "Let me know if you have questions!", "Feel free to reach out."
- **Knowledge-cutoff / hedging disclaimers** — "As of my last update", "I'm not an expert, but".
- **Sycophancy** — "Great question!", "That's a fascinating point."
- **Generic conclusions** — "In conclusion", "To sum up", "All in all". `article_style.md` bans "Key takeaways" sections for the same reason.

## Step 3: Preserve — but on a budget, not unlimited

The humanizer philosophy over-corrects by blanket-banning patterns that are deliberate in this voice. The moves below are signatures — **when sparse**. But there's an opposite failure mode that's just as real: treating them as always-keep, instance by instance, so they pile up until the density itself is the tell. Each of these is a signature in ones and twos and a tic in dozens. Preserve them; budget them.

The discriminator is **density, judged across the whole piece** — never per-instance. So count first (use the Cadence tells method above), then decide. When a device is over budget, keep the strongest one or two instances and rewrite the weakest as plain prose — don't zero out the device.

- **The "same X, completely different Y" contrast** — a signature move (`writing_style.md`). It's a contrast, not a "not X but Y" correction. Keep it — sparingly.
- **Closing tricolons** — "Pain is the ignition. Curiosity is the engine. You need both." A deliberate rhythm, not reflexive rule-of-three — until the piece has five of them. Keep the strongest; thin the rest.
- **Single-line emphasis beats** — a standalone short sentence after a longer block. Intentional pacing — but a *run* of them is the staccato cadence above. Keep them as occasional punctuation, not the default sentence shape.
- **Dry one-liner closers** and **quiet reframes** — the whole point of the ending. Don't "smooth" them into a generic conclusion. One balanced aphorism per section closing is the budget; if *every* section ends on one, that's the tell, not the voice.
- **Deliberate repetition** for rhythm or emphasis. Repetition is human; flag it only when it's reflexive or when the device repeats past its budget.

When you're unsure whether a single instance is deliberate or a tell, leave it and note it in the audit report rather than changing it. The judgment call is reserved for *density*, not for any one sentence.

## Step 4: Rewrite (pass 1)

Produce a cleaned version that fixes every hard tell and the soft tells that aren't deliberate. Rules:

- **Preserve meaning, structure, paragraph order, and length.** This is surgery, not a rewrite. If the cleaned version is dramatically shorter or differently shaped, you've overstepped.
- **Match the register of the original.** A casual post stays casual; a researched article stays researched.
- **Don't add anything** — no new claims, no new evidence, no new transitions. Removing and replacing only.
- Apply `writing_style.md` voice rules and `profile.md` vocabulary throughout.

## Step 5: Audit the rewrite (pass 2)

Re-read your own pass-1 output as if it were a fresh submission and run Step 2 again. LLM tells survive first passes — this second read is the part of the humanizer worth keeping. Catch:
- Tells you introduced while rewriting (it's easy to swap one inflation verb for another).
- Tells you missed the first time.
- Anywhere the fix changed the meaning — revert toward the original's intent.

Fix what you find. If a tell is genuinely load-bearing (removing it would change the meaning), leave it and say so in the report — don't mangle the sentence to hit zero.

## Step 6: Output

Present, in this order:

1. **The cleaned text** — between horizontal rules (`---`) so it's copy-pasteable. Always render it as plain text in the response (never inside an AskUserQuestion preview).
2. **Audit report** — a short bulleted list of what changed and why, grouped by tell type. Quote the before phrase. Keep it tight: the point is the user can see what you touched, not a lecture. Example:
   - *Em dash* — "the moat — it walks out" → "the moat. It walks out."
   - *`-ing` clause* — cut "…, underscoring the importance of retention."
   - *Inflation verb* — "serves as the foundation" → "is the foundation."
3. **Left alone (if any)** — anything you flagged but deliberately preserved, with a one-line reason ("kept the closing tricolon — it's an earned signature move, not reflexive").

## Step 7: Offer to apply (file inputs only)

If the input was a file (path or slug), use AskUserQuestion:
- **Apply to the file** — use `Edit` to replace the body with the cleaned version (frontmatter, hashtags, and media references untouched). Confirm the path written.
- **Leave the file as-is** — the user copies what they want manually.

If the input was pasted text, skip this step — the user takes the cleaned text from the response.

Never write back to a file without explicit confirmation.
