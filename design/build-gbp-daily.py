"""Build the daily GBP artwork template and planner sheet from one JSON source.

    python3 design/build-gbp-daily.py

strategy/gbp-daily-content.json is the only file to hand edit. This script
regenerates design/gbp-daily.html from it and rewrites the GBP Daily tab in
strategy/ig-content-strategy.xlsx, keeping whatever Status and Notes are
already typed into that tab. Render the artwork afterwards with

    python3 design/render.py gbp-daily
"""
import json
import os
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, 'strategy', 'gbp-daily-content.json')
TEMPLATE = os.path.join(ROOT, 'design', 'gbp-daily.html')
SHEET = os.path.join(ROOT, 'strategy', 'ig-content-strategy.xlsx')
TAB = 'GBP Daily'
IMG_DIR = 'content/gbp'


def load():
    with open(CONTENT, encoding='utf-8') as f:
        return json.load(f)


def image_path(post):
    """Flat, date-named so the folder reads in posting order."""
    return f"{IMG_DIR}/{post['date']}-{post['slug']}.jpg"


# --- artwork template ------------------------------------------------------

PHOTO_DIR = 'photos/gbp'
UNSPLASH = ('https://images.unsplash.com/{file}'
            '?fm=jpg&q=82&w=1600&h=1200&fit=crop&crop=entropy&cs=tinysrgb')


def photo_src(photo):
    """Prefer a downloaded file, fall back to the Unsplash CDN.

    design/fetch-gbp-photos.py pulls the photos local, which is what you want:
    renders stay identical offline and do not depend on a CDN. Until then the
    card points at Unsplash directly, and if that will not load either the
    layout drops the circle and widens the text rather than leaving a hole.
    """
    local = os.path.join(ROOT, 'design', PHOTO_DIR, f"{photo['id']}.jpg")
    if os.path.exists(local):
        return f"{PHOTO_DIR}/{photo['id']}.jpg"
    return UNSPLASH.format(file=photo['file'])


def markup(text):
    """*asterisks* become the gold emphasis span."""
    out, gold = [], False
    for chunk in text.split('*'):
        out.append(f'<span class="hi">{chunk}</span>' if gold and chunk else chunk)
        gold = not gold
    return ''.join(out)


# Headline and script start at these sizes and are shrunk to fit by the
# template itself. Estimating widths from character counts was never accurate
# enough for Playfair at 800 or for Pinyon's swashes, so the browser measures.
HEADLINE_SIZE = 80
SCRIPT_SIZE = 64


CSS = """
  @font-face { font-family:'Playfair Display'; src:url('fonts/PlayfairDisplay.ttf');
               font-weight:400 900; }
  @font-face { font-family:'Pinyon Script'; src:url('fonts/PinyonScript-Regular.ttf'); }
  @font-face { font-family:'Jost'; src:url('fonts/Jost.ttf'); font-weight:100 900; }

  :root{
    --cream:#F3EEE5; --ink:#2E2A23; --gold:#C9A85C;
    --deep:#1F1C17;                 /* card ground, a shade under brand ink so
                                       cream type and the photo both lift off it */
    --muted:rgba(243,238,229,.72);
  }
  *{margin:0;padding:0;box-sizing:border-box;}
  body{background:#888;}

  /* Maps crops the 1200x900 to the centre 900x900, so every piece of type sits
     inside .safe. Only the photo is allowed into the 150px bleed either side. */
  .slide{
    width:1200px;height:900px;position:relative;overflow:hidden;
    background:var(--deep);color:var(--cream);font-family:'Jost',sans-serif;
  }
  .safe{position:absolute;left:150px;top:0;width:900px;height:900px;}

  /* photo: a circle on the right, only 30px past the safe edge so it still
     reads as a circle after the square crop instead of a cut off blob */
  .orb{
    position:absolute;left:480px;top:225px;width:450px;height:450px;
    border-radius:50%;overflow:hidden;display:none;
    box-shadow:0 0 0 1px rgba(201,168,92,.35);
  }
  .orb img{width:100%;height:100%;object-fit:cover;}
  .orb::after{content:'';position:absolute;inset:0;border-radius:50%;
              background:linear-gradient(180deg,rgba(31,28,23,0) 40%,rgba(31,28,23,.45) 100%);}
  .has-photo .orb{display:block;}

  .col{
    position:absolute;left:14px;top:0;width:446px;height:900px;
    display:flex;flex-direction:column;justify-content:center;
    padding:132px 0 118px;
  }
  /* no photo: the column takes the whole safe square back, but the body keeps a
     readable measure so the block does not collapse to one long line */
  .slide:not(.has-photo) .col{width:900px;padding-right:60px;}
  .slide:not(.has-photo) .body{max-width:620px;}

  .monogram{position:absolute;top:72px;left:14px;}
  .service{
    font-size:21px;font-weight:500;letter-spacing:.2em;text-transform:uppercase;
    color:var(--gold);line-height:1.4;
  }
  .rule{width:46px;height:2px;background:var(--gold);margin:20px 0 24px;}
  .headline{
    font-family:'Playfair Display',serif;font-weight:800;
    text-transform:uppercase;line-height:1.0;letter-spacing:.005em;
    font-size:80px;
  }
  .headline .hi{color:var(--gold);}
  .script{
    /* Pinyon's p, g and j hang well left of their origin. The indent lets the
       swash fall where the headline's left axis is, optically aligned, without
       crossing the Maps crop line at x=150. */
    font-family:'Pinyon Script',cursive;font-size:64px;line-height:.95;
    color:var(--gold);margin-top:6px;padding-left:22px;white-space:nowrap;
  }
  .body{
    margin-top:28px;font-size:22px;font-weight:300;line-height:1.58;
    letter-spacing:.02em;color:var(--muted);
  }
  .cta{
    margin-top:34px;display:inline-block;align-self:flex-start;
    border:1px solid rgba(243,238,229,.8);padding:16px 30px;text-align:center;
  }
  .cta .go{font-size:17px;font-weight:500;letter-spacing:.24em;text-transform:uppercase;}
  .cta .at{
    margin-top:7px;font-size:13px;font-weight:300;letter-spacing:.14em;
    text-transform:uppercase;color:var(--muted);
  }
"""


def build_html(data):
    """One 1200x900 card per date. Hard left column, photo right, dark ground."""
    by_id = {p['id']: p for p in json.load(
        open(os.path.join(ROOT, 'strategy', 'gbp-photos.json'), encoding='utf-8'))['photos']}
    posts = {}
    for p in data['posts']:
        photo = by_id[p['photo']]
        posts[p['date']] = {
            'service': p.get('service', data['_meta']['service_line']),
            'headline': markup(p['headline']),

            'script': p['script'],
            'body': p['body'],
            'cta': p['button'],
            'src': photo_src(photo),
            'alt': photo['alt'],
        }
    first = data['posts'][0]['date']
    handle = data['_meta']['instagram']
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Google Business Profile — daily 1200x900</title>
<!-- Generated by design/build-gbp-daily.py. Edit strategy/gbp-daily-content.json
     and strategy/gbp-photos.json, not this file. Preview with ?date=2026-09-14 -->
<style>{CSS}</style>
</head>
<body>
<div id="stage"></div>

<script>
const HEADLINE_SIZE = {HEADLINE_SIZE}, SCRIPT_SIZE = {SCRIPT_SIZE};
const POSTS = {json.dumps(posts, indent=2, ensure_ascii=False)};

const P = POSTS[new URLSearchParams(location.search).get('date') || '{first}'];

document.getElementById('stage').innerHTML = `
<div class="slide has-photo" id="slide">
  <div class="safe">
    <div class="orb"><img id="photo" src="${{P.src}}" alt="${{P.alt}}"></div>
    <img class="monogram" src="brand/logo-monogram.png" width="68" alt="LB"
         style="filter:brightness(0) invert(1);opacity:.9">
    <div class="col">
      <div class="service">${{P.service}}</div>
      <div class="rule"></div>
      <div class="headline">${{P.headline}}</div>
      <div class="script">${{P.script}}</div>
      <div class="body">${{P.body}}</div>
      <div class="cta">
        <div class="go">${{P.cta}}</div>
        <div class="at">{handle}</div>
      </div>
    </div>
  </div>
</div>`;

// Shrink to fit. A long unbreakable word, or one of Pinyon's trailing swashes,
// overflows the column and would run under the photo circle. Measure and step
// down until it fits, which the estimate from character counts could not do.
function fit(sel, start, floor) {{
  const el = document.querySelector(sel);
  if (!el) return;
  for (let size = start; size > floor; size -= 2) {{
    el.style.fontSize = size + 'px';
    if (el.scrollWidth <= el.clientWidth) return;
  }}
}}
fit('.headline', HEADLINE_SIZE, 40);
fit('.script', SCRIPT_SIZE, 34);

// no photo available: drop the circle, the column takes the full safe square
document.getElementById('photo').addEventListener('error', () => {{
  document.getElementById('slide').classList.remove('has-photo');
}});
</script>
</body>
</html>
"""


# --- planner tab -----------------------------------------------------------

HEADERS = ['Date', 'Day', 'Source', 'Pillar', 'Post Text (short)', 'Chars',
           'Description (long, SEO)', 'Desc Chars', 'CTA Button', 'CTA Link',
           'Image File', 'Open Image', 'Preview', 'Photo Credit', 'Status', 'Notes']


def build_sheet(data):
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill
    from openpyxl.utils import get_column_letter

    meta = data['_meta']
    wb = openpyxl.load_workbook(SHEET)

    # keep anything already typed into Status / Notes before the tab is replaced
    kept = {}
    if TAB in wb.sheetnames:
        old = wb[TAB]
        head = [c.value for c in old[1]]
        if 'Date' in head:
            di = head.index('Date')
            si = head.index('Status') if 'Status' in head else None
            ni = head.index('Notes') if 'Notes' in head else None
            for row in old.iter_rows(min_row=2, values_only=True):
                key = row[di]
                key = key.strftime('%Y-%m-%d') if hasattr(key, 'strftime') else str(key)
                kept[key] = (row[si] if si is not None else None,
                             row[ni] if ni is not None else None)
        del wb[TAB]

    ws = wb.create_sheet(TAB, wb.sheetnames.index('Posting Schedule') + 1)

    ink = Font(name='Calibri', size=11)
    ws.append(HEADERS)
    for c in ws[1]:
        c.font = Font(bold=True, color='FFFFFF')
        c.fill = PatternFill('solid', fgColor='2E2A23')
        c.alignment = Alignment(vertical='center')
    ws.freeze_panes = 'C2'

    raw = f"https://raw.githubusercontent.com/RepoKing23/InstagramCarousel/{meta['branch']}/"
    by_id = {q['id']: q for q in json.load(
        open(os.path.join(ROOT, 'strategy', 'gbp-photos.json'), encoding='utf-8'))['photos']}

    for p in data['posts']:
        img = image_path(p)
        photo = by_id[p['photo']]
        status, notes = kept.get(p['date'], (None, None))
        ws.append([
            datetime.datetime.strptime(p['date'], '%Y-%m-%d'),
            p['day'], p['source'], p['pillar'], p['text'], len(p['text']),
            p['description'], len(p['description']),
            meta['cta_button'], meta['instagram_url'], img.split('/')[-1],
            'Open image', f'=IMAGE("{raw}{img}")',
            f"{photo['by']} / Unsplash", status or 'Ready', notes or '',
        ])
        r = ws.max_row
        ws.cell(r, 1).number_format = 'yyyy-mm-dd'
        link = ws.cell(r, HEADERS.index('CTA Link') + 1)
        link.hyperlink = meta['instagram_url']
        link.value = meta['instagram']
        link.style = 'Hyperlink'
        # links straight at the jpg, so it opens ready to save and post
        im = ws.cell(r, HEADERS.index('Open Image') + 1)
        im.hyperlink = f'{raw}{img}'
        im.style = 'Hyperlink'
        cr = ws.cell(r, HEADERS.index('Photo Credit') + 1)
        cr.hyperlink = f"https://unsplash.com/photos/{photo['id']}"
        cr.style = 'Hyperlink'
        for col in ('Post Text (short)', 'Description (long, SEO)', 'Notes'):
            ws.cell(r, HEADERS.index(col) + 1).alignment = Alignment(wrap_text=True, vertical='top')
        # Sunday and Wednesday have no Instagram post behind them
        if p['source'] == 'GBP only':
            for c in ws[r]:
                c.fill = PatternFill('solid', fgColor='F3EEE5')
        for c in ws[r]:
            if not c.font.bold:
                c.font = ink

    widths = {'A': 12, 'B': 6, 'C': 32, 'D': 17, 'E': 54, 'F': 7, 'G': 96, 'H': 8,
              'I': 12, 'J': 26, 'K': 32, 'L': 13, 'M': 14, 'N': 24, 'O': 10, 'P': 28}
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    for r in range(2, ws.max_row + 1):
        ws.row_dimensions[r].height = 132

    wb.save(SHEET)
    return ws.max_row - 1


def main():
    data = load()
    with open(TEMPLATE, 'w', encoding='utf-8') as f:
        f.write(build_html(data))
    print(f'wrote {os.path.relpath(TEMPLATE, ROOT)}  ({len(data["posts"])} days)')
    n = build_sheet(data)
    print(f'wrote "{TAB}" tab in {os.path.relpath(SHEET, ROOT)}  ({n} rows)')


if __name__ == '__main__':
    main()
