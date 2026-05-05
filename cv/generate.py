#!/usr/bin/env python3
"""Generate a brutalist dark-theme CV PDF from cv.md.

Reads cv.md as the source of truth so the PDF and the website's About page
never drift apart. About-only sections (Hero, Thesis, Building, Open To) are
deliberately skipped — they belong to the narrative pages, not the printed CV.
"""

import os
import re
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------- paths ----------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(SCRIPT_DIR, "fonts")
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT = os.path.join(PROJECT_ROOT, "cv_joaofogoncalves.pdf")
CV_MD = os.path.join(PROJECT_ROOT, "cv.md")

# ---------- register fonts ----------
HEADING_FONT = "Helvetica-Bold"
pdfmetrics.registerFont(TTFont("Inter", os.path.join(FONT_DIR, "Inter-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Inter-SemiBold", os.path.join(FONT_DIR, "Inter-SemiBold.ttf")))
pdfmetrics.registerFont(TTFont("JetBrainsMono", os.path.join(FONT_DIR, "JetBrainsMono-Regular.ttf")))

# ---------- colors ----------
BG      = HexColor("#0e131e")
TEXT    = HexColor("#dee2f2")
ACCENT  = HexColor("#44d8f1")
MUTED   = HexColor("#bbc9cc")
OUTLINE = HexColor("#3c494c")
BRIDGE_RED = HexColor("#cc0000")

# ---------- page geometry ----------
W, H = A4
MARGIN = 18 * mm
LEFT   = MARGIN
RIGHT  = W - MARGIN
TOP    = H - MARGIN
BOT    = MARGIN
CONTENT_W = RIGHT - LEFT

# ---------- font sizes ----------
NAME_SIZE     = 22
SUBTITLE_SIZE = 9.5
SECTION_SIZE  = 10
BODY_SIZE     = 9
COMPANY_SIZE  = 9
DATE_SIZE     = 8
SKILL_SIZE    = 8
CONTACT_SIZE  = 7.5
BULLET_SIZE   = 9

BODY_LEADING   = BODY_SIZE * 1.45
BULLET_LEADING = BULLET_SIZE * 1.4

# Sections in cv.md that belong to the About page narrative — never render
# them in the printed CV.
ABOUT_ONLY_SECTIONS = {"Hero", "Thesis", "Building", "Open To"}

# Header contact line. Kept here because cv.md only lists email/LinkedIn under
# `## Contact` and the printed CV header uses LinkedIn + GitHub + site URL.
CONTACT_LINKS = [
    "linkedin.com/in/joaofogoncalves",
    "github.com/joaofogoncalves",
    "joaofogoncalves.com",
]

_MONTH_ABBR = {
    "January": "Jan", "February": "Feb", "March": "Mar", "April": "Apr",
    "May": "May", "June": "Jun", "July": "Jul", "August": "Aug",
    "September": "Sep", "October": "Oct", "November": "Nov", "December": "Dec",
}


def _abbr_date(date_str: str) -> str:
    """Convert 'November 2025 – Present' → 'Nov 2025 – Present'."""
    out = date_str
    for full, short in _MONTH_ABBR.items():
        out = out.replace(full, short)
    return out


# ---------- markdown parsing ----------

def _parse_intro(intro_text: str) -> tuple[str, str, str]:
    """Pull name, title, and location from the pre-section intro block."""
    name = title = location = ""
    for line in intro_text.split("\n"):
        s = line.strip()
        if not s:
            continue
        if s.startswith("# "):
            name = s[2:].strip()
        elif s.startswith("**") and s.endswith("**"):
            title = s.strip("*").strip()
        elif name and not location and not s.startswith("#"):
            location = s
    return name, title, location


def parse_cv(md_text: str) -> dict:
    """Parse cv.md into name, title, location, and a section dict."""
    sections: dict[str, str] = {}
    current = None
    intro_lines: list[str] = []
    buf: list[str] = []

    for line in md_text.split("\n"):
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = line[3:].strip()
            buf = []
        elif current is None:
            intro_lines.append(line)
        else:
            buf.append(line)

    if current is not None:
        sections[current] = "\n".join(buf).strip()

    name, title, location = _parse_intro("\n".join(intro_lines))
    return {
        "name": name,
        "title": title,
        "location": location,
        "sections": sections,
    }


def parse_experience(text: str) -> list[dict]:
    """Parse Experience section into entries.

    Each entry: company, role, dates, location, bullets.
    Compact role = single bullet (rendered in the Earlier Career section).
    """
    entries = []
    for raw in re.split(r'\n---\n', text):
        raw = raw.strip()
        if not raw:
            continue
        lines = raw.split("\n")

        m = re.match(r'^###\s+(.+?)\s+[—–]\s+(.+)$', lines[0])
        if not m:
            continue
        company = m.group(1).strip()
        role = m.group(2).strip()

        dates = location = ""
        for line in lines[1:]:
            s = line.strip()
            if not s:
                continue
            dm = re.match(r'^\*\*(.+?)\*\*\s*[·•]\s*(.+)$', s)
            if dm:
                dates = _abbr_date(dm.group(1))
                location = dm.group(2).strip()
                break

        bullets = [ln.strip()[2:] for ln in lines if ln.strip().startswith("- ")]

        entries.append({
            "company": company,
            "role": role,
            "dates": dates,
            "location": location,
            "bullets": bullets,
        })
    return entries


def parse_list_items(text: str) -> list[str]:
    """Pull `- item` lines from a section body."""
    items = []
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("- "):
            items.append(s[2:].strip())
    return items


def _strip_completion_badge(skill: str) -> str:
    """Drop the trailing 'Completion Badge' tail from cert names for compactness."""
    return re.sub(r'\s+Completion Badge$', '', skill).strip()


# ---------- drawing primitives ----------

def draw_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def wrap_lines(c, text, font, size, max_width):
    words = text.split()
    lines, current = [], ""
    for w in words:
        test = (current + " " + w).strip()
        if c.stringWidth(test, font, size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


class CVBuilder:
    def __init__(self, cv: dict):
        self.cv = cv
        self.c = canvas.Canvas(OUTPUT, pagesize=A4)
        self.c.setTitle(f"{cv['name']} — CV")
        self.c.setAuthor(cv["name"])
        self.y = TOP
        self.page = 1
        draw_bg(self.c)

    def new_page(self):
        self.c.showPage()
        self.page += 1
        draw_bg(self.c)
        self.y = TOP

    def check_space(self, needed):
        if self.y - needed < BOT:
            self.new_page()

    def draw_styled_title_segment(self, x: float, y: float, segments: list[tuple]) -> float:
        """Draw a sequence of (text, font, color) segments left-to-right."""
        for text, font, color in segments:
            self.c.setFont(font, SUBTITLE_SIZE)
            self.c.setFillColor(color)
            self.c.drawString(x, y, text)
            x += self.c.stringWidth(text, font, SUBTITLE_SIZE)
        return x

    def draw_header(self):
        y = self.y

        # Line 1: Name
        self.c.setFont(HEADING_FONT, NAME_SIZE)
        self.c.setFillColor(ACCENT)
        self.c.drawString(LEFT, y, self.cv["name"])
        y -= 15

        # Line 2: Subtitle (title · location), with BRIDGE IN styled red+bold
        title = self.cv["title"]
        segments = self._split_title_for_bridge_in(title)
        x = LEFT
        x = self.draw_styled_title_segment(x, y, segments)
        if self.cv.get("location"):
            self.c.setFont("Inter", SUBTITLE_SIZE)
            self.c.setFillColor(MUTED)
            self.c.drawString(x, y, "  ·  " + self.cv["location"])
        y -= 12

        # Line 3: Contact links
        contact = "  ·  ".join(CONTACT_LINKS)
        self.c.setFont("JetBrainsMono", CONTACT_SIZE)
        self.c.setFillColor(MUTED)
        self.c.drawString(LEFT, y, contact)

        self.y = y - 6

    @staticmethod
    def _split_title_for_bridge_in(title: str) -> list[tuple]:
        """Split a title string so that 'BRIDGE IN' renders in red bold."""
        if "BRIDGE IN" not in title:
            return [(title, "Inter", TEXT)]

        parts = title.split("BRIDGE IN")
        segments: list[tuple] = []
        for i, part in enumerate(parts):
            if part:
                segments.append((part, "Inter", TEXT))
            if i < len(parts) - 1:
                segments.append(("BRIDGE IN", "Inter-SemiBold", BRIDGE_RED))
        return segments

    def draw_section_title(self, title):
        self.check_space(24)
        self.y -= 10
        self.c.setFont(HEADING_FONT, SECTION_SIZE)
        self.c.setFillColor(ACCENT)
        x = LEFT
        for ch in title.upper():
            self.c.drawString(x, self.y, ch)
            x += self.c.stringWidth(ch, HEADING_FONT, SECTION_SIZE) * 1.08

        self.y -= 5
        self.c.setStrokeColor(ACCENT)
        self.c.setLineWidth(0.5)
        self.c.line(LEFT, self.y, RIGHT, self.y)
        self.y -= 14

    def draw_summary(self, text):
        lines = wrap_lines(self.c, text, "Inter", BODY_SIZE, CONTENT_W)
        for line in lines:
            self.check_space(BODY_LEADING)
            self.c.setFont("Inter", BODY_SIZE)
            self.c.setFillColor(TEXT)
            self._draw_string_with_brand(LEFT, self.y, line, "Inter", BODY_SIZE, TEXT)
            self.y -= BODY_LEADING

    def _draw_string_with_brand(self, x: float, y: float, text: str,
                                font: str, size: float, base_color):
        """Draw a string, rendering 'BRIDGE IN' in red+bold inline."""
        if "BRIDGE IN" not in text:
            self.c.setFont(font, size)
            self.c.setFillColor(base_color)
            self.c.drawString(x, y, text)
            return

        cx = x
        parts = text.split("BRIDGE IN")
        for i, part in enumerate(parts):
            if part:
                self.c.setFont(font, size)
                self.c.setFillColor(base_color)
                self.c.drawString(cx, y, part)
                cx += self.c.stringWidth(part, font, size)
            if i < len(parts) - 1:
                bold_font = "Inter-SemiBold" if font.startswith("Inter") else font
                self.c.setFont(bold_font, size)
                self.c.setFillColor(BRIDGE_RED)
                self.c.drawString(cx, y, "BRIDGE IN")
                cx += self.c.stringWidth("BRIDGE IN", bold_font, size)

    def estimate_entry_height(self, bullets):
        height = 13
        bc_w = self.c.stringWidth("•  ", "Inter", BULLET_SIZE)
        bullet_width = CONTENT_W - 8 - bc_w
        for b in bullets:
            lines = wrap_lines(self.c, b, "Inter", BULLET_SIZE, bullet_width)
            height += len(lines) * BULLET_LEADING + 0.5
        height += 14
        return height

    def draw_experience(self, entry: dict, last: bool):
        bullets = entry["bullets"]
        needed = self.estimate_entry_height(bullets)
        self.check_space(needed)

        y = self.y

        # Company — Role
        company = entry["company"]
        self._draw_string_with_brand(LEFT, y, company, "Inter-SemiBold", COMPANY_SIZE, TEXT)
        x = LEFT + self.c.stringWidth(company, "Inter-SemiBold", COMPANY_SIZE)
        self.c.setFont("Inter", COMPANY_SIZE)
        self.c.setFillColor(TEXT)
        self.c.drawString(x, y, " — " + entry["role"])

        # Date right-aligned
        date_loc = f"{entry['dates']}  ·  {entry['location']}"
        self.c.setFont("JetBrainsMono", DATE_SIZE)
        self.c.setFillColor(MUTED)
        dw = self.c.stringWidth(date_loc, "JetBrainsMono", DATE_SIZE)
        self.c.drawString(RIGHT - dw, y, date_loc)

        y -= BODY_LEADING + 1.5

        # Bullets
        bullet_char = "•  "
        bc_w = self.c.stringWidth(bullet_char, "Inter", BULLET_SIZE)
        bullet_width = CONTENT_W - 8 - bc_w
        for b in bullets:
            lines = wrap_lines(self.c, b, "Inter", BULLET_SIZE, bullet_width)
            for j, line in enumerate(lines):
                bx = LEFT + 8 + bc_w
                if j == 0:
                    self.c.setFont("Inter", BULLET_SIZE)
                    self.c.setFillColor(TEXT)
                    self.c.drawString(LEFT + 8, y, bullet_char)
                self._draw_string_with_brand(bx, y, line, "Inter", BULLET_SIZE, TEXT)
                y -= BULLET_LEADING
            y -= 0.5

        y -= 6

        if not last:
            self.c.setStrokeColor(OUTLINE)
            self.c.setLineWidth(0.3)
            self.c.line(LEFT, y, RIGHT, y)
            y -= 12

        self.y = y

    def draw_compact_role(self, entry: dict, last: bool):
        self.check_space(28)
        y = self.y

        company = entry["company"]
        self._draw_string_with_brand(LEFT, y, company, "Inter-SemiBold", COMPANY_SIZE, TEXT)
        x = LEFT + self.c.stringWidth(company, "Inter-SemiBold", COMPANY_SIZE)
        self.c.setFont("Inter", COMPANY_SIZE)
        self.c.setFillColor(TEXT)
        self.c.drawString(x, y, " — " + entry["role"])

        self.c.setFont("JetBrainsMono", DATE_SIZE)
        self.c.setFillColor(MUTED)
        dw = self.c.stringWidth(entry["dates"], "JetBrainsMono", DATE_SIZE)
        self.c.drawString(RIGHT - dw, y, entry["dates"])

        y -= BODY_LEADING + 0.5

        description = entry["bullets"][0] if entry["bullets"] else ""
        if description:
            lines = wrap_lines(self.c, description, "Inter", BULLET_SIZE, CONTENT_W)
            for line in lines:
                self.c.setFont("Inter", BULLET_SIZE)
                self.c.setFillColor(MUTED)
                self.c.drawString(LEFT + 8, y, line)
                y -= BULLET_LEADING

        y -= 4
        if not last:
            self.c.setStrokeColor(OUTLINE)
            self.c.setLineWidth(0.2)
            self.c.line(LEFT, y, RIGHT, y)
            y -= 10

        self.y = y

    def draw_education(self, school, degree, dates):
        self.check_space(20)
        self.c.setFont("Inter-SemiBold", COMPANY_SIZE)
        self.c.setFillColor(TEXT)
        self.c.drawString(LEFT, self.y, school)

        self.c.setFont("Inter", BODY_SIZE)
        self.c.setFillColor(TEXT)
        x = LEFT + self.c.stringWidth(school, "Inter-SemiBold", COMPANY_SIZE)
        self.c.drawString(x, self.y, "  —  " + degree)

        self.c.setFont("JetBrainsMono", DATE_SIZE)
        self.c.setFillColor(MUTED)
        dw = self.c.stringWidth(dates, "JetBrainsMono", DATE_SIZE)
        self.c.drawString(RIGHT - dw, self.y, dates)
        self.y -= BODY_LEADING + 2

    def draw_inline_section(self, items):
        text = "  ·  ".join(items)
        lines = wrap_lines(self.c, text, "JetBrainsMono", SKILL_SIZE, CONTENT_W)
        for line in lines:
            self.check_space(BODY_LEADING)
            self.c.setFont("JetBrainsMono", SKILL_SIZE)
            self.c.setFillColor(MUTED)
            self.c.drawString(LEFT, self.y, line)
            self.y -= SKILL_SIZE * 1.4

    def build(self):
        sections = self.cv["sections"]

        self.draw_header()

        if "Summary" in sections and sections["Summary"]:
            self.draw_section_title("Summary")
            self.draw_summary(sections["Summary"])

        if "Experience" in sections and sections["Experience"]:
            entries = parse_experience(sections["Experience"])
            detailed = [e for e in entries if len(e["bullets"]) >= 2]
            earlier = [e for e in entries if len(e["bullets"]) <= 1]

            if detailed:
                self.draw_section_title("Experience")
                for i, e in enumerate(detailed):
                    self.draw_experience(e, last=(i == len(detailed) - 1))

            if earlier:
                self.draw_section_title("Earlier Career")
                for i, e in enumerate(earlier):
                    self.draw_compact_role(e, last=(i == len(earlier) - 1))

        if "Education" in sections and sections["Education"]:
            self.draw_section_title("Education")
            edu_text = sections["Education"]
            edu_lines = [l for l in edu_text.split("\n") if l.strip()]
            if edu_lines:
                school = edu_lines[0].lstrip("#").strip()
                degree_line = edu_lines[1] if len(edu_lines) > 1 else ""
                # Format: "Computer Science (incomplete) · September 2001 – May 2009"
                if "·" in degree_line:
                    degree, dates = [p.strip() for p in degree_line.split("·", 1)]
                else:
                    degree, dates = degree_line.strip(), ""
                self.draw_education(school, degree, _abbr_date(dates))

        if "Languages" in sections and sections["Languages"]:
            self.draw_section_title("Languages")
            self.draw_inline_section(parse_list_items(sections["Languages"]))

        if "Top Skills" in sections and sections["Top Skills"]:
            self.draw_section_title("Top Skills")
            self.draw_inline_section(parse_list_items(sections["Top Skills"]))

        if "Certifications" in sections and sections["Certifications"]:
            self.draw_section_title("Certifications")
            certs = [_strip_completion_badge(c) for c in parse_list_items(sections["Certifications"])]
            self.draw_inline_section(certs)

        self.c.save()
        size_kb = os.path.getsize(OUTPUT) / 1024
        print(f"PDF saved to {OUTPUT} ({size_kb:.0f} KB, {self.page} page(s))")


def main():
    if not os.path.exists(CV_MD):
        print(f"ERROR: cv.md not found at {CV_MD}", file=sys.stderr)
        sys.exit(1)

    with open(CV_MD, "r", encoding="utf-8") as f:
        md = f.read()

    cv = parse_cv(md)
    if not cv["name"]:
        print(f"ERROR: could not parse name from cv.md (expected '# Name' header)", file=sys.stderr)
        sys.exit(1)

    # Filter About-only sections out so they never accidentally render in the PDF
    cv["sections"] = {
        k: v for k, v in cv["sections"].items()
        if k not in ABOUT_ONLY_SECTIONS
    }

    CVBuilder(cv).build()


if __name__ == "__main__":
    main()
