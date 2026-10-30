"""COULD YOU SURVIVE? #05 — Mars, no suit: the soundtrack. Our own tune for the red plain (E minor, 99 BPM: a glassy
mallet playing a slow arpeggio, a theremin-like sine lead with wide vibrato for the "alien" feel, a low drone pad, a
soft kick on 1 and 3 and dry ticks on the off-beats; the sunset section drops to the mallet and the lead alone, in
E major for the blue light), a thin Martian wind bed, the effects on the story beats, the three voices on top.
Nothing to license.

    python3 cys05_audio.py      -> out/cys05_audio.wav, then out/SubjectZero_CYS05_Mars.mp4 (-14 LUFS)
    python3 cys05_audio.py --mixgate   also writes out/cys05mix_voice.wav + out/cys05mix_lines.json for listen.py
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
import cys05_pic as P       # noqa: E402

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
D = P.DURATION
BPM = 99
NBARS = 27                  # 27 bars = 65.45 s: the music ends on a bar line with the respawn flash
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(5)


def t_(d):
    return np.arange(int(d * SR)) / SR


def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


def mallet(f, d, v=1.0):
    """A glassy mallet: a sine with a bright inharmonic partial and a fast decay."""
    tt = t_(d)
    x = np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * f * 3.98 * tt) * np.exp(-tt * 18)
    x += 0.15 * np.sin(2 * np.pi * f * 2 * tt) * np.exp(-tt * 6)
    return x * np.exp(-tt * 3.2) * np.minimum(1, tt / 0.004) * v


def theremin(f, d, v=1.0):
    """A sine lead with wide, slow vibrato and a glide in from below."""
    tt = t_(d)
    glide = 1 - 0.03 * np.exp(-tt * 12)
    vib = 1 + 0.012 * np.sin(2 * np.pi * 5.2 * tt) * np.minimum(1, tt / 0.25)
    ph = 2 * np.pi * np.cumsum(f * glide * vib) / SR
    x = np.sin(ph) + 0.12 * np.sin(2 * ph)
    return x * np.minimum(1, tt / 0.08) * np.minimum(1, (d - tt) / 0.15) * v


def pad(f, d, v=1.0):
    tt = t_(d)
    x = sum(np.sin(2 * np.pi * f * k * (1 + 0.002 * j) * tt) / k for j, k in enumerate((1, 2, 3)))
    x += 0.5 * np.sin(2 * np.pi * f * 1.003 * tt)
    return TA.lp(x, 900) * np.minimum(1, tt / 0.6) * np.minimum(1, (d - tt) / 0.6) * v


def kick(v=1.0):
    tt = t_(0.35)
    f = 48 + 90 * np.exp(-tt * 35)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 10) * v


def tick_hat(v=1.0):
    tt = t_(0.05)
    return TA.hp(TA.noise(0.05), 6000) * np.exp(-tt * 90) * v


EM = [52, 55, 59, 62, 64, 66, 67, 71, 74, 76]        # E minor-ish from E3
CHORDS = [(40, (0, 2, 4)), (36, (1, 3, 5)), (43, (1, 2, 4)), (38, (3, 5, 7))]   # Em  C  G  D (bass, steps)
LEAD = [(0, 7, 1.5), (1.5, 6, 0.5), (2, 4, 2.0)]
LEAD_B = [(0, 4, 1.0), (1, 5, 1.0), (2, 7, 1.5), (3.5, 8, 0.5)]
MAJ = [52, 56, 59, 63, 64, 66, 68, 71, 75, 76]       # E major for the blue sunset


def music():
    n = int(D * SR) + 2 * SR
    out = np.zeros((n, 2))
    t_sun = P.L["n21"] - 0.1
    cache = {}
    for b in range(NBARS):
        t0 = b * BAR
        sun = t_sun - BAR * 0.5 <= t0 < P.L["n23"] - 0.3
        root, steps = CHORDS[b % 4]
        sc = MAJ if sun else EM
        if sun:
            root = (40, 45, 47, 40)[b % 4]
        TA.place(out, pad(midi(root), BAR * 1.02, 0.12), t0, 1.0)
        TA.place(out, TA.bass_note(root, BEAT * 1.8, 0.45), t0, 1.0)
        if not sun:
            TA.place(out, TA.bass_note(root + 7, BEAT * 1.2, 0.35), t0 + 2 * BEAT, 1.0)
        for k in range(8):                         # the mallet arpeggio in eighths
            st = steps[(0, 1, 2, 1)[k % 4]] + (2 if k >= 4 else 0)
            m = sc[min(st, len(sc) - 1)]
            key = (m, sun)
            if key not in cache:
                cache[key] = mallet(midi(m), 0.9)
            TA.place(out, cache[key] * (0.12 if k % 2 == 0 else 0.08), t0 + k * BEAT / 2, 1.0, pan=0.3 * (1 if k % 2 else -1))
        if b >= 2 and (b % 2 == 0 or sun):          # the theremin lead
            mot = LEAD if (b // 4) % 2 == 0 else LEAD_B
            for beat, step, ln in mot:
                TA.place(out, theremin(midi(sc[step] + 12), ln * BEAT * 0.95, 0.06), t0 + beat * BEAT, 1.0, pan=-0.15)
        if b >= 1 and not sun:
            for k in range(4):
                tb = t0 + k * BEAT
                if k in (0, 2):
                    TA.place(out, kick(0.55), tb, 1.0)
                TA.place(out, tick_hat(0.22), tb + BEAT / 2, 1.0, pan=0.35)
    out = out[: int(NBARS * BAR * SR)]
    return np.pad(out, ((0, n - len(out)), (0, 0)))


def mars_bed(n):
    """Thin Martian wind: a high, airy band of noise that swells slowly; quieter under the inserts; in space
    (the signal shot) nothing at all."""
    tt = np.arange(n) / SR
    gust = 0.4 + 0.6 * np.sin(2 * np.pi * 0.09 * tt) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.23 * tt + 1))
    y = TA.bp(TA.noise(n / SR), 600, 3500)[:n] * gust * 0.7
    y += TA.bp(TA.noise(n / SR), 1800, 2200)[:n] * gust ** 2 * 0.4
    for name in ("gauge", "co2", "lungs", "boil", "crater", "clock", "chamber", "horizon", "glow"):
        for nth in range(3):
            try:
                s_ = P.shot_start(name, nth)
            except IndexError:
                break
            y *= 1 - 0.7 * ((tt >= s_) & (tt < P.shot_end(s_)))
    a, b = P.shot_start("signal"), P.shot_end(P.shot_start("signal"))
    y *= 1 - 1.0 * ((tt >= a) & (tt < b))
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


def dust_whump(v=1.0, d=0.9):
    """Dust thrown off: a soft low thump and a long gritty hiss."""
    tt = t_(d)
    x = TA.lp(TA.noise(d), 240) * np.exp(-tt * 9) * 2.0
    x += TA.bp(TA.noise(d), 900, 5000) * np.minimum(1, tt / 0.03) * np.exp(-tt * 3.0) * 0.55
    return x * v


def metal_clank(v=1.0, d=0.8):
    """The lander's dish snapping off: a bright metallic hit with ringing partials."""
    tt = t_(d)
    x = sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * k) for f, k in ((523, 6), (1187, 8), (1931, 11), (2817, 14)))
    x += TA.hp(TA.noise(d), 2000) * np.exp(-tt * 40) * 1.5
    return x * 0.4 * v


def rockfall(v=1.0, d=1.8, n=18):
    """The mesa coming down: heavy stony thuds that speed up, a grinding rumble under them."""
    out = np.zeros(int(d * SR) + SR)
    t = 0.0
    for j in range(n):
        tt = t_(0.4)
        f = 60 + 50 * np.exp(-tt * 18)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 10) + TA.bp(TA.noise(0.4), 150, 1200) * np.exp(-tt * 14) * 0.8
        i = int(t * SR)
        out[i:i + len(x)] += x[: len(out) - i] * (0.5 + 0.03 * j)
        t += 0.1 - 0.003 * j
    out[: int(d * SR)] += TA.lp(TA.noise(d), 200) * np.sin(np.pi * t_(d) / d) * 0.8
    return out[: int(d * SR)] * v


def storm(v=1.0, d=2.0):
    tt = t_(d)
    return TA.bp(TA.noise(d), 300, 2500) * np.minimum(1, tt / 0.3) * np.exp(-tt * 1.2) * v


def bubbles(v=1.0, d=1.2, n=22):
    out = np.zeros(int(d * SR))
    for _ in range(n):
        t0 = rng.uniform(0, d - 0.08)
        tt = t_(0.06)
        f = rng.uniform(500, 1400) * (1 + 3 * tt)
        b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 70)
        i = int(t0 * SR)
        out[i:i + len(b)] += b * rng.uniform(0.3, 0.8)
    return out * v


def radio(v=1.0):
    tt = t_(0.12)
    beep = np.sin(2 * np.pi * 1250 * tt) * (tt < 0.07) * 0.5
    sq = TA.bp(TA.noise(0.12), 1500, 5000) * np.exp(-tt * 30) * 0.6
    return (beep + sq) * v


def blip(v=1.0, f=880):
    tt = t_(0.18)
    return np.sin(2 * np.pi * f * tt) * np.exp(-tt * 16) * v


def squeak(v=1.0, up=True):
    tt = t_(0.22)
    f = np.geomspace(1100, 2100, len(tt)) if up else np.geomspace(2000, 1300, len(tt))
    vib = 1 + 0.04 * np.sin(2 * np.pi * 38 * tt)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    x = np.sign(np.sin(ph)) * 0.3 + np.sin(ph) * 0.5
    return TA.lp(x, 4000) * np.minimum(1, tt / 0.01) * np.exp(-tt * 6) * v


def hiss(v=1.0, d=1.0):
    tt = t_(d)
    return TA.hp(TA.noise(d), 3000) * np.sin(np.pi * tt / d) * v


def build(mixgate=False):
    n = int(D * SR)
    mus = music()[:n + SR]
    fx = np.zeros((n + 2 * SR, 2))
    L, E, WT = P.L, P.E, P.WT
    # spawn: she lands in the dust
    TA.place(fx, dust_whump(0.35, 0.3), 0.0, 1.0)
    # gauge: whoosh in, the Mars column drains (a falling hiss), stamp on < 1 %
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("gauge") - 0.08, 0.6)
    TA.place(fx, TA.sfx("whoosh_down"), WT("n3", "1%") - 0.15, 0.5)
    TA.place(fx, TA.sfx("stamp"), WT("n3", "pressure") + 0.2, 0.7)
    # co2: the dots patter coral
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("co2") - 0.05, 0.5)
    for j in range(10):
        TA.place(fx, TA.sfx("tick", j), P.shot_start("co2") + 0.1 + 0.06 * j, 0.15)
    TA.place(fx, blip(0.25, 1760), P.shot_start("co2") + 0.95, 1.0, pan=0.3)
    # lungs: two balloons stretching (squeaks up), stamp
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("lungs") - 0.05, 0.5)
    TA.place(fx, squeak(0.35, True), P.shot_start("lungs") + 0.4, 1.0, pan=-0.3)
    TA.place(fx, squeak(0.35, True), P.shot_start("lungs") + 0.9, 1.0, pan=0.3)
    TA.place(fx, TA.sfx("stamp"), WT("n6", "tear") - 0.05, 0.8)
    # the lab
    for k in P.KEYS:
        if P.WHO[k] == "LAB":
            TA.place(fx, radio(0.7), L[k] - 0.22, 1.0, pan=0.4)
    # breathe out: a puff
    TA.place(fx, hiss(0.3, 0.5), L["n7"] + 0.6, 1.0)
    # boil: bubbles, stamps
    TA.place(fx, TA.sfx("whoosh"), P.shot_start("boil") - 0.05, 0.5)
    TA.place(fx, bubbles(0.5, 1.6), WT("n9", "boil") - 0.4, 1.0)
    TA.place(fx, TA.sfx("stamp"), WT("n9", "boil"), 0.7)
    TA.place(fx, bubbles(0.3, 2.0), P.shot_start("boil", 1), 1.0)
    TA.place(fx, TA.sfx("stamp"), WT("n11", "hot"), 0.7)
    TA.place(fx, TA.sfx("stamp"), WT("n11", "thin"), 0.5)
    # crater: she slides down (a scrape), the bar rises, x10 ding, FALLS SHORT thud
    TA.place(fx, TA.sfx("whoosh_down"), P.shot_start("crater") - 0.05, 0.5)
    TA.place(fx, TA.sfx("ding"), WT("n12", "10×"), 0.4)
    TA.place(fx, TA.sfx("riser"), WT("n12", "Even") - 0.2, 0.3)
    TA.place(fx, TA.sfx("boing_down"), WT("n12", "falls"), 0.4)
    TA.place(fx, TA.sfx("stamp"), WT("n12", "falls"), 0.8)
    # duck: squeak, stamp
    TA.place(fx, squeak(0.5), P.shot_start("duck") + 0.3, 1.0, pan=0.2)
    TA.place(fx, TA.sfx("stamp"), WT("n13", "breathe") - 0.3, 0.7)
    # signal: a slow sonar ping, the timer ticks, stamp on 22
    a = P.shot_start("signal")
    for j in range(4):
        TA.place(fx, blip(0.3, 660), a + 0.2 + 1.2 * j, 1.0, pan=-0.2)
    for j in range(int((WT("n14", "22") - a) // 1)):
        TA.place(fx, TA.sfx("tick", j), a + 1.0 * j + 0.05, 0.25)
    TA.place(fx, TA.sfx("stamp"), WT("n14", "22"), 0.9)
    # the tease: a riser into the question; the horizon: a soft shimmer
    TA.place(fx, TA.sfx("riser"), L["n16"] + 1.0, 0.35)
    TA.place(fx, TA.sfx("sparkle"), P.shot_start("horizon") + 0.1, 0.3)
    # the answer: silence (music cut), then the stopwatch clicks and the stamp
    t_rev = WT("n17", "15")
    TA.place(fx, TA.sfx("stamp"), t_rev, 1.1)
    for j in range(8):
        TA.place(fx, TA.sfx("tick", j), t_rev - 0.15 + 0.05 * j, 0.25)
    TA.place(fx, TA.sfx("ding"), WT("n17", "90"), 0.5)
    # chamber: hiss as the air goes, bubbles, then air rushing back and a sparkle
    a = P.shot_start("chamber")
    TA.place(fx, hiss(0.5, 1.2), a + 0.1, 1.0)
    TA.place(fx, bubbles(0.45, 1.4), WT("n20", "spit") - 0.1, 1.0)
    TA.place(fx, TA.sfx("whoosh"), WT("n20", "87") - 0.3, 0.6)
    TA.place(fx, TA.sfx("ding"), WT("n20", "87") + 0.3, 0.4)
    TA.place(fx, TA.sfx("stamp"), WT("n20", "recovered"), 0.8)
    # sunset: a sparkle on 'blue', a soft chime on the light
    TA.place(fx, TA.sfx("whoosh_down"), P.shot_start("sunset") - 0.05, 0.4)
    TA.place(fx, TA.sfx("sparkle"), WT("n21", "blue"), 0.6)
    TA.place(fx, TA.sfx("ding"), WT("n22", "blue"), 0.35)
    # the NOPEs: the word first, clean; the damage lands as it ends
    for key, lvl in P.NOPES.items():
        hit = E[key] + 0.02
        if lvl == 1:              # the dust blows off the plain, the dust devil is flung away
            TA.place(fx, boom(0.3, 0.9), hit - 0.07, 1.0)
            TA.place(fx, dust_whump(0.9), hit - 0.05, 1.0)
            TA.place(fx, TA.sfx("whoosh"), hit + 0.05, 0.5)
        elif lvl == 2:            # the lander tips, its dish snaps off and flies
            TA.place(fx, boom(0.55, 1.0), hit, 1.0)
            TA.place(fx, metal_clank(0.9), hit + 0.03, 1.0, pan=-0.4)
            TA.place(fx, TA.sfx("whoosh"), hit + 0.15, 0.6)
            TA.place(fx, dust_whump(0.6, 0.6), hit + 0.2, 1.0, pan=-0.3)
        else:                     # the mesa collapses, a dust storm rolls in from both sides
            for i in (0, 1):
                TA.place(fx, boom(0.12 + 0.06 * i, 0.18), P.W3[i] + 0.22, 1.0)
            TA.place(fx, boom(1.15, 1.0), hit, 1.0)
            TA.place(fx, rockfall(0.9, 1.8), hit + 0.05, 1.0, pan=0.3)
            TA.place(fx, storm(0.9, 2.0), hit + 0.15, 1.0)
    # the end: the three choices, the countdown, the respawn
    for word in ("medieval", "Pompeii", "Mariana"):
        TA.place(fx, TA.sfx("pop"), WT("n23", word), 0.7)
    TA.place(fx, TA.sfx("riser_fast"), E["n25"] - 0.7, 0.6)
    TA.place(fx, TA.sfx("pop"), E["n25"] + 0.02, 1.0)
    TA.place(fx, TA.sfx("sparkle"), E["n25"] + 0.05, 0.7)
    fx = fx[:n]
    mus = mus[:n]
    bed = mars_bed(n)
    cut(mus, E["n16"] + 0.05, t_rev + 0.05)          # silence before the answer
    cut(bed, E["n16"] + 0.05, t_rev - 0.05)
    cut(mus, L["n5"] - 0.08, E["n5"] + 0.02)          # "So I hold my breath?": the band holds its breath too
    for key, lvl in P.NOPES.items():
        cut(mus, L[key] - 0.12, E[key] + (0.2, 0.35, 0.9)[lvl - 1])
        cut(bed, L[key] - 0.12, E[key] + 0.05)
    vsr, v = wavfile.read(os.path.join(OUT, "cys05_voice.wav"))
    v = v.astype(np.float32) / 32768
    if vsr != SR:
        from scipy import signal
        v = signal.resample_poly(v, SR, vsr).astype(np.float32)
    v = np.pad(v, (0, max(0, n - len(v))))[:n]
    # NOPE 3 a little louder, so it lands at least 3 dB above NOPE 2 on the final mix
    a_, b_ = int((L["n19"] - 0.05) * SR), int((E["n19"] + 0.1) * SR)
    gain = np.ones(n, np.float32)
    gain[a_:b_] = 10 ** (4.0 / 20)
    v = v * np.convolve(gain, np.ones(240) / 240, mode="same")
    voice = np.stack([v, v], 1)

    def rms(x):
        a = np.abs(x).mean(axis=1) if x.ndim > 1 else np.abs(x)
        m = a > 0.01
        return float(np.sqrt((x[m] ** 2).mean())) if m.any() else 1e-6
    vr = rms(voice)
    mus *= vr * 10 ** (-15 / 20) / rms(mus)
    fx *= vr * 10 ** (-12 / 20) / rms(fx)
    bed *= vr * 10 ** (-28 / 20) / rms(bed)
    talk = np.convolve((np.abs(v) > 0.02).astype(np.float32), np.ones(int(0.3 * SR)) / (0.3 * SR), mode="same")
    duck_ = (1 - 0.5 * np.clip(talk * 1.5, 0, 1))[:, None]
    mus *= duck_
    bed *= duck_
    i1 = int((E["n1"] + 0.05) * SR)                    # the first line stays clear: the spawn is heard, not masked
    mus[:i1] *= 0.35
    bed[:i1] *= 0.35
    mix = voice + mus + fx + bed
    mix = mix / (np.abs(mix).max() or 1) * 0.89
    wav = os.path.join(OUT, "cys05_audio.wav")
    wavfile.write(wav, SR, (mix * 32767).astype(np.int16))
    lv = []
    mono = mix.mean(axis=1)
    for key in P.NOPES:
        seg = mono[int(L[key] * SR):int(E[key] * SR)]
        lv.append(20 * math.log10(float(np.sqrt((seg ** 2).mean())) + 1e-9))
    print("NOPE levels on the mix (dB):", [round(x, 1) for x in lv])
    if mixgate:
        wavfile.write(os.path.join(OUT, "cys05mix_voice.wav"), SR, (mono * 32767).astype(np.int16))
        shutil.copy(os.path.join(OUT, "cys05_lines.json"), os.path.join(OUT, "cys05mix_lines.json"))
    vid = os.path.join(OUT, "cys05_pic_video.mp4")
    dst = os.path.join(OUT, "SubjectZero_CYS05_Mars.mp4")
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
