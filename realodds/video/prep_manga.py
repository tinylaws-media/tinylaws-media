"""Prépare les images pour la DA « manga imprimé » : contours encrés des personnages, fonds en trame de points, portraits, papier."""
import os, math, numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageDraw
SRC = "assets_in/le verdict"; OUT = "manga"
PAPER = (239, 230, 210); INK = (24, 20, 18)

def outline(name, out, ink=12, white=0, maxh=1500):
    im = Image.open(os.path.join(SRC, name)).convert("RGBA"); im = im.crop(im.getbbox())
    if im.height > maxh: im = im.resize((int(im.width * maxh / im.height), maxh), Image.LANCZOS)
    pad = ink + white + 6; base = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); base.paste(im, (pad, pad), im)
    a = base.split()[3].point(lambda v: 255 if v > 40 else 0)
    ring = a.filter(ImageFilter.MaxFilter(2 * ink + 1)).filter(ImageFilter.GaussianBlur(1.2))
    out_im = Image.new("RGBA", base.size, INK + (0,)); out_im.putalpha(ring)
    out_im.alpha_composite(base); out_im.save(os.path.join(OUT, out))

def halftone(name, out, tint=None, cell=9, w=1080, h=None, crop=None):
    im = Image.open(os.path.join(SRC, name)).convert("RGB")
    if h: im = ImageOps.fit(im, (w, h), Image.LANCZOS)
    else: im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    g = np.asarray(ImageOps.autocontrast(im.convert("L"), cutoff=2), float) / 255
    H, W = g.shape; canvas = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(canvas)
    col = tint or INK
    # trame à 45° : points de taille ∝ obscurité
    for yy in range(-cell, H + cell, cell):
        for xx in range(-cell, W + cell, cell):
            cx = xx + (cell / 2 if (yy // cell) % 2 else 0); cy = yy
            if 0 <= cx < W and 0 <= cy < H:
                dark = (1 - g[int(cy), int(cx)]) ** 1.9 * 0.82
                r = cell * 0.72 * math.sqrt(dark)
                if r > .6: d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    canvas.save(os.path.join(OUT, out), quality=92)

def portrait(name, out, size=260, fy=.38):
    im = Image.open(os.path.join(SRC, name)).convert("RGB"); s = min(im.size)
    cx, cy = im.width / 2, im.height * fy; box = [int(cx - s * .38), int(max(0, cy - s * .38)), int(cx + s * .38), int(max(0, cy - s * .38) + s * .76)]
    im = im.crop(box).resize((size, size), Image.LANCZOS)
    m = Image.new("L", (size, size), 0); ImageDraw.Draw(m).ellipse([0, 0, size - 1, size - 1], fill=255)
    o = Image.new("RGBA", (size, size), (0, 0, 0, 0)); o.paste(im, (0, 0), m); o.save(os.path.join(OUT, out))

def paper(out, w=1080, h=1920):
    rng = np.random.default_rng(3); n = rng.normal(0, 1, (h // 4, w // 4)); n = np.asarray(Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype("uint8")).resize((w, h), Image.BICUBIC), float)
    fine = rng.normal(0, 1, (h, w)) * 4
    base = np.array(PAPER, float)[None, None, :] + ((n - 128) * 0.10 + fine)[..., None]
    yy, xx = np.mgrid[0:h, 0:w]; vig = 1 - 0.18 * (((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    Image.fromarray(np.clip(base * vig[..., None], 0, 255).astype("uint8")).save(os.path.join(OUT, out), quality=90)

outline("minato facing front fight mode.png", "minato_fight.png")
outline("minato facing right.png", "minato_right.png")
outline("itachi facing front fight mode.png", "itachi_fight.png")
outline("itachi facing left.png", "itachi_left.png")
outline("itachi facing front.png", "itachi_front.png")
outline("sitting obito.png", "obito.png")
outline("sitting kakashi.png", "kakashi.png")
outline("A raikage.png", "raikage.png")
outline("killer b.png", "killer_b.png")
outline("kunai hiraishin.png", "kunai.png", ink=8)
halftone("nuit de kyubi.webp", "bg_kyubi.jpg", tint=(150, 28, 20), h=1100)
halftone("Dimension_du_Kamui.webp", "bg_kamui.jpg", h=1100)
halftone("ciel rouge.avif", "bg_tsukuyomi.jpg", tint=(178, 18, 30), h=1100)
for f, o in [("Madara_Uchiwa3.webp", "p_madara"), ("Hashirama_Senju.webp", "p_hashirama"), ("Naruto_Uzumaki.webp", "p_naruto"), ("Sasuke_portrait.webp", "p_sasuke"),
             ("Jiraya.PNG.webp", "p_jiraiya"), ("Orochimaru.webp", "p_orochimaru"), ("Nagato.webp", "p_nagato"), ("Kisame_Hoshigaki.webp", "p_kisame"),
             ("Ga%3F_Maito.webp", "p_gai"), ("Tsunade2.webp", "p_tsunade")]:
    portrait(f, o + ".png")
paper("paper.jpg")
print("ok", sorted(os.listdir(OUT)))

def face(name, out, cx, cy, sf, size=260):
    im = Image.open(os.path.join(SRC, name)).convert("RGBA"); s = sf * im.width
    box = [int(cx * im.width - s / 2), int(cy * im.height - s / 2), int(cx * im.width + s / 2), int(cy * im.height + s / 2)]
    c = Image.new("RGBA", (int(s), int(s)), (216, 205, 181, 255)); c.alpha_composite(im.crop(box).resize((int(s), int(s))) if False else im.crop(box))
    c = c.resize((size, size), Image.LANCZOS); m = Image.new("L", (size, size), 0); ImageDraw.Draw(m).ellipse([0, 0, size - 1, size - 1], fill=255)
    o = Image.new("RGBA", (size, size), (0, 0, 0, 0)); o.paste(c, (0, 0), m); o.save(os.path.join(OUT, out))

face("minato facing right.png", "f_minato.png", .6, .09, .56)
face("sitting obito.png", "f_obito.png", .47, .13, .42)
face("sitting kakashi.png", "f_kakashi.png", .5, .07, .6)
face("itachi facing front.png", "f_itachi.png", .5, .07, .42)
