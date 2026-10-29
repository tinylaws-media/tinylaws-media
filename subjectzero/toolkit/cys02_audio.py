"""COULD YOU SURVIVE? #02 — Everest: the soundtrack. Our own tune for the high mountains (E minor pentatonic, 88 BPM:
a breathy bamboo-flute lead, singing-bowl drones, a low pluck bass, a frame drum), a wind bed that roars on the wind
line, the effects on the story beats, the three voices on top. Nothing to license.

    python3 cys02_audio.py      -> out/cys02_audio.wav, then out/SubjectZero_CYS02_Everest.mp4 (-14 LUFS)
    python3 cys02_audio.py --mixgate   also writes out/cys02mix_voice.wav + out/cys02mix_lines.json for listen.py
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
import cys02_pic as P       # noqa: E402

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
D = P.DURATION
BPM = 88
NBARS = 24                  # 24 bars = 65.45 s: the music ends on a bar line with the respawn flash
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(2)


def t_(d):
    return np.arange(int(d * SR)) / SR


def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


def flute(f, d, v=1.0):
    """A breathy bamboo flute: sine + a little 2nd and 3rd, delayed vibrato, a puff of breath at the attack."""
    tt = t_(d)
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.2 * tt) * np.minimum(1, tt / 0.35)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    x = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)
    breath = TA.bp(TA.noise(d), f * 0.8, min(9000, f * 4)) * 0.18
    env = np.minimum(1, tt / 0.06) * np.minimum(1, (d - tt) / 0.12) * (0.85 + 0.15 * np.exp(-tt * 3))
    x = (x + breath) * env
    x[: int(0.05 * SR)] += TA.bp(TA.noise(0.05), 1500, 6000) * 0.25 * np.linspace(1, 0, int(0.05 * SR))
    return x * v


def bowl(f, d=4.0, v=1.0):
    """A singing bowl: inharmonic partials with slow beating."""
    tt = t_(d)
    x = np.zeros_like(tt)
    for r, a, dec in ((1.0, 1.0, 0.6), (2.76, 0.45, 1.0), (5.40, 0.2, 1.6), (8.93, 0.08, 2.4)):
        x += a * np.sin(2 * np.pi * f * r * tt) * (1 + 0.15 * np.sin(2 * np.pi * 0.9 * tt)) * np.exp(-tt * dec)
    return x * np.minimum(1, tt / 0.01) * v


def frame_drum(v=1.0):
    tt = t_(0.5)
    f = 70 + 50 * np.exp(-tt * 25)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7)
    x += TA.lp(TA.noise(0.5), 1200) * np.exp(-tt * 40) * 0.4
    return x * v


def woodblock(v=1.0, f=1400):
    tt = t_(0.08)
    return (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 70) + 0.4 * np.sin(2 * np.pi * f * 2.7 * tt) * np.exp(-tt * 110)) * v


def taiko(v=1.0):
    tt = t_(0.7)
    f = 52 + 70 * np.exp(-tt * 18)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 5)
    x += TA.lp(TA.noise(0.7), 900) * np.exp(-tt * 30) * 0.5
    return x * v


SCALE = [64, 67, 69, 71, 74, 76, 79, 81]       # E minor pentatonic
MOTIF = [(0, 3, 1.0), (1, 4, 0.5), (1.5, 3, 0.5), (2, 1, 1.5)]              # beat, step, length (beats)
MOTIF_B = [(0, 2, 0.5), (0.5, 3, 0.5), (1, 5, 1.5), (3, 4, 1.0)]
SEA_MOTIF = [(0, 5, 1.0), (1, 4, 1.0), (2, 2, 2.0)]


def music():
    n = int(D * SR) + 2 * SR
    out = np.zeros((n, 2))
    t_deep = P.L["n20"] - 0.05          # deep time: the old sea
    t_deep_end = P.L["n21"]
    for b in range(NBARS):
        t0 = b * BAR
        deep = t_deep - BAR * 0.5 <= t0 < t_deep_end
        roots = [40, 36, 38, 40] if not deep else [36, 38, 35, 36]
        root = roots[b % 4]
        for beat, m in ((0, root), (2.5, root + 7)):
            TA.place(out, TA.bass_note(m, BEAT * 1.8, 0.5), t0 + beat * BEAT, 1.0)
        if b % 2 == 0:
            TA.place(out, bowl(midi(root + 24), 2 * BAR, 0.16), t0, 1.0, pan=-0.2)
        if b >= 1:
            mot = SEA_MOTIF if deep else (MOTIF if b % 2 else MOTIF_B)
            for beat, step, ln in mot:
                st = step + (1 if (b // 4) % 2 and not deep else 0)
                TA.place(out, flute(midi(SCALE[min(len(SCALE) - 1, st)]), ln * BEAT * 0.95, 0.20), t0 + beat * BEAT, 1.0,
                         pan=0.15)
        for k in range(4):
            tb = t0 + k * BEAT
            if deep:
                if k == 0:
                    TA.place(out, taiko(0.7), tb, 1.0)
            else:
                if k in (0, 2) and b >= 1:
                    TA.place(out, frame_drum(0.55 if k == 0 else 0.4), tb, 1.0)
                if k in (1, 3) and b >= 2:
                    TA.place(out, woodblock(0.22), tb + BEAT / 2, 1.0, pan=0.3)
    out = out[: int(NBARS * BAR * SR)]
    return np.pad(out, ((0, n - len(out)), (0, 0)))


def wind_bed(n):
    """High-altitude wind: band noise with a slow swell; it roars on the wind line, eases off after."""
    tt = np.arange(n) / SR
    x = TA.bp(TA.noise(n / SR), 250, 2200)[:n]
    sw = 0.5 + 0.5 * np.sin(2 * np.pi * 0.23 * tt) * np.sin(2 * np.pi * 0.07 * tt + 1)
    lvl = np.full(n, 0.35)
    a, b = P.WT("n9", "wind"), P.L["n13"]
    lvl += 0.65 * np.clip((tt - (a - 0.3)) / 0.8, 0, 1) * np.clip((b - tt) / 0.6, 0, 1)
    for s_, e_ in ((P.shot_start("jars"), P.L["n4"] - 0.1), (P.shot_start("climb"), P.L["n6"] - 0.35),
                   (P.shot_start("gauge"), P.L["n19"] - 0.05), (P.shot_start("strata"), P.L["n21"] - 0.15)):
        lvl *= 1 - 0.7 * ((tt >= s_) & (tt < e_))       # quieter inside the insert shots
    y = x * sw * lvl
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


def avalanche_fx(v=1.0, d=2.2):
    tt = t_(d)
    x = TA.lp(TA.noise(d), 700) * np.minimum(1, tt / 0.3) * np.exp(-np.maximum(0, tt - 0.8) * 2.5)
    x += 0.5 * np.sin(2 * np.pi * 42 * tt) * np.exp(-tt * 1.5)
    return x * v


def sea_wash(v=1.0, d=1.6):
    tt = t_(d)
    return TA.bp(TA.noise(d), 200, 3000) * np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 2 * v


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
    # spawn: a crunch into the snow
    TA.place(fx, TA.sfx("crunch"), 0.0, 0.8)
    TA.place(fx, TA.sfx("pop"), 0.02, 0.6)
    # the altitude counts up: blips rising
    a, b = P.T_ALT0, P.T_ALT1
    for i in range(10):
        TA.place(fx, TA.blip(72 + i * 2, 0.05, 0.22), a + (b - a) * i / 10, 1.0)
    TA.place(fx, TA.sfx("ding"), b, 0.5)
    # jars: whoosh in, the oxygen dots leave one by one, stamp on "third"
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("jars") - 0.08, 0.6)
    t3 = WT("n3", "third")
    for i in range(10):
        TA.place(fx, TA.sfx("pop"), t3 - 0.6 + 0.09 * i, 0.25, pan=0.3)
    TA.place(fx, TA.sfx("stamp"), t3, 0.9)
    # the lab: squelch before each line
    for k in P.KEYS:
        if P.WHO[k] == "LAB":
            TA.place(fx, radio(0.7), L[k] - 0.22, 1.0, pan=0.4)
    # climb chart: the line is drawn, then she goes straight up, stamp
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("climb") - 0.05, 0.6)
    TA.place(fx, TA.sfx("scribble"), L["n5"] + 0.15, 0.5)
    TA.place(fx, TA.sfx("boing_up"), WT("n5", "zero") - 0.35, 0.5)
    TA.place(fx, TA.sfx("stamp"), WT("n5", "zero"), 0.9)
    # wide: whoosh, the thermometer drops, glass on the stamp
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("wide") - 0.05, 0.6)
    TA.place(fx, TA.sfx("whoosh_down"), P.shot_start("wide") + 0.3, 0.4)
    TA.place(fx, TA.sfx("glass"), WT("n7", "−36") + 0.02, 0.5)
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("close", 3) - 0.05, 0.5)
    # timer: ticks of the hourglass, stamp
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("timer") - 0.05, 0.6)
    t = P.shot_start("timer") + 0.2
    while t < P.shot_start("close", 4) - 0.1:
        TA.place(fx, TA.sfx("tick"), t, 0.25, pan=-0.4)
        t += 0.5
    TA.place(fx, TA.sfx("stamp"), WT("n11", "5"), 0.9)
    # the duck
    TA.place(fx, squeak(0.5), L["n13"] + 0.1, 1.0, pan=0.2)
    TA.place(fx, TA.sfx("stamp"), WT("n13", "air"), 0.8)
    # the tease: she taps her head; something glints under the snow
    TA.place(fx, TA.sfx("tap"), L["n15"] + 0.2, 0.7)
    TA.place(fx, TA.sfx("sparkle"), WT("n15", "rock") - 0.1, 0.6)
    # gauge: whoosh, drumroll while it hunts, silence, stamp on the answer
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("gauge") - 0.08, 0.6)
    t_rev = WT("n17", "about")
    TA.place(fx, drumroll(max(0.4, t_rev - 0.4 - (L["n16"] + 0.3))), L["n16"] + 0.3, 0.8)
    TA.place(fx, TA.sfx("stamp"), t_rev, 1.2)
    # dizzy
    TA.place(fx, TA.sfx("dizzy"), L["n19"] + 0.2, 0.5)
    # strata: down into the rock, the old sea comes back, the zoom, stamps
    TA.place(fx, TA.sfx("whoosh_down"), P.shot_start("strata") - 0.05, 0.7)
    TA.place(fx, TA.sfx("paper"), L["n20"] + 0.1, 0.5)
    t_sea = WT("n20", "seafloor") - 0.3
    TA.place(fx, sea_wash(0.6), t_sea - 0.3, 1.0)
    TA.place(fx, TA.sfx("stamp"), t_sea + 0.2, 0.8)
    TA.place(fx, TA.sfx("whoosh"), L["n20b"] + 0.2, 0.5)
    TA.place(fx, TA.sfx("stamp"), WT("n20b", "400"), 0.9)
    # the NOPEs: the word first, clean; the damage lands as it ends
    for key, lvl in P.NOPES.items():
        hit = E[key] + 0.02
        if lvl == 1:              # the cornice snaps and drops
            TA.place(fx, boom(0.3, 0.9), hit, 1.0)
            TA.place(fx, TA.sfx("crack"), hit + 0.02, 0.7)
            TA.place(fx, TA.sfx("fall"), hit + 0.15, 0.5)
        elif lvl == 2:            # an avalanche on the next face
            TA.place(fx, boom(0.6, 1.2), hit, 1.0)
            TA.place(fx, avalanche_fx(0.55, 1.6), hit + 0.1, 1.0, pan=-0.4)
        else:                     # the snow cap blows off the summit
            for i in (0, 1):
                TA.place(fx, boom(0.18 + 0.1 * i, 0.22), P.W3[i + 1] - 0.14, 1.0)
            TA.place(fx, boom(1.15, 1.0), hit, 1.0)
            TA.place(fx, TA.sfx("crunch"), hit + 0.03, 1.0)
            TA.place(fx, TA.sfx("whoosh"), P.T_BLAST3 + 0.15, 0.8)
            TA.place(fx, squeak(0.6, up=True), hit + 0.3, 1.0, pan=0.5)
            TA.place(fx, TA.sfx("sparkle"), P.T_BLAST3 + 1.25, 0.7)
    # the end: the three choices, the countdown, the respawn
    for word in ("Pompeii", "Mariana", "Moon"):
        TA.place(fx, TA.sfx("pop"), WT("n22", word), 0.7)
    TA.place(fx, TA.sfx("riser_fast"), E["n24"] - 0.7, 0.6)
    TA.place(fx, TA.sfx("pop"), E["n24"] + 0.02, 1.0)
    TA.place(fx, TA.sfx("sparkle"), E["n24"] + 0.05, 0.7)
    fx = fx[:n]
    mus = mus[:n]
    wind = wind_bed(n)
    cut(mus, t_rev - 0.45, t_rev + 0.05)
    for key, lvl in P.NOPES.items():
        cut(mus, L[key] - 0.12, E[key] + (0.2, 0.35, 0.9)[lvl - 1])
        cut(wind, L[key] - 0.12, E[key] + 0.05)
    vsr, v = wavfile.read(os.path.join(OUT, "cys02_voice.wav"))
    v = v.astype(np.float32) / 32768
    if vsr != SR:
        from scipy import signal
        v = signal.resample_poly(v, SR, vsr).astype(np.float32)
    v = np.pad(v, (0, max(0, n - len(v))))[:n]
    # NOPE 2 a little louder, so each NOPE is at least 3 dB above the one before
    a, b = int((L["n12"] - 0.05) * SR), int((E["n12"] + 0.1) * SR)
    gain = np.ones(n, np.float32)
    gain[a:b] = 10 ** (1.0 / 20)
    v = v * np.convolve(gain, np.ones(240) / 240, mode="same")
    voice = np.stack([v, v], 1)

    def rms(x):
        a = np.abs(x).mean(axis=1) if x.ndim > 1 else np.abs(x)
        m = a > 0.01
        return float(np.sqrt((x[m] ** 2).mean())) if m.any() else 1e-6
    vr = rms(voice)
    mus *= vr * 10 ** (-15 / 20) / rms(mus)
    fx *= vr * 10 ** (-12 / 20) / rms(fx)
    wind *= vr * 10 ** (-24 / 20) / rms(wind)
    talk = np.convolve((np.abs(v) > 0.02).astype(np.float32), np.ones(int(0.3 * SR)) / (0.3 * SR), mode="same")
    duck_ = (1 - 0.5 * np.clip(talk * 1.5, 0, 1))[:, None]
    mus *= duck_
    wind *= duck_
    mix = voice + mus + fx + wind
    mix = mix / (np.abs(mix).max() or 1) * 0.89
    wav = os.path.join(OUT, "cys02_audio.wav")
    wavfile.write(wav, SR, (mix * 32767).astype(np.int16))
    # NOPE loudness check: each one at least 3 dB above the one before
    lv = []
    for key in P.NOPES:
        seg = v[int(L[key] * SR):int(E[key] * SR)]
        lv.append(20 * math.log10(float(np.sqrt((seg ** 2).mean())) + 1e-9))
    print("NOPE levels (dB):", [round(x, 1) for x in lv])
    if mixgate:
        mono = mix.mean(axis=1)
        wavfile.write(os.path.join(OUT, "cys02mix_voice.wav"), SR, (mono * 32767).astype(np.int16))
        shutil.copy(os.path.join(OUT, "cys02_lines.json"), os.path.join(OUT, "cys02mix_lines.json"))
    vid = os.path.join(OUT, "cys02_pic_video.mp4")
    dst = os.path.join(OUT, "SubjectZero_CYS02_Everest.mp4")
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
