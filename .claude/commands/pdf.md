Generate a PDF version of the user's CV, styled to match the site's brutalist dark theme.

## Arguments

`$ARGUMENTS` controls the mode:

- **Empty** → Generic CV PDF for the About page. Uses `cv.md` as-is.
- **Text or URL** → Tailored CV PDF for a specific job description.

If `$ARGUMENTS` starts with `http`, fetch the job description via WebFetch first. Otherwise treat it as inline JD text.

## Step 1: Read inputs

Read these files in parallel:

1. `cv.md` — the CV content (required; abort if missing)
2. `config/site.yaml` — site identity (name, LinkedIn, GitHub, etc.)
3. `web/css/style.css` — theme reference for colors, fonts, spacing

If in **tailored mode**, also read:
4. `profile.md` — voice profile (if exists, for tone reference)
5. The job description (fetched from URL or from `$ARGUMENTS` text)

## Step 2: Prepare CV content

### Generic mode (no arguments)

Parse `cv.md` into sections: intro (pre-`##`), Summary, Experience, Education, Top Skills/Skills. Use the content as-is.

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

## Step 3: Generate self-contained HTML

Write a single HTML file with all CSS inlined. This is the source for the PDF.

**Design system — "The Brutalist Compiler" adapted for print:**

```
Fonts:
  - Headlines: 'Space Grotesk', sans-serif (bold, tight letter-spacing)
  - Body: 'Inter', sans-serif (1.5 line-height for print)
  - Metadata: 'JetBrains Mono', monospace (dates, locations, skills)

Colors (dark theme):
  - Background: #0e131e (dark navy)
  - Text: #dee2f2 (light gray)
  - Accent: #44d8f1 (teal — used for section dividers, name)
  - Muted: #bbc9cc (secondary text — dates, locations)
  - Outline: #3c494c (subtle borders)
  - BRIDGE IN: #cc0000 (brand red, always)

Layout:
  - A4 page size, 18mm margins
  - Zero border-radius (brutalist)
  - No decorative elements — clean, dense, functional
  - Section titles: uppercase, letter-spaced, teal accent underline
  - Experience: company bold, role normal, date/location in mono muted
  - Skills: horizontal flow, monospace, separated by middots
  - Contact: name large + social links in header
```

**HTML structure:**

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
  <style>
    /* Full inline CSS here — page setup, typography, layout */
    @page { size: A4; margin: 18mm; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    body { background: #0e131e; color: #dee2f2; font-family: 'Inter', sans-serif; font-size: 10pt; line-height: 1.5; }
    /* ... all theme styles ... */
  </style>
</head>
<body>
  <header><!-- Name + contact links --></header>
  <section class="summary"><!-- Summary text --></section>
  <section class="experience"><!-- Timeline entries --></section>
  <section class="skills"><!-- Skill tags --></section>
  <section class="education"><!-- Education --></section>
</body>
</html>
```

**Important styling details:**
- Every occurrence of "BRIDGE IN" must be wrapped in `<span style="color:#cc0000;font-weight:600">BRIDGE IN</span>`
- Section titles use Space Grotesk, uppercase, with a thin teal bottom border
- Experience entries: company name bold, em-dash, role. Date range in JetBrains Mono muted. Bullets as a compact list
- The header should include the person's name (large, teal) and social links (LinkedIn, GitHub, site URL) in monospace
- Keep it dense — aim for 1-2 pages maximum
- No images, no headshot — text only

**Output path for HTML:**
- Generic mode: `web/dist/about/cv.html`
- Tailored mode: `cv-{company-slug}.html` in project root

Make sure `web/dist/about/` directory exists (create with mkdir -p if needed).

## Step 4: Convert HTML to PDF with Playwright

Write and execute a small Python script that uses Playwright to render the HTML to PDF:

```python
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

html_path = Path(sys.argv[1]).resolve()
pdf_path = Path(sys.argv[2]).resolve()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f'file://{html_path}')
    page.wait_for_load_state('networkidle')
    # Wait for Google Fonts to load
    page.evaluate('() => document.fonts.ready')
    page.pdf(
        path=str(pdf_path),
        format='A4',
        margin={'top': '18mm', 'right': '18mm', 'bottom': '18mm', 'left': '18mm'},
        print_background=True,
    )
    browser.close()
    print(f'PDF saved: {pdf_path} ({pdf_path.stat().st_size / 1024:.0f} KB)')
```

Save this script as a temp file, run it with the venv Python, then clean up.

**PDF output paths:**
- Generic mode: `web/dist/about/cv.pdf`
- Tailored mode: `cv-{company-slug}.pdf` in project root

## Step 5: Clean up

- Delete the temp Python script
- Keep the HTML file (useful for debugging/iteration)

## Step 6: Confirm completion

Tell the user:
- Which mode was used (generic or tailored)
- Output file path and size
- If tailored: which aspects were reframed for the target role
- If generic: remind them to run `python web/build.py` and deploy to make it available on the About page
