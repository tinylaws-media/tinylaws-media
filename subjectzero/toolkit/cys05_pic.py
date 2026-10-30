"""COULD YOU SURVIVE? #05 — Mars, no suit: the picture (2D estampe look, sz2d.py). Timed on out/cys05_lines.json.

    python3 sz2render.py cys05_pic                # -> out/cys05_pic_video.mp4
    python3 sz2render.py cys05_pic --sheet 0 2 5 ...

Shots (named, none held longer than 8 s): close (her on the red plain in her hoodie, a dust devil wandering on the
horizon, an old lander and a mesa behind her) → gauge (two columns of air: Earth 101 kPa, Mars drains to 0.6) → co2
(100 dots, 95 turn to CO2, the one tiny O2 dot) → close ("So I hold my breath?") → lungs (two balloons swelling in her
outline) → close (the lab: breathe out; push in: now it gets weird) → boil (a glass at 37 °C boiling) → close (NOPE 1:
the dust blows off the plain in a ring, the dust devil is flung away) → boil (NOT HOT) → crater (a cutaway of the
deepest basin: she slides down, the pressure bar fills toward the boiling line and stops short) → duck (on a rock,
fine: NO LUNGS) → signal (Earth and Mars in the dark, the radio pulse crawling, UP TO 22 MIN) → close (NOPE 2: the
lander's dish snaps off and flies over the horizon) → tease (push in; the HUD question) → horizon (the low sun, the
"strangest part") → clock (the answer: 15 s ring, then the 90 s rescue ring) → close (the lab; NOPE 3: the mesa
collapses, a wall of dust from both sides) → chamber (a steel test chamber, 1960s: the needle falls, bubbles, then
HE RECOVERED; no person drawn) → relief (her, HE RECOVERED) → sunset (new: the blue sunset, her and the duck on a rock) → glow
(split screen: an Earth sunset, orange; a Mars sunset, blue near the sun) → end (the next spawns, "Somewhere with air.", the respawn).
HUD: "YOU'D LAST ?? SECONDS" until the answer, then "YOU'D LAST ~15 S AWAKE". The progress bar is the crater's pressure
bar (its target, the boiling line at 6.3 kPa, is never reached).
"""
import json
import math
import os

import numpy as np
import skia

from sz2d import (W, H, FPS, rgb, mixc, fill, ink, text, smooth_path, rrect, oval, ease_io, prog, font,
                  draw_hero, draw_duck, paper_over, vignette, seal, mottle, words_caption, hud_card, woodgrain,
                  draw_legs, thermometer, mars_sky, mars_ground, mesa, lander, dust_burst, dust_wall, dust_devil,
                  PAPER, PAPER_HI, INKC, PRUSSIAN, CORAL, SEAL, FOAM, YEL, YEL_D, YEL_L, WHITE, SAFE_X0, SAFE_X1, CAP_CX,
                  RUST, RUST_D, RUST_L, OCHRE, MARS_BLUE, MARS_DUSK, IRON, WATER, SKIN, STONE, STONE_D, STONE_L)
import cys05 as EP

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
EPNAME = "cys05_pic"
DURATION = EP.DURATION

_js = json.load(open(os.path.join(OUT, "cys05_lines.json"), encoding="utf-8"))
L = {l["key"]: l["t"] for l in _js["lines"]}
DUR = {l["key"]: l["dur"] for l in _js["lines"]}
WHO = {l["key"]: l["who"] for l in _js["lines"]}
TXT = {l["key"]: l["text"] for l in _js["lines"]}
E = {k: L[k] + DUR[k] for k in L}
KEYS = sorted(L, key=lambda k: L[k])
ENV = {w: np.load(os.path.join(OUT, f"cys05_env_{w}.npy")) for w in ("N", "HERO", "LAB")}

# what the captions show (numbers as figures; the voice says them in words)
CAP = {"n3": "The air? Under 1% of Earth's pressure. Mostly carbon dioxide.",
       "n12": "You'd need 10× more air. Even the deepest crater falls short.",
       "n14": "Lab here. Rescue is coming. Signal delay: up to 22 minutes.",
       "n17": "About 15 seconds before you pass out. About 90 to get rescued.",
       "n18": "Noted. 15 seconds.",
       "n20": "A NASA test subject felt his spit boil in a vacuum chamber. Back to air in 87 seconds, he recovered.",
       "n25": "Respawning in 3... 2..."}
# how long a caption word takes to SAY (characters of the spoken words), so a figure lights up when it is said
SAYLEN = {"1%": 11, "10×": 9, "22": 10, "15": 7, "90": 6, "87": 12, "3...": 5, "2...": 3}
NOPES = {"n10": 1, "n15": 2, "n19": 3}
XH, YH, HS = 450, 840, 0.95            # her head in the close shot, and her scale
HORIZON = 1010
FEET_Y = YH + 640 * HS
SUN = (790, 380)


def env(who, t):
    e = ENV[who]
    i = int(t * FPS)
    return float(e[i]) if 0 <= i < len(e) else 0.0


def word_times(key):
    words = CAP.get(key, TXT[key]).split()
    wts = []
    for w in words:
        x = (SAYLEN.get(w, len(w)) if key in CAP else len(w)) + 1
        if w.endswith("...") or w.endswith(":"):
            x += 7
        elif w[-1] in ",.?!":
            x += 3
        wts.append(x)
    tot = sum(wts)
    t, out = L[key], []
    for w, x in zip(words, wts):
        out.append((w, t))
        t += DUR[key] * x / tot
    return out


def chunks(key, maxw=3, maxc=17):
    out, cur = [], []
    for w, t in word_times(key):
        if cur and (len(cur) >= maxw or sum(len(x) for x, _ in cur) + len(w) > maxc):
            out.append(cur)
            cur = []
        cur.append((w, t))
        if w[-1] in ",.?!:" or w.endswith("..."):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


CHUNKS = {k: chunks(k) for k in KEYS if k not in NOPES}


def WT(key, word):
    for w, t in word_times(key):
        if w.lower().strip(",.?!:").startswith(word.lower()):
            return t
    return L[key]


def twos(t):
    return math.floor(t * 12) / 12


# ---------------------------------------------------------------- shots


def shot_start(name, nth=0):
    return [a for a, n in SHOTS if n == name][nth]


def shot_at(t):
    cur = SHOTS[0]
    for s in SHOTS:
        if t >= s[0]:
            cur = s
    return cur


def shot_end(t):
    nxt = [a for a, _ in SHOTS if a > t]
    return nxt[0] if nxt else DURATION


# ---------------------------------------------------------------- NOPE machinery (as #01–#04)
def nope_words():
    e = ENV["HERO"]
    a, b = int(L["n19"] * FPS) - 1, int(E["n19"] * FPS) + 1
    seg = e[max(0, a):b]
    on, ups = False, []
    for i, v in enumerate(seg):
        if not on and v > 0.25:
            ups.append((max(0, a) + i) / FPS)
            on = True
        elif on and v < 0.08:
            on = False
    if len(ups) >= 3:
        return ups[:3]
    return [wt for _, wt in word_times("n19")]


W3 = nope_words()
T_BLAST3 = W3[-1]
T_N1 = L["n10"] + 0.15                # damage lands on / just after each word
T_N2 = L["n15"] + 0.2

SHOTS = [                                 # rule: no camera setup held longer than 8 s
    (0.0, "close"),
    (WT("n3", "Under") - 0.1, "gauge"),   # under 1% of Earth's pressure
    (WT("n3", "Mostly") - 0.05, "co2"),   # mostly carbon dioxide
    (L["n5"] - 0.1, "close"),             # "So I hold my breath?"
    (L["n6"] - 0.05, "lungs"),            # your lungs could tear
    (L["n7"] - 0.15, "close"),            # the lab: breathe out
    (L["n8"] - 0.05, "push"),             # breathe out; now it gets weird (push in on her)
    (L["n9"] - 0.05, "boil"),             # the water on your tongue starts to boil
    (L["n10"] - 0.15, "close"),           # NOPE 1
    (L["n11"] - 0.05, "boil"),            # it's not hot
    (L["n12"] - 0.05, "crater"),          # ten times more air; the deepest crater falls short
    (L["n13"] - 0.05, "duck"),            # the duck is fine
    (L["n14"] - 0.1, "signal"),           # signal delay: up to 22 minutes
    (L["n15"] - 0.15, "close"),           # NOPE 2
    (L["n16"] - 0.05, "tease"),           # how long would you last?
    (WT("n16", "And") - 0.05, "horizon"),  # and it's not the strangest part
    (L["n17"] - 0.05, "clock"),           # 15 seconds; 90 to get rescued
    (L["n18"] - 0.1, "close"),            # the lab; NOPE 3
    (max(L["n20"] - 0.05, T_BLAST3 + 1.1), "chamber"),   # the 1960s test chamber (NOPE 3's damage holds 1 s+)
    (WT("n20", "recovered") - 0.35, "relief"),   # he recovered: her, relieved
    (L["n21"] - 0.05, "sunset"),          # sunsets here are blue
    (L["n22"] - 0.05, "glow"),            # the dust lets blue light through, near the sun
    (L["n23"] - 0.05, "end"),             # the next spawns
    (L["n24"] - 0.1, "plead"),            # "Somewhere with air." tight on her
    (L["n25"] - 0.05, "end"),             # the countdown
]


def nope_at(t):
    for key, lvl in NOPES.items():
        a = L[key]
        nxt = min(L[k2] for k2 in KEYS if L[k2] > L[key]) - 0.15
        end = min(nxt, (E[key] + 0.5, E[key] + 0.6, T_BLAST3 + 1.05)[lvl - 1])
        if a - 0.05 <= t <= end:
            if lvl == 3:
                return 3, max(0.0, (t - T_BLAST3) / (end - T_BLAST3))
            return lvl, (t - a) / (end - a)
    return 0, 0.0


def nope_word(t):
    if not (L["n19"] - 0.05 <= t <= min(T_BLAST3 + 1.05, L["n20"] - 0.15)):
        return -1
    return max(i for i, w in enumerate(W3) if t >= w - 0.05) if t >= W3[0] - 0.05 else 0


def punch(t):
    for key, lvl in NOPES.items():
        a, e = L[key], E[key]
        if lvl == 3:
            i = nope_word(t)
            if i < 0:
                continue
            z = (0.10, 0.20, 0.34)[i]
            a = W3[i]
            e = W3[i + 1] - 0.02 if i < 2 else E[key]
        else:
            z = (0.07, 0.17)[lvl - 1]
        if a - 0.05 <= t <= e + 0.4:
            kin = min(1.0, (t - a + 0.05) / 0.09)
            kout = 1.0 if t <= e else max(0.0, 1 - (t - e) / 0.4)
            return 1 + z * ease_io(kin) * ease_io(kout)
    return 1.0


def shake(t):
    lvl, k = nope_at(t)
    if not lvl or shot_at(t)[1] != "close":
        return 0.0, 0.0
    if lvl == 3 and t < T_BLAST3:
        i = nope_word(t)
        amp = (5, 11)[min(1, max(0, i))] * max(0.0, 1 - (t - W3[max(0, i)]) / 0.4)
        return amp * math.sin(t * 83), amp * math.cos(t * 71)
    amp = (8, 18, 40)[lvl - 1] * max(0.0, 1 - k) ** 1.5
    return amp * math.sin(t * 83), amp * math.cos(t * 71)


# ---------------------------------------------------------------- her state in the close shots
def hero_state(t):
    st = dict(face="shock", arms="none", shiver=0.0, look=None, squash=0.0, blink=0.0, mouth_open=None, tilt=0.0,
              hop=0.0, cheeks=0.0)
    for b in (2.4, 6.0, 12.4, 21.0, 30.2, 34.4, 43.0, 47.0, 58.4, 62.4):
        if b <= t <= b + 0.12:
            st["blink"] = 1.0
    if t < 0.6:                                    # spawn: a squash bounce as she lands in the dust
        k = t / 0.6
        st["squash"] = 0.45 * math.sin(k * math.pi * 2) * (1 - k)
    elif t < L["n2"]:
        st["look"] = (10, -8)
    elif t < shot_start("gauge"):                  # "No suit. Just the hoodie." she looks down at it
        st["face"] = "worried"
        st["look"] = (0, 10)
        st["arms"] = "hug"
    elif L["n5"] - 0.2 <= t < shot_start("lungs"):   # "So I hold my breath?" then she puffs her cheeks
        st["face"] = "worried"
        st["arms"] = "hug"
        st["mouth_open"] = 0.4 + 1.1 * env("HERO", t)
        if t >= E["n5"] + 0.05:
            st["mouth_open"] = None
            st["face"] = "smug"
            st["cheeks"] = ease_io(prog(t, E["n5"], E["n5"] + 0.2))
    elif shot_start("close", 2) <= t < shot_start("push"):    # the lab says breathe out: she lets it go
        st["face"] = "deadpan"
        st["look"] = (12, -6)
        st["cheeks"] = 1 - ease_io(prog(t, L["n7"] + 0.6, L["n7"] + 0.9))
    elif shot_start("push") <= t < shot_start("boil"):
        st["face"] = "worried"
        st["look"] = (0, -4)
    elif shot_start("tease") <= t < shot_start("horizon"):
        st["face"] = "worried"
        st["look"] = (-12, -10)
    elif L["n18"] - 0.2 <= t < L["n19"]:            # the lab: fifteen seconds
        st["face"] = "deadpan"
        st["look"] = (12, -6)
    elif shot_start("relief") <= t < L["n21"]:
        st["face"] = "happy"
        st["arms"] = "hug"
    elif L["n23"] - 0.1 <= t:
        st["face"] = "worried"
        st["arms"] = "hug"
        if L["n24"] - 0.1 <= t < L["n25"]:          # "Somewhere with air."
            st["look"] = (0, -8)
            st["mouth_open"] = 0.5 + 1.1 * env("HERO", t)
    lvl, k = nope_at(t)
    if lvl and k < 0.85:
        st["face"] = "nope"
        st["mouth_open"] = min(2.0, 1.0 + 0.5 * lvl * max(0.0, 1 - k))
        if lvl == 3 and t < T_BLAST3:
            st["mouth_open"] = min(2.0, 1.0 + 0.45 * (nope_word(t) + 1) * (0.4 + env("HERO", t)))
        st["squash"] = 0.35 * lvl * math.sin(min(1.0, k * 3) * math.pi) * (1 - k)
        st["arms"] = ("hug", "up", "up")[lvl - 1]
        st["tilt"] = (0.0, -6.0, 0.0)[lvl - 1]
        st["cheeks"] = 0.0
    elif lvl == 3 or (T_BLAST3 <= t < shot_start("chamber")):
        st["face"] = "shock"
    return st


# ---------------------------------------------------------------- the plain (the close shot)
def devil_pos(t):
    """The dust devil on the horizon from frame 0: it wanders right to left; NOPE 1 flings it off to the left."""
    x = 1000 - 9 * t
    y = HORIZON + 6
    if t >= T_N1:
        k = prog(t, T_N1, T_N1 + 0.9)
        return x + 700 * ease_io(k), y + 40 * k, 1.0 + 1.2 * k, 1 - k
    return x, y, 1.0, 1.0


def plain_bg(c, t, boil, y0=HORIZON, dusk=0.0):
    tw = twos(t)
    mars_sky(c, tw, horizon=y0, sun=SUN, sun_r=46, dusk=dusk)
    # far hills
    hill = smooth_path([(-60, y0 - 70), (220, y0 - 110), (480, y0 - 80), (700, y0 - 120), (1140, y0 - 70)], closed=False)
    hill.lineTo(1140, y0 + 10)
    hill.lineTo(-60, y0 + 10)
    hill.close()
    c.drawPath(hill, fill(mixc(mixc(OCHRE, RUST_L, 0.5), MARS_DUSK[1], 0.5 * dusk)))
    c.drawPath(smooth_path([(-60, y0 - 70), (220, y0 - 110), (480, y0 - 80), (700, y0 - 120), (1140, y0 - 70)],
                           closed=False), ink(3, alpha=0.5, boil=boil))
    # the mesa on the right: NOPE 3 brings it down
    col = prog(t, T_BLAST3 + 0.05, T_BLAST3 + 0.9) if t >= T_BLAST3 else 0.0
    mesa(c, 600, 1060, y0 + 4, 300, boil=boil, collapse=col, dusk=dusk)
    # the dust devil wandering on the horizon (paid off by NOPE 1)
    dx, dy, ds, da = devil_pos(t)
    if da > 0 and dx < W + 300:
        dust_devil(c, dx, dy, 300 * ds, tw, k=1.0, alpha=0.85 * da, boil=boil, col=RUST_L, col_d=RUST_D)
    mars_ground(c, tw, y0, boil=boil, seed=2, dusk=dusk)
    # the old lander on the left: NOPE 2 snaps its dish off
    dish = prog(t, T_N2, T_N2 + 1.1) if t >= T_N2 else 0.0
    tip = ease_io(prog(t, T_N2 + 0.05, T_N2 + 0.45)) if t >= T_N2 else 0.0
    c.save()
    c.translate(240, y0 + 130)
    c.rotate(-28 * tip)
    c.translate(-240, -(y0 + 130))
    lander(c, 170, y0 + 130, s=0.66, boil=boil, dish=dish, t=tw)
    c.restore()
    if T_N2 <= t < T_N2 + 1.2:
        dust_burst(c, 200, y0 + 120, prog(t, T_N2, T_N2 + 1.2), n=18, spread=420, seed=21, up=300, size=(14, 34))


def close_shot(c, t, s=HS):
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 1.0)
    lvl, nk = nope_at(t)
    plain_bg(c, t, boil)
    if T_N1 <= t < T_N1 + 1.3:                     # NOPE 1: the dust blows off the plain behind her, in a ring
        dust_burst(c, 450, HORIZON + 40, prog(t, T_N1, T_N1 + 1.3), n=40, spread=1200, seed=3, up=380, size=(10, 26))
    if T_BLAST3 <= t < T_BLAST3 + 1.4:             # NOPE 3: dust thrown off the falling mesa
        dust_burst(c, 820, HORIZON - 120, prog(t, T_BLAST3 + 0.15, T_BLAST3 + 1.5), n=30, spread=900, seed=9,
                   up=700, size=(14, 40))
    st = hero_state(t)
    c.drawPath(oval(XH, FEET_Y - 4, 200 * s, 30 * s), fill(RUST_D, 0.5))
    draw_legs(c, XH, YH, s=s, boil=boil, t=tw, hop=st["hop"], squash=st["squash"], shiver=st["shiver"])
    draw_hero(c, XH, YH, s=s, face=st["face"], boil=boil, arms=st["arms"], t=tw, blink=st["blink"],
              squash=st["squash"], look=st["look"], shiver=st["shiver"], mouth_open=st["mouth_open"], tilt=st["tilt"])
    if st["cheeks"] > 0:                           # puffed cheeks: she is holding her breath
        q = st["cheeks"]
        for side in (-1, 1):
            cx_, cy_ = XH + side * 62 * s, YH + 40 * s
            c.drawPath(oval(cx_, cy_, 30 * s * q, 24 * s * q), fill(rgb("#EE8A78"), 0.85))
            c.drawPath(oval(cx_, cy_, 30 * s * q, 24 * s * q), ink(3, alpha=0.6 * q, boil=boil))
    # the duck sits on a stone at her feet, perfectly fine
    dkx = XH + 260
    c.drawPath(smooth_path([(dkx - 70, FEET_Y), (dkx - 50, FEET_Y - 40), (dkx + 40, FEET_Y - 46), (dkx + 76, FEET_Y)]),
               fill(rgb("#5E3426")))
    c.drawPath(smooth_path([(dkx - 70, FEET_Y), (dkx - 50, FEET_Y - 40), (dkx + 40, FEET_Y - 46), (dkx + 76, FEET_Y)]),
               ink(4, boil=boil))
    draw_duck(c, dkx, FEET_Y - 46, s=0.6, boil=None, tilt=-3 + 2 * math.sin(twos(t) * 1.3), look=0.3)
    # NOPE 1: dust explodes from her feet to both sides
    if T_N1 <= t < T_N1 + 1.3:
        k1 = prog(t, T_N1, T_N1 + 1.3)
        dust_burst(c, XH - 330, FEET_Y - 30, k1, n=14, spread=500, seed=7, up=260, size=(16, 40))
        dust_burst(c, XH + 330, FEET_Y - 30, k1, n=14, spread=500, seed=8, up=260, size=(16, 40))
    # NOPE 3: the dust storm rolls in from both sides, in front
    if T_BLAST3 <= t < T_BLAST3 + 1.3:
        k3 = prog(t, T_BLAST3, T_BLAST3 + 1.3)
        dust_burst(c, XH - 360, FEET_Y - 40, k3, n=20, spread=700, seed=12, up=380, size=(20, 50))
        dust_burst(c, XH + 360, FEET_Y - 40, k3, n=20, spread=700, seed=13, up=380, size=(20, 50))
    if T_BLAST3 <= t < shot_start("chamber"):
        dust_wall(c, tw, prog(t, T_BLAST3, T_BLAST3 + 0.7), HORIZON + 200, boil=boil)
    # NOPE rings: only in front of her
    yw = FEET_Y - 10
    if lvl == 3 and t < T_BLAST3:
        i = nope_word(t)
        kk = min(1.0, (t - W3[max(0, i)]) / 0.6)
        ring(c, XH, yw, 200 + 260 * (i + 1) * kk, (1 - kk) * 0.9, 7)
    elif lvl:
        for j in range(lvl):
            rr = 200 + (500 + 400 * lvl) * min(1.0, nk * (1.4 - 0.2 * j))
            ring(c, XH, yw, rr, (1 - nk) * 0.9, 6 + 3 * lvl)


def ring(c, x, y, r, alpha, width=8):
    p = skia.Path()
    p.addArc(skia.Rect.MakeLTRB(x - r, y - r * 0.18, x + r, y + r * 0.18), 8, 164)   # only in front of her
    c.drawPath(p, ink(width, col=WHITE, alpha=alpha))


# ---------------------------------------------------------------- paper backgrounds for the inserts
def paper_bg(c, col=None, seed=11):
    bg = rrect(-10, -10, W + 20, H + 20, 0)
    c.drawPath(bg, fill(col or rgb("#EADFC4")))
    woodgrain(c, bg, alpha=0.18, seed=seed, fx=0.004, fy=0.08)
    mottle(c, bg, rgb("#CDBE9C"), alpha=0.2, scale=0.01, seed=seed)


def seigaiha(c, t, base=None, line=None, r=64, alpha=0.2):
    """Seigaiha, the woodblock wave-scale pattern, drifting slowly (as #01)."""
    base = base or rgb("#1B3A5E")
    line = line or FOAM
    c.drawRect(skia.Rect.MakeWH(W, H), fill(base))
    drift = (twos(t) * 12) % (2 * r)
    j = 0
    y = -r
    while y < H + r:
        off = (r if j % 2 else 0) - drift
        x = -2 * r + off
        while x < W + 2 * r:
            c.drawCircle(x, y, r, fill(base))
            for rr in (r, r * 0.75, r * 0.5, r * 0.25):
                c.drawCircle(x, y, rr, ink(3, col=line, alpha=alpha))
            x += 2 * r
        y += r * 0.5
        j += 1


def stamp(c, x, y, s, size=90, k=1.0, rot=-5, col=None, txtcol=None, font_name="display", pop=0.6):
    col = col or SEAL
    sc = 1 + pop - pop * ease_io(k) if k < 1 else 1.0
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(sc, sc)
    f = font(font_name, size)
    w = f.measureText(s)
    pad = size * 0.35
    box = rrect(-w / 2 - pad, -size * 0.85, w + 2 * pad, size * 1.25, 12)
    c.drawPath(box, fill(col, min(1, k * 2)))
    mottle(c, box, col, alpha=0.3, scale=0.06)
    c.drawPath(rrect(-w / 2 - pad + 8, -size * 0.85 + 8, w + 2 * pad - 16, size * 1.25 - 16, 8), ink(3, col=FOAM, alpha=min(1, k * 2)))
    text(c, s, 0, size * 0.18, f, txtcol or FOAM, align="center", alpha=min(1, k * 2))
    c.restore()


def label(c, s, x, y, size=40, col=None, alpha=1.0, align="center", stroke=8):
    text(c, s, x, y, font("mono", size), col or INKC, align=align, alpha=alpha, stroke=stroke, stroke_col=PAPER_HI)


# ---------------------------------------------------------------- gauge: Earth's air column vs Mars's
def air_dots(c, x0, y0, w, h, n, col, seed, t, alpha=1.0):
    rng = np.random.default_rng(seed)
    for j in range(n):
        x = x0 + rng.uniform(0.05, 0.95) * w + 4 * math.sin(t * 3 + j)
        y = y0 + rng.uniform(0.03, 0.97) * h + 4 * math.cos(t * 2.5 + j * 1.3)
        c.drawCircle(x, y, rng.uniform(6, 10), fill(col, alpha))


def gauge_shot(c, t):
    """Two tall glass columns of air on cream paper. EARTH: packed with blue dots, 101 kPa. MARS: starts full, then
    drains to a sliver as 'under one percent' is said; the readout counts down to 0.6 kPa."""
    a = shot_start("gauge")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    tw = twos(t)
    paper_bg(c, seed=11)
    k_in = ease_io(prog(t, a, a + 0.3))
    t_drain0, t_drain1 = WT("n3", "1%") - 0.15, WT("n3", "pressure") + 0.2
    kd = ease_io(prog(t, t_drain0, t_drain1))
    top, bot = 600, 1130
    hh = bot - top
    for j, (name, x, col) in enumerate((("EARTH", 270, PRUSSIAN), ("MARS", 630, RUST))):
        yy = (1 - k_in) * 300
        c.save()
        c.translate(0, yy)
        tube = rrect(x - 120, top, 240, hh, 30)
        c.drawPath(rrect(x - 108, top + 14, 240, hh, 30), fill(INKC, 0.2))
        c.drawPath(tube, fill(PAPER_HI))
        frac = 1.0 if j == 0 else (1 - kd) + 0.006 * kd
        lev = bot - hh * frac
        c.save()
        c.clipPath(tube, doAntiAlias=True)
        c.drawRect(skia.Rect.MakeLTRB(x - 120, lev, x + 120, bot), fill(mixc(col, PAPER_HI, 0.55)))
        n = 70 if j == 0 else max(1, int(70 * frac))
        air_dots(c, x - 120, lev, 240, bot - lev, n, col, 5 + j, tw)
        if j == 1 and kd > 0.9:
            c.drawRect(skia.Rect.MakeLTRB(x - 120, bot - 14, x + 120, bot), fill(SEAL))
        c.restore()
        c.drawPath(tube, ink(5, boil=boil))
        for k in range(1, 10):                         # the scale
            c.drawLine(x + 120, top + hh * k / 10, x + 140, top + hh * k / 10, ink(3, alpha=0.6))
        # the planet under its column
        pc = (x, top - 120)
        c.drawPath(oval(pc[0], pc[1], 80, 80), fill(rgb("#5D8FB8") if j == 0 else RUST))
        if j == 0:
            for dx, dy, r in ((-30, -20, 30), (24, 22, 26), (40, -40, 14)):
                c.drawPath(oval(pc[0] + dx, pc[1] + dy, r, r * 0.7), fill(rgb("#7DAA6A")))
        else:
            for dx, dy, r in ((-26, -18, 14), (30, 20, 11), (4, 40, 9)):
                c.drawPath(oval(pc[0] + dx, pc[1] + dy, r, r), fill(RUST_D))
        c.drawPath(oval(pc[0], pc[1], 80, 80), ink(5, boil=boil))
        label(c, name, x, top - 230, size=46)
        c.restore()
    # the readouts
    v = 101.3 - (101.3 - 0.6) * kd
    label(c, "101 kPa", 270, 1340, size=48, col=PRUSSIAN, alpha=k_in)
    label(c, "0.6 kPa", 630, 1340, size=48, col=SEAL, alpha=k_in)
    if kd > 0.95:
        stamp(c, 630, 860, "< 1 %", size=110, k=prog(t, t_drain1 - 0.1, t_drain1 + 0.15), rot=-6)


# ---------------------------------------------------------------- co2: what there is, is carbon dioxide
def co2_shot(c, t):
    """100 dots: 95 turn coral (CO2) in a wave; 2.7 grey-blue (nitrogen), 1.6 cream (argon); the oxygen is a speck
    circled in ink: 0.13 %."""
    a = shot_start("co2")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    seigaiha(c, t, base=rgb("#3A2A2A"), line=RUST_L, alpha=0.16)
    z = 1.0 + 0.05 * prog(t, a, shot_end(a))
    c.save()
    c.translate(450, 860)
    c.scale(z, z)
    c.translate(-450, -860)
    card = rrect(150, 390, 600, 720, 26)
    c.drawPath(rrect(162, 406, 600, 720, 26), fill(INKC, 0.4))
    c.drawPath(card, fill(PAPER_HI))
    mottle(c, card, PAPER, alpha=0.2, scale=0.02)
    c.drawPath(card, ink(5, boil=boil))
    step = 52
    x0, y0 = 450 - 4.5 * step, 460
    for i in range(100):
        r_, c_ = divmod(i, 10)
        kw = ease_io(prog(t, a + 0.1 + 0.006 * i, a + 0.3 + 0.006 * i))
        col = mixc(rgb("#C9BFA9"), CORAL if i < 95 else (rgb("#7E9AB0") if i < 98 else PAPER), kw)
        c.drawCircle(x0 + c_ * step, y0 + r_ * step, 19, fill(col))
        c.drawCircle(x0 + c_ * step, y0 + r_ * step, 19, ink(2.5, alpha=0.7))
    kt = ease_io(prog(t, a + 0.4, a + 0.7))
    text(c, "95% CO2", 450, 1060, font("display", 92), SEAL, align="center", alpha=kt, stroke=10, stroke_col=PAPER_HI)
    c.restore()
    ko = ease_io(prog(t, a + 0.9, a + 1.2))
    if ko > 0:                                         # the oxygen: one speck
        ox, oy = 640, 1340
        c.drawCircle(ox, oy, 3, fill(INKC, ko))
        c.drawCircle(ox, oy, 40, ink(4, col=FOAM, alpha=ko))
        label(c, "OXYGEN 0.13%", ox - 70, oy + 14, size=40, col=FOAM, alpha=ko, align="right", stroke=0)


# ---------------------------------------------------------------- lungs: don't hold it
def lungs_shot(c, t):
    """Her outline on paper (bun, hood), two balloon lungs inside: they swell against the outline, the ink strains,
    a warning tag; no injury shown."""
    a = shot_start("lungs")
    fi = int(t * FPS)
    boil = (fi // 2, 0.9)
    paper_bg(c, rgb("#E9DDBF"), seed=13)
    k = ease_io(prog(t, a + 0.1, WT("n6", "tear") + 0.2))
    wob = 3 * math.sin(t * 40) * k
    cx, cy = 450, 900
    # her silhouette as a dashed blueprint outline
    sil = smooth_path([(cx - 260, cy + 460), (cx - 250, cy + 60), (cx - 150, cy - 40), (cx - 100, cy - 160),
                       (cx - 130, cy - 300), (cx, cy - 400), (cx + 130, cy - 300), (cx + 100, cy - 160),
                       (cx + 150, cy - 40), (cx + 250, cy + 60), (cx + 260, cy + 460)], closed=False)
    pd = ink(6, col=PRUSSIAN, alpha=0.8, boil=boil)
    pd.setPathEffect(skia.DashPathEffect.Make([22, 12], 0))
    c.drawPath(sil, pd)
    c.drawPath(oval(cx + 10, cy - 450, 60, 50), ink(6, col=PRUSSIAN, alpha=0.8))
    for side in (-1, 1):
        r = 95 + 70 * k
        lx = cx + side * (95 + 30 * k) + wob * side
        ly = cy + 140
        lung = smooth_path([(lx, ly - r * 1.3), (lx + side * r * 0.9, ly - r * 0.6), (lx + side * r, ly + r * 0.5),
                            (lx + side * r * 0.4, ly + r * 1.1), (lx - side * r * 0.5, ly + r * 0.9),
                            (lx - side * r * 0.45, ly - r * 0.4)])
        c.drawPath(lung, fill(mixc(CORAL, SEAL, k)))
        mottle(c, lung, SEAL, alpha=0.25, scale=0.03, seed=3 + side)
        c.drawPath(oval(lx + side * r * 0.3, ly - r * 0.5, r * 0.22, r * 0.14), fill(WHITE, 0.6))
        c.drawPath(lung, ink(5, boil=boil))
    c.drawLine(cx, cy - 160, cx, cy + 20, ink(14, col=SEAL))      # windpipe
    for j in range(6):                                 # pressure arrows pushing out
        an = j * math.pi / 3 + 0.5
        r0 = 300 + 60 * k
        x1, y1 = cx + math.cos(an) * r0, cy + 160 + math.sin(an) * r0 * 0.9
        x2, y2 = cx + math.cos(an) * (r0 + 70 * k), cy + 160 + math.sin(an) * (r0 + 70 * k) * 0.9
        if k > 0.2:
            c.drawLine(x1, y1, x2, y2, ink(8, col=INKC, alpha=k))
    if t >= WT("n6", "tear") - 0.05:
        stamp(c, CAP_CX, 470, "DON'T HOLD IT", size=84, k=prog(t, WT("n6", "tear") - 0.05, WT("n6", "tear") + 0.2), rot=-5)


# ---------------------------------------------------------------- boil: 37 °C and boiling
def boil_shot(c, t):
    """A plain glass of water on a red rock under the butterscotch sky, a thermometer at body temperature: it
    boils hard. Second time (it's not hot): the stamp NOT HOT and the air around it, a few sparse dots."""
    a = shot_at(t)[0]
    second = a > L["n10"]
    fi = int(t * FPS)
    boil = (fi // 2, 0.9)
    tw = twos(t)
    z = 1.0 + 0.06 * prog(t, a, shot_end(a)) + (0.12 if second else 0.0)
    c.save()
    c.translate(450, 900)
    c.scale(z, z)
    c.translate(-450, -900)
    mars_sky(c, tw, horizon=1150, sun=(760, 420), sun_r=46)
    mars_ground(c, tw, 1150, boil=boil, seed=6, rocks=False)
    rock = smooth_path([(160, 1200), (240, 1090), (660, 1080), (760, 1210), (700, 1280), (200, 1280)])
    c.drawPath(rock, fill(rgb("#6E3A28")))
    c.drawPath(rock, ink(4, boil=boil))
    gx, gy, gw, gh = 380, 760, 220, 330                # the glass
    glass = skia.Path()
    glass.addPoly([skia.Point(gx - gw / 2, gy), skia.Point(gx + gw / 2, gy), skia.Point(gx + gw / 2 - 24, gy + gh),
                   skia.Point(gx - gw / 2 + 24, gy + gh)], True)
    c.drawPath(glass, fill(PAPER_HI, 0.55))
    water = skia.Path()
    wl = gy + 80 + 6 * math.sin(tw * 9)
    water.addPoly([skia.Point(gx - gw / 2 + 6, wl), skia.Point(gx + gw / 2 - 6, wl), skia.Point(gx + gw / 2 - 26, gy + gh - 6),
                   skia.Point(gx - gw / 2 + 28, gy + gh - 6)], True)
    c.drawPath(water, fill(WATER, 0.9))
    kb = ease_io(prog(t, WT("n9", "boil") - 0.4, WT("n9", "boil"))) if not second else 1.0
    rng = np.random.default_rng(4)
    for j in range(int(26 * kb) + 2):                  # bubbles rising, bursting at the top
        ph = (t * rng.uniform(0.9, 1.6) + rng.uniform(0, 1)) % 1.0
        bx = gx + rng.uniform(-gw / 2 + 40, gw / 2 - 40) + 6 * math.sin(t * 7 + j)
        by = gy + gh - 20 - (gy + gh - 20 - wl) * ph
        c.drawCircle(bx, by, 6 + 10 * ph * kb, ink(3, col=WHITE, alpha=0.9))
    for j in range(int(8 * kb)):                       # spray leaping above the water
        ph = (t * 2.2 + j / 8) % 1.0
        sx = gx - 60 + j * 18
        sy = wl - 120 * math.sin(ph * math.pi)
        c.drawCircle(sx, sy, 7 * (1 - ph) + 2, fill(WATER, 0.9 * (1 - ph)))
    c.drawPath(glass, ink(5, boil=boil))
    thermometer(c, 640, 640, 380, 0.42, alpha=1.0, boil=boil, col=SEAL)
    label(c, "37 °C", 640, 610, size=50, col=SEAL)
    if not second:
        label(c, "BODY TEMP", 640, 556, size=36)
    if second:                                         # thin air: a few dots drifting around the glass
        air_dots(c, 120, 420, 680, 700, 9, RUST_D, 8, tw, alpha=0.7)
    c.restore()
    if second:
        tn = WT("n11", "hot")
        if t >= tn - 0.25:
            stamp(c, CAP_CX, 420, "NOT HOT", size=100, k=prog(t, tn - 0.25, tn), rot=-6)
    elif t >= WT("n9", "boil") - 0.1:
        stamp(c, CAP_CX, 420, "BOILING", size=100, k=prog(t, WT("n9", "boil") - 0.1, WT("n9", "boil") + 0.15), rot=-6)


# ---------------------------------------------------------------- crater: the deepest basin falls short
P_MAX = 7.0                                            # kPa at the top of the bar
P_LINE = 6.3                                           # the Armstrong limit: water boils at body temperature below it


def crater_shot(c, t):
    """A cutaway of the ground: the plain at 0.6 kPa, the great basin dropping away. She slides down into it; the
    pressure bar on the left fills from 0.6 toward the boiling line (6.3) and stops at 1.16: FALLS SHORT."""
    a = shot_start("crater")
    b = shot_end(a)
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    tw = twos(t)
    mars_sky(c, tw, horizon=1500, sun=(800, 340), sun_r=40)
    # the cross-section
    surf = 700
    prof = [(-40, surf), (330, surf), (420, surf + 120), (520, surf + 420), (640, surf + 560), (760, surf + 600),
            (900, surf + 580), (1000, surf + 450), (1060, surf + 300), (1120, surf + 240)]
    ground = smooth_path(prof, closed=False)
    ground.lineTo(1120, H + 20)
    ground.lineTo(-40, H + 20)
    ground.close()
    c.drawPath(ground, fill(RUST))
    for j in range(8):                                 # strata
        yy = surf + 140 + j * 130
        c.drawLine(-40, yy + 20 * math.sin(j), 1120, yy - 10, ink(3, col=RUST_D, alpha=0.6))
    mottle(c, ground, RUST_D, alpha=0.3, scale=0.01, seed=5)
    c.drawPath(smooth_path(prof, closed=False), ink(5, boil=boil))
    label(c, "DEEPEST BASIN", 760, surf + 700, size=40, col=FOAM, stroke=0)
    # her, small, sliding down the slope
    kd = ease_io(prog(t, WT("n12", "Even") - 0.2, WT("n12", "falls") - 0.1))
    path = smooth_path(prof[1:7], closed=False)
    meas = skia.PathMeasure(path, False)
    pos, tan = meas.getPosTan(meas.getLength() * kd)
    hx, hy = pos.x(), pos.y()
    draw_legs(c, hx, hy - 100, s=0.16, boil=boil, t=tw)
    draw_hero(c, hx, hy - 100, s=0.16, face="worried" if kd < 1 else "shock", boil=boil, arms="up", t=tw)
    # the pressure bar: the target line is the boiling line
    bx, by0, by1 = 170, 380, 1110
    bar = rrect(bx - 44, by0, 88, by1 - by0, 44)
    c.drawPath(rrect(bx - 34, by0 + 12, 88, by1 - by0, 44), fill(INKC, 0.3))
    c.drawPath(bar, fill(PAPER_HI))
    p = 0.6 + (1.16 - 0.6) * kd
    lev = by1 - (by1 - by0) * p / P_MAX
    c.save()
    c.clipPath(bar, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeLTRB(bx - 44, lev, bx + 44, by1), fill(SEAL))
    c.restore()
    c.drawPath(bar, ink(5, boil=boil))
    yl = by1 - (by1 - by0) * P_LINE / P_MAX
    kl = ease_io(prog(t, WT("n12", "10×") - 0.15, WT("n12", "10×") + 0.2))
    pl = ink(7, col=PRUSSIAN, alpha=max(0.35, kl))
    pl.setPathEffect(skia.DashPathEffect.Make([18, 10], 0))
    c.drawLine(bx - 70, yl, bx + 300, yl, pl)
    label(c, "BOILING STOPS", bx + 70, yl - 26, size=42, col=PRUSSIAN, align="left", alpha=max(0.5, kl))
    label(c, "6.3 kPa", bx + 70, yl + 52, size=42, col=PRUSSIAN, align="left", alpha=max(0.5, kl))
    if kl > 0:
        text(c, "×10", bx + 64, 830, font("display", 90), PRUSSIAN, align="left", alpha=kl, stroke=10,
             stroke_col=PAPER_HI)
    label(c, f"{p:.1f} kPa" if kd < 1 else "1.16 kPa", bx + 70, lev - 10, size=46, col=SEAL, align="left")
    tf = WT("n12", "falls")
    if t >= tf - 0.1:
        stamp(c, 560, 600, "FALLS SHORT", size=72, k=prog(t, tf - 0.1, tf + 0.15), rot=-5)


# ---------------------------------------------------------------- duck: it doesn't breathe
def duck_shot(c, t):
    """The duck on its stone on the red plain, perfectly calm, the dust devil going by behind; a tag: NO LUNGS."""
    a = shot_start("duck")
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 0.9)
    z = 1.0 + 0.06 * prog(t, a, shot_end(a))
    c.save()
    c.translate(450, 980)
    c.scale(z, z)
    c.translate(-450, -980)
    mars_sky(c, tw, horizon=1060, sun=(300, 420), sun_r=46)
    dust_devil(c, 860 - 60 * (t - a), 1066, 360, tw, k=1.0, alpha=0.8, boil=boil, col=RUST_L, col_d=RUST_D)
    mars_ground(c, tw, 1060, boil=boil, seed=9)
    st = smooth_path([(170, 1330), (250, 1160), (650, 1140), (760, 1330)])
    c.drawPath(st, fill(rgb("#5E3426")))
    c.drawPath(oval(380, 1180, 160, 22), fill(RUST_L, 0.4))
    c.drawPath(st, ink(5, boil=boil))
    draw_duck(c, 450, 1150, s=2.6, boil=boil, tilt=-3 + 2 * math.sin(tw * 1.1), look=0.4)
    c.restore()
    tn = WT("n13", "breathe")
    if t >= tn - 0.3:
        stamp(c, CAP_CX, 520, "NO LUNGS", size=96, k=prog(t, tn - 0.3, tn - 0.05), rot=6, col=PRUSSIAN)


# ---------------------------------------------------------------- signal: up to 22 minutes
def signal_shot(c, t):
    """Earth (top left) and Mars (bottom right) in the dark; a dashed radio path; a pulse crawls along it while a
    big timer runs; at 'twenty-two minutes' the timer slams to UP TO 22 MIN."""
    a = shot_start("signal")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    tw = twos(t)
    c.drawRect(skia.Rect.MakeWH(W, H), fill(rgb("#121A2E")))
    rng = np.random.default_rng(31)
    for _ in range(110):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        k = 0.5 + 0.5 * math.sin(tw * rng.uniform(1.5, 4) + x)
        c.drawCircle(x, y, rng.uniform(1.4, 3.4), fill(FOAM, 0.3 + 0.5 * k))
    ex, ey, mx, my = 250, 560, 690, 1180
    c.drawPath(oval(ex, ey, 110, 110), fill(rgb("#5D8FB8")))
    for dx, dy, r in ((-36, -24, 36), (28, 26, 30), (46, -46, 16)):
        c.drawPath(oval(ex + dx, ey + dy, r, r * 0.7), fill(rgb("#7DAA6A")))
    c.drawPath(oval(ex, ey, 110, 110), ink(5, boil=boil))
    c.drawPath(oval(mx, my, 80, 80), fill(RUST))
    for dx, dy, r in ((-24, -16, 14), (26, 18, 10), (2, 36, 8)):
        c.drawPath(oval(mx + dx, my + dy, r, r), fill(RUST_D))
    c.drawPath(oval(mx, my, 80, 80), ink(5, boil=boil))
    label(c, "EARTH", ex, ey - 140, size=40, col=FOAM, stroke=0)
    label(c, "MARS", mx, my + 136, size=40, col=FOAM, stroke=0)
    path = smooth_path([(ex + 80, ey + 80), (520, 820), (mx - 60, my - 60)], closed=False)
    pd = ink(5, col=YEL_L, alpha=0.7)
    pd.setPathEffect(skia.DashPathEffect.Make([16, 14], -tw * 40))
    c.drawPath(path, pd)
    meas = skia.PathMeasure(path, False)
    kp = 0.04 + 0.08 * prog(t, a, shot_end(a))            # the pulse barely moves
    pos, _ = meas.getPosTan(meas.getLength() * kp)
    for r in (34, 24, 14):
        c.drawCircle(pos.x(), pos.y(), r, fill(YEL_L, 0.25 if r > 14 else 1.0))
    t22 = WT("n14", "22")
    if t < t22 - 0.05:
        mins = 22 * ease_io(prog(t, a + 0.3, t22 - 0.1)) ** 1.6
        s = f"{int(mins):02d}:{int((mins % 1) * 60):02d}"
        text(c, s, 450, 990, font("display", 130), FOAM, align="center", stroke=14)
        label(c, "SIGNAL DELAY", 450, 860, size=40, col=YEL_L, stroke=0)
    else:
        stamp(c, CAP_CX, 960, "UP TO 22 MIN", size=96, k=prog(t, t22 - 0.05, t22 + 0.2), rot=-4)


# ---------------------------------------------------------------- horizon: the strangest part
def horizon_shot(c, t):
    """Wide and low: the plain to the horizon, the small sun sinking, the sky starting to turn: a hint of blue."""
    a = shot_start("horizon")
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 0.9)
    k = prog(t, a, shot_end(a))
    z = 1.0 + 0.08 * k
    c.save()
    c.translate(450, 1100)
    c.scale(z, z)
    c.translate(-450, -1100)
    mars_sky(c, tw, horizon=1240, sun=(450, 1080 + 60 * k), sun_r=40, dusk=0.25 + 0.2 * k, blue=0.15 + 0.15 * k)
    mesa(c, 620, 1100, 1244, 180, boil=boil, dusk=0.4)
    mars_ground(c, tw, 1240, boil=boil, seed=12, dusk=0.4)
    c.restore()
    text(c, "?", 450, 640, font("display", 220), FOAM, align="center", alpha=ease_io(prog(t, a + 0.2, a + 0.5)), stroke=16)


# ---------------------------------------------------------------- clock: the answer
CLOCK_C = (450, 660, 250)
GOLD, GOLD_D = rgb("#C9973E"), rgb("#8E6524")


def clock_shot(c, t):
    """A big stopwatch on the seigaiha. Inner ring: 0 → 15 s as 'fifteen seconds' is said: PASS OUT. Outer ring:
    0 → 90 s as 'ninety': RESCUE WINDOW."""
    a = shot_start("clock")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    seigaiha(c, t, base=rgb("#3A2A2A"), line=RUST_L, alpha=0.18)
    cx, cy, R = CLOCK_C
    t15, t90 = WT("n17", "15"), WT("n17", "90")
    k_in = ease_io(prog(t, a, a + 0.3))
    pop = max(0.0, 1 - (t - t15) / 0.25) if t >= t15 else 0.0
    z = (1.25 - 0.25 * k_in) * (1 + 0.05 * pop)
    c.save()
    c.translate(cx, cy)
    c.scale(z, z)
    c.rotate(2 * math.sin(t * 1.3))
    c.translate(-cx, -cy)
    c.drawCircle(cx + 16, cy + 22, R + 40, fill(INKC, 0.4))
    c.drawCircle(cx, cy - R - 84, 34, ink(20, boil=boil))
    c.drawCircle(cx, cy - R - 84, 34, ink(13, col=GOLD))
    crown = rrect(cx - 34, cy - R - 64, 68, 50, 12)
    c.drawPath(crown, fill(GOLD))
    c.drawPath(crown, ink(5, boil=boil))
    rim = oval(cx, cy, R + 40, R + 40)
    c.drawPath(rim, fill(GOLD))
    mottle(c, rim, GOLD_D, alpha=0.35, scale=0.03, seed=4)
    c.drawPath(rim, ink(6, boil=boil))
    c.drawCircle(cx, cy, R + 12, fill(GOLD_D))
    face = oval(cx, cy, R, R)
    c.drawPath(face, fill(PAPER_HI))
    mottle(c, face, PAPER, alpha=0.18, scale=0.02, seed=6)
    c.drawPath(face, ink(4))
    for i in range(60):
        ang = math.radians(-90 + 6 * i)
        r0 = R * (0.88 if i % 5 else 0.82)
        c.drawLine(cx + math.cos(ang) * r0, cy + math.sin(ang) * r0, cx + math.cos(ang) * R * 0.97,
                   cy + math.sin(ang) * R * 0.97, ink(3 if i % 5 else 5))
    # the 90 s ring (outer, one turn = 120 s) and the 15 s ring (inner, one turn = 60 s)
    k90 = ease_io(prog(t, t90 - 0.15, t90 + 0.5))
    if k90 > 0:
        rr = R * 0.74
        p = skia.Path()
        p.addArc(skia.Rect.MakeLTRB(cx - rr, cy - rr, cx + rr, cy + rr), -90, 270 * k90)
        c.drawPath(p, ink(30, col=PRUSSIAN, alpha=0.9))
    k15 = ease_io(prog(t, t15 - 0.2, t15 + 0.3))
    rr = R * 0.56
    p = skia.Path()
    p.addArc(skia.Rect.MakeLTRB(cx - rr, cy - rr, cx + rr, cy + rr), -90, max(0.5, 45 * k15))
    c.drawPath(p, ink(36, col=SEAL))
    ang = math.radians(-90 + 90 * k15 + (360 * 1.5 - 90) * k90 * 0)
    hand = math.radians(-90 + 3 * (15 * k15 + 75 * k90))
    c.drawLine(cx, cy, cx + math.cos(hand) * R * 0.8, cy + math.sin(hand) * R * 0.8, ink(10, col=INKC))
    c.drawCircle(cx, cy, 18, fill(INKC))
    c.drawCircle(cx, cy, 7, fill(GOLD))
    del ang
    c.restore()
    if t >= t15 - 0.1:
        text(c, "~15 S  PASS OUT", cx, 1060, font("display", 64), SEAL, align="center", stroke=12, stroke_col=PAPER_HI)
    if k90 > 0:
        text(c, "~90 S  RESCUE", cx, 1140, font("display", 64), PRUSSIAN, align="center", alpha=k90, stroke=12,
             stroke_col=PAPER_HI)


# ---------------------------------------------------------------- chamber: the 1960s test
def chamber_shot(c, t):
    """A riveted steel test chamber with a round porthole and a pressure dial (no person drawn: only a warm glow in
    the porthole). The needle drops; bubbles in the porthole (the spit boiling); at 'recovered' the air rushes back,
    the light turns warm, the stamp HE RECOVERED."""
    a = shot_start("chamber")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    tw = twos(t)
    paper_bg(c, rgb("#D9D2C2"), seed=17)
    z = 1.0 + 0.08 * prog(t, a, shot_end(a))
    c.save()
    c.translate(450, 860)
    c.scale(z, z)
    c.translate(-450, -860)
    for yy in range(300, 1500, 80):                    # the lab wall: tiles
        c.drawLine(0, yy, W, yy, ink(2, alpha=0.25))
    ch = rrect(130, 520, 640, 760, 260)
    c.drawPath(rrect(146, 540, 640, 760, 260), fill(INKC, 0.3))
    c.drawPath(ch, fill(STONE))
    mottle(c, ch, STONE_D, alpha=0.35, scale=0.02, seed=3)
    for j in range(10):                                # rivets
        an = j * math.pi / 5
        c.drawCircle(450 + 290 * math.cos(an), 900 + 350 * math.sin(an), 9, fill(STONE_D))
    c.drawPath(ch, ink(6, boil=boil))
    tr = WT("n20", "87")
    back = ease_io(prog(t, tr - 0.3, tr + 0.4))
    tsp = WT("n20", "spit")
    pr = rrect(310, 720, 280, 280, 140)
    c.drawPath(pr, fill(mixc(rgb("#3B4A63"), rgb("#F2C27A"), back)))
    for j in range(int(14 * prog(t, tsp - 0.2, tsp + 0.3) * (1 - back))):     # bubbles in the porthole
        ph = (t * 1.3 + j / 14) % 1.0
        bx = 360 + (j * 37) % 180
        by = 960 - 220 * ph
        c.drawCircle(bx, by, 8 + 12 * ph, ink(4, col=WHITE, alpha=0.9))
    c.drawPath(pr, ink(14, col=STONE_D))
    c.drawPath(pr, ink(5, boil=boil))
    # the dial: the needle falls toward VACUUM, then swings back
    dx, dy, dr = 450, 1130, 90
    c.drawPath(oval(dx, dy, dr, dr), fill(PAPER_HI))
    c.drawPath(oval(dx, dy, dr, dr), ink(5, boil=boil))
    fall = ease_io(prog(t, a + 0.2, a + 1.4))
    an = math.radians(-160 + 140 * (1 - fall) + 140 * back)
    c.drawLine(dx, dy, dx + math.cos(an) * dr * 0.8, dy + math.sin(an) * dr * 0.8, ink(8, col=SEAL))
    c.drawCircle(dx, dy, 10, fill(INKC))
    c.restore()
    label(c, "1960s · TEST CHAMBER", CAP_CX, 400, size=44, alpha=ease_io(prog(t, a + 0.1, a + 0.4)))
    t87 = WT("n20", "87")
    if t >= t87 - 0.3:
        k87 = ease_io(prog(t, t87 - 0.3, t87 + 0.3))
        text(c, f"AIR BACK: {int(87 * k87)} S", CAP_CX, 1420, font("display", 72), rgb("#3F7A4E"), align="center", stroke=12,
             stroke_col=PAPER_HI)



# ---------------------------------------------------------------- sunset: the blue sunset (new scene)
def sunset_shot(c, t, glow=False):
    """Mars at sunset (new scene): a butterscotch sky going dusky, a small white sun low over the plain wrapped in a
    big cold-blue halo; she sits on a rock in the foreground with the duck, watching. glow=True: a split screen,
    an Earth sunset (orange around the sun) over a Mars sunset (blue around the sun)."""
    a = shot_at(t)[0]
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 0.9)
    k = prog(t, a, shot_end(a))
    if not glow:
        kb = ease_io(prog(t, a + 0.1, WT("n21", "blue") + 0.1))
        z = 1.0 + 0.05 * k
        c.save()
        c.translate(450, 900)
        c.scale(z, z)
        c.translate(-450, -900)
        mars_sky(c, tw, horizon=1080, sun=(600, 760), sun_r=48, dusk=0.35, blue=0.3 + 0.7 * kb)
        mesa(c, 760, 1160, 1084, 160, boil=boil, dusk=0.6)
        mars_ground(c, tw, 1080, boil=boil, seed=14, dusk=0.6)
        rk = smooth_path([(60, 1500), (120, 1330), (560, 1310), (660, 1500)])
        c.drawPath(rk, fill(rgb("#3A2620")))
        c.drawPath(rk, ink(4, boil=boil))
        draw_legs(c, 300, 930, s=0.6, boil=boil, t=tw)
        draw_hero(c, 300, 930, s=0.6, face="happy" if kb > 0.6 else "shock", boil=boil, arms="hug", t=tw, look=(12, -8))
        draw_duck(c, 520, 1310, s=1.0, boil=None, tilt=-3, look=0.6)
        c.restore()
        if kb > 0.8:
            stamp(c, CAP_CX, 450, "BLUE", size=120, k=prog(t, WT("n21", "blue") - 0.05, WT("n21", "blue") + 0.2), rot=-6,
                  col=rgb("#3C6E99"))
        return
    # split screen: Earth above, Mars below
    c.drawRect(skia.Rect.MakeWH(W, H), fill(rgb("#1E1A26")))
    for j, (y0, y1) in enumerate(((240, 830), (850, 1460))):
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(0, y0, W, y1))
        c.translate(0, y0)
        hz = (y1 - y0) * 0.78
        sx, sy = 450, 230
        if j == 0:                                     # Earth: orange sky, orange glow
            p = skia.Paint()
            p.setShader(skia.GradientShader.MakeLinear([(0, 0), (0, hz)], [rgb("#3E4E7A"), rgb("#E07A4A"), rgb("#F6C26B")],
                                                       [0.0, 0.65, 1.0]))
            c.drawRect(skia.Rect.MakeWH(W, hz + 4), p)
            g = skia.Paint(AntiAlias=True)
            g.setShader(skia.GradientShader.MakeRadial((sx, sy), 260, [skia.Color4f(1, 0.6, 0.25, 0.8), skia.Color4f(1, 0.5, 0.2, 0)]))
            c.drawCircle(sx, sy, 260, g)
            c.drawPath(oval(sx, sy, 60, 60), fill(rgb("#FFD27A")))
            c.drawRect(skia.Rect.MakeLTRB(-10, hz, W + 10, y1 - y0 + 10), fill(rgb("#2E4A6E")))
            for q in range(5):                         # the sea, with the sun's path on it
                yy = hz + 20 + q * 22
                c.drawLine(sx - 120 + q * 10, yy, sx + 120 - q * 10, yy, ink(5, col=rgb("#F6C26B"), alpha=0.7))
        else:                                          # Mars: dusky sky, blue around the sun
            mars_sky(c, tw, horizon=hz, sun=(sx, sy), sun_r=40, dusk=0.55, blue=1.0)
            mars_ground(c, tw, hz, boil=boil, seed=15, dusk=0.7, rocks=False, y_end=y1 - y0 + 10)
        c.drawLine(-10, hz, W + 10, hz, ink(3, alpha=0.6, boil=boil))
        c.restore()
        c.drawRect(skia.Rect.MakeLTRB(0, y0, W, y1), ink(6))
        stamp(c, 250, y0 + 90, ("EARTH", "MARS")[j], size=60, k=ease_io(prog(t, a + 0.15 * j, a + 0.3 + 0.15 * j)),
              rot=-4, col=(rgb("#C8402E"), rgb("#3C6E99"))[j], pop=0.3)


# ---------------------------------------------------------------- HUD, intercom, NOPE, captions, end cards
def hud(c, t):
    """Top-left cartouche: one story number at a time. Hidden while a NOPE owns the frame or the lab talks."""
    shot = shot_at(t)[1]
    lvl, nk = nope_at(t)
    lvl = lvl if shot == "close" else 0
    title_on = t < E["n1"] + 0.15
    lab_live = any(WHO[k] == "LAB" and L[k] - 0.35 <= t <= E[k] + 0.35 for k in KEYS)
    y = 290
    if title_on:
        hud_card(c, SAFE_X0 + 30, 540, [("AWAKE FOR", "?? SECONDS", SEAL, 0.0)], w=600)
    elif shot in ("close", "tease", "push") and not lvl and not lab_live and t < T_BLAST3 and t >= L["n2"] + 0.1:
        known = t >= WT("n17", "15")
        hud_card(c, SAFE_X0, y, [("AWAKE FOR", "~15 SECONDS" if known else "?? SECONDS", SEAL, 0.0)], w=600)
    if title_on:
        f1, f2 = font("mono", 38), font("display", 112)
        c.save()
        c.translate(CAP_CX, 284)
        c.rotate(-3)
        tag = "COULD YOU SURVIVE"
        wv = f1.measureText(tag)
        c.drawPath(rrect(-wv / 2 - 18, -40, wv + 36, 56, 10), fill(INKC, 0.92))
        text(c, tag, 0, 2, f1, YEL_L, align="center")
        for j, name in enumerate(("MARS,", "NO SUIT?")):
            c.save()
            sc = min(1.0 if j == 0 else 0.8, 640 / f2.measureText(name))
            c.translate(0, 104 + 104 * j)
            c.scale(sc, sc)
            text(c, name, 0, 0, f2, FOAM, align="center", stroke=22)
            c.restore()
        c.restore()
    ks = prog(t, 3.0, 3.3)
    if ks > 0 and shot != "end":
        seal(c, 874, 120, 86, alpha=ks)


def intercom(c, t):
    live = [k for k in KEYS if WHO[k] == "LAB" and L[k] - 0.35 <= t <= E[k] + 0.35]
    if not live:
        return
    k = live[0]
    kin = ease_io(min(prog(t, L[k] - 0.35, L[k] - 0.05), 1 - prog(t, E[k] + 0.05, E[k] + 0.35)))
    x = SAFE_X1 - 230 + (1 - kin) * 560
    y = 290
    c.drawPath(rrect(x + 8, y + 10, 230, 96, 14), fill(INKC, 0.3 * kin))
    c.drawPath(rrect(x, y, 230, 96, 14), fill(INKC, 0.95 * kin))
    c.drawCircle(x + 46, y + 48, 26, fill(rgb("#33405E"), kin))
    for r in (8, 15, 22):
        c.drawCircle(x + 46, y + 48, r, ink(2.5, col=FOAM, alpha=0.6 * kin))
    text(c, "LAB", x + 86, y + 40, font("mono", 32), YEL_L, alpha=kin)
    for i in range(9):
        e = env("LAB", t - i * 0.03)
        hgt = 6 + 30 * e * (0.6 + 0.4 * math.sin(i * 1.7 + t * 20))
        c.drawPath(rrect(x + 88 + i * 14, y + 72 - hgt / 2, 8, hgt, 4), fill(FOAM, kin))
    if "Noted" in TXT[k]:
        tk = WT(k, "Noted")
        kk = prog(t, tk - 0.05, tk + 0.15)
        if kk > 0:
            c.save()
            c.translate(x + 208, y + 6)
            sc = 1.6 - 0.6 * ease_io(kk)
            c.scale(sc, sc)
            c.drawCircle(0, 0, 30, fill(PAPER_HI, kin))
            c.drawCircle(0, 0, 30, ink(4, alpha=kin))
            p = skia.Path()
            p.moveTo(-15, 1)
            p.lineTo(-4, 13)
            p.lineTo(17, -13)
            c.drawPath(p, ink(8, col=SEAL, alpha=kin))
            c.restore()


def nope_text(c, t):
    lvl, k = nope_at(t)
    if not lvl or shot_at(t)[1] != "close":
        return
    if lvl == 3:
        i = nope_word(t)
        word = ("Nope.", "NOPE.", "NOPE!")[max(0, i)]
        size = (150, 200, 250)[max(0, i)]
        k = 0.0 if i < 2 else k
        if i < 2:
            k = min(0.7, (t - W3[max(0, i)]) / 1.2)
    else:
        word = {1: "Nope.", 2: "NOPE!"}[lvl]
        size = (120, 200)[lvl - 1]
    f = font("display", size)
    wv = f.measureText(word)
    pop = 1.0 + 0.5 * max(0.0, 1 - k * 5)
    sc = min(pop, 620 / wv)
    alpha = 1.0 if k < 0.75 else max(0.0, 1 - (k - 0.75) / 0.25)
    c.save()
    c.translate(CAP_CX + math.sin(t * 90) * 4 * lvl, 460 if lvl < 3 else 450)
    c.rotate(-6 + 3 * lvl * math.sin(t * 50) * (1 - k))
    c.scale(sc, sc)
    text(c, word, 0, 0, f, YEL_L if (lvl < 3 or nope_word(t) < 2) else rgb("#FF6B4A"), align="center", alpha=alpha, stroke=26)
    if lvl == 3 and nope_word(t) == 2:
        rng = np.random.default_rng(3)
        for _ in range(6):
            x, y = rng.uniform(-wv / 2, wv / 2), rng.uniform(-size * 0.7, 0)
            p = skia.Path()
            p.moveTo(x, y)
            for _ in range(4):
                x += rng.uniform(-30, 30)
                y += rng.uniform(10, 40)
                p.lineTo(x, y)
            c.drawPath(p, ink(5, alpha=alpha))
    c.restore()
    text(c, "[comically deep voice]", CAP_CX, 1235, font("mono", 40), FOAM, align="center", alpha=alpha, stroke=10)


def captions(c, t):
    for k in KEYS:
        if k in NOPES or k == "n1" or not (L[k] - 0.05 <= t <= E[k] + 0.25):
            continue
        for ch in CHUNKS[k]:
            t0 = ch[0][1] - 0.05
            nxt = [c2 for c2 in CHUNKS[k] if c2[0][1] > ch[0][1]]
            later = [L[k2] for k2 in KEYS if L[k2] > L[k]]
            t1 = (nxt[0][0][1] - 0.05) if nxt else min(E[k] + 0.25, (later[0] - 0.08) if later else 99)
            if t0 <= t < t1:
                words = [w for w, _ in ch]
                active = max([i for i, (_, wt) in enumerate(ch) if wt <= t] or [0])
                words_caption(c, words, active, y=1235, size=74 if WHO[k] != "LAB" else 66)
                return


OPTS = [("A", "MEDIEVAL FARM", "medieval"), ("B", "POMPEII", "Pompeii"), ("C", "MARIANA TRENCH", "Mariana")]


def end_cards(c, t):
    a = L["n23"]
    if t < a:
        return
    gone = 1 - prog(t, L["n24"] - 0.25, L["n24"] - 0.05)      # cleared for her close-up and the countdown
    if gone <= 0:                                             # ... into one small strip until just before the flash
        ks = ease_io(prog(t, L["n24"] - 0.15, L["n24"] + 0.1)) * (1 - prog(t, E["n25"] - 0.35, E["n25"] - 0.1))
        if ks > 0:
            f = font("mono", 34)
            msg = "A FARM · B POMPEII · C TRENCH"
            wv = f.measureText(msg)
            x0 = CAP_CX - wv / 2 - 22
            c.drawPath(rrect(x0, 400, wv + 44, 66, 14), fill(PAPER_HI, 0.95 * ks))
            c.drawPath(rrect(x0, 400, wv + 44, 66, 14), ink(3, alpha=ks))
            text(c, msg, CAP_CX, 445, f, INKC, align="center", alpha=ks)
        return
    dim = ease_io(prog(t, a, a + 0.4)) * gone
    c.drawRect(skia.Rect.MakeWH(W, H), fill(INKC, 0.12 * dim))
    for i, (letter, name, word) in enumerate(OPTS):
        tk = WT("n23", word)
        k = ease_io(prog(t, tk - 0.15, tk + 0.15)) * gone
        if k <= 0:
            continue
        x, y = SAFE_X0 + 10, 300 + i * 122
        c.save()
        c.translate(x + 320, y + 50)
        c.scale(0.8 + 0.2 * k, 0.8 + 0.2 * k)
        c.translate(-(x + 320), -(y + 50))
        c.drawPath(rrect(x + 8, y + 10, 640, 104, 16), fill(INKC, 0.35 * k))
        c.drawPath(rrect(x, y, 640, 104, 16), fill(PAPER_HI, k))
        c.drawPath(rrect(x, y, 640, 104, 16), ink(4, alpha=k))
        c.drawCircle(x + 58, y + 52, 34, fill(SEAL, k))
        text(c, letter, x + 58, y + 69, font("display", 46), FOAM, align="center", alpha=k)
        f = font("display", 46 if len(name) < 12 else 40)
        text(c, name, x + 112, y + 68, f, INKC, alpha=k)
        icon(c, i, x + 585, y + 52, k * 0.9)
        c.restore()


def icon(c, i, x, y, k):
    if i == 0:    # a farm: a field in furrows and a haystack
        c.drawPath(rrect(x - 50, y - 6, 100, 44, 6), fill(rgb("#9C7A3C"), k))
        for j in range(4):
            c.drawLine(x - 46, y + 4 + j * 10, x + 46, y + 4 + j * 10, ink(2.5, col=rgb("#6E5226"), alpha=k))
        hs = smooth_path([(x - 24, y - 4), (x - 18, y - 34), (x, y - 44), (x + 18, y - 34), (x + 24, y - 4)])
        c.drawPath(hs, fill(YEL_L, k))
        c.drawPath(hs, ink(3, alpha=k))
        c.drawPath(rrect(x - 50, y - 6, 100, 44, 6), ink(3, alpha=k))
    elif i == 1:  # Pompeii: a volcano with an ash cloud
        v = skia.Path()
        v.moveTo(x - 52, y + 38)
        v.lineTo(x - 14, y - 16)
        v.lineTo(x + 14, y - 16)
        v.lineTo(x + 52, y + 38)
        v.close()
        c.drawPath(v, fill(rgb("#6E5A4A"), k))
        c.drawPath(v, ink(3, alpha=k))
        for dx, dy, r in ((0, -34, 16), (-16, -48, 13), (16, -50, 14), (2, -62, 12)):
            c.drawCircle(x + dx, y + dy, r, fill(rgb("#8E8A86"), k))
        c.drawPath(smooth_path([(x - 12, y - 16), (x, y - 26), (x + 12, y - 16)], closed=False), ink(5, col=CORAL, alpha=k))
    else:         # the trench: a V cut into the sea floor under waves
        c.drawPath(rrect(x - 50, y - 40, 100, 80, 10), fill(rgb("#2E5B7C"), k))
        p = skia.Path()
        p.moveTo(x - 50, y - 6)
        p.lineTo(x - 14, y - 6)
        p.lineTo(x, y + 36)
        p.lineTo(x + 14, y - 6)
        p.lineTo(x + 50, y - 6)
        p.lineTo(x + 50, y + 40)
        p.lineTo(x - 50, y + 40)
        p.close()
        c.drawPath(p, fill(rgb("#6E5A4A"), k))
        for j in range(2):
            w = skia.Path()
            w.moveTo(x - 46, y - 28 + j * 12)
            for q in range(4):
                w.quadTo(x - 34 + q * 24, y - 36 + j * 12, x - 22 + q * 24, y - 28 + j * 12)
            c.drawPath(w, ink(2.5, col=FOAM, alpha=k))
        c.drawPath(rrect(x - 50, y - 40, 100, 80, 10), ink(3, alpha=k))


def respawn_flash(c, t):
    a = E["n25"] + 0.02
    if t >= a:
        k = prog(t, a, DURATION)
        c.drawRect(skia.Rect.MakeWH(W, H), fill(PAPER_HI, ease_io(min(1, k * 1.6))))


def cam_close(t):
    """Camera on the close shot: a slow push-out over the hook, punch-ins on the NOPEs."""
    z = 1.0
    if t < shot_start("gauge"):
        z = 1.10 - 0.10 * ease_io(prog(t, 0.4, shot_start("gauge")))
    return z * punch(t)


# ---------------------------------------------------------------- frame
def draw_frame(c, t):
    sx, sy = shake(t)
    c.save()
    c.translate(sx, sy)
    shot = shot_at(t)[1]
    if shot in ("close", "end"):
        z = cam_close(t)
        dyc = 0.0
        if shot == "end":
            z = 1.10 + 0.08 * ease_io(prog(t, L["n23"], DURATION))
            dyc = 70.0
        if z != 1.0 or dyc:
            c.translate(XH, YH + dyc)
            c.scale(z, z)
            c.translate(-XH, -YH)
        close_shot(c, t)
    elif shot in ("push", "tease"):            # slow push in on her
        a = shot_start(shot)
        z = 1.12 + 0.12 * ease_io(prog(t, a, shot_end(a)))
        c.translate(XH, YH + 60)
        c.scale(z, z)
        c.translate(-XH, -YH)
        close_shot(c, t)
    elif shot == "relief":                    # she exhales: he recovered
        z = 1.25
        c.translate(XH, YH + 40)
        c.scale(z, z)
        c.translate(-XH, -YH)
        close_shot(c, t)
        tr = WT("n20", "recovered")
        stamp(c, CAP_CX, 470, "HE RECOVERED", size=64, k=prog(t, tr - 0.2, tr + 0.05), rot=-5, col=rgb("#3F7A4E"))
    elif shot == "plead":
        z = 1.5
        c.translate(XH, 830)
        c.scale(z, z)
        c.translate(-XH, -YH)
        close_shot(c, t)
    elif shot == "gauge":
        gauge_shot(c, t)
    elif shot == "co2":
        co2_shot(c, t)
    elif shot == "lungs":
        lungs_shot(c, t)
    elif shot == "boil":
        boil_shot(c, t)
    elif shot == "crater":
        crater_shot(c, t)
    elif shot == "duck":
        duck_shot(c, t)
    elif shot == "signal":
        signal_shot(c, t)
    elif shot == "horizon":
        horizon_shot(c, t)
    elif shot == "clock":
        clock_shot(c, t)
    elif shot == "chamber":
        chamber_shot(c, t)
    elif shot == "sunset":
        sunset_shot(c, t)
    elif shot == "glow":
        sunset_shot(c, t, glow=True)
    c.restore()
    paper_over(c, 1.0)
    vignette(c, 0.24)
    hud(c, t)
    intercom(c, t)
    end_cards(c, t)
    nope_text(c, t)
    captions(c, t)
    respawn_flash(c, t)
