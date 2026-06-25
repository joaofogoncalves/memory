---
date: 2026-04-22
post_type: original
authored: true
post_url: "https://www.linkedin.com/posts/joaofogoncalves_opensource-devops-selfhosted-share-7452688127594450944-4r7C"
x_url: "https://x.com/joaofogoncalves/status/2046923364661395503"
substack_note_url: "https://substack.com/profile/113523350-joaofogoncalves/note/c-247338394"
tags: [opensource, devops, infrastructure, engineering, bridgeport]
source_urls:
  - https://www.bridgein.pt/blog/bridgeport-open-source-deployment-management
angle: Personal take on why BRIDGEPORT went open source — 15 years of seeing the same infra problem across companies, the specific moment that triggered the build, and why the problem isn't ours to hoard.
template: short-form
media_descriptions:
  image-1.webp: >-
    Screenshot/preview of the linked bridgein.pt blog post. White background
    serif headline "Building in Public: How we built BRIDGEPORT to solve
    our own deployment problem" above a wide hero image: a dark cinematic
    motion-blurred shot of glowing red "BRIDGEPORT" wordmark with a
    glitchy/streaked motion effect, looking like a sci-fi movie title card.
    External brand asset, light-mode at top with dark hero below.
---

Fifteen years in infrastructure teaches you what breaks.

The 2am debugging sessions. Teams drowning in tooling that was supposed to help and somehow added more complexity than it solved. Same pattern, different companies.

BRIDGEPORT started with one specific moment: a config change that touched multiple servers, our cloud provider's UI, our secret manager, and a handful of services that each needed a restart and a health check after.

There has to be a single place for all of this.

There wasn't. So I built it.

Today we're open-sourcing it. Self-hosted, lightweight, small enough that you can actually read the code.

The reasoning is simple. The problem isn't ours. Anyone running distributed infrastructure has felt the same friction. Keeping the tool private would have meant hoarding a solution to a shared problem.

The best way to make it better is to put it in front of people who'll push it in directions I never imagined.

Fork it, break it, improve it.

More on why we open-sourced it: https://www.bridgein.pt/blog/bridgeport-open-source-deployment-management

**Hashtags:** #OpenSource #DevOps #SelfHosted
