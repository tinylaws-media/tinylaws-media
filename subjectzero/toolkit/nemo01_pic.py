"""COULD YOU SURVIVE? #01 — Point Nemo: the picture (2D estampe look, sz2d.py). Timed on out/nemo01_lines.json.

    python3 sz2render.py nemo01_pic                # -> out/nemo01_pic_video.mp4
    python3 sz2render.py nemo01_pic --sheet 0 2 5 ...
"""
import json
import math
import os

import numpy as np
import skia

from sz2d import (W, H, FPS, rgb, mixc, fill, ink, text, smooth_path, rrect, oval, ease_io, prog, font, sky, mist_band,
                  iss, Sea, draw_hero, draw_duck, paper_over, vignette, seal, mottle, words_caption, woodgrain, hud_card,
                  PAPER, PAPER_HI, INKC, PRUSSIAN, CORAL, SEAL, FOAM, YEL, YEL_D, YEL_L, SKIN, WHITE, SEA, SAFE_X0, SAFE_X1, CAP_CX)
import nemo01 as EP

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
EPNAME = "nemo01_pic"
DURATION = EP.DURATION

_js = json.load(open(os.path.join(OUT, "nemo01_lines.json"), encoding="utf-8"))
L = {l["key"]: l["t"] for l in _js["lines"]}
DUR = {l["key"]: l["dur"] for l in _js["lines"]}
WHO = {l["key"]: l["who"] for l in _js["lines"]}
TXT = {l["key"]: l["text"] for l in _js["lines"]}
E = {k: L[k] + DUR[k] for k in L}
KEYS = sorted(L, key=lambda k: L[k])
ENV = {w: np.load(os.path.join(OUT, f"nemo01_env_{w}.npy")) for w in ("N", "HERO", "LAB")}

# what the captions show (numbers as figures; the voice says them in words)
CAP = {"n3": "Nearest land: 2,688 km away.", "n21": "More than 260 were dropped out here.",
       "n17": "Even afloat: about 1–3 hours.", "n25": "Respawning in 3... 2..."}
# how long a caption word takes to SAY (characters of the spoken words), so a figure lights up when it is said
SAYLEN = {"2,688": 37, "km": 10, "afloat:": 19, "1–3": 13, "260": 21, "3...": 6, "2...": 4}
NOPES = {"n13": 1, "n15": 2, "n23": 3}


def env(who, t):
    e = ENV[who]
    i = int(t * FPS)
    return float(e[i]) if 0 <= i < len(e) else 0.0


def word_times(key):
    """Start time of each caption word, spread over the line by characters, with a little extra weight on pauses."""
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
    """1 to 3 words per caption chunk; a chunk ends at punctuation."""
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


# ---------------------------------------------------------------- the story clock (survival time)
T_GASP = WT("n9", "gasp")
T_18 = WT("n11", "eighteen")
T_ARMS = WT("n14", "arms")
T_REVEAL = WT("n17", "about")
CLOCK = [(L["n9"], 0.0), (E["n9"], 60.0), (L["n14"], 4 * 60.0), (T_ARMS, 600.0), (L["n16"], 640.0),
         (L["n17"] - 0.2, 3500.0)]


def story_clock(t):
    if t < CLOCK[0][0]:
        return None
    for (a, va), (b, vb) in zip(CLOCK, CLOCK[1:]):
        if t <= b:
            k = (t - a) / (b - a) if b > a else 1
            return va + (vb - va) * (k if b - a > 3 else ease_io(k))
    return CLOCK[-1][1]


def fmt_clock(s):
    s = int(s)
    return f"{s // 3600:02d}:{s // 60 % 60:02d}:{s % 60:02d}"


# ---------------------------------------------------------------- shots
SHOTS = [                               # rule: no camera setup held longer than 8 s
    (0.0, "close"),
    (E["n2"] + 0.05, "map"),            # zoom out to the chart
    (L["n5"] - 0.1, "sky"),             # tilt up: the ISS
    (L["n8"] - 0.15, "close"),
    (WT("n11", "world") - 0.05, "swim_map"),  # the swim on the chart: 0.00 % there... 18 days
    (L["n13"] - 0.15, "close"),         # NOPE 1
    (L["n14"] - 0.1, "under"),          # half underwater: legs dangling over 4 km of water, the arms go on strike
    (L["n15"] - 0.15, "close"),         # NOPE 2
    (L["n16"] - 0.05, "clock"),         # the survival clock, big: spinning, then 1-3 hours
    (L["n18"] - 0.1, "duck"),
    (L["n20"] - 0.05, "graveyard"),
    (L["n22"] - 0.05, "close"),
]


def shot_start(name, nth=0):
    return [a for a, n in SHOTS if n == name][nth]


def shot_at(t):
    cur = SHOTS[0]
    for s in SHOTS:
        if t >= s[0]:
            cur = s
    return cur


SEA_CLOSE = Sea(horizon=600)
SEA_SKY = Sea(horizon=1170, seed=3, layers=[(1190, 3, 0.2), (1225, 6, 0.3), (1275, 10, 0.4), (1350, 16, 0.5),
                                            (1440, 22, 0.6), (1530, 30, 0.7), (1640, 40, 0.85), (1750, 50, 1.0)])
SEA_WIDE = Sea(horizon=820, seed=9, layers=[(842, 3, 0.2), (872, 5, 0.3), (915, 8, 0.38), (975, 12, 0.46),
                                             (1060, 18, 0.56), (1190, 28, 0.7), (1380, 42, 0.85), (1640, 60, 1.0)])


def twos(t):
    """Hand animation on twos: characters and waves move 12 times a second."""
    return math.floor(t * 12) / 12


def nope_words():
    """Start times of the three words of the last NOPE ("Nope. Nope. NOPE!"), measured on her voice track
    (rising edges of its loudness), or spread by characters if the measure fails."""
    e = ENV["HERO"]
    a, b = int(L["n23"] * FPS) - 1, int(E["n23"] * FPS) + 1
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
    return [wt for _, wt in word_times("n23")]


W3 = nope_words()
T_BLAST3 = W3[-1]                 # the third word: the big blast


def nope_at(t):
    """(level, k) of the NOPE currently blasting, k = 0..1 over its effect."""
    for key, lvl in NOPES.items():
        a = L[key]
        end = (E[key] + 0.5, E[key] + 0.8, T_BLAST3 + 1.05)[lvl - 1]
        if a - 0.05 <= t <= end:
            if lvl == 3:          # k runs over the big blast; before it, the two small ones
                return 3, max(0.0, (t - T_BLAST3) / (end - T_BLAST3))
            return lvl, (t - a) / (end - a)
    return 0, 0.0


def nope_word(t):
    """Index (0, 1, 2) of the word of the last NOPE being said, or -1."""
    if not (L["n23"] - 0.05 <= t <= T_BLAST3 + 1.05):
        return -1
    return max(i for i, w in enumerate(W3) if t >= w - 0.05) if t >= W3[0] - 0.05 else 0


def punch(t):
    """Punch-in zoom on her face while she says it: small for the first, more each time."""
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
            z = (0.06, 0.16)[lvl - 1]
        if a - 0.05 <= t <= e + 0.4:
            kin = min(1.0, (t - a + 0.05) / 0.09)
            kout = 1.0 if t <= e else max(0.0, 1 - (t - e) / 0.4)
            return 1 + z * ease_io(kin) * ease_io(kout)
    return 1.0


def shake(t):
    lvl, k = nope_at(t)
    if not lvl:
        return 0.0, 0.0
    if lvl == 3 and t < T_BLAST3:
        i = nope_word(t)
        amp = (5, 11)[min(1, max(0, i))] * max(0.0, 1 - (t - W3[max(0, i)]) / 0.4)
        return amp * math.sin(t * 83), amp * math.cos(t * 71)
    amp = (8, 18, 40)[lvl - 1] * max(0.0, 1 - k) ** 1.5
    return amp * math.sin(t * 83), amp * math.cos(t * 71)


# ---------------------------------------------------------------- hero state in the close shots
def hero_state(t):
    st = dict(face="worried", arms="paddle", shiver=0.0, look=None, squash=0.0, blink=0.0, mouth_open=None, tilt=0.0)
    # blinks
    for b in (2.6, 6.0, 18.4, 26.4, 32.2, 38.0, 44.8, 52.2, 59.6, 63.0):
        if b <= t <= b + 0.12:
            st["blink"] = 1.0
    if t < 0.6:                                    # spawn: a squash bounce as she lands
        st["face"] = "shock"
        k = t / 0.6
        st["squash"] = 0.45 * math.sin(k * math.pi * 2) * (1 - k)
    elif t < E["n2"]:
        st["look"] = (8 * math.sin(t * 2.2), 0)
    elif L["n8"] - 0.2 <= t < L["n10"]:
        st["face"] = "cold"
        st["shiver"] = min(1.0, (t - L["n8"]) / 1.5)
        if T_GASP - 0.1 <= t < T_GASP + 1.0:
            st["face"] = "shock"
            st["squash"] = -0.45 * math.sin(min(1, (t - T_GASP + 0.1) / 0.3) * math.pi / 2)
            st["shiver"] = 0.3
    elif L["n10"] <= t < L["n11"]:
        st["face"] = "worried"
        st["look"] = (9, -8)
        st["shiver"] = 0.5
    elif L["n11"] <= t < L["n13"]:
        st["face"] = "smug"
        st["arms"] = "swim"
        if t >= T_18:
            st["face"] = "shock"
            st["arms"] = "paddle"
    elif L["n14"] <= t < L["n15"]:
        st["face"] = "deadpan" if t > T_ARMS else "worried"
        st["arms"] = "limp" if t > T_ARMS - 0.2 else "paddle"
        st["shiver"] = 0.6
    elif L["n16"] <= t < L["n17"]:
        st["face"] = "worried"
        st["shiver"] = 0.8
        st["look"] = (6 * math.sin(t * 5), 2)
    elif L["n17"] <= t < L["n18"]:
        st["face"] = "cold"
        st["shiver"] = 1.0
    elif L["n22"] - 0.1 <= t < L["n23"]:
        st["face"] = "up"
        st["shiver"] = 0.3
        if t > WT("n22", "that"):
            st["face"] = "shock"
    elif t >= L["n24"]:
        st["face"] = "deadpan"
        st["shiver"] = 0.4
        if L["n24b"] - 0.1 <= t < L["n25"]:         # "Please say Sahara.": hopeful, hands together
            st["face"] = "happy"
            st["arms"] = "hug"
            st["look"] = (0, -8)
            st["mouth_open"] = 0.5 + 1.1 * env("HERO", t)
        elif t >= L["n25"]:
            st["face"] = "worried"
    lvl, k = nope_at(t)
    if lvl and k < 0.85:
        st["face"] = "nope"
        st["mouth_open"] = min(2.0, 1.0 + 0.5 * lvl * max(0.0, 1 - k))
        if lvl == 3 and t < T_BLAST3:
            st["mouth_open"] = min(2.0, 1.0 + 0.45 * (nope_word(t) + 1) * (0.4 + env("HERO", t)))
        st["squash"] = 0.35 * lvl * math.sin(min(1.0, k * 3) * math.pi) * (1 - k)
        st["arms"] = "up"
    if L["n6"] - 0.05 <= t < L["n7"] + 0.3:          # "Hey! Down here!" in the sky shot (drawn small)
        st["face"] = "happy"
        st["arms"] = "up"
        st["mouth_open"] = 0.6 + 1.2 * env("HERO", t)
    if L["n7"] + 0.3 <= t < L["n8"]:
        st["face"] = "deadpan"
        st["arms"] = "paddle"
    return st


# ---------------------------------------------------------------- the close shot (sea, her, the duck)
def streak(c, x0, y0, x1, y1, k, w=10, alpha=1.0, body=True):
    """A spacecraft coming in: a fiery woodblock trail from (x0, y0) toward (x1, y1), head at progress k."""
    hx, hy = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    tl = 0.35
    tx, ty = x0 + (x1 - x0) * max(0, k - tl), y0 + (y1 - y0) * max(0, k - tl)
    ang = math.atan2(y1 - y0, x1 - x0)
    nx, ny = -math.sin(ang), math.cos(ang)
    p = skia.Path()
    p.moveTo(tx, ty)
    p.quadTo((tx + hx) / 2 + nx * w * 0.8, (ty + hy) / 2 + ny * w * 0.8, hx + nx * w, hy + ny * w)
    p.lineTo(hx - nx * w, hy - ny * w)
    p.quadTo((tx + hx) / 2 - nx * w * 0.8, (ty + hy) / 2 - ny * w * 0.8, tx, ty)
    p.close()
    c.drawPath(p, fill(CORAL, alpha))
    inner = skia.Path()
    inner.moveTo((tx + hx * 2) / 3, (ty + hy * 2) / 3)
    inner.lineTo(hx + nx * w * 0.5, hy + ny * w * 0.5)
    inner.lineTo(hx - nx * w * 0.5, hy - ny * w * 0.5)
    inner.close()
    c.drawPath(inner, fill(YEL_L, alpha))
    c.drawPath(p, ink(2.5, alpha=alpha * 0.9))
    if body:
        c.drawCircle(hx, hy, w * 0.9, fill(INKC, alpha))
        c.drawCircle(hx, hy, w * 1.6, fill(rgb("#FFE9B0"), 0.25 * alpha))
    return hx, hy


def splash(c, x, y, k, size=1.0, alpha=1.0):
    """A woodblock splash: a crown of foam tongues that rises and falls."""
    if not 0 <= k <= 1:
        return
    hgt = 120 * size * math.sin(k * math.pi)
    for i in range(7):
        a = (i - 3) / 3
        bx = x + a * 70 * size * (0.6 + 0.6 * k)
        tip = (bx + a * 40 * size, y - hgt * (1 - 0.45 * abs(a)))
        p = skia.Path()
        p.moveTo(bx - 12 * size, y)
        p.quadTo(bx - 8 * size, y - hgt * 0.5, tip[0], tip[1])
        p.quadTo(bx + 8 * size, y - hgt * 0.5, bx + 12 * size, y)
        p.close()
        c.drawPath(p, fill(FOAM, alpha))
        c.drawPath(p, ink(2.5, alpha=alpha))
        c.drawCircle(tip[0] + a * 14 * size, tip[1] - 18 * size * k, 7 * size * (1 - k), fill(FOAM, alpha))
    # the foam it falls back into: a flat churned base, so a splash sits ON the water
    base = oval(x, y + 4 * size, 120 * size * (0.7 + 0.5 * k), 16 * size * (1 - 0.4 * k))
    c.drawPath(base, fill(FOAM, alpha * (1 - 0.5 * k)))
    c.drawPath(base, ink(2.5, alpha=alpha * (1 - 0.5 * k)))


def ring(c, x, y, r, alpha, width=8, front_only=False):
    p = skia.Path()
    rect = skia.Rect.MakeLTRB(x - r, y - r * 0.16, x + r, y + r * 0.16)
    if front_only:
        p.addArc(rect, 8, 164)
    else:
        p.addOval(rect)
    c.drawPath(p, ink(width, col=FOAM, alpha=alpha))


def frost(c, k):
    """Ice creeping in from the corners (water at 7 degrees)."""
    if k <= 0:
        return
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeRadial((W / 2, H * 0.45), H * 0.72,
                                                [skia.Color4f(0.85, 0.93, 1.0, 0), skia.Color4f(0.85, 0.93, 1.0, 0.55 * k)], [0.6, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)
    rng = np.random.default_rng(4)
    for _ in range(26):
        corner = rng.integers(4)
        cx = 0 if corner in (0, 2) else W
        cy = 0 if corner in (0, 1) else H
        a = math.atan2(H / 2 - cy, W / 2 - cx) + rng.uniform(-0.7, 0.7)
        ln = rng.uniform(60, 220) * k
        x1, y1 = cx + math.cos(a) * ln, cy + math.sin(a) * ln
        c.drawLine(cx, cy, x1, y1, ink(3, col=WHITE, alpha=0.7 * k))
        for j in (0.4, 0.7):
            bx, by = cx + math.cos(a) * ln * j, cy + math.sin(a) * ln * j
            for da in (-0.6, 0.6):
                c.drawLine(bx, by, bx + math.cos(a + da) * ln * 0.25, by + math.sin(a + da) * ln * 0.25,
                           ink(2, col=WHITE, alpha=0.6 * k))


T_DUCK_PASS = (L["n11"] + 0.1, WT("n11", "world") - 0.15)     # "Swim for it?": the duck overtakes her


def duck_x(t, xh=520, s=1.0):
    """Where the duck floats: beside her; it zips past her when she starts to swim; NOPE 2's wave surfs it back."""
    base, left = xh + 280 * s, xh - 400 * s
    a, b = T_DUCK_PASS
    if t < a:
        return base
    if t < b:
        return base + (left - base) * ease_io((t - a) / (b - a))
    a2, b2 = L["n15"] + 0.05, L["n15"] + 0.85
    if t < a2:
        return left
    if t < b2:
        return left + (base - left) * ease_io((t - a2) / (b2 - a2))
    return base


def impact_zone(c, x, y, k, t, back):
    """A dashed red ellipse painted on the sea around her: the ISS impact zone. back=True: the half behind her."""
    rx, ry = 430 * (0.6 + 0.4 * ease_io(k)), 70
    p = skia.Path()
    p.addArc(skia.Rect.MakeLTRB(x - rx, y - ry, x + rx, y + ry), 180 if back else 0, 180)
    pd = ink(7, col=SEAL, alpha=k * (0.7 if back else 1.0))
    pd.setPathEffect(skia.DashPathEffect.Make([26, 16], -twos(t) * 40))
    c.drawPath(p, pd)


def close_shot(c, t, sea=SEA_CLOSE, s=1.0, xh=520, cam_y=0.0, show_hero=True):
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 1.0)
    lvl, nk = nope_at(t)
    storm = 0.0
    c.save()
    c.translate(0, cam_y)
    horizon = sea.horizon
    sky(c, tw, horizon=horizon, sun=(870, 470), sun_r=78)
    blow = 0.0
    if t >= T_BLAST3:
        blow = min(1.0, (t - T_BLAST3) / 1.0)
    for (x0, y, w_, h_, sp) in ((-60, 250, 520, 46, 14), (560, 430, 620, 38, -10), (120, 520, 380, 28, 6)):
        x = x0 + sp * tw + (1400 * blow * (1 if x0 > 300 else -1) * ease_io(blow))
        mist_band(c, x, y, w_, h_, alpha=0.9)
    # the teaser from frame 0: something burning in over the sea (pays off in the graveyard)
    if t < L["n8"] or L["n10"] <= t < L["n16"]:
        k = (t % 12.0) / 12.0
        streak(c, 1060, 330, 700, 610, 0.24 + 0.5 * k, w=10, alpha=0.95)
    if t >= L["n22"] - 0.1:
        _iss_callback(c, t)
    for i in range(0, 5):
        sea.draw_layer(c, i, tw, boil, storm)
    if show_hero:
        st = hero_state(t)
        yw = float(sea.height(5, np.array([xh]), tw)[0])
        t30 = WT("n22", "2030")
        kz = ease_io(prog(t, t30 - 0.1, t30 + 0.5)) * (1 - prog(t, T_BLAST3, T_BLAST3 + 0.3))
        if kz > 0:
            impact_zone(c, xh, yw + 4, kz, t, back=True)
        draw_hero(c, xh, yw - 175 * s, s=s, face=st["face"], boil=boil, arms=st["arms"], t=tw,
                  blink=st["blink"], squash=st["squash"], look=st["look"], shiver=st["shiver"], mouth_open=st["mouth_open"])
        # the duck: never in danger
        dx = duck_x(t, xh, s)
        dy, drot = 0.0, -4.0
        if t >= T_BLAST3:                       # the third NOPE launches it over her, two flips, lands upright
            fly = min(1.0, (t - T_BLAST3) / 1.2)
            dx = dx + (xh - 300 * s - dx) * ease_io(fly)
            dy = -640 * math.sin(fly * math.pi)
            drot = -4 + 720 * ease_io(fly)
        yd = float(sea.height(5, np.array([dx]), tw)[0])
        a, b = T_DUCK_PASS
        if a <= t < b + 0.25:                  # its wake as it zips past
            kk = prog(t, a, b + 0.25)
            for j in range(4):
                yy = yd - 30 + j * 22
                c.drawLine(dx + 70, yy, dx + 70 + 220 * (1 - kk) * (1 - 0.15 * j), yy, ink(6, col=FOAM, alpha=0.9 * (1 - kk)))
        look = 1.0 if L["n10"] <= t < L["n11"] else 0.0
        draw_duck(c, dx, yd + 6 + dy, s=0.85 * s, boil=boil, tilt=drot, look=look)
        sea.draw_layer(c, 5, tw, boil, storm)
        if kz > 0:
            impact_zone(c, xh, yw + 4, kz, t, back=False)
        ring(c, xh, yw + 6, 200 * s, 0.85, 9, front_only=True)
        if t < 0.55:
            splash(c, xh - 170 * s, yw + 8, 0.3 + t / 0.55 * 0.7, size=0.7 * s)
            splash(c, xh + 190 * s, yw + 8, 0.35 + t / 0.55 * 0.65, size=0.6 * s)
        if lvl == 3 and t < T_BLAST3:          # the first two words of the last NOPE: small rings
            i = nope_word(t)
            kk = min(1.0, (t - W3[max(0, i)]) / 0.6)
            ring(c, xh, yw + 6, 200 * s + 260 * (i + 1) * kk, (1 - kk) * 0.9, 7, front_only=True)
        elif lvl:
            for j in range(lvl):
                rr = 200 * s + (500 + 400 * lvl) * min(1.0, nk * (1.4 - 0.2 * j))
                ring(c, xh, yw + 6, rr, (1 - nk) * 0.9, 6 + 3 * lvl, front_only=True)
            splash(c, xh - 230 * s, yw + 10, min(1.0, nk * 1.6), size=0.6 * lvl)
            splash(c, xh + 240 * s, yw + 10, min(1.0, nk * 1.4), size=0.5 * lvl)
        if st["arms"] == "swim":
            for j in range(3):
                kk = ((tw * 2.5 + j / 3) % 1)
                splash(c, xh + (-1) ** j * 210 * s, yw + 8, kk, size=0.45 * s, alpha=0.9)
    for i in range(6, 8):
        sea.draw_layer(c, i, tw, boil, storm)
    c.restore()


ISS_TWINKLE = (300, 250)


def _iss_callback(c, t):
    """n22: the space station comes in, glowing, toward her; the third NOPE blows it back up into space."""
    a = L["n22"] - 0.1
    k = ease_io(min(1.0, (t - a) / 2.6))
    x, y = 1030 - 200 * k, 110 + 330 * k
    sc = 1.0 + 1.3 * k
    if t >= T_BLAST3:
        b = min(1.0, (t - T_BLAST3) / 1.1)
        tx, ty = ISS_TWINKLE
        x, y = x + (tx - x) * ease_io(b), y + (ty - y) * ease_io(b) - 140 * math.sin(b * math.pi)
        sc *= (1 - 0.92 * b)
        if b >= 1.0:
            tw_ = (t - T_BLAST3 - 1.1) / 0.45
            if tw_ < 1:     # a twinkle where it vanished
                r = 36 * math.sin(tw_ * math.pi)
                star = skia.Path()
                for i in range(8):
                    rr = r if i % 2 == 0 else r * 0.3
                    ang = i * math.pi / 4
                    (star.moveTo if i == 0 else star.lineTo)(tx + rr * math.cos(ang), ty + rr * math.sin(ang))
                star.close()
                c.drawPath(star, fill(WHITE))
            return
    else:
        g = skia.Paint(AntiAlias=True)          # it is coming down: it glows
        g.setShader(skia.GradientShader.MakeRadial((x, y + 20), 95 * sc,
                                                    [skia.Color4f(1, 0.6, 0.35, 0.6 * k), skia.Color4f(1, 0.6, 0.35, 0)]))
        c.drawCircle(x, y + 20, 95 * sc, g)
    iss(c, x, y, s=sc, glint=0.4)


def stamp(c, x, y, s, size=90, k=1.0, rot=-5, col=None, txtcol=None, font_name="display"):
    """A red seal stamp that thumps in (k = 0..1)."""
    col = col or SEAL
    sc = 1.6 - 0.6 * ease_io(k) if k < 1 else 1.0
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


# ---------------------------------------------------------------- the chart (azimuthal equidistant on Point Nemo)
NEMO = (-48.8767, -123.3933)
R_EARTH = 6371.0
PLACES = [("DUCIE ISLAND", (-24.6667, -124.7833), "n4", "Two", "left"),
          ("MOTU NUI · EASTER ISLAND", (-27.2014, -109.4536), "n4", "islands", "below"),
          ("MAHER ISLAND · ANTARCTICA", (-72.9667, -126.3667), "n4", "one", "below")]


def aeqd(lat, lon, lat0=NEMO[0], lon0=NEMO[1]):
    la, lo, la0, lo0 = map(np.radians, (lat, lon, lat0, lon0))
    cosc = np.sin(la0) * np.sin(la) + np.cos(la0) * np.cos(la) * np.cos(lo - lo0)
    cc = np.arccos(np.clip(cosc, -1, 1))
    az = np.arctan2(np.cos(la) * np.sin(lo - lo0), np.cos(la0) * np.sin(la) - np.sin(la0) * np.cos(la) * np.cos(lo - lo0))
    d = cc * R_EARTH
    return d * np.sin(az), d * np.cos(az), d        # km east, km north, distance


def _land_rings():
    geo = json.load(open(os.path.join(HERE, "data", "ne_110m_land.geojson")))
    rings = []
    for f in geo["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            ring_ = np.array(poly[0])
            x, y, d = aeqd(ring_[:, 1], ring_[:, 0])
            if d.min() > 9000:
                continue
            cut = (np.abs(ring_[:, 0]) > 179.9) | (ring_[:, 1] < -84)     # Antarctica's seam along the dateline
            rings.append((x, y, d, cut, float(ring_[:, 1].mean()) < -60))     # last: ice (Antarctica)
    return rings


LAND = _land_rings()
MAP_CX, MAP_CY = 540, 930
MAP_KM = 330 / 2688.0           # px per km: the 2,688 km circle is 330 px


def map_xy(xkm, ykm, zoom=1.0):
    return MAP_CX + xkm * MAP_KM * zoom, MAP_CY - ykm * MAP_KM * zoom


T_KM0, T_KM1 = WT("n3", "2,688"), WT("n3", "km")     # the 2,688 km count runs while the number is said


def chart(c, t, zoom=1.0, alpha=1.0, me=None, labels=None, ruler=True):
    """The chart. me = where her marker is (default Point Nemo); labels = the place names to show (None = all)."""
    fi = int(t * FPS)
    boil = (fi // 2, 0.7)
    c.drawRect(skia.Rect.MakeWH(W, H), fill(rgb("#2A4E73")))
    sea_p = rrect(-10, -10, W + 20, H + 20, 0)
    mottle(c, sea_p, PRUSSIAN, alpha=0.18, scale=0.004, seed=21)
    # engraved swell lines
    for yy in range(80, H, 46):
        p = skia.Path()
        p.moveTo(-20, yy)
        for x in range(0, W + 40, 40):
            p.lineTo(x, yy + 5 * math.sin(x * 0.02 + yy * 0.3 + twos(t) * 1.5))
        c.drawPath(p, ink(2, col=FOAM, alpha=0.10))
    # graticule
    for lat in range(-80, 1, 10):
        lons = np.linspace(-180, 180, 361)
        x, y, d = aeqd(np.full_like(lons, lat), lons)
        ok = d < 9000
        pts = [map_xy(a, b, zoom) for a, b, o in zip(x, y, ok) if o]
        if len(pts) > 2:
            c.drawPath(smooth_path(pts, closed=False), ink(1.5, col=FOAM, alpha=0.16))
    for lon in range(-180, 180, 15):
        lats = np.linspace(-89, 10, 120)
        x, y, d = aeqd(lats, np.full_like(lats, lon))
        pts = [map_xy(a, b, zoom) for a, b, dd in zip(x, y, d) if dd < 9000]
        if len(pts) > 2:
            c.drawPath(smooth_path(pts, closed=False), ink(1.5, col=FOAM, alpha=0.16))
    # land
    for x, y, d, cut, ice in LAND:
        p = skia.Path()
        coast = skia.Path()
        pen = False
        for i, (a, b) in enumerate(zip(x, y)):
            px, py = map_xy(a, b, zoom)
            (p.moveTo if i == 0 else p.lineTo)(px, py)
            if cut[i]:
                pen = False
                continue
            if pen:
                coast.lineTo(px, py)
            else:
                coast.moveTo(px, py)
                pen = True
        p.close()
        c.drawPath(p, fill(rgb("#F3F1EA") if ice else rgb("#E9DDBF")))
        mottle(c, p, rgb("#BFD3E6") if ice else PAPER, alpha=0.25 if ice else 0.2, scale=0.02, seed=5)
        c.drawPath(coast, ink(3, boil=boil))
    # the 2,688 km circle, drawn on as the number is said
    k = ease_io(prog(t, T_KM0, T_KM1))
    r = 2688 * MAP_KM * zoom
    arc = skia.Path()
    arc.addArc(skia.Rect.MakeLTRB(MAP_CX - r, MAP_CY - r, MAP_CX + r, MAP_CY + r), -90, 360 * k)
    pa = ink(6, col=YEL_L)
    pa.setPathEffect(skia.DashPathEffect.Make([22, 14], 0))
    c.drawPath(arc, pa)
    if k > 0 and ruler:
        # radius ruler
        c.drawLine(MAP_CX, MAP_CY, MAP_CX + r * math.cos(math.radians(-30)), MAP_CY + r * math.sin(math.radians(-30)), ink(4, col=YEL_L, alpha=k))
    # the three nearest bits of land
    for name, (la, lo), key, word, side in PLACES:
        tk = WT(key, word)
        kk = prog(t, tk - 0.1, tk + 0.25)
        if kk <= 0:
            continue
        x, y, d = aeqd(la, lo)
        px, py = map_xy(float(x), float(y), zoom)
        pin(c, px, py, name if labels is None or name in labels else None, kk, side=side)
    # Point Nemo: her, tiny
    mx, my = me or (MAP_CX, MAP_CY)
    c.drawCircle(mx, my, 16, fill(YEL))
    c.drawCircle(mx, my - 14, 8, fill(rgb("#3B2420")))
    c.drawCircle(mx, my, 16, ink(4))
    if labels is None or "POINT NEMO" in labels:
        text(c, "POINT NEMO", MAP_CX, MAP_CY + 58, font("mono", 34), FOAM, align="center", stroke=8)
    compass(c, 905, 1560, 70)


def pin(c, x, y, name, k, side="up"):
    sc = ease_io(min(1, k * 1.3))
    c.save()
    c.translate(x, y)
    c.scale(sc, sc)
    p = skia.Path()
    p.moveTo(0, 0)
    p.cubicTo(-30, -36, -26, -66, 0, -66)
    p.cubicTo(26, -66, 30, -36, 0, 0)
    c.drawPath(p, fill(SEAL))
    c.drawPath(p, ink(4))
    c.drawCircle(0, -44, 9, fill(FOAM))
    c.restore()
    if not name:
        return
    f = font("mono", 32)
    wv = f.measureText(name)
    if side == "left":
        tx, ty = x - 40 - wv / 2, y - 96
    elif side == "right":
        tx, ty = x + 30 + wv / 2, y - 40
    elif side == "below":
        tx, ty = x, y + 56
    else:
        tx, ty = x, y - 86
    tx = min(max(tx, 40 + wv / 2), W - 40 - wv / 2)
    c.drawPath(rrect(tx - wv / 2 - 12, ty - 32, wv + 24, 44, 8), fill(PAPER_HI, k))
    c.drawPath(rrect(tx - wv / 2 - 12, ty - 32, wv + 24, 44, 8), ink(3, alpha=k))
    text(c, name, tx, ty, f, INKC, align="center", alpha=k)


def compass(c, x, y, r):
    for i, ang in enumerate(range(0, 360, 45)):
        a = math.radians(ang - 90)
        rr = r if i % 2 == 0 else r * 0.55
        p = skia.Path()
        p.moveTo(x, y)
        p.lineTo(x + math.cos(a - 0.22) * rr * 0.3, y + math.sin(a - 0.22) * rr * 0.3)
        p.lineTo(x + math.cos(a) * rr, y + math.sin(a) * rr)
        p.close()
        c.drawPath(p, fill(FOAM if i % 2 == 0 else CORAL))
        c.drawPath(p, ink(2.5))
    text(c, "N", x, y - r - 12, font("mono", 30), FOAM, align="center", stroke=6)


def map_shot(c, t):
    a = shot_start("map")
    # iris: the sea close-up shrinks into the Point Nemo dot while the chart comes in
    k_in = ease_io(prog(t, a, a + 0.6))
    k_out = ease_io(prog(t, L["n5"] - 0.45, L["n5"] - 0.1))
    zoom = 1.35 - 0.35 * k_in
    chart(c, t, zoom=zoom)
    if k_in < 1:
        r = max(16, (1 - k_in) * 1300)
        c.save()
        clip = skia.Path()
        clip.addCircle(MAP_CX, MAP_CY, r)
        c.clipPath(clip, doAntiAlias=True)
        close_shot(c, t)
        c.restore()
        c.drawCircle(MAP_CX, MAP_CY, r, ink(8))
    if k_out > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), fill(PAPER, k_out))


# ---------------------------------------------------------------- the sky shot: her, tiny, and the ISS 400 km up
def sky_shot(c, t):
    a = shot_start("sky")
    k = ease_io(prog(t, a, a + 0.5))
    pan = (1 - k) * -900                       # the frame tilts up from the sea
    fi = int(t * FPS)
    boil = (fi // 2, 1.0)
    tw = twos(t)
    c.drawRect(skia.Rect.MakeWH(W, H), fill(rgb("#132A47")))      # the tilt never shows an empty edge
    c.save()
    c.translate(0, -pan * 0.3)
    c.drawRect(skia.Rect.MakeXYWH(0, 300, W, H), fill(PAPER))
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeLinear([(0, 0), (0, 1180)], [rgb("#132A47"), rgb("#2E5F8E"),
                                                                    skia.Color4f(PAPER.fR, PAPER.fG, PAPER.fB, 1)],
                                               [0.0, 0.55, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, 1500), p)
    rng = np.random.default_rng(7)
    for _ in range(70):
        x, y = rng.uniform(0, W), rng.uniform(0, 760)
        tw_ = 0.5 + 0.5 * math.sin(t * rng.uniform(2, 5) + x)
        c.drawCircle(x, y, rng.uniform(1.5, 3.2), fill(FOAM, 0.5 + 0.4 * tw_))
    mist_band(c, -80 + 10 * tw, 900, 560, 40, alpha=0.9)
    mist_band(c, 600 - 8 * tw, 1010, 520, 34, alpha=0.85)
    # the station crosses
    # it passes right over her as "space" is said
    ts = WT("n5", "space")
    ix = 560 + (t - ts) * 170
    iy = 600 - 0.00012 * (ix - 560) ** 2 * 1.0
    iss(c, ix, iy, s=2.6, glint=0.0, light=True)
    # the sea, low in the frame, and her
    sea = SEA_SKY
    for i in range(0, 4):
        sea.draw_layer(c, i, tw, boil)
    st = hero_state(t)
    yw = float(sea.height(4, np.array([540]), tw)[0])
    draw_hero(c, 540, yw - 76, s=0.40, face=st["face"], boil=boil, arms=st["arms"], t=tw, blink=st["blink"],
              look=(0, -9) if st["face"] != "deadpan" else (0, 2), mouth_open=st["mouth_open"])
    draw_duck(c, 660, float(sea.height(4, np.array([660]), tw)[0]) + 2, s=0.36, boil=boil, look=0)
    for i in range(4, 8):
        sea.draw_layer(c, i, tw, boil)
    # 400 km, measured
    kl = ease_io(prog(t, WT("n5", "space") - 0.3, WT("n5", "space") + 0.4))
    if kl > 0:
        x0, y0, x1, y1 = 540, 1150, ix, iy + 40          # starts just above the caption line
        pd = ink(5, col=YEL_L)
        pd.setPathEffect(skia.DashPathEffect.Make([18, 12], 0))
        c.drawLine(x0, y0, x0 + (x1 - x0) * kl, y0 + (y1 - y0) * kl, pd)
        if kl > 0.6:
            stamp(c, min(x0, x1) - 175, (y0 + y1) / 2, "400 km", size=58, k=min(1, (kl - 0.6) / 0.3), rot=-4, col=INKC, txtcol=YEL_L, font_name="mono")
    c.restore()


# ---------------------------------------------------------------- the duck, up close
def duck_shot(c, t):
    fi = int(t * FPS)
    boil = (fi // 2, 1.0)
    tw = twos(t)
    sea = Sea(horizon=560, seed=11)
    sky(c, tw, horizon=560, sun=(300, 330), sun_r=96)
    mist_band(c, 380 + 8 * tw, 420, 560, 40, alpha=0.9)
    for i in range(0, 4):
        sea.draw_layer(c, i, tw, boil)
    yd = float(sea.height(4, np.array([540]), tw)[0])
    draw_duck(c, 500, yd + 60, s=3.2, boil=None, tilt=4 * math.sin(tw * 1.6), look=0.0)
    for i in range(4, 8):
        sea.draw_layer(c, i, tw, boil)
    # its survival time: no clock needed
    kk = prog(t, WT("n18", "floated") - 0.2, WT("n18", "floated") + 0.1)
    if kk > 0:
        stamp(c, 400, 370, "YEARS", size=110, k=kk, rot=-7)


# ---------------------------------------------------------------- the graveyard: spacecraft rain, the seafloor below
FALLERS = [(0.0, 1000, -60, 720, 842, 22), (0.35, 120, -80, 360, 846, 16), (0.7, 760, -120, 560, 850, 26), (1.0, 1140, 60, 900, 845, 14),
           (1.3, 300, -140, 200, 852, 18), (1.6, 640, -160, 460, 848, 24), (1.9, 1080, -80, 1000, 846, 15), (2.2, 0, -40, 110, 850, 14),
           (2.5, 880, -140, 640, 844, 20), (2.8, 460, -160, 300, 850, 22), (3.1, 980, -100, 820, 846, 16), (3.4, 200, -120, 420, 850, 18)]


def capsule(c, x, y, r, rot):
    """A falling capsule: a blunt cone, heat shield first."""
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    p = skia.Path()
    p.moveTo(-r, r * 0.2)
    p.lineTo(-r * 0.45, -r * 1.3)
    p.lineTo(r * 0.45, -r * 1.3)
    p.lineTo(r, r * 0.2)
    p.quadTo(0, r * 0.9, -r, r * 0.2)
    p.close()
    c.drawPath(p, fill(rgb("#8B8792")))
    sh = skia.Path()
    sh.moveTo(-r, r * 0.2)
    sh.quadTo(0, r * 0.9, r, r * 0.2)
    sh.quadTo(0, r * 0.45, -r, r * 0.2)
    c.drawPath(sh, fill(rgb("#FF9A4A")))
    c.drawPath(p, ink(3))
    c.drawCircle(0, -r * 0.5, r * 0.22, fill(FOAM))
    c.restore()


def graveyard_shot(c, t):
    a = shot_start("graveyard")
    fi = int(t * FPS)
    boil = (fi // 2, 1.0)
    tw = twos(t)
    sea = SEA_WIDE
    cut = ease_io(prog(t, L["n21"] - 0.2, L["n21"] + 0.7))       # the frame lifts: we see down to the floor
    lift = -880 * cut
    c.save()
    c.translate(0, lift)
    sky(c, tw, horizon=sea.horizon, sun=(860, 560), sun_r=80)
    c.drawRect(skia.Rect.MakeWH(W, sea.horizon), fill(rgb("#3B1F2E"), 0.25))       # dusk: something is burning up
    mist_band(c, -40 + 8 * tw, 380, 600, 40, alpha=0.85)
    mist_band(c, 520 - 6 * tw, 600, 600, 32, alpha=0.8)
    for (d0, x0, y0, x1, y1, w_) in FALLERS:
        st = a + 0.2 + d0
        k = (t - st) / 1.2
        if 0 <= k <= 1:
            hx, hy = streak(c, x0, y0, x1, y1, k, w=w_, body=False)
            capsule(c, hx, hy, w_ * 1.1, math.degrees(math.atan2(y1 - y0, x1 - x0)) - 90)
    for i in range(0, 6):
        sea.draw_layer(c, i, tw, boil)
        if i == 2:
            for (d0, x0, y0, x1, y1, w_) in FALLERS:
                k = (t - (a + 0.2 + d0) - 1.2) / 0.9
                if 0 <= k <= 1:
                    splash(c, x1, y1 + 4, k, size=0.3 + w_ * 0.035)
    for i in range(6, 8):
        sea.draw_layer(c, i, tw, boil)
    # under the surface: the column down to the floor, about 4 km
    top = 1650
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeLinear([(0, top), (0, top + 900)], [rgb("#112842"), rgb("#070F1D")]))
    c.drawRect(skia.Rect.MakeXYWH(0, top, W, 1400), p)
    floor = smooth_path([(-20, top + 560), (200, top + 530), (420, top + 570), (640, top + 520), (860, top + 560),
                         (1100, top + 535), (1100, top + 1400), (-20, top + 1400)])
    c.drawPath(floor, fill(rgb("#2B2A33")))
    c.drawPath(floor, ink(3, col=rgb("#5A5866")))
    rng = np.random.default_rng(12)
    for j in range(7):        # pieces still on their way down
        sx_ = 120 + j * 140 + 30 * math.sin(j * 2.1)
        sy_ = top + 80 + ((t * 60 + j * 97) % 420)
        c.save()
        c.translate(sx_, sy_)
        c.rotate(20 * math.sin(t + j))
        c.drawPath(rrect(-22, -10, 44, 20, 5), fill(rgb("#5E5A66"), 0.8))
        c.drawPath(rrect(-22, -10, 44, 20, 5), ink(2, col=rgb("#1B1A22"), alpha=0.8))
        c.restore()
        for b in range(3):
            c.drawCircle(sx_ + 8 * math.sin(t * 3 + b), sy_ - 30 - b * 22, 4 - b, ink(1.5, col=FOAM, alpha=0.4))
    n_show = int(min(1.0, prog(t, L["n21"], E["n21"])) * 70)
    for i in range(70):
        if i >= n_show:
            break
        x = rng.uniform(40, 1040)
        y = top + 535 + rng.uniform(-14, 26)
        kind = rng.integers(3)
        ang = rng.uniform(-30, 30)
        c.save()
        c.translate(x, y)
        c.rotate(ang)
        c.scale(1.6, 1.6)
        if kind == 0:
            c.drawPath(rrect(-26, -12, 52, 24, 6), fill(rgb("#6E6A72")))
            c.drawPath(rrect(-26, -12, 52, 24, 6), ink(2.5, col=rgb("#1B1A22")))
        elif kind == 1:
            pp = skia.Path()
            pp.moveTo(-20, 14)
            pp.lineTo(0, -22)
            pp.lineTo(20, 14)
            pp.close()
            c.drawPath(pp, fill(rgb("#7C756C")))
            c.drawPath(pp, ink(2.5, col=rgb("#1B1A22")))
        else:
            c.drawRect(skia.Rect.MakeXYWH(-30, -4, 60, 8), fill(rgb("#8A6C3A")))
            c.drawRect(skia.Rect.MakeXYWH(-30, -4, 60, 8), ink(2, col=rgb("#1B1A22")))
        c.restore()
    if cut > 0.9:                      # the label waits until the frame has stopped moving
        f = font("mono", 44)
        c.drawLine(100, top + 20, 100, top + 520, ink(4, col=FOAM, alpha=0.7))
        for yy in range(top + 20, top + 521, 50):
            c.drawLine(90, yy, 112, yy, ink(3, col=FOAM, alpha=0.7))
        text(c, "≈ 4 km DOWN", 132, top + 300, f, FOAM, alpha=cut, stroke=8)
    c.restore()


# ---------------------------------------------------------------- the swim, on the chart: 0.00 % there... 18 days
T_GO = WT("n11", "non-stop") - 0.05          # the time-lapse starts on "non-stop"
SWIM_DY = 90                                  # the chart sits a little lower here, under the two-row card


def swim_p(t):
    return prog(t, T_GO, T_18)


def swim_map(c, t):
    a = shot_start("swim_map")
    kz = ease_io(prog(t, a, a + 0.3))
    zoom = 1.12 - 0.12 * kz
    x, y, d = aeqd(*PLACES[0][1])
    px, py = map_xy(float(x), float(y), zoom)
    p = swim_p(t)
    mx, my = MAP_CX + (px - MAP_CX) * p, MAP_CY + (py - MAP_CY) * p
    c.drawRect(skia.Rect.MakeWH(W, H), fill(rgb("#2A4E73")))
    c.save()
    c.translate(0, SWIM_DY)
    chart(c, t, zoom=zoom, me=(mx, my), labels={"DUCIE ISLAND"}, ruler=False)
    if p > 0:                          # her track across the ocean
        pd = ink(7, col=YEL_L)
        pd.setPathEffect(skia.DashPathEffect.Make([4, 16], 0))
        c.drawLine(MAP_CX, MAP_CY, mx, my, pd)
        c.drawCircle(MAP_CX, MAP_CY, 10, ink(4, col=YEL_L))
        draw_hero_dot(c, mx, my)
    else:                              # at world-record pace: tiny ripples, going nowhere
        for j in range(3):
            kk = (twos(t) * 2 + j / 3) % 1
            c.drawCircle(MAP_CX, MAP_CY, 20 + 46 * kk, ink(4, col=FOAM, alpha=0.8 * (1 - kk)))
    c.restore()


def draw_hero_dot(c, x, y):
    c.drawCircle(x, y, 16, fill(YEL))
    c.drawCircle(x, y - 14, 8, fill(rgb("#3B2420")))
    c.drawCircle(x, y, 16, ink(4))


def swim_rows(t):
    p = swim_p(t)
    rows = [("SWIM TO LAND", f"{100 * p:.2f} %", INKC, 0.0)]
    if t >= T_GO:
        rows.append(("NON-STOP", f"DAY {int(18 * p + 1e-6)}", SEAL, max(0.0, 1 - (t - T_18) * 4) if t >= T_18 else 0.0))
    return rows


# ---------------------------------------------------------------- half underwater: 4 km of water under her feet
WL_UNDER = 900
SEA_ABOVE = Sea(horizon=640, seed=13, layers=[(660, 3, 0.2), (700, 6, 0.3), (760, 9, 0.4), (830, 12, 0.5), (905, 14, 0.6),
                                             (1000, 16, 0.7), (1100, 18, 0.8), (1200, 20, 0.9)])
UNDER_S = 0.8


def waterline(x, tw):
    return WL_UNDER + 9 * np.sin(x * 0.011 + tw * 2.2) + 5 * np.sin(x * 0.027 - tw * 3.1)


def legs(c, tw, boil):
    """Her legs treading water (hero coordinates: head centre at 0, 0; s = 1)."""
    for side in (-1, 1):
        ph = tw * 2.4 + (0 if side < 0 else math.pi)
        hip = (side * 60, 380)
        knee = (side * 92 + 30 * math.sin(ph), 600)
        foot = (side * 70 + 46 * math.sin(ph + 0.8), 790)
        pth = skia.Path()
        pth.moveTo(*hip)
        pth.quadTo(knee[0], knee[1], foot[0], foot[1])
        c.drawPath(pth, ink(84, boil=boil))
        c.drawPath(pth, ink(70, col=rgb("#2A3656")))
        shoe = oval(foot[0] + side * 10, foot[1] + 26, 46, 26)
        c.drawPath(shoe, fill(WHITE))
        c.drawPath(shoe, ink(6, boil=boil))
        c.drawLine(foot[0] + side * 10 - 40, foot[1] + 44, foot[0] + side * 10 + 40, foot[1] + 44, ink(8, col=CORAL))
    hem = smooth_path([(-168, 300), (168, 300), (160, 420), (0, 432), (-160, 420)])
    c.drawPath(hem, fill(YEL))
    c.drawPath(rrect(-160, 392, 320, 34, 12), fill(YEL_D))
    c.drawPath(hem, ink(6, boil=boil))


def strike_sign(c, x, y, k, tw):
    """ON STRIKE: a cardboard picket sign, held up by an arm that has quit."""
    if k <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(-24 + 3 * math.sin(tw * 3))
    sc = 1.2 * ease_io(min(1.0, k)) * (1 + 0.25 * max(0.0, 1 - k * 2))
    c.scale(sc, sc)
    c.drawLine(0, 0, 0, -205, ink(16))
    c.drawLine(0, 0, 0, -205, ink(10, col=rgb("#A9793F")))
    board = rrect(-84, -300, 168, 128, 8)
    c.drawPath(board, fill(rgb("#D9B57B")))
    mottle(c, board, rgb("#C79F62"), alpha=0.3, scale=0.05)
    c.drawPath(board, ink(5))
    text(c, "ON", 0, -250, font("display", 46), SEAL, align="center")
    text(c, "STRIKE", 0, -194, font("display", 46), INKC, align="center")
    c.restore()


def under_shot(c, t):
    fi = int(t * FPS)
    boil = (fi // 2, 1.0)
    tw = twos(t)
    s = UNDER_S
    cx, cy = 540, WL_UNDER - 175 * s
    sky(c, tw, horizon=640, sun=(850, 430), sun_r=70)
    mist_band(c, -60 + 10 * tw, 520, 520, 36, alpha=0.85)
    for i in range(0, 5):
        SEA_ABOVE.draw_layer(c, i, tw, boil)
    xs = np.linspace(-40, W + 40, 90)
    ys = waterline(xs, tw)
    body = smooth_path(list(zip(xs.tolist(), ys.tolist())), closed=False)
    body.lineTo(W + 40, H + 40)
    body.lineTo(-40, H + 40)
    body.close()
    g = skia.Paint(AntiAlias=True)
    g.setShader(skia.GradientShader.MakeLinear([(0, WL_UNDER), (0, H)], [rgb("#3C7EA6"), rgb("#1C4467"), rgb("#07152A")],
                                               [0.0, 0.42, 1.0]))
    c.drawPath(body, g)
    c.save()
    c.clipPath(body, doAntiAlias=True)
    woodgrain(c, body, alpha=0.07, seed=31)
    for j in range(5):                  # light from the surface
        x0 = 120 + j * 210 + 40 * math.sin(tw * 0.8 + j)
        ray = skia.Path()
        ray.moveTo(x0 - 26, WL_UNDER)
        ray.lineTo(x0 + 26, WL_UNDER)
        ray.lineTo(x0 + 190, H)
        ray.lineTo(x0 + 40, H)
        ray.close()
        c.drawPath(ray, fill(FOAM, 0.07))
    rng = np.random.default_rng(17)
    for _ in range(40):                 # marine snow
        x = rng.uniform(0, W)
        y = WL_UNDER + 40 + (rng.uniform(0, 1000) - tw * 14) % 1000
        c.drawCircle(x, y, rng.uniform(1.5, 3.5), fill(FOAM, 0.35))
    c.restore()
    # her: legs and hoodie under the water, head above it
    st = hero_state(t)
    if st["face"] == "nope":                     # NOPE 1 is over: back to worrying
        st.update(face="worried", mouth_open=None)
    arms = "limp" if t >= T_ARMS - 0.2 else "paddle"
    c.save()
    c.translate(cx, cy)
    c.scale(s, s)
    legs(c, tw, boil)
    c.restore()
    draw_hero(c, cx, cy, s=s, face=st["face"], boil=boil, arms=arms, t=tw, blink=st["blink"], look=st["look"],
              shiver=st["shiver"], mouth_open=st["mouth_open"])
    # the duck, at the surface (half above, half below)
    dxu = 820
    draw_duck(c, dxu, float(waterline(np.array([dxu]), tw)[0]) + 6, s=0.7, boil=boil, tilt=-4)
    # everything under the line is seen through the water
    c.save()
    c.clipPath(body, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeWH(W, H), fill(rgb("#2B6A99"), 0.30))
    for j in range(5):                  # bubbles off her legs
        k = ((tw * 0.6 + j / 5) % 1)
        bx = 540 + (-1) ** j * (50 + 14 * j) + 10 * math.sin(tw * 3 + j)
        by = cy + 760 * s - k * 560
        c.drawCircle(bx, by, 6 + 3 * (j % 2), ink(2.5, col=FOAM, alpha=0.7 * (1 - k)))
    c.restore()
    c.drawPath(smooth_path(list(zip(xs.tolist(), ys.tolist())), closed=False), ink(6, col=FOAM))
    for j in range(9):                  # bright scallops just under the surface
        x = 60 + j * 120 + 20 * math.sin(tw + j)
        y = float(waterline(np.array([x]), tw)[0]) + 16
        c.drawLine(x - 26, y, x + 26, y, ink(4, col=FOAM, alpha=0.5))
    # 4 km of water under her feet
    gx = 150
    pd = ink(4, col=FOAM, alpha=0.8)
    pd.setPathEffect(skia.DashPathEffect.Make([18, 12], -tw * 30))
    c.drawLine(gx, WL_UNDER + 40, gx, 1440, pd)
    ar = skia.Path()
    ar.moveTo(gx - 16, 1418)
    ar.lineTo(gx, 1446)
    ar.lineTo(gx + 16, 1418)
    c.drawPath(ar, ink(4, col=FOAM, alpha=0.8))
    text(c, "≈ 4 km", gx + 22, WL_UNDER + 112, font("mono", 40), FOAM, stroke=8)
    text(c, "OF WATER", gx + 22, WL_UNDER + 152, font("mono", 32), FOAM, stroke=8)
    # her arms quit: they go on strike
    hx = cx - 176 * s
    hy = cy + 330 * s
    strike_sign(c, hx, hy, prog(t, T_ARMS + 0.02, T_ARMS + 0.32), tw)


# ---------------------------------------------------------------- the survival clock, big
LOG_LO, LOG_HI = math.log(20), math.log(12000)


def dial_ang(sec):
    return 135 + 270 * (math.log(max(20.0, sec)) - LOG_LO) / (LOG_HI - LOG_LO)


def seigaiha(c, t, base=None, line=None, r=64, alpha=0.2):
    """Seigaiha, the woodblock wave-scale pattern, drifting slowly."""
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


def crack(c, x, y, scale=1.0, alpha=1.0, seed=3):
    rng = np.random.default_rng(seed)
    for i in range(8):
        a = i * math.pi / 4 + rng.uniform(-0.3, 0.3)
        px, py = x, y
        pth = skia.Path()
        pth.moveTo(px, py)
        ln = rng.uniform(70, 170) * scale
        for _ in range(4):
            a += rng.uniform(-0.45, 0.45)
            px += math.cos(a) * ln / 4
            py += math.sin(a) * ln / 4
            pth.lineTo(px, py)
        c.drawPath(pth, ink(6, alpha=0.35 * alpha))
        c.drawPath(pth, ink(3, col=WHITE, alpha=0.9 * alpha))
    ringp = skia.Path()
    ringp.addCircle(x, y, 26 * scale)
    pd = ink(3, col=WHITE, alpha=0.8 * alpha)
    pd.setPathEffect(skia.DashPathEffect.Make([14, 9], 0))
    c.drawPath(ringp, pd)


CLOCK_C = (540, 880, 290)
GOLD, GOLD_D = rgb("#C9973E"), rgb("#8E6524")


def clock_shot(c, t):
    a = shot_start("clock")
    b = shot_start("duck")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    seigaiha(c, t)
    cx, cy, R = CLOCK_C
    k_in = ease_io(prog(t, a, a + 0.3))
    z = 1.3 - 0.3 * k_in + 0.05 * prog(t, a + 0.3, b)
    pop = max(0.0, 1 - (t - T_REVEAL) / 0.25) if t >= T_REVEAL else 0.0
    z *= 1 + 0.06 * pop
    c.save()
    c.translate(cx, cy)
    c.scale(z, z)
    c.rotate(2 * math.sin(t * 1.3))
    c.translate(-cx, -cy)
    c.drawCircle(cx + 16, cy + 22, R + 40, fill(INKC, 0.4))
    # the bow and crown on top
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
    # the 1-10-1 scale round the dial (log time: 1 min, 10 min, 1 h, 3 h)
    rr = R * 0.8
    rect = skia.Rect.MakeLTRB(cx - rr, cy - rr, cx + rr, cy + rr)
    base = skia.Path()
    base.addArc(rect, 135, 270)
    c.drawPath(base, ink(30, col=rgb("#DCCFB0")))
    v = story_clock(t) or 0.0
    if t < T_REVEAL:
        fillp = skia.Path()
        fillp.addArc(rect, 135, max(1.0, dial_ang(v) - 135))
        c.drawPath(fillp, ink(30, col=PRUSSIAN))
    else:
        kk = ease_io(prog(t, T_REVEAL, T_REVEAL + 0.35))
        band = skia.Path()
        a0 = dial_ang(3600)
        band.addArc(rect, a0, (dial_ang(10800) - a0) * kk)
        c.drawPath(band, ink(40, col=SEAL))
    for i in range(28):
        ang = math.radians(135 + 270 * i / 27)
        c.drawLine(cx + math.cos(ang) * R * 0.93, cy + math.sin(ang) * R * 0.93, cx + math.cos(ang) * R * 0.98,
                   cy + math.sin(ang) * R * 0.98, ink(3))
    for sec, lab in ((60, "1 MIN"), (600, "10 MIN"), (3600, "1 H"), (10800, "3 H")):
        ang = math.radians(dial_ang(sec))
        c.drawLine(cx + math.cos(ang) * R * 0.68, cy + math.sin(ang) * R * 0.68, cx + math.cos(ang) * R * 0.92,
                   cy + math.sin(ang) * R * 0.92, ink(5))
        lx, ly = cx + math.cos(ang) * R * 0.52, cy + math.sin(ang) * R * 0.52 + 11
        text(c, lab, lx, ly, font("mono", 32), INKC, align="center")
    # the needle: jittery while it works it out, then it swings into 1-3 hours
    if t < T_REVEAL:
        spin = L["n16"] <= t
        ang = dial_ang(v) + (14 * math.sin(t * 31) + 9 * math.sin(t * 47) if spin else 0)
    else:
        e = t - T_REVEAL
        ang = dial_ang(6235) + 22 * math.exp(-e * 5) * math.cos(e * 18)
    a_ = math.radians(ang)
    nd = skia.Path()
    nd.moveTo(cx + math.cos(a_) * R * 0.74, cy + math.sin(a_) * R * 0.74)
    nd.lineTo(cx + math.cos(a_ + 1.57) * 12, cy + math.sin(a_ + 1.57) * 12)
    nd.lineTo(cx - math.cos(a_) * 40, cy - math.sin(a_) * 40)
    nd.lineTo(cx + math.cos(a_ - 1.57) * 12, cy + math.sin(a_ - 1.57) * 12)
    nd.close()
    c.drawPath(nd, fill(SEAL if t >= T_REVEAL else INKC))
    c.drawPath(nd, ink(3))
    c.drawCircle(cx, cy, 18, fill(INKC))
    c.drawCircle(cx, cy, 7, fill(GOLD))
    # the readout
    text(c, "YOU'VE SURVIVED", cx, cy + 150, font("mono", 32), mixc(INKC, PAPER, 0.3), align="center")
    if t < T_REVEAL:
        if L["n16"] <= t:
            r_ = np.random.default_rng(int(t * 24))
            s_ = f"{r_.integers(0, 4):02d}:{r_.integers(0, 60):02d}:{r_.integers(0, 60):02d}"
        else:
            s_ = fmt_clock(v)
        text(c, s_, cx, cy + 222, font("mono", 64), INKC, align="center")
    else:
        kk = prog(t, T_REVEAL, T_REVEAL + 0.2)
        sz = 70 * (1.5 - 0.5 * ease_io(kk))
        text(c, "1–3 HOURS", cx, cy + 226, font("display", sz), SEAL, align="center")
    # the glass: a shine, and the crack NOPE 2 put in it
    sh = skia.Path()
    sh.addArc(skia.Rect.MakeLTRB(cx - R * 0.86, cy - R * 0.86, cx + R * 0.86, cy + R * 0.86), 200, 50)
    c.drawPath(sh, ink(14, col=WHITE, alpha=0.5))
    crack(c, cx + R * 0.42, cy - R * 0.5, 1.0)
    c.restore()


# ---------------------------------------------------------------- HUD, intercom, NOPE, captions, end cards
def hud(c, t):
    """Top-left cartouche: one story number at a time. Hidden while a NOPE owns the frame."""
    shot = shot_at(t)[1]
    lvl, nk = nope_at(t)
    lvl = lvl if shot == "close" else 0          # a NOPE only clears the HUD in its own shot
    title_on = t < E["n1"] + 0.15
    rows = []
    if shot == "swim_map":
        rows = swim_rows(t)
    elif not lvl:
        if t < L["n8"] - 0.15 and shot in ("close", "map"):
            k = ease_io(prog(t, T_KM0, T_KM1))
            val = "???? km" if k < 0.04 else f"{int(2688 * k):,} km"
            rows.append(("NEAREST LAND", val, INKC, 0.0))
        if shot == "close" and L["n8"] <= t < L["n18"] - 0.1:
            rows.append(("WATER", "7 °C · 45 °F", PRUSSIAN, max(0.0, 1 - (t - WT("n8", "seven")) * 3)))
        if WT("n21", "260") - 0.05 <= t < L["n22"] - 0.05:
            n = max(1, int(min(1.0, prog(t, WT("n21", "260"), WT("n21", "were") + 0.2)) * 260))
            rows.append(("SPACECRAFT DROPPED", f"{n}+", SEAL, 0.0))
        t30 = WT("n22", "2030")
        if t30 - 0.1 <= t < L["n23"] - 0.05:
            rows.append(("ISS IMPACT ZONE", "~2030", SEAL, max(0.0, 1 - (t - t30) * 3)))
    y = 290
    if rows:
        if title_on:                      # frame 0: under the title, a question mark where the number will be
            hud_card(c, SAFE_X0 + 30, 470, rows, w=600)
        else:
            hud_card(c, SAFE_X0, y, rows, w=600)
            y += 30 + 78 * len(rows) + 24
    if not lvl and shot in ("close", "under") and t < L["n16"]:
        clock_bar(c, t, y)
    # the hook, on frame 0: the series question with the place (no caption for n1: this is it)
    if title_on:
        f1, f2 = font("mono", 38), font("display", 112)
        c.save()
        c.translate(W / 2, 300)
        c.rotate(-3)
        tag = "COULD YOU SURVIVE"
        wv = f1.measureText(tag)
        c.drawPath(rrect(-wv / 2 - 18, -40, wv + 36, 56, 10), fill(INKC, 0.92))
        text(c, tag, 0, 2, f1, YEL_L, align="center")
        text(c, "POINT NEMO?", 0, 130, f2, FOAM, align="center", stroke=22)
        c.restore()
    ks = prog(t, 3.0, 3.3)                # the seal arrives once the hook has done its job
    if ks > 0:
        seal(c, 874, 120, 86, alpha=ks)


def clock_bar(c, t, y):
    """The survival clock and its 1-10-1 bar (1 min, 10 min, 1 h, 3 h on a log scale)."""
    v = story_clock(t)
    if v is None:
        return
    x0, w = SAFE_X0, 600
    card = rrect(x0, y, w, 156, 14)
    c.drawPath(rrect(x0 + 8, y + 10, w, 156, 14), fill(INKC, 0.25))
    c.drawPath(card, fill(PAPER_HI, 0.96))
    mottle(c, card, PAPER, alpha=0.12, scale=0.03, seed=8)
    c.drawPath(card, ink(4))
    c.drawPath(rrect(x0 + 8, y + 8, w - 16, 140, 9), ink(1.6, alpha=0.7))
    text(c, "YOU'VE SURVIVED", x0 + 24, y + 46, font("mono", 32), mixc(INKC, PAPER, 0.3))
    text(c, fmt_clock(v), x0 + w - 24, y + 52, font("mono", 46), INKC, align="right")
    bx, by, bw = x0 + 24, y + 80, w - 48
    lo, hi = LOG_LO, LOG_HI

    def X(sec):
        return bx + bw * (math.log(max(20, sec)) - lo) / (hi - lo)
    c.drawPath(rrect(bx, by, bw, 14, 7), fill(rgb("#D9CDB0")))
    c.drawPath(rrect(bx, by, max(14, X(v) - bx), 14, 7), fill(PRUSSIAN))
    for sec, lab in ((60, "1 MIN"), (600, "10 MIN"), (3600, "1 H"), (10800, "3 H")):
        x = X(sec)
        c.drawLine(x, by - 6, x, by + 20, ink(3))
        text(c, lab, min(x, x0 + w - 44), by + 56, font("mono", 30), INKC, align="center")


def intercom(c, t):
    """The lab's voice: a little speaker card that slides in from the right while it talks (inside the safe zone)."""
    live = [k for k in KEYS if WHO[k] == "LAB" and L[k] - 0.35 <= t <= E[k] + 0.35]
    if not live:
        return
    k = live[0]
    kin = ease_io(min(prog(t, L[k] - 0.35, L[k] - 0.05), 1 - prog(t, E[k] + 0.05, E[k] + 0.35)))
    x = SAFE_X1 - 230 + (1 - kin) * 560
    y = 680 if k == "n25" else 440
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
    if "Noted" in TXT[k]:                 # "Noted.": a red tick on the card
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
    if not lvl or shot_at(t)[1] != "close":       # a NOPE never spills into the next shot
        return
    if lvl == 3:
        i = nope_word(t)
        word = ("nope.", "NOPE.", "NOOOPE!")[max(0, i)]
        size = (150, 200, 250)[max(0, i)]
        k = 0.0 if i < 2 else k
        if i < 2:        # the two small ones: each word pops in on its own
            k = min(0.7, (t - W3[max(0, i)]) / 1.2)
    else:
        word = {1: "nope.", 2: "NOPE!"}[lvl]
        size = (120, 200)[lvl - 1]
    f = font("display", size)
    wv = f.measureText(word)
    pop = 1.0 + 0.5 * max(0.0, 1 - k * 5)
    sc = min(pop, 680 / wv)              # the pop is inside the width limit: never wider than the safe zone
    alpha = 1.0 if k < 0.75 else max(0.0, 1 - (k - 0.75) / 0.25)
    c.save()
    c.translate(CAP_CX + math.sin(t * 90) * 4 * lvl, 600 if lvl < 3 else 560)    # above her head, never over her face
    c.rotate(-6 + 3 * lvl * math.sin(t * 50) * (1 - k))
    c.scale(sc, sc)
    text(c, word, 0, 0, f, YEL_L if (lvl < 3 or nope_word(t) < 2) else rgb("#FF6B4A"), align="center", alpha=alpha, stroke=26)
    if lvl == 3 and nope_word(t) == 2:   # cracks
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
    if lvl == 1:                          # for people watching on mute: the joke is the voice
        text(c, "[comically deep voice]", CAP_CX, 1235, font("mono", 40), FOAM, align="center", alpha=alpha, stroke=10)


def captions(c, t):
    for k in KEYS:
        if k in NOPES or k == "n1" or not (L[k] - 0.05 <= t <= E[k] + 0.25):
            continue
        for ch in CHUNKS[k]:
            t0 = ch[0][1] - 0.05
            nxt = [c2 for c2 in CHUNKS[k] if c2[0][1] > ch[0][1]]
            t1 = (nxt[0][0][1] - 0.05) if nxt else E[k] + 0.25
            if t0 <= t < t1:
                words = [w for w, _ in ch]
                active = max([i for i, (_, wt) in enumerate(ch) if wt <= t] or [0])
                y = 1235
                words_caption(c, words, active, y=y, size=74 if WHO[k] != "LAB" else 66)
                return


def end_cards(c, t):
    a = L["n24"]
    if t < a:
        return
    gone = 1 - prog(t, E["n25"] - 0.1, E["n25"] + 0.1)          # the cards clear before the respawn flash
    if gone <= 0:
        return
    opts = [("A", "SAHARA", "Sahara"), ("B", "ANCIENT ROME", "Ancient"), ("C", "EVEREST", "Everest")]
    dim = ease_io(prog(t, a, a + 0.4)) * gone
    c.drawRect(skia.Rect.MakeWH(W, H), fill(INKC, 0.35 * dim))
    for i, (letter, name, word) in enumerate(opts):
        tk = WT("n24", word)
        k = ease_io(prog(t, tk - 0.15, tk + 0.15)) * gone
        if k <= 0:
            continue
        x, y = SAFE_X0 + 10, 300 + i * 122
        c.save()
        c.translate(x + 330, y + 50)
        c.scale(0.8 + 0.2 * k, 0.8 + 0.2 * k)
        c.translate(-(x + 330), -(y + 50))
        c.drawPath(rrect(x + 8, y + 10, 640, 104, 16), fill(INKC, 0.35 * k))
        c.drawPath(rrect(x, y, 640, 104, 16), fill(PAPER_HI, k))
        c.drawPath(rrect(x, y, 640, 104, 16), ink(4, alpha=k))
        c.drawCircle(x + 58, y + 52, 34, fill(SEAL, k))
        text(c, letter, x + 58, y + 69, font("display", 46), FOAM, align="center", alpha=k)
        text(c, name, x + 112, y + 70, font("display", 50), INKC, alpha=k)
        icon(c, i, x + 570, y + 52, k * 0.9)
        c.restore()


def icon(c, i, x, y, k):
    if i == 0:    # dune and sun
        c.drawCircle(x + 10, y - 18, 18, fill(CORAL, k))
        p = smooth_path([(x - 50, y + 36), (x - 10, y + 2), (x + 30, y + 20), (x + 54, y + 36)], closed=False)
        p.lineTo(x + 54, y + 40)
        p.lineTo(x - 50, y + 40)
        p.close()
        c.drawPath(p, fill(YEL, k))
        c.drawPath(p, ink(3, alpha=k))
    elif i == 1:  # a column
        c.drawRect(skia.Rect.MakeXYWH(x - 34, y - 40, 68, 12), fill(PAPER, k))
        c.drawRect(skia.Rect.MakeXYWH(x - 22, y - 28, 44, 56), fill(PAPER, k))
        c.drawRect(skia.Rect.MakeXYWH(x - 34, y + 28, 68, 12), fill(PAPER, k))
        for r in (skia.Rect.MakeXYWH(x - 34, y - 40, 68, 12), skia.Rect.MakeXYWH(x - 22, y - 28, 44, 56),
                  skia.Rect.MakeXYWH(x - 34, y + 28, 68, 12)):
            c.drawRect(r, ink(3, alpha=k))
        for dx in (-10, 0, 10):
            c.drawLine(x + dx, y - 24, x + dx, y + 24, ink(2, alpha=k))
    else:         # a mountain with a flag
        p = skia.Path()
        p.moveTo(x - 54, y + 40)
        p.lineTo(x - 4, y - 36)
        p.lineTo(x + 54, y + 40)
        p.close()
        c.drawPath(p, fill(rgb("#7D8FA6"), k))
        snow = skia.Path()
        snow.moveTo(x - 20, y - 12)
        snow.lineTo(x - 4, y - 36)
        snow.lineTo(x + 14, y - 10)
        snow.lineTo(x + 2, y - 16)
        snow.close()
        c.drawPath(snow, fill(WHITE, k))
        c.drawPath(p, ink(3, alpha=k))
        c.drawLine(x - 4, y - 36, x - 4, y - 62, ink(3, alpha=k))
        fl = skia.Path()
        fl.moveTo(x - 4, y - 62)
        fl.lineTo(x + 20, y - 55)
        fl.lineTo(x - 4, y - 48)
        fl.close()
        c.drawPath(fl, fill(SEAL, k))


def respawn_flash(c, t):
    """The loop: 'three... two...' and the lab presses the button: a cream flash, and she spawns at frame 0."""
    a = E["n25"] + 0.02
    if t >= a:
        k = prog(t, a, DURATION)
        c.drawRect(skia.Rect.MakeWH(W, H), fill(PAPER_HI, ease_io(min(1, k * 1.6))))


def cam_close(t):
    """Camera on the close shot: a slow push-out over the hook, punch-ins on the NOPEs, a slow push-in at the end."""
    z = 1.0
    if t < shot_start("map"):
        z = 1.10 - 0.10 * ease_io(prog(t, 1.5, shot_start("map")))
    elif t >= L["n24"]:
        z = 1.0 + 0.06 * ease_io(prog(t, L["n24"], DURATION))
    return z * punch(t)


# ---------------------------------------------------------------- frame
def draw_frame(c, t):
    sx, sy = shake(t)
    c.save()
    c.translate(sx, sy)
    shot = shot_at(t)[1]
    if shot == "close":
        z = cam_close(t)
        if z != 1.0:
            fy = float(SEA_CLOSE.height(5, np.array([520]), twos(t))[0]) - 175
            c.translate(520, fy)
            c.scale(z, z)
            c.translate(-520, -fy)
        close_shot(c, t)
        if L["n8"] <= t < L["n18"]:
            frost(c, min(1.0, (t - L["n8"]) / 3.0) * 0.55)
    elif shot == "map":
        map_shot(c, t)
    elif shot == "swim_map":
        swim_map(c, t)
    elif shot == "under":
        under_shot(c, t)
    elif shot == "clock":
        clock_shot(c, t)
    elif shot == "sky":
        sky_shot(c, t)
    elif shot == "duck":
        duck_shot(c, t)
    elif shot == "graveyard":
        graveyard_shot(c, t)
    c.restore()
    paper_over(c, 1.0)
    vignette(c, 0.26)
    hud(c, t)
    # stamps land on the story, above the HUD
    if shot == "swim_map" and t >= T_18 - 0.05:
        stamp(c, 540, 860, "18 DAYS", size=110, k=prog(t, T_18 - 0.05, T_18 + 0.2), rot=-6)
    intercom(c, t)
    end_cards(c, t)
    nope_text(c, t)
    captions(c, t)
    respawn_flash(c, t)
