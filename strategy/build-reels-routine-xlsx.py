# -*- coding: utf-8 -*-
"""Add the Reels & Video Routine tab to the exported master workbook.

Existing sheets are not modified apart from an additive note block appended to
the empty rows at the bottom of 'How to Use'.
"""
import csv, datetime, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter as L

SRC = "/tmp/claude-0/-home-user-InstagramCarousel/2d398c26-b4fd-5582-a06c-decfe796759f/scratchpad/master.xlsx"
CSV = "/home/user/InstagramCarousel/strategy/reels-video-weekly-routine-w2-w24.csv"
OUT = "/home/user/InstagramCarousel/strategy/luxury-beauty-content-plan-with-reels-routine.xlsx"

# Conventions lifted from the existing 'Posting Schedule' tab.
INK       = "FF2E2A23"   # header band / section band
BAND      = "FFF3EEE5"   # alternating row shade
RULE      = "FFD8D0C0"   # cell border
GOLD      = "FFC9A85C"   # schedule-tab colour
MUTED     = "FF6E6557"   # subtitle text

hdr_font  = Font(name="Calibri", size=11, bold=True, color="FFFFFFFF")
hdr_fill  = PatternFill("solid", fgColor=INK)
hdr_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
body_font = Font(name="Arial", size=10)
body_align= Alignment(vertical="top", wrap_text=True)
band_fill = PatternFill("solid", fgColor=BAND)
edge      = Side(style="thin", color=RULE)
box       = Border(left=edge, right=edge, top=edge, bottom=edge)

# column key -> width, taken from how much each field actually holds
WIDTHS = [7, 12, 6, 18, 20, 16, 22, 16, 40, 34, 60, 34, 55, 24, 10,
          40, 32, 38, 9, 9, 12, 18, 8, 8, 8, 8, 9]

wb = openpyxl.load_workbook(SRC)
assert "Reels & Video Routine" not in wb.sheetnames

rows = list(csv.reader(open(CSV, encoding="utf-8")))
header, data = rows[0], rows[1:]
assert len(header) == len(WIDTHS) == 27, (len(header), len(WIDTHS))
assert len(data) == 69, len(data)

ws = wb.create_sheet("Reels & Video Routine", index=2)   # sits after Posting Schedule
ws.sheet_properties.tabColor = GOLD
ws.sheet_view.showGridLines = False

for i, name in enumerate(header, start=1):
    c = ws.cell(1, i, name)
    c.font, c.fill, c.alignment, c.border = hdr_font, hdr_fill, hdr_align, box
    ws.column_dimensions[L(i)].width = WIDTHS[i - 1]
ws.row_dimensions[1].height = 30

for r, row in enumerate(data, start=2):
    week = int(row[0])
    shade = week % 2 == 0                      # one shade per week block
    for i, val in enumerate(row, start=1):
        if i == 1:                             # Week -> number
            val = week
        elif i == 2:                           # Date -> real date
            val = datetime.datetime.strptime(val, "%b %d, %Y")
        c = ws.cell(r, i, val if val != "" else None)
        c.font, c.alignment, c.border = body_font, body_align, box
        if shade:
            c.fill = band_fill
        if i == 2:
            c.number_format = 'mmm\\ d", "yyyy'
        if i in (1, 3, 15, 19, 20, 21):        # short codes read better centred
            c.alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
    ws.row_dimensions[r].height = 75

last = len(data) + 1
ws.freeze_panes = "C2"                          # matches Posting Schedule
ws.auto_filter.ref = f"A1:{L(len(header))}{last}"

status_dv = DataValidation(type="list", formula1='"Idea,Design,Ready,Hold,Posted"', allow_blank=True)
ws.add_data_validation(status_dv)
status_dv.add(f"U2:U{last}")                    # Status

done_dv = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True)
ws.add_data_validation(done_dv)
done_dv.add(f"S2:T{last}")                      # Filmed / Edited

# --- additive note on 'How to Use' -------------------------------------------
h = wb["How to Use"]
assert all(h.cell(r, c).value is None for r in range(18, 32) for c in (2, 3)), "How to Use rows 18+ are not empty"

def band(row, text):
    for col in (2, 3):
        c = h.cell(row, col)
        c.value = text if col == 2 else None
        c.font = Font(name="Arial", size=10, bold=True, color="FFFFFFFF")
        c.fill = PatternFill("solid", fgColor=INK)

def pair(row, label, value):
    a = h.cell(row, 2, label)
    a.font = Font(name="Arial", size=10, bold=True)
    a.fill = PatternFill(fill_type=None)
    b = h.cell(row, 3, value)
    b.font = Font(name="Arial", size=10)
    b.fill = PatternFill(fill_type=None)
    b.alignment = Alignment(vertical="top", wrap_text=True)

band(19, "REELS & VIDEO ROUTINE")
pair(20, "The tab", "Reels & Video Routine. Weeks 2 to 24, Aug 26 2026 to Jan 31 2027, which is month 6. Nothing on Posting Schedule was changed.")
pair(21, "Wednesday", "Slot 1. Reel. Wednesday is open on the Posting Schedule.")
pair(22, "Friday", "Slot 2. Image post or paid ad creative. Weeks 2 to 13 this is the boosted version of that week's work; weeks 14 to 24 it is a fresh image post.")
pair(23, "Sunday", "Slot 3. Reel. Sunday is open on the Posting Schedule.")
pair(24, "Cadence", "Three create-and-post actions every week. 69 items in total.")
pair(25, "New themes", "The plan stopped at Nov 15. Gift Season Opens (Nov 16-30), Glow Into the New Year (December), New Year, Real Results (January) carry it to month 6.")
pair(26, "Reuse", "About half the routine repurposes finished carousels and Photo Library pairs. The Source Assets & Notes column names the exact file or post.")
pair(27, "Consent", "Rows using client photos name the pair and its consent state. Pair D is excluded while its direction is unconfirmed. Jan 24 needs new consent and photos taken over time.")
for r in range(20, 28):
    h.row_dimensions[r].height = 28

wb.save(OUT)
print("wrote", OUT)
