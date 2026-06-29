---
date: 2026-06-29
post_type: original
authored: true
post_url: "https://www.linkedin.com/posts/joaofogoncalves_ai-promptengineering-llm-share-7477400802844774400-5sV_/"
x_url: "https://x.com/joaofogoncalves/status/2071635514600325622"
substack_note_url: "https://substack.com/profile/113523350-joaofogoncalves/note/c-284937888"
tags: [ai, promptengineering, llm]
source_urls:
  - https://arxiv.org/html/2606.26300v1
angle: "Explicit intent is the lever. The Qwen 'Verification Horizon' paper shows intent is unmeasurable (every verifier is only a proxy); the same gap shows up when prompting, so making intent explicit shrinks it. Bridges the training finding to inference."
template: article-reaction
---

Verifying what a coding agent built is now harder than building it. A new paper from the Qwen team says why: intent can't be measured. Every verifier you build is only a proxy for what you actually wanted, never the thing itself.

The paper is about training. But you hit the same gap every time you prompt.

The model has the capability. It's being asked to infer an intent you kept in your head, then graded against your private copy of it. And evaluating intent is hard for the model because it's hard for us. It's subjective, observer-dependent. We can't cleanly say what we meant, then act surprised the guess misses.

So the lever is yours, not the model's: how explicitly you state the intent. Make it an actual goal and the proxy gap shrinks. We've been drifting toward this by feel. The paper is why it works.

The model was never guessing wrong. You were never saying.

**Hashtags:** #AI #PromptEngineering #LLM

---

## Media

![image-1.webp](media/image-1.webp)

![image-2.webp](media/image-2.webp)
