# LinkedIn post — most-of-the-agent-stack-still

Paste this directly into LinkedIn's composer. Zero emojis, 2-4 hashtags at the end.
Do **not** put external URLs in the body.

---

Most of the agent stack still looks like frameworks for writing agents. Google open-sourced Agent Substrate for the other half: how you run them at density, with isolation and state that survives idle time.

Agent-like workloads sit idle most of the time, so you map many actors onto fewer ready workers, suspend and resume in under half a second, and keep working memory plus filesystem across hibernation. Kubernetes still owns the pods, while Substrate owns the agent-shaped scheduling on top.

It is framework-agnostic on purpose. Claude Code sessions, MCP servers, and LangChain tools share the same lifecycle instead of asking you to rewrite against another SDK.

Early and not production-ready. The interesting claim is still the shape of the problem: the scarce layer may be the runtime that treats agents as multiplexed, stateful sessions.

#AI #Kubernetes #SoftwareEngineering #AgenticAI

---

**Attach image:** media/image-1.svg

---

**First comment (post immediately after the main post goes live):**
Source:
https://github.com/agent-substrate/substrate

---

**After posting:** copy the LinkedIn permalink and paste it into `post.md` as `post_url:`.
