# Google Business Profile — Daily Posting Plan

Aug 19 to Sep 30, 2026. One post every day, 43 in total, each with its own
1200x900 image and a Learn more button pointed at Instagram.

## Why daily

The Instagram plan posts five days a week: Monday, Tuesday, Thursday, Friday,
Saturday. Google Business Profile rewards a different thing than Instagram
does. Posts feed the Maps and Search panel, they are what someone sees when
they look up the clinic before booking, and a profile that posts every day
reads as open and active to both the visitor and the ranking. So this calendar
fills all seven days.

- **30 days** carry the same message as that day's Instagram post, rewritten
  for a Google audience. Someone who finds the clinic on Maps has never seen
  the grid, so the copy stands alone and does not say "swipe" or "link in bio".
- **13 days** are Wednesdays and Sundays, which have no Instagram post behind
  them. These are evergreen: location, credentials, what a consult includes,
  aftercare, safety, what to ask before booking anywhere. They are shaded in
  the planner tab. Reorder or reuse them freely, nothing dates them.

## Where everything lives

| What | Where |
| --- | --- |
| The calendar you post from | `GBP Daily` tab in `strategy/ig-content-strategy.xlsx` |
| The 43 images | `content/gbp/`, named `YYYY-MM-DD-slug.jpg` |
| The copy, as source | `strategy/gbp-daily-content.json` |
| The photo picked for each day | `strategy/gbp-photos.json` |
| The artwork template | `design/gbp-daily.html` |

The folder is flat and date-named on purpose. Sort by name and it reads in
posting order, so the morning routine is: open `content/gbp`, take today's
date, done.

## The photos, and the one step left to run

Each day is matched to a specific Unsplash photo, hand picked for that day's
subject. The card is the photo full bleed, dimmed under a warm scrim, with the
brand type over it.

**The photos are not in the repo yet.** The session that built this could not
reach `images.unsplash.com`, so the artwork currently in `content/gbp/` is the
cream fallback rather than the photo version. One command fixes it on any
machine with normal internet:

    python3 design/fetch-gbp-photos.py     # pulls the 36 photos
    python3 design/build-gbp-daily.py      # switch the cards to local files
    python3 design/render.py gbp-daily     # re-render all 43

If the fetch is blocked for you too, the Photo Credit column in the planner
links to each photo. Download them by hand, save each as
`design/photos/gbp/<photo id>.jpg`, then run the last two commands.

The template checks for a local file first and only falls back to the Unsplash
CDN, so once the photos are on disk the renders are reproducible offline. If a
photo will not load at all, the card falls back to the cream layout rather than
rendering a blank frame, which is why nothing is broken right now.

### About the photos

They are Unsplash License: free for commercial use, no permission needed, no
attribution required. The photographer and a link are recorded anyway, in
`strategy/gbp-photos.json` and in the Photo Credit column.

**These are stock models, not clients of the clinic.** Keep it that way in the
captions. None of this copy claims a photo is a result, and none of it should:
that is the line between an illustrated post and an implied before and after.
Real client work stays in `design/photos/cleo/crops/` under the consent rules
in the design README.

Thirty six photos cover forty three days, so seven repeat. The closest repeat is
22 days apart, which is far enough that it does not read as a repeat in the feed.

## Posting a day, start to finish

1. Open the `GBP Daily` tab and find today's row.
2. Click Open Image, which opens that day's jpg ready to save. Or take it
   straight from `content/gbp/`.
3. In Google Business Profile choose **Add update**.
4. Paste the Post Text column. Do not add hashtags, they do nothing on GBP.
5. Set the button to **Learn more** and paste the CTA link, the Instagram
   profile.
6. Mark the row Posted.

## Rules baked into the copy

- **First 80 characters carry it.** GBP truncates to roughly 80 characters
  behind a Read more, so every post front-loads the point. The Chars column
  shows total length. All 43 sit between 178 and 248, well under the 1500 limit
  and long enough to say something.
- **No hashtags.** They are inert on GBP.
- **Nothing in the bleed.** Maps crops the 1200x900 to a centre square, so all
  type sits inside the middle 900x900. Every card is checked against this.
- **The button always goes to Instagram.** GBP has no Instagram button, so the
  Learn more URL is the profile. Swap it in `strategy/gbp-daily-content.json`
  once a booking page exists, then rebuild.
- **Voice.** Plain, direct, first person. No em dashes, no sparkle emoji.

## Changing something

Edit `strategy/gbp-daily-content.json` for copy, or the `photo` key on a day to
swap its image for another id in `strategy/gbp-photos.json`. Never edit the
generated files. Then:

    python3 design/build-gbp-daily.py    # rebuilds the template and the tab
    python3 design/render.py gbp-daily   # re-renders the 43 images

The rebuild keeps whatever you have typed into the Status and Notes columns,
matched by date, so tracking survives a copy change.

Preview one day in a browser without rendering anything:
`design/gbp-daily.html?date=2026-09-14`.

## One thing to check before posting

The house rules in this workbook flag that Health Canada restricts consumer
advertising of prescription drugs, and name "neuromodulator" as the safe swap
for the brand name. This calendar uses the brand name, as confirmed. It is
worth a compliance read before the first post, because Google Business Profile
is a public and indexed surface. The swap is a find and replace in the json
followed by a rebuild.
