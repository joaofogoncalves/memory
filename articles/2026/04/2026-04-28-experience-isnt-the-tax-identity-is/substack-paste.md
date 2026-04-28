# Substack paste-in — Experience Isn't the Tax. Identity Is.

## Posting checklist (do these in Substack's editor)

1. **Title:** Experience Isn't the Tax. Identity Is.
2. **Subtitle:** Jaya Gupta's piece on AI rewiring decision-making is right about the diagnosis. It mis-attributes the variable.
3. **Canonical URL** (Post settings → SEO → Canonical URL): `https://joaofogoncalves.com/articles/2026/04/2026-04-28-experience-isnt-the-tax-identity-is/` — this keeps SEO pointed at your site, not Substack.
4. **Hero image:** upload `media/hero.jpg` at the top of the post (Substack strips local paths on paste; you have to upload through their UI).
5. **Inline images:** re-upload any of these as you reach them in the body:
   - `media/three-groups.webp`
6. **Tags:** ai-adoption, leadership, decision-making, experience
7. At the end of the post, add this canonical-pointer line so readers who found you on Substack know where the piece actually lives:

   > Originally published at [joaofogoncalves.com/articles/2026/04/2026-04-28-experience-isnt-the-tax-identity-is](https://joaofogoncalves.com/articles/2026/04/2026-04-28-experience-isnt-the-tax-identity-is/).

## Body to paste

Everything below the `---` line is the article body. Select all and paste into Substack's editor after you've set title and subtitle.

---

## What Jaya got right

There's a piece going around called ["Experience is now a tax."](https://x.com/JayaGup10/status/2047508230813917600) It went up a couple of days ago and has been doing the rounds. [Jaya Gupta](https://x.com/JayaGup10) wrote it. If you haven't read it, the setup is this. Somewhere right now there's a CIO at a Fortune 500 firm who has never opened Claude, can't explain what a Claude skill is, and still asks his reports to print documents and leave them on his desk. He is the person making the decision about his firm's AI ROI.

Meanwhile, a 22-year-old is writing production code in an afternoon and turning a napkin sketch into a working prototype before lunch.

These two people are having different experiences of the same technology, and the cultural conversation hasn't caught up. The senior cohort defends its seat with two words: judgment and taste. Things AI cannot replicate. Things that take decades to develop. Things, conveniently, that the person making the argument has spent a career accumulating.

Jaya's argument is that AI just collapsed the cost of three decision-making algorithms the brain runs constantly. *Trying something new versus sticking with what works* used to be expensive. *Carrying knowledge in your head versus offloading it* used to be the senior advantage. *Committing to a decision versus reversing it* used to be a one-way door. AI cheapened all three. The skill is no longer weighing every option before choosing. It's choosing fast, learning fast, and not attaching your identity to the last version of yourself who made the previous choice.

She lands the punch on the third one. Senior people reverse slowly because they've spent careers learning that reversing is admitting they were wrong. Young people haven't learned to attach identity to their decisions yet. Reversal feels like iteration to them. Her closer to young readers: if you can still think clearly without a filter, leave the environment that's training you not to.

The diagnosis is right. I see it every week. Some of the smartest engineers I know are the slowest to ship because they're protecting an old version of themselves who knew the answer before AI changed what knowing meant.

But the article mis-attributes the variable. The thing being taxed isn't experience. It's identity attachment to past decisions, and that's a separate axis from age.

## The variable isn't age

Jaya names the right phenomenon, then attaches it to the wrong axis. She points at the senior cohort and says: this group has more reputation to defend, more decisions tied to their identity, so reversal is more expensive for them. All true. But she frames identity attachment as a natural byproduct of having been right in public for a long time.

It isn't natural. It's a choice, made compulsory by environment and habit.

Here is the steelman of Jaya's position, and it survives most of the data. *On average* experience correlates with identity attachment because the longer you've been right in public, the more reputation you've put on the line. Most senior people are paying the tax. That's true at the population level, and it's the part of her argument that doesn't go away.

The piece's gap is conflating the average with the rule. Some senior operators figured out, somewhere along the way, that holding your previous self lightly is the only way to keep clarity past the age it's supposed to expire. They aren't outliers because they got lucky. They built environments around themselves, and habits inside themselves, where reversal stayed cheap. They're the existence proof that the tax is a default, not a fate.

The 2026 adoption data is also messier than Jaya's piece suggests. A poll of 4,000 US and UK workers found [senior staff adopting AI faster than junior peers](https://www.metaintro.com/blog/ai-adoption-gap-high-earners-workers-2026), not slower. Top earners have better access to paid tools, more dedicated training time, and more autonomy to experiment. By 2025, 73% of director-level workers had adopted AI, against 65% of individual contributors. Caveat the numbers honestly. "Adopted" is a low bar. The headline gap is single-digit. Among regular AI users only, 21% of leaders report extremely positive productivity impact against 13% of individual contributors, but that's self-report inside an already-fluent population. None of these prove seniority dominance. What they show is that the binary "old people are slow, young people are fast" doesn't hold cleanly even at the population level.

The decade of life isn't doing the work. The decade of identity-protection is.

[IMAGE: Three groups, one missing axis — upload media/three-groups.webp here]

## What the verification asymmetry looks like

There is [one finding](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1699320/full) in the cognitive offloading research that matters here. When AI produces an output, you have to evaluate it. Hold the claims against what you know. Spot the hallucinations. Decide whether to revise or regenerate. That work is cognitively demanding. Experienced professionals catch errors faster because they have deep domain knowledge to compare against. Novices pay a verification tax that sometimes cancels out the efficiency gains.

In software this shows up cleanly. Junior engineers using Claude daily are shipping faster than they were a year ago. Some of the seniors using Claude daily are shipping faster than the juniors *and* catching a category of issues the juniors didn't see was a category.

A specific example. Last month I watched a junior engineer prompt Claude to refactor a payment service. The output was clean, the tests passed, and the refactor did exactly what the prompt asked. A senior on the team noticed in about thirty seconds, in code review, that the new version had quietly removed a retry-on-rate-limit pattern that wasn't covered by the test suite. The model had simplified the wrong thing. The junior's verification was test-pass. The senior's was twenty years of "what does this look like in production at 3am." Both shipped. Only one would have caught it.

This is the asymmetry the binary obscures. AI fluency without a pattern library lets you ship things you can't fully evaluate. A pattern library without AI fluency keeps you from shipping at all in the new medium.

It isn't a moat in the durable sense. Tool fluency in 2026 won't look like tool fluency in 2028, and anyone betting their career on "I'm fluent in Claude" is making the same mistake the CIO made one cycle earlier. What's durable is the disposition that produced the fluency. The willingness to put hours into something you didn't grow up with, learn it like a craft, and let your priors get tested by it instead of using them to deflect the test.

## What the discipline looks like in practice

It isn't judgment and taste. That phrase is exactly the defensive crouch Jaya named.

The patterns I see in operators who have un-taxed themselves:

They run their own experiments. They don't delegate the prompt to a junior and review the output. They paste their own context, read their own raw output, fix their own broken prompts. They've put in the same kind of hours they put into mastering a previous craft.

They reverse without ego. The last decision is a hypothesis, not a stake. When the data comes back wrong, they don't relitigate. They commit again.

They use AI to attack their own priors. Most people use the tool to confirm what they already think. The discipline is asking the tool for the strongest counter-argument to your position, the cleanest version of the case against, the data point that breaks the model. Adversarial use, on purpose.

They've stopped leading with "in my experience." That phrase used to be a gear shift in a meeting. Now they treat it as a flag. They might still have the analogy. They might be right. But they've noticed that "in my experience" arriving early in a conversation often shuts the conversation down before anyone has tested whether the analogy actually fits this case.

They pattern-match live. Instead of pulling examples from memory, they pull them from a tool that has more examples and less ego. The senior person who used to win the room with "I've seen this before" now does that work in real time, with citations.

I run this loop at BRIDGE IN. Specifically: I open a task, write the spec myself, prompt Claude to find the worst implementation I'd still accept, then prompt it to defend the cleanest one, then argue with it. The thing that's changed in the last year isn't that I'm faster. It's that the version of me who would have shipped the first plausible-looking design is gone. The tool replaced that version of me.

The discipline is identifiable by behavior, not by years on a CV.

## The thing being taxed

The thing being taxed isn't experience. It isn't age. It's the version of you that needs to be right.

The CIO isn't slow because he's old. He's slow because he can't afford to be visibly wrong. He spent thirty years building a self that was correct, and the cost of admitting that self is now operating in a medium it doesn't understand is higher than the cost of pretending the medium doesn't matter.

The 22-year-old isn't fast because she's young. She's fast because her identity is in motion. Nothing she's said publicly has the gravitational mass of three decades of correct calls. She can change her mind cheaply.

That's the real variable. Not chronological age. Identity weight.

Some senior people have built careers without putting much weight on any single call. They reverse easily because they never made reversal the expensive thing. Some 22-year-olds are already attaching identity to their first big decision. You can see it in the way they double down on a take that didn't land. The tax shows up in them too, just earlier.

This is reversible. Most people don't reverse it. That's the honest version of Jaya's point. The base rate is real. The ones who do reverse it figured out, somewhere along the way, that holding your previous self lightly is the only way to keep clarity past the age it's supposed to expire.

## The discipline of staying clear

Jaya closes her piece with a message to young readers. If you can still think about a problem without first running every thought through "yes but what would my boss or the world say," use that ability now. Use it while you have it. The window narrows faster than you think. If you're in an environment that punishes the clarity you currently have, leave.

That's true for the toxic environments. It isn't the only move available, and it isn't the deepest reading of her own argument.

Clarity isn't an asset of being young. It's a discipline.

Some 22-year-olds will lose it inside ten years if they let the next decade teach them that being right is a personality. Some 50-year-olds never lost it because they refused to learn that lesson. They built environments around themselves where reversal stayed cheap. They kept the tool they had at 22 and added thirty years of analogies to it.

The discipline is identifiable by behavior. Who's running their own experiments. Who's reversed publicly in the last quarter. Who's using the tools in their actual workflow and not just their demo. That's the question, for hiring, for learning, for staying sharp yourself.

Experience is only a tax if you treat it as a fixed asset. As a moving one, it compounds.

---

## After posting

- Grab the Substack post URL.
- Add a `substack_url:` field to the article frontmatter (alongside `medium_url`).
- Optional: share the Substack URL in a Notes post on Substack itself for an extra discovery pass.
