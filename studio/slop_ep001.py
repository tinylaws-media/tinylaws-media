"""SLOP SHOP #001 — "Did You Know? (No)"  (bank row 6). 61.94 s at 124 BPM (32 bars), loops.

Glorp, a glossy pink blob with too many fingers, reads "100% real facts" while the picture disagrees
with every one of them. A sticker sets the game on frame 0: "1 of these facts is real".
Escalation: an object disagrees (the penguin's signs, the Sun next to the Moon), his own body disagrees
live (the finger counter), the whole picture outnumbers him (penguins that can read), and the pressure
cracks him (sweat, "this video is not AI" while the watermark grows). The drop: he finally says a TRUE
fact, the card does not melt, the reality bar hits 100% for the first time, the SYSTEM flags it, and Glorp
admits nobody told him which ones were real ("Correct."). That is the satire: a fact channel says true and
false with the same confidence. Then "Reality reset", the comment button, and "Okay. A real one this time."
melts straight back into frame 0 ("Fact: penguins invented Wednesday.").

The one real fact (checked 25 Oct 2026):
  first sharks ~450 million years ago (Late Ordovician scales): Natural History Museum, London,
  https://www.nhm.ac.uk/discover/shark-evolution-a-450-million-year-timeline
  first trees ~385 million years ago (Middle Devonian): BBC Wildlife / Discover Wildlife,
  https://www.discoverwildlife.com/prehistoric-life/are-sharks-older-than-trees
Every other "fact" is absurd on purpose and contradicted on screen, so none can pass as real news.

Built against an independent review (game sticker on frame 0, intro cut, sign "it was thursday.",
hand and signs inside the safe zone, numbers on screen not spoken, lemonade beat cut, loop line that
melts, "fake fact" comment prompt).

Timing: python3 slop_voice.py slop_ep001 measure  -> out/slop_ep001_durs.json; the timeline below is
laid out from those measured line lengths plus the GAP after each line (scaled to fill DURATION).
"""
import json
import math
import os

import numpy as np

from slop_engine import *
from slop_engine import _hand

BPM = 124
BEAT = 60.0 / BPM
BAR = 4 * BEAT
DURATION = 32 * BAR            # 61.94 s
TRANSPOSE = 5                  # F major: bright, bouncy "infomercial" jingle
CHORDS = [  # F, Am, Bb, C  (one per bar), written in C and transposed by audio.py
    ([36, 48, 52, 55], 36), ([40, 47, 52, 55], 40), ([41, 48, 53, 57], 41), ([43, 50, 55, 59], 43),
]
MOTIFS = [   # Glorp's jingle (8ths): da-da-DA, da-da-DUM
    [(0, 4, 1), (1, 4, 1), (2, 6, 2), (4, 5, 1), (5, 4, 1), (6, 2, 2)],
    [(0, 2, 1), (1, 3, 1), (2, 4, 2), (4, 7, 1), (5, 6, 1), (6, 5, 2)],
    [(0, 4, 1), (1, 4, 1), (2, 6, 2), (4, 8, 1), (5, 7, 1), (6, 6, 2)],
    [(0, 5, 1), (1, 4, 1), (2, 2, 1), (3, 1, 1), (4, 0, 4)],
]

# ------------------------------------------------------------------ cast & lines
CAST = {"G": ("am_michael", 1.12, {"semitones": 1.0}),      # Glorp: the over-eager AI narrator
        "S": ("bf_emma", 0.95, {"semitones": -2.0})}        # SYSTEM: the flat generator voice
CAST_GAIN = {"G": 1.0, "S": 0.9}
MOUTH = "G"

#   name       who  text                                                 opts                gap after (s)
LINES_T = [
    ("wed",     "G", "Fact: penguins invented Wednesday.", {}, 0.2),
    ("one",     "S", "One of these facts is real.", {}, 0.3),
    ("1974",    "G", "In nineteen seventy-four. With their hands.", {}, 0.75),
    ("src",     "G", "Source: me.", {}, 0.2),
    ("srcnf",   "S", "Source not found.", {}, 0.55),
    ("moon",    "G", "Fact: the Moon is just the Sun, at night.", {}, 0.45),
    ("never",   "G", "Never seen together.", {}, 0.75),
    ("outfit",  "G", "Different outfit.", {}, 0.55),
    ("five",    "G", "Fact: I have five fingers.", {}, 0.4),
    ("normal",  "G", "Normal amount.", {}, 0.35),
    ("count",   "G", "Five. Count them.", {}, 0.35),
    ("wait",    "G", "I'll wait.", {}, 0.7),
    ("nopen",   "G", "Fact: there are no penguins in this video.", {}, 0.2),
    ("zero",    "G", "Zero penguins.", {}, 0.65),
    ("read",    "G", "Fact: penguins can't read.", {}, 1.15),
    ("calm",    "G", "Fact: I am calm.", {}, 0.55),
    ("notai",   "G", "Fact: this video is not AI.", {}, 0.95),
    ("shark",   "G", "Fact: sharks are older than trees.", {}, 1.05),
    ("warn",    "S", "Warning. True fact detected.", {}, 0.3),
    ("what",    "G", "What?", {"semitones": 3.0}, 0.9),
    ("wasreal", "G", "That one was real?!", {"semitones": 3.0}, 0.2),
    ("nobody",  "G", "Nobody told me which ones were real!", {"speed": 1.2}, 0.3),
    ("correct", "S", "Correct.", {}, 0.35),
    ("who",     "G", "Wait. Who wrote my facts?", {}, 0.25),
    ("you",     "S", "You did.", {}, 0.7),
    ("reset",   "G", "Reality reset!", {}, 0.35),
    ("comment", "G", "Comment a fake fact. I'll make it real.", {}, 0.55),
    ("trust",   "G", "Trust me.", {}, 0.45),
    ("again",   "G", "Okay. A real one this time.", {}, 0.15),
]
LINES = [(w, s, o) for (_, w, s, o, _) in LINES_T]

_DURS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "slop_ep001_durs.json")
DURS = None
if os.path.exists(_DURS):
    _d = json.load(open(_DURS))
    if isinstance(_d, dict) and _d.get("lines") == [s for (_, _, s, _, _) in LINES_T]:
        DURS = _d["durs"]
if DURS is None:
    DURS = [max(0.6, len(s.split()) * 0.36) for (_, _, s, _, _) in LINES_T]
GAPS = [g for (*_, g) in LINES_T]
LEAD_IN = 0.08
_free = DURATION - LEAD_IN - sum(DURS)
_k = _free / sum(GAPS)                       # stretch/shrink the pauses to fill exactly 32 bars
T, E = {}, {}
_t = LEAD_IN
for (name, *_), d, g in zip(LINES_T, DURS, GAPS):
    T[name], E[name] = _t, _t + d
    _t += d + g * _k
NARRATION = [(T[n], w, s, o) for (n, w, s, o, _) in LINES_T]


def W_(name, frac):
    """A moment inside a line (frac of its length): for words like 'hands' or 'Sun'."""
    return T[name] + (E[name] - T[name]) * frac


# scene boundaries
S_MOON = T["moon"] - 0.15
S_FING = T["five"] - 0.15
S_PENG = T["nopen"] - 0.15
S_PRESS = T["calm"] - 0.15
S_SHARK = T["shark"] - 0.15
S_RESET = T["reset"] - 0.1
LOOP_SNAP = min(DURATION - 0.25, E["again"] - 0.05)   # the world snaps back to frame 0

# ------------------------------------------------------------------ captions (mirror the voice)
FACT_Y = 500


def melt_after(name, top, d=0.8):
    a = E[name] + 0.25
    return lambda t: top * ease_in_out(prog(t, a, a + d))


CAPTIONS = [
    Caption(0.0, T["src"], [(0.0, "Penguins invented / *Wednesday.*")], "fact", FACT_Y, melt=melt_after("1974", 0.45)),
    Caption(T["one"], T["1974"], [(T["one"], "One of these facts / is *real.*")]),
    Caption(T["1974"], T["src"], [(T["1974"], "In 1974. / With their *hands.*")]),
    Caption(T["src"], T["srcnf"], [(T["src"], "Source: *me.*")]),
    Caption(T["srcnf"], S_MOON, [(T["srcnf"], "SOURCE / NOT FOUND")], "sys", FACT_Y + 110, size=60),
    Caption(S_MOON, S_FING, [(T["moon"], "The Moon is just / the Sun at night.")], "fact", FACT_Y,
            melt=melt_after("never", 0.6)),
    Caption(T["never"], T["outfit"], [(T["never"], "Never seen / *together.*")]),
    Caption(T["outfit"], S_FING, [(T["outfit"], "Different *outfit.*")]),
    Caption(S_FING, S_PENG, [(T["five"], "I have five fingers.")], "fact", FACT_Y, melt=melt_after("normal", 0.85)),
    Caption(T["normal"], T["count"], [(T["normal"], "Normal *amount.*")]),
    Caption(T["count"], T["wait"], [(T["count"], "Five. *Count them.*")]),
    Caption(T["wait"], S_PENG, [(T["wait"], "I'll *wait.*")]),
    Caption(S_PENG, T["read"] - 0.05, [(T["nopen"], "There are no penguins / in this video.")], "fact", FACT_Y,
            melt=melt_after("nopen", 0.7)),
    Caption(T["zero"], T["read"], [(T["zero"], "*Zero* penguins.")]),
    Caption(T["read"], S_PRESS, [(T["read"], "Penguins / can't read.")], "fact", FACT_Y, melt=melt_after("read", 0.8)),
    Caption(S_PRESS, T["notai"] - 0.05, [(T["calm"], "I am calm.")], "fact", FACT_Y, melt=melt_after("calm", 0.95, 0.6)),
    Caption(T["notai"], S_SHARK, [(T["notai"], "This video / is not AI.")], "fact", FACT_Y, melt=melt_after("notai", 1.2, 0.6)),
    Caption(S_SHARK, T["warn"], [(T["shark"], "Sharks are older / than trees.")], "fact", FACT_Y),
    Caption(T["warn"], T["wasreal"], [(T["warn"], "WARNING: / TRUE FACT DETECTED")], "sys", FACT_Y + 110, size=52),
    Caption(T["what"], T["wasreal"], [(T["what"], "*What?*")]),
    Caption(T["wasreal"], T["nobody"], [(T["wasreal"], "That one / was *real?!*")]),
    Caption(T["nobody"], T["correct"], [(T["nobody"], "Nobody told me / which were *real!*")]),
    Caption(T["correct"], T["who"], [(T["correct"], "CORRECT.")], "sys", FACT_Y + 110, size=64),
    Caption(T["who"], T["you"], [(T["who"], "Wait. Who wrote / my *facts?*")]),
    Caption(T["you"], S_RESET, [(T["you"], "YOU DID.")], "sys", FACT_Y + 110, size=64),
    Caption(T["reset"], T["comment"], [(T["reset"], "Reality *reset!*")]),
    Caption(T["comment"], T["trust"], [(T["comment"], "Comment a fake fact. / I'll make it *real.*")]),
    Caption(T["trust"], T["again"], [(T["trust"], "Trust *me.*")]),
    Caption(T["again"], LOOP_SNAP, [(T["again"], "Okay. A *real* one / this time.")], y=FACT_Y + 40,
            size=92, melt=None),
]
# the loop: frame 0's card is back on the last frames (drawn outside CAPTIONS, so it is not a subtitle)
LOOP_CARD = Caption(LOOP_SNAP, DURATION + 1, [(0.0, "Penguins invented / *Wednesday.*")], "fact", FACT_Y)

SUBTITLE_EXTRAS = [   # the jokes that are only written on screen
    (0.0, T["1974"], "[sign: it was thursday.]"),
    (W_("1974", 0.85), T["src"] + 0.4, "[sign: no hands.]"),
    (T["src"] + 0.45, S_MOON, "[sign: source?]"),
    (E["read"] + 0.15, S_PRESS, "[signs: we can.]"),
    (T["what"], T["wasreal"], "[first sharks: ~450 million years ago / first trees: ~385 million years ago]"),
    (E["comment"] - 0.1, T["again"], "[sign: he can't.]"),
]

# ------------------------------------------------------------------ beats
SIGN_FLIPS = {"nohands": W_("1974", 0.85), "source": T["src"] + 0.45, "wecan": E["read"] + 0.15,
              "hecant": E["comment"] - 0.1, "thursday": T["again"] + 0.2}
SUN_IN = W_("moon", 0.62)
SELFIE = T["never"] + 0.1
SHADES = W_("outfit", 0.55)
FINGERS = [(0.0, 7), (W_("normal", 0.3), 8), (W_("normal", 0.75), 9), (W_("count", 0.2), 10), (W_("count", 0.55), 11),
           (W_("count", 0.9), 12), (W_("wait", 0.5), 13), (E["wait"] + 0.3, 14),
           (W_("calm", 0.7), 15), (E["calm"] + 0.2, 16), (E["calm"] + 0.45, 17),
           (S_RESET, 6), (SIGN_FLIPS["thursday"], 7)]
PEN_T0 = W_("nopen", 0.45)
BAR_FULL = (E["shark"] + 0.05, E["shark"] + 0.85)      # 99 -> 100 % in the silence
WM_GROW = (W_("notai", 0.6), E["notai"] + 0.6)

SFX = [
    (0.02, "pop", 0), (T["one"] - 0.05, "tap", 0), (T["srcnf"] - 0.05, "thud", 1), (T["you"] - 0.05, "thud", 2),
    (SIGN_FLIPS["nohands"], "paper", 0), (SIGN_FLIPS["source"], "paper", 1),
    (S_MOON, "whoosh", 0), (SUN_IN, "pop", 2), (SELFIE + 0.3, "tap", 1), (SHADES, "pop", 5),
    (S_FING, "whoosh", 0),
] + [(t, "pop", i + 3) for i, (t, n) in enumerate(FINGERS[1:8])] + [
    (S_PENG, "whoosh", 0), (PEN_T0, "pop", 1), (PEN_T0 + 0.7, "pop", 4), (PEN_T0 + 1.4, "pop", 6),
    (SIGN_FLIPS["wecan"], "paper", 2), (S_PRESS, "dizzy", 0), (WM_GROW[0], "riser", 0),
    (BAR_FULL[1], "ding", 0), (T["warn"] - 0.05, "thud", 0),
    (T["wasreal"] + 0.2, "fall", 0), (S_RESET + 0.05, "shrink", 0), (S_RESET + 0.5, "sparkle", 0),
    (SIGN_FLIPS["hecant"], "paper", 4), (W_("again", 0.5), "fall", 1), (LOOP_SNAP, "pop", 0),
]
_cut_end = math.ceil((T["warn"] + 0.05) / BAR) * BAR
MUSIC_CUTS = [(E["shark"] + 0.02, _cut_end)]


def music_sections(t):
    s = {"drums": 1, "bass": 1, "keys": 1, "lead": 1}
    if t < S_MOON:
        s.update(var=0)
    elif t < S_PENG:
        s.update(var=1)
    elif t < S_SHARK:
        s.update(drums=2, var=2)
    elif t < S_RESET:
        s.update(lead=0, keys=0, drums=1)
    else:
        s.update(glock=1, var=3)
    return s


# ------------------------------------------------------------------ mouth
_ENV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "slop_ep001_voice_env.npy")
VOICE_ENV = np.load(_ENV) if os.path.exists(_ENV) else None
WORD_TIMES = sorted(T.values())


def talking(t):
    if VOICE_ENV is not None:
        i = int(t * FPS)
        if 0 <= i < len(VOICE_ENV):
            return float(clamp01((VOICE_ENV[i] - 0.05) * 2.2))
        return 0.0
    for (n, w, *_) in LINES_T:
        if w == "G" and T[n] <= t < E[n]:
            return 0.5 + 0.5 * math.sin(t * 28)
    return 0.0


def blink(t, off=0.0):
    return ((t + 1.3 + off) % 3.7) < 0.1 and 0.3 < t < DURATION - 0.4


# ------------------------------------------------------------------ shared pieces
def hud(R, t):
    if BAR_FULL[0] <= t < S_RESET + 0.3:
        pct = 99 if t < BAR_FULL[1] else 100
        if t >= S_RESET + 0.15:
            pct = 99
        reality_bar(R, pct, ok=pct == 100)
    else:
        reality_bar(R, 99)
    # the game sticker
    found = T["warn"] <= t < S_RESET
    sticker(R, "1 of these facts is real", 330, 388, size=48, stamp="FOUND" if found else None,
            stamp_k=prog(t, T["warn"], T["warn"] + 0.25))


def fingers_at(t):
    n = 7
    for (t0, k) in FINGERS:
        if t >= t0:
            n = k
    return n


def flip_val(t, t0, d=0.3):
    """sign flip: 1 -> 0 (edge-on) -> 1, the text swaps at the middle."""
    u = prog(t, t0 - d / 2, t0 + d / 2)
    return abs(math.cos(u * math.pi))


def any_flip(t, keys):
    for k in keys:
        if abs(t - SIGN_FLIPS[k]) < 0.15:
            return flip_val(t, SIGN_FLIPS[k])
    return 1.0


def glorp_base(t, **kw):
    G = GlorpState(**kw)
    G.wobble = t
    G.talk = talking(t)
    G.blink = blink(t)
    return G


def host_shot(R, t, sign_text, flip, melt=0.0, fingers=7, pen_x=760):
    """Frame 0's layout: Glorp left (hand up-left, away from the app buttons), the penguin right."""
    R.gradient_bg()
    R.bokeh(t, 1)
    R.flare(820, 860, 0.8, 0.7)
    floor(R)
    G = glorp_base(t, x=360, y=1130, r=185)
    G.hand = "wave"
    G.side = -1
    G.expr = "grin"
    G.fingers = fingers
    G.melt = melt
    G.look = (0.7, 0.1)
    draw_glorp(R, G)
    flap = 1.0 if abs(t - SIGN_FLIPS["nohands"]) < 0.6 else 0.0
    penguin(R, pen_x, 1345, 1.12, t, look=-0.7, sign_text=sign_text, flip=flip, blink=blink(t, 1.1),
            flap=flap * abs(math.sin(t * 9)), sign_size=62, sign_side=-1)


# ------------------------------------------------------------------ scenes
def scene_open(R, t):                    # 0 -> S_MOON
    seq = [(-1, "it was thursday."), (SIGN_FLIPS["nohands"], "no hands."), (SIGN_FLIPS["source"], "source?")]
    txt = [s for t0, s in seq if t >= t0][-1]
    host_shot(R, t, txt, any_flip(t, ("nohands", "source")))
    watermark(R)


def scene_moon(R, t):                    # the Moon and the Sun, in the same sky
    R.gradient_bg(NIGHT0, VIOLET, NIGHT1)
    rng = np.random.default_rng(4)
    for i in range(40):
        x, y = rng.uniform(0, W), rng.uniform(250, 1500)
        R.fill(circle(x, y, rng.uniform(2, 5)), WHITE, 0.5 + 0.3 * math.sin(t * 1.5 + i))
    floor(R, 1330, 0xFF8A7BD0)
    k_in = pop(t, S_MOON, 0.35, 0.5)
    sel = ease_in_out(prog(t, SELFIE, SELFIE + 0.4))          # they squeeze together for a selfie
    mx, sx_ = lerp(300, 380, sel), lerp(760, 630, sel)
    tilt = 8 * sel
    look_m, look_s = ((0.6, -0.8), (-0.6, -0.8)) if sel > 0.5 else ((0, 0), (0, 0))
    c = R.c
    c.save()
    c.rotate(0)
    moon(R, mx, 990 - 20 * sel, 175 * k_in, t, look=look_m, expr="flat")
    if t >= SUN_IN:
        sun(R, sx_, 960 - 10 * sel, 150 * pop(t, SUN_IN, 0.35, 0.3), t, look=look_s, expr="flat")
    c.restore()
    if t >= SHADES:                       # the Sun's "different outfit"
        k = pop(t, SHADES, 0.25, 0.4)
        c.save()
        c.translate(sx_, 960 - 10 * sel - 150 * 0.12)
        c.scale(k, k)
        for ex in (-0.32, 0.32):
            R.fill(rrect(ex * 150 - 34, -24, 68, 46, 14), INK)
        R.stroke(poly([(-0.32 * 150 + 30, -6), (0.32 * 150 - 30, -6)], False), INK, 8)
        c.restore()
    if t >= SELFIE:                       # the phone, held up by a tiny hand
        k = pop(t, SELFIE, 0.3, 0.4)
        c.save()
        c.translate(520, 700)
        c.rotate(-10)
        c.scale(k, k)
        ph = rrect(-62, -105, 124, 210, 22)
        R.fill(ph, 0xFF23202E)
        R.stroke(ph, INK, 6)
        R.fill(rrect(-50, -90, 100, 170, 12), 0xFF6E5AB8)
        R.fill(circle(-18, -10, 22), 0xFFE4DEF5)
        R.fill(circle(20, -14, 20), YELLOW)
        c.restore()
        R.stroke(poly([(560, 800), (sx_ - 60, 900)], False), INK, 22)
        R.stroke(poly([(560, 800), (sx_ - 60, 900)], False), YELLOW, 12)
    if t >= SUN_IN + 0.2:
        tag(R, "hyperrealistic", 300, 1230, scale=pop(t, SUN_IN + 0.2, 0.3, 0.4))
    G = glorp_base(t, x=800, y=1235, r=92)
    G.hand = "point"
    G.expr = "grin"
    G.look = (-1, -0.6)
    draw_glorp(R, G)
    watermark(R)


def scene_fingers(R, t):                 # his own hand disagrees, live
    R.gradient_bg(drift=0.3)
    R.bokeh(t, 3)
    floor(R)
    n = fingers_at(t)
    G = glorp_base(t, x=380, y=1215, r=160)
    G.hand = "up"
    G.hand_k = 1.45
    G.fingers = n
    G.expr = "grin" if t < T["count"] else "smug"
    G.look = (0.6, -0.8)
    hp = draw_glorp(R, G)
    hx, hy = G.x + hp[0], G.y + hp[1]
    last = max([t0 for t0, k in FINGERS if t >= t0 and t0 > 0] + [0])
    sc = pop(t, last, 0.25, 0.6) if last > 0 else 1.0
    R.text(f"({n})", hx + 240, hy + 20, "comic", 120, WHITE, INK, 14, scale=sc)
    watermark(R)


# penguin crowd: (x, feet y, sign side, sign) — signs stay inside x 60..880; back rows have no signs
PEN_GRID = [
    (110, 1050, 1, "no."), (330, 1050, 1, "Wednesday was us"), (650, 1060, 0, None), (850, 1050, -1, "no.o"),
    (120, 1265, 1, "sourse?"), (860, 1265, -1, "hello?"),
    (80, 1470, 0, None), (300, 1490, 0, None), (760, 1490, 0, None), (980, 1470, 0, None),
    (180, 1680, 0, None), (540, 1700, 0, None), (880, 1680, 0, None),
]
PEN_POP = {i: PEN_T0 + 1.9 * (k / len(PEN_GRID)) ** 0.8 for k, i in
           enumerate([3, 0, 7, 10, 5, 1, 8, 12, 2, 4, 11, 6, 9])}


def penguin_crowd(R, t, flip_t=None):
    for i, (x, y, side, txt) in enumerate(PEN_GRID):
        t0 = PEN_POP[i]
        if t < t0:
            continue
        s = 0.62 * pop(t, t0, 0.3, 0.2)
        flip = 1.0
        if txt and flip_t is not None:
            tf = flip_t + 0.03 * i
            if t >= tf:
                txt = "we can."
            if abs(t - tf) < 0.15:
                flip = flip_val(t, tf)
        heads = 2 if i == 5 else 1           # the AI fused two penguins (hidden detail)
        penguin(R, x, y, s, t + i, look=(0.5 if x < 540 else -0.5), sign_text=txt, flip=flip,
                blink=blink(t, i * 0.37), heads=heads, sign_size=74 if txt != "Wednesday was us" else 58,
                bob=False, sign_side=side or 1)


def scene_penguins(R, t):                # the picture outnumbers him
    R.gradient_bg(drift=0.6)
    floor(R)
    G = glorp_base(t, x=540, y=1215, r=140)
    G.hand = "none"
    G.expr = "grin" if t < SIGN_FLIPS["wecan"] else "worried"
    G.sweat = 0.4 if t >= SIGN_FLIPS["wecan"] + 0.3 else 0.0
    G.look = (-0.4, -0.3)
    penguin_crowd(R, t, flip_t=SIGN_FLIPS["wecan"])
    draw_glorp(R, G)
    watermark(R)


def scene_pressure(R, t):                # "I am calm." / "This video is not AI."
    R.gradient_bg(drift=0.9)
    R.bokeh(t, 5)
    floor(R)
    G = glorp_base(t, x=600, y=1090, r=215)
    G.hand = "up" if t >= W_("calm", 0.5) else "none"
    G.side = -1
    G.hand_k = 1.0
    G.fingers = fingers_at(t)
    G.expr = "worried"
    G.sweat = lerp(0.6, 1.0, prog(t, T["calm"], E["notai"]))
    G.look = (0.1, -0.2)
    hp = draw_glorp(R, G)
    if G.hand == "up":
        last = max([t0 for t0, k in FINGERS if t >= t0 and t0 > 0] + [0])
        R.text(f"({G.fingers})", G.x + hp[0] - 150, G.y + hp[1] + 90, "comic", 96, WHITE, INK, 12,
               scale=pop(t, last, 0.25, 0.6))
    u = ease_in_out(prog(t, *WM_GROW))
    watermark(R, lerp(0.3, 0.62, u), lerp(1.0, 2.0, u), y=lerp(1190, 1050, u))


def scene_shark(R, t):                   # the drop: one true fact
    found = t >= T["warn"]
    R.gradient_bg(SEA0, VIOLET if t < BAR_FULL[1] else 0xFF5B3A9A, SEA1)
    R.bokeh(t, 7, 7, 0.14)
    floor(R, 1330, 0xFF7FD6E8)
    u = ease_out(prog(t, T["shark"] + 0.3, T["shark"] + 1.1))
    shark(R, lerp(1500, 690, u), 960, 1.15, t,
          nod=(math.sin((t - T["what"]) * 6) * 0.5 if T["what"] <= t < T["what"] + 1.2 else 0))
    st = W_("shark", 0.8)
    if t >= st:
        sapling(R, 190, 1235, 1.8 * pop(t, st, 0.3, 0.2), t)
    if E["shark"] + 0.15 <= t < T["warn"]:   # the card is not melting
        k = pop(t, E["shark"] + 0.15, 0.3, 0.5)
        c = R.c
        c.save()
        c.translate(820, 800)
        c.scale(k, k)
        R.fill(circle(0, 0, 50), GREEN)
        R.stroke(circle(0, 0, 50), INK, 6)
        R.stroke(poly([(-22, 2), (-6, 20), (24, -18)], False), INK, 12)
        c.restore()
        R.text("(not melting)", 640, 880, "comic", 58, WHITE, INK, 10, rot=-4, scale=k)
    G = glorp_base(t, x=850, y=1215, r=95)
    G.hand = "none"
    G.expr = "worried"
    if t >= T["what"]:
        G.expr = "shock"
    if t >= T["wasreal"]:
        G.expr = "panic"
        G.melt = ease_in_out(prog(t, T["wasreal"], E["nobody"]))
    G.sweat = 0.6
    G.look = (-0.8, -0.6)
    if t < T["shark"] + 0.3:              # he starts big and shrinks into the corner as the shark arrives
        v = ease_in_out(prog(t, S_SHARK, T["shark"] + 0.3))
        G.x, G.y, G.r = lerp(600, 850, v), lerp(1090, 1215, v), lerp(215, 95, v)
    draw_glorp(R, G)
    if t >= T["what"]:                    # the numbers, on screen only
        k = pop(t, T["what"] + 0.1, 0.3, 0.5)
        R.text("first trees:", 190, 950, "comic", 50, WHITE, INK, 9, rot=-3, scale=k)
        R.text("~385M yrs ago", 190, 1008, "comic", 50, WHITE, INK, 9, rot=-3, scale=k)
        k = pop(t, T["what"] + 0.35, 0.3, 0.5)
        R.text("first sharks:", 470, 1160, "comic", 54, YELLOW, INK, 9, rot=2, scale=k)
        R.text("~450M yrs ago", 470, 1222, "comic", 54, YELLOW, INK, 9, rot=2, scale=k)
    watermark(R, text="AI GENERATED (don't trust me)" if found else "AI GENERATED (trust me)")


def scene_reset(R, t):                   # reality reset, the button, the loop
    txt = "it was thursday."
    if SIGN_FLIPS["hecant"] <= t < SIGN_FLIPS["thursday"]:
        txt = "he can't."
    melt = 1.0 - ease_out_back(prog(t, S_RESET, S_RESET + 0.45), 1.5)
    if t >= T["again"]:                   # "a real one this time": he starts to melt (he is lying)
        melt = 0.55 * ease_in(prog(t, W_("again", 0.4), LOOP_SNAP))
    if t >= LOOP_SNAP:
        melt = 0.0
    pen_x = lerp(1250, 760, ease_out(prog(t, S_RESET + 0.15, S_RESET + 0.8)))
    host_shot(R, t, txt, any_flip(t, ("hecant", "thursday")), melt=melt, fingers=fingers_at(t), pen_x=pen_x)
    k_mark, a_mark = 1.0, 0.3
    if T["trust"] <= t < T["again"]:
        u = math.sin(math.pi * prog(t, T["trust"], T["again"]))
        a_mark, k_mark = 0.3 + 0.3 * u, 1 + 0.12 * u
    watermark(R, a_mark, k_mark)
    if T["comment"] <= t < T["trust"]:
        tag(R, "comments >>", 700, 760, YELLOW, rot=-5, size=50, scale=pop(t, T["comment"] + 0.3, 0.3, 0.4))


SCENES = [(0.0, S_MOON, scene_open), (S_MOON, S_FING, scene_moon), (S_FING, S_PENG, scene_fingers),
          (S_PENG, S_PRESS, scene_penguins), (S_PRESS, S_SHARK, scene_pressure), (S_SHARK, S_RESET, scene_shark),
          (S_RESET, DURATION + 0.01, scene_reset)]


def draw_frame(R, t):
    for a, b, fn in SCENES:
        if a <= t < b:
            fn(R, t)
            break
    hud(R, t)
    for cap in CAPTIONS:
        if cap.start <= t < cap.end and cap is CAPTIONS[-1]:
            # the loop line melts: he is lying again
            cap.melt = lambda tt: 0.0
            _draw_loop_line(R, t, cap)
            continue
        cap.draw(R, t)
    LOOP_CARD.draw(R, t)


def _draw_loop_line(R, t, cap):
    """'Okay. A real one this time.' drawn as a big white card that melts as he says it."""
    from slop_engine import _render_block, draw_melting
    lines = ["Okay. A real one", "this time."]
    key = ("loopline",)
    if key not in R.A.cache:
        R.A.cache[key] = _render_block(R.A, lines, 104, WHITE)
    img, hgt = R.A.cache[key]
    m = 1.1 * ease_in(prog(t, W_("again", 0.35), LOOP_SNAP))
    k = pop(t, T["again"], 0.22, 0.7)
    c = R.c
    c.save()
    c.translate(520, FACT_Y + hgt / 2)
    c.scale(k, k)
    c.translate(-W / 2, -hgt / 2)
    draw_melting(R, img, 0, 0, m, seed=5)
    c.restore()
