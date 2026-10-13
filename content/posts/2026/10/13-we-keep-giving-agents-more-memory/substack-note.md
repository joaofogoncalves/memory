# Substack Note — 13-we-keep-giving-agents-more-memory

Paste into Substack Notes. No hashtags.

---

We keep giving agents more memory, with longer context windows and smarter compaction, and a new paper from Microsoft Research makes a strong case that long-running agents sometimes need the opposite.

The team ran autoresearch agents that propose a solution, score it and iterate for hours or days on problems like polyomino packing, job-shop scheduling and kernel optimization. Independent runs of the same agent on the same task settled at very different scores and stayed there even with more compute, because each run kept refining the family of ideas it had picked early, which the authors call an idea basin, and compacting the conversation along the way did not get them out. https://x.com/DimitrisPapail/status/2109661202733212136

Their fix, Fork-and-Flush, periodically splits the agent into four copies that keep the full workspace and files while starting from an empty chat, lets each run for a short stretch, and continues from the highest-scoring one. At equal compute it improved the normalized average score by 66% over single runs and 44% over best-of-4, posting the highest mean score on 12 of 13 tasks. https://arxiv.org/html/2610.07447

What makes this useful in practice is the line it draws between the state an agent has built, which lives in its files, and the reasoning that built it, which lives in the chat and keeps steering the agent back toward the same approach. When a long run stalls, keeping the work and dropping the conversation is a cheap intervention to try before reaching for more context.

---

**Attach image:** media/figure-basins-polyomino.png

---

**After posting:** paste the Note URL into `post.md` as `substack_note_url:`.
