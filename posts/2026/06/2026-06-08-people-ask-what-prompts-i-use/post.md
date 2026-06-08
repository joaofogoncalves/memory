---
date: 2026-06-08
post_type: original
authored: true
post_url: ""
x_url: ""
substack_note_url: "https://substack.com/profile/113523350-joaofogoncalves/note/c-272937555"
tags: [ai, agents, software-engineering]
source_urls:
  - https://joaofogoncalves.com/articles/2026/06/2026-06-08-the-harness-is-the-moat/
angle: "Article promo for 'The Harness Is the Moat' — prompt-vs-system, the harness is the hard and owned part. Reinforces the thesis, does not summarize; teases part 2."
template: article-reaction
---

People ask what prompts I use to run a multi-agent system in production. It's the wrong question.

The prompts took an afternoon. The system took months.

The months went into the harness. How agents share one repo without writing over each other. What an agent can do without a human in the loop, and what it can never touch. The verification gates that catch the confident, plausible, wrong output before it reaches a customer. The recovery path for when an agent dies mid-feature and the next one has to pick up where it left off.

That's the part no benchmark scores. A better model climbs SWE-bench. It still doesn't coordinate your worktrees or know your deploy gates.

The model is the commodity. The harness is the moat.

Wrote the long version, with the receipts: https://joaofogoncalves.com/articles/2026/06/2026-06-08-the-harness-is-the-moat/

Part two, on what to actually build and own, is next.

**Hashtags:** #AI #Agents #SoftwareEngineering
