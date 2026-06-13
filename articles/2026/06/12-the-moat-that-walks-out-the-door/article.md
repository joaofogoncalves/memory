---
title: "The Moat That Walks Out the Door"
subtitle: "Part three. If the moat is the judgment in your team's heads, then the moat can quit. What it takes to keep that judgment from leaving with the people who hold it."
description: "The real moat is your team's judgment, and judgment can quit. Why you can't write it down, why it rots unused, and what keeps it from walking out the door."
date: 2026-06-12
tags: [ai, software-engineering, engineering-leadership]
substack_url:
hero_image: media/hero.jpg
reading_time: 11
draft: true
---

Part two ended somewhere uncomfortable, though it read like a win. The moat is not the harness, and it is not the skill files either. Those depreciate and those copy. What is left, the part a competitor cannot lift out of your repo, is the judgment of the people who were there when the system broke. [It lives in the team, not the repo.](/articles/2026/06/11-rent-the-loop-build-the-moat/)

True. It is also the one a company can least protect.

Walk back through what the series has been calling durable. The model is rented, and it improves on someone else's schedule. The harness is owned, and [it rots on yours](/articles/2026/06/2026-06-08-the-harness-is-the-moat/), shedding a gate every time a model release makes one redundant. Both of those change slowly and predictably. The moat we landed on does neither. It does not depreciate on a roadmap or get productized by a vendor. It resigns. It takes a better offer. It burns out in Q3 and goes quiet until spring.

The one thing you cannot rent and cannot buy turns out to be the one that can leave on its own.

So the question part two left open is the one that actually keeps you up. How do you own a moat that has legs?

## Write it down, then

There is an obvious answer, and a whole industry sells it. Capture the tribal knowledge. Kill the bus factor. A runbook for every gate, a postmortem for every incident, a wiki page for every decision, and the knowledge stops living in one person's head.

For most of what a team knows, that is right. Write it down. The architecture, the runbook steps, the config, the timeline of what actually happened: all of it belongs on a page, and a team that skips that work is not guarding a moat, it is just undocumented.

But the series has already walked us into the problem with it. The thing we are trying to preserve here is not a fact. It is judgment, and judgment does not hold still long enough to be written down.

Write a piece of it down completely enough to hand over, and what you have captured is a snapshot: what was true against one model, one architecture, one quarter's failure surface. The harness depreciates, and a frozen record of why you built it depreciates faster, because it cannot tell you which of its reasons still hold. The week a model ships, the page explaining last year's gate is worse than no page. It reads as current. It is not.

So far this is the case against the wiki, and every engineer nodding along has already made it. Keep it in people's heads, then. That is where it has to live, for a reason the next section makes plain. But a head is not a vault, and this is where the easy version of the argument stops too early.

Judgment in a head fails two ways, and they are not the same problem with the same fix. Left unused, it rots. The senior who built it, then moved to another team and stopped working the surface, is calibrated to failures that have already moved. Use it or lose it is not a slogan here, it is the mechanism. And left in one head, it concentrates, until the moat is a single person with a notice period. That second failure is the one the title is about.

So the question part two left open splits in two. You keep judgment exercised so it does not rot. You spread it so it cannot walk out. The rest of this is those two fixes, and the reason a team does neither until it is too late.

## What a runbook can't hold

This is not an argument against writing things down. It is an argument about what writing things down can hold.

Michael Polanyi named it sixty years ago, in a line that has outlived most of what surrounded it: we can know more than we can tell. A diagnostician cannot fully explain the read that took thirty years to build. A senior engineer cannot fully explain why a passing test on the billing path still makes them reach for a second look. They can give you the rule. They cannot give you the thousand cases that taught them when the rule does not apply. The economist David Autor gave the idea a name for the automation age, Polanyi's Paradox: the work hardest to hand to a machine is the work whose rules we cannot fully state, because we never held them as rules.

Documentation catches the what. The skill file, the gate config, the runbook step, the postmortem timeline. All of it real, all of it worth having. What it misses is the judgment underneath: the instinct for which failures were flukes and which were the model telling you something, the feel for when a gate has quietly become latency and when it is still load-bearing.

Make it concrete, and notice that keeping the page current does not save you. A model ships and you audit the gates. The runbook for the billing path was updated last release, so it is not stale: this gate routes billing diffs to a human because the model cannot be trusted to grade them alone. Then the new model lands and the billing evals come back greener than they have ever been. Read literally, the up-to-date page now says the gate is redundant, because the reason it records no longer holds. The newer engineer cuts it. The one who was there keeps it, and cannot give you the sentence that would go in the wiki. The gate was never really about whether the model was good at billing. It was about the cost of being wrong on billing being asymmetric, which is a fact about the business and not about the model, and no release touches it. The page held the reason that was given. It could not hold the reason that was meant. That gap is the judgment, and it does not close by writing the page more carefully.

::: wide
![What documentation holds versus what walks out the door: the skill files and runbooks transfer cleanly; the judgment underneath them does not.](media/runbook-vs-judgment.webp)
:::

Your [ledger of incidents](/articles/2026/06/11-rent-the-loop-build-the-moat/) records the answer to the last failure. It cannot record the instinct for the next one, the failure nobody has seen yet, the one that matches no entry in the book.

This is where the AI-era objection lands, and it deserves a straight answer instead of a dodge. The model can read the whole ledger in a way no engineer can, and a frontier model does more than recite it back, it generalizes past the entries. Autor saw the move coming in the same paper that named the paradox: the project of modern machine learning is precisely to overcome Polanyi's Paradox by inferring, from enough examples, the rules we apply but cannot state. So why doesn't that close the gap here.

Because the part you would need to learn from is the part the ledger never recorded. An incident log holds the decision taken and the symptom seen. It does not hold the hypothesis the on-call discarded in the first thirty seconds, or the unlogged signal that made them distrust the obvious next step, or, in the billing case, the reason that was meant rather than the reason that was written. The tacit layer is missing from the training data for the same reason it was missing from the wiki: nobody could state it well enough to write it down. What the model learns cleanly is the recorded answer to a failure that already happened. The failure that matters is the one that matches no entry yet, where being confidently wrong about something more sophisticated than last year is the entire risk. The model improves on someone else's schedule, and it improves at the answers. The judgment is the part that was never on the page to train on.

That instinct is the asset, and it is the part no wiki page and no training set has ever held. Which means the people actively working the surface are not a documentation gap waiting to be closed. They are the moat, in the only form the moat takes: judgment in use.

## Onboard into the incident

If judgment only stays sharp while it is being used, you transfer it the way it got built in the first place. Through exposure to failure.

That sounds soft. It is the most concrete thing in this piece.

When the next incident hits, the move most teams make is to send in whoever can fix it fastest. Of course they do. The system is down. But the fix is the cheap part, and the person doing it already has the judgment. The expensive, durable thing is the reasoning happening out loud while they work, the hypotheses raised and discarded, the read on which signal mattered, and most teams let it evaporate. Put someone newer on the call. Not to watch. To hold the pen while the one with the judgment narrates what they are seeing and why this and not that. The outage is the curriculum. You will not build one this good on purpose.

The same logic runs through the re-derivation itself. Auditing the harness when a new model lands, deciding which gates to delete and which to keep, is the highest-judgment work the team does. It is also usually done fast, alone, by the one person who can. That is how you end up with a bus factor of one on the exact capability the series called the moat. Rotate the pen. Make the audit something two people do together, and change who leads it each release. It is slower the first few times. It is the only way the judgment ends up in more than one head.

There is a problem with learning from incidents, and a skeptic names it fast: on a healthy system they are rare. You cannot keep a second person sharp by waiting for the next high-severity failure on the expensive path, because if you are running well, one may not arrive for a quarter. So you stop waiting. The ledger changes job. Stored as a record, it is a filing cabinet nobody opens. Run as a drill, it is the closest thing you have to a flight simulator. Re-run an old incident with someone who was not there, let them make the calls, and only then show them where the real one went. Pilots rehearse the engine failure they will probably never see, on purpose, on the simulator. The entry was paid for once. Nothing says you can only spend it once.

None of this scales to every engineer and every incident, and it is not meant to. Most tickets are routine, and routine is what the runbook is for. The high-touch version is reserved for the part that earns it: the non-deterministic core, the harness audit the week a model lands, the high-severity incident on the path where being wrong is expensive. That is a thin slice of the work, and the slice that is the moat. The point is not to slow everything down so juniors can watch. It is to stop spending the rarest work in the building on an audience of one.

## Hire for the slope

There is a hiring version of this, and it cuts against how most teams write the job description.

You cannot hire someone who already holds your judgment. Nobody has it. The incidents that built it happened in your production, against your data, with your customers finding the failure modes only your product has. The most experienced engineer on the market arrives with deep judgment about systems that are not yours. That is worth a lot. It is not the same thing.

So the trait that matters is not how much a candidate already knows about harnesses. It is how fast they can take on an incident they never lived through and start producing judgment of their own. Absorption rate, not inventory.

This is the same direction [the filter has been moving](/posts/2026/06/2026-06-11-software-engineering-has-always-filtered-people/) for a while now. As models close the gap on syntax, the thing that separates engineers is system-wide reasoning, the ability to hold the whole system in their head and reason about where it breaks. You are not hiring for the code anymore. You are hiring for the slope: how quickly someone goes from not having your context to having it. That slope is what turns a new hire into part of the moat instead of a standing drain on the people who already are.

The trouble is that slope does not show up on a résumé, and most interview loops are built to measure inventory. You can measure it directly, but not by asking a candidate to guess at a system they have never seen. Give them enough to reason with: a redacted incident writeup from your own history and the slice of the current harness around it, the gates, the retries, what routes to a human and what does not. Then ask what they would look at first, which gate they would re-examine after a model change, and the single question they would put to the on-call to decide whether it still holds. You are not scoring the answer. It is your system and they cannot know it. You are watching how they build the question: what they reach for, which failure modes they suspect, whether they can reason about where this breaks without having lived in it.

The same signal shows up in the first ninety days, and it is the one worth tracking. Not how much they shipped. How soon they could lead a harness audit without a chaperone, take the pen on a real incident and have it go well.

The engineer who can absorb your ledger in a month and the one who needs a year are not the same hire, even with identical résumés. One compounds the moat. The other borrows against it.

## Nobody is paid to do this

Everything above is correct and almost no one does it, and that is not because managers are careless. It is because every one of these moves bills the wrong account at the worst possible time.

Putting a newer engineer on the incident slows the fix while the system is down. Rotating the audit hands it, half the time, to the slower of the two people who could run it. Re-running an old case spends senior hours on a problem that is already solved. Each cost is immediate, visible, and lands this quarter. The payoff is a bus factor you do not need until someone leaves, which is exactly the benefit a quarterly review cannot see. Sending the best person in alone to fix it fast is not a lapse. It is what optimizing for this week returns, every week, and a bus factor of one is what it compounds into.

There is a second cost, quieter, and it explains why this cannot be solved by decree. The person who holds the moat knows it is a moat. Asking them to spread it is asking them to make themselves more replaceable, deliberately, for an institution that does not always return that kind of favor. That only happens when the spreading is seen and valued as the senior work it is, not booked as overhead between real tasks. A moat moves to a second head when the first head has a reason to let it.

## The moat has legs

So walk the whole series back out.

The model is rented. It gets better on someone else's schedule, and you take the upgrade when it lands. The harness is owned. It rots on yours, and the work is keeping it from rotting. And the moat underneath both of them, the judgment that decides which gate to cut and which to keep, lives in people. Which means it has legs. It can quit.

You do not protect it by writing it down. The page never held the part that mattered, and the model reading the page inherits the same gap. You protect it the two ways the failures demand: you keep it exercised so it does not rot, and you spread it so it does not leave inside one person's resignation. That means treating every incident as a curriculum and not only a fix, every model release as a lesson and not only a sprint, every hire as a question of how fast someone takes on what only your production could teach. None of it is free, and all of it loses to this quarter unless someone decides it will not. The moat does not last because you locked it in a document, or because one person guards it. It lasts because more than one person is using it, and because the next person is already learning to.

The harness, you can lose to a better model. The judgment, you can only lose to a worse manager.
