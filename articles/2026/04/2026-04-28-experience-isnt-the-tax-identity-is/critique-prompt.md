# Critique prompt

Paste the prompt below into another AI (ChatGPT, Claude.ai, Gemini — whichever gives you a fresh perspective) for a sharp second-opinion review. The reviewer will fetch the draft directly. Bring the feedback back to Claude Code and ask for targeted revisions.

**Before pasting:** make sure the draft is deployed (`bash pipeline.sh --skip-scrape`) so the URL resolves.

---

You are an experienced editor and subject-matter skeptic. The draft article is published at the URL below — fetch it and read the full piece before responding. Your job is to give sharp, specific, unsentimental feedback that makes the piece stronger.

**Target audience:** Mixed / broad audience. Smart non-specialist. Decision-making and AI adoption framing should be accessible to PMs, founders, engineering leaders, and curious professionals — not narrowly technical, not preachy.

**Draft article URL:** https://joaofogoncalves.com/articles/drafts/6f261bbcfdf59908/

---

**Review criteria — give specific, quote-level feedback on each:**

1. **Argument strength.** Is the thesis actually supported by the evidence and examples? Where are the gaps or unproven leaps? In particular: does the "third group" reframe genuinely complicate Jaya's thesis, or is it a semantic dodge?
2. **Evidence.** Which claims need a citation or concrete example? Which feel assertive without grounding? The piece cites four sources (Jaya's article, Metaintro, Grant Thornton, Frontiers in Psychology) — are any used loosely or stretched beyond what the source supports?
3. **Voice consistency.** Where does the writing drift into corporate, generic, or AI-ish language? Quote specific phrases. The voice should be a senior engineering practitioner with hands-on AI experience — confident, dry, contrarian-but-fair.
4. **Weakest section.** If you had to cut or rewrite one section end-to-end, which one? Why?
5. **Missing counterargument.** What's the strongest objection a skeptical reader would raise that the article fails to address? In particular: is there a steelman of Jaya's "experience is a tax" thesis that survives the "third group" reframe?
6. **Overstatements and filler.** Quote specific sentences that are overclaims, hedges, throat-clearing, or fluff. Watch for the "third group is quietly winning everything" framing — does it overpromise?
7. **Opening and closing.** Does the opening earn the reader's attention given that the article is responding to another piece? Does the closing land, or fade out? The closing tries to reframe "experience is a tax" as "experience is a tax only if it calcifies" — does that land?
8. **Audience fit.** Does the writing match the stated audience? Where is it too technical, not technical enough, or missing their vocabulary? The piece is for a mixed audience — flag any sections that lean too hard into engineering specifics or, conversely, get too vague to be useful.

**Output format:**

Start with your **top 3 recommended changes** in priority order — the ones that would most improve the piece.

Then go through each criterion above with specific quotes and line-level suggestions.

Be direct. Don't cushion. The goal is a sharper article, not a comfortable author.
