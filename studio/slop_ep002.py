"""SLOP SHOP #002 — "SLOP NEWS: The Moon Has Been Sold"   61.94 s at 124 BPM (32 bars), loops.

News parody, YouTube-Poop cut. Glorp anchors SLOP NEWS. Breaking: the Moon has been sold, for three
dollars and a hug (the hug is pending). Frame 0: the Moon crammed into the studio window, wearing a SOLD
tag. Every report escalates the one premise, and each one is caused by the last:
  the buyer, a tech boss (a USB stick in a vest), makes it better: smaller, square square SQUARE ("fits
  the box"), full moon premium, half moon free with ads, fine print at double speed ("werewolves may
  experience buffering") -> silent cutaway: a werewolf, buffering ->
  no Moon, so the Minister of Night (a loaf of bread, Grand Duchy of Flurb, a sing-song invented accent)
  puts night on Thursday ("bring a lamp"); Thursday has not been informed (a calendar page: "Night? I barely
  do afternoons! What? what? WHAT?") -> so an influencer (a ring light with a face) becomes the Moon
  ("link in my crater") -> a toaster who has seen things (invented "toaster" accent): "I was there, in
  eighty-seven. They sold the Sun once. I've been doing its job since." (the toast pops, charred) ->
  UPDATE: the hug bounced (bounced bounced BOUNCED): sale cancelled, the Moon is now the buyer ->
  on the beat it buys the tech boss, Thursday, the toaster, and this channel (SOLD slams on the screen) ->
  the Moon leans out of the window: "Hug... pending." -> it hugs Glorp; each squeeze squeezes out a "B-";
  the tag flips to HUG: RECEIVED (1/1) -> the loop: "B- b- b- b-" + frame 0 "Breaking! The Moon has been sold."
Hidden details: the price tag on frame 0 says "seller: the moon" (the Moon sold itself); the ticker on
frame 0 already says "MOON OPEN TO OFFERS"; Glorp's finger count drops at every return to the desk (9, 8, 7).
Running gags: GENERATING NEWS... 99% (never 100), the AI GENERATED (trust me) watermark.

Guardrails: every character is invented (no real person, brand, country, flag or accent: all voices use the
same Kokoro US-English locale, the only "accents" are a vibrato and a toaster filter); the "news" is
impossible on its face (a pink blob, a bread minister, a talking calendar), so it cannot pass for real news;
no real fact is claimed. No strobe: at most two cuts a second, no flashes, the RGB split keeps the frame's
brightness, the werewolf's picture-skip only moves a small shape.

Built against an independent review (26 Oct 2026): bridges cut ("X has responded"), the werewolf said once,
lines chained, the egg (too close to a real platform's avatar) replaced by a USB stick, ticker spoilers
removed, tag flip as the final punchline, bigger hidden detail, safe zone fixes.

Timing: python3 slop_voice.py slop_ep002 measure -> out/slop_ep002_durs.json (every line and part);
the timeline is laid out from it: lines marked CUT start on the next half beat (cuts on the beat), and
the pauses are scaled so the last "B-" lands 0.3 s before the end.
"""
import math
import os
import sys

import numpy as np
import skia

from slop_engine import *  # noqa: F401,F403
from slop_ytp import *  # noqa: F401,F403
import slop_voice as SV

EPNAME = "slop_ep002"
BPM = 124
BEAT = 60.0 / BPM
HALF = BEAT / 2
BAR = 4 * BEAT
DURATION = 32 * BAR            # 61.94 s
TRANSPOSE = 3                  # E-flat: the news jingle
CHORDS = [([36, 48, 52, 55], 36), ([45, 48, 52, 57], 45), ([41, 48, 53, 57], 41), ([43, 50, 55, 59], 43)]
MOTIFS = [
    [(0, 5, 1), (1, 5, 1), (2, 7, 2), (4, 4, 1), (5, 5, 1), (6, 2, 2)],
    [(0, 2, 1), (1, 4, 1), (2, 5, 2), (4, 7, 2), (6, 8, 2)],
    [(0, 5, 1), (1, 5, 1), (2, 7, 2), (4, 8, 1), (5, 7, 1), (6, 5, 2)],
    [(0, 4, 1), (1, 2, 1), (2, 1, 1), (3, 0, 1), (4, 0, 4)],
]

# ------------------------------------------------------------------ cast (casting: slop_casting.py)
# Every voice is a US-English Kokoro voice: no real accent anywhere. The minister's "Flurb" accent is a
# slow vibrato, the toaster's is a small-chrome-box filter.
WOB = [["wobble", 1.8, 2.3]]
CASTS = {
    "A": {"G": ("am_michael", 1.12, {"semitones": 1.0}), "T": ("am_fenrir", 1.06, {"semitones": 0.0}),
          "M": ("am_eric", 0.94, {"semitones": -1.5, "chain": WOB}),
          "I": ("af_bella", 1.16, {"semitones": 1.5}), "X": ("am_onyx", 0.86, {"semitones": -2.0, "chain": ["toaster"]}),
          "H": ("af_sky", 1.12, {"semitones": 4.0}), "L": ("am_puck", 0.8, {"semitones": -7.0})},
    "B": {"G": ("am_puck", 1.12, {"semitones": 2.0}), "T": ("am_eric", 1.05, {"semitones": 0.0}),
          "M": ("am_michael", 0.94, {"semitones": -1.5, "chain": WOB}),
          "I": ("af_jessica", 1.16, {"semitones": 1.5}), "X": ("am_onyx", 0.86, {"semitones": -2.0, "chain": ["toaster"]}),
          "H": ("af_heart", 1.12, {"semitones": 4.0}), "L": ("am_fenrir", 0.8, {"semitones": -6.0})},
    "C": {"G": ("am_fenrir", 1.12, {"semitones": 1.5}), "T": ("am_michael", 1.05, {"semitones": -1.0}),
          "M": ("am_liam", 0.94, {"semitones": -1.5, "chain": WOB}),
          "I": ("af_sarah", 1.18, {"semitones": 1.0}), "X": ("am_onyx", 0.86, {"semitones": -2.0, "chain": ["toaster"]}),
          "H": ("af_bella", 1.12, {"semitones": 4.0}), "L": ("am_puck", 0.8, {"semitones": -7.0})},
    "D": {"G": ("am_eric", 1.12, {"semitones": 1.5}), "T": ("am_puck", 1.05, {"semitones": 0.0}),
          "M": ("am_fenrir", 0.94, {"semitones": -1.5, "chain": WOB}),
          "I": ("af_nova", 1.16, {"semitones": 1.0}), "X": ("am_michael", 0.84, {"semitones": -3.0, "chain": ["toaster"]}),
          "H": ("af_sky", 1.12, {"semitones": 4.0}), "L": ("am_onyx", 0.8, {"semitones": -5.0})},
}
CAST_CHOICE = os.environ.get("SLOP_CAST", "A")
CAST = CASTS[CAST_CHOICE]
CAST_GAIN = {"G": 1.0, "T": 1.0, "M": 1.0, "I": 0.95, "X": 1.05, "H": 0.85, "L": 1.1}
CASTING_LINES = ["brk", "price", "hug", "better", "square", "night", "what", "iam", "job", "toastq", "pend"]

CUT = True
#   name       who  text or parts                                                                          opts  gap   cut
#   a gap given as ("fixed", s) is not scaled (a silent beat that must keep its length)
LINES_T = [
    ("brk",     "G", [("Breaking!", {"gap": 0.08}), ("The Moon has been sold.", {})], {}, 0.12, False),
    ("price",   "G", "For three dollars.", {}, 0.08, False),
    ("hug",     "G", "And a hug.", {}, 0.45, False),
    ("better",  "T", "We're making the Moon better.", {}, 0.15, CUT),
    ("smaller", "T", "Smaller.", {}, 0.35, False),
    ("square",  "T", [("Square.", {"rep": 2, "rep_st": 2.5, "rep_gap": 0.16, "gap": 0.25}), ("Fits the box.", {})], {}, 0.3, False),
    ("premium", "T", [("And the full moon?", {"gap": 0.12}), ("Premium.", {})], {}, 0.2, False),
    ("ads",     "T", [("Half moon:", {"gap": 0.06}), ("free. With ads.", {})], {}, 0.2, False),
    ("fine",    "T", [("Tides sold separately.", {"tempo": 1.85, "st": 3}),
                      ("Werewolves may experience buffering.", {"tempo": 1.85, "st": 3})], {}, ("fixed", 1.9), False),
    ("nowhere", "G", "Fact: without the Moon, night has nowhere to go.", {}, 0.15, CUT),
    ("night",   "M", [("No Moon? No problem.", {"gap": 0.15}), ("Night is now on Thursday.", {})], {}, 0.2, CUT),
    ("lamp",    "M", "Bring a lamp.", {}, 0.25, False),
    ("noinf",   "M", "Thursday has not been informed.", {}, 0.15, False),
    ("what",    "H", [("Night?", {"gap": 0.1}), ("I barely do afternoons!", {"gap": 0.12}),
                      ("What?", {"rep": 2, "rep_st": 3, "rep_gap": 0.1})], {}, 0.4, CUT),
    ("grwm",    "I", [("Get ready with me...", {"gap": 0.2}), ("to be the Moon.", {})], {}, 0.2, CUT),
    ("round",   "I", "Step one: be round.", {}, 0.25, False),
    ("iam",     "I", "I am literally the Moon now.", {}, 0.3, False),
    ("link",    "I", "Link in my crater.", {}, 0.4, False),
    ("87",      "X", "I was there. In eighty-seven.", {}, 0.3, CUT),
    ("sun",     "X", "They sold the Sun once.", {}, 0.35, False),
    ("job",     "X", "I've been doing its job since.", {}, 0.3, False),
    ("toastq",  "X", "Toast?", {}, 0.5, False),
    ("update",  "G", [("Update:", {"gap": 0.08}), ("the hug", {"gap": 0.14}),
                      ("bounced.", {"rep": 2, "rep_st": 3, "rep_gap": 0.14})], {}, 0.25, CUT),
    ("cancel",  "G", "The sale is cancelled.", {}, 0.1, False),
    ("buyer2",  "G", "The Moon is now the buyer.", {}, 0.55, False),
    ("b1",      "G", "It bought the tech boss.", {}, 0.05, CUT),
    ("b2",      "G", "Thursday.", {}, 0.05, CUT),
    ("b3",      "G", "The toaster.", {}, 0.05, CUT),
    ("b4",      "G", [("And...", {"gap": 0.1}), ("this channel.", {})], {}, 0.3, CUT),
    ("pend",    "L", [("Hug...", {"gap": 0.3}), ("pending.", {})], {}, 0.35, CUT),
    ("bbb",     "G", [("Breaking", {"stutter": 4, "stut": 0.085, "stut_gap": 0.17, "stutter_only": True})], {}, 0.0, False),
]
LINES = [(w, s, o) for (_, w, s, o, _, _) in LINES_T]
NAMES = [l[0] for l in LINES_T]

# ------------------------------------------------------------------ timeline from the measured voice
sys.modules.setdefault(EPNAME, sys.modules[__name__])
_D = SV.load_durs(EPNAME)
if _D:
    DURS, SPANS = _D["durs"], _D["spans"]
else:
    DURS, SPANS = [], []
    for (_, _, s, _, _, _) in LINES_T:
        parts = [s] if isinstance(s, str) else [p[0] for p in s]
        sp, tt = [], 0.0
        for p in parts:
            d = max(0.45, len(p.split()) * 0.34)
            sp.append((tt, tt + d))
            tt += d + 0.1
        DURS.append(tt)
        SPANS.append(sp)
LEAD_IN = 0.04
TAIL = 0.32


def _layout(k):
    T_, E_ = {}, {}
    t = LEAD_IN
    for (name, _, _, _, gap, cut), d in zip(LINES_T, DURS):
        if cut:
            t = math.ceil((t - 0.02) / HALF) * HALF
        T_[name], E_[name] = t, t + d
        t += d + (gap[1] if isinstance(gap, tuple) else gap * k)
    return T_, E_


_lo, _hi = 0.05, 4.0
for _ in range(50):
    _k = (_lo + _hi) / 2
    _T, _E = _layout(_k)
    if _E["bbb"] + TAIL > DURATION:
        _hi = _k
    else:
        _lo = _k
_k = _lo
T, E = _layout(_k)
NARRATION = [(T[n], w, s, o) for (n, w, s, o, _, _) in LINES_T]
SP = {n: [(T[n] + a, T[n] + b) for (a, b) in sp] for n, sp in zip(NAMES, SPANS)}


def P(name, i=0):
    return SP[name][i][0]


def PE(name, i=0):
    return SP[name][i][1]


def W_(name, frac):
    return T[name] + (E[name] - T[name]) * frac


def reps(name, part=0, n=3):
    """Start times of a part said n times (rep): its span split evenly (close enough to sync a cut)."""
    a, b = SP[name][part]
    return [a + (b - a) * i / n for i in range(n)]


# ------------------------------------------------------------------ scenes (start, end)
S_BOSS = T["better"]
S_WOLF = math.ceil((E["fine"] + 0.2) / HALF) * HALF       # silent cutaway, on the beat
S_NOW = T["nowhere"]
S_MIN = T["night"]
S_THU = T["what"]
S_INF = T["grwm"]
S_TOAST = T["87"]
S_UPD = T["update"]
S_B1, S_B2, S_B3, S_B4 = T["b1"], T["b2"], T["b3"], T["b4"]
S_HUG = T["pend"]
HUG_T = PE("pend", 1) + 0.05                 # the arms close
LOOP_SNAP = DURATION - 0.2                   # the world snaps back to frame 0
SQUEEZES = [T["bbb"] + i * (0.085 + 0.17) for i in range(4)]
FLASHBACK = (T["sun"] - 0.1, E["sun"] + 0.2)          # sepia flashback (held, not flashed)
TOAST_UP = W_("job", 0.75)
BOUNCES = reps("update", 2, 3)
SQUARES = reps("square", 0, 3)
WHATS = reps("what", 2, 3)
TURN_T = W_("buyer2", 0.45)                  # the Moon turns to camera
HOWL = S_WOLF + 0.35

# ------------------------------------------------------------------ captions (mirror the voice)
FACT_Y = 455
SUB_Y = 1356


def CS(name, segs, end=None, **kw):
    return Caption(segs[0][0], end or E[name] + 0.12, segs, "sub", y=SUB_Y, size=kw.pop("size", 76), **kw)


CAPTIONS = [
    Caption(0.0, T["price"], [(0.0, "The Moon has / been *sold.*")], "fact", FACT_Y, size=96, label="BREAKING:"),
    CS("price", [(T["price"], "For *three dollars.*")]),
    CS("hug", [(T["hug"], "And a *hug.*")], end=S_BOSS),
    CS("better", [(T["better"], "We're making / the Moon *better.*")]),
    CS("smaller", [(T["smaller"], "*Smaller.*")], end=T["square"]),
    CS("square", [(SQUARES[0], "Square."), (SQUARES[1], "*Square.*"), (SQUARES[2], "*SQUARE.* /"),
                  (P("square", 1), "Fits the *box.*")], end=T["premium"]),
    CS("premium", [(P("premium", 0), "And the full moon? /"), (P("premium", 1), "*Premium.*")], end=T["ads"]),
    CS("ads", [(P("ads", 0), "Half moon: /"), (P("ads", 1), "free. *With ads.*")], end=P("fine", 0)),
    CS("fine", [(P("fine", 0), "Tides sold separately.")], end=P("fine", 1), size=64),
    CS("fine", [(P("fine", 1), "Werewolves may experience / *buffering.*")], end=S_WOLF, size=64),
    Caption(S_WOLF, S_NOW, [(S_WOLF, "Werewolves are / *buffering.*")], "fact", FACT_Y, size=96, label="FACT:"),
    CS("nowhere", [(T["nowhere"], "Without the Moon, / night has *nowhere to go.*")], end=S_MIN),
    CS("night", [(P("night", 0), "No Moon? *No problem.*")], end=P("night", 1)),
    CS("night", [(P("night", 1), "Night is now / on *Thursday.*")]),
    CS("lamp", [(T["lamp"], "Bring a *lamp.*")], end=T["noinf"]),
    CS("noinf", [(T["noinf"], "Thursday has not / been *informed.*")], end=S_THU),
    CS("what", [(P("what", 0), "Night? /"), (P("what", 1), "I barely do *afternoons!*")], end=WHATS[0]),
    CS("what", [(WHATS[0], "What?"), (WHATS[1], "*what?*"), (WHATS[2], "*WHAT?*")], end=S_INF, size=96),
    CS("grwm", [(P("grwm", 0), "Get ready with me... /"), (P("grwm", 1), "to be the *Moon.*")]),
    CS("round", [(T["round"], "Step one: / be *round.*")], end=T["iam"]),
    CS("iam", [(T["iam"], "I am literally / the *Moon* now.")]),
    CS("link", [(T["link"], "Link in my *crater.*")], end=S_TOAST),
    CS("87", [(T["87"], "I was there. / In *'87.*")]),
    CS("sun", [(T["sun"], "They sold / the *Sun* once.")]),
    CS("job", [(T["job"], "I've been doing / its *job* since.")], end=T["toastq"]),
    CS("toastq", [(T["toastq"], "*Toast?*")], end=S_UPD),
    CS("update", [(P("update", 0), "Update: the hug... /"), (BOUNCES[0], "bounced."), (BOUNCES[1], "*bounced.*"),
                  (BOUNCES[2], "*BOUNCED.*")]),
    CS("cancel", [(T["cancel"], "The sale is *cancelled.*")], end=T["buyer2"]),
    Caption(T["buyer2"], S_B1, [(T["buyer2"], "The Moon is now / the *buyer.*")], "fact", FACT_Y, size=96, label="UPDATE:"),
    CS("b1", [(T["b1"], "It bought / the *tech boss.*")], end=S_B2),
    CS("b2", [(T["b2"], "*Thursday.*")], end=S_B3),
    CS("b3", [(T["b3"], "The *toaster.*")], end=S_B4),
    CS("b4", [(P("b4", 0), "And... /"), (P("b4", 1), "*this channel.*")], end=S_HUG),
    CS("pend", [(P("pend", 0), "Hug... /"), (P("pend", 1), "*pending.*")], end=T["bbb"]),
    CS("bbb", [(SQUEEZES[0], "B-"), (SQUEEZES[1], "b-"), (SQUEEZES[2], "b-"), (SQUEEZES[3], "b-")], end=LOOP_SNAP, size=96),
]
LOOP_CARD = Caption(LOOP_SNAP, DURATION + 1, [(0.0, "The Moon has / been *sold.*")], "fact", FACT_Y, size=96,
                    label="BREAKING:")
SUBTITLE_EXTRAS = [
    (0.0, S_BOSS, "[tag: SOLD — $3 + 1 hug (pending)]"),
    (T["premium"], S_WOLF, "[slide: FULL MOON — $9.99/month]"),
    (S_WOLF + 0.4, S_NOW, "[BUFFERING 12%]"),
    (T["night"], S_THU, "[MINISTER OF NIGHT — Grand Duchy of Flurb]"),
    (T["87"], S_UPD, "[TOASTER — has seen things]"),
    (HUG_T + 0.6, LOOP_SNAP, "[tag: HUG RECEIVED (1/1)]"),
]

# ------------------------------------------------------------------ camera & time (the YTP layer)
PUNCH = []
PUNCH += [(PE("brk", 1) - 0.25, 0.10, 690, 900, 0.35)]                    # "sold"
PUNCH += [(T["hug"] + 0.25, 0.22, 560, 1000, 0.45)]                        # "hug" -> the tag
PUNCH += [(t, 0.12 + 0.1 * i, 485, 760, 0.4) for i, t in enumerate(SQUARES)]
PUNCH += [(P("premium", 1), 0.14, 485, 760, 0.4), (P("ads", 1), 0.1, 420, 790, 0.35)]
PUNCH += [(HOWL, 0.12, 330, 800, 0.4)]
PUNCH += [(t, 0.10 + 0.12 * i, 480, 880, 0.35) for i, t in enumerate(WHATS)]
PUNCH += [(t, 0.10 + 0.08 * i, 540, 1150, 0.35) for i, t in enumerate(BOUNCES)]
PUNCH += [(S_B1, 0.16, 520, 900, 0.4), (S_B2, 0.16, 480, 880, 0.4), (S_B3, 0.16, 470, 1000, 0.4),
          (P("b4", 1), 0.22, 540, 900, 0.5)]
PUNCH += [(t, 0.06, 360, 1000, 0.22) for t in SQUEEZES]
PUNCH += [(TOAST_UP, 0.12, 470, 900, 0.4)]
HOLDS = [
    (T["smaller"] + 0.15, SQUARES[0] - 0.02, 3.0, 485, 760),            # crash zoom on the tiny moon
    (TURN_T, S_B1, 0.55, 690, 900),                                     # the Moon turns: crash zoom, music stops
    (T["link"] + 0.2, S_TOAST, 0.35, 480, 760),
    (HUG_T, LOOP_SNAP, 0.22, 430, 900),                                 # the hug fills the frame
]
SHAKES = [(P("fine", 0), PE("fine", 1), 5), (WHATS[2], WHATS[2] + 0.45, 12), (P("b4", 1), P("b4", 1) + 0.4, 14),
          (HUG_T, HUG_T + 0.3, 10)]
TILTS = [(BOUNCES[2], -4, 0.4), (S_B2, 3, 0.3), (S_B3, -3, 0.3)]
CAM = Cam(PUNCH, HOLDS, SHAKES, TILTS)
STUTTERS = [(HOWL + 0.3, HOWL + 0.9, 0.15),                     # the werewolf buffers (visual skip)
            (BOUNCES[1], BOUNCES[1] + 0.3, 0.1)]
FREEZES = [(TOAST_UP + 0.3, TOAST_UP + 0.75)]
SPLITS = [(P("fine", 0), PE("fine", 1), 7), (BOUNCES[0], E["update"], 9), (P("b4", 1), P("b4", 1) + 0.35, 10)]
FRY = [(WHATS[2], WHATS[2] + 0.5, 0.8), (P("b4", 1), S_HUG, 0.5)]

# ------------------------------------------------------------------ sound
SFX = [
    (0.0, "boop", 0), (PE("brk", 1) - 0.25, "boom", 0), (P("price", 0) + 0.5, "kaching", 0),
    (T["hug"] + 0.3, "squeak", 0), (E["hug"] + 0.1, "boop", 5),
    (S_BOSS - 0.05, "whoosh", 0), (S_BOSS + 0.05, "mictap", 0), (T["smaller"], "shrink", 0),
    (T["smaller"] + 0.15, "scratch", 0),
] + [(t, "pop", 2 * i + 2) for i, t in enumerate(SQUARES)] + [
    (P("square", 1), "tap", 0), (P("premium", 1), "kaching", 0), (P("ads", 1), "stamp", 0),
    (P("fine", 0) - 0.05, "rewind", 0),
    (S_WOLF, "whoosh_down", 0), (HOWL, "howl", 0), (HOWL + 0.45, "skip", 0), (HOWL + 0.75, "skip", 0),
    (S_NOW, "bonk", 0), (W_("nowhere", 0.6), "slide_down", 0),
    (S_MIN - 0.05, "whoosh", 0), (S_MIN + 0.05, "crackle", 0), (PE("night", 1) - 0.2, "slide_up", 0),
    (T["lamp"] + 0.2, "click", 0), (T["noinf"] + 0.5, "crackle", 1),
] + [(t, "boing_up", 0) for t in WHATS[2:]] + [(t, "pop", 6 + i) for i, t in enumerate(WHATS[:2])] + [
    (S_INF, "sparkle", 0), (T["iam"] + 0.4, "riser_fast", 0), (T["link"] + 0.1, "click", 0),
    (S_TOAST, "whoosh_down", 0), (S_TOAST + 0.1, "creak", 0), (FLASHBACK[0], "rumble", 0),
    (TOAST_UP - 0.05, "ding", 0), (TOAST_UP, "boing_up", 0), (E["toastq"] + 0.05, "wahwah", 0),
    (S_UPD - 0.05, "scratch", 0),
] + [(t, "boing_down" if i < 2 else "boing_up", 0) for i, t in enumerate(BOUNCES)] + [
    (T["cancel"] + 0.6, "stamp", 0), (TURN_T, "boom", 0),
    (S_B1, "stamp", 0), (S_B2, "stamp", 1), (S_B3, "stamp", 2), (P("b4", 1), "slam", 0), (P("b4", 1) + 0.1, "kaching", 0),
    (S_HUG, "slide_down", 0), (HUG_T, "squeak", 3),
] + [(t, "squeak", i) for i, t in enumerate(SQUEEZES)] + [(SQUEEZES[3] + 0.2, "kaching", 0), (LOOP_SNAP, "pop", 0)]
MUSIC_CUTS = [(TURN_T, S_B1)]
BEAT_REPEATS = [(SQUARES[1] - 0.06, HALF / 2, 2), (WHATS[1] - 0.06, HALF / 2, 2), (BOUNCES[1] - 0.06, HALF / 2, 2)]


def music_sections(t):
    s = {"drums": 1, "bass": 1, "keys": 1, "lead": 1}
    if t < S_BOSS:
        s.update(var=0)
    elif t < S_WOLF:
        s.update(var=1, drums=2)
    elif t < S_NOW:
        s.update(lead=0, drums=1)
    elif t < S_TOAST:
        s.update(var=2)
    elif t < S_UPD:
        s.update(lead=0, drums=1, keys=1)
    elif t < S_B1:
        s.update(var=3, drums=2)
    elif t < S_HUG:
        s.update(drums=2, glock=1, var=0)
    else:
        s.update(lead=0, drums=0, bass=1, keys=1)
    return s


# ------------------------------------------------------------------ mouths
_ENV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", f"{EPNAME}_env.npz")
ENVS = dict(np.load(_ENV)) if os.path.exists(_ENV) else {}
WORD_TIMES = sorted(T.values())


def talk(t, who):
    e = ENVS.get(who)
    if e is not None:
        i = int(t * FPS)
        return float(clamp01((e[i] - 0.05) * 2.2)) if 0 <= i < len(e) else 0.0
    for (n, w, *_) in LINES_T:
        if w == who and T[n] <= t < E[n]:
            return 0.5 + 0.5 * math.sin(t * 28)
    return 0.0


def blink(t, off=0.0):
    return ((t + 1.3 + off) % 3.7) < 0.1 and 0.3 < t < DURATION - 0.4


# overlays drawn outside the camera (lower thirds stay put while the picture punches)
OVERLAY = []


def lower(name, role, k, y=1205):
    OVERLAY.append((name, role, k, y))


# ------------------------------------------------------------------ the desk shot (frame 0 lives here)
WIN = (480, 690, 410, 420)
MOON_HOME = (690, 905, 212)          # crammed into the window: too big for it


def fingers_at(t):
    return 9 if (t < S_UPD or t >= LOOP_SNAP) else (8 if t < S_B4 else 7)


def glorp_desk(t, **kw):
    G = GlorpState(x=270, y=1005, r=172)
    G.wobble = t
    G.talk = talk(t, "G")
    G.blink = blink(t)
    G.hand = "up"
    G.hand_k = 0.72
    G.side = -1
    G.fingers = fingers_at(t)
    G.look = (0.6, -0.2)
    G.__dict__.update(kw)
    return G


def ticker_items(t):
    if t >= LOOP_SNAP:
        t = 0.0
    items = ["HUG: PENDING", "MOON SOLD FOR $3", "MOON: NO COMMENT", "MOON OPEN TO OFFERS"]
    if t >= S_WOLF:
        items += ["MOON NOW SQUARE", "FULL MOON $9.99"]
    if t >= S_THU:
        items += ["NIGHT MOVED TO THURSDAY", "BRING A LAMP"]
    if t >= S_UPD:
        items = ["HUG: BOUNCED"] + items[1:]
    return items


def desk_shot(R, t, glorp=None, tag_stamp=None, tag_k=0.0, heart_t=None, moon_out=0.0,
              moon_look=(0, 0), moon_expr="smile", moon_talk=0.0, arms=0.0, reach=0.0, show_ticker=True,
              hug_tag=None):
    news_bg(R, t)
    wx, wy, ww, wh = WIN
    mx, my, mr = MOON_HOME
    inside_moon = moon_out <= 0.0

    def inside(R_):
        if inside_moon:
            R_.c.save()
            R_.c.translate(mx, my)
            R_.c.scale(1.0, 0.94)           # squashed against the glass
            R_.c.translate(-mx, -my)
            moon_body(R_, mx, my + math.sin(t * 1.4) * 5, mr, t, look=moon_look, expr=moon_expr, talk=moon_talk,
                      blink=blink(t, 2.0))
            R_.c.restore()
    window(R, wx, wy, ww, wh, t, inside)
    if inside_moon and tag_stamp != "hide":
        price_tag(R, 455, 1025, ["SOLD", "$3 + 1 hug", "(pending)"], rot=-8, s=0.92, tiny="seller: the moon",
                  string_to=(mx - 120, my + 110), stamp=tag_stamp, stamp_k=tag_k)
    G = glorp or glorp_desk(t)
    u = ease_in_out(moon_out)
    mpos = (lerp(mx, 610, u), lerp(my, 740, u), lerp(mr, 225, u))
    if not inside_moon:
        # the Moon leans out of the window, huge, arms first
        moon_body(R, *mpos, t, look=moon_look, expr=moon_expr, talk=moon_talk, blink=False)
        if arms > 0:
            _hug_arms(R, t, mpos, G, arms, reach, "far")
    draw_glorp(R, G)
    if not inside_moon and arms > 0:
        _hug_arms(R, t, mpos, G, arms, reach, "near")
    desk(R)
    if hug_tag:
        lines, stamp, sk = hug_tag
        price_tag(R, mpos[0] - 20, mpos[1] + mpos[2] + 40, lines, rot=6, s=0.85, string_to=(mpos[0] + 30, mpos[1] + mpos[2] - 10),
                  stamp=stamp, stamp_k=sk)
    if heart_t is not None:
        _bouncing_heart(R, t, heart_t)
    if show_ticker:
        ticker(R, t - DURATION if t >= LOOP_SNAP else t, ticker_items(t))


def _hug_arms(R, t, moon, G, arms, reach, layer="near"):
    """The Moon's arms: the far one goes behind Glorp (hand peeks out on his left), the near one
    wraps his belly, under his face."""
    mx, my, mr = moon
    gx, gy, gr = G.x, G.y, G.r
    sgn = 1 if layer == "far" else -1
    sx, sy = mx + sgn * mr * 0.78, my + mr * 0.45
    if sgn > 0:
        ex, ey = lerp(sx + 120, gx - gr * 1.02, reach), lerp(sy + 160, gy + gr * 0.15, reach)
        cxp, cyp = lerp(sx + 200, gx + gr * 0.2, reach), lerp(sy + 60, gy + gr * 1.3, reach)
    else:
        ex, ey = lerp(sx - 120, gx + gr * 0.25, reach), lerp(sy + 160, gy + gr * 0.62, reach)
        cxp, cyp = lerp(sx - 200, gx + gr * 0.9, reach), lerp(sy + 40, gy + gr * 0.75, reach)
    p = skia.Path()
    p.moveTo(sx, sy)
    p.quadTo(cxp, cyp, ex, ey)
    R.stroke(p, INK, 72 * arms)
    R.stroke(p, MOON1, 54 * arms)
    R.glossy(circle(ex, ey, 48 * arms), ex, ey, 48 * arms, MOON0, MOON1, MOON2, INK, 6)


def _bouncing_heart(R, t, t0):
    """The hug bounces like a rubber ball, three times, across the desk."""
    x0, x1 = 820, 160
    u = prog(t, BOUNCES[0] - 0.3, E["update"] + 0.1)
    x = lerp(x0, x1, u)
    y, sq = 1080, 1.0
    for i, b in enumerate(BOUNCES):
        h = prog(t, b, b + 0.42)
        if 0 < h < 1:
            y = 1080 - math.sin(math.pi * h) * (300 - 60 * i)
            if h < 0.1 or h > 0.92:
                sq = 0.7
    if BOUNCES[0] - 0.3 <= t < E["update"] + 0.4:
        heart(R, x, y, 0.85, rot=-u * 220, sq=sq)


# ------------------------------------------------------------------ scenes
def scene_desk_open(R, t):                       # 0 -> S_BOSS (and the loop's last frames)
    G = glorp_desk(t)
    G.expr = "grin"
    desk_shot(R, t, glorp=G)
    if T["hug"] + 0.25 <= t < S_BOSS:
        k = pop(t, T["hug"] + 0.3, 0.3, 0.4)
        heart(R, 840, 1010, 0.6 * k, rot=12)
        tag(R, "pending", 800, 1092, YELLOW, rot=6, size=40, scale=k)


def _slide(t):
    crash = T["smaller"] + 0.15 <= t < SQUARES[0]

    def draw(R, cx, cy):
        if not crash:
            R.text("MOON 2.0", cx, cy - 190, "bungee", 76, WHITE, None)
        r, sq, slip = 150, 0.0, 0.0
        if t >= T["smaller"]:
            r = lerp(150, 46, ease_in_out(prog(t, T["smaller"], T["smaller"] + 0.3)))
        if t >= SQUARES[0]:
            i = min(2, sum(1 for s in SQUARES if t >= s) - 1)
            r = lerp(46, 150, ease_out_back(prog(t, SQUARES[0], SQUARES[0] + 0.3)))
            sq = [0.38, 0.72, 1.0][i]
            slip = [0.0, 0.15, 0.4][i]
        half = ease_out(prog(t, P("premium", 1) - 0.1, P("premium", 1) + 0.2)) if t >= P("premium", 1) - 0.1 else 0.0
        moon_body(R, cx, cy + 30, r, t, sq=sq, seed=7, eye_slip=slip,
                  expr="smile" if t < T["smaller"] else "flat", look=(0.3, 0.2), half=half)
        if t >= P("square", 1):                       # it fits the box
            k = pop(t, P("square", 1), 0.25, 0.5)
            R.stroke(rrect(cx - 170 * k, cy + 30 - 170 * k, 340 * k, 340 * k, 8), YELLOW, 8, 0.9)
        if half > 0:
            lock(R, cx + 75, cy + 40, 0.9 * half)
            R.text("FULL MOON: $9.99/mo", cx, cy + 250, "anton", 62, YELLOW, INK, 8, scale=half)
        if t >= P("ads", 1):                          # the free half comes with an ad
            k = pop(t, P("ads", 1), 0.25, 0.3)
            R.c.save()
            R.c.translate(cx - 70, cy + 30)
            R.c.rotate(-8)
            R.c.scale(k, k)
            R.fill(rrect(-150, -55, 300, 110, 14), YELLOW)
            R.stroke(rrect(-150, -55, 300, 110, 14), INK, 6)
            R.text("AD", -80, 22, "bungee", 64, INK, None)
            R.text("skip in 5", 50, 14, "comic", 34, INK, None)
            R.c.restore()
        if T["better"] + 0.3 <= t < T["smaller"]:
            for i, (dx, dy) in enumerate(((-230, -40), (220, -90), (200, 150))):
                star4(R, cx + dx, cy + dy, 40 * pop(t, T["better"] + 0.3 + i * 0.12, 0.3, 0.2), YELLOW, 10 * i)
        if P("fine", 0) <= t:                         # the fine print races by
            u = prog(t, P("fine", 0), PE("fine", 1))
            fp = ["tides sold separately", "werewolves may experience buffering", "the moon may buy you back",
                  "no refunds on gravity", "hugs non-transferable"]
            for i, s in enumerate(fp):
                R.text(s, cx + 420 - u * 1500 + i * 60, cy + 205 + (i % 2) * 42, "comic", 38, WHITE, INK, 5,
                       align="left")
    return draw


def scene_boss(R, t):                            # S_BOSS -> S_WOLF
    keynote(R, t, _slide(t))
    fast = P("fine", 0) <= t < E["fine"]
    tk = talk(t, "T")
    tech_boss(R, 700, 1285, 0.72, t, talk=tk if not fast else 0.5 + 0.5 * math.sin(t * 60),
              point=ease_out(prog(t, T["smaller"] - 0.1, T["smaller"] + 0.2)) if t < P("fine", 0) else 0.0)
    lower("TECH BOSS", "bought the Moon", ease_out(prog(t, S_BOSS + 0.2, S_BOSS + 0.45)))


def scene_wolf(R, t):                            # S_WOLF -> S_MIN (silent)
    R.c.drawRect(skia.Rect(0, 0, W, H), R.paint(shader=R.lin(0, 0, 0, H, [0xFF1A1450, 0xFF3B2A8E, 0xFF1A0E4C])))
    rng = np.random.default_rng(21)
    for i in range(40):
        R.fill(circle(rng.uniform(0, W), rng.uniform(250, 1300), rng.uniform(2, 4)), WHITE, 0.6)
    moon_body(R, 690, 820, 150, t, sq=1.0, seed=7, eye_slip=0.4, half=1.0, expr="flat")
    spinner(R, 690, 820, 60, t)
    R.c.drawRect(skia.Rect(0, 1200, W, H), R.paint(shader=R.lin(0, 1200, 0, H, [0xFF2A1A50, 0xFF0B0728])))
    howl = ease_out(prog(t, HOWL - 0.1, HOWL + 0.25))
    wolf(R, 330, 1270, 1.0, t, howl)
    R.fill(rrect(90, 1110, 440, 70, 35), INK, 0.85)
    R.fill(rrect(102, 1122, 416 * 0.12, 46, 23), GREEN)
    R.text("BUFFERING 12%", 310, 1160, "bungee", 34, WHITE, None)


def scene_nowhere(R, t):                         # back at the desk: night is homeless
    G = glorp_desk(t)
    G.expr = "smug"
    desk_shot(R, t, glorp=G, moon_look=(0.5, 0.3))
    if t >= W_("nowhere", 0.6):                  # night itself, a small dark cloud with a bindle, wanders by
        u = prog(t, W_("nowhere", 0.6), S_MIN)
        x = lerp(980, 560, u)
        b_ = blobby(x, 860, 90, 60, 3, 0.08, phase=t * 2)
        R.fill(b_, 0xFF140A3C)
        R.stroke(b_, 0xFFB8A8F0, 5)
        for ex in (-25, 25):
            R.fill(circle(x + ex, 850, 9), WHITE)
        R.stroke(poly([(x + 60, 840), (x + 120, 760)], False), INK, 8)
        R.fill(circle(x + 126, 752, 26), 0xFFFF3B3B)
        R.stroke(circle(x + 126, 752, 26), INK, 5)


def scene_minister(R, t):                        # S_MIN -> S_THU
    R.gradient_bg(0xFF2B86C5, 0xFF784BA0, 0xFF3A1670)
    R.bokeh(t, 9, 7, 0.12)
    flurb_flag(R, 110, 520, t)
    R.c.drawRect(skia.Rect(0, 1280, W, H), R.paint(shader=R.lin(0, 1280, 0, H, [0xFF2A1458, 0xFF0F0828])))
    if t >= T["lamp"] + 0.15:                    # the lamp, as recommended
        k = pop(t, T["lamp"] + 0.15, 0.3, 0.3)
        R.c.save()
        R.c.translate(820, 980)
        R.c.scale(k, k)
        g = R.rad(0, -120, 260, [argb(0xFFFFF6B0, 0.55), argb(0xFFFFF6B0, 0)])
        R.c.drawCircle(0, -120, 260, R.paint(shader=g))
        R.stroke(poly([(0, -60), (0, 200)], False), INK, 14)
        R.fill(poly([(-80, -60), (80, -60), (50, -170), (-50, -170)]), YELLOW)
        R.stroke(poly([(-80, -60), (80, -60), (50, -170), (-50, -170)]), INK, 6)
        R.fill(oval(0, 205, 70, 18), INK)
        R.c.restore()
    minister(R, 520, 900, 0.85, t, talk=talk(t, "M"), look=-0.3 if t < T["noinf"] else 0.6,
             sweat=1.0 if t >= T["noinf"] + 0.4 else 0.0)
    lower("MINISTER OF NIGHT", "Grand Duchy of Flurb", ease_out(prog(t, S_MIN + 0.2, S_MIN + 0.45)))


def scene_thursday(R, t):                        # S_THU -> S_INF
    R.gradient_bg(0xFFFF3CAC, 0xFF784BA0, 0xFF2B86C5, 0.4)
    R.bokeh(t, 11)
    k = pop(t, S_THU, 0.3, 0.4)
    thursday(R, 480, 860, 1.25 * k, t, talk=talk(t, "H"), expr="shock")


def scene_influencer(R, t):                      # S_INF -> S_TOAST
    rise = ease_in_out(prog(t, W_("iam", 0.35), E["iam"] + 0.1))
    a = rise
    R.c.drawRect(skia.Rect(0, 0, W, H), R.paint(shader=R.lin(0, 0, 0, H, [0xFFFFC4E6, 0xFFFF9AD5, 0xFFC08AE8])))
    if a > 0:
        R.c.drawRect(skia.Rect(0, 0, W, H), R.paint(shader=R.lin(0, 0, 0, H, [0xFF140A3C, 0xFF2B1D6E, 0xFF4B2C86]),
                                                   alpha=a))
        rng = np.random.default_rng(5)
        for i in range(36):
            R.fill(circle(rng.uniform(0, W), rng.uniform(560, 1250), rng.uniform(2, 4)), WHITE, 0.6 * a)
    else:
        R.fill(rrect(80, 640, 300, 24, 8), 0xFFFFF0F8, 0.8)
        R.fill(rrect(680, 1080, 200, 200, 30), 0xFFFFF0F8, 0.6)
    R.c.drawRect(skia.Rect(0, 1280, W, H), R.paint(shader=R.lin(0, 1280, 0, H, [0xFFE8A0D0, 0xFF8A5AB8]), alpha=1 - a))
    y = lerp(880, 760, rise)
    influencer(R, 480, y, lerp(1.05, 0.9, rise), t, talk=talk(t, "I"), glow=rise, pose=1.0 if rise > 0.5 else 0.0)
    story_ui(R, t, prog(t, S_INF, S_TOAST))
    for i in range(5):                                  # hearts float up (reactions)
        t0 = S_INF + 0.3 + i * 0.5
        u = prog(t, t0, t0 + 1.6)
        if t >= t0 and u < 1:
            heart(R, 780 + math.sin(i * 2 + u * 4) * 40, 1200 - u * 520, 0.3, rot=10 * math.sin(i), sq=1.0)
    if t >= T["link"]:
        k = pop(t, T["link"] + 0.1, 0.3, 0.4)
        tag(R, "link in crater", 480, 1120, YELLOW, rot=-4, size=50, scale=k)
        R.stroke(poly([(480, 1060), (470, 960)], False), INK, 10)


def scene_toaster(R, t):                         # S_TOAST -> S_UPD
    sep = 1.0 if FLASHBACK[0] <= t < FLASHBACK[1] else 0.0
    c = R.c
    push = 1 + 0.12 * prog(t, S_TOAST, S_UPD)
    c.save()
    c.translate(470, 1000)
    c.scale(push, push)
    c.translate(-470, -1000)
    kitchen(R, t, sep)
    if sep:   # the flashback, held in sepia: the Sun with a SOLD tag, 1987
        sun(R, 640, 700, 140, t, expr="flat")
        price_tag(R, 700, 880, ["SOLD", "1 sun"], rot=8, s=0.7, string_to=(680, 800))
        R.text("1987", 230, 760, "bungee", 110, 0xFFFFE6B0, INK, 10, rot=-6)
    heat = ease_in_out(prog(t, T["job"], W_("job", 0.8)))
    if heat > 0 and not sep:   # it has been doing the Sun's job: it glows
        g = R.rad(470, 1030, 520, [argb(0xFFFFB040, 0.55 * heat), argb(0xFFFF6A00, 0.2 * heat), argb(0xFFFF6A00, 0)])
        c.drawCircle(470, 1030, 520, R.paint(shader=g))
    toaster_char(R, 470, 1250, 0.92, t, talk=talk(t, "X"), toast_up=ease_out_back(prog(t, TOAST_UP, TOAST_UP + 0.25)),
                 burnt=1.0, smoke=1.0, stare=1.0)
    c.restore()
    if sep:
        R.c.drawRect(skia.Rect(0, 0, W, H), R.paint(0xFF8A5A2A, 0.18))
    lower("TOASTER", "has seen things", ease_out(prog(t, S_TOAST + 0.2, S_TOAST + 0.45)))


def scene_update(R, t):                          # S_UPD -> S_B1
    G = glorp_desk(t)
    G.expr = "worried" if t < T["buyer2"] else "shock"
    G.sweat = 0.5 if t >= T["cancel"] else 0.0
    stamp = "VOID" if t >= T["cancel"] + 0.6 else None
    turn = t >= TURN_T
    desk_shot(R, t, glorp=G, heart_t=S_UPD, tag_stamp=stamp, tag_k=prog(t, T["cancel"] + 0.6, T["cancel"] + 0.85),
              moon_look=(-0.8, 0.6) if turn else (0, 0), moon_expr="grin" if turn else "smile")


def scene_b1(R, t):
    keynote(R, t, lambda R_, cx, cy: R_.text("MOON 2.0", cx, cy - 190, "bungee", 76, WHITE, None))
    tech_boss(R, 520, 1285, 0.85, t, talk=0, sold_k=prog(t, S_B1, S_B1 + 0.2))


def scene_b2(R, t):
    R.gradient_bg(0xFFFF3CAC, 0xFF784BA0, 0xFF2B86C5, 0.4)
    thursday(R, 480, 860, 1.15, t, expr="shock", sold_k=prog(t, S_B2, S_B2 + 0.2), rot=-4)


def scene_b3(R, t):
    kitchen(R, t)
    toaster_char(R, 470, 1250, 0.92, t, toast_up=1.0, smoke=0.5, sold_k=prog(t, S_B3, S_B3 + 0.2))


def scene_b4(R, t):
    G = glorp_desk(t)
    G.expr = "shock"
    G.sweat = 0.6
    desk_shot(R, t, glorp=G, moon_look=(-0.8, 0.6), moon_expr="grin")


def scene_hug(R, t):                             # S_HUG -> LOOP_SNAP
    G = glorp_desk(t)
    G.expr = "shock" if t < HUG_T else "panic"
    G.hand = "none" if t >= HUG_T else "up"
    out = ease_in_out(prog(t, S_HUG, P("pend", 1)))
    reach = ease_out(prog(t, P("pend", 1), HUG_T + 0.1))
    sq = 0.0
    if t >= HUG_T:
        sq = 0.35
        for s0 in SQUEEZES:
            if s0 <= t < s0 + 0.25:
                sq = 0.35 + 0.45 * math.sin(math.pi * prog(t, s0, s0 + 0.25))
    squeeze(G, sq)
    G.y = lerp(1005, 905, reach)          # the hug lifts him off his chair
    done = t >= SQUEEZES[3] + 0.15
    hug_tag = (["HUG", "received (1/1)"], "PAID", prog(t, SQUEEZES[3] + 0.15, SQUEEZES[3] + 0.4)) if done else \
        (["HUG", "pending..."], None, 0.0)
    desk_shot(R, t, glorp=G, moon_out=max(0.001, out), moon_look=(-0.7, 0.5), moon_expr="grin",
              moon_talk=talk(t, "L"), arms=ease_out(prog(t, S_HUG, S_HUG + 0.4)), reach=reach,
              show_ticker=t < HUG_T, hug_tag=hug_tag if t >= HUG_T - 0.3 else None)


SCENES = [
    (0.0, S_BOSS, scene_desk_open), (S_BOSS, S_WOLF, scene_boss), (S_WOLF, S_NOW, scene_wolf),
    (S_NOW, S_MIN, scene_nowhere), (S_MIN, S_THU, scene_minister), (S_THU, S_INF, scene_thursday), (S_INF, S_TOAST, scene_influencer),
    (S_TOAST, S_UPD, scene_toaster), (S_UPD, S_B1, scene_update), (S_B1, S_B2, scene_b1), (S_B2, S_B3, scene_b2),
    (S_B3, S_B4, scene_b3), (S_B4, S_HUG, scene_b4), (S_HUG, LOOP_SNAP, scene_hug),
    (LOOP_SNAP, DURATION + 1, scene_desk_open),
]
DESK_SCENES = (scene_desk_open, scene_update, scene_b4, scene_hug, scene_nowhere)


def _in(lst, t):
    for it in lst:
        if it[0] <= t < it[1]:
            return it[2]
    return 0.0


def draw_scene(R, t):
    tv = remap(t, STUTTERS, FREEZES)
    for a, b, fn in SCENES:
        if a <= t < b:
            c = R.c
            c.save()
            CAM.apply(c, t)
            fn(R, tv)
            c.restore()
            return fn


def card_on(t):
    return any(cp.style == "fact" and cp.start <= t < cp.end for cp in CAPTIONS) or t >= LOOP_SNAP


def hud(R, t, fn):
    reality_bar(R, 99, label="GENERATING NEWS...")
    if fn in DESK_SCENES and not card_on(t):
        news_bug(R, t)
    if P("b4", 1) <= t < LOOP_SNAP:
        sold(R, 760, 282, 0.42, -8, k=prog(t, P("b4", 1), P("b4", 1) + 0.2))
    watermark(R, 0.26, y=1150)


def draw_frame(R, t):
    OVERLAY.clear()
    split, fry = _in(SPLITS, t), _in(FRY, t)
    box = {}
    if split or fry:
        post(R, lambda R2: box.setdefault("fn", draw_scene(R2, t)), split=split, fry=fry)
    else:
        box["fn"] = draw_scene(R, t)
    for (name, role, k, y) in OVERLAY:
        lower_third(R, name, role, k, y=y)
    hud(R, t, box.get("fn"))
    if P("b4", 1) <= t < S_HUG:   # SOLD on the whole screen ("this channel")
        sold(R, 500, 820, 2.1, -14, k=prog(t, P("b4", 1), P("b4", 1) + 0.22))
    for cap in CAPTIONS:
        cap.draw(R, t)
    LOOP_CARD.draw(R, t)


def cover(R):
    """Cover: the frame-0 desk shot with the title card."""
    desk_shot(R, 0.4, glorp=glorp_desk(0.4, expr="grin"))
    reality_bar(R, 99, label="GENERATING NEWS...")
    news_bug(R, 0.4)
    R.text("BREAKING:", 300, 520, "anton", 92, WHITE, INK, 12, rot=-3, shadow=(INK, 5, 7))
    R.text("THE MOON", 500, 640, "anton", 150, YELLOW, INK, 16, shadow=(INK, 7, 10))
    R.text("WAS SOLD", 500, 790, "anton", 150, YELLOW, INK, 16, shadow=(INK, 7, 10))
