---
title: "The Moat That Walks Out the Door"
subtitle: "Part three. If the moat is the judgment in your team's heads, then the moat can quit. What it takes to keep re-derivation from leaving with the people who hold it."
description: "The real moat is your team's judgment, and judgment can quit. Why you can't document your way out of it, and what actually keeps it from walking out the door."
date: 2026-06-12
tags: [ai, software-engineering, engineering-leadership]
substack_url:
hero_image:
reading_time: 7
draft: true
---

Part two ended somewhere uncomfortable, though it read like a win. The moat is not the harness, and it is not the skill files either. Those depreciate and those copy. What is left, the part a competitor cannot lift out of your repo, is the judgment of the people who were there when the system broke. [It lives in the team, not the repo.](/articles/2026/06/11-rent-the-loop-build-the-moat/)

True. It is also the most fragile thing a company owns.

Walk back through what the series has been calling durable. The model is rented, and it improves on someone else's schedule. The harness is owned, and [it rots on yours](/articles/2026/06/2026-06-08-the-harness-is-the-moat/), shedding a gate every time a model release makes one redundant. Both of those change slowly and predictably. The moat we landed on does neither. It does not depreciate on a roadmap or get productized by a vendor. It resigns. It takes a better offer. It burns out in Q3 and goes quiet until spring.

The one thing you cannot rent and cannot buy turns out to be the thing most likely to walk out the door.

So the question part two left open is the one that actually keeps you up. How do you own a moat that has legs?

## Write it down, then

There is an obvious answer, and a whole industry sells it. Capture the tribal knowledge. Kill the bus factor. A runbook for every gate, a postmortem for every incident, a wiki page for every decision, and the knowledge stops living in one person's head. The research on bus factor keeps arriving at the same fix: one survey of engineers put documentation at the top of the list for protecting the components most at risk when someone leaves. The vendors selling knowledge bases call undocumented understanding the silent productivity killer. Everyone agrees. The fix for knowledge in heads is knowledge on pages.

For most of what a team knows, that is correct. Write it down.

But the series has already walked us into the problem with it. The thing we are trying to preserve here is not a fact. It is judgment. And the moment you write judgment down completely enough to hand it to someone else, two things happen, both bad.

The first: it becomes copyable. Part two's whole argument was that a competitor with your repo still loses, because the skill file is the answer and they never had the question. A document that fully captured your judgment would be the answer with the question stapled to it. You would have built, at real expense, the one artifact the series said was never the moat.

The second: it goes stale. A written-down judgment is a snapshot of what was true against one model, one architecture, one quarter's failure surface. The harness depreciates, and a frozen record of why you built it depreciates faster, because it cannot tell you which of its reasons still hold. The week a model ships, the page explaining last year's gate is worse than no page. It reads as current. It is not.

So the reflexive fix has a category error inside it. The judgment is valuable precisely because it has not been reduced to a transferable artifact. Making it durable the obvious way is the act of destroying what made it worth keeping.

You cannot document your way out of this one.

## What a runbook can't hold

This is not an argument against writing things down. It is an argument about what writing things down can hold.

Michael Polanyi named it sixty years ago, in a line that has outlived most of what surrounded it: we can know more than we can tell. A diagnostician cannot fully explain the read that took thirty years to build. A senior engineer cannot fully explain why a passing test on the billing path still makes them reach for a second look. They can give you the rule. They cannot give you the thousand cases that taught them when the rule does not apply.

Documentation catches the what. The skill file, the gate config, the runbook step, the postmortem timeline. All of it real, all of it worth having. What it misses is the why-it-was-judgment underneath: the instinct for which failures were flukes and which were the model telling you something, the feel for when a gate has quietly become latency and when it is still load-bearing.

::: wide
![What documentation holds versus what walks out the door: the skill files and runbooks transfer cleanly; the judgment underneath them does not.](media/runbook-vs-judgment.webp)
:::

Your [ledger of incidents](/articles/2026/06/11-rent-the-loop-build-the-moat/) records the answer to the last failure. It cannot record the instinct for the next one, the failure nobody has seen yet, the one that matches no entry in the book. That instinct is the asset. It is also the part no wiki page has ever held.

Which means the people who have it are not a documentation gap waiting to be closed. They are the moat, in the only form the moat can take.

## Onboard into the incident

If you cannot transfer judgment by writing it down, you transfer it the way it got built in the first place. Through exposure to failure.

That sounds soft. It is the most concrete thing in this piece.

When the next incident hits, the move most teams make is to send in whoever can fix it fastest. Of course they do. The system is down. But the fix is the cheap part, and the person doing it already has the judgment. The expensive, durable thing is happening in the room around them, and most teams let it evaporate. Put someone newer on the call. Not to watch. To hold the pen while the one with the judgment narrates what they are seeing and why this and not that. The outage is the curriculum. You will not build one this good on purpose.

The same logic runs through the re-derivation itself. Auditing the harness when a new model lands, deciding which gates to delete and which to keep, is the highest-judgment work the team does all quarter. It is also usually done fast, alone, by the one person who can. That is how you end up with a bus factor of one on the exact capability the series called the moat. Rotate the pen. Make the audit something two people do together, and change who leads it each release. It is slower the first few times. It is the only way the judgment ends up in more than one head.

And the ledger changes job. Stored as a record, it is a filing cabinet nobody opens. Used as a training ground, it is the closest thing you have to a flight simulator. Re-run an old incident with someone who was not there. Let them make the calls. Show them where the real one went and why. The entry was paid for once. Nothing says you can only spend it once.

## Hire for the slope

There is a hiring version of this, and it cuts against how most teams write the job description.

You cannot hire someone who already holds your judgment. Nobody has it. The incidents that built it happened in your production, against your data, with your customers finding the failure modes only your product has. The most experienced engineer on the market arrives with deep judgment about systems that are not yours. That is worth a lot. It is not the same thing.

So the trait that matters is not how much a candidate already knows about harnesses. It is how fast they can take on an incident they never lived through and start producing judgment of their own. Absorption rate, not inventory.

This is the same direction [the filter has been moving](/posts/2026/06/2026-06-11-software-engineering-has-always-filtered-people/) for a while now. As models close the gap on syntax, the thing that separates engineers is system-wide reasoning, the ability to hold the whole system in their head and reason about where it breaks. You are not hiring for the code anymore. You are hiring for the slope: how quickly someone goes from not having your context to having it. That slope is what turns a new hire into part of the moat instead of a standing drain on the people who already are.

The engineer who can absorb your ledger in a month and the one who needs a year are not the same hire, even with identical résumés. One compounds the moat. The other borrows against it.

## The moat has legs

So walk the whole series back out.

The model is rented. It gets better on someone else's schedule, and you take the upgrade when it lands. The harness is owned. It rots on yours, and the work is keeping it from rotting. And the moat underneath both of them, the judgment that decides which gate to cut and which to keep, lives in people. Which means it has legs. It can quit.

You do not protect it by writing it down. That turns it into the artifact that was never the moat to begin with. You protect it by spreading it. By treating every incident as a curriculum and not only a fix, every model release as a lesson and not only a sprint, every hire as a question of how fast they can take on what only your production could teach. The moat does not last because you locked it in a document. It lasts because more than one person carries it, and because the next person is already learning to.

The harness, you can lose to a better model. The judgment, you can only lose to a worse manager.
