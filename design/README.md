# Editorial Carousel Design System

Soft editorial style for @luxury_beauty_aestheticz: cream/beige palette,
Playfair Display serif + Pinyon Script accents + Jost letterspaced labels.

## Files
- `botox-myths.html` — "5 Botox Lies You Still Believe" carousel (8 slides)
- `slides.html` — "Still You, Just Refreshed" carousel (6 slides)
- `before-after.html` — before/after result cards, one per client pair (4 slides)
- `real-results.html` — "Real Lips. Real Results." carousel (6 slides)
- `every-angle.html` — "One Result, Every Angle" carousel (7 slides)
- `fonts/` — Playfair Display, Pinyon Script, Jost (all SIL Open Font License)
- `brand/` — Luxury Beauty by Cleo R logo (full lockup, tight crop, monogram; transparent PNGs)
- `photos/<carousel-name>/` — working photos used by each carousel template
- `photos/cleo/crops/` — client photos cropped to the treatment area. **Result
  posts use these, never the originals**, so no face ends up in a published
  file. Regenerate with the crop boxes documented in `photos/cleo/README.md`.

Final ready-to-post images live in `/content/<date-topic>/` at the repo root:
one folder per scheduled post, each with a `brief.md` (hook, caption, hashtags,
visual notes) generated from `/strategy/ig-content-strategy.xlsx`. The
spreadsheet's Folder Link column points at each post's folder.

## Previewing a slide in a browser
Open the HTML file with `?slide=N` in the URL (e.g. `botox-myths.html?slide=3`).

## Re-rendering PNGs (headless Chromium)
The `.slide.active` class controls which slide is shown. Generate one HTML
file per slide with the `active` class set, then screenshot at window size
1080x1437 (headless window chrome eats 87px) and crop to 1080x1350.

Photo placeholders ("YOUR PHOTO HERE") are swapped by replacing the
`.photo` div contents with an `<img>` styled `object-fit:cover`.

## Design assignment

Each post's `content/<date-topic>/brief.md` carries a Design section that names
the style to build. It defaults to the editorial house style above. To give a
specific post a different look, edit that section (or drop an inspiration image
in the post's folder) and ask Claude to design from the brief. New styles get
their own template file in this directory so they stay reusable.

## Grid tone rhythm (light / dark)

The profile grid shows three tiles per row, newest first. House rule: **exactly
one Dark or dark-photo tile per row of three, and never two Dark tiles side by
side.** Cream is the base; the dark tiles are what stop the grid reading as one
beige block.

- `single.html` and `carousel.html` posts flip with `theme:'dark'` in their
  POSTS entry — one line and a re-render, not a redesign.
- The Tone column in the planner (Light / Dark / Photo) tracks this per post.
  Check it when moving dates: swapping two posts can put two Dark tiles
  together.
- August is balanced (dark tiles: Aug 21, 25, 28). September onward is all
  Light until designed — assign roughly one Dark per week.
- If the black and gold before/after style is used for Aug 22, flip Aug 21 back
  to light or the row becomes dark-dark-cream.
