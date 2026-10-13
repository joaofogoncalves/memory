---
date: 2026-10-13
post_type: original
authored: true
post_url: "https://www.linkedin.com/feed/update/urn:li:activity:7515779350768762880/"
x_url: "https://x.com/joaofogoncalves/status/2110013203119784329"
substack_note_url: "https://substack.com/@joaofogoncalves/note/c-359971357"
tags: [ai, agents]
source_urls:
  - https://arxiv.org/html/2610.07447
  - https://x.com/DimitrisPapail/status/2109661202733212136
  - https://the-decoder.com/clearing-chat-history-helps-ai-agents-find-better-solutions/
angle: We keep giving agents more memory, but sometimes the useful move is to keep the work and drop the conversation that keeps steering them back.
template: article-reaction
---

We keep giving agents more memory, with longer context windows and smarter compaction, and a new paper from Microsoft Research makes a strong case that long-running agents sometimes need the opposite.

The team, including Dimitris Papailiopoulos, ran autoresearch agents that propose a solution, score it and iterate for hours or days on hard optimization and engineering problems. Independent runs of the same agent on the same task settled at very different scores and stayed there even with more compute, because each run kept refining the family of ideas it had picked early, which the authors call an idea basin. Compacting the conversation did not get them out.

Their fix, Fork-and-Flush, periodically splits the agent into four copies that keep the full workspace and files while starting from an empty chat, lets each run for a short stretch, and continues from the highest-scoring one. At equal compute it improved the normalized average score by 66% over single runs and 44% over best-of-4, posting the highest mean score on 12 of 13 tasks, on runs that in some cases went past 100 hours.

What makes this useful in practice is the line it draws between the state an agent has built, which lives in its files, and the reasoning that built it, which lives in the chat and keeps steering the agent back toward the same approach. When a long run stalls, keeping the work and dropping the conversation is a cheap intervention to try before reaching for more context.

**Hashtags:** #AI #Agents
