# Personal Website Design — João Gonçalves

Design a personal website for a Portuguese engineering leader and AI coding practitioner based in Lisbon. He is currently a Founding Engineer at a startup (BRIDGE IN), previously Director of Software Engineering at Altium where he steered a team through a $20M acquisition (Valispace → Altium), with 15+ years across SaaS, engineering software, and IoT. He writes actively on LinkedIn about AI tooling, engineering leadership, and software craft.

The site serves three audiences: community/following building (primary), speaking/podcast invitations, and recruiters (secondary). It is NOT a corporate portfolio. It's a practitioner's home base — someone who builds things daily, not someone who comments from the sidelines.

---

## Design System & Visual Direction

### Mood
Think "senior engineer's personal site" — closer to a well-crafted dev blog than a marketing page. Substance over polish. The brand is confidence and specificity, not decoration. It should feel like the digital equivalent of a dark-mode terminal with good typography.

### Color Palette
- **Background:** Dark navy / near-black (#0a0f1a or similar deep blue-black). Dark mode is the only mode.
- **Primary text:** Off-white / light gray (#e0e0e0 to #f0f0f0). Never pure white — too harsh.
- **Accent:** Teal / cyan (#00bcd4 or similar muted teal) used sparingly for links, hover states, and subtle highlights. One accent color only.
- **Secondary accent:** Deep blue (#1a237e range) for card backgrounds, code blocks, or subtle section differentiation.
- **Borders/dividers:** Very subtle — dark gray lines (#1e2a3a) or no visible borders at all. Let spacing do the work.
- **No bright pastels, pinks, magentas, or gradient backgrounds.**

### Typography
- **Headings:** A clean sans-serif with personality — Inter, Space Grotesk, or similar. Medium weight, not bold. Lowercase or sentence case preferred over ALL CAPS.
- **Body text:** Readable, generous line-height (1.6+). 16-18px base. Same sans-serif family or a complementary one.
- **Accent/monospace:** A monospace font (JetBrains Mono, Fira Code, or similar) used for: metadata labels, dates, tags, the nav bar, or small decorative elements. This is a recurring texture that reinforces the technical identity without overdoing the "hacker aesthetic."
- **No serif fonts. No decorative/display fonts. No handwritten fonts.**

### Spacing & Layout
- Generous whitespace everywhere. Let the content breathe. Whitespace IS the design.
- Max content width: ~720px for text content (like a good blog), up to ~1100px for the overall page container.
- Single-column layout for all content pages. No sidebars. No multi-column grids for text.
- Cards (for posts) can use a 1-column or 2-column grid on desktop, single column on mobile.

### Interactions
- Subtle hover effects only: slight color shift on links, gentle opacity change on cards.
- No animations, parallax, scroll effects, or loading transitions. Nothing moves unless the user causes it.
- Links are teal/cyan and underlined on hover only.

### Images & Media
- No stock photography anywhere.
- No decorative illustrations, 3D renders, or AI-generated art.
- Images only appear inside post content (screenshots, diagrams from the original LinkedIn posts).
- The site itself is text-first. The design doesn't depend on any images to look complete.

---

## Site Structure — 3 pages

### Page 1: Home (/)

The landing page. First impression. Sets the tone.

**Layout (top to bottom):**

1. **Navigation bar** (fixed top, transparent/dark background that subtly solidifies on scroll)
   - Left: Name "João Gonçalves" in monospace or the heading font, functions as home link
   - Right: "About" · "Posts" — just two links. Minimal. No hamburger menu on desktop.
   - Mobile: Name left, compact hamburger or just stack the two links.
   - No logo, no icon, no avatar in the nav.

2. **Hero section** (takes roughly 70-80vh, not full screen)
   - Large heading: "João Gonçalves" — big, confident, clean.
   - Subline: "Founding Engineer at BRIDGE IN. Previously Director of Engineering at Altium/Valispace. Building things with AI, not just talking about it." — 1-2 sentences max, in a slightly larger body font or a muted lighter weight.
   - Below the subline: a horizontal row of minimal contact/social icons or text links: LinkedIn · GitHub · Email — in monospace, small, muted gray. Not buttons — just text links.
   - A subtle downward-scroll indicator (thin line or small chevron) or nothing at all. No "scroll to explore" text.
   - **No photo/headshot in the hero.** The text does the work.
   - **No background image, no gradient, no pattern.** Just the dark background and text.

3. **Recent Posts section**
   - Section heading: "Recent" — one word, left-aligned, in the heading font. No "Latest Posts" or "What I've Been Writing." Just "Recent."
   - Show the 6 most recent original posts as cards in a 2-column grid (desktop) / 1-column (mobile).
   - **Post card design:**
     - Date in monospace, small, muted (e.g., "2026-03-15")
     - Post title/first line of content as a clickable heading (truncated to ~80 chars if needed)
     - 2-line preview of the post body text in muted gray
     - Tags displayed as small, inline, monospace labels (e.g., `AI` `leadership` `Claude`) with subtle background (#1e2a3a or similar)
     - If the post has an image: show a small thumbnail to the right of the text (not above it, not full-width). Thumbnail is optional — the card works without it.
     - No like counts, no comment counts, no engagement metrics. Zero.
   - Below the 6 cards: a single text link "All posts →" pointing to /posts. Not a button — a teal text link with an arrow.

4. **Brief about teaser** (optional, right above the footer)
   - 2-3 sentences: "15+ years building software and teams. Steered an engineering org through a $20M acquisition. Now building from scratch again. Currently writing about what happens when AI changes how we build."
   - A text link: "More about me →" pointing to /about.
   - This section is optional — skip it if the page feels better without it. The hero subline might be enough.

5. **Footer**
   - Minimal. One line: "João Gonçalves · Lisbon" with the social/contact links repeated.
   - Or just the social links centered. Nothing else. No copyright notice, no "built with X," no newsletter signup.

---

### Page 2: About (/about)

The CV/professional story page. Not a traditional resume — it's a narrative that happens to contain career data.

**Layout (top to bottom):**

1. **Navigation bar** (same as homepage)

2. **Page header**
   - Heading: "About" — simple, left-aligned.
   - Optional: A professional headshot here (small, ~150px, circular or slightly rounded, desaturated or with a subtle teal tint). Positioned to the right of the heading or below it. This is the ONE place a photo is acceptable.

3. **Intro/Summary block**
   - 3-4 sentences in the user's own voice (casual authority, not LinkedIn-summary corporate-speak):
     "I'm an engineering leader who still writes code daily. 15+ years of building teams and shipping products across SaaS, engineering software, and IoT — from a 4-person startup to a 25-person department through a $20M acquisition. Based in Lisbon, currently building BRIDGE IN from scratch. I write about AI tooling, software craft, and what it actually takes to lead engineering teams."
   - This is body text, not a blockquote. Generous font size.

4. **Career timeline**
   - Vertical timeline design — each role as a node on a line.
   - **Timeline node design:**
     - Left side (or top on mobile): Date range in monospace, muted (e.g., "2024 – 2025")
     - Company name in the heading font, teal accent color
     - Role title in regular weight, slightly smaller
     - Location in small monospace, muted gray: "Lisbon, Portugal"
     - 1-2 bullet points of key achievements (not the full LinkedIn description — curated highlights only). Keep these short. The most impressive number or outcome per role.
   - **Roles to include (chronological, most recent first):**
     - BRIDGE IN — Founding Engineer (Nov 2025–present)
     - Altium — Director of Software Engineering (Jan 2024–Nov 2025). Highlight: led integration post-$20M acquisition, doubled eng team, 90% retention post-merger.
     - Valispace — Head of Technology & Interim CTO (Aug 2022–Feb 2024). Highlight: positioned company for acquisition, ISO-27001 for aerospace clients (Airbus, Clearspace).
     - Valispace — Head of DevOps (Oct 2020–Aug 2022). Highlight: 100+ deployments, 89% faster releases.
     - Valispace — Senior Developer (Aug 2018–Oct 2020).
     - Quidgest — R&D Software Engineer (Jan 2016–Aug 2018). Highlight: low-code platform for Portuguese government & armed forces.
     - Sources.pt — Co-Founder & Lead Developer (Jan 2015–Oct 2017). Highlight: IoT platform, built prototype to pitch.
     - Earlier roles (Inova, Quidgest, EmergeIT, NAD) can be collapsed into a "Earlier career" expandable section or a single line: "2009–2015: Mobile development, web applications, and R&D across startups in Lisbon."
   - The timeline should visually emphasize the last 4 roles (Valispace through BRIDGE IN) as the core narrative arc: developer → DevOps lead → CTO → acquisition → director → founding engineer.

5. **Skills & domains** (optional compact section)
   - NOT a grid of technology logos. Instead, a few short descriptive lines grouped by theme:
     - "Engineering Leadership — Scaling teams from 4 to 25+, coaching leads, M&A integration"
     - "AI & Tooling — Claude Code, AI-assisted development, GenAI strategy"
     - "Infrastructure — Kubernetes, cloud architecture, CI/CD, ISO-27001"
     - "Languages — Python, JavaScript/TypeScript, full-stack SaaS"
   - Style: monospace labels for the category, regular text for the description. All on dark card backgrounds or just inline text.

6. **Speaking & Contact**
   - Short text: "Available for speaking, podcasts, and conversations about engineering leadership and AI in practice."
   - Contact: email address as a teal mailto link, LinkedIn profile link.
   - No contact form. No Calendly embed. Just the email.

7. **Education** (subtle, at the bottom)
   - Single line: "Universidade de Évora — Computer Science"
   - No dates, no "incomplete" label. Just the institution and field.

8. **Footer** (same as homepage)

---

### Page 3: Posts (/posts)

The main content archive. This is the heart of the site. It needs to handle 400+ original posts spanning 2016–2026 without feeling overwhelming.

**Layout (top to bottom):**

1. **Navigation bar** (same as all pages)

2. **Page header**
   - Heading: "Posts" — left-aligned.
   - Below: A single-line description in muted text: "Archived from LinkedIn. Originals only." (or similar — short context about what this is.)
   - Below that: total post count in monospace: "437 posts" (dynamic, based on actual count of original posts).

3. **Filter/search bar**
   - A single row containing:
     - **Search input:** Dark-themed input field with placeholder "Search posts..." — searches post content and tags.
     - **Year filter:** Horizontal row of years (2026 · 2025 · 2024 · ... · 2016) as clickable text links, with the active year in teal and the rest in muted gray. "All" as the default. Not a dropdown — visible inline.
     - **Tag filter:** A compact "Tags" dropdown or expandable pill row showing the most common tags (AI, leadership, engineering, Claude, build-vs-buy, etc.). Clicking a tag filters. Multiple tags selectable.
   - The filters should feel lightweight — not a complex dashboard. Think of it as a few text links, not a form.
   - On mobile: search input full-width, year filter as a horizontal scroll row, tags as a dropdown.

4. **Curated window — "Recent" section**
   - Only visible when no filters are active (i.e., the default view).
   - Shows the 10 most recent original posts in a visually prominent format — larger cards, more content preview.
   - **Prominent post card:**
     - Date in monospace
     - First line of post as heading (larger font)
     - 3-4 line preview of body text
     - Tags as inline pills
     - Optional: thumbnail image on the right if the post has media
   - After these 10 cards: a subtle divider line and a heading "Archive" in muted text.

5. **Full archive list**
   - Below the curated window (or as the main view when filters are active).
   - **Compact post row design** (not cards — denser):
     - Date on the left in monospace, fixed-width column
     - Post title/first line as a text link
     - Tags as small inline pills on the right
     - No preview text, no images — just date + title + tags per row
     - Grouped by year with year headers (e.g., "2026" as a small heading)
   - **Pagination:** Infinite scroll or "Load more" at the bottom. NOT numbered pagination. Keep it seamless.
   - When filters are active, the curated section hides and all matching posts show in the compact row format.

6. **Empty state**
   - If search/filter returns no results: "No posts match that filter." in muted text, centered. Nothing else.

7. **Footer** (same as all pages)

---

### Individual Post View (/posts/YYYY/MM/slug)

When a user clicks a post from the archive, they see the full post rendered from its markdown file.

**Layout:**

1. **Navigation bar**

2. **Post header**
   - Date in monospace, muted, at the top
   - Tags as inline pills below the date
   - No title heading — LinkedIn posts don't have titles. The content IS the post. Jump straight to the body.

3. **Post body**
   - Rendered markdown. Clean typography. Max-width ~680px for comfortable reading.
   - Images rendered inline at full content-width (if media files are available).
   - Hashtags from the original post are fine to keep — they're part of the voice.
   - Links styled in teal.
   - Blockquotes with a left teal border (for repost-style quoted content if any remains).
   - Code blocks with a slightly lighter dark background and monospace font.

4. **Post footer**
   - "View original on LinkedIn →" as a teal text link pointing to the LinkedIn URL.
   - Navigation: "← Previous" and "Next →" links (chronologically) in muted text, edges of the content column.
   - No comments section. No share buttons. No engagement metrics.

5. **Footer** (same as all pages)

---

## Responsive Behavior

- **Desktop (>1024px):** Full layout as described. 2-column post card grids, inline year filters, spacious margins.
- **Tablet (768–1024px):** Single-column post cards, slightly tighter margins. Timeline still vertical.
- **Mobile (<768px):** Single-column everything. Nav collapses to minimal layout (name + hamburger or just stacked links). Search bar full-width. Year filter horizontal-scroll. Timeline nodes stack vertically with date above content. Post cards are full-width. Generous touch targets.

---

## What This Site is NOT

- Not a corporate portfolio with case studies and testimonials
- Not a marketing site with CTAs, newsletter popups, or conversion funnels
- Not a flashy animated experience with scroll-triggered effects
- Not a template with stock photos, gradient backgrounds, or decorative illustrations
- Not a blog with commenting, social sharing widgets, or "related posts" carousels
- Not a dark-mode GitHub/VS Code clone — it should be inspired by that aesthetic without cosplaying it

The site should feel like opening a well-organized markdown file in a beautifully configured editor. The content is the product. The design is invisible infrastructure.

---

## Design Deliverables Needed

Please generate high-fidelity mockups for:
1. **Homepage** — desktop and mobile
2. **About page** — desktop (full career timeline visible) and mobile
3. **Posts archive page** — desktop (default view with curated + archive) and mobile
4. **Posts archive page — filtered state** — with a year or tag selected, showing the compact list view
5. **Individual post view** — desktop and mobile, with a sample post that includes body text, an image, and hashtags

All mockups should use realistic content — use the name "João Gonçalves," realistic post titles about AI tooling and engineering leadership, and real-looking dates.
