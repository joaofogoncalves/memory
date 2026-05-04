# Critique prompt

Paste the prompt below into another AI (ChatGPT, Claude.ai, Gemini — whichever gives you a fresh perspective) for a sharp second-opinion review. The reviewer will fetch the draft directly. Bring the feedback back to Claude Code and ask for targeted revisions.

**Before pasting:** make sure the draft is deployed (`bash pipeline.sh --skip-scrape`) so the URL resolves.

---

You are an experienced editor and subject-matter skeptic. The draft article is published at the URL below — fetch it and read the full piece before responding. Your job is to give sharp, specific, unsentimental feedback that makes the piece stronger.

**Target audience:** Engineering leaders and senior engineers — Staff/Principal ICs, EMs, Directors, VPs, CTOs at AI-adopting companies. Smart, time-poor, allergic to hype, have been using AI tools long enough to have opinions. Tone should be peer-to-peer, not didactic.

**Draft article URL:** https://joaofogoncalves.com/articles/drafts/dafd43db55d9a550/

---

**Review criteria — give specific, quote-level feedback on each:**

1. **Argument strength.** Is the central thesis — that AI is a "Great Filter" selecting against engineers without depth — actually supported, or is it just a catchy frame stretched over conventional advice ("review your AI code", "use it carefully")? Where are the unproven leaps? Does the Hanson Great Filter analogy earn its weight, or is it decorative?
2. **Evidence.** The piece relies on five anchors: the Amazon Kiro / Cost Explorer outage, the two Amazon retail outages (6.3M orders, 12 hours), BullshitBench (Sonnet 4.6 ~90% pushback vs ~50% average), the SycEval and medical-domain sycophancy papers, and the 43% AI-code-debug-in-production survey. Are any used loosely or stretched beyond what they support? Any that need a hedge or a more specific citation? The Amazon incidents are real and recent — flag if the framing reads as cherry-picked rather than representative.
3. **Voice consistency.** Where does the writing drift into corporate, generic, or AI-ish language? Quote specific phrases. The voice should be a senior engineering practitioner with hands-on AI experience — confident, dry, peer-to-peer, opinionated but fair. No motivational or self-help cadence.
4. **Weakest section.** If you had to cut or rewrite one section end-to-end, which one? Why? Specifically — does **The gambling loop** earn its length, or is the slot-machine metaphor over-extended? Does **What survives the filter** drift into generic "depth matters" rhetoric?
5. **Missing counterargument.** What's the strongest objection a skeptical reader would raise? In particular: (a) the "shallow engineers will get filtered" claim could be read as gatekeeping — does the piece earn that take, or does it owe more nuance? (b) is there a steelman where AI actually closes the depth gap (rather than widening it) for the next generation, by acting as a tutor rather than a substitute?
6. **Overstatements and filler.** Quote specific sentences that are overclaims, hedges, throat-clearing, or fluff. In particular: "Both engineers are using the same tool. They're getting completely different outcomes" — does the dichotomy oversimplify? Are there sentences in the closer ("selected against, quietly") that read as dramatic without earning it?
7. **Opening and closing.** Does the cold open with the Amazon Kiro incident hook the right audience, or does it feel like clickbait? Does the Hanson framing pay off in the closer — does "the gap between depth and the appearance of depth" actually land, or fade?
8. **Audience fit.** Does the writing match the stated audience? Where is it too technical, not technical enough, or missing engineering-leader vocabulary? Flag any sections that lean too hard into philosophy and lose the engineering-leader reader, or conversely get too tactical and lose the strategic frame.
9. **Originality of frame.** The "AI selects for depth" argument has been made before in various shapes (Karpathy, Patel, others). Does this piece add a genuinely new angle (the Hanson analogy + the gambling-loop mechanism + the "selection not extinction" reframe), or is it remixing existing takes? Where could the framing be sharpened to feel less familiar?

**Output format:**

Start with your **top 3 recommended changes** in priority order — the ones that would most improve the piece.

Then go through each criterion above with specific quotes and line-level suggestions.

Be direct. Don't cushion. The goal is a sharper article, not a comfortable author.
