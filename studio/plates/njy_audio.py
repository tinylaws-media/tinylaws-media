"""NOT JUST YOU — soundtrack: a slow night pad, a felt piano, soft rain, a few quiet effects.

    python3 njy_audio.py njy_ep001   -> out/njy_ep001_audio.wav   (needs out/<ep>_voice.wav)

Mix rules (owner's standing feedback): music ~13 dB under the voice (ducking 3 dB more while
the voice talks), effects ~19 dB under the voice, nothing sudden. Everything is synthesised.
The episode may define SFX = [(t, name)], MUSIC_KEYS = [(t, 'minor'|'major')].
"""
import importlib
import os
import sys

import numpy as np
from scipy import signal
from scipy.io import wavfile

from audio import SR, place, lp, hp, bp, midi, noise, glock   # Tiny Laws helpers (generic DSP)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
MUSIC_UNDER_VOICE_DB = 13.0
SFX_UNDER_VOICE_DB = 19.0
DUCK_DB = 3.0
RNG = np.random.default_rng(4)


def tt(d):
    return np.arange(int(d * SR)) / SR


def pad_chord(notes, d, v=1.0):
    """Warm, slow pad: detuned sines + a little triangle, long attack and release."""
    t = tt(d)
    x = np.zeros_like(t)
    for m in notes:
        f = midi(m)
        for det in (-0.003, 0.0, 0.0032):
            x += np.sin(2 * np.pi * f * (1 + det) * t + RNG.uniform(0, 6.28)) * 0.5
            x += signal.sawtooth(2 * np.pi * f * (1 + det) * t, 0.5) * 0.12
    x = lp(x, 1400)
    att, rel = min(1.6, d / 3), min(1.8, d / 3)
    e = np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1)
    return x * e * v / len(notes)


def felt(m, v=1.0, d=2.6):
    """Felt piano: soft hammer, quick fall, long quiet tail."""
    f = midi(m)
    t = tt(d)
    x = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 3)
         + 0.12 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t * 6))
    e = np.minimum(1, t / 0.012) * (0.6 * np.exp(-t * 2.2) + 0.4 * np.exp(-t * 0.6))
    return lp(x * e, 2600) * v


MINOR = [([45, 52, 55, 60], 33), ([41, 48, 52, 57], 29), ([48, 52, 55, 59], 36), ([43, 50, 55, 59], 31)]  # Am9 Fmaj7 Cmaj7 G
MAJOR = [([41, 48, 52, 57], 29), ([48, 52, 55, 60], 36), ([43, 50, 55, 59], 31), ([45, 52, 57, 60], 33)]  # F C G Am
ARP = [0, 2, 3, 1, 2, 3]


def music(D, keys):
    bar = 4.0                        # one chord every 4 s (60 BPM, 4 beats)
    n = int(D * SR) + SR * 4
    padb = np.zeros((n, 2))
    pno = np.zeros((n, 2))
    k = 0
    t0 = 0.0
    while t0 < D + 1:
        mode = "minor"
        for (tk, md) in keys:
            if t0 + 0.01 >= tk:
                mode = md
        prog_ = MINOR if mode == "minor" else MAJOR
        notes, root = prog_[k % 4]
        place(padb, pad_chord(notes + [root], bar + 1.6, 0.9), t0 - 0.4, 1, 0)
        # sparse felt piano, one note per beat-and-a-half, high and quiet
        for j, ix in enumerate(ARP[: 3 if mode == "minor" else 4]):
            m = sorted(notes)[ix] + 12
            place(pno, felt(m, 0.32 if mode == "minor" else 0.36), t0 + j * 1.33 + 0.05, 1, 0.25 * (-1) ** j)
        t0 += bar
        k += 1
    # soft rain: filtered noise, steady (it never 'grows')
    rain = bp(noise(n / SR), 900, 7000) * 0.05
    rain = np.stack([rain, np.roll(rain, 997)], axis=1)[:n]
    mix = padb * 0.9 + pno * 0.75 + rain
    return mix[: int(D * SR)]


def sfx(name):
    if name == "tone":            # a node appears: a soft glass tone
        return glock(84, 0.22, 1.4) * 0.8
    if name == "tone_low":
        return glock(79, 0.22, 1.4) * 0.8
    if name == "slide":           # a card slides in: soft paper
        d = 0.35
        x = bp(noise(d), 1200, 6000)
        t = tt(d)
        return x * np.sin(np.pi * t / d) ** 2 * 0.25
    if name == "rise":            # a bar grows: a breathy swell
        d = 1.2
        x = bp(noise(d), 300, 2000)
        t = tt(d)
        return x * np.sin(np.pi * t / d) ** 2 * 0.35
    if name == "flip":            # phone set face down: a soft cloth thud
        t = tt(0.3)
        return lp(noise(0.3), 400) * np.exp(-t * 16) * 1.2
    if name == "warm":            # the lamp warms: two felt notes
        out = np.zeros(int(3.0 * SR))
        a, b = felt(69, 0.5, 2.8), felt(76, 0.4, 2.6)
        out[: len(a)] += a
        out[int(0.25 * SR): int(0.25 * SR) + len(b)] += b[: len(out) - int(0.25 * SR)]
        return out
    if name == "window":          # a far window lights up
        return glock(91, 0.12, 0.9) * 0.6
    raise ValueError(name)


def build(epname):
    ep = importlib.import_module(epname)
    D = ep.DURATION
    n = int(D * SR)
    mus = music(D, getattr(ep, "MUSIC_KEYS", []))[:n]
    fx = np.zeros((n + SR * 4, 2))
    for (t, name) in ep.SFX:
        place(fx, sfx(name), t, 1.0, 0.0)
    fx = fx[:n]

    def active_rms(x):
        e = np.abs(x).max(axis=1)
        sm = np.convolve(e, np.ones(int(0.05 * SR)) / int(0.05 * SR), mode="same")
        act = x[sm > 1e-3]
        return float(np.sqrt((act ** 2).mean())) if len(act) else 1e-9

    vsr, v = wavfile.read(os.path.join(OUT, f"{epname}_voice.wav"))
    v = v.astype(np.float32) / 32768.0
    if vsr != SR:
        v = signal.resample_poly(v, SR, vsr).astype(np.float32)
    v = np.pad(v, (0, max(0, n - len(v))))[:n]
    voice = np.stack([v, v], axis=1)
    v_rms = active_rms(voice)
    mus *= (v_rms * 10 ** (-MUSIC_UNDER_VOICE_DB / 20)) / active_rms(mus)
    fx *= (v_rms * 10 ** (-SFX_UNDER_VOICE_DB / 20)) / active_rms(fx)
    env = np.abs(v)
    sm = np.convolve(env, np.ones(int(0.04 * SR)) / int(0.04 * SR), mode="same")
    talk = np.convolve((sm > 0.02).astype(np.float32), np.ones(int(0.4 * SR)) / int(0.4 * SR), mode="same")
    mus *= (1.0 - (1.0 - 10 ** (-DUCK_DB / 20)) * np.clip(talk * 1.5, 0, 1))[:, None]
    # a small room on the effects only; the voice stays dry and close
    ir_n = int(0.9 * SR)
    ir = np.random.default_rng(3).standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 6)
    ir = lp(ir, 4000) * 0.04
    wet = np.stack([signal.fftconvolve(fx[:, ch], ir)[:n] for ch in range(2)], axis=1)
    mix = voice + mus + fx + wet * 0.6
    mix *= 10 ** (-16 / 20) / max(float(np.sqrt((mix ** 2).mean())), 1e-9)
    mix = np.tanh(mix / 0.95) * 0.95
    fade = int(0.03 * SR)
    mix[:fade] *= np.linspace(0, 1, fade)[:, None]
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    p = os.path.join(OUT, f"{epname}_audio.wav")
    wavfile.write(p, SR, (mix * 32767).astype(np.int16))
    print("wrote", p, round(n / SR, 2), "s")


if __name__ == "__main__":
    build(sys.argv[1])
