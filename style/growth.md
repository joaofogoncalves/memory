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
