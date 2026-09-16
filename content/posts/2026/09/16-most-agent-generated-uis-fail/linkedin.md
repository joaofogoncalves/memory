# LinkedIn post — most-agent-generated-uis-fail

Paste this directly into LinkedIn's composer. Zero emojis, 2-4 hashtags at the end.
Do **not** put external URLs in the body. Tag @shadcn when composing (LinkedIn mention).

---

Most agent-generated UIs fail the same quiet way: Tailwind className is a string, so there is nothing to refuse when an agent overrides padding, color, or shape on a component that already has a contract.

An agent-first linter for Tailwind design systems just landed from @shadcn. You define what is allowed, and when an agent breaks a rule the error explains what went wrong and how to fix it using your components, variants, and theme.

Verification lives in that failure message. A prompt file can drift, while a lint rule that fails the build with your Button variants in the message is a feedback loop the agent can actually close.

The design system holds when the refusal surface is machine-checkable.

#AI #SoftwareEngineering #DesignSystems #Tailwind

---

**Attach image:** media/image-1.svg

---

**First comment (post immediately after the main post goes live):**
Source:
https://x.com/shadcn/status/2099534231114314145

---

**After posting:** copy the LinkedIn permalink and paste it into `post.md` as `post_url:`.
