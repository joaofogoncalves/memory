# X post — self-hosted-infrastructure-tools-dont-lose-to-aws

Paste into X manually. No hashtags.

---

**Main post:**
Self-hosted infrastructure tools don't lose to AWS or Vercel on features. They lose on trust.

Nobody evaluates a deploy tool by asking if it can run a container. They ask what happens when someone leaves the company, whether an audit log can leave the building, and whether a bad rollout gets undone before anyone notices. Alerts either fire before the outage or show up after it, as a postmortem.

That's the shape of milestone 4.0 on the BridgePort roadmap: one-click rollback and phased rollouts, threshold alerts, backup restore instead of backup-only, SSO, 2FA, audit-log export, secrets pulled from Vault instead of hardcoded into a compose file.

None of it is a feature anyone asks for on day one. It's the reason a team says yes on day 400.

Even the page itself makes the point. Generated straight from the GitHub tracker, no fake dates. Directions, not commitments.
*Attach: media/image-1.webp*

**Reply (link):**
Roadmap:
https://bridgeport.bridgein.com/roadmap/

---

**After posting:** copy the X permalink (of the main post) and paste it into `post.md` as `x_url:`.
