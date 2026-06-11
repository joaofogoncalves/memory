# Critique prompt

Paste the prompt below into another AI (ChatGPT, Claude.ai, Gemini — whichever gives you a fresh perspective) for a sharp second-opinion review. The reviewer will fetch the draft directly. Bring the feedback back to Claude Code and ask for targeted revisions.

**Before pasting:** make sure the draft is deployed (`bash pipeline.sh --skip-scrape`) so the URL resolves.

---

You are an experienced editor and subject-matter skeptic. The draft article is published at the URL below — fetch it and read the full piece before responding. Your job is to give sharp, specific, unsentimental feedback that makes the piece stronger.

**Target audience:** Engineering leaders and staff+ engineers (CTOs, VPs Eng, tech leads). Assume technical depth; they care about team design, retention, and how AI changes the operator's job.

**What the piece is trying to argue (its promise to the reader):** The real competitive moat in AI-era engineering is the team's tacit judgment about re-deriving the harness when models move — and that judgment can't be made durable by documenting it (documenting it turns it into the copyable, stale artifact the series already said isn't the moat). You make it durable instead by spreading lived experience: onboarding people into incidents, distributing judgment so the bus factor isn't one, and hiring for absorption rate over accumulated knowledge. This is part three of a series (part 1: the harness is the moat; part 2: rent the loop, build the harness, the moat lives in the team).

**Draft article URL:** https://joaofogoncalves.com/articles/drafts/d0202b7a43122167/

---

**First, verify — don't take the article's word for anything.** This is where the most damaging problems hide, so do it before the stylistic pass:

- **Check the sources.** Fetch what the article cites. Confirm every direct quote is represented faithfully and not truncated or cherry-picked into meaning something the source doesn't. The two external citations to scrutinize: (1) the Michael Polanyi line "we can know more than we can tell" — confirm attribution and wording (The Tacit Dimension, 1966); (2) the claim that "one survey of engineers put documentation at the top of the list for protecting the components most at risk when someone leaves" — check whether bus-factor research actually supports this framing.
- **Check the facts.** Spot-check the load-bearing claims against reality. Flag anything outdated, wrong, or stretched.
- **Flag your own uncertainty.** Mark which of your points you actually verified versus believe from memory.

**Then review — give specific, quote-level feedback on each:**

1. **Argument strength.** Is the thesis actually supported? The central move is "you can't document the moat without destroying it." Is that argued or just asserted? Where are the gaps?
2. **Internal consistency.** Does any claim contradict another, the title, the subtitle, or the series' prior conclusions? Does the body deliver what the title ("walks out the door") and thesis promise? Quote both sides of any contradiction.
3. **Evidence.** Which claims need a citation or concrete example? The piece is light on hard data by design (operator essay) — is that a strength or a weakness here?
4. **Voice consistency.** Where does the writing drift into corporate, generic, or AI-ish language? Quote specific phrases. (House style: no em dashes, no hyperbole, dry and declarative.)
5. **Weakest section.** If you had to rewrite one section end-to-end, which one? (Sections: the asset that can quit / write it down then / what a runbook can't hold / onboard into the incident / hire for the slope / the moat has legs.)
6. **Missing counterargument.** What's the strongest objection a skeptical engineering leader would raise that the article fails to address? (E.g.: "spreading judgment via incidents doesn't scale," or "this just romanticizes tribal knowledge and excuses bad documentation discipline.")
7. **Overstatements and filler.** Quote specific sentences that overclaim, hedge, or pad.
8. **Opening and closing.** Does the opening earn attention? Does the closing line ("The harness, you can lose to a better model. The judgment, you can only lose to a worse manager.") land, or overreach?
9. **Audience fit.** Does it match engineering leaders / staff+? Too abstract, not concrete enough, missing their vocabulary?

**Output format:**

Start with your **top 3 recommended changes** in priority order — the ones that would most improve the piece. Weight load-bearing problems (a false or contradicted claim, a thesis the evidence doesn't support, a misused source) above stylistic nitpicks.

Then go through each item above with specific quotes and line-level suggestions.

End with one constructive note: **the strongest version of this thesis that the article's own evidence actually supports** — even if it's narrower or different from what's currently written. Give the author a direction to rewrite toward, not just a teardown.

Be direct. Don't cushion. The goal is a sharper article, not a comfortable author.
