# Substack Note — verifying-what-a-coding-agent-built

Paste into Substack Notes (substack.com/notes). No hashtags. Link welcome inline.

---

There's a new Qwen paper arguing that verifying what a coding agent built is now harder than building it. The reason: intent can't be measured. Every verifier you build is only a proxy for what you actually wanted, never the thing itself.

It's about training. But you hit the same gap every time you prompt.

The model has the capability. It's being asked to infer an intent you kept in your head, then graded against your private copy of it. And evaluating intent is hard for the model because it's hard for us. It's subjective, observer-dependent. We can't cleanly say what we meant, then act surprised the guess misses.

So the lever is yours, not the model's: how explicitly you state the intent. Make it a real goal and the proxy gap shrinks.

The model was never guessing wrong. You were never saying.

Paper: https://arxiv.org/html/2606.26300v1

---

**Attach inline (in order):**
- media/image-1.webp (the quote card)
- media/image-2.webp (the paper's verifier/policy co-evolution figure)

---

**After posting:** copy the Note URL and paste it into `post.md` as `substack_note_url:`.
