---
date: 2026-06-28
post_type: original
authored: true
post_url: "https://www.linkedin.com/posts/joaofogoncalves_mcp-selfhosted-opensource-share-7477264270947393536-1b-6/"
x_url: "https://x.com/joaofogoncalves/status/2071499235384549609"
substack_note_url: "https://substack.com/profile/113523350-joaofogoncalves/note/c-284695287"
tags: [mcp, selfhosted, opensource, devtools]
source_urls:
  - https://joaofogoncalves.com/articles/2026/06/28-two-features-one-contract/
angle: "BridgePort 3.0 release promo. Lead with the announcement (Terraform provider + MCP server), then the no-model / BYO-model decision and why self-hosted is the right posture for an infra tool."
template: article-reaction
---

BridgePort 3.0 is out, with two new ways to drive it.

A Terraform provider, so your environments, servers, secrets, and services live in version control and `terraform plan` shows drift before it bites. And an MCP server, so you can operate it from an AI agent in your editor.

The MCP server is the interesting one, because it runs no model.

Every obvious "AI feature" pointed the other way. Log triage, drift explained in plain English, a risk score on a deploy. Each one means the tool holds an API key, pays for inference, and ships your logs, config, and topology to a third-party model. For a self-hosted control plane that already holds your SSH keys and secrets, that is a lot of new surface for a summary.

So it exposes tools instead, and the model lives in your own client, on your own account. That hands you a choice BridgePort shouldn't make for you: a cheap model when the task is simple, a local self-hosted one when it isn't, so your infrastructure data never leaves your network. For a tool that holds the keys to your infra, the self-hosted option is usually the right one.

The hard call was the one not to build.

It's all open source. Wrote up how the two surfaces are the same API contract projected two ways:

https://joaofogoncalves.com/articles/2026/06/28-two-features-one-contract/

**Hashtags:** #MCP #SelfHosted #OpenSource #DevTools
