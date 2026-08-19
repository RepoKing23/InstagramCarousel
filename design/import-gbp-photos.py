"""Import hand-downloaded Unsplash photos into the daily GBP card pipeline.

    python3 design/import-gbp-photos.py

Reads whatever sits in design/photos/"gbp images" and writes
design/photos/gbp/<photo id>.jpg at 1600x1200, which is the path and size
photo_src() in build-gbp-daily.py already looks for.

The mapping needs no manual table: Unsplash names each download after the slug
that strategy/gbp-photos.json already stores in each photo's "file" field, so
photo-1501812467184-ed92ff087e10.avif is unambiguously Bsg_9a2PDX0. Browser
copies numbered "(1)" are ignored as duplicates.

Re-runnable. Files already imported are skipped unless --force is passed.
"""
import json
import os
import re
import sys

try:                                  # AVIF needs the plugin on most Pillows
    import pillow_avif  # noqa: F401
except ImportError:
    pass
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'design', 'photos', 'gbp images')
OUT = os.path.join(ROOT, 'design', 'photos', 'gbp')
SIZE = (1600, 1200)                   # 4:3, matching the 1200x900 card
SLUG = re.compile(r'^(photo-[0-9a-z-]+?)(?: \(\d+\))?\.\w+$', re.I)


def cover(im, size):
    """Fill the box and centre-crop the overflow, like object-fit: cover."""
    tw, th = size
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    im = im.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    left, top = (im.width - tw) // 2, (im.height - th) // 2
    return im.crop((left, top, left + tw, top + th))


def main(force=False):
    photos = json.load(open(os.path.join(ROOT, 'strategy', 'gbp-photos.json'),
                            encoding='utf-8'))['photos']
    by_slug = {p['file']: p for p in photos}
    os.makedirs(OUT, exist_ok=True)

    if not os.path.isdir(SRC):
        sys.exit(f'no source folder at {SRC}')

    seen, done, skipped, unknown = set(), 0, 0, []
    for name in sorted(os.listdir(SRC)):
        m = SLUG.match(name)
        if not m:
            continue
        slug = m.group(1)
        if slug in seen:              # the "(1)" duplicate of one already taken
            continue
        photo = by_slug.get(slug)
        if not photo:
            unknown.append(name)
            continue
        seen.add(slug)
        dest = os.path.join(OUT, f"{photo['id']}.jpg")
        if os.path.exists(dest) and not force:
            skipped += 1
            continue
        with Image.open(os.path.join(SRC, name)) as im:
            cover(im.convert('RGB'), SIZE).save(dest, quality=86, optimize=True)
        done += 1
        print(f"  {photo['id']:14} {photo['by']:24} {os.path.getsize(dest)//1024:4}KB")

    print(f'\nimported {done}, already had {skipped}, unrecognised {len(unknown)}')
    for n in unknown:
        print(f'  not in gbp-photos.json: {n}')
    missing = [p for p in photos if not os.path.exists(os.path.join(OUT, f"{p['id']}.jpg"))]
    if missing:
        print(f'\n{len(missing)} photos in the manifest have no file yet:')
        for p in missing:
            print(f"  {p['id']:14} {p['alt']}")


if __name__ == '__main__':
    main('--force' in sys.argv)
