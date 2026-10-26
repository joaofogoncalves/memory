# Growth feedback loop

Linked from `writing_style.md`, which stays the primary authority. This file records how posts are measured and what the numbers say. It never overrides a voice rule on its own: a change to the style docs is proposed here, confirmed by João, then made in `writing_style.md` (or `post.md`).

## Daily metrics log

- Once a day, pull X `public_metrics` (impressions, likes, reposts, quotes, replies, bookmarks) for every post and reply under 7 days old, plus the X follower count. Log one row per post per day.
- Log LinkedIn reactions, comments and impressions from `/sync` front matter, and Substack Notes impressions, restacks and subscribers from the dashboard when a logged-in read is available.
- Tag each post once: platform, format (text, quote, image, carousel, video, step list, counter-take, reply), topic (robotics, science/medicine, builder, launch, jobs), hook (number, claim, scene, counter-take), length bucket, day and hour (Lisbon), wave or evergreen, and for the LinkedIn A/B test, link placement (`comment` or `body`).

## Weekly review (Mondays)

- Score each post as **impressions divided by João's rolling 30-post median for that platform and format**. Show the median score by format, topic, hook and length, with n next to each cell. Cells with n under 5 are noted, not acted on.
- List the top 3 and bottom 3 posts with URLs, the follower delta per platform, and the replies row on its own (replies are currently the best X lever).
- Propose at most two style changes, each tied to the posts that support it. João confirms or rejects; only confirmed changes go into the style docs, with the date.
- Pick one or two experiments for the week.

### LinkedIn link-placement test (open)

The next 6 LinkedIn flagships from 2026-10-26 alternate: post 1, 3, 5 put the source URL in the first comment; post 2, 4, 6 put it at the end of the body. Record `link_placement` in the log. Decide at the first weekly review after post 6, using the 30-post median score. Until then the first-comment rule stays the default for anything outside the test.

## Variety rules

Added 2026-10-26 after João noted that recent posts all felt alike. In October, 7 of 12 flagships used a clipped source video, 3 an image and 1 a paper figure, nearly all were single-source launch explainers opening with the company and a verb, and 9 of 12 were about models, agents or robot video. Each flagship picks from four independent dimensions, and the weekly review flags when the last 7 days lean on one.

**Subject lane.** Rotate across physical AI and robotics, science and medicine, builder tools and João's own builds, Europe and industry, and one human or culture story. Never the same lane two days in a row, and no lane more than twice in a week. The physical AI thread keeps running inside this rotation.

**Post type.** Launch explainer, contrarian counter-take, numbered step list, quote post with a real take, first-person build log ("I tried this"), a chart built around one number, a question to the community, and a long-form article about once a fortnight on Substack and X. At most two launch explainers in a week.

**Visual.** Source video, carousel of source screenshots, annotated screenshot, João's own screen recording or photo, a paper figure, or text only. Never the same visual two days in a row, and video on at most 2 days out of 5. Quote cards and chart cards from the repo (`charts/render.mjs`, real JG monogram from `web/img/logo.svg`, `joaofogoncalves.com` in white Inter bottom right) are made only when João asks. The digest may mention that a card would fit, but does not make one unprompted.

**Opener.** Rotate between a number, a quote, a scene, a plain claim and a question. Do not start two flagships in a row with the product or company name and a verb. Every opener still carries a concrete number or claim.

**First-person material.** João sends his own builds, recordings or photos occasionally. When he does, it jumps the queue as a flagship, since the stickers post was the one different post in October. The digest asks for it when the week has none.

**Article cadence.** One long-form article about every two weeks, written with the `article` workflow and `style/article_style.md`, published on Substack and X, with a LinkedIn post that points to it. It counts as that day's flagship.

**Tagging.** Do not default every post to `ai, agents`. Use tags that match the lane.

**Tracking.** Each post's front matter gets `lane`, `type`, `visual` and `opener` fields so the weekly review can score variety and compare formats against the 30-post median.

## What the data says so far

Seeded from the 2026-10-26 growth research. Numbers as reported there.

**Baselines**
- X: 353 followers. Median original 31 impressions (n=168, Jan to Oct 2026), mean 46. 119 of 168 originals (71%) got zero likes. Replies median 12, mean 80 (n=98).
- X by format (median impressions): image 34 (n=58), quote-post 31 (n=75), plain text 29 (n=31), video 17 (n=4, too few to judge).
- LinkedIn (96 posts with data, data stops in June 2026): median 1,407 impressions, 11 reactions, 3 comments. Monthly medians fell from 2,381 in March to 775 in June.
- Substack Notes: no metrics stored yet.

**What worked**
- **Replies.** The best replies reached 2,524, 1,631, 887 and 658 impressions, against a best original of 409. Short human replies inside other people's conversations, written by João.
- **Video for robotics.** For 10 of 16 comparable accounts, video beat image and text, often by 3 to 10x (for example @TheHumanoidHub video median 14,679 vs image 7,884).
- **Quote with a real take.** Quote-posts sit at the median (31) when the line is descriptive. Quote weight is 5x a repost, so the line has to be an arguable claim.
- **Concrete first line.** All three viral posts studied and the top LinkedIn hits open with a stakes or results claim. On LinkedIn every top-6 post was a counter-take on something already viral (top: 149,793 impressions, then 114,545).

**Targets (estimates, not forecasts):** X original median from 31 to above 100 impressions and followers up 10% or more a month within 8 weeks; LinkedIn back to its Feb to Mar median (about 2,300).
