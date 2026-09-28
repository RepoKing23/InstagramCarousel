"""Find and download a fresh Unsplash photo for every Oct and Nov post.

    python3 design/fetch-octnov-photos.py              # fill every empty slot
    python3 design/fetch-octnov-photos.py --redo 2026-10-06-ig 2026-10-06-gbp
    python3 design/build-octnov.py && python3 design/render.py octnov

Two slots per post: <date>-ig (the Instagram cover, 1080x1350 portrait) and
<date>-gbp (the Google Business card, 1600x1200 landscape). Result posts use
real client photos, so they only get a GBP slot.

Each slot searches Unsplash with the phrase in that post's "photo" entry in
strategy/plan-*.json and takes the first result that:
  - is free under the Unsplash License (Unsplash+ photos are skipped)
  - is not already in strategy/gbp-photos.json, so nothing from Aug or Sep repeats
  - has not been picked for any other slot, so nothing repeats inside Oct and Nov
  - has not been rejected with --redo
  - does not describe product packaging, which the cards never show

Picks are recorded in strategy/octnov-photos.json with the photographer, and a
contact sheet is written to design/photos/octnov/contact-sheet.html so the
whole set can be checked by eye before posting. To swap one, run --redo with
its slot name; the old photo is remembered as rejected. To force a specific
photo, put its Unsplash id in the plan, e.g. "photo": {"ig_id": "abc123", ...}.

Needs network access to unsplash.com and images.unsplash.com.
"""
import glob
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PICKS = os.path.join(ROOT, 'strategy', 'octnov-photos.json')
GBP_PHOTOS = os.path.join(ROOT, 'strategy', 'gbp-photos.json')
IG_DIR = os.path.join(ROOT, 'design', 'photos', 'octnov')
GBP_DIR = os.path.join(ROOT, 'design', 'photos', 'gbp')

SEARCH = 'https://unsplash.com/napi/search/photos?{}'
PHOTO = 'https://unsplash.com/napi/photos/{}'
IMG = ('https://images.unsplash.com/{file}?fm=jpg&q=82&w={w}&h={h}'
       '&fit=crop&crop=faces,entropy&cs=tinysrgb')
SIZES = {'ig': (1080, 1350, 'portrait'), 'gbp': (1600, 1200, 'landscape')}

# Words in a photo's own description that mean it is not right for these cards
BANNED = ('bottle', 'packaging', 'package', 'jar', 'tube', 'product', 'brand',
          'label', 'serum', 'dropper', 'syringe', 'needle', 'blood', 'surgery',
          'nude', 'naked', 'topless', 'shirtless', 'lingerie', 'bikini', 'underwear',
          'cigarette', 'smoking', 'alcohol', 'wine', 'beer', 'text', 'logo')

HEADERS = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}


def get(url, binary=False):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            data = urllib.request.urlopen(req, timeout=60).read()
            return data if binary else json.loads(data)
        except Exception as exc:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)


def plan():
    posts = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'strategy', 'plan-*.json'))):
        posts += json.load(open(f, encoding='utf-8'))['posts']
    return sorted(posts, key=lambda p: p['date'])


def slots(posts):
    for p in posts:
        ph = p.get('photo', {})
        if p['kind'] in ('carousel', 'single') and not p.get('cover_file') and ph.get('ig'):
            yield f"{p['date']}-ig", 'ig', ph['ig'], ph.get('ig_id'), p
        if ph.get('gbp'):
            yield f"{p['date']}-gbp", 'gbp', ph['gbp'], ph.get('gbp_id'), p


def file_of(photo):
    """The images.unsplash.com path, e.g. photo-1570172619644-dfd03ed5d881."""
    raw = photo['urls']['raw']
    return urllib.parse.urlparse(raw).path.strip('/')


def acceptable(photo, used):
    if photo['id'] in used or photo.get('premium') or photo.get('plus'):
        return False
    words = ' '.join(filter(None, [photo.get('alt_description'), photo.get('description')])).lower()
    return not any(b in words for b in BANNED)


def record(photo, query):
    return {'id': photo['id'], 'by': photo['user']['name'], 'user': photo['user']['username'],
            'alt': photo.get('alt_description') or '', 'file': file_of(photo), 'query': query}


def dest(kind, slot, pick):
    if kind == 'ig':
        return os.path.join(IG_DIR, f'{slot}.jpg')
    return os.path.join(GBP_DIR, f"{pick['id']}.jpg")


def main(argv):
    redo = set(argv[argv.index('--redo') + 1:]) if '--redo' in argv else set()
    store = json.load(open(PICKS, encoding='utf-8')) if os.path.exists(PICKS) else {
        '_meta': {'license': 'Unsplash License. Free for commercial use. Stock models, never '
                             'presented as clients.', 'rejected': []}, 'picks': {}}
    picks, rejected = store['picks'], set(store['_meta'].get('rejected', []))
    for slot in redo:
        if slot in picks:
            rejected.add(picks.pop(slot)['id'])
    earlier = {p['id'] for p in json.load(open(GBP_PHOTOS, encoding='utf-8'))['photos']}
    os.makedirs(IG_DIR, exist_ok=True)
    os.makedirs(GBP_DIR, exist_ok=True)

    got = failed = 0
    for slot, kind, query, forced, post in slots(plan()):
        pick = picks.get(slot)
        if pick and os.path.exists(dest(kind, slot, pick)):
            continue
        # everything already used anywhere, except this slot's own pick
        used = earlier | rejected | {v['id'] for k, v in picks.items() if k != slot}
        try:
            if not pick:
                if forced:
                    pick = record(get(PHOTO.format(forced)), f'id:{forced}')
                else:
                    w, h, orient = SIZES[kind]
                    q = urllib.parse.urlencode({'query': query, 'per_page': 30,
                                                'orientation': orient})
                    found = [ph for ph in get(SEARCH.format(q))['results'] if acceptable(ph, used)]
                    if not found:
                        print(f'  {slot}: nothing unused for "{query}". Edit the phrase in the plan.')
                        failed += 1
                        continue
                    pick = record(found[0], query)
            w, h, _ = SIZES[kind]
            data = get(IMG.format(file=pick['file'], w=w, h=h), binary=True)
            if len(data) < 20_000:
                raise ValueError(f'suspiciously small: {len(data)} bytes')
            with open(dest(kind, slot, pick), 'wb') as f:
                f.write(data)
            picks[slot] = pick
            got += 1
            print(f"  {slot:16} {pick['id']:12} {pick['by'][:24]:24} {pick['alt'][:50]}")
        except Exception as exc:
            failed += 1
            print(f'  {slot}: FAILED {exc}')
            if 'Tunnel' in str(exc) or '403' in str(exc):
                print('\nunsplash.com is blocked from this machine. Allow unsplash.com and '
                      'images.unsplash.com in the environment network settings.')
                break
        store['_meta']['rejected'] = sorted(rejected)
        with open(PICKS, 'w', encoding='utf-8') as f:
            json.dump(store, f, indent=2, ensure_ascii=False)
            f.write('\n')

    if picks:
        contact_sheet(picks)
    ids = [v['id'] for v in picks.values()]
    assert len(ids) == len(set(ids)), 'a photo was picked twice'
    print(f'\ndownloaded {got}, failed {failed}, {len(picks)} slots filled')
    print('next: python3 design/build-octnov.py && python3 design/render.py octnov')


def contact_sheet(picks):
    cells = []
    for slot in sorted(picks):
        p = picks[slot]
        src = (f'{slot}.jpg' if slot.endswith('-ig') else f"../gbp/{p['id']}.jpg")
        cells.append(f'<figure><img src="{src}" loading="lazy"><figcaption><b>{slot}</b><br>'
                     f'{p["by"]} &middot; <a href="https://unsplash.com/photos/{p["id"]}">'
                     f'{p["id"]}</a><br><i>{p["query"]}</i></figcaption></figure>')
    with open(os.path.join(IG_DIR, 'contact-sheet.html'), 'w', encoding='utf-8') as f:
        f.write('<!doctype html><meta charset="utf-8"><title>Oct and Nov photos</title>'
                '<style>body{font:13px system-ui;margin:16px;background:#f3eee5}'
                'main{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}'
                'img{width:100%;height:220px;object-fit:cover;display:block}'
                'figure{margin:0;background:#fff;padding:6px}</style>'
                f'<h1>Oct and Nov photos ({len(picks)})</h1><main>{"".join(cells)}</main>')


if __name__ == '__main__':
    main(sys.argv[1:])
