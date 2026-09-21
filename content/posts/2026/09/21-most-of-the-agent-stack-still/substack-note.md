# Substack Note — most-of-the-agent-stack-still

Paste into Substack Notes (substack.com/notes). No hashtags. Links welcome.

---

Google open-sourced Agent Substrate for the half of the stack that is usually missing: how you run agents at density, with isolation and state that survives idle time.

Agent-like workloads sit idle most of the time, so you map many actors onto fewer ready workers, suspend and resume in under half a second, and keep working memory plus filesystem across hibernation. Kubernetes still owns the pods, while Substrate owns the agent-shaped scheduling on top.

It is framework-agnostic on purpose. Claude Code sessions, MCP servers, and LangChain tools share the same lifecycle instead of asking you to rewrite against another SDK.

Early and not production-ready. The interesting claim is still the shape of the problem: the scarce layer may be the runtime that treats agents as multiplexed, stateful sessions.

https://github.com/agent-substrate/substrate

---

**Attach image:** media/image-1.svg

---

**After posting:** copy the Note URL and paste it into `post.md` as `substack_note_url:`.
