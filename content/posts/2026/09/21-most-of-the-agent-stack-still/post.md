---
date: 2026-09-21
post_type: original
authored: true
post_url: "https://www.linkedin.com/feed/update/urn:li:share:7507773870125477888/"
x_url: "https://x.com/joaofogoncalves/status/2102007878714347546"
substack_note_url: "https://substack.com/profile/113523350-joaofogoncalves/note/c-342233326"
tags: [ai, kubernetes, software-engineering, agentic-ai]
source_urls:
  - https://github.com/agent-substrate/substrate
  - https://www.youtube.com/watch?v=ZEzkCFJkzjY
angle: Runtime not SDK — scarce layer is running agents at density with isolation and state
template: short-form
---

Most of the agent stack still looks like frameworks for writing agents. Google open-sourced Agent Substrate for the other half: how you run them at density, with isolation and state that survives idle time.

Agent-like workloads sit idle most of the time, so you map many actors onto fewer ready workers, suspend and resume in under half a second, and keep working memory plus filesystem across hibernation. Kubernetes still owns the pods, while Substrate owns the agent-shaped scheduling on top.

It is framework-agnostic on purpose. Claude Code sessions, MCP servers, and LangChain tools share the same lifecycle instead of asking you to rewrite against another SDK.

Early and not production-ready. The interesting claim is still the shape of the problem: the scarce layer may be the runtime that treats agents as multiplexed, stateful sessions.

**Hashtags:** #AI #Kubernetes #SoftwareEngineering #AgenticAI
