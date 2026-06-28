# Critique prompt

Paste the prompt below into another AI (ChatGPT, Claude.ai, Gemini — whichever gives you a fresh perspective) for a sharp second-opinion review. The reviewer will fetch the draft directly. Bring the feedback back to Claude Code and ask for targeted revisions.

**Before pasting:** make sure the draft is deployed (`bash scripts/pipeline.sh --skip-scrape`) so the URL resolves.

---

You are an experienced editor and subject-matter skeptic. The draft article is published at the URL below — fetch it and read the full piece before responding. Your job is to give sharp, specific, unsentimental feedback that makes the piece stronger.

**Target audience:** Builders of developer tools and OSS, plus engineering leaders. They know Terraform, MCP, OpenAPI, and SQLite. The transferable lesson is the point; BridgePort is the worked example.

**What the piece is trying to argue (its promise to the reader):** BridgePort 3.0's Terraform provider and MCP server are the same hardened API contract projected onto two surfaces, declarative and conversational. The real work was hardening the contract (typed OpenAPI from Zod, an importable Go client kept in lockstep, a stability policy, scopes, idempotency); once that exists, a new surface is mostly a projection. A sub-argument: a self-hosted tool should not embed an LLM — expose tools via MCP and let the operator bring the model.

**Draft article URL:** https://joaofogoncalves.com/articles/drafts/e3a297b612febe2c/

---

**First, verify — don't take the article's word for anything.** This is where the most damaging problems hide, so do it before the stylistic pass:

- **Check the sources.** Fetch what the article cites (the Speakeasy, HashiCorp, Christian Posta, and Northflank links, and the linked prior posts/articles). Confirm every claim attributed to them is represented faithfully and not stretched. Flag any link used to support a point the source doesn't actually make.
- **Check the facts.** Spot-check the load-bearing technical claims against current reality: how a Zod-to-OpenAPI type provider actually works, MCP's Streamable HTTP transport and the stateless server model, Terraform write-only arguments and offline `plan`, SQLite `SQLITE_BUSY`/busy-timeout behavior, and the idempotency-key semantics. Flag anything outdated, wrong, or overstated. (You can't see the private BridgePort repo, so treat repo-specific specifics as the author's claim — focus on whether the general mechanisms described are accurate.)
- **Flag your own uncertainty.** Mark which points you actually verified versus believe from memory, so the author doesn't chase a correction that turns out to be your error.

**Then review — give specific, quote-level feedback on each:**

1. **Argument strength.** Is the "one contract, two surfaces" thesis actually supported by the evidence? Where are the gaps or unproven leaps? Does the "don't embed an LLM" sub-argument hold up, or is it too convenient?
2. **Internal consistency.** Does any claim contradict another, the title, the subtitle, or the article's own evidence? Does the body deliver what the title and thesis promise? Quote both sides of any contradiction.
3. **Evidence.** Which claims need a citation or concrete example they don't have? Which technical assertions feel confident but ungrounded?
4. **Voice consistency.** The piece is deliberately calm, declarative, and reportage-style (not a punchy opinion essay). Where does it drift into corporate, promotional, or AI-ish language? Quote specific phrases. Also flag the opposite failure: anywhere it's so flat it loses the reader.
5. **Weakest section.** If you had to cut or rewrite one section end-to-end, which one and why?
6. **Missing counterargument.** What's the strongest objection a skeptical builder would raise? (For example: is "the contract made the features cheap" survivorship bias? Is curating ~55 of 251 tools actually a limitation dressed up as a virtue? Is BYO-model just punting the AI problem to the user?) Does the article address it?
7. **Overstatements and filler.** Quote sentences that overclaim or pad.
8. **Opening and closing.** Does the opening earn attention without a hook gimmick? Does the closing land, or fade?
9. **Audience fit.** Does the depth match builders and engineering leaders? Where is it too shallow to be useful, or too deep to follow? Is there a tactical detail a would-be implementer would still be missing?

**Output format:**

Start with your **top 3 recommended changes** in priority order — the ones that would most improve the piece. Weight load-bearing problems (a false or contradicted claim, a thesis the evidence doesn't support, a misused source) above stylistic nitpicks.

Then go through each item above with specific quotes and line-level suggestions.

End with one constructive note: **the strongest version of this thesis that the article's own evidence actually supports** — even if it's narrower or different from what's currently written. Give the author a direction to rewrite toward, not just a teardown.

Be direct. Don't cushion. The goal is a sharper article, not a comfortable author.
