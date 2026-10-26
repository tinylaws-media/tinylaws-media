"""THE EXIT MANUAL — TRANSMISSION 001 · FOLLOW THE MONEY: "The richest pay a lower tax rate than the merely rich."

Facts (checked 25 Oct 2026):
- IPP (Institut des politiques publiques), Note n°92, "Quels impôts les milliardaires paient-ils ?", Bach, Bozio,
  Guillouzouic & Malgouyres, June 2023 (updated PDF, page modified 21 Jul 2026). French administrative tax data for
  2016. Effective DIRECT tax rate (income tax, social levies, wealth tax, corporate tax on profits of companies the
  household controls) as a share of "economic income" (incl. undistributed profits of companies they control):
  46 % for the top 0.1 % (about 37,800 households), 26 % for the top 0.0002 % (about 75 households, "billionaires").
  Cause stated by IPP: most of their income stays in companies they control, and corporate tax is lower than
  personal income tax. https://www.ipp.eu/en/publication/what-taxes-do-billionaires-pay/
- Critics (iFRAP; F. Geerolf, OFCE) say part of it is taxed later (on payout, sale or inheritance) and that the
  study covers direct taxes only, one year (2016). Both points are said or shown in the video.
- Adam Smith, The Wealth of Nations (1776), Book V, ch. 2, part II, first maxim: "The subjects of every state ought
  to contribute towards the support of the government, as nearly as possible, in proportion to their respective
  abilities; that is, in proportion to the revenue which they respectively enjoy under the protection of the state."

Times come from measured line lengths: python3 exit_voice.py exit_ep001 writes out/exit_ep001_timing.json.
"""
import json
import math
import os

import skia

from exit_engine import *

EPISODE = "TRANSMISSION 001"
SERIES = "FOLLOW THE MONEY"
VOICE = "am_fenrir"
VOICE_SPEED = 0.95
VOICE_FX = {"semitones": -3.0, "radio": 0.55}

# (id, spoken text with '|' where the caption block changes, pause after (s), options)
LINES = [
    ("hook", "In twenty sixteen, France's seventy-five top-earning households | paid twenty-six percent in direct taxes.", 0.55),
    ("nums", "The top zero point one percent, as a whole? | Forty-six.", 0.8),
    ("cheat", "Not because they cheat. | It's legal.", 0.6),
    ("inside", "Most of their income | stays inside companies they control.", 0.35),
    ("less", "And company profits are taxed less.", 0.7),
    ("later", "Fair point: | some of it is taxed later, | when it's paid out or passed on.", 0.25),
    ("choose", "But they choose when.", 0.65),
    ("smith", "Adam Smith's first rule of taxes, | seventeen seventy-six:", 0.2),
    ("prop", "pay in proportion to your abilities.", 0.45),
    ("breaks", "A lower rate at the very top | breaks that rule.", 0.4),
    ("arith", "Not left. | Not right. | Just Smith's rule.", 0.65),
    ("voted", "Rules are voted, | so they can change. | In twenty twenty-six, France voted a tax | on yachts, planes and jewels | kept in such companies.", 0.3),
    ("small", "A small step. | But a step.", 0.75),
    ("step", "Step one: | send this to someone who thinks | the richest pay the highest rate.", 0.55),
    ("ask", "Then tell me below: | one rate for everyone, | or more for the top?", 0.75),
    ("sign", "build the commons.", 0.7),
    ("loop", "Twenty-six. | Forty-six. | Send it.", 0.0),
]

# caption blocks, one per '|' chunk (None = the picture itself carries the words)
CAPS = {
    "hook": ["In *2016*, France's / *75 top-earning* households", "paid *26%* / in *direct taxes.*"],
    "nums": ["The *top 0.1%,* / as a whole?", "*46%.*"],
    "cheat": ["Not because / they cheat.", "It's *legal.*"],
    "inside": ["Most of their income", "stays inside *companies* / they control."],
    "less": ["And company profits / are *taxed less.*"],
    "later": ["Fair point:", "some of it is / *taxed later,*", "when it's paid out / or passed on."],
    "choose": ["But *they choose* / *when.*"],
    "smith": ["Adam Smith's first / rule of taxes,", "*1776:*"],
    "prop": ["pay *in proportion* / to your abilities."],
    "breaks": ["A lower rate / at the very top", "*breaks that rule.*"],
    "arith": [None, None, None],
    "voted": ["Rules are *voted,*", "so they *can change.*", "In *2026*, France / voted a tax", "on *yachts, planes* / *and jewels*", "kept in such companies."],
    "small": ["A small step.", "But *a step.*"],
    "step": ["*Step one:*", "send this to someone / who thinks", "the richest pay / the *highest rate.*"],
    "ask": ["Then *tell me below:*", "*one rate* / for everyone,", "or *more* / for the top?"],
    "sign": [None],
    "loop": ["*26%.*", "*46%.*", "*Send it.*"],
}

# ------------------------------------------------------------------ timing
_TP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "exit_ep001_timing.json")
TIM = json.load(open(_TP)) if os.path.exists(_TP) else None
if TIM and [(l[0], " ".join(p.strip() for p in l[1].split("|"))) for l in LINES] != \
        [(k, v["text"]) for k, v in TIM.items() if not k.startswith("_")]:
    TIM = None                     # stale timing: run exit_voice.py again
DURATION = round(TIM["_end"] + 0.75, 2) if TIM else None


def T(i):
    return TIM[i]["start"]


def E(i):
    return TIM[i]["end"]


def CH(i, k):
    return TIM[i]["chunks"][k]


def nxt(i):
    ids = [l[0] for l in LINES]
    j = ids.index(i)
    return T(ids[j + 1]) if j + 1 < len(ids) else DURATION


CAPTIONS = []
if TIM:
    for (lid, _, _, *r) in LINES:
        blocks = CAPS[lid]
        ch = TIM[lid]["chunks"]
        assert len(blocks) == len(ch), lid
        for k, txt in enumerate(blocks):
            if txt is None:
                continue
            a = 0.0 if lid == "hook" and k == 0 else ch[k] - 0.04
            # a block stays until the next block starts (frame-exact hand-over, no overlap)
            b = ch[k + 1] - 0.04 if k + 1 < len(blocks) else (DURATION + 1 if lid == "loop" else nxt(lid) - 0.04)
            CAPTIONS.append(Caption(a, b, txt))

# narrator loudness per frame (Relay's nodes)
_EP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "exit_ep001_voice_env.npy")
import numpy as _np
VOICE_ENV = _np.load(_EP) if os.path.exists(_EP) else None


def level(t):
    if VOICE_ENV is None:
        return 0.0
    i = int(t * FPS)
    return float(VOICE_ENV[i]) if 0 <= i < len(VOICE_ENV) else 0.0


# ------------------------------------------------------------------ shared pieces
SRC_IPP = ["source: IPP note 92 (2023) \u00b7 French tax data, 2016"]
SRC_SMITH = ["source: Adam Smith, The Wealth of Nations (1776), V.2"]
SRC_LAW = ["source: French Finance Law for 2026 (JO, 20 Feb 2026),", "art. 7 \u00b7 tax code art. 235 ter C"]


def header(X):
    relay_icon(X, 98, 270, 30)
    X.text("> " + EPISODE, 148, 288, 54, "green", align="left", rgb=True)
    X.text(SERIES, 150, 336, 38, "cyan", align="left")
    X.text("THE EXIT MANUAL", 892, 288, 34, "grey", align="right")


def sources(X, lines, alpha=1.0):
    for i, s in enumerate(lines):
        X.text(s, 80, 1412 + i * 38, 36, "grey", align="left", alpha=alpha)


BAR_X, BAR_SCALE = 110, 12.0         # px per percentage point (50 % -> 600 px)
BARS = [("TOP 0.1%", "about 37,800 households", 46, "cyan", 600), ("TOP 75", "top-earning households", 26, "magenta", 850)]


def bars(X, fills, ghost=0.0, title_alpha=1.0, hi=(0.0, 0.0)):
    """The one picture: two bars. fills = (0..1, 0..1) of each bar's value."""
    X.text("THE TOP 75 PAID A LOWER RATE", 80, 446, 60, "white", align="left", alpha=title_alpha, rgb=True)
    X.text("direct taxes, % of income incl. profits kept in", 80, 490, 30, "grey", align="left", alpha=title_alpha)
    X.text("companies they control", 80, 520, 30, "grey", align="left", alpha=title_alpha)
    for (name, sub, v, color, y), f, h in zip(BARS, fills, hi):
        if h > 0:                      # calm highlight on the number being spoken (no flash: slow in, slow out)
            X.neon_rect(BAR_X - 16, y - 58, 790, 200, color, width=3, r=16, glow=0.6, alpha=h)
        X.text(name, BAR_X, y, 60, color, align="left", rgb=False, glow=0.4)
        X.text(sub, BAR_X + X.width(name, 60) + 18, y, 32, "grey", align="left")
        # track
        X.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(BAR_X, y + 26, BAR_X + 50 * BAR_SCALE, y + 126), 10, 10),
                      X.paint(DIM, 1.0))
        w = v * BAR_SCALE * ease_out(f)
        if w > 4:
            X.neon_rect(BAR_X, y + 26, w, 100, color, width=4, r=10, fill=color, fill_alpha=0.30)
        if f > 0.02:                   # both numbers sit in one column, right of the longest bar
            val = int(round(v * ease_out(f)))
            X.text(f"{val}%", BAR_X + 46 * BAR_SCALE + 24, y + 106, 104, color, align="left", glow=0.7)
    if ghost > 0:                      # the missing 20 points, as a dashed outline on the second bar
        y = BARS[1][4]
        x0, x1 = BAR_X + 26 * BAR_SCALE, BAR_X + 46 * BAR_SCALE
        p = X.paint("cyan", 0.8 * ghost, stroke=3)
        p.setPathEffect(skia.DashPathEffect.Make([12, 10], 0))
        X.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y + 26, x1, y + 126), 10, 10), p)


# ------------------------------------------------------------------ scenes
def ghost_label(X, a):
    y = BARS[1][4]
    X.text("20 points less", BAR_X + 36 * BAR_SCALE, y + 168, 40, "cyan", alpha=a)


def hl(t, t0, t1):
    return 0.9 * prog(t, t0, t0 + 0.25) * (1 - prog(t, t1 - 0.25, t1))


def scene_hook(X, t):            # 0 -> cheat: the claim and its proof, from frame 0; numbers already final
    k = 1.0 + 0.03 * ease_in_out(prog(t, 0, T("cheat")))           # slow push-in (calm)
    X.c.save()
    X.c.translate(485, 760)
    X.c.scale(k, k)
    X.c.translate(-485, -760)
    h2 = hl(t, 0.5, T("nums") - 0.1)                                # the 75, then "paid 26%"
    h1 = hl(t, T("nums") - 0.1, CH("nums", 1) + 0.9)               # "the top 0.1%... 46"
    g = prog(t, CH("nums", 1) + 0.3, CH("nums", 1) + 0.8)          # the missing 20 points trace in after "46"
    bars(X, (1.0, 1.0), ghost=g, hi=(h1, h2))
    if g > 0:
        ghost_label(X, g)
    X.c.restore()
    sources(X, SRC_IPP)


# --- the mechanism: a neon money-flow diagram that draws itself
BOX = (175, 600, 620, 190)               # company they control
POCKET = (520, 935, 330, 110)
TAXBOX = (110, 935, 330, 110)


def coin_stack(X, n, alpha=1.0):
    x0, y0 = BOX[0] + 60, BOX[1] + BOX[3] - 34
    for i in range(n):
        col_i, row = i % 9, i // 9
        coin(X, x0 + col_i * 56, y0 - row * 34, 20, "green", alpha)


def scene_mech(X, t):
    t_cheat = T("cheat")
    t_in = T("inside")
    if t < t_in:                         # "Not because they cheat. It's legal."  terminal check
        X.panel(110, 520, 760, 330, alpha=0.9)
        X.typed("> cheating?", 150, 620, 72, t_cheat + 0.15, color="white")
        if t >= CH("cheat", 0) + 0.9:
            X.text("NO", 820, 620, 72, "magenta", align="right", glow=0.5)
        X.typed("> legal?", 150, 760, 72, CH("cheat", 1) - 0.1, color="white")
        if t >= CH("cheat", 1) + 0.3:
            X.text("YES", 820, 760, 72, "green", align="right", glow=0.6)
        sources(X, SRC_IPP)
        return
    bx, by, bw, bh = BOX
    u = ease_out(prog(t, t_in, t_in + 0.7))
    X.text("PROFITS", 485, 470, 64, "green", glow=0.5, alpha=prog(t, t_in, t_in + 0.3))
    X.arrow([(485, 492), (485, by - 8)], "green", u=prog(t, t_in + 0.1, t_in + 0.5), width=5)
    if u > 0:
        X.neon_rect(bx + bw / 2 * (1 - u), by, bw * u, bh, "cyan", width=5, fill=0xFF061018, fill_alpha=0.9)
    if u > 0.9:
        X.text("COMPANY THEY CONTROL", bx + bw / 2, by + 52, 50, "cyan")
    t_flow = t_in + 0.6
    n_land = 0
    if t >= t_flow:
        k = int((t - t_flow) / 0.45)
        for j in range(max(0, k - 2), k + 1):
            tj = t_flow + j * 0.45
            ph = (t - tj) / 0.7
            if 0 <= ph < 1 and n_land < 27:
                coin(X, 485, lerp(500, by + bh - 40, ease_in_out(ph)), 20)
        n_land = min(18, max(0, int((t - t_flow - 0.7) / 0.45) + 1))
    coin_stack(X, n_land)
    if t >= CH("inside", 1) + 0.6:
        X.text("stays here", bx + bw - 20, by + bh + 46, 44, "green", align="right",
               alpha=prog(t, CH("inside", 1) + 0.6, CH("inside", 1) + 0.9) * (1 - prog(t, T("later"), T("later") + 0.3)))
    if t >= T("less"):
        t0 = T("less") + 0.2
        X.arrow([(bx + 150, by + bh), (bx + 150, TAXBOX[1] - 6)], "magenta", u=prog(t, t0, t0 + 0.4), width=4)
        a = prog(t, t0 + 0.3, t0 + 0.6)
        X.neon_rect(*TAXBOX, "magenta", width=4, fill=0xFF14040C, fill_alpha=0.9, alpha=a)
        X.text("company tax:", TAXBOX[0] + TAXBOX[2] / 2, TAXBOX[1] + 46, 42, "white", alpha=a)
        X.text("LOWER RATE", TAXBOX[0] + TAXBOX[2] / 2, TAXBOX[1] + 92, 50, "magenta", alpha=a, glow=0.5)
    if t >= T("later"):
        t0 = CH("later", 1)
        X.arrow([(bx + bw - 120, by + bh), (bx + bw - 120, POCKET[1] - 6)], "white", u=prog(t, t0, t0 + 0.5),
                width=4, dashed=True, alpha=0.9)
        a = prog(t, t0 + 0.3, t0 + 0.6)
        X.neon_rect(*POCKET, "white", width=3, glow=0.5, fill=0xFF0A0C12, fill_alpha=0.9, alpha=a)
        X.text("THEIR POCKET", POCKET[0] + POCKET[2] / 2, POCKET[1] + 50, 44, "white", alpha=a)
        X.text("taxed later", POCKET[0] + POCKET[2] / 2, POCKET[1] + 92, 36, "grey", alpha=a)
    if t >= T("choose"):                 # the valve they control
        vx, vy = bx + bw - 120, by + bh + 72
        k = ease_out(prog(t, T("choose"), T("choose") + 0.4))
        X.c.drawCircle(vx, vy, 34 * k, X.paint(0xFF05060A))
        X.c.drawCircle(vx, vy, 34 * k, X.paint("green", 0.9, stroke=5))
        X.neon_line(vx - 24 * k, vy, vx + 24 * k, vy, "green", 5)
        if k > 0.9:
            X.panel(vx - 330, vy - 44, 270, 92, alpha=0.9, border=None)
            X.text("they choose", vx - 60, vy - 6, 42, "green", align="right", glow=0.4)
            X.text("when", vx - 60, vy + 34, 42, "green", align="right", glow=0.4)
    sources(X, SRC_IPP)


def scene_smith(X, t):
    t0 = T("smith")
    X.panel(90, 410, 800, 420, alpha=0.9, border="cyan")
    X.typed("> ADAM SMITH, 1776", 130, 490, 60, t0 + 0.1, color="cyan", rgb=True)
    if t >= T("prop") - 0.2:
        a = prog(t, T("prop") - 0.2, T("prop") + 0.1)
        X.text("\u201c...in proportion to", 130, 600, 66, "white", align="left", alpha=a)
        X.text("their respective", 130, 672, 66, "white", align="left", alpha=a)
        X.text("abilities.\u201d", 130, 744, 66, "white", align="left", alpha=a)
        X.text("the first rule of taxes", 860, 800, 34, "grey", align="right", alpha=a)
    if t >= T("breaks"):
        a = prog(t, T("breaks"), T("breaks") + 0.3)
        for i, (name, _, v, color, _) in enumerate(BARS):
            y = 900 + i * 100
            X.text(name, 110, y + 44, 48, color, align="left", alpha=a)
            X.neon_rect(330, y + 6, v * 9.5 * a, 50, color, width=3, r=8, fill=color, fill_alpha=0.3, alpha=a)
            X.text(f"{v}%", 330 + 46 * 9.5 + 18, y + 48, 58, color, align="left", alpha=a)
        if t >= CH("breaks", 1):
            X.typed("> proportional?  NO", 110, 1112, 56, CH("breaks", 1), color="magenta")
    sources(X, SRC_SMITH)


def scene_arith(X, t):           # "Not left. Not right. Just Smith's rule."  The words are the picture.
    rows = [("NOT LEFT.", "white", CH("arith", 0), 560, 104), ("NOT RIGHT.", "white", CH("arith", 1), 700, 104),
            ("SMITH'S RULE.", "green", CH("arith", 2), 880, 120)]
    for s_, c, ta, y, size in rows:
        if t >= ta - 0.03:
            a = prog(t, ta - 0.03, ta + 0.12)
            big = c == "green"
            X.text(s_, 485, y, size, c, alpha=a, rgb=not big, glow=0.8 if big else 0.0)
    if t >= CH("arith", 2) + 0.2:
        X.text("same share for all", 485, 1000, 52, "grey", alpha=prog(t, CH("arith", 2) + 0.2, CH("arith", 2) + 0.5))


def scene_voted(X, t):           # rules are voted -> a real, voted change (small, honest)
    if t < CH("voted", 2) - 0.15:
        relay(X, 485, 720, 0.8)
        return
    t0 = CH("voted", 2)
    X.panel(90, 410, 800, 640, alpha=0.92, border="cyan")
    X.typed("> FRANCE \u00b7 FINANCE LAW 2026", 130, 490, 56, t0 - 0.1, color="cyan", rgb=True)
    X.text("new tax on what holding", 130, 566, 44, "grey", align="left", alpha=prog(t, t0 + 0.3, t0 + 0.6))
    X.text("companies keep for their owners:", 130, 612, 44, "grey", align="left", alpha=prog(t, t0 + 0.3, t0 + 0.6))
    items = [("yachts", CH("voted", 3)), ("planes", CH("voted", 3) + 0.45), ("jewels", CH("voted", 3) + 0.95)]
    for i, (w, ti) in enumerate(items):
        if t >= ti:
            y = 710 + i * 92
            a = prog(t, ti, ti + 0.15)
            X.c.drawRect(skia.Rect(140, y - 50, 194, y + 4), X.paint("green", a, stroke=4))
            X.neon_line(150, y - 24, 164, y - 8, "green", 5, alpha=a, glow=0.5)
            X.neon_line(164, y - 8, 186, y - 44, "green", 5, alpha=a, glow=0.5)
            X.text(w, 230, y, 70, "white", align="left", alpha=a)
    if t >= T("small"):
        X.text("a small step.", 860, 1010, 50, "green", align="right", alpha=prog(t, T("small"), T("small") + 0.2), glow=0.4)
    sources(X, SRC_LAW)


def scene_step(X, t):
    t0 = T("step")
    X.typed("> STEP ONE", 110, 470, 72, t0 + 0.05, color="green", rgb=True)
    if t >= CH("step", 1):
        a = prog(t, CH("step", 1), CH("step", 1) + 0.25)
        X.neon_rect(110, 540, 620, 250, "white", width=3, glow=0.4, fill=0xFF0C0F18, fill_alpha=0.95, alpha=a)
        X.text("someone you know:", 140, 600, 38, "grey", align="left", alpha=a)
        if t >= CH("step", 2):
            b = prog(t, CH("step", 2), CH("step", 2) + 0.2)
            X.text("\u201cThe richest pay", 140, 676, 58, "white", align="left", alpha=b)
            X.text("the highest rate.\u201d", 140, 740, 58, "white", align="left", alpha=b)
        sx, sy = 800, 640
        X.arrow([(sx - 30, sy + 60), (sx - 30, sy + 90), (sx + 50, sy + 90), (sx + 50, sy + 60)], "cyan", u=a, width=4, head=1)
        X.arrow([(sx + 10, sy + 50), (sx + 10, sy - 30)], "cyan", u=a, width=5, head=20)
        X.text("send", sx + 10, sy + 140, 40, "cyan", alpha=a)


def scene_ask(X, t):
    X.text("> YOUR TURN", 110, 470, 72, "green", align="left", rgb=True)
    X.text("what's fair? answer below", 110, 522, 40, "grey", align="left")
    opts = [("ONE RATE", "FOR EVERYONE", CH("ask", 1)), ("MORE", "FOR THE TOP", CH("ask", 2))]
    for i, (a1, a2, ta) in enumerate(opts):
        y = 580 + i * 230
        a = prog(t, ta - 0.05, ta + 0.2)
        X.neon_rect(110, y, 700, 190, "cyan", width=4, fill=0xFF061018, fill_alpha=0.9, alpha=a)
        X.c.drawRect(skia.Rect(150, y + 60, 210, y + 120), X.paint("cyan", a, stroke=4))
        X.text(a1, 250, y + 86, 68, "white", align="left", alpha=a)
        X.text(a2, 250, y + 152, 56, "cyan", align="left", alpha=a)
    if t >= CH("ask", 2) + 0.4:
        X.arrow([(460, 1060), (460, 1130)], "green", u=prog(t, CH("ask", 2) + 0.4, CH("ask", 2) + 0.7), width=5)


def scene_sign(X, t):
    relay(X, 485, 660, 0.72)
    a = prog(t, T("sign") - 0.05, T("sign") + 0.25)
    X.text("build the commons.", 485, 1130, 58, "magenta", kind="sign", alpha=a, glow=0.8)
    X.text("THE EXIT MANUAL", 485, 1220, 50, "cyan", alpha=a)


def scene_loop(X, t):            # back to frame 0: bars already final, highlight on each number as it is said
    h2 = hl(t, CH("loop", 0), CH("loop", 1))
    h1 = hl(t, CH("loop", 1), CH("loop", 2) + 0.1)
    bars(X, (1.0, 1.0), hi=(h1, h2))
    sources(X, SRC_IPP)


def scenes():
    return [
        (0.0, T("cheat") - 0.2, scene_hook),
        (T("cheat") - 0.2, T("smith") - 0.2, scene_mech),
        (T("smith") - 0.2, T("arith") - 0.15, scene_smith),
        (T("arith") - 0.15, T("voted") - 0.2, scene_arith),
        (T("voted") - 0.2, T("step") - 0.2, scene_voted),
        (T("step") - 0.2, T("ask") - 0.2, scene_step),
        (T("ask") - 0.2, T("sign") - 0.25, scene_ask),
        (T("sign") - 0.25, T("loop") - 0.2, scene_sign),
        (T("loop") - 0.2, DURATION + 1, scene_loop),
    ]


_SC = None


def draw_frame(X, t):
    global _SC
    _SC = _SC or scenes()
    X.level = level(t)
    X.background()
    for a, b, fn in _SC:
        if a <= t < b:
            fn(X, t)
            break
    header(X)
    for cap in CAPTIONS:
        cap.draw(X)
    X.overlay()


# ------------------------------------------------------------------ sound (exit_audio.py)
BPM = 84
TRANSPOSE = 0


def sfx_list():
    s = [
        (CH("hook", 1), "blip", 0),
        (CH("nums", 1), "blip", 1),
        (CH("nums", 1) + 0.3, "rise", 0),
        (T("cheat") - 0.2, "whoosh_low", 1),
        (T("cheat") + 0.15, "keys", 0),
        (CH("cheat", 1) - 0.1, "keys", 1),
        (CH("cheat", 1) + 0.3, "blip", 2),
        (T("inside"), "whoosh_low", 2),
    ]
    for j in range(0, 9):
        s.append((T("inside") + 0.6 + 0.7 + j * 0.9, "coin", j))
    s += [
        (T("less") + 0.3, "blip", 0),
        (CH("later", 1) + 0.3, "blip", 1),
        (T("choose"), "clunk", 0),
        (T("smith") - 0.2, "whoosh_low", 3),
        (T("smith") + 0.1, "keys", 2),
        (CH("breaks", 1), "keys", 3),
        (CH("arith", 2), "low_hit", 0),
        (T("voted") - 0.2, "whoosh_low", 4),
        (CH("voted", 2) - 0.1, "keys", 4),
        (CH("voted", 3), "blip", 2), (CH("voted", 3) + 0.45, "blip", 3), (CH("voted", 3) + 0.95, "blip", 4),
        (T("step") + 0.05, "keys", 5),
        (CH("ask", 1), "blip", 3),
        (CH("ask", 2), "blip", 4),
        (T("sign") - 0.25, "low_hit", 1),
        (T("loop") - 0.2, "whoosh_low", 5),
    ]
    return s


SUBTITLE_EXTRAS = []
EXTRA_KEYS = []
if TIM:
    EXTRA_KEYS = [round(CH("arith", 2) + 0.4, 2), round(T("sign") + 0.4, 2), round(CH("loop", 1) + 0.2, 2)]
    SUBTITLE_EXTRAS = [
        (CH("arith", 0) - 0.04, CH("arith", 1) - 0.04, "Not left."),
        (CH("arith", 1) - 0.04, CH("arith", 2) - 0.04, "Not right."),
        (CH("arith", 2) - 0.04, nxt("arith") - 0.04, "Just Smith's rule."),
        (T("sign") - 0.04, nxt("sign") - 0.04, "build the commons."),
    ]


def draw_cover(X):
    """Cover / thumbnail: the claim, the two bars, Relay's badge. No byline."""
    X.t = 0.0
    X.background(drift=False)
    header(X)
    X.text("FRANCE'S TOP 75", 485, 470, 104, "white", rgb=True)
    X.text("PAID A LOWER", 485, 570, 104, "white", rgb=True)
    X.text("TAX RATE", 485, 670, 116, "green", glow=0.9)
    X.c.save()
    X.c.translate(0, 300)
    for (name, sub, v, color, y) in BARS:
        X.text(name, BAR_X, y, 60, color, align="left", glow=0.4)
        w = v * BAR_SCALE
        X.neon_rect(BAR_X, y + 26, w, 100, color, width=4, r=10, fill=color, fill_alpha=0.30)
        X.text(f"{v}%", BAR_X + 46 * BAR_SCALE + 24, y + 106, 104, color, align="left", glow=0.7)
    X.c.restore()
    X.text("direct taxes, 2016 · source: IPP note 92 (2023)", 80, 1412, 36, "grey", align="left")
    X.overlay()
