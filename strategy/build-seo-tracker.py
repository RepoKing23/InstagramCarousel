#!/usr/bin/env python3
"""
Builds strategy/seo-roadmap-tracker.xlsx — the working task tracker for the
90-day local SEO and Instagram plan in strategy/seo-roadmap-90-day.docx.

Run from the repo root:
    pip install openpyxl
    python3 strategy/build-seo-tracker.py

Designed to be uploaded to Google Sheets and updated daily. Every task here
traces back to a section of the roadmap document; if you change one, change
the other. Dates assume the quarter runs Sept 1 - Nov 30, 2026.
"""

import datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

OUT = "strategy/seo-roadmap-tracker.xlsx"

# Palette carried over from the roadmap document and design/botox-myths.html
INK = "2E2A23"
GOLD = "C9A85C"
CREAM_DEEP = "E5DCCA"
CREAM = "F3EEE5"
GREEN = "DDEBD8"
AMBER = "FBEFD4"
RED = "F6DCDA"
GREY = "6E6557"

STATUSES = ["Not started", "In progress", "Blocked", "Done", "Not applicable"]
OWNERS = ["Agency", "Cleo", "Both"]
PRIORITIES = ["High", "Medium", "Low"]
CADENCES = ["One-off", "Weekly", "Fortnightly", "Ongoing"]
APPLIES = ["Any path", "Path B or C", "Path C only", "Path A only"]

# Week 1 starts Tue Sept 1 2026; each task is due at the end of its week.
WEEK_DUE = {
    1: dt.date(2026, 9, 6),    2: dt.date(2026, 9, 13),
    3: dt.date(2026, 9, 20),   4: dt.date(2026, 9, 27),
    5: dt.date(2026, 10, 4),   6: dt.date(2026, 10, 11),
    7: dt.date(2026, 10, 18),  8: dt.date(2026, 10, 25),
    9: dt.date(2026, 11, 1),  10: dt.date(2026, 11, 8),
    11: dt.date(2026, 11, 15), 12: dt.date(2026, 11, 22),
}

# (week, area, task, owner, cadence, priority, applies)
TASKS = [
    # ---------------------------------------------------- Month 1: foundation
    (1, "Google profile", "Find out who owns the Google Business Profile and which email holds it", "Cleo", "One-off", "High", "Any path"),
    (1, "Google profile", "Confirm with Allure whether you can use your own signage and suite designation", "Cleo", "One-off", "High", "Any path"),
    (1, "Google profile", "Claim and verify the Google Business Profile", "Agency", "One-off", "High", "Any path"),
    (1, "Google profile", "Correct the GBP address to L6M 0T9 and add the suite designation", "Agency", "One-off", "High", "Any path"),
    (1, "Google profile", "Replace the dead website link on GBP with Instagram or the booking link", "Agency", "One-off", "High", "Any path"),
    (1, "Citations", "Decide on one email address and one phone number to use everywhere", "Cleo", "One-off", "High", "Any path"),
    (1, "Measurement", "Record baseline: 12 reviews, 5.0 average, GBP calls and direction requests", "Agency", "One-off", "High", "Any path"),
    (1, "Measurement", "Send us your real opening hours for every day of the week", "Cleo", "One-off", "High", "Any path"),

    (2, "Website", "WEBSITE DECISION DUE: Path A, Path B or Path C", "Cleo", "One-off", "High", "Any path"),
    (2, "Google profile", "Set real opening hours on GBP for all days", "Agency", "One-off", "High", "Any path"),
    (2, "Google profile", "Choose the primary GBP category", "Agency", "One-off", "High", "Any path"),
    (2, "Google profile", "Choose secondary categories that avoid colliding with Allure's listing", "Agency", "One-off", "High", "Any path"),
    (2, "Google profile", "Add a working booking link to GBP", "Agency", "One-off", "High", "Any path"),
    (2, "Google profile", "Upload real photos to GBP: treatment room, you, the space", "Both", "One-off", "High", "Any path"),
    (2, "Measurement", "Set up Google Search Console", "Agency", "One-off", "Medium", "Any path"),
    (2, "Measurement", "Set up analytics", "Agency", "One-off", "Medium", "Any path"),

    (3, "Citations", "Correct postal code to L6M 0T9 on Birdeye", "Agency", "One-off", "High", "Any path"),
    (3, "Citations", "Correct postal code to L6M 0T9 on Facebook", "Agency", "One-off", "High", "Any path"),
    (3, "Citations", "Correct postal code to L6M 0T9 on Fresha", "Agency", "One-off", "High", "Any path"),
    (3, "Citations", "Correct postal code to L6M 0T9 on Yelp.ca", "Agency", "One-off", "Medium", "Any path"),
    (3, "Citations", "Correct postal code to L6M 0T9 on Yellow Pages", "Agency", "One-off", "Medium", "Any path"),
    (4, "Citations", "Correct postal code to L6M 0T9 on Apple Maps", "Agency", "One-off", "Medium", "Any path"),
    (4, "Citations", "Correct postal code to L6M 0T9 on Bing Places", "Agency", "One-off", "Medium", "Any path"),
    (4, "Citations", "Correct postal code to L6M 0T9 on RateMDs", "Agency", "One-off", "Low", "Any path"),
    (4, "Citations", "Correct postal code to L6M 0T9 on the Canadian chamber directories", "Agency", "One-off", "Low", "Any path"),
    (4, "Citations", "Claim any listing about the practice that is not under your control", "Agency", "One-off", "Medium", "Any path"),

    # ------------------------------------------- Month 2: reviews and presence
    (5, "Reviews", "Write the WhatsApp review-ask message", "Agency", "One-off", "High", "Any path"),
    (5, "Reviews", "Start sending the review ask within 24 hours of every appointment", "Cleo", "Ongoing", "High", "Any path"),
    (5, "Reviews", "Reply to all 12 existing reviews", "Cleo", "One-off", "Medium", "Any path"),
    (5, "Reviews", "Reply to every new review within two days", "Cleo", "Ongoing", "Medium", "Any path"),
    (5, "Compliance", "Confirm the signed before-and-after consent form is on file", "Cleo", "One-off", "High", "Any path"),
    (5, "Compliance", "Compliance pass on the 21 briefs naming Botox or Dysport in client-facing copy", "Agency", "One-off", "High", "Any path"),
    (5, "Instagram", "Rewrite the Instagram name field to read 'Cleo | Nurse Injector Oakville'", "Agency", "One-off", "High", "Any path"),
    (5, "Instagram", "Rewrite the Instagram bio to name the town and the treatments", "Agency", "One-off", "High", "Any path"),
    (5, "Instagram", "Fix the link in bio so it no longer points at the dead domain", "Agency", "One-off", "High", "Any path"),
    (5, "Instagram", "Start location-tagging Oakville on every post", "Cleo", "Ongoing", "High", "Any path"),
    (5, "Ads", "Send us your current monthly Instagram and Google ad spend", "Cleo", "One-off", "High", "Any path"),
    (5, "Website", "Hosting sorted, DNS pointed, platform set up, page structure agreed", "Agency", "One-off", "High", "Path B or C"),

    (6, "Reviews", "Design and print the QR review card for the treatment room", "Agency", "One-off", "Medium", "Any path"),
    (6, "Google profile", "Fill out the GBP services list with a plain description of each treatment", "Agency", "One-off", "Medium", "Any path"),
    (6, "Google profile", "Seed the GBP questions section with real questions and answers", "Both", "One-off", "Medium", "Any path"),
    (6, "Google profile", "Post to GBP once a week using carousels from the content calendar", "Agency", "Weekly", "Medium", "Any path"),
    (6, "Instagram", "Switch to locally weighted hashtag sets, clear of prescription brand names", "Agency", "One-off", "Medium", "Any path"),
    (6, "Instagram", "Write alt text on every new post", "Cleo", "Ongoing", "Medium", "Any path"),
    (6, "Instagram", "Reorganise Highlights by treatment", "Agency", "One-off", "Medium", "Any path"),
    (6, "Instagram", "Build out Highlights as the full treatment menu, standing in for a website", "Agency", "One-off", "High", "Path A only"),
    (6, "Ads", "Build the local radius audience, 15km around Oakville", "Agency", "One-off", "High", "Any path"),
    (6, "Ads", "Build the 30-day engagement retargeting audience", "Agency", "One-off", "High", "Any path"),
    (6, "Ads", "Launch three or four ad creatives pulled from existing carousels", "Agency", "One-off", "High", "Any path"),
    (6, "Website", "Home and contact pages live with correct NAP, hours, booking link and schema", "Agency", "One-off", "High", "Path B or C"),

    (7, "Ads", "Export the patient list from the booking system for the lookalike audience", "Cleo", "One-off", "Medium", "Any path"),
    (7, "Ads", "Build the lookalike audience", "Agency", "One-off", "Medium", "Any path"),
    (7, "Website", "Build treatment pages: lip filler, dermal filler, anti-wrinkle, skin boosters", "Agency", "One-off", "High", "Path C only"),
    (7, "Website", "Build treatment pages: dermaplaning, electrolysis, Belkyra", "Agency", "One-off", "High", "Path C only"),

    (8, "Ads", "Fortnightly ad review: kill anything below average cost per DM, reallocate", "Agency", "Fortnightly", "High", "Any path"),
    (8, "Website", "Oakville and surrounding-area content, plus internal linking", "Agency", "One-off", "Medium", "Path C only"),
    (8, "Website", "Mobile speed pass", "Agency", "One-off", "Medium", "Path B or C"),
    (8, "Website", "Launch: verify Search Console, submit sitemap, confirm analytics running", "Agency", "One-off", "High", "Path B or C"),
    (8, "Website", "Repoint the GBP website field at the live site", "Agency", "One-off", "High", "Path B or C"),
    (8, "Citations", "Update every directory listing to the new website URL", "Agency", "One-off", "Medium", "Path B or C"),

    # ------------------------------------------------- Month 3: make it compound
    (9, "Local links", "Submit to Oakville business directories", "Agency", "One-off", "Medium", "Any path"),
    (9, "Local links", "Ask Allure about a cross-link between the two businesses", "Cleo", "One-off", "Low", "Any path"),
    (9, "Google profile", "Add the weight-loss service entry to GBP ahead of the launch", "Agency", "One-off", "Medium", "Any path"),
    (10, "Local links", "Approach Halton-area partners for mentions and links", "Agency", "One-off", "Medium", "Any path"),
    (10, "Website", "Build the weight-loss pre-launch page", "Agency", "One-off", "Medium", "Path C only"),
    (10, "Website", "Write the first question-intent article and link it to its treatment page", "Agency", "One-off", "Medium", "Path C only"),
    (11, "Website", "Write two more question-intent articles from real consult questions", "Agency", "One-off", "Medium", "Path C only"),
    (11, "Reviews", "Check progress against the 8 to 10 new reviews target and adjust the ask", "Agency", "One-off", "High", "Any path"),
    (12, "Measurement", "Full review of every number against the week-one baseline", "Agency", "One-off", "High", "Any path"),
    (12, "Measurement", "Write the recommendation for Q1 2027", "Agency", "One-off", "High", "Any path"),
]

# ------------------------------------------------------------------- styling

def hdr(ws, row, headers, widths):
    for i, (h, w) in enumerate(zip(headers, widths), start=1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = Font(name="Calibri", size=10, bold=True, color=INK)
        c.fill = PatternFill("solid", fgColor=CREAM_DEEP)
        c.alignment = Alignment(vertical="center", wrap_text=True)
        c.border = Border(bottom=Side("thin", color=GOLD))
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 28


def title_block(ws, title, subtitle):
    a = ws.cell(row=1, column=1, value=title)
    a.font = Font(name="Georgia", size=15, bold=True, color=INK)
    b = ws.cell(row=2, column=1, value=subtitle)
    b.font = Font(name="Calibri", size=10, italic=True, color=GREY)
    ws.row_dimensions[1].height = 22


def dv(ws, values, cells):
    v = DataValidation(type="list", formula1='"' + ",".join(values) + '"', allow_blank=True)
    ws.add_data_validation(v)
    v.add(cells)
    return v


wb = Workbook()

# ============================================================== Start Here tab
ws = wb.active
ws.title = "Start Here"
title_block(ws, "Getting Found in Oakville — 90-day tracker",
            "Working file for Luxury Beauty by Cleo R. Companion to seo-roadmap-90-day.docx")

rows = [
    ("", ""),
    ("HOW THIS WORKS", ""),
    ("The plan", "Everything in the Tasks tab comes from a section of the roadmap document. Read that first, once."),
    ("Daily", "Open the Tasks tab. Filter Status to 'In progress' and 'Not started'. Update what moved."),
    ("You edit", "Status, Date done, and Notes. Leave the rest unless the plan genuinely changes."),
    ("Blocked?", "Set Status to Blocked and write what you are waiting on in Notes. Blocked rows turn red."),
    ("Applies to", "Website tasks are tagged Path B or C / Path C only. Once Cleo decides, filter out what does not apply."),
    ("Weekly", "Check the Reviews tab. It is the single highest-return thing in the plan and it needs a weekly nudge."),
    ("Monthly", "Fill the Metrics tab. Compare against the baseline column, not against last week."),
    ("", ""),
    ("THE ONE DECISION EVERYTHING WAITS ON", ""),
    ("Website", "Path A: no site. Path B: one page in two weeks. Path C: full build. Due week 2."),
    ("If it slips", "Site tasks shift with it. A decision after week 4 pushes launch outside the quarter."),
    ("", ""),
    ("WHERE THINGS STAND", ""),
]
r = 4
for a, b in rows:
    ca = ws.cell(row=r, column=1, value=a)
    cb = ws.cell(row=r, column=2, value=b)
    if a.isupper() and a:
        ca.font = Font(name="Calibri", size=10, bold=True, color="B99753")
    else:
        ca.font = Font(name="Calibri", size=10, bold=True, color=INK)
    cb.font = Font(name="Calibri", size=10, color=INK)
    cb.alignment = Alignment(wrap_text=True, vertical="top")
    r += 1

snap_start = r
n = len(TASKS)
for lbl, formula in [
    ("Total tasks", f"=COUNTA(Tasks!F2:F{n+1})"),
    ("Not started", f'=COUNTIF(Tasks!K2:K{n+1},"Not started")'),
    ("In progress", f'=COUNTIF(Tasks!K2:K{n+1},"In progress")'),
    ("Blocked", f'=COUNTIF(Tasks!K2:K{n+1},"Blocked")'),
    ("Done", f'=COUNTIF(Tasks!K2:K{n+1},"Done")'),
    ("Overdue and not done", f'=SUMPRODUCT((Tasks!D2:D{n+1}<TODAY())*(Tasks!K2:K{n+1}<>"Done")*(Tasks!K2:K{n+1}<>"Not applicable"))'),
    ("Percent complete", f'=IFERROR(COUNTIF(Tasks!K2:K{n+1},"Done")/COUNTA(Tasks!F2:F{n+1}),0)'),
]:
    ws.cell(row=r, column=1, value=lbl).font = Font(name="Calibri", size=10, bold=True, color=INK)
    c = ws.cell(row=r, column=2, value=formula)
    c.font = Font(name="Calibri", size=10, color=INK)
    if lbl == "Percent complete":
        c.number_format = "0%"
    r += 1
ws.cell(row=snap_start - 1, column=1).font = Font(name="Calibri", size=10, bold=True, color="B99753")

ws.column_dimensions["A"].width = 26
ws.column_dimensions["B"].width = 96

r += 1
note = ws.cell(row=r, column=1, value="Import to Google Sheets: drive.google.com > New > File upload > pick this file > open with Google Sheets.")
note.font = Font(name="Calibri", size=9, italic=True, color=GREY)

# =================================================================== Tasks tab
ws = wb.create_sheet("Tasks")
headers = ["ID", "Month", "Week", "Due", "Area", "Task", "Owner",
           "Cadence", "Priority", "Applies to", "Status", "Date done", "Notes / blockers"]
widths = [5, 9, 7, 11, 15, 62, 9, 12, 9, 13, 14, 11, 40]
hdr(ws, 1, headers, widths)

for i, (week, area, task, owner, cadence, prio, applies) in enumerate(TASKS, start=1):
    month = 1 if week <= 4 else (2 if week <= 8 else 3)
    row = i + 1
    vals = [i, f"Month {month}", f"W{week}", WEEK_DUE[week], area, task,
            owner, cadence, prio, applies, "Not started", None, None]
    for col, v in enumerate(vals, start=1):
        c = ws.cell(row=row, column=col, value=v)
        c.font = Font(name="Calibri", size=10, color=INK)
        c.alignment = Alignment(vertical="top", wrap_text=(col in (6, 13)))
        if col in (4, 12):
            c.number_format = "yyyy-mm-dd"
    ws.row_dimensions[row].height = 15

last = len(TASKS) + 1
ws.freeze_panes = "A2"
ws.auto_filter.ref = f"A1:M{last}"

dv(ws, OWNERS, f"G2:G{last}")
dv(ws, CADENCES, f"H2:H{last}")
dv(ws, PRIORITIES, f"I2:I{last}")
dv(ws, APPLIES, f"J2:J{last}")
dv(ws, STATUSES, f"K2:K{last}")

rng = f"A2:M{last}"
ws.conditional_formatting.add(rng, FormulaRule(formula=['$K2="Done"'], fill=PatternFill("solid", fgColor=GREEN), stopIfTrue=False))
ws.conditional_formatting.add(rng, FormulaRule(formula=['$K2="Blocked"'], fill=PatternFill("solid", fgColor=RED), stopIfTrue=False))
ws.conditional_formatting.add(rng, FormulaRule(formula=['$K2="In progress"'], fill=PatternFill("solid", fgColor=AMBER), stopIfTrue=False))
ws.conditional_formatting.add(rng, FormulaRule(
    formula=[f'AND($D2<TODAY(),$K2<>"Done",$K2<>"Not applicable")'],
    font=Font(color="B03A2E", bold=True), stopIfTrue=False))

# ================================================================= Reviews tab
ws = wb.create_sheet("Reviews")
title_block(ws, "Review tracker",
            "Baseline 12 reviews at 5.0. Target 8 to 10 new ones this quarter, roughly one every ten days.")
hdr(ws, 4, ["Date asked", "Patient (initials)", "How we asked", "Asked by",
            "Review received", "Date received", "Platform", "Replied", "Notes"],
    [12, 17, 16, 11, 15, 13, 12, 10, 40])
for row in range(5, 65):
    for col in range(1, 10):
        ws.cell(row=row, column=col).font = Font(name="Calibri", size=10, color=INK)
    ws.cell(row=row, column=1).number_format = "yyyy-mm-dd"
    ws.cell(row=row, column=6).number_format = "yyyy-mm-dd"
ws.freeze_panes = "A5"
dv(ws, ["WhatsApp", "QR card in room", "In person", "Email", "Text"], "C5:C64")
dv(ws, ["Cleo", "Agency"], "D5:D64")
dv(ws, ["Yes", "No", "Waiting"], "E5:E64")
dv(ws, ["Google", "Facebook", "Birdeye", "Fresha"], "G5:G64")
dv(ws, ["Yes", "No"], "H5:H64")
ws.conditional_formatting.add("A5:I64", FormulaRule(formula=['$E5="Yes"'], fill=PatternFill("solid", fgColor=GREEN), stopIfTrue=False))

ws.cell(row=2, column=6, value="Asks sent").font = Font(name="Calibri", size=10, bold=True, color=INK)
ws.cell(row=2, column=7, value="=COUNTA(A5:A64)").font = Font(name="Calibri", size=10, color=INK)
ws.cell(row=2, column=8, value="Reviews landed").font = Font(name="Calibri", size=10, bold=True, color=INK)
ws.cell(row=2, column=9, value='=COUNTIF(E5:E64,"Yes")').font = Font(name="Calibri", size=10, bold=True, color=INK)

# ================================================================= Metrics tab
ws = wb.create_sheet("Metrics")
title_block(ws, "Monthly numbers",
            "Fill at the end of each month. Compare against the baseline column, not against last month.")
hdr(ws, 4, ["What we track", "Baseline (week 1)", "Target by Nov 30",
            "End of Sept", "End of Oct", "End of Nov", "Notes"],
    [38, 18, 34, 13, 13, 13, 38])
metrics = [
    ("Google reviews", "12", "20 to 22, still at or near 5.0"),
    ("Google review average", "5.0", "At or near 5.0"),
    ("Calls from Google profile", "", "Up on baseline"),
    ("Direction requests from Google", "", "Up on baseline"),
    ("Google profile views", "", "Up on baseline"),
    ("Map pack position: nurse injector oakville", "", "Visible in the pack"),
    ("Map pack position: botox oakville", "", "Visible in the pack"),
    ("Map pack position: lip filler oakville", "", "Visible in the pack"),
    ("Instagram profile visits", "", "Up on baseline"),
    ("Instagram link taps", "", "Rising faster than profile visits"),
    ("DMs received", "Not tracked", "Tracked weekly from week 1"),
    ("Consultations booked", "Not tracked", "Tracked weekly, attributed to source"),
    ("Ad spend", "Not supplied", "Confirmed and split 70/20/10"),
    ("Cost per DM from ads", "", "Falling month on month"),
    ("Organic website sessions", "No site", "Only applies under Path B or C"),
]
for i, (m, base, target) in enumerate(metrics, start=5):
    for col, v in enumerate([m, base, target], start=1):
        c = ws.cell(row=i, column=col, value=v)
        c.font = Font(name="Calibri", size=10, bold=(col == 1), color=INK)
        c.alignment = Alignment(wrap_text=True, vertical="top")
ws.freeze_panes = "A5"

# ============================================================== Site Build tab
ws = wb.create_sheet("Site Build")
title_block(ws, "Website build timeline",
            "Only in play if Cleo approves Path B or C. Weeks counted from her approval, not from the start of the quarter.")
hdr(ws, 4, ["Week from approval", "What we do", "What we need from Cleo", "Status", "Date done", "Notes"],
    [17, 58, 40, 14, 11, 32])
build = [
    ("1", "Hosting sorted, DNS pointed, platform set up, page structure agreed", "Registrar access, final treatment list and pricing"),
    ("2", "Home and contact live with correct address (L6M 0T9), hours, booking link, schema. Path B ends here and you are live", "Photos of the room and of Cleo, headshot, logo files"),
    ("3-4", "Treatment pages: lip filler, dermal filler and facial balancing, anti-wrinkle injections, skin boosters, dermaplaning, electrolysis, Belkyra", "Read the copy, confirm every claim is one she can stand behind"),
    ("5", "Oakville and surrounding-area content, internal linking, mobile speed pass, GBP repointed", "Nothing. This week is ours"),
    ("6", "Launch. Search Console verified, sitemap submitted, analytics running, citations updated", "Final sign-off"),
    ("7-12", "Indexing and iteration. Question-intent articles and the weight-loss page", "The questions she gets asked most in consults"),
]
for i, (wk, doing, needs) in enumerate(build, start=5):
    for col, v in enumerate([wk, doing, needs, "Not started", None, None], start=1):
        c = ws.cell(row=i, column=col, value=v)
        c.font = Font(name="Calibri", size=10, bold=(col == 1), color=INK)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.cell(row=i, column=5).number_format = "yyyy-mm-dd"
    ws.row_dimensions[i].height = 34
dv(ws, STATUSES, "D5:D10")
ws.conditional_formatting.add("A5:F10", FormulaRule(formula=['$D5="Done"'], fill=PatternFill("solid", fgColor=GREEN), stopIfTrue=False))
ws.conditional_formatting.add("A5:F10", FormulaRule(formula=['$D5="Blocked"'], fill=PatternFill("solid", fgColor=RED), stopIfTrue=False))
ws.freeze_panes = "A5"

# ============================================================ Waiting On tab
ws = wb.create_sheet("Waiting On Cleo")
title_block(ws, "Waiting on Cleo",
            "Access, assets and answers. Most delay in work like this comes from waiting on these.")
hdr(ws, 4, ["Type", "What we need", "Why it blocks us", "Status", "Date received", "Notes"],
    [11, 46, 46, 14, 13, 30])
waiting = [
    ("Access", "Google Business Profile, and which email holds it", "Nothing on the profile can start until this is settled"),
    ("Access", "Domain registrar login for luxurybeautybycleo.ca", "Needed to point the domain at anything live"),
    ("Access", "Meta Business account and ad account", "Needed to build audiences and run ads"),
    ("Access", "Instagram collaborator invitation", "Needed to fix the name field, bio and link"),
    ("Access", "Booking system login", "Needed for the booking link and the lookalike audience"),
    ("Asset", "Photos of the treatment room and the space", "GBP photos and any website page"),
    ("Asset", "A current headshot", "GBP, Instagram and the site"),
    ("Asset", "Signed before-and-after consent form", "Determines what we are allowed to publish"),
    ("Asset", "Treatment list with current pricing", "Service pages and GBP services list"),
    ("Answer", "Real opening hours for every day", "GBP hours are wrong until we have these"),
    ("Answer", "Whether Allure allows her own signage and suite designation", "Decides how we build the Google listing"),
    ("Answer", "The three competitors she wants to be measured against", "Shapes what we track and benchmark"),
    ("Answer", "Her ideal patient, in her own words", "Ad audiences and page copy"),
    ("Answer", "Current monthly spend on Instagram and Google ads", "Cannot recommend a budget without it"),
    ("Answer", "THE WEBSITE DECISION: Path A, B or C", "Roughly a third of the plan depends on this"),
]
for i, (t, need, why) in enumerate(waiting, start=5):
    for col, v in enumerate([t, need, why, "Not started", None, None], start=1):
        c = ws.cell(row=i, column=col, value=v)
        c.font = Font(name="Calibri", size=10, bold=(col == 1), color=INK)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.cell(row=i, column=5).number_format = "yyyy-mm-dd"
last_w = 4 + len(waiting)
dv(ws, ["Not started", "Asked", "Chased", "Received", "Not applicable"], f"D5:D{last_w}")
ws.conditional_formatting.add(f"A5:F{last_w}", FormulaRule(formula=['$D5="Received"'], fill=PatternFill("solid", fgColor=GREEN), stopIfTrue=False))
ws.conditional_formatting.add(f"A5:F{last_w}", FormulaRule(formula=['$D5="Chased"'], fill=PatternFill("solid", fgColor=AMBER), stopIfTrue=False))
ws.freeze_panes = "A5"

wb.save(OUT)
print(f"wrote {OUT} — {len(TASKS)} tasks across {len(wb.sheetnames)} tabs: {', '.join(wb.sheetnames)}")
