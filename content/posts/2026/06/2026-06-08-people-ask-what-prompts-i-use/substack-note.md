# Substack Note — people-ask-what-prompts-i-use

Paste into Substack Notes (substack.com/notes). No hashtags. Links welcome.

---

People ask what prompts I use to run a multi-agent system in production. It's the wrong question.

The prompts took an afternoon. The system took months.

The months went into the harness. How agents share one repo without writing over each other. What an agent can do without a human in the loop, and what it can never touch. The verification gates that catch the confident, plausible, wrong output before it reaches a customer. The recovery path for when an agent dies mid-feature and the next one has to pick up where it left off.

That's the part no benchmark scores. A better model climbs SWE-bench. It still doesn't coordinate your worktrees or know your deploy gates.

The model is the commodity. The harness is the moat.

Full piece, with the receipts: https://joaofogoncalves.com/articles/2026/06/2026-06-08-the-harness-is-the-moat/

Part two, on what to build and own, is next.

---

**Attach image:** media/article-card.webp

---

**After posting:** copy the Note URL and paste it into `post.md` as `substack_note_url:`.
