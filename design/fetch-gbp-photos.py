"""Download the Unsplash photos used by the daily GBP cards.

    python3 design/fetch-gbp-photos.py

Saves each photo to design/photos/gbp/<id>.jpg at 1600x1200. Once they are on
disk, rebuild and re-render so the cards use the local files:

    python3 design/build-gbp-daily.py
    python3 design/render.py gbp-daily

Skips anything already downloaded, so it is safe to re-run. All photos are
Unsplash License: free for commercial use, no permission needed. Photographer
credits live in strategy/gbp-photos.json and in the planner tab.
"""
import json
import os
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, 'strategy', 'gbp-photos.json')
OUT = os.path.join(ROOT, 'design', 'photos', 'gbp')
# 4:3 to match the 1200x900 card, downloaded a little over size for crisp text
PARAMS = 'fm=jpg&q=82&w=1600&h=1200&fit=crop&crop=entropy&cs=tinysrgb'


def url_for(photo):
    return f"https://images.unsplash.com/{photo['file']}?{PARAMS}"


def main():
    os.makedirs(OUT, exist_ok=True)
    photos = json.load(open(MANIFEST, encoding='utf-8'))['photos']
    ok = skip = 0
    failed = []
    for p in photos:
        dest = os.path.join(OUT, f"{p['id']}.jpg")
        if os.path.exists(dest) and os.path.getsize(dest) > 50_000:
            skip += 1
            continue
        for attempt in range(4):
            try:
                req = urllib.request.Request(url_for(p), headers={'User-Agent': 'Mozilla/5.0'})
                data = urllib.request.urlopen(req, timeout=60).read()
                if len(data) < 20_000:
                    raise ValueError(f'suspiciously small: {len(data)} bytes')
                with open(dest, 'wb') as f:
                    f.write(data)
                ok += 1
                print(f"  {p['id']}  {len(data)//1024}KB  {p['by']}")
                break
            except Exception as exc:
                if attempt == 3:
                    failed.append((p['id'], exc))
                else:
                    time.sleep(2 ** attempt)

    print(f'\ndownloaded {ok}, already had {skip}, failed {len(failed)}')
    for pid, exc in failed:
        print(f'  FAILED {pid}: {exc}')
    if failed:
        print('\nIf every one failed with 403, the network blocks images.unsplash.com.'
              '\nDownload them by hand from the Photo Credit links in the GBP Daily tab'
              f'\nand save each as {os.path.relpath(OUT, ROOT)}/<photo id>.jpg')


if __name__ == '__main__':
    main()
