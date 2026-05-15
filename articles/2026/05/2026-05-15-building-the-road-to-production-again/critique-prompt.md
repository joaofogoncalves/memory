# Critique prompt

Paste the prompt below into another AI (ChatGPT, Claude.ai, Gemini — whichever gives you a fresh perspective) for a sharp second-opinion review. The reviewer will fetch the draft directly. Bring the feedback back to Claude Code and ask for targeted revisions.

**Before pasting:** make sure the draft is deployed (`bash pipeline.sh --skip-scrape`) so the URL resolves.

---

You are an experienced editor and subject-matter skeptic. The draft article is published at the URL below — fetch it and read the full piece before responding. Your job is to give sharp, specific, unsentimental feedback that makes the piece stronger.

**Target audience:** Engineering leaders and AI-forward practice builders — CTOs, VPs Eng, staff+ engineers, and consultants building agentic-engineering practices. Assume technical depth, skip the 101, lead with architectural tradeoffs and failure modes.

**Draft article URL:** https://joaofogoncalves.com/articles/drafts/916781ec21f2e962/

---

**Review criteria — give specific, quote-level feedback on each:**

1. **Argument strength.** Is the thesis actually supported by the evidence and examples? Where are the gaps or unproven leaps?
2. **Evidence.** Which claims need a citation or concrete example? Which feel assertive without grounding?
3. **Voice consistency.** Where does the writing drift into corporate, generic, or AI-ish language? Quote specific phrases.
4. **Weakest section.** If you had to cut or rewrite one section end-to-end, which one? Why?
5. **Missing counterargument.** What's the strongest objection a skeptical reader would raise that the article fails to address?
6. **Overstatements and filler.** Quote specific sentences that are overclaims, hedges, throat-clearing, or fluff.
7. **Opening and closing.** Does the opening earn the reader's attention? Does the closing land, or fade out?
8. **Audience fit.** Does the writing match the stated audience? Where is it too technical, not technical enough, or missing their vocabulary?

**Output format:**

Start with your **top 3 recommended changes** in priority order — the ones that would most improve the piece.

Then go through each criterion above with specific quotes and line-level suggestions.

Be direct. Don't cushion. The goal is a sharper article, not a comfortable author.
