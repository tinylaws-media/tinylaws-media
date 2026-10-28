"""Subject Zero brand kit: profile picture (her face, 800x800, reads at 40 px) and YouTube banner (2560x1440, safe
area 1546x423 in the middle). python3 make_brand.py -> out/brand/"""
import os
import skia
from sz2d import (rgb, fill, ink, text, font, draw_hero, draw_duck, Sea, sky, mist_band, paper_over, seal, rrect,
                  PAPER, INKC, PRUSSIAN, YEL_L, FOAM, CORAL)
import sz2d

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "brand")
os.makedirs(OUT, exist_ok=True)


def avatar():
    s = skia.Surface(800, 800)
    c = s.getCanvas()
    c.clear(skia.Color4f(*[x for x in (0, 0, 0)], 1))
    c.drawRect(skia.Rect.MakeWH(800, 800), fill(PRUSSIAN))
    c.drawCircle(400, 400, 360, fill(rgb("#F4B62F")))
    c.drawCircle(400, 400, 360, ink(14))
    draw_hero(c, 400, 470, s=1.45, face="smile", boil=None, arms="none", t=0.0)
    s.makeImageSnapshot().save(os.path.join(OUT, "avatar_800.png"), skia.kPNG)


def banner():
    W_, H_ = 2560, 1440
    s = skia.Surface(W_, H_)
    c = s.getCanvas()
    # the sea scene, stretched to banner width
    c.save()
    c.scale(W_ / 1080, W_ / 1080)
    c.translate(0, -360)
    sky(c, 0.0, horizon=520, sun=(140, 430), sun_r=56)
    mist_band(c, 40, 450, 420, 26)
    mist_band(c, 600, 480, 380, 22)
    sea = Sea(horizon=520)
    import numpy as np
    for i in range(0, 3):
        sea.draw_layer(c, i, 0.4, (1, 0.6))
    yw = float(sea.height(3, np.array([830]), 0.4)[0])
    draw_hero(c, 830, yw - 62, s=0.36, face="worried", boil=None, arms="paddle", t=0.4)
    draw_duck(c, 915, float(sea.height(3, np.array([915]), 0.4)[0]) + 2, s=0.3)
    for i in range(3, 8):
        sea.draw_layer(c, i, 0.4, (1, 0.6))
    c.restore()
    # title in the safe area (centre 1546 x 423)
    f = font("display", 150)
    text(c, "SUBJECT ZERO", 1200, 690, f, FOAM, align="center", stroke=30)
    f2 = font("mono", 54)
    tag = "COULD YOU SURVIVE?  ·  NEW EPISODES DAILY"
    wv = f2.measureText(tag)
    c.drawPath(rrect(1200 - wv / 2 - 30, 740, wv + 60, 84, 14), fill(INKC, 0.9))
    text(c, tag, 1200, 800, f2, YEL_L, align="center")
    paper_over(c, 1.0) if False else None
    s.makeImageSnapshot().save(os.path.join(OUT, "youtube_banner_2560x1440.png"), skia.kPNG)


if __name__ == "__main__":
    avatar()
    banner()
    print("wrote", OUT)
