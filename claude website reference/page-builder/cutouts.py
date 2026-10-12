"""Cut products out of their studio backgrounds so they can sit on the page without a card."""
import sys, glob, os
import numpy as np
import cv2
from PIL import Image, ImageFilter, ImageDraw
Image.MAX_IMAGE_PIXELS = None

ROOT = 'D:/Beaver/Ctrl+P/'
OUT = ROOT + 'claude website test/assets/img/cutouts/'
S = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

def video(tag):
    r = [f for f in glob.glob(ROOT + 'Video/*.png') if tag in f]
    assert len(r) == 1, (tag, r)
    return r[0]

def load(path, maxw=1600):
    im = Image.open(path).convert('RGB')
    if im.size[0] > maxw:
        im = im.resize((maxw, round(im.size[1] * maxw / im.size[0])), Image.LANCZOS)
    return im

def flood_cut(im, tol=10, seeds=None, feather=1.2, grow=1):
    """Remove a near-uniform studio background connected to the image border."""
    a = np.array(im)
    h, w = a.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    work = cv2.GaussianBlur(a, (0, 0), 1.2)
    pts = seeds or [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3), (w // 2, 2), (2, h // 2), (w - 3, h // 2), (w // 2, h - 3)]
    for (x, y) in pts:
        if mask[y + 1, x + 1]:
            continue
        cv2.floodFill(work.copy(), mask, (x, y), 0, (tol,) * 3, (tol,) * 3, 4 | cv2.FLOODFILL_MASK_ONLY | (255 << 8) | cv2.FLOODFILL_FIXED_RANGE * 0)
    bg = mask[1:-1, 1:-1] > 0
    if grow:
        bg = cv2.dilate(bg.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=grow) > 0
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    alpha = cv2.GaussianBlur(alpha, (0, 0), feather)
    return Image.fromarray(np.dstack([a, alpha]), 'RGBA')

def grab_cut(im, rect, iters=6, feather=1.5):
    a = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    mask = np.zeros(a.shape[:2], np.uint8)
    bgd = np.zeros((1, 65), np.float64); fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(a, mask, rect, bgd, fgd, iters, cv2.GC_INIT_WITH_RECT)
    fg = ((mask == 1) | (mask == 3)).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(fg)
    if n > 1:
        keep = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        fg = (lab == keep).astype(np.uint8)
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    alpha = cv2.GaussianBlur(fg * 255, (0, 0), feather)
    return Image.fromarray(np.dstack([np.array(im), alpha]), 'RGBA')

def finish(im, name, width=900, crop=None):
    if crop:
        im = im.crop(crop)
    bb = im.getchannel('A').point(lambda v: 255 if v > 12 else 0).getbbox()
    im = im.crop(bb)
    if im.size[0] > width:
        im = im.resize((width, round(im.size[1] * width / im.size[0])), Image.LANCZOS)
    im.save(OUT + name + '.webp', 'WEBP', quality=88, method=6)
    print(name, im.size, os.path.getsize(OUT + name + '.webp') // 1024, 'KB')
    return im

results = {}
# studio backgrounds: flood from the borders
results['boxes'] = finish(flood_cut(load(ROOT + 'CardboardBox1_Mockup.png'), tol=7), 'boxes')
results['box-tape'] = finish(flood_cut(load(ROOT + 'MockupBox1.png'), tol=6), 'box-tape')
results['mailers'] = finish(flood_cut(load(ROOT + 'mockuupenv.png'), tol=7), 'mailers')
results['booklet'] = finish(flood_cut(load(video('2776179820')), tol=6), 'booklet')
results['box-label'] = finish(flood_cut(load(video('2793018420')), tol=7), 'box-label')
results['cards'] = finish(flood_cut(load(video('2792971203')), tol=5), 'cards')
results['sticker-pack'] = finish(flood_cut(load(video('2764408362')), tol=14), 'sticker-pack')

# busy backgrounds: GrabCut from a rectangle around the subject
t = load(video('2792797124'))                       # tote on a desk
w, h = t.size
results['tote'] = finish(grab_cut(t, (int(w * .19), int(h * .02), int(w * .58), int(h * .97))), 'tote')
r = load(ROOT + '362424f9-e2ec-40c4-842a-0a88ff76db37.png', 1100)   # rider in the tee
w, h = r.size
results['tee'] = finish(grab_cut(r, (int(w * .08), int(h * .02), int(w * .84), int(h * .97))), 'tee')

# contact sheet on a loud background so halos show
names = list(results)
cell = 420
sheet = Image.new('RGB', (cell * 5, cell * 2), (48, 127, 226))
for i, nme in enumerate(names):
    im = results[nme].copy(); im.thumbnail((cell - 30, cell - 30))
    x = (i % 5) * cell + (cell - im.size[0]) // 2; y = (i // 5) * cell + (cell - im.size[1]) // 2
    sheet.paste(im, (x, y), im)
    ImageDraw.Draw(sheet).text(((i % 5) * cell + 8, (i // 5) * cell + 6), nme, fill=(255, 255, 255))
sheet.save(S + '/cutouts.jpg', quality=85)
