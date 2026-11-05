---
date: 2026-11-05
post_type: original
authored: true
post_url: "https://www.linkedin.com/feed/update/urn:li:activity:7524032320232656896/"
x_url: "https://x.com/joaofogoncalves/status/2118265114692387225"
substack_note_url: "https://substack.com/@joaofogoncalves/note/c-379256340"
tags: [ai-security, linux, openai, cybersecurity]
source_urls:
  - https://x.com/OpenAI/status/2118119451401048497
angle: "OpenAI's kernel run is a find-and-patch pipeline at about $1,270 a bug, and the bottleneck moves to the humans who review the patches"
template: short-form
lane: ai-security
type: quote-post
visual: quoted-chart
opener: number
link_placement: end-of-body
found_via: scan
post_hour: 9
---

OpenAI's security team spent $1.2 million in API credits and ended up with 948 working local privilege escalation exploits in the Linux kernel, each with a generated patch. That is about $1,270 a bug, and the part worth reading is the funnel in their chart.

OpenAI's run started with 2,308 candidate findings. 1,724 survived validation, 1,238 were screened as privilege escalation candidates, and 948 turned into working exploits. Every one of those is a way to get root on a Linux machine that can now be closed.

What the post doesn't say is how many of the patches have been merged upstream. Finding the bugs got cheap, but reviewing hundreds of patches still takes people in the kernel community, and I'd expect that to be the next bottleneck.

I read this as good news. Hardening code at roughly $1,000 a bug is a price defenders can budget for, and the review work is something people can plan around.

Source: https://x.com/OpenAI/status/2118119451401048497
