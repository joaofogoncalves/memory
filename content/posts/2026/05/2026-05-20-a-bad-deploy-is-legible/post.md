---
date: 2026-05-20
post_type: original
authored: true
post_url: "https://www.linkedin.com/feed/update/urn:li:activity:7462868545165479937/"
x_url: "https://x.com/joaofogoncalves/status/2057103333928706529"
substack_note_url: "https://substack.com/@adfectusadulatio393615/note/c-262187695"
tags: [ai, software-engineering, devops, engineering-leadership]
source_urls:
  - https://joaofogoncalves.com/articles/2026/05/2026-05-20-building-the-road-to-production-again/
angle: The cheap-failure doctrine breaks because it assumed failure was detectable — agent-PR loops produce illegible failure that accumulates as architectural drift.
template: article-reaction
---

A bad deploy is legible.

The alert fires, the rollback runs, blast radius is the customer base, recovery is measured in minutes. That's why two-week cycles worked. Failure was cheap because failure was loud.

A bad agentic pattern is illegible.

The PR passes lint and tests. The reviewer agent approves. The diff merges. Six months later you're untangling architectural drift you can't trace to a single decision, because no single decision caused it. It accumulated across hundreds of PRs that each looked locally fine.

The cheap-failure doctrine that made the old SDLC work assumed failure was detectable. That assumption is what breaks.

Most teams building the agent-PR loop got the throughput right. They didn't replace the part that always asked: would we notice if this was wrong?

The loop runs faster. It doesn't see better.

Full piece, with what the new detection layer actually has to do:
https://joaofogoncalves.com/articles/2026/05/2026-05-20-building-the-road-to-production-again/

**Hashtags:** #AI #SoftwareEngineering #DevOps #EngineeringLeadership
