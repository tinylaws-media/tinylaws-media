"""SLOP SHOP — the YouTube-Poop layer and the SLOP NEWS cast (built on slop_engine).

Camera: punch zooms on the beat, crash zooms that hold, small shakes; time remaps (a visual stutter
repeats a tiny slice of motion, a freeze holds a frame). Glitch: an RGB split drawn from an offscreen
copy (small, short, never a flash). Bad morphs: outlines interpolated through a lumpy, wrong middle.
Cast: news desk + window, the Moon (morphs to a square, a premium half with a lock, arms for the hug),
the tech boss (an egg in a vest), the Minister of Night (a loaf of bread from the Grand Duchy of Flurb),
the influencer (a ring light with a face), the toaster who has seen things, Thursday (a calendar page),
the werewolf (buffering), the hug (a heart), SOLD stickers, price tags.

No strobing: nothing alternates light/dark; cuts are at most two a second and between scenes of a
similar brightness; the RGB split keeps the luminance of the frame.
"""
import math

import numpy as np
import skia

from slop_engine import *  # noqa: F401,F403
from slop_engine import _hand  # noqa: F401

BEIGE0, BEIGE1, BEIGE2 = 0xFFFFF4E0, 0xFFF2D9B0, 0xFFC99D62
CHROME0, CHROME1, CHROME2 = 0xFFFFFFFF, 0xFFC9D2DE, 0xFF6F7C90
CRUST0, CRUST1, CRUST2 = 0xFFFFD79A, 0xFFE0A050, 0xFF9A5A22
MOON0, MOON1, MOON2 = 0xFFFFFFFF, 0xFFE4DEF5, 0xFFA79BCB
LIME = 0xFFB8F04A
TEAL = 0xFF00E5FF


# ------------------------------------------------------------------ camera, time, glitch
class Cam:
    """punches: [(t, amp, cx, cy, dur)] sudden zoom that eases back; holds: [(t0, t1, amp, cx, cy)]
    crash zoom that snaps in and holds; shakes: [(t0, t1, px)]; tilts: [(t, deg, dur)]."""

    def __init__(self, punches=(), holds=(), shakes=(), tilts=()):
        self.punches, self.holds, self.shakes, self.tilts = list(punches), list(holds), list(shakes), list(tilts)

    def apply(self, c, t):
        s, ox, oy, rot = 1.0, W / 2, H / 2, 0.0
        for (t0, t1, amp, cx, cy) in self.holds:
            if t0 <= t < t1:
                k = ease_out(prog(t, t0, t0 + 0.12), 4)
                s *= 1 + amp * k
                ox, oy = lerp(W / 2, cx, k), lerp(H / 2, cy, k)
        for (t0, amp, cx, cy, d) in self.punches:
            if t0 <= t < t0 + d:
                u = prog(t, t0, t0 + d)
                k = (1 - u) ** 2.2
                s *= 1 + amp * k
                ox, oy = lerp(ox, cx, k), lerp(oy, cy, k)
        dx = dy = 0.0
        for (t0, t1, px) in self.shakes:
            if t0 <= t < t1:
                f = int(t * 24)
                rng = np.random.default_rng(f)
                fade = 1 - prog(t, t0, t1) ** 2
                dx += rng.uniform(-px, px) * fade
                dy += rng.uniform(-px, px) * fade
        for (t0, deg, d) in self.tilts:
            if t0 <= t < t0 + d:
                rot += deg * (1 - prog(t, t0, t0 + d)) ** 2
        c.translate(ox + dx, oy + dy)
        if rot:
            c.rotate(rot)
        c.scale(s, s)
        c.translate(-ox, -oy)


def remap(t, stutters=(), freezes=()):
    """Visual time: a stutter (t0, t1, chunk) loops the slice [t0, t0+chunk) until t1; a freeze (t0, t1) holds t0."""
    for (t0, t1, ch) in stutters:
        if t0 <= t < t1:
            return t0 + ((t - t0) % ch)
    for (t0, t1) in freezes:
        if t0 <= t < t1:
            return t0
    return t


def _cm(m):
    p = skia.Paint()
    p.setColorFilter(skia.ColorFilters.Matrix(m))
    return p


def fry_matrix(k):
    """Extra saturation + contrast (the 'over-processed' look), as a 4x5 colour matrix."""
    s = 1 + 0.8 * k
    con = 1 + 0.15 * k
    lr, lg, lb = 0.2126 * (1 - s), 0.7152 * (1 - s), 0.0722 * (1 - s)
    off = -0.07 * k
    return [(lr + s) * con, lg * con, lb * con, 0, off,
            lr * con, (lg + s) * con, lb * con, 0, off,
            lr * con, lg * con, (lb + s) * con, 0, off,
            0, 0, 0, 1, 0]


def post(R, draw, split=0.0, fry=0.0):
    """Draw the scene offscreen, then composite it: RGB split = the red and blue channels nudged apart
    and added back to the green one (the brightness of the frame is unchanged, only edges fringe);
    fry = the saturated look. Neither ever flashes."""
    s = skia.Surface(W, H)
    c2 = s.getCanvas()
    c2.clear(skia.ColorBLACK)
    draw(Slop(R.A, c2, R.t))
    img = s.makeImageSnapshot()
    c = R.c
    if fry > 0:
        c.saveLayer(None, _cm(fry_matrix(fry)))
    if split <= 0.5:
        c.drawImage(img, 0, 0)
    else:
        c.drawRect(skia.Rect(0, 0, W, H), R.paint(skia.ColorBLACK))
        for (dx, dy, row) in ((-split, 0, 0), (0, 0, 1), (split, split * 0.35, 2)):
            m = [0] * 20
            m[row * 6] = 1
            m[18] = 1
            p = _cm(m)
            p.setBlendMode(skia.BlendMode.kPlus)
            c.drawImage(img, dx, dy, skia.SamplingOptions(), p)
    if fry > 0:
        c.restore()


# ------------------------------------------------------------------ shapes & morphs
def ring_pts(cx, cy, r, n=64):
    return [(cx + math.cos(i / n * 2 * math.pi) * r, cy + math.sin(i / n * 2 * math.pi) * r) for i in range(n)]


def square_pts(cx, cy, r, n=64, round_=0.08):
    out = []
    for i in range(n):
        a = i / n * 2 * math.pi
        x, y = math.cos(a), math.sin(a)
        m = max(abs(x), abs(y))
        out.append((cx + x / m * r * (1 - round_ * 0.0), cy + y / m * r))
    return out


def bad_morph(a, b, u, seed=1, amp=0.16):
    """Interpolate two outlines through a wrong middle: lumps, a pinched side, an extra corner."""
    rng = np.random.default_rng(seed)
    n = len(a)
    ph = rng.uniform(0, 6.28, 3)
    lump = math.sin(math.pi * clamp01(u)) * amp
    cx = sum(p[0] for p in a) / n
    cy = sum(p[1] for p in a) / n
    out = []
    for i, (pa, pb) in enumerate(zip(a, b)):
        x, y = lerp(pa[0], pb[0], u), lerp(pa[1], pb[1], u)
        ang = i / n * 2 * math.pi
        k = 1 + lump * (math.sin(3 * ang + ph[0]) + 0.8 * math.sin(7 * ang + ph[1]) * (u > 0.5)) \
            + lump * 1.4 * math.exp(-((ang - ph[2]) % 6.28 - 3.14) ** 2 * 6)
        out.append((cx + (x - cx) * k, cy + (y - cy) * k))
    return out


def path_of(pts):
    return poly(pts)


# ------------------------------------------------------------------ studio
def news_bg(R, t, drift=0.0, top=0xFF3A1670, bot=0xFF0F2A6A):
    R.gradient_bg(top, VIOLET, bot, drift)
    c = R.c
    # soft studio light cones
    for (x, a) in ((180, 0.10), (900, 0.08)):
        g = R.lin(x, 230, x, 1300, [argb(WHITE, a), argb(WHITE, 0)])
        c.drawPath(poly([(x - 40, 230), (x + 40, 230), (x + 260, 1300), (x - 260, 1300)]), R.paint(shader=g))
    # LED wall dots
    for j in range(9):
        for i in range(14):
            x, y = 40 + i * 78, 690 + j * 66
            R.fill(circle(x, y, 4), WHITE, 0.07)


def window(R, x, y, w, h, t, inside, frame=0xFF1B0B26):
    """A rounded window onto the night sky; inside(R) draws what is in it (clipped)."""
    c = R.c
    box = rrect(x, y, w, h, 34)
    sh = R.lin(0, y, 0, y + h, [0xFF140A3C, 0xFF2B1D6E, 0xFF4B2C86])
    R.fill(box, shader=sh)
    c.save()
    c.clipPath(box, doAntiAlias=True)
    rng = np.random.default_rng(12)
    for i in range(26):
        sx, sy = x + rng.uniform(0, w), y + rng.uniform(0, h)
        R.fill(circle(sx, sy, rng.uniform(2, 4.5)), WHITE, 0.55 + 0.25 * math.sin(t * 1.3 + i))
    inside(R)
    c.restore()
    R.stroke(box, frame, 16)
    R.stroke(rrect(x + 8, y + 8, w - 16, h - 16, 28), WHITE, 3, 0.25)


def star4(R, x, y, r, color=YELLOW, rot=0.0):
    c = R.c
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    p = poly([(0, -r), (r * 0.22, -r * 0.22), (r, 0), (r * 0.22, r * 0.22), (0, r), (-r * 0.22, r * 0.22),
              (-r, 0), (-r * 0.22, -r * 0.22)])
    R.fill(p, color)
    R.stroke(p, INK, 5)
    c.restore()


def desk(R, y=1110, label="SLOP NEWS"):
    top = poly([(70, y), (1010, y), (1060, y + 40), (20, y + 40)])
    R.fill(top, shader=R.lin(0, y, 0, y + 40, [0xFFFFFFFF, 0xFFBFC7FF]))
    R.stroke(top, INK, 6)
    front = poly([(20, y + 40), (1060, y + 40), (1010, y + 175), (70, y + 175)])
    R.fill(front, shader=R.lin(0, y + 40, W, y + 175, [MAGENTA, VIOLET, CYAN]))
    R.stroke(front, INK, 6)
    R.text(label, 540, y + 128, "bungee", 64, WHITE, None, alpha=0.22)
    # glossy streak
    R.fill(poly([(120, y + 48), (190, y + 48), (150, y + 168), (90, y + 168)]), WHITE, 0.18)


def news_bug(R, t, label="LIVE", sub="SLOP NEWS", alpha=1.0):
    """The channel bug under the reality bar: a red LIVE pill (steady, never blinks) + SLOP NEWS."""
    R.fill(rrect(60, 340, 150, 64, 32), RED, alpha)
    R.stroke(rrect(60, 340, 150, 64, 32), INK, 5, alpha)
    R.fill(circle(96, 372, 11), WHITE, alpha)
    R.text(label, 156, 389, "bungee", 34, WHITE, None, alpha=alpha)
    R.text(sub, 230, 389, "bungee", 38, WHITE, INK, 8, align="left", alpha=alpha)


def ticker(R, t, items, y=1262, speed=150):
    R.fill(rrect(-10, y - 42, W + 20, 64, 0), INK, 0.9)
    R.fill(rrect(-10, y - 42, 220, 64, 0), YELLOW)
    R.text("BREAKING", 100, y + 2, "bungee", 32, INK, None)
    s = "   •   ".join(items) + "   •   "
    f = R.A.font("comic", 40)
    wtot = f.measureText(s)
    x0 = 230 - (t * speed) % wtot
    c = R.c
    c.save()
    c.clipRect(skia.Rect(212, y - 42, W, y + 22))
    for k in range(3):
        R.text(s, x0 + k * wtot, y + 3, "comic", 40, WHITE, None, align="left")
    c.restore()


def lower_third(R, name, role, k=1.0, y=1240, color=YELLOW):
    if k <= 0:
        return
    c = R.c
    c.save()
    c.translate(70, y)
    c.scale(k, 1)
    f = R.A.font("bungee", 40)
    w = max(f.measureText(name) + 60, R.A.font("comic", 38).measureText(role) + 60)
    w = min(w, 800)
    R.fill(rrect(0, -52, w, 62, 10), color)
    R.stroke(rrect(0, -52, w, 62, 10), INK, 5)
    R.text(name, 30, -6, "bungee", 40, INK, None, align="left")
    R.fill(rrect(0, 12, w, 54, 10), INK, 0.92)
    R.text(role, 30, 52, "comic", 38, WHITE, None, align="left")
    c.restore()


# ------------------------------------------------------------------ props
def price_tag(R, x, y, lines, rot=-10, s=1.0, tiny=None, string_to=None, stamp=None, stamp_k=0.0):
    c = R.c
    if string_to:
        R.stroke(poly([string_to, (x, y)], False), INK, 4)
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    w, h = 300, 96 + 62 * (len(lines) - 1) + (34 if tiny else 0)
    tag_ = poly([(0, 0), (46, -h / 2), (w, -h / 2), (w, h / 2), (46, h / 2)])
    R.fill(tag_, 0xFFFFF8EC)
    R.stroke(tag_, INK, 6)
    R.fill(circle(30, 0, 11), 0xFF2B1D6E)
    R.stroke(circle(30, 0, 11), INK, 4)
    yy = -h / 2 + 70
    for i, ln in enumerate(lines):
        R.text(ln, 175, yy + i * 62, "anton" if i == 0 else "comic", 64 if i == 0 else 44, RED if i == 0 else INK, None)
    if tiny:   # the hidden detail: only readable on a pause
        R.text(tiny, 175, h / 2 - 12, "comic", 27, 0xFF2B1D6E, None)
    if stamp and stamp_k > 0:
        k = lerp(2.0, 1.0, ease_out_back(clamp01(stamp_k), 1.3))
        c.save()
        c.translate(175, 0)
        c.rotate(12)
        c.scale(k, k)
        R.stroke(rrect(-120, -42, 240, 84, 12), GREEN, 9)
        R.text(stamp, 0, 24, "bungee", 58, GREEN, None)
        c.restore()
    c.restore()


def sold(R, x, y, s=1.0, rot=-12, text="SOLD", k=1.0, color=RED):
    """A SOLD sticker slapped on: lands big and settles (k = 0..1 progress of the slap)."""
    if k <= 0:
        return
    sc = s * lerp(1.9, 1.0, ease_out_back(clamp01(k), 1.2))
    c = R.c
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(sc, sc)
    f = R.A.font("bungee", 96)
    w = f.measureText(text) + 80
    b = rrect(-w / 2, -76, w, 132, 22)
    R.fill(b, color)
    R.stroke(b, INK, 9)
    R.stroke(rrect(-w / 2 + 14, -62, w - 28, 104, 14), WHITE, 4, 0.8)
    R.text(text, 0, 30, "bungee", 96, WHITE, INK, 8)
    c.restore()


def heart(R, x, y, s=1.0, rot=0.0, sq=1.0, color=0xFFFF4F9A):
    c = R.c
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s / sq ** 0.5, s * sq)
    p = skia.Path()
    p.moveTo(0, 40)
    p.cubicTo(-110, -30, -70, -120, 0, -66)
    p.cubicTo(70, -120, 110, -30, 0, 40)
    p.close()
    R.glossy(p, -10, -40, 90, 0xFFFFC4DD, color, 0xFFB0145A, INK, 7)
    c.restore()


def lock(R, x, y, s=1.0):
    c = R.c
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    R.stroke(rrect(-34, -70, 68, 90, 34), INK, 22)
    R.stroke(rrect(-34, -70, 68, 90, 34), 0xFFC9D2DE, 12)
    b = rrect(-60, -20, 120, 96, 16)
    R.glossy(b, 0, 20, 70, 0xFFFFF6B0, YELLOW, 0xFFE0A800, INK, 7)
    R.fill(circle(0, 20, 12), INK)
    R.fill(rrect(-5, 20, 10, 30, 4), INK)
    c.restore()


def spinner(R, x, y, r, t, alpha=1.0):
    for i in range(10):
        a = i / 10 * 2 * math.pi + t * 5
        R.fill(circle(x + math.cos(a) * r, y + math.sin(a) * r, r * 0.16), WHITE, alpha * (0.2 + 0.8 * i / 9))


# ------------------------------------------------------------------ the Moon
def moon_body(R, x, y, r, t, sq=0.0, seed=4, look=(0, 0), expr="smile", talk=0.0, half=0.0, eye_slip=0.0,
              arms=0.0, arm_reach=0.0, blink=False):
    """The Moon. sq 0..1 morphs it (badly) into a square; half 0..1 hides the right half behind a 'premium'
    shadow; arms 0..1 grows two grey arms that reach (arm_reach) for a hug."""
    c = R.c
    a = ring_pts(x, y, r)
    b = square_pts(x, y, r * 0.92)
    pts = bad_morph(a, b, sq, seed, amp=0.13) if 0 < sq < 1 else (b if sq >= 1 else a)
    body = path_of(pts) if sq > 0 else circle(x, y, r)
    if arms > 0:
        for sgn in (-1, 1):
            ex = x + sgn * (r * 0.95 + arm_reach * 260)
            ey = y + r * 0.35 + arm_reach * 140
            R.stroke(poly([(x + sgn * r * 0.7, y + r * 0.25), (ex, ey)], False), INK, 70 * arms)
            R.stroke(poly([(x + sgn * r * 0.7, y + r * 0.25), (ex, ey)], False), MOON1, 52 * arms)
            R.glossy(circle(ex, ey, 52 * arms), ex, ey, 52 * arms, MOON0, MOON1, MOON2, INK, 6)
    R.glossy(body, x, y, r, MOON0, MOON1, MOON2, INK, 8)
    c.save()
    c.clipPath(body, doAntiAlias=True)
    for (dx, dy, cr) in ((-0.5, 0.42, 0.15), (0.52, -0.5, 0.12), (0.48, 0.52, 0.1), (-0.1, -0.62, 0.08)):
        R.fill(circle(x + dx * r, y + dy * r, cr * r), 0xFFBDB2DD)
        R.stroke(circle(x + dx * r, y + dy * r, cr * r), 0xFF9C90C4, 3)
    if half > 0:
        R.fill(rrect(x + lerp(r * 1.2, 0, half), y - r * 1.3, r * 1.4, r * 2.6, 0), 0xFF120A2E, 0.93)
    c.restore()
    # face
    fy = y - 0.1 * r
    for k, ex in enumerate((-0.33, 0.33)):
        cx, cy = x + ex * r + (eye_slip * r * 0.9 if k == 1 else 0), fy + (eye_slip * r * 0.5 if k == 1 else 0)
        er = r * (0.13 if k == 0 else 0.15)
        R.fill(oval(cx, cy, er, er * 1.2), WHITE)
        R.stroke(oval(cx, cy, er, er * 1.2), INK, 5)
        if blink:
            R.stroke(poly([(cx - er, cy), (cx + er, cy)], False), INK, 6)
        else:
            R.fill(circle(cx + look[0] * er * 0.45, cy + look[1] * er * 0.45, er * 0.5), INK)
            R.fill(circle(cx + look[0] * er * 0.45 - er * 0.18, cy + look[1] * er * 0.45 - er * 0.2, er * 0.15), WHITE)
    m = skia.Path()
    my = y + r * 0.3
    if talk > 0.05 or expr == "open":
        op = max(talk, 0.4 if expr == "open" else 0)
        R.fill(oval(x, my + r * 0.04, r * 0.2, r * (0.05 + 0.16 * op)), 0xFF3A0B24)
        R.stroke(oval(x, my + r * 0.04, r * 0.2, r * (0.05 + 0.16 * op)), INK, 5)
    elif expr == "smile":
        m.moveTo(x - r * 0.28, my)
        m.quadTo(x, my + r * 0.24, x + r * 0.28, my)
        R.stroke(m, INK, 6)
    elif expr == "grin":
        m.moveTo(x - r * 0.4, my - r * 0.04)
        m.quadTo(x, my + r * 0.4, x + r * 0.4, my - r * 0.04)
        m.close()
        R.fill(m, 0xFF3A0B24)
        c.save()
        c.clipPath(m, doAntiAlias=True)
        for i in range(11):
            tx = x - r * 0.4 + i * r * 0.08
            R.fill(rrect(tx, my - r * 0.06, r * 0.06, r * 0.1, 2), WHITE)
        c.restore()
        R.stroke(m, INK, 6)
    else:
        m.moveTo(x - r * 0.22, my + r * 0.06)
        m.lineTo(x + r * 0.22, my + r * 0.05)
        R.stroke(m, INK, 6)
    return body


# ------------------------------------------------------------------ tech boss
def tech_boss(R, x, y, s=1.0, t=0.0, talk=0.0, expr="smug", point=0.0, sold_k=0.0):
    """A USB stick in a quilted vest, with a headset mic and a lanyard. (x, y) = feet. Invented archetype."""
    c = R.c
    c.save()
    c.translate(x, y + math.sin(t * 2.4) * 4)
    c.scale(s, s)
    R.fill(oval(0, 6, 150, 22), INK, 0.25)
    for fx in (-50, 50):   # legs + shoes
        R.stroke(poly([(fx, -120), (fx, -16)], False), INK, 34)
        R.stroke(poly([(fx, -120), (fx, -16)], False), 0xFF3B3F5C, 22)
        R.fill(oval(fx + 10, -10, 44, 18), WHITE)
        R.stroke(oval(fx + 10, -10, 44, 18), INK, 5)
    # body: a USB stick (connector on top like a tiny hat)
    R.fill(rrect(-70, -650, 140, 110, 10), shader=R.lin(-70, 0, 70, 0, [0xFFE6EAF2, 0xFF9AA3B8, 0xFFE6EAF2]))
    R.stroke(rrect(-70, -650, 140, 110, 10), INK, 6)
    for hx in (-30, 30):
        R.fill(rrect(hx - 14, -625, 28, 28, 4), INK)
    stick = rrect(-150, -560, 300, 470, 70)
    R.glossy(stick, 0, -360, 260, 0xFFFFFFFF, 0xFFE4E0EE, 0xFFA8A0C0, INK, 8)
    R.fill(rrect(-150, -540, 300, 34, 0), MAGENTA, 0.9)
    # vest (puffy, quilted)
    vest = skia.Path()
    vest.moveTo(-140, -330)
    vest.quadTo(-70, -300, -40, -230)
    vest.lineTo(-40, -100)
    vest.quadTo(-120, -110, -146, -200)
    vest.close()
    for sgn in (1, -1):
        c.save()
        c.scale(sgn, 1)
        R.glossy(vest, -100, -230, 120, 0xFF5C6380, 0xFF353A52, 0xFF1C1F30, INK, 6)
        for k in range(3):
            R.stroke(poly([(-140 + k * 4, -280 + k * 55), (-44, -250 + k * 55)], False), INK, 3, 0.5)
        c.restore()
    # lanyard + badge
    R.stroke(poly([(-60, -330), (0, -230), (60, -330)], False), RED, 8)
    R.fill(rrect(-40, -236, 80, 96, 10), WHITE)
    R.stroke(rrect(-40, -236, 80, 96, 10), INK, 5)
    R.text("CEO", 0, -178, "bungee", 26, INK, None)
    # face: confident half-lids, huge smile
    for ex in (-58, 58):
        R.fill(oval(ex, -420, 34, 26), WHITE)
        R.stroke(oval(ex, -420, 34, 26), INK, 5)
        R.fill(circle(ex + 6, -416, 12), INK)
        R.fill(rrect(ex - 36, -450, 72, 26 if expr == "smug" else 12, 6), 0xFFE4E0EE)
        R.stroke(poly([(ex - 34, -424 + (0 if expr != "smug" else 0)), (ex + 34, -428)], False), INK, 5)
    my = -350
    op = clamp01(talk)
    m = skia.Path()
    m.moveTo(-80, my)
    m.quadTo(0, my + 40 + 70 * op, 80, my)
    m.quadTo(0, my + 20 + 20 * op, -80, my)
    m.close()
    R.fill(m, 0xFF3A0B24)
    c.save()
    c.clipPath(m, doAntiAlias=True)
    R.fill(rrect(-80, my - 4, 160, 18, 4), WHITE)
    c.restore()
    R.stroke(m, INK, 6)
    # headset mic
    R.stroke(poly([(-150, -470), (-140, -340), (-60, -330)], False), INK, 7)
    R.fill(circle(-58, -330, 11), INK)
    # arm (points up at the slide)
    ax, ay = 150, -300
    hx, hy = ax + lerp(60, 120, point), ay - lerp(40, 260, point)
    R.stroke(poly([(ax - 20, ay), (hx, hy)], False), INK, 34)
    R.stroke(poly([(ax - 20, ay), (hx, hy)], False), 0xFFE4E0EE, 22)
    R.glossy(circle(hx, hy, 30), hx, hy, 30, 0xFFFFFFFF, 0xFFE4E0EE, 0xFFA8A0C0, INK, 5)
    c.restore()
    if sold_k > 0:
        sold(R, x - 10 * s, y - 380 * s, 0.9, -14, k=sold_k)


def keynote(R, t, slide):
    """Dark stage, a huge rounded screen; slide(R, cx, cy) draws the slide's content."""
    R.c.drawRect(skia.Rect(0, 0, W, H), R.paint(shader=R.lin(0, 0, 0, H, [0xFF0B0820, 0xFF1A1240, 0xFF07051A])))
    g = R.rad(W / 2, 760, 700, [argb(0xFF6E5AB8, 0.45), argb(0xFF6E5AB8, 0)])
    R.c.drawRect(skia.Rect(0, 0, W, H), R.paint(shader=g))
    scr = rrect(70, 450, 830, 560, 30)
    R.fill(scr, shader=R.lin(0, 450, 0, 1010, [0xFF1D1648, 0xFF0E0A2A]))
    R.stroke(scr, 0xFF3A2F7A, 6)
    R.c.save()
    R.c.clipPath(scr, doAntiAlias=True)
    slide(R, 485, 730)
    R.c.restore()
    # stage floor
    R.c.drawRect(skia.Rect(0, 1285, W, H), R.paint(shader=R.lin(0, 1285, 0, H, [0xFF2A2060, 0xFF0B0820])))
    R.stroke(poly([(0, 1285), (W, 1285)], False), 0xFF6E5AB8, 3, 0.6)


# ------------------------------------------------------------------ minister (Grand Duchy of Flurb)
def flurb_flag(R, x, y, t, w=300, h=200):
    """An invented flag: lime and magenta waves with a spoon. Matches no real flag."""
    c = R.c
    c.save()
    c.translate(x, y)
    R.stroke(poly([(0, -30), (0, h + 380)], False), INK, 14)
    R.stroke(poly([(0, -30), (0, h + 380)], False), 0xFFD8C08A, 8)
    pts_top, pts_bot = [], []
    for i in range(17):
        u = i / 16
        wv = math.sin(u * 5 - t * 3) * 14 * u
        pts_top.append((u * w, wv))
        pts_bot.append((u * w, h + wv))
    p = poly(pts_top + pts_bot[::-1])
    R.fill(p, LIME)
    c.save()
    c.clipPath(p, doAntiAlias=True)
    for k in range(3):
        R.fill(rrect(0, h * 0.33 + math.sin(t * 3) * 3, w, h * 0.33, 0), MAGENTA)
    # spoon
    R.fill(oval(w * 0.55, h * 0.5, 30, 22), WHITE)
    R.stroke(oval(w * 0.55, h * 0.5, 30, 22), INK, 4)
    R.stroke(poly([(w * 0.55 + 26, h * 0.5), (w * 0.9, h * 0.5 - 8)], False), INK, 10)
    R.stroke(poly([(w * 0.55 + 26, h * 0.5), (w * 0.9, h * 0.5 - 8)], False), WHITE, 5)
    c.restore()
    R.stroke(p, INK, 6)
    c.restore()


def minister(R, x, y, s=1.0, t=0.0, talk=0.0, look=0.0, sold_k=0.0, sweat=0.0):
    """A loaf of bread in a sash, with a monocle and a magnificent moustache. (x, y) = top of the podium."""
    c = R.c
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    loaf = skia.Path()
    loaf.moveTo(-150, 40)
    loaf.lineTo(-150, -260)
    loaf.cubicTo(-200, -300, -170, -420, -60, -410)
    loaf.cubicTo(-20, -450, 20, -450, 60, -410)
    loaf.cubicTo(170, -420, 200, -300, 150, -260)
    loaf.lineTo(150, 40)
    loaf.close()
    R.glossy(loaf, -20, -260, 240, CRUST0, CRUST1, CRUST2, INK, 8)
    # score marks on the crust
    for k in range(3):
        R.stroke(poly([(-90 + k * 70, -405), (-60 + k * 70, -370)], False), CRUST2, 7, 0.8)
    # sash
    R.c.save()
    R.c.clipPath(loaf, doAntiAlias=True)
    sash = poly([(-160, -200), (-110, -230), (170, 20), (110, 60)])
    R.fill(sash, MAGENTA)
    R.stroke(sash, INK, 5)
    R.c.restore()
    R.glossy(circle(40, -80, 26), 40, -80, 26, 0xFFFFF6B0, YELLOW, 0xFFE0A800, INK, 5)
    # eyes + monocle
    for k, ex in enumerate((-55, 55)):
        R.fill(oval(ex, -250, 26, 30), WHITE)
        R.stroke(oval(ex, -250, 26, 30), INK, 5)
        R.fill(circle(ex + look * 8, -246, 11), INK)
        R.fill(rrect(ex - 30, -284, 60, 16, 6), CRUST1)
    R.stroke(circle(55, -250, 42), 0xFFE8C860, 7)
    R.stroke(poly([(95, -240), (120, -120)], False), 0xFFE8C860, 3)
    # sweat (Thursday was not informed)
    if sweat > 0:
        d = skia.Path()
        d.moveTo(-120, -300)
        d.quadTo(-104, -270, -120, -258)
        d.quadTo(-136, -270, -120, -300)
        R.fill(d, 0xFF9FE8FF)
        R.stroke(d, INK, 4)
    # mouth + moustache
    op = clamp01(talk)
    R.fill(oval(0, -160, 36, 10 + 26 * op), 0xFF3A0B24)
    R.stroke(oval(0, -160, 36, 10 + 26 * op), INK, 5)
    for sgn in (-1, 1):
        m = skia.Path()
        m.moveTo(0, -192)
        m.cubicTo(sgn * 40, -215, sgn * 90, -200, sgn * 120, -230 - 10 * math.sin(t * 3))
        m.cubicTo(sgn * 100, -172, sgn * 50, -170, 0, -180)
        m.close()
        R.fill(m, 0xFF4A2A14)
        R.stroke(m, INK, 4)
    c.restore()
    # podium (in front)
    pod = poly([(x - 230 * s, y + 10 * s), (x + 230 * s, y + 10 * s), (x + 190 * s, y + 420 * s), (x - 190 * s, y + 420 * s)])
    R.fill(pod, shader=R.lin(0, y, 0, y + 420 * s, [0xFF5B3A9A, 0xFF2A1458]))
    R.stroke(pod, INK, 7)
    R.glossy(circle(x, y + 150 * s, 62 * s), x, y + 150 * s, 62 * s, 0xFFFFF6B0, YELLOW, 0xFFE0A800, INK, 5)
    R.stroke(oval(x, y + 150 * s, 30 * s, 20 * s), INK, 4)   # the Flurb seal: a spoon in a circle
    for k, (mx, a) in enumerate(((-70, -14), (0, 0), (70, 14))):
        R.c.save()
        R.c.translate(x + mx * s, y + 10 * s)
        R.c.rotate(a)
        R.stroke(poly([(0, 0), (0, -90 * s)], False), INK, 10 * s)
        R.fill(rrect(-16 * s, -130 * s, 32 * s, 48 * s, 14 * s), 0xFF2B2B3A)
        R.stroke(rrect(-16 * s, -130 * s, 32 * s, 48 * s, 14 * s), INK, 4)
        R.c.restore()
    if sold_k > 0:
        sold(R, x, y - 240 * s, 0.85, 10, k=sold_k)


# ------------------------------------------------------------------ Thursday
def thursday(R, x, y, s=1.0, t=0.0, talk=0.0, expr="shock", sold_k=0.0, rot=0.0):
    c = R.c
    c.save()
    c.translate(x, y)
    c.rotate(rot + math.sin(t * 2.6) * 2)
    c.scale(s, s)
    page = rrect(-170, -210, 340, 420, 26)
    R.fill(oval(0, 230, 160, 18), INK, 0.2)
    R.glossy(page, -20, -40, 300, WHITE, 0xFFF4F1FA, 0xFFD6D0E6, INK, 7)
    R.fill(rrect(-170, -210, 340, 110, 26), RED)
    R.fill(rrect(-170, -140, 340, 40, 0), RED)
    R.stroke(page, INK, 7)
    for rx in (-90, 0, 90):
        R.fill(circle(rx, -210, 14), INK)
    R.text("THURSDAY", 0, -132, "bungee", 46, WHITE, None)
    for k, ex in enumerate((-62, 62)):
        R.fill(circle(ex, -10, 40 if expr == "shock" else 32), WHITE)
        R.stroke(circle(ex, -10, 40 if expr == "shock" else 32), INK, 5)
        R.fill(circle(ex, -6, 12 if expr == "shock" else 15), INK)
    op = clamp01(talk)
    R.fill(oval(0, 110, 34 + 6 * op, 22 + 30 * op), 0xFF3A0B24)
    R.stroke(oval(0, 110, 34 + 6 * op, 22 + 30 * op), INK, 5)
    c.restore()
    if sold_k > 0:
        sold(R, x, y + 40 * s, 0.85, -8, k=sold_k)


# ------------------------------------------------------------------ influencer
def influencer(R, x, y, s=1.0, t=0.0, talk=0.0, glow=0.0, pose=0.0):
    """A ring light with a face in the middle, on a tripod; glow 0..1 makes it shine like a moon."""
    c = R.c
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    if glow > 0:
        g = R.rad(0, 0, 420, [argb(0xFFFFF6E8, 0.55 * glow), argb(0xFFFFF6E8, 0)])
        c.drawCircle(0, 0, 420, R.paint(shader=g))
    # tripod (hidden once it flies)
    if pose < 0.5:
        for a in (-18, 0, 18):
            c.save()
            c.rotate(a)
            R.stroke(poly([(0, 190), (0, 640)], False), INK, 16)
            R.stroke(poly([(0, 190), (0, 640)], False), 0xFF9AA3B8, 8)
            c.restore()
    ring = skia.Path()
    ring.addCircle(0, 0, 200)
    ring.addCircle(0, 0, 138)
    ring.setFillType(skia.PathFillType.kEvenOdd)
    R.fill(ring, shader=R.rad(-60, -60, 300, [WHITE, 0xFFFFF0F8, 0xFFE8D6F0]))
    R.stroke(circle(0, 0, 200), INK, 8)
    R.stroke(circle(0, 0, 138), INK, 6)
    for i in range(24):
        a = i / 24 * 2 * math.pi
        R.fill(circle(math.cos(a) * 169, math.sin(a) * 169, 9), 0xFFFFF6B0, 0.9)
    # face (in the hole)
    R.fill(circle(0, 0, 132), shader=R.rad(-30, -40, 200, [0xFFFFE3F0, 0xFFFFB8D8, 0xFFE87AB0]))
    for k, ex in enumerate((-46, 46)):
        R.fill(oval(ex, -20, 24, 30), WHITE)
        R.stroke(oval(ex, -20, 24, 30), INK, 5)
        R.fill(circle(ex + 4, -14, 13), INK)
        R.fill(circle(ex, -20, 4), WHITE)
        for j in range(3):   # lashes
            R.stroke(poly([(ex - 18 + j * 18, -48), (ex - 24 + j * 22, -66)], False), INK, 5)
    op = clamp01(talk)
    if pose > 0.5:   # duck face
        R.fill(oval(0, 52, 34, 20), 0xFFFF4F9A)
        R.stroke(oval(0, 52, 34, 20), INK, 5)
    else:
        R.fill(oval(0, 52, 44, 10 + 26 * op), 0xFF3A0B24)
        R.stroke(oval(0, 52, 44, 10 + 26 * op), INK, 5)
        R.fill(rrect(-40, 40, 80, 12, 4), WHITE)
    for sgn in (-1, 1):
        R.fill(oval(sgn * 84, 30, 22, 12), 0xFFFF7AC6, 0.7)
    c.restore()


def story_ui(R, t, prog_k, name="@ringlight.glow"):
    """A generic phone 'story' frame: progress bars, a name chip, hearts. No real app's design."""
    for i in range(3):
        x0 = 70 + i * 280
        R.fill(rrect(x0, 450, 260, 10, 5), WHITE, 0.4)
        f = 1.0 if i < 1 else (clamp01(prog_k) if i == 1 else 0)
        R.fill(rrect(x0, 450, 260 * f, 10, 5), WHITE, 0.95)
    R.fill(circle(104, 512, 30), shader=R.lin(74, 482, 134, 542, [MAGENTA, YELLOW]))
    R.fill(circle(104, 512, 22), 0xFFFFB8D8)
    R.text(name, 150, 526, "comic", 40, WHITE, INK, 6, align="left")


# ------------------------------------------------------------------ toaster
def toaster_char(R, x, y, s=1.0, t=0.0, talk=0.0, toast_up=0.0, burnt=1.0, smoke=1.0, sold_k=0.0, stare=1.0):
    """A chrome toaster with a thousand-yard stare. (x, y) = bottom centre."""
    c = R.c
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    R.fill(oval(0, 8, 260, 26), INK, 0.3)
    # toast slices (behind the body)
    for k, sx in enumerate((-80, 80)):
        up = toast_up * (1.0 if k == 0 else 0.7)
        ty = -470 - up * 220
        sl = rrect(sx - 70, ty, 140, 190, 40)
        col = (0xFFE9B872, 0xFFC98A48, 0xFF7A4A24) if burnt < 0.5 else (0xFF6A4026, 0xFF4A2A18, 0xFF2A160C)
        R.glossy(sl, sx, ty + 60, 100, *col, INK, 6, hl=False)
    if smoke > 0:
        for i in range(4):
            u = ((t * 0.35 + i * 0.25) % 1.0)
            R.fill(circle(-60 + math.sin(u * 6 + i) * 30, -520 - u * 260, 26 + u * 40), 0xFFB8B0C8, 0.35 * (1 - u) * smoke)
    body = rrect(-250, -430, 500, 430, 110)
    R.glossy(body, -40, -260, 360, CHROME0, CHROME1, CHROME2, INK, 8)
    R.fill(rrect(-180, -440, 160, 26, 13), INK)
    R.fill(rrect(20, -440, 160, 26, 13), INK)
    # reflection streaks
    R.fill(rrect(-210, -380, 30, 300, 15), WHITE, 0.45)
    # lever
    R.fill(rrect(240, -300 + toast_up * 120, 60, 34, 12), INK)
    # eyes: tired, the stare
    for k, ex in enumerate((-90, 90)):
        R.fill(oval(ex, -270, 52, 44), WHITE)
        R.stroke(oval(ex, -270, 52, 44), INK, 6)
        R.fill(circle(ex + (6 if k == 0 else -2), -262, 10 if stare > 0.5 else 18), INK)
        R.fill(rrect(ex - 56, -320, 112, 36, 10), CHROME1)      # heavy lids
        R.stroke(poly([(ex - 52, -286), (ex + 52, -284)], False), INK, 6)
        R.stroke(oval(ex, -214, 44, 10), CHROME2, 5, 0.8)       # eye bags
    # scar (it has seen things)
    R.stroke(poly([(110, -350), (70, -300)], False), INK, 5)
    for k in range(3):
        R.stroke(poly([(104 - k * 14, -338 + k * 16), (116 - k * 14, -330 + k * 16)], False), INK, 4)
    op = clamp01(talk)
    R.fill(rrect(-70, -150, 140, 14 + 40 * op, 10), 0xFF2A1A22)
    R.stroke(rrect(-70, -150, 140, 14 + 40 * op, 10), INK, 5)
    # dial
    R.glossy(circle(-150, -90, 30), -150, -90, 30, WHITE, 0xFFE8E8F0, 0xFF9AA3B8, INK, 5)
    R.stroke(poly([(-150, -90), (-132, -108)], False), INK, 5)
    c.restore()
    if sold_k > 0:
        sold(R, x + 20 * s, y - 250 * s, 0.85, 12, k=sold_k)


def kitchen(R, t, sepia=0.0):
    top, bot = (0xFF6B3F8E, 0xFF2B1D4E) if sepia < 0.5 else (0xFF8A6A44, 0xFF3A2A1A)
    R.c.drawRect(skia.Rect(0, 0, W, H), R.paint(shader=R.lin(0, 0, 0, H, [top, bot])))
    # tiles
    for j in range(12):
        for i in range(8):
            R.stroke(rrect(20 + i * 134, 230 + j * 92, 124, 82, 10), WHITE, 3, 0.08)
    # counter
    R.c.drawRect(skia.Rect(0, 1240, W, H), R.paint(shader=R.lin(0, 1240, 0, H, [0xFF2A2140, 0xFF120C22] if sepia < 0.5 else [0xFF4A3622, 0xFF1E140A])))
    R.stroke(poly([(0, 1240), (W, 1240)], False), WHITE, 4, 0.3)


# ------------------------------------------------------------------ werewolf
def wolf(R, x, y, s=1.0, t=0.0, howl=0.0):
    """A werewolf sitting in profile, muzzle up at the moon (on our right), a buffering wheel on its chest.
    (x, y) = paws on the ground."""
    c = R.c
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    fill = R.lin(-200, -650, 150, 0, [0xFF6A5AA0, 0xFF2E2456])
    rim = 0xFFFFE08A
    tail = skia.Path()
    tail.moveTo(-150, -40)
    tail.cubicTo(-260, -20, -330, -90, -300, -180)
    tail.cubicTo(-270, -110, -220, -90, -140, -100)
    tail.close()
    body = skia.Path()
    body.moveTo(-170, 0)
    body.cubicTo(-200, -160, -150, -330, -40, -420)
    body.cubicTo(40, -440, 90, -380, 80, -300)
    body.cubicTo(70, -200, 120, -100, 130, 0)
    body.close()
    head = skia.Path()
    head.addCircle(20, -480, 85)
    snout = poly([(40, -540), (190, -660), (215, -630), (95, -455)])
    ears = [poly([(-50, -520), (-75, -640), (0, -560)]), poly([(0, -555), (5, -665), (60, -570)])]
    for p in [tail, body, head, snout] + ears:
        R.fill(p, shader=fill)
        R.stroke(p, rim, 6)
    for p in [body, head, snout]:   # hide inner seams
        R.fill(p, shader=fill)
    R.fill(oval(60, -505, 14, 10), YELLOW)
    R.fill(circle(63, -505, 4), INK)
    R.fill(circle(205, -645, 12), INK)
    for fx in (-40, 70):
        R.fill(oval(fx, -6, 46, 16), 0xFF2E2456)
        R.stroke(oval(fx, -6, 46, 16), rim, 5)
    if howl > 0.2:   # the howl: three little arcs
        for k in range(3):
            p = skia.Path()
            p.addArc(skia.Rect(170 - 40 * k, -800 - 40 * k, 310 + 40 * k, -660 + 40 * k), -80, 70)
            R.stroke(p, WHITE, 6, 0.6 * howl)
    spinner(R, -20, -300, 46, t)
    c.restore()


# ------------------------------------------------------------------ hug squeeze helper
def squeeze(G, k):
    """Squash Glorp in a hug: k 0..1."""
    G.squash = lerp(1.0, 0.74, k)
    return G
