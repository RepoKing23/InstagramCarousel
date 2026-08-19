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

**The photos are in.** They were downloaded by hand and committed to
`design/photos/gbp images/` as AVIF, then imported with

    python3 design/import-gbp-photos.py    # AVIF in, design/photos/gbp/<id>.jpg out

which maps each file to its photo by the Unsplash slug in the filename, so no
manual table is needed. All 43 cards now render with real photography.

`design/fetch-gbp-photos.py` remains for anyone re-pulling from Unsplash
directly. The template still prefers a local file and falls back to the CDN, and
if neither loads the photo panel renders as a tonal block rather than a hole.

### About the photos

They are Unsplash License: free for commercial use, no permission needed, no
attribution required. The photographer and a link are recorded anyway, in
`strategy/gbp-photos.json` and in the Photo Credit column.

**These are stock models, not clients of the clinic.** Keep it that way in the
captions. None of this copy claims a photo is a result, and none of it should:
that is the line between an illustrated post and an implied before and after.
Real client work stays in `design/photos/cleo/crops/` under the consent rules
in the design README.

**No product packaging, ever.** Thirteen of the original picks were retired for
this reason: nine product still lifes, plus two shots where branded packaging is
legible in frame, and two more that were simply wrong for a clinic, a shocked
open-mouth expression and a bare-shouldered portrait. Anything showing a branded
tube, bottle or box does not go on these cards.

Twenty three photos cover forty three days, so sixteen repeat. The closest
repeat is six days apart. If that feels tight, adding a handful more non-product
photos to `design/photos/gbp images/` and re-running the importer widens it.

## Posting a day, start to finish

1. Open the `GBP Daily` tab and find today's row.
2. Click Open Image, which opens that day's jpg ready to save. Or take it
   straight from `content/gbp/`.
3. In Google Business Profile choose **Add update**.
4. Paste the Post Text column. Do not add hashtags, they do nothing on GBP.
5. Set the button to **Learn more** and paste the CTA link, the Instagram
   profile.
6. Mark the row Posted.

## The card design

Dark ground, hard left column, circular photo on the right, in the brand's own
fonts. Each card carries, top to bottom:

- **Service line** in gold, the SEO line. `BOTOX & DERMAL FILLER · OAKVILLE` by
  default, from `_meta.service_line`, overridden per day only where the topic is
  plainly another service (lip filler, preventative). Naming the service and the
  city on every card is the part search actually rewards.
- **Headline** in Playfair Display at weight 800, uppercase. The first word is
  gold and the rest cream, which is where the two tone comes from. Mark emphasis
  in the json with `*asterisks*` if you want it somewhere else.
- **Script line** in Pinyon, gold.
- **Body**, two lines.
- **CTA block**, outlined, with the day's action over the Instagram handle. The
  image itself is not clickable; the real link is still the GBP Learn more
  button, already pointed at the profile. The handle is there so someone can
  find you without pressing anything.

Headline and script **shrink to fit**. A long word cannot wrap and Pinyon's
swashes run long, so the template measures each one in the browser and steps the
size down until it clears the photo. Nothing to tune by hand when you rewrite a
headline.

Two invariants are checked on every render, and both matter because Maps crops
the 1200x900 to its centre square: no type may cross the crop line at x=150, and
no type may run under the photo circle.

## Two lengths of copy per day

Each day carries both, and you pick per post:

- **Post Text** is the short version, 178 to 248 characters. Good when you just
  want the day up.
- **Description** is the long form body, 598 to 885 characters. This is the one
  written for search, and the one to use on the days that matter.

Every description names a service, 32 of the 43 name Oakville or a nearby city,
and all 43 end pointing at Instagram. Keyword density stays under 3 percent
because stuffing is what actually costs you a content score, not helps it.

They are written to avoid reading like a machine wrote them: no em dashes, no
"elevate", "delve", "unlock" or "seamless", no three item lists used as
decoration. Sentence length runs from 2 words to 41 and averages 13, because
uniform sentence length is the clearest tell. The specifics are real ones from
your own practice, the 45 minute first visit, the ten minute treatment, the two
week follow up, RN(EC), 3060 Preserve Dr.

If you run these through a content scoring tool, the levers it will want are
already pulled: keyword in the opening sentence, service and locality present,
adequate length, varied readability, a clear call to action. The one thing no
writing can fix from here is search volume data for your specific terms, which
needs a live keyword tool.

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
