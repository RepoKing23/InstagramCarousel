"""Clean up a before/after photo pair without changing what the face looks like.

    python3 design/enhance-photo.py BEFORE AFTER [--name pair-x] [--match]

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
"""
import argparse
import os

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
    args = ap.parse_args()

    name = args.name or os.path.splitext(os.path.basename(args.before))[0]
    before, after = load(args.before), load(args.after)
    if args.match:
        before, after = match_pair(before, after)

    os.makedirs(OUT, exist_ok=True)
    for tag, img in (('before', before), ('after', after)):
        out = enhance(img)
        path = os.path.join(OUT, f'{name}-{tag}.jpg')
        Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).save(
            path, quality=95, subsampling=0, optimize=True)
        print(f'{out.shape[1]}x{out.shape[0]}  {os.path.relpath(path)}')


if __name__ == '__main__':
    main()
