# LinkedIn post — 13-we-keep-giving-agents-more-memory

Paste this directly into LinkedIn's composer. Zero emojis, hashtags at the end.
Do **not** put external URLs in the body.

---

We keep giving agents more memory, with longer context windows and smarter compaction, and a new paper from @Microsoft Research makes a strong case that long-running agents sometimes need the opposite.

The team, including @Dimitris Papailiopoulos, ran autoresearch agents that propose a solution, score it and iterate for hours or days on hard optimization and engineering problems. Independent runs of the same agent on the same task settled at very different scores and stayed there even with more compute, because each run kept refining the family of ideas it had picked early, which the authors call an idea basin. Compacting the conversation did not get them out.

Their fix, Fork-and-Flush, periodically splits the agent into four copies that keep the full workspace and files while starting from an empty chat, lets each run for a short stretch, and continues from the highest-scoring one. At equal compute it improved the normalized average score by 66% over single runs and 44% over best-of-4, posting the highest mean score on 12 of 13 tasks, on runs that in some cases went past 100 hours.

What makes this useful in practice is the line it draws between the state an agent has built, which lives in its files, and the reasoning that built it, which lives in the chat and keeps steering the agent back toward the same approach. When a long run stalls, keeping the work and dropping the conversation is a cheap intervention to try before reaching for more context.

#AI #Agents

---

**Attach image:** media/figure-basins-polyomino.png

---

**First comment:**
The Fork-and-Flush paper from Microsoft Research:
https://arxiv.org/html/2610.07447

**Second comment:**
Dimitris Papailiopoulos on idea basins:
https://x.com/DimitrisPapail/status/2109661202733212136

**Third comment:**
The Decoder's write-up:
https://the-decoder.com/clearing-chat-history-helps-ai-agents-find-better-solutions/

---

**After posting:** copy the LinkedIn permalink and paste it into `post.md` as `post_url:`.
