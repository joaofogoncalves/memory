#!/usr/bin/env python3
"""Generate a brutalist dark-theme CV PDF using reportlab."""

import os
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
OUTPUT = os.path.join(PROJECT_ROOT, "cv.pdf")

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
    def __init__(self):
        self.c = canvas.Canvas(OUTPUT, pagesize=A4)
        self.c.setTitle("João Gonçalves — CV")
        self.c.setAuthor("João Gonçalves")
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

    def draw_header(self):
        y = self.y

        # Line 1: Name
        self.c.setFont(HEADING_FONT, NAME_SIZE)
        self.c.setFillColor(ACCENT)
        self.c.drawString(LEFT, y, "João Gonçalves")

        y -= 15

        # Line 2: Subtitle
        self.c.setFont("Inter", SUBTITLE_SIZE)
        self.c.setFillColor(TEXT)
        sub = "Founding Engineer @ "
        self.c.drawString(LEFT, y, sub)
        x = LEFT + self.c.stringWidth(sub, "Inter", SUBTITLE_SIZE)

        self.c.setFont("Inter-SemiBold", SUBTITLE_SIZE)
        self.c.setFillColor(TEXT)
        self.c.drawString(x, y, "BRIDGE IN")
        x += self.c.stringWidth("BRIDGE IN", "Inter-SemiBold", SUBTITLE_SIZE)

        self.c.setFont("Inter", SUBTITLE_SIZE)
        self.c.setFillColor(MUTED)
        self.c.drawString(x, y, "  ·  Lisbon, Portugal")

        y -= 12

        # Line 3: Contact links
        contact = "linkedin.com/in/joaofogoncalves  ·  github.com/joaofogoncalves  ·  joaofogoncalves.com"
        self.c.setFont("JetBrainsMono", CONTACT_SIZE)
        self.c.setFillColor(MUTED)
        self.c.drawString(LEFT, y, contact)

        self.y = y - 6

    def draw_section_title(self, title):
        self.check_space(24)
        self.y -= 10
        self.c.setFont(HEADING_FONT, SECTION_SIZE)
        self.c.setFillColor(ACCENT)
        spaced = title.upper()
        x = LEFT
        for ch in spaced:
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
            self.c.drawString(LEFT, self.y, line)
            self.y -= BODY_LEADING

    def estimate_entry_height(self, bullets):
        height = 13
        bc_w = self.c.stringWidth("•  ", "Inter", BULLET_SIZE)
        bullet_width = CONTENT_W - 8 - bc_w
        for b in bullets:
            lines = wrap_lines(self.c, b, "Inter", BULLET_SIZE, bullet_width)
            height += len(lines) * BULLET_LEADING + 0.5
        height += 14  # spacing around separator
        return height

    def draw_experience(self, company, role, dates, location, bullets, last=False):
        needed = self.estimate_entry_height(bullets)
        self.check_space(needed)

        y = self.y

        # Company — Role
        self.c.setFont("Inter-SemiBold", COMPANY_SIZE)
        self.c.setFillColor(TEXT)
        self.c.drawString(LEFT, y, company)
        x = LEFT + self.c.stringWidth(company, "Inter-SemiBold", COMPANY_SIZE)

        self.c.setFont("Inter", COMPANY_SIZE)
        self.c.setFillColor(TEXT)
        self.c.drawString(x, y, " \u2014 " + role)

        # Date right-aligned
        date_loc = f"{dates}  ·  {location}"
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
                self.c.setFont("Inter", BULLET_SIZE)
                self.c.setFillColor(TEXT)
                self.c.drawString(bx, y, line)
                y -= BULLET_LEADING
            y -= 0.5

        y -= 6

        if not last:
            self.c.setStrokeColor(OUTLINE)
            self.c.setLineWidth(0.3)
            self.c.line(LEFT, y, RIGHT, y)
            y -= 12

        self.y = y

    def draw_compact_role(self, company, role, dates, description, last=False):
        self.check_space(28)
        y = self.y

        self.c.setFont("Inter-SemiBold", COMPANY_SIZE)
        self.c.setFillColor(TEXT)
        self.c.drawString(LEFT, y, company)
        x = LEFT + self.c.stringWidth(company, "Inter-SemiBold", COMPANY_SIZE)

        self.c.setFont("Inter", COMPANY_SIZE)
        self.c.setFillColor(TEXT)
        self.c.drawString(x, y, " \u2014 " + role)

        self.c.setFont("JetBrainsMono", DATE_SIZE)
        self.c.setFillColor(MUTED)
        dw = self.c.stringWidth(dates, "JetBrainsMono", DATE_SIZE)
        self.c.drawString(RIGHT - dw, y, dates)

        y -= BODY_LEADING + 0.5

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
        self.draw_header()

        self.draw_section_title("Summary")
        self.draw_summary(
            "Software Engineering Leader with 15+ years of experience scaling infrastructure, "
            "teams, and technical strategy across SaaS, engineering software, and IoT ventures. "
            "Builds high-performing, cross-functional teams to ship enterprise platforms, align "
            "system architecture with business objectives, and drive cloud adoption, security "
            "compliance, and DevOps maturity."
        )

        self.draw_section_title("Experience")

        detailed = [
            ("BRIDGE IN", "Founding Engineer", "Nov 2025 – Present", "Lisbon",
             [
                 "Building the BRIDGE IN Operating System from the ground up — a full-stack platform (Django, React) centralizing payroll, accounting, HR, legal, and tax compliance across four European markets.",
                 "Designing and operating a 14-agent AI orchestration system that plans, implements, tests, and delivers full-stack features end-to-end with minimal human intervention.",
                 "Authoring 27 custom development skills automating the entire engineering pipeline: Sentry triage, Slack feedback processing, autonomous issue creation, CI failure resolution, and production deployment.",
                 "Establishing the entire product development function from zero — CI/CD, quality gates, error monitoring, and release cadence in under 3 months.",
             ]),
            ("Altium", "Director of Software Engineering", "Jan 2024 – Nov 2025", "Lisbon",
             [
                 "Integrated Valispace as an Altium 365 app, ensuring continuity and merging capabilities post-acquisition.",
                 "Doubled the engineering department's size; coached new team leads to own project management, architecture, and development.",
                 "Equipped DevOps with improved Kubernetes infrastructure to accommodate a surge in demand; streamlined cross-departmental technology solutions.",
                 "Cultivated a meritocratic department culture that retained 90% of staff post-merger.",
             ]),
            ("Valispace", "Head of Technology & Interim CTO", "Aug 2022 – Feb 2024", "Lisbon",
             [
                 "Positioned Valispace as an attractive asset for a $20M acquisition by Altium; directed all due diligence for a frictionless transition.",
                 "Partnered with CEO & CPO on strategic direction; pioneered AI's early adoption.",
                 "Orchestrated 25+ staff on three teams; operated a complex global cloud environment with only three engineers.",
                 "Implemented ISO-27001 to access regulated aerospace opportunities (Airbus, Clearspace, iSpace).",
             ]),
            ("Valispace", "Head of DevOps", "Oct 2020 – Aug 2022", "Lisbon",
             [
                 "Led an operations team responsible for 100+ cloud-based & on-premise deployments.",
                 "Owned a CI/CD pipeline that accelerated time-to-market by 88.89%.",
                 "Managed external vendor relationships for third-party tool integration.",
             ]),
            ("Valispace", "Senior Developer", "Aug 2018 – Oct 2020", "Lisbon",
             [
                 "Introduced Agile and automated testing; performed code reviews that amplified team productivity.",
                 "Developed and maintained both the backend REST API and Frontend application.",
             ]),
        ]

        for i, (co, role, dates, loc, bullets) in enumerate(detailed):
            self.draw_experience(co, role, dates, loc, bullets, last=(i == len(detailed) - 1))

        self.draw_section_title("Earlier Career")

        earlier = [
            ("Quidgest", "R&D Software Engineer", "Jan 2016 – Aug 2018",
             "Built a low-code platform enabling non-technical users to assemble ERPs, HR portals, and document management; clients included Portugal's government & armed forces."),
            ("Sources.pt", "Co-Founder & Lead Developer", "Jan 2015 – Oct 2017",
             "Conceived an IoT modular platform and built a working prototype; secured financing by pitching to a larger tech company."),
            ("Inova Software", "Senior Mobile Developer", "Apr 2013 – Jan 2015",
             "Led Partnering Place Mobile app; designed UI render engine based on descriptive models using Phonegap, Backbone.js, Angular.js."),
            ("Quidgest", "R&D Software Engineer", "May 2011 – Apr 2013",
             "Low-code platform development for government & defence clients."),
            ("EmergeIT", "Developer", "Jan 2011 – May 2011",
             "Remote management applications for mobile devices and web-based admin tools."),
            ("NAD / Design Solutions", "Developer", "Sep 2009 – Dec 2010",
             "Web applications (HTML, CSS, JS, Python, Django, SQL) for intranets, newsletters, and multimedia."),
        ]

        for i, (co, role, dates, desc) in enumerate(earlier):
            self.draw_compact_role(co, role, dates, desc, last=(i == len(earlier) - 1))

        self.draw_section_title("Education")
        self.draw_education("Universidade de Évora", "Computer Science (incomplete)", "Sep 2001 – May 2009")

        self.draw_section_title("Languages")
        self.draw_inline_section(["Portuguese (Native)", "English (Full Professional)", "French (Elementary)"])

        self.draw_section_title("Top Skills")
        self.draw_inline_section(["Python", "AI-Augmented Engineering", "Engineering Leadership", "Cloud Infrastructure & DevOps", "Product Discovery"])

        self.draw_section_title("Certifications")
        self.draw_inline_section([
            "GenAI + Marketing", "GenAI + Strategy", "GenAI + Finance",
            "Formação Pedagógica Inicial de Formadores", "Angular 6 – The Complete Guide"
        ])

        self.c.save()
        size_kb = os.path.getsize(OUTPUT) / 1024
        print(f"PDF saved to {OUTPUT} ({size_kb:.0f} KB, {self.page} page(s))")


if __name__ == "__main__":
    CVBuilder().build()
