"""COULD YOU SURVIVE? #04 — A Roman winter camp: the soundtrack. Our own tune for the frontier fort (A dorian, 100 BPM,
a march: a plucked lyre playing broken chords, a brassy horn call in fourths and fifths like an army horn, a field
drum on the beat with a rim click on the off-beats, a low pluck bass; the mail section drops the drum for a lighter
lyre-and-pipe feel), a winter bed (wind gusting round the timber, creaks; inside the bathhouse a warm drip room),
the effects on the story beats, the three voices on top. Nothing to license.

    python3 cys04_audio.py      -> out/cys04_audio.wav, then out/SubjectZero_CYS04_RomanCamp.mp4 (-14 LUFS)
    python3 cys04_audio.py --mixgate   also writes out/cys04mix_voice.wav + out/cys04mix_lines.json for listen.py
"""
import json
import math
import os
import shutil
import subprocess
import sys

import numpy as np
from scipy.io import wavfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tl_audio as TA       # noqa: E402
import cys04_pic as P       # noqa: E402

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
D = P.DURATION
BPM = 100
NBARS = 27                  # 27 bars = 64.8 s: the music ends on a bar line with the respawn flash
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(4)


def t_(d):
    return np.arange(int(d * SR)) / SR


def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


def lyre(f, d, v=1.0):
    """A plucked gut string (Karplus-Strong, a soft pluck): the lyre."""
    n = int(d * SR)
    period = int(round(SR / f))
    line = TA.lp(rng.uniform(-1, 1, period + 2), 3000)[: period]
    y = np.zeros(n)
    buf = line.copy()
    for i in range(n):
        j = i % period
        a = buf[j]
        b = buf[(j + 1) % period]
        buf[j] = 0.994 * 0.5 * (a + b)
        y[i] = a
    y *= np.minimum(1, (d - t_(d)[:n]) / 0.05)
    return TA.lp(y, 4200) * v


def horn(f, d, v=1.0):
    """A bright, slightly rough brass call (saw partials, a lip 'blat' at the start, slow swell)."""
    tt = t_(d)
    blat = 1 - 0.04 * np.exp(-tt * 18)
    ph = 2 * np.pi * np.cumsum(f * blat * (1 + 0.004 * np.sin(2 * np.pi * 5 * tt))) / SR
    x = sum(np.sin(k * ph) / k ** 1.1 for k in range(1, 9))
    env = np.minimum(1, tt / 0.07) * np.minimum(1, (d - tt) / 0.12)
    return np.tanh(TA.lp(x, 2400) * 1.4) * env * v


def pipe(f, d, v=1.0):
    tt = t_(d)
    ph = 2 * np.pi * f * tt * (1 + 0.006 * np.sin(2 * np.pi * 5.5 * tt) * np.minimum(1, tt / 0.3))
    x = np.sin(ph) + 0.2 * np.sin(2 * ph) + TA.bp(TA.noise(d), f, min(12000, f * 2.5)) * 0.05
    return x * np.minimum(1, tt / 0.05) * np.minimum(1, (d - tt) / 0.1) * v


def field_drum(v=1.0):
    tt = t_(0.45)
    f = 90 + 70 * np.exp(-tt * 30)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)
    x += TA.bp(TA.noise(0.45), 300, 3000) * np.exp(-tt * 22) * 0.6
    return x * v


def rim(v=1.0):
    tt = t_(0.06)
    return (np.sin(2 * np.pi * 1700 * tt) * 0.5 + TA.hp(TA.noise(0.06), 3000)) * np.exp(-tt * 70) * v


SCALE = [57, 59, 60, 62, 64, 66, 67, 69, 71, 72]     # A dorian from A3
CHORDS = [(45, (0, 2, 4)), (43, (6, 8, 1)), (41, (5, 7, 2)), (40, (4, 6, 1))]   # bass root, scale steps (Am G F/D Em-ish)
HORN_A = [(0, 4, 1.0), (1, 7, 1.5), (2.5, 6, 0.5), (3, 4, 1.0)]          # beat, step, beats: the call (E A G E)
HORN_B = [(0, 3, 0.5), (0.5, 4, 0.5), (1, 7, 2.0), (3, 6, 1.0)]
PIPE = [(0, 7, 1.5), (1.5, 8, 0.5), (2, 9, 1.0), (3, 7, 1.0)]


def music():
    n = int(D * SR) + 2 * SR
    out = np.zeros((n, 2))
    t_mail, t_mail_end = P.L["n8"] - 0.1, P.shot_start("latrine")     # the mail: lighter, no drum
    t_dig = P.L["n19"] - 0.1                                           # the twist: warm, slower pulse
    cache = {}
    for b in range(NBARS):
        t0 = b * BAR
        mail = t_mail - BAR * 0.5 <= t0 < t_mail_end
        dig = t_dig - BAR * 0.5 <= t0 < P.L["n21"]
        root, steps = CHORDS[b % 4]
        for beat, m in ((0, root), (2, root + 7)):
            TA.place(out, TA.bass_note(m, BEAT * 1.6, 0.5), t0 + beat * BEAT, 1.0)
        if b >= 1:                                 # the lyre: broken chord in eighths
            for k in range(8):
                st = steps[(0, 1, 2, 1)[k % 4]]
                m = SCALE[st] - 12 + (12 if k >= 4 and not dig else 0)
                if m not in cache:
                    cache[m] = lyre(midi(m), 0.8)
                TA.place(out, cache[m] * (0.13 if k % 2 == 0 else 0.09), t0 + k * BEAT / 2, 1.0, pan=0.25)
        if b >= 2 and not mail and not dig:       # the horn call every other bar
            if b % 2 == 0:
                mot = HORN_A if (b // 4) % 2 == 0 else HORN_B
                for beat, step, ln in mot:
                    TA.place(out, horn(midi(SCALE[step]), ln * BEAT * 0.92, 0.07), t0 + beat * BEAT, 1.0, pan=-0.15)
        if mail or dig:
            for beat, step, ln in PIPE:
                TA.place(out, pipe(midi(SCALE[step] + 12), ln * BEAT * 0.9, 0.06), t0 + beat * BEAT, 1.0, pan=-0.2)
        for k in range(4):                         # the march: drum on the beat, rim on the off-beat
            tb = t0 + k * BEAT
            if b >= 1 and not mail:
                TA.place(out, field_drum((0.55 if k in (0, 2) else 0.35) * (0.6 if dig else 1.0)), tb, 1.0)
                if not dig:
                    TA.place(out, rim(0.25), tb + BEAT / 2, 1.0, pan=0.3)
            elif mail and k in (0, 2):
                TA.place(out, rim(0.18), tb, 1.0, pan=0.3)
    out = out[: int(NBARS * BAR * SR)]
    return np.pad(out, ((0, n - len(out)), (0, 0)))


def winter_bed(n):
    """Wind gusting round the timber (a band of noise that swells), a far creak now and then; inside the insert
    shots it drops; in the bathhouse, drips instead of wind."""
    tt = np.arange(n) / SR
    gust = 0.45 + 0.55 * np.sin(2 * np.pi * 0.11 * tt) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.29 * tt + 1))
    wind = TA.bp(TA.noise(n / SR), 250, 1400)[:n] * gust
    whist = TA.bp(TA.noise(n / SR), 900, 1100)[:n] * gust ** 2 * 0.6
    y = wind * 0.8 + whist
    for name in ("map", "march", "pack", "report", "letter", "beer", "latrine", "sponge", "mud", "contract", "dig", "invite"):
        for nth in range(3):
            try:
                s_ = P.shot_start(name, nth)
            except IndexError:
                break
            y *= 1 - 0.75 * ((tt >= s_) & (tt < P.shot_end(s_)))
    a, b = P.shot_start("duck"), P.shot_end(P.shot_start("duck"))
    y *= 1 - 0.9 * ((tt >= a) & (tt < b))
    return np.stack([y, np.roll(y, 300)], 1)


def cut(mus, a, b, fade=0.04):
    i, j = int(a * SR), int(b * SR)
    f = int(fade * SR)
    mus[i:j] = 0
    if i - f > 0:
        mus[i - f:i] *= np.linspace(1, 0, f)[:, None]
    if j + f < len(mus):
        mus[j:j + f] *= np.linspace(0, 1, f)[:, None]


def boom(v=1.0, d=1.6):
    tt = t_(d)
    f = 34 + 60 * np.exp(-tt * 6)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.2)
    x += TA.lp(TA.noise(d), 400) * np.exp(-tt * 4) * 0.8
    return np.tanh(x * 1.5) * v


def snow_whump(v=1.0, d=0.9):
    """Snow thrown off: a soft low thump and a long airy hiss."""
    tt = t_(d)
    x = TA.lp(TA.noise(d), 260) * np.exp(-tt * 9) * 2.0
    x += TA.bp(TA.noise(d), 1500, 7000) * np.minimum(1, tt / 0.03) * np.exp(-tt * 3.5) * 0.5
    return x * v


def crunch_steps(v=1.0, k=3, gap=0.16):
    out = np.zeros(int((k * gap + 0.3) * SR))
    for j in range(k):
        x = TA.sfx("crunch")
        i = int(j * gap * SR)
        out[i:i + len(x)] += x[: len(out) - i] * 0.6
    return out * v


def wood_creak(v=1.0, d=0.6):
    tt = t_(d)
    f = 70 + 50 * np.sin(2 * np.pi * 1.5 * tt) + 20 * tt
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (rng.uniform(0, 1, len(tt)) > 0.25)
    return TA.bp(x, 250, 1800) * np.sin(np.pi * tt / d) * 0.35 * v


def clatter(v=1.0, d=1.2, n=16):
    """Shingles raining down: many short wooden knocks."""
    out = np.zeros(int(d * SR))
    for _ in range(n):
        t0 = rng.uniform(0, d - 0.12)
        f = rng.uniform(500, 1400)
        tt = t_(0.08)
        knock = (np.sin(2 * np.pi * f * tt) + 0.6 * TA.bp(TA.noise(0.08), 800, 4000)) * np.exp(-tt * 60)
        i = int(t0 * SR)
        out[i:i + len(knock)] += knock * rng.uniform(0.3, 0.8)
    return out * v


def timber_fall(v=1.0, d=1.6, n=14):
    """The rampart posts going over one after another: heavy wooden thuds that speed up."""
    out = np.zeros(int(d * SR) + SR)
    t = 0.0
    for j in range(n):
        tt = t_(0.35)
        f = 80 + 40 * np.exp(-tt * 20)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 12) + TA.bp(TA.noise(0.35), 200, 1500) * np.exp(-tt * 18) * 0.6
        i = int(t * SR)
        out[i:i + len(x)] += x[: len(out) - i] * (0.5 + 0.03 * j)
        t += 0.11 - 0.004 * j
    return out[: int(d * SR)] * v


def drip(v=1.0):
    tt = t_(0.12)
    f = 1400 + 900 * np.exp(-tt * 40)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 35) * v


def splash(v=1.0, d=0.5):
    tt = t_(d)
    return TA.bp(TA.noise(d), 700, 5000) * np.minimum(1, tt / 0.01) * np.exp(-tt * 9) * v


def radio(v=1.0):
    tt = t_(0.12)
    beep = np.sin(2 * np.pi * 1250 * tt) * (tt < 0.07) * 0.5
    sq = TA.bp(TA.noise(0.12), 1500, 5000) * np.exp(-tt * 30) * 0.6
    return (beep + sq) * v


def squeak(v=1.0, up=True):
    tt = t_(0.22)
    f = np.geomspace(1100, 2100, len(tt)) if up else np.geomspace(2000, 1300, len(tt))
    vib = 1 + 0.04 * np.sin(2 * np.pi * 38 * tt)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    x = np.sign(np.sin(ph)) * 0.3 + np.sin(ph) * 0.5
    return TA.lp(x, 4000) * np.minimum(1, tt / 0.01) * np.exp(-tt * 6) * v


def stone_tick(v=1.0):
    tt = t_(0.08)
    return (np.sin(2 * np.pi * 900 * tt) * 0.4 + TA.bp(TA.noise(0.08), 1000, 5000)) * np.exp(-tt * 50) * v


def dig_scrape(v=1.0, d=0.8):
    tt = t_(d)
    x = TA.bp(TA.noise(d), 600, 3000) * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * tt) ** 2)
    return x * np.sin(np.pi * tt / d) * v


def build(mixgate=False):
    n = int(D * SR)
    mus = music()[:n + SR]
    fx = np.zeros((n + 2 * SR, 2))
    L, E, WT = P.L, P.E, P.WT
    # spawn: she lands in the snow
    TA.place(fx, snow_whump(0.7, 0.6), 0.0, 1.0)
    TA.place(fx, TA.sfx("pop"), 0.02, 0.5)
    # map: whoosh in, the road draws, the pin, the card
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("map") - 0.08, 0.6)
    TA.place(fx, TA.sfx("scribble"), P.shot_start("map") + 0.15, 0.4)
    TA.place(fx, TA.sfx("pop"), P.shot_start("map") + 0.75, 0.7)
    TA.place(fx, TA.sfx("paper"), WT("n2", "year") - 0.1, 0.4)
    # march: the milestones whip past (ticks speeding up), stamps on the two cards
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("march") - 0.05, 0.6)
    tm0, tm1 = P.shot_start("march") + 0.2, WT("n3", "km") + 0.4
    for i in range(20):
        u = i / 19
        tt = tm0 + (tm1 - tm0) * (1 - (1 - u) ** 2) ** 0.5
        TA.place(fx, stone_tick(0.5), tt, 1.0, pan=0.4)
    TA.place(fx, TA.sfx("stamp"), WT("n3", "30"), 0.7)
    # "Thirty WHAT?": a boing
    TA.place(fx, TA.sfx("boing_up"), E["n4"] + 0.25, 0.3)
    # pack: each bundle clanks on, she sinks
    a = P.shot_start("pack")
    for j in range(4):
        TA.place(fx, TA.sfx("thud") if j else TA.sfx("slam"), a + 0.3 + 0.25 * j, 0.35)
    TA.place(fx, TA.sfx("boing_down"), WT("n3", "20"), 0.35)
    TA.place(fx, TA.sfx("stamp"), WT("n3", "20"), 0.6)
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("march", 1) - 0.05, 0.4)
    TA.place(fx, TA.sfx("stamp"), WT("n5", "6"), 0.6)
    # the sick list: paper, the dots patter in, a low hit on 31
    TA.place(fx, TA.sfx("paper"), P.shot_start("report"), 0.5)
    for j in range(12):
        TA.place(fx, TA.sfx("tick", j), P.shot_start("report") + 0.05 + 0.1 * j, 0.15)
    TA.place(fx, boom(0.25, 0.6), WT("n6", "31"), 1.0)
    # the lab: squelch before each line
    for k in P.KEYS:
        if P.WHO[k] == "LAB":
            TA.place(fx, radio(0.7), L[k] - 0.22, 1.0, pan=0.4)
    # mail: the letter flutters down, paper, sparkle
    TA.place(fx, TA.sfx("whoosh_down"), L["n8"] - 0.1, 0.4)
    TA.place(fx, TA.sfx("paper"), P.T_CATCH, 0.7)
    TA.place(fx, TA.sfx("sparkle"), P.T_CATCH + 0.05, 0.4)
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("letter") - 0.05, 0.5)
    for w in ("socks", "sandals", "underpants"):
        TA.place(fx, TA.sfx("pop"), WT("n9", w), 0.7)
    # beer: the tap creaks, one drop, stamp
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("beer") - 0.05, 0.5)
    TA.place(fx, wood_creak(0.6, 0.4), WT("n10", "no") - 0.2, 1.0)
    TA.place(fx, drip(0.5), WT("n10", "beer") + 0.35, 1.0)
    TA.place(fx, TA.sfx("stamp"), WT("n10", "beer") + 0.1, 0.8)
    # the duck in the bath: splash, squeak, drips
    TA.place(fx, splash(0.4), P.shot_start("duck") + 0.05, 1.0)
    TA.place(fx, squeak(0.5), P.shot_start("duck") + 0.35, 1.0, pan=0.2)
    for j in range(4):
        TA.place(fx, drip(0.25), P.shot_start("duck") + 0.2 + 0.37 * j, 1.0, pan=-0.3 + 0.2 * j)
    # latrine: water trickles (bed), stamp; sponge: a squelch-pop, stamp
    TA.place(fx, TA.sfx("whoosh_down"), P.shot_start("latrine") - 0.05, 0.5)
    TA.place(fx, splash(0.15, 1.5), P.shot_start("latrine"), 1.0, pan=-0.2)
    TA.place(fx, TA.sfx("stamp"), WT("n12", "No"), 0.8)
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("sponge") - 0.05, 0.5)
    TA.place(fx, TA.sfx("stamp"), WT("n13", "shared"), 0.8)
    # the tease: a riser into the question; the mud: a low rumble
    TA.place(fx, TA.sfx("riser"), L["n15"] + 0.8, 0.35)
    TA.place(fx, TA.sfx("rumble"), P.shot_start("mud"), 0.4)
    # the answer: silence (music cut), then the stamp; the snowflakes tick in; MINIMUM stamp
    t_rev = WT("n16", "25")
    TA.place(fx, TA.sfx("stamp"), t_rev, 1.2)
    for j in range(10):
        TA.place(fx, TA.sfx("tick", j), t_rev + 0.05 + 0.075 * j, 0.25)
    TA.place(fx, TA.sfx("stamp"), WT("n16", "Minimum"), 0.9)
    # dig: scrape, the tablets pop up, the trowel lifts one
    TA.place(fx, TA.sfx("whoosh_down"), P.shot_start("dig") - 0.05, 0.5)
    TA.place(fx, dig_scrape(0.5), P.shot_start("dig") + 0.2, 1.0)
    for j in range(7):
        TA.place(fx, TA.sfx("pop", j), P.shot_start("dig") + 0.3 + 0.28 * j, 0.35)
    TA.place(fx, dig_scrape(0.6, 0.6), WT("n19", "dug") - 0.1, 1.0, pan=0.3)
    TA.place(fx, TA.sfx("sparkle"), E["n19"] - 0.3, 0.4)
    # invitation: paper, ding on the birthday, stamp on her hand
    TA.place(fx, TA.sfx("paper"), P.shot_start("invite"), 0.6)
    TA.place(fx, TA.sfx("ding"), WT("n20", "birthday"), 0.45)
    TA.place(fx, TA.sfx("scribble"), WT("n20", "woman") - 0.3, 0.5)
    TA.place(fx, TA.sfx("stamp"), WT("n20", "woman"), 0.9)
    # the NOPEs: the word first, clean; the damage lands as it ends
    for key, lvl in P.NOPES.items():
        hit = E[key] + 0.02
        if lvl == 1:              # the snow blows off the fort
            TA.place(fx, boom(0.3, 0.9), hit - 0.07, 1.0)
            TA.place(fx, snow_whump(0.9), hit - 0.05, 1.0)
        elif lvl == 2:            # the barrack roof's shingles rip off and rain down
            TA.place(fx, boom(0.55, 1.0), hit, 1.0)
            TA.place(fx, wood_creak(0.8, 0.4), hit, 1.0, pan=-0.3)
            TA.place(fx, clatter(0.8, 1.3), hit + 0.1, 1.0, pan=0.2)
        else:                     # the rampart falls like dominoes, the gate tower topples, a wall of snow
            for i in (0, 1):
                TA.place(fx, boom(0.12 + 0.06 * i, 0.18), P.W3[i] + 0.22, 1.0)
            TA.place(fx, boom(1.15, 1.0), hit, 1.0)
            TA.place(fx, timber_fall(0.9, 1.6), hit + 0.05, 1.0)
            TA.place(fx, snow_whump(1.0, 1.2), hit + 0.15, 1.0)
            TA.place(fx, wood_creak(0.9, 0.7), P.T_BLAST3 + 0.3, 1.0, pan=0.4)
            TA.place(fx, TA.sfx("slam"), P.T_BLAST3 + 1.1, 0.8)
    # the end: the three choices, the countdown, the respawn
    for word in ("Mars", "medieval", "Pompeii"):
        TA.place(fx, TA.sfx("pop"), WT("n21", word), 0.7)
    TA.place(fx, TA.sfx("riser_fast"), E["n23"] - 0.7, 0.6)
    TA.place(fx, TA.sfx("pop"), E["n23"] + 0.02, 1.0)
    TA.place(fx, TA.sfx("sparkle"), E["n23"] + 0.05, 0.7)
    fx = fx[:n]
    mus = mus[:n]
    bed = winter_bed(n)
    cut(mus, E["n15"] + 0.05, t_rev + 0.05)          # silence before the answer
    cut(bed, E["n15"] + 0.05, t_rev - 0.05)
    cut(mus, L["n4"] - 0.08, E["n4"] + 0.02)          # "Thirty WHAT?": the band stops for her
    cut(bed, L["n4"] - 0.08, E["n4"] + 0.02)
    for key, lvl in P.NOPES.items():
        cut(mus, L[key] - 0.12, E[key] + (0.2, 0.35, 0.9)[lvl - 1])
        cut(bed, L[key] - 0.12, E[key] + 0.05)
    vsr, v = wavfile.read(os.path.join(OUT, "cys04_voice.wav"))
    v = v.astype(np.float32) / 32768
    if vsr != SR:
        from scipy import signal
        v = signal.resample_poly(v, SR, vsr).astype(np.float32)
    v = np.pad(v, (0, max(0, n - len(v))))[:n]
    # NOPE 3 a little louder, so it lands at least 3 dB above NOPE 2 on the final mix
    a_, b_ = int((L["n18"] - 0.05) * SR), int((E["n18"] + 0.1) * SR)
    gain = np.ones(n, np.float32)
    gain[a_:b_] = 10 ** (2.0 / 20)
    v = v * np.convolve(gain, np.ones(240) / 240, mode="same")
    voice = np.stack([v, v], 1)

    def rms(x):
        a = np.abs(x).mean(axis=1) if x.ndim > 1 else np.abs(x)
        m = a > 0.01
        return float(np.sqrt((x[m] ** 2).mean())) if m.any() else 1e-6
    vr = rms(voice)
    mus *= vr * 10 ** (-15 / 20) / rms(mus)
    fx *= vr * 10 ** (-12 / 20) / rms(fx)
    bed *= vr * 10 ** (-27 / 20) / rms(bed)
    talk = np.convolve((np.abs(v) > 0.02).astype(np.float32), np.ones(int(0.3 * SR)) / (0.3 * SR), mode="same")
    duck_ = (1 - 0.5 * np.clip(talk * 1.5, 0, 1))[:, None]
    mus *= duck_
    bed *= duck_
    mix = voice + mus + fx + bed
    mix = mix / (np.abs(mix).max() or 1) * 0.89
    wav = os.path.join(OUT, "cys04_audio.wav")
    wavfile.write(wav, SR, (mix * 32767).astype(np.int16))
    lv = []
    mono = mix.mean(axis=1)
    for key in P.NOPES:
        seg = mono[int(L[key] * SR):int(E[key] * SR)]
        lv.append(20 * math.log10(float(np.sqrt((seg ** 2).mean())) + 1e-9))
    print("NOPE levels on the mix (dB):", [round(x, 1) for x in lv])
    if mixgate:
        wavfile.write(os.path.join(OUT, "cys04mix_voice.wav"), SR, (mono * 32767).astype(np.int16))
        shutil.copy(os.path.join(OUT, "cys04_lines.json"), os.path.join(OUT, "cys04mix_lines.json"))
    vid = os.path.join(OUT, "cys04_pic_video.mp4")
    dst = os.path.join(OUT, "SubjectZero_CYS04_RomanCamp.mp4")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", "loudnorm=I=-14:TP=-2:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    js = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    if os.path.exists(vid):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", dst],
                       check=True)
        print("wrote", dst)
    print("wrote", wav)


if __name__ == "__main__":
    build("--mixgate" in sys.argv)
