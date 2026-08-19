"""Render post artwork to JPEG with headless Chromium.

Two sizes per post: 1080x1350 for Instagram, 1200x900 for Google Business
Profile. GBP crops to a centre square in Maps, so its layout keeps everything
inside the middle 900x900 rather than being a crop of the Instagram file.

Output is JPEG, not PNG. The slides are flat cream/dark artwork with no
transparency, and the PNGs ran 1-1.3MB each against 150-200KB for the same
frame as JPEG, which is what actually gets posted.

    python3 design/render.py             # everything
    python3 design/render.py august      # August only
    python3 design/render.py gbp-daily   # the daily Google Business cards
"""
import json
import os
import sys
from playwright.sync_api import sync_playwright

CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
DESIGN = os.path.abspath(os.path.dirname(__file__))

IG = (1080, 1350)
GBP = (1200, 900)
QUALITY = 90


def ig(url, out):
    return (url, IG, out)


def gbp(key, folder):
    return (f'gbp.html?post={key}', GBP, f'content/{folder}/images/gbp.jpg')


def carousel(tpl, query, folder, slides, prefix='slide'):
    q = f'{query}&' if query else ''
    return [ig(f'{tpl}?{q}slide={i}',
               f'content/{folder}/images/{prefix}-{i}.jpg')
            for i in range(1, slides + 1)]


AUGUST = []
# Aug 17 and Aug 18 predate this script. Their slides are here so the artwork
# stays regenerable, which is what let the retired gold logo survive on them.
AUGUST += carousel('botox-myths.html', '', '2026-08-17-5-botox-lies-you-still', 8)
AUGUST += [gbp('aug-17', '2026-08-17-5-botox-lies-you-still')]
AUGUST += [ig('spotlight.html?slide=1',
              'content/2026-08-18-service-spotlight-botox/images/post.jpg')]
AUGUST += [gbp('aug-18', '2026-08-18-service-spotlight-botox')]

AUGUST += carousel('carousel.html', 'post=red-flags',
                   '2026-08-20-5-red-flags-at-a', 7)
AUGUST += [gbp('aug-20', '2026-08-20-5-red-flags-at-a')]

AUGUST += [ig('single.html?post=the-prep',
              'content/2026-08-21-behind-the-scenes-the-prep/images/post.jpg'),
           gbp('aug-21', '2026-08-21-behind-the-scenes-the-prep')]

AUGUST += [ig('before-after.html?slide=6',
              'content/2026-08-22-great-work-is-invisible/images/before-after-result.jpg'),
           gbp('aug-22', '2026-08-22-great-work-is-invisible')]

AUGUST += carousel('carousel.html', 'post=first-visit',
                   '2026-08-24-your-first-visit-step-by', 8)
AUGUST += [gbp('aug-24', '2026-08-24-your-first-visit-step-by')]

AUGUST += [ig('single.html?post=what-it-costs',
              'content/2026-08-25-why-i-do-not-post/images/post.jpg'),
           gbp('aug-25', '2026-08-25-why-i-do-not-post')]

AUGUST += carousel('owner.html', '', '2026-08-27-meet-np-cleo-the-face', 5)
AUGUST += [gbp('aug-27', '2026-08-27-meet-np-cleo-the-face')]

AUGUST += [ig('single.html?post=treatment-room',
              'content/2026-08-28-welcome-to-the-treatment-room/images/post.jpg'),
           gbp('aug-28', '2026-08-28-welcome-to-the-treatment-room')]

AUGUST += [ig('single.html?post=rested-vs-frozen',
              'content/2026-08-29-this-or-that-rested-vs/images/post.jpg'),
           gbp('aug-29', '2026-08-29-this-or-that-rested-vs')]

AUGUST += carousel('carousel.html', 'post=preventative',
                   '2026-08-31-preventative-botox-when-to-actually', 7)
AUGUST += [gbp('aug-31', '2026-08-31-preventative-botox-when-to-actually')]

LATER = [
    ig('before-after.html?slide=1',
       'content/2026-10-08-lip-filler-natural-vs-overdone/images/before-after-result.jpg'),
    ig('before-after.html?slide=2',
       'content/2026-10-10-subtle-is-the-new-dramatic/images/before-after-result.jpg'),
    ig('before-after.html?slide=3',
       'content/2026-10-24-client-words-the-lip-glow/images/before-after-result.jpg'),
    ig('before-after.html?slide=4',
       'content/2026-10-30-one-syringe-balanced-lips/images/before-after-result.jpg'),
    ig('before-after.html?slide=5',
       'content/2026-10-22-lip-filler-aftercare-your-first/images/day-zero-before-after.jpg'),
]
LATER += carousel('real-results.html', '', '2026-10-15-real-lips-real-results', 7)
LATER += carousel('every-angle.html', '', '2026-11-06-one-result-every-angle', 7)

def gbp_daily():
    """One 1200x900 card per day, flat and date named so the folder reads in
    posting order. Content comes from the same json the planner tab is built
    from, so the sheet and the artwork can never drift apart."""
    path = os.path.join(os.path.dirname(DESIGN), 'strategy', 'gbp-daily-content.json')
    with open(path, encoding='utf-8') as f:
        posts = json.load(f)['posts']
    return [(f"gbp-daily.html?date={p['date']}", GBP,
             f"content/gbp/{p['date']}-{p['slug']}.jpg") for p in posts]


GBP_DAILY = gbp_daily()

JOBS = {'august': AUGUST, 'later': LATER, 'gbp-daily': GBP_DAILY,
        'all': AUGUST + LATER + GBP_DAILY}


def main(which='all'):
    jobs = JOBS[which]
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME)
        page = browser.new_page(device_scale_factor=1)
        for url, (w, h), out in jobs:
            page.set_viewport_size({'width': w, 'height': h})
            os.makedirs(os.path.dirname(out), exist_ok=True)
            page.goto(f'file://{DESIGN}/{url}')
            page.wait_for_timeout(350)
            # botox-myths and spotlight keep every slide in the DOM and reveal
            # one with .active, so the first .slide is a hidden one. The other
            # templates build a single .slide, where both selectors agree.
            el = page.query_selector('.slide.active') or page.query_selector('.slide')
            if el is None:
                print('MISSING .slide:', url)
                continue
            el.screenshot(path=out, type='jpeg', quality=QUALITY)
            print(f'{w}x{h}  {out}')
        browser.close()
    print(f'\n{len(jobs)} rendered')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'all')
