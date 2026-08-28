# Reels & Video Weekly Routine — Weeks 2 to 24

Companion to the **Luxury Beauty by Cleo R** content plan spreadsheet. This adds a
recurring video and image production routine on top of the existing feed calendar.

**Nothing in the existing Content Calendar tab is changed.** All 65 rows there already
carry a status (Done, Ready, Scheduled, Design, Idea), so the routine is delivered as a
separate tab that starts at Week 2 and runs to Week 24.

## The routine

Three create-and-post actions every week, on the two days the feed calendar leaves open
plus a Friday paid/boost slot:

| Slot | Day | What | Why this day |
| :-- | :-- | :-- | :-- |
| Slot 1 | Wednesday | Reel (video) | Wednesday is empty in the feed calendar |
| Slot 2 | Friday | Image post or paid ad creative | Pairs with the existing Friday image post — Weeks 2–13 this is the boosted/ad version, Weeks 14–24 it is a fresh image post |
| Slot 3 | Sunday | Reel (video) | Sunday is empty in the feed calendar |

Weeks 2 to 24 = 23 weeks × 3 = **69 items**. Week 2 starts Aug 26, 2026 and Week 24 ends
Jan 31, 2027, which is month 6 of the plan.

## Already posted

Six items that went out between Aug 17 and Aug 28 are logged in the same tab, merged into the
plan in date order so it reads as one chronological record. They carry Slot `Posted - Reel`,
`Posted - Carousel` or `Posted - Image`, and a bold `Posted` status you can filter on. Captions
are recorded exactly as supplied; production columns (shot list, on-screen text, audio, asset to
create) are blank, because these are finished posts rather than briefs.

They already run at three a week: Aug 17, 18, 20, then Aug 24, 27, 28.

Two of them drifted from Posting Schedule and the Notes column says so. The `5 Botox Lies`
carousel was planned for Aug 17 but ran on Aug 18, and Aug 17 instead carried a lip-enhancement
before/after that is not on the schedule at all.

## What each row carries

Week, Date, Day, Slot, Month Theme, Format, Platforms, Pillar, Topic & Hook,
Hook (first 3 sec), Script / Shot List, On-screen Text, Caption Draft, CTA, Hashtag Set,
Audio / Style / Ad Spend, Asset to Create, Source Assets & Notes, Filmed, Edited, Status,
Posted Link, Views, Saves, Shares, DMs, Bookings.

Hashtag sets are the same A–E sets already in the spreadsheet. Statuses use the same
vocabulary as the main calendar and every new row starts at `Idea`.

## Month themes added past Nov 15

The existing plan stops at Nov 15, 2026. Three new themes carry it to month 6:

| Period | Theme | Goal |
| :-- | :-- | :-- |
| Nov 16–30, 2026 | Gift Season Opens | Launch gift certificates and take the Black Friday position on honest pricing |
| December 2026 | Glow Into the New Year | Party-season urgency, then the quiet late-December booking window |
| January 2027 | New Year, Real Results | Price transparency, men's treatments, and the six-month proof post |

## Reuse and consent

Roughly half the routine repurposes work that already exists — carousels from the feed
calendar become 30-second talking-head reels, and the Photo Library pairs become
before/after video sequences. Rows name the exact source asset.

Every row using client photos names the pair and its consent state from the Photo Library
tab. Pair D stays out of the routine while its direction is unconfirmed. The Jan 24 row
(*Three Sessions, One Client*) needs **new** client consent and photos captured over time —
confirm that before filming.

Before running the Oct 30 before/after as a paid ad, check the current Meta advertising
policy on before/after imagery for cosmetic treatments.

## Regenerating

```
python3 strategy/build-reels-routine.py
```

Writes `strategy/reels-video-weekly-routine-w2-w24.csv`.
