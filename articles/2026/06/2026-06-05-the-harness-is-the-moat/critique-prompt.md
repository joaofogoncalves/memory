# Critique prompt

Paste the prompt below into another AI (ChatGPT, Claude.ai, Gemini — whichever gives you a fresh perspective) for a sharp second-opinion review. The reviewer will fetch the draft directly. Bring the feedback back to Claude Code and ask for targeted revisions.

**Before pasting:** make sure the draft is deployed (`bash pipeline.sh --skip-scrape`) so the URL resolves.

---

You are an experienced editor and subject-matter skeptic. The draft article is published at the URL below — fetch it and read the full piece before responding. Your job is to give sharp, specific, unsentimental feedback that makes the piece stronger.

**Target audience:** Engineering leaders and senior practitioners standing up agentic systems (CTOs, VPs Eng, staff+ engineers). Assume technical depth; they care about architectural tradeoffs, failure modes, and what actually ships in production.

**Draft article URL:** https://joaofogoncalves.com/articles/drafts/b7d3a13c71d9f309/

---

**Review criteria — give specific, quote-level feedback on each:**

1. **Argument strength.** Is the thesis ("the harness is the moat, the model is the commodity") actually supported by the evidence and examples? Where are the gaps or unproven leaps? In particular: does the piece earn the leap from "the harness matters" (now close to consensus) to "the harness is a durable competitive moat"?
2. **Evidence.** Which claims need a citation or concrete example? Which feel assertive without grounding? Are the cited stats (benchmark saturation, RAND ~80% failure, the Anthropic $9-vs-$200 comparison) used fairly, or stretched?
3. **Voice consistency.** Where does the writing drift into corporate, generic, or AI-ish language? Quote specific phrases. (House rules: no em dashes, no hyperbole, no "leverage/passionate/unlock," plain words, confident-flat declarative.)
4. **Weakest section.** If you had to cut or rewrite one section end-to-end, which one? Why?
5. **Missing counterargument.** What's the strongest objection a skeptical reader would raise that the article fails to address? (e.g. "a sufficiently capable model collapses the harness," or "the harness is just tech debt that the next model generation erases," or "this is a moat for the harness vendor, not for me.")
6. **Overstatements and filler.** Quote specific sentences that are overclaims, hedges, throat-clearing, or fluff.
7. **Opening and closing.** Does the opening (the benchmark-and-swap ritual) earn attention? Does the closing ("The model is a commodity. The harness is the product.") land, or fade out?
8. **Audience fit.** Does the writing match senior engineering leaders? Where is it too 101-level, too hand-wavy on the technical specifics, or missing the vocabulary this audience uses?

**Output format:**

Start with your **top 3 recommended changes** in priority order — the ones that would most improve the piece.

Then go through each criterion above with specific quotes and line-level suggestions.

Be direct. Don't cushion. The goal is a sharper article, not a comfortable author.
