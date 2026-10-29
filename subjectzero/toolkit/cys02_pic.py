"""COULD YOU SURVIVE? #02 — Everest: the picture (2D estampe look, sz2d.py). Timed on out/cys02_lines.json.

    python3 sz2render.py cys02_pic                # -> out/cys02_pic_video.mp4
    python3 sz2render.py cys02_pic --sheet 0 2 5 ...

Shots (named, none held longer than 8 s): close (her on the summit snow, the plume streaming off behind her) →
jars (the air in a jar at sea level vs on the summit) → close → climb (the climbers' weeks of rotations vs her zero)
→ close (lab) → wide (the range, her a yellow dot on top, the thermometer) → close (wind, NOPE 1: the cornice
breaks off) → timer (the snow hourglass: bare skin freezes in about 5 min) → close (NOPE 2: an avalanche on the next
face) → duck → close (the tease: something under the snow) → gauge (clear thinking left: 1-3 min) → close (dizzy) →
strata (the summit sliced open: limestone, fossils, the old sea comes back) → close (NOPE 3 blows the snow cap off:
fossils under her boots) → end (the three next spawns, respawn flash).
HUD: altitude, then O2 per breath, temperature, wind; the progress bar is a real-time clock "TIME UP HERE" with the
1 MIN and 3 MIN marks: the viewer watches it fill toward the answer.
"""
import json
import math
import os

import numpy as np
import skia

from sz2d import (W, H, FPS, rgb, mixc, fill, ink, text, smooth_path, rrect, oval, ease_io, prog, font, mist_band,
                  Sea, draw_hero, draw_duck, paper_over, vignette, seal, mottle, words_caption, hud_card,
                  alpine_sky, peak, snow_plume, snowfall, trilobite, crinoid, shell_fossil, thermometer,
                  PAPER, PAPER_HI, INKC, PRUSSIAN, CORAL, SEAL, FOAM, YEL, YEL_D, YEL_L, WHITE, SAFE_X0, SAFE_X1, CAP_CX,
                  SNOW, SNOW_SH, SNOW_D, ROCK, ROCK_D, LIME, LIME_D, LIME_L)
import cys02 as EP

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
EPNAME = "cys02_pic"
DURATION = EP.DURATION

_js = json.load(open(os.path.join(OUT, "cys02_lines.json"), encoding="utf-8"))
L = {l["key"]: l["t"] for l in _js["lines"]}
DUR = {l["key"]: l["dur"] for l in _js["lines"]}
WHO = {l["key"]: l["who"] for l in _js["lines"]}
TXT = {l["key"]: l["text"] for l in _js["lines"]}
E = {k: L[k] + DUR[k] for k in L}
KEYS = sorted(L, key=lambda k: L[k])
ENV = {w: np.load(os.path.join(OUT, f"cys02_env_{w}.npy")) for w in ("N", "HERO", "LAB")}

# what the captions show (numbers as figures; the voice says them in words)
CAP = {"n2": "8,849 meters up.", "n7": "In January, it averages −36°C.", "n9": "The wind can blow over 100 mph.",
       "n17": "About 1–3 minutes of clear thinking.", "n11": "In that wind, bare skin can freeze in under 5 minutes.",
       "n20": "Last time, you escaped the ocean. This rock was seafloor.", "n20b": "It still holds sea fossils, over 400 million years old.", "n24": "Respawning in 3... 2..."}
# how long a caption word takes to SAY (characters of the spoken words), so a figure lights up when it is said
SAYLEN = {"8,849": 40, "−36°C.": 16, "100": 9, "mph.": 13, "5": 4, "1–3": 12, "400": 12, "3...": 6, "2...": 4}
NOPES = {"n10": 1, "n12": 2, "n21": 3}
XH, YH = 450, 870                     # her head in the close shot


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
    (E["n2"] + 0.05, "jars"),             # the air in a jar: sea level vs summit
    (L["n4"] - 0.1, "close"),             # "Okay. Just breathe."
    (L["n5"] - 0.05, "climb"),            # the climbers' weeks of rotations vs her zero
    (L["n6"] - 0.35, "close"),            # the lab: "Saves time."
    (L["n7"] - 0.1, "wide"),              # the range, the thermometer
    (L["n8"] - 0.1, "close"),             # the cold is not what gets you first
    (WT("n9", "wind") - 0.1, "gale"),     # the wind: tight on her, snow streaking across
    (L["n10"] - 0.15, "close"),           # NOPE 1
    (L["n11"] - 0.05, "timer"),           # the snow hourglass
    (L["n12"] - 0.15, "close"),           # NOPE 2
    (WT("n13", "It's") - 0.05, "duck"),
    (L["n15"] - 0.05, "close"),           # the tease: something under the snow
    (L["n16"] - 0.05, "gauge"),           # clear thinking left: 1-3 min
    (L["n19"] - 0.05, "close"),           # dizzy
    (L["n20"] - 0.05, "strata"),          # the summit sliced open
    (L["n21"] - 0.15, "close"),           # NOPE 3
    (L["n22"] - 0.05, "end"),             # the next spawns
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


# ---------------------------------------------------------------- NOPE machinery (as #01)
def nope_words():
    e = ENV["HERO"]
    a, b = int(L["n21"] * FPS) - 1, int(E["n21"] * FPS) + 1
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
    return [wt for _, wt in word_times("n21")]


W3 = nope_words()
T_BLAST3 = W3[-1]
T_N1 = E["n10"] - 0.05                # damage lands just after each word
T_N2 = L["n12"] + 0.25


def nope_at(t):
    for key, lvl in NOPES.items():
        a = L[key]
        end = (E[key] + 0.5, E[key] + 0.8, T_BLAST3 + 1.05)[lvl - 1]
        if a - 0.05 <= t <= end:
            if lvl == 3:
                return 3, max(0.0, (t - T_BLAST3) / (end - T_BLAST3))
            return lvl, (t - a) / (end - a)
    return 0, 0.0


def nope_word(t):
    if not (L["n21"] - 0.05 <= t <= T_BLAST3 + 1.05):
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
    st = dict(face="worried", arms="none", shiver=0.0, look=None, squash=0.0, blink=0.0, mouth_open=None, tilt=0.0)
    for b in (2.4, 6.0, 12.0, 18.6, 24.1, 33.2, 37.8, 47.1, 53.0, 59.4, 63.6):
        if b <= t <= b + 0.12:
            st["blink"] = 1.0
    if t < 0.6:                                    # spawn: a squash bounce as she lands
        st["face"] = "shock"
        k = t / 0.6
        st["squash"] = 0.45 * math.sin(k * math.pi * 2) * (1 - k)
    elif t < E["n2"]:
        st["face"] = "shock" if t > WT("n2", "8,849") + 0.4 else "worried"
        st["look"] = (8 * math.sin(t * 2.2), 4)
    elif L["n4"] - 0.2 <= t < L["n5"]:             # "Okay. Just breathe.": hands on her chest
        st["face"] = "worried"
        st["arms"] = "hug"
        st["mouth_open"] = 0.4 + 1.0 * env("HERO", t)
    elif L["n6"] - 0.2 <= t < L["n7"]:
        st["face"] = "deadpan"
        st["look"] = (10, -4)
    elif L["n8"] - 0.2 <= t < L["n10"]:
        st["face"] = "cold"
        st["shiver"] = min(1.0, 0.4 + (t - L["n8"]) / 2.0)
        if t > WT("n9", "wind"):
            st["face"] = "shock"
            st["tilt"] = -4 * min(1.0, (t - WT("n9", "wind")) / 0.5)
    elif E["n10"] + 0.4 <= t < L["n12"]:
        st["face"] = "cold"
        st["shiver"] = 1.0
    elif L["n15"] - 0.1 <= t < L["n16"]:          # "the real clock is in your head": she taps it, then looks down
        st["face"] = "worried"
        st["arms"] = "point"
        if t > WT("n15", "wait"):
            st["face"] = "shock"
            st["arms"] = "none"
            st["look"] = (0, 10)
    elif L["n19"] - 0.1 <= t < L["n20"]:           # dizzy: too confused to climb down
        st["face"] = "worried"
        st["tilt"] = 7 * math.sin(t * 3.2)
        st["look"] = (10 * math.sin(t * 6), 6 * math.cos(t * 6))
    elif L["n22"] - 0.1 <= t:
        st["face"] = "deadpan"
        st["shiver"] = 0.4
        if L["n23"] - 0.1 <= t < L["n24"]:          # "Anywhere with air."
            st["face"] = "happy"
            st["arms"] = "hug"
            st["look"] = (0, -8)
            st["mouth_open"] = 0.5 + 1.1 * env("HERO", t)
        elif t >= L["n24"]:
            st["face"] = "worried"
    if E["n21"] + 0.4 <= t < L["n22"]:
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
        st["tilt"] = (0.0, -6.0, 0.0)[lvl - 1]
    return st


# ---------------------------------------------------------------- pieces of the close shot
RIDGE = [(-60, 1500), (130, 1270), (300, 1100), (450, 1044), (600, 1090), (740, 1190), (880, 1320), (1000, 1430),
         (1140, 1560)]


def ridge_y(x):
    return float(np.interp(x, [p[0] for p in RIDGE], [p[1] for p in RIDGE]))


def cornice(c, k, boil, t):
    """The snow lip overhanging the right ridge. NOPE 1 snaps it: it tips and drops out of frame (k 0..1)."""
    x0, x1 = 640, 900
    p = skia.Path()
    p.moveTo(x0 - 20, ridge_y(x0 - 20) + 4)
    p.cubicTo(x0 + 40, ridge_y(x0) - 40, x1 - 10, ridge_y(x1) - 70, x1 + 60, ridge_y(x1) - 50)
    p.cubicTo(x1 + 70, ridge_y(x1) - 20, x1 + 30, ridge_y(x1) + 10, x1 - 10, ridge_y(x1) + 14)
    p.cubicTo(x1 - 60, ridge_y(x1) + 40, x0 + 40, ridge_y(x0) + 50, x0 - 20, ridge_y(x0 - 20) + 4)
    p.close()
    under = skia.Path()
    under.moveTo(x1 + 60, ridge_y(x1) - 50)
    under.cubicTo(x1 + 70, ridge_y(x1) - 20, x1 + 30, ridge_y(x1) + 10, x1 - 10, ridge_y(x1) + 14)
    under.cubicTo(x1 - 60, ridge_y(x1) + 40, x0 + 40, ridge_y(x0) + 50, x0 - 20, ridge_y(x0 - 20) + 4)
    under.lineTo(x0 + 60, ridge_y(x0) + 8)
    under.cubicTo(x0 + 120, ridge_y(x0) + 10, x1 - 30, ridge_y(x1) - 10, x1 + 60, ridge_y(x1) - 50)
    under.close()
    if k <= 0:
        c.drawPath(p, fill(SNOW))
        c.drawPath(under, fill(SNOW_SH))
        for j in range(4):             # icicles under the lip
            ix = x0 + 60 + j * (x1 - x0 - 40) / 4
            iy = ridge_y(ix) + 28
            ic = skia.Path()
            ic.moveTo(ix - 7, iy)
            ic.lineTo(ix, iy + 34 - 6 * j)
            ic.lineTo(ix + 7, iy)
            ic.close()
            c.drawPath(ic, fill(WHITE))
            c.drawPath(ic, ink(2.5))
        c.drawPath(p, ink(4, boil=boil))
        return
    if k >= 1:
        return
    c.save()
    c.translate(260 * k, 700 * k * k)
    c.rotate(28 * k)
    c.drawPath(p, fill(SNOW))
    c.drawPath(under, fill(SNOW_SH))
    c.drawPath(p, ink(4, boil=boil))
    c.restore()
    # the crack line where it broke, and a puff
    if k < 0.6:
        c.drawPath(oval(x0 + 40, ridge_y(x0) + 10, 90 * (0.5 + k), 30 * (0.5 + k)), fill(SNOW, 0.8 * (1 - k / 0.6)))


def avalanche(c, k, boil, t):
    """NOPE 2: a slab lets go on the next face (the left peak) and pours down in a woodblock cloud."""
    if k <= 0:
        return
    pts = [(150, 905), (210, 960), (270, 1030), (320, 1120), (360, 1230), (380, 1360)]
    n = len(pts)
    head = min(n - 1.0, k * (n - 1) * 1.15)
    for i in range(int(head) + 1):
        x, y = pts[i]
        a = min(1.0, (head - i) + 0.3)
        fade = 1 - max(0.0, (k - 0.75) / 0.25)
        r = 56 + 20 * i
        for j in range(3):
            c.drawPath(oval(x + (j - 1) * r * 0.6, y - j * 6, r, r * 0.62), fill(SNOW, 0.95 * a * fade))
            c.drawPath(oval(x + (j - 1) * r * 0.6, y - j * 6, r, r * 0.62), ink(2.5, alpha=0.6 * a * fade))


def blown_snow(c, k):
    """NOPE 3: the snow cap leaves the summit in a burst of chunks to the right."""
    if not 0 < k < 1:
        return
    rng = np.random.default_rng(31)
    for _ in range(46):
        x0 = rng.uniform(-40, 1100)
        y0 = ridge_y(x0) + rng.uniform(0, 160)
        vx, vy = rng.uniform(300, 1300), rng.uniform(-900, -200)
        x, y = x0 + vx * k, y0 + vy * k + 900 * k * k
        r = rng.uniform(16, 46) * (1 - 0.5 * k)
        c.drawPath(oval(x, y, r, r * 0.7), fill(SNOW, 1 - k))
        c.drawPath(oval(x, y, r, r * 0.7), ink(2.5, alpha=0.7 * (1 - k)))


def summit_front(c, t, boil, bare):
    """The summit crest in front of her: snow (or, after NOPE 3, the bare grey limestone full of fossils)."""
    pts = RIDGE
    path = smooth_path(pts, closed=False)
    path.lineTo(1140, H + 60)
    path.lineTo(-60, H + 60)
    path.close()
    if bare < 1:
        c.drawPath(path, fill(SNOW))
        mottle(c, path, SNOW_SH, alpha=0.06, scale=0.008, seed=9)
        c.save()
        c.clipPath(path, doAntiAlias=True)
        sh = smooth_path([(450, 1044), (600, 1090), (740, 1190), (880, 1320), (1140, 1560), (1140, H + 60), (620, H + 60),
                          (540, 1440), (500, 1200)], closed=True)
        c.drawPath(sh, fill(SNOW_SH, 0.85))
        for (rx, ry, rw, rh) in ((170, 1560, 80, 64), (840, 1640, 130, 70)):
            rock = skia.Path()
            rock.moveTo(rx - rw, ry + rh * 0.4)
            rock.lineTo(rx - rw * 0.55, ry - rh * 0.5)
            rock.lineTo(rx - rw * 0.15, ry - rh * 0.2)
            rock.lineTo(rx + rw * 0.2, ry - rh)
            rock.lineTo(rx + rw * 0.65, ry - rh * 0.1)
            rock.lineTo(rx + rw, ry + rh * 0.4)
            rock.close()
            c.drawPath(rock, fill(ROCK_D))
            c.drawLine(rx + rw * 0.2, ry - rh, rx + rw * 0.05, ry + rh * 0.4, ink(3, col=ROCK, alpha=0.9))
            c.drawPath(rock, ink(3.5, boil=boil))
            cap = skia.Path()
            cap.moveTo(rx - rw * 0.62, ry - rh * 0.38)
            cap.lineTo(rx - rw * 0.15, ry - rh * 0.1)
            cap.lineTo(rx + rw * 0.2, ry - rh * 0.88)
            cap.lineTo(rx + rw * 0.3, ry - rh * 0.55)
            cap.lineTo(rx - rw * 0.15, ry + rh * 0.05)
            cap.close()
            c.drawPath(cap, fill(SNOW))
        for i in range(6):               # carved wind ripples in the snow
            y = 1330 + i * 105
            p = skia.Path()
            p.moveTo(-40, y + 60)
            p.cubicTo(250, y - 30, 600, y + 40, 1120, y + 90)
            c.drawPath(p, ink(2.5, col=SNOW_D, alpha=0.45))
        c.restore()
    if bare > 0:                         # the rock under the snow
        c.save()
        c.clipPath(path, doAntiAlias=True)
        rp = skia.Paint()
        c.drawRect(skia.Rect.MakeWH(W, H), fill(LIME, bare))
        for i in range(9):
            y = 1150 + i * 92
            band = smooth_path([(-60, y), (300, y - 30), (700, y + 20), (1140, y - 10), (1140, y + 46), (700, y + 66),
                                (300, y + 16), (-60, y + 46)])
            c.drawPath(band, fill(LIME_D if i % 2 else LIME_L, 0.55 * bare))
        mottle(c, path, LIME_D, alpha=0.25 * bare, scale=0.02, seed=12)
        trilobite(c, 250, 1420, s=1.15, rot=-14, alpha=bare)
        shell_fossil(c, 640, 1380, s=1.1, rot=12, alpha=bare)
        crinoid(c, 880, 1350, s=1.0, rot=8, alpha=bare)
        shell_fossil(c, 470, 1600, s=0.8, rot=-30, alpha=bare)
        trilobite(c, 760, 1640, s=0.8, rot=30, alpha=bare)
        c.restore()
        del rp
    c.drawPath(smooth_path(pts, closed=False), ink(5, boil=boil))


def breath_puffs(c, t, x, y):
    """Little clouds of breath in the cold (she breathes fast: thin air)."""
    for j in range(3):
        ph = ((t * 1.6) + j / 3) % 1.0
        c.drawPath(oval(x + 30 + 60 * ph, y - 30 * ph, 16 + 30 * ph, 10 + 18 * ph), fill(WHITE, 0.55 * (1 - ph)))


def dizzy(c, t, x, y):
    for j in range(4):
        a = t * 4 + j * math.pi / 2
        sx, sy = x + math.cos(a) * 150, y - 150 + math.sin(a) * 34
        star = skia.Path()
        for i in range(10):
            rr = 18 if i % 2 == 0 else 7
            an = i * math.pi / 5 - math.pi / 2
            (star.moveTo if i == 0 else star.lineTo)(sx + rr * math.cos(an), sy + rr * math.sin(an))
        star.close()
        c.drawPath(star, fill(YEL_L))
        c.drawPath(star, ink(3))


def ring(c, x, y, r, alpha, width=8):
    p = skia.Path()
    p.addArc(skia.Rect.MakeLTRB(x - r, y - r * 0.18, x + r, y + r * 0.18), 8, 164)   # only in front of her
    c.drawPath(p, ink(width, col=WHITE, alpha=alpha))


def frost(c, k):
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


def wind_k(t):
    """How hard the wind blows in the close shot (the plume is there from frame 0, it roars on n9)."""
    k = 0.45
    if t >= WT("n9", "wind") - 0.2:
        k = 0.45 + 0.55 * ease_io(prog(t, WT("n9", "wind") - 0.2, WT("n9", "wind") + 0.6))
    if t >= L["n13"]:
        k = 0.6
    if t >= L["n22"]:
        k = 0.4
    return k


def range_far(c, t, boil, y0=1000):
    """The Himalaya below her, far away and pale, in mist bands."""
    far = mixc(rgb("#8FA7BD"), PAPER, 0.35)
    peak(c, [(-60, y0 + 70), (60, y0 + 20), (170, y0 + 60), (300, y0 - 10), (420, y0 + 50), (560, y0 + 15), (700, y0 + 60),
             (840, y0 - 5), (980, y0 + 40), (1140, y0 + 10)], col=far, snow_y=y0 + 40, seed=3, hatch=False, line=2.5,
         alpha=0.95)
    tw = twos(t)
    mist_band(c, -100 + 6 * tw, y0 + 60, 520, 34, alpha=0.85)
    mist_band(c, 560 - 5 * tw, y0 + 110, 600, 30, alpha=0.8)


def close_shot(c, t, s=1.0, cam=(1.0, 0.0)):
    tw = twos(t)
    fi = int(t * FPS)
    boil = (fi // 2, 1.0)
    lvl, nk = nope_at(t)
    bare = ease_io(prog(t, T_BLAST3, T_BLAST3 + 0.45))
    alpine_sky(c, tw, horizon=1060, stars=0.35, sun=(820, 330), sun_r=58)
    for (x0, y, w_, h_, sp) in ((-60, 300, 460, 40, 12), (620, 520, 520, 34, -9)):
        mist_band(c, x0 + sp * tw, y, w_, h_, alpha=0.8)
    range_far(c, t, boil)
    # the next face on the left (lower than her: she is on the highest point on Earth)
    peak(c, [(-80, 1300), (40, 1010), (150, 905), (240, 980), (330, 1120), (420, 1300)], col=ROCK, snow_y=980, seed=5,
         boil=boil, line=4)
    avalanche(c, prog(t, T_N2, T_N2 + 1.1), boil, t)
    # the plume off the summit, behind her (it streams right, with the jet stream)
    snow_plume(c, XH + 80, 950, tw, strength=wind_k(t), length=620)
    st = hero_state(t)
    if L["n4"] - 0.2 <= t < L["n16"] and not lvl:
        breath_puffs(c, tw, XH + 40 * s, YH + 60 * s)
    draw_hero(c, XH, YH, s=s, face=st["face"], boil=boil, arms=st["arms"], t=tw, blink=st["blink"],
              squash=st["squash"], look=st["look"], shiver=st["shiver"], mouth_open=st["mouth_open"], tilt=st["tilt"])
    if L["n19"] - 0.1 <= t < L["n20"]:
        dizzy(c, t, XH, YH)
    # the duck on the crest, never in danger
    dx, dy, drot = 640, 0.0, -4.0
    if t >= T_BLAST3:                       # NOPE 3 launches it, two flips, it lands upright on the bare rock
        fly = min(1.0, (t - T_BLAST3) / 1.2)
        dx = 640 + (250 - 640) * ease_io(fly)
        dy = -620 * math.sin(fly * math.pi)
        drot = -4 + 720 * ease_io(fly)
    yd = ridge_y(dx) + 4
    summit_front(c, t, boil, bare)
    cornice(c, prog(t, T_N1, T_N1 + 0.9), boil, t)
    if L["n15"] + 0.3 <= t < T_BLAST3:      # the tease: a curl of fossil shell peeking out of the snow
        kk = ease_io(prog(t, WT("n15", "rock") - 0.3, WT("n15", "rock") + 0.2))
        if kk > 0:
            c.save()
            c.clipPath(skia.Path.Rect(skia.Rect.MakeXYWH(0, 1050, W, 400)))
            trilobite(c, 400, 1126 + 40 * (1 - kk), s=0.55, rot=24, alpha=kk)
            c.restore()
            c.drawPath(oval(400, 1136, 70, 16), fill(SNOW, 0.9))
    draw_duck(c, dx, yd + dy, s=0.8 * s, boil=boil, tilt=drot, look=0.0)
    blown_snow(c, prog(t, T_BLAST3, T_BLAST3 + 1.0))
    # NOPE rings: only in front of her
    yw = ridge_y(XH) + 6
    if lvl == 3 and t < T_BLAST3:
        i = nope_word(t)
        kk = min(1.0, (t - W3[max(0, i)]) / 0.6)
        ring(c, XH, yw, 200 + 260 * (i + 1) * kk, (1 - kk) * 0.9, 7)
    elif lvl:
        for j in range(lvl):
            rr = 200 + (500 + 400 * lvl) * min(1.0, nk * (1.4 - 0.2 * j))
            ring(c, XH, yw, rr, (1 - nk) * 0.9, 6 + 3 * lvl)
    snowfall(c, tw, density=34, alpha=0.75, wind=wind_k(t) * 0.8)


# ---------------------------------------------------------------- jars: the air at sea level vs on the summit
def glass_jar(c, x, y, w, h, dots, n_on, t, label, boil, seed):
    body = rrect(x - w / 2, y, w, h, 34)
    c.drawPath(rrect(x - w / 2 + 10, y + 12, w, h, 34), fill(INKC, 0.3))
    c.drawPath(body, fill(rgb("#DDE7EE"), 0.92))
    rng = np.random.default_rng(seed)
    pos = [(rng.uniform(x - w / 2 + 30, x + w / 2 - 30), rng.uniform(y + 70, y + h - 30)) for _ in range(dots)]
    for i, (px, py) in enumerate(pos):
        if i >= n_on:
            break
        px += 6 * math.sin(t * 3 + i)
        py += 6 * math.cos(t * 2.4 + i * 1.3)
        c.drawCircle(px, py, 15, fill(CORAL))
        c.drawCircle(px, py, 15, ink(3))
    c.drawPath(rrect(x - w / 2 - 12, y - 30, w + 24, 46, 12), fill(rgb("#C9973E")))
    c.drawPath(rrect(x - w / 2 - 12, y - 30, w + 24, 46, 12), ink(4, boil=boil))
    c.drawPath(body, ink(5, boil=boil))
    c.drawLine(x - w / 2 + 26, y + 60, x - w / 2 + 26, y + h - 60, ink(10, col=WHITE, alpha=0.6))
    text(c, label, x, y + h + 62, font("mono", 36), FOAM, align="center", stroke=8)


def jars_shot(c, t):
    a, b = shot_start("jars"), shot_end(shot_start("jars"))
    fi = int(t * FPS)
    boil = (fi // 2, 0.9)
    tw = twos(t)
    alpine_sky(c, tw, horizon=1500, stars=0.6)
    peak(c, [(-60, 1500), (130, 1330), (300, 1420), (470, 1240), (640, 1400), (820, 1300), (1140, 1460)],
         col=rgb("#2E4A6A"), snow_y=1330, seed=8, hatch=False, line=3)
    k_in = ease_io(prog(t, a, a + 0.35))
    dy = (1 - k_in) * 200
    t3 = WT("n3", "third")
    drain = ease_io(prog(t, t3 - 0.6, t3 + 0.3))
    n_sum = int(round(42 - (42 - 14) * drain))
    c.save()
    c.translate(0, dy)
    glass_jar(c, 270, 560, 270, 470, 42, 42, tw, "SEA LEVEL", boil, 3)
    glass_jar(c, 630, 560, 270, 470, 42, n_sum, tw, "SUMMIT", boil, 3)
    c.drawCircle(178, 459, 15, fill(CORAL))
    c.drawCircle(178, 459, 15, ink(3))
    text(c, "= OXYGEN IN ONE BREATH", 470, 470, font("mono", 32), FOAM, align="center", stroke=8)
    c.restore()
    if t >= t3 - 0.05:
        stamp(c, 630, 900, "1/3", size=120, k=prog(t, t3 - 0.05, t3 + 0.2), rot=-7)


# ---------------------------------------------------------------- climb: the climbers' weeks vs her zero
def climb_shot(c, t):
    a = shot_start("climb")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    c.drawRect(skia.Rect.MakeWH(W, H), fill(PRUSSIAN))
    k_in = ease_io(prog(t, a, a + 0.3))
    x0, y0, w, h = SAFE_X0, 330 + (1 - k_in) * 120, 660, 820
    card = rrect(x0, y0, w, h, 18)
    c.drawPath(rrect(x0 + 10, y0 + 12, w, h, 18), fill(INKC, 0.35))
    c.drawPath(card, fill(PAPER_HI))
    mottle(c, card, PAPER, alpha=0.15, scale=0.02, seed=6)
    c.drawPath(card, ink(4))
    gx, gy, gw, gh = x0 + 150, y0 + 130, w - 190, h - 290
    # the death zone band at the top
    dz = rrect(gx, gy, gw, 92, 8)
    c.drawPath(dz, fill(SEAL, 0.18))
    text(c, "DEATH ZONE 8,000 m+", gx + gw / 2, gy + 58, font("mono", 32), SEAL, align="center")
    c.drawLine(gx, gy, gx, gy + gh, ink(4))
    c.drawLine(gx, gy + gh, gx + gw, gy + gh, ink(4))
    text(c, "SUMMIT", gx - 16, gy + 12, font("mono", 30), INKC, align="right")
    text(c, "BASE", gx - 16, gy + gh - 8, font("mono", 30), INKC, align="right")
    text(c, "CAMP", gx - 16, gy + gh + 26, font("mono", 30), INKC, align="right")
    for wk in range(1, 6):
        x = gx + gw * wk / 5.4
        c.drawLine(x, gy + gh, x, gy + gh + 14, ink(3))
        text(c, f"W{wk}", x, gy + gh + 50, font("mono", 30), INKC, align="center")
    text(c, "WEEKS ON THE MOUNTAIN", gx + gw / 2 - 40, gy + gh + 100, font("mono", 30), mixc(INKC, PAPER, 0.3), align="center")
    # the climbers: up, back down, higher, back down... then the summit (about 4 weeks of rotations, then the push)
    zz = [(0, 0.0), (0.5, 0.0), (1.1, 0.42), (1.5, 0.08), (2.2, 0.62), (2.7, 0.1), (3.4, 0.78), (3.9, 0.08), (4.7, 0.08),
          (5.2, 1.0)]
    kz = ease_io(prog(t, L["n5"] + 0.1, WT("n5", "You") - 0.1))
    pts = [(gx + gw * d / 5.4, gy + gh - (gh - 10) * hgt) for d, hgt in zz]
    tot = sum(math.dist(p, q) for p, q in zip(pts, pts[1:]))
    run, path = 0.0, skia.Path()
    path.moveTo(*pts[0])
    for p, q in zip(pts, pts[1:]):
        seg = math.dist(p, q)
        if run + seg <= kz * tot:
            path.lineTo(*q)
        else:
            f = (kz * tot - run) / seg
            path.lineTo(p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f)
            break
        run += seg
    c.drawPath(path, ink(9, col=CORAL))
    if kz > 0.2:
        text(c, "CLIMBERS", gx + gw * 0.62, gy + gh - 230, font("mono", 32), CORAL, align="center")
    # her: straight up at week zero
    tz = WT("n5", "zero")
    ky = ease_io(prog(t, tz - 0.35, tz + 0.05))
    if ky > 0:
        c.drawLine(gx + 6, gy + gh, gx + 6, gy + gh - (gh - 10) * ky, ink(14, col=YEL))
        c.drawLine(gx + 6, gy + gh, gx + 6, gy + gh - (gh - 10) * ky, ink(3))
        if ky >= 1:
            c.drawCircle(gx + 6, gy + 10, 20, fill(YEL))
            c.drawCircle(gx + 6, gy + 10, 20, ink(4))
            text(c, "0", gx + 6, gy + 21, font("display", 28), INKC, align="center")
    if t >= tz:
        stamp(c, x0 + w / 2 + 40, y0 + h / 2 + 30, "YOU: 0 DAYS", size=78, k=prog(t, tz, tz + 0.2), rot=-6)


# ---------------------------------------------------------------- wide: the range, her a yellow dot on top
def wide_shot(c, t):
    a = shot_start("wide")
    fi = int(t * FPS)
    boil = (fi // 2, 0.9)
    tw = twos(t)
    z = 1.08 - 0.08 * ease_io(prog(t, a, shot_end(a)))
    c.save()
    c.translate(450, 700)
    c.scale(z, z)
    c.translate(-450, -700)
    alpine_sky(c, tw, horizon=1400, stars=0.4, sun=(160, 420), sun_r=56)
    mist_band(c, 480 + 8 * tw, 330, 520, 36, alpha=0.8)
    far = mixc(rgb("#8FA7BD"), PAPER, 0.3)
    peak(c, [(-60, 1150), (90, 980), (210, 1080), (330, 1000), (450, 1120), (620, 960), (780, 1060), (1140, 980)],
         col=far, snow_y=1010, seed=2, hatch=False, line=2.5)
    snow_plume(c, 450, 570, tw, strength=0.7, length=480)
    peak(c, [(-60, 1500), (120, 1200), (280, 860), (400, 640), (450, 560), (520, 640), (600, 700), (690, 660), (760, 760),
             (900, 1060), (1140, 1400)], col=ROCK, snow_y=780, seed=6, boil=boil)
    peak(c, [(-60, 1260), (60, 1060), (180, 990), (300, 1040), (420, 1180), (560, 1400)], col=rgb("#56647A"),
         snow_y=1060, seed=9, boil=boil, line=3.5)
    peak(c, [(-60, 1600), (160, 1420), (360, 1560), (600, 1380), (820, 1520), (1140, 1450)], col=rgb("#3F4E63"),
         snow_y=1460, seed=7, hatch=True, line=3.5)
    mist_band(c, -60 - 8 * tw, 1250, 600, 46, alpha=0.9)
    mist_band(c, 540 + 6 * tw, 1330, 640, 40, alpha=0.85)
    # her, tiny, on the very top, and the duck
    draw_hero(c, 450, 534, s=0.11, face="cold", boil=None, arms="none", t=tw)
    c.restore()
    t36 = WT("n7", "−36")
    kk = ease_io(prog(t, a, t36 + 0.2))
    thermometer(c, 700, 470, 560, 0.62 - 0.54 * kk, label="°C")
    text(c, "0", 650, 470 + 30 + 3 * (560 - 60) / 8 + 10, font("mono", 30), INKC, align="right")
    if t >= t36 - 0.05:
        stamp(c, 390, 920, "−36 °C", size=104, k=prog(t, t36 - 0.05, t36 + 0.2), rot=-6, font_name="mono")
        text(c, "JANUARY AVERAGE", 390, 1020, font("mono", 34), FOAM, align="center", stroke=8)


# ---------------------------------------------------------------- timer: the snow hourglass
def asanoha_bg(c, t, base, line, r=70, alpha=0.18):
    """Asanoha (hemp-leaf) pattern, the woodblock frost: six-pointed stars on a triangular grid."""
    c.drawRect(skia.Rect.MakeWH(W, H), fill(base))
    drift = (twos(t) * 10) % (r * 2)
    hgt = r * math.sqrt(3)
    j = 0
    y = -hgt
    while y < H + hgt:
        x = -2 * r + (r if j % 2 else 0) - drift
        while x < W + 2 * r:
            for k in range(6):
                an = k * math.pi / 3
                c.drawLine(x, y, x + math.cos(an) * r, y + math.sin(an) * r, ink(2.5, col=line, alpha=alpha))
            x += 2 * r
        y += hgt
        j += 1


def timer_shot(c, t):
    a = shot_start("timer")
    b = shot_end(a)
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    asanoha_bg(c, t, rgb("#2A4A6E"), WHITE)
    k = prog(t, a, b)
    cx, cy = 450, 860
    # frame of the hourglass
    c.drawPath(rrect(cx - 210, cy - 380, 420, 40, 14), fill(rgb("#8E6524")))
    c.drawPath(rrect(cx - 210, cy + 340, 420, 40, 14), fill(rgb("#8E6524")))
    glass = skia.Path()
    glass.moveTo(cx - 170, cy - 340)
    glass.cubicTo(cx - 170, cy - 110, cx - 30, cy - 60, cx - 14, cy)
    glass.cubicTo(cx - 30, cy + 60, cx - 170, cy + 110, cx - 170, cy + 340)
    glass.lineTo(cx + 170, cy + 340)
    glass.cubicTo(cx + 170, cy + 110, cx + 30, cy + 60, cx + 14, cy)
    glass.cubicTo(cx + 30, cy - 60, cx + 170, cy - 110, cx + 170, cy - 340)
    glass.close()
    c.drawPath(glass, fill(rgb("#5F86A8"), 0.95))
    c.save()
    c.clipPath(glass, doAntiAlias=True)
    top = cy - 300 + 260 * k          # the snow surface in the top bulb drops
    c.drawRect(skia.Rect.MakeLTRB(cx - 200, top, cx + 200, cy), fill(SNOW))
    c.drawLine(cx - 200, top, cx + 200, top, ink(3, col=SNOW_D))
    pile = cy + 330 - 230 * k
    mound = skia.Path()
    mound.moveTo(cx - 200, cy + 345)
    mound.lineTo(cx - 200, pile + 60)
    mound.quadTo(cx, pile - 50, cx + 200, pile + 60)
    mound.lineTo(cx + 200, cy + 345)
    mound.close()
    c.drawPath(mound, fill(SNOW))
    c.drawPath(mound, ink(3, col=SNOW_D))
    for j in range(10):               # the falling stream
        yy = cy + ((t * 420 + j * 40) % 300)
        c.drawCircle(cx + 3 * math.sin(j + t * 9), yy, 5, fill(SNOW))
    c.restore()
    c.drawPath(glass, ink(5, boil=boil))
    c.drawLine(cx - 120, cy - 300, cx - 120, cy - 150, ink(10, col=WHITE, alpha=0.6))
    for sx in (-200, 200):
        c.drawPath(rrect(cx + sx - 14, cy - 345, 28, 690, 10), fill(rgb("#A77A2C")))
        c.drawPath(rrect(cx + sx - 14, cy - 345, 28, 690, 10), ink(4, boil=boil))
    c.drawPath(rrect(cx - 210, cy - 380, 420, 40, 14), ink(4, boil=boil))
    c.drawPath(rrect(cx - 210, cy + 340, 420, 40, 14), ink(4, boil=boil))
    text(c, "BARE SKIN FREEZES IN", cx, 400, font("mono", 40), FOAM, align="center", stroke=8)
    t5 = WT("n11", "5")
    if t >= t5 - 0.05:
        stamp(c, cx, cy + 40, "< 5 MIN", size=104, k=prog(t, t5 - 0.05, t5 + 0.2), rot=-6)
    frost(c, 0.5)


# ---------------------------------------------------------------- the duck, up close
def duck_shot(c, t):
    a = shot_start("duck")
    fi = int(t * FPS)
    boil = (fi // 2, 1.0)
    tw = twos(t)
    alpine_sky(c, tw, horizon=1160, stars=0.3, sun=(250, 420), sun_r=70)
    range_far(c, t, boil, y0=1120)
    snow_plume(c, 300, 1200, tw, strength=0.6, length=700)
    ground = smooth_path([(-60, 1380), (300, 1300), (700, 1320), (1140, 1400)], closed=False)
    ground.lineTo(1140, H + 50)
    ground.lineTo(-60, H + 50)
    ground.close()
    c.drawPath(ground, fill(SNOW))
    mottle(c, ground, SNOW_SH, alpha=0.06, scale=0.01, seed=4)
    c.drawPath(smooth_path([(-60, 1380), (300, 1300), (700, 1320), (1140, 1400)], closed=False), ink(5, boil=boil))
    # an oxygen bottle and its mask, unused, beside it
    bx, by = 690, 1250
    c.drawPath(rrect(bx - 40, by - 190, 80, 210, 30), fill(CORAL))
    c.drawPath(rrect(bx - 40, by - 190, 80, 210, 30), ink(5, boil=boil))
    c.drawPath(rrect(bx - 20, by - 226, 40, 40, 8), fill(rgb("#C9973E")))
    c.drawPath(rrect(bx - 20, by - 226, 40, 40, 8), ink(4))
    text(c, "O₂", bx, by - 70, font("mono", 46), FOAM, align="center")
    hose = skia.Path()
    hose.moveTo(bx, by - 210)
    hose.cubicTo(bx - 120, by - 300, bx - 240, by - 60, bx - 160, by + 40)
    c.drawPath(hose, ink(10, col=INKC))
    c.drawPath(oval(bx - 160, by + 54, 46, 30), fill(rgb("#7D8FA6")))
    c.drawPath(oval(bx - 160, by + 54, 46, 30), ink(4))
    z = 1 + 0.04 * prog(t, a, shot_end(a))
    draw_duck(c, 330, 1310 - 4 * abs(math.sin(tw * 1.5)), s=3.0 * z, boil=None, tilt=3 * math.sin(tw * 1.2), look=0.6)
    ta = WT("n13", "air")
    if t >= ta - 0.05:
        stamp(c, 450, 470, "NEEDS NO AIR", size=66, k=prog(t, ta - 0.05, ta + 0.2), rot=-6, pop=0.25)
    snowfall(c, tw, density=30, alpha=0.8, wind=0.5)


# ---------------------------------------------------------------- gauge: clear thinking left
G_C = (450, 900, 230)
G_MAX = 300.0              # the dial runs 0..5 minutes


def g_ang(sec):
    return 135 + 270 * max(0.0, min(1.0, sec / G_MAX))


def gauge_shot(c, t):
    a = shot_start("gauge")
    fi = int(t * FPS)
    boil = (fi // 2, 0.8)
    tw = twos(t)
    alpine_sky(c, tw, horizon=1500, stars=0.7)
    peak(c, [(-60, 1560), (200, 1380), (450, 1300), (700, 1400), (1140, 1520)], col=rgb("#2E4A6A"), snow_y=1380,
         seed=4, hatch=False, line=3)
    snowfall(c, tw, density=40, alpha=0.6, wind=0.6)
    cx, cy, R = G_C
    t_rev = WT("n17", "about")
    k_in = ease_io(prog(t, a, a + 0.3))
    z = 1.25 - 0.25 * k_in + 0.12 * ease_io(prog(t, L["n16"], t_rev))
    pop = max(0.0, 1 - (t - t_rev) / 0.25) if t >= t_rev else 0.0
    z *= 1 + 0.06 * pop
    c.save()
    c.translate(cx, cy)
    c.scale(z, z)
    c.translate(-cx, -cy)
    c.drawCircle(cx + 16, cy + 22, R + 44, fill(INKC, 0.45))
    rim = oval(cx, cy, R + 44, R + 44)
    c.drawPath(rim, fill(rgb("#7D8FA6")))
    mottle(c, rim, ROCK_D, alpha=0.3, scale=0.03, seed=4)
    c.drawPath(rim, ink(6, boil=boil))
    for i in range(12):                 # bolts round the rim, like an old altimeter
        an = i * math.pi / 6
        c.drawCircle(cx + math.cos(an) * (R + 22), cy + math.sin(an) * (R + 22), 7, fill(INKC))
    face = oval(cx, cy, R, R)
    c.drawPath(face, fill(PAPER_HI))
    mottle(c, face, PAPER, alpha=0.18, scale=0.02, seed=6)
    c.drawPath(face, ink(4))
    rr = R * 0.8
    rect = skia.Rect.MakeLTRB(cx - rr, cy - rr, cx + rr, cy + rr)
    base = skia.Path()
    base.addArc(rect, 135, 270)
    c.drawPath(base, ink(30, col=rgb("#DCCFB0")))
    if t >= t_rev:
        kk = ease_io(prog(t, t_rev, t_rev + 0.35))
        band = skia.Path()
        a0 = g_ang(60)
        band.addArc(rect, a0, (g_ang(180) - a0) * kk)
        c.drawPath(band, ink(40, col=SEAL))
    for i in range(21):
        an = math.radians(135 + 270 * i / 20)
        c.drawLine(cx + math.cos(an) * R * 0.93, cy + math.sin(an) * R * 0.93, cx + math.cos(an) * R * 0.98,
                   cy + math.sin(an) * R * 0.98, ink(3))
    for m in range(0, 6):
        an = math.radians(g_ang(m * 60))
        c.drawLine(cx + math.cos(an) * R * 0.68, cy + math.sin(an) * R * 0.68, cx + math.cos(an) * R * 0.92,
                   cy + math.sin(an) * R * 0.92, ink(5))
        lx, ly = cx + math.cos(an) * R * 0.52, cy + math.sin(an) * R * 0.52 + 12
        text(c, f"{m}", lx, ly, font("mono", 40), INKC, align="center")
    text(c, "MIN", cx, cy + 100, font("mono", 32), mixc(INKC, PAPER, 0.3), align="center")
    # the needle: it hunts while the question is asked, then swings into 1-3 minutes
    if t < t_rev:
        hunt = L["n16"] <= t
        ang = g_ang(150) + (60 * math.sin(t * 7) + 30 * math.sin(t * 13) if hunt else 0)
    else:
        e = t - t_rev
        ang = g_ang(120) + 26 * math.exp(-e * 5) * math.cos(e * 18)
    a_ = math.radians(ang)
    nd = skia.Path()
    nd.moveTo(cx + math.cos(a_) * R * 0.74, cy + math.sin(a_) * R * 0.74)
    nd.lineTo(cx + math.cos(a_ + 1.57) * 12, cy + math.sin(a_ + 1.57) * 12)
    nd.lineTo(cx - math.cos(a_) * 40, cy - math.sin(a_) * 40)
    nd.lineTo(cx + math.cos(a_ - 1.57) * 12, cy + math.sin(a_ - 1.57) * 12)
    nd.close()
    c.drawPath(nd, fill(SEAL if t >= t_rev else INKC))
    c.drawPath(nd, ink(3))
    c.drawCircle(cx, cy, 18, fill(INKC))
    c.drawCircle(cx, cy, 7, fill(YEL))
    sh = skia.Path()
    sh.addArc(skia.Rect.MakeLTRB(cx - R * 0.86, cy - R * 0.86, cx + R * 0.86, cy + R * 0.86), 200, 50)
    c.drawPath(sh, ink(14, col=WHITE, alpha=0.5))
    c.restore()
    text(c, "CLEAR THINKING LEFT", cx, 420, font("mono", 40), FOAM, align="center", stroke=8)
    text(c, "IF YOU SPAWN WITHOUT ADAPTING", cx, 466, font("mono", 30), FOAM, align="center", stroke=8)
    if t >= t_rev:
        kk = prog(t, t_rev, t_rev + 0.2)
        sz = 84 * (1.4 - 0.4 * ease_io(kk))
        text(c, "~1–3 MIN", cx, 580, font("mono", sz), YEL_L, align="center", stroke=16)


# ---------------------------------------------------------------- strata: the summit sliced open
APEX = (560, 440)


def strata_shot(c, t):
    a = shot_start("strata")
    fi = int(t * FPS)
    boil = (fi // 2, 0.9)
    tw = twos(t)
    t_sea = WT("n20", "seafloor") - 0.3
    t_fos = L["n20b"]
    # camera: wide on the slice, then a push into the trilobite on "fossils"
    zk = ease_io(prog(t, t_fos + 0.2, t_fos + 1.4))
    z = 1.0 + 1.3 * zk
    fx, fy = 450 + (300 - 450) * zk, 860 + (930 - 860) * zk
    alpine_sky(c, tw, horizon=1700, stars=0.6)
    c.save()
    c.translate(450, 860)
    c.scale(z, z)
    c.translate(-fx, -fy)
    sl = skia.Path()
    sl.moveTo(*APEX)
    sl.lineTo(1080, 1750)
    sl.lineTo(-180, 1750)
    sl.close()
    c.drawPath(sl, fill(LIME))
    c.save()
    c.clipPath(sl, doAntiAlias=True)
    for i in range(16):                 # folded limestone beds
        y = 470 + i * 82
        band = smooth_path([(-200, y + 40), (150, y - 20), (450, y + 30), (800, y - 30), (1100, y + 20), (1100, y + 64),
                            (800, y + 14), (450, y + 74), (150, y + 24), (-200, y + 84)])
        c.drawPath(band, fill(LIME_D if i % 2 else LIME_L, 0.6))
        c.drawPath(smooth_path([(-200, y + 40), (150, y - 20), (450, y + 30), (800, y - 30), (1100, y + 20)], closed=False),
                   ink(2.0, col=LIME_D, alpha=0.6))
    mottle(c, sl, LIME_D, alpha=0.25, scale=0.015, seed=5)
    trilobite(c, 300, 930, s=0.9, rot=-12)
    shell_fossil(c, 560, 760, s=0.8, rot=18)
    crinoid(c, 640, 1090, s=0.9, rot=-6)
    shell_fossil(c, 210, 1240, s=0.7, rot=-20)
    trilobite(c, 520, 1330, s=0.7, rot=26)
    shell_fossil(c, 760, 1330, s=0.7, rot=40)
    crinoid(c, 380, 610, s=0.55, rot=10)
    c.restore()
    kl = ease_io(prog(t, t_sea + 0.5, t_sea + 0.8)) * (1 - ease_io(prog(t, t_fos + 0.2, t_fos + 0.5)))
    if kl > 0:              # name the fossils (they zoom with the camera)
        for (fx_, fy_, lab, dxl) in ((300, 930, "TRILOBITE", -10), (640, 1090, "SEA LILY", 10), (560, 760, "SHELL", 10)):
            lx = fx_ + (90 if dxl > 0 else -90)
            c.drawLine(fx_ + (40 if dxl > 0 else -40), fy_, lx, fy_ - 40, ink(3, alpha=kl))
            text(c, lab, lx, fy_ - 50, font("mono", 32), INKC, align="left" if dxl > 0 else "right", alpha=kl,
                 stroke=6, stroke_col=PAPER_HI)
    # the snow coat on the outside of the slice
    for side in (-1, 1):
        p = skia.Path()
        p.moveTo(*APEX)
        ex = 1080 if side > 0 else -180
        p.lineTo(APEX[0] + (ex - APEX[0]) * 0.32, APEX[1] + (1750 - APEX[1]) * 0.32)
        c.drawPath(p, ink(26, col=SNOW))
    c.drawPath(sl, ink(6, boil=boil))
    # her, tiny on the apex, and the duck
    draw_hero(c, APEX[0], APEX[1] - 38, s=0.13, face="shock", boil=None, arms="none", t=tw)
    draw_duck(c, APEX[0] + 52, APEX[1] - 4, s=0.12)
    # the old sea comes back over everything (ghost waves): 'this rock was seafloor'
    ks = ease_io(prog(t, t_sea - 0.2, t_sea + 0.9))
    if ks > 0:
        sea = Sea(horizon=int(1800 - 1500 * ks), seed=21, layers=[(int(1800 - 1500 * ks) + d, a_, s_) for d, a_, s_ in
                                                                   ((0, 8, 0.3), (40, 12, 0.4), (110, 16, 0.5))])
        lay = skia.Paint()
        lay.setAlphaf(0.5)
        c.saveLayer(None, lay)
        for i in range(3):
            sea.draw_layer(c, i, tw, boil, foam=(i == 0))
        c.restore()
    c.restore()
    # the callback card: last time, the ocean
    kc = ease_io(prog(t, L["n20"], L["n20"] + 0.3)) * (1 - ease_io(prog(t, t_sea - 0.1, t_sea + 0.2)))
    if kc > 0:
        x, y = SAFE_X0, 250
        c.save()
        c.translate(x + 160, y + 120)
        c.rotate(-4)
        c.scale(0.8 + 0.2 * kc, 0.8 + 0.2 * kc)
        c.translate(-(x + 160), -(y + 120))
        c.drawPath(rrect(x, y, 320, 250, 12), fill(PAPER_HI, kc))
        c.drawPath(rrect(x + 16, y + 16, 288, 170, 8), fill(rgb("#3D6E8A"), kc))
        for j in range(3):
            yy = y + 90 + j * 30
            p = skia.Path()
            p.moveTo(x + 16, yy)
            for q in range(6):
                p.quadTo(x + 40 + q * 48, yy - 14, x + 64 + q * 48, yy)
            c.drawPath(p, ink(4, col=FOAM, alpha=kc))
        c.drawPath(rrect(x, y, 320, 250, 12), ink(4, alpha=kc))
        text(c, "#01 POINT NEMO", x + 160, y + 228, font("mono", 32), INKC, align="center", alpha=kc)
        c.restore()
    if ks >= 0.5 and t < t_fos + 0.2:
        stamp(c, 450, 1000, "SEAFLOOR", size=100, k=prog(t, t_sea + 0.2, t_sea + 0.45), rot=-6)
    t400 = WT("n20b", "400")
    if t >= t400 - 0.05:
        stamp(c, 450, 560, "400+ MILLION YEARS", size=50, k=prog(t, t400 - 0.05, t400 + 0.2), rot=-4, font_name="mono", pop=0.15)


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
T_ALT0, T_ALT1 = WT("n2", "8,849"), WT("n2", "meters")


def hud(c, t):
    """Top-left cartouche: one story number at a time. Hidden while a NOPE owns the frame."""
    shot = shot_at(t)[1]
    lvl, nk = nope_at(t)
    lvl = lvl if shot == "close" else 0
    shot = "close" if shot == "gale" else shot
    title_on = t < E["n1"] + 0.15
    rows = []
    if not lvl and shot == "close":
        if t < L["n3"]:
            k = ease_io(prog(t, T_ALT0, T_ALT1))
            val = "???? m" if k < 0.04 else f"{int(8849 * k):,} m"
            rows.append(("ALTITUDE", val, INKC, max(0.0, 1 - (t - T_ALT1) * 3) if t > T_ALT1 else 0.0))
        elif t < L["n5"] - 0.05:
            rows.append(("O₂ PER BREATH", "~33 %", SEAL, 0.0))
        elif t < L["n7"]:
            pass
        elif t < WT("n9", "wind"):
            rows.append(("TEMPERATURE", "−36 °C", PRUSSIAN, 0.0))
        elif t < L["n13"]:
            rows.append(("WIND", "100+ mph", PRUSSIAN, max(0.0, 1 - (t - WT("n9", "100")) * 3)))
    y = 290
    if title_on:
        rows = [("YOU'D LAST", "?? MIN", SEAL, 0.0)]
    if rows:
        if title_on:
            hud_card(c, SAFE_X0 + 30, 470, rows, w=600)
        else:
            hud_card(c, SAFE_X0, y, rows, w=600)
            y += 30 + 78 * len(rows) + 24
    if not lvl and shot == "close" and not rows and L["n5"] - 0.05 <= t < L["n20"]:
        clock_bar(c, t, y)
    if title_on:
        f1, f2 = font("mono", 38), font("display", 124)
        c.save()
        c.translate(CAP_CX, 300)
        c.rotate(-3)
        tag = "COULD YOU SURVIVE"
        wv = f1.measureText(tag)
        c.drawPath(rrect(-wv / 2 - 18, -40, wv + 36, 56, 10), fill(INKC, 0.92))
        text(c, tag, 0, 2, f1, YEL_L, align="center")
        text(c, "EVEREST?", 0, 136, f2, FOAM, align="center", stroke=22)
        c.restore()
    ks = prog(t, 3.0, 3.3)
    if ks > 0 and shot != "end":
        seal(c, 874, 120, 86, alpha=ks)


CB_MAX = 210.0          # the bar runs 0..3:30


def clock_bar(c, t, y):
    """The progress bar: real time since she spawned, with the 1 MIN and 3 MIN marks of the answer."""
    x0, w = SAFE_X0, 600
    card = rrect(x0, y, w, 156, 14)
    c.drawPath(rrect(x0 + 8, y + 10, w, 156, 14), fill(INKC, 0.25))
    c.drawPath(card, fill(PAPER_HI, 0.96))
    mottle(c, card, PAPER, alpha=0.12, scale=0.03, seed=8)
    c.drawPath(card, ink(4))
    c.drawPath(rrect(x0 + 8, y + 8, w - 16, 140, 9), ink(1.6, alpha=0.7))
    text(c, "TIME UP HERE", x0 + 24, y + 46, font("mono", 32), mixc(INKC, PAPER, 0.3))
    v = t + (200.0 - t) * ease_io(prog(t, L["n19"], L["n19"] + 0.7))     # "After that": the clock jumps ahead
    s = int(v)
    text(c, f"{s // 60}:{s % 60:02d}", x0 + w - 24, y + 52, font("mono", 46), INKC, align="right")
    bx, by, bw = x0 + 24, y + 80, w - 48

    def X(sec):
        return bx + bw * min(1.0, sec / CB_MAX)
    if t >= WT("n17", "about"):       # once the answer is in: the 1-3 min band, in red
        c.drawPath(rrect(X(60), by - 2, X(180) - X(60), 18, 7), fill(SEAL, 0.35))
    c.drawPath(rrect(bx, by, bw, 14, 7), fill(rgb("#D9CDB0"), 0.8))
    c.drawPath(rrect(bx, by, max(14, X(v) - bx), 14, 7), fill(PRUSSIAN))
    for sec, lab in (((60, "1 MIN"), (180, "3 MIN")) if t >= WT("n17", "about") else ()):
        x = X(sec)
        c.drawLine(x, by - 6, x, by + 20, ink(3))
        text(c, lab, x, by + 56, font("mono", 30), INKC, align="center")


def intercom(c, t):
    live = [k for k in KEYS if WHO[k] == "LAB" and L[k] - 0.35 <= t <= E[k] + 0.35]
    if not live:
        return
    k = live[0]
    kin = ease_io(min(prog(t, L[k] - 0.35, L[k] - 0.05), 1 - prog(t, E[k] + 0.05, E[k] + 0.35)))
    x = SAFE_X1 - 230 + (1 - kin) * 560
    shot = shot_at(t)[1]
    y = 655 if k == "n24" else (290 if shot == "gauge" else 600)
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
        word = ("nope.", "NOPE.", "NOOOPE!")[max(0, i)]
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
    c.translate(CAP_CX + math.sin(t * 90) * 4 * lvl, 540 if lvl < 3 else 520)
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
    gone = 1 - prog(t, E["n24"] - 0.1, E["n24"] + 0.1)
    if gone <= 0:
        return
    opts = [("A", "POMPEII", "Pompeii"), ("B", "MARIANA TRENCH", "Mariana"), ("C", "THE MOON", "Moon")]
    dim = ease_io(prog(t, a, a + 0.4)) * gone
    c.drawRect(skia.Rect.MakeWH(W, H), fill(INKC, 0.35 * dim))
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
        text(c, name, x + 112, y + 70, font("display", 46 if len(name) < 10 else 40), INKC, alpha=k)
        icon(c, i, x + 575, y + 52, k * 0.9)
        c.restore()


def icon(c, i, x, y, k):
    if i == 0:    # a volcano with an ash column
        p = skia.Path()
        p.moveTo(x - 54, y + 40)
        p.lineTo(x - 16, y - 18)
        p.lineTo(x + 16, y - 18)
        p.lineTo(x + 54, y + 40)
        p.close()
        c.drawPath(p, fill(rgb("#6E5A4E"), k))
        c.drawPath(p, ink(3, alpha=k))
        for j, (dx, dy, r) in enumerate(((0, -34, 16), (-12, -52, 14), (10, -62, 15))):
            c.drawCircle(x + dx, y + dy, r, fill(rgb("#9C9590"), k))
            c.drawCircle(x + dx, y + dy, r, ink(2.5, alpha=k))
        c.drawPath(oval(x, y - 18, 16, 5), fill(CORAL, k))
    elif i == 1:  # the deep: a descending line into dark water
        c.drawPath(rrect(x - 50, y - 40, 100, 80, 10), fill(rgb("#163250"), k))
        c.drawLine(x, y - 40, x, y + 24, ink(3, col=FOAM, alpha=k))
        c.drawCircle(x, y + 28, 9, fill(YEL, k))
        c.drawCircle(x, y + 28, 9, ink(2.5, alpha=k))
        c.drawPath(rrect(x - 50, y - 40, 100, 80, 10), ink(3, alpha=k))
    else:         # the moon
        c.drawCircle(x, y, 40, fill(rgb("#E6E1D3"), k))
        for dx, dy, r in ((-12, -10, 9), (14, 8, 7), (-4, 18, 5)):
            c.drawCircle(x + dx, y + dy, r, fill(rgb("#BDB6A6"), k))
        c.drawCircle(x, y, 40, ink(3, alpha=k))


def respawn_flash(c, t):
    a = E["n24"] + 0.02
    if t >= a:
        k = prog(t, a, DURATION)
        c.drawRect(skia.Rect.MakeWH(W, H), fill(PAPER_HI, ease_io(min(1, k * 1.6))))


def gale_overlay(c, t):
    """The wind, tight on her: long woodblock wind strokes and snow streaking across the frame."""
    tw = twos(t)
    for j in range(9):
        ph = (tw * 2.2 + j * 0.37) % 1.0
        y = 300 + j * 130 + 30 * math.sin(j * 2.1)
        x0 = -400 + ph * 1900
        p = skia.Path()
        p.moveTo(x0, y)
        p.cubicTo(x0 + 160, y - 30, x0 + 300, y + 26, x0 + 460, y - 8)
        c.drawPath(p, ink(5, col=WHITE, alpha=0.75 * math.sin(ph * math.pi)))
    snowfall(c, tw, density=70, alpha=0.85, wind=1.0, seed=9)


def cam_close(t):
    """Camera on the close shot: a slow push-out over the hook, punch-ins on the NOPEs, a push-in at the end."""
    z = 1.0
    if t < shot_start("jars"):
        z = 1.10 - 0.10 * ease_io(prog(t, 1.2, shot_start("jars")))
    return z * punch(t)


# ---------------------------------------------------------------- frame
def draw_frame(c, t):
    sx, sy = shake(t)
    c.save()
    c.translate(sx, sy)
    shot = shot_at(t)[1]
    if shot in ("close", "end", "gale"):
        z = cam_close(t)
        dyc = 0.0
        if shot == "end":
            z = 1.12 + 0.08 * ease_io(prog(t, L["n22"], DURATION))
            dyc = 70.0
        elif shot == "gale":
            z = 1.32 + 0.06 * prog(t, shot_start("gale"), L["n10"])
            dyc = 40.0
        if z != 1.0 or dyc:
            c.translate(XH, YH + dyc)
            c.scale(z, z)
            c.translate(-XH, -YH)
        close_shot(c, t)
        if shot == "gale":
            c.restore()
            c.save()
            gale_overlay(c, t)
        if L["n7"] <= t < L["n16"] and shot == "close":
            frost(c, min(1.0, (t - L["n8"]) / 3.0) * 0.5 if t >= L["n8"] else 0.0)
    elif shot == "jars":
        jars_shot(c, t)
    elif shot == "climb":
        climb_shot(c, t)
    elif shot == "wide":
        wide_shot(c, t)
    elif shot == "timer":
        timer_shot(c, t)
    elif shot == "duck":
        duck_shot(c, t)
    elif shot == "gauge":
        gauge_shot(c, t)
    elif shot == "strata":
        strata_shot(c, t)
    c.restore()
    paper_over(c, 1.0)
    vignette(c, 0.26)
    hud(c, t)
    intercom(c, t)
    end_cards(c, t)
    nope_text(c, t)
    captions(c, t)
    respawn_flash(c, t)
