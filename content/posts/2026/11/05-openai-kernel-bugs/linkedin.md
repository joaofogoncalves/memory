# LinkedIn: openai-kernel-bugs

Published with the chart image from OpenAI's post attached ("One thousand fewer paths to root"; the image is not stored in the repo). OpenAI (first paragraph) is a LinkedIn @ mention of the company page https://www.linkedin.com/company/openai/ in the published post, written here as a plain name. Source link at the end of the body; it shows as a shortened LinkedIn link when published.

---

OpenAI's security team spent $1.2 million in API credits and ended up with 948 working local privilege escalation exploits in the Linux kernel, each with a generated patch. That is about $1,270 a bug, and the part worth reading is the funnel in their chart.

OpenAI's run started with 2,308 candidate findings. 1,724 survived validation, 1,238 were screened as privilege escalation candidates, and 948 turned into working exploits. Every one of those is a way to get root on a Linux machine that can now be closed.

What the post doesn't say is how many of the patches have been merged upstream. Finding the bugs got cheap, but reviewing hundreds of patches still takes people in the kernel community, and I'd expect that to be the next bottleneck.

I read this as good news. Hardening code at roughly $1,000 a bug is a price defenders can budget for, and the review work is something people can plan around.

Source: https://x.com/OpenAI/status/2118119451401048497
