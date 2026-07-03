---
date: 2026-07-03
post_type: original
authored: true
post_url: "https://www.linkedin.com/posts/joaofogoncalves_selfhosted-devops-opensource-share-7478814997784018947-yhGa/"
x_url: "https://x.com/joaofogoncalves/status/2073049565310120211"
substack_note_url: "https://substack.com/profile/113523350-joaofogoncalves/note/c-287423693"
tags: [selfhosted, devops, opensource, infrastructure]
source_urls:
  - https://bridgeport.bridgein.com/roadmap/
angle: Self-hosted infra tools don't lose to managed platforms on features — they lose on trust. Milestone 4.0 is a deliberate trust-building move (safe rollouts, proactive alerts, real DR, SSO/2FA/audit export), not a feature dump.
template: article-reaction
---

Self-hosted infrastructure tools don't lose to AWS or Vercel on features. They lose on trust.

Nobody evaluates a deploy tool by asking if it can run a container. They ask what happens when someone leaves the company, whether an audit log can leave the building, and whether a bad rollout gets undone before anyone notices. Alerts either fire before the outage or show up after it, as a postmortem.

That's the shape of milestone 4.0 on the BridgePort roadmap: one-click rollback and phased rollouts, threshold alerts, backup restore instead of backup-only, SSO, 2FA, audit-log export, secrets pulled from Vault instead of hardcoded into a compose file.

None of it is a feature anyone asks for on day one. It's the reason a team says yes on day 400.

Even the page itself makes the point. Generated straight from the GitHub tracker, no fake dates. Directions, not commitments.

Roadmap: https://bridgeport.bridgein.com/roadmap/

**Hashtags:** #SelfHosted #DevOps #OpenSource #Infrastructure
