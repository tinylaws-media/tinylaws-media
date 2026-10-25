"""LAW #002 — Double pain (Brain Laws).  62.07 s at 116 BPM (30 bars), loops.

Stub your toe and it hurts twice: a sharp pain first, then an ache. Two kinds of pain wires: Aδ fibres
have a thin fatty coat (myelin) and conduct ~13 m/s; C fibres are bare and conduct ~0.8 m/s. Felt at the
foot, the sharp pain comes in ~0.4 s and the ache in ~1.9 s (from the hand: ~0.26 s and ~1.26 s, so the
gap is ~1 s at the hand, ~1.5 s at the toe). The C fibres keep firing, so the ache lingers. Rubbing sends
touch up thick, fast Aβ wires; in the spinal cord they recruit inhibitory ("blocker") cells that gate the
pain signals. By then the sharp part is over, so what gets turned down is the ache. The effect is real
but modest, and it lasts while you rub.

Sources: Plaghki, Decruynaere, Van Dooren & Le Bars 2010, PLoS ONE 5:e10269 (Aδ 13.0 m/s, C 0.8 m/s;
psychophysical latencies hand 263/1255 ms, foot 409/1918 ms); Melzack & Wall 1965, Science 150:971;
Mancini et al. 2015, Pain 156:1936 (touch inhibits Aδ and C nociceptive responses at a subcortical level).

Built against an independent review (claim on frame 0, race early, replay to explain, Pip bigger,
honest wording on rubbing, gate across both wires, a question that sends people back to the race).
"""
import math
import numpy as np
import skia
from engine import *

TITLE = "LAW #002"
BPM = 116
BEAT = 60.0 / BPM
BAR = 4 * BEAT
DURATION = 30 * BAR          # 62.07 s, just over one minute
CAP_Y = 410
SERIES = "Brain Laws"
TRANSPOSE = 2
# Dm7 - G7 - Cmaj7 - Am7: a soft lo-fi turnaround (one chord per bar)
CHORDS = [
    ([50, 57, 60, 65], 38), ([47, 53, 55, 62], 43), ([48, 55, 59, 64], 36), ([45, 55, 60, 64], 45),
]
MOTIFS = [
    [(0, 4, 2), (2, 5, 1), (3, 4, 1), (4, 2, 2), (6, 3, 2)],
    [(0, 6, 1), (1, 5, 1), (2, 4, 2), (4, 5, 1), (5, 6, 3)],
    [(0, 3, 1), (1, 4, 1), (2, 5, 1), (3, 7, 3), (6, 6, 2)],
    [(0, 5, 2), (2, 4, 1), (3, 2, 1), (4, 1, 4)],
]


def C(a, b, segs, **kw):
    kw.setdefault("y", CAP_Y)
    kw.setdefault("size", 80)
    kw.setdefault("emph_size", 104)
    kw.setdefault("word_gap", 0.0)
    return Caption(a, b, segs, **kw)


# ------------------------------------------------------------------ key times (laid out on the measured voice)
T_OW1, T_OW2 = 1.75, 2.75           # cold open: the sharp pain, then the ache
T_STAMP = 4.65
T_DIAG = 5.6                        # the diagram appears
RACE_T0 = 8.22                      # "Bonk!" in the race
FAST_ARR = RACE_T0 + 0.4            # felt at the foot: ~0.4 s
SLOW_ARR = RACE_T0 + 1.9            # felt at the foot: ~1.9 s
T_REPLAY = 14.7
T_GATESCENE = 35.8
T_BLOCKERS = 41.2
T_GATE = 42.6
T_DOWN = 47.5
T_CARD = 51.1
T_OUTRO = 54.0

CAPTIONS = [
    C(0.0, T_OW1, [(-0.5, "Stubbed toes /"), (-0.5, "hurt *twice.*")]),
    C(T_OW1, T_OW2, [(T_OW1, "*OW!*")], emph_size=150),
    C(T_OW2, 4.35, [(T_OW2, "...ow... *OWWW!*")], emph_size=124),
    C(T_DIAG, 7.47, [(T_DIAG, "*2 wires.* /"), (6.4, "Let's race them!")]),
    C(7.47, 8.17, [(7.47, "*Ready?*")]),
    C(8.17, 8.87, [(8.17, "*BONK!*")]),
    C(8.87, 10.17, [(8.87, "*OW!*")]),
    C(10.17, 10.95, [(10.17, "*OWWW!*")]),
    C(10.95, 13.02, [(10.95, "Sharp pain: /"), (11.7, "*under half a second.*")]),
    C(13.02, T_REPLAY, [(13.02, "The ache: /"), (13.6, "*almost 2!*")]),
    C(T_REPLAY, 16.85, [(T_REPLAY, "Why so slow? /"), (15.6, "Let's *replay it.*")]),
    C(16.85, 18.71, [(16.85, "One wire has /"), (17.4, "a *fatty coat...*")]),
    C(18.71, 20.51, [(18.71, "The fat makes /"), (19.4, "the signal *jump.*")]),
    C(20.51, 22.34, [(20.51, "About *13 meters* /"), (21.3, "a second.")]),
    C(22.34, 24.19, [(22.34, "Usain Bolt's /"), (22.9, "*top speed!*")]),
    C(24.19, 25.61, [(24.19, "The other wire /"), (24.8, "is *bare.*")]),
    C(25.61, 27.23, [(25.61, "*Under 1 meter* /"), (26.3, "a second.")]),
    C(27.23, 28.65, [(27.23, "Slower than a *stroll!*")]),
    C(28.65, 31.15, [(28.65, "It keeps firing, /"), (29.7, "so the *ache lingers.*")]),
    C(31.15, 33.73, [(31.15, "From your hand: /"), (32.3, "*a 1-second gap.*")]),
    C(33.73, T_GATESCENE, [(33.73, "From your toe? /"), (34.4, "*1.5 seconds!*")]),
    C(T_GATESCENE, 37.18, [(T_GATESCENE, "So why do we /"), (36.4, "*rub it?*")]),
    C(37.18, 39.36, [(37.18, "Rubbing sends *touch* /"), (38.1, "up thick wires.")]),
    C(39.36, 42.21, [(39.36, "In your spinal cord, /"), (40.6, "they switch on *blockers...*")]),
    C(42.21, 43.57, [(42.21, "...that close a *gate.*")]),
    C(43.57, 45.67, [(43.57, "By then, the /"), (44.4, "*sharp part* is over...")]),
    C(45.67, 48.37, [(45.67, "...so the gate turns /"), (47.1, "down *the ache.*")]),
    C(48.37, 49.75, [(48.37, "Rubbing *really helps!*")]),
    C(49.75, T_CARD, [(49.75, "A bit. /"), (50.3, "*While you rub.*")]),
    C(T_OUTRO, 55.99, [(54.12, "Be honest: /"), (54.8, "do you feel *the gap?*")]),
    C(55.99, 57.94, [(55.99, "Or is it /"), (56.7, "*one long OW?*")]),
    C(57.94, 59.13, [(57.94, "Tell me *below!*")]),
    C(59.13, 60.85, [(59.13, "Anyway... /"), (59.9, "where was I *going?*")]),
    C(60.85, DURATION, [(60.85, "And *that's why...*")], plate=True),
]

# ------------------------------------------------------------------ narration (voice 07, varied per line)
VOICE = "af_heart"
VOICE_SPEED = 1.0
VOICE_FX = {"semitones": 3}
NARRATION = [
    (0.10, "Stubbed toes hurt twice."),
    (T_OW1, "OW!", {"semitones": 5}),
    (T_OW2, "Ow... ow... OWWW!"),
    (4.35, "That's double pain!", {"semitones": 4}),
    (5.61, "Two wires. Let's race them!", {"semitones": 4}),
    (7.47, "Ready?", {"semitones": 4}),
    (8.17, "Bonk!", {"semitones": 4}),
    (8.87, "Ow!", {"semitones": 5}),
    (10.17, "Owww!", {"semitones": 2}),
    (10.95, "Sharp pain: under half a second."),
    (13.02, "The ache: almost two!"),
    (14.71, "Why so slow? Let's replay it.", {"semitones": 4}),
    (16.85, "One wire has a fatty coat..."),
    (18.71, "The fat makes the signal jump."),
    (20.51, "About thirteen meters a second."),
    (22.34, "Usain Bolt's top speed!", {"semitones": 4}),
    (24.19, "The other wire is bare."),
    (25.61, "Under one meter a second."),
    (27.23, "Slower than a stroll!", {"semitones": 2}),
    (28.65, "And it keeps firing, so the ache lingers."),
    (31.15, "From your hand, the gap is about one second."),
    (33.73, "From your toe? One and a half!", {"semitones": 4}),
    (35.81, "So why do we rub it?", {"semitones": 4}),
    (37.18, "Rubbing sends touch up thick wires."),
    (39.36, "In your spinal cord, they switch on blocker cells..."),
    (42.21, "that close a gate."),
    (43.57, "By then, the sharp part is over..."),
    (45.67, "so the gate turns down what's left: the ache."),
    (48.37, "Rubbing really helps!", {"semitones": 4}),
    (49.75, "A bit. While you rub.", {"semitones": 2}),
    (51.27, "Sharp first. Ache second. Rub it down."),
    (54.12, "Be honest: do you feel the gap?", {"semitones": 4}),
    (55.99, "Or is it one long OW?"),
    (57.94, "Tell me below!"),
    (59.13, "Anyway... where was I going?"),
    (60.85, "And that's why..."),
]

import os as _os
_ENV_PATH = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "out", f"{__name__}_voice_env.npy")
VOICE_ENV = np.load(_ENV_PATH) if _os.path.exists(_ENV_PATH) else None
SEG_TIMES = sorted({max(0.0, ta) for cap in CAPTIONS for (ta, s, e) in cap.words if s != "/"})
WORD_TIMES = SEG_TIMES


def talking(t):
    if VOICE_ENV is not None:
        i = int(t * 24)
        return 1.0 if 0 <= i < len(VOICE_ENV) and VOICE_ENV[i] > 0.12 else 0.0
    for ts in SEG_TIMES:
        if 0 <= t - ts < 0.6:
            return 1.0 if math.sin((t - ts) * 30) > 0 else 0.0
    return 0.0


# ------------------------------------------------------------------ scoreboard
HUD_ON = (11.9, T_CARD)
HUD = {
    "SHARP": ("teal", [(12.05, "0.4 s")]),
    "ACHE": ("pink", [(13.8, "1.9 s"), (T_DOWN, "less!")]),
    "GAP": ("navy", [(34.6, "1.5 s")]),
}

# ------------------------------------------------------------------ sound
CAPSULE_T = [17.3 + i * 0.16 for i in range(5)]
JUMP_T = [19.0 + i * 0.3 for i in range(5)]
SFX = [
    (0.02, "thud", 0), (0.05, "tap", 0), (T_OW1, "whip", 0), (T_OW2, "rumble", 0), (T_STAMP, "slam", 0),
    (5.75, "pop", 0), (6.0, "pop", 3),
    (RACE_T0 + 0.02, "thud", 1), (FAST_ARR, "whip", 1), (SLOW_ARR, "rumble", 1), (12.05, "ding", 0), (13.8, "ding", 1),
    (T_REPLAY + 0.2, "shrink", 0),
] + [(t, "tick", i) for i, t in enumerate(CAPSULE_T)] + [(t, "tick", i + 2) for i, t in enumerate(JUMP_T)] + [
    (20.9, "pop", 1), (25.9, "pop", 2), (34.5, "ding", 2),
    (36.3, "scribble", 0), (37.6, "scribble", 1), (38.4, "sparkle", 0), (T_BLOCKERS, "pop", 3), (T_GATE, "tap", 1),
    (T_DOWN, "shrink", 1), (48.4, "sparkle", 1), (T_CARD, "paper", 0), (53.6, "stamp", 1), (57.94, "pop", 3),
]
SHAKES = [(0.02, 6), (T_STAMP, 5), (RACE_T0, 4)]
MUSIC_CUTS = [(0.0, 2 * BAR), (7.4, 5 * BAR)]   # silence for the stub and for the race, back on downbeats

SUBTITLE_EXTRAS = [
    (4.35, T_DIAG, "That's double pain!"),
    (T_CARD, T_OUTRO, "Sharp first, ache second. Rubbing turns the ache down."),
]


def music_sections(t):
    s = {"drums": 1, "bass": 1, "keys": 1, "lead": 1}
    if t < T_DIAG:
        s.update(lead=0)
    elif t < T_REPLAY:
        s.update(var=2)
    elif t < T_GATESCENE:
        s.update(var=1)
    elif T_CARD <= t < T_OUTRO:
        s.update(glock=1, var=3)
    elif t >= T_OUTRO:
        s.update(lead=0)
    return s


# ------------------------------------------------------------------ helpers
GROUND = 1330.0


def shake_offset(t):
    dx = dy = 0.0
    for t0, k in SHAKES:
        if 0 <= t - t0 < 0.5:
            a = k * math.exp(-(t - t0) * 10)
            ph = (t - t0) * 60
            dx += math.sin(ph * 1.7) * a
            dy += math.cos(ph * 1.3) * a
    return dx, dy


def pop_scale(t, t0, dur=0.35, frm=0.4):
    return lerp(frm, 1.0, ease_out_back(prog(t, t0, t0 + dur), 1.6))


def label(R, s, x, y, size=84, ink="navy", shadow="pink", t=None, t0=None, font="bagel", rot=0.0, alpha=1.0):
    sc = 1.0
    if t is not None and t0 is not None:
        if t < t0:
            return
        sc = pop_scale(t, t0)
    R.text(s, x, y, R.A.font(font, size), ink, shadow=(shadow, 5, 5) if shadow else None, scale=sc, rot=rot, alpha=alpha)


def hand(R, s, x, y, size=58, ink="navy", t=None, t0=None, align="center", rot=-3.0, alpha=1.0):
    if t is not None and t0 is not None and t < t0:
        return
    k = 1.0 if t is None else pop_scale(t, t0, 0.3, 0.5)
    R.text(s, x, y, R.A.font("hand", size), ink, align=align, rot=rot, scale=k, alpha=alpha)


def draw_ground(R, x0=40, x1=1040, y=GROUND, w=7):
    R.stroke(wline(x0, y + 2, x1, y - 2, R.s("ground", x0), 2.0), "navy", w)


def draw_star(R, x, y, r, rot, seed, ink="yellow"):
    sp = star_path(x, y, r, r * 0.45, rot=rot, seed=R.s("star", seed))
    R.fill(sp, ink)
    R.stroke(sp, "navy", 5)


def header(R):
    f = R.A.font("mono", 30)
    w = f.measureText(TITLE)
    b = wrect(56, 236, w + 40, 58, R.s("hdr"), amp=1.2, r=8)
    R.fill(b, SERIES_INK[SERIES])
    R.stroke(b, "navy", 5)
    R.text(TITLE, 76 + w / 2, 276, f, "navy")


def dots_bg(R, ink="blue", alpha=0.12):
    p = R._ink_paint(ink, alpha, texture=False)
    for gy in range(0, H + 60, 60):
        for gx in range(0, W + 60, 60):
            R.c.drawCircle(gx + 30, gy + 20, 2.4, p)


def pip_blink(t):
    return ((t + 1.7) % 3.3) < 0.09          # never on the first or last frame


def hud_value(vals, t):
    cur, t_set = None, None
    for (t0, v) in vals:
        if t >= t0:
            cur, t_set = v, t0
    return cur, t_set


def draw_hud(R, t):
    if not (HUD_ON[0] <= t < HUD_ON[1]):
        return
    k_in = pop_scale(t, HUD_ON[0], 0.4, 0.6)
    out = 1 - ease_in(prog(t, HUD_ON[1] - 0.3, HUD_ON[1]))
    for i, (name, (ink, vals)) in enumerate(HUD.items()):
        cx = 205 + i * 290
        y0, w, h = 236, 270, 120
        c = R.c
        c.save()
        c.translate(cx, y0 + h / 2)
        c.scale(k_in * out, k_in * out)
        c.translate(-cx, -(y0 + h / 2))
        v, t_set = hud_value(vals, t)
        card = wrect(cx - w / 2, y0, w, h, R.s("hud", i), amp=1.2, r=14)
        R.knockout(card)
        if t_set is not None and t - t_set < 1.5:
            R.fill(card, "yellow", alpha=0.55 * (1 - prog(t, t_set + 0.8, t_set + 1.5)))
        R.stroke(card, "navy", 5)
        R.text(name, cx, y0 + 36, R.A.font("mono", 30), "navy")
        if v is None:
            R.text("?", cx, y0 + 102, R.A.font("bagel", 58), "navy", alpha=0.35)
        else:
            f = R.A.font("bagel", 62)
            wv = f.measureText(v)
            if wv > w - 36:
                f = R.A.font("bagel", 62 * (w - 36) / wv)
            R.text(v, cx, y0 + 104, f, ink, shadow=("navy", 4, 4) if ink != "navy" else ("yellow", 4, 4),
                   scale=pop_scale(t, t_set, 0.35, 0.5))
        c.restore()


# ------------------------------------------------------------------ props
BLOCK_X, BLOCK_W, BLOCK_H = 640, 120, 100
PIP_S = 1.7
STUB_X = BLOCK_X - (44 + 13) * PIP_S + 4     # Pip's centre when his right foot meets the block


def toy_block(R, x=BLOCK_X, w=BLOCK_W, h=BLOCK_H):
    """A wooden toy block with a letter: the thing Pip stubs his toe on."""
    y = GROUND - h
    d = w * 0.26
    top = wpoly([(x, y), (x + d, y - d), (x + w + d, y - d), (x + w, y)], R.s("tbt"), 0.6)
    side = wpoly([(x + w, y), (x + w + d, y - d), (x + w + d, y + h - d), (x + w, y + h)], R.s("tbs"), 0.6)
    front = wrect(x, y, w, h, R.s("tbf"), amp=1.0, r=6)
    for p, ink in ((side, "teal"), (top, "yellow"), (front, "yellow")):
        R.knockout(p)
        R.fill(p, ink)
        R.stroke(p, "navy", 6)
    R.halftone(side, "navy", scale=0.5, alpha=0.25)
    R.stroke(wrect(x + 12, y + 12, w - 24, h - 24, R.s("tbi"), amp=0.8, r=6), "navy", 3)
    R.text("A", x + w / 2, y + h * 0.72, R.A.font("bagel", 64), "pink", shadow=("navy", 3, 3))


def bolt(R, x, y, s, ink="yellow", rot=0.0):
    """Lightning bolt = the sharp first pain (and Usain 'Lightning' Bolt)."""
    pts = [(-0.2, -1.0), (0.45, -1.0), (0.1, -0.25), (0.5, -0.25), (-0.35, 1.0), (-0.05, 0.1), (-0.45, 0.1)]
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    P = [(x + s * (px * ca - py * sa), y + s * (px * sa + py * ca)) for px, py in pts]
    p = wpoly(P, R.s("bolt", int(x), int(y)), 0.8)
    R.fill(p, ink)
    R.stroke(p, "navy", 6)


def ache_rings(R, x, y, t, t0, strength=1.0, ink="red"):
    """Throbbing rings = the dull ache that comes second."""
    u = t - t0
    if u < 0:
        return
    for k in range(3):
        ph = (u * 1.6 + k / 3.0) % 1.0
        r = 50 + 150 * ph
        a = min(1.0, (1 - ph) * 1.1) * strength
        if a > 0.02:
            R.stroke(blob(x, y, r, r * 0.8, R.s("ring", k), amp=0.05), ink, 14 * (1 - ph) + 4, alpha=a)


def walk_lift(t, speed=7.0, h=16.0):
    ph = math.sin(t * speed)
    return (max(0.0, ph) * h, max(0.0, -ph) * h)


# --- the one picture: toe at the bottom, spinal cord, brain at the top, wires in between
BRAIN = (600, 742, 230, 104)
FOOT = (600, 1368)
Y_TOP, Y_BOT = 846, 1236
LANE = {"fast": 470, "slow": 630, "touch": 790}
SPINE_Y = 1078
PIP_X, PIP_G, PIP_SIDE = 170, 1330, 0.95      # Pip watches from the left, big enough to read his face


def brain_icon(R, t, flash_t=None, ache_t=None, ache_k=1.0):
    cx, cy, rx, ry = BRAIN
    b = blob(cx, cy, rx, ry, R.s("brain"), amp=0.03)
    R.knockout(b)
    R.fill(b, "pink", 0.9)
    R.c.save()
    R.c.clipPath(b, doAntiAlias=True)
    R.halftone(blob(cx + rx * 0.5, cy + ry * 0.5, rx * 0.8, ry * 0.7, R.s("bsh")), "blue", 0.6, alpha=0.45)
    R.c.restore()
    if flash_t is not None and 0 <= t - flash_t < 0.9:
        R.fill(b, "yellow", alpha=0.9 * (1 - prog(t, flash_t + 0.3, flash_t + 0.9)))
    R.stroke(b, "navy", 7)
    R.stroke(wline(cx, cy - ry + 10, cx + 6, cy + ry - 12, R.s("bmid"), 1.2), "navy", 4)
    for i, (x0, y0) in enumerate(((-150, -30), (-90, 30), (60, -40), (120, 25), (-30, -60), (30, 55))):
        pts = [(cx + x0 + k * 18, cy + y0 + (8 if k % 2 else -8)) for k in range(4)]
        R.stroke(wpoly(pts, R.s("sulc", i), 1.0, closed=False), "navy", 4)
    if ache_t is not None:
        ache_rings(R, cx, cy, t, ache_t, strength=ache_k)


def foot_icon(R, t, glow=0.0):
    cx, cy = FOOT
    sole = union(blob(cx + 4, cy - 14, 140, 70, R.s("sole"), amp=0.03), blob(cx - 26, cy + 48, 86, 50, R.s("heel"), amp=0.03))
    toes = [blob(cx - 92, cy - 82, 34, 30, R.s("toe", 0)), blob(cx - 34, cy - 92, 24, 22, R.s("toe", 1)),
            blob(cx + 14, cy - 90, 22, 20, R.s("toe", 2)), blob(cx + 58, cy - 82, 20, 18, R.s("toe", 3)),
            blob(cx + 94, cy - 66, 17, 15, R.s("toe", 4))]
    shape = union(sole, *toes)
    R.knockout(shape)
    R.fill(shape, "pink", 0.9)
    if glow > 0:
        R.fill(toes[0], "red", alpha=0.8 * glow)
    R.stroke(shape, "navy", 7)


def lane_path(x):
    """A wire from the big toe up to the brain."""
    bx, by = FOOT[0] - 92, FOOT[1] - 100
    return [(bx + (x - bx) * 0.15, by), (x, Y_BOT - 60), (x, Y_TOP)]


def lane_point(x, frac):
    """Point on a lane, frac 0 = toe, 1 = brain."""
    pts = lane_path(x)
    if frac < 0.15:
        u = frac / 0.15
        return (lerp(pts[0][0], pts[1][0], u), lerp(pts[0][1], pts[1][1], u))
    u = (frac - 0.15) / 0.85
    return (pts[1][0], lerp(pts[1][1], pts[2][1], u))


def capsules(x, n=5, gap=16):
    y0, y1 = Y_TOP + 6, Y_BOT - 66
    L = (y1 - y0 - gap * (n - 1)) / n
    return [(y1 - (i + 1) * L - i * gap, y1 - i * L - i * gap) for i in range(n)]   # bottom to top


def draw_wire(R, t, kind, t_draw, ink="navy", thick=6, myelin=None, pulse_t=None):
    if t < t_draw:
        return
    u = ease_out(prog(t, t_draw, t_draw + 0.6))
    x = LANE[kind]
    pts = lane_path(x)
    full = [pts[0], pts[1], (x, lerp(pts[1][1], pts[2][1], u))]
    R.stroke(wpoly(full, R.s("wire", kind), 0.6, closed=False), ink, thick)
    if myelin:
        for i, (ya, yb) in enumerate(capsules(x)):
            ti = t_draw + 0.2 + i * 0.08
            if t >= ti:
                k = pop_scale(t, ti, 0.3, 0.3)
                if pulse_t is not None and 0 <= t - (pulse_t + i * 0.16) < 0.5:
                    k *= 1 + 0.25 * math.sin(prog(t, pulse_t + i * 0.16, pulse_t + i * 0.16 + 0.5) * math.pi)
                wcap = myelin[1]
                cap = wrect(x - wcap / 2 * k, ya, wcap * k, yb - ya, R.s("cap", kind, i), amp=1.0, r=wcap / 2)
                R.knockout(cap)
                R.fill(cap, myelin[0])
                R.stroke(cap, "navy", 5)


def spark(R, x, y, r=28, trail_from=None, ink="yellow"):
    if trail_from is not None:
        R.stroke(wline(trail_from[0], trail_from[1], x, y, R.s("trail", int(y)), 0.4), ink, 14, alpha=0.7)
    draw_star(R, x, y, r, 0, int(y) % 7, ink)


def walker(R, x, y, t, scale=1.0):
    """The ache: a small grumpy red blob that walks up the bare wire."""
    s = scale
    ph = math.sin(t * 9.0)
    for sx, lift in ((-1, max(0, ph)), (1, max(0, -ph))):
        R.stroke(wline(x + sx * 12 * s, y + 18 * s, x + sx * 16 * s, y + (36 - 10 * lift) * s, R.s("wl", sx), 0.3), "navy", 5 * s + 1)
    b = blob(x, y, 32 * s, 28 * s, R.s("walker"), amp=0.05)
    R.knockout(b)
    R.fill(b, "red", 0.85)
    R.stroke(b, "navy", 5)
    if s > 0.45:
        for sx in (-1, 1):
            R.fill(blob(x + sx * 10 * s, y - 2 * s, 4 * s, 5 * s, 3), "navy", texture=False, misreg=False)
            R.stroke(wline(x + sx * 4 * s, y - 14 * s, x + sx * 18 * s, y - 10 * s, R.s("wb", sx), 0.3), "navy", 3)


# the ache keeps firing: walkers set off from the toe one after another and climb slowly
WALK_SPAWN = [24.2 + i * 1.8 for i in range(16)]
WALK_V = 0.11                                  # fraction of the wire per second (slow-motion feel)


def walkers(R, t, shrink_from=None):
    xs = LANE["slow"]
    for i, t0 in enumerate(WALK_SPAWN):
        if t < t0:
            break
        f = 0.02 + (t - t0) * WALK_V
        if f > 0.98:
            continue
        p = lane_point(xs, f)
        small = shrink_from is not None and t >= shrink_from and p[1] < SPINE_Y
        walker(R, p[0], p[1], t + i, scale=0.42 if small else 0.8)


def stopwatch(R, t, x=780, y=1000):
    v = max(0.0, min(t - RACE_T0, SLOW_ARR - RACE_T0))
    box = wrect(x - 118, y - 60, 236, 104, R.s("sw"), amp=1.2, r=18)
    R.knockout(box)
    R.fill(box, "yellow", 0.9)
    R.stroke(box, "navy", 6)
    R.text(f"{v:.2f} s", x, y + 20, R.A.font("mono", 54), "navy")


def side_pip(R, t, expr="normal", look=(1, -0.6), sweat=0.0, lift=(0, 0), arms="down", hop=0.0):
    P = PipState(x=PIP_X, ground=PIP_G - hop, scale=PIP_SIDE, blink=pip_blink(t), talk=talking(t), look=look, expr=expr)
    P.sweat, P.lift, P.arms = sweat, lift, arms
    draw_pip(R, P)


def stub_pip(R, t, x, expr="shock", hop=0.0, lift=(0.0, 6.0), arms="down", sweat=0.0, tilt=0.0, tremble=0.0):
    P = PipState(x=x, ground=GROUND - hop, scale=PIP_S, blink=pip_blink(t), talk=talking(t))
    P.expr, P.lift, P.arms, P.sweat, P.tilt, P.tremble = expr, lift, arms, sweat, tilt, tremble
    draw_pip(R, P)


def diagram(R, t, touch=False, glow_t=None):
    """The one picture. Everything that exists at time t."""
    # spinal cord band: the relay between the wires and the brain (and later the gate)
    if t >= T_DIAG + 0.3:
        k = ease_out(prog(t, T_DIAG + 0.3, T_DIAG + 0.8))
        band = wrect(380, SPINE_Y - 26, 460 * k, 52, R.s("spine"), amp=1.0, r=24)
        R.knockout(band)
        R.fill(band, "yellow", 0.6 if not touch or t < 39.6 else 0.9)
        R.stroke(band, "navy", 5)
    if t >= T_DIAG + 0.1:
        k = pop_scale(t, T_DIAG + 0.1, 0.4, 0.5)
        R.c.save()
        R.c.translate(FOOT[0], FOOT[1])
        R.c.scale(k, k)
        R.c.translate(-FOOT[0], -FOOT[1])
        glow = 1 - prog(t, glow_t + 0.1, glow_t + 1.0) if glow_t is not None and t >= glow_t else 0.0
        foot_icon(R, t, glow=glow)
        R.c.restore()
        if t < 8.0:
            hand(R, "toe", FOOT[0] + 220, FOOT[1] - 40, 58, t=t, t0=T_DIAG + 0.1, rot=-4)
    draw_wire(R, t, "fast", T_DIAG + 0.6, myelin=("yellow", 40), pulse_t=CAPSULE_T[0])
    draw_wire(R, t, "slow", T_DIAG + 0.8, thick=5)
    if touch:
        draw_wire(R, t, "touch", 37.6, ink="navy", thick=7, myelin=("blue", 54))
    if t >= T_DIAG + 0.3:
        k = pop_scale(t, T_DIAG + 0.3, 0.4, 0.5)
        R.c.save()
        R.c.translate(BRAIN[0], BRAIN[1])
        R.c.scale(k, k)
        R.c.translate(-BRAIN[0], -BRAIN[1])
        if t < T_REPLAY:
            flash, ache, ak = (FAST_ARR if t >= FAST_ARR else None), (SLOW_ARR if t >= SLOW_ARR else None), 1.0
        else:
            first = WALK_SPAWN[0] + 0.96 / WALK_V
            flash = None
            ache = first if t >= first else None
            ak = 1.0 if not touch else lerp(1.0, 0.25, prog(t, T_DOWN, T_DOWN + 1.0))
        brain_icon(R, t, flash_t=flash, ache_t=ache, ache_k=ak)
        R.c.restore()
        if t < 8.0:
            hand(R, "brain", BRAIN[0] + 160, BRAIN[1] - 128, 58, "navy", t=t, t0=T_DIAG + 0.3, rot=4)
        if T_DIAG + 0.3 <= t < 8.0:
            hand(R, "spinal cord", 640, SPINE_Y + 82, 50, "navy", t=t, t0=T_DIAG + 0.5, rot=-3)
    if 16.85 <= t < 28.6:
        hand(R, "myelin", (LANE["fast"] + LANE["slow"]) / 2, 960, 52, "navy", t=t, t0=17.1, rot=-6)


def scene_cold(R, t):             # 0 - 5.6: the claim on frame 0, the sharp pain, the pause, the ache, the stamp
    draw_ground(R)
    toy_block(R)
    foot = (BLOCK_X - 4, GROUND - 34)
    if t < T_OW2:
        if t < T_OW1:
            stub_pip(R, t, STUB_X, expr="worried", lift=(0.0, 6.0), tilt=1.5, sweat=0.4, tremble=1.5)
        else:
            stub_pip(R, t, STUB_X, expr="shock" if t < T_OW1 + 0.45 else "deadpan", lift=(0.0, 6.0), sweat=0.4)
    else:                          # the ache arrives: hop on one foot
        u = t - T_OW2
        hop = abs(math.sin(u * 6.0)) * 26
        stub_pip(R, t, STUB_X - 40, expr="worried", hop=hop, lift=(0.0, 34.0), arms="up", sweat=0.4 + prog(t, T_OW2, T_OW2 + 0.8) * 0.6)
        ache_rings(R, foot[0] - 40, foot[1] - hop, t, T_OW2)
    if t < T_OW1:
        for k in range(4):
            ang = k * 1.6 + t * 2
            draw_star(R, foot[0] + math.cos(ang) * 46, foot[1] - 30 + math.sin(ang) * 22, 18, 0, k)
        label(R, "BONK!", 700, 1450, 110, "yellow", "navy", t=t, t0=-0.4, rot=-6)
    if t >= T_OW1:                 # 1 = sharp pain (bolt), 2 = ache (rings)
        k = pop_scale(t, T_OW1, 0.3, 0.3)
        bolt(R, 210, 900, 80 * k)
        hand(R, "1", 290, 990, 80, "navy", t=t, t0=T_OW1, rot=-4)
    if T_OW1 + 0.5 <= t < T_OW2:
        hand(R, "...", 810, 880, 84, "navy", t=t, t0=T_OW1 + 0.5, rot=0)
    if t >= T_OW2:
        hand(R, "2", 830, 1150, 80, "red", t=t, t0=T_OW2, rot=4)
    if t >= T_STAMP:              # the law's name lands as a stamp over the action
        k = lerp(1.7, 1.0, ease_out_back(prog(t, T_STAMP, T_STAMP + 0.3), 1.2))
        c = R.c
        c.save()
        c.translate(W / 2, 560)
        c.rotate(-6)
        c.scale(k, k)
        st = wrect(-390, -140, 780, 280, R.s("lawst"), 2.0, r=22)
        R.knockout(st)
        R.stroke(st, "teal", 12)
        R.stroke(wrect(-365, -115, 730, 230, R.s("lawst2"), 1.6, r=16), "teal", 4)
        R.text("TINY LAWS · LAW #002", 0, -62, R.A.font("mono", 34), "navy")
        R.text("DOUBLE PAIN", 0, 62, R.A.font("bagel", 104), "navy", shadow=("pink", 6, 6))
        c.restore()


def scene_race(R, t):             # 5.6 - 14.7: the race, in real time
    R.flood("teal", 0.14)
    dots_bg(R, "navy", 0.06)
    diagram(R, t, glow_t=RACE_T0)
    xf, xs = LANE["fast"], LANE["slow"]
    if 7.47 <= t < 12.0:
        stopwatch(R, t)
    if t >= RACE_T0 - 0.8:
        if t < RACE_T0:
            spark(R, *lane_point(xf, 0.0), r=24)
            walker(R, *lane_point(xs, 0.02), t)
        else:
            uf = prog(t, RACE_T0, FAST_ARR)
            if t < FAST_ARR + 0.3:
                p = lane_point(xf, uf)
                spark(R, p[0], p[1], 30, trail_from=lane_point(xf, max(0, uf - 0.4)))
            us = prog(t, RACE_T0, SLOW_ARR)
            if t < SLOW_ARR + 0.4:
                walker(R, *lane_point(xs, 0.02 + 0.96 * us), t)
    if t >= FAST_ARR:
        hand(R, "0.4 s", xf - 96, Y_TOP + 74, 58, "teal", t=t, t0=FAST_ARR, rot=-6)
    if t >= SLOW_ARR:
        hand(R, "1.9 s", xs + 130, Y_TOP + 74, 58, "red", t=t, t0=SLOW_ARR, rot=6)
    # Pip feels each arrival
    if t < RACE_T0:
        side_pip(R, t, expr="normal" if t >= 7.47 else "happy", look=(1, -0.6))
    elif t < FAST_ARR:
        side_pip(R, t, expr="normal", look=(1, -1))
    elif t < SLOW_ARR:
        side_pip(R, t, expr="shock" if t < FAST_ARR + 0.6 else "deadpan", look=(1, -1), sweat=0.3)
    else:
        u = t - SLOW_ARR
        hop = abs(math.sin(u * 6.0)) * 18 if u < 2.0 else 0.0
        side_pip(R, t, expr="worried", look=(1, -1), sweat=min(1.0, 0.3 + u), lift=(0, 26), arms="up" if u < 2.0 else "down", hop=hop)


def scene_replay(R, t):           # 14.7 - 35.8: slow-motion replay explains the two wires
    R.flood("teal", 0.14)
    dots_bg(R, "navy", 0.06)
    diagram(R, t)
    xf, xs = LANE["fast"], LANE["slow"]
    if t < 33.0:                   # slow-motion tag
        f = R.A.font("mono", 30)
        tag = wrect(660, 870, 230, 56, R.s("smt"), amp=1.2, r=8)
        R.fill(tag, "pink", 0.9)
        R.stroke(tag, "navy", 5)
        R.text("SLOW-MO", 775, 908, f, "navy")
    # the fast spark: waits at the toe, then jumps from gap to gap
    caps = capsules(xf)
    nodes = [Y_BOT - 60] + [(caps[i][0] + caps[i + 1][1]) / 2 for i in range(len(caps) - 1)] + [Y_TOP]
    if t < JUMP_T[0]:
        spark(R, *lane_point(xf, 0.0), r=30)
    elif t < 24.2:
        i = 0
        while i + 1 < len(JUMP_T) and t >= JUMP_T[i + 1]:
            i += 1
        i = min(i, len(nodes) - 2)
        u = ease_in_out(prog(t, JUMP_T[i], JUMP_T[i] + 0.18))
        y = lerp(nodes[i], nodes[i + 1], u)
        spark(R, xf - math.sin(u * math.pi) * 40, y, 34)
    if 24.19 <= t < 25.4:             # the bare wire gets a highlight when Pip names it
        R.stroke(wpoly(lane_path(xs), R.s("hl"), 0.6, closed=False), "pink", 16, alpha=0.6 * (1 - prog(t, 25.0, 25.4)))
    walkers(R, t)
    # speeds, with a lightning bolt for Usain "Lightning" Bolt
    if 20.9 <= t < 28.6:
        label(R, "13 m/s", xf - 150, 900, 60, "navy", "yellow", t=t, t0=20.9, rot=-4)
    if 22.9 <= t < 28.6:
        k = pop_scale(t, 22.9, 0.3, 0.3)
        bolt(R, xf - 150, 800, 46 * k)
    if 25.9 <= t < 31.0:
        label(R, "0.8 m/s", xs + 150, 1000, 58, "red", "navy", t=t, t0=25.9, rot=4)
    # Pip: walks in place for "a stroll", then compares his hand and his toe
    if 27.23 <= t < 28.65:
        side_pip(R, t, expr="happy", look=(1, 0), lift=walk_lift(t, 8.0, 14.0))
    elif 31.15 <= t < 33.73:
        side_pip(R, t, expr="normal", look=(1, -0.6), arms="up")
    elif 33.73 <= t < T_GATESCENE:
        side_pip(R, t, expr="shock", look=(1, 1), lift=(0, 26))
    else:
        side_pip(R, t, expr="normal", look=(1, -0.6))
    if 31.15 <= t < 33.73:
        hand(R, "hand: 1 s gap", PIP_X + 10, 900, 50, "navy", t=t, t0=31.5, rot=-4)
    if 33.73 <= t < T_GATESCENE:
        hand(R, "toe: 1.5 s gap", PIP_X + 20, 900, 50, "red", t=t, t0=34.4, rot=-4)


def mitten(R, x, y):
    m = union(blob(x, y, 62, 44, R.s("mit"), amp=0.04), blob(x - 52, y - 30, 20, 16, R.s("thumb")))
    R.knockout(m)
    R.fill(m, "pink")
    R.halftone(blob(x + 20, y + 14, 46, 30, R.s("mitsh")), "blue", 0.6, alpha=0.4)
    R.stroke(m, "navy", 6)
    R.stroke(wline(x + 70, y - 6, x + 150, y + 30, R.s("arm"), 0.8), "navy", 8)


def scene_gate(R, t):             # 35.8 - 51.1: rubbing switches on blockers that close a gate
    R.flood("teal", 0.14)
    dots_bg(R, "navy", 0.06)
    diagram(R, t, touch=True)
    xf, xs, xt = LANE["fast"], LANE["slow"], LANE["touch"]
    if 37.6 <= t < 39.4:
        hand(R, "touch", xt, 900, 54, "blue", t=t, t0=37.8, rot=6)
    if t >= 36.2:                  # the rub
        mx = FOOT[0] - 60 + 36 * math.sin((t - 36.2) * 2 * math.pi * 1.6)
        mitten(R, mx, FOOT[1] - 6)
    if t >= 38.4:                  # touch signals zip up the thick wire
        for k in range(6):
            ph = ((t - 38.4) * 2.2 + k / 6.0) % 1.0
            p = lane_point(xt, ph)
            draw_star(R, p[0], p[1], 15, 0, k, "blue")
    # blocker cells in the spinal cord, wired from the touch line
    if t >= T_BLOCKERS:
        R.stroke(wline(xt - 20, SPINE_Y, xf + 40, SPINE_Y, R.s("inh"), 0.6), "blue", 7, alpha=prog(t, T_BLOCKERS, T_BLOCKERS + 0.3))
        for j, cx in enumerate((xf + 44, xs + 44)):
            k = pop_scale(t, T_BLOCKERS + j * 0.15, 0.3, 0.3)
            cell = blob(cx, SPINE_Y - 2, 22 * k, 22 * k, R.s("blk", j))
            R.knockout(cell)
            R.fill(cell, "blue")
            R.stroke(cell, "navy", 4)
            R.stroke(wline(cx - 9 * k, SPINE_Y - 2, cx + 9 * k, SPINE_Y - 2, R.s("minus", j), 0.2), "navy", 5)
        if t < T_GATE + 1.2:
            tagbg = wrect(xs - 52, SPINE_Y + 44, 184, 58, R.s("blkbg"), amp=1.0, r=12)
            R.knockout(tagbg)
            R.stroke(tagbg, "blue", 3)
            hand(R, "blockers", xs + 40, SPINE_Y + 86, 50, "blue", t=t, t0=T_BLOCKERS, rot=-3)
    # the gate: doors swing in over BOTH pain wires (touch damps the sharp and the slow signals)
    if t >= T_GATE - 0.3:
        gk = ease_out_back(prog(t, T_GATE, T_GATE + 0.4), 1.4)
        for lane in (xf, xs):
            for sx in (-1, 1):
                w = 8 + 26 * gk
                x0 = lane - 40 if sx < 0 else lane + 40 - w
                door = wrect(x0, SPINE_Y - 44, w, 88, R.s("door", lane, sx), amp=0.8, r=6)
                R.knockout(door)
                R.fill(door, "orange")
                R.stroke(door, "navy", 5)
        if t >= T_GATE:
            gbg = wrect((xf + xs) / 2 - 58, SPINE_Y - 116, 116, 62, R.s("gatebg"), amp=1.0, r=12)
            R.knockout(gbg)
            R.stroke(gbg, "navy", 3)
            hand(R, "gate", (xf + xs) / 2, SPINE_Y - 70, 56, "navy", t=t, t0=T_GATE, rot=-4)
    walkers(R, t, shrink_from=T_DOWN)
    if t < 37.18:
        side_pip(R, t, expr="normal", look=(1, -0.4))
    elif t < T_DOWN:
        side_pip(R, t, expr="worried", look=(1, 0.4), sweat=0.5, lift=(0, 26))
    elif t < 49.75:
        side_pip(R, t, expr="happy", look=(1, -0.4))
    else:
        side_pip(R, t, expr="normal", look=(0.6, -0.4), arms="shrug")


CARD_ROWS_T = [51.3, 52.27, 53.04]          # "Sharp first. Ache second. Rub it down."


def scene_card(R, t):             # 51.1 - 54.0
    R.flood("teal", 0.55)
    dots_bg(R, "navy", 0.1)
    c = R.c
    k = ease_out_back(prog(t, T_CARD, T_CARD + 0.45), 1.2)
    cy = lerp(-900, 980, k)
    rot = lerp(-10, -2.0, k)
    c.save()
    c.translate(W / 2, cy)
    c.rotate(rot)
    cw, ch = 820, 960
    card = wrect(-cw / 2, -ch / 2, cw, ch, R.s("card"), 1.5, r=26)
    R.knockout(card)
    R.stroke(card, "navy", 8)
    R.stroke(wrect(-cw / 2 + 26, -ch / 2 + 26, cw - 52, ch - 52, R.s("card2"), 1.2, r=16), "navy", 3)
    R.text("LAW #002", -cw / 2 + 60, -ch / 2 + 100, R.A.font("mono", 40), "navy", align="left")
    R.text("BRAIN LAWS", cw / 2 - 60, -ch / 2 + 100, R.A.font("mono", 28), "teal", align="right")
    fb = R.A.font("bagel", 116)
    R.text("DOUBLE", 0, -ch / 2 + 250, fb, "navy", shadow=("pink", 6, 6))
    R.text("PAIN", 0, -ch / 2 + 370, fb, "navy", shadow=("pink", 6, 6))
    R.stroke(wline(-cw / 2 + 70, -ch / 2 + 418, cw / 2 - 70, -ch / 2 + 418, R.s("rule"), 0.8), "navy", 4)
    rows = [("SHARP: 0.4 s", "teal", CARD_ROWS_T[0]), ("ACHE: 1.9 s", "pink", CARD_ROWS_T[1]), ("RUB IT: GATE", "blue", CARD_ROWS_T[2])]
    for i, (s, ink, t0) in enumerate(rows):
        y = -ch / 2 + 526 + i * 116
        if t >= t0:
            R.text(s, -cw / 2 + 90, y, R.A.font("bagel", 78), ink, align="left", shadow=("navy", 4, 4), scale=pop_scale(t, t0))
    hand(R, "Plaghki 2010 · Melzack & Wall 1965", -cw / 2 + 80, ch / 2 - 56, 44, align="left", rot=-1)
    c.restore()
    # Pip sits on the card's top edge
    P = PipState(x=790, ground=cy - ch / 2 + 6, scale=0.55, blink=pip_blink(t), talk=talking(t), expr="happy")
    draw_pip(R, P)
    if t >= 53.6:
        sc = lerp(1.8, 1.0, ease_out_back(prog(t, 53.6, 53.9), 1.1))
        c.save()
        c.translate(760, 1290)
        c.rotate(-12)
        c.scale(sc * 0.7, sc * 0.7)
        R.stroke(wrect(-190, -62, 380, 124, R.s("stamp"), 2.0, r=18), "pink", 11)
        R.text("COLLECTED", 0, 22, R.A.font("mono", 54), "pink")
        c.restore()


def scene_outro(R, t):            # 54.0 - end: the question, then Pip wanders back into frame 0
    draw_ground(R)
    toy_block(R)
    if t < 60.2:
        P = PipState(x=300, ground=GROUND, scale=PIP_S, blink=pip_blink(t), talk=talking(t), expr="happy")
        P.squash = 1 + 0.015 * math.sin(t * 3.0)
        if 54.0 <= t < 57.9:
            P.expr, P.look = "normal", (0.2, -0.3)
        if 59.13 <= t < 60.2:
            P.expr, P.look = "normal", (math.sin((t - 59.13) * 5) * 1.0, -0.2)
        draw_pip(R, P)
        if 57.94 <= t < 59.6:       # arrow down to the comments
            k = ease_out(prog(t, 58.1, 58.5))
            R.stroke(wline(W / 2 + 60, 720, W / 2 + 70, 720 + 200 * k, R.s("arr"), 0.6), "blue", 8)
            if k >= 1:
                R.stroke(wpoly([(W / 2 + 30, 890), (W / 2 + 70, 930), (W / 2 + 104, 884)], R.s("arrh"), 0.4, closed=False), "blue", 8)
    else:                           # walks right, into the block: the last frame meets frame 0
        u = prog(t, 60.2, DURATION)
        x = lerp(300, STUB_X, u)
        P = PipState(x=x, ground=GROUND, scale=PIP_S, blink=pip_blink(t), talk=talking(t), expr="happy")
        P.lift = walk_lift(t, 9.0, 18.0) if u < 0.97 else (0.0, 6.0)
        P.ground = GROUND - abs(math.sin(t * 9.0)) * 5 * (1 - u)
        draw_pip(R, P)


SCENES = [
    (0.0, T_DIAG, scene_cold), (T_DIAG, T_REPLAY, scene_race), (T_REPLAY, T_GATESCENE, scene_replay),
    (T_GATESCENE, T_CARD, scene_gate), (T_CARD, T_OUTRO, scene_card), (T_OUTRO, DURATION + 0.01, scene_outro),
]


def draw_frame(R, t):
    c = R.c
    c.drawImage(R.A.paper, 0, 0)
    for a, b, fn in SCENES:
        if a <= t < b:
            if fn not in (scene_race, scene_replay, scene_gate, scene_card):
                dots_bg(R)
            dx, dy = shake_offset(t)
            c.save()
            c.translate(dx, dy)
            fn(R, t)
            c.restore()
            break
    if not (HUD_ON[0] <= t < HUD_ON[1]) and not (T_CARD <= t < T_OUTRO):
        header(R)
    draw_hud(R, t)
    for cap in CAPTIONS:
        cap.draw(R, t)
