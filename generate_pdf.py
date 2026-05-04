"""
generate_pdf.py  –  Tericsoft offer letter generator
Uses the official letterhead PDF as a background layer, then overlays
all letter content (date, subject, body, signature) on top via ReportLab.
"""

import io, os
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)
from reportlab.lib import colors

from pypdf import PdfReader, PdfWriter
from templates import get_paragraph_2

# ── Letterhead dimensions (A4 in points) ─────────────────────────────────────
PAGE_W, PAGE_H = A4          # 595 x 842 pt

# Measured from letterhead inspection:
#   Logo/address header ends at ~125 pt from top
#   Footer (www / phone / email) starts at ~782 pt from top
# We add a little breathing room so text never crowds the header.
HEADER_BOTTOM  = 140         # pt from top  — content starts here
FOOTER_TOP     = 775         # pt from top  — content must end before here

MARGIN_LEFT    = 50          # pt  (~17.6 mm) — matches letterhead left edge
MARGIN_RIGHT   = 50          # pt
CONTENT_H      = FOOTER_TOP - HEADER_BOTTOM   # 635 pt

LETTERHEAD_PATH = os.path.join(os.path.dirname(__file__), "Letterhead.pdf")

COMPANY_SHORT  = "Tericsoft Technology"
DIRECTOR_NAME  = "Abdul Rahman"
DIRECTOR_TITLE = "Director"


# ── Helpers ───────────────────────────────────────────────────────────────────
def ordinal(n: int) -> str:
    sfx = {1: "st", 2: "nd", 3: "rd"}
    return f"{n}{'th' if 11 <= n % 100 <= 13 else sfx.get(n % 10, 'th')}"

def fmt_date(d: date) -> str:
    return f"{ordinal(d.day)} {d.strftime('%B %Y')}"

def make_style(name, **kw):
    defaults = dict(fontName="Helvetica", fontSize=10.5, leading=17,
                    textColor=colors.black, alignment=TA_JUSTIFY)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)


# ── Core generator ────────────────────────────────────────────────────────────
def generate_offer_letter(
    candidate_name:      str,
    role:                str,
    reporting_to:        str,
    joining_date:        date,
    team:                str  = "AI",
    employment_type:     str  = "Internship",
    duration:            str  = "",
    offer_date:          date = None,
    candidate_full_name: str  = None,
) -> bytes:

    if offer_date is None:
        offer_date = date.today()
    if candidate_full_name is None:
        candidate_full_name = candidate_name

    first_name    = candidate_name.strip().split()[0]
    manager_first = reporting_to.strip().split()[0]

    # ── Styles ────────────────────────────────────────────────────────────────
    left      = make_style("l",  alignment=TA_LEFT)
    bold_left = make_style("bl", alignment=TA_LEFT, fontName="Helvetica-Bold")
    normal    = make_style("n",  alignment=TA_JUSTIFY)
    detail    = make_style("d",  alignment=TA_LEFT)

    # ── Build story ───────────────────────────────────────────────────────────
    story = []

    def sp(mm_val): return Spacer(1, mm_val * mm)  # mm → pt approx

    # Date
    story += [Paragraph(f"<b>{fmt_date(offer_date)}</b>", bold_left), sp(6)]

    # Subject
    subj = ("Offer of Employment at" if employment_type == "Full-Time"
            else "Internship at")
    story += [
        Paragraph(f"<b><u>Subject: {subj} {COMPANY_SHORT}</u></b>", bold_left),
        sp(5),
    ]

    # Salutation
    story += [Paragraph(f"Dear {first_name},", left), sp(4)]

    # Para 1
    if employment_type == "Full-Time":
        p1 = (
            f"In reference to your application, we are pleased to extend this offer of employment "
            f"for the position of <b>{role}</b> at {COMPANY_SHORT}. Your employment is scheduled "
            f"to commence effective from {fmt_date(joining_date)}. All of us at {COMPANY_SHORT} "
            f"are excited that you will be joining our team."
        )
    else:
        p1 = (
            f"In reference to your application, we would like to congratulate you on your "
            f"internship for the position of <b>{role}</b> for {duration}. Your internship is "
            f"scheduled to start effective from {fmt_date(joining_date)}. All of us at "
            f"{COMPANY_SHORT} are excited that you will be joining our team."
        )
    story += [Paragraph(p1, normal), sp(4)]

    # Para 2 — team-specific
    p2 = get_paragraph_2(team=team, manager=reporting_to,
                         employment_type=employment_type,
                         duration=duration, role=role)
    story += [Paragraph(p2, normal), sp(4)]

    # Para 3
    if employment_type == "Full-Time":
        p3 = (f"The detailed terms of your employment, including policies and benefits, "
              f"will be shared by {manager_first}.")
    else:
        p3 = f"The in-depth details of the internship will be shared by {manager_first}."
    story += [Paragraph(p3, normal), sp(5)]

    # Joining details
    story.append(Paragraph(f"<b>Date of Joining:</b> {fmt_date(joining_date)}", detail))
    story.append(Paragraph("<b>Timings:</b> 10:30am – 7pm", detail))
    story.append(Paragraph("<b>Weekdays:</b> Monday to Friday", detail))
    if employment_type == "Full-Time":
        story.append(Paragraph(f"<b>Reporting To:</b> {reporting_to}", detail))
    story += [sp(5)]

    # Closing
    closing = ("Again, congratulations and we look forward to working with you."
               if employment_type == "Internship"
               else "We are delighted to have you on board and look forward to achieving great things together.")
    story += [Paragraph(closing, normal), sp(7)]

    # Sign-off
    story += [
        Paragraph("Yours sincerely,", left),
        sp(14),   # space for physical signature
        Paragraph(DIRECTOR_NAME,  left),
        Paragraph(DIRECTOR_TITLE, left),
        Paragraph(COMPANY_SHORT,  left),
        sp(10),
    ]

    # Acceptance
    story += [
        Paragraph(f"I accept the terms of this offer with {COMPANY_SHORT.split()[0]}.", left),
        sp(6),
    ]

    # Signature row — name line wide, date line compact
    usable_w = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
    sig_w  = 90 * mm   # ~90 mm
    date_w = 40 * mm   # ~40 mm
    gap_w  = usable_w - sig_w - date_w

    def _underline_cell(label, width):
        t = Table([[label], [" "]], colWidths=[width])
        t.setStyle(TableStyle([
            ("FONTNAME",      (0,0),(-1,-1), "Helvetica"),
            ("FONTSIZE",      (0,0),(-1,-1), 10),
            ("LINEBELOW",     (0,1),(0,1), 0.75, colors.black),
            ("LEFTPADDING",   (0,0),(-1,-1), 0),
            ("RIGHTPADDING",  (0,0),(-1,-1), 0),
            ("TOPPADDING",    (0,0),(-1,-1), 0),
            ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ]))
        return t

    sig_row = Table(
        [[_underline_cell("Signature", sig_w),
          Spacer(gap_w, 1),
          _underline_cell("Date", date_w)]],
        colWidths=[sig_w, gap_w, date_w],
    )
    sig_row.setStyle(TableStyle([
        ("LEFTPADDING",  (0,0),(-1,-1), 0), ("RIGHTPADDING",  (0,0),(-1,-1), 0),
        ("TOPPADDING",   (0,0),(-1,-1), 0), ("BOTTOMPADDING", (0,0),(-1,-1), 0),
        ("VALIGN",       (0,0),(-1,-1), "BOTTOM"),
    ]))
    story += [sig_row, sp(2), Paragraph(candidate_full_name, left)]

    # ── Render story onto a blank canvas ─────────────────────────────────────
    content_buf = io.BytesIO()

    frame = Frame(
        x1        = MARGIN_LEFT,
        y1        = PAGE_H - FOOTER_TOP,        # bottom of frame in RL coords
        width     = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT,
        height    = CONTENT_H,
        leftPadding=0, rightPadding=0,
        topPadding=0,  bottomPadding=0,
    )

    def noop_background(canvas, doc): pass

    tmpl = PageTemplate(id="main", frames=[frame], onPage=noop_background)
    doc  = BaseDocTemplate(
        content_buf,
        pagesize    = (PAGE_W, PAGE_H),
        pageTemplates = [tmpl],
        leftMargin  = 0, rightMargin  = 0,
        topMargin   = 0, bottomMargin = 0,
    )
    doc.build(story)

    # ── Merge: letterhead (background) + content (foreground) ─────────────────
    letterhead_reader = PdfReader(LETTERHEAD_PATH)
    content_reader    = PdfReader(io.BytesIO(content_buf.getvalue()))

    writer = PdfWriter()
    lh_page      = letterhead_reader.pages[0]
    content_page = content_reader.pages[0]

    # Stamp the text content over the letterhead
    lh_page.merge_page(content_page)
    writer.add_page(lh_page)

    out_buf = io.BytesIO()
    writer.write(out_buf)
    return out_buf.getvalue()
