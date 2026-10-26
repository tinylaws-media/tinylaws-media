"""THE EXIT MANUAL — look v2 (owner feedback, 25 Oct 2026: "not another AI channel", no generic neon).

What changed from v1 (exit_engine.py stays for the old episode):
  - no synthwave floor grid, no RGB offset on every caption: a dark, quiet room lit by a phone
  - one meaning per colour: green = our time, magenta = their money, cyan = data / sources, off-white = words
  - captions in IBM Plex Sans Condensed Bold (human, editorial), numbers and documents in IBM Plex Mono
  - glow only on what matters (the phone's light, the money); everything else is flat
  - FIXED film grain and faint fixed scanlines (nothing animated, nothing flashes)
Phone rules: text between y 230 and 1450, nothing important at x > 900, captions <= 5 words a line, 2 lines.
"""
import math
import os

import numpy as np
import skia

from exit_engine import (W, H, FPS, BG, GREEN, MAGENTA, CYAN, WHITE, GREY, DIM, INK, Assets, Ctx, clamp01, prog,
                         lerp, ease_out, ease_in_out, col, relay, relay_icon)

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
CAP_CX = 485
AMBER = 0xFFFFC27A          # only for the bedside clock (warm, human)
INK.update({"amber": AMBER, "ink": 0xFF0B0E16, "paper": 0xFFDCE1E6})


def ease_io5(x):
    x = clamp01(x)
    return 16 * x ** 5 if x < 0.5 else 1 - (-2 * x + 2) ** 5 / 2


class Assets2(Assets):
    def __init__(self):
        super().__init__()
        for k, f in (("sans", "IBMPlexSansCondensed-Bold.ttf"), ("sansm", "IBMPlexSansCondensed-SemiBold.ttf"),
                     ("mono", "IBMPlexMono-Medium.ttf")):
            self.tf[k] = skia.Typeface.MakeFromFile(os.path.join(FONT_DIR, f))
        self.bg2 = self._background2()
        self.grain = self._grain()

    def _background2(self):
        s = skia.Surface(W, H)
        c = s.getCanvas()
        c.clear(BG)
        p = skia.Paint(Shader=skia.GradientShader.MakeRadial((540, 820), 1100, [0xFF0C1018, 0xFF05060A]))
        c.drawRect(skia.Rect(0, 0, W, H), p)
        p = skia.Paint(Shader=skia.GradientShader.MakeRadial((540, 900), 1300, [0x00000000, 0xC0000000]))
        c.drawRect(skia.Rect(0, 0, W, H), p)
        return s.makeImageSnapshot()

    def _grain(self):
        r = np.random.default_rng(11)
        g = (r.random((H, W)) * 255).astype(np.uint8)
        a = np.zeros((H, W, 4), np.uint8)
        a[..., 0] = a[..., 1] = a[..., 2] = g
        a[..., 3] = 9                                   # very faint, and fixed
        return skia.Image.fromarray(a, colorType=skia.ColorType.kRGBA_8888_ColorType)


class Ctx2(Ctx):
    def bg(self, tint=None, tint_a=0.0):
        self.c.drawImage(self.A.bg2, 0, 0)
        if tint is not None and tint_a > 0:
            p = skia.Paint(Shader=skia.GradientShader.MakeLinear(
                [(0, 0), (0, H)], [skia.Color4f(*_rgb(tint), tint_a).toColor(), 0x00000000]))
            self.c.drawRect(skia.Rect(0, 0, W, H), p)

    def finish(self):
        self.c.drawImage(self.A.grain, 0, 0)
        p = skia.Paint(Color=0xFF000000)
        p.setAlphaf(0.07)
        for y in range(0, H, 4):
            self.c.drawRect(skia.Rect(0, y, W, y + 1.5), p)

    def t2(self, s, x, y, size, color="white", kind="sans", align="center", alpha=1.0, glow=0.0):
        return self.text(s, x, y, size, color, kind=kind, align=align, alpha=alpha, glow=glow)

    def cam(self, cx, cy, z, fx=None, fy=None):
        """Camera: world point (cx, cy) lands at screen (fx, fy) (default CAP_CX, 760) with zoom z."""
        fx = CAP_CX if fx is None else fx
        fy = 760 if fy is None else fy
        self.c.save()
        self.c.translate(fx, fy)
        self.c.scale(z, z)
        self.c.translate(-cx, -cy)


def _rgb(c):
    c = INK.get(c, c) if isinstance(c, str) else c
    return ((c >> 16) & 255) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255


# ------------------------------------------------------------------ captions v2
class Caption2:
    """A caption block shown whole while its words are spoken. '/' = line break, *word* = accent. <= 5 words/line."""

    def __init__(self, start, end, text, y=1222, size=86, hi="green"):
        self.start, self.end, self.text, self.y, self.size, self.hi = start, end, text, y, size, hi
        self.lines = []
        for raw in text.split("/"):
            toks, on = [], False
            for tok in raw.strip().split(" "):
                if not tok:
                    continue
                if tok.startswith("*"):
                    on = True
                toks.append((tok.replace("*", ""), on))
                if "*" in tok.lstrip("*"):
                    on = False
            self.lines.append(toks)
        for toks in self.lines:
            assert len(toks) <= 5, f"caption line over 5 words: {text}"
        assert len(self.lines) <= 2, f"caption over 2 lines: {text}"

    def plain(self):
        return " / ".join(" ".join(w for w, _ in toks) for toks in self.lines)

    def draw(self, X):
        t = X.t
        if not (self.start <= t < self.end):
            return
        a = (1.0 if self.start <= 0 else prog(t, self.start, self.start + 0.07)) * (1 - prog(t, self.end - 0.07, self.end))
        size = self.size
        f = "sans"
        sp = X.width(" ", size, f)
        widths = [sum(X.width(w, size, f) for w, _ in toks) + sp * (len(toks) - 1) for toks in self.lines]
        if max(widths) > 800:
            size *= 800 / max(widths)
            sp = X.width(" ", size, f)
            widths = [sum(X.width(w, size, f) for w, _ in toks) + sp * (len(toks) - 1) for toks in self.lines]
        lh = size * 1.06
        # a soft dark bed behind the words (no box): keeps them readable on any picture
        top = self.y
        hgt = lh * len(self.lines)
        bed = skia.Paint(AntiAlias=True, Color=0xFF000000)
        bed.setAlphaf(0.55 * a)
        bed.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 38))
        X.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(CAP_CX - max(widths) / 2 - 20, top - 6,
                                                      CAP_CX + max(widths) / 2 + 20, top + hgt + 10), 30, 30), bed)
        rise = 10 * (1 - ease_out(prog(t, self.start, self.start + 0.18))) if self.start > 0 else 0
        for li, toks in enumerate(self.lines):
            x = CAP_CX - widths[li] / 2
            base = top + lh * (li + 0.8) + rise
            for w, on in toks:
                ww = X.width(w, size, f)
                X.text(w, x, base, size, self.hi if on else "white", kind=f, align="left", alpha=a,
                       glow=0.35 if on else 0.0)
                x += ww + sp


# ------------------------------------------------------------------ the phone and its feed
PHONE_W, PHONE_H = 380, 780
CARD_H = 300
CARD_GAP = 22


def is_ad(i):
    return i % 4 == 3


def feed_card(X, x, y, w, i, alpha=1.0, ad_glow=1.0, dim_posts=1.0):
    """A generic post (no real person, no real brand). Every 4th card is an ad slot."""
    c = X.c
    h = CARD_H
    ad = is_ad(i)
    r = np.random.default_rng((i * 7 + 3) % 9973)
    base = 0xFF141924 if not ad else 0xFF1E0A16
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), 18, 18), X.paint(base, alpha))
    pa = alpha * (dim_posts if not ad else 1.0)
    # avatar + name bars
    av = [0xFF3A4458, 0xFF2E5A4A, 0xFF5A4A2E, 0xFF44385A][(i * 5) % 4]
    c.drawCircle(x + 34, y + 34, 18, X.paint(av if not ad else MAGENTA, pa))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x + 62, y + 24, x + 62 + r.integers(90, 170), y + 36), 6, 6),
                X.paint(0xFF4A5468, pa))
    # picture: an abstract landscape / shape
    px0, py0, px1, py1 = x + 14, y + 64, x + w - 14, y + h - 46
    sky = [0xFF1D2A40, 0xFF2A1D33, 0xFF1D3330, 0xFF33291D][r.integers(0, 4)]
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(px0, py0, px1, py1), 12, 12), X.paint(sky if not ad else 0xFF2C0F22, pa))
    c.save()
    c.clipRRect(skia.RRect.MakeRectXY(skia.Rect(px0, py0, px1, py1), 12, 12), doAntiAlias=True)
    if not ad:
        sx = lerp(px0, px1, r.uniform(0.2, 0.8))
        c.drawCircle(sx, py0 + 50, 26, X.paint(0xFF8A93A3, 0.55 * pa))
        hill = skia.Path()
        hill.moveTo(px0, py1)
        hill.lineTo(px0, py1 - 60)
        hill.quadTo(lerp(px0, px1, 0.35), py1 - 140 + r.uniform(-30, 30), lerp(px0, px1, 0.6), py1 - 70)
        hill.quadTo(lerp(px0, px1, 0.8), py1 - 110, px1, py1 - 50)
        hill.lineTo(px1, py1)
        hill.close()
        c.drawPath(hill, X.paint(0xFF2B3346, pa))
    c.restore()
    if ad:
        X.text("AD", px0 + 18, py0 + 46, 40, "magenta", kind="mono", align="left", alpha=alpha)
        X.neon_rect(x, y, w, h, "magenta", width=3, r=18, glow=0.7 * ad_glow, alpha=alpha)
    # action row
    for k in range(3):
        c.drawCircle(x + 30 + k * 40, y + h - 22, 9, X.paint(0xFF4A5468, pa))


def feed(X, x, top, w, scroll, i0=-6, i1=40, clip=None, alpha=1.0, outside_alpha=None, ad_glow=1.0, dim_posts=1.0):
    """Cards stacked from 'top' (world y of card 0) moved up by 'scroll' px. clip = rect where cards are fully lit."""
    step = CARD_H + CARD_GAP
    for i in range(i0, i1):
        y = top + i * step - scroll
        if y > H * 3 or y + CARD_H < -H * 2:
            continue
        feed_card(X, x, y, w, i, alpha=alpha, ad_glow=ad_glow, dim_posts=dim_posts)


def phone(X, cx, cy, scroll=0.0, clock="23:12", screen_on=1.0, w=PHONE_W, h=PHONE_H, glow=1.0, scrollbar=None,
          content=None):
    """A phone seen from the front. The screen shows the feed (or content(X, rect))."""
    c = X.c
    x0, y0 = cx - w / 2, cy - h / 2
    body = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x0 + w, y0 + h), 52, 52)
    if glow > 0 and screen_on > 0:
        c.drawRRect(body, X.paint(0xFF9FC4FF, 0.10 * glow * screen_on, blur=60))
    c.drawRRect(body, X.paint(0xFF0A0C11))
    c.drawRRect(body, X.paint(0xFF2A3040, 1.0, stroke=5))
    sx0, sy0, sx1, sy1 = x0 + 16, y0 + 16, x0 + w - 16, y0 + h - 16
    scr = skia.RRect.MakeRectXY(skia.Rect(sx0, sy0, sx1, sy1), 40, 40)
    c.save()
    c.clipRRect(scr, doAntiAlias=True)
    c.drawRRect(scr, X.paint(0xFF07090D))
    if content:
        content(X, (sx0, sy0, sx1, sy1))
    else:
        feed(X, sx0 + 14, sy0 + 70, sx1 - sx0 - 28, scroll)
        # status bar
        c.drawRect(skia.Rect(sx0, sy0, sx1, sy0 + 58), X.paint(0xFF07090D, 0.92))
        X.text(clock, sx0 + 40, sy0 + 42, 30, "white", kind="sansm", align="left")
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(sx1 - 74, sy0 + 22, sx1 - 36, sy0 + 40), 5, 5),
                    X.paint(0xFF8A93A3, 1.0, stroke=2.5))
        if scrollbar is not None:              # the scroll thumb: shrinks as the feed grows, never reaches the end
            frac, pos = scrollbar
            th = max(10, (sy1 - sy0 - 100) * frac)
            ty = sy0 + 70 + (sy1 - sy0 - 100 - th) * pos
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(sx1 - 12, ty, sx1 - 6, ty + th), 3, 3), X.paint(0xFFAAB2C0, 0.8))
    if screen_on < 1:
        c.drawRRect(scr, X.paint(0xFF000000, 1 - screen_on))
    c.restore()
    # notch
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(cx - 50, y0 + 26, cx + 50, y0 + 50), 12, 12), X.paint(0xFF000000))
    return (sx0, sy0, sx1, sy1)


# ------------------------------------------------------------------ the eye (generic, drawn; not a real person)
def eye(X, cx, cy, s=1.0, look=0.0, lid=1.0, reflect=1.0):
    c = X.c
    c.save()
    c.translate(cx, cy)
    c.scale(s, s)
    wdt, hgt = 330, 150 * lid
    almond = skia.Path()
    almond.moveTo(-wdt, 0)
    almond.cubicTo(-wdt * 0.5, -hgt * 1.25, wdt * 0.5, -hgt * 1.25, wdt, 0)
    almond.cubicTo(wdt * 0.5, hgt * 1.25, -wdt * 0.5, hgt * 1.25, -wdt, 0)
    almond.close()
    c.drawPath(almond, X.paint(0xFFC9CED6))
    c.save()
    c.clipPath(almond, doAntiAlias=True)
    p = skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((0, 0), 330, [0x00000000, 0x90000000]))
    c.drawPath(almond, p)
    ix = look * 40
    p = skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial(
        (ix, 0), 132, [0xFF2F6E5C, 0xFF1C4A3E, 0xFF0D2620]))
    c.drawCircle(ix, 0, 132, p)
    for k in range(36):                         # iris fibres
        a = k / 36 * 2 * math.pi
        c.drawLine(ix + 58 * math.cos(a), 58 * math.sin(a), ix + 126 * math.cos(a), 126 * math.sin(a),
                   X.paint(0xFF4FA88C, 0.25, stroke=3))
    c.drawCircle(ix, 0, 56, X.paint(0xFF020304))
    if reflect > 0:                             # the phone, reflected in the pupil
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(ix - 14, -24, ix + 12, 22), 5, 5), X.paint(0xFFBFD6FF, 0.85 * reflect))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(ix - 14, -24, ix + 12, 22), 5, 5),
                    X.paint(0xFFBFD6FF, 0.5 * reflect, blur=8))
    c.drawCircle(ix + 40, -42, 14, X.paint(0xFFFFFFFF, 0.55))
    c.restore()
    c.drawPath(almond, X.paint(0xFF0B0E16, 1.0, stroke=10))
    c.restore()


def pixelated(X, draw_fn, block):
    """Draw draw_fn(X') into an offscreen layer, then show it as square pixels of 'block' px (no flicker)."""
    if block <= 1.01:
        draw_fn(X)
        return
    s = skia.Surface(W, H)
    c2 = s.getCanvas()
    c2.clear(0x00000000)
    X2 = Ctx2(X.A, c2, X.t, X.level)
    draw_fn(X2)
    img = s.makeImageSnapshot()
    sw, sh = max(1, int(W / block)), max(1, int(H / block))
    small = skia.Surface(sw, sh)
    small.getCanvas().drawImageRect(img, skia.Rect(0, 0, W, H), skia.Rect(0, 0, sw, sh),
                                    skia.SamplingOptions(skia.FilterMode.kLinear))
    simg = small.makeImageSnapshot()
    X.c.drawImageRect(simg, skia.Rect(0, 0, sw, sh), skia.Rect(0, 0, sw * W / sw, sh * H / sh),
                      skia.SamplingOptions(skia.FilterMode.kNearest))
    # thin pixel seams: the façade turns into a grid of numbers
    if block > 10:
        p = X.paint(0xFF05060A, clamp01((block - 10) / 30) * 0.8, stroke=1.5)
        for gx in range(0, W, int(block)):
            X.c.drawLine(gx, 0, gx, H, p)
        for gy in range(0, H, int(block)):
            X.c.drawLine(0, gy, W, gy, p)


# ------------------------------------------------------------------ the year grid
GRID_COLS, GRID_PITCH, GRID_CELL = 25, 30, 25
GRID_X0, GRID_Y0 = CAP_CX - GRID_COLS * GRID_PITCH / 2 + (GRID_PITCH - GRID_CELL) / 2, 700
SLIVER = 18.6 / 7 / 24        # 18 h 36 min a week = 2.657 h a day = 11.07 % of each day


def cell_xy(i):
    return GRID_X0 + (i % GRID_COLS) * GRID_PITCH, GRID_Y0 + (i // GRID_COLS) * GRID_PITCH


def year_grid(X, u, alpha=1.0, block_hi=0.0, others=1.0):
    """365 days. u = 0: every day keeps its own 11 % sliver of feed time; u = 1: the slivers are stacked into
    whole days at the start of the year (365 x 11.07 % = 40.4 days)."""
    c = X.c
    for i in range(365):
        x, y = cell_xy(i)
        c.drawRect(skia.Rect(x, y, x + GRID_CELL, y + GRID_CELL), X.paint(0xFF1A2030, alpha * others))
    hs = GRID_CELL * SLIVER
    n_per = 1 / SLIVER                       # 9.03 slivers fill one day
    for i in range(365):
        x0, y0 = cell_xy(i)
        sy0 = y0 + GRID_CELL - hs
        tgt = int(i // n_per)
        slot = i - tgt * n_per
        tx, ty = cell_xy(tgt)
        ty = ty + GRID_CELL - hs * (slot + 1)
        d = (i % 37) / 37 * 0.45             # staggered start
        k = ease_in_out(clamp01((u - d) / 0.55))
        x = lerp(x0, tx, k)
        y = lerp(sy0, ty, k) - math.sin(math.pi * k) * 40
        c.drawRect(skia.Rect(x, y, x + GRID_CELL, y + hs + 0.6), X.paint("green", alpha))
    if block_hi > 0:
        x0, y0 = cell_xy(0)
        x1, y1 = cell_xy(24)
        X.neon_rect(x0 - 8, y0 - 8, x1 + GRID_CELL - x0 + 16, GRID_PITCH + GRID_CELL + 16, "green", width=3, r=8,
                    glow=0.8, alpha=block_hi * alpha)


# ------------------------------------------------------------------ small pieces
def tag(X, s, x, y, color="cyan", alpha=1.0, size=34):
    w = X.width(s, size, "mono")
    X.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 14, y - size * 0.9, x + w + 14, y + size * 0.35), 8, 8),
                  X.paint(color, 0.14 * alpha))
    X.text(s, x, y, size, color, kind="mono", align="left", alpha=alpha)


def doc_lines(X, lines, x, y, size=40, lh=1.38, color=0xFFB8C0CC, hi=(), hi_u=(), alpha=1.0, maxw=760):
    """Typeset text in Plex Mono; hi = list of (start_word_index, end_word_index) highlight ranges,
    hi_u = progress 0..1 of each highlight sweep. Returns end y."""
    f = X.A.font("mono", size)
    words = " ".join(lines).split(" ")
    sp = f.measureText(" ")
    rows, cur, curw = [], [], 0
    for wi, wd in enumerate(words):
        ww = f.measureText(wd)
        if cur and curw + sp + ww > maxw:
            rows.append(cur)
            cur, curw = [], 0
        cur.append((wi, wd, ww))
        curw += (sp if len(cur) > 1 else 0) + ww
    rows.append(cur)
    yy = y
    for row in rows:
        xx = x
        for wi, wd, ww in row:
            on = None
            for k, (a, b) in enumerate(hi):
                if a <= wi <= b:
                    span = b - a + 1
                    if (wi - a + 1) / span <= hi_u[k] + 1e-6:
                        on = k
            if on is not None:
                X.c.drawRect(skia.Rect(xx - 4, yy - size * 0.82, xx + ww + sp * 0.6, yy + size * 0.28),
                             X.paint("green" if on == 0 else "magenta", 0.28 * alpha))
            X.text(wd, xx, yy, size, ("white" if on is not None else color), kind="mono", align="left", alpha=alpha)
            xx += ww + sp
        yy += size * lh
    return yy
