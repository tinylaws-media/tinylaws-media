"""COULD YOU SURVIVE? #04 — A Roman winter camp: the picture (2D estampe look, sz2d.py). Timed on out/cys04_lines.json.

    python3 sz2render.py cys04_pic                # -> out/cys04_pic_video.mp4
    python3 sz2render.py cys04_pic --sheet 0 2 5 ...

Shots (named, none held longer than 8 s): close (her in the snow inside the timber fort, a letter tumbling in the wind
overhead) → map (Rome to the frontier: Vindolanda, AD ~100) → march (a Roman road, the milestones counting to XX and
the hours to V) → close ("Thirty WHAT?") → pack (her under a recruit's load on a pole) → close (the lab, NOPE 1: the
snow blows off the whole fort) → close (the letter lands in her hands) → letter (socks, sandals, underpants) → beer
(the barrel runs dry) → duck (the bathhouse pool) → latrine (seats side by side) → sponge → close (NOPE 2: the barrack
roof rips off) → close (the tease) → mud (something is down there) → contract (the answer: 25 winters, you are on
the first) → close (the lab; NOPE 3: the rampart falls like dominoes, the gate tower topples) → dig (the tablets in
the wet ground, 1973, 1,700+) → invite (the birthday invitation; her own hand) → end (the next spawns, respawn).
HUD: "YOUR CONTRACT", a progress bar whose end is hidden ("DAY 1 OF ????") until the answer: DAY 1 OF 9,131.
"""
import json
import math
import os

import numpy as np
import skia

from sz2d import (W, H, FPS, rgb, mixc, fill, ink, text, smooth_path, rrect, oval, ease_io, prog, font, mist_band,
                  draw_hero, draw_duck, paper_over, vignette, seal, mottle, words_caption, hud_card, woodgrain,
                  draw_legs, snowfall, winter_sky, snow_ground, palisade, gate_tower, barrack, leaf_tablet, barrel,
                  steam, breath, snow_burst,
                  PAPER, PAPER_HI, INKC, PRUSSIAN, CORAL, SEAL, FOAM, YEL, YEL_D, YEL_L, WHITE, SAFE_X0, SAFE_X1, CAP_CX,
                  SNOW, SNOW_SH, SNOW_D, TIMBER, TIMBER_D, TIMBER_L, MUD, MUD_D, MUD_L, LEAF_WOOD, LEAF_WOOD_D, IRON,
                  STONE, STONE_D, STONE_L, SAND, SAND_L, WATER)
import cys04 as EP

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
EPNAME = "cys04_pic"
DURATION = EP.DURATION

_js = json.load(open(os.path.join(OUT, "cys04_lines.json"), encoding="utf-8"))
L = {l["key"]: l["t"] for l in _js["lines"]}
DUR = {l["key"]: l["dur"] for l in _js["lines"]}
WHO = {l["key"]: l["who"] for l in _js["lines"]}
TXT = {l["key"]: l["text"] for l in _js["lines"]}
E = {k: L[k] + DUR[k] for k in L}
KEYS = sorted(L, key=lambda k: L[k])
ENV = {w: np.load(os.path.join(OUT, f"cys04_env_{w}.npy")) for w in ("N", "HERO", "LAB")}

# what the captions show (numbers as figures; the voice says them in words)
CAP = {"n2": "Winter, around the year 100. The army signs you up.",
       "n3": "A Roman manual: carry about 20 kg. March 30 km.", "n4": "Thirty WHAT?",
       "n5": "In just over 6 hours.", "n6": "Lab here. Fort sick list: 31 unfit. Noted.",
       "n9": "Someone here got socks, sandals, and 2 pairs of underpants.",
       "n16": "25 years. Minimum. If you make it.", "n17": "Noted. See you in 25 years.",
       "n23": "Respawning in 3... 2..."}
# how long a caption word takes to SAY (characters of the spoken words), so a figure lights up when it is said
SAYLEN = {"100.": 11, "30": 6, "km.": 10, "6": 3, "20": 6, "kg.": 5, "2": 3, "25": 11, "31": 10, "3...": 5, "2...": 3}
NOPES = {"n7": 1, "n14": 2, "n18": 3}
XH, YH, HS = 450, 840, 0.95            # her head in the close shot, and her scale
HORIZON = 1010
FEET_Y = YH + 640 * HS


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
SHOTS = [                                 # rule: no camera setup held longer than 8 s
    (0.0, "close"),
    (WT("n2", "Winter") + 0.25, "map"),   # Rome to the frontier
    (L["n3"] - 0.05, "pack"),             # carry about 20 kg
    (WT("n3", "March") - 0.05, "march"),  # march 20 Roman miles: the milestones count to XX
    (L["n4"] - 0.1, "close"),             # "Thirty WHAT?"
    (L["n5"] - 0.05, "march"),            # in just over 6 hours: the dial sweeps 5 summer hours
    (L["n6"] - 0.15, "report"),           # the lab reads the fort's sick list
    (L["n7"] - 0.15, "close"),            # NOPE 1
    (L["n8"] - 0.05, "catch"),            # the letter lands in her hands
    (L["n9"] - 0.05, "letter"),           # socks, sandals, underpants
    (L["n10"] - 0.05, "beer"),            # no beer
    (L["n11"] - 0.05, "duck"),            # the bathhouse
    (L["n12"] - 0.05, "latrine"),         # seats side by side
    (L["n13"] - 0.05, "sponge"),          # a shared sponge on a stick
    (L["n14"] - 0.15, "close"),           # NOPE 2
    (L["n15"] - 0.05, "tease"),           # how long would you last? (her, the contract)
    (WT("n15", "The") - 0.05, "mud"),     # the real surprise is underground
    (L["n16"] - 0.05, "contract"),        # 25 years
    (L["n17"] - 0.1, "close"),            # the lab; NOPE 3
    (WT("n19", "Those") - 0.05, "dig"),   # real letters, dug out of the mud here
    (L["n20"] - 0.05, "invite"),          # the birthday invitation
    (L["n21"] - 0.05, "end"),             # the next spawns
    (L["n22"] - 0.1, "plead"),            # "Anywhere with heating." tight on her
    (L["n23"] - 0.05, "end"),             # the countdown
]


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


CLOSE_LIKE = ("close", "end", "plead", "catch", "tease")


# ---------------------------------------------------------------- NOPE machinery (as #01–#03)
def nope_words():
    e = ENV["HERO"]
    a, b = int(L["n18"] * FPS) - 1, int(E["n18"] * FPS) + 1
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
    return [wt for _, wt in word_times("n18")]


W3 = nope_words()
T_BLAST3 = W3[-1]
T_N1 = L["n7"] + 0.15                 # damage lands on / just after each word
T_N2 = L["n14"] + 0.2


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
    if not (L["n18"] - 0.05 <= t <= min(T_BLAST3 + 1.05, L["n19"] - 0.15)):
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
T_CATCH = L["n8"] + 0.35             # the tumbling letter lands in her hands


def hero_state(t):
    st = dict(face="cold", arms="hug", shiver=0.35, look=None, squash=0.0, blink=0.0, mouth_open=None, tilt=0.0,
              hop=0.0, tablet=False)
    for b in (2.6, 6.0, 12.9, 19.0, 26.9, 33.2, 38.0, 44.1, 53.0, 58.4, 62.9):
        if b <= t <= b + 0.12:
            st["blink"] = 1.0
    if t < 0.6:                                    # spawn: a squash bounce as she lands in the snow
        st["face"] = "shock"
        k = t / 0.6
        st["squash"] = 0.45 * math.sin(k * math.pi * 2) * (1 - k)
        st["arms"] = "none"
    elif t < E["n1"]:
        st["face"] = "shock"
        st["look"] = (10, -8)
    elif L["n4"] - 0.2 <= t < L["n5"]:              # "Thirty WHAT?"
        st["face"] = "panic"
        st["arms"] = "up"
        st["shiver"] = 0.0
        st["mouth_open"] = 0.6 + 1.2 * env("HERO", t)
    elif L["n6"] - 0.3 <= t < L["n7"]:             # the lab enlists her
        st["face"] = "deadpan"
        st["look"] = (12, -6)
    elif L["n8"] - 0.1 <= t < shot_start("letter"):   # the letter tumbles down into her hands
        st["face"] = "up" if t < T_CATCH else "happy"
        st["look"] = (0, -9) if t < T_CATCH else (0, 4)
        st["arms"] = "raise" if t < T_CATCH else "hug"
        st["tablet"] = t >= T_CATCH
        st["shiver"] = 0.0
    elif L["n15"] - 0.1 <= t < L["n16"]:            # the tease: she holds the letter, then looks at the HUD
        st["face"] = "worried"
        st["tablet"] = True
        st["look"] = (-12, -10)
    elif L["n17"] - 0.2 <= t < L["n18"]:            # the lab: 25 years
        st["face"] = "deadpan"
        st["look"] = (12, -6)
        st["shiver"] = 0.15
    elif L["n21"] - 0.1 <= t:
        st["face"] = "cold"
        st["arms"] = "hug"
        if L["n22"] - 0.1 <= t < L["n23"]:          # "Anywhere with heating."
            st["face"] = "worried"
            st["look"] = (0, -8)
            st["mouth_open"] = 0.5 + 1.1 * env("HERO", t)
        elif t >= L["n23"]:
            st["face"] = "worried"
    if E["n18"] + 0.4 <= t < L["n21"]:
        st["face"] = "shock"
        st["look"] = (0, 10)
    lvl, k = nope_at(t)
    if lvl and k < 0.85:
        st["face"] = "nope"
        st["mouth_open"] = min(2.0, 1.0 + 0.5 * lvl * max(0.0, 1 - k))
        if lvl == 3 and t < T_BLAST3:
            st["mouth_open"] = min(2.0, 1.0 + 0.45 * (nope_word(t) + 1) * (0.4 + env("HERO", t)))
        st["squash"] = 0.35 * lvl * math.sin(min(1.0, k * 3) * math.pi) * (1 - k)
        st["arms"] = ("hug", "up", "up")[lvl - 1]
        st["tablet"] = False
        st["shiver"] = 0.0
        st["tilt"] = (0.0, -6.0, 0.0)[lvl - 1]
    return st


# ---------------------------------------------------------------- the fort (the close shot)
def fall_fn(t):
    """NOPE 3: the rampart posts tip over left to right, one after another, like dominoes."""
    k = t - T_BLAST3
    if k <= 0:
        return None

    def f(i, x):
        d = k - (x + 100) / 1300 * 0.5
        return 0.0 if d <= 0 else 78 * ease_io(min(1.0, d / 0.3))
    return f


def fort_bg(c, t, boil, y0=HORIZON):
    """Behind her: the far rampart with its gate tower and a cohort banner (plain red cloth, no emblem),
    a barrack block on the left, snow falling."""
    tw = twos(t)
    winter_sky(c, tw, horizon=y0, sun=(760, 330))
    # the hills beyond the wall
    hill = smooth_path([(-60, y0 - 210), (180, y0 - 260), (420, y0 - 230), (700, y0 - 290), (1140, y0 - 220)], closed=False)
    hill.lineTo(1140, y0 + 10)
    hill.lineTo(-60, y0 + 10)
    hill.close()
    c.drawPath(hill, fill(mixc(SNOW_SH, WHITE, 0.4)))
    c.drawPath(smooth_path([(-60, y0 - 210), (180, y0 - 260), (420, y0 - 230), (700, y0 - 290), (1140, y0 - 220)],
                           closed=False), ink(3, alpha=0.6, boil=boil))
    blast = t >= T_BLAST3
    snow_on = 1.0 - prog(t, T_N1, T_N1 + 0.5) if t < T_N2 + 5 else 0.0
    snow_on = 0.0 if T_N1 + 0.5 <= t else snow_on
    fall = fall_fn(t)
    palisade(c, -40, 1120, y0 + 6, 270, boil=boil, fall=fall, snow=snow_on, seed=4)
    topple = prog(t, T_BLAST3 + 0.1, T_BLAST3 + 0.6) if blast else 0.0
    gate_tower(c, 760, y0 + 8, s=0.78, boil=boil, topple=ease_io(topple), snow=snow_on)
    # the banner: a plain red cloth on a cross-bar, flapping (no emblem, no lettering)
    if topple < 0.05:
        px, py = 900, y0 - 470
        c.drawLine(px, py, px, y0 + 4, ink(8, col=TIMBER_D))
        c.drawLine(px - 50, py + 10, px + 50, py + 10, ink(7, col=TIMBER_D))
        fl = []
        for j in range(7):
            yy = py + 14 + j * 18
            fl.append((px - 46 + 6 * math.sin(tw * 6 + j), yy))
        for j in range(6, -1, -1):
            yy = py + 14 + j * 18
            fl.append((px + 46 + 8 * math.sin(tw * 6 + j + 1), yy))
        cloth = smooth_path(fl)
        c.drawPath(cloth, fill(SEAL))
        c.drawPath(cloth, ink(3, boil=boil))
    # the barrack block on the left
    sh = prog(t, T_N2, T_N2 + 1.4) if t >= T_N2 else 0.0
    barrack(c, -80, 300, y0 + 40, 200, boil=boil, shingles_off=sh, t=tw, snow=snow_on if sh <= 0 else 0.0)
    snow_ground(c, tw, y0 + 40, boil=boil)


def tumbling_letter(c, t):
    """From frame 0 a letter tumbles across the sky in the wind; at 'you get mail' it drops into her hands."""
    if t >= T_CATCH:
        return
    t0 = L["n8"] - 0.2
    if t < t0:
        x = 980 - ((t * 60) % 1250)
        y = 640 + 50 * math.sin(t * 1.3) if x < 560 else 300 + 50 * math.sin(t * 1.3)
        rot = t * 160
        s = 0.6
    else:
        k = ease_io(prog(t, t0, T_CATCH))
        x = 760 + (XH + 120 - 760) * k
        y = 260 + (YH + 120 - 260) * k
        rot = 40 * (1 - k) + 60 * math.sin(t * 6) * (1 - k)
        s = 0.42 + 0.18 * k
    leaf_tablet(c, x, y, 260 * s, 120 * s, rot=rot, seed=5, rows=3)


def close_shot(c, t, s=HS):
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 1.0)
    lvl, nk = nope_at(t)
    fort_bg(c, t, boil)
    snowfall(c, tw, density=55, alpha=0.85, wind=0.15, seed=4, area=(0, 0, W, HORIZON + 200))
    tumbling_letter(c, t)
    if T_N1 <= t < T_N1 + 1.3:                     # NOPE 1: the snow blows off the whole fort, behind her
        snow_burst(c, 450, HORIZON - 260, prog(t, T_N1, T_N1 + 1.3), n=40, spread=1200, seed=3, up=360, size=(10, 26))
    if T_BLAST3 <= t < T_BLAST3 + 1.4:             # NOPE 3: a wall of snow off the falling rampart, behind her
        snow_burst(c, 450, HORIZON - 60, prog(t, T_BLAST3 + 0.2, T_BLAST3 + 1.5), n=34, spread=1300, seed=9, up=1000, size=(14, 40))
    st = hero_state(t)
    if t >= L["n21"] - 0.2:                         # the end: the duck in a steaming tub beside her
        tx, ty = XH + 270, FEET_Y - 10
        tub = smooth_path([(tx - 90, ty - 110), (tx + 90, ty - 110), (tx + 76, ty), (tx - 76, ty)])
        steam(c, twos(t), tx, ty - 120, w=150, n=3, alpha=0.8, height=260)
        draw_duck(c, tx, ty - 100, s=0.75, boil=None, tilt=-4 + 2 * math.sin(twos(t) * 2))
        c.drawPath(tub, fill(TIMBER))
        woodgrain(c, tub, alpha=0.25, seed=4)
        c.drawLine(tx - 86, ty - 70, tx + 86, ty - 70, ink(8, col=IRON))
        c.drawPath(tub, ink(4))
    c.drawPath(oval(XH, FEET_Y - 4, 200 * s, 30 * s), fill(SNOW_D, 0.45))
    draw_legs(c, XH, YH, s=s, boil=boil, t=tw, hop=st["hop"], squash=st["squash"], shiver=st["shiver"])
    # snow up to her ankles
    drift = smooth_path([(XH - 260, FEET_Y + 10), (XH - 170, FEET_Y - 34), (XH - 40, FEET_Y - 22), (XH + 90, FEET_Y - 38),
                         (XH + 240, FEET_Y - 6), (XH + 300, FEET_Y + 40), (XH - 300, FEET_Y + 40)])
    c.drawPath(drift, fill(SNOW))
    c.drawPath(drift, ink(3, col=SNOW_D, alpha=0.8, boil=boil))
    draw_hero(c, XH, YH, s=s, face=st["face"], boil=boil, arms=st["arms"], t=tw, blink=st["blink"],
              squash=st["squash"], look=st["look"], shiver=st["shiver"], mouth_open=st["mouth_open"], tilt=st["tilt"])
    if t < shot_start("duck"):                     # the duck sits in the snow at her feet, perfectly fine
        draw_duck(c, XH + 250, FEET_Y - 20, s=0.6, boil=None, tilt=-3 + 2 * math.sin(twos(t) * 1.3), look=0.3)
    if st["tablet"]:                                # the letter, held against her chest
        leaf_tablet(c, XH + 4, YH + 214 * s, 230 * s, 104 * s, rot=-4, seed=5, rows=3)
    if not lvl:
        breath(c, t, XH + 30, YH + 50 * s, k=0.9, s=s)
    # NOPE 1: her drift explodes to both sides
    if T_N1 <= t < T_N1 + 1.3:
        k1 = prog(t, T_N1, T_N1 + 1.3)
        snow_burst(c, XH - 330, FEET_Y - 30, k1, n=14, spread=500, seed=7, up=260, size=(16, 40))
        snow_burst(c, XH + 330, FEET_Y - 30, k1, n=14, spread=500, seed=8, up=260, size=(16, 40))
    # NOPE 3: snow thrown at us from both sides, low
    if T_BLAST3 <= t < T_BLAST3 + 1.4:
        k3 = prog(t, T_BLAST3, T_BLAST3 + 1.4)
        snow_burst(c, XH - 360, FEET_Y - 40, k3, n=20, spread=700, seed=12, up=360, size=(20, 50))
        snow_burst(c, XH + 360, FEET_Y - 40, k3, n=20, spread=700, seed=13, up=360, size=(20, 50))
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


# ---------------------------------------------------------------- map: Rome to the frontier
def _land_rings():
    geo = json.load(open(os.path.join(HERE, "data", "ne_110m_land.geojson")))
    rings = []
    for f in geo["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            r = np.array(poly[0])
            if r[:, 1].mean() < 20 or r[:, 0].mean() < -40 or r[:, 0].mean() > 60:
                continue
            rings.append(r)
    return rings


LAND = _land_rings()
VIND = (-2.36, 54.99)                  # Vindolanda (lon, lat)
ROME = (12.48, 41.89)


def map_xy(lon, lat, zoom, ctr):
    k = 1080 / 360 * zoom
    return 450 + (lon - ctr[0]) * k * math.cos(math.radians(50)), 820 - (lat - ctr[1]) * k


def map_shot(c, t):
    a, b = shot_start("map"), shot_end(shot_start("map"))
    fi = int(t * FPS)
    boil = (fi // 2, 0.7)
    k = ease_io(prog(t, a + 0.6, b - 0.2))
    zoom = 6.5 + 16 * k
    ctr = (5.0 + (VIND[0] - 5.0) * k, 48.5 + (VIND[1] - 48.5) * k)
    c.drawRect(skia.Rect.MakeWH(W, H), fill(rgb("#2A4E73")))
    mottle(c, rrect(-10, -10, W + 20, H + 20, 0), PRUSSIAN, alpha=0.18, scale=0.004, seed=21)
    for yy in range(60, H, 44):                       # engraved swell lines
        p = skia.Path()
        p.moveTo(-20, yy)
        for i in range(12):
            p.lineTo(i * 100, yy + 6 * math.sin(i * 1.3 + yy))
        c.drawPath(p, ink(2, col=FOAM, alpha=0.12))
    for r in LAND:
        pts = [map_xy(lon, lat, zoom, ctr) for lon, lat in r]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        if max(xs) < -50 or min(xs) > W + 50 or max(ys) < -50 or min(ys) > H + 50:
            continue
        path = skia.Path()
        path.addPoly([skia.Point(*p) for p in pts], True)
        c.drawPath(path, fill(PAPER_HI))
        mottle(c, path, PAPER, alpha=0.3, scale=0.01, seed=4)
        c.drawPath(path, ink(3, boil=boil))
    # snow over the north
    rx, ry = map_xy(ROME[0], ROME[1], zoom, ctr)
    vx, vy = map_xy(VIND[0], VIND[1], zoom, ctr)
    kl = ease_io(prog(t, a + 0.1, a + 0.9))
    if kl > 0:                                        # the road north: Rome to the frontier, dashed
        path = smooth_path([(rx, ry), ((rx + vx) / 2 + 60, (ry + vy) / 2), (vx, vy)], closed=False)
        meas = skia.PathMeasure(path, False)
        seg = skia.Path()
        meas.getSegment(0, meas.getLength() * kl, seg, True)
        pd = ink(7, col=SEAL)
        pd.setPathEffect(skia.DashPathEffect.Make([20, 14], 0))
        c.drawPath(seg, pd)
    if -100 < rx < W + 100:
        c.drawCircle(rx, ry, 14, fill(INKC))
        text(c, "ROME", rx + 26, ry + 12, font("mono", 40), INKC, stroke=8, stroke_col=PAPER_HI)
    # the frontier line across northern Britain (Solway to Tyne), drawn as the map arrives
    if k > 0.5:
        kk = ease_io(prog(k, 0.5, 0.9))
        a_ = map_xy(-3.3, 54.95, zoom, ctr)
        b_ = map_xy(-1.45, 55.0, zoom, ctr)
        c.drawLine(a_[0], a_[1], a_[0] + (b_[0] - a_[0]) * kk, a_[1] + (b_[1] - a_[1]) * kk, ink(9, col=INKC, alpha=0.8))
    kp = prog(t, a + 0.7, a + 1.1)
    for j in range(3):                                # cold rings pulsing out of the fort
        ph = ((t - a) * 1.2 + j / 3) % 1.0
        c.drawCircle(vx, vy, 30 + 160 * ph, ink(5, col=FOAM, alpha=kp * (1 - ph)))
    c.save()
    c.translate(vx, vy)
    c.scale(ease_io(kp), ease_io(kp))
    pin = skia.Path()
    pin.moveTo(0, 0)
    pin.cubicTo(-30, -36, -26, -66, 0, -66)
    pin.cubicTo(26, -66, 30, -36, 0, 0)
    c.drawPath(pin, fill(SEAL))
    c.drawPath(pin, ink(4))
    c.drawCircle(0, -44, 9, fill(FOAM))
    c.restore()
    if kp > 0:
        text(c, "VINDOLANDA", vx, vy + 70, font("mono", 44), INKC, align="center", alpha=kp, stroke=10, stroke_col=PAPER_HI)
    snowfall(c, twos(t), density=40, alpha=0.6, wind=0.1, seed=8)
    kc = ease_io(prog(t, WT("n2", "year") - 0.1, WT("n2", "year") + 0.25))
    if kc > 0:
        hud_card(c, SAFE_X0, 290, [("WHEN", "AROUND AD 100", INKC, 0.0)], alpha=kc, w=600)


# ---------------------------------------------------------------- march: 20 Roman miles in 5 summer hours
def roman_numeral(n):
    vals = ((10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"))
    s = ""
    for v, r in vals:
        while n >= v:
            s += r
            n -= v
    return s


def march_shot(c, t):
    """A Roman road runs straight to the horizon through summer hills; milestones rush past, counting to XX, while
    a sun dial's shadow sweeps five hours."""
    a = shot_start("march")
    a2 = shot_start("march", 1)
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    tw = twos(t)
    hz = 760
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeLinear([(0, 0), (0, hz)], [rgb("#6F86A0"), rgb("#D9DCD6")], [0.0, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, hz + 4), p)
    for j, (y, w_, h_, sp) in enumerate(((180, 520, 30, 12), (300, 600, 26, -9))):
        mist_band(c, ((j * 400 + sp * tw) % (W + 600)) - 300, y, w_, h_, alpha=0.8)
    hills = smooth_path([(-60, hz - 60), (200, hz - 130), (430, hz - 70), (700, hz - 150), (1140, hz - 80)], closed=False)
    hills.lineTo(1140, H + 20)
    hills.lineTo(-60, H + 20)
    hills.close()
    c.drawPath(hills, fill(SNOW))
    mottle(c, hills, SNOW_SH, alpha=0.35, scale=0.01, seed=3)
    c.drawPath(smooth_path([(-60, hz - 60), (200, hz - 130), (430, hz - 70), (700, hz - 150), (1140, hz - 80)], closed=False),
               ink(3, boil=boil))
    # the road in perspective
    vx = 450
    road = skia.Path()
    road.moveTo(vx - 8, hz - 70)
    road.lineTo(vx + 8, hz - 70)
    road.lineTo(vx + 520, H + 20)
    road.lineTo(vx - 520, H + 20)
    road.close()
    c.drawPath(road, fill(STONE_L))
    run = (t - a) * 2.2 if t < a2 else (t - a2) * 1.0
    c.save()
    c.clipPath(road, doAntiAlias=True)
    rngp = np.random.default_rng(9)
    offs = rngp.uniform(0, 1, 40)
    for j in range(40):                               # paving stones rushing toward us, staggered joints
        z0 = ((j - run) % 40) / 40.0
        z1 = ((j + 1 - run) % 40) / 40.0
        if z1 < z0:
            continue
        y0_ = hz - 70 + (H + 90 - hz) * z0 ** 2.2
        y1_ = hz - 70 + (H + 90 - hz) * z1 ** 2.2
        half0 = 8 + 512 * (y0_ - (hz - 70)) / (H + 90 - hz)
        half1 = 8 + 512 * (y1_ - (hz - 70)) / (H + 90 - hz)
        c.drawLine(vx - half1, y1_, vx + half1, y1_, ink(1.5 + 4 * z1, col=STONE_D, alpha=0.8))
        for u in np.arange(-1 + 0.25 * offs[j], 1, 0.5):
            c.drawLine(vx + u * half0, y0_, vx + u * half1, y1_, ink(1.2 + 3 * z1, col=STONE_D, alpha=0.6))
    c.drawLine(vx, hz - 70, vx, H + 20, ink(6, col=STONE_D, alpha=0.35))      # the crown of the road
    c.restore()
    c.drawPath(road, ink(4, boil=boil))
    # milestones on the right verge, rushing past; the count is the number of the stone nearest us
    tm0, tm1 = a + 0.1, WT("n3", "30") + 0.35
    miles = 20 * ease_io(prog(t, tm0, tm1))
    for j in range(4):
        z = ((j - miles * 0.999) % 4) / 4.0
        if z < 0.05:
            continue
        sx = vx + 30 + 600 * z ** 2
        sy = hz - 60 + (H - hz) * z ** 2
        sc = 0.15 + 1.5 * z ** 2
        stn = rrect(sx - 50 * sc, sy - 210 * sc, 100 * sc, 210 * sc, 30 * sc)
        c.drawPath(stn, fill(STONE))
        c.drawPath(stn, ink(max(1.5, 4 * sc), boil=boil))
    n = max(1, min(20, int(miles) + 1)) if miles > 0.01 else 1
    # the milestone count, big, and the dial
    k_in = ease_io(prog(t, a, a + 0.3))
    cx, cy, r = 450, 600 + (1 - k_in) * 200, 150
    c.drawCircle(cx + 8, cy + 10, r, fill(INKC, 0.25))
    c.drawCircle(cx, cy, r, fill(PAPER_HI))
    mottle(c, oval(cx, cy, r, r), PAPER, alpha=0.2, scale=0.03, seed=2)
    hrs = 5 * ease_io(prog(t, a2 + 0.1, WT("n5", "6") + 0.3)) if t >= a2 else 0.0
    sweep = skia.Path()
    sweep.moveTo(cx, cy)
    sweep.arcTo(skia.Rect.MakeLTRB(cx - r + 16, cy - r + 16, cx + r - 16, cy + r - 16), 180, 180 * hrs / 5, False)
    sweep.close()
    c.drawPath(sweep, fill(CORAL, 0.45))
    for i in range(6):                                # a half-dial: the day's hours
        an = math.radians(180 + i * 36)
        c.drawLine(cx + (r - 30) * math.cos(an), cy + (r - 30) * math.sin(an), cx + (r - 8) * math.cos(an),
                   cy + (r - 8) * math.sin(an), ink(5))
    an = math.radians(180 + 36 * hrs)
    c.drawLine(cx, cy, cx + (r - 36) * math.cos(an), cy + (r - 36) * math.sin(an), ink(10, col=SEAL))
    c.drawCircle(cx, cy, 12, fill(INKC))
    c.drawCircle(cx, cy, r, ink(6, boil=boil))
    text(c, f"MILE {roman_numeral(n)}", cx, cy + r + 70, font("display", 64), INKC, align="center", stroke=12, stroke_col=PAPER_HI)
    t30, t6 = WT("n3", "30"), WT("n5", "6")
    rows = []
    if t >= t30 - 0.1:
        rows = [("20 ROMAN MILES", "≈ 30 KM", SEAL, max(0.0, 1 - (t - t30) * 3))]
    if t >= t6 - 0.1:
        rows = [("5 SUMMER HOURS", "≈ 6 H", SEAL, max(0.0, 1 - (t - t6) * 3))]
    if rows:
        hud_card(c, SAFE_X0, 290, rows, alpha=ease_io(prog(t, t30 - 0.1, t30 + 0.15)) if t < a2 else 1.0, w=600)


# ---------------------------------------------------------------- pack: a recruit's load
def pack_shot(c, t):
    """Her, tight, under a pole across her shoulder hung with a pot, a sack, a satchel and a cloak roll; she sinks
    a little with each bundle; the tag reads at least 20 kg."""
    a = shot_start("pack")
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 1.0)
    winter_sky(c, tw, horizon=1100, sun=(780, 300))
    snow_ground(c, tw, 1100, boil=boil, seed=5)
    s = 1.05
    hx, hy = 450, 760
    k = ease_io(prog(t, a, a + 0.6))
    sink = 0.18 * ease_io(prog(t, WT("n3", "20") - 0.1, WT("n3", "20") + 0.4))
    # the pole over her right shoulder, the bundles swinging
    p0 = (hx - 360, hy + 120)
    p1 = (hx + 330, hy - 150)
    c.drawLine(p0[0], p0[1], p1[0], p1[1], ink(26, col=TIMBER_D))
    c.drawLine(p0[0], p0[1], p1[0], p1[1], ink(4, boil=boil))
    sw = 8 * math.sin(tw * 3.4)
    items = [(0.08, "pot"), (0.25, "sack"), (0.82, "bag"), (0.96, "roll")]
    for j, (u, kind) in enumerate(items):
        kj = ease_io(prog(t, a + 0.1 + 0.2 * j, a + 0.35 + 0.2 * j))
        if kj <= 0:
            continue
        x = p0[0] + (p1[0] - p0[0]) * u
        y = p0[1] + (p1[1] - p0[1]) * u
        c.save()
        c.translate(x, y)
        c.rotate(sw * (1 if j % 2 else -1))
        c.translate(0, -60 * (1 - kj))
        c.drawLine(0, 0, 0, 40, ink(4))
        if kind == "pot":
            c.drawPath(oval(0, 100, 62, 56), fill(IRON))
            c.drawPath(oval(0, 100, 62, 56), ink(4, boil=boil))
            c.drawPath(oval(0, 50, 54, 12), fill(rgb("#2E3238")))
        elif kind == "sack":
            sk = smooth_path([(-40, 40), (40, 40), (66, 140), (40, 200), (-40, 200), (-66, 140)])
            c.drawPath(sk, fill(rgb("#B9A27A")))
            mottle(c, sk, rgb("#9C845C"), alpha=0.35, scale=0.03)
            c.drawPath(sk, ink(4, boil=boil))
        elif kind == "bag":
            bg = rrect(-60, 40, 120, 110, 16)
            c.drawPath(bg, fill(rgb("#7A4A2E")))
            c.drawPath(rrect(-60, 40, 120, 40, 12), fill(rgb("#5E3622")))
            c.drawPath(bg, ink(4, boil=boil))
        else:
            rl = rrect(-80, 40, 160, 56, 28)
            c.drawPath(rl, fill(SEAL))
            c.drawPath(rl, ink(4, boil=boil))
        c.restore()
    draw_legs(c, hx, hy, s=s, boil=boil, t=tw, squash=sink, shiver=0.25)
    draw_hero(c, hx, hy + 30 * sink, s=s, face="panic", boil=boil, arms="raise", t=tw, squash=sink, shiver=0.25,
              look=(8, -4))
    breath(c, t, hx + 30, hy + 50, k=1.0, s=s)
    kt = ease_io(prog(t, WT("n3", "20") - 0.1, WT("n3", "20") + 0.2))
    if kt > 0:
        hud_card(c, SAFE_X0, 290, [("60 ROMAN POUNDS", "≈ 20 KG", SEAL, max(0.0, 1 - (t - WT("n3", "20")) * 3))],
                 alpha=kt, w=600)


# ---------------------------------------------------------------- report: the fort's sick list
def report_shot(c, t):
    """The fort's strength report as a field of 296 ink dots (one per man present: no one is drawn); at
    'thirty-one' 31 of them turn red."""
    a = shot_start("report")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    bg = rrect(-10, -10, W + 20, H + 20, 0)
    c.drawPath(bg, fill(rgb("#E9DDBF")))
    woodgrain(c, bg, alpha=0.25, seed=31, fx=0.004, fy=0.08)
    mottle(c, bg, LEAF_WOOD_D, alpha=0.2, scale=0.01, seed=5)
    z = 1.0 + 0.08 * prog(t, a, shot_end(a))
    c.save()
    c.translate(450, 860)
    c.scale(z, z)
    c.translate(-450, -860)
    t31 = WT("n6", "31")
    kr = ease_io(prog(t, t31 - 0.1, t31 + 0.5))
    rng = np.random.default_rng(154)
    red = set(rng.choice(296, 31, replace=False).tolist())
    cols, step = 16, 38
    x0, y0 = 450 - (cols - 1) * step / 2, 560
    for i in range(296):
        r_, c_ = divmod(i, cols)
        ki = ease_io(prog(t, a + i * 0.004, a + 0.2 + i * 0.004))
        if ki <= 0:
            continue
        x, y = x0 + c_ * step, y0 + r_ * step
        if i in red and kr > 0:
            c.drawCircle(x, y, 12 + 5 * kr, fill(SEAL, ki))
        else:
            c.drawCircle(x, y, 11, fill(INKC, 0.85 * ki))
    c.restore()
    k_in = ease_io(prog(t, a + 0.1, a + 0.4))
    text(c, "SICK LIST", 150, 470, font("mono", 44), INKC, alpha=k_in)
    if kr > 0:
        text(c, "31", 640, 486, font("display", 110), SEAL, align="center", alpha=kr, stroke=10, stroke_col=PAPER_HI)


# ---------------------------------------------------------------- letter: socks, sandals, underpants
def sock_icon(c, x, y, s, col):
    p = smooth_path([(-20, -70), (22, -70), (22, 10), (60, 34), (60, 62), (-6, 62), (-20, 30)])
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawPath(p, fill(col))
    for yy in (-56, -44):
        c.drawLine(-20, yy, 22, yy, ink(3, col=PAPER_HI, alpha=0.8))
    c.drawPath(p, ink(4 / s))
    c.restore()


def sandal_icon(c, x, y, s):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    sole = smooth_path([(-30, -70), (30, -70), (36, 40), (24, 72), (-24, 72), (-36, 40)])
    c.drawPath(sole, fill(rgb("#8A5A3A")))
    c.drawPath(sole, ink(4 / s))
    for yy in (-30, 10, 44):
        c.drawLine(-38, yy, 38, yy - 10, ink(9, col=rgb("#4A2E1E")))
    c.restore()


def pants_icon(c, x, y, s):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    p = smooth_path([(-64, -40), (64, -40), (60, 0), (20, 44), (-20, 44), (-60, 0)])
    c.drawPath(p, fill(PAPER_HI))
    mottle(c, p, PAPER, alpha=0.3, scale=0.04)
    c.drawPath(rrect(-66, -46, 132, 16, 6), fill(SEAL))
    c.drawPath(p, ink(4 / s))
    c.restore()


def letter_shot(c, t):
    """The letter on a dark table; the three things it lists pop out of it, one by one, as they are said."""
    a = shot_start("letter")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    table = rrect(-10, -10, W + 20, H + 20, 0)
    c.drawPath(table, fill(rgb("#4A3426")))
    woodgrain(c, table, alpha=0.35, seed=12)
    k_in = ease_io(prog(t, a, a + 0.35))
    z = 1.0 + 0.04 * prog(t, a, shot_end(a))
    c.save()
    c.translate(450, 800)
    c.scale(z, z)
    c.translate(-450, -800)
    leaf_tablet(c, 450, 650 + (1 - k_in) * 300, 700, 330, rot=-3, seed=21, rows=6,
                hl=(1, 3, 4), hl_k=prog(t, WT("n9", "socks") - 0.2, WT("n9", "underpants") + 0.3))
    c.restore()
    for j, (word, lab) in enumerate((("socks", "SOCKS"), ("sandals", "SANDALS"), ("underpants", "UNDERPANTS"))):
        tk = WT("n9", word)
        k = ease_io(prog(t, tk - 0.15, tk + 0.2))
        if k <= 0:
            continue
        x, y = 210 + j * 240, 960 - 30 * math.sin(k * math.pi)
        c.save()
        c.translate(x, y)
        c.scale(0.6 + 0.4 * k, 0.6 + 0.4 * k)
        c.drawCircle(0, 0, 96, fill(PAPER_HI, k))
        c.drawCircle(0, 0, 96, ink(4, alpha=k))
        if j == 0:
            sock_icon(c, -16, 0, 0.9, SEAL)
        elif j == 1:
            sandal_icon(c, -26, 0, 0.75)
            sandal_icon(c, 26, 6, 0.75)
        else:
            pants_icon(c, 0, -14, 0.8)
            pants_icon(c, 0, 34, 0.6)
        if j > 0:                                   # the "x2" badge
            c.drawCircle(70, -70, 34, fill(SEAL, k))
            text(c, "×2", 70, -56, font("display", 38), FOAM, align="center", alpha=k)
        c.restore()
        text(c, lab, x, y + 142, font("mono", 34), FOAM, align="center", alpha=k, stroke=8)
    if t >= a + 0.3:
        text(c, "FOUND AT VINDOLANDA", CAP_CX, 420, font("mono", 40), YEL_L, align="center",
             alpha=ease_io(prog(t, a + 0.3, a + 0.6)) * (1 - prog(t, WT("n9", "socks") - 0.4, WT("n9", "socks") - 0.1)),
             stroke=8)


# ---------------------------------------------------------------- beer: the barrel runs dry
def beer_shot(c, t):
    """The officer's letter pinned on the barrack wall, the barrel below: at 'no beer' the tap gives one sad
    drop and the stamp lands."""
    a = shot_start("beer")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    tw = twos(t)
    wall = rrect(-10, -10, W + 20, H + 20, 0)
    c.drawPath(wall, fill(TIMBER_L))
    for yy in range(0, H, 60):
        c.drawLine(0, yy, W, yy, ink(3, col=TIMBER, alpha=0.8))
    woodgrain(c, wall, alpha=0.25, seed=14)
    c.drawRect(skia.Rect.MakeXYWH(0, 1300, W, 700), fill(rgb("#5E4A38")))
    c.drawLine(0, 1300, W, 1300, ink(4))
    k_in = ease_io(prog(t, a, a + 0.3))
    leaf_tablet(c, 450, 560 + (1 - k_in) * -200, 560, 260, rot=4, seed=33, rows=5,
                hl=(2,), hl_k=prog(t, WT("n10", "no") - 0.1, WT("n10", "beer") + 0.3))
    c.drawCircle(450, 440, 12, fill(IRON))               # the nail
    z = 1.0 + 0.22 * ease_io(prog(t, a, shot_end(a)))
    c.save()
    c.translate(420, 1300)
    c.scale(z, z)
    c.translate(-420, -1300)
    tn0 = WT("n10", "beer")
    rock = 7 * math.sin((t - tn0) * 9) * math.exp(-(t - tn0) * 1.5) if t > tn0 else 0.0
    c.save()
    c.translate(380, 1300)
    c.rotate(rock)
    c.translate(-380, -1300)
    barrel(c, 380, 1300, s=1.15, boil=boil)
    c.restore()
    # the cup under the tap and the single drop
    cup = smooth_path([(560, 1210), (640, 1210), (630, 1296), (570, 1296)])
    c.drawPath(cup, fill(rgb("#B9814E")))
    c.drawPath(cup, ink(4, boil=boil))
    tn = WT("n10", "beer")
    for j in range(3):
        ph = ((t - tn) * 1.1 + j * 0.33) % 1.0 if t >= tn else -1
        if 0 <= ph < 1 and j == 0:
            dy = 1200 + 90 * ph * ph
            drop = smooth_path([(598, dy - 14), (605, dy + 2), (598, dy + 9), (591, dy + 2)])
            c.drawPath(drop, fill(rgb("#D9A441"), 1 - ph))
            c.drawPath(drop, ink(2.5, alpha=1 - ph))
    c.restore()
    if t >= tn + 0.1:
        stamp(c, CAP_CX, 940, "NO BEER", size=110, k=prog(t, tn + 0.1, tn + 0.35), rot=-6)


# ---------------------------------------------------------------- duck: the bathhouse
def duck_shot(c, t):
    """Inside the bathhouse: a stone vault, a warm pool, steam curling up; the duck floats, perfectly content."""
    a = shot_start("duck")
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 0.9)
    z = 1.0 + 0.06 * prog(t, a, shot_end(a))
    c.save()
    c.translate(450, 980)
    c.scale(z, z)
    c.translate(-450, -980)
    c.drawRect(skia.Rect.MakeWH(W, H), fill(rgb("#C8B79A")))
    for row in range(14):                               # ashlar blocks
        y = 120 + row * 70
        off = 60 if row % 2 else 0
        for col in range(-1, 9):
            x = col * 140 + off
            c.drawPath(rrect(x + 3, y + 3, 134, 64, 4), fill(mixc(STONE_L, STONE, (row * 7 + col * 3) % 5 / 8)))
            c.drawPath(rrect(x + 3, y + 3, 134, 64, 4), ink(2, alpha=0.45))
    arch = skia.Path()
    arch.addArc(skia.Rect.MakeLTRB(90, 160, 810, 880), 180, 180)
    c.drawPath(arch, ink(40, col=STONE_D))
    c.drawPath(arch, ink(4, boil=boil))
    win = skia.Path()
    win.addArc(skia.Rect.MakeLTRB(330, 330, 570, 570), 180, 180)
    win.lineTo(570, 640)
    win.lineTo(330, 640)
    win.close()
    c.drawPath(win, fill(rgb("#9FB4C8")))
    snowfall(c, tw, density=14, alpha=0.9, seed=3, area=(330, 330, 240, 310))
    c.drawPath(win, ink(4, boil=boil))
    # the pool
    pool = rrect(20, 1030, 860, 420, 26)
    c.drawPath(rrect(0, 990, 900, 80, 14), fill(STONE_D))
    c.drawPath(pool, fill(rgb("#6FA3B8")))
    mottle(c, pool, rgb("#4E8197"), alpha=0.3, scale=0.01)
    for j in range(6):
        y = 1080 + j * 60
        p = skia.Path()
        for i in range(10):
            x = 40 + i * 92
            (p.moveTo if i == 0 else p.lineTo)(x, y + 6 * math.sin(i * 1.4 + tw * 3 + j))
        c.drawPath(p, ink(3, col=FOAM, alpha=0.6))
    c.drawPath(pool, ink(5, boil=boil))
    steam(c, tw, 450, 1080, w=760, n=8, alpha=0.75, height=640)
    bob = 6 * math.sin(tw * 2.2)
    draw_duck(c, 450, 1150 + bob, s=2.4, boil=boil, tilt=-3 + 2 * math.sin(tw * 1.7), look=0.4)
    c.restore()


# ---------------------------------------------------------------- latrine: seats side by side
def latrine_shot(c, t, sponge=False):
    """A Roman fort latrine: a long wooden seat with keyhole openings side by side, no walls between them, a
    gutter of running water at our feet. sponge=True: tight on the gutter, where a sponge on a stick leans."""
    a = shot_start("sponge" if sponge else "latrine")
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 0.9)
    if sponge:
        z = 1.7 + 0.12 * prog(t, a, shot_end(a))
        fx, fy = 640, 1150
    else:
        z = 1.0 + 0.05 * prog(t, a, shot_end(a))
        fx, fy = 450, 900
    c.save()
    c.translate(450 if not sponge else 470, 900 if not sponge else 960)
    c.scale(z, z)
    c.translate(-fx, -fy)
    if not sponge:
        c.translate(0, -160)                            # the gutter clear of the caption line
    c.drawRect(skia.Rect.MakeXYWH(-100, -100, W + 200, H + 400), fill(rgb("#B9A88C")))
    for row in range(11):                               # the stone wall behind
        y = 80 + row * 64
        for col in range(-1, 9):
            x = col * 150 + (75 if row % 2 else 0)
            c.drawPath(rrect(x + 3, y + 3, 144, 58, 4), fill(mixc(STONE_L, STONE, (row * 5 + col * 2) % 4 / 6)))
            c.drawPath(rrect(x + 3, y + 3, 144, 58, 4), ink(2, alpha=0.4))
    # the seat board, seen a little from above: a long plank
    top = skia.Path()
    top.moveTo(-40, 800)
    top.lineTo(W + 40, 800)
    top.lineTo(W + 40, 930)
    top.lineTo(-40, 930)
    top.close()
    c.drawPath(top, fill(TIMBER_L))
    woodgrain(c, top, alpha=0.3, seed=2)
    c.drawPath(top, ink(4, boil=boil))
    # the front board, and under each opening the slot that runs down the front (the Roman 'keyhole')
    front = rrect(-40, 930, W + 40 + 40, 230, 0)
    c.drawPath(front, fill(TIMBER))
    woodgrain(c, front, alpha=0.3, seed=3)
    for j in range(6):
        x = 90 + j * 150
        hole = oval(x, 862, 56, 30)
        c.drawPath(hole, fill(rgb("#24170F")))
        c.drawPath(hole, ink(3.5))
        slot = rrect(x - 11, 880, 22, 140, 8)
        c.drawPath(slot, fill(rgb("#24170F")))
        c.drawPath(slot, ink(3))
    c.drawPath(front, ink(4, boil=boil))
    c.drawRect(skia.Rect.MakeXYWH(-40, 1160, W + 80, 900), fill(STONE))
    mottle(c, rrect(-40, 1160, W + 80, 900, 0), STONE_D, alpha=0.25, scale=0.01)
    # the gutter of running water in front of the seats
    ch = rrect(-40, 1180, W + 80, 70, 10)
    c.drawPath(ch, fill(WATER))
    for i in range(9):
        x = ((i * 130 + tw * 120) % (W + 140)) - 70
        c.drawLine(x, 1215, x + 46, 1215, ink(4, col=WHITE, alpha=0.75))
    c.drawPath(ch, ink(4, boil=boil))
    # the sponge on its stick, leaning in the gutter
    sx0, sy0, sx1, sy1 = 660, 1230, 770, 900
    c.drawLine(sx0, sy0, sx1, sy1, ink(12, col=TIMBER_D))
    c.drawLine(sx0, sy0, sx1, sy1, ink(2.5))
    sp = smooth_path([(sx0 - 40, sy0 - 26), (sx0 - 10, sy0 - 58), (sx0 + 34, sy0 - 50), (sx0 + 46, sy0 - 14),
                      (sx0 + 20, sy0 + 12), (sx0 - 28, sy0 + 6)])
    c.drawPath(sp, fill(rgb("#E8C86A")))
    for (dx, dy) in ((-14, -30), (8, -38), (24, -20), (-4, -10), (16, -2)):
        c.drawCircle(sx0 + dx, sy0 + dy, 5, fill(rgb("#B8963A")))
    c.drawPath(sp, ink(3.5, boil=boil))
    c.restore()
    if not sponge:
        tn = WT("n12", "No")
        ts = WT("n12", "side")
        if t >= ts - 0.1:                               # the bracket: seat, seat, seat
            k = ease_io(prog(t, ts - 0.1, ts + 0.3)) * (1 - prog(t, tn - 0.2, tn))
            for j in range(5):
                x0 = 90 + j * 150
                p = skia.Path()
                p.moveTo(x0 + 20, 600)
                p.quadTo(x0 + 75, 540, x0 + 130, 600)
                c.drawPath(p, ink(5, col=SEAL, alpha=k))
        if t >= tn - 0.05:
            stamp(c, CAP_CX, 470, "NO CUBICLES", size=96, k=prog(t, tn - 0.05, tn + 0.2), rot=-6)
    else:
        ts = WT("n13", "shared")
        if t >= ts - 0.05:
            stamp(c, CAP_CX, 560, "SHARED", size=110, k=prog(t, ts - 0.05, ts + 0.2), rot=-6)


# ---------------------------------------------------------------- mud: the ground in cross-section
def ground_section(c, t, reveal=0.0, boil=None, glow=0.0, dig=0.0):
    """The ground under the fort as a carved cutaway: snow on top, brown soil bands, then the dark, wet,
    airless layer where wood does not rot. reveal 0..1 = the tablets in it show; glow = a '?' tease;
    dig 0..1 = a trowel lifts one out."""
    tw = twos(t)
    top = 470
    winter_sky(c, tw, horizon=top, sun=None)
    palisade(c, -40, 1120, top + 4, 160, boil=boil, snow=1.0, seed=8, post_w=34)
    bands = [(top, 40, SNOW), (top + 40, 170, rgb("#7D6448")), (top + 210, 200, rgb("#6A5038")),
             (top + 410, 520, rgb("#3A2B1F")), (top + 930, 700, rgb("#2C211A"))]
    for y, h, col in bands:
        p = skia.Path()
        p.moveTo(-20, y + 8 * math.sin(y))
        for i in range(1, 12):
            p.lineTo(i * 100, y + 10 * math.sin(i * 1.1 + y))
        p.lineTo(W + 20, y + h + 40)
        p.lineTo(-20, y + h + 40)
        p.close()
        c.drawPath(p, fill(col))
        mottle(c, p, col, alpha=0.25, scale=0.012, seed=int(y) % 50)
        c.drawPath(smooth_path([(i * 100 - 20, y + 10 * math.sin(i * 1.1 + y)) for i in range(13)], closed=False),
                   ink(3, alpha=0.7, boil=boil))
    rng = np.random.default_rng(4)
    for _ in range(40):                                  # pebbles
        x, y = rng.uniform(0, W), rng.uniform(top + 60, top + 400)
        c.drawPath(oval(x, y, rng.uniform(6, 16), rng.uniform(4, 10)), fill(rgb("#9C8A70"), 0.8))
    # water seeping in the deep layer: thin wavy blue lines
    for j in range(5):
        y = top + 460 + j * 90
        p = skia.Path()
        for i in range(12):
            (p.moveTo if i == 0 else p.lineTo)(i * 100 - 20, y + 6 * math.sin(i * 1.7 + tw * 1.5 + j))
        c.drawPath(p, ink(3, col=rgb("#6FA3B8"), alpha=0.45))
    if glow > 0:
        for j, (x, y) in enumerate(((260, top + 450), (620, top + 520), (430, top + 600))):
            ph = 0.6 + 0.4 * math.sin(tw * 4 + j)
            g = skia.Paint(AntiAlias=True)
            g.setShader(skia.GradientShader.MakeRadial((x, y), 120, [skia.Color4f(1, 0.85, 0.4, 0.45 * glow * ph),
                                                                      skia.Color4f(1, 0.85, 0.4, 0)]))
            c.drawCircle(x, y, 120, g)
            text(c, "?", x, y + 30, font("display", 90), YEL_L, align="center", alpha=glow, stroke=10)
    if reveal > 0:
        spots = [(200, top + 600, -12), (520, top + 660, 8), (330, top + 790, 4), (690, top + 820, -6),
                 (150, top + 880, 10), (480, top + 960, -3), (740, top + 600, 14)]
        for j, (x, y, r) in enumerate(spots):
            kj = ease_io(prog(reveal, j * 0.08, j * 0.08 + 0.4))
            if kj <= 0:
                continue
            lift = 0.0
            if j == 1 and dig > 0:
                lift = ease_io(dig)
            leaf_tablet(c, x, y - 640 * lift, 190, 86, rot=r * (1 - lift), seed=40 + j, rows=3, alpha=kj)
        if dig > 0:                                     # the trowel (no hand: it is an archaeologist's tool)
            kx, ky = 640, top + 560 - 600 * ease_io(dig)
            tr = skia.Path()
            tr.moveTo(kx - 120, ky + 40)
            tr.lineTo(kx - 20, ky - 10)
            tr.lineTo(kx - 10, ky + 40)
            tr.close()
            c.drawPath(tr, fill(rgb("#9AA3AD")))
            c.drawPath(tr, ink(4))
            c.drawLine(kx - 15, ky + 10, kx + 90, ky - 40, ink(22, col=TIMBER_D))
            c.drawLine(kx - 15, ky + 10, kx + 90, ky - 40, ink(3))


def mud_shot(c, t):
    a = shot_start("mud")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    z = 1.0 + 0.08 * ease_io(prog(t, a, shot_end(a)))
    c.save()
    c.translate(450, 1100)
    c.scale(z, z)
    c.translate(-450, -1100)
    ground_section(c, t, glow=ease_io(prog(t, WT("n15", "underground") - 0.2, WT("n15", "underground") + 0.3)), boil=boil)
    c.restore()


def dig_shot(c, t):
    a = shot_start("dig")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    ground_section(c, t, reveal=prog(t, a + 0.1, WT("n19", "letters") + 0.6), boil=boil,
                   dig=prog(t, WT("n19", "dug") - 0.1, E["n19"] - 0.2))
    t73 = a + 0.4
    t17 = WT("n19", "mud")
    rows = []
    if t >= t73:
        rows = [("FIRST FOUND", "1973", SEAL, max(0.0, 1 - (t - t73) * 3))]
    if t >= t17:
        rows = [("TABLETS FOUND", "1,700+", SEAL, max(0.0, 1 - (t - t17) * 3))]
    if rows:
        hud_card(c, SAFE_X0, 290, rows, alpha=ease_io(prog(t, t73, t73 + 0.25)), w=600)


# ---------------------------------------------------------------- contract: the answer
def contract_shot(c, t):
    """25 winters as 25 snowflakes in a grid; the first one lit: you are here."""
    a = shot_start("contract")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    bg = rgb("#20395A")
    c.drawRect(skia.Rect.MakeWH(W, H), fill(bg))
    snowfall(c, twos(t), density=30, alpha=0.35, seed=6)
    t25 = WT("n16", "25")
    k_in = ease_io(prog(t, a, a + 0.3))
    x0, y0, step = 190, 560, 130
    for i in range(25):
        r_, c_ = divmod(i, 5)
        x, y = x0 + c_ * step, y0 + r_ * step
        ki = ease_io(prog(t, t25 - 0.2 + i * 0.03, t25 + 0.1 + i * 0.03)) * k_in
        if ki <= 0:
            continue
        col = YEL_L if i == 0 else FOAM
        for j in range(3):                             # a carved six-armed flake
            an = math.radians(j * 60 + 90)
            c.drawLine(x - 38 * math.cos(an) * ki, y - 38 * math.sin(an) * ki, x + 38 * math.cos(an) * ki,
                       y + 38 * math.sin(an) * ki, ink(6, col=col, alpha=0.9 if i == 0 else 0.6))
        if i == 0:
            c.drawCircle(x, y, 54, ink(5, col=SEAL))
    kh = ease_io(prog(t, t25 - 0.1, t25 + 0.2))
    if kh > 0 and t < WT("n16", "If"):
        hud_card(c, SAFE_X0, 290, [("YOU'RE IN FOR", "25 YEARS", SEAL, max(0.0, 1 - (t - t25) * 3))], alpha=kh, w=600)
    elif kh > 0:
        contract_bar(c, t, 290)
        text(c, "you are here", 300, 500, font("hand", 60), YEL_L, align="left", alpha=kh, stroke=10)
        p = skia.Path()
        p.moveTo(290, 470)
        p.quadTo(240, 480, 222, 520)
        c.drawPath(p, ink(5, col=YEL_L, alpha=kh))
    tm = WT("n16", "Minimum")
    if t >= tm - 0.05:
        stamp(c, CAP_CX, 1010, "MINIMUM", size=90, k=prog(t, tm - 0.05, tm + 0.2), rot=-6)


# ---------------------------------------------------------------- invite: the birthday invitation
def invite_shot(c, t):
    """The invitation, big: a scribe's neat lines, then two lines in another hand and darker ink: hers."""
    a = shot_start("invite")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    bg = rrect(-10, -10, W + 20, H + 20, 0)
    c.drawPath(bg, fill(rgb("#3E2C22")))
    woodgrain(c, bg, alpha=0.35, seed=19)
    z = 1.0 + 0.25 * ease_io(prog(t, a, E["n20"]))
    c.save()
    c.translate(450, 860)
    c.scale(z, z)
    c.translate(-450, -860)
    th = WT("n20", "hand")
    leaf_tablet(c, 450, 820, 740, 420, rot=-2, seed=61, rows=7, hand2=(5, 6),
                hl=(5, 6), hl_k=prog(t, WT("n20", "woman") - 0.3, th + 0.2))
    kc = prog(t, WT("n20", "woman") - 0.2, WT("n20", "woman") + 0.5)
    if kc > 0:                                       # an ink ring drawn round her own two lines
        ring_ = skia.Path()
        ring_.addOval(skia.Rect.MakeLTRB(90, 880, 810, 1050))
        meas = skia.PathMeasure(ring_, False)
        seg = skia.Path()
        meas.getSegment(0, meas.getLength() * kc, seg, True)
        c.drawPath(seg, ink(7, col=SEAL))
    c.restore()
    kb = ease_io(prog(t, WT("n20", "birthday") - 0.1, WT("n20", "birthday") + 0.2))
    if kb > 0:
        hud_card(c, SAFE_X0, 290, [("A BIRTHDAY PARTY", "11 SEPT", SEAL, max(0.0, 1 - (t - WT("n20", "birthday")) * 3))],
                 alpha=kb, w=600)
    tw_ = WT("n20", "woman")
    if t >= tw_:
        stamp(c, CAP_CX, 1110, "HER OWN HAND", size=76, k=prog(t, tw_, tw_ + 0.2), rot=-5, pop=0.2)


# ---------------------------------------------------------------- stamps
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
        hud_card(c, SAFE_X0 + 30, 476, [("YOU'RE IN FOR", "?? YEARS", SEAL, 0.0)], w=600)
    elif (shot in ("close", "catch", "tease") and not lvl and not lab_live and L["n8"] - 0.2 <= t < T_BLAST3
          and not (T_N2 <= t < T_N2 + 1.5)):
        contract_bar(c, t, y)
    if title_on:
        f1, f2 = font("mono", 38), font("display", 112)
        c.save()
        c.translate(CAP_CX, 262)
        c.rotate(-3)
        tag = "COULD YOU SURVIVE"
        wv = f1.measureText(tag)
        c.drawPath(rrect(-wv / 2 - 18, -40, wv + 36, 56, 10), fill(INKC, 0.92))
        text(c, tag, 0, 2, f1, YEL_L, align="center")
        for j, name in enumerate(("A ROMAN", "WINTER CAMP?")):
            c.save()
            sc = min(0.8, 640 / f2.measureText(name))
            c.translate(0, (92 + 82 * j))
            c.scale(sc, sc)
            text(c, name, 0, 0, f2, FOAM, align="center", stroke=22)
            c.restore()
        c.restore()
    ks = prog(t, 3.0, 3.3)
    if ks > 0 and shot != "end":
        seal(c, 874, 120, 86, alpha=ks)


def contract_bar(c, t, y):
    """The progress bar: your contract, day 1 of ???? — the end mark only shows once the answer is said."""
    x0, w = SAFE_X0, 600
    card = rrect(x0, y, w, 156, 14)
    c.drawPath(rrect(x0 + 8, y + 10, w, 156, 14), fill(INKC, 0.25))
    c.drawPath(card, fill(PAPER_HI, 0.96))
    mottle(c, card, PAPER, alpha=0.12, scale=0.03, seed=8)
    c.drawPath(card, ink(4))
    c.drawPath(rrect(x0 + 8, y + 8, w - 16, 140, 9), ink(1.6, alpha=0.7))
    text(c, "YOUR CONTRACT", x0 + 24, y + 46, font("mono", 32), mixc(INKC, PAPER, 0.3))
    known = t >= WT("n16", "25")
    text(c, "DAY 1", x0 + w - 24, y + 52, font("mono", 46), SEAL, align="right")
    bx, by, bw = x0 + 24, y + 86, w - 48
    c.drawPath(rrect(bx, by, bw, 26, 13), fill(rgb("#D9CDB0"), 0.8))
    c.drawPath(rrect(bx, by, 26, 26, 13), fill(SEAL))
    if known:
        for i in range(1, 25):                         # one tick per winter
            xx = bx + bw * i / 25
            c.drawLine(xx, by + 4, xx, by + 22, ink(2, alpha=0.5))
    c.drawPath(rrect(bx, by, bw, 26, 13), ink(3))
    text(c, "DAY 1", bx, by + 64, font("mono", 32), mixc(INKC, PAPER, 0.35))
    text(c, "DAY 9,131" if known else "DAY ????", bx + bw, by + 64, font("mono", 32),
         SEAL if known else mixc(INKC, PAPER, 0.35), align="right")


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
    if True:
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


def end_cards(c, t):
    a = L["n21"]
    if t < a:
        return
    gone = 1 - prog(t, L["n22"] - 0.25, L["n22"] - 0.05)      # cleared for her close-up and the countdown
    if gone <= 0:                                             # ... into one small strip until just before the flash
        ks = ease_io(prog(t, L["n22"] - 0.15, L["n22"] + 0.1)) * (1 - prog(t, E["n23"] - 0.35, E["n23"] - 0.1))
        if ks > 0:
            f = font("mono", 34)
            msg = "A MARS · B FARM · C POMPEII"
            wv = f.measureText(msg)
            x0 = CAP_CX - wv / 2 - 22
            c.drawPath(rrect(x0, 1060, wv + 44, 66, 14), fill(PAPER_HI, 0.95 * ks))
            c.drawPath(rrect(x0, 1060, wv + 44, 66, 14), ink(3, alpha=ks))
            text(c, msg, CAP_CX, 1105, f, INKC, align="center", alpha=ks)
        return
    opts = [("A", "MARS", "Mars"), ("B", "MEDIEVAL FARM", "medieval"), ("C", "POMPEII", "Pompeii")]
    dim = ease_io(prog(t, a, a + 0.4)) * gone
    c.drawRect(skia.Rect.MakeWH(W, H), fill(INKC, 0.12 * dim))
    for i, (letter, name, word) in enumerate(opts):
        tk = WT("n21", word)
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
    if i == 0:    # Mars: a red planet with craters
        c.drawCircle(x, y, 40, fill(rgb("#C8553A"), k))
        for dx, dy, r in ((-12, -10, 8), (14, 10, 6), (-4, 20, 5)):
            c.drawCircle(x + dx, y + dy, r, fill(rgb("#9A3C2A"), k))
        c.drawCircle(x, y, 40, ink(3, alpha=k))
    elif i == 1:  # a farm: a field in furrows and a haystack
        c.drawPath(rrect(x - 50, y - 6, 100, 44, 6), fill(rgb("#9C7A3C"), k))
        for j in range(4):
            c.drawLine(x - 46, y + 4 + j * 10, x + 46, y + 4 + j * 10, ink(2.5, col=rgb("#6E5226"), alpha=k))
        hs = smooth_path([(x - 24, y - 4), (x - 18, y - 34), (x, y - 44), (x + 18, y - 34), (x + 24, y - 4)])
        c.drawPath(hs, fill(YEL_L, k))
        c.drawPath(hs, ink(3, alpha=k))
        c.drawPath(rrect(x - 50, y - 6, 100, 44, 6), ink(3, alpha=k))
    else:         # Pompeii: a volcano with an ash cloud
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


def respawn_flash(c, t):
    a = E["n23"] + 0.02
    if t >= a:
        k = prog(t, a, DURATION)
        c.drawRect(skia.Rect.MakeWH(W, H), fill(PAPER_HI, ease_io(min(1, k * 1.6))))


def cam_close(t):
    """Camera on the close shot: a slow push-out over the hook, punch-ins on the NOPEs."""
    z = 1.0
    if t < shot_start("map"):
        z = 1.10 - 0.10 * ease_io(prog(t, 0.4, shot_start("map")))
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
            z = 1.10 + 0.08 * ease_io(prog(t, L["n21"], DURATION))
            dyc = 70.0
        if z != 1.0 or dyc:
            c.translate(XH, YH + dyc)
            c.scale(z, z)
            c.translate(-XH, -YH)
        close_shot(c, t)
    elif shot == "catch":                     # a little tighter: the letter drops into her hands
        z = 1.18
        c.translate(XH, YH + 60)
        c.scale(z, z)
        c.translate(-XH, -YH)
        close_shot(c, t)
    elif shot == "tease":                     # slow push in on her and the letter
        z = 1.12 + 0.1 * ease_io(prog(t, shot_start("tease"), shot_end(shot_start("tease"))))
        c.translate(XH, YH + 60)
        c.scale(z, z)
        c.translate(-XH, -YH)
        close_shot(c, t)
    elif shot == "plead":
        z = 1.5
        c.translate(XH, 830)
        c.scale(z, z)
        c.translate(-XH, -YH)
        close_shot(c, t)
    elif shot == "map":
        map_shot(c, t)
    elif shot == "march":
        march_shot(c, t)
    elif shot == "pack":
        pack_shot(c, t)
    elif shot == "report":
        report_shot(c, t)
    elif shot == "letter":
        letter_shot(c, t)
    elif shot == "beer":
        beer_shot(c, t)
    elif shot == "duck":
        duck_shot(c, t)
    elif shot == "latrine":
        latrine_shot(c, t)
    elif shot == "sponge":
        latrine_shot(c, t, sponge=True)
    elif shot == "mud":
        mud_shot(c, t)
    elif shot == "contract":
        contract_shot(c, t)
    elif shot == "dig":
        dig_shot(c, t)
    elif shot == "invite":
        invite_shot(c, t)
    c.restore()
    paper_over(c, 1.0)
    vignette(c, 0.24)
    hud(c, t)
    intercom(c, t)
    end_cards(c, t)
    nope_text(c, t)
    captions(c, t)
    respawn_flash(c, t)
