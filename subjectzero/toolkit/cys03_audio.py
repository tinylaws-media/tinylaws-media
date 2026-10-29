"""COULD YOU SURVIVE? #03 — Death Valley: the soundtrack. Our own tune for the hot flat (D minor pentatonic, 96 BPM:
a slide-plucked twang guitar, a whistled lead, a dry shaker and a frame drum, a low pluck bass; the 1849 section
turns to a slow reed "harmonica" over the same chords), a desert bed (dry wind + a cicada buzz by day, crickets at
night), the effects on the story beats, the three voices on top. Nothing to license.

    python3 cys03_audio.py      -> out/cys03_audio.wav, then out/SubjectZero_CYS03_DeathValley.mp4 (-14 LUFS)
    python3 cys03_audio.py --mixgate   also writes out/cys03mix_voice.wav + out/cys03mix_lines.json for listen.py
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
import cys03_pic as P       # noqa: E402

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
D = P.DURATION
BPM = 96
NBARS = 26                  # 26 bars = 65.0 s: the music ends on a bar line with the respawn flash
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(3)


def t_(d):
    return np.arange(int(d * SR)) / SR


def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


def twang(f, d, v=1.0, slide=True):
    """A plucked steel string (Karplus-Strong) that slides up into the note: the dry desert guitar."""
    n = int(d * SR)
    period = SR / f
    y = np.zeros(n)
    line = rng.uniform(-1, 1, int(period * 1.06) + 4)   # the delay line, filled with a pluck of noise
    pos = 0
    for i in range(n):
        p_now = period * (1.06 - 0.06 * min(1.0, i / (0.06 * SR))) if slide else period
        j = pos - p_now
        j0 = int(math.floor(j)) % len(line)
        fr = j - math.floor(j)
        a = line[j0]
        b = line[(j0 + 1) % len(line)]
        s = (1 - fr) * a + fr * b
        s2 = line[(j0 - 1) % len(line)]
        val = 0.996 * 0.5 * (s + s2)
        line[pos % len(line)] = val
        y[i] = val
        pos += 1
    y *= np.minimum(1, (d - t_(d)[:n]) / 0.05)
    return TA.lp(y, 5000) * v


def whistle(f, d, v=1.0):
    tt = t_(d)
    vib = 1 + 0.008 * np.sin(2 * np.pi * 6.0 * tt) * np.minimum(1, tt / 0.25)
    glide = 1 - 0.03 * np.exp(-tt * 30)
    ph = 2 * np.pi * np.cumsum(f * vib * glide) / SR
    x = np.sin(ph) + 0.04 * np.sin(2 * ph)
    breath = TA.bp(TA.noise(d), f * 0.9, min(12000, f * 3)) * 0.08
    env = np.minimum(1, tt / 0.04) * np.minimum(1, (d - tt) / 0.1)
    return (x + breath) * env * v


def reed(f, d, v=1.0):
    """A harmonica-like reed: a few odd and even partials, a slow swell, tremolo."""
    tt = t_(d)
    ph = 2 * np.pi * f * tt
    x = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.35 * np.sin(3 * ph) + 0.15 * np.sin(4 * ph)
    env = np.minimum(1, tt / 0.12) * np.minimum(1, (d - tt) / 0.15) * (1 + 0.15 * np.sin(2 * np.pi * 5 * tt))
    return TA.lp(x, 3000) * env * v


def shaker(v=1.0):
    tt = t_(0.09)
    return TA.hp(TA.noise(0.09), 5000) * np.minimum(1, tt / 0.02) * np.exp(-tt * 45) * v


def frame_drum(v=1.0):
    tt = t_(0.5)
    f = 70 + 50 * np.exp(-tt * 25)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7)
    x += TA.lp(TA.noise(0.5), 1200) * np.exp(-tt * 40) * 0.4
    return x * v


SCALE = [62, 65, 67, 69, 72, 74, 77, 79]       # D minor pentatonic
RIFF = [(0, 0), (0.75, 2), (1.5, 3), (2.5, 2), (3, 1)]          # beat, step (the twang riff)
LEAD_A = [(0, 4, 1.5), (1.5, 3, 0.5), (2, 2, 2.0)]              # beat, step, length (beats)
LEAD_B = [(0, 5, 0.5), (0.5, 4, 0.5), (1, 3, 1.0), (2, 4, 2.0)]
OLD = [(0, 2, 2.0), (2, 3, 1.0), (3, 1, 1.0)]


def music():
    n = int(D * SR) + 2 * SR
    out = np.zeros((n, 2))
    t_old, t_old_end = P.L["n20"] - 0.1, P.L["n22"] - 0.05      # 1849: the old west, slower feel
    t_night, t_night_end = P.shot_start("night"), P.shot_start("night") + 2.6
    cache = {}
    for b in range(NBARS):
        t0 = b * BAR
        old = t_old - BAR * 0.5 <= t0 < t_old_end
        night = t_night - BAR * 0.5 <= t0 < t_night_end
        roots = [38, 38, 41, 36] if not old else [38, 34, 36, 38]
        root = roots[b % 4]
        for beat, m in ((0, root), (2, root + 7)) if not old else ((0, root),):
            TA.place(out, TA.bass_note(m, BEAT * 1.6, 0.5), t0 + beat * BEAT, 1.0)
        if old:
            for beat, step, ln in OLD:
                TA.place(out, reed(midi(SCALE[step] - 12), ln * BEAT * 0.95, 0.16), t0 + beat * BEAT, 1.0, pan=-0.1)
        elif b >= 1:
            for beat, step in RIFF:
                m = SCALE[step] - 12 + (root - 38)
                key = m
                if key not in cache:
                    cache[key] = twang(midi(m), 0.9, 1.0)
                TA.place(out, cache[key] * (0.12 if not night else 0.07), t0 + beat * BEAT, 1.0, pan=0.25)
            if b >= 2 and not night:
                mot = LEAD_A if b % 2 else LEAD_B
                for beat, step, ln in mot:
                    st = step + (1 if (b // 4) % 2 else 0)
                    TA.place(out, whistle(midi(SCALE[min(7, st)] + 12), ln * BEAT * 0.9, 0.08), t0 + beat * BEAT, 1.0,
                             pan=-0.15)
        for k in range(8):                         # eighths: shaker; drum on 1 and 3
            tb = t0 + k * BEAT / 2
            if b >= 1 and not night:
                TA.place(out, shaker(0.16 if k % 2 else 0.24), tb, 1.0, pan=0.35)
            if k in (0, 4) and b >= 1 and not old:
                TA.place(out, frame_drum(0.5 if k == 0 else 0.35), tb, 1.0)
            if old and k == 0:
                TA.place(out, frame_drum(0.4), tb, 1.0)
    out = out[: int(NBARS * BAR * SR)]
    return np.pad(out, ((0, n - len(out)), (0, 0)))


def desert_bed(n):
    """Dry wind and a cicada buzz in the day; crickets in the night shot; quieter inside the insert shots."""
    tt = np.arange(n) / SR
    wind = TA.bp(TA.noise(n / SR), 200, 1600)[:n] * (0.5 + 0.5 * np.sin(2 * np.pi * 0.17 * tt) ** 2)
    buzz = TA.bp(TA.noise(n / SR), 4200, 6500)[:n] * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 38 * tt))) * 0.5
    a, b = P.shot_start("night"), P.shot_end(P.shot_start("night"))
    night = ((tt >= a) & (tt < b)).astype(float)
    chirp = np.sin(2 * np.pi * 4400 * tt) * (np.sin(2 * np.pi * 3.2 * tt) > 0.6) * (np.sin(2 * np.pi * 60 * tt) > 0) * 0.3
    y = wind * 0.8 + buzz * (1 - night) + chirp * night
    for name in ("map", "bottle", "thermo", "days", "trail", "ridge"):
        s_ = P.shot_start(name)
        y *= 1 - 0.75 * ((tt >= s_) & (tt < P.shot_end(s_)))
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


def swirl(v=1.0, d=1.6):
    """The dust devil: a band of noise whose centre whirls up and down, rising, with sand grains."""
    tt = t_(d)
    x = TA.noise(d)
    out = np.zeros_like(x)
    for k in range(6):
        f0 = 400 + 300 * k
        out += TA.bp(x, f0, f0 * 1.6) * (0.5 + 0.5 * np.sin(2 * np.pi * (3 + 2 * tt) * tt + k))
    env = np.minimum(1, tt / 0.25) * np.minimum(1, (d - tt) / 0.5)
    grains = TA.hp(TA.noise(d), 6000) * (rng.uniform(0, 1, len(tt)) > 0.996) * 4
    return (out * 0.5 + grains) * env * v


def sizzle(v=1.0, d=1.2):
    tt = t_(d)
    x = TA.hp(TA.noise(d), 3000) * (rng.uniform(0, 1, len(tt)) > 0.6)
    return x * np.minimum(1, tt / 0.2) * np.minimum(1, (d - tt) / 0.3) * 0.5 * v


def glug(v=1.0, d=0.18):
    tt = t_(d)
    f = 300 + 500 * tt / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) * v


def bubbles(v=1.0, d=1.4):
    out = np.zeros(int(d * SR))
    t = 0.0
    while t < d - 0.1:
        b = glug(0.3, 0.05 + 0.04 * rng.uniform())
        i = int(t * SR)
        out[i:i + len(b)] += b[: len(out) - i]
        t += rng.uniform(0.05, 0.14)
    return out * v


def shatter(v=1.0, d=1.4):
    tt = t_(d)
    out = TA.hp(TA.noise(d), 2500) * np.exp(-tt * 3) * 0.6
    for k in range(14):
        f = rng.uniform(2500, 7000)
        t0 = rng.uniform(0, 0.8)
        i = int(t0 * SR)
        seg = np.sin(2 * np.pi * f * tt[: len(tt) - i]) * np.exp(-tt[: len(tt) - i] * 30) * 0.3
        out[i:] += seg
    return out * v


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


def creak(v=1.0, d=0.5):
    tt = t_(d)
    f = 90 + 40 * np.sin(2 * np.pi * 2 * tt)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (rng.uniform(0, 1, len(tt)) > 0.3)
    return TA.bp(x, 300, 2000) * np.sin(np.pi * tt / d) * 0.3 * v


def drumroll(d, v=1.0):
    out = np.zeros(int(d * SR) + SR // 4)
    t = 0.0
    while t < d:
        k = t / d
        x = TA.snare(0.25 + 0.6 * k)
        i = int(t * SR)
        out[i:i + len(x)] += x[: len(out) - i] * v
        t += 0.055 - 0.02 * k
    return out


def build(mixgate=False):
    n = int(D * SR)
    mus = music()[:n + SR]
    fx = np.zeros((n + 2 * SR, 2))
    L, E, WT = P.L, P.E, P.WT
    # spawn: a crunch onto the salt
    TA.place(fx, TA.sfx("crunch"), 0.0, 0.8)
    TA.place(fx, TA.sfx("pop"), 0.02, 0.6)
    # the temperature counts up: blips rising, ding on 134
    a, b = P.T_T0 - 0.2, P.T_T1
    for i in range(10):
        TA.place(fx, TA.blip(70 + i * 2, 0.05, 0.22), a + 0.2 + (b - a - 0.2) * i / 10, 1.0)
    TA.place(fx, TA.sfx("stamp"), b, 0.9)
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("heat") - 0.06, 0.6)
    # map: whoosh in, the pin, the record card, stamp on the date
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("map") - 0.08, 0.6)
    TA.place(fx, TA.sfx("pop"), P.shot_start("map") + 0.3, 0.7)
    TA.place(fx, TA.sfx("paper"), WT("n3", "hottest") - 0.1, 0.4)
    TA.place(fx, TA.sfx("stamp"), WT("n3", "Earth"), 0.8)
    # "I brought water!": a little proud sparkle
    TA.place(fx, TA.sfx("sparkle"), WT("n4", "brought"), 0.4)
    # bottle: the clock ticks faster, glugs as it drains, stamp EMPTY
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("bottle") - 0.05, 0.6)
    t0b, t1b = WT("n5", "drink") - 0.2, WT("n5", "every") + 0.5
    t = t0b
    i = 0
    while t < t1b:
        TA.place(fx, TA.sfx("tick", i), t, 0.3, pan=0.4)
        TA.place(fx, glug(0.25), t + 0.05, 1.0, pan=-0.4)
        t += 0.22
        i += 1
    TA.place(fx, TA.sfx("stamp"), t1b, 0.9)
    # the lab: squelch before each line; the gulp on "breakfast"
    for k in P.KEYS:
        if P.WHO[k] == "LAB":
            TA.place(fx, radio(0.7), L[k] - 0.22, 1.0, pan=0.4)
    for j in range(4):
        TA.place(fx, glug(0.35), L["n6"] + 0.3 + 0.2 * j, 1.0)
    # boots: the ground sizzles
    TA.place(fx, TA.sfx("whoosh_down"), P.shot_start("boots") - 0.05, 0.6)
    TA.place(fx, sizzle(0.8, 2.0), P.shot_start("boots") + 0.1, 1.0)
    # thermo: the ground column climbs with blips, bubbles on "boiling", stamp-ish ding on 11
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("thermo") - 0.05, 0.6)
    t201 = WT("n9", "201")
    for i in range(10):
        TA.place(fx, TA.blip(66 + i * 2, 0.05, 0.22), t201 - 0.3 + 0.1 * i, 1.0)
    TA.place(fx, TA.sfx("ding"), WT("n10", "11"), 0.5)
    TA.place(fx, bubbles(0.8), WT("n10", "boiling") - 0.1, 1.0, pan=0.3)
    # the duck: squeak, the mirage shimmers away, stamp
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("duck") - 0.05, 0.5)
    TA.place(fx, squeak(0.5), P.shot_start("duck") + 0.25, 1.0, pan=0.2)
    TA.place(fx, TA.sfx("shrink"), WT("n13", "mirage") - 0.05, 0.6)
    TA.place(fx, TA.sfx("stamp"), WT("n13", "mirage") + 0.2, 0.8)
    TA.place(fx, squeak(0.4, up=False), WT("n13", "care") + 0.1, 1.0, pan=0.2)
    # night: a soft whoosh, a ding on 100+
    TA.place(fx, TA.sfx("whoosh_down"), P.shot_start("night") - 0.05, 0.5)
    TA.place(fx, TA.sfx("ding"), WT("n14", "100"), 0.35)
    # the tease: a riser into the question
    TA.place(fx, TA.sfx("riser"), L["n15"] + 0.6, 0.35)
    # the answer: silence (music cut), then the stamp; two days roll by; the bottles pop; the stamp
    t_rev = WT("n16", "2")
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("days") - 0.05, 0.5)
    TA.place(fx, TA.sfx("stamp"), t_rev, 1.2)
    for j in range(4):
        TA.place(fx, TA.sfx("tick", j * 2), t_rev + 0.15 + 0.22 * j, 0.4)
    TA.place(fx, TA.sfx("pop"), WT("n17", "bottle"), 0.7)
    TA.place(fx, TA.sfx("pop", 3), WT("n17", "no"), 0.7)
    TA.place(fx, TA.sfx("whoosh"), WT("n17", "Only") - 0.1, 0.4)
    # wide: whoosh out, scribble the arrow, stamp NO SHADE
    TA.place(fx, TA.sfx("whoosh_down"), P.shot_start("wide") - 0.05, 0.6)
    TA.place(fx, TA.sfx("scribble"), L["n18"] + 0.2, 0.5)
    TA.place(fx, TA.sfx("ding"), WT("n18", "shade"), 0.4)
    # 1849: paper, the wagon creaks along the trail
    TA.place(fx, TA.sfx("paper"), P.shot_start("trail"), 0.6)
    TA.place(fx, TA.sfx("stamp"), WT("n20", "1849"), 0.6)
    for j in range(5):
        TA.place(fx, creak(0.6), WT("n20", "lost") + 0.6 * j, 1.0, pan=-0.2)
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("ridge") - 0.05, 0.5)
    TA.place(fx, creak(0.5, 0.7), P.shot_start("ridge") + 0.4, 1.0, pan=0.3)
    TA.place(fx, TA.sfx("stamp"), WT("n21", "Only"), 1.0)
    # the NOPEs: the word first, clean; the damage lands as it ends
    for key, lvl in P.NOPES.items():
        hit = E[key] + 0.02
        if lvl == 1:              # the salt crust cracks round her boots
            TA.place(fx, boom(0.3, 0.9), hit - 0.07, 1.0)
            TA.place(fx, TA.sfx("crack"), hit - 0.05, 0.8)
            TA.place(fx, TA.sfx("crunch"), hit + 0.05, 0.5)
        elif lvl == 2:            # the dust devil arrives and tears across
            TA.place(fx, boom(0.55, 1.0), hit, 1.0)
            TA.place(fx, swirl(0.9, 1.6), E["n11"] - 0.05, 1.0, pan=0.3)
            TA.place(fx, TA.sfx("hop"), E["n11"] + 0.05, 0.5)
        else:                     # the salt flat shatters, the air breaks like glass
            for i in (0, 1):
                TA.place(fx, boom(0.18 + 0.1 * i, 0.22), P.W3[i + 1] - 0.14, 1.0)
            TA.place(fx, boom(1.15, 1.0), hit, 1.0)
            TA.place(fx, shatter(0.8), hit + 0.02, 1.0)
            TA.place(fx, TA.sfx("crunch"), hit + 0.1, 1.0)
            TA.place(fx, TA.sfx("whoosh"), P.T_BLAST3 + 0.15, 0.8)
            TA.place(fx, squeak(0.5, up=True), hit + 0.4, 1.0, pan=0.5)
    # the end: the three choices, the countdown, the respawn
    for word in ("Roman", "Mars", "medieval"):
        TA.place(fx, TA.sfx("pop"), WT("n22", word), 0.7)
    TA.place(fx, TA.sfx("riser_fast"), E["n24"] - 0.7, 0.6)
    TA.place(fx, TA.sfx("pop"), E["n24"] + 0.02, 1.0)
    TA.place(fx, TA.sfx("sparkle"), E["n24"] + 0.05, 0.7)
    fx = fx[:n]
    mus = mus[:n]
    bed = desert_bed(n)
    cut(mus, E["n15"] + 0.05, t_rev + 0.05)          # silence before the answer
    cut(bed, E["n15"] + 0.05, t_rev - 0.05)
    for key, lvl in P.NOPES.items():
        cut(mus, L[key] - 0.12, E[key] + (0.2, 0.35, 0.9)[lvl - 1])
        cut(bed, L[key] - 0.12, E[key] + 0.05)
    vsr, v = wavfile.read(os.path.join(OUT, "cys03_voice.wav"))
    v = v.astype(np.float32) / 32768
    if vsr != SR:
        from scipy import signal
        v = signal.resample_poly(v, SR, vsr).astype(np.float32)
    v = np.pad(v, (0, max(0, n - len(v))))[:n]
    # NOPE 3 a little louder, so it lands at least 3 dB above NOPE 2 on the final mix
    a_, b_ = int((L["n19"] - 0.05) * SR), int((E["n19"] + 0.1) * SR)
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
    bed *= vr * 10 ** (-26 / 20) / rms(bed)
    talk = np.convolve((np.abs(v) > 0.02).astype(np.float32), np.ones(int(0.3 * SR)) / (0.3 * SR), mode="same")
    duck_ = (1 - 0.5 * np.clip(talk * 1.5, 0, 1))[:, None]
    mus *= duck_
    bed *= duck_
    mix = voice + mus + fx + bed
    mix = mix / (np.abs(mix).max() or 1) * 0.89
    wav = os.path.join(OUT, "cys03_audio.wav")
    wavfile.write(wav, SR, (mix * 32767).astype(np.int16))
    lv = []
    for key in P.NOPES:
        seg = v[int(L[key] * SR):int(E[key] * SR)]
        lv.append(20 * math.log10(float(np.sqrt((seg ** 2).mean())) + 1e-9))
    print("NOPE levels (dB):", [round(x, 1) for x in lv])
    if mixgate:
        mono = mix.mean(axis=1)
        wavfile.write(os.path.join(OUT, "cys03mix_voice.wav"), SR, (mono * 32767).astype(np.int16))
        shutil.copy(os.path.join(OUT, "cys03_lines.json"), os.path.join(OUT, "cys03mix_lines.json"))
    vid = os.path.join(OUT, "cys03_pic_video.mp4")
    dst = os.path.join(OUT, "SubjectZero_CYS03_DeathValley.mp4")
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
