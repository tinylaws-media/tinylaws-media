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
                  iss, Sea, draw_hero, draw_duck, paper_over, vignette, seal, mottle, words_caption,
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
CAP = {"n3": "Nearest land: almost 2,700 km.", "n21": "More than 260 were dropped out here.",
       "n17": "In water this cold, about 1 to 3 hours.", "n25": "Respawning in 3... 2..."}
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
        x = len(w) + 1
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
SHOTS = [
    (0.0, "close"),
    (E["n2"] + 0.05, "map"),            # zoom out to the chart
    (L["n5"] - 0.1, "sky"),             # tilt up: the ISS
    (L["n8"] - 0.15, "close"),
    (L["n18"] - 0.1, "duck"),
    (L["n20"] - 0.05, "graveyard"),
    (L["n22"] - 0.05, "close"),
]


def shot_at(t):
    cur = SHOTS[0]
    for s in SHOTS:
        if t >= s[0]:
            cur = s
    return cur


SEA_CLOSE = Sea(horizon=600)
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
        st["face"] = "deadpan" if t < L["n25"] else "worried"
        st["shiver"] = 0.4
    lvl, k = nope_at(t)
    if lvl and k < 0.85:
        st["face"] = "nope"
        st["mouth_open"] = 1.0 + 0.9 * lvl * max(0.0, 1 - k)
        if lvl == 3 and t < T_BLAST3:
            st["mouth_open"] = 1.0 + 0.8 * (nope_word(t) + 1) * (0.4 + env("HERO", t))
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
    # what flies over: the ISS (n22 callback) and the teaser streak from frame 0 on
    if t < L["n8"] or L["n10"] <= t < L["n16"]:
        k = (t % 12.0) / 12.0
        streak(c, 980, 60, 760, 520, 0.25 + 0.5 * k, w=6, alpha=0.55)
    if t >= L["n22"] - 0.1:
        _iss_callback(c, t)
    for i in range(0, 5):
        sea.draw_layer(c, i, tw, boil, storm)
    if show_hero:
        st = hero_state(t)
        yw = float(sea.height(5, np.array([xh]), tw)[0])
        # the spawn: she drops in at frame 0, loops from the respawn at the end
        drop = 0.0
        draw_hero(c, xh, yw - 175 * s + drop, s=s, face=st["face"], boil=boil, arms=st["arms"], t=tw,
                  blink=st["blink"], squash=st["squash"], look=st["look"], shiver=st["shiver"], mouth_open=st["mouth_open"])
        # the duck: never in danger; launched by the third NOPE, lands upright
        dx = xh + 280 * s
        yd = float(sea.height(5, np.array([dx]), tw)[0])
        dy, drot = 0.0, -4.0
        if lvl == 3 and t >= T_BLAST3:
            fly = min(1.0, (t - T_BLAST3) / 1.2)
            dy = -900 * math.sin(fly * math.pi)
            drot = 720 * fly
        elif lvl == 2:
            dx += 120 * math.sin(min(1, nk * 2) * math.pi / 2) * (1 - nk)
        look = 1.0 if L["n10"] <= t < L["n11"] else 0.0
        draw_duck(c, dx, yd + 6 + dy, s=0.85 * s, boil=boil, tilt=drot, look=look)
        sea.draw_layer(c, 5, tw, boil, storm)
        ring(c, xh, yw + 6, 200 * s, 0.85, 9, front_only=True)
        if t < 0.55:
            splash(c, xh - 170 * s, yw + 8, 0.3 + t / 0.55 * 0.7, size=0.7 * s)
            splash(c, xh + 190 * s, yw + 8, 0.35 + t / 0.55 * 0.65, size=0.6 * s)
        if lvl == 3 and t < T_BLAST3:          # the first two words of the last NOPE: small rings
            i = nope_word(t)
            kk = min(1.0, (t - W3[max(0, i)]) / 0.6)
            ring(c, xh, yw + 6, 200 * s + 260 * (i + 1) * kk, (1 - kk) * 0.9, 7)
        elif lvl:
            for j in range(lvl):
                rr = 200 * s + (500 + 400 * lvl) * min(1.0, nk * (1.4 - 0.2 * j))
                ring(c, xh, yw + 6, rr, (1 - nk) * 0.9, 6 + 3 * lvl)
            splash(c, xh - 230 * s, yw + 10, min(1.0, nk * 1.6), size=0.6 * lvl)
            splash(c, xh + 240 * s, yw + 10, min(1.0, nk * 1.4), size=0.5 * lvl)
        if st["arms"] == "swim":
            for j in range(3):
                kk = ((tw * 2.5 + j / 3) % 1)
                splash(c, xh + (-1) ** j * 210 * s, yw + 8, kk, size=0.45 * s, alpha=0.9)
    for i in range(6, 8):
        sea.draw_layer(c, i, tw, boil, storm)
    c.restore()


def _iss_callback(c, t):
    """n22: the space station from the start, now with a target on it; the third NOPE blows it back up."""
    a = L["n22"] - 0.1
    k = min(1.0, (t - a) / 2.6)
    x, y = 760 - 140 * k, 150 + 200 * ease_io(k)
    sc = 1.2 + 1.3 * ease_io(k)
    lvl, nk = nope_at(t)
    if t >= T_BLAST3:
        b = min(1.0, (t - T_BLAST3) / 1.2)
        x, y = x + 260 * b, y - 500 * ease_io(b)
        sc *= (1 - 0.85 * b)
        if b >= 1.0:
            tw_ = min(1.0, (t - T_BLAST3 - 1.2) / 0.5)
            if tw_ < 1:     # the twinkle where it vanished
                cx, cy = 880, -110 + 260
                r = 30 * math.sin(tw_ * math.pi)
                star = skia.Path()
                for i in range(8):
                    rr = r if i % 2 == 0 else r * 0.3
                    ang = i * math.pi / 4
                    (star.moveTo if i == 0 else star.lineTo)(cx + rr * math.cos(ang), cy + rr * math.sin(ang))
                star.close()
                c.drawPath(star, fill(WHITE))
            return
    if t < T_BLAST3:
        # it is coming down: a glow under it
        g = skia.Paint(AntiAlias=True)
        g.setShader(skia.GradientShader.MakeRadial((x, y + 30), 160 * sc / 2,
                                                    [skia.Color4f(1, 0.6, 0.35, 0.55 * k), skia.Color4f(1, 0.6, 0.35, 0)]))
        c.drawCircle(x, y + 30, 160 * sc / 2, g)
    iss(c, x, y, s=sc, glint=0.4)
    if t < T_BLAST3:
        r = 70 * sc * (1.1 + 0.08 * math.sin(t * 9))
        c.drawCircle(x, y, r, ink(5, col=SEAL))
        for ang in (0, 90, 180, 270):
            a_ = math.radians(ang)
            c.drawLine(x + math.cos(a_) * r * 0.75, y + math.sin(a_) * r * 0.75, x + math.cos(a_) * r * 1.2,
                       y + math.sin(a_) * r * 1.2, ink(5, col=SEAL))
        if t >= WT("n22", "2030") - 0.1:
            stamp(c, x, y + r + 70, "2030", size=64, k=min(1.0, (t - WT("n22", "2030") + 0.1) / 0.25), rot=-6)


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
          ("MOTU NUI · EASTER ISLAND", (-27.2014, -109.4536), "n4", "islands", "right"),
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
            rings.append((x, y, d, cut))
    return rings


LAND = _land_rings()
MAP_CX, MAP_CY = 540, 930
MAP_KM = 330 / 2688.0           # px per km: the 2,688 km circle is 330 px


def map_xy(xkm, ykm, zoom=1.0):
    return MAP_CX + xkm * MAP_KM * zoom, MAP_CY - ykm * MAP_KM * zoom


def chart(c, t, zoom=1.0, alpha=1.0):
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
    for x, y, d, cut in LAND:
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
        c.drawPath(p, fill(rgb("#E9DDBF")))
        mottle(c, p, PAPER, alpha=0.2, scale=0.02, seed=5)
        c.drawPath(coast, ink(3, boil=boil))
    # the 2,688 km circle, drawn on as the number is said
    k = ease_io(prog(t, L["n3"] + 0.2, WT("n3", "2,700") + 0.6))
    r = 2688 * MAP_KM * zoom
    arc = skia.Path()
    arc.addArc(skia.Rect.MakeLTRB(MAP_CX - r, MAP_CY - r, MAP_CX + r, MAP_CY + r), -90, 360 * k)
    pa = ink(6, col=YEL_L)
    pa.setPathEffect(skia.DashPathEffect.Make([22, 14], 0))
    c.drawPath(arc, pa)
    if k > 0:
        # radius ruler
        c.drawLine(MAP_CX, MAP_CY, MAP_CX + r * math.cos(math.radians(-30)), MAP_CY + r * math.sin(math.radians(-30)), ink(4, col=YEL_L, alpha=k))
        mx, my = MAP_CX + r * 0.55 * math.cos(math.radians(-30)), MAP_CY + r * 0.55 * math.sin(math.radians(-30))
        lab = "2,688 km"
        f = font("mono", 40)
        c.save()
        c.translate(mx, my - 18)
        c.rotate(-30)
        wv = f.measureText(lab)
        c.drawPath(rrect(-wv / 2 - 12, -38, wv + 24, 52, 10), fill(INKC, 0.85 * k))
        text(c, lab, 0, 0, f, YEL_L, align="center", alpha=k)
        c.restore()
    # the three nearest bits of land
    for name, (la, lo), key, word, side in PLACES:
        tk = WT(key, word)
        kk = prog(t, tk - 0.1, tk + 0.25)
        if kk <= 0:
            continue
        x, y, d = aeqd(la, lo)
        px, py = map_xy(float(x), float(y), zoom)
        pin(c, px, py, name, kk, side=side)
    # Point Nemo: her, tiny
    c.drawCircle(MAP_CX, MAP_CY, 16, fill(YEL))
    c.drawCircle(MAP_CX, MAP_CY - 14, 8, fill(rgb("#3B2420")))
    c.drawCircle(MAP_CX, MAP_CY, 16, ink(4))
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
    f = font("mono", 30)
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
    a = SHOTS[1][0]
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
    a = SHOTS[2][0]
    k = ease_io(prog(t, a, a + 0.5))
    pan = (1 - k) * -900                       # the frame tilts up from the sea
    fi = int(t * FPS)
    boil = (fi // 2, 1.0)
    tw = twos(t)
    c.save()
    c.translate(0, -pan * 0.3)
    c.drawRect(skia.Rect.MakeWH(W, H), fill(PAPER))
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeLinear([(0, 0), (0, 1400)], [rgb("#132A47"), rgb("#2E5F8E"),
                                                                    skia.Color4f(PAPER.fR, PAPER.fG, PAPER.fB, 1)],
                                               [0.0, 0.55, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, 1500), p)
    rng = np.random.default_rng(7)
    for _ in range(70):
        x, y = rng.uniform(0, W), rng.uniform(0, 760)
        tw_ = 0.5 + 0.5 * math.sin(t * rng.uniform(2, 5) + x)
        c.drawCircle(x, y, rng.uniform(1.5, 3.2), fill(FOAM, 0.5 + 0.4 * tw_))
    mist_band(c, -80 + 10 * tw, 1180, 560, 40, alpha=0.9)
    mist_band(c, 600 - 8 * tw, 1290, 520, 34, alpha=0.85)
    # the station crosses
    # it passes right over her as "space" is said
    ts = WT("n5", "space")
    ix = 560 + (t - ts) * 170
    iy = 600 - 0.00012 * (ix - 560) ** 2 * 1.0
    iss(c, ix, iy, s=2.6, glint=0.0, light=True)
    # the sea, low in the frame, and her
    sea = Sea(horizon=1520, seed=3, layers=[(1540, 3, 0.2), (1575, 6, 0.3), (1625, 10, 0.4), (1700, 16, 0.5),
                                            (1790, 22, 0.6), (1880, 30, 0.7), (1990, 40, 0.85), (2100, 50, 1.0)])
    for i in range(0, 4):
        sea.draw_layer(c, i, tw, boil)
    st = hero_state(t)
    yw = float(sea.height(4, np.array([540]), tw)[0])
    draw_hero(c, 540, yw - 80, s=0.42, face=st["face"], boil=boil, arms=st["arms"], t=tw, blink=st["blink"],
              look=(0, -9) if st["face"] != "deadpan" else (0, 2), mouth_open=st["mouth_open"])
    draw_duck(c, 660, float(sea.height(4, np.array([660]), tw)[0]) + 2, s=0.36, boil=boil, look=0)
    for i in range(4, 8):
        sea.draw_layer(c, i, tw, boil)
    # 400 km, measured
    kl = ease_io(prog(t, WT("n5", "space") - 0.3, WT("n5", "space") + 0.4))
    if kl > 0:
        x0, y0, x1, y1 = 540, yw - 200, ix, iy + 40
        pd = ink(5, col=YEL_L)
        pd.setPathEffect(skia.DashPathEffect.Make([18, 12], 0))
        c.drawLine(x0, y0, x0 + (x1 - x0) * kl, y0 + (y1 - y0) * kl, pd)
        if kl > 0.6:
            stamp(c, (x0 + x1) / 2 + 170, (y0 + y1) / 2, "400 km", size=58, k=min(1, (kl - 0.6) / 0.3), rot=-4, col=INKC, txtcol=YEL_L, font_name="mono")
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
    draw_duck(c, 500, yd + 60, s=3.2, boil=boil, tilt=4 * math.sin(tw * 1.6), look=0.0)
    for i in range(4, 8):
        sea.draw_layer(c, i, tw, boil)
    # its survival time: no clock needed
    kk = prog(t, WT("n18", "floated") - 0.2, WT("n18", "floated") + 0.1)
    if kk > 0:
        stamp(c, 420, 400, "YEARS", size=110, k=kk, rot=-7)
    if t >= L["n19"] - 0.05:
        kk = prog(t, L["n19"] - 0.05, L["n19"] + 0.2)
        # the lab's clipboard tick
        cx, cy = 860, 520
        c.drawPath(rrect(cx - 70, cy - 80, 140, 170, 14), fill(PAPER_HI, kk))
        c.drawPath(rrect(cx - 70, cy - 80, 140, 170, 14), ink(4, alpha=kk))
        p = skia.Path()
        p.moveTo(cx - 34, cy + 6)
        p.lineTo(cx - 8, cy + 34)
        p.lineTo(cx + 40, cy - 30)
        c.drawPath(p, ink(12, col=SEAL, alpha=kk))


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
    a = SHOTS[5][0]
    fi = int(t * FPS)
    boil = (fi // 2, 1.0)
    tw = twos(t)
    sea = SEA_WIDE
    cut = ease_io(prog(t, L["n21"] - 0.2, L["n21"] + 0.7))       # the frame lifts: we see down to the floor
    lift = -560 * cut
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
    c.drawRect(skia.Rect.MakeXYWH(0, top, W, 1000), p)
    floor = smooth_path([(-20, top + 760), (200, top + 730), (420, top + 770), (640, top + 720), (860, top + 760),
                         (1100, top + 735), (1100, top + 1000), (-20, top + 1000)])
    c.drawPath(floor, fill(rgb("#2B2A33")))
    c.drawPath(floor, ink(3, col=rgb("#5A5866")))
    rng = np.random.default_rng(12)
    for j in range(7):        # pieces still on their way down
        sx_ = 120 + j * 140 + 30 * math.sin(j * 2.1)
        sy_ = top + 80 + ((t * 60 + j * 97) % 600)
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
        y = top + 735 + rng.uniform(-14, 26)
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
    if cut > 0.3:
        f = font("mono", 44)
        c.drawLine(70, top + 20, 70, top + 720, ink(4, col=FOAM, alpha=0.7))
        for yy in range(top + 20, top + 721, 70):
            c.drawLine(60, yy, 82, yy, ink(3, col=FOAM, alpha=0.7))
        text(c, "≈ 4 km DOWN", 100, top + 440, f, FOAM, alpha=cut, stroke=8)
    c.restore()


# ---------------------------------------------------------------- HUD, intercom, NOPE, captions, end cards
def hud(c, t):
    shot = shot_at(t)[1]
    rows = []
    if L["n3"] <= t < L["n8"] - 0.15:
        k = ease_io(prog(t, L["n3"] + 0.2, WT("n3", "2,700") + 0.6))
        rows.append(("NEAREST LAND", f"{int(2688 * k):,} km", INKC, 0.0))
    if L["n5"] <= t < L["n8"] - 0.15 and t >= WT("n5", "space") - 0.2:
        rows.append(("NEAREST HUMANS", "↑ 400 km", SEAL, max(0.0, 1 - (t - WT("n5", "space")) * 3)))
    if L["n8"] <= t < L["n18"] - 0.1:
        rows.append(("WATER", "7 °C · 45 °F", PRUSSIAN, max(0.0, 1 - (t - WT("n8", "seven")) * 3)))
    if L["n21"] - 0.1 <= t < L["n22"] - 0.05:
        n = int(min(1.0, prog(t, L["n21"], WT("n21", "dropped"))) * 260)
        rows.append(("SPACECRAFT DROPPED HERE", f"{n}+", SEAL, 0.0))
    lvl, nk = nope_at(t)
    rot = 0.0
    if t >= T_BLAST3 + 0.1:
        rot = 7.0 * min(1.0, (t - T_BLAST3 - 0.1) / 0.2)       # the third NOPE knocked the HUD crooked
    c.save()
    c.translate(SAFE_X0 + 280, 330)
    c.rotate(rot)
    c.translate(-(SAFE_X0 + 280), -330)
    y = 290
    if rows:
        from sz2d import hud_card
        hud_card(c, SAFE_X0, y, rows, w=600)
        y += 30 + 74 * len(rows) + 24
    clock_bar(c, t, y)
    c.restore()
    # the hook, on frame 0: the series question with the place (no caption for n1: this is it)
    if t < E["n1"] + 0.15 or t > E["n25"]:
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
    seal(c, 874, 120, 86)


def clock_bar(c, t, y):
    """The survival clock and its 1-10-1 bar (1 min, 10 min, 1 h, 3 h on a log scale)."""
    v = story_clock(t)
    if v is None or t >= L["n18"] - 0.1:
        return
    x0, w = SAFE_X0, 600
    c.drawPath(rrect(x0 + 8, y + 10, w, 150, 14), fill(INKC, 0.25))
    c.drawPath(rrect(x0, y, w, 150, 14), fill(PAPER_HI, 0.96))
    c.drawPath(rrect(x0, y, w, 150, 14), ink(4))
    text(c, "YOU'VE SURVIVED", x0 + 24, y + 42, font("mono", 24), mixc(INKC, PAPER, 0.35))
    spinning = L["n16"] <= t < T_REVEAL
    if spinning:
        s = f"{np.random.default_rng(int(t * 24)).integers(0, 4):02d}:{np.random.default_rng(int(t * 24) + 1).integers(0, 60):02d}:{np.random.default_rng(int(t * 24) + 2).integers(0, 60):02d}"
    elif t >= T_REVEAL:
        s = "1 – 3 h"
    else:
        s = fmt_clock(v)
    text(c, s, x0 + w - 24, y + 48, font("mono", 46), SEAL if t >= T_REVEAL else INKC, align="right")
    # the bar
    bx, by, bw = x0 + 24, y + 92, w - 48
    marks = [(60, "1 MIN"), (600, "10 MIN"), (3600, "1 H"), (10800, "3 H")]
    lo, hi = math.log(20), math.log(12000)

    def X(sec):
        return bx + bw * (math.log(max(20, sec)) - lo) / (hi - lo)
    c.drawPath(rrect(bx, by, bw, 14, 7), fill(rgb("#D9CDB0")))
    if t >= T_REVEAL:
        kk = ease_io(prog(t, T_REVEAL, T_REVEAL + 0.4))
        c.drawPath(rrect(X(3600), by - 4, (X(10800) - X(3600)) * kk, 22, 11), fill(SEAL))
    else:
        c.drawPath(rrect(bx, by, max(14, X(v) - bx), 14, 7), fill(PRUSSIAN))
    for sec, lab in marks:
        x = X(sec)
        c.drawLine(x, by - 6, x, by + 20, ink(3))
        text(c, lab, x, by + 46, font("mono", 20), INKC, align="center")


def intercom(c, t):
    """The lab's voice: a little speaker card that slides in from the right while it talks."""
    live = [k for k in KEYS if WHO[k] == "LAB" and L[k] - 0.35 <= t <= E[k] + 0.35]
    if not live:
        return
    k = live[0]
    kin = ease_io(min(prog(t, L[k] - 0.35, L[k] - 0.05), 1 - prog(t, E[k] + 0.05, E[k] + 0.35)))
    x = W - 40 - 250 * kin
    y = 230
    c.drawPath(rrect(x + 8, y + 10, 230, 96, 14), fill(INKC, 0.3 * kin))
    c.drawPath(rrect(x, y, 230, 96, 14), fill(INKC, 0.95 * kin))
    c.drawCircle(x + 46, y + 48, 26, fill(rgb("#33405E"), kin))
    for r in (8, 15, 22):
        c.drawCircle(x + 46, y + 48, r, ink(2.5, col=FOAM, alpha=0.6 * kin))
    text(c, "LAB", x + 86, y + 40, font("mono", 26), YEL_L, alpha=kin)
    for i in range(9):
        e = env("LAB", t - i * 0.03)
        hgt = 6 + 34 * e * (0.6 + 0.4 * math.sin(i * 1.7 + t * 20))
        c.drawPath(rrect(x + 88 + i * 14, y + 70 - hgt / 2, 8, hgt, 4), fill(FOAM, kin))
    if k == "n25":
        for word, num in (("three", "3"), ("two", "2")):
            tk = WT("n25", word if word != "three" else "3")
        # the countdown is in the caption


def nope_text(c, t):
    lvl, k = nope_at(t)
    if not lvl:
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
    sc = min(1.0, (W - 100) / wv)
    pop = 1.0 + 0.5 * max(0.0, 1 - k * 5)
    alpha = 1.0 if k < 0.75 else max(0.0, 1 - (k - 0.75) / 0.25)
    c.save()
    c.translate(W / 2 + math.sin(t * 90) * 4 * lvl, 1170 if lvl < 3 else 560)      # 1 and 2 under her chin; the big one in the sky
    c.rotate(-6 + 3 * lvl * math.sin(t * 50) * (1 - k))
    c.scale(sc * pop, sc * pop)
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
                if WHO[k] == "LAB":
                    f = font("mono", 26)
                    text(c, "LAB", CAP_CX, y - 96, f, YEL_L, align="center", stroke=8)
                words_caption(c, words, active, y=y, size=74 if WHO[k] != "LAB" else 66)
                return


def end_cards(c, t):
    a = L["n24"]
    if t < a:
        return
    opts = [("A", "SAHARA", "Sahara"), ("B", "ANCIENT ROME", "Ancient"), ("C", "EVEREST", "Everest")]
    dim = ease_io(prog(t, a, a + 0.4))
    c.drawRect(skia.Rect.MakeWH(W, H), fill(INKC, 0.35 * dim))
    for i, (letter, name, word) in enumerate(opts):
        tk = WT("n24", word)
        k = ease_io(prog(t, tk - 0.15, tk + 0.15))
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
        seal(c, W / 2 - 90 * (1 + k), H / 2 - 90 * (1 + k), 180 * (1 + k), alpha=1 - k * 0.3)


# ---------------------------------------------------------------- frame
def draw_frame(c, t):
    sx, sy = shake(t)
    c.save()
    c.translate(sx, sy)
    shot = shot_at(t)[1]
    if shot == "close":
        z = punch(t)
        if z != 1.0:
            fy = float(SEA_CLOSE.height(5, np.array([520]), twos(t))[0]) - 175
            c.translate(520, fy)
            c.scale(z, z)
            c.translate(-520, -fy)
        close_shot(c, t)
        if L["n8"] <= t < L["n18"]:
            frost(c, min(1.0, (t - L["n8"]) / 3.0) * (0.55 if t < L["n17"] else 0.9))
    elif shot == "map":
        map_shot(c, t)
    elif shot == "sky":
        sky_shot(c, t)
    elif shot == "duck":
        duck_shot(c, t)
    elif shot == "graveyard":
        graveyard_shot(c, t)
    c.restore()
    paper_over(c, 1.0)
    vignette(c, 0.26)
    # stamps that land on the story
    kk = prog(t, T_18 - 0.05, T_18 + 0.2)
    if 0 < kk and t < L["n13"]:
        stamp(c, 540, 560, "18 DAYS", size=110, k=kk, rot=-6)
    if L["n17"] <= t < L["n18"] - 0.1 and t >= T_REVEAL:
        stamp(c, 540, 720, "1–3 HOURS", size=96, k=prog(t, T_REVEAL, T_REVEAL + 0.25), rot=-5)
    hud(c, t)
    intercom(c, t)
    end_cards(c, t)
    nope_text(c, t)
    captions(c, t)
    respawn_flash(c, t)
