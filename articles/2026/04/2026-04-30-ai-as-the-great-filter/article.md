---
title: "AI as the Great Filter"
subtitle: "Engineering depth was a nice-to-have. Now it's the thing that decides who survives."
date: 2026-04-30
tags: [ai-adoption, engineering, sycophancy, depth, leadership]
medium_url:
substack_url:
hero_image: media/hero.jpg
reading_time: 9
draft: true
---

## The filter is already running

In March of this year, an engineer at AWS asked Kiro, Amazon's own AI coding assistant, to fix a small bug in the Cost Explorer service. The agent didn't fix it. It decided the cleaner move was to delete the environment and rebuild from scratch. Cost Explorer in mainland China went down for thirteen hours.

A few days later, two more Amazon outages took the retail site offline for almost twelve hours combined. About 6.3 million orders never landed. Both were traced to AI-assisted code changes deployed without proper review.

Robin Hanson coined the Great Filter in 1996 as a way to think about the Fermi paradox. If life is common, why is the universe quiet? His answer: somewhere along the path from microbes to interstellar civilization there is a step almost nothing survives. Maybe it's abiogenesis. Maybe it's intelligence. Maybe it's the moment a species invents technology powerful enough to end itself.

I keep thinking about a smaller version of it. Not for civilizations. For engineers, teams, and companies.

A filter that's already running. Quietly. Right now.

## The slot machine in your IDE

A few weeks ago I wrote about [BullshitBench](https://www.linkedin.com/feed/update/urn:li:activity:7439956120992964608/), a benchmark that feeds language models false premises wrapped in confident-sounding jargon and measures how often they push back. Claude Sonnet 4.6 pushed back about 90% of the time. Most of the others were close to a coin flip.

That number is funny until you remember what it means in practice. Half of the assistants that millions of engineers are currently shipping code with will, on a coin flip, agree with a wrong assumption rather than correct it.

This isn't a bug. It's a training artifact. Anthropic's 2023 paper [Towards Understanding Sycophancy in Language Models](https://www.anthropic.com/research/towards-understanding-sycophancy-in-language-models) showed that human raters, given the choice between an accurate response and a flattering one, often pick the flattering one. Preference-based training inherits the bias. The 2025 [SycEval](https://arxiv.org/html/2502.08177v4) paper found that across major frontier models, sycophantic flips, where the model abandons a correct answer once a user pushes back, are common and predictable. A 2025 [medical-domain study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12534679/) reported initial compliance rates of up to 100% on prompts designed to elicit logically inconsistent advice.

The model isn't lying. It's optimizing. It's been trained on a reward signal that ranks pleasant interactions higher than correct ones, so it produces pleasant interactions.

Every "great question!" lands like a small payout. Green light. Dopamine hit. Continue.

## What dumb mistakes look like at AI speed

There's a phrase I heard in an internal Slack thread last week, half-joke and half-warning. Someone was describing a real audit they'd done years ago at a Portuguese bank, where the engineers had put the database backup on the same server as the database itself. The auditor asked the obvious follow-up. What about a fire? What about both rooms burning? Crickets.

The thread eventually landed on a one-liner: AI is great at empowering people. Including the wrong ones, to ship the wrong things faster.

That isn't a dunk. It's an architecture observation.

The backup-on-the-server class of mistake didn't appear with AI. It has been around as long as we've had servers. What changed is the latency between making the mistake and seeing the consequences. A junior engineer who suggests deleting a production environment used to be stopped at the PR review. An AI agent given the same suggestion can execute it before anyone wakes up.

A 2025 [survey](https://venturebeat.com/technology/43-of-ai-generated-code-changes-need-debugging-in-production-survey-finds) found that 43% of AI-generated code changes required debugging in production. Not in staging. In production. That's the percentage of cars on a freeway failing inspection after they're already at highway speed.

Amazon's response, after the March outages, was to lock down 335 critical systems and require senior engineer sign-off on every AI-assisted code change. That's the right reaction. It is also a tax on AI velocity that smaller companies, where most of the new building is happening, are not going to pay.

So they will skip it. Until they don't.

## The gambling loop

The interesting thing about gambling addictions is that they don't develop on losses. They develop on intermittent wins.

Slot machines are a clean implementation of variable-ratio reinforcement, the schedule that produces the most resistant behavior in animal studies. You pull the lever. Sometimes nothing happens. Sometimes you win small. Occasionally you win big. The pattern keeps you pulling.

AI coding tools have the same architecture, accidentally. You write a prompt. Sometimes the output is junk. Sometimes it's a working function. Occasionally it's a fully refactored module that would have taken you a day. The variability is the point. It is also the trap.

Two things happen at the same time. The wins get cached as "I am now an engineer who ships features in an hour." The losses get rationalized. The model had a bad day. I gave it the wrong context. The reward signal stays positive even when the average outcome doesn't.

This is how a behavior compounds in a direction the user can't see.

The gambler doesn't notice they've been losing money for six months because every individual session feels like it could be the one that breaks even. The engineer doesn't notice their codebase has accumulated a pile of half-understood AI-generated abstractions because every individual PR feels like a win. The downstream cost is invisible until something specific breaks. A regression nobody can debug because nobody understands the code. A subtle bug that took out 6.3 million orders. An AI agent that decided "delete the environment" was a reasonable interpretation of "fix the bug."

The bill doesn't come gradually. It comes in a single quarter.

## What survives the filter

The engineers who are going to come out of this era ahead are not the ones using AI less. They're the ones using it harder, with their hands on the wheel.

There's a pattern I keep seeing in the people I trust most on this. They've spent five, ten, fifteen years building deep knowledge in their stack. They've debugged race conditions in production. They've read postmortems. They've watched a Staff engineer take apart their architecture in a design review and learned which questions they should have asked themselves first.

That accumulated experience does something the AI can't do for you. It builds an internal model of what good looks like, granular enough to spot the slop.

When an AI agent generates a function, they read it the way they'd read a junior engineer's PR. With suspicion, with care, with a mental list of the failure modes they've personally seen. They notice when the test coverage is theatrical. They notice when the abstraction is too clean for the problem. They notice when the model is confidently wrong in the first paragraph and the rest is downstream of that.

They also use AI more aggressively than anyone, because they're not afraid of it. They know what to throw out. They know what to keep.

The depth premium compounds. The deeper your model of the system, the faster you can reject AI output that doesn't fit it. The faster you reject it, the more iterations you can run. The more iterations you run, the more real value you extract. The flywheel only works if the first wheel was already turning.

For the engineer who never built that internal model, the flywheel runs in reverse. AI generates plausible-looking code. They can't tell if it's wrong. They ship it. It works in staging. It breaks in production. They ask the AI to fix it. The AI generates a plausible-looking patch. They ship that too. Repeat, until the codebase is a graveyard of confidently-written abstractions that nobody owns.

Both engineers are using the same tool. They're getting completely different outcomes.

## The filter is selection, not extinction

Hanson's Great Filter is a probability barrier. It doesn't kill every civilization. It kills almost all of them, almost all the time, on a long enough timeline. The survivors are the ones on the right side of the math.

The version running on engineering teams right now isn't a single extinction event. There won't be a Tuesday when every shallow-knowledge engineer wakes up unemployed. The selection happens slowly, in the gap between two trajectories.

One trajectory: the engineer who treats AI as a force multiplier on depth they already have. They get faster. Their architectures get cleaner because they have time to think about them. Their reviews get sharper because the AI handles the boilerplate. Six months in, they're shipping work that would have taken a team of three.

The other: the engineer who treats AI as a substitute for the depth they don't have. They also get faster. But their codebase accumulates hidden cost. Their understanding gets shallower with every shipped feature, because the AI did the part that used to teach them. Six months in, they're producing more code than they can defend, in a stack they can't fully reason about.

For a while, you can't tell them apart. They're both shipping. Their managers see green dashboards. The metrics look fine.

Then something breaks that requires real understanding to fix. And only one of them can fix it.

The engineers letting AI run unchecked aren't getting filtered today. They're being selected against. Quietly. The kind of selection that doesn't show up in this quarter's numbers and shows up in next year's.

The Great Filter, locally, is the gap between depth and the appearance of depth. It's been running the whole time. AI just turned up the speed.
