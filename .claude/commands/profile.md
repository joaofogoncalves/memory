Analyze the user's LinkedIn post archive and generate a voice profile system prompt.

## Arguments

`$ARGUMENTS` is the recency window in days. Default: 60.
Parse the first number from the arguments. If empty or not a number, use 60.

## Step 1: Discover and filter posts

1. Glob `posts/**/post.md` to find all archived posts.
2. Read each file's YAML frontmatter to extract `date` and `post_type`.
3. **Include** posts where `post_type` is `original` or `article`.
4. **Include** reposts ONLY if there is user-written text between the `# Date` heading and the `## Repost` section (this indicates the user added their own commentary when sharing).
5. **Exclude** pure reposts where content immediately goes to `## Repost` after the date heading.
6. **Exclude** posts with empty or no text content.

Use parallel tool calls to read frontmatter from multiple posts simultaneously. You can read many files in one turn.

## Step 2: Tiered recency weighting

Calculate a cutoff date: today minus the day window from arguments.

- **Tier 1 "Current voice"**: posts with `date` >= cutoff. These define the current writing style.
- **Tier 2 "Established patterns"**: posts with `date` < cutoff. These reinforce or show evolution.

If fewer than 5 posts qualify for Tier 1, expand the window by 30-day increments until at least 10 posts are included. If the entire archive is small (< 15 posts), skip tiering and treat all posts equally.

**Important**: Some dates may reflect batch import times (e.g., all January posts dated 2026-01-26) rather than actual publication dates. Note this in the output if detected.

## Step 3: Read all qualifying posts

Read the full content of all qualifying posts. Use parallel tool calls to read multiple posts at once for efficiency.

For each post, extract:
- The body text (everything between the date heading and the `---` separator before Media)
- The `tags` from frontmatter (if present)
- The `post_type`

## Step 4: Analyze in parallel

Launch 2 agents in parallel:

**Agent 1 — Writing Style & Structure**
Provide this agent with ALL qualifying post content (copy the text into the prompt). Ask it to analyze and return a structured report on:
- Opening hooks: how posts begin (provocative claims, questions, references to events, personal anecdotes)
- Sentence patterns: length variation, use of fragments, rhythm (short/long alternation)
- Paragraph structure: typical length, single-line paragraphs as emphasis
- Tone markers: contrarian, conversational, authoritative, vulnerable, humorous
- Vocabulary: characteristic words/phrases that recur; words that would sound unnatural
- Rhetorical devices: questions, analogies, reframing, "both things are true" patterns
- Emoji usage: frequency, types, placement
- Bold/formatting: when and how bold, lists, or headers are used
- Closers: how posts end (CTA, punchline, open question, link)
- Post length: typical word count range for short vs long posts
Tell the agent to tag each observation as Tier 1 (current) or Tier 2 (established) based on which posts it appears in. Tier 1 observations take priority.

**Agent 2 — Topics & Themes**
Provide this agent with ALL qualifying post content plus all `tags` values. Ask it to analyze and return:
- Primary topics: subjects the user writes about from scratch (original posts)
- Curated topics: subjects they share/comment on (reposts with commentary, articles promoting external content)
- Recurring angles: the specific POSITION the user takes on each topic (not just "AI" but "AI augments expertise, doesn't replace it")
- Contrarian vs consensus: which opinions go against mainstream, which align
- Narrative patterns: recurring metaphors, analogies, or frameworks
- Professional identity: what role/expertise comes through in the writing
Tell the agent to weight Tier 1 topics more heavily. If a topic appears only in Tier 2 and not Tier 1, note it as "historical focus."

## Step 5: Synthesize into profile.md

Using the reports from both agents, write `profile.md` to the project root.

**Critical rules for the output:**
- Every line must be a DIRECTIVE ("Use short opening sentences that make a claim") not a description ("The author uses short opening sentences")
- Include a "What NOT To Do" section with anti-patterns that would break the voice
- Keep under ~150 lines total so it works as a system prompt
- Do NOT include raw post text — synthesize patterns only
- Use specific vocabulary examples, not abstract categories
- The tone should feel like instructions to a ghostwriter, not an academic analysis

**Output structure:**

```markdown
# Voice Profile

You write LinkedIn posts in a distinctive voice. Follow these guidelines precisely.

## Core Identity
[1-2 directive sentences: who you are, what you stand for]

## Tone and Attitude
[Specific, actionable bullets — not vague adjectives]

## Writing Mechanics

### Opening Hooks
[Patterns with paraphrased examples from actual posts]

### Sentence and Paragraph Style
[Rhythm, length, fragment usage, emphasis patterns]

### Vocabulary
**Use naturally:** [specific words and phrases]
**Avoid:** [words that would sound unlike this voice]

### Emoji and Formatting
[Frequency, types, bold/list usage]

## Post Structure Templates

### Short-form (commentary/reaction)
[Structural pattern]

### Long-form (original thought piece)
[Structural pattern]

### Article promotion
[How articles are introduced and linked]

## Recurring Topics and Angles
[Topics with the SPECIFIC angle taken on each]

## What NOT To Do
[Anti-patterns: corporate jargon, AI writing tics, hedging patterns, etc.]

---
Generated from [N] posts ([M] in current voice window of [X] days)
Last updated: [today's date]
```

## Step 6: Confirm completion

Tell the user:
- How many posts were analyzed (total, Tier 1, Tier 2)
- That `profile.md` has been written to the project root
- Suggest running `/taste` to add visual style analysis
