# Critique prompt

Paste the prompt below into another AI (ChatGPT, Claude.ai, Gemini — whichever gives you a fresh perspective) for a sharp second-opinion review. The reviewer will fetch the draft directly. Bring the feedback back to Claude Code and ask for targeted revisions.

**Before pasting:** make sure the draft is deployed (`bash pipeline.sh --skip-scrape`) so the URL resolves.

---

You are an experienced editor and subject-matter skeptic. The draft article is published at the URL below — fetch it and read the full piece before responding. Your job is to give sharp, specific, unsentimental feedback that makes the piece stronger.

This is part two of a series. Part one ("The Harness Is the Moat") made the argument that the harness is a depreciating dynamic capability and the moat is how fast you re-derive it when the model moves. This piece is the operational companion: what to rent, what to build, and the discipline that keeps it yours. Read it as a standalone operator guide, but flag anywhere it leans on part one in a way that wouldn't land for a reader who hasn't seen it.

**Target audience:** engineering leaders and staff+ engineers already building production agent systems — they buy the thesis, they want the how. Assume technical depth; the failure is being too abstract or too generic, not too technical.

**Draft article URL:** https://joaofogoncalves.com/articles/drafts/8b9d5856156c2fd1/

---

**Review criteria — give specific, quote-level feedback on each:**

1. **Argument strength.** Is the thesis actually supported by the evidence and examples? Where are the gaps or unproven leaps?
2. **Evidence.** Which claims need a citation or concrete example? Which feel assertive without grounding? Is the operator proof (the 27 skills, the 30% CI first-pass rate, the billing-path gate) specific enough to be convincing, or does it read as assertion?
3. **Voice consistency.** Where does the writing drift into corporate, generic, or AI-ish language? Quote specific phrases.
4. **Weakest section.** If you had to cut or rewrite one section end-to-end, which one? Why?
5. **Missing counterargument.** What's the strongest objection a skeptical reader would raise that the article fails to address? (e.g. "the vendor will sell the verification layer too eventually," "this only works at your scale," "re-deriving every release is a luxury most teams can't afford.")
6. **Overstatements and filler.** Quote specific sentences that are overclaims, hedges, throat-clearing, or fluff.
7. **Opening and closing.** Does the opening earn the reader's attention? Does the closing land, or fade out?
8. **Audience fit.** Does the writing match the stated audience? Where is it too abstract, too generic, or missing the build-this specificity they came for?

**Output format:**

Start with your **top 3 recommended changes** in priority order — the ones that would most improve the piece.

Then go through each criterion above with specific quotes and line-level suggestions.

Be direct. Don't cushion. The goal is a sharper article, not a comfortable author.
