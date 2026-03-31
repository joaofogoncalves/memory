---
argument-hint: [job description URL or text] (optional, for tailored CV)
description: Generate a styled PDF of the CV matching the site's brutalist dark theme
allowed-tools: Read, Skill, WebFetch
---

Generate a PDF version of the user's CV, styled to match the site's brutalist dark theme. Uses native PDF creation via `document-skills:pdf` — no HTML-to-PDF conversion.

## Arguments

`$ARGUMENTS` controls the mode:

- **Empty** → Generic CV PDF for the About page. Uses `cv.md` as-is.
- **Text or URL** → Tailored CV PDF for a specific job description.

If `$ARGUMENTS` starts with `http`, fetch the job description via WebFetch first. Otherwise treat it as inline JD text.

## Step 1: Read inputs

Read these files in parallel:

1. `cv.md` — the CV content (required; abort if missing)
2. `config/site.yaml` — site identity (name, LinkedIn, GitHub, site URL, etc.)

If in **tailored mode**, also read:
3. `profile.md` — voice profile (if exists, for tone reference)
4. The job description (fetched from URL or from `$ARGUMENTS` text)

## Step 2: Prepare CV content

### Generic mode (no arguments)

Parse `cv.md` into sections: header (pre-`##`), Summary, Experience, Education, Top Skills/Skills, Languages, Certifications. Use the content as-is.

### Tailored mode (JD provided)

1. Parse the job description for: key requirements, valued skills, technologies, seniority signals, company name
2. Parse `cv.md` into sections
3. **Reframe** the CV to emphasize fit for this role:
   - Rewrite Summary to target the role (2-3 sentences)
   - Reorder experience bullets to lead with most relevant
   - Add/emphasize skills that match JD requirements
   - Adjust role descriptions to highlight transferable experience
4. **Maintain factual integrity** — reframe and emphasize, never fabricate
5. Extract a company slug (lowercase, hyphenated) for the output filename

## Step 3: Generate PDF natively

Invoke the `document-skills:pdf` skill via `Skill("document-skills:pdf")` to create the PDF.

Pass the prepared CV content and the complete design specification below. The PDF must be created natively — **no HTML, no browser rendering, no Playwright**.

### Design system — "The Brutalist Compiler" (print edition)

**Page setup:**
- A4 (210 × 297 mm)
- Margins: 18mm all sides
- Background: `#0e131e` (dark navy) — full page fill on every page
- Target: 1–2 pages maximum. Dense layout.
- Force background color on every page (this is critical for the dark theme look)

**Color palette:**

| Token | Hex | Usage |
|-------|------|-------|
| Background | `#0e131e` | Page fill |
| Text | `#dee2f2` | Primary body text |
| Accent | `#44d8f1` | Name, section titles, section underlines |
| Muted | `#bbc9cc` | Dates, locations, contact links, skill tags |
| Outline | `#3c494c` | Subtle separators between experience entries |
| BRIDGE IN | `#cc0000` | Brand name — always this color, always bold |

**Typography:**

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Name | Space Grotesk | 22pt | Bold | `#44d8f1` |
| Section titles | Space Grotesk | 11pt | Bold | `#44d8f1` |
| Body text | Inter | 9.5pt | Regular (400) | `#dee2f2` |
| Company names | Inter | 9.5pt | SemiBold (600) | `#dee2f2` |
| Dates, locations | JetBrains Mono | 8.5pt | Regular | `#bbc9cc` |
| Skills, tags | JetBrains Mono | 8.5pt | Regular | `#bbc9cc` |
| Contact links | JetBrains Mono | 8pt | Regular | `#bbc9cc` |

Font fallbacks (if Google Fonts unavailable): Space Grotesk → Helvetica Bold, Inter → Helvetica, JetBrains Mono → Courier

Line height: 1.5 for body text, 1.2 for headings.

**Layout rules:**

- **Zero border-radius** everywhere (brutalist aesthetic)
- **Header**: Name left-aligned (large, teal). Contact links right-aligned in mono muted, separated by ` · ` (middots). Include LinkedIn, GitHub, and site URL from `site.yaml`. One line.
- **Section titles**: UPPERCASE, letter-spacing +0.08em, with a thin (0.5pt) teal (`#44d8f1`) horizontal line underneath spanning content width. 16pt space before each section.
- **Experience entries**: Company name in Inter SemiBold followed by ` — ` (em-dash) and role in Inter Regular, same line. Date range right-aligned in JetBrains Mono muted. Bullets as compact list below (4pt between bullets). 10pt between entries. Subtle `#3c494c` separator line between entries.
- **Skills**: Horizontal flow, JetBrains Mono, items separated by ` · ` (middots)
- **Education**: Same format as experience but more compact
- **BRIDGE IN** must always be rendered in `#cc0000` with bold/semibold weight — scan all text for this string and apply the color
- No images, no headshot, no decorative elements — text only
- No page numbers

**Page break rules:**
- Never break in the middle of an experience entry (company + role + all bullets stay together)
- If content exceeds one page, break between experience entries or between sections
- Prefer breaking before a section title rather than after one

### Output path

- Generic mode: `cv_joaofogoncalves.pdf` in project root
- Tailored mode: `cv-{company-slug}.pdf` in project root

## Step 4: Confirm completion

Tell the user:
- Which mode was used (generic or tailored)
- Output file path and size
- If tailored: which aspects were reframed for the target role
- If generic: remind them that `build.py` will copy `cv_joaofogoncalves.pdf` to `dist/about/` and the About page download link picks it up automatically
