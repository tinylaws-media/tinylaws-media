"""TINY LAWS — riso-print animation engine.

Everything is drawn as if printed on a risograph: a few fluorescent inks that
multiply on off-white paper, slight misregistration between inks, speckled ink
coverage, halftone shading and lines that 'boil' (are redrawn) 12 times a second.
"""
import math
import os
import numpy as np
import skia
from PIL import Image, ImageFilter

W, H = 1080, 1920
FPS = 24
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

# ---------------------------------------------------------------- inks
INKS = {
    "navy": (38, 40, 86),        # key ink: lines + text
    "pink": (255, 72, 176),      # riso Fluorescent Pink
    "yellow": (255, 226, 0),     # riso Yellow
    "blue": (0, 120, 191),       # riso Blue
    # series accent inks (standard riso drum colours)
    "teal": (0, 131, 138),       # riso Teal      -> Brain Laws
    "purple": (118, 91, 167),    # riso Purple    -> Mind Laws
    "red": (241, 80, 96),        # riso Bright Red -> Body Laws
    "orange": (255, 108, 47),    # riso Orange    -> Crowd Laws
    "green": (0, 169, 92),       # riso Green     -> From Scratch
    "forest": (64, 112, 96),     # riso Hunter Green -> Planet Laws
    "brown": (146, 95, 82),      # riso Brown     -> World Laws
    "aqua": (94, 200, 229),      # riso Aqua      -> Big Questions
}
# Pip stays fluorescent pink everywhere; each series adds one accent ink (title stamp, law card, scoreboard).
SERIES_INK = {"Tiny Laws": "yellow", "Brain Laws": "teal", "Mind Laws": "purple", "Body Laws": "red",
              "Crowd Laws": "orange", "From Scratch": "green", "Money & Power Laws": "blue",
              "Planet Laws": "forest", "World Laws": "brown", "Big Questions": "aqua"}
PAPER = (244, 239, 228)

# base misregistration of each drum (px); the key ink (navy) is the reference
MISREG = {"navy": (0, 0), "pink": (3, -2), "yellow": (-3, 2), "blue": (2, 3),
          "teal": (2, -2), "purple": (-2, 3), "red": (3, 2), "orange": (-3, -2), "green": (2, 2),
          "forest": (-2, -2), "brown": (2, -3), "aqua": (-3, 3)}

# Calm print (user feedback, 25 Oct 2026): no boiling lines, no animated grain, no jitter.
# BOIL_FRAMES = 0 keeps every drawing identical from frame to frame; set e.g. 4 for a slow boil.
BOIL_FRAMES = 0


def ease_out_back(x, s=1.70158):
    x = min(max(x, 0.0), 1.0) - 1
    return x * x * ((s + 1) * x + s) + 1


def ease_out_elastic(x):
    x = min(max(x, 0.0), 1.0)
    if x in (0.0, 1.0):
        return x
    return 2 ** (-10 * x) * math.sin((x * 10 - 0.75) * (2 * math.pi) / 3) + 1


def ease_in_out(x):
    x = min(max(x, 0.0), 1.0)
    return 3 * x * x - 2 * x * x * x


def ease_out(x, p=3):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** p


def ease_in(x, p=3):
    x = min(max(x, 0.0), 1.0)
    return x ** p


def clamp01(x):
    return min(max(x, 0.0), 1.0)


def prog(t, a, b):
    """0..1 progress of t between a and b."""
    if b <= a:
        return 1.0 if t >= a else 0.0
    return clamp01((t - a) / (b - a))


def lerp(a, b, x):
    return a + (b - a) * x


def hseed(*parts):
    h = 2166136261
    for p in parts:
        for ch in str(p):
            h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    return h


# ---------------------------------------------------------------- textures
def _to_image(rgb):
    """float/uint8 HxWx3 RGB -> opaque skia image in the surface's native BGRA layout."""
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    h, w = rgb.shape[:2]
    bgra = np.empty((h, w, 4), np.uint8)
    bgra[..., 0] = rgb[..., 2]
    bgra[..., 1] = rgb[..., 1]
    bgra[..., 2] = rgb[..., 0]
    bgra[..., 3] = 255
    return skia.Image.fromarray(bgra, colorType=skia.ColorType.kBGRA_8888_ColorType,
                                alphaType=skia.AlphaType.kPremul_AlphaType)


def _blur_noise(w, h, radius, rng):
    """Gaussian-blurred noise that tiles seamlessly (blurred with wrap-around)."""
    a = (rng.random((h, w)) * 255).astype(np.uint8)
    big = np.tile(a, (3, 3))
    im = Image.fromarray(big).filter(ImageFilter.GaussianBlur(radius))
    b = np.asarray(im)[h:2 * h, w:2 * w].astype(np.float32) / 255.0
    b = (b - b.mean()) / (b.std() + 1e-6)
    return b


def _ink_texture(rgb, seed, size=512):
    """Ink colour with riso-style coverage gaps (light speckles + soft mottling)."""
    rng = np.random.default_rng(seed)
    mott = _blur_noise(size, size, 18, rng)
    fine = _blur_noise(size, size, 0.8, rng)
    gaps = np.clip((fine - 2.4) * 0.8, 0, 1)            # rare paper specks showing through
    light = np.clip(0.07 + 0.045 * mott, 0, 0.25)       # gently uneven ink density
    k = np.clip(light + gaps, 0, 1)[..., None]
    col = np.array(rgb, np.float32)[None, None, :]
    out = col * (1 - k) + 255.0 * k
    return _to_image(out)


def _halftone_tile(rgb, cell=18, radius=5.2):
    a = np.zeros((cell, cell, 4), np.float32)
    yy, xx = np.mgrid[0:cell, 0:cell] + 0.5
    d = np.sqrt((xx - cell / 2) ** 2 + (yy - cell / 2) ** 2)
    cov = np.clip(radius + 0.5 - d, 0, 1)
    a[..., 0] = rgb[0]
    a[..., 1] = rgb[1]
    a[..., 2] = rgb[2]
    a[..., 3] = 255 * cov
    a[..., :3] *= cov[..., None]          # premultiply
    bgra = a[..., [2, 1, 0, 3]]
    return skia.Image.fromarray(np.ascontiguousarray(bgra.astype(np.uint8)),
                                colorType=skia.ColorType.kBGRA_8888_ColorType,
                                alphaType=skia.AlphaType.kPremul_AlphaType)


def _paper(seed=7):
    rng = np.random.default_rng(seed)
    base = np.array(PAPER, np.float32)[None, None, :]
    big = _blur_noise(W // 4, H // 4, 10, rng)
    big = np.asarray(Image.fromarray(((big * 30 + 128).clip(0, 255)).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32) / 255 - 0.5
    fib = _blur_noise(W, H, 0.6, rng)
    img = base + big[..., None] * 10 + fib[..., None] * 2.2
    # sparse dark flecks in the paper
    fl = rng.random((H, W)) > 0.99990
    img[fl] -= 45
    # gentle vignette
    yy, xx = np.mgrid[0:H, 0:W]
    v = ((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2
    img -= (v * 26)[..., None]
    return _to_image(img)


def _grain(seed):
    rng = np.random.default_rng(seed)
    g = _blur_noise(W // 2, H // 2, 0.7, rng)
    v = (255 - np.clip(g - 0.9, 0, 3) * 26).clip(0, 255)
    return _to_image(np.stack([v, v, v], axis=2))


class Assets:
    def __init__(self):
        self.ink_tex = {k: [_ink_texture(v, hseed(k, i)) for i in range(3)] for k, v in INKS.items()}
        self.halftone = {k: _halftone_tile(v) for k, v in INKS.items()}
        self.paper = _paper()
        self.grains = [_grain(100 + i) for i in range(6)]
        tf = lambda n: skia.Typeface.MakeFromFile(f"{FONT_DIR}/{n}.ttf")
        self.tf = {
            "bagel": tf("BagelFatOne-Regular"),
            "hand": tf("CaveatBrush-Regular"),
            "mono": tf("SpaceMono-Bold"),
            "grot": tf("BricolageGrotesque"),
        }

    def font(self, name, size):
        f = skia.Font(self.tf[name], size)
        f.setEdging(skia.Font.Edging.kAntiAlias)
        f.setSubpixel(True)
        return f


# ---------------------------------------------------------------- paths
def smooth_closed(xs, ys):
    """Catmull-Rom closed spline through points -> skia.Path."""
    n = len(xs)
    p = skia.Path()
    p.moveTo(xs[0], ys[0])
    for i in range(n):
        x0, y0 = xs[i - 1], ys[i - 1]
        x1, y1 = xs[i], ys[i]
        x2, y2 = xs[(i + 1) % n], ys[(i + 1) % n]
        x3, y3 = xs[(i + 2) % n], ys[(i + 2) % n]
        p.cubicTo(x1 + (x2 - x0) / 6, y1 + (y2 - y0) / 6,
                  x2 - (x3 - x1) / 6, y2 - (y3 - y1) / 6, x2, y2)
    p.close()
    return p


def blob(cx, cy, rx, ry, seed, amp=0.025, n=40, rot=0.0):
    rng = np.random.default_rng(seed)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    m = np.ones(n)
    for k in (2, 3, 5):
        m += amp * rng.uniform(0.4, 1.0) * np.sin(k * th + rng.uniform(0, 2 * np.pi))
    ca, sa = math.cos(rot), math.sin(rot)
    x = rx * m * np.cos(th)
    y = ry * m * np.sin(th)
    return smooth_closed(cx + x * ca - y * sa, cy + x * sa + y * ca)


def _wiggle_pts(pts, seed, amp, closed, step=10.0):
    """Resample a polyline every `step` px and push it sideways with smooth noise."""
    pts = [tuple(p) for p in pts]
    if closed:
        pts = pts + [pts[0]]
    rng = np.random.default_rng(seed)
    waves = [(rng.uniform(70, 260), rng.uniform(0, 6.28), rng.uniform(0.5, 1.0)) for _ in range(3)]
    out = []
    s_acc = 0.0
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(L / step))
        nx, ny = (-(y1 - y0) / L, (x1 - x0) / L) if L > 0 else (0, 0)
        for j in range(n):
            f = j / n
            s = s_acc + f * L
            d = sum(a * math.sin(2 * math.pi * s / wl + ph) for wl, ph, a in waves) * amp / 1.6
            out.append((x0 + (x1 - x0) * f + nx * d, y0 + (y1 - y0) * f + ny * d))
        s_acc += L
    if not closed:
        out.append(pts[-1])
    return out


def wpoly(pts, seed, amp=2.2, closed=True):
    w = _wiggle_pts(pts, seed, amp, closed)
    p = skia.Path()
    p.moveTo(*w[0])
    for q in w[1:]:
        p.lineTo(*q)
    if closed:
        p.close()
    return p


def wrect(x, y, w, h, seed, amp=2.2, r=0):
    if r <= 0:
        return wpoly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], seed, amp)
    pts = []
    for cx, cy, a0 in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)):
        for k in range(7):
            a = math.radians(a0 + k * 15)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return wpoly(pts, seed, amp)


def wline(x0, y0, x1, y1, seed, amp=2.0):
    return wpoly([(x0, y0), (x1, y1)], seed, amp, closed=False)


def union(*paths):
    out = paths[0]
    for p in paths[1:]:
        r = skia.Op(out, p, skia.PathOp.kUnion_PathOp)
        if r is not None:
            out = r
    return out


def star_path(cx, cy, r_out, r_in, n=5, rot=-90, seed=0):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return wpoly(pts, seed, 1.5)


# ---------------------------------------------------------------- the press
class Riso:
    """Drawing helpers bound to one canvas + one frame (boil index)."""

    def __init__(self, assets, canvas, frame):
        self.A = assets
        self.c = canvas
        self.frame = frame
        self.boil = frame // BOIL_FRAMES if BOIL_FRAMES else 0
        self.misreg = dict(MISREG)      # fixed registration: nothing flickers

    def s(self, *parts):
        """seed that changes on every boil."""
        return hseed(self.boil, *parts)

    _shader_cache = {}

    def _tex_shader(self, ink):
        key = (ink, self.boil % 24)
        sh = Riso._shader_cache.get(key)
        if sh is None:
            tex = self.A.ink_tex[ink][self.boil % 3]
            rng = np.random.default_rng(hseed("tex", ink, self.boil % 24))
            m = skia.Matrix.Translate(float(int(rng.uniform(0, 512))), float(int(rng.uniform(0, 512))))
            if not BOIL_FRAMES:
                m = skia.Matrix.Translate(0.0, 0.0)
            sh = tex.makeShader(skia.TileMode.kRepeat, skia.TileMode.kRepeat, skia.SamplingOptions(), m)
            Riso._shader_cache[key] = sh
        return sh

    def _ink_paint(self, ink, alpha=1.0, texture=True):
        # NB: Paint(Shader=...) is fast; Paint.setShader() is very slow in skia-python
        if texture:
            p = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kMultiply, Shader=self._tex_shader(ink))
        else:
            p = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kMultiply, Color=skia.ColorSetRGB(*INKS[ink]))
        if alpha < 1:
            p.setAlphaf(alpha)
        return p

    def fill(self, path, ink, alpha=1.0, texture=True, misreg=True):
        p = self._ink_paint(ink, alpha, texture)
        p.setStyle(skia.Paint.kFill_Style)
        dx, dy = self.misreg[ink] if misreg else (0, 0)
        self.c.save()
        self.c.translate(dx, dy)
        self.c.drawPath(path, p)
        self.c.restore()

    def stroke(self, path, ink="navy", width=8.0, alpha=1.0):
        p = self._ink_paint(ink, alpha, texture=True)
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(width)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
        dx, dy = self.misreg[ink]
        self.c.save()
        self.c.translate(dx, dy)
        self.c.drawPath(path, p)
        self.c.restore()

    def halftone(self, path, ink, scale=1.0, angle=22.0, alpha=1.0):
        m = skia.Matrix()
        m.setRotate(angle)
        m.preScale(scale, scale)
        sh = self.A.halftone[ink].makeShader(skia.TileMode.kRepeat, skia.TileMode.kRepeat,
                                             skia.SamplingOptions(skia.FilterMode.kLinear), m)
        p = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kMultiply, Shader=sh)
        if alpha < 1:
            p.setAlphaf(alpha)
        dx, dy = self.misreg[ink]
        self.c.save()
        self.c.translate(dx, dy)
        self.c.drawPath(path, p)
        self.c.restore()

    def knockout(self, path):
        """Paper-coloured shape (a riso 'knockout': no ink printed here)."""
        p = skia.Paint(AntiAlias=True, Color=skia.ColorSetRGB(*PAPER))
        self.c.drawPath(path, p)

    def flood(self, ink, alpha=1.0):
        self.fill(wrect(-60, -60, W + 120, H + 120, 1, amp=0), ink, alpha, misreg=False)

    # ---- text
    def text(self, s, x, y, font, ink="navy", align="center", alpha=1.0, shadow=None, rot=0.0, scale=1.0):
        """Draw text in an ink. shadow=(ink, dx, dy) adds an overprinted offset copy."""
        w = font.measureText(s)
        ox = {"center": -w / 2, "left": 0, "right": -w}[align]
        rng = np.random.default_rng(hseed("txt", s) if not BOIL_FRAMES else self.s("txt", s, int(x), int(y)))
        jx, jy, jr = 0.0, 0.0, rng.uniform(-0.6, 0.6)
        self.c.save()
        self.c.translate(x + jx, y + jy)
        self.c.rotate(rot + jr)
        self.c.scale(scale, scale)
        if shadow:
            sink, sdx, sdy = shadow
            p = self._ink_paint(sink, alpha)
            self.c.drawString(s, ox + sdx, sdy, font, p)
        p = self._ink_paint(ink, alpha)
        dx, dy = self.misreg[ink]
        self.c.drawString(s, ox + dx, dy, font, p)
        self.c.restore()
        return w


# ---------------------------------------------------------------- captions
class Caption:
    """A block of words that pop in one by one (Pip 'speaks' each with a blip).

    segs: list of (time, text). Words wrapped in *stars* are emphasised.
    """

    WORD_GAP = 0.10

    def __init__(self, start, end, segs, y=470, size=92, emph_size=128, plate=False, word_gap=None):
        self.start, self.end, self.y = start, end, y
        self.plate = plate
        gap = self.WORD_GAP if word_gap is None else word_gap   # 0 = a whole line appears at once
        self.size, self.emph_size = size, emph_size
        self.words = []          # (t_appear, text, emph)
        for t0, txt in segs:
            emph = False
            i = 0
            for tok in txt.split(" "):
                if not tok:
                    continue
                e_start = tok.startswith("*")
                e_end = "*" in tok[1:] or (e_start and len(tok) == 1)
                clean = tok.replace("*", "")
                if e_start:
                    emph = True
                self.words.append((t0 + i * gap, clean, emph))
                if e_end:
                    emph = False
                i += 1

    def word_times(self):
        return [w[0] for w in self.words if w[1] != "/"]

    def layout(self, A):
        lines, cur, cur_w = [], [], 0
        maxw = 940
        for (ta, s, e) in self.words:
            if s == "/":
                if cur:
                    lines.append(cur)
                cur, cur_w = [], 0
                continue
            f = A.font("bagel", self.emph_size if e else self.size)
            ww = f.measureText(s)
            sp = A.font("bagel", self.size).measureText(" ")
            if cur and cur_w + sp + ww > maxw:
                lines.append(cur)
                cur, cur_w = [], 0
            cur.append((ta, s, e, f, ww, sp))
            cur_w += (sp if len(cur) > 1 else 0) + ww
        if cur:
            lines.append(cur)
        return lines

    def draw(self, R, t):
        if t < self.start or t >= self.end:
            return
        A = R.A
        lines = self.layout(A)
        out = prog(t, self.end - 0.12, self.end)
        y = self.y
        for li, line in enumerate(lines):
            lh = max((self.emph_size if e else self.size) for (_, _, e, _, _, _) in line)
            total = sum(ww for (_, _, _, _, ww, _) in line) + sum(sp for (_, _, _, _, _, sp) in line[1:])
            x = W / 2 - total / 2
            base = y + lh * 0.80
            if self.plate and t >= line[0][0]:
                vis = [ww for (ta, _, _, _, ww, _) in line if t >= ta]
                pw = sum(vis) + sum(sp for (ta, _, _, _, _, sp) in line[1:] if t >= ta) + 56
                pk = ease_out_back(prog(t, line[0][0], line[0][0] + 0.15), 2) * (1 - ease_in(out))
                if pk > 0.02:
                    pl = wrect(x - 28, y - 8, pw, lh * 1.0, R.s("plate", li, int(pw) // 40), amp=2, r=16)
                    R.c.save()
                    R.c.translate(W / 2, y + lh / 2)
                    R.c.scale(1, pk)
                    R.c.translate(-W / 2, -(y + lh / 2))
                    R.knockout(pl)
                    R.stroke(pl, "navy", 5)
                    R.c.restore()
            for wi, (ta, s, e, f, ww, sp) in enumerate(line):
                if wi > 0:
                    x += sp
                if t >= ta:
                    k = ease_out_back(prog(t, ta, ta + 0.18), 1.8)
                    sc = lerp(0.55, 1.0, k) * (1 - ease_in(out))
                    if sc > 0.01:
                        cx = x + ww / 2
                        if e:
                            rng = np.random.default_rng(hseed("sw", s, li))
                            hl = wrect(x - 16, base - lh * 0.70, ww + 32, lh * 0.78, R.s("hl", s), amp=3, r=18)
                            R.c.save()
                            R.c.translate(cx, base - lh * 0.3)
                            R.c.scale(sc, sc)
                            R.c.rotate(float(rng.uniform(-2.5, 2.5)))
                            R.c.translate(-cx, -(base - lh * 0.3))
                            R.fill(hl, "yellow")
                            R.c.restore()
                            R.text(s, cx, base, f, "navy", shadow=("pink", 7, 7), scale=sc)
                        else:
                            R.text(s, cx, base, f, "navy", shadow=("pink", 4, 4), scale=sc)
                x += ww
            y += lh * 1.02


# ---------------------------------------------------------------- characters & props
class PipState:
    def __init__(self, **kw):
        self.x = W / 2
        self.ground = 1430.0
        self.scale = 1.0
        self.expr = "normal"      # normal, happy, shock, worried, dizzy, deadpan
        self.talk = 0.0           # 0..1 mouth open
        self.squash = 1.0         # vertical squash of body
        self.flat = 0.0           # 0..1 pancake
        self.tremble = 0.0        # px
        self.crack = 0.0          # 0..1 crack lines on legs
        self.legs_thick = 1.0
        self.sweat = 0.0
        self.look = (0.0, 0.0)
        self.blink = False
        self.arms = "down"        # down, up, shrug, point
        self.tilt = 0.0
        self.lift = (0.0, 0.0)    # px each foot is raised (left, right): walking, hopping, holding a toe
        self.__dict__.update(kw)


def draw_pip(R, P):
    """Pip: a fluorescent-pink bean with a two-leaf sprout. Feet sit on P.ground."""
    c = R.c
    s = P.scale
    rng = np.random.default_rng(R.s("pip-trem"))
    tx = rng.uniform(-1, 1) * P.tremble
    c.save()
    c.translate(P.x + tx, P.ground)
    c.scale(s, s)
    c.rotate(P.tilt)
    lw = 8.0 / max(s, 0.35) ** 0.35       # keep lines from becoming huge when scaled

    flat = ease_in_out(P.flat)
    body_rx = 108 * (1 + 0.9 * flat) / max(P.squash, 0.5) ** 0.3
    body_ry = 118 * P.squash * (1 - 0.72 * flat)
    leg_h = 52 * (1 - flat)
    leg_w = 26 * P.legs_thick
    by = -(leg_h + body_ry - 10)       # body centre

    # shadow
    R.halftone(blob(0, 4, body_rx * 1.05, 16, R.s("pipsh")), "blue", scale=0.8)

    # legs
    legs = []
    if leg_h > 2:
        for sx in (-1, 1):
            lx = sx * (44 + 6 * (P.legs_thick - 1)) - leg_w / 2
            up = P.lift[0 if sx < 0 else 1]
            legs.append(wrect(lx, -leg_h - 14 - up, leg_w, leg_h + 14, R.s("leg", sx), amp=1.6, r=min(12, leg_w / 2)))
    # arms
    arms = []
    arm_pose = {"down": (35, 0), "up": (-40, 0), "shrug": (-10, 1), "point": (-20, 0)}[P.arms]
    for sx in (-1, 1):
        ax = sx * body_rx * 0.92
        ay = by + 10
        ang = math.radians(arm_pose[0] if sx > 0 else 180 - arm_pose[0])
        ex, ey = ax + math.cos(ang) * 46 * sx * sx, ay + math.sin(ang) * 46
        if P.arms == "shrug":
            ex, ey = ax + sx * 40, ay - 26
        arms.append(wpoly([(ax, ay), ((ax + ex) / 2 + sx * 6, (ay + ey) / 2 + 6), (ex, ey)], R.s("arm", sx), 1.2, closed=False))
    body = blob(0, by, body_rx, body_ry, R.s("pipbody"), amp=0.018)
    pink_shape = union(body, *legs) if legs else body
    R.fill(pink_shape, "pink")
    # halftone shade (lower right)
    c.save()
    c.clipPath(body, doAntiAlias=True)
    R.halftone(blob(body_rx * 0.62, by + body_ry * 0.62, body_rx * 0.85, body_ry * 0.7, R.s("pshade")), "blue", scale=0.62, alpha=0.55)
    c.restore()
    # sprout (yellow x blue overlap prints green)
    if flat < 0.7:
        top = by - body_ry + 6
        stem = wpoly([(0, top), (4, top - 26), (2, top - 42)], R.s("stem"), 1.0, closed=False)
        R.stroke(stem, "navy", lw * 0.8)
        leafL = blob(-24, top - 50, 24, 12, R.s("leafL"), rot=-0.5)
        leafR = blob(26, top - 52, 24, 12, R.s("leafR"), rot=0.5)
        for lf in (leafL, leafR):
            R.fill(lf, "yellow")
            R.fill(lf, "blue", alpha=0.9)
            R.stroke(lf, "navy", lw * 0.7)
    # outlines
    for lg in legs:
        R.stroke(lg, "navy", lw)
    R.stroke(body, "navy", lw)
    for a in arms:
        R.stroke(a, "navy", lw)
    if P.crack > 0 and legs:
        for sx in (-1, 1):
            lx = sx * (44 + 6 * (P.legs_thick - 1))
            pts = [(lx - 10, -leg_h + 4), (lx + 6, -leg_h + 18), (lx - 6, -leg_h + 30), (lx + 8, -leg_h + 44)]
            n = max(2, int(len(pts) * P.crack + 0.5))
            R.stroke(wpoly(pts[:n], R.s("crk", sx), 1.0, closed=False), "navy", lw * 0.55)

    # face
    ex0, ey0 = 36 + P.look[0] * 8, by - 14 + P.look[1] * 6
    face_sq = (1 - 0.5 * flat)
    cheek_y = by + 22
    for sx in (-1, 1):
        R.fill(blob(sx * 64, cheek_y, 17, 10, R.s("chk", sx)), "yellow", alpha=0.95)
    if P.expr == "dizzy":
        for sx in (-1, 1):
            cx_, cy_ = sx * ex0, ey0
            R.stroke(wline(cx_ - 12, cy_ - 12, cx_ + 12, cy_ + 12, R.s("x1", sx), 0.8), "navy", lw * 0.8)
            R.stroke(wline(cx_ + 12, cy_ - 12, cx_ - 12, cy_ + 12, R.s("x2", sx), 0.8), "navy", lw * 0.8)
    elif P.expr == "happy":
        for sx in (-1, 1):
            arc = wpoly([(sx * ex0 - 14, ey0 + 6), (sx * ex0, ey0 - 8), (sx * ex0 + 14, ey0 + 6)], R.s("ha", sx), 0.6, closed=False)
            R.stroke(arc, "navy", lw * 0.85)
    elif P.blink:
        for sx in (-1, 1):
            R.stroke(wline(sx * ex0 - 12, ey0, sx * ex0 + 12, ey0, R.s("bl", sx), 0.5), "navy", lw * 0.8)
    else:
        er = 11 if P.expr == "shock" else 13
        ery = (11 if P.expr == "shock" else 17) * face_sq
        for sx in (-1, 1):
            e = blob(sx * ex0, ey0, er, ery, R.s("eye", sx), amp=0.03)
            R.fill(e, "navy", texture=False, misreg=False)
            R.knockout(blob(sx * ex0 + 4, ey0 - 6 * face_sq, 4.2, 4.2, 3))
        if P.expr in ("worried", "deadpan"):
            for sx in (-1, 1):
                if P.expr == "worried":
                    br = wline(sx * ex0 - 14, ey0 - 30 + (-6 if sx < 0 else 0), sx * ex0 + 14, ey0 - 30 + (0 if sx < 0 else -6), R.s("br", sx), 0.5)
                else:
                    br = wline(sx * ex0 - 15, ey0 - 26, sx * ex0 + 15, ey0 - 26, R.s("br", sx), 0.5)
                R.stroke(br, "navy", lw * 0.7)
    # mouth
    my = by + 26
    if P.expr == "shock" or P.talk > 0.5:
        mo = 9 + 7 * (P.talk if P.expr != "shock" else 1)
        m = blob(0, my + 2, 10, mo * face_sq, R.s("mo"), amp=0.05)
        R.fill(m, "navy", texture=False, misreg=False)
        R.fill(blob(0, my + mo * 0.5, 6, 3.5, 1), "pink")
    elif P.expr == "happy":
        sm = wpoly([(-16, my - 2), (0, my + 10), (16, my - 2)], R.s("sm"), 0.6, closed=True)
        R.fill(sm, "navy", texture=False, misreg=False)
    elif P.expr in ("worried", "deadpan"):
        R.stroke(wpoly([(-12, my + 4), (-4, my), (4, my + 4), (12, my)], R.s("wm"), 0.6, closed=False), "navy", lw * 0.7)
    else:
        R.stroke(wpoly([(-10, my), (0, my + 6), (10, my)], R.s("nm"), 0.5, closed=False), "navy", lw * 0.75)
    # sweat
    if P.sweat > 0:
        for i, (dx, dy) in enumerate(((-body_rx - 18, by - 60), (body_rx + 12, by - 80), (body_rx + 30, by - 30))):
            if P.sweat > i / 3:
                d = wpoly([(dx, dy - 22), (dx + 11, dy), (dx, dy + 10), (dx - 11, dy)], R.s("sw", i), 1, True)
                R.fill(d, "blue")
                R.stroke(d, "navy", lw * 0.55)
    c.restore()


def iso(x, y, z, s0, ox, oy):
    c30, s30 = 0.8660254, 0.5
    return (ox + (x - y) * c30 * s0, oy + (x + y) * s30 * s0 - z * s0)


def draw_cube(R, ox, oy, size, pos=(0, 0, 0), seed="cube", grid=1, alpha=1.0, outline_only=False, faces=("yellow", "pink", "blue")):
    """Isometric cube. (ox, oy) is the projection origin. pos/size in world units (s0 = 1)."""
    x, y, z = pos
    s = size
    P = lambda a, b, c_: iso(a, b, c_, 1.0, ox, oy)
    top = [P(x, y, z + s), P(x + s, y, z + s), P(x + s, y + s, z + s), P(x, y + s, z + s)]
    right = [P(x + s, y, z), P(x + s, y + s, z), P(x + s, y + s, z + s), P(x + s, y, z + s)]
    left = [P(x, y + s, z), P(x + s, y + s, z), P(x + s, y + s, z + s), P(x, y + s, z + s)]
    tp, rp, lp = (wpoly(f, R.s(seed, i), 1.8) for i, f in enumerate((top, right, left)))
    if not outline_only:
        if alpha >= 0.99:
            hexa = [P(x, y, z + s), P(x + s, y, z + s), P(x + s, y, z), P(x + s, y + s, z), P(x, y + s, z), P(x, y + s, z + s)]
            R.knockout(wpoly(hexa, R.s(seed, "ko"), 0.5))
        R.fill(tp, faces[0], alpha)
        R.fill(lp, faces[1], alpha)
        R.fill(rp, faces[2], alpha * 0.85)
        R.halftone(rp, "navy", scale=0.6, alpha=0.35 * alpha)
    for pth in (tp, rp, lp):
        R.stroke(pth, "navy", 7, alpha)
    if grid > 1:
        for k in range(1, grid):
            f = s * k / grid
            for a, b in (
                (P(x + f, y, z + s), P(x + f, y + s, z + s)), (P(x, y + f, z + s), P(x + s, y + f, z + s)),
                (P(x + s, y + f, z), P(x + s, y + f, z + s)), (P(x + s, y, z + f), P(x + s, y + s, z + f)),
                (P(x + f, y + s, z), P(x + f, y + s, z + s)), (P(x, y + s, z + f), P(x + s, y + s, z + f)),
            ):
                R.stroke(wline(*a, *b, R.s(seed, "g", k, a[0]), 1.0), "navy", 4.5, alpha)


def draw_bone(R, cx, cy, length, thick, seed, rot=0.0, ink="yellow"):
    c = R.c
    c.save()
    c.translate(cx, cy)
    c.rotate(rot)
    hl = length / 2
    k = thick
    shaft = wrect(-hl + k * 0.6, -k * 0.42, length - k * 1.2, k * 0.84, R.s(seed, "sh"), 1.2)
    knobs = [blob(sx * (hl - k * 0.35), sy * k * 0.42, k * 0.48, k * 0.48, R.s(seed, sx, sy)) for sx in (-1, 1) for sy in (-1, 1)]
    shape = union(shaft, *knobs)
    R.fill(shape, ink)
    R.halftone(shape, "pink", scale=0.6, alpha=0.6)
    R.stroke(shape, "navy", 7)
    c.restore()


def draw_ant(R, x, y, scale=1.0, step=0.0, flip=False):
    c = R.c
    c.save()
    c.translate(x, y)
    c.scale(-scale if flip else scale, scale)
    head = blob(30, -22, 11, 10, R.s("ah"))
    thor = blob(8, -20, 12, 8, R.s("at"))
    abd = blob(-22, -24, 20, 14, R.s("aa"))
    body = union(head, thor, abd)
    for i, lx in enumerate((-2, 8, 18)):
        ph = math.sin(step * 2 * math.pi + i * 2.1) * 6
        R.stroke(wpoly([(lx, -18), (lx - 6 + ph, -8), (lx - 10 + ph, 0)], R.s("lg", i), 0.4, closed=False), "navy", 3.4)
        R.stroke(wpoly([(lx + 2, -18), (lx + 9 - ph, -8), (lx + 12 - ph, 0)], R.s("lg2", i), 0.4, closed=False), "navy", 3.4)
    R.fill(body, "navy", texture=True)
    R.stroke(wpoly([(36, -30), (44, -44), (52, -46)], R.s("an1"), 0.3, closed=False), "navy", 2.8)
    R.stroke(wpoly([(34, -31), (38, -46), (46, -52)], R.s("an2"), 0.3, closed=False), "navy", 2.8)
    R.knockout(blob(33, -25, 2.6, 2.6, 1))
    c.restore()
