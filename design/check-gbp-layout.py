"""Assert the daily GBP cards lay out correctly, by measuring the real boxes.

    python3 design/check-gbp-layout.py

Loads every card in the same headless Chromium render.py uses and reads
getBoundingClientRect for the elements that can collide. Pixel sniffing was not
good enough here: it reads gold from the headline's first word as readily as
from the service line, and it missed a logo overlap that shipped on most of the
set. Measuring the DOM is exact.

Two invariants:
  the service line clears the lockup by at least 24px
  the CTA clears the footer by at least 12px
"""
import sys, json, os
sys.path.insert(0,'design')
from playwright.sync_api import sync_playwright
import render

posts=json.load(open('strategy/gbp-daily-content.json'))['posts']
JS = """() => {
  const r = s => { const e = document.querySelector(s); if (!e) return null;
                   const b = e.getBoundingClientRect();
                   return {top:b.top, bottom:b.bottom, left:b.left, right:b.right}; };
  return {lockup:r('.lockup'), service:r('.service'), cta:r('.cta'),
          foot:r('.foot'), col:r('.col'), body:r('.body')};
}"""
rows=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path=render.CHROME)
    pg=br.new_page(device_scale_factor=1)
    pg.set_viewport_size({'width':1200,'height':900})
    for post in posts:
        pg.goto(f"file://{render.DESIGN}/gbp-daily.html?date={post['date']}")
        pg.wait_for_timeout(220)
        m=pg.evaluate(JS)
        rows.append((post['date'], m))
    br.close()

gap_fail=[]; foot_fail=[]
gaps=[]
for d,m in rows:
    g=m['service']['top']-m['lockup']['bottom']
    gaps.append((g,d))
    if g < 24: gap_fail.append((d, round(g,1)))
    slack=m['foot']['top']-m['cta']['bottom']
    if slack < 12: foot_fail.append((d, round(slack,1)))
gaps.sort()
print(f"{len(rows)} cards measured from the DOM")
print(f"logo -> service gap: min {gaps[0][0]:.0f}px ({gaps[0][1]}), max {gaps[-1][0]:.0f}px")
print(f"cards with gap < 24px: {gap_fail or 'none'}")
print(f"cards whose CTA crowds the footer (<12px): {foot_fail or 'none'}")
tall=max(rows, key=lambda r: r[1]['cta']['bottom']-r[1]['service']['top'])
print(f"tallest content: {tall[0]} spans y {tall[1]['service']['top']:.0f} to {tall[1]['cta']['bottom']:.0f}, "
      f"footer top {tall[1]['foot']['top']:.0f}")
