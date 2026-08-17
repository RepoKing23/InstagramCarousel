# Planner Rebuild: Before & After + Carousel Posts

Plan for adding real-result content to the Aug 17 – Nov 15, 2026 schedule,
plus a corrected audit of the 20 client photos in `design/photos/cleo/`.

---

## Part 1. Photo audit — what we actually have

I opened all 20 photos and grouped them by client. The result differs from the
current `design/photos/cleo/README.md` in four places (flagged below).

### Distinct clients: 7

| # | Client (how to spot them) | Photos | What it is |
|---|---|---|---|
| A | Neck tattoos, nose ring, front-on | `img_0221`, `img_0233` | **Before + after pair** |
| B | 3/4 profile, plain wall, lower face only | `img_0962`, `img_0998` | **Before + after pair** |
| C | Blonde, reclined in chair, black tank | `img_1119`, `img_1123` | **Before + after pair** |
| D | Blonde, pearl earring, mole on chin | `img_1444`, `img_1447` | Pair, but direction unclear |
| E | Fair skin, black top, lower face only | `img_9908`, `img_9912` | **Before + after pair** |
| F | Yellow headband, day 0 | `img_9848`, `img_9850`, `whatsapp-…10.14.36-pm` | After only, 2 angles |
| G | Dark hair, salon corner, beige top | `img_4775`, `4777`, `4778`, `4780`, `4781`, `4782` | After only, 6 angles, healed |
| H | Dark hair, reclined, black top + chain | `img_7715` | After only, day 0 |

### Corrections to the existing README

1. **`img_1119` is a before, not an after.** The README files both `1119` and
   `1123` under "same-day post treatment (swollen and red)." Same client, same
   chair, same black tank, same mole below the jaw — `1119` has flat, thin lips
   and `1123` has clearly fuller, defined ones. That is a pair we were not
   counting.
2. **`img_0962` was left out of every category.** It is the before for
   `img_0998` — same 3/4 angle, same spot pattern on the cheek and jaw. Another
   pair we were not counting.
3. **"All 20 photos are lower face" is wrong.** The `img_4775`–`4782` set is
   full face, including brows and eyes. (The README contradicts itself two
   paragraphs later.) It matters for consent.
4. **The WhatsApp composite is not a before/after.** Both halves show the
   yellow headband and day-0 swelling — it is one client, two angles, after
   only. Safe as a result card, misleading if labelled Before/After.

### Answer: how many before/afters can we make

**Four publishable pairs, plus one to confirm with Cleo.**

| Pair | Photos | Strength | Gate |
|---|---|---|---|
| E | `img_9908` → `img_9912` | ★★★ Cleanest. No identifying features. | None. Already rendered for Oct 8 |
| A | `img_0221` → `img_0233` | ★★★ Biggest visible change, front-on | Neck tattoos identify her — written consent or crop above the collarbone |
| B | `img_0962` → `img_0998` | ★★ Strong change, lower face only | Colour-match: before is cool, after is warm |
| C | `img_1119` → `img_1123` | ★★ Same session, real change | Crop before to lower face (eyes visible); white balance differs a lot |
| D | `img_1444` / `img_1447` | ✗ Hold | The change is not legible at post size and I read the direction as the reverse of what the README says. Do not publish until Cleo confirms which is which |

Every pair is high enough resolution for the template (each frame renders at
450×520; the smallest file, `img_0962`, is 945×1390).

**Two after-only sets that carry their own posts:**

- **Client G** (6 angles, healed, full face) — a "one result, every angle"
  carousel or a testimonial card. Needs written consent, full face.
- **Clients F + H** (day 0, swollen, injection marks visible) — the honest
  aftercare post where swelling is the teaching point, not a results post.

---

## Part 2. What to add to the schedule

**Decisions taken:** convert rows already marked `Idea` rather than add dates, so
the post count stays at 65 and the 5-per-week rhythm holds. Consent is on file
for the identifiable clients on the condition that **faces are covered** — so
every result photo gets cropped to the treatment area, which also makes all 20
photos usable. Displaced topics move to the Ideas Backlog tab, not the bin.

Seven photo-backed posts, four of them carousels, using **all 20 photos**:

| Date | Slot was | Becomes | Format | Photos |
|---|---|---|---|---|
| Oct 8 (Thu) | Lip Filler: Natural vs Overdone | unchanged topic, result slide added | Carousel | Pair E — `9908`, `9912` |
| Oct 10 (Sat) | Quote: Subtle Is the New Dramatic | **Subtle Is the New Dramatic** — the quote proved with a real result | **Before/After** | Pair C — `1119`, `1123` |
| Oct 15 (Thu) | Is Filler Right for You? | **Real Lips. Real Results.** cover + 4 result slides + CTA | Carousel | Pairs E, A, B, C |
| Oct 22 (Thu) | Lip Filler Aftercare: Your First Week | unchanged topic, day-0 photos added | Carousel | `7715`, `9848`, `9850`, composite |
| Oct 24 (Sat) | Client Words: The Lip Glow-Up | testimonial backed by the result | **Before/After** | Pair B — `0962`, `0998` |
| Oct 30 (Fri) | Faces, Not Lines | **One Syringe. Balanced Lips.** | **Before/After** | Pair A — `0221`, `0233` |
| Nov 6 (Fri) | The Clinic Is Holiday Ready | **One Result, Every Angle** | Carousel | Client G — `4775`–`4782` |

Displaced to the Ideas Backlog: *Is Filler Right for You? An Honest Checklist*,
*Quote: Subtle Is the New Dramatic* (as a plain quote card), *The Clinic Is
Holiday Ready*.

Notes:
- Every pair appears once as its own post and once inside the Oct 15 carousel.
  Two-plus weeks apart with different framing, so it does not read as a repeat.
- Pair D stays out of the schedule until Cleo confirms the direction. It is
  logged in the Photo Library tab as `Hold` so it is not forgotten.
- Format counts after the change: 27 Carousel, 3 Before/After, 35 Single Image.

---

## Part 3. Planner rebuild

Rebuild `strategy/ig-content-strategy.xlsx` from a generator script so it can
be regenerated as the schedule changes, rather than hand-edited.

**Posting Schedule tab**
- Add `Before/After` as a Format value alongside Carousel and Single Image.
- New column **Photo Assets** — the exact `img_*.jpg` files each post uses, so
  nobody has to re-guess which photo goes where.
- New column **Consent** — `Not needed` / `Needed` / `On file`. Any row using
  clients A or G starts as `Needed`.
- Fix stale statuses: Aug 17, Aug 18 and Oct 8 all have finished renders on
  disk but are still marked `Idea` (Aug 18) or missing (Oct 8). Set to `Ready`.
- Add the six rows from Part 2.

**New tab: Photo Library**
One row per photo — filename, client group A–H, type (before / after / day 0 /
healed), pair ID, consent status, and which post uses it. This is the thing the
current setup is missing: the photo audit lives in a README that the planner
never points at.

**How to Use tab**
- Update the count (65 posts → 71) and the status snapshot formulas to match.
- Add a line for the before/after rules already in the photo README: consent
  first, "individual results vary" on every result post, and no paid boosting
  of before/after cosmetic imagery on IG or TikTok.

**Design template**
`design/before-after.html` already renders one pair well. It needs a second
mode for the Oct 15 carousel — same layout, `?slide=N` swapping the photo pair
and the four benefit bullets — following the pattern in `design/botox-myths.html`.

---

## Part 4. Order of work

1. Correct `design/photos/cleo/README.md` (the four fixes in Part 1).
2. Ask Cleo: consent status for clients A and G, and the direction of pair D.
3. Write the workbook generator + rebuild the xlsx with the new columns, the
   Photo Library tab, and the six new rows.
4. Create the six `content/<date-topic>/` folders with briefs.
5. Extend `design/before-after.html` to multi-slide; render the Oct 15 carousel.
6. Render the remaining single-image before/after posts.

Steps 1 and 3–4 need nothing from Cleo. Step 2 gates only the pair-A and
client-G posts; pairs B, C and E can be built immediately.

---

## Open question for Cleo

**Pair D** (`img_1444` / `img_1447`) — which one is the before? I read it as the
opposite of what the old README said, and the change is subtle either way. It is
the only photo decision still outstanding; everything else is unblocked.

## Settled

- **Consent** is on file for clients A and G, conditional on faces being
  covered. That is now a house rule for every result photo, written into
  `design/photos/cleo/README.md`: crop to the treatment area, no eyes, no brows,
  no identifying tattoos or jewellery.
- **All 20 uploads are in use.** Nothing from the original batch was lost — the
  two files in the most recent upload were duplicates of `img_4777` and
  `img_4778`, which were already in the folder.
