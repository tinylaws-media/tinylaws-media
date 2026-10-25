"""TINY LAWS — synthesised soundtrack: lo-fi toy-pop music, Pip's blip voice and cartoon SFX.

Everything is generated from oscillators and noise, so there is nothing to license.
Usage: python3 audio.py ep001  -> out/ep001_audio.wav
"""
import importlib
import os
import sys

import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 44100
RNG = np.random.default_rng(1)


def t_(d):
    return np.arange(int(d * SR)) / SR


def env(n, a=0.005, d=0.2, curve=4.0):
    tt = np.arange(n) / SR
    e = np.minimum(1, tt / max(a, 1e-4)) * np.exp(-tt * curve / max(d, 1e-4))
    return e


def lp(x, f, order=2):
    b, a = signal.butter(order, min(f, SR / 2 - 100) / (SR / 2), "low")
    return signal.lfilter(b, a, x)


def hp(x, f, order=2):
    b, a = signal.butter(order, f / (SR / 2), "high")
    return signal.lfilter(b, a, x)


def bp(x, f0, f1, order=2):
    b, a = signal.butter(order, [f0 / (SR / 2), min(f1, SR / 2 - 100) / (SR / 2)], "band")
    return signal.lfilter(b, a, x)


def sweep(f0, f1, d, shape="exp"):
    n = int(d * SR)
    if shape == "exp":
        f = f0 * (f1 / f0) ** (np.arange(n) / n)
    else:
        f = np.linspace(f0, f1, n)
    return np.sin(2 * np.pi * np.cumsum(f) / SR), f


def noise(d):
    return RNG.uniform(-1, 1, int(d * SR))


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def place(buf, x, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= buf.shape[0] or i + len(x) <= 0:
        return
    if i < 0:
        x = x[-i:]
        i = 0
    n = min(len(x), buf.shape[0] - i)
    l = np.cos((pan + 1) * np.pi / 4)
    r = np.sin((pan + 1) * np.pi / 4)
    buf[i:i + n, 0] += x[:n] * gain * l * 1.414
    buf[i:i + n, 1] += x[:n] * gain * r * 1.414


# ------------------------------------------------------------------ instruments
def kick2(v=1.0):
    n = int(0.34 * SR)
    tt = np.arange(n) / SR
    f = 46 + 120 * np.exp(-tt * 28)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)
    click = lp(noise(0.006), 4000) * 0.4
    s[:len(click)] += click
    return np.tanh(s * 1.4) * v


def snare(v=1.0):
    n = noise(0.22)
    body = np.sin(2 * np.pi * 190 * t_(0.22)) * env(len(n), 0.001, 0.08, 6)
    nz = bp(n, 900, 6500) * env(len(n), 0.001, 0.16, 6)
    return (0.55 * body + 0.9 * nz) * v


def hat(v=1.0, open_=False):
    d = 0.18 if open_ else 0.045
    n = hp(noise(d), 7000, 3) * env(int(d * SR), 0.0005, d, 5)
    return n * v


def crash(v=1.0):
    n = hp(noise(2.2), 4500, 2) * env(int(2.2 * SR), 0.001, 2.2, 3.5)
    return n * v


def bass_note(m, d, v=1.0):
    f = midi(m)
    tt = t_(d)
    x = 0.8 * np.sin(2 * np.pi * f * tt) + 0.25 * signal.sawtooth(2 * np.pi * f * tt)
    x = lp(x, 520)
    e = np.minimum(1, tt / 0.006) * np.exp(-tt * 2.2) * np.clip((d - tt) / 0.03, 0, 1)
    return np.tanh(x * e * 1.3) * v


def marimba(m, v=1.0, d=0.6):
    f = midi(m)
    tt = t_(d)
    x = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 7) + 0.35 * np.sin(2 * np.pi * f * 3.93 * tt) * np.exp(-tt * 22)
    x += 0.12 * np.sin(2 * np.pi * f * 9.2 * tt) * np.exp(-tt * 50)
    return x * np.minimum(1, tt / 0.002) * v


def glock(m, v=1.0, d=1.2):
    f = midi(m)
    tt = t_(d)
    mod = np.sin(2 * np.pi * f * 3.5 * tt) * 2.2 * np.exp(-tt * 6)
    x = np.sin(2 * np.pi * f * tt + mod) * np.exp(-tt * 3.5)
    return x * np.minimum(1, tt / 0.001) * v


def keys_chord(ms, d, v=1.0):
    """Soft detuned 'toy keyboard' chord, a little wobbly like an old cassette."""
    tt = t_(d)
    x = np.zeros_like(tt)
    wob = 1 + 0.0025 * np.sin(2 * np.pi * 0.7 * tt)
    for m in ms:
        f = midi(m)
        for det in (-0.004, 0.0, 0.0045):
            ph = 2 * np.pi * np.cumsum(f * (1 + det) * wob) / SR
            x += signal.sawtooth(ph, 0.5) * 0.33
    x = lp(x, 1500)
    e = np.minimum(1, tt / 0.04) * (0.55 + 0.45 * np.exp(-tt * 2.5)) * np.clip((d - tt) / 0.12, 0, 1)
    return x * e * v / len(ms)


# ------------------------------------------------------------------ music
CHORDS = [  # C, G/B, Am, F  (one per bar)
    ([48, 55, 60, 64], 36), ([47, 55, 59, 62], 43), ([45, 52, 57, 60], 45), ([41, 53, 57, 60], 41),
]
PENTA = [60, 62, 64, 67, 69, 72, 74, 76, 79]
TRANSPOSE = 0   # semitones; an episode can set TRANSPOSE, CHORDS, MOTIFS to get its own tune
MOTIFS = [
    # (beat offset in 8ths, scale index, length in 8ths)
    [(0, 5, 1), (1, 4, 1), (2, 2, 2), (5, 3, 1), (6, 4, 2)],
    [(0, 4, 1), (2, 5, 1), (3, 6, 1), (4, 5, 2), (7, 3, 1)],
    [(0, 2, 2), (2, 3, 1), (3, 4, 1), (4, 6, 2), (6, 5, 2)],
    [(0, 7, 1), (1, 6, 1), (2, 5, 1), (3, 4, 1), (4, 2, 4)],
]


def music(duration, bpm, sections, cuts):
    beat = 60.0 / bpm
    bars = int(round(duration / (beat * 4)))
    n = int(duration * SR) + SR * 3
    drums = np.zeros((n, 2))
    bass = np.zeros((n, 2))
    keys = np.zeros((n, 2))
    lead = np.zeros((n, 2))
    for b in range(bars):
        t0 = b * 4 * beat
        sec = sections(t0)
        chord, root = CHORDS[b % 4]
        # drums
        for k in range(8):
            tk = t0 + k * beat / 2
            if sec["drums"] >= 1:
                place(drums, hat(0.32 if k % 2 else 0.22), tk + (0.012 if k % 2 else 0), 1, 0.25)
                if sec["drums"] >= 2:
                    place(drums, hat(0.12), tk + beat / 4, 1, 0.3)
            if k in (0, 4) or (k == 3 and b % 2 == 1):
                if sec["drums"] >= 1:
                    place(drums, kick2(0.95), tk, 1)
            if k in (2, 6) and sec["drums"] >= 1:
                place(drums, snare(0.5), tk, 1, -0.05)
        # bass: root, root, fifth, octave-ish groove
        if sec["bass"]:
            pat = [(0, 0, 1.5), (3, 0, 0.5), (4, 7, 1.0), (6, 12, 0.5), (7, 10 if b % 4 == 3 else 7, 0.5)]
            for (k, iv, dur) in pat:
                place(bass, bass_note(root + iv + TRANSPOSE, dur * beat * 0.95, 0.75), t0 + k * beat / 2, 1)
        # toy keys: stabs on 1 and the 'and' of 2
        if sec["keys"]:
            ch_t = [m + TRANSPOSE for m in chord]
            place(keys, keys_chord(ch_t, beat * 1.4, 0.5), t0, 1, -0.3)
            place(keys, keys_chord(ch_t, beat * 1.9, 0.38), t0 + 1.5 * beat, 1, -0.3)
            place(keys, keys_chord(ch_t, beat * 0.9, 0.3), t0 + 3 * beat, 1, -0.3)
        # marimba lead
        if sec["lead"]:
            mot = MOTIFS[(b // 2 + sec.get("var", 0)) % len(MOTIFS)] if b % 2 == 0 else MOTIFS[(b // 2 + 1 + sec.get("var", 0)) % len(MOTIFS)]
            for (k, si, ln) in mot:
                place(lead, marimba(PENTA[si] + TRANSPOSE + sec.get("oct", 0), 0.42, d=min(0.9, ln * beat / 2 + 0.3)), t0 + k * beat / 2, 1, 0.3)
        if sec.get("glock"):
            for k, si in enumerate((0, 2, 4, 5, 7, 8, 7, 5)):
                place(lead, glock(PENTA[si] + TRANSPOSE + 12, 0.16), t0 + k * beat / 2, 1, -0.4)
        if sec.get("crash") and b == sec["crash"]:
            place(drums, crash(0.18), t0, 1)
    # mix the music bus
    mix = drums * 0.85 + bass * 0.8 + keys * 0.55 + lead * 0.6
    # cassette-ish warmth: gentle saturation + slow wow
    mix = np.tanh(mix * 0.9) / 0.9
    tt = np.arange(n) / SR
    wow = 0.0016 * np.sin(2 * np.pi * 0.55 * tt) + 0.0006 * np.sin(2 * np.pi * 3.1 * tt)
    idx = np.clip(np.arange(n) + wow * SR * 0.4, 0, n - 1)
    for ch in range(2):
        mix[:, ch] = np.interp(idx, np.arange(n), mix[:, ch])
    # cuts with a tape-stop into the cut
    for (a, b_) in cuts:
        ia, ib = int(a * SR), int(b_ * SR)
        stop = int(0.5 * SR)
        seg = mix[ia:ia + stop].copy()
        pos = np.cumsum(np.linspace(1.0, 0.0, stop))
        for ch in range(2):
            mix[ia:ia + stop, ch] = np.interp(pos, np.arange(stop), seg[:, ch]) * np.linspace(1, 0.2, stop)
        mix[ia + stop:ib] = 0
        fade = int(0.01 * SR)
        mix[ib:ib + fade] *= np.linspace(0, 1, fade)[:, None]
    return mix[: int(duration * SR)]


# ------------------------------------------------------------------ sfx
def sfx(name, p=0):
    if name == "pop":
        s, _ = sweep(380 * 2 ** (p / 12 * 2), 900 * 2 ** (p / 12 * 2), 0.07)
        return s * env(len(s), 0.001, 0.07, 3) * 0.6
    if name == "tick":
        f = midi(84 + [0, 2, 4, 7, 9, 12, 14, 16][p % 8])
        tt = t_(0.07)
        return (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 2.7 * tt)) * np.exp(-tt * 70) * 0.45
    if name == "ding":
        return (glock(88, 0.5, 1.4) + glock(95, 0.25, 1.4)) * 0.8
    if name == "sparkle":
        out = np.zeros(int(0.8 * SR))
        for i, m in enumerate((84, 88, 91, 96, 100)):
            g = glock(m, 0.22, 0.5)
            out[int(i * 0.05 * SR): int(i * 0.05 * SR) + len(g)] += g[: len(out) - int(i * 0.05 * SR)]
        return out
    if name == "squash":
        s, _ = sweep(220, 110, 0.12)
        return s * env(len(s), 0.002, 0.12, 3) * 0.5
    if name in ("boing_up", "boing_down", "hop"):
        d = 0.16 if name == "hop" else 0.5
        tt = t_(d)
        f0, f1 = (220, 780) if name != "boing_down" else (650, 140)
        if name == "hop":
            f0, f1 = 500, 950
        f = f0 * (f1 / f0) ** (tt / d) * (1 + 0.09 * np.sin(2 * np.pi * 14 * tt))
        s = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR, 0.5)
        return lp(s, 2500) * env(len(s), 0.004, d, 2.5) * 0.45
    if name == "crack":
        n = int(0.18 * SR)
        out = np.zeros(n)
        r = np.random.default_rng(p + 11)
        for k in range(5):
            i = int(r.uniform(0, 0.12) * SR)
            b = hp(noise(0.012), 1800) * r.uniform(0.4, 1.0)
            out[i:i + len(b)] += b[: n - i]
        out[:200] += hp(noise(200 / SR), 3000) * 1.2
        return out * 0.55
    if name in ("whoosh", "whoosh_down", "swoosh", "whip"):
        d = {"whoosh": 0.45, "whoosh_down": 0.45, "swoosh": 0.28, "whip": 0.22}[name]
        x = noise(d)
        n = len(x)
        out = np.zeros(n)
        f = np.geomspace(400, 4000, n) if name != "whoosh_down" else np.geomspace(3500, 300, n)
        if name == "whip":
            f = np.geomspace(1200, 7000, n)
        hop_ = 512
        for i in range(0, n, hop_):
            fc = f[i]
            seg = x[max(0, i - 256): i + hop_]
            yb = bp(seg, fc * 0.7, fc * 1.4)
            out[i:i + hop_] = yb[-min(hop_, n - i):]
        e = np.sin(np.pi * np.arange(n) / n) ** 1.5
        return out * e * 0.9
    if name in ("slam", "stamp", "thud"):
        d = 0.5 if name == "slam" else 0.32
        tt = t_(d)
        f = (45 if name != "stamp" else 70) + 140 * np.exp(-tt * 25)
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * (6 if name == "slam" else 11))
        slap = bp(noise(0.05), 1500, 6000) * env(int(0.05 * SR), 0.0005, 0.05, 5) * (0.9 if name != "thud" else 0.2)
        s[: len(slap)] += slap
        s = np.tanh(s * 1.6) * 0.75
        if name == "slam":
            c = crash(0.07)
            s = np.concatenate([s, np.zeros(len(c) - len(s))]) + c
        return s
    if name == "scribble":
        d = 0.6
        x = bp(noise(d), 2500, 7000)
        tt = t_(d)
        am = np.clip(np.sin(2 * np.pi * 9 * tt + 2 * np.sin(2 * np.pi * 3 * tt)), 0, 1) ** 2
        return x * am * env(len(x), 0.01, d, 1) * 0.35
    if name == "rumble":
        d = 1.7
        x = lp(noise(d), 110, 3)
        tt = t_(d)
        return x * (tt / d) * (0.6 + 0.4 * np.sin(2 * np.pi * 11 * tt)) * 2.6
    if name in ("riser", "riser_fast"):
        d = 1.5 if name == "riser" else 0.75
        s, _ = sweep(180, 1400, d)
        x = bp(noise(d), 1500, 6000) * np.linspace(0, 0.22, int(d * SR))
        return (s * np.linspace(0, 0.35, len(s)) + x) * 0.8
    if name == "glass":
        out = hp(noise(0.5), 3000) * env(int(0.5 * SR), 0.0005, 0.25, 6) * 0.7
        for f in (3100, 4250, 5300, 6900):
            out += np.sin(2 * np.pi * f * t_(0.5)) * np.exp(-t_(0.5) * 9) * 0.12
        return out
    if name == "crunch":
        d = 0.75
        tt = t_(d)
        f = 38 + 110 * np.exp(-tt * 14)
        low = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 4.5)
        r = np.random.default_rng(5)
        gr = np.zeros(len(tt))
        for k in range(26):
            i = int(r.uniform(0, 0.35) * SR)
            b = bp(noise(0.02), 600, 5000) * r.uniform(0.3, 1)
            gr[i:i + len(b)] += b[: len(gr) - i]
        return np.tanh((low * 1.4 + gr * 0.8) * 1.8) * 0.9
    if name == "dizzy":
        d = 1.6
        tt = t_(d)
        f = 1500 * (1 - 0.35 * tt / d) * (1 + 0.06 * np.sin(2 * np.pi * 7 * tt))
        s = np.sin(2 * np.pi * np.cumsum(f) / SR)
        tw = np.zeros_like(s)
        for k, t0 in enumerate((0.2, 0.55, 0.95, 1.3)):
            g = glock(96 + (k % 2) * 3, 0.18, 0.3)
            i = int(t0 * SR)
            tw[i:i + len(g)] += g[: len(tw) - i]
        return s * env(len(s), 0.05, d, 1.5) * 0.18 + tw
    if name == "shrink":
        d = 0.5
        tt = t_(d)
        f = 300 * (5.0 ** (tt / d)) * (1 + 0.05 * np.sin(2 * np.pi * 20 * tt))
        s = np.sin(2 * np.pi * np.cumsum(f) / SR)
        return s * env(len(s), 0.01, d, 2) * 0.35
    if name == "fall":
        d = 2.1
        tt = t_(d)
        f = 1700 * (0.2 ** (tt / d)) * (1 + 0.012 * np.sin(2 * np.pi * 6 * tt))
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.15 * np.sin(4 * np.pi * np.cumsum(f) / SR)
        return s * np.minimum(1, tt / 0.1) * np.clip((d - tt) / 0.1, 0, 1) * 0.22
    if name == "tap":
        tt = t_(0.06)
        return np.sin(2 * np.pi * 1900 * tt) * np.exp(-tt * 90) * 0.4
    if name == "paper":
        d = 0.35
        x = bp(noise(d), 1500, 8000)
        tt = t_(d)
        return x * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 23 * tt))) * env(len(x), 0.005, d, 2) * 0.35
    if name == "shrug":
        a = blip(76, 0.09)
        b = blip(81, 0.12)
        out = np.zeros(int(0.3 * SR))
        out[: len(a)] += a
        out[int(0.11 * SR): int(0.11 * SR) + len(b)] += b
        return out
    raise ValueError(name)


def blip(m, d=0.075, v=0.27):
    """Pip's voice: a tiny rounded square-wave 'bip' that bends up a little."""
    tt = t_(d)
    f = midi(m) * (1 + 0.06 * np.minimum(1, tt / 0.03))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = signal.square(ph, 0.4) * 0.6 + np.sin(ph) * 0.6
    x = lp(x, 3200)
    e = np.minimum(1, tt / 0.004) * np.clip((d - tt) / 0.025, 0, 1)
    return x * e * v


VOICE = [72, 74, 76, 79, 81, 84]
SFX_DB = 16.0     # effects this many dB under the music (user: still too present at 11)
# narrated episodes (voice.py): everything is set relative to Pip's voice
MUSIC_UNDER_VOICE_DB = 13.0
SFX_UNDER_VOICE_DB = 19.0
DUCK_DB = 4.0     # extra music dip while Pip is talking
VOICE_DB = 13.0   # Pip's voice blips this many dB under the music


def build(epname):
    global CHORDS, MOTIFS, TRANSPOSE
    ep = importlib.import_module(epname)
    D = ep.DURATION
    CHORDS = getattr(ep, "CHORDS", CHORDS)
    MOTIFS = getattr(ep, "MOTIFS", MOTIFS)
    TRANSPOSE = getattr(ep, "TRANSPOSE", TRANSPOSE)
    custom_sections = getattr(ep, "music_sections", None)

    def sections(t):
        s = {"drums": 1, "bass": 1, "keys": 1, "lead": 1}
        if t < 6.5:
            s.update(lead=0, drums=1)
        elif t < 8.5:
            s.update(lead=0)
        elif 19.5 <= t < 28.5:
            s.update(drums=2, var=1)
        elif 28.5 <= t < 36:
            s.update(lead=0, drums=2)
        elif 44 <= t < 56.5:
            s.update(var=2)
        elif 56.5 <= t < 62.5:
            s.update(glock=1, drums=2, var=3, crash=28)
        elif t >= 62.5:
            s.update(lead=0, drums=1)
        return s

    mus = music(D, ep.BPM, custom_sections or sections, ep.MUSIC_CUTS)
    fx = np.zeros((int(D * SR) + SR * 3, 2))
    for (t, name, p) in ep.SFX:
        x = sfx(name, p)
        g = {"crunch": 1.6, "slam": 1.3, "rumble": 0.9, "stamp": 1.2}.get(name, 1.0)
        place(fx, x, t, g)
    n = int(D * SR)
    mus, fx = mus[:n], fx[:n]

    def active_rms(x):
        e = np.abs(x).max(axis=1) if x.ndim > 1 else np.abs(x)
        win = int(0.05 * SR)
        sm = np.convolve(e, np.ones(win) / win, mode="same")
        act = x[sm > 1e-3]
        return float(np.sqrt((act ** 2).mean())) if len(act) else 1e-9

    voice_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", f"{epname}_voice.wav")
    if os.path.exists(voice_path) and getattr(ep, "NARRATION", None):
        # Narrated episode: Pip's voice leads, the music sits under it and ducks while he talks.
        vsr, v = wavfile.read(voice_path)
        v = v.astype(np.float32) / 32768.0
        if vsr != SR:
            v = signal.resample_poly(v, SR, vsr).astype(np.float32)
        v = np.pad(v, (0, max(0, n - len(v))))[:n]
        voice = np.stack([v, v], axis=1)
        v_rms = active_rms(voice)
        mus *= (v_rms * 10 ** (-MUSIC_UNDER_VOICE_DB / 20)) / active_rms(mus)
        fx *= (v_rms * 10 ** (-SFX_UNDER_VOICE_DB / 20)) / active_rms(fx)
        env = np.abs(v)
        att, rel = int(0.04 * SR), int(0.35 * SR)
        sm = np.convolve(env, np.ones(att) / att, mode="same")
        talk = np.convolve((sm > 0.02).astype(np.float32), np.ones(rel) / rel, mode="same")
        duck = 1.0 - (1.0 - 10 ** (-DUCK_DB / 20)) * np.clip(talk * 1.5, 0, 1)
        mus *= duck[:, None]
    else:
        # Text-only episode: one soft blip per caption line, the music is the bed.
        voice = np.zeros_like(fx)
        for i, t in enumerate(ep.WORD_TIMES):
            m = VOICE[(i * 7 + int(t * 10)) % len(VOICE)]
            place(voice, blip(m), t, 1.0, 0.0)
        voice = voice[:n]
        m_rms = active_rms(mus)
        fx *= (m_rms * 10 ** (-SFX_DB / 20)) / active_rms(fx)
        voice *= (m_rms * 10 ** (-VOICE_DB / 20)) / active_rms(voice)
        m_rms = active_rms(mus)
    m_rms = active_rms(mus)
    lim = m_rms * 10 ** (6 / 20) * 3
    fx = np.tanh(fx / lim) * lim
    ir_n = int(0.6 * SR)
    ir = np.random.default_rng(3).standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 9)
    ir = lp(ir, 5000) * 0.05
    narrated = os.path.exists(voice_path) and getattr(ep, "NARRATION", None)
    send = fx if narrated else fx + voice          # keep the narration dry for intelligibility
    wet = np.stack([signal.fftconvolve(send[:, ch], ir)[:n] for ch in range(2)], axis=1)
    mix = mus + fx + voice + wet * 0.5
    # bring the whole thing to about -16 dBFS RMS, then catch peaks gently
    rms = float(np.sqrt((mix ** 2).mean()))
    mix *= 10 ** (-16 / 20) / max(rms, 1e-9)
    mix = np.tanh(mix / 0.9) * 0.9
    # short crossfade at the loop seam so the end flows back into the start
    fade = int(0.02 * SR)
    mix[:fade] *= np.linspace(0, 1, fade)[:, None]
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", f"{epname}_audio.wav")
    wavfile.write(path, SR, (mix * 32767).astype(np.int16))
    print("wrote", path, round(len(mix) / SR, 2), "s")


if __name__ == "__main__":
    build(sys.argv[1])
