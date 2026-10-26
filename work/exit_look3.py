"""THE EXIT MANUAL — look v3 (owner feedback, 26 Oct 2026: dark, cryptic, a whistleblower's transmission;
animation pushed further: camera moves through space, depth, data streams, kinetic type; never a flash).

Builds on exit_look2.py (phone, feed, eye, year grid, documents). New here:
  - Cam: a real perspective camera (x, y, z world -> screen), used for depth, dollies and fly-throughs
  - plane(): draws any 2D drawing on a plane in 3D space (skia perspective matrix)
  - data rain: pre-rendered columns of digits in three depth layers, drifting slowly (parallax)
  - streams(): particles running along curves (data / money flowing)
  - glitch(): horizontal slice displacement + a fixed-width chromatic split. Offsets move smoothly (< 2 Hz),
    brightness never changes: no flash, no strobe.
  - Caption3: words of a caption block appear one after another as they are spoken (kinetic, no pop)
  - HUD: "INTERCEPTED" header with a steady red dot and a running timecode (decoration, left of x 900)
Rules kept: text between y 230 and 1450, nothing important at x > 900, <= 5 words a caption line, 2 lines.
"""
import math

import numpy as np
import skia

from exit_look2 import *            # noqa: F401,F403  (phone, feed, eye, year_grid, doc_lines, Ctx2, Assets2...)
from exit_look2 import Ctx2, Assets2, CAP_CX, _rgb
from exit_engine import W, H, FPS, clamp01, prog, lerp, ease_out, ease_in_out, INK

RED = 0xFFFF3B3B
INK.update({"red": RED})


def smooth(x):
    x = clamp01(x)
    return x * x * x * (x * (6 * x - 15) + 10)


# ------------------------------------------------------------------ assets
class Assets3(Assets2):
    def __init__(self):
        super().__init__()
        self.rain = [self._rain(k) for k in range(3)]
        self.vig = self._vignette()

    def _rain(self, layer):
        """A tall transparent strip of digit columns. layer 0 = far (small, dim), 2 = near (bigger)."""
        size = (18, 26, 38)[layer]
        r = np.random.default_rng(40 + layer)
        h = H * 2
        s = skia.Surface(W, h)
        c = s.getCanvas()
        c.clear(0x00000000)
        f = skia.Font(self.tf["mono"], size)
        pitch = size * 1.25
        ncol = int(W / (size * (2.6, 2.2, 2.0)[layer]))
        for k in range(ncol):
            x = r.uniform(0, W)
            y = r.uniform(-h, 0)
            run = int(r.uniform(8, 34))
            for j in range(int(h / pitch) + 1):
                yy = (y + j * pitch) % h
                pos = j % (run + int(r.uniform(4, 30)))
                if pos > run:
                    continue
                a = (0.25 + 0.75 * (pos / run)) * r.uniform(0.4, 1.0)
                p = skia.Paint(AntiAlias=True)
                p.setColor4f(skia.Color4f(*_rgb(0xFF39FF88), a))
                ch = "0123456789ABCDEF"[int(r.integers(0, 16))] if r.random() < 0.85 else "€$"[int(r.integers(0, 2))]
                c.drawString(ch, x, yy, f, p)
        return s.makeImageSnapshot()

    def _vignette(self):
        s = skia.Surface(W, H)
        c = s.getCanvas()
        c.clear(0x00000000)
        p = skia.Paint(Shader=skia.GradientShader.MakeRadial((540, 860), 1150, [0x00000000, 0x00000000, 0xE0000000],
                                                              [0.0, 0.55, 1.0]))
        c.drawRect(skia.Rect(0, 0, W, H), p)
        return s.makeImageSnapshot()


# ------------------------------------------------------------------ camera
class Cam:
    """Perspective camera looking down +z. World units = px at z = F (the screen plane)."""

    def __init__(self, x=CAP_CX, y=800, z=0.0, F=1100.0, cx=CAP_CX, cy=800, roll=0.0):
        self.x, self.y, self.z, self.F, self.cx, self.cy, self.roll = x, y, z, F, cx, cy, roll

    def p(self, x, y, z):
        """World point -> (sx, sy, scale). z is depth in front of the camera's z."""
        d = (z - self.z)
        if d < 5:
            d = 5
        k = self.F / d
        dx, dy = (x - self.x) * k, (y - self.y) * k
        if self.roll:
            cr, sr = math.cos(self.roll), math.sin(self.roll)
            dx, dy = dx * cr - dy * sr, dx * sr + dy * cr
        return self.cx + dx, self.cy + dy, k


def quad_matrix(w, h, quad):
    m = skia.Matrix()
    ok = m.setPolyToPoly([skia.Point(0, 0), skia.Point(w, 0), skia.Point(w, h), skia.Point(0, h)],
                         [skia.Point(*q) for q in quad])
    return m if ok else None


def plane(X, cam, corners, w, h, draw_fn, alpha=1.0):
    """Draw draw_fn(X) (content in a w x h box) onto a 3D quad given by 4 world corners (tl, tr, br, bl)."""
    if min(c[2] for c in corners) - cam.z < 20:
        return
    quad = [cam.p(*c)[:2] for c in corners]
    m = quad_matrix(w, h, quad)
    if m is None:
        return
    X.c.save()
    if alpha < 1:
        X.c.saveLayerAlpha(None, int(255 * clamp01(alpha)))
    X.c.concat(m)
    draw_fn(X)
    if alpha < 1:
        X.c.restore()
    X.c.restore()


def tilt_quad(cx, cy, w, h, yaw=0.0, pitch=0.0, z=1100.0):
    """Corners of a w x h rectangle centred on (cx, cy, z), rotated by yaw (around y) then pitch (around x)."""
    pts = []
    for (ux, uy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        x, y, zz = ux * w / 2, uy * h / 2, 0.0
        x, zz = x * math.cos(yaw) + zz * math.sin(yaw), -x * math.sin(yaw) + zz * math.cos(yaw)
        y, zz = y * math.cos(pitch) - zz * math.sin(pitch), y * math.sin(pitch) + zz * math.cos(pitch)
        pts.append((cx + x, cy + y, z + zz))
    return pts


# ------------------------------------------------------------------ atmosphere
def data_rain(X, t, alpha=1.0, speed=1.0, layers=(0, 1, 2)):
    """Three depth layers of falling digits; far layers slower and dimmer (parallax). Very low contrast."""
    for k in layers:
        img = X.A.rain[k]
        v = (14, 26, 44)[k] * speed
        a = (0.07, 0.06, 0.05)[k] * alpha
        if a <= 0.002:
            continue
        off = (t * v) % (H * 2)
        p = skia.Paint()
        p.setAlphaf(a)
        X.c.drawImage(img, 0, off - H * 2, skia.SamplingOptions(), p)
        X.c.drawImage(img, 0, off, skia.SamplingOptions(), p)


def vignette(X):
    X.c.drawImage(X.A.vig, 0, 0)


def hud(X, t, alpha=1.0, ep="001", series="EXIT"):
    """Header of an intercepted transmission. The red dot is steady (never blinks)."""
    c = X.c
    c.drawCircle(92, 262, 11, X.paint("red", 0.9 * alpha))
    c.drawCircle(92, 262, 20, X.paint("red", 0.25 * alpha, blur=8))
    X.text("INTERCEPTED", 116, 274, 32, "white", kind="mono", align="left", alpha=0.8 * alpha)
    X.text(f"TRANSMISSION {ep} · {series}", 116, 312, 26, "grey", kind="mono", align="left", alpha=0.85 * alpha)
    s = int(t)
    X.text(f"{s // 60:02d}:{s % 60:02d}:{int((t % 1) * FPS):02d}", 892, 274, 28, "grey", kind="mono", align="right",
           alpha=0.6 * alpha)
    X.text("THE EXIT MANUAL", 892, 312, 24, "grey", kind="sansm", align="right", alpha=0.6 * alpha)
    X.text("staged · public sources only", 892, 340, 20, "grey", kind="mono", align="right", alpha=0.55 * alpha)


def glitch(X, img, amount, t, seed=0, rgb=True):
    """Redraw img (a full-frame snapshot) as horizontal slices pushed sideways by up to amount*60 px.
    Offsets drift smoothly (no frame-to-frame jumps), so nothing flashes. A fixed 6 px cyan/magenta split."""
    if amount <= 0.001:
        X.c.drawImage(img, 0, 0)
        return
    r = np.random.default_rng(seed)
    n = 26
    edges = np.sort(r.uniform(0, H, n - 1))
    edges = np.concatenate([[0], edges, [H]])
    for i in range(n):
        y0, y1 = edges[i], edges[i + 1]
        ph, fr = r.uniform(0, 6.28), r.uniform(0.6, 1.8)
        off = amount * 60 * math.sin(t * fr * 2 * math.pi * 0.5 + ph) * (r.random() < 0.55)
        X.c.save()
        X.c.clipRect(skia.Rect(0, y0, W, y1))
        if rgb and amount > 0.05:
            for colr, dx in ((0xFF00E5FF, -6 * amount), (0xFFFF2E88, 6 * amount)):
                p = skia.Paint()
                p.setColorFilter(skia.ColorFilters.Blend(colr, skia.BlendMode.kModulate))
                p.setBlendMode(skia.BlendMode.kScreen)
                p.setAlphaf(0.5 * min(1, amount * 2))
                X.c.drawImage(img, off + dx, 0, skia.SamplingOptions(), p)
        X.c.drawImage(img, off, 0)
        X.c.restore()


def offscreen(X, fn):
    """Render fn(Y) to a transparent full-frame image (same time, same assets)."""
    s = skia.Surface(W, H)
    c2 = s.getCanvas()
    c2.clear(0x00000000)
    Y = X.__class__(X.A, c2, X.t, X.level)
    fn(Y)
    return s.makeImageSnapshot()


def streams(X, paths, t, color="magenta", n=6, speed=0.6, r=7, alpha=1.0, trail=5, seed=0):
    """Particles running along polylines (data or money in motion). paths = list of point lists."""
    rr = np.random.default_rng(seed)
    for pi, pts in enumerate(paths):
        segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        tot = sum(segs) or 1
        ph0 = rr.uniform(0, 1)
        for k in range(n):
            for j in range(trail):
                u = ((t * speed + ph0 + k / n) - j * 0.012) % 1.0
                d = u * tot
                acc = 0
                for i, L in enumerate(segs):
                    if acc + L >= d:
                        f = (d - acc) / L if L else 0
                        x = lerp(pts[i][0], pts[i + 1][0], f)
                        y = lerp(pts[i][1], pts[i + 1][1], f)
                        break
                    acc += L
                a = alpha * (1 - j / trail) * (0.4 + 0.6 * math.sin(math.pi * u))
                X.c.drawCircle(x, y, r * (1 - j / (trail + 1)), X.paint(color, a))
                if j == 0:
                    X.c.drawCircle(x, y, r * 2.4, X.paint(color, 0.3 * a, blur=8))


def bezier(p0, p1, p2, p3, n=24):
    out = []
    for i in range(n + 1):
        u = i / n
        a, b, c, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


# ------------------------------------------------------------------ kinetic type
def kin_text(X, s, x, y, size, t0, color="white", kind="sans", align="center", dur=0.5, alpha=1.0, glow=0.0,
             track0=0.35, rise=26, out_t=None):
    """Letters arrive one by one: each slides up from 'rise' px, its spacing closes from track0 (x size) to 0.
    No flash: alpha only ramps."""
    if X.t < t0:
        return
    f = X.A.font(kind, size)
    n = len(s)
    widths = [f.measureText(ch) for ch in s]
    total = sum(widths)
    u = clamp01((X.t - t0) / dur)
    tr = track0 * size * (1 - ease_out(u, 3))
    full = total + tr * (n - 1)
    x0 = x - full / 2 if align == "center" else (x - full if align == "right" else x)
    a_out = 1.0 if out_t is None else 1 - prog(X.t, out_t, out_t + 0.3)
    xx = x0
    for i, ch in enumerate(s):
        ui = clamp01((X.t - t0 - i * dur * 0.5 / max(1, n)) / (dur * 0.6))
        e = ease_out(ui, 3)
        X.text(ch, xx, y + rise * (1 - e), size, color, kind=kind, align="left", alpha=alpha * e * a_out,
               glow=glow)
        xx += widths[i] + tr


def typed_mono(X, s, x, y, size, t0, cps=24, color="green", alpha=1.0, cursor=True):
    if X.t < t0:
        return
    n = int((X.t - t0) * cps)
    shown = s[:n]
    X.text(shown, x, y, size, color, kind="mono", align="left", alpha=alpha)
    if cursor and n < len(s) + 6:
        cx = x + X.width(shown, size, "mono") + 4
        X.c.drawRect(skia.Rect(cx, y - size * 0.75, cx + size * 0.55, y + size * 0.12), X.paint(color, 0.8 * alpha))


def count(X, value, x, y, size, color="white", kind="sans", align="center", alpha=1.0, glow=0.0, fmt="{:,}"):
    X.text(fmt.format(int(round(value))), x, y, size, color, kind=kind, align=align, alpha=alpha, glow=glow)


# ------------------------------------------------------------------ captions v3 (word by word)
class Caption3:
    """Shown while its words are spoken. Each word fades/rises in at its estimated time (letters-proportional
    inside the block), so the caption follows the voice. '/' = line break, *word* = accent. <= 5 words a line."""

    def __init__(self, start, end, text, y=1232, size=84, hi="green", speak_end=None):
        self.start, self.end, self.text, self.y, self.size, self.hi = start, end, text, y, size, hi
        self.speak_end = speak_end if speak_end is not None else end
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
        words = [w for toks in self.lines for w, _ in toks]
        lens = [max(2, sum(ch.isalnum() for ch in w)) for w in words]
        tot = sum(lens)
        span = max(0.2, (self.speak_end - start) * 0.92)
        acc, self.wt = 0, []
        for L in lens:
            self.wt.append(start + span * acc / tot)
            acc += L

    def plain(self):
        return " / ".join(" ".join(w for w, _ in toks) for toks in self.lines)

    def draw(self, X):
        t = X.t
        if not (self.start <= t < self.end):
            return
        a_out = 1 - prog(t, self.end - 0.08, self.end)
        size = self.size
        f = "sans"
        sp = X.width(" ", size, f)
        widths = [sum(X.width(w, size, f) for w, _ in toks) + sp * (len(toks) - 1) for toks in self.lines]
        if max(widths) > 800:
            size *= 800 / max(widths)
            sp = X.width(" ", size, f)
            widths = [sum(X.width(w, size, f) for w, _ in toks) + sp * (len(toks) - 1) for toks in self.lines]
        lh = size * 1.06
        top = self.y
        hgt = lh * len(self.lines)
        bed = skia.Paint(AntiAlias=True, Color=0xFF000000)
        bed.setAlphaf(0.62 * a_out)
        bed.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40))
        X.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(CAP_CX - max(widths) / 2 - 24, top - 8,
                                                      CAP_CX + max(widths) / 2 + 24, top + hgt + 12), 30, 30), bed)
        wi = 0
        for li, toks in enumerate(self.lines):
            x = CAP_CX - widths[li] / 2
            base = top + lh * (li + 0.8)
            for w, on in toks:
                ww = X.width(w, size, f)
                t_w = self.wt[wi] if self.start > 0 else -1
                u = ease_out(prog(t, t_w - 0.02, t_w + 0.16), 3)
                a = a_out * (0.18 + 0.82 * u)            # not-yet-spoken words wait as ghosts (no pop-in)
                X.text(w, x, base + 8 * (1 - u), size, self.hi if on else "white", kind=f, align="left", alpha=a,
                       glow=0.35 * u if on else 0.0)
                x += ww + sp
                wi += 1
