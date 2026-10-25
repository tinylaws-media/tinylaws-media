"""NOT JUST YOU — drawing engine (skia).

A bedroom at night, painted in cold blues, with one warm light: the lamp (help, other people,
what holds). Lumen, a small moth, listens and reacts; he never speaks. Everything is calm:
fixed rain and grain, light that barely breathes, slow camera moves, no flashes, no shakes.

Palette and type come from the channel bible: night #0A0F1E, deep blue #18243A, amber #F2B35B,
faded rose #C9A7B8, cream #F3E9DA; Instrument Serif, roman and italic, never shouting capitals.
"""
import math
import os

import numpy as np
import skia

W, H, FPS = 1080, 1920, 24
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

NIGHT = (10, 15, 30)
DEEP = (24, 36, 58)
AMBER = (242, 179, 91)
ROSE = (201, 167, 184)
CREAM = (243, 233, 218)
COLD = (150, 178, 215)      # the phone's light: the one cold glow (derived from the blues)
MID = (40, 56, 84)          # furniture, a step lighter than DEEP
SAFE_TOP, SAFE_BOTTOM, SAFE_RIGHT = 230, 1450, 900


def rgb(c, a=1.0):
    return skia.Color4f(c[0] / 255, c[1] / 255, c[2] / 255, a)


def col(c, a=1.0):
    return skia.ColorSetARGB(int(255 * max(0, min(1, a))), *c)


def mix(c1, c2, x):
    return tuple(int(round(a + (b - a) * x)) for a, b in zip(c1, c2))


def clamp01(x):
    return max(0.0, min(1.0, x))


def prog(t, a, b):
    return clamp01((t - a) / (b - a)) if b > a else float(t >= a)


def smooth(x):
    x = clamp01(x)
    return x * x * (3 - 2 * x)


def ease_out(x, p=3):
    return 1 - (1 - clamp01(x)) ** p


def lerp(a, b, x):
    return a + (b - a) * x


# ------------------------------------------------------------------ fonts
_TF = {}


def typeface(name):
    if name not in _TF:
        f = {"serif": "InstrumentSerif-Regular.ttf", "italic": "InstrumentSerif-Italic.ttf"}[name]
        _TF[name] = skia.Typeface.MakeFromFile(os.path.join(FONT_DIR, f))
    return _TF[name]


def font(size, italic=False):
    f = skia.Font(typeface("italic" if italic else "serif"), size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def paint(c, a=1.0, stroke=None, blend=None):
    p = skia.Paint(AntiAlias=True, Color=col(c, a))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if blend:
        p.setBlendMode(blend)
    return p


def glow(c, x, y, r, color, a=1.0):
    """Soft radial light (additive-looking 'screen' blend)."""
    sh = skia.GradientShader.MakeRadial(
        (x, y), r, [col(color, a), col(color, a * 0.35), col(color, 0)], [0.0, 0.35, 1.0])
    p = skia.Paint(AntiAlias=True, Shader=sh, BlendMode=skia.BlendMode.kScreen)
    c.drawCircle(x, y, r, p)


def text(c, s, x, y, size, color=CREAM, a=1.0, italic=False, align="center"):
    f = font(size, italic)
    w = f.measureText(s)
    ox = {"center": -w / 2, "left": 0, "right": -w}[align]
    c.drawString(s, x + ox, y, f, paint(color, a))
    return w


# ------------------------------------------------------------------ rich lines: *word* = amber italic
def parse_rich(line):
    """'more *stress* later' -> [(word, emph)]; stars may wrap several words."""
    out, emph = [], False
    for tok in line.split(" "):
        if not tok:
            continue
        st = tok.startswith("*")
        if st:
            emph = True
            tok = tok[1:]
        en = tok.endswith("*") or tok.rstrip(".,?!:;").endswith("*")
        if en:
            tok = tok.replace("*", "")
        out.append((tok, emph))
        if en:
            emph = False
    return out


def rich_width(words, size):
    fr, fi = font(size), font(size, True)
    sp = fr.measureText(" ")
    return sum((fi if e else fr).measureText(w) for w, e in words) + sp * (len(words) - 1)


def draw_rich(c, line, cx, y, size, a=1.0, color=CREAM, accent=AMBER):
    words = parse_rich(line)
    fr, fi = font(size), font(size, True)
    sp = fr.measureText(" ")
    x = cx - rich_width(words, size) / 2
    for w, e in words:
        f = fi if e else fr
        c.drawString(w, x, y, f, paint(accent if e else color, a))
        x += f.measureText(w) + sp


class Caption:
    """One line of narration on screen: appears whole when the voice starts it, stays until the next
    line. " / " breaks the line (2 lines max, <= 5 words each)."""

    def __init__(self, t0, t1, txt, size=94):
        self.t0, self.t1, self.size = t0, t1, size
        self.lines = [s.strip() for s in txt.split(" / ")]
        assert len(self.lines) <= 2, txt
        for ln in self.lines:
            assert len(parse_rich(ln)) <= 5, ln

    def width(self):
        return max(rich_width(parse_rich(l), self.size) for l in self.lines)

    def draw(self, c, t, y=360, fade=0.18, first=False):
        if not (self.t0 - (0 if first else 0.0) <= t < self.t1):
            return
        a = 1.0 if first and self.t0 <= 0.05 else smooth(prog(t, self.t0, self.t0 + fade))
        a *= 1 - smooth(prog(t, self.t1 - 0.12, self.t1))
        size = self.size
        while self.width() * size / self.size > 2 * (SAFE_RIGHT - 540) - 6:
            size -= 2
        lh = size * 1.12
        n = len(self.lines)
        # soft night plate behind the words for legibility over any background
        wpl = self.width() * size / self.size + 90
        top = y - size * 0.95
        hgt = lh * (n - 1) + size * 1.45
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(540 - wpl / 2, top, wpl, hgt), 46, 46)
        p = skia.Paint(AntiAlias=True, Color=col(NIGHT, 0.55 * a))
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22))
        c.drawRRect(rr, p)
        for i, ln in enumerate(self.lines):
            draw_rich(c, ln, 540, y + i * lh, size, a)
        return y + (n - 1) * lh


def source_line(c, s, y, a=1.0):
    """Every figure shows its source in small type under the sentence (bible)."""
    size = 40
    while font(size, True).measureText(s) > 2 * (SAFE_RIGHT - 540) - 10:
        size -= 1
    text(c, s, 540, y, size, ROSE, 0.92 * a, italic=True)


# ------------------------------------------------------------------ grain (fixed)
_GRAIN = None


def grain_image():
    global _GRAIN
    if _GRAIN is None:
        rng = np.random.default_rng(7)
        n = rng.normal(0, 1, (H // 2, W // 2))
        a = np.clip(128 + n * 22, 0, 255).astype(np.uint8)
        rgba = np.dstack([a, a, a, np.full_like(a, 255)])
        _GRAIN = skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType)
    return _GRAIN


def draw_grain(c, amount=0.07):
    p = skia.Paint(BlendMode=skia.BlendMode.kOverlay)
    p.setAlphaf(amount)
    c.drawImageRect(grain_image(), skia.Rect(0, 0, W, H), skia.SamplingOptions(skia.FilterMode.kLinear), p)


def vignette(c, a=0.55):
    sh = skia.GradientShader.MakeRadial((540, 900), 1250, [col(NIGHT, 0), col(NIGHT, 0), col(NIGHT, a)],
                                        [0.0, 0.55, 1.0])
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sh))


def dim(c, a):
    if a > 0:
        c.drawRect(skia.Rect(0, 0, W, H), paint(NIGHT, a))


# ------------------------------------------------------------------ the room
WINDOW = skia.Rect.MakeLTRB(500, 560, 860, 1030)
LAMP = (205, 1010)          # centre of the lampshade's light
PHONE = (575, 1335)         # phone lying on the bed
BED_Y = 1235

# a little city across the street: buildings and their windows (x, y, w, h); lit ones light up later
_rng = np.random.default_rng(11)
BUILDINGS = [(500, 830, 90), (590, 760, 70), (660, 880, 110), (770, 720, 90)]
CITY_WINDOWS = []
for bx, by, bw in BUILDINGS:
    for yy in range(int(by) + 22, 1010, 44):
        for xx in range(int(bx) + 14, int(bx + bw) - 18, 30):
            CITY_WINDOWS.append((xx, yy, 14, 20, float(_rng.uniform())))
RAIN = [(float(_rng.uniform(505, 855)), float(_rng.uniform(565, 1000)), float(_rng.uniform(24, 70)))
        for _ in range(70)]


def draw_wall(c):
    sh = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [col(NIGHT), col(DEEP), col(NIGHT)], [0.0, 0.55, 1.0])
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sh))


def draw_window(c, lit=0.0, t=0.0, extra=()):
    """lit: 0..1 how many city windows are warm. extra: indices forced on."""
    r = WINDOW
    # sky
    sh = skia.GradientShader.MakeLinear([(0, r.top()), (0, r.bottom())], [col((22, 34, 60)), col((14, 22, 42))])
    c.drawRect(r, skia.Paint(Shader=sh))
    # buildings
    for bx, by, bw in BUILDINGS:
        c.drawRect(skia.Rect.MakeLTRB(bx, by, min(bx + bw, r.right()), r.bottom()), paint((12, 18, 34)))
    for i, (x, y, w, h, u) in enumerate(CITY_WINDOWS):
        on = u < 0.10 or u < lit or i in extra
        if on:
            k = 1.0 if u < 0.10 else smooth(clamp01((lit - u) * 8))
            c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint(AMBER, 0.25 + 0.55 * k))
            if k > 0.05:
                glow(c, x + w / 2, y + h / 2, 26, AMBER, 0.10 * k)
        else:
            c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint((30, 42, 66), 0.9))
    # fixed rain on the glass
    for (x, y, l) in RAIN:
        c.drawLine(x, y, x - 4, y + l, paint(CREAM, 0.10, stroke=1.6))
    # frame and cross bars
    fr = paint(MID, 1.0, stroke=16)
    c.drawRect(r, fr)
    c.drawLine(r.centerX(), r.top(), r.centerX(), r.bottom(), paint(MID, 1.0, stroke=10))
    c.drawLine(r.left(), r.top() + r.height() * 0.42, r.right(), r.top() + r.height() * 0.42, paint(MID, 1.0, stroke=10))
    c.drawRect(skia.Rect.MakeLTRB(r.left() - 26, r.bottom() + 4, r.right() + 26, r.bottom() + 24), paint(MID))


def draw_lamp(c, t, power=1.0):
    """The only warm light. power 0..1.6; the light breathes very slightly."""
    x, y = LAMP
    br = 1 + 0.03 * math.sin(t * 2 * math.pi / 5.0)
    pw = power * br
    glow(c, x, y + 20, 520 * (0.8 + 0.2 * min(1.4, pw)), AMBER, 0.20 * pw)
    glow(c, x, y + 10, 190, AMBER, 0.38 * pw)
    # table
    c.drawRect(skia.Rect.MakeLTRB(60, 1170, 360, 1192), paint(MID))
    c.drawRect(skia.Rect.MakeLTRB(80, 1192, 340, 1260), paint((30, 44, 70)))
    # base and stem
    c.drawLine(x, 1080, x, 1160, paint((60, 70, 90), 1, stroke=10))
    c.drawOval(skia.Rect.MakeLTRB(x - 60, 1150, x + 60, 1174), paint((60, 70, 90)))
    # shade (lit from inside)
    p = skia.Path()
    p.moveTo(x - 70, 930)
    p.lineTo(x + 70, 930)
    p.lineTo(x + 112, 1080)
    p.lineTo(x - 112, 1080)
    p.close()
    sh = skia.GradientShader.MakeLinear([(0, 930), (0, 1080)], [col(mix(AMBER, CREAM, 0.35), 0.55 + 0.4 * min(1, pw)),
                                                               col(AMBER, 0.75 + 0.25 * min(1, pw))])
    c.drawPath(p, skia.Paint(AntiAlias=True, Shader=sh))
    # bright opening under the shade
    c.drawOval(skia.Rect.MakeLTRB(x - 112, 1068, x + 112, 1092), paint(mix(AMBER, CREAM, 0.6), 0.8 * min(1, pw)))


def draw_bed(c):
    # headboard
    c.drawRoundRect(skia.Rect.MakeLTRB(380, 1080, 1120, 1300), 30, 30, paint((28, 40, 64)))
    # mattress + blanket
    p = skia.Path()
    p.moveTo(360, BED_Y)
    p.cubicTo(520, BED_Y - 18, 800, BED_Y - 12, 1100, BED_Y + 4)
    p.lineTo(1100, H)
    p.lineTo(300, H)
    p.close()
    sh = skia.GradientShader.MakeLinear([(0, BED_Y), (0, H)], [col((52, 66, 98)), col((26, 36, 60))])
    c.drawPath(p, skia.Paint(AntiAlias=True, Shader=sh))
    # blanket fold lines
    for k, yy in enumerate((1420, 1560, 1700)):
        q = skia.Path()
        q.moveTo(330, yy)
        q.cubicTo(560, yy - 30 - 10 * k, 820, yy + 20, 1100, yy - 10)
        c.drawPath(q, paint((70, 86, 120), 0.35, stroke=5))
    # pillow
    c.drawRoundRect(skia.Rect.MakeLTRB(700, 1170, 1040, 1270), 50, 50, paint((70, 84, 116)))
    c.drawRoundRect(skia.Rect.MakeLTRB(712, 1180, 1028, 1258), 44, 44, paint((86, 100, 132), 0.6))


def draw_phone(c, t, light=1.0, face_down=0.0, x=None, y=None, scale=1.0, screen=None):
    """A phone lying on the bed. light 0..1 (its cold glow). face_down 0..1 turns it over.
    screen(c, rect, t) can paint the screen content (rect in local coords)."""
    x = PHONE[0] if x is None else x
    y = PHONE[1] if y is None else y
    if light > 0:
        glow(c, x, y - 40 * scale, 430 * scale, COLD, 0.30 * light)
        glow(c, x, y - 10 * scale, 160 * scale, COLD, 0.40 * light)
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    c.rotate(-8)
    w, h = 118, 230
    body = skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h)
    c.drawRoundRect(body, 20, 20, paint((14, 18, 30)))
    scr = skia.Rect.MakeXYWH(-w / 2 + 8, -h / 2 + 10, w - 16, h - 20)
    if face_down < 1:
        a = light * (1 - face_down)
        c.drawRoundRect(scr, 14, 14, paint(mix(DEEP, COLD, 0.85 * a), 1.0))
        if screen and a > 0.02:
            c.save()
            c.clipRRect(skia.RRect.MakeRectXY(scr, 14, 14), skia.ClipOp.kIntersect, True)
            screen(c, scr, t, a)
            c.restore()
    if face_down > 0:
        c.drawRoundRect(scr, 14, 14, paint((24, 30, 46), face_down))
        c.drawCircle(-w / 2 + 26, -h / 2 + 30, 10, paint((40, 48, 70), face_down))
    c.restore()


def feed_screen(speed=40.0, cards=None):
    """An endless feed: grey cards with a red-ish 'breaking' bar, scrolling slowly. No real text."""
    def scr(c, r, t, a):
        hcard = 74
        off = (t * speed) % hcard
        for k in range(-1, 5):
            yy = r.top() + 8 + k * hcard - off
            c.drawRoundRect(skia.Rect.MakeXYWH(r.left() + 7, yy, r.width() - 14, hcard - 10), 8, 8,
                            paint(CREAM, 0.80 * a))
            c.drawRect(skia.Rect.MakeXYWH(r.left() + 14, yy + 8, 34, 9), paint(ROSE, 0.95 * a))
            c.drawRect(skia.Rect.MakeXYWH(r.left() + 14, yy + 24, r.width() - 34, 7), paint(DEEP, 0.45 * a))
            c.drawRect(skia.Rect.MakeXYWH(r.left() + 14, yy + 37, r.width() - 50, 7), paint(DEEP, 0.35 * a))
    return scr


def draw_room(c, t, lamp=1.0, phone_light=1.0, phone_down=0.0, lit=0.0, screen=None, extra=()):
    draw_wall(c)
    draw_window(c, lit, t, extra)
    draw_bed(c)
    draw_lamp(c, t, lamp)
    draw_phone(c, t, phone_light, phone_down, screen=screen)


# ------------------------------------------------------------------ Lumen, the moth
def draw_moth(c, x, y, t, scale=1.0, flap=1.0, spread=1.0, rot=0.0, lit=0.0, a=1.0):
    """Lumen. flap 0..1 (0 = resting), spread 0.2 (folded, curled up) .. 1.2 (wings wide open).
    lit 0..1 warms the wings when he is near the lamp."""
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(scale, scale)
    ph = math.sin(t * 2 * math.pi * 2.2)              # gentle flap, 2.2 Hz
    open_ = spread * (1 - flap * 0.5 * (1 + ph) * 0.75)
    open_ = max(0.12, open_)
    wing = mix(mix(ROSE, DEEP, 0.12), mix(AMBER, CREAM, 0.4), 0.55 * lit)
    edge = mix(CREAM, AMBER, 0.4 * lit)
    for side in (-1, 1):
        c.save()
        c.scale(side * open_, 1)
        fw = skia.Path()
        fw.moveTo(0, -10)
        fw.cubicTo(26, -40, 70, -44, 96, -36)
        fw.cubicTo(100, -18, 84, 4, 4, 6)
        fw.close()
        hw = skia.Path()
        hw.moveTo(0, 2)
        hw.cubicTo(30, 6, 62, 22, 58, 46)
        hw.cubicTo(44, 60, 16, 40, 2, 16)
        hw.close()
        c.drawPath(hw, paint(mix(wing, DEEP, 0.25), a))
        c.drawPath(fw, paint(wing, a))
        c.drawPath(fw, paint(edge, 0.55 * a, stroke=2.4))
        c.drawCircle(56, -26, 7, paint(mix(DEEP, wing, 0.4), 0.8 * a))   # eye-spot
        c.restore()
    # body
    c.drawOval(skia.Rect.MakeLTRB(-12, -26, 12, 36), paint(mix(CREAM, ROSE, 0.45), a))
    for k in range(4):   # fuzzy body bands
        c.drawLine(-9, -8 + k * 11, 9, -8 + k * 11, paint(mix(ROSE, DEEP, 0.3), 0.5 * a, stroke=2.2))
    c.drawCircle(0, -26, 12, paint(CREAM, a))
    # eyes (he listens)
    c.drawCircle(-4, -27, 2.6, paint(NIGHT, a))
    c.drawCircle(4, -27, 2.6, paint(NIGHT, a))
    # feathery antennae
    for side in (-1, 1):
        q = skia.Path()
        q.moveTo(side * 3, -34)
        q.quadTo(side * 14, -58, side * 28, -62)
        c.drawPath(q, paint(CREAM, 0.9 * a, stroke=2.2))
        for k in range(5):
            u = 0.25 + k * 0.15
            px, py = side * (3 + 25 * u), -34 - 28 * u
            c.drawLine(px, py, px + side * 6, py - 5, paint(CREAM, 0.6 * a, stroke=1.4))
    c.restore()


# ------------------------------------------------------------------ diagram pieces (calm, cream lines)
def bar(c, x, base, w, h, color, a=1.0, label=None, label_size=54, label_color=CREAM, sub=None):
    if h > 0.5:
        c.drawRoundRect(skia.Rect.MakeLTRB(x - w / 2, base - h, x + w / 2, base), 14, 14, paint(color, a))
    if label:
        text(c, label, x, base + 66, label_size, label_color, a, italic=True)
    if sub:
        text(c, sub, x, base + 118, 44, ROSE, a, italic=True)


def node(c, x, y, s, a=1.0, size=64, color=CREAM, ring=ROSE):
    if a <= 0:
        return
    f = font(size, True)
    w = f.measureText(s) + 60
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2, y - size * 0.82, w, size * 1.3), 40, 40)
    c.drawRRect(rr, paint(NIGHT, 0.75 * a))
    c.drawRRect(rr, paint(ring, 0.8 * a, stroke=3))
    c.drawString(s, x - (w - 60) / 2, y + size * 0.22, f, paint(color, a))


def arc_arrow(c, cx, cy, r, a0, a1, prog_, color=CREAM, a=1.0, width=6):
    """Arrow along a circle from angle a0 to a1 (degrees, clockwise), drawn up to prog_."""
    if prog_ <= 0 or a <= 0:
        return
    sweep = (a1 - a0) * prog_
    rect = skia.Rect.MakeLTRB(cx - r, cy - r, cx + r, cy + r)
    p = skia.Path()
    p.addArc(rect, a0, sweep)
    c.drawPath(p, paint(color, a, stroke=width))
    if prog_ > 0.98:
        ang = math.radians(a0 + sweep)
        hx, hy = cx + r * math.cos(ang), cy + r * math.sin(ang)
        tang = ang + math.pi / 2 * (1 if sweep > 0 else -1)
        for d in (-0.5, 0.5):
            dx = math.cos(tang + math.pi + d) * 26
            dy = math.sin(tang + math.pi + d) * 26
            c.drawLine(hx, hy, hx + dx, hy + dy, paint(color, a, stroke=width))


def dotted(c, x0, y0, x1, y1, color=CREAM, a=1.0, width=5, gap=16):
    n = int(math.hypot(x1 - x0, y1 - y0) / gap)
    for k in range(n + 1):
        u = k / max(1, n)
        c.drawCircle(lerp(x0, x1, u), lerp(y0, y1, u), width / 2, paint(color, a))
