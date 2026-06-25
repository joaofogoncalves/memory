# Critique prompt

Paste the prompt below into another AI (ChatGPT, Claude.ai, Gemini — whichever gives you a fresh perspective) for a sharp second-opinion review. Bring the feedback back to Claude Code and ask for targeted revisions.

---

You are an experienced editor and subject-matter skeptic. Below is a draft article. Your job is to give sharp, specific, unsentimental feedback that makes the piece stronger.

**Target audience:** Mixed / broad LinkedIn reach — smart non-specialist readers, including engineers, PMs, founders, and business leaders. The frame is economic, not technical.

**Article:**

# AI Will Create More Jobs. Just Not For Everyone.

**Jevons paradox is real. So is the door policy.**

## The paradox has two sides

In January 2025, Satya Nadella posted a link to the Wikipedia article on Jevons paradox. The timing was deliberate. DeepSeek had just released a model that made frontier AI cheaper overnight, and the market was wobbling. Nadella's one-line commentary: "Jevons paradox strikes again. As AI gets more efficient and accessible, we will see its use skyrocket, turning it into a commodity we just can't get enough of."

He was right. A year later, the data is lopsided in his favor. US engineering job listings are up 30% in 2026. AI coding tool experience as a listed requirement is up 340%. PwC's 2025 Global AI Jobs Barometer clocked productivity growth at roughly 4x in AI-exposed industries. The total labor pie is growing, and it's growing fastest exactly where people predicted it would shrink.

This is the take that crushed on my LinkedIn last month. Cheaper software means more software. More software means more work. Nothing about it is false.

But pointing at the total and calling it good news hides what the totals are actually made of.

## Quick detour: what Jevons actually said

In 1865, an economist named William Stanley Jevons noticed something counterintuitive about steam engines. They were getting dramatically more efficient. Each ton of coal produced more work than the year before. Everyone expected coal consumption to drop. Efficiency should save fuel.

It didn't. Coal consumption went up.

The reason was straightforward once Jevons explained it. Cheaper energy opened uses that weren't economical before. Factories expanded. New industries started. Railroads extended. The total demand for coal grew faster than efficiency reduced it.

That's the paradox. When you make something more efficient, you don't necessarily use less of it. You often use more of it, because cheaper access unlocks demand that was previously priced out.

It's been applied to electricity, fuel economy, bandwidth, and now AI. The logic is the same every time: when the cost of a thing drops, demand for that thing tends to grow faster than the savings. The pie expands.

Hold onto that, because it's about to get complicated.

## The part everyone quotes

If you read only the top-line numbers, Jevons looks airtight.

Engineering postings are up 30% year over year despite two years of layoffs. AI-related roles specifically are up 74%. PwC reports the AI wage premium jumped from 25% in 2024 to 56% in 2025, meaning roles requiring AI skills now pay 56% more than otherwise comparable roles that don't. Their barometer shows AI-exposed occupations saw 27% revenue growth per employee and 16.7% wage growth. Total coal consumption went up when steam engines got efficient, and total demand for software is doing the same thing.

Every argument in the "AI will replace coders" panic from 2023 is being refuted in real time. Claude Code ships code. Engineers ship more code. Companies ship more software. The market absorbs more software than it did last year. Nothing about the shape of the industry suggests contraction.

Mr Phil Games wrote a piece on exactly this called *Jevons' Paradox and AI: Why It Means More Developers, Not Fewer*. The argument is straightforward. Software was never a fixed pie. The cost of writing it dropped. The volume being written went up. The ceiling on useful software is much higher than we ever acknowledged, because the constraint was always the cost of building, not the demand for it.

This is correct. I've said it myself, in almost these exact words.

The trouble is that the same dataset tells a different story if you read it from the bottom up.

## The part nobody prices in

Junior developer postings are down about 40% compared to pre-2022 levels. Engineering postings overall are up 30%, but the composition has shifted. Experienced roles are expanding. Entry-level roles are vanishing.

That 56% wage premium for AI skills? It doubled in a single year. A 25-point gap became a 56-point gap. The curve describing the return on AI fluency is getting steeper, not flatter.

[CHART: AI wage premium 25% (2024) → 56% (2025) — stat-compare]

PwC's data, read carefully, says the same thing in a less comfortable way. AI-exposed roles are growing revenue per employee 3x faster than non-exposed roles. That's a widening gap between the boats that move and the boats that don't.

The Anthropic Economic Index from March 2026 adds a quieter datapoint. Roughly 49% of jobs have had at least a quarter of their tasks performed using Claude. In computer and math roles, the theoretical coverage is 94%. The actual usage is around 33%. The gap between what AI can do and what people are doing with it is enormous, and it's where the distribution is separating.

Here's the pattern the top-line numbers hide. The pie is growing. The line at the door is getting longer. The door isn't getting wider.

## Why both things are true

Both readings are correct. They aren't describing different economies. They're describing different halves of the same one.

Jevons says: when a thing gets cheaper, more of it gets made. Software gets cheaper, more software gets made, more people get hired to make it. That's the first-order effect and it's real.

The second-order effect is the one nobody quotes. When the marginal cost of adequate output drops to near zero, the new demand skips past adequate entirely and lands on work that requires something adequate can't deliver. Leverage. Judgment. Taste. The ability to orchestrate five agents toward one outcome. The ability to decide what's worth building in the first place.

Matt Gray said it in a tweet last week: the person doing adequate work at adequate speed is in trouble, because adequate is now free. That's the part Jevons doesn't cover and nobody is quoting.

The middle of the skill distribution isn't being squeezed by less work. It's being squeezed by work it can't do. Jevons creates the demand. Adequate-is-free determines who that demand reaches.

Both things are probably true. They just measure different parts of the same shift.

## Who gets the new jobs

There are two doors. Most people who will thrive in the next five years walk through both. Almost everyone who doesn't will be locked out by one.

[CHART: Two doors — Leverage vs Judgment — feature-compare]

The first door is leverage. Can you produce the work of five people with a harness of agents? Can you run a code review, a spec, a refactor, and a migration in parallel because you've built a system for it? This is the harness-engineering argument. OpenAI's framing earlier this year captured it well: the primary job of an engineering team is no longer writing code, it is enabling agents to do useful work. The engineers who build those systems are the ones whose postings are up 30%.

The second door is judgment. When adequate code is free, the bottleneck moves to deciding what to build, what to kill, what good looks like. This is the taste problem. AI can generate a hundred variants in an hour. A person still has to pick the one worth shipping. That picking is the work that doesn't compress.

Adopters get both doors. Non-adopters get neither. The people in the middle, doing careful, correct, adequate work at a pace that used to be valuable, are the ones discovering that neither door opens for them anymore.

The Anthropic data is the quiet scream here. 94% theoretical coverage in computer and math roles. 33% actual. Two-thirds of the opportunity is sitting on the table, unclaimed, waiting for someone to walk through.

## Why this is hard to hear

The obvious response to all this is: fine, tell people to adopt. Run the training. Hand out Copilot licenses. Mandate the tools.

It doesn't work that way. I wrote about this in an earlier piece called *Pain Gets You In The Door. Curiosity Builds Everything Else*. The research on AI adoption inside organizations is painful and clear. Mandate-driven adoption crowds out intrinsic motivation. The people who adopt because they're told to don't build the deep fluency that the adopters-by-curiosity build. A 2026 study in Frontiers in Psychology pegged intrinsic motivation as the single strongest predictor of creative and frequent AI use. Ahead of training. Ahead of org support. Ahead of everything else.

So the people most exposed to the adequate-is-free shift are also the people most likely to receive the framing that guarantees they'll never close the gap. "Just use AI." "Upskill." "Get with the program." These phrases describe the adoption pattern that doesn't stick.

The companies doing this well aren't running training programs. They're hiring for curiosity, rewarding internal exploration, letting people get obsessed on company time. The companies panicking about productivity are doing the opposite, and the gap between the two cohorts will widen the same way the wage gap is widening right now.

There's no gentle way to say this. If you're relying on your company to pull you through this shift, your company is statistically the worst-positioned actor to do it.

## The paradox has a door policy

Jevons is real. AI will create more jobs. That was never the question.

The question was who gets to do them.

The top-line data says the labor pie is growing. The bottom-line data says the growth is concentrated in a narrow slice of workers who were already adopting. The gap is widening because the cost of being adequate dropped to zero, and the new demand landed entirely above adequate.

Both halves of the story are true. Nadella was right. Matt Gray was right. The engineers shipping 10x with Claude Code and the designers watching their adequate-tier competitors get priced to nothing are living in the same economy, describing the same shift, from different sides of the door.

The paradox works. It has always worked. It just has a door policy now, and it's getting stricter every quarter.

---

**Review criteria — give specific, quote-level feedback on each:**

1. **Argument strength.** Is the thesis actually supported by the evidence and examples? Where are the gaps or unproven leaps? Specifically: does the piece actually prove that Jevons + adequate-is-free produce a narrower door, or does it merely assert it?
2. **Evidence.** Which claims need a citation or concrete example? Which feel assertive without grounding? Flag any statistic that looks suspicious or insufficiently sourced.
3. **Voice consistency.** Where does the writing drift into corporate, generic, or AI-ish language? Quote specific phrases.
4. **Weakest section.** If you had to cut or rewrite one section end-to-end, which one? Why?
5. **Missing counterargument.** What's the strongest objection a skeptical reader would raise that the article fails to address? (Obvious candidates: historical adaptation, reskilling success stories, the labor share question, the role of policy.)
6. **Overstatements and filler.** Quote specific sentences that are overclaims, hedges, throat-clearing, or fluff.
7. **Opening and closing.** Does the opening earn the reader's attention? Does the closing land, or fade out?
8. **Audience fit.** Does the writing match a mixed LinkedIn audience of engineers, PMs, founders, and business leaders? Where is it too technical, not technical enough, or missing their vocabulary?

**Output format:**

Start with your **top 3 recommended changes** in priority order — the ones that would most improve the piece.

Then go through each criterion above with specific quotes and line-level suggestions.

Be direct. Don't cushion. The goal is a sharper article, not a comfortable author.
