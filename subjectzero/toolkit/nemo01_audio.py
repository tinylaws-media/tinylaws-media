"""COULD YOU SURVIVE? #01 — the soundtrack: our own tune (plucked koto-like synth, woodblock, soft bass; nothing to
license), the effects on the story beats, the three voices on top.

    python3 nemo01_audio.py      -> out/nemo01_audio.wav, then out/SubjectZero_CYS01_PointNemo.mp4 (-14 LUFS)
"""
import json
import math
import os
import subprocess
import sys

import numpy as np
from scipy import signal
from scipy.io import wavfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tl_audio as TA       # noqa: E402  synth effects shared with Tiny Laws (pop, tick, stamp, whoosh, sparkle...)
import nemo01_pic as P      # noqa: E402  the picture's timings

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
D = P.DURATION
BPM = 97.5                  # 27 bars = 66.46 s: the music ends on a bar line with the respawn flash
NBARS = 27
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(1)


def t_(d):
    return np.arange(int(d * SR)) / SR


def pluck(f, d=1.2, v=1.0, bright=0.5):
    """Karplus-Strong string: a koto-ish pluck."""
    n = int(d * SR)
    p = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, p)
    buf = signal.lfilter([bright, 1 - bright], [1], buf)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.996 * 0.5 * (buf[i % p] + buf[(i + 1) % p])
    return out * v


def woodblock(v=1.0, f=1600):
    tt = t_(0.08)
    x = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 70) + 0.4 * np.sin(2 * np.pi * f * 2.7 * tt) * np.exp(-tt * 110)
    return x * v


def taiko(v=1.0):
    tt = t_(0.7)
    f = 52 + 70 * np.exp(-tt * 18)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 5)
    x += TA.lp(TA.noise(0.7), 900) * np.exp(-tt * 30) * 0.5
    return x * v


def shaker(v=1.0):
    return TA.hp(TA.noise(0.06), 5000) * TA.env(int(0.06 * SR), 0.01, 0.05) * v


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


def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


MAJ = [62, 64, 66, 69, 71, 74, 76, 78, 81]       # D major pentatonic
MIN = [59, 62, 64, 66, 69, 71, 74, 76]           # B minor pentatonic
MOTIF = [(0, 4), (0.5, 3), (1, 5), (1.5, 4), (2, 2), (3, 3), (3.5, 1)]     # beat, scale step
MOTIF_B = [(0, 5), (0.5, 6), (1, 5), (2, 3), (2.5, 4), (3, 2)]
DUCK_MOTIF = [(0, 6), (0.25, 7), (0.5, 8), (1.5, 6), (2, 7)]


def music():
    n = int(D * SR) + 2 * SR
    out = np.zeros((n, 2))
    nbars = NBARS
    t_drama = P.L["n20"] - 0.05
    t_dend = P.L["n23"]
    for b in range(nbars):
        t0 = b * BAR
        dark = t_drama <= t0 < t_dend
        duck = P.L["n18"] - 0.1 <= t0 < P.L["n20"] - 0.05
        scale = MIN if dark else MAJ
        roots = [50, 47, 43, 45] if not dark else [47, 43, 45, 42]
        root = roots[b % 4]
        # bass: root on 1, fifth on 3
        for beat, m in ((0, root), (2, root + 7)):
            x = TA.bass_note(m - 12, BEAT * 1.6, 0.55)
            TA.place(out, x, t0 + beat * BEAT, 1.0)
        # melody: the motif, varied every other bar
        if b >= 1:
            mot = DUCK_MOTIF if duck else (MOTIF if b % 2 else MOTIF_B)
            for beat, step in mot:
                st = step + (1 if (b // 2) % 2 and not dark else 0)
                m = scale[min(len(scale) - 1, st)]
                TA.place(out, pluck(midi(m), 1.0, 0.32, 0.45 if not dark else 0.7), t0 + beat * BEAT, 1.0,
                         pan=-0.3 if beat % 1 else 0.3)
        # percussion
        for k in range(4):
            tb = t0 + k * BEAT
            if dark:
                if k in (0, 2):
                    TA.place(out, taiko(0.9 if k == 0 else 0.6), tb, 1.0)
            else:
                if k in (1, 3):
                    TA.place(out, woodblock(0.35), tb, 1.0, pan=0.2)
                if b >= 2:
                    TA.place(out, shaker(0.18), tb + BEAT / 2, 1.0, pan=-0.4)
        if dark:     # a low drone under the graveyard
            dd = BAR
            tt = t_(dd)
            dr = sum(np.sin(2 * np.pi * midi(root - 12) * r * tt) for r in (1, 1.5, 2.0)) / 3
            TA.place(out, dr * 0.12 * np.minimum(1, tt / 0.3) * np.minimum(1, (dd - tt) / 0.3), t0, 1.0)
    out = out[: int(NBARS * BAR * SR)]
    out = np.pad(out, ((0, n - len(out)), (0, 0)))
    return out


def cut(mus, a, b, fade=0.04):
    i, j = int(a * SR), int(b * SR)
    f = int(fade * SR)
    mus[i:j] = 0
    if i - f > 0:
        mus[i - f:i] *= np.linspace(1, 0, f)[:, None]
    if j + f < len(mus):
        mus[j:j + f] *= np.linspace(0, 1, f)[:, None]


def splash_fx(v=1.0, d=0.6):
    tt = t_(d)
    x = TA.bp(TA.noise(d), 300, 5000) * np.exp(-tt * 7) * np.minimum(1, tt / 0.01)
    for _ in range(6):
        t0 = rng.uniform(0.05, d * 0.7)
        f = rng.uniform(900, 2200)
        dt = t_(0.05)
        drop = np.sin(2 * np.pi * np.cumsum(np.geomspace(f, f * 1.8, len(dt))) / SR) * np.exp(-dt * 60) * 0.4
        i = int(t0 * SR)
        x[i:i + len(drop)] += drop[: len(x) - i]
    return x * v


def boom(v=1.0, d=1.6):
    tt = t_(d)
    f = 34 + 60 * np.exp(-tt * 6)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.2)
    x += TA.lp(TA.noise(d), 400) * np.exp(-tt * 4) * 0.8
    return np.tanh(x * 1.5) * v


def radio(v=1.0):
    """The lab's intercom: a squelch and a short beep."""
    tt = t_(0.12)
    beep = np.sin(2 * np.pi * 1250 * tt) * (tt < 0.07) * 0.5
    sq = TA.bp(TA.noise(0.12), 1500, 5000) * np.exp(-tt * 30) * 0.6
    return (beep + sq) * v


def squeak(v=1.0, up=True):
    """Rubber duck."""
    tt = t_(0.22)
    f = np.geomspace(1100, 2100, len(tt)) if up else np.geomspace(2000, 1300, len(tt))
    vib = 1 + 0.04 * np.sin(2 * np.pi * 38 * tt)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f * vib) / SR)) * 0.3 + np.sin(2 * np.pi * np.cumsum(f * vib) / SR) * 0.5
    x = TA.lp(x, 4000) * np.minimum(1, tt / 0.01) * np.exp(-tt * 6)
    return x * v


def whistle_down(d=1.2, v=1.0):
    tt = t_(d)
    f = np.geomspace(2400, 500, len(tt))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 + TA.bp(TA.noise(d), 800, 3000) * 0.5
    return x * np.minimum(1, tt / 0.2) * v


def build():
    n = int(D * SR)
    mus = music()[:n + SR]
    fx = np.zeros((n + 2 * SR, 2))
    L, E, WT = P.L, P.E, P.WT
    # spawn
    TA.place(fx, splash_fx(1.0), 0.0, 1.0)
    TA.place(fx, TA.sfx("pop"), 0.0, 0.8)
    # map: whoosh in, circle draws, pins pop
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("map") - 0.1, 0.7)
    TA.place(fx, TA.sfx("scribble"), L["n3"] + 0.2, 0.5)
    for name, _, key, word, _ in P.PLACES:
        TA.place(fx, TA.sfx("pop"), WT(key, word), 0.8)
    # tilt up, the station, "400 km"
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("sky") - 0.05, 0.7)
    TA.place(fx, TA.sfx("sparkle"), WT("n5", "space"), 0.6)
    TA.place(fx, TA.sfx("stamp"), WT("n5", "space") + 0.35, 0.7)
    # the lab speaks: squelch before each line
    for k in P.KEYS:
        if P.WHO[k] == "LAB":
            TA.place(fx, radio(0.7), L[k] - 0.22, 1.0, pan=0.4)
    # cold: a shiver of ice, the gasp
    TA.place(fx, TA.sfx("glass"), L["n8"] + 0.3, 0.4)
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("close", 1) - 0.05, 0.5)
    TA.place(fx, TA.sfx("boing_up"), P.T_GASP - 0.05, 0.5)
    # the clock ticks while it runs
    t = L["n9"]
    while t < L["n16"]:
        TA.place(fx, TA.sfx("tick"), t, 0.18, pan=-0.5)
        t += 0.5
    # swim: splashes on the strokes; the duck zips past; on the chart the days fly by, one tick a day
    t = L["n11"] + 0.2
    while t < P.T_GO:
        TA.place(fx, splash_fx(0.35, 0.3), t, 1.0, pan=0.3 * math.sin(t * 7))
        t += 0.42
    TA.place(fx, TA.sfx("whoosh"), P.T_DUCK_PASS[0], 0.45, pan=-0.3)
    TA.place(fx, squeak(0.4, up=True), P.T_DUCK_PASS[0] + 0.15, 1.0, pan=-0.4)
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("swim_map") - 0.05, 0.6)
    for d in range(18):
        TA.place(fx, TA.sfx("tick"), P.T_GO + (P.T_18 - P.T_GO) * d / 18, 0.35, pan=0.3)
    TA.place(fx, TA.sfx("stamp"), P.T_18, 1.0)
    # half underwater: a dip, the bubbles; the strike sign
    TA.place(fx, splash_fx(0.5, 0.5), P.shot_start("under") - 0.05, 1.0)
    TA.place(fx, TA.sfx("whoosh_down"), P.shot_start("under"), 0.5)
    TA.place(fx, TA.sfx("pop"), P.T_ARMS + 0.05, 0.8)
    # the big clock slams in
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("clock") - 0.08, 0.6)
    TA.place(fx, TA.sfx("glass"), P.shot_start("clock") + 0.05, 0.35)
    # the NOPEs: bigger each time
    for key, lvl in P.NOPES.items():
        # the word first, clean; the damage lands as it ends (an effect on top of a word masks it)
        hit = P.E[key] + 0.02
        if lvl == 3:
            # the two small ones between the words, then the big one
            for i in (0, 1):      # short and between the words, so the next "nope" stays clear
                TA.place(fx, boom(0.18 + 0.1 * i, 0.22), P.W3[i + 1] - 0.14, 1.0)
            TA.place(fx, boom(1.15, 1.0), hit, 1.0)          # short: it must not sit under the next line
            TA.place(fx, splash_fx(1.3, 1.1), hit + 0.05, 1.0)
            TA.place(fx, TA.sfx("crack"), hit + 0.1, 0.8)
            TA.place(fx, squeak(0.6, up=True), hit + 0.3, 1.0, pan=0.5)
            TA.place(fx, TA.sfx("whoosh"), P.T_BLAST3 + 0.15, 0.7)
            TA.place(fx, TA.sfx("sparkle"), P.T_BLAST3 + 1.25, 0.8)
        else:
            TA.place(fx, boom(0.3 * lvl, 0.6 + 0.5 * lvl), hit, 1.0)
            TA.place(fx, splash_fx(0.35 + 0.3 * lvl, 0.4 + 0.3 * lvl), hit + 0.05, 1.0)
    # arms give up
    TA.place(fx, TA.sfx("boing_down"), P.T_ARMS - 0.1, 0.5)
    # the wait for the answer: a drumroll, silence, the hit
    TA.place(fx, drumroll(P.T_REVEAL - 0.35 - L["n16"] - 0.6), L["n16"] + 0.6, 0.9)
    TA.place(fx, TA.sfx("stamp"), P.T_REVEAL, 1.2)
    # the duck
    TA.place(fx, squeak(0.6), L["n18"] + 0.15, 1.0, pan=0.2)
    TA.place(fx, TA.sfx("stamp"), WT("n18", "floated"), 0.9)
    TA.place(fx, TA.sfx("tap"), L["n19"] + 0.05, 0.8)
    # the graveyard: whistles and splashes
    a = P.shot_start("graveyard")
    for (d0, x0, y0, x1, y1, w_) in P.FALLERS:
        st = a + 0.2 + d0
        g = 0.5 if 48.3 <= st + 0.6 <= 51.1 else 1.0      # -6 dB under "Look up: spacecraft come here to die"
        hole = (P.E["n20"] - 0.55, P.E["n20"] + 0.15)       # nothing lands on "die": it is the punchline
        if not hole[0] - 0.6 <= st <= hole[1]:
            TA.place(fx, whistle_down(1.2, (0.18 + 0.006 * w_) * g), st, 1.0, pan=(x1 - 540) / 540)
        if not hole[0] - 0.3 <= st + 1.2 <= hole[1]:
            TA.place(fx, splash_fx((0.25 + 0.012 * w_) * g, 0.5), st + 1.2, 1.0, pan=(x1 - 540) / 540)
    TA.place(fx, TA.sfx("whoosh_down"), L["n21"] - 0.2, 0.6)
    TA.place(fx, TA.sfx("stamp"), WT("n22", "2030"), 0.9)
    TA.place(fx, TA.sfx("riser"), L["n23"] - 1.5, 0.6)
    # the end: the three choices, the countdown, the respawn
    for word in ("Sahara", "Ancient", "Everest"):
        TA.place(fx, TA.sfx("pop"), WT("n24", word), 0.7)
    TA.place(fx, TA.sfx("riser_fast"), E["n25"] - 0.7, 0.6)
    TA.place(fx, TA.sfx("pop"), E["n25"] + 0.02, 1.0)
    TA.place(fx, TA.sfx("sparkle"), E["n25"] + 0.05, 0.7)
    fx = fx[:n]
    mus = mus[:n]
    # music: out for the silence before the answer, out under each NOPE
    cut(mus, P.T_REVEAL - 0.45, P.T_REVEAL + 0.05)
    for key, lvl in P.NOPES.items():
        cut(mus, L[key] - 0.12, P.E[key] + (0.2, 0.35, 0.9)[lvl - 1])     # silence first: the word lands in it
    vsr, v = wavfile.read(os.path.join(OUT, "nemo01_voice.wav"))
    v = v.astype(np.float32) / 32768
    v = np.pad(v, (0, max(0, n - len(v))))[:n]
    # NOPE 2 a little louder, so each NOPE is at least 3 dB above the one before (-21.2, -17.7, -13.8 dB)
    a, b = int((L["n15"] - 0.05) * SR), int((E["n15"] + 0.1) * SR)
    gain = np.ones(n, np.float32)
    gain[a:b] = 10 ** (1.0 / 20)
    gain = np.convolve(gain, np.ones(240) / 240, mode="same")
    v = v * gain
    voice = np.stack([v, v], 1)

    def rms(x):
        a = np.abs(x).mean(axis=1) if x.ndim > 1 else np.abs(x)
        m = a > 0.01
        return float(np.sqrt((x[m] ** 2).mean())) if m.any() else 1e-6
    vr = rms(voice)
    mus *= vr * 10 ** (-15 / 20) / rms(mus)
    fx *= vr * 10 ** (-12 / 20) / rms(fx)
    talk = np.convolve((np.abs(v) > 0.02).astype(np.float32), np.ones(int(0.3 * SR)) / (0.3 * SR), mode="same")
    mus *= (1 - 0.5 * np.clip(talk * 1.5, 0, 1))[:, None]
    mix = voice + mus + fx
    mix = mix / (np.abs(mix).max() or 1) * 0.89
    wav = os.path.join(OUT, "nemo01_audio.wav")
    wavfile.write(wav, SR, (mix * 32767).astype(np.int16))
    vid = os.path.join(OUT, "nemo01_pic_video.mp4")
    dst = os.path.join(OUT, "SubjectZero_CYS01_PointNemo.mp4")
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
    build()
