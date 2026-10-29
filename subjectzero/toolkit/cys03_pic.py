"""COULD YOU SURVIVE? #03 — Death Valley: the picture (2D estampe look, sz2d.py). Timed on out/cys03_lines.json.

    python3 sz2render.py cys03_pic                # -> out/cys03_pic_video.mp4
    python3 sz2render.py cys03_pic --sheet 0 2 5 ...

Shots (named, none held longer than 8 s): close (her standing on the Badwater salt flat, bottle in hand, the mirage
lake and a far dust devil on the horizon) → map (the world: the hottest air ever recorded, 1913) → close ("I brought
water!") → bottle (one litre vs the clock: drink it every hour) → close (the lab, NOPE 1: the crust cracks around her
boots) → boots (low, on her boots: the ground is the hottest thing) → thermo (air 134 °F, ground 201 °F, water boils
212 °F) → close (NOPE 2: the far dust devil arrives and rips across the flat) → duck (it floats on the mirage) →
night (stars, and still over 100 °F) → close (the tease) → days (the answer: about two days, bottle or not, in shade)
→ wide (no shade anywhere: her own shadow is all of it) → close (NOPE 3: the salt flat shatters) → trail (1849: the
lost wagons cross the valley) → ridge (they leave over the mountains: the name) → end (the next spawns, respawn).
HUD: the air temperature counts up to 134 °F, then the progress bar is the bottle itself, "WATER LEFT", draining
sip by sip toward empty — and the answer says it barely matters.
"""
import json
import math
import os

import numpy as np
import skia

from sz2d import (W, H, FPS, rgb, mixc, fill, ink, text, smooth_path, rrect, oval, ease_io, prog, font, mist_band,
                  draw_hero, draw_duck, paper_over, vignette, seal, mottle, words_caption, hud_card, peak, thermometer,
                  desert_sky, heat_haze, mirage, SaltFlat, dust_devil, water_bottle, draw_legs, covered_wagon, woodgrain,
                  PAPER, PAPER_HI, INKC, PRUSSIAN, CORAL, SEAL, FOAM, YEL, YEL_D, YEL_L, WHITE, SAFE_X0, SAFE_X1, CAP_CX,
                  SAND, SAND_D, SAND_L, SALT, SALT_SH, SALT_D, DESERT_ROSE, DESERT_ROSE_D, WATER)
import cys03 as EP

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
EPNAME = "cys03_pic"
DURATION = EP.DURATION

_js = json.load(open(os.path.join(OUT, "cys03_lines.json"), encoding="utf-8"))
L = {l["key"]: l["t"] for l in _js["lines"]}
DUR = {l["key"]: l["dur"] for l in _js["lines"]}
WHO = {l["key"]: l["who"] for l in _js["lines"]}
TXT = {l["key"]: l["text"] for l in _js["lines"]}
E = {k: L[k] + DUR[k] for k in L}
KEYS = sorted(L, key=lambda k: L[k])
ENV = {w: np.load(os.path.join(OUT, f"cys03_env_{w}.npy")) for w in ("N", "HERO", "LAB")}

# what the captions show (numbers as figures; the voice says them in words)
CAP = {"n2": "July. The air here once hit 134°F.", "n5": "One liter. Above 100°F, the army says drink that every hour.",
       "n9": "The ground once hit 201°F.", "n10": "11 degrees short of boiling water.",
       "n14": "Even at night, it can stay over 100°F.", "n16": "About 2 days.",
       "n20": "The twist? In 1849, lost travelers crossed this valley.", "n24": "Respawning in 3... 2..."}
# how long a caption word takes to SAY (characters of the spoken words), so a figure lights up when it is said
SAYLEN = {"134°F.": 29, "100°F,": 18, "201°F.": 23, "11": 6, "100°F.": 10, "2": 3, "1849,": 20, "3...": 6, "2...": 4}
NOPES = {"n7": 1, "n11": 2, "n19": 3}
XH, YH, HS = 450, 800, 0.95            # her head in the close shot, and her scale
HORIZON = 980
FLAT = SaltFlat(horizon=HORIZON, cx=XH, f=1000.0, cam_h=1.6, r=1.5, seed=3)
Z_FEET = 1.6 * 1000.0 / (YH + 640 * HS - HORIZON)       # where her boots stand on the crust (m)
DUCK_FAR = (700, HORIZON - 6)          # the duck, tiny, on the mirage lake


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
    (WT("n2", "once") - 0.1, "heat"),     # the thermometer climbs to 134
    (L["n3"] - 0.05, "map"),              # the hottest air ever recorded
    (L["n4"] - 0.1, "close"),             # "It's fine. I brought water!"
    (WT("n5", "Above") - 0.05, "bottle"), # one litre vs the clock
    (L["n6"] - 0.3, "close"),             # the lab; NOPE 1
    (L["n8"] - 0.05, "boots"),            # but the air isn't the hottest thing here
    (L["n9"] - 0.05, "thermo"),           # air, ground, boiling water
    (L["n11"] - 0.15, "close"),           # NOPE 2: the dust devil
    (WT("n12", "only") - 0.1, "duck"),    # the only lake for miles: a mirage
    (L["n14"] - 0.05, "night"),           # even the nights
    (L["n15"] - 0.05, "close"),           # the tease
    (L["n16"] - 0.05, "days"),            # the answer
    (WT("n17", "Only") - 0.1, "close"),   # only resting in shade: she looks around for some
    (L["n18"] - 0.1, "wide"),             # there is no shade
    (L["n19"] - 0.15, "close"),           # NOPE 3
    (L["n20"] + 0.5, "trail"),            # 1849
    (L["n21"] - 0.05, "ridge"),           # goodbye, Death Valley
    (L["n22"] - 0.05, "end"),             # the next spawns
    (L["n23"] - 0.1, "plead"),            # "Somewhere cold. Please." tight on her
    (L["n24"] - 0.05, "end"),             # the countdown
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


# ---------------------------------------------------------------- NOPE machinery (as #01, #02)
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
T_N1 = L["n7"] + 0.15                 # damage lands on / just after each word
T_N2 = L["n11"] + 0.25


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


# ---------------------------------------------------------------- the water left in her bottle (the HUD bar)
SIPS = [(L["n6"] + 0.2, 1.0, 0.7), (L["n13"] - 0.3, 0.7, 0.45), (L["n15"] + 0.4, 0.45, 0.2), (WT("n17", "no"), 0.2, 0.0)]


def water_left(t):
    v = 1.0
    for a, v0, v1 in SIPS:
        if t >= a:
            v = v0 + (v1 - v0) * ease_io(prog(t, a, a + 0.8))
    return v


# ---------------------------------------------------------------- her state in the close shots
def hero_state(t):
    st = dict(face="worried", arms="none", shiver=0.0, look=None, squash=0.0, blink=0.0, mouth_open=None, tilt=0.0,
              hop=0.0, bottle="hand")
    for b in (2.6, 6.0, 12.4, 19.0, 26.9, 33.2, 37.8, 45.1, 53.0, 59.4, 63.4):
        if b <= t <= b + 0.12:
            st["blink"] = 1.0
    if t < 0.6:                                    # spawn: a squash bounce as she lands
        st["face"] = "shock"
        k = t / 0.6
        st["squash"] = 0.45 * math.sin(k * math.pi * 2) * (1 - k)
    elif t < E["n2"]:
        st["face"] = "shock" if t > WT("n2", "134") + 0.4 else "worried"
        st["look"] = (10, -8) if t < WT("n2", "134") else (8 * math.sin(t * 2.2), 4)
        st["arms"] = "fan" if t > WT("n2", "134") + 0.3 else "none"
    elif L["n4"] - 0.2 <= t < L["n5"] + 0.6:       # "It's fine. I brought water!": bottle held up, proud
        st["face"] = "happy"
        st["arms"] = "raise"
        st["bottle"] = "up"
        st["mouth_open"] = 0.4 + 1.1 * env("HERO", t)
    elif L["n6"] - 0.3 <= t < L["n7"]:             # the lab: she gulps it down
        st["face"] = "deadpan"
        st["arms"] = "raise"
        st["bottle"] = "drink" if t < L["n6"] + 1.2 else "up"
        st["look"] = (10, -4)
    elif L["n11"] - 0.3 <= t < L["n12"]:
        st["face"] = "shock"
        st["hop"] = 0.0
    elif L["n12"] <= t < shot_start("duck"):
        st["face"] = "shock"
        st["look"] = (12, -2)
    elif L["n15"] - 0.1 <= t < L["n16"]:          # the tease: she fans herself, sweating, and looks at the bottle
        st["face"] = "worried"
        st["arms"] = "fan"
        st["shiver"] = 0.15
        if t > WT("n15", "answer"):
            st["arms"] = "raise"
            st["bottle"] = "up"
            st["look"] = (12, -10)
    elif WT("n17", "Only") - 0.1 <= t < L["n18"] + 0.5:   # looking around for shade
        st["face"] = "worried"
        st["arms"] = "fan"
        st["look"] = (14 * math.sin(t * 3.0), 2)
    elif L["n22"] - 0.1 <= t:
        st["face"] = "deadpan"
        st["arms"] = "fan"
        if L["n23"] - 0.1 <= t < L["n24"]:          # "Somewhere cold. Please."
            st["face"] = "worried"
            st["arms"] = "hug"
            st["look"] = (0, -8)
            st["mouth_open"] = 0.5 + 1.1 * env("HERO", t)
        elif t >= L["n24"]:
            st["face"] = "worried"
            st["arms"] = "none"
    if E["n19"] + 0.4 <= t < L["n22"]:
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
        st["bottle"] = "hand" if lvl == 1 else "none"
        st["tilt"] = (0.0, -6.0, 0.0)[lvl - 1]
        if lvl == 2:                                 # NOPE 2: she hops off the hot ground
            st["hop"] = math.sin(min(1.0, k * 1.6) * math.pi) * 0.9
    if st["arms"] in ("up", "fan", "hug") and st["bottle"] in ("up", "drink"):
        st["bottle"] = "hand"
    return st


# ---------------------------------------------------------------- pieces of the close shot
def mountains(c, t, boil, y0=HORIZON, night=0.0):
    """The Panamint Range behind the flat (Telescope Peak, two miles above Badwater), rose and ochre bands."""
    far = mixc(mixc(DESERT_ROSE, PAPER, 0.35), rgb("#2A3550"), night * 0.7)
    near = mixc(DESERT_ROSE_D, rgb("#1E2840"), night * 0.7)
    peak(c, [(-60, y0 - 120), (90, y0 - 210), (210, y0 - 170), (330, y0 - 300), (420, y0 - 250), (540, y0 - 330),
             (660, y0 - 240), (790, y0 - 280), (930, y0 - 190), (1140, y0 - 230)], col=far, seed=13, boil=boil, line=3,
         alpha=0.95)
    tw = twos(t)
    mist_band(c, -120 + 5 * tw, y0 - 210, 420, 30, alpha=0.75 * (1 - night), col=mixc(PAPER_HI, SAND_L, 0.4))
    mist_band(c, 600 - 4 * tw, y0 - 150, 520, 26, alpha=0.7 * (1 - night), col=mixc(PAPER_HI, SAND_L, 0.4))
    peak(c, [(-60, y0 - 40), (120, y0 - 100), (260, y0 - 60), (420, y0 - 120), (560, y0 - 70), (700, y0 - 110),
             (880, y0 - 50), (1140, y0 - 90)], col=near, seed=17, boil=boil, line=3.5, hatch=True)
    # the alluvial fans spreading onto the flat
    for (x, w) in ((180, 260), (620, 300), (960, 240)):
        fan = smooth_path([(x - w, y0 + 2), (x - 30, y0 - 50), (x + 30, y0 - 50), (x + w, y0 + 2)])
        c.drawPath(fan, fill(mixc(SAND, rgb("#2A3550"), night * 0.6), 0.9))


def hero_shadow(c, x, y, s, k=1.0):
    """Noon: her shadow is a small puddle right under her boots."""
    c.drawPath(oval(x, y, 190 * s, 34 * s), fill(rgb("#7E6B55"), 0.45 * k))


def close_shot(c, t, s=HS, cam=(1.0, 0.0)):
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 1.0)
    lvl, nk = nope_at(t)
    desert_sky(c, tw, horizon=HORIZON, sun=(760, 380), sun_r=96)
    mountains(c, t, boil)
    # the mirage lake and the duck on it (there from frame 0, paid off at n12)
    mirage(c, tw, 560, 900, HORIZON - 2, h=24, boil=boil)
    duck_fly3 = prog(t, T_BLAST3, T_BLAST3 + 1.4)
    draw_duck(c, DUCK_FAR[0], DUCK_FAR[1] - 4 - 4 * math.sin(tw * 2), s=0.3, boil=None, tilt=-3)
    # the crust; NOPE 1 cracks it round her boots, NOPE 3 throws the near plates
    shat = prog(t, T_BLAST3, T_BLAST3 + 1.15)
    FLAT.draw(c, tw, boil=boil, crack=prog(t, T_N1, T_N1 + 0.9) if t < T_BLAST3 else 0.0,
              u0=0.0, z0=Z_FEET, shatter=shat if shat < 1 else 0.0)
    heat_haze(c, tw, HORIZON - 30, HORIZON + 160, alpha=0.55, n=6)
    # the dust devil: far and small from frame 0, it arrives with NOPE 2 and rips across the flat
    dd_far = (170 + 6 * tw, HORIZON + 8, 150)
    if t < T_N2:
        dust_devil(c, dd_far[0], dd_far[1], dd_far[2], tw, k=0.55, alpha=0.8, boil=boil)
    st = hero_state(t)
    feet_y = YH + 640 * s
    hero_shadow(c, XH, feet_y - 6, s, k=1.0 - 0.7 * st["hop"])
    draw_legs(c, XH, YH, s=s, boil=boil, t=tw, hop=st["hop"], squash=st["squash"], shiver=st["shiver"])
    hy = YH - 160 * s * st["hop"]
    if st["bottle"] == "hand":                      # the bottle in her left hand, at her side
        water_bottle(c, XH - 175 * s, hy + 330 * s, s=0.42 * s, level=water_left(t), boil=boil, rot=8)
    draw_hero(c, XH, hy, s=s, face=st["face"], boil=boil, arms=st["arms"], t=tw, blink=st["blink"],
              squash=st["squash"], look=st["look"], shiver=st["shiver"], mouth_open=st["mouth_open"], tilt=st["tilt"])
    if st["bottle"] == "up":
        water_bottle(c, XH + 196 * s, hy - 120 * s, s=0.5 * s, level=water_left(t), boil=boil, rot=6)
    elif st["bottle"] == "drink":                 # tipped to her mouth
        water_bottle(c, XH + 110 * s, hy + 10 * s, s=0.5 * s, level=water_left(t), boil=boil, rot=-62)
    # sweat drops (it gets worse through the episode)
    sweat = min(1.0, 0.3 + t / 40.0)
    for j in range(int(2 + 3 * sweat)):
        ph = (tw * 0.9 + j * 0.31) % 1.0
        sx = XH + (-96 + 46 * j) * s
        sy = hy + (-60 + 120 * ph) * s
        drop = smooth_path([(sx, sy - 14), (sx + 8, sy + 2), (sx, sy + 9), (sx - 8, sy + 2)])
        c.drawPath(drop, fill(rgb("#BFE0EC"), 0.9 * (1 - ph)))
        c.drawPath(drop, ink(2.5, alpha=0.8 * (1 - ph)))
    if t >= T_N2:                                    # NOPE 2: it whips across in front of her
        kk = prog(t, T_N2, T_N2 + 1.5)
        if kk < 1:
            x = -60 + (1160 + 60) * ease_io(kk)
            y = 1500 - 40 * math.sin(kk * math.pi)
            dust_devil(c, x, y, 1150, tw, k=min(1.0, 0.4 + kk * 2.2), alpha=1.0 - max(0.0, kk - 0.85) * 6.6, boil=boil)
            rng = np.random.default_rng(8)
            for j in range(12):                       # salt plates flung out of its path
                ph = min(1.0, kk * 1.3 + j * 0.02)
                px = x - 80 + rng.uniform(-60, 60) + 300 * ph
                py = y - rng.uniform(100, 600) * math.sin(ph * math.pi) - 20
                r_ = rng.uniform(16, 34)
                c.save()
                c.translate(px, py)
                c.rotate(400 * ph * rng.uniform(-1, 1))
                hx = skia.Path()
                hx.addPoly([skia.Point(r_ * math.cos(a), r_ * 0.7 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 7)[:-1]], True)
                c.drawPath(hx, fill(SALT))
                c.drawPath(hx, ink(3))
                c.restore()
    # NOPE rings: only in front of her
    yw = feet_y - 10
    if lvl == 3 and t < T_BLAST3:
        i = nope_word(t)
        kk = min(1.0, (t - W3[max(0, i)]) / 0.6)
        ring(c, XH, yw, 200 + 260 * (i + 1) * kk, (1 - kk) * 0.9, 7)
    elif lvl:
        for j in range(lvl):
            rr = 200 + (500 + 400 * lvl) * min(1.0, nk * (1.4 - 0.2 * j))
            ring(c, XH, yw, rr, (1 - nk) * 0.9, 6 + 3 * lvl)
    if 0 < shat < 1:                                 # NOPE 3: the haze breaks like glass over the whole sky
        glass_break(c, shat)


def ring(c, x, y, r, alpha, width=8):
    p = skia.Path()
    p.addArc(skia.Rect.MakeLTRB(x - r, y - r * 0.18, x + r, y + r * 0.18), 8, 164)   # only in front of her
    c.drawPath(p, ink(width, col=WHITE, alpha=alpha))


def glass_break(c, k):
    """The shimmering air shatters: shards of sky slide and fall away."""
    rng = np.random.default_rng(12)
    cx, cy = 560, 520
    for j in range(16):
        a0 = j * 2 * math.pi / 16
        a1 = a0 + 2 * math.pi / 16
        r0, r1 = rng.uniform(40, 120), rng.uniform(520, 900)
        shard = skia.Path()
        shard.moveTo(cx + r0 * math.cos(a0), cy + r0 * math.sin(a0))
        shard.lineTo(cx + r1 * math.cos(a0), cy + r1 * math.sin(a0))
        shard.lineTo(cx + r1 * math.cos(a1), cy + r1 * math.sin(a1))
        shard.lineTo(cx + r0 * math.cos(a1), cy + r0 * math.sin(a1))
        shard.close()
        fall = max(0.0, k - 0.25) / 0.75
        c.save()
        c.translate(math.cos(a0 + 0.2) * 60 * fall, 900 * fall * fall * rng.uniform(0.6, 1.2))
        c.drawPath(shard, fill(WHITE, 0.10 * (1 - fall)))
        c.drawPath(shard, ink(4, col=WHITE, alpha=0.9 * (1 - fall)))
        c.restore()


# ---------------------------------------------------------------- heat: the thermometer climbs to 134
def heat_shot(c, t):
    """Tight on the sun and a giant thermometer: the column shoots up to 134 °F as the number is said; heat
    rings pulse off the sun and the glass sweats."""
    a = shot_start("heat")
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 0.9)
    sun_rays(c, t, 640, 640, rgb("#F3C98C"), CORAL, n=20, alpha=0.32)
    g = skia.Paint(AntiAlias=True)
    g.setShader(skia.GradientShader.MakeRadial((640, 640), 520, [skia.Color4f(1, 0.9, 0.7, 0.7), skia.Color4f(1, 0.9, 0.7, 0)]))
    c.drawCircle(640, 640, 520, g)
    c.drawCircle(640, 640, 230, fill(CORAL))
    mottle(c, oval(640, 640, 230, 230), CORAL, alpha=0.18, scale=0.03)
    for j in range(3):
        ph = ((t - a) * 1.4 + j / 3) % 1.0
        c.drawCircle(640, 640, 240 + 300 * ph, ink(6, col=SEAL, alpha=0.6 * (1 - ph)))
    k_in = ease_io(prog(t, a, a + 0.25))
    k = ease_io(prog(t, T_T0, T_T1))
    x, y, h = 300, 520 + (1 - k_in) * 200, 560
    thermometer(c, x, y, h, 0.15 + 0.82 * k, boil=boil, col=SEAL)
    for j, (dx, dy) in enumerate(((-30, 120), (34, 260), (-28, 380))):      # the glass sweats
        ph = (tw * 0.8 + j * 0.37) % 1.0
        drop = smooth_path([(x + dx, y + dy + 60 * ph - 12), (x + dx + 7, y + dy + 60 * ph + 3), (x + dx, y + dy + 60 * ph + 9),
                            (x + dx - 7, y + dy + 60 * ph + 3)])
        c.drawPath(drop, fill(rgb("#BFE0EC"), 1 - ph))
        c.drawPath(drop, ink(2.5, alpha=1 - ph))
    heat_haze(c, tw, 300, 1300, alpha=0.4, n=8)
    if t >= T_T1:
        stamp(c, 560, 1060, "134°F", size=110, k=prog(t, T_T1, T_T1 + 0.2), rot=-6)


# ---------------------------------------------------------------- map: the hottest air ever recorded
def _land_rings():
    geo = json.load(open(os.path.join(HERE, "data", "ne_110m_land.geojson")))
    rings = []
    for f in geo["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            r = np.array(poly[0])
            if r[:, 1].mean() < -60:
                continue
            rings.append(r)
    return rings


LAND = _land_rings()
DV = (-116.87, 36.46)                 # Furnace Creek (lon, lat)


def map_xy(lon, lat, zoom, ctr):
    k = 1080 / 360 * zoom
    return 450 + (lon - ctr[0]) * k, 820 - (lat - ctr[1]) * k * 1.15


def map_shot(c, t):
    a, b = shot_start("map"), shot_end(shot_start("map"))
    fi = int(t * FPS)
    boil = (fi // 2, 0.7)
    k = ease_io(prog(t, a, b - 0.3))
    zoom = 1.25 + 1.6 * k
    ctr = (DV[0] * (0.3 + 0.7 * k) + 0 * (1 - k), 20 + (DV[1] - 20) * k)
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
        if max(xs) < -50 or min(xs) > W + 50:
            continue
        path = skia.Path()
        path.addPoly([skia.Point(*p) for p in pts], True)
        c.drawPath(path, fill(SAND_L))
        mottle(c, path, SAND, alpha=0.3, scale=0.01, seed=4)
        c.drawPath(path, ink(3, boil=boil))
    px, py = map_xy(DV[0], DV[1], zoom, ctr)
    kp = prog(t, a + 0.2, a + 0.6)
    for j in range(3):                                # heat rings pulsing out of Death Valley
        ph = ((t - a) * 1.2 + j / 3) % 1.0
        c.drawCircle(px, py, 30 + 160 * ph, ink(5, col=CORAL, alpha=kp * (1 - ph)))
    c.save()
    c.translate(px, py)
    c.scale(ease_io(kp), ease_io(kp))
    pin = skia.Path()
    pin.moveTo(0, 0)
    pin.cubicTo(-30, -36, -26, -66, 0, -66)
    pin.cubicTo(26, -66, 30, -36, 0, 0)
    c.drawPath(pin, fill(SEAL))
    c.drawPath(pin, ink(4))
    c.drawCircle(0, -44, 9, fill(FOAM))
    c.restore()
    kc = ease_io(prog(t, WT("n3", "hottest") - 0.1, WT("n3", "hottest") + 0.25))
    if kc > 0:
        hud_card(c, SAFE_X0, 290, [("HOTTEST AIR EVER", "134 °F", SEAL, 0.0), ("OFFICIAL RECORD", "57 °C", INKC, 0.0)],
                 alpha=kc, w=600)
    kr = prog(t, WT("n3", "officially") - 0.1, WT("n3", "officially") + 0.15)
    if kr > 0:
        stamp(c, CAP_CX, 1040, "JULY 10, 1913", size=60, k=kr, rot=-4, font_name="mono", pop=0.2)


# ---------------------------------------------------------------- bottle: one litre vs the clock
def sun_rays(c, t, cx, cy, base, line, n=18, alpha=0.25):
    c.drawRect(skia.Rect.MakeWH(W, H), fill(base))
    rot = twos(t) * 4
    for i in range(n):
        a0 = math.radians(rot + i * 360 / n)
        a1 = math.radians(rot + (i + 0.5) * 360 / n)
        p = skia.Path()
        p.moveTo(cx, cy)
        p.lineTo(cx + 2400 * math.cos(a0), cy + 2400 * math.sin(a0))
        p.lineTo(cx + 2400 * math.cos(a1), cy + 2400 * math.sin(a1))
        p.close()
        c.drawPath(p, fill(line, alpha))


def bottle_shot(c, t):
    a, b = shot_start("bottle"), shot_end(shot_start("bottle"))
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    sun_rays(c, t, 450, 760, SAND_L, SAND, alpha=0.55)
    k_in = ease_io(prog(t, a, a + 0.3))
    t_hr = WT("n5", "every")
    run = ease_io(prog(t, WT("n5", "drink") - 0.2, t_hr + 0.5))
    # the bottle, draining
    water_bottle(c, 280, 820 + (1 - k_in) * 300, s=1.55, level=1.0 - run, boil=boil, rot=-4)
    # the clock: the minute hand sweeps one hour
    cx, cy, r = 640, 780, 150
    c.save()
    c.translate(0, (1 - k_in) * 300)
    c.drawCircle(cx + 8, cy + 10, r, fill(INKC, 0.25))
    c.drawCircle(cx, cy, r, fill(PAPER_HI))
    mottle(c, oval(cx, cy, r, r), PAPER, alpha=0.2, scale=0.03, seed=2)
    sweep = skia.Path()
    sweep.moveTo(cx, cy)
    sweep.arcTo(skia.Rect.MakeLTRB(cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14), -90, 360 * run, False)
    sweep.close()
    c.drawPath(sweep, fill(CORAL, 0.55))
    for i in range(12):
        an = math.radians(i * 30 - 90)
        c.drawLine(cx + (r - 26) * math.cos(an), cy + (r - 26) * math.sin(an), cx + (r - 8) * math.cos(an),
                   cy + (r - 8) * math.sin(an), ink(5 if i % 3 == 0 else 3))
    an = math.radians(360 * run - 90)
    c.drawLine(cx, cy, cx + (r - 34) * math.cos(an), cy + (r - 34) * math.sin(an), ink(9, col=SEAL))
    c.drawCircle(cx, cy, 12, fill(INKC))
    c.drawCircle(cx, cy, r, ink(6, boil=boil))
    text(c, "60 MIN", cx, cy + r + 62, font("mono", 40), INKC, align="center", stroke=8, stroke_col=PAPER_HI)
    c.restore()
    if t >= t_hr + 0.5:
        stamp(c, 450, 1080, "EMPTY", size=90, k=prog(t, t_hr + 0.5, t_hr + 0.75), rot=-7)


# ---------------------------------------------------------------- boots: low on the hot ground
def boots_shot(c, t):
    """Low and tight on her boots: the salt ridges big, the air wobbling, wisps of heat rising off the crust."""
    a = shot_start("boots")
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 1.0)
    z = 2.5 + 0.15 * prog(t, a, shot_end(a))
    fx, fy = XH, YH + 640 * HS - 60
    c.save()
    c.translate(450, 1000)
    c.scale(z, z)
    c.translate(-fx, -fy)
    close_shot(c, t)
    c.restore()
    # heat rising: long wavy wisps from the ground up
    for j in range(7):
        ph = (tw * 0.6 + j / 7) % 1.0
        x = 120 + j * 110 + 30 * math.sin(j * 2.3)
        y0 = 1500 - 900 * ph
        p = skia.Path()
        p.moveTo(x, y0 + 260)
        p.cubicTo(x - 40, y0 + 170, x + 40, y0 + 90, x, y0)
        c.drawPath(p, ink(7, col=WHITE, alpha=0.65 * math.sin(ph * math.pi)))
    heat_haze(c, tw, 300, 1500, alpha=0.35, n=9)
    k = ease_io(prog(t, WT("n8", "hottest") - 0.15, WT("n8", "hottest") + 0.15))
    if k > 0:
        hud_card(c, SAFE_X0, 290, [("THE GROUND", "??? °F", SEAL, 0.0)], alpha=k, w=600)


# ---------------------------------------------------------------- thermo: air, ground, boiling water
T_MAX = 230.0


def thermo_shot(c, t):
    a = shot_start("thermo")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    tw = twos(t)
    c.drawRect(skia.Rect.MakeWH(W, H), fill(PRUSSIAN))
    asanoha(c, t, PRUSSIAN, FOAM, alpha=0.12)
    k_in = ease_io(prog(t, a, a + 0.3))
    x0, y0, w, h = SAFE_X0, 300 + (1 - k_in) * 140, 660, 860
    card = rrect(x0, y0, w, h, 18)
    c.drawPath(rrect(x0 + 10, y0 + 12, w, h, 18), fill(INKC, 0.35))
    c.drawPath(card, fill(PAPER_HI))
    mottle(c, card, PAPER, alpha=0.15, scale=0.02, seed=6)
    c.drawPath(card, ink(4))
    ty, th = y0 + 190, 560

    def Y(f):
        return ty + th - 30 - (th - 30) * f / T_MAX
    t201 = WT("n9", "201")
    t11 = WT("n10", "11")
    t_boil = WT("n10", "boiling")
    g = ease_io(prog(t, t201 - 0.3, t201 + 0.7)) * 201
    cols = [("AIR", 134.0, 1.0, PRUSSIAN, 200), ("GROUND", g, 1.0, CORAL, 450),
            ("BOILS", 212.0, ease_io(prog(t, t_boil - 0.3, t_boil + 0.1)), SEAL, 700)]
    for name, val, alpha, col, x in cols:
        if alpha <= 0:
            continue
        thermometer(c, x, ty, th, val / T_MAX, alpha=alpha, boil=boil, col=col)
        text(c, name, x, ty - 100, font("mono", 34), INKC, align="center", alpha=alpha)
        lab = f"{int(round(val))}°F" if (name != "GROUND" or t >= t201 - 0.3) else "???°F"
        text(c, lab, x, ty - 36, font("display", 54), col, align="center", alpha=alpha)
    if t >= t_boil - 0.1:                         # bubbles at the top of the boiling column
        for j in range(5):
            ph = (tw * 1.3 + j / 5) % 1.0
            c.drawCircle(700 + (j - 2) * 6, Y(212) + 10 - 30 * ph, 5 + 3 * ph, ink(2.5, col=SEAL, alpha=1 - ph))
    if t >= t11 - 0.1:                            # the gap: 11 degrees, a bracket between the two lines
        k = ease_io(prog(t, t11 - 0.1, t11 + 0.3))
        for v in (201, 212):
            pd = ink(3, col=INKC, alpha=0.8 * k)
            pd.setPathEffect(skia.DashPathEffect.Make([12, 8], 0))
            c.drawLine(470, Y(v), 680, Y(v), pd)
        c.drawLine(600, Y(212), 600, Y(201), ink(5, col=SEAL, alpha=k))
        text(c, "11°F", 590, Y(206) - 30, font("display", 50), SEAL, align="right", alpha=k, stroke=8,
             stroke_col=PAPER_HI)


def asanoha(c, t, base, line, r=70, alpha=0.18):
    """Asanoha, the hemp-leaf star pattern of woodblock textiles, drifting slowly."""
    drift = (twos(t) * 10) % (r * 2)
    hgt = r * math.sqrt(3)
    j = 0
    y = -hgt
    while y < H + hgt:
        x = -2 * r + (r if j % 2 else 0) - drift
        while x < W + 2 * r:
            for k in range(6):
                an = k * math.pi / 3
                c.drawLine(x, y, x + r * math.cos(an), y + r * math.sin(an), ink(2, col=line, alpha=alpha))
            x += 2 * r
        y += hgt
        j += 1


# ---------------------------------------------------------------- the duck on the mirage
def duck_shot(c, t):
    """Tight on the horizon: the duck floats on the only lake for miles. At "mirage" the lake fades to salt and
    the duck keeps floating, on nothing, unbothered."""
    a = shot_start("duck")
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 0.9)
    tm0 = WT("n13", "mirage")
    z = 1.0 + 0.04 * prog(t, a, shot_end(a)) + 0.22 * ease_io(prog(t, tm0 - 0.1, tm0 + 0.5))
    c.save()
    c.translate(450, 960)
    c.scale(z, z)
    c.translate(-450, -960)
    desert_sky(c, tw, horizon=1060, sun=(820, 330), sun_r=150)
    mountains(c, t, boil, y0=1060)
    c.drawRect(skia.Rect.MakeXYWH(0, 1060, W, H - 1060), fill(SALT_SH))
    big = SaltFlat(horizon=1060, cx=450, f=1000.0, cam_h=0.5, r=1.5, seed=7) if not hasattr(duck_shot, "_flat") else duck_shot._flat
    duck_shot._flat = big
    big.draw(c, tw, boil=boil)
    tm = WT("n13", "mirage")
    gone = ease_io(prog(t, tm - 0.1, tm + 0.6))
    lake_a = 1.0 - gone * (0.85 + 0.15 * math.sin(t * 30))
    mirage(c, tw, -60, 1140, 1080, h=190, alpha=lake_a, boil=boil)
    # the mountains' upside-down reflection in the 'lake'
    if lake_a > 0.05:
        c.save()
        c.clipPath(rrect(-60, 1000, 1200, 170, 60))
        c.translate(0, 2 * 1080)
        c.scale(1, -1)
        peak(c, [(-60, 960), (160, 920), (330, 950), (540, 900), (760, 945), (1140, 925)], col=DESERT_ROSE, seed=3,
             hatch=False, line=2, alpha=0.35 * lake_a)
        c.restore()
    heat_haze(c, tw, 960, 1200, alpha=0.6, n=7)
    bob = 6 * math.sin(tw * 2.2)
    draw_duck(c, 450, 1072 + bob, s=2.6, boil=boil, tilt=-3 + 2 * math.sin(tw * 1.7), look=0.4)
    if lake_a > 0.05:                                  # its reflection
        c.save()
        c.translate(0, 2 * (1078 + bob))
        c.scale(1, -1)
        c.save()
        c.clipPath(rrect(250, 1078 + bob - 10, 400, 200, 10))
        draw_duck(c, 450, 1072 + bob, s=2.6, boil=None, tilt=-3)
        c.restore()
        c.restore()
    c.restore()
    if t >= tm + 0.2:
        stamp(c, CAP_CX, 560, "MIRAGE", size=110, k=prog(t, tm + 0.2, tm + 0.45), rot=-6)


# ---------------------------------------------------------------- night: still over a hundred
def night_shot(c, t):
    a = shot_start("night")
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 0.9)
    k = ease_io(prog(t, a, a + 0.5))
    desert_sky(c, tw, horizon=HORIZON, sun=None, night=1.0, stars=1.0)
    c.drawCircle(760, 330, 64, fill(rgb("#F3E9CF")))
    c.drawCircle(782, 316, 56, fill(rgb("#1B2E4E")))     # a crescent moon
    mountains(c, t, boil, night=1.0)
    FLAT.draw(c, tw, boil=boil, alpha=1.0)
    c.drawRect(skia.Rect.MakeXYWH(0, HORIZON, W, H - HORIZON), fill(rgb("#1B2E4E"), 0.55))
    heat_haze(c, tw, HORIZON - 20, HORIZON + 300, alpha=0.35, n=6, col=rgb("#F6C59A"))
    s = 0.62
    draw_legs(c, XH, 980, s=s, boil=boil, t=tw)
    draw_hero(c, XH, 980, s=s, face="worried", boil=boil, arms="fan", t=tw, shiver=0.2)
    water_bottle(c, XH - 175 * s, 980 + 330 * s, s=0.42 * s, level=water_left(t), boil=boil, rot=8)
    c.drawRect(skia.Rect.MakeWH(W, H), fill(rgb("#0E1A30"), 0.25 * (1 - k)))
    t100 = WT("n14", "100")
    kc = ease_io(prog(t, t100 - 0.15, t100 + 0.15))
    if kc > 0:
        hud_card(c, SAFE_X0, 290, [("AT NIGHT", "100+ °F", SEAL, max(0.0, 1 - (t - t100) * 3))], alpha=kc, w=600)


# ---------------------------------------------------------------- days: the answer
def sun_icon(c, x, y, r, k):
    c.drawCircle(x, y, r, fill(CORAL, k))
    for i in range(8):
        an = i * math.pi / 4
        c.drawLine(x + (r + 8) * math.cos(an), y + (r + 8) * math.sin(an), x + (r + 22) * math.cos(an),
                   y + (r + 22) * math.sin(an), ink(5, col=CORAL, alpha=k))
    c.drawCircle(x, y, r, ink(3.5, alpha=k))


def moon_icon(c, x, y, r, k, bg):
    c.drawCircle(x, y, r, fill(rgb("#F3E9CF"), k))
    c.drawCircle(x + r * 0.4, y - r * 0.25, r * 0.85, fill(bg, k))


def days_shot(c, t):
    """Two days and two nights roll past on a track; then the two bottles, full and empty, land on the same mark."""
    a = shot_start("days")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    bg = rgb("#20395A")
    c.drawRect(skia.Rect.MakeWH(W, H), fill(bg))
    asanoha(c, t, bg, FOAM, alpha=0.10)
    k_in = ease_io(prog(t, a, a + 0.3))
    # the track: 2 days
    x0, x1, y = SAFE_X0 + 30, SAFE_X1 - 30, 560
    run = ease_io(prog(t, WT("n16", "2") - 0.3, E["n16"] + 0.3))
    c.drawPath(rrect(x0, y - 16, x1 - x0, 32, 16), fill(PAPER_HI, 0.25 * k_in))
    c.drawPath(rrect(x0, y - 16, max(32, (x1 - x0) * run), 32, 16), fill(YEL_L, k_in))
    c.drawPath(rrect(x0, y - 16, x1 - x0, 32, 16), ink(4, col=FOAM, alpha=k_in))
    for i in range(4):                                  # day, night, day, night
        cx_ = x0 + (x1 - x0) * (i + 0.5) / 4
        kk = k_in * (1.0 if run >= (i + 0.5) / 4 - 0.02 else 0.35)
        if i % 2 == 0:
            sun_icon(c, cx_, y - 110, 34, kk)
        else:
            moon_icon(c, cx_, y - 110, 34, kk, bg)
    for i, lab in enumerate(("DAY 1", "DAY 2")):
        cx_ = x0 + (x1 - x0) * (i + 0.5) / 2
        text(c, lab, cx_, y + 80, font("mono", 36), FOAM, align="center", alpha=k_in)
    # the big answer
    kd = ease_io(prog(t, WT("n16", "2") - 0.1, WT("n16", "2") + 0.2))
    if kd > 0:
        hud_card(c, SAFE_X0, 290, [("YOU'D LAST", "~2 DAYS", SEAL, max(0.0, 1 - (t - WT("n16", "2")) * 3))],
                 alpha=kd, w=600)
    # the two bottles: with it, without it
    tb, tw_ = WT("n17", "bottle"), WT("n17", "without")
    for j, (tk, lvl, lab) in enumerate(((tb, 1.0, "1 L"), (tw_, 0.0, "0 L"))):
        k = ease_io(prog(t, tk - 0.15, tk + 0.2))
        if k <= 0:
            continue
        bx = 270 + j * 360
        water_bottle(c, bx, 860 + (1 - k) * 80, s=0.8, level=lvl, boil=boil, label=lab, alpha=k)
        text(c, "= ~2 DAYS", bx, 1040, font("mono", 40), YEL_L, align="center", alpha=k, stroke=8)
    ts = WT("n17", "resting")
    if t >= ts - 0.1:
        stamp(c, CAP_CX, 1130, "RESTING IN SHADE", size=54, k=prog(t, ts - 0.1, ts + 0.15), rot=-4, font_name="mono",
              pop=0.2)


# ---------------------------------------------------------------- wide: there is no shade
def wide_shot(c, t):
    a = shot_start("wide")
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    z = 1.0 + 0.05 * prog(t, a, shot_end(a))
    c.save()
    c.translate(450, 900)
    c.scale(z, z)
    c.translate(-450, -900)
    desert_sky(c, tw, horizon=760, sun=(700, 300), sun_r=120)
    mountains(c, t, boil, y0=760)
    wf = SaltFlat(horizon=760, cx=450, f=1000.0, cam_h=9.0, r=1.5, seed=5) if not hasattr(wide_shot, "_flat") else wide_shot._flat
    wide_shot._flat = wf
    wf.draw(c, tw, boil=boil)
    heat_haze(c, tw, 740, 1000, alpha=0.5, n=6)
    s = 0.2
    hx, hy = 450, 1010
    c.drawPath(oval(hx, hy + 640 * s - 4, 190 * s, 30 * s), fill(rgb("#7E6B55"), 0.6))
    draw_legs(c, hx, hy, s=s, t=tw)
    draw_hero(c, hx, hy, s=s, face="worried", arms="none", t=tw)
    c.restore()
    tn = WT("n18", "shade")
    k = ease_io(prog(t, L["n18"] + 0.2, L["n18"] + 0.6))
    if k > 0:                                        # the arrow: all the shade there is
        ax, ay = hx + 40, hy + 640 * s + 40
        p = skia.Path()
        p.moveTo(ax + 80, ay - 250)
        p.quadTo(ax + 140, ay - 20, ax + 30, ay + 20)
        c.drawPath(p, ink(7, col=INKC, alpha=k))
        hd = skia.Path()
        hd.moveTo(ax + 30, ay + 20)
        hd.lineTo(ax + 64, ay + 34)
        hd.lineTo(ax + 44, ay + 58)
        hd.close()
        c.drawPath(hd, fill(INKC, k))
        text(c, "all the shade", ax + 60, ay - 280, font("hand", 70), INKC, align="center", alpha=k, stroke=10,
             stroke_col=PAPER_HI)


# ---------------------------------------------------------------- 1849: the lost wagons
def trail_shot(c, t):
    """A painted map of the valley: the two ranges, the salt flat down the middle, the wagons' dotted trail."""
    a = shot_start("trail")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    tw = twos(t)
    c.drawRect(skia.Rect.MakeWH(W, H), fill(rgb("#5C3B2A")))
    k_in = ease_io(prog(t, a, a + 0.3))
    x0, y0, w, h = 70, 440 + (1 - k_in) * 120, 760, 740
    card = rrect(x0, y0, w, h, 16)
    c.drawPath(rrect(x0 + 10, y0 + 12, w, h, 16), fill(INKC, 0.4))
    c.drawPath(card, fill(rgb("#EAD9B5")))
    mottle(c, card, SAND, alpha=0.35, scale=0.015, seed=9)
    c.save()
    c.clipPath(card, doAntiAlias=True)
    # the valley floor, running top to bottom, salt-white down the middle
    floor = smooth_path([(x0 + 300, y0 - 20), (x0 + 470, y0 - 20), (x0 + 500, y0 + 300), (x0 + 450, y0 + 620),
                         (x0 + 480, y0 + h + 20), (x0 + 300, y0 + h + 20), (x0 + 270, y0 + 600), (x0 + 330, y0 + 300)])
    c.drawPath(floor, fill(SALT))
    c.drawPath(floor, ink(2.5, alpha=0.5))
    # the two ranges as rows of carved peaks
    for (px0, side) in ((x0 + 40, -1), (x0 + 560, 1)):
        for j in range(7):
            py = y0 + 70 + j * 125
            px = px0 + (j % 2) * 40
            pk = skia.Path()
            pk.moveTo(px, py + 50)
            pk.lineTo(px + 60, py - 40)
            pk.lineTo(px + 120, py + 50)
            pk.close()
            c.drawPath(pk, fill(DESERT_ROSE))
            c.drawLine(px + 60, py - 40, px + 80, py + 50, ink(2.5, col=DESERT_ROSE_D))
            c.drawPath(pk, ink(3, boil=boil))
    c.restore()
    c.drawPath(card, ink(4))
    text(c, "PANAMINT RANGE", x0 + 130, y0 + 40, font("mono", 30), INKC, align="left")
    text(c, "SALT FLAT", x0 + 390, y0 + 600, font("mono", 30), INKC, align="center")
    # the trail: from the east (right) down into the valley and out west over the Panamints
    trail = [(x0 + w + 20, y0 + 180), (x0 + 610, y0 + 230), (x0 + 470, y0 + 330), (x0 + 380, y0 + 450),
             (x0 + 330, y0 + 560), (x0 + 250, y0 + 650), (x0 + 120, y0 + 720), (x0 - 20, y0 + 760)]
    k = ease_io(prog(t, WT("n20", "lost") - 0.2, E["n20"] + 0.6))
    path = smooth_path(trail, closed=False)
    meas = skia.PathMeasure(path, False)
    ln = meas.getLength()
    seg = skia.Path()
    meas.getSegment(0, ln * k, seg, True)
    pd = ink(6, col=SEAL)
    pd.setPathEffect(skia.DashPathEffect.Make([18, 12], 0))
    c.drawPath(seg, pd)
    if k > 0:
        pos, tan = meas.getPosTan(min(ln, ln * k))
        covered_wagon(c, pos.x(), pos.y() + 14, s=0.3, boil=boil, t=tw * 3)
    ky = ease_io(prog(t, WT("n20", "1849") - 0.1, WT("n20", "1849") + 0.2))
    if ky > 0:
        hud_card(c, SAFE_X0, 290, [("WINTER", "1849", SEAL, max(0.0, 1 - (t - WT("n20", "1849")) * 3))], alpha=ky,
                 w=600)


def ridge_shot(c, t):
    """Sunset. A wagon tops the Panamint ridge, leaving; the valley glows below. "Only one had died": the stamp."""
    a = shot_start("ridge")
    fi = int(t * FPS)
    boil = (fi // 2, 0.9)
    tw = twos(t)
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeLinear([(0, 0), (0, 1200)], [rgb("#3D3A63"), rgb("#C8645A"), rgb("#F2B46E")],
                                                [0.0, 0.6, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)
    c.drawCircle(300, 1080, 130, fill(rgb("#F6D79A")))
    ridge = [(-60, 1150), (120, 1060), (260, 1100), (430, 980), (600, 1030), (760, 940), (900, 1000), (1140, 960)]
    peak(c, ridge, col=rgb("#3A2A38"), seed=21, boil=boil, line=4, hatch=True)
    k = ease_io(prog(t, a, E["n21"]))
    wx = 380 + 360 * k
    wy = float(np.interp(wx, [p_[0] for p_ in ridge], [p_[1] for p_ in ridge]))
    c.save()
    c.translate(wx, wy + 6)
    c.rotate(-6)
    covered_wagon(c, 0, 0, s=0.62, boil=boil, t=tw * 2)
    c.restore()
    for (x0, y, w_, h_, sp) in ((-60, 420, 460, 36, 10), (560, 620, 520, 30, -8)):
        mist_band(c, x0 + sp * tw, y, w_, h_, alpha=0.5, col=rgb("#F6C59A"))
    to = WT("n21", "Only")
    if t >= to - 0.05:
        stamp(c, CAP_CX, 560, "ONLY 1 DIED", size=96, k=prog(t, to - 0.05, to + 0.2), rot=-6)


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
T_T0, T_T1 = WT("n2", "134") - 0.05, WT("n2", "134") + 0.45


def hud(c, t):
    """Top-left cartouche: one story number at a time. Hidden while a NOPE owns the frame."""
    shot = shot_at(t)[1]
    lvl, nk = nope_at(t)
    lvl = lvl if shot == "close" else 0
    title_on = t < E["n1"] + 0.15
    rows = []
    lab_live = any(WHO[k] == "LAB" and L[k] - 0.35 <= t <= E[k] + 0.35 for k in KEYS)
    if shot == "heat":
        k = ease_io(prog(t, T_T0, T_T1))
        val = "??? °F" if k < 0.04 else f"{int(round(60 + 74 * k))} °F"
        rows.append(("AIR RECORD", val, SEAL, max(0.0, 1 - (t - T_T1) * 3) if t > T_T1 else 0.0))
    if not lvl and shot == "close":
        if L["n4"] - 0.2 <= t < L["n5"]:
            rows.append(("WATER", "1 L", PRUSSIAN, 0.0))
        elif WT("n17", "Only") - 0.1 <= t < L["n18"] - 0.1:
            rows.append(("ONLY", "IN SHADE", SEAL, 0.0))
    y = 290
    if title_on:
        rows = [("YOU'D LAST", "?? DAYS", SEAL, 0.0)]
    if rows:
        if title_on:
            hud_card(c, SAFE_X0 + 30, 470, rows, w=600)
        else:
            hud_card(c, SAFE_X0, y, rows, w=600)
    if not lvl and shot == "close" and not rows and not lab_live and L["n6"] - 0.3 <= t < L["n22"]:
        water_bar(c, t, y)
    if title_on:
        f1, f2 = font("mono", 38), font("display", 112)
        c.save()
        c.translate(CAP_CX, 300)
        c.rotate(-3)
        tag = "COULD YOU SURVIVE"
        wv = f1.measureText(tag)
        c.drawPath(rrect(-wv / 2 - 18, -40, wv + 36, 56, 10), fill(INKC, 0.92))
        text(c, tag, 0, 2, f1, YEL_L, align="center")
        name = "DEATH VALLEY?"
        sc = min(1.0, 630 / f2.measureText(name))
        c.scale(sc, sc)
        text(c, name, 0, 130 / sc, f2, FOAM, align="center", stroke=22)
        c.restore()
    ks = prog(t, 3.0, 3.3)
    if ks > 0 and shot != "end":
        seal(c, 874, 120, 86, alpha=ks)


def water_bar(c, t, y):
    """The progress bar: the water left in her one-litre bottle, sip by sip toward empty."""
    x0, w = SAFE_X0, 600
    card = rrect(x0, y, w, 156, 14)
    c.drawPath(rrect(x0 + 8, y + 10, w, 156, 14), fill(INKC, 0.25))
    c.drawPath(card, fill(PAPER_HI, 0.96))
    mottle(c, card, PAPER, alpha=0.12, scale=0.03, seed=8)
    c.drawPath(card, ink(4))
    c.drawPath(rrect(x0 + 8, y + 8, w - 16, 140, 9), ink(1.6, alpha=0.7))
    text(c, "WATER LEFT", x0 + 24, y + 46, font("mono", 32), mixc(INKC, PAPER, 0.3))
    v = water_left(t)
    text(c, f"{v:.1f} L", x0 + w - 24, y + 52, font("mono", 46), SEAL if v < 0.25 else INKC, align="right")
    bx, by, bw = x0 + 24, y + 86, w - 48
    c.drawPath(rrect(bx, by, bw, 26, 13), fill(rgb("#D9CDB0"), 0.8))
    if v > 0.005:
        c.drawPath(rrect(bx, by, max(26, bw * v), 26, 13), fill(WATER))
        for j in range(int(bw * v / 40)):         # a ripple on the water
            xx = bx + 20 + j * 40 + 6 * math.sin(t * 4 + j)
            c.drawLine(xx, by + 9, xx + 14, by + 9, ink(2.5, col=WHITE, alpha=0.7))
    c.drawPath(rrect(bx, by, bw, 26, 13), ink(3))
    text(c, "EMPTY", bx, by + 64, font("mono", 30), mixc(INKC, PAPER, 0.35))
    text(c, "1 L", bx + bw, by + 64, font("mono", 30), mixc(INKC, PAPER, 0.35), align="right")


def intercom(c, t):
    live = [k for k in KEYS if WHO[k] == "LAB" and L[k] - 0.35 <= t <= E[k] + 0.35]
    if not live:
        return
    k = live[0]
    kin = ease_io(min(prog(t, L[k] - 0.35, L[k] - 0.05), 1 - prog(t, E[k] + 0.05, E[k] + 0.35)))
    x = SAFE_X1 - 230 + (1 - kin) * 560
    shot = shot_at(t)[1]
    y = 290 if k == "n24" else (290 if shot in ("duck",) else (290 if shot == "wide" else 620))
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
        word = ("nope.", "NOPE.", "NOPE!")[max(0, i)]
        size = (150, 200, 250)[max(0, i)]
        k = 0.0 if i < 2 else k
        if i < 2:
            k = min(0.7, (t - W3[max(0, i)]) / 1.2)
    else:
        word = {1: "nope.", 2: "NOPE!"}[lvl]
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
    if lvl == 1:
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
    a = L["n22"]
    if t < a:
        return
    gone = 1 - prog(t, L["n23"] - 0.25, L["n23"] - 0.05)      # cleared for her close-up and the countdown
    if gone <= 0:
        return
    opts = [("A", "ROMAN WINTER CAMP", "Roman"), ("B", "MARS", "Mars"), ("C", "MEDIEVAL FARM", "medieval")]
    dim = ease_io(prog(t, a, a + 0.4)) * gone
    c.drawRect(skia.Rect.MakeWH(W, H), fill(INKC, 0.12 * dim))
    for i, (letter, name, word) in enumerate(opts):
        tk = WT("n22", word)
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
        f = font("display", 46 if len(name) < 12 else 38)
        text(c, name, x + 112, y + 68, f, INKC, alpha=k)
        icon(c, i, x + 585, y + 52, k * 0.9)
        c.restore()


def icon(c, i, x, y, k):
    if i == 0:    # a tent in the snow, with a banner pole
        c.drawPath(oval(x, y + 36, 50, 9), fill(WHITE, k))
        p = skia.Path()
        p.moveTo(x - 44, y + 34)
        p.lineTo(x, y - 26)
        p.lineTo(x + 44, y + 34)
        p.close()
        c.drawPath(p, fill(rgb("#B58A5A"), k))
        c.drawLine(x, y - 26, x, y + 34, ink(3, alpha=k))
        c.drawPath(p, ink(3, alpha=k))
        c.drawLine(x + 34, y + 34, x + 34, y - 40, ink(4, col=rgb("#5A3A2A"), alpha=k))
        c.drawPath(rrect(x + 34, y - 40, 22, 16, 2), fill(SEAL, k))
        for dx, dy in ((-30, -30), (24, -10), (-10, -44)):
            c.drawCircle(x + dx, y + dy, 3, fill(WHITE, k))
    elif i == 1:  # Mars: a red planet with craters
        c.drawCircle(x, y, 40, fill(rgb("#C8553A"), k))
        for dx, dy, r in ((-12, -10, 8), (14, 10, 6), (-4, 20, 5)):
            c.drawCircle(x + dx, y + dy, r, fill(rgb("#9A3C2A"), k))
        c.drawCircle(x, y, 40, ink(3, alpha=k))
    else:         # a farm: a field in furrows and a haystack
        c.drawPath(rrect(x - 50, y - 6, 100, 44, 6), fill(rgb("#9C7A3C"), k))
        for j in range(4):
            c.drawLine(x - 46, y + 4 + j * 10, x + 46, y + 4 + j * 10, ink(2.5, col=rgb("#6E5226"), alpha=k))
        hs = smooth_path([(x - 24, y - 4), (x - 18, y - 34), (x, y - 44), (x + 18, y - 34), (x + 24, y - 4)])
        c.drawPath(hs, fill(YEL_L, k))
        c.drawPath(hs, ink(3, alpha=k))
        c.drawPath(rrect(x - 50, y - 6, 100, 44, 6), ink(3, alpha=k))


def respawn_flash(c, t):
    a = E["n24"] + 0.02
    if t >= a:
        k = prog(t, a, DURATION)
        c.drawRect(skia.Rect.MakeWH(W, H), fill(PAPER_HI, ease_io(min(1, k * 1.6))))


def cam_close(t):
    """Camera on the close shot: a slow push-out over the hook, punch-ins on the NOPEs."""
    z = 1.0
    if t < shot_start("map"):
        z = 1.10 - 0.10 * ease_io(prog(t, 1.2, shot_start("map")))
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
            z = 1.10 + 0.08 * ease_io(prog(t, L["n22"], DURATION))
            dyc = 70.0
        if z != 1.0 or dyc:
            c.translate(XH, YH + dyc)
            c.scale(z, z)
            c.translate(-XH, -YH)
        close_shot(c, t)
    elif shot == "plead":
        z = 1.5
        c.translate(XH, 830)
        c.scale(z, z)
        c.translate(-XH, -YH)
        close_shot(c, t)
    elif shot == "heat":
        heat_shot(c, t)
    elif shot == "map":
        map_shot(c, t)
    elif shot == "bottle":
        bottle_shot(c, t)
    elif shot == "boots":
        boots_shot(c, t)
    elif shot == "thermo":
        thermo_shot(c, t)
    elif shot == "duck":
        duck_shot(c, t)
    elif shot == "night":
        night_shot(c, t)
    elif shot == "days":
        days_shot(c, t)
    elif shot == "wide":
        wide_shot(c, t)
    elif shot == "trail":
        trail_shot(c, t)
    elif shot == "ridge":
        ridge_shot(c, t)
    c.restore()
    paper_over(c, 1.0)
    vignette(c, 0.24)
    hud(c, t)
    intercom(c, t)
    end_cards(c, t)
    nope_text(c, t)
    captions(c, t)
    respawn_flash(c, t)
