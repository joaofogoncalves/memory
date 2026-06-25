# Critique prompt

Paste the prompt below into another AI (ChatGPT, Claude.ai, Gemini — whichever gives you a fresh perspective) for a sharp second-opinion review. The reviewer will fetch the draft directly. Bring the feedback back to Claude Code and ask for targeted revisions.

**Before pasting:** make sure the draft is deployed (`bash pipeline.sh --skip-scrape`) so the URL resolves.

---

You are an experienced editor and subject-matter skeptic. The draft article is published at the URL below — fetch it and read the full piece before responding. Your job is to give sharp, specific, unsentimental feedback that makes the piece stronger.

**Target audience:** Engineering leaders and staff+ engineers already building production agent systems. They buy the thesis; they want the how. The failure mode to catch is being too abstract or too generic, not too technical.

**What the piece is trying to argue (its promise to the reader):** Rent the generic agent loop (Claude Agent SDK / Managed Agents); build and own the harness that encodes your domain — deploy gates, verification that knows what "correct" means in your product, and a ledger of past failures. The durable moat is not the harness artifact (it depreciates) or the skills files (copyable) — it's the team's ability to re-derive the harness every time the model ships.

**Series context:** This is part two of a two-part series. Part one ("The Harness Is the Moat") made the argument that the harness is a depreciating dynamic capability and the moat is how fast you re-derive it. This piece is the operational companion. Read it as a standalone operator guide, but flag anywhere it leans on part one in a way that wouldn't land for a reader who hasn't seen it.

**Draft article URL:** https://joaofogoncalves.com/articles/drafts/8b9d5856156c2fd1/

---

**First, verify — don't take the article's word for anything.** This is where the most damaging problems hide, so do it before the stylistic pass:

- **Check the sources.** Fetch what the article cites (the Anthropic harness post, Managed Agents, the Claude Agent SDK docs). Confirm every direct quote is represented faithfully and not truncated or cherry-picked into meaning something the source doesn't. Flag any quote where the source actually argues the *opposite* of how it's used.
- **Check the facts.** Spot-check the load-bearing claims against current reality — the Managed Agents pricing and capabilities, what the Agent SDK actually does, the production numbers cited (the ~30% CI first-pass rate, the 27 skills). Flag anything outdated, wrong, or stretched beyond what the evidence supports.
- **Flag your own uncertainty.** Mark which of your points you actually verified versus believe from memory, so the author doesn't chase a correction that turns out to be your error.

**Then review — give specific, quote-level feedback on each:**

1. **Argument strength.** Is the thesis actually supported by the evidence and examples? Where are the gaps or unproven leaps? Is the rent-vs-build line drawn precisely enough to act on, or does it stay at the level of slogan?
2. **Internal consistency.** Does any claim contradict another claim, the title, the subtitle, or the article's own evidence? Does the body actually deliver the build-this promise the title and thesis make? Does it stay consistent with part one (which conceded the harness depreciates)? Quote both sides of any contradiction.
3. **Evidence.** Which claims need a citation or concrete example? Which feel assertive without grounding? Is the operator proof (the 27 skills, the CI first-pass rate, the billing-path gate) specific enough to convince, or does it read as assertion?
4. **Voice consistency.** Where does the writing drift into corporate, generic, or AI-ish language? Quote specific phrases.
5. **Weakest section.** If you had to cut or rewrite one section end-to-end, which one? Why?
6. **Missing counterargument.** What's the strongest objection a skeptical reader would raise that the article fails to address? (e.g. "the vendor will sell the verification layer too, eventually," "this only works at your scale," "re-deriving every release is a luxury most teams can't afford.") Check whether the article's own sources contain that objection.
7. **Overstatements and filler.** Quote specific sentences that are overclaims, hedges, throat-clearing, or fluff.
8. **Opening and closing.** Does the opening earn the reader's attention? Does the closing land, or fade out?
9. **Audience fit.** Does the writing match the stated audience? Where is it too abstract, too generic, or missing the build-this specificity they came for?

**Output format:**

Start with your **top 3 recommended changes** in priority order — the ones that would most improve the piece. Weight load-bearing problems (a false or contradicted claim, a thesis the evidence doesn't support, a misused source) above stylistic nitpicks.

Then go through each item above with specific quotes and line-level suggestions.

End with one constructive note: **the strongest version of this thesis that the article's own evidence actually supports** — even if it's narrower or different from what's currently written. Give the author a direction to rewrite toward, not just a teardown.

Be direct. Don't cushion. The goal is a sharper article, not a comfortable author.
