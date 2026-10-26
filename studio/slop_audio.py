"""SLOP SHOP — soundtrack for the YouTube-Poop episodes: python3 slop_audio.py slop_ep002 -> out/<ep>_audio.wav

Uses audio.py's synthesised jingle and effects, adds the YTP gags (soft sub boom, record scratch,
slide whistle, cash register, wood bonk, rubber squeak, howl, digital skip, tape rewind, muted
wah-wah, camera click) and the music edits (tape stops, beat repeats).
Everything is synthesised, nothing is sampled. Nothing harsh: every gag is low-passed, short and
sits under the voice (music 13 dB under it, effects 15 dB under it, the music ducks while anyone talks).
Episode hooks: SFX [(t, name, p)], MUSIC_CUTS [(a, b)], BEAT_REPEATS [(t, chunk_s, n)], BPM, DURATION,
CHORDS / MOTIFS / TRANSPOSE, music_sections(t).
"""
import importlib
import os
import sys

import numpy as np
from scipy import signal
from scipy.io import wavfile

import audio as A

SR = A.SR
HERE = os.path.dirname(os.path.abspath(__file__))
MUSIC_UNDER_VOICE_DB = 13.0
SFX_UNDER_VOICE_DB = 15.0
DUCK_DB = 4.0


def _t(d):
    return np.arange(int(d * SR)) / SR


def gag(name, p=0):
    if name == "boom":      # soft sub drop
        tt = _t(1.4)
        f = 34 + 40 * np.exp(-tt * 6)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.4) * np.minimum(1, tt / 0.01)
        return A.lp(np.tanh(x * 1.3), 300) * 1.1
    if name == "scratch":   # gentle record scratch (band-limited, quiet)
        d = 0.32
        tt = _t(d)
        rate = 1 + 0.9 * np.sin(2 * np.pi * 5.5 * tt)
        x = A.bp(A.noise(d), 500, 2600) * np.abs(rate)
        s = np.sin(2 * np.pi * np.cumsum(300 * rate) / SR) * 0.25
        return (x * 0.5 + s) * A.env(len(tt), 0.005, d, 1.5) * 0.8
    if name in ("slide_up", "slide_down"):
        d = 0.55
        tt = _t(d)
        f0, f1 = (500, 1400) if name == "slide_up" else (1300, 420)
        f = f0 * (f1 / f0) ** (tt / d) * (1 + 0.02 * np.sin(2 * np.pi * 7 * tt))
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.2 * A.lp(A.noise(d), 3000)
        return x * np.sin(np.pi * tt / d) ** 0.6 * 0.3
    if name == "kaching":
        out = np.zeros(int(1.0 * SR))
        click = A.bp(A.noise(0.03), 1500, 6000) * A.env(int(0.03 * SR), 0.0005, 0.03, 5) * 0.6
        out[: len(click)] += click
        for i, m in enumerate((91, 96)):
            g = A.glock(m, 0.35, 0.8)
            j = int((0.06 + i * 0.07) * SR)
            out[j:j + len(g)] += g[: len(out) - j]
        return out
    if name == "bonk":
        tt = _t(0.18)
        x = np.sin(2 * np.pi * (620 + 300 * np.exp(-tt * 40)) * tt) * np.exp(-tt * 28)
        return x * 0.6
    if name == "squeak":
        d = 0.16
        tt = _t(d)
        f = (900 + 120 * p) * (1 + 0.25 * np.sin(np.pi * tt / d)) * (1 + 0.04 * np.sin(2 * np.pi * 30 * tt))
        x = np.sin(2 * np.pi * np.cumsum(f) / SR)
        return A.lp(x, 2500) * np.sin(np.pi * tt / d) * 0.32
    if name == "howl":
        d = 1.3
        tt = _t(d)
        f = (330 + 240 * np.sin(np.pi * np.minimum(1, tt / 0.9)) ** 0.7) * (1 + 0.012 * np.sin(2 * np.pi * 6 * tt))
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
        return A.lp(x, 1800) * np.minimum(1, tt / 0.08) * np.clip((d - tt) / 0.3, 0, 1) * 0.34
    if name == "skip":      # a digital skip: two soft square-ish blips
        out = np.zeros(int(0.14 * SR))
        for i, f in enumerate((1300, 900)):
            tt = _t(0.05)
            b = A.lp(signal.square(2 * np.pi * f * tt), 2200) * np.exp(-tt * 40) * 0.22
            j = int(i * 0.06 * SR)
            out[j:j + len(b)] += b
        return out
    if name == "rewind":
        d = 0.6
        tt = _t(d)
        f = 300 * (8 ** (tt / d))
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.15
        x = A.bp(A.noise(d), 800, 4000) * 0.25
        return (s + x) * np.sin(np.pi * tt / d) * 0.8
    if name == "wahwah":    # muted 'wah-wah', two falling notes
        out = np.zeros(int(1.3 * SR))
        for i, m in enumerate((58, 55)):
            d = 0.55 if i == 0 else 0.7
            tt = _t(d)
            f = A.midi(m) * (1 - 0.03 * tt / d)
            x = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR)
            cut = 500 + 1400 * np.sin(np.pi * np.minimum(1, tt / (d * 0.8))) ** 2
            y = np.zeros_like(x)
            for k in range(0, len(x), 512):
                y[k:k + 512] = A.lp(x[max(0, k - 512):k + 512], float(cut[k]))[-len(x[k:k + 512]):]
            y *= np.minimum(1, tt / 0.03) * np.clip((d - tt) / 0.1, 0, 1)
            j = int(i * 0.55 * SR)
            out[j:j + len(y)] += y * 0.28
        return out
    if name == "creak":     # old springs
        d = 0.45
        tt = _t(d)
        f = 140 + 40 * np.sin(2 * np.pi * 3 * tt)
        x = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR, 0.2)
        x = A.bp(x, 600, 2400) * (0.5 + 0.5 * np.sin(2 * np.pi * 23 * tt)) ** 2
        return x * np.sin(np.pi * tt / d) * 0.3
    if name == "crackle":   # crusty bread
        out = np.zeros(int(0.35 * SR))
        r = np.random.default_rng(p + 3)
        for k in range(14):
            i = int(r.uniform(0, 0.3) * SR)
            b = A.bp(A.noise(0.008), 1500, 6000) * r.uniform(0.3, 1)
            out[i:i + len(b)] += b[: len(out) - i]
        return out * 0.5
    if name == "mictap":
        out = np.zeros(int(0.5 * SR))
        for i in range(2):
            tt = _t(0.12)
            b = A.lp(np.sin(2 * np.pi * 90 * tt) * np.exp(-tt * 30) + A.noise(0.12) * np.exp(-tt * 60) * 0.3, 1200)
            j = int(i * 0.22 * SR)
            out[j:j + len(b)] += b * 0.7
        return out
    if name == "click":
        return A.bp(A.noise(0.04), 2000, 7000) * A.env(int(0.04 * SR), 0.0005, 0.04, 6) * 0.5
    if name == "boop":
        tt = _t(0.12)
        return np.sin(2 * np.pi * A.midi(79 + p) * tt) * np.exp(-tt * 20) * 0.4
    return A.sfx(name, p)


GAINS = {"boom": 1.6, "slam": 1.2, "stamp": 1.1, "kaching": 0.9, "scratch": 0.7, "howl": 1.0, "crunch": 1.3}


def build(epname):
    ep = importlib.import_module(epname)
    D = ep.DURATION
    A.CHORDS = getattr(ep, "CHORDS", A.CHORDS)
    A.MOTIFS = getattr(ep, "MOTIFS", A.MOTIFS)
    A.TRANSPOSE = getattr(ep, "TRANSPOSE", A.TRANSPOSE)
    mus = A.music(D, ep.BPM, ep.music_sections, getattr(ep, "MUSIC_CUTS", []))
    n = int(D * SR)
    mus = mus[:n]
    for (t0, ch, k) in getattr(ep, "BEAT_REPEATS", []):   # YTP beat repeat: a slice of music stutters
        a, L = int(t0 * SR), int(ch * SR)
        sl = mus[a:a + L].copy()
        fd = int(0.004 * SR)
        sl[:fd] *= np.linspace(0, 1, fd)[:, None]
        sl[-fd:] *= np.linspace(1, 0, fd)[:, None]
        for j in range(1, k + 1):
            b = a + j * L
            if b + L <= n:
                mus[b:b + L] = sl
    fx = np.zeros((n + SR * 3, 2))
    for (t, name, p) in ep.SFX:
        A.place(fx, gag(name, p), t, GAINS.get(name, 1.0), pan=0.0)
    fx = fx[:n]

    def active_rms(x):
        e = np.abs(x).max(axis=1) if x.ndim > 1 else np.abs(x)
        win = int(0.05 * SR)
        sm = np.convolve(e, np.ones(win) / win, mode="same")
        act = x[sm > 1e-3]
        return float(np.sqrt((act ** 2).mean())) if len(act) else 1e-9

    vsr, v = wavfile.read(os.path.join(HERE, "out", f"{epname}_voice.wav"))
    v = v.astype(np.float32) / 32768.0
    if vsr != SR:
        v = signal.resample_poly(v, SR, vsr).astype(np.float32)
    v = np.pad(v, (0, max(0, n - len(v))))[:n]
    voice = np.stack([v, v], axis=1)
    v_rms = active_rms(voice)
    mus *= (v_rms * 10 ** (-MUSIC_UNDER_VOICE_DB / 20)) / active_rms(mus)
    fx *= (v_rms * 10 ** (-SFX_UNDER_VOICE_DB / 20)) / active_rms(fx)
    # effects never peak above the voice's own peaks
    lim = np.abs(v).max() * 0.6
    fx = np.tanh(fx / lim) * lim
    env = np.abs(v)
    att, rel = int(0.04 * SR), int(0.35 * SR)
    sm = np.convolve(env, np.ones(att) / att, mode="same")
    talk = np.convolve((sm > 0.02).astype(np.float32), np.ones(rel) / rel, mode="same")
    duck = 1.0 - (1.0 - 10 ** (-DUCK_DB / 20)) * np.clip(talk * 1.5, 0, 1)
    mus *= duck[:, None]
    fx *= (1.0 - 0.35 * np.clip(talk * 1.5, 0, 1))[:, None]   # gags step back under words too
    ir_n = int(0.5 * SR)
    ir = np.random.default_rng(3).standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 10)
    ir = A.lp(ir, 5000) * 0.05
    wet = np.stack([signal.fftconvolve(fx[:, ch], ir)[:n] for ch in range(2)], axis=1)
    mix = mus + fx + voice + wet * 0.4
    rms = float(np.sqrt((mix ** 2).mean()))
    mix *= 10 ** (-16 / 20) / max(rms, 1e-9)
    mix = np.tanh(mix / 0.9) * 0.9
    fade = int(0.015 * SR)
    mix[:fade] *= np.linspace(0, 1, fade)[:, None]
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    path = os.path.join(HERE, "out", f"{epname}_audio.wav")
    wavfile.write(path, SR, (mix * 32767).astype(np.int16))
    print("wrote", path, round(len(mix) / SR, 2), "s")


if __name__ == "__main__":
    build(sys.argv[1])
