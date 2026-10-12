import sys, glob, os
import numpy as np
import cv2
from PIL import Image, ImageFilter, ImageDraw
Image.MAX_IMAGE_PIXELS = None
ROOT = 'D:/Beaver/Ctrl+P/'
OUT = ROOT + 'claude website test/assets/img/cutouts/'
S = sys.argv[1]

def video(tag):
    r = [f for f in glob.glob(ROOT + 'Video/*.png') if tag in f]
    assert len(r) == 1, (tag, r)
    return r[0]

def save(im, name, width=900):
    bb = im.getchannel('A').point(lambda v: 255 if v > 12 else 0).getbbox()
    im = im.crop(bb)
    if im.size[0] > width:
        im = im.resize((width, round(im.size[1] * width / im.size[0])), Image.LANCZOS)
    im.save(OUT + name + '.webp', 'WEBP', quality=88, method=6)
    print(name, im.size, os.path.getsize(OUT + name + '.webp') // 1024, 'KB')
    return im

res = {}

# booklet: the spread is an upright rectangle on a plain grey ground, so find it by where the picture stops being flat grey
b = Image.open(video('2776179820')).convert('RGB')
a = np.array(b).astype(np.int32)
bg = np.median(a[:40, :40].reshape(-1, 3), axis=0)
diff = np.abs(a - bg).max(axis=2)
solid = diff > 26
cols = np.where(solid.mean(axis=0) > 0.25)[0]; rows = np.where(solid.mean(axis=1) > 0.2)[0]
x0, x1, y0, y1 = cols.min(), cols.max(), rows.min(), rows.max()
print('booklet box', x0, y0, x1, y1, b.size)
bk = b.crop((x0, y0, x1 + 1, y1 + 1)).convert('RGBA')
res['booklet'] = save(bk, 'booklet')

# boxes: GrabCut, seeded from the studio grey
bx = Image.open(ROOT + 'CardboardBox1_Mockup.png').convert('RGB'); bx = bx.resize((1500, round(bx.size[1] * 1500 / bx.size[0])), Image.LANCZOS)
ab = np.array(bx); h, w = ab.shape[:2]
d = np.abs(ab.astype(np.int32) - np.array([231, 231, 231])).max(axis=2)
mask = np.full((h, w), cv2.GC_PR_FGD, np.uint8)
mask[d < 5] = cv2.GC_PR_BGD
mask[:int(h * .08)] = cv2.GC_BGD; mask[:, :int(w * .2)] = cv2.GC_BGD; mask[:, int(w * .94):] = cv2.GC_BGD
sat = ab.max(axis=2).astype(int) - ab.min(axis=2).astype(int)
mask[sat > 40] = cv2.GC_FGD
bgd = np.zeros((1, 65)); fgd = np.zeros((1, 65))
cv2.grabCut(cv2.cvtColor(ab, cv2.COLOR_RGB2BGR), mask, None, bgd, fgd, 5, cv2.GC_INIT_WITH_MASK)
fg = ((mask == 1) | (mask == 3)).astype(np.uint8)
n, lab, stats, _ = cv2.connectedComponentsWithStats(fg)
fg = (lab == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
res['boxes'] = save(Image.fromarray(np.dstack([ab, cv2.GaussianBlur(fg * 255, (0, 0), 1.3)]), 'RGBA'), 'boxes')

# tee: trim the saddle off the bottom of the earlier cut
t = Image.open(OUT + 'tee.webp').convert('RGBA')
t = t.crop((0, 0, t.size[0], int(t.size[1] * 0.86)))
res['tee'] = save(t, 'tee')

# posters: two prints with white borders, one over the other
def poster(src, box, size, border=22):
    art = Image.open(src).convert('RGB').crop(box).resize((size[0] - 2 * border, size[1] - 2 * border), Image.LANCZOS)
    p = Image.new('RGBA', size, (255, 255, 255, 255)); p.paste(art, (border, border))
    ImageDraw.Draw(p).rectangle((0, 0, size[0] - 1, size[1] - 1), outline=(0, 0, 0, 34))
    return p
def place(canvas, layer, xy, angle):
    r = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', r.size, (0, 0, 0, 0)); sh.putalpha(r.getchannel('A').point(lambda v: v * 0.16)); sh = sh.filter(ImageFilter.GaussianBlur(14))
    canvas.alpha_composite(sh, (xy[0] + 6, xy[1] + 16)); canvas.alpha_composite(r, xy)
stripes = ROOT + 'Video/Animate PNG/16.png'
script = ROOT + 'Text Effect_ 3600 x 2400 px.png'
geo = video('2792838050')
c = Image.new('RGBA', (1100, 1150), (0, 0, 0, 0))
place(c, poster(geo, (150, 0, 700, 768), (560, 760)), (40, 150), 7)
place(c, poster(stripes, (560, 0, 1340, 1080), (560, 760)), (400, 40), -5)
res['posters'] = save(c, 'posters')

# stickers: a loose handful of the brand stickers
c = Image.new('RGBA', (1300, 1100), (0, 0, 0, 0))
def sticker(n):
    s = Image.open(ROOT + 'Stickers/Frame %d.png' % n).convert('RGBA')
    return s.crop(s.getchannel('A').point(lambda v: 255 if v > 10 else 0).getbbox())
lay = [(1, 0.62, (60, 60), -8), (6, 0.55, (640, 40), 9), (3, 0.9, (120, 420), 6), (4, 0.6, (560, 420), -6), (8, 0.62, (300, 760), 4), (2, 0.9, (900, 640), -10)]
for n, scale, xy, ang in lay:
    s = sticker(n); s = s.resize((round(s.size[0] * scale), round(s.size[1] * scale)), Image.LANCZOS)
    place(c, s, xy, ang)
res['stickers'] = save(c, 'stickers')

names = list(res); cell = 420
sheet = Image.new('RGB', (cell * 5, cell), (48, 127, 226))
for i, nme in enumerate(names):
    im = res[nme].copy(); im.thumbnail((cell - 30, cell - 30))
    sheet.paste(im, (i * cell + (cell - im.size[0]) // 2, (cell - im.size[1]) // 2), im)
sheet.save(S + '/cutouts2.jpg', quality=85)
for f in ['mailers', 'box-label', 'cards']:
    p = OUT + f + '.webp'
    if os.path.exists(p): os.remove(p)
