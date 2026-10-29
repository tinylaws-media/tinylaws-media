"""SUBJECT ZERO — 2D look « estampe »: flat painted colour, paper grain, woodblock-print waves, an ink line that
boils a little (redrawn every 2 frames, like hand animation on twos). Everything drawn in code with skia.

Palette: Prussian blue, cream paper, coral sun, and Subject Zero's yellow hoodie as the only loud colour.
"""
import math
import os

import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 24
FONTS = os.path.join(HERE, "fonts")          # Open Font License fonts shipped with the toolkit


def rgb(h, a=1.0):
    h = h.lstrip("#")
    return skia.Color4f(int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


def mixc(c1, c2, k):
    return skia.Color4f(c1.fR + (c2.fR - c1.fR) * k, c1.fG + (c2.fG - c1.fG) * k, c1.fB + (c2.fB - c1.fB) * k,
                        c1.fA + (c2.fA - c1.fA) * k)


PAPER = rgb("#F1E5C9")
PAPER_HI = rgb("#F8F0DD")
INKC = rgb("#1B2238")
PRUSSIAN = rgb("#24456B")
CORAL = rgb("#E8704A")
SEAL = rgb("#C8402E")
FOAM = rgb("#F5ECD7")
YEL, YEL_D, YEL_L = rgb("#F4B62F"), rgb("#D7951C"), rgb("#FBD36A")
SKIN, SKIN_D = rgb("#F2B48E"), rgb("#D99270")
HAIR = rgb("#3B2420")
HAIR_L = rgb("#6A3F33")
BLUSH = rgb("#EE8A78")
WHITE = rgb("#FBF7EE")
DUCK, DUCK_D, BEAK = rgb("#FFD43B"), rgb("#E9AE1E"), rgb("#EE7F36")
SEA = [rgb(h) for h in ("#6C97A3", "#4E8197", "#3D6E8A", "#2E5B7C", "#244A6D", "#1C3C5E", "#163250", "#112842")]

_TF = {}


def font(name, size):
    path = {"bold": "BricolageGrotesque.ttf", "mono": "SpaceMono-Bold.ttf", "hand": "CaveatBrush-Regular.ttf",
            "display": "BagelFatOne-Regular.ttf"}[name]
    if path not in _TF:
        _TF[path] = skia.Typeface.MakeFromFile(os.path.join(FONTS, path))
    f = skia.Font(_TF[path], size)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def fill(col, alpha=1.0):
    p = skia.Paint(AntiAlias=True)
    p.setColor4f(skia.Color4f(col.fR, col.fG, col.fB, col.fA * alpha))
    return p


def ink(width=6.0, col=None, alpha=1.0, boil=None):
    """The ink line. `boil` = (frame index on twos, strength): the line wobbles a little differently every 2 frames."""
    col = col or INKC
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=width)
    p.setColor4f(skia.Color4f(col.fR, col.fG, col.fB, col.fA * alpha))
    p.setStrokeCap(skia.Paint.kRound_Cap)
    p.setStrokeJoin(skia.Paint.kRound_Join)
    if boil is not None:
        seed, k = boil
        p.setPathEffect(skia.DiscretePathEffect.Make(16.0, 1.3 * k, int(seed) & 0xFFFF))
    return p


def text(c, s, x, y, f, col, align="left", alpha=1.0, stroke=0.0, stroke_col=None):
    w = f.measureText(s)
    if align == "center":
        x -= w / 2
    elif align == "right":
        x -= w
    if stroke:
        p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=stroke)
        sc = stroke_col or INKC
        p.setColor4f(skia.Color4f(sc.fR, sc.fG, sc.fB, alpha))
        p.setStrokeJoin(skia.Paint.kRound_Join)
        c.drawString(s, x, y, f, p)
    c.drawString(s, x, y, f, fill(col, alpha))
    return w


def smooth_path(pts, closed=True):
    """Catmull-Rom through the points, as cubic Béziers."""
    p = skia.Path()
    n = len(pts)
    if n < 2:
        return p
    p.moveTo(*pts[0])
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        p.cubicTo(*c1, *c2, *p2)
    if closed:
        p.close()
    return p


def rrect(x, y, w, h, r):
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r))
    return p


def oval(cx, cy, rx, ry):
    p = skia.Path()
    p.addOval(skia.Rect.MakeLTRB(cx - rx, cy - ry, cx + rx, cy + ry))
    return p


def ease_io(k):
    k = min(1.0, max(0.0, k))
    return k * k * (3 - 2 * k)


def prog(t, a, b):
    return min(1.0, max(0.0, (t - a) / (b - a))) if b > a else float(t >= a)


# ---------------------------------------------------------------- paper and texture
_GRAIN = {}


def grain_image(seed=0):
    """A paper sheet: fibres + mottling, made once, multiplied over every frame."""
    if seed in _GRAIN:
        return _GRAIN[seed]
    rng = np.random.default_rng(seed)
    s = skia.Surface(W, H)
    c = s.getCanvas()
    c.clear(skia.Color4f(1, 1, 1, 1))
    p = skia.Paint()
    p.setShader(skia.PerlinNoiseShader.MakeFractalNoise(0.004, 0.004, 4, seed))
    p.setAlphaf(0.10)
    c.drawRect(skia.Rect.MakeWH(W, H), p)
    p2 = skia.Paint()
    p2.setShader(skia.PerlinNoiseShader.MakeFractalNoise(0.35, 0.35, 2, seed + 1))
    p2.setAlphaf(0.10)
    c.drawRect(skia.Rect.MakeWH(W, H), p2)
    fib = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0)
    for _ in range(900):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        a = rng.uniform(0, math.pi)
        ln = rng.uniform(6, 22)
        fib.setColor4f(skia.Color4f(0.45, 0.38, 0.28, rng.uniform(0.05, 0.14)))
        c.drawLine(x, y, x + math.cos(a) * ln, y + math.sin(a) * ln, fib)
    img = s.makeImageSnapshot()
    _GRAIN[seed] = img
    return img


def paper_over(c, alpha=1.0):
    p = skia.Paint()
    p.setBlendMode(skia.BlendMode.kMultiply)
    p.setAlphaf(alpha)
    c.drawImage(grain_image(), 0, 0, skia.SamplingOptions(), p)


def mottle(c, path, col, alpha=0.18, scale=0.012, seed=3):
    """Gouache unevenness inside a flat shape."""
    c.save()
    c.clipPath(path, doAntiAlias=True)
    p = skia.Paint()
    p.setShader(skia.PerlinNoiseShader.MakeTurbulence(scale, scale * 1.6, 3, seed))
    p.setBlendMode(skia.BlendMode.kMultiply)
    p.setAlphaf(alpha)
    c.drawPath(path, p)
    c.restore()


def vignette(c, k=0.35):
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeRadial((W / 2, H * 0.46), H * 0.75,
                                                [skia.Color4f(0, 0, 0, 0), skia.Color4f(0.06, 0.05, 0.10, k)], [0.55, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)


# ---------------------------------------------------------------- sky
def sky(c, t, horizon=740, sun=(780, 470), sun_r=105):
    c.drawRect(skia.Rect.MakeWH(W, horizon + 10), fill(PAPER))
    # bokashi: the band of blue printed at the top of the sheet
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeLinear([(0, 0), (0, horizon * 0.72)],
                                                [mixc(PRUSSIAN, PAPER, 0.05), skia.Color4f(PRUSSIAN.fR, PRUSSIAN.fG, PRUSSIAN.fB, 0)]))
    c.drawRect(skia.Rect.MakeWH(W, horizon), p)
    # warm glow near the horizon
    g = skia.Paint()
    g.setShader(skia.GradientShader.MakeLinear([(0, horizon - 220), (0, horizon)],
                                                [skia.Color4f(1, 0.8, 0.6, 0), skia.Color4f(0.98, 0.74, 0.55, 0.35)]))
    c.drawRect(skia.Rect.MakeXYWH(0, horizon - 220, W, 220), g)
    if sun:
        sp = oval(sun[0], sun[1], sun_r, sun_r)
        c.drawPath(sp, fill(CORAL))
        mottle(c, sp, CORAL, alpha=0.12, scale=0.03)


def mist_band(c, x, y, w, h, alpha=0.92, col=None):
    """Suyari-gasumi: the long rounded mist bands of woodblock prints, drifting across the sky."""
    col = col or PAPER_HI
    path = rrect(x, y, w, h, h / 2)
    # scalloped top edge
    n = max(2, int(w / (h * 1.1)))
    for i in range(n):
        cx = x + h * 0.6 + i * (w - h * 1.2) / max(1, n - 1)
        path.addOval(skia.Rect.MakeLTRB(cx - h * 0.55, y - h * 0.35, cx + h * 0.55, y + h * 0.55))
    c.drawPath(path, fill(col, alpha))
    return path


def iss(c, x, y, s=1.0, alpha=1.0, glint=0.0, light=False):
    """The space station as a woodblock silhouette: the long truss, four pairs of wide gold solar wings, white
    radiators and the row of modules across the middle. light=True for a night sky (pale lines on dark)."""
    line = FOAM if light else INKC
    gold, gold_d = (rgb("#E0AE4E"), rgb("#A77A2C")) if light else (rgb("#C9973E"), rgb("#8E6524"))
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    if light:
        g = skia.Paint(AntiAlias=True)
        g.setShader(skia.GradientShader.MakeRadial((0, 0), 90, [skia.Color4f(1, 0.95, 0.8, 0.35 * alpha), skia.Color4f(1, 1, 1, 0)]))
        c.drawCircle(0, 0, 90, g)
    # the truss
    c.drawRect(skia.Rect.MakeXYWH(-58, -2, 116, 4), fill(FOAM if light else rgb("#D8D4CC"), alpha))
    c.drawRect(skia.Rect.MakeXYWH(-58, -2, 116, 4), ink(1.2, col=line, alpha=alpha))
    # four pairs of solar wings (each wing a long gold panel with cell lines)
    for px in (-50, -38, 38, 50):
        for sy in (-1, 1):
            r = skia.Rect.MakeXYWH(px - 4.5, 3 if sy > 0 else -27, 9, 24)
            c.drawRect(r, fill(gold, alpha))
            for k in range(1, 4):
                yy = r.top() + r.height() * k / 4
                c.drawLine(r.left(), yy, r.right(), yy, ink(0.8, col=gold_d, alpha=alpha))
            c.drawRect(r, ink(1.2, col=line, alpha=alpha))
    # radiators (white, angled) and the modules
    for px in (-20, 20):
        r = skia.Rect.MakeXYWH(px - 3, -14, 6, 12)
        c.drawRect(r, fill(WHITE, alpha))
        c.drawRect(r, ink(1.0, col=line, alpha=alpha))
    mod = rrect(-12, -5, 24, 10, 4)
    c.drawPath(mod, fill(WHITE, alpha))
    c.drawPath(mod, ink(1.2, col=line, alpha=alpha))
    c.drawPath(rrect(-4, -12, 8, 24, 3), fill(WHITE, alpha))
    c.drawPath(rrect(-4, -12, 8, 24, 3), ink(1.2, col=line, alpha=alpha))
    if glint > 0:
        g = skia.Paint(AntiAlias=True)
        g.setShader(skia.GradientShader.MakeRadial((0, 0), 60, [skia.Color4f(1, 0.98, 0.9, 0.85 * glint), skia.Color4f(1, 1, 1, 0)]))
        c.drawCircle(0, 0, 60, g)
    c.restore()


def woodgrain(c, path, alpha=0.10, seed=5, fx=0.0016, fy=0.045):
    """Wood grain printed through a flat colour: long horizontal streaks (very different x and y frequencies)."""
    c.save()
    c.clipPath(path, doAntiAlias=True)
    p = skia.Paint()
    p.setShader(skia.PerlinNoiseShader.MakeFractalNoise(fx, fy, 2, seed))
    p.setBlendMode(skia.BlendMode.kMultiply)
    p.setAlphaf(alpha)
    c.drawPath(path, p)
    c.restore()


# ---------------------------------------------------------------- sea
class Sea:
    """Layered woodblock waves. Layer i has a base line, an amplitude and a speed; nearer = darker, bigger, faster."""

    def __init__(self, horizon=740, seed=5, layers=None):
        rng = np.random.default_rng(seed)
        self.horizon = horizon
        self.layers = layers or [
            (horizon + 22, 4, 0.20), (horizon + 62, 8, 0.28), (horizon + 120, 13, 0.36), (horizon + 205, 20, 0.45),
            (horizon + 330, 30, 0.55), (horizon + 520, 46, 0.70), (horizon + 800, 66, 0.85), (horizon + 1120, 86, 1.0)]
        self.ph = [rng.uniform(0, 6.28, 4) for _ in self.layers]
        self.xs = np.linspace(-40, W + 40, 120)

    def height(self, i, x, t, storm=0.0):
        y0, amp, sp = self.layers[i]
        amp = amp * (1 + 1.6 * storm)
        ph = self.ph[i]
        wl = 1.0 / (1 + 0.6 * i)
        k = 2 * math.pi / (520 * (0.55 + 0.25 * i) )
        v = (np.sin(k * x + ph[0] + t * 1.3 * sp) * 0.55 + np.sin(2.1 * k * x + ph[1] - t * 1.9 * sp) * 0.28
             + np.sin(4.3 * k * x + ph[2] + t * 2.6 * sp) * 0.17)
        return y0 - amp * v * (1 + 0 * wl)

    def draw_layer(self, c, i, t, boil, storm=0.0, foam=True):
        y = self.height(i, self.xs, t, storm)
        pts = list(zip(self.xs.tolist(), y.tolist()))
        path = smooth_path(pts, closed=False)
        path.lineTo(W + 40, H + 40)
        path.lineTo(-40, H + 40)
        path.close()
        col = SEA[min(i, len(SEA) - 1)]
        c.drawPath(path, fill(col))
        mottle(c, path, col, alpha=0.10 + 0.02 * i, scale=0.006 + 0.002 * i, seed=11 + i)
        woodgrain(c, path, alpha=0.08 + 0.012 * i, seed=21 + i)
        # engraved lines: the crest repeated inside the wave, a little lighter
        if i >= 2:
            for j, (dy, a) in enumerate(((14 + 4 * i, 0.22), (30 + 8 * i, 0.13))):
                lp = smooth_path([(x, yy + dy + 4 * math.sin(x * 0.01 + j)) for x, yy in pts], closed=False)
                c.drawPath(lp, ink(2.0 + 0.4 * i, col=FOAM, alpha=a))
        if foam and i >= 1:
            self._foam(c, pts, i, t, boil, storm)
        c.drawPath(smooth_path(pts, closed=False), ink(2.0 + 0.6 * i, alpha=0.85, boil=boil))
        return y

    def _foam(self, c, pts, i, t, boil, storm):
        ys = np.array([p[1] for p in pts])
        xs = np.array([p[0] for p in pts])
        # crest = local minima of y (screen y down), foam caps on each
        for j in range(2, len(ys) - 2):
            if ys[j] < ys[j - 1] and ys[j] <= ys[j + 1] and ys[j] < self.layers[i][0] - self.layers[i][1] * 0.05:
                w = (46 + 22 * i) * (1 + storm)
                seg = [(x, y) for x, y in pts if abs(x - xs[j]) < w]
                if len(seg) < 3:
                    continue
                th = 6 + 2.6 * i
                cap = skia.Path()
                cap.moveTo(*seg[0])
                for x, y in seg[1:]:
                    cap.lineTo(x, y)
                for x, y in reversed(seg):
                    d = 1 - abs(x - xs[j]) / w
                    cap.lineTo(x, y + th * d * 1.6)
                cap.close()
                c.drawPath(cap, fill(FOAM, 0.95))
                if i >= 4:   # the claws of a woodblock crest
                    for k in range(3):
                        cx = xs[j] + (k - 1) * w * 0.33
                        cy = np.interp(cx, xs, ys)
                        r = 7 + 1.5 * i
                        claw = skia.Path()
                        claw.moveTo(cx - r, cy + 1)
                        claw.quadTo(cx - r * 0.2, cy - r * 1.3, cx + r, cy - r * 0.2)
                        claw.quadTo(cx + r * 0.1, cy - r * 0.4, cx - r * 0.2, cy + r * 0.5)
                        claw.close()
                        c.drawPath(claw, fill(FOAM))
                        c.drawPath(claw, ink(2.0, alpha=0.8, boil=boil))


# ---------------------------------------------------------------- Subject Zero
MOUTHS = {
    # name: list of (x, y) control points around the mouth, relative to the mouth centre, in head units (head = 100)
    "smile": [(-16, -2), (0, 5), (16, -2), (0, 9)],
    "flat": None,
    "o": None,
    "open": None,
    "wavy": None,
}

FACES = {
    #           brow tilt, brow lift, look (x, y), mouth, mouth size, lids
    "neutral": (0, 0, (0, 0), "flat", 1.0, 0.0),
    "worried": (14, 4, (0, 2), "wavy", 0.8, 0.0),
    "panic":   (22, 8, (0, 0), "open", 1.35, 0.0),
    "deadpan": (0, -5, (0, 4), "flat", 0.9, 0.45),
    "smug":    (-12, 0, (5, 0), "smirk", 1.0, 0.35),
    "shock":   (6, 11, (0, 0), "o", 1.0, 0.0),
    "up":      (10, 8, (0, -9), "o", 0.7, 0.0),
    "cold":    (16, 3, (0, 2), "chatter", 1.1, 0.15),
    "happy":   (-4, 4, (0, 0), "grin", 1.1, 0.0),
    "nope":    (-24, -6, (0, 0), "open", 1.7, 0.2),
    "smile":   (-2, 3, (0, 0), "grin", 0.8, 0.0),
}


def draw_hero(c, cx, cy, s=1.0, face="neutral", boil=None, arms="paddle", t=0.0, blink=0.0, squash=0.0, tilt=0.0,
              look=None, shiver=0.0, mouth_open=None):
    """Subject Zero, chest up (she's in water). (cx, cy) = centre of the head; s = 1 -> head 210 px wide.
    squash > 0 squashes (impact), < 0 stretches (surprise)."""
    bt, bl, lk, mouth, msz, lid = FACES[face]
    if look is not None:
        lk = look
    c.save()
    c.translate(cx + (math.sin(t * 60) * 3 * shiver), cy)
    c.rotate(tilt)
    sy = 1 - 0.18 * squash
    sx = 1 + 0.14 * squash
    c.scale(s * sx, s * sy)
    L = ink(6.0 / s, boil=boil)
    # --- the bun and the hair behind the head (her silhouette: readable even tiny)
    bun = oval(6, -176, 60, 54)
    c.drawPath(bun, fill(HAIR))
    for k in (0, 1):
        arc = skia.Path()
        arc.addArc(skia.Rect.MakeLTRB(-34 + 12 * k, -214 + 10 * k, 46 - 8 * k, -140 - 6 * k), 200, 120)
        c.drawPath(arc, ink(3.5 / s, col=HAIR_L, boil=boil))
    c.drawPath(bun, L)
    # --- hood behind the head
    hood = smooth_path([(-120, 60), (-128, -40), (-70, -118), (70, -118), (128, -40), (120, 60), (0, 92)])
    c.drawPath(hood, fill(YEL_D))
    c.drawPath(hood, L)
    back = smooth_path([(-112, 52), (-116, -40), (-92, -110), (-30, -138), (40, -136), (98, -106), (118, -40), (112, 52),
                        (92, 64), (96, -10), (0, -60), (-96, -10), (-92, 64)])
    c.drawPath(back, fill(HAIR))
    c.drawPath(back, L)
    tie = oval(6, -128, 36, 11)
    c.drawPath(tie, fill(CORAL))
    c.drawPath(tie, ink(4.0 / s, boil=boil))
    # --- torso (hoodie), cut by the water in the frame anyway
    torso = smooth_path([(-150, 170), (-118, 120), (-60, 108), (60, 108), (118, 120), (150, 170), (168, 330), (-168, 330)])
    c.drawPath(torso, fill(YEL))
    shade = smooth_path([(60, 108), (118, 120), (150, 170), (168, 330), (70, 330), (88, 180)])
    c.drawPath(shade, fill(YEL_D, 0.55))
    mottle(c, torso, YEL, alpha=0.10, scale=0.05)
    c.drawPath(torso, L)
    # drawstrings
    for x in (-26, 26):
        sp = skia.Path()
        sp.moveTo(x, 112)
        sp.cubicTo(x + 2, 140, x - 4, 160, x + 1, 186)
        c.drawPath(sp, ink(5.0 / s, col=FOAM, boil=boil))
        c.drawCircle(x + 1, 190, 5, fill(FOAM))
    # the "0" patch
    c.drawCircle(-80, 200, 22, fill(CORAL))
    c.drawCircle(-80, 200, 22, ink(4.0 / s, boil=boil))
    text(c, "0", -80, 211, font("display", 30), FOAM, align="center")
    # --- arms
    _arms(c, arms, t, L, s, boil)
    # --- neck + head
    c.drawPath(rrect(-30, 70, 60, 50, 18), fill(SKIN_D))
    head = smooth_path([(-100, -6), (-96, -78), (-62, -104), (0, -110), (62, -104), (96, -78), (100, -6), (90, 62),
                        (44, 92), (-44, 92), (-90, 62)])
    c.drawPath(head, fill(SKIN))
    hshade = smooth_path([(62, -104), (96, -78), (100, -6), (90, 62), (44, 92), (70, 30), (78, -40)])
    c.drawPath(hshade, fill(SKIN_D, 0.5))
    c.drawPath(head, L)
    # fringe swept to one side, and two locks framing the face
    fringe = smooth_path([(-104, -14), (-104, -80), (-62, -120), (8, -128), (74, -110), (106, -66), (104, -24),
                          (84, -54), (46, -64), (6, -84), (-22, -60), (-58, -56), (-86, -38)])
    c.drawPath(fringe, fill(HAIR))
    c.drawPath(smooth_path([(-30, -110), (10, -100), (44, -80)], closed=False), ink(3.0 / s, col=HAIR_L, boil=boil))
    c.drawPath(fringe, L)
    for side in (-1, 1):
        lock = smooth_path([(side * 100, -40), (side * 110, 10), (side * 104, 66), (side * 92, 80), (side * 90, 30), (side * 88, -24)])
        c.drawPath(lock, fill(HAIR))
        c.drawPath(lock, L)
    # --- face
    for side in (-1, 1):
        ex, ey = side * 40, 2
        # whites
        w = oval(ex, ey, 27, 32 * (1 - 0.9 * blink))
        c.drawPath(w, fill(WHITE))
        c.drawPath(w, ink(4.5 / s, boil=boil))
        if blink < 0.7:
            c.save()
            c.clipPath(w, doAntiAlias=True)
            px, py = ex + lk[0] * 1.4, ey + lk[1] * 1.4
            c.drawCircle(px, py, 13, fill(INKC))
            c.drawCircle(px + 5, py - 5, 4.5, fill(WHITE))
            if lid > 0:
                c.drawRect(skia.Rect.MakeLTRB(ex - 30, ey - 34, ex + 30, ey - 34 + 66 * lid), fill(SKIN))
                c.drawLine(ex - 30, ey - 34 + 66 * lid, ex + 30, ey - 34 + 66 * lid, ink(4.5 / s))
            c.restore()
        # brows
        by = ey - 46 - bl
        br = skia.Path()
        a = math.radians(bt) * side
        x0, x1 = ex - 22, ex + 22
        y0 = by + (x0 - ex) * math.tan(a) * 0.9
        y1 = by + (x1 - ex) * math.tan(a) * 0.9
        br.moveTo(x0, y0)
        br.lineTo(x1, y1)
        c.drawPath(br, ink(11.0 / s, col=HAIR, boil=boil))
        # lashes: one flick at the outer corner
        lf = skia.Path()
        lf.moveTo(ex + side * 22, ey - 22 * (1 - 0.9 * blink))
        lf.quadTo(ex + side * 32, ey - 28, ex + side * 36, ey - 38)
        c.drawPath(lf, ink(4.5 / s, boil=boil))
        # blush and freckles
        c.drawPath(oval(side * 62, 40, 14, 7), fill(BLUSH, 0.7))
        for (fx, fy) in ((50, 30), (60, 24), (68, 32)):
            c.drawCircle(side * fx, fy, 2.4, fill(SKIN_D))
    # nose
    nose = skia.Path()
    nose.moveTo(-4, 18)
    nose.quadTo(-12, 36, 2, 38)
    c.drawPath(nose, ink(4.5 / s, col=mixc(SKIN_D, INKC, 0.4), boil=boil))
    _mouth(c, mouth if mouth_open is None else "open", msz if mouth_open is None else mouth_open, t, s, boil)
    c.restore()


def _mouth(c, kind, k, t, s, boil):
    my = 60
    L = ink(5.0 / s, boil=boil)
    if kind == "flat":
        p = skia.Path()
        p.moveTo(-18 * k, my)
        p.quadTo(0, my + 3, 18 * k, my)
        c.drawPath(p, L)
    elif kind == "wavy":
        p = skia.Path()
        p.moveTo(-20 * k, my + 2)
        p.cubicTo(-10 * k, my - 6, -4 * k, my + 8, 4 * k, my + 1)
        p.cubicTo(10 * k, my - 6, 16 * k, my + 6, 20 * k, my + 1)
        c.drawPath(p, L)
    elif kind == "chatter":
        p = skia.Path()
        p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-22 * k, my - 7, 22 * k, my + 7), 6, 6))
        c.drawPath(p, fill(WHITE))
        for x in range(-14, 16, 9):
            c.drawLine(x * k, my - 7, x * k, my + 7, ink(2.5 / s))
        c.drawPath(p, L)
    elif kind in ("open", "o", "grin"):
        if kind == "o":
            p = oval(0, my + 4, 10 * k, 13 * k)
        elif kind == "grin":
            p = skia.Path()
            p.moveTo(-26 * k, my - 4)
            p.quadTo(0, my - 2, 26 * k, my - 4)
            p.quadTo(0, my + 26 * k, -26 * k, my - 4)
            p.close()
        else:
            p = smooth_path([(-24 * k, my - 6), (0, my - 10), (24 * k, my - 6), (16 * k, my + 22 * k), (0, my + 28 * k),
                             (-16 * k, my + 22 * k)])
        c.drawPath(p, fill(rgb("#7A2230")))
        if kind != "o":
            c.save()
            c.clipPath(p, doAntiAlias=True)
            c.drawPath(oval(0, my + 26 * k, 16 * k, 10 * k), fill(rgb("#E46A6A")))
            if kind == "grin":
                c.drawRect(skia.Rect.MakeLTRB(-30 * k, my - 8, 30 * k, my + 3), fill(WHITE))
            c.restore()
        c.drawPath(p, L)
    elif kind == "smirk":
        p = skia.Path()
        p.moveTo(-16 * k, my + 2)
        p.quadTo(4, my + 4, 20 * k, my - 6)
        c.drawPath(p, L)


def _arms(c, mode, t, L, s, boil=None):
    """Rubber-hose arms from the shoulders. paddle: hands sweeping at the waterline; up: both arms waving;
    point: right arm pointing up."""
    for side in (-1, 1):
        sx, sy = side * 128, 150
        if mode == "paddle":
            ph = t * 5.0 + (0 if side < 0 else math.pi)
            hx, hy = side * (200 + 18 * math.sin(ph)), 250 + 14 * math.cos(ph)
            mx, my = side * 190, 160
        elif mode == "up" or (mode == "point" and side > 0):
            ph = t * 9.0 + (0 if side < 0 else 1.7)
            hx, hy = side * (170 + 26 * math.sin(ph)), -170 + 16 * math.cos(ph)
            if mode == "point":
                hx, hy = 150, -210
            mx, my = side * 200, 30
        elif mode == "swim":         # front crawl, seen from the front: one arm over, the other pulling
            ph = t * 7.0 + (0 if side < 0 else math.pi)
            hx, hy = side * (150 + 70 * math.cos(ph)), 60 - 200 * max(0.0, math.sin(ph))
            mx, my = side * (210 + 30 * math.cos(ph)), 80 - 120 * max(0.0, math.sin(ph))
        elif mode == "limp":         # arms gave up: hanging, a little noodly
            hx, hy = side * (176 + 6 * math.sin(t * 3 + side)), 330
            mx, my = side * 236, 210
        elif mode == "hug":
            hx, hy = side * 60, 230 + 6 * math.sin(t * 40)
            mx, my = side * 170, 230
        else:
            hx, hy = side * 180, 280
            mx, my = side * 190, 200
        a = skia.Path()
        a.moveTo(sx, sy)
        a.quadTo(mx, my, hx, hy)
        c.drawPath(a, ink(44.0 + 12.0 / s, boil=boil))
        c.drawPath(a, ink(44.0, col=YEL_D if side > 0 else YEL))
        hand = oval(hx, hy, 24, 22)
        c.drawPath(hand, fill(SKIN))
        c.drawPath(hand, L)
        if mode == "point" and side > 0:
            f = rrect(hx - 7, hy - 50, 14, 40, 7)
            c.drawPath(f, fill(SKIN))
            c.drawPath(f, L)


def draw_duck(c, cx, cy, s=1.0, boil=None, tilt=0.0, look=0.0, quack=0.0):
    c.save()
    c.translate(cx, cy)
    c.rotate(tilt)
    c.scale(s, s)
    if boil is not None and s > 1.5:
        boil = (boil[0], boil[1] / s)        # the wobble is in drawing units: keep it small when the duck is huge
    L = ink(5.0 / s, boil=boil)
    body = smooth_path([(-58, 0), (-50, -34), (-6, -42), (40, -36), (66, -10), (50, 18), (-40, 18)])
    tail = smooth_path([(-50, -6), (-70, -26), (-76, -46), (-62, -40), (-54, -26), (-44, -16)])
    c.drawPath(tail, fill(DUCK))
    c.drawPath(tail, L)
    c.drawPath(body, fill(DUCK))
    c.drawPath(smooth_path([(-30, -10), (10, -26), (30, -6), (-6, 6)]), fill(DUCK_D, 0.7))
    c.drawPath(body, L)
    head = oval(34, -62, 30, 28)
    c.drawPath(head, fill(DUCK))
    c.drawPath(head, L)
    beak = skia.Path()
    beak.moveTo(58, -62)
    beak.quadTo(86, -64 - 6 * quack, 90, -54)
    beak.quadTo(78, -44 + 8 * quack, 58, -50)
    beak.close()
    c.drawPath(beak, fill(BEAK))
    c.drawPath(beak, L)
    c.drawCircle(42 + 4 * look, -70, 6, fill(INKC))
    c.drawCircle(44 + 4 * look, -72, 2, fill(WHITE))
    c.restore()


# ---------------------------------------------------------------- HUD & captions (estampe grammar)
SAFE_X0, SAFE_X1 = 120, 780
CAP_CX = (SAFE_X0 + SAFE_X1) / 2


def seal(c, x, y, size=86, label="0", alpha=1.0):
    """The red hanko seal: the series' signature in the corner of every frame."""
    p = rrect(x, y, size, size, 10)
    c.drawPath(p, fill(SEAL, alpha))
    mottle(c, p, SEAL, alpha=0.25, scale=0.08)
    c.drawPath(rrect(x + 7, y + 7, size - 14, size - 14, 6), ink(3, col=FOAM, alpha=alpha))
    text(c, label, x + size / 2, y + size * 0.72, font("display", size * 0.62), FOAM, align="center", alpha=alpha)


def hud_card(c, x, y, rows, alpha=1.0, w=560):
    """A cream cartouche, like the title panel of a woodblock print: double ink border, notched corners.
    rows = [(label, value, colour, pulse)]. Labels at 30 px, values at 48 px (readable on a phone)."""
    hgt = 30 + 78 * len(rows)
    card = rrect(x, y, w, hgt, 14)
    sh = rrect(x + 8, y + 10, w, hgt, 14)
    c.drawPath(sh, fill(INKC, 0.25 * alpha))
    c.drawPath(card, fill(PAPER_HI, 0.96 * alpha))
    mottle(c, card, PAPER, alpha=0.12 * alpha, scale=0.03, seed=8)
    c.drawPath(card, ink(4, alpha=alpha))
    c.drawPath(rrect(x + 8, y + 8, w - 16, hgt - 16, 9), ink(1.6, alpha=0.7 * alpha))
    for cx_, cy_ in ((x + 8, y + 8), (x + w - 8, y + 8), (x + 8, y + hgt - 8), (x + w - 8, y + hgt - 8)):
        c.drawCircle(cx_, cy_, 5, fill(SEAL, alpha))
    yy = y + 22
    for label, value, col, pulse in rows:
        text(c, label, x + 26, yy + 30, font("mono", 32), mixc(INKC, PAPER, 0.3), alpha=alpha)
        f = font("mono", 48 * (1 + 0.08 * pulse))
        text(c, value, x + w - 26, yy + 56, f, col or INKC, align="right", alpha=alpha)
        yy += 78


def words_caption(c, words, active, y=1190, size=76, alpha=1.0):
    f = font("bold", size)
    sp = f.measureText(" ")
    widths = [f.measureText(w) for w in words]
    tw = sum(widths) + sp * (len(words) - 1)
    scale = min(1.0, (SAFE_X1 - SAFE_X0) / max(1, tw))
    if scale < 1.0:
        f = font("bold", size * scale)
        sp = f.measureText(" ")
        widths = [f.measureText(w) for w in words]
        tw = sum(widths) + sp * (len(words) - 1)
    x = CAP_CX - tw / 2
    for i, (w, ww) in enumerate(zip(words, widths)):
        col = YEL_L if i == active else (CORAL if any(ch.isdigit() for ch in w) else FOAM)
        text(c, w, x, y, f, col, alpha=alpha, stroke=14)
        x += ww + sp


# ---------------------------------------------------------------- mountains, snow, rock (added for #02 Everest)
SNOW, SNOW_SH, SNOW_D = rgb("#F7F2E6"), rgb("#B8C8D8"), rgb("#8EA6BF")
ROCK, ROCK_D = rgb("#6E7A8A"), rgb("#4C5666")
LIME, LIME_D, LIME_L = rgb("#B3A68C"), rgb("#8C7F67"), rgb("#D2C6AA")
ALPINE_SKY = [rgb("#132A47"), rgb("#24456B"), rgb("#5F86A8")]


def alpine_sky(c, t, horizon=900, stars=0.0, sun=None, sun_r=70):
    """The sky up high: deep Prussian at the top (thin air), a pale bokashi band near the horizon."""
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeLinear([(0, 0), (0, horizon)],
                                                [ALPINE_SKY[0], ALPINE_SKY[1], mixc(ALPINE_SKY[2], PAPER, 0.55)], [0.0, 0.55, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, horizon + 4), p)
    c.drawRect(skia.Rect.MakeXYWH(0, horizon, W, H - horizon), fill(mixc(ALPINE_SKY[2], PAPER, 0.55)))
    if stars > 0:
        rng = np.random.default_rng(17)
        for _ in range(60):
            x, y = rng.uniform(0, W), rng.uniform(0, horizon * 0.55)
            k = 0.5 + 0.5 * math.sin(t * rng.uniform(1.5, 4) + x)
            c.drawCircle(x, y, rng.uniform(1.4, 3.0), fill(FOAM, stars * (0.35 + 0.45 * k)))
    if sun:
        g = skia.Paint(AntiAlias=True)
        g.setShader(skia.GradientShader.MakeRadial(sun, sun_r * 2.6, [skia.Color4f(1, 0.93, 0.8, 0.45), skia.Color4f(1, 1, 1, 0)]))
        c.drawCircle(sun[0], sun[1], sun_r * 2.6, g)
        sp = oval(sun[0], sun[1], sun_r, sun_r)
        c.drawPath(sp, fill(rgb("#FBE7C2")))
        mottle(c, sp, CORAL, alpha=0.10, scale=0.03)


def peak(c, pts, col=None, snow_y=None, boil=None, light_left=True, seed=1, hatch=True, line=4.0, alpha=1.0):
    """A woodblock mountain: pts = the skyline from left to right (x, y); it is closed down to the bottom of the
    frame. The sunlit side is cream snow, the other side blue snow (split at the highest point); rock below snow_y.
    Hatching = the carved lines of a print, following the slope."""
    col = col or ROCK
    top = min(pts, key=lambda p: p[1])
    path = smooth_path(pts, closed=False)
    path.lineTo(pts[-1][0], H + 50)
    path.lineTo(pts[0][0], H + 50)
    path.close()
    c.drawPath(path, fill(col, alpha))
    mottle(c, path, col, alpha=0.16 * alpha, scale=0.01, seed=seed)
    c.save()
    c.clipPath(path, doAntiAlias=True)
    if snow_y is not None:     # the snow mantle: everything above snow_y, ragged lower edge
        rng = np.random.default_rng(seed)
        edge = []
        for i, x in enumerate(np.linspace(pts[0][0], pts[-1][0], 26)):
            edge.append((float(x), snow_y + rng.uniform(-40, 70) + (abs(x - top[0]) * 0.12)))
        sn = skia.Path()
        sn.moveTo(pts[0][0], -10)
        sn.lineTo(pts[-1][0], -10)
        for x, y in reversed(edge):
            sn.lineTo(x, y)
        sn.close()
        c.drawPath(sn, fill(SNOW, alpha))
        # shadow side
        sh = skia.Path()
        if light_left:
            sh.moveTo(top[0], top[1] - 5)
            sh.lineTo(pts[-1][0] + 10, -10 + 0 * top[1])
            sh.lineTo(pts[-1][0] + 10, H + 50)
            sh.lineTo(top[0] + 30, H + 50)
            sh.cubicTo(top[0] + 60, top[1] + 400, top[0] - 10, top[1] + 160, top[0], top[1] - 5)
        else:
            sh.moveTo(top[0], top[1] - 5)
            sh.lineTo(pts[0][0] - 10, -10)
            sh.lineTo(pts[0][0] - 10, H + 50)
            sh.lineTo(top[0] - 30, H + 50)
            sh.cubicTo(top[0] - 60, top[1] + 400, top[0] + 10, top[1] + 160, top[0], top[1] - 5)
        sh.close()
        c.drawPath(sh, fill(SNOW_SH, 0.85 * alpha))
        c.drawPath(sh, fill(ROCK_D, 0.18 * alpha))
    if hatch:                  # carved lines running down the faces
        rng = np.random.default_rng(seed + 7)
        for _ in range(int(abs(pts[-1][0] - pts[0][0]) / 26)):
            x = rng.uniform(pts[0][0], pts[-1][0])
            y0 = np.interp(x, [p[0] for p in pts], [p[1] for p in pts]) + rng.uniform(20, 80)
            ln = rng.uniform(40, 160)
            dx = (x - top[0]) * 0.25
            hp = skia.Path()
            hp.moveTo(x, y0)
            hp.quadTo(x + dx * 0.5, y0 + ln * 0.5, x + dx, y0 + ln)
            c.drawPath(hp, ink(2.2, col=INKC, alpha=0.22 * alpha))
    c.restore()
    c.drawPath(smooth_path(pts, closed=False), ink(line, alpha=0.9 * alpha, boil=boil))
    return path


def snow_plume(c, x, y, t, strength=1.0, length=520, alpha=1.0, direction=1):
    """The plume of blown snow streaming off a summit (the jet stream made visible). direction 1 = to the right."""
    if strength <= 0:
        return
    rng = np.random.default_rng(23)
    for i in range(14):
        ph = (t * (0.9 + 0.5 * strength) + i / 14) % 1.0
        ln = length * strength * (0.4 + 0.6 * rng.uniform())
        px = x + direction * ph * ln
        py = y - 10 + rng.uniform(-30, 30) - 60 * ph * (0.5 + rng.uniform() * 0.5)
        w = 26 + 90 * ph
        h = 14 + 34 * ph
        c.drawPath(oval(px, py, w, h), fill(SNOW, alpha * 0.8 * (1 - ph) * min(1.0, strength * 1.4)))
    for j in range(5):         # wind lines, the woodblock way: long thin curved strokes
        ph = (t * 1.6 * (0.6 + strength) + j * 0.21) % 1.0
        x0 = x + direction * (ph * 700 - 120)
        yy = y - 120 + j * 46
        p = skia.Path()
        p.moveTo(x0, yy)
        p.cubicTo(x0 + direction * 90, yy - 18, x0 + direction * 170, yy + 14, x0 + direction * 260, yy - 4)
        c.drawPath(p, ink(3.0, col=FOAM, alpha=alpha * 0.75 * math.sin(ph * math.pi) * min(1.0, strength * 1.3)))


def snowfall(c, t, density=60, alpha=0.9, wind=0.0, seed=4, area=(0, 0, W, H)):
    rng = np.random.default_rng(seed)
    x0, y0, w, h = area
    for _ in range(density):
        bx, by, sp = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(40, 120)
        y = y0 + (by + t * sp) % h
        x = x0 + (bx + t * (20 + 400 * wind) + 14 * math.sin(t * 2 + bx)) % w
        r = rng.uniform(2, 5)
        if wind > 0.4:
            c.drawLine(x, y, x - 30 * wind, y - 4, ink(r * 0.9, col=SNOW, alpha=alpha))
        else:
            c.drawCircle(x, y, r, fill(SNOW, alpha))


def trilobite(c, x, y, s=1.0, rot=0.0, col=None, line=None, alpha=1.0, boil=None):
    """A trilobite fossil, the woodblock way: head shield, segmented body in three lobes, tail."""
    col = col or LIME_L
    line = line or LIME_D
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    body = smooth_path([(0, -70), (34, -62), (48, -38), (40, -10), (34, 30), (24, 58), (0, 70), (-24, 58), (-34, 30),
                        (-40, -10), (-48, -38), (-34, -62)])
    c.drawPath(body, fill(col, alpha))
    c.drawPath(body, ink(4 / s, col=line, alpha=alpha, boil=boil))
    c.drawPath(oval(0, -46, 15, 18), fill(mixc(col, line, 0.25), alpha))
    c.drawPath(oval(0, -46, 15, 18), ink(3 / s, col=line, alpha=alpha))
    for k in range(9):                 # thorax segments
        yy = -18 + k * 8.5
        hw = 38 - k * 2.6
        p = skia.Path()
        p.moveTo(-hw, yy)
        p.quadTo(0, yy + 6, hw, yy)
        c.drawPath(p, ink(2.6 / s, col=line, alpha=alpha))
    for side in (-1, 1):               # the three lobes
        p = skia.Path()
        p.moveTo(side * 12, -22)
        p.lineTo(side * 9, 60)
        c.drawPath(p, ink(2.6 / s, col=line, alpha=alpha))
        c.drawCircle(side * 24, -50, 5, fill(line, alpha))
    c.restore()


def crinoid(c, x, y, s=1.0, rot=0.0, col=None, line=None, alpha=1.0):
    """A sea lily fossil: a stalk of discs and a crown of feathery arms."""
    col = col or LIME_L
    line = line or LIME_D
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    for k in range(10):
        yy = 20 + k * 13
        c.drawPath(rrect(-9, yy, 18, 10, 4), fill(col, alpha))
        c.drawPath(rrect(-9, yy, 18, 10, 4), ink(2.2 / s, col=line, alpha=alpha))
    c.drawPath(oval(0, 8, 20, 16), fill(col, alpha))
    c.drawPath(oval(0, 8, 20, 16), ink(3 / s, col=line, alpha=alpha))
    for k in range(5):
        a = math.radians(-150 + k * 30)
        p = skia.Path()
        p.moveTo(0, 0)
        p.quadTo(math.cos(a) * 40, math.sin(a) * 70 - 10, math.cos(a) * 46 + (k - 2) * 6, math.sin(a) * 96)
        c.drawPath(p, ink(7 / s, col=col, alpha=alpha))
        c.drawPath(p, ink(2.2 / s, col=line, alpha=alpha))
    c.restore()


def shell_fossil(c, x, y, s=1.0, rot=0.0, col=None, line=None, alpha=1.0):
    """A brachiopod shell: a ribbed fan."""
    col = col or LIME_L
    line = line or LIME_D
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    p = smooth_path([(0, 26), (-38, 6), (-44, -22), (-22, -40), (0, -44), (22, -40), (44, -22), (38, 6)])
    c.drawPath(p, fill(col, alpha))
    for k in range(-4, 5):
        q = skia.Path()
        q.moveTo(0, 24)
        q.lineTo(k * 10, -40 + abs(k) * 4)
        c.drawPath(q, ink(2.0 / s, col=line, alpha=alpha))
    c.drawPath(p, ink(3 / s, col=line, alpha=alpha))
    c.restore()


def thermometer(c, x, y, h, frac, label=None, alpha=1.0, boil=None):
    """A glass thermometer, cream with a coral column: frac 0..1 of the tube filled. (x, y) = top of the tube."""
    tube = rrect(x - 22, y, 44, h, 22)
    c.drawPath(rrect(x - 14, y + 8, 44, h, 22), fill(INKC, 0.25 * alpha))
    c.drawPath(tube, fill(PAPER_HI, alpha))
    bulb = oval(x, y + h + 26, 44, 44)
    c.drawPath(bulb, fill(PRUSSIAN, alpha))
    col_h = max(0.0, min(1.0, frac)) * (h - 30)
    c.drawPath(rrect(x - 10, y + h - col_h, 20, col_h + 20, 10), fill(PRUSSIAN, alpha))
    for k in range(9):
        yy = y + 30 + k * (h - 60) / 8
        c.drawLine(x + 22, yy, x + (36 if k % 2 == 0 else 30), yy, ink(3, alpha=alpha))
    c.drawPath(tube, ink(4, alpha=alpha, boil=boil))
    c.drawPath(bulb, ink(4, alpha=alpha, boil=boil))
    if label:
        text(c, label, x, y - 24, font("mono", 32), INKC, align="center", alpha=alpha)
