"""LAW #001 — The Square-Cube Law (v5: cold open, loop).  62 s at 120 BPM (31 bars).

Built against an independent review (25 Oct 2026). The rules it set for every episode:
- frame 0 shows the most dramatic outcome, and Pip says it within 1.5 s; the explanation comes after (cold open);
- no title card: the law's name lands as a rubber stamp over the action;
- the hook never overstates: 2x bigger is the "ouch" step, 10x is what breaks (bone takes twice the load);
- one picture carries the idea: the same cubes are the weight from the first count to the last;
- Pip stays on screen; every big number is said out loud, one per second;
- captions mirror the line Pip is saying; labels >= 50 px; nothing under the TikTok buttons (x > 900);
- the recap is short, there is one famous reference (shares) and one question to argue about (comments);
- the last line runs into the first ("...unless you" -> "Make me ten times bigger") and the last frame is the first;
- just over one minute: TikTok's Creator Rewards only pay for videos longer than 1 minute.
"""
import math
import numpy as np
import skia
from engine import *

TITLE = "LAW #001"
DURATION = 62.0
BPM = 120
CAP_Y = 410
SERIES = "Tiny Laws"
TRANSPOSE = 0


def C(a, b, segs, **kw):
    kw.setdefault("y", CAP_Y)
    kw.setdefault("size", 80)
    kw.setdefault("emph_size", 104)
    kw.setdefault("word_gap", 0.0)
    return Caption(a, b, segs, **kw)


# times of the things Pip counts (the picture, the pops and the voice all use them; measured on the voice)
CUBE_T = [14.86, 15.2, 15.46, 15.85, 16.2, 16.55, 16.9, 17.26]
SQUARE_T = [25.98, 26.24, 26.58, 26.8]
BLOCK_T = [30.0 + j * 0.22 for j in range(8)]
CARD_ROWS_T = [53.05, 54.35, 55.7]          # "Size times two. Strength times four. Weight times eight."
CRUNCH_OPEN, CRUNCH_BIG = 1.6, 44.5
MYTH_STRIKE, LAW_STAMP = 6.7, 7.35

CAPTIONS = [
    C(0.0, 1.6, [(-0.5, "Make me *10× bigger...*")], plate=True),
    C(1.6, 3.8, [(1.6, "...and my own weight /"), (2.8, "*crushes me!*")], plate=True),
    C(3.8, 4.55, [(3.8, "*Rewind!*")], plate=True),
    C(4.55, 7.1, [(4.55, "Bigger = *stronger?*")]),
    C(8.6, 10.2, [(8.6, "This *cube* /"), (9.0, "stands for me.")]),
    C(10.2, 12.9, [(10.2, "Make it *2× bigger* /"), (11.0, "in every direction.")]),
    C(12.9, 18.0, [(12.9, "How many small cubes /"), (13.6, "fit inside?")]),
    C(18.0, 19.4, [(18.0, "8 cubes = /"), (18.1, "*8× the weight.*")]),
    C(19.4, 21.5, [(19.4, "My bones hold me up, /"), (20.3, "like *pillars.*")]),
    C(21.5, 24.5, [(21.5, "Pillar strength = /"), (22.3, "the size of its *slice.*")]),
    C(24.5, 27.3, [(24.5, "2× bigger pillar: /"), (25.4, "its slice = *4 squares.*")]),
    C(27.3, 28.8, [(27.3, "4 squares = /"), (27.4, "*4× the strength.*")]),
    C(28.8, 31.8, [(28.8, "Weight ×8, /"), (29.6, "but strength only *×4.*")]),
    C(31.8, 34.3, [(31.8, "Each square of bone /"), (32.6, "carries *2 cubes.*")]),
    C(34.3, 36.4, [(34.3, "*Twice the load.* /"), (35.3, "Ouch.")]),
    C(36.4, 39.4, [(36.4, "Now *10× bigger.* /"), (37.9, "Like King Kong.")], plate=True),
    C(39.4, 41.0, [(39.4, "*1,000×* heavier...")], plate=True),
    C(41.0, 42.9, [(41.0, "but only /"), (41.4, "*100×* stronger.")], plate=True),
    C(42.9, 44.5, [(42.9, "*10 cubes* /"), (43.5, "on every square!")], plate=True),
    C(44.5, 46.0, [(44.5, "*CRUNCH.*")], emph_size=150),
    C(46.0, 49.0, [(46.0, "That's why real giants /"), (47.0, "need *thick legs...*")]),
    C(49.0, 52.6, [(49.0, "...and tiny ants /"), (50.0, "are strong *for their size.*")]),
    C(57.8, 60.6, [(57.8, "So... I'm staying *tiny.*")]),
    C(60.6, 62.0, [(60.6, "...unless *you...*")], plate=True),
]

# ------------------------------------------------------------------ narration (voice.py, free Kokoro voice)
VOICE = "af_heart"
VOICE_SPEED = 1.0
# Pip's character voice ("light cartoon", casting take 07): +3 semitones, clean and bright.
# Lines can vary it ({"semitones": 4} for excitement, 2 for sad) so the delivery is not flat.
VOICE_FX = {"semitones": 3}
NARRATION = [
    (0.0, "Make me ten times bigger..."),
    (1.9, "and my own weight crushes me!", {"semitones": 2}),
    (3.8, "Rewind!", {"semitones": 4, "speed": 1.1}),
    (4.55, "Bigger means stronger... right?", {"semitones": 4}),
    (6.65, "Nope! Meet the square-cube law."),
    (8.6, "This cube stands for me."),
    (10.2, "Make it two times bigger, in every direction."),
    (12.9, "How many small cubes fit inside?"),
    (14.8, "One, two, three..."),
    (17.25, "eight!", {"semitones": 4}),
    (18.0, "Eight times the weight!"),
    (19.4, "My bones hold me up, like pillars."),
    (21.5, "A pillar's strength depends on the size of its slice."),
    (24.5, "Two times bigger pillar..."),
    (25.9, "one, two, three, four."),
    (27.3, "Four times the strength."),
    (28.8, "Weight times eight, but strength only times four."),
    (31.8, "So each square of bone carries two cubes."),
    (34.3, "Twice the load. Ouch!", {"semitones": 2}),
    (36.4, "Now make me ten times bigger. Like King Kong.", {"semitones": 4}),
    (39.4, "A thousand times heavier..."),
    (41.0, "but only a hundred times stronger."),
    (42.9, "Ten cubes on every square!", {"semitones": 2}),
    (45.15, "Owww...", {"semitones": 1}),
    (46.0, "That's why real giants need thick legs..."),
    (49.0, "and why tiny ants are so strong for their size.", {"semitones": 4}),
    (53.0, "Size times two. Strength times four. Weight times eight."),
    (57.8, "So, I'm staying tiny..."),
    (60.6, "unless you...", {"semitones": 4}),
]

import os as _os
_ENV_PATH = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "out", f"{__name__}_voice_env.npy")
VOICE_ENV = np.load(_ENV_PATH) if _os.path.exists(_ENV_PATH) else None

# Without narration, Pip "speaks" each line with one soft voice blip (not one per word)
SEG_TIMES = sorted({max(0.0, ta) for cap in CAPTIONS for (ta, s, e) in cap.words
                    if s not in ("/", "CRUNCH.") and not s.startswith("CRUNCH")})
WORD_TIMES = SEG_TIMES


def talking(t):
    if VOICE_ENV is not None:                      # mouth follows the narration
        i = int(t * 24)
        return 1.0 if 0 <= i < len(VOICE_ENV) and VOICE_ENV[i] > 0.12 else 0.0
    for ts in SEG_TIMES:
        u = t - ts
        if 0 <= u < 0.6:
            return 1.0 if math.sin(u * 30) > 0 else 0.0
    return 0.0


# ------------------------------------------------------------------ scoreboard (the teaching spine)
HUD_ON = (11.1, 46.0)
HUD = {
    "SIZE": ("navy", [(11.1, "×2"), (37.2, "×10")]),
    "STRENGTH": ("blue", [(27.4, "×4"), (41.5, "×100")]),
    "WEIGHT": ("pink", [(18.1, "×8"), (39.65, "×1,000")]),
}

# ------------------------------------------------------------------ sound: few, soft accents
SFX = [
    (0.15, "boing_up", 0), (CRUNCH_OPEN, "crunch", 0), (2.0, "dizzy", 0),
    (3.8, "shrink", 0), (MYTH_STRIKE, "scribble", 0), (LAW_STAMP, "slam", 0),
    (9.1, "thud", 0), (11.1, "boing_up", 1),
] + [(t, "pop", i) for i, t in enumerate(CUBE_T)] + [
    (18.1, "ding", 0), (23.5, "pop", 2),
] + [(t, "tick", i) for i, t in enumerate(SQUARE_T)] + [
    (27.4, "ding", 1),
] + [(t, "pop", i) for i, t in enumerate(BLOCK_T)] + [
    (35.3, "crack", 1), (36.8, "boing_up", 2),
    (CRUNCH_BIG, "crunch", 0), (44.9, "dizzy", 0),
    (47.5, "boing_down", 0), (52.6, "paper", 0), (56.8, "stamp", 1), (58.4, "shrug", 0), (60.8, "boing_up", 3),
]
SHAKES = [(CRUNCH_OPEN, 12), (LAW_STAMP, 5), (CRUNCH_BIG, 12), (56.8, 3)]
MUSIC_CUTS = [(1.5, 4.0), (44.0, 46.0)]   # tape-stops into both crunches, back on the downbeats of bars 3 and 24

SUBTITLE_EXTRAS = [
    (7.1, 8.6, "Nope! Meet the square–cube law."),
    (52.6, 57.6, "Size ×2, strength ×4, weight ×8. Weight grows faster than strength."),
]


def music_sections(t):
    s = {"drums": 1, "bass": 1, "keys": 1, "lead": 1}
    if t < 8.6:
        s.update(lead=0)
    elif 19.4 <= t < 28.8:
        s.update(var=1)
    elif 28.8 <= t < 44.0:
        s.update(var=2)
    elif 52.0 <= t < 57.6:
        s.update(glock=1, var=3)
    elif t >= 58.0:
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


def draw_ground(R, x0=40, x1=1040, y=GROUND, w=7):
    R.stroke(wline(x0, y + 2, x1, y - 2, R.s("ground", x0), 2.0), "navy", w)


def draw_star(R, x, y, r, rot, seed, ink="yellow"):
    sp = star_path(x, y, r, r * 0.45, rot=rot, seed=R.s("star", seed))
    R.fill(sp, ink)
    R.stroke(sp, "navy", 5)


def pop_scale(t, t0, dur=0.35, frm=0.4):
    return lerp(frm, 1.0, ease_out_back(prog(t, t0, t0 + dur), 1.6))


def label(R, s, x, y, size=84, ink="navy", shadow="pink", t=None, t0=None, font="bagel", rot=0.0):
    sc = 1.0
    if t is not None and t0 is not None:
        if t < t0:
            return
        sc = pop_scale(t, t0)
    f = R.A.font(font, size)
    R.text(s, x, y, f, ink, shadow=(shadow, 5, 5) if shadow else None, scale=sc, rot=rot)


def hand(R, s, x, y, size=58, ink="navy", t=None, t0=None, align="center", rot=-3.0):
    if t is not None and t0 is not None and t < t0:
        return
    k = 1.0 if t is None else pop_scale(t, t0, 0.3, 0.5)
    R.text(s, x, y, R.A.font("hand", size), ink, align=align, rot=rot, scale=k)


def dim_arrow(R, x0, y0, x1, y1, ink, seed, w=6):
    R.stroke(wline(x0, y0, x1, y1, R.s("dim", seed), 0.8), ink, w)
    ang = math.atan2(y1 - y0, x1 - x0)
    for (px, py, a) in ((x1, y1, ang), (x0, y0, ang + math.pi)):
        for d in (0.45, -0.45):
            R.stroke(wline(px, py, px - 24 * math.cos(a + d), py - 24 * math.sin(a + d), R.s("dh", seed, d, px), 0.3), ink, w)


def box(R, x, y, w, h, ink, seed, r=10, shade=True):
    p = wrect(x, y, w, h, R.s("box", seed), amp=1.4, r=r)
    R.knockout(p)
    R.fill(p, ink)
    if shade:
        R.halftone(wrect(x + w * 0.62, y, w * 0.38, h, 2, amp=0), "navy", scale=0.55, alpha=0.25)
    R.stroke(p, "navy", 6)


def block(R, x, y, s, seed):
    """One of the small cubes from the count, seen from the front (same three inks), so the weight
    keeps one shape for the whole episode."""
    d = s * 0.28
    top = wpoly([(x, y), (x + d, y - d), (x + s + d, y - d), (x + s, y)], R.s("bt", seed), 0.5)
    side = wpoly([(x + s, y), (x + s + d, y - d), (x + s + d, y + s - d), (x + s, y + s)], R.s("bs", seed), 0.5)
    front = wrect(x, y, s, s, R.s("bf", seed), amp=1.0, r=4)
    for p, ink in ((side, "blue"), (top, "yellow"), (front, "pink")):
        R.knockout(p)
        R.fill(p, ink)
        R.stroke(p, "navy", 5)
    R.halftone(front, "navy", scale=0.5, alpha=0.18)


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
    return ((t + 1.3) % 3.1) < 0.09          # never on the first or last frame (thumbnail, loop seam)


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
        # a fresh value glows for 1.5 s so the eye knows where to look
        if t_set is not None and t - t_set < 1.5:
            R.fill(card, "yellow", alpha=0.55 * (1 - prog(t, t_set + 0.8, t_set + 1.5)))
        R.stroke(card, "navy", 5)
        R.text(name, cx, y0 + 34, R.A.font("mono", 24), "navy")
        if v is None:
            R.text("?", cx, y0 + 100, R.A.font("bagel", 58), "navy", alpha=0.35)
        else:
            f = R.A.font("bagel", 64)
            wv = f.measureText(v)
            if wv > w - 36:
                f = R.A.font("bagel", 64 * (w - 36) / wv)
            R.text(v, cx, y0 + 102, f, ink, shadow=("navy", 4, 4) if ink != "navy" else ("yellow", 4, 4),
                   scale=pop_scale(t, t_set, 0.35, 0.5))
        c.restore()


def caption_width(R, cap):
    """Width of the first line of a caption, as Caption.draw lays it out."""
    line = cap.layout(R.A)[0]
    return sum(ww for (_, _, _, _, ww, _) in line) + sum(sp for (_, _, _, _, _, sp) in line[1:])


# ------------------------------------------------------------------ the big Pip (cold open, climax, loop)
BIG0 = (0.74, 6.0)        # zoom and scale of frame 0; the last frame grows back into it


def big_pip(R, t, z, sc, strain, crunch_t=None, crack0=0.0):
    """Pip at giant scale inside a zoomed-out world. strain 0..1 drives tremble, sweat and cracks."""
    c = R.c
    c.save()
    c.translate(W / 2, GROUND)
    c.scale(z, z)
    c.translate(-W / 2, -GROUND)
    draw_ground(R, -1200, 2300, w=7 / z)
    P = PipState(ground=GROUND, scale=sc, blink=pip_blink(t), talk=talking(t))
    P.expr = "worried" if strain > 0 else "happy"
    P.tremble = 1.5 + 2.5 * strain if strain > 0 else 0
    P.crack = max(crack0, strain)
    P.sweat = min(1.0, strain * 1.5)
    if crunch_t is not None and t >= crunch_t:
        P.flat = ease_out_back(prog(t, crunch_t, crunch_t + 0.3), 1.1)
        P.tremble = 0
        P.expr = "dizzy"
        P.crack = 0
        P.sweat = 0
    draw_pip(R, P)
    c.restore()
    if crunch_t is not None and t >= crunch_t:
        u = t - crunch_t
        for i, sx in enumerate((-1, 1)):
            for j in range(3):
                r = 30 + 60 * ease_out(prog(u, 0, 0.6)) + j * 18
                a = 1 - prog(u, 0.3, 1.0)
                if a > 0:
                    R.halftone(blob(W / 2 + sx * (420 + j * 70 + u * 160), GROUND - 30 - j * 26, r, r * 0.7, R.s("dust", i, j)), "navy", 0.7, alpha=a)
        for k in range(5):
            ang = u * 1.8 + k * 2 * math.pi / 5
            draw_star(R, W / 2 + math.cos(ang) * 280, GROUND - 330 + math.sin(ang) * 50, 34, 0, k)


# ------------------------------------------------------------------ scenes
def scene_cold(R, t):             # 0 - 3.8: the outcome first
    u = ease_in_out(prog(t, 0.0, 1.3))
    z = lerp(BIG0[0], 0.62, u)
    sc = lerp(BIG0[1], 10.0, u)
    strain = lerp(0.35, 1.0, prog(t, 0.0, 1.5))
    big_pip(R, t, z, sc, strain, crunch_t=CRUNCH_OPEN, crack0=0.3)
    if t >= CRUNCH_OPEN:
        label(R, "CRUNCH!", W / 2, 930, 140, "navy", "yellow", t=t, t0=CRUNCH_OPEN, rot=-6)


def scene_myth(R, t):             # 3.8 - 8.6: rewind, the myth, the law's name
    u = ease_in_out(prog(t, 3.8, 4.4))
    if t < 4.4:                    # the crunch plays backwards: un-flatten, shrink, zoom back in
        z = lerp(0.62, 1.0, u)
        sc = lerp(10.0, 1.8, u)
        c = R.c
        c.save()
        c.translate(W / 2, GROUND)
        c.scale(z, z)
        c.translate(-W / 2, -GROUND)
        draw_ground(R, -1200, 2300, w=7 / z)
        P = PipState(ground=GROUND, scale=sc, expr="dizzy" if u < 0.5 else "normal")
        P.flat = 1 - u
        draw_pip(R, P)
        c.restore()
        f = R.A.font("mono", 34)
        tag = wrect(W - 360, 236, 300, 64, R.s("rw"), amp=1.2, r=8)
        R.fill(tag, "pink")
        R.stroke(tag, "navy", 5)
        R.text("<< REWIND", W - 210, 280, f, "navy")
        return
    draw_ground(R)
    P = PipState(ground=GROUND, scale=1.8, blink=pip_blink(t), talk=talking(t))
    P.squash = 1 + 0.015 * math.sin(t * 3.0)
    if t < MYTH_STRIKE:
        P.expr = "happy"
        P.arms = "up" if 4.9 <= t < 6.5 else "down"
    elif t < MYTH_STRIKE + 0.35:
        P.expr = "shock"
    else:
        P.expr = "worried"
        P.sweat = prog(t, 6.9, 7.6)
    draw_pip(R, P)
    if t >= LAW_STAMP:              # the law's name lands as a rubber stamp, no title card
        k = lerp(1.7, 1.0, ease_out_back(prog(t, LAW_STAMP, LAW_STAMP + 0.3), 1.2))
        c = R.c
        c.save()
        c.translate(W / 2, 560)
        c.rotate(-6)
        c.scale(k, k)
        st = wrect(-430, -150, 860, 300, R.s("lawst"), 2.0, r=22)
        R.knockout(st)
        R.stroke(st, "pink", 12)
        R.stroke(wrect(-405, -125, 810, 250, R.s("lawst2"), 1.6, r=16), "pink", 4)
        R.text("LAW #001", 0, -66, R.A.font("mono", 40), "navy")
        R.text("SQUARE–CUBE LAW", 0, 56, R.A.font("bagel", 90), "navy", shadow=("yellow", 6, 6))
        c.restore()


def scene_cube(R, t):             # 8.6 - 19.4
    ox, oy = 620, 1000
    s_small, s_big = 150, 280
    drop = ease_out_back(prog(t, 8.8, 9.3), 1.2)
    s = lerp(s_small, s_big, ease_out_elastic(prog(t, 11.1, 11.9)))
    yoff = lerp(-1500, 0, drop)
    P = lambda x, y, z: iso(x, y, z, 1, ox, oy)
    if t < 13.3:
        draw_cube(R, ox, oy + yoff, s, (-s / 2, -s / 2, -s / 2), seed="big")
        if 9.3 <= t < 11.1:
            hand(R, "= me", 380, 1150, 60, t=t, t0=9.3, rot=-6)
            R.stroke(wpoly([(330, 1170), (360, 1200), (410, 1215)], R.s("eqme"), 0.4, closed=False), "navy", 4)
        if t >= 11.9:
            h = s / 2
            on = t < 13.0
            ink = "pink" if on else "navy"
            a, b = P(-h, h, -h), P(h, h, -h)
            dim_arrow(R, a[0] - 26, a[1] + 34, b[0] - 26, b[1] + 34, ink, "w")
            hand(R, "×2", (a[0] + b[0]) / 2 - 60, (a[1] + b[1]) / 2 + 80, 60, ink, rot=28)
            a, b = P(h, -h, -h), P(h, h, -h)
            dim_arrow(R, a[0] + 26, a[1] + 34, b[0] + 26, b[1] + 34, ink, "d")
            hand(R, "×2", (a[0] + b[0]) / 2 + 66, (a[1] + b[1]) / 2 + 76, 60, ink, rot=-28)
            a, b = P(-h, h, -h), P(-h, h, h)
            dim_arrow(R, a[0] - 36, a[1], b[0] - 36, b[1], ink, "t")
            hand(R, "×2", a[0] - 76, (a[1] + b[1]) / 2 + 10, 60, ink, rot=0)
    else:
        draw_cube(R, ox, oy, s_big, (-s_big / 2, -s_big / 2, -s_big / 2), seed="ghost", outline_only=True, alpha=0.3)
        hs = s_big / 2
        order = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1)]
        present, n_landed = [], 0
        for i, (a, b, cc) in enumerate(order):
            t0 = CUBE_T[i]
            if t >= t0 - 0.25:
                d = ease_out(prog(t, t0 - 0.25, t0), 2)
                present.append(((a, b, cc), lerp(220, 0, d), i))
            if t >= t0:
                n_landed = i + 1
        present.sort(key=lambda v: v[0][0] + v[0][1] + v[0][2])
        cols = [("yellow", "pink", "blue"), ("yellow", "blue", "pink")]
        for (a, b, cc), zoff, i in present:
            draw_cube(R, ox, oy, hs, (-s_big / 2 + a * hs, -s_big / 2 + b * hs, -s_big / 2 + cc * hs + zoff),
                      seed=("m", i), faces=cols[i % 2])
        if n_landed:
            label(R, str(n_landed), 190, 900, 150, "pink", "navy", t=t, t0=CUBE_T[n_landed - 1])
            hand(R, "small cubes", 190, 980, 52, rot=-4)
    Pp = PipState(x=190, ground=GROUND, scale=0.55, blink=pip_blink(t), talk=talking(t), look=(1, -0.5))
    Pp.expr = "shock" if CUBE_T[-1] < t < CUBE_T[-1] + 1.5 else "normal"
    draw_pip(R, Pp)
    draw_ground(R, 60, 1020, w=5)


def draw_leg(R, x, y0, y1, w):
    leg = wrect(x - w / 2, y0, w, y1 - y0, R.s("legc"), amp=1.4, r=w / 2.2)
    R.knockout(leg)
    R.fill(leg, "pink", 0.85)
    R.stroke(leg, "navy", 7)
    draw_bone(R, x, (y0 + y1) / 2, (y1 - y0) * 0.86, w * 0.42, "xbone", rot=90)


def slice_square(R, cx, cy, side, seed, grid=1, t=None, t_nums=None):
    p = wrect(cx - side / 2, cy - side / 2, side, side, R.s("sl", seed), amp=1.2, r=8)
    R.knockout(p)
    R.fill(p, "blue", 0.9)
    R.halftone(p, "navy", 0.5, alpha=0.2)
    R.stroke(p, "navy", 6)
    if grid > 1:
        for k in range(1, grid):
            f = side * k / grid
            R.stroke(wline(cx - side / 2 + f, cy - side / 2, cx - side / 2 + f, cy + side / 2, R.s("gx", seed, k), 0.6), "navy", 4)
            R.stroke(wline(cx - side / 2, cy - side / 2 + f, cx + side / 2, cy - side / 2 + f, R.s("gy", seed, k), 0.6), "navy", 4)
    if t_nums is not None:
        q = side / grid
        for i in range(grid * grid):
            t0 = t_nums[i]
            if t >= t0:
                gx_, gy_ = i % grid, i // grid
                label(R, str(i + 1), cx - side / 2 + q * (gx_ + 0.5), cy - side / 2 + q * (gy_ + 0.5) + 26, 70, "navy", "yellow", t=t, t0=t0)


def side_pip(R, t, x, ground, scale, expr="normal", look=(-1, -0.5), sweat=0.0):
    """Pip stays on screen in the explanation, small, watching and reacting."""
    P = PipState(x=x, ground=ground, scale=scale, blink=pip_blink(t), talk=talking(t), look=look, expr=expr)
    P.sweat = sweat
    draw_pip(R, P)


def scene_bones(R, t):            # 19.4 - 28.8
    R.flood("blue", 0.16)
    dots_bg(R, "navy", 0.07)
    if t >= 19.6:
        k = pop_scale(t, 19.6, 0.45, 0.6)
        R.c.save()
        R.c.translate(270, 1000)
        R.c.scale(k, k)
        R.c.translate(-270, -1000)
        draw_leg(R, 270, 740, 1300, 150)
        R.c.restore()
        hand(R, "my leg", 270, 1390, 56, rot=-3)
        hand(R, "bone", 420, 800, 54, rot=-6, t=t, t0=20.2)
        if t >= 20.2:
            R.stroke(wpoly([(380, 810), (330, 845), (290, 880)], R.s("ba"), 0.5, closed=False), "navy", 4)
    if t >= 22.9:
        u = ease_out(prog(t, 22.9, 23.4))
        R.stroke(wline(150, 1000, 150 + 240 * u, 1000, R.s("cut"), 0.4), "pink", 7)
        hand(R, "cut", 455, 975, 50, "navy", t=t, t0=23.1, rot=-4)
    if t >= 23.5:
        slice_square(R, 600, 1010, 90 * pop_scale(t, 23.5), "s1")
        hand(R, "slice", 600, 1116, 52, rot=-2)
        R.stroke(wpoly([(420, 1005), (480, 990), (540, 1000)], R.s("sa"), 0.5, closed=False), "navy", 4)
        if t >= 23.9:
            label(R, "1", 600, 1036, 64, "navy", "yellow", t=t, t0=23.9)
    if t >= 25.0:
        sz = 180 * pop_scale(t, 25.0, 0.45, 0.3)
        slice_square(R, 800, 1010, sz, "s2", grid=2, t=t, t_nums=SQUARE_T)
        hand(R, "2× bigger", 800, 1166, 52, rot=2)
    side_pip(R, t, 760, 1480, 0.5, expr="happy" if t >= 27.4 else "normal", look=(-1, -0.6))


def scene_load(R, t):             # 28.8 - 36.4
    R.flood("yellow", 0.28)
    dots_bg(R, "navy", 0.07)
    base, sq = 1260, 100
    # normal me: 1 square of bone, 1 cube on it
    if t >= 29.0:
        box(R, 230 - sq / 2, base - sq, sq, sq, "blue", "n-sq")
        block(R, 230 - sq / 2, base - 2 * sq, sq, "n-bl")
        hand(R, "normal me", 230, base + 70, 52, rot=-3)
        hand(R, "1 each", 230, base - 2 * sq - 56, 50, rot=-3)
    xs = [470 + i * (sq + 8) for i in range(4)]
    crack_on = t >= 35.3
    if t >= 29.5:
        for i, x in enumerate(xs):
            jitter = math.sin(t * 30 + i) * 1.2 if crack_on else 0
            box(R, x + jitter, base - sq, sq, sq, "blue", ("q", i))
            if crack_on:
                R.stroke(wpoly([(x + 30, base - sq + 10), (x + 50, base - sq + 40), (x + 36, base - sq + 62)], R.s("qc", i), 0.4, closed=False), "navy", 4)
        hand(R, "2× me: 4 squares", 470 + 2 * (sq + 8) - 4, base + 70, 52, rot=2)
        for j in range(8):
            t0 = BLOCK_T[j]
            if t >= t0 - 0.25:
                col, lvl = j % 4, j // 4
                d = ease_out(prog(t, t0 - 0.25, t0), 2)
                yb = lerp(base - sq - 420, base - sq - sq * (lvl + 1), d)
                block(R, xs[col], yb, sq, ("b", j))
    if t >= 33.5:
        label(R, "8 ÷ 4 = 2", 660, 840, 84, "navy", "pink", t=t, t0=33.5)
    side_pip(R, t, 540, 1540, 0.46, expr="worried" if crack_on else "normal", look=(0, -1), sweat=prog(t, 35.3, 35.9))


def scene_giant(R, t):            # 36.4 - 46
    u = ease_in_out(prog(t, 36.8, 38.4))
    z = lerp(1.0, 0.62, u)
    sc = lerp(1.6, 10.0, u)
    strain = prog(t, 41.0, 44.4) if t > 41.0 else 0.0
    big_pip(R, t, z, sc, strain, crunch_t=CRUNCH_BIG)
    c = R.c
    if 42.9 <= t < 44.4:
        k = pop_scale(t, 42.9, 0.3, 0.5)
        c.save()
        c.translate(220, 1000)
        c.scale(k, k)
        c.translate(-220, -1000)
        panel = wrect(70, 700, 300, 600, R.s("inset"), amp=1.5, r=16)
        R.knockout(panel)
        R.stroke(panel, "navy", 6)
        bs = 1240
        box(R, 180, bs - 80, 80, 80, "blue", "isq")
        for j in range(10):
            if t >= 43.0 + j * 0.1:
                box(R, 180, bs - 80 - 36 * (j + 1), 80, 36, "pink", ("ib", j), r=6, shade=False)
        hand(R, "10 per square", 220, 770, 50, rot=-2)
        c.restore()


def scene_thick(R, t):            # 46 - 49
    draw_ground(R)
    P = PipState(ground=GROUND, scale=1.6, expr="deadpan", blink=pip_blink(t), talk=talking(t))
    P.legs_thick = lerp(1.0, 4.3, ease_out_elastic(prog(t, 47.5, 48.5)))
    draw_pip(R, P)
    if t >= 47.9:
        hand(R, "(like an elephant's)", 520, GROUND + 74, 58, t=t, t0=47.9, rot=-2)


def draw_leaf(R, x, y, w, rot=0.0):
    lf = blob(x, y, w / 2, w / 4.2, R.s("leaf"), amp=0.03, rot=rot)
    R.knockout(lf)
    R.fill(lf, "yellow")
    R.fill(lf, "blue", 0.85)
    R.stroke(lf, "navy", 5)
    R.stroke(wline(x - w * 0.42 * math.cos(rot), y - w * 0.42 * math.sin(rot), x + w * 0.42 * math.cos(rot), y + w * 0.42 * math.sin(rot), R.s("rib"), 0.4), "navy", 3)


def scene_small(R, t):            # 49 - 52.6
    draw_ground(R)
    P = PipState(x=240, ground=GROUND, scale=0.6, blink=pip_blink(t), talk=talking(t), look=(1, 0))
    P.expr = "shock" if t >= 50.6 else "normal"
    draw_pip(R, P)
    ax = lerp(1150, 700, ease_out(prog(t, 49.3, 50.6)))
    stp = t * 3.0 if t < 50.6 else 0
    draw_leaf(R, ax - 30, GROUND - 215, 220, rot=-0.12)
    R.stroke(wline(ax - 70, GROUND - 78, ax - 45, GROUND - 185, R.s("stick"), 0.3), "navy", 4)
    draw_ant(R, ax, GROUND - 2, 2.8, step=stp, flip=True)
    if t >= 50.8:
        hand(R, "ant + a leaf", 560, GROUND + 66, 56, t=t, t0=50.8, rot=-2)
        hand(R, "many times its weight", 560, GROUND + 130, 52, t=t, t0=50.8, rot=-2)


def scene_card(R, t):             # 52.6 - 57.6
    R.flood("blue", 0.7)
    dots_bg(R, "navy", 0.1)
    c = R.c
    k = ease_out_back(prog(t, 52.6, 53.1), 1.2)
    cy = lerp(-900, 960, k)
    rot = lerp(-10, -2.0, k)
    c.save()
    c.translate(W / 2, cy)
    c.rotate(rot)
    cw, ch = 820, 1000
    card = wrect(-cw / 2, -ch / 2, cw, ch, R.s("card"), 1.5, r=26)
    R.knockout(card)
    R.stroke(card, "navy", 8)
    inner = wrect(-cw / 2 + 26, -ch / 2 + 26, cw - 52, ch - 52, R.s("card2"), 1.2, r=16)
    R.stroke(inner, "navy", 3)
    R.text("LAW #001", -cw / 2 + 60, -ch / 2 + 100, R.A.font("mono", 40), "navy", align="left")
    R.text("TINY LAWS", cw / 2 - 60, -ch / 2 + 100, R.A.font("mono", 28), "pink", align="right")
    fb = R.A.font("bagel", 104)
    R.text("THE SQUARE–", 0, -ch / 2 + 250, fb, "navy", shadow=("pink", 6, 6))
    R.text("CUBE LAW", 0, -ch / 2 + 360, fb, "navy", shadow=("pink", 6, 6))
    R.stroke(wline(-cw / 2 + 70, -ch / 2 + 410, cw / 2 - 70, -ch / 2 + 410, R.s("rule"), 0.8), "navy", 4)
    rows = [("SIZE ×2", "navy", CARD_ROWS_T[0]), ("STRENGTH ×4", "blue", CARD_ROWS_T[1]), ("WEIGHT ×8", "pink", CARD_ROWS_T[2])]
    for i, (s, ink, t0) in enumerate(rows):
        y = -ch / 2 + 520 + i * 120
        if t >= t0:
            R.text(s, -cw / 2 + 90, y, R.A.font("bagel", 80), ink, align="left",
                   shadow=("navy", 4, 4) if ink != "navy" else ("yellow", 4, 4), scale=pop_scale(t, t0))
    hand(R, "weight grows faster than strength", -cw / 2 + 90, -ch / 2 + 852, 50, align="left", rot=-1, t=t, t0=55.9)
    hand(R, "Galileo, 1638", -cw / 2 + 80, ch / 2 - 60, 50, align="left", rot=-2)
    c.restore()
    if t >= 56.8:
        sc = lerp(1.8, 1.0, ease_out_back(prog(t, 56.8, 57.1), 1.1))
        c.save()
        c.translate(780, 1260)
        c.rotate(-12)
        c.scale(sc * 0.7, sc * 0.7)
        st = wrect(-190, -62, 380, 124, R.s("stamp"), 2.0, r=18)
        R.stroke(st, "pink", 11)
        R.text("COLLECTED", 0, 22, R.A.font("mono", 54), "pink")
        c.restore()


def scene_outro(R, t):            # 57.6 - 62: grows back into frame 0, so the loop is seamless
    u = ease_in(prog(t, 60.8, 62.0))
    if u <= 0:
        draw_ground(R)
        P = PipState(ground=GROUND, scale=0.9, blink=pip_blink(t), talk=talking(t), expr="happy")
        P.squash = 1 + 0.015 * math.sin(t * 3.0)
        if 58.4 <= t < 60.4:
            P.arms = "shrug"
            P.tilt = 4 * math.sin(prog(t, 58.4, 59.1) * math.pi)
        if t >= 60.4:
            P.expr = "normal"
            P.look = (0.4, -0.4)
        draw_pip(R, P)
    else:
        z = lerp(1.0, BIG0[0], u)
        sc = lerp(0.9, BIG0[1], u)
        big_pip(R, t, z, sc, 0.35 * u, crack0=0.3 * u)
    if 58.2 <= t < 60.8:            # the question people answer in the comments
        hand(R, "which movie giant", W / 2, 820, 62, "blue", t=t, t0=58.2, rot=-3)
        hand(R, "breaks first?", W / 2, 900, 62, "blue", t=t, t0=58.2, rot=-3)
        if t >= 58.5:               # hand-drawn arrow down to the comments
            k = ease_out(prog(t, 58.5, 58.8))
            R.stroke(wline(W / 2 + 250, 870, W / 2 + 300, 870 + 160 * k, R.s("arr"), 0.6), "blue", 7)
            if k >= 1:
                R.stroke(wpoly([(W / 2 + 268, 1006), (W / 2 + 300, 1030), (W / 2 + 318, 996)], R.s("arrh"), 0.4, closed=False), "blue", 7)


SCENES = [
    (0.0, 3.8, scene_cold), (3.8, 8.6, scene_myth), (8.6, 19.4, scene_cube),
    (19.4, 28.8, scene_bones), (28.8, 36.4, scene_load), (36.4, 46.0, scene_giant),
    (46.0, 49.0, scene_thick), (49.0, 52.6, scene_small), (52.6, 57.6, scene_card),
    (57.6, 62.01, scene_outro),
]


def draw_frame(R, t):
    c = R.c
    c.drawImage(R.A.paper, 0, 0)
    for a, b, fn in SCENES:
        if a <= t < b:
            if fn not in (scene_bones, scene_load, scene_card):
                dots_bg(R)
            dx, dy = shake_offset(t)
            c.save()
            c.translate(dx, dy)
            fn(R, t)
            c.restore()
            break
    if not (HUD_ON[0] <= t < HUD_ON[1]) and not (3.8 <= t < 4.4) and not (52.6 <= t < 58.0):
        header(R)
    draw_hud(R, t)
    for cap in CAPTIONS:
        cap.draw(R, t)
    # the myth gets crossed out when Pip says "Nope!"
    myth = CAPTIONS[3]
    if MYTH_STRIKE <= t < myth.end:
        wv = caption_width(R, myth)
        u = ease_out(prog(t, MYTH_STRIKE, MYTH_STRIKE + 0.25))
        x0 = W / 2 - wv / 2 - 24
        R.stroke(wline(x0, CAP_Y + 62, x0 + (wv + 48) * u, CAP_Y + 50, R.s("strike"), 1.2), "pink", 14)
