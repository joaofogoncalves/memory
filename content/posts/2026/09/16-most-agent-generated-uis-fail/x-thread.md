# X post — most-agent-generated-uis-fail

Paste into X manually. No hashtags.

---

**Main post:**
Most agent-generated UIs fail the same quiet way: Tailwind className is a string, so there is nothing to refuse when an agent overrides padding, color, or shape on a component that already has a contract.

An agent-first linter for Tailwind design systems just landed from @shadcn. You define what is allowed, and when an agent breaks a rule the error explains what went wrong and how to fix it using your components, variants, and theme.

Verification lives in that failure message. A prompt file can drift, while a lint rule that fails the build with your Button variants in the message is a feedback loop the agent can actually close.

The design system holds when the refusal surface is machine-checkable.
*Attach: media/image-1.png*

**Reply (link):**
Source:
https://x.com/shadcn/status/2099534231114314145

---

**After posting:** copy the X permalink (of the main post) and paste it into `post.md` as `x_url:`.
