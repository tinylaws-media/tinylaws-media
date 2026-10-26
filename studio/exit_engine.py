"""THE EXIT MANUAL — renderer (skia). Sober cyberpunk: a terminal in the dark, Relay, neon diagrams.

Look (from the channel bible):
  palette   black #05060A, neon green #39FF88, magenta #FF2E88, cyan #00E5FF, off-white #E8ECEF
  type      VT323 (terminal) for messages and numbers, Major Mono Display for the signature
  texture   perspective grid, FIXED scanlines, FIXED RGB offset on titles. Nothing blinks or flickers.
  motion    text types like a terminal, clean cuts, neon diagrams that draw themselves
  Relay     hooded silhouette, smooth white mask with three linked nodes (original; no Guy Fawkes)
Phone rules: text between y 230 and 1450, nothing important at x > 900, captions <= 5 words a line.
"""
import math
import os

import numpy as np
import skia

W, H, FPS = 1080, 1920, 24
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

BG = 0xFF05060A
GREEN = 0xFF39FF88
MAGENTA = 0xFFFF2E88
CYAN = 0xFF00E5FF
WHITE = 0xFFE8ECEF
GREY = 0xFF8A93A3
DIM = 0xFF1A1F2B
INK = {"green": GREEN, "magenta": MAGENTA, "cyan": CYAN, "white": WHITE, "grey": GREY, "bg": BG, "dim": DIM}

SAFE_X0, SAFE_X1 = 70, 900          # important content stays inside
CAP_CX = 485                        # captions are centred left of the apps' buttons
HORIZON = 1470                      # the perspective grid lives below the text zone


# ------------------------------------------------------------------ easing
def clamp01(x):
    return max(0.0, min(1.0, x))


def prog(t, a, b):
    if b <= a:
        return 1.0 if t >= b else 0.0
    return clamp01((t - a) / (b - a))


def lerp(a, b, x):
    return a + (b - a) * x


def ease_out(x, p=3):
    return 1 - (1 - clamp01(x)) ** p


def ease_in_out(x):
    x = clamp01(x)
    return 3 * x * x - 2 * x * x * x


def col(c, a=1.0):
    c = INK.get(c, c) if isinstance(c, str) else c
    return skia.Color4f.FromColor(c).makeOpaque() if a >= 1 else skia.Color4f(
        skia.Color4f.FromColor(c).fR, skia.Color4f.FromColor(c).fG, skia.Color4f.FromColor(c).fB, a)


# ------------------------------------------------------------------ assets
class Assets:
    def __init__(self):
        self.tf = {
            "term": skia.Typeface.MakeFromFile(os.path.join(FONT_DIR, "VT323-Regular.ttf")),
            "sign": skia.Typeface.MakeFromFile(os.path.join(FONT_DIR, "MajorMonoDisplay-Regular.ttf")),
        }
        self._fonts = {}
        self.bg = self._background()
        self.scan = self._scanlines()

    def font(self, kind, size):
        k = (kind, round(size, 1))
        if k not in self._fonts:
            f = skia.Font(self.tf[kind], size)
            f.setEdging(skia.Font.Edging.kAntiAlias)
            f.setSubpixel(True)
            self._fonts[k] = f
        return self._fonts[k]

    def _background(self):
        s = skia.Surface(W, H)
        c = s.getCanvas()
        c.clear(BG)
        # a faint magenta glow behind the centre, and a cool one low down (static)
        for (cx, cy, r, color, a) in ((540, 760, 900, MAGENTA, 0.07), (540, 1700, 900, CYAN, 0.035)):
            p = skia.Paint(Shader=skia.GradientShader.MakeRadial(
                (cx, cy), r, [skia.Color4f.FromColor(color).toColor() & 0x00FFFFFF | (int(255 * a) << 24), 0x00000000]))
            c.drawRect(skia.Rect(0, 0, W, H), p)
        # vignette
        p = skia.Paint(Shader=skia.GradientShader.MakeRadial((540, 900), 1250, [0x00000000, 0xB0000000]))
        c.drawRect(skia.Rect(0, 0, W, H), p)
        # horizon line
        p = skia.Paint(Color=MAGENTA, AntiAlias=True, StrokeWidth=3, Style=skia.Paint.kStroke_Style)
        p.setAlphaf(0.45)
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
        c.drawLine(0, HORIZON, W, HORIZON, p)
        return s.makeImageSnapshot()

    def _scanlines(self):
        s = skia.Surface(W, H)
        c = s.getCanvas()
        c.clear(0x00000000)
        p = skia.Paint(Color=0xFF000000)
        p.setAlphaf(0.18)
        for y in range(0, H, 4):
            c.drawRect(skia.Rect(0, y, W, y + 1.5), p)
        return s.makeImageSnapshot()


# ------------------------------------------------------------------ drawing context
class Ctx:
    def __init__(self, A, canvas, t, level=0.0):
        self.A, self.c, self.t = A, canvas, t
        self.level = level            # narrator loudness 0..1 (drives Relay's nodes, gently)

    # ---- paints
    def paint(self, color, alpha=1.0, stroke=None, blur=0.0, cap_round=True):
        p = skia.Paint(AntiAlias=True)
        p.setColor4f(col(color, alpha))
        if stroke:
            p.setStyle(skia.Paint.kStroke_Style)
            p.setStrokeWidth(stroke)
            if cap_round:
                p.setStrokeCap(skia.Paint.kRound_Cap)
                p.setStrokeJoin(skia.Paint.kRound_Join)
        if blur:
            p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
        return p

    # ---- background
    def background(self, drift=True):
        c = self.c
        c.drawImage(self.A.bg, 0, 0)
        # perspective floor grid below the horizon; drifts towards us, one cell every 5 s (calm)
        vx = 540
        p = self.paint("green", 0.16, stroke=2)
        for k in range(-14, 15):
            x_far = vx + k * 46
            x_near = vx + k * 260
            c.drawLine(x_far, HORIZON, x_near, H + 40, p)
        ph = (self.t / 5.0) % 1.0 if drift else 0.0
        for i in range(10):
            y = HORIZON + (H - HORIZON) * (1.0 / (1.0 + (9 - i + ph) * 0.55)) ** 1.6
            a = 0.05 + 0.18 * ((y - HORIZON) / (H - HORIZON))
            c.drawLine(0, y, W, y, self.paint("green", a, stroke=2))

    def overlay(self):
        self.c.drawImage(self.A.scan, 0, 0)

    # ---- neon primitives
    def neon_path(self, path, color, width=6, glow=1.0, alpha=1.0):
        if glow > 0:
            self.c.drawPath(path, self.paint(color, 0.55 * glow * alpha, stroke=width * 2.6, blur=9))
        self.c.drawPath(path, self.paint(color, alpha, stroke=width))

    def neon_line(self, x0, y0, x1, y1, color, width=6, glow=1.0, alpha=1.0):
        p = skia.Path()
        p.moveTo(x0, y0)
        p.lineTo(x1, y1)
        self.neon_path(p, color, width, glow, alpha)

    def neon_rect(self, x, y, w, h, color, width=5, r=14, glow=1.0, fill=None, fill_alpha=0.0, alpha=1.0):
        rr = skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r)
        if fill is not None and fill_alpha > 0:
            self.c.drawRRect(rr, self.paint(fill, fill_alpha * alpha))
        p = skia.Path()
        p.addRRect(rr)
        self.neon_path(p, color, width, glow, alpha)

    def panel(self, x, y, w, h, alpha=0.82, r=18, border="cyan", border_alpha=0.55):
        rr = skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r)
        self.c.drawRRect(rr, self.paint(0xFF020306, alpha))
        if border:
            self.c.drawRRect(rr, self.paint(border, border_alpha * alpha, stroke=2.5))

    def partial_polyline(self, pts, u):
        """Path through pts, drawn up to fraction u of its length (diagrams that trace themselves)."""
        segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        total = sum(segs) or 1
        goal = total * clamp01(u)
        p = skia.Path()
        p.moveTo(*pts[0])
        acc = 0
        end = pts[0]
        for i, L in enumerate(segs):
            if acc + L >= goal:
                f = (goal - acc) / L if L else 1
                end = (lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f))
                p.lineTo(*end)
                return p, end, i
            p.lineTo(*pts[i + 1])
            acc += L
            end = pts[i + 1]
        return p, end, len(segs) - 1

    def arrow(self, pts, color, u=1.0, width=6, head=22, dashed=False, alpha=1.0, glow=1.0):
        if u <= 0:
            return
        path, end, i = self.partial_polyline(pts, u)
        if dashed:
            p1 = self.paint(color, 0.5 * alpha * glow, stroke=width * 2.4, blur=8)
            p2 = self.paint(color, alpha, stroke=width)
            eff = skia.DashPathEffect.Make([18, 16], 0)
            p1.setPathEffect(eff)
            p2.setPathEffect(eff)
            self.c.drawPath(path, p1)
            self.c.drawPath(path, p2)
        else:
            self.neon_path(path, color, width, glow, alpha)
        if u >= 0.98:
            a, b = pts[-2], pts[-1]
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            hp = skia.Path()
            hp.moveTo(b[0] - head * math.cos(ang - 0.45), b[1] - head * math.sin(ang - 0.45))
            hp.lineTo(*b)
            hp.lineTo(b[0] - head * math.cos(ang + 0.45), b[1] - head * math.sin(ang + 0.45))
            self.neon_path(hp, color, width, glow, alpha)

    # ---- text
    def text(self, s, x, y, size, color="white", kind="term", align="center", alpha=1.0, rgb=False, glow=0.0,
             scale=1.0):
        f = self.A.font(kind, size)
        w = f.measureText(s)
        if align == "center":
            x0 = x - w / 2
        elif align == "right":
            x0 = x - w
        else:
            x0 = x
        c = self.c
        if scale != 1.0:
            c.save()
            c.translate(x, y)
            c.scale(scale, scale)
            c.translate(-x, -y)
        blob = skia.TextBlob.MakeFromString(s, f)
        if glow > 0:
            c.drawTextBlob(blob, x0, y, self.paint(color, 0.5 * glow * alpha, blur=10))
        if rgb:                                  # FIXED chromatic offset (never animated)
            off = max(2.0, size * 0.035)
            pc = self.paint("cyan", 0.75 * alpha)
            pm = self.paint("magenta", 0.75 * alpha)
            pc.setBlendMode(skia.BlendMode.kScreen)
            pm.setBlendMode(skia.BlendMode.kScreen)
            c.drawTextBlob(blob, x0 - off, y, pc)
            c.drawTextBlob(blob, x0 + off, y, pm)
        c.drawTextBlob(blob, x0, y, self.paint(color, alpha))
        if scale != 1.0:
            c.restore()
        return w

    def width(self, s, size, kind="term"):
        return self.A.font(kind, size).measureText(s)

    def typed(self, s, x, y, size, t0, cps=38.0, color="green", align="left", cursor=True, alpha=1.0, rgb=False,
              glow=0.0):
        """Terminal typing. The cursor is a steady block (never blinks). Returns True when fully typed."""
        if self.t < t0:
            return False
        n = int((self.t - t0) * cps)
        shown = s[:n]
        f = self.A.font("term", size)
        full_w = f.measureText(s)
        if align == "center":
            x0 = x - full_w / 2
        else:
            x0 = x
        if shown:
            self.text(shown, x0, y, size, color, align="left", alpha=alpha, rgb=rgb, glow=glow)
        done = n >= len(s)
        if cursor and not done:
            cw = f.measureText("M")
            cx = x0 + f.measureText(shown) + 4
            self.c.drawRect(skia.Rect(cx, y - size * 0.62, cx + cw * 0.8, y + size * 0.08), self.paint(color, 0.85 * alpha))
        return done


# ------------------------------------------------------------------ captions (mirror the voice)
class Caption:
    """A caption block shown whole while its words are spoken. '/' breaks the line; *word* = highlighted.
    Max 5 words a line, 2 lines."""

    def __init__(self, start, end, text, y=1165, size=98, hi="green", plate=True):
        self.start, self.end, self.text, self.y, self.size, self.hi, self.plate = start, end, text, y, size, hi, plate
        self.lines = []
        for raw in text.split("/"):
            toks, on = [], False
            for tok in raw.strip().split(" "):
                if not tok:
                    continue
                if tok.startswith("*"):
                    on = True
                toks.append((tok.replace("*", ""), on))
                if "*" in tok.lstrip("*"):          # closing star (maybe before punctuation)
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
        a = (1.0 if self.start <= 0 else prog(t, self.start, self.start + 0.08)) * (1 - prog(t, self.end - 0.08, self.end))
        size = self.size
        lh = size * 1.02
        sp = X.width(" ", size)
        widths = [sum(X.width(w, size) for w, _ in toks) + sp * (len(toks) - 1) for toks in self.lines]
        maxw = max(widths)
        if maxw > 800:                     # never wider than the safe column
            size = size * 800 / maxw
            lh = size * 1.02
            sp = X.width(" ", size)
            widths = [sum(X.width(w, size) for w, _ in toks) + sp * (len(toks) - 1) for toks in self.lines]
            maxw = max(widths)
        top = self.y
        if self.plate:
            X.panel(CAP_CX - maxw / 2 - 34, top - 16, maxw + 68, lh * len(self.lines) + 30, alpha=0.78 * a,
                    border=None)
        for li, toks in enumerate(self.lines):
            x = CAP_CX - widths[li] / 2
            base = top + lh * (li + 0.78)
            for w, on in toks:
                ww = X.width(w, size)
                X.text(w, x, base, size, self.hi if on else "white", align="left", alpha=a, rgb=not on,
                       glow=0.6 if on else 0.0)
                x += ww + sp


# ------------------------------------------------------------------ Relay
def relay(X, cx, cy, s=1.0, alpha=1.0, rim=1.0):
    """Relay: hood + mask with three linked nodes. cy = centre of the mask. s=1 -> mask ~300 px wide."""
    c = X.c
    c.save()
    c.translate(cx, cy)
    c.scale(s, s)
    hood = skia.Path()
    hood.moveTo(0, -430)
    hood.cubicTo(150, -420, 270, -250, 285, -40)
    hood.cubicTo(295, 120, 300, 230, 330, 300)
    hood.cubicTo(420, 360, 520, 400, 560, 520)
    hood.lineTo(-560, 520)
    hood.cubicTo(-520, 400, -420, 360, -330, 300)
    hood.cubicTo(-300, 230, -295, 120, -285, -40)
    hood.cubicTo(-270, -250, -150, -420, 0, -430)
    hood.close()
    c.drawPath(hood, X.paint(0xFF0B0E16, alpha))
    # soft inner shading
    p = skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((0, -60), 520, [0x00000000, 0x66000000]))
    p.setAlphaf(alpha)
    c.drawPath(hood, p)
    X.neon_path(hood, "magenta", 4, glow=1.2 * rim, alpha=0.75 * alpha * rim)
    # hood folds
    for sx in (-1, 1):
        f = skia.Path()
        f.moveTo(sx * 230, 270)
        f.cubicTo(sx * 190, 360, sx * 175, 450, sx * 180, 520)
        c.drawPath(f, X.paint(0xFF262B3A, alpha, stroke=5))
    # face opening and the mask
    c.drawOval(skia.Rect(-190, -245, 190, 245), X.paint(0xFF010102, alpha))
    mask = skia.Rect(-150, -195, 150, 195)
    c.drawOval(mask, X.paint(WHITE, alpha))
    c.save()
    mp = skia.Path()
    mp.addOval(mask)
    c.clipPath(mp, doAntiAlias=True)
    lp = X.paint(0xFFB9C0CC, 0.55 * alpha)
    for y in range(-195, 196, 7):
        c.drawRect(skia.Rect(-150, y, 150, y + 2), lp)
    c.restore()
    c.drawOval(mask, X.paint(0xFF9AA2B0, alpha, stroke=3))
    # three linked nodes (a network without a chief). They brighten a little with the voice.
    k = 0.8 + 0.2 * clamp01(X.level)
    nodes = [(0, -62), (-76, 70), (76, 70)]
    tri = skia.Path()
    tri.moveTo(*nodes[0])
    tri.lineTo(*nodes[1])
    tri.lineTo(*nodes[2])
    tri.close()
    c.drawPath(tri, X.paint(0xFF13B866, alpha, stroke=7))
    for (nx, ny) in nodes:
        c.drawCircle(nx, ny, 34, X.paint(GREEN, 0.35 * k * alpha, blur=10))
        c.drawCircle(nx, ny, 24, X.paint(GREEN, alpha * (0.85 + 0.15 * k)))
        c.drawCircle(nx, ny, 24, X.paint(0xFF0A2A18, alpha, stroke=4))
    c.restore()


def relay_icon(X, cx, cy, r=34, alpha=1.0):
    """Tiny mask badge for the header."""
    c = X.c
    c.drawOval(skia.Rect(cx - r * 0.78, cy - r, cx + r * 0.78, cy + r), X.paint(WHITE, alpha))
    nodes = [(cx, cy - r * 0.34), (cx - r * 0.4, cy + r * 0.36), (cx + r * 0.4, cy + r * 0.36)]
    tri = skia.Path()
    tri.moveTo(*nodes[0])
    tri.lineTo(*nodes[1])
    tri.lineTo(*nodes[2])
    tri.close()
    c.drawPath(tri, X.paint(0xFF13B866, alpha, stroke=3))
    for n in nodes:
        c.drawCircle(n[0], n[1], r * 0.15, X.paint(GREEN, alpha))


def coin(X, x, y, r=20, color="green", alpha=1.0):
    X.c.drawCircle(x, y, r * 1.5, X.paint(color, 0.3 * alpha, blur=8))
    X.c.drawCircle(x, y, r, X.paint(0xFF041008, alpha))
    X.c.drawCircle(x, y, r, X.paint(color, alpha, stroke=3.5))
    X.text("€", x, y + r * 0.42, r * 1.25, color, alpha=alpha)
