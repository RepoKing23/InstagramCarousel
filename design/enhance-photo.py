"""Clean up a before/after photo pair without changing what the face looks like.

    python3 design/enhance-photo.py BEFORE AFTER [--name pair-x] [--match]
                                    [--trim] [--black-bg]

Writes design/photos/before-after/<name>-before.jpg and <name>-after.jpg, which
before-after-stack.html reads.

What it does, in order, with the exact same settings on both photos:
  1. applies the phone's EXIF rotation and converts to sRGB (HEIC too, when
     pillow-heif is installed)
  2. a very light chroma denoise, which takes out phone-sensor colour speckle
     in shadows but leaves luminance alone, so pores and skin texture stay
  3. a gentle local contrast lift (CLAHE on lightness, blended at 35%)
  4. an unsharp mask at a small radius, for crisp lashes, lip line and hair
  5. upscales with Lanczos when the photo is smaller than the frame needs, so
     the 1080px wide card is never stretched in the browser. This runs last:
     sharpening after an upscale sharpens the interpolation and JPEG blocks,
     which reads as crunchy skin

What it never does: smooth skin, reshape anything, remove marks, or treat the
after differently from the before. A result photo that has been retouched is
not a result, and processing the pair unequally makes the comparison dishonest.

--match pulls both photos halfway toward a shared white balance. Use it when
the two were shot under different lighting (one warm, one cool), so the card
shows the treatment and not the light bulb. Both move, neither is flattered.

--trim cuts off black letterbox or pillarbox bars (photos exported from an
Instagram story or a square crop app come with them).

--black-bg replaces the wall behind a profile shot with pure black, as in the
black and gold card. The subject edge comes from a background-removal model
(bg-mask.mjs, run `npm install` in design/ once), which traces the nose and lip
line cleanly but is unsure about skin in the middle of a close-up. So the model
only supplies the profile line; everything to the right of it is kept at full
strength, untouched, and everything to the left goes black. Where the model is
unsure of the line itself (a shaded chin), the wall's own colour and brightness
decide it. Assumes the face looks left, as in the reference.
"""
import argparse
import os
import subprocess
import tempfile

import cv2
import numpy as np
from PIL import Image, ImageOps

try:  # iPhone photos arrive as HEIC
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

DESIGN = os.path.abspath(os.path.dirname(__file__))
OUT = os.path.join(DESIGN, 'photos', 'before-after')

# Each half of the card is 1080 wide. 1.5x that leaves room to crop and zoom
# with object-position without the browser upscaling.
MIN_WIDTH = 1620

DENOISE_CHROMA = 4      # cv2 h for the colour channels; 0 turns it off
CLAHE_CLIP = 1.6
CLAHE_BLEND = 0.35
SHARPEN_RADIUS = 1.1    # gaussian sigma, in pixels of the source
SHARPEN_AMOUNT = 0.55
MATCH_STRENGTH = 0.5    # partial; a full pull flattens real skin tone


def load(path):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im).convert('RGB')
    return cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)


def trim_bars(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cols = np.flatnonzero(g.mean(0) > 20)
    rows = np.flatnonzero(g.mean(1) > 20)
    # a couple of px in from the bar, where the phone's edge blur lives
    return img[rows[0] + 2:rows[-1] - 1, cols[0] + 2:cols[-1] - 1]


def ai_mask(img):
    with tempfile.TemporaryDirectory() as tmp:
        src, out = os.path.join(tmp, 'in.png'), os.path.join(tmp, 'mask.png')
        cv2.imwrite(src, img)
        subprocess.run(['node', os.path.join(DESIGN, 'bg-mask.mjs'), src, out],
                       check=True, cwd=DESIGN)
        m = cv2.imread(out, cv2.IMREAD_UNCHANGED)
    return m[..., 3] if m.ndim == 3 else m


def profile_alpha(img, inset=1.0, feather=1.4):
    """Alpha that is 0 left of the face profile and 1 right of it."""
    from scipy.ndimage import median_filter, gaussian_filter1d
    ai = ai_mask(img)
    h, w = img.shape[:2]
    lab = cv2.cvtColor(cv2.GaussianBlur(img, (0, 0), 1.5),
                       cv2.COLOR_BGR2LAB).astype(np.float32)
    L = lab[..., 0]

    # Wall model from what the model is sure is background, left third.
    # Dark clutter and clothing are left out; they go black either way.
    strip = ai[:, :w // 3] < 10
    bg = lab[:, :w // 3][strip]
    bg = bg[bg[:, 0] > 80]
    mu = bg.mean(0)
    d = lab - mu
    icov = np.linalg.inv(np.cov(bg.T) + np.eye(3) * 4)
    dist = np.sqrt(np.einsum('...i,ij,...j->...', d, icov, d))
    warm = (lab[..., 1] - 128) + (lab[..., 2] - 128)
    wall_warm = (mu[1] - 128) + (mu[2] - 128)
    # per-row wall brightness, for skin in shade that is only darker than it
    near = ai[:, :w // 6] < 10
    wall_l = np.array([np.median(L[y, :w // 6][near[y]]) if near[y].any()
                       else mu[0] for y in range(h)])
    darker = (L < wall_l[:, None] - 22) & (warm > wall_warm + 5)
    not_wall = ((dist > 6) | (warm > wall_warm + 12) | darker) & (L > 55)
    # opening drops stray hairs on the wall
    not_wall = cv2.morphologyEx(not_wall.astype(np.uint8), cv2.MORPH_OPEN,
                                np.ones((9, 9), np.uint8)) > 0
    face = (ai > 40) | not_wall

    # Leftmost solid run of face in each row is the profile.
    edge = np.full(h, np.nan)
    for y in range(h):
        for x in np.flatnonzero(face[y]):
            if face[y, x:x + 25].all():
                edge[y] = x
                break
    rows = np.arange(h)
    ok = ~np.isnan(edge)
    edge = median_filter(np.interp(rows, rows[ok], edge[ok]), 13, mode='nearest')

    # Rows the model traced itself stay exact (lip notch, nostril). Rows that
    # fell back to the colour tests may bulge right on a highlight; pull those
    # toward a smooth curve, only ever leftward.
    sure = ai[rows, np.clip(edge.round().astype(int) + 4, 0, w - 1)] > 128
    for _ in range(4):
        smooth = gaussian_filter1d(edge, 14)
        fix = ~sure & (edge > smooth + 3)
        edge[fix] = smooth[fix]
    edge = gaussian_filter1d(edge, 2.5)

    # 1px inset keeps the wall's light fringe off the black
    a = np.clip((np.arange(w)[None, :] - (edge[:, None] + inset)) / feather + .5, 0, 1)
    return cv2.GaussianBlur(a.astype(np.float32), (0, 0), 0.9)


def upscale(img):
    h, w = img.shape[:2]
    if w >= MIN_WIDTH:
        return img
    k = MIN_WIDTH / w
    return cv2.resize(img, (MIN_WIDTH, round(h * k)),
                      interpolation=cv2.INTER_LANCZOS4)


def denoise_chroma(img):
    if not DENOISE_CHROMA:
        return img
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    a = cv2.fastNlMeansDenoising(a, None, DENOISE_CHROMA, 7, 21)
    b = cv2.fastNlMeansDenoising(b, None, DENOISE_CHROMA, 7, 21)
    return cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)


def local_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    tile = max(4, img.shape[1] // 120)
    lifted = cv2.createCLAHE(CLAHE_CLIP, (tile, tile)).apply(l)
    l = cv2.addWeighted(lifted, CLAHE_BLEND, l, 1 - CLAHE_BLEND, 0)
    return cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)


def sharpen(img):
    blur = cv2.GaussianBlur(img, (0, 0), SHARPEN_RADIUS)
    return cv2.addWeighted(img, 1 + SHARPEN_AMOUNT, blur, -SHARPEN_AMOUNT, 0)


def skin_ref(img):
    """Per-channel median over mid-lightness pixels: skin, not shadow or a
    black backdrop or blown highlights."""
    small = cv2.resize(img, (200, round(200 * img.shape[0] / img.shape[1])))
    px = small.reshape(-1, 3).astype(np.float32)
    lum = px @ np.array([0.114, 0.587, 0.299], np.float32)
    lo, hi = np.percentile(lum, [40, 85])
    band = px[(lum >= lo) & (lum <= hi)]
    return np.median(band if len(band) else px, axis=0)


def match_pair(a, b):
    ra, rb = skin_ref(a), skin_ref(b)
    mid = (ra + rb) / 2
    out = []
    for img, ref in ((a, ra), (b, rb)):
        gain = 1 + MATCH_STRENGTH * (mid / np.maximum(ref, 1) - 1)
        out.append(np.clip(img.astype(np.float32) * gain, 0, 255).astype(np.uint8))
    return out


def enhance(img):
    return upscale(sharpen(local_contrast(denoise_chroma(img))))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('before')
    ap.add_argument('after')
    ap.add_argument('--name', help='output name, default: the before file name')
    ap.add_argument('--match', action='store_true',
                    help='even out white balance between the two')
    ap.add_argument('--trim', action='store_true',
                    help='cut off black letterbox/pillarbox bars')
    ap.add_argument('--black-bg', action='store_true',
                    help='replace the wall behind a profile with black')
    args = ap.parse_args()

    name = args.name or os.path.splitext(os.path.basename(args.before))[0]
    before, after = load(args.before), load(args.after)
    if args.trim:
        before, after = trim_bars(before), trim_bars(after)
    # masks come from the untouched photos, before any processing
    alphas = [profile_alpha(i) for i in (before, after)] if args.black_bg else None
    if args.match:
        before, after = match_pair(before, after)

    os.makedirs(OUT, exist_ok=True)
    for k, (tag, img) in enumerate((('before', before), ('after', after))):
        out = enhance(img)
        if alphas:
            a = cv2.resize(alphas[k], (out.shape[1], out.shape[0]),
                           interpolation=cv2.INTER_LINEAR)[..., None]
            out = (out.astype(np.float32) * a).round().astype(np.uint8)
        path = os.path.join(OUT, f'{name}-{tag}.jpg')
        Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).save(
            path, quality=95, subsampling=0, optimize=True)
        print(f'{out.shape[1]}x{out.shape[0]}  {os.path.relpath(path)}')


if __name__ == '__main__':
    main()
