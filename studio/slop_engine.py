"""SLOP SHOP — renderer (skia). The glossy, over-saturated "AI image" look, drawn in code.

Palette (bible): magenta #FF3CAC, violet #784BA0, cyan #2B86C5, fact-card yellow #FFE600.
Type: Anton (fact cards, yellow with a black outline), Comic Neue (captions, signs), Bungee (logo, HUD).
Running gags built in: GENERATING REALITY... 99% bar, "AI GENERATED (trust me)" watermark,
melting text, Glorp's finger count, lens flares, misaligned eyes, too many teeth.

Calm image: no flashes, no jitter. Motion = eases, pops and slow drifts.
"""
import math
import os

import numpy as np
import skia

W, H, FPS = 1080, 1920, 24
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "slop_fonts")

MAGENTA, VIOLET, CYAN, YELLOW = 0xFFFF3CAC, 0xFF784BA0, 0xFF2B86C5, 0xFFFFE600
INK = 0xFF140A1E          # near-black outline (violet-tinted)
WHITE = 0xFFFFFFFF
PINK = 0xFFFF7AC6
HOTPINK = 0xFFE8288E
RED = 0xFFFF3B3B
GREEN = 0xFF7CF5B0
ORANGE = 0xFFFF9A1F
NIGHT0, NIGHT1 = 0xFF2A1458, 0xFF0E1A4A
SEA0, SEA1 = 0xFF22B5C9, 0xFF16407A


# ------------------------------------------------------------------ easing
def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def prog(t, a, b):
    if b <= a:
        return 1.0 if t >= b else 0.0
    return clamp01((t - a) / (b - a))


def lerp(a, b, x):
    return a + (b - a) * x


def ease_out(x, p=3):
    return 1 - (1 - clamp01(x)) ** p


def ease_in(x, p=3):
    return clamp01(x) ** p


def ease_in_out(x):
    x = clamp01(x)
    return x * x * (3 - 2 * x)


def ease_out_back(x, s=1.70158):
    x = clamp01(x) - 1
    return x * x * ((s + 1) * x + s) + 1


def pop(t, t0, dur=0.3, frm=0.3, s=1.8):
    """0 before t0, then a springy 0->1 scale."""
    if t < t0:
        return 0.0
    return lerp(frm, 1.0, ease_out_back(prog(t, t0, t0 + dur), s))


def hseed(*parts):
    h = 2166136261
    for ch in repr(parts).encode():
        h = ((h ^ ch) * 16777619) & 0xFFFFFFFF
    return h


def argb(c, a=1.0):
    return (int(((c >> 24) & 0xFF) * a) << 24) | (c & 0xFFFFFF)


def mix(c1, c2, x):
    r = [int(lerp((c1 >> s) & 0xFF, (c2 >> s) & 0xFF, x)) for s in (16, 8, 0)]
    return 0xFF000000 | (r[0] << 16) | (r[1] << 8) | r[2]


# ------------------------------------------------------------------ assets
class Assets:
    def __init__(self):
        mgr = skia.FontMgr()
        self.tf = {
            "anton": mgr.makeFromFile(os.path.join(FONT_DIR, "Anton-Regular.ttf")),
            "comic": mgr.makeFromFile(os.path.join(FONT_DIR, "ComicNeue-Bold.ttf")),
            "comicr": mgr.makeFromFile(os.path.join(FONT_DIR, "ComicNeue-Regular.ttf")),
            "bungee": mgr.makeFromFile(os.path.join(FONT_DIR, "Bungee-Regular.ttf")),
        }
        self._fonts = {}
        self.cache = {}

    def font(self, name, size):
        key = (name, int(size * 4))
        f = self._fonts.get(key)
        if f is None:
            f = skia.Font(self.tf[name], size)
            f.setEdging(skia.Font.Edging.kAntiAlias)
            f.setSubpixel(True)
            self._fonts[key] = f
        return f


# ------------------------------------------------------------------ paths
def circle(cx, cy, r):
    p = skia.Path()
    p.addCircle(cx, cy, r)
    return p


def oval(cx, cy, rx, ry):
    p = skia.Path()
    p.addOval(skia.Rect(cx - rx, cy - ry, cx + rx, cy + ry))
    return p


def rrect(x, y, w, h, r):
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r))
    return p


def poly(pts, closed=True):
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if closed:
        p.close()
    return p


def smooth(pts, closed=True):
    """Catmull-Rom through points."""
    p = skia.Path()
    n = len(pts)
    p.moveTo(*pts[0])
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if closed or i > 0 else pts[0]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if closed or i + 2 < n else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        p.cubicTo(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    if closed:
        p.close()
    return p


def blobby(cx, cy, rx, ry, seed, amp=0.04, n=24, phase=0.0):
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, 6.28, 3)
    pts = []
    for i in range(n):
        a = i / n * 2 * math.pi
        k = 1 + amp * (math.sin(3 * a + ph[0] + phase) + 0.6 * math.sin(5 * a + ph[1] - phase * 0.7))
        pts.append((cx + math.cos(a) * rx * k, cy + math.sin(a) * ry * k))
    return smooth(pts)


# ------------------------------------------------------------------ canvas helper
class Slop:
    def __init__(self, A, canvas, t):
        self.A, self.c, self.t = A, canvas, t

    # paints
    def paint(self, color=WHITE, alpha=1.0, stroke=0.0, shader=None):
        p = skia.Paint(AntiAlias=True)
        if shader is not None:
            p.setShader(shader)
        else:
            p.setColor(color)
        if alpha < 1:
            p.setAlphaf(p.getAlphaf() * alpha)
        if stroke:
            p.setStyle(skia.Paint.kStroke_Style)
            p.setStrokeWidth(stroke)
            p.setStrokeCap(skia.Paint.kRound_Cap)
            p.setStrokeJoin(skia.Paint.kRound_Join)
        return p

    def fill(self, path, color=WHITE, alpha=1.0, shader=None):
        self.c.drawPath(path, self.paint(color, alpha, shader=shader))

    def stroke(self, path, color=INK, w=8.0, alpha=1.0):
        self.c.drawPath(path, self.paint(color, alpha, stroke=w))

    def lin(self, x0, y0, x1, y1, colors, pos=None):
        return skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], colors, pos)

    def rad(self, cx, cy, r, colors, pos=None):
        return skia.GradientShader.MakeRadial(skia.Point(cx, cy), r, colors, pos)

    def glossy(self, path, cx, cy, r, light, mid, dark, outline=INK, ow=7.0, hl=True):
        """Plastic look: radial gradient lit from the top-left + a soft specular ellipse."""
        sh = self.rad(cx - r * 0.35, cy - r * 0.4, r * 1.55, [light, mid, dark], [0.0, 0.5, 1.0])
        self.fill(path, shader=sh)
        if hl:
            self.c.save()
            self.c.clipPath(path, doAntiAlias=True)
            self.fill(oval(cx - r * 0.32, cy - r * 0.52, r * 0.34, r * 0.17), WHITE, 0.55)
            self.c.restore()
        if outline:
            self.stroke(path, outline, ow)

    # backgrounds
    def gradient_bg(self, top=MAGENTA, mid=VIOLET, bot=CYAN, drift=0.0):
        sh = self.lin(0, -200 + drift * 80, W * 0.3, H + 200, [top, mid, bot], [0.0, 0.5, 1.0])
        self.c.drawRect(skia.Rect(0, 0, W, H), self.paint(shader=sh))
        # a soft "hyperreal" glow in the upper right
        g = self.rad(W * 0.78, H * 0.3, 620, [argb(WHITE, 0.32), argb(WHITE, 0.0)])
        self.c.drawRect(skia.Rect(0, 0, W, H), self.paint(shader=g))

    def bokeh(self, t, seed=1, n=9, alpha=0.18):
        rng = np.random.default_rng(seed)
        for i in range(n):
            x = rng.uniform(0, W) + math.sin(t * 0.3 + i) * 30
            y = rng.uniform(250, H - 250) + math.cos(t * 0.25 + i * 2) * 26
            r = rng.uniform(30, 90)
            g = self.rad(x, y, r, [argb(WHITE, alpha), argb(WHITE, alpha * 0.5), argb(WHITE, 0)], [0, 0.7, 1])
            self.c.drawCircle(x, y, r, self.paint(shader=g))

    def flare(self, x, y, s=1.0, alpha=1.0):
        """Over-the-top lens flare (the AI 'cinematic' tell). Static, never flashes."""
        g = self.rad(x, y, 160 * s, [argb(0xFFFFF6D0, 0.75 * alpha), argb(0xFFFFC0E8, 0.25 * alpha), argb(WHITE, 0)], [0, 0.35, 1])
        self.c.drawCircle(x, y, 160 * s, self.paint(shader=g))
        self.stroke(circle(x, y, 70 * s), WHITE, 3, 0.25 * alpha)
        for k, (d, r) in enumerate(((0.45, 26), (0.8, 46), (1.15, 18))):
            px, py = lerp(x, W / 2, d * 1.4), lerp(y, H / 2, d * 1.4)
            g = self.rad(px, py, r * s, [argb(0xFFB8F0FF, 0.35 * alpha), argb(WHITE, 0)])
            self.c.drawCircle(px, py, r * s, self.paint(shader=g))

    # text
    def text(self, s, x, y, font="comic", size=72, color=WHITE, outline=INK, ow=10.0, align="center",
             rot=0.0, scale=1.0, alpha=1.0, shadow=None):
        f = self.A.font(font, size)
        w = f.measureText(s)
        ox = {"center": -w / 2, "left": 0, "right": -w}[align]
        c = self.c
        c.save()
        c.translate(x, y)
        if rot:
            c.rotate(rot)
        if scale != 1:
            c.scale(scale, scale)
        if shadow:
            sp = self.paint(shadow[0], alpha)
            c.drawString(s, ox + shadow[1], shadow[2], f, sp)
            if outline:
                c.drawString(s, ox + shadow[1], shadow[2], f, self.paint(shadow[0], alpha, stroke=ow))
        if outline:
            c.drawString(s, ox, 0, f, self.paint(outline, alpha, stroke=ow))
        c.drawString(s, ox, 0, f, self.paint(color, alpha))
        c.restore()
        return w


# ------------------------------------------------------------------ melting text
def _render_block(A, lines, size, color, font="anton", ow=14, width=W, lh=1.02, shadow=10, maxw=760):
    """Render centred lines into an offscreen image (cached by the caller). Shrinks to fit maxw."""
    f = A.font(font, size)
    widest = max(f.measureText(l) for l in lines)
    if widest > maxw:
        size = size * maxw / widest
        f = A.font(font, size)
    hgt = int(len(lines) * size * lh + size * 0.5)
    surf = skia.Surface(width, hgt)
    c = surf.getCanvas()
    c.clear(0)
    R = Slop(A, c, 0)
    y = size * 0.95
    for ln in lines:
        R.text(ln, width / 2, y, font, size, color, INK, ow, shadow=(INK, shadow * 0.6, shadow) if shadow else None)
        y += size * lh
    return surf.makeImageSnapshot(), hgt


def draw_melting(R, img, x, y, melt, seed=3, strip=6, tsec=0.0):
    """Draw img with its top-left at (x, y). melt 0..1+: the lower part of each column sags into drips."""
    c = R.c
    w, h = img.width(), img.height()
    if melt <= 0.001:
        c.drawImage(img, x, y)
        return
    rng = np.random.default_rng(seed)
    nd = 18
    cx = rng.uniform(0, w, nd)
    cw = rng.uniform(10, 34, nd)
    ca = rng.uniform(0.3, 1.0, nd)
    cut = h * 0.45
    samp = skia.SamplingOptions(skia.FilterMode.kLinear)
    for sx in range(0, w, strip):
        xs = sx + strip / 2
        drip = (0.25 + 0.75 * np.sum(ca * np.exp(-((xs - cx) / cw) ** 2))) * melt
        sag = melt * 14 * math.sin(xs * 0.013 + 1.3)
        extra = max(0.0, drip) * h * 0.9
        # top part: only sags a little
        src = skia.Rect(sx, 0, sx + strip, cut)
        dst = skia.Rect(x + sx, y + max(0, sag) * 0.3, x + sx + strip, y + cut + max(0, sag) * 0.3)
        c.drawImageRect(img, src, dst, samp)
        src = skia.Rect(sx, cut, sx + strip, h)
        dst = skia.Rect(x + sx, y + cut + max(0, sag) * 0.3, x + sx + strip, y + h + extra + max(0, sag))
        c.drawImageRect(img, src, dst, samp)


# ------------------------------------------------------------------ captions (subtitles.py-compatible)
class Caption:
    """A line of dialogue on screen. style: "sub" (Comic Neue, bottom), "fact" (Anton fact card, top),
    "sys" (the generator's warning box). segs = [(t, "words with *emph*  / = line break")].
    Exposes .words [(t, word, emph)] and .end like the Tiny Laws captions, so subtitles.py works."""

    def __init__(self, start, end, segs, style="sub", y=None, size=None, melt=None, label="FACT:"):
        self.start, self.end, self.style = start, end, style
        self.melt = melt or (lambda t: 0.0)
        self.label = label
        self.y = y if y is not None else {"sub": 1372, "fact": 440, "sys": 560}[style]
        self.size = size or {"sub": 80, "fact": 118, "sys": 64}[style]
        self.words = []
        for t0, txt in segs:
            emph = False
            for tok in txt.split(" "):
                if not tok:
                    continue
                e0 = tok.startswith("*")
                e1 = "*" in tok[1:] or (e0 and len(tok) == 1)
                if e0:
                    emph = True
                self.words.append((t0, tok.replace("*", ""), emph))
                if e1:
                    emph = False

    def lines(self, t=None):
        out, cur = [], []
        for (ta, s, e) in self.words:
            if s == "/":
                out.append(cur)
                cur = []
                continue
            if t is None or t >= ta:
                cur.append((s, e))
        if cur:
            out.append(cur)
        return [l for l in out if l]

    def draw(self, R, t):
        if not (self.start <= t < self.end):
            return
        k_out = 1 - ease_in(prog(t, self.end - 0.1, self.end))
        if self.style == "sub":
            self._draw_sub(R, t, k_out)
        elif self.style == "fact":
            self._draw_fact(R, t, k_out)
        else:
            self._draw_sys(R, t, k_out)

    def _draw_sub(self, R, t, k):
        A = R.A
        y = self.y
        ls = self.lines(t)
        for li, line in enumerate(ls):
            f = A.font("comic", self.size)
            sp = f.measureText(" ")
            ws = [f.measureText(s) for s, e in line]
            tot = sum(ws) + sp * (len(ws) - 1)
            x = 520 - tot / 2
            first_t = [ta for (ta, s, e) in self.words if s != "/"][0]
            sc = lerp(0.8, 1.0, ease_out_back(prog(t, first_t, first_t + 0.16), 2)) * k
            for (s, e), ww in zip(line, ws):
                R.text(s, x + ww / 2, y + li * self.size * 1.08, "comic", self.size, YELLOW if e else WHITE, INK, 12,
                       scale=sc)
                x += ww + sp

    def _draw_fact(self, R, t, k):
        A = R.A
        lines = [" ".join(s for s, e in l) for l in self.lines(None)]
        key = ("fact", tuple(lines), self.size)
        if key not in A.cache:
            A.cache[key] = _render_block(A, lines, self.size, YELLOW)
        img, hgt = A.cache[key]
        t0 = self.words[0][0]
        sc = 1.0 if t0 <= 0.05 else lerp(1.25, 1.0, ease_out_back(prog(t, max(self.start, t0 - 0.05), max(self.start, t0 - 0.05) + 0.22), 1.6))
        c = R.c
        # "FACT:" tag
        if self.label:
            R.text(self.label, 520, self.y - 14, "anton", 74, WHITE, INK, 12, rot=-3, scale=k,
                   shadow=(INK, 5, 7))
        c.save()
        c.translate(520, self.y + hgt / 2)
        c.scale(sc * k, sc * k)
        c.translate(-W / 2, -hgt / 2)
        draw_melting(R, img, 0, 0, self.melt(t), seed=len(lines[0]))
        c.restore()

    def _draw_sys(self, R, t, k):
        lines = [" ".join(s for s, e in l) for l in self.lines(None)]
        t0 = self.words[0][0]
        sc = pop(t, t0 - 0.05, 0.25, 0.6) * k
        if sc <= 0:
            return
        c = R.c
        bw, bh = 820, 120 + 78 * len(lines)
        c.save()
        c.translate(520, self.y)
        c.scale(sc, sc)
        box = rrect(-bw / 2, -bh / 2, bw, bh, 26)
        R.fill(box, 0xFF1B0B26, 0.92)
        R.stroke(box, RED, 8)
        R.stroke(rrect(-bw / 2 + 14, -bh / 2 + 14, bw - 28, bh - 28, 18), RED, 2, 0.6)
        # warning triangle
        tri = poly([(-bw / 2 + 80, -bh / 2 + 34), (-bw / 2 + 128, -bh / 2 + 112), (-bw / 2 + 32, -bh / 2 + 112)])
        R.fill(tri, YELLOW)
        R.stroke(tri, INK, 4)
        R.text("!", -bw / 2 + 80, -bh / 2 + 104, "bungee", 50, INK, None)
        R.text("SYSTEM", -bw / 2 + 160, -bh / 2 + 92, "bungee", 44, RED, None, align="left")
        for i, ln in enumerate(lines):
            R.text(ln, 0, -bh / 2 + 186 + i * 78, "bungee", self.size, WHITE, None)
        c.restore()


# ------------------------------------------------------------------ HUD: reality bar, watermark, logo
def reality_bar(R, pct, label="GENERATING REALITY...", ok=False, alpha=1.0, brand="SLOP SHOP"):
    x, y, w, h = 60, 236, 830, 86
    bg = rrect(x, y, w, h, 43)
    R.fill(bg, 0xFF2A1238, 0.72 * alpha)
    if brand:
        R.text(brand, x + w - 36, y + 46, "bungee", 34, YELLOW, None, align="right", alpha=alpha)
    R.text(f"{label} {pct}%", x + 44, y + 44, "comic", 40, WHITE, None, align="left", alpha=alpha)
    tw, th = w - 60, 16
    R.fill(rrect(x + 30, y + 58, tw, th, 8), WHITE, 0.18 * alpha)
    col = GREEN if not ok else YELLOW
    R.fill(rrect(x + 30, y + 58, tw * pct / 100.0, th, 8), col, alpha)


def watermark(R, alpha=0.3, scale=1.0, y=1190, text="AI GENERATED (trust me)"):
    R.text(text, 480, y, "bungee", 54, WHITE, None, rot=-18, scale=scale, alpha=alpha)


def sticker(R, s, x, y, scale=1.0, rot=-3, color=RED, size=42, stamp=None, stamp_k=0.0):
    """The game sticker under the bar ("1 of these facts is real"); stamp = e.g. "FOUND" slammed on it."""
    f = R.A.font("comic", size)
    w = f.measureText(s) + 56
    c = R.c
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(scale, scale)
    b = rrect(-w / 2, -size * 0.9, w, size * 1.5, size * 0.4)
    R.fill(b, color)
    R.stroke(b, INK, 5)
    R.text(s, 0, size * 0.22, "comic", size, WHITE, INK, 6)
    if stamp and stamp_k > 0:
        k = lerp(1.8, 1.0, ease_out_back(clamp01(stamp_k), 1.4))
        c.save()
        c.rotate(-8)
        c.scale(k, k)
        sb = rrect(-150, -48, 300, 96, 14)
        R.fill(sb, GREEN)
        R.stroke(sb, INK, 7)
        R.text(stamp, 0, 26, "bungee", 64, INK, None)
        c.restore()
    c.restore()


def logo(R, alpha=1.0):
    R.text("SLOP SHOP", 70, 1540, "bungee", 50, YELLOW, INK, 8, align="left", alpha=alpha)


def floor(R, y=1330, tint=WHITE):
    """A glossy studio floor the cast stands on (fills the bottom of the frame, calmly)."""
    sh = R.lin(0, y, 0, H, [argb(tint, 0.28), argb(INK, 0.35)])
    R.c.drawRect(skia.Rect(0, y, W, H), R.paint(shader=sh))
    g = R.rad(W / 2, y + 30, 640, [argb(WHITE, 0.30), argb(WHITE, 0.0)])
    R.c.save()
    R.c.scale(1, 0.22)
    R.c.drawCircle(W / 2, (y + 30) / 0.22, 640, R.paint(shader=g))
    R.c.restore()
    R.stroke(poly([(0, y), (W, y)], False), WHITE, 3, 0.35)


def tag(R, s, x, y, color=0xFF00E5FF, rot=-6, size=46, scale=1.0, txt=INK):
    """A sticker label, like the 'hyperrealistic' tag of AI image sites."""
    f = R.A.font("comic", size)
    w = f.measureText(s) + 50
    c = R.c
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(scale, scale)
    b = rrect(-w / 2, -size * 0.85, w, size * 1.4, size * 0.5)
    R.fill(b, color)
    R.stroke(b, INK, 5)
    R.text(s, 0, size * 0.25, "comic", size, txt, None)
    c.restore()


# ------------------------------------------------------------------ Glorp
class GlorpState:
    def __init__(self, x=640, y=1000, r=230, **kw):
        self.x, self.y, self.r = x, y, r
        self.talk = 0.0          # 0..1 mouth open
        self.expr = "grin"       # grin | shock | worried | smug | panic
        self.look = (0.0, 0.0)
        self.blink = False
        self.fingers = 7
        self.hand = "wave"       # wave | up | none | point | hide
        self.hand_k = 1.0        # hand scale (for the finger close-up)
        self.sweat = 0.0
        self.melt = 0.0
        self.squash = 1.0
        self.wobble = 0.0        # time, for idle wobble
        self.tilt = 0.0
        self.side = 1            # 1 = hand on his right (our right), -1 = mirrored (keeps it off the app buttons)
        self.__dict__.update(kw)


def _hand(R, x, y, fingers, s=1.0, rot=0.0, wave=0.0, light=0xFFFFC4E6, mid=PINK, dark=HOTPINK):
    """A pink plastic hand with any number of fingers fanned out above the palm."""
    c = R.c
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    n = max(1, fingers)
    spread = min(150, 22 * n + 20)
    for i in range(n):
        a = math.radians(-90 - spread / 2 + spread * (i + 0.5) / n + wave * math.sin(i * 1.3 + wave * 4) * 6)
        L = 112 + 10 * math.sin(i * 2.1)
        x1, y1 = math.cos(a) * L, math.sin(a) * L
        R.stroke(poly([(0, 0), (x1, y1)], False), INK, 46)
        R.stroke(poly([(0, 0), (x1, y1)], False), mid, 32)
        R.stroke(poly([(x1 * 0.55, y1 * 0.55), (x1 * 0.92, y1 * 0.92)], False), light, 10, 0.7)
    palm = oval(0, 8, 72, 66)
    R.glossy(palm, 0, 8, 70, light, mid, dark, INK, 7)
    c.restore()


def draw_glorp(R, G):
    c = R.c
    t = G.wobble
    r = G.r
    sq = G.squash * (1 + 0.012 * math.sin(t * 3.1))
    melt = G.melt
    c.save()
    c.translate(G.x, G.y)
    if G.tilt:
        c.rotate(G.tilt)
    # body: squash + melt (melt widens the bottom and pulls it down into drips)
    sy = sq * (1 - 0.32 * melt)
    sx = (1 / max(0.6, sq)) * (1 + 0.28 * melt)
    pts = []
    n = 40
    for i in range(n):
        a = i / n * 2 * math.pi
        px, py = math.cos(a) * r * sx, math.sin(a) * r * sy
        if py > 0:
            py += melt * r * 0.42 * (py / r) ** 2 * (1 + 0.5 * math.sin(a * 7 + 1))
            px *= 1 + melt * 0.25 * (py / r)
        px *= 1 + 0.015 * math.sin(a * 3 + t * 2)
        pts.append((px, py))
    body = smooth(pts)
    base_y = r * sy + melt * r * 0.4
    # shadow on the floor
    R.fill(oval(0, base_y + 18, r * 0.9 * sx, 26), INK, 0.22)
    # arm (behind the body for "wave"/"up")
    hand_pos = None
    if G.hand in ("wave", "up", "point"):
        if G.hand == "wave":
            hx, hy = r * 0.95, -r * 0.55
            hand_pos = (hx + 70 * G.hand_k, hy - 120 * G.hand_k)
        elif G.hand == "up":
            hx, hy = r * 0.7, -r * 0.6
            hand_pos = (hx + 40 * G.hand_k, hy - 230 * G.hand_k)
        else:
            hx, hy = -r * 0.9, -r * 0.1
            hand_pos = (hx - 140, hy - 30)
        hx *= G.side
        hand_pos = (hand_pos[0] * G.side, hand_pos[1])
        R.stroke(poly([(hx * 0.8, hy * 0.8), hand_pos], False), INK, 44)
        R.stroke(poly([(hx * 0.8, hy * 0.8), hand_pos], False), PINK, 30)
    R.glossy(body, -r * 0.1, -r * 0.1, r, 0xFFFFD6EE, PINK, HOTPINK, INK, 8, hl=False)
    # big specular highlight (the "plastic" tell)
    c.save()
    c.clipPath(body, doAntiAlias=True)
    R.fill(oval(-r * 0.36, -r * 0.6 * sy, r * 0.3, r * 0.14), WHITE, 0.7)
    R.fill(oval(r * 0.55, r * 0.2, r * 0.08, r * 0.05), WHITE, 0.35)
    c.restore()
    # eyes: deliberately misaligned (left bigger and lower)
    ey = -r * 0.12 * sy + melt * r * 0.25
    lx, ly, lr = -r * 0.33, ey + r * 0.05 + melt * r * 0.12, r * 0.25
    rx_, ry_, rr = r * 0.3, ey - r * 0.04, r * 0.29
    look = G.look
    for (ex, eyy, er, k) in ((lx, ly, lr, 0), (rx_, ry_, rr, 1)):
        R.fill(circle(ex, eyy, er), WHITE)
        R.stroke(circle(ex, eyy, er), INK, 5)
        if G.blink:
            R.stroke(poly([(ex - er * 0.8, eyy), (ex + er * 0.8, eyy)], False), INK, 8)
            continue
        pr = er * (0.42 if G.expr not in ("shock", "panic") else 0.28)
        px = ex + look[0] * er * 0.4 + (er * 0.12 if k == 0 else -er * 0.05)
        py = eyy + look[1] * er * 0.4 + (er * 0.08 if k == 0 else 0)
        R.fill(circle(px, py, pr), INK)
        R.fill(circle(px - pr * 0.35, py - pr * 0.4, pr * 0.3), WHITE)
        if G.expr in ("worried", "panic"):
            sgn = -1 if k == 0 else 1
            R.stroke(poly([(ex - er * 0.9, eyy - er * 1.15 + sgn * 6), (ex + er * 0.9, eyy - er * 1.15 - sgn * 10)], False), INK, 8)
        if G.expr == "smug":
            R.fill(oval(ex, eyy - er * 0.55, er * 1.05, er * 0.5), PINK)
            R.stroke(poly([(ex - er, eyy - er * 0.2), (ex + er, eyy - er * 0.2)], False), INK, 6)
    # mouth
    my = r * 0.38 * sy + melt * r * 0.3
    mw = r * 0.62
    op = clamp01(G.talk)
    if G.expr in ("shock", "panic"):
        mo = oval(0, my + 6, r * 0.16 + op * 10, r * 0.2 + op * 18)
        R.fill(mo, 0xFF3A0B24)
        R.stroke(mo, INK, 6)
    else:
        drop = 26 + op * 46
        if G.expr == "worried":
            drop = 14 + op * 30
        m = skia.Path()
        m.moveTo(-mw, my - 10)
        m.quadTo(0, my + drop * 2, mw, my - 14)
        m.quadTo(0, my + drop * 0.6, -mw, my - 10)
        m.close()
        R.fill(m, 0xFF3A0B24)
        # too many teeth: a row of small uneven squares on the upper lip
        c.save()
        c.clipPath(m, doAntiAlias=True)
        nt = 15
        for i in range(nt):
            u = (i + 0.5) / nt
            tx = lerp(-mw, mw, u)
            ty = my - 12 + (u - 0.5) ** 2 * 10 + drop * 0.6 * 4 * u * (1 - u) * 0.62
            tw = mw * 2 / nt * 0.78
            R.fill(rrect(tx - tw / 2, ty - 4, tw, 22 + (i % 3) * 3, 3), WHITE)
        c.restore()
        R.stroke(m, INK, 7)
    # sweat
    if G.sweat > 0:
        for i, (dx, dy) in enumerate(((-0.75, -0.55), (0.85, -0.45), (0.95, 0.05), (-0.92, -0.05), (0.6, -0.8))):
            if G.sweat * 5 <= i:
                break
            fall = ((t * 0.9 + i * 0.37) % 1.0) * 60 * G.sweat
            sx_, sy_ = dx * r, dy * r + fall
            d = skia.Path()
            d.moveTo(sx_, sy_ - 30)
            d.quadTo(sx_ + 18, sy_ + 2, sx_, sy_ + 14)
            d.quadTo(sx_ - 18, sy_ + 2, sx_, sy_ - 30)
            R.fill(d, getattr(G, "sweat_color", 0xFF9FE8FF))
            R.stroke(d, INK, 4)
    # melt drips under the body
    if melt > 0.05:
        for i, dx in enumerate((-0.6, -0.25, 0.1, 0.42, 0.7)):
            L = melt * r * (0.3 + 0.25 * math.sin(i * 2.7 + 1)) + 6 * math.sin(t * 2 + i)
            x0 = dx * r * sx
            y0 = base_y - 20
            d = rrect(x0 - 14, y0 - 10, 28, L + 20, 14)
            R.fill(d, HOTPINK)
            R.stroke(d, INK, 5)
            R.fill(circle(x0, y0 + L + 4, 18), HOTPINK)
            R.stroke(circle(x0, y0 + L + 4, 18), INK, 5)
    # the hand on top
    if hand_pos is not None:
        wave = math.sin(t * 6) if G.hand == "wave" else 0.0
        rot = 18 * wave if G.hand == "wave" else (0 if G.hand == "up" else -70)
        rot *= G.side
        _hand(R, hand_pos[0], hand_pos[1], G.fingers, 0.9 * G.hand_k, rot, wave=0.6 if G.hand == "wave" else 0.2)
    c.restore()
    return hand_pos


# ------------------------------------------------------------------ cast & props
def sign(R, x, y, text, flip=1.0, scale=1.0, rot=0.0, size=58, w=None, stick=True):
    """Cardboard protest sign on a stick. flip: 1 = facing us; a flip animates through 0."""
    c = R.c
    f = R.A.font("comic", size)
    tw = f.measureText(text)
    bw = w or max(200, tw + 60)
    bh = size * 1.7
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(scale, scale)
    if stick:
        R.fill(rrect(-9, -10, 18, 230, 6), 0xFFB07A44)
        R.stroke(rrect(-9, -10, 18, 230, 6), INK, 5)
    c.save()
    c.scale(max(0.02, abs(flip)), 1)
    card = rrect(-bw / 2, -bh, bw, bh, 12)
    R.fill(card, 0xFFFFF8EC)
    R.fill(rrect(-bw / 2, -bh * 0.18, bw, bh * 0.18, 0), 0xFFEADFC8, 0.6)
    R.stroke(card, INK, 6)
    if flip > 0.08:
        R.text(text, 0, -bh / 2 + size * 0.34, "comic", size, INK, None)
    c.restore()
    c.restore()


def penguin(R, x, y, s=1.0, t=0.0, look=0.0, sign_text=None, flip=1.0, blink=False, flap=0.0, heads=1,
            sign_size=58, sign_w=None, bob=True, sign_side=1):
    """A deadpan penguin (the straight man). (x, y) = feet. Holds a sign in its flipper."""
    c = R.c
    c.save()
    c.translate(x, y - (abs(math.sin(t * 2.2)) * 4 if bob else 0) * s)
    c.scale(s, s)
    R.fill(oval(0, 6, 100, 18), INK, 0.22)
    # feet
    for fx in (-40, 40):
        R.fill(oval(fx, -6, 34, 14), ORANGE)
        R.stroke(oval(fx, -6, 34, 14), INK, 5)
    body = blobby(0, -150, 98, 150, 7, amp=0.02)
    R.glossy(body, 0, -170, 150, 0xFF4A4468, 0xFF22203A, 0xFF0C0B16, INK, 7)
    belly = oval(0, -118, 66, 108)
    R.glossy(belly, 0, -130, 100, WHITE, 0xFFF1EEF8, 0xFFCFC8E0, None, 0, hl=False)
    heads_x = [0] if heads == 1 else [-46, 46]
    for hx in heads_x:
        # eyes: half-closed, unimpressed
        for ex in (-30, 30):
            R.fill(circle(hx + ex, -228, 22), WHITE)
            R.stroke(circle(hx + ex, -228, 22), INK, 4)
            R.fill(circle(hx + ex + look * 8, -222, 9), INK)
            if not blink:
                R.fill(rrect(hx + ex - 24, -252, 48, 22, 4), 0xFF22203A)   # heavy lids
            else:
                R.fill(rrect(hx + ex - 24, -252, 48, 46, 4), 0xFF22203A)
            R.stroke(poly([(hx + ex - 22, -230 + (0 if not blink else 16)), (hx + ex + 22, -230 + (0 if not blink else 16))], False), INK, 4)
        beak = poly([(hx - 24, -196), (hx + 24, -196), (hx, -166)])
        R.fill(beak, ORANGE)
        R.stroke(beak, INK, 5)
    # flippers
    R.fill(oval(-104, -140 + flap * -30, 22, 62), 0xFF22203A)
    R.stroke(oval(-104, -140 + flap * -30, 22, 62), INK, 5)
    c.restore()
    if sign_text is not None:
        sx = sign_side
        sign(R, x + sx * 100 * s, y - 300 * s, sign_text, flip=flip, scale=s, size=sign_size, w=sign_w)
        # flipper holding the stick
        R.fill(oval(x + sx * 104 * s, y - 120 * s, 22 * s, 30 * s), 0xFF22203A)
        R.stroke(oval(x + sx * 104 * s, y - 120 * s, 22 * s, 30 * s), INK, 5 * s)


def sun(R, x, y, r, t, look=(0, 0), expr="smile"):
    c = R.c
    c.save()
    c.translate(x, y)
    c.rotate(t * 8)
    for i in range(12):
        a = i / 12 * 2 * math.pi
        p = poly([(math.cos(a - 0.12) * r * 1.05, math.sin(a - 0.12) * r * 1.05), (math.cos(a) * r * 1.5, math.sin(a) * r * 1.5),
                  (math.cos(a + 0.12) * r * 1.05, math.sin(a + 0.12) * r * 1.05)])
        R.fill(p, ORANGE)
        R.stroke(p, INK, 5)
    c.restore()
    body = circle(x, y, r)
    R.glossy(body, x, y, r, 0xFFFFFBD0, YELLOW, 0xFFFFA800, INK, 7)
    _face(R, x, y, r, look, expr)


def moon(R, x, y, r, t, look=(0, 0), expr="smile"):
    body = circle(x, y, r)
    R.glossy(body, x, y, r, 0xFFFFFFFF, 0xFFE4DEF5, 0xFFA79BCB, INK, 7)
    c = R.c
    c.save()
    c.clipPath(body, doAntiAlias=True)
    for (dx, dy, cr) in ((-0.45, 0.35, 0.16), (0.5, -0.45, 0.12), (0.45, 0.5, 0.1)):
        R.fill(circle(x + dx * r, y + dy * r, cr * r), 0xFFBDB2DD)
    c.restore()
    _face(R, x, y, r, look, expr)


def _face(R, x, y, r, look, expr):
    for ex in (-0.32, 0.32):
        cx, cy = x + ex * r, y - 0.12 * r
        R.fill(oval(cx, cy, r * 0.12, r * 0.15), WHITE)
        R.stroke(oval(cx, cy, r * 0.12, r * 0.15), INK, 4)
        R.fill(circle(cx + look[0] * r * 0.05, cy + look[1] * r * 0.05, r * 0.065), INK)
    m = skia.Path()
    if expr == "smile":
        m.moveTo(x - r * 0.3, y + r * 0.25)
        m.quadTo(x, y + r * 0.5, x + r * 0.3, y + r * 0.25)
    else:   # flat, unimpressed
        m.moveTo(x - r * 0.25, y + r * 0.35)
        m.lineTo(x + r * 0.25, y + r * 0.33)
    R.stroke(m, INK, 6)


def shark(R, x, y, s=1.0, t=0.0, nod=0.0):
    """A smug glossy shark, side view, facing left. (x, y) = body centre."""
    c = R.c
    c.save()
    c.translate(x, y + math.sin(t * 2) * 8 * s)
    c.rotate(math.sin(t * 1.7) * 2 + nod * 8)
    c.scale(s, s)
    body = smooth([(-250, 10), (-200, -50), (-60, -85), (120, -60), (240, -18), (300, -6), (240, 22), (100, 60),
                   (-60, 70), (-200, 50)])
    tail = poly([(260, -4), (370, -110), (340, -6), (380, 90)])
    fin = poly([(-20, -78), (40, -190), (90, -66)])
    fin2 = poly([(-40, 50), (20, 130), (60, 50)])
    for p in (tail, fin, fin2):
        R.glossy(p, 0, -60, 220, 0xFFB9D2E6, 0xFF6F93B5, 0xFF3D5C7E, INK, 7, hl=False)
    R.glossy(body, -40, -20, 260, 0xFFCFE2F0, 0xFF7FA3C4, 0xFF3D5C7E, None, 0)
    c.save()
    c.clipPath(body, doAntiAlias=True)
    R.fill(oval(-60, 70, 230, 60), 0xFFF4F7FB)
    c.restore()
    R.stroke(body, INK, 7)
    for gx in (-120, -100, -80):
        R.stroke(poly([(gx, -20), (gx - 8, 20)], False), INK, 4, 0.7)
    R.fill(circle(-178, -24, 14), INK)
    R.fill(circle(-182, -28, 4), WHITE)
    # grin
    m = skia.Path()
    m.moveTo(-238, 14)
    m.quadTo(-200, 34, -150, 22)
    R.stroke(m, INK, 6)
    for i in range(5):
        tx = -230 + i * 18
        R.fill(poly([(tx, 18 + i * 1.5), (tx + 12, 18 + i * 1.5), (tx + 6, 30 + i * 1.5)]), WHITE)
    c.restore()


def sapling(R, x, y, s=1.0, t=0.0):
    c = R.c
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.rotate(math.sin(t * 2.3) * 3)
    R.fill(oval(0, 4, 60, 12), INK, 0.25)
    R.stroke(poly([(0, 0), (0, -90)], False), INK, 16)
    R.stroke(poly([(0, 0), (0, -90)], False), 0xFF7A5230, 8)
    for sx in (-1, 1):
        leaf = oval(sx * 32, -96 - (8 if sx > 0 else 0), 34, 16)
        R.fill(leaf, 0xFF5FD068)
        R.stroke(leaf, INK, 5)
    c.restore()
