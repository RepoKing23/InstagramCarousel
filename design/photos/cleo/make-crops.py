"""Crop client photos to the treatment area so no face is in the published file.

Also colour-matches before/after pairs shot under different white balance, so the
comparison shows the result rather than the lighting.
"""
from PIL import Image, ImageDraw, ImageStat
import os

SRC = 'design/photos/cleo'
OUT = 'design/photos/cleo/crops'
SP = '/tmp/claude-0/-home-user-InstagramCarousel/c1afbe22-4fc3-5184-a3b6-dc6b3d674dd8/scratchpad'

# (left, top, right, bottom) as fractions of the source image
CROPS = {
    'img_0221': (0.20, 0.16, 0.80, 0.64),
    'img_0233': (0.20, 0.14, 0.80, 0.62),
    'img_0962': (0.00, 0.20, 0.60, 0.68),
    'img_0998': (0.00, 0.16, 0.78, 0.80),
    'img_1119': (0.18, 0.46, 0.62, 0.78),
    'img_1123': (0.32, 0.14, 0.80, 0.48),
    'img_9908': (0.22, 0.16, 0.92, 0.72),
    'img_9912': (0.02, 0.14, 0.90, 0.88),
    'img_4775': (0.22, 0.30, 0.82, 0.56),
    'img_4777': (0.30, 0.34, 0.85, 0.62),
    'img_4778': (0.25, 0.38, 0.85, 0.64),
    'img_4780': (0.22, 0.42, 0.82, 0.68),
    'img_4781': (0.25, 0.40, 0.78, 0.68),
    'img_4782': (0.35, 0.42, 0.90, 0.70),
}

# Pairs shot under different lighting. Both frames get pulled to the midpoint so
# neither the before nor the after is flattered.
COLOUR_MATCH = [('img_1119', 'img_1123'), ('img_0962', 'img_0998')]

ASPECT = 450 / 520  # template frame


def crop(name, box):
    im = Image.open(f'{SRC}/{name}.jpg').convert('RGB')
    W, H = im.size
    l, t, r, b = box[0] * W, box[1] * H, box[2] * W, box[3] * H
    cw, ch = r - l, b - t
    cx, cy = (l + r) / 2, (t + b) / 2
    if cw / ch > ASPECT:
        cw = ch * ASPECT
    else:
        ch = cw / ASPECT
    l, r, t, b = cx - cw / 2, cx + cw / 2, cy - ch / 2, cy + ch / 2
    if l < 0: r -= l; l = 0
    if t < 0: b -= t; t = 0
    if r > W: l -= r - W; r = W
    if b > H: t -= b - H; b = H
    return im.crop((int(max(0, l)), int(max(0, t)), int(min(W, r)), int(min(H, b))))


STRENGTH = 0.5  # partial correction; a full pull flattens real skin tone


def skin_ref(im):
    """Per-channel median over mid-luminance pixels: skin, not shadow or blowout."""
    small = im.resize((160, int(160 * im.height / im.width)))
    px = list(small.getdata())
    lum = sorted(0.299 * r + 0.587 * g + 0.114 * b for r, g, b in px)
    lo, hi = lum[int(len(lum) * .30)], lum[int(len(lum) * .80)]
    band = [p for p in px if lo <= 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2] <= hi]
    band = band or px
    return [sorted(p[i] for p in band)[len(band) // 2] for i in range(3)]


def apply_gains(im, ref, target):
    g = [1 + STRENGTH * (target[i] / ref[i] - 1) for i in range(3)]
    return Image.merge('RGB', [
        ch.point(lambda v, k=g[i]: min(255, int(v * k)))
        for i, ch in enumerate(im.split())
    ])


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    crops = {n: crop(n, b) for n, b in CROPS.items()}

    for a, b in COLOUR_MATCH:
        ra, rb = skin_ref(crops[a]), skin_ref(crops[b])
        target = [(ra[i] + rb[i]) / 2 for i in range(3)]
        print(f'colour-match {a} {ra} + {b} {rb} -> {[round(v) for v in target]}')
        crops[a] = apply_gains(crops[a], ra, target)
        crops[b] = apply_gains(crops[b], rb, target)

    # img_1119 was shot under a hard shadow from the treatment chair. Lift the
    # dark end only; this changes lighting, never lip shape or size.
    crops['img_1119'] = crops['img_1119'].point(
        lambda v: min(255, int(255 * (v / 255) ** 0.78)))

    made = []
    for name, im in crops.items():
        im.save(f'{OUT}/{name}.jpg', quality=92)
        made.append((name, im))
        print(f'{name}: {im.size}')

    CELL, cols = 380, 4
    rows = (len(made) + cols - 1) // cols
    sheet = Image.new('RGB', (CELL * cols, (CELL + 34) * rows), (18, 18, 18))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(made):
        s = min(CELL / im.width, CELL / im.height)
        t = im.resize((int(im.width * s), int(im.height * s)))
        x, y = (i % cols) * CELL, (i // cols) * (CELL + 34)
        sheet.paste(t, (x + (CELL - t.width) // 2, y))
        d.text((x + 6, y + CELL + 10), name, fill=(255, 255, 255))
    sheet.save(f'{SP}/crops_check.jpg', quality=90)
    print('check sheet:', f'{SP}/crops_check.jpg')
