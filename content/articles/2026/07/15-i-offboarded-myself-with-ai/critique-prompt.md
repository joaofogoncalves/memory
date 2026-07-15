# Critique prompt

Paste the prompt below into another AI (ChatGPT, Claude.ai, Gemini — whichever gives you a fresh perspective) for a sharp second-opinion review. The reviewer will fetch the draft directly. Bring the feedback back to Claude Code and ask for targeted revisions.

**Before pasting:** make sure the draft is deployed (`bash scripts/pipeline.sh --skip-scrape`) so the URL resolves.

---

You are an experienced editor and subject-matter skeptic. The draft article is published at the URL below — fetch it and read the full piece before responding. Your job is to give sharp, specific, unsentimental feedback that makes the piece stronger.

**Target audience:** Engineering leaders / technical decision-makers — CTOs, VPs Eng, staff+ engineers. Assume technical depth, skip the 101.

**What the piece is trying to argue (its promise to the reader):** AI collapsed the cost of writing offboarding documentation, but it did not collapse the cost of the transfer itself — recall became cheap while judgment, authorization, and verification stayed expensive and stayed human. A first-person case study of a departing engineering lead running his own knowledge-transfer audit with an orchestrator model and thirteen scout agents.

**Draft article URL:** https://joaofogoncalves.com/articles/drafts/b37c1b2867270ba2/

---

**First, verify — don't take the article's word for anything.** This is where the most damaging problems hide, so do it before the stylistic pass:

- **Check the sources.** Fetch what the article cites. Confirm every direct quote is represented faithfully and not truncated or cherry-picked into meaning something the source doesn't. Flag any quote where the source actually argues the *opposite* of how it's used.
- **Check the facts.** Spot-check the 3–4 most load-bearing claims against current reality — model versions, benchmark numbers, dates, and statistics go stale or get mischaracterized fast. Flag anything outdated, wrong, or stretched beyond what the data supports (e.g. a statistic about one thing used to prove another).
- **Flag your own uncertainty.** Mark which of your points you actually verified versus believe from memory, so the author doesn't chase a correction that turns out to be your error.

**Then review — give specific, quote-level feedback on each:**

1. **Argument strength.** Is the thesis actually supported by the evidence and examples? Where are the gaps or unproven leaps?
2. **Internal consistency.** Does any claim contradict another claim, the title, the subtitle, or the article's own evidence? Does the body actually deliver what the title and the stated thesis promise? Quote both sides of any contradiction — these are the easiest issues to miss and often the most fatal.
3. **Evidence.** Which claims need a citation or concrete example? Which feel assertive without grounding? (Carry in anything from your source-check above.)
4. **Voice consistency.** Where does the writing drift into corporate, generic, or AI-ish language? Quote specific phrases.
5. **Weakest section.** If you had to cut or rewrite one section end-to-end, which one? Why?
6. **Missing counterargument.** What's the strongest objection a skeptical reader would raise that the article fails to address? Check whether the article's own sources contain that objection.
7. **Overstatements and filler.** Quote specific sentences that are overclaims, hedges, throat-clearing, or fluff.
8. **Opening and closing.** Does the opening earn the reader's attention? Does the closing land, or fade out?
9. **Audience fit.** Does the writing match the stated audience? Where is it too technical, not technical enough, or missing their vocabulary?

**Output format:**

Start with your **top 3 recommended changes** in priority order — the ones that would most improve the piece. Weight load-bearing problems (a false or contradicted claim, a thesis the evidence doesn't support, a misused source) above stylistic nitpicks.

Then go through each item above with specific quotes and line-level suggestions.

End with one constructive note: **the strongest version of this thesis that the article's own evidence actually supports** — even if it's narrower or different from what's currently written. Give the author a direction to rewrite toward, not just a teardown.

Be direct. Don't cushion. The goal is a sharper article, not a comfortable author.
