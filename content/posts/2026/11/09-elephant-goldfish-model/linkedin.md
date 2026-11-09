# LinkedIn: elephant-goldfish-model

Published ~08:50 Europe/Lisbon on 2026-11-09 with the 66-second Google Cloud Tech explainer attached as native video (same clip as https://x.com/GoogleCloudTech/status/2119203243054023129; the clip is not stored in the repo, same as AirPointer). Google was tagged to https://www.linkedin.com/company/google/. Source link at the end of the body; LinkedIn rewrote it to https://lnkd.in/eERbWVe4.

---

The agent that writes a design should not be the one that reviews it. That's the whole idea behind Google's Elephant-Goldfish Model, and I think it's the most useful habit in agentic coding right now.

It started inside Google, where they say thousands of engineers use it every day to ship production code. Last month @Google open-sourced it as a plugin that works with Antigravity, Claude Code, Codex and ChatGPT.

How it works:
1. The elephant, an agent with the full project context, helps you brainstorm and drafts the spec.
2. Goldfish reviewers read only that draft and the source it points to, in fresh sessions with none of the earlier conversation.
3. You resolve what they find, loop until the design holds up, and make the architectural calls before any code gets written.

The first thing a goldfish does is explain the spec back. If it can't, the document is still ambiguous, however clear it felt to the agent that wrote it.

That's the part I'd copy even without the plugin. A long session piles up assumptions that feel settled because they were discussed an hour ago. A reviewer that wasn't in the room only has the document, so the gaps show up before they turn into code.

The repo is clear that this doesn't replace tests or your own judgment. It just puts a cheap, honest review at the point where changing your mind costs the least.

https://opensource.googleblog.com/2026/10/introducing-elephant-goldfish-model-plugin.html
