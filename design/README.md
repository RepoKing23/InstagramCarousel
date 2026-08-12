# Editorial Carousel Design System

Soft editorial style for @luxury_beauty_aestheticz: cream/beige palette,
Playfair Display serif + Pinyon Script accents + Jost letterspaced labels.

## Files
- `botox-myths.html` — "5 Botox Lies You Still Believe" carousel (8 slides)
- `slides.html` — "Still You, Just Refreshed" carousel (6 slides)
- `fonts/` — Playfair Display, Pinyon Script, Jost (all SIL Open Font License)
- `brand/` — Luxury Beauty by Cleo R logo (full lockup, tight crop, monogram; transparent PNGs)
- `photos/<carousel-name>/` — working photos used by each carousel template

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
