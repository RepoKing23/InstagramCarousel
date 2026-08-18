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
    template drops back to the cream layout rather than rendering a hole.
    """
    local = os.path.join(ROOT, 'design', PHOTO_DIR, f"{photo['id']}.jpg")
    if os.path.exists(local):
        return f"{PHOTO_DIR}/{photo['id']}.jpg"
    return UNSPLASH.format(file=photo['file'])


CSS = """
  @font-face { font-family:'Playfair Display'; src:url('fonts/PlayfairDisplay.ttf'); }
  @font-face { font-family:'Pinyon Script'; src:url('fonts/PinyonScript-Regular.ttf'); }
  @font-face { font-family:'Jost'; src:url('fonts/Jost.ttf'); }

  :root{ --cream:#F3EEE5; --ink:#2E2A23; --ink-soft:#6E6557; --gold:#C9A85C; }
  *{margin:0;padding:0;box-sizing:border-box;}
  body{background:#888;}

  /* GBP serves 1200x900 but crops to a centre square in Maps and the Knowledge
     Panel, so every piece of type lives inside the middle 900x900. The photo is
     allowed to bleed the full width, only the words are constrained. */
  .slide{
    width:1200px;height:900px;position:relative;overflow:hidden;
    background:var(--cream);color:var(--ink);font-family:'Jost',sans-serif;
  }
  .photo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:none;}
  .scrim{position:absolute;inset:0;display:none;}
  /* .has-photo is dropped by the onerror handler if the image will not load,
     which returns the card to the plain cream layout instead of a blank frame */
  .has-photo .photo{display:block;}
  .has-photo .scrim{
    display:block;
    background:
      radial-gradient(120% 85% at 50% 50%, rgba(24,21,17,.78) 0%, rgba(24,21,17,.62) 45%, rgba(24,21,17,.72) 100%),
      linear-gradient(180deg, rgba(24,21,17,.55) 0%, rgba(24,21,17,.25) 35%, rgba(24,21,17,.65) 100%);
  }
  .has-photo{color:var(--cream);}
  .has-photo .label,.has-photo .body,.has-photo .handle{color:rgba(243,238,229,.86);}
  .has-photo .button{border-color:rgba(243,238,229,.85);color:var(--cream);}
  .has-photo .monogram{filter:brightness(0) invert(1);opacity:.92;}
  .has-photo .rule{background:var(--gold);}

  .safe{
    position:absolute;left:150px;top:0;width:900px;height:900px;
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    text-align:center;padding:118px 62px 96px;
  }
  .monogram{position:absolute;top:46px;left:50%;transform:translateX(-50%);z-index:3;}
  .label{font-size:19px;letter-spacing:.36em;text-transform:uppercase;color:var(--ink-soft);}
  .rule{width:54px;height:1px;background:var(--gold);margin:22px auto 0;opacity:.9;}
  .serif{font-family:'Playfair Display',serif;font-weight:500;font-size:70px;line-height:1.04;}
  .script{font-family:'Pinyon Script',cursive;font-size:66px;line-height:.95;margin-top:4px;}
  .body{margin-top:30px;font-size:25px;line-height:1.58;letter-spacing:.05em;color:var(--ink-soft);}
  .button{
    margin-top:38px;border:1px solid var(--ink);padding:19px 40px;
    font-size:19px;letter-spacing:.28em;text-transform:uppercase;font-weight:500;
  }
  .handle{
    position:absolute;bottom:40px;left:0;right:0;text-align:center;z-index:3;
    font-size:17px;letter-spacing:.22em;text-transform:uppercase;
    color:var(--ink-soft);font-weight:300;
  }
"""


def build_html(data):
    """One 1200x900 card per date, photo led, same brand as the rest."""
    by_id = {p['id']: p for p in json.load(
        open(os.path.join(ROOT, 'strategy', 'gbp-photos.json'), encoding='utf-8'))['photos']}
    posts = {}
    for p in data['posts']:
        photo = by_id[p['photo']]
        posts[p['date']] = {k: p[k] for k in ('label', 'serif', 'script', 'body', 'button')}
        posts[p['date']]['src'] = photo_src(photo)
        posts[p['date']]['alt'] = photo['alt']
    first = data['posts'][0]['date']
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
const POSTS = {json.dumps(posts, indent=2, ensure_ascii=False)};

const P = POSTS[new URLSearchParams(location.search).get('date') || '{first}'];

document.getElementById('stage').innerHTML = `
<div class="slide has-photo" id="slide">
  <img class="photo" id="photo" src="${{P.src}}" alt="${{P.alt}}">
  <div class="scrim"></div>
  <img class="monogram" src="brand/logo-monogram.png" width="76" alt="LB">
  <div class="safe">
    <div class="label">${{P.label}}</div>
    <div class="rule"></div>
    <div style="margin-top:22px">
      <div class="serif">${{P.serif}}</div>
      <div class="script">${{P.script}}</div>
    </div>
    <div class="body">${{P.body}}</div>
    <div class="button">${{P.button}}</div>
  </div>
  <div class="handle">@luxury_beauty_aestheticz</div>
</div>`;

// no photo available: fall back to the cream card rather than a blank frame
document.getElementById('photo').addEventListener('error', () => {{
  document.getElementById('slide').classList.remove('has-photo');
}});
</script>
</body>
</html>
"""


# --- planner tab -----------------------------------------------------------

HEADERS = ['Date', 'Day', 'Source', 'Pillar', 'Post Text (first 80 chars show)',
           'Chars', 'CTA Button', 'CTA Link', 'Image File', 'Open Image', 'Preview',
           'Photo Credit', 'Status', 'Notes']


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
        for col in ('Post Text (first 80 chars show)', 'Notes'):
            ws.cell(r, HEADERS.index(col) + 1).alignment = Alignment(wrap_text=True, vertical='top')
        # Sunday and Wednesday have no Instagram post behind them
        if p['source'] == 'GBP only':
            for c in ws[r]:
                c.fill = PatternFill('solid', fgColor='F3EEE5')
        for c in ws[r]:
            if not c.font.bold:
                c.font = ink

    widths = {'A': 12, 'B': 6, 'C': 34, 'D': 18, 'E': 78, 'F': 7, 'G': 12,
              'H': 26, 'I': 34, 'J': 13, 'K': 14, 'L': 24, 'M': 10, 'N': 30}
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    for r in range(2, ws.max_row + 1):
        ws.row_dimensions[r].height = 58

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
