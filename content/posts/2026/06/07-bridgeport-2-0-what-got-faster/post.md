---
date: 2026-06-07
post_type: original
authored: true
post_url: "https://www.linkedin.com/feed/update/urn:li:activity:7469639285458173952/"
posted_at: 2026-06-08T06:39:44Z
x_url: "https://x.com/joaofogoncalves/status/2063737601732083972"
substack_note_url: "https://substack.com/profile/113523350-joaofogoncalves/note/c-272337016"
tags: [open-source, devtools, software-engineering, bridgeport]
source_urls:
  - https://github.com/bridgeinpt/bridgeport/releases/tag/v2.0.0
angle: 2.0 is a redesign whose headline is performance, not a feature. Lead with the numbers (8.2s to 46ms p99, 6s to <500ms dashboard) and let them carry; the service-model rewrite and the 2.0.1/2.0.2 cleanup are the supporting cast.
template: short-form
reactions: 11
comments: 2
impressions: 586
---

Most 2.0 releases lead with a new feature. This one leads with what got faster.

The slowest transaction in production, a metrics summary, used to have a p99 of 8.2 seconds. It's now 46 milliseconds. The dashboard's first paint went from about six seconds to under 500. Agent metrics ingest went from 115 requests per second to 639.

The pattern repeats across the surface. Health checks went from a 224ms p99 to 42, and from 184 requests per second to 789. The server metrics history endpoint dropped its p99 from 395 milliseconds to 12 and more than tripled its throughput. The per-service version serves almost six times the requests at a fifth of the latency.

None of it came from a clever trick. It came from the unglamorous list: batched transactions, single-flight caching, killing N+1 queries, denormalizing the columns the hot path actually reads.

2.0 also reworked the service model from scratch. A service is now a template that fans out to per-server deployments. That's the bigger change on paper. It's not the one I'd point at.

Then 2.0.1 and 2.0.2 followed with the cleanup: a deploy race condition, a token-permission hole that let viewers decrypt secrets, eight more service types. The headline release gets the writeup. The patches that follow it are what keep it trustworthy.

A control plane nobody waits on is a different tool than one they do.

Full notes: https://github.com/bridgeinpt/bridgeport/releases/tag/v2.0.0

**Hashtags:** #OpenSource #DevTools #SoftwareEngineering
