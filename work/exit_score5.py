"""THE EXIT MANUAL — v5 score: original dark, epic electronic music, synthesised in numpy (nothing sampled).

    python3 exit_score5.py --test            # -> out/exit_music_test_v5.wav (20 s, the whole arc) + analysis
    python3 exit_score5.py exit_ep005        # -> out/exit_ep005_audio.wav (score + effects + voice, mixed)

Owner's notes (26 Oct 2026): dark and epic, in the spirit of Mozart's Lacrimosa or the old Anonymous videos.
Dark electronic: low drones and pads in a minor key, deep sub-bass, slow pulses, a slow heavy HALF-TIME beat
(one kick and one deep impact a bar: never a march), digital textures and glitches, tension that rises to the end.
Never: organ, full chorale harmony, snare rolls, marching rhythm, any recording or sample.

Language: D minor, 64 BPM, 12/8 feel (each beat = 3 triplet eighths). Progression Dm | Bb | Gm | A (the dominant
of harmonic minor: dark, not churchy: no four-voice block chords, the pads are open, detuned, filtered synths).
What it borrows from the Lacrimosa (Requiem K. 626, 1791, public domain) is its gestures, written here from scratch:
the slow 12/8 sway, falling two-note "sighs" over each chord, and a slow chromatic climb before the last word.
Layers, each driven by one intensity curve I(t) in [0, 1] given by the episode (music_plan()):
  drone   D1/A1 detuned saws, slow breathing low-pass          always
  sub     sine roots + soft 2nd harmonic (audible on phones)  always
  pad     wide detuned saw chords, cut-off opens with I        0.15 + 0.85 I
  sighs   glassy FM pluck, falling pairs, ping-pong delay      from I > 0.3
  arp     triplet-eighth filtered saw arpeggio                 from I > 0.45
  beat    half-time: deep kick on 1, a ghost kick, a dark impact on 3 (low tom + band noise, big room)  I > 0.55
  grit    bit-crushed ticks and digital air; stutter glitches at the cuts the episode lists
  climb   a chromatic rising saw line (plan["climb"]) that lands on D at the last word
  heart   "lub-dub" sub thumps (plan["heart"]): the logo's heartbeat; the beat stops so the heart is the pulse
Mix: music about 13 dB under the voice (active RMS, after ducking), ducked 4 dB while Relay speaks, a further
3 dB under key lines; effects 17 dB under the voice. Reuses exit_audio.dark_sfx and the Tiny Laws helpers.
"""
import importlib
import json
import os
import sys

import numpy as np
from scipy import signal
from scipy.io import wavfile

from audio import SR, place, lp, hp, bp, midi, t_

HERE = os.path.dirname(os.path.abspath(__file__))
BPM = 64
BEAT = 60.0 / BPM
BAR = 4 * BEAT
# (pad voicing, bass root, sighs: [(upper, lower), (upper, lower)])
CHORDS = [
    ([50, 57, 62, 65, 69], 38, [(70, 69), (64, 62)]),     # Dm   (D3 A3 D4 F4 A4 / D2)
    ([50, 58, 62, 65, 70], 34, [(72, 70), (67, 65)]),     # Bb   (over Bb1)
    ([50, 55, 62, 67, 70], 31, [(69, 67), (64, 62)]),     # Gm   (over G1)
    ([49, 57, 61, 64, 69], 33, [(74, 73), (65, 64)]),     # A    (over A1, C# leading note)
]
MUSIC_UNDER_VOICE_DB = 13.0
SFX_UNDER_VOICE_DB = 17.0
DUCK_DB = 4.0
DIP_DB = 3.0


# ------------------------------------------------------------------ helpers
def curve(D, pts):
    """Piecewise-linear curve over D seconds from [(t, v), ...]."""
    tt = np.arange(int(D * SR)) / SR
    ts, vs = zip(*sorted(pts))
    return np.interp(tt, ts, vs).astype(np.float32)


def gate(I, lo, width):
    return np.clip((I - lo) / width, 0, 1)


def saws(freqs, d, det=(-0.006, -0.002, 0.002, 0.0065), seed=0):
    tt = t_(d)
    r = np.random.default_rng(seed)
    out = np.zeros((len(tt), 2))
    for f in freqs:
        for j, dd in enumerate(det):
            ph = 2 * np.pi * f * (1 + dd) * tt + r.uniform(0, 6.28)
            x = signal.sawtooth(ph)
            pan = -0.8 + 1.6 * j / max(1, len(det) - 1)
            out[:, 0] += x * np.cos((pan + 1) * np.pi / 4)
            out[:, 1] += x * np.sin((pan + 1) * np.pi / 4)
    return out / (len(freqs) * len(det)) * 2


def lp2(x, f, order=2):
    return np.stack([lp(x[:, c], f, order) for c in range(2)], axis=1)


def room(x, secs=3.2, decay=2.0, tone=2600, seed=4, wet=0.5):
    n = len(x)
    ir_n = int(secs * SR)
    r = np.random.default_rng(seed)
    out = x.copy()
    for c in range(2):
        ir = r.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * decay)
        ir = lp(ir, tone) * 0.02
        ir[: int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
        out[:, c] += signal.fftconvolve(x[:, c], ir)[:n] * wet
    return out


def pingpong(x, delay, fb=0.45, n_rep=5):
    out = x.copy()
    d = int(delay * SR)
    for k in range(1, n_rep + 1):
        g = fb ** k
        src = x[:, (k % 2)]
        dst = 1 - (k % 2)
        if d * k < len(x):
            out[d * k:, dst] += src[: len(x) - d * k] * g
    return out


# ------------------------------------------------------------------ instruments
def pad_chord(ms, d, bright):
    """Detuned saw chord, slow swell, two cut-offs crossfaded by 'bright' (0..1). Not an organ: detuned, filtered,
    with a slow attack and a breathing filter."""
    x = saws([midi(m) for m in ms], d, seed=sum(ms))
    tt = t_(d)
    e = np.minimum(1, tt / 1.2) * np.clip((d - tt) / 1.0, 0, 1)
    dark = lp2(x, 420, 2)
    lite = lp2(x, 1900, 2)
    return (dark * (1 - bright) + lite * bright) * e[:, None]


def glass(m, d=1.6, v=1.0):
    """Glassy digital FM pluck: the sighs."""
    tt = t_(d)
    f = midi(m)
    mod = np.sin(2 * np.pi * f * 2.0 * tt) * 1.6 * np.exp(-tt * 5)
    x = np.sin(2 * np.pi * f * tt + mod) * np.exp(-tt * 2.6)
    x += 0.25 * np.sin(2 * np.pi * f * 0.5 * tt) * np.exp(-tt * 3)
    x = np.round(x * 24) / 24                                    # a little bit-crush: digital
    return lp(x, 3800) * np.minimum(1, tt / 0.006) * v


def pluck_saw(m, d=0.35, v=1.0):
    tt = t_(d)
    x = signal.sawtooth(2 * np.pi * midi(m) * tt) * 0.6 + signal.square(2 * np.pi * midi(m) * 1.003 * tt, 0.3) * 0.3
    x = lp(x, 1400, 2)
    return x * np.minimum(1, tt / 0.003) * np.exp(-tt * 9) * v


def cello(m, d):
    """A bowed, cello-like synth line (200-800 Hz): slow attack, vibrato, saturated, dark. Carries the sighs in
    the mid-range so phones hear the melody."""
    tt = t_(d)
    f = midi(m) * (1 + 0.004 * np.sin(2 * np.pi * 5.2 * tt) * np.minimum(1, tt / 0.4))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = signal.sawtooth(ph) * 0.7 + signal.sawtooth(ph * 1.003) * 0.5
    x = np.tanh(lp(x, 1100, 2) * 1.6)
    e = np.minimum(1, tt / 0.18) * np.clip((d - tt) / 0.25, 0, 1)
    x = x * e
    return np.stack([x * 0.9, np.roll(x, 300) * 0.9], axis=1)


def kick(v=1.0):
    tt = t_(0.9)
    f = 38 + 70 * np.exp(-tt * 22)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 4.5)
    x = np.tanh(x * 2.2) * 0.8
    sk = skin(0.25, 130, 0.35, 0.3, 1)
    x[: len(sk)] += sk
    return x * v


def impact(v=1.0, seed=0):
    """The half-time backbeat: a deep, dark impact (low tom body + band-limited noise), no snare wires, no roll."""
    r = np.random.default_rng(seed + 50)
    tt = t_(1.2)
    f = 62 + 55 * np.exp(-tt * 16)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 5.5)
    nz = bp(r.uniform(-1, 1, len(tt)), 180, 1700) * np.exp(-tt * 11) * 0.7
    return np.tanh((body + nz) * 1.8) * 0.7 * v


def skin(d=0.25, f0=140, v=1.0, click=0.25, seed=0):
    """What a phone speaker can play of a low thump: a saturated 100-250 Hz body and a short 2-4 kHz click."""
    tt = t_(d)
    f = f0 * (1 + 0.6 * np.exp(-tt * 30))
    body = np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * 3.0) * np.exp(-tt * 14)
    body = bp(body, 90, 400)
    r = np.random.default_rng(seed)
    ck = bp(r.uniform(-1, 1, len(tt)), 2000, 4500) * np.exp(-tt * 260) * click
    return (body + ck) * v


def heart_thump(v=1.0):
    tt = t_(0.55)
    f = 34 + 38 * np.exp(-tt * 18)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7.5) * np.minimum(1, tt / 0.004)
    x = np.tanh(x * 2.6)                                          # harmonics so phones hear it
    x = lp(x, 900)
    sk = skin(0.3, 120, 0.45, 0.18, 3)
    x[: len(sk)] += sk
    return x * v


def heartbeat(v=1.0):
    """Lub-dub: the second thump 0.30 s later and softer."""
    out = np.zeros(int(1.0 * SR))
    a = heart_thump(v)
    b = heart_thump(0.68 * v)
    out[: len(a)] += a
    i = int(0.30 * SR)
    out[i:i + len(b)] += b[: len(out) - i]
    return out


def braam(d=3.6, v=1.0):
    """A big low synth swell for the hits (epic, cinematic): D1 + D2 + A2 detuned saws, filter opening then
    closing, saturated. Synth, not brass samples."""
    tt = t_(d)
    x = saws([midi(26), midi(38), midi(45)], d, det=(-0.01, -0.003, 0.004, 0.011), seed=77)
    fc = 180 + 1500 * np.sin(np.pi * np.clip(tt / 2.2, 0, 1)) ** 2 * np.exp(-tt * 0.4)
    out = np.zeros_like(x)
    hop = 1024
    for i in range(0, len(tt), hop):
        seg = x[max(0, i - 2048): i + hop]
        y = lp2(seg, fc[i], 2)
        out[i:i + hop] = y[-min(hop, len(tt) - i):]
    e = np.minimum(1, tt / 0.08) * np.exp(-tt * 0.7)
    return np.tanh(out * e[:, None] * 2.0) * v


def tick(r):
    d = int(r.uniform(0.008, 0.04) * SR)
    g = bp(r.uniform(-1, 1, d), r.uniform(1800, 4200), 8000) * np.exp(-np.arange(d) / d * 3)
    return np.round(g * 5) / 5


def riser(d):
    tt = t_(d)
    r = np.random.default_rng(9)
    n = r.uniform(-1, 1, len(tt))
    out = np.zeros_like(tt)
    hop = 1024
    fc = 200 * (12 ** (tt / d))
    for i in range(0, len(tt), hop):
        seg = n[max(0, i - 512): i + hop]
        y = bp(seg, fc[i] * 0.8, fc[i] * 1.25)
        out[i:i + hop] = y[-min(hop, len(tt) - i):]
    return out * (tt / d) ** 2 * 1.2


# ------------------------------------------------------------------ the score
def score(D, plan, seed=0):
    """plan = dict(anchor=t of a downbeat, intensity=[(t, I)], heart=(t0, t1, fade_from), climb=(t0, t1),
    cuts=[t...], hits=[t...], risers=[(t_end, dur)], beat_off=[(a, b)])."""
    n = int(D * SR)
    I = curve(D, plan["intensity"])
    anchor = plan.get("anchor", 0.0)
    first = anchor - np.ceil(anchor / BAR) * BAR                 # a downbeat at or before 0
    bars = np.arange(first, D + BAR, BAR)
    buf = {k: np.zeros((n + SR * 6, 2)) for k in ("drone", "sub", "pad", "sigh", "arp", "beat", "grit", "climb",
                                                   "heart", "fx", "cello")}
    tt = np.arange(n) / SR
    # drone: D1 + A1, slow breathing filter
    dr = saws([midi(26), midi(33), midi(38)], D + 1, det=(-0.004, 0.0, 0.0037), seed=1)[:n]
    breath = 0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * tt)
    dr = lp2(dr, 260) * (1 - breath[:, None]) + lp2(dr, 620) * breath[:, None]
    buf["drone"][:n] += dr * 1.3
    # per bar
    hb = plan.get("heart")
    for bi, b0 in enumerate(bars):
        k = int(round((b0 - anchor) / BAR)) % 4
        ms, root, sighs = CHORDS[k]
        i0 = max(0, int(b0 * SR))
        Ib = float(I[min(n - 1, max(0, int((b0 + BAR / 2) * SR)))])
        place_st(buf["pad"], pad_chord(ms, BAR + 1.4, min(1, Ib * 1.1)), b0)
        # sub: root for the bar, sine + soft 2nd harmonic
        d = BAR + 0.05
        u = t_(d)
        s = np.sin(2 * np.pi * midi(root) * u) + 0.22 * np.sin(4 * np.pi * midi(root) * u)
        s *= np.minimum(1, u / 0.08) * np.clip((d - u) / 0.08, 0, 1)
        place(buf["sub"], s, b0, 1.0)
        # sighs: long-short falling pairs on beats 1 and 3 (12/8 sway)
        for j, (hi_, lo_) in enumerate(sighs):
            tb = b0 + j * 2 * BEAT
            place(buf["sigh"], glass(hi_, 1.4, 0.9), tb, 1.0, -0.3 + 0.6 * j)
            place(buf["sigh"], glass(lo_, 2.2, 0.7), tb + 2 * BEAT / 3 * 2, 1.0, 0.3 - 0.6 * j)
            place_st(buf["cello"], cello(hi_ - 12, 2 * BEAT / 3 * 2 + 0.05), tb)
            place_st(buf["cello"], cello(lo_ - 12, 2 * BEAT / 3 * 1 + 0.6), tb + 2 * BEAT / 3 * 2)
        # arp: triplet eighths through the chord tones, two octaves up
        tones = sorted(set(m + 12 for m in ms[1:]))
        order = [0, 2, 1, 3, 2, 4, 3, 1, 2, 4, 3, 2]
        for q in range(12):
            m = tones[order[q] % len(tones)]
            place(buf["arp"], pluck_saw(m, 0.32, 0.55 if q % 3 == 0 else 0.35), b0 + q * BEAT / 3, 1.0,
                  -0.45 if q % 2 else 0.45)
        # beat: half-time. kick on 1, ghost kick on the last triplet of beat 2, impact on 3. Nothing else.
        place(buf["beat"], kick(1.0), b0, 1.0)
        place(buf["beat"], kick(0.45), b0 + BEAT + 2 * BEAT / 3, 1.0)
        place(buf["beat"], impact(0.9, bi), b0 + 2 * BEAT, 1.0)
    # grit: sparse crushed ticks on the triplet grid + faint digital air
    r = np.random.default_rng(17 + seed)
    tq = first
    while tq < D:
        if r.random() < 0.28:
            place(buf["grit"], tick(r) * r.uniform(0.2, 0.6), tq + r.uniform(0, 0.01), 1.0, r.uniform(-0.8, 0.8))
        tq += BEAT / 3
    air = hp(np.random.default_rng(23).standard_normal(n), 4000) * 0.012
    buf["grit"][:n, 0] += air
    buf["grit"][:n, 1] += np.roll(air, 999)
    # climb: chromatic ascent in triplet-quarter steps, landing on D5 at climb end
    if plan.get("climb"):
        c0, c1 = plan["climb"]
        steps = list(range(57, 75))                               # A3 .. D5 (chromatic) -> 18 notes
        st = (c1 - c0) / (len(steps) - 1)
        for j, m in enumerate(steps):
            tj = c0 + j * st
            d = st * 1.15 if j < len(steps) - 1 else 2.8
            u = t_(d)
            x = saws([midi(m), midi(m - 12)], d, det=(-0.004, 0.004), seed=j)
            x = lp2(x, 700 + 2200 * j / len(steps))
            e = np.minimum(1, u / 0.05) * np.clip((d - u) / 0.12, 0, 1)
            place_st(buf["climb"], x * e[:, None] * (0.5 + 0.5 * j / len(steps)), tj)
    # heartbeat (the logo's): lub-dub every beat from t0 to t1, fading out after fade_from
    if hb:
        h0, h1, hf = hb
        tb = h0
        while tb < h1:
            g = 1.0 - 0.75 * np.clip((tb - hf) / max(0.1, h1 - hf), 0, 1)
            place(buf["heart"], heartbeat(g), tb, 1.0)
            tb += BEAT
    for (g0, g1, gg) in plan.get("heart_ghost", []):
        tb = g0
        while tb < g1:
            place(buf["heart"], heartbeat(gg), tb, 1.0)
            tb += BEAT
    # punctuation: deep hits, risers
    for th in plan.get("hits", []):
        place(buf["fx"], impact(1.2, 99) + 0, th, 1.0)
        place(buf["fx"], kick(1.0), th, 1.0)
        place_st(buf["fx"], braam(3.6, 0.55), th)
    for (te, dur) in plan.get("risers", []):
        place(buf["fx"], riser(dur) * 0.5, te - dur, 1.0, -0.2)
        place(buf["fx"], riser(dur) * 0.5, te - dur + 0.013, 1.0, 0.2)
    for k_ in buf:
        buf[k_] = buf[k_][:n]
    # gains from the intensity curve
    beat_on = np.ones(n, np.float32)
    for (a, b) in plan.get("beat_off", []):
        beat_on[max(0, int(a * SR)):min(n, int(b * SR))] = 0
    w = int(0.4 * SR)
    beat_on = np.convolve(beat_on, np.ones(w) / w, mode="same")
    G = {
        "drone": 0.55 + 0.25 * I,
        "sub": 0.5 + 0.3 * I,
        "pad": 0.15 + 0.85 * I,
        "sigh": gate(I, 0.3, 0.25),
        "arp": gate(I, 0.45, 0.25),
        "beat": gate(I, 0.55, 0.15) * beat_on,
        "grit": 0.4 + 0.6 * I,
        "climb": np.ones(n),
        "heart": np.ones(n),
        "fx": np.ones(n),
        "cello": gate(I, 0.4, 0.3),
    }
    VOL = {"drone": 0.45, "sub": 0.42, "pad": 0.5, "sigh": 0.22, "arp": 0.16, "beat": 0.75, "grit": 0.35,
           "climb": 0.32, "heart": 1.15, "fx": 0.55, "cello": 0.30}
    wet_bus = (buf["pad"] * (G["pad"] * VOL["pad"])[:, None] + buf["sigh"] * (G["sigh"] * VOL["sigh"])[:, None]
               + buf["climb"] * VOL["climb"] + buf["cello"] * (G["cello"] * VOL["cello"])[:, None])
    wet_bus = pingpong(buf["sigh"] * (G["sigh"] * VOL["sigh"])[:, None], BEAT * 2 / 3, 0.4) + wet_bus
    arp = pingpong(buf["arp"] * (G["arp"] * VOL["arp"])[:, None], BEAT / 2, 0.35)
    roomy = room(wet_bus + arp + buf["beat"] * (G["beat"] * VOL["beat"] * 0.6)[:, None]
                 + buf["fx"] * VOL["fx"] * 0.5, 3.4, 1.7, 2400, 4, 0.9)
    dry = (buf["drone"] * (G["drone"] * VOL["drone"])[:, None] + buf["sub"] * (G["sub"] * VOL["sub"])[:, None]
           + buf["beat"] * (G["beat"] * VOL["beat"])[:, None] + buf["grit"] * (G["grit"] * VOL["grit"])[:, None]
           + buf["heart"] * VOL["heart"] + buf["fx"] * VOL["fx"] * 0.6)
    mix = dry + roomy
    # glitches at the cuts: a short stutter (a 70 ms slice repeated, filtered), never louder than the music
    for tc in plan.get("cuts", []):
        i = int(tc * SR)
        sl = int(0.07 * SR)
        if 0 < i - sl and i + 5 * sl < n:
            src = mix[i - sl:i].copy()
            for k_ in range(5):
                g = 0.9 * (1 - k_ / 6)
                mix[i + k_ * sl:i + (k_ + 1) * sl] = mix[i + k_ * sl:i + (k_ + 1) * sl] * 0.35 + \
                    np.round(src * g * 8) / 8 * 0.65
    mix = np.tanh(mix * 1.1) / 1.1
    return mix.astype(np.float32), I


def place_st(buf, x, t):
    i = int(t * SR)
    if i >= len(buf):
        return
    if i < 0:
        x = x[-i:]
        i = 0
    m = min(len(x), len(buf) - i)
    buf[i:i + m] += x[:m]


# ------------------------------------------------------------------ analysis (the "listen check")
def analyse(x, I=None, label=""):
    """Numbers that check the rules: key, tempo of the pulse, no snare roll, no organ-like steady spectrum."""
    mono = x.mean(axis=1) if x.ndim > 1 else x
    n = len(mono)
    rep = {}
    # 1. pitch classes (chroma) 60-1000 Hz -> key estimate (Krumhansl profiles, major/minor)
    f, tt, Z = signal.stft(mono, SR, nperseg=8192, noverlap=4096)
    P = np.abs(Z) ** 2
    band = (f > 55) & (f < 1000)
    pc = np.zeros(12)
    for fi in np.where(band)[0]:
        p = int(round(12 * np.log2(f[fi] / 440.0))) % 12
        pc[(p + 9) % 12] += P[fi].sum()
    pc /= pc.sum()
    maj = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    mnr = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
    names = "C C# D D# E F F# G G# A A# B".split()
    best = max(((np.corrcoef(pc, np.roll(prof, k))[0, 1], names[k] + (" minor" if mi else " major"))
                for mi, prof in ((0, maj), (1, mnr)) for k in range(12)))
    rep["key"] = f"{best[1]} (r={best[0]:.2f})"
    # 2. onset pulse: low band (< 150 Hz) envelope autocorrelation -> beat period
    lo = lp(mono, 150, 4)
    hop = 441
    e = np.sqrt(np.convolve(lo ** 2, np.ones(hop) / hop, mode="same")[::hop])
    od = np.maximum(0, np.diff(e))
    ac = np.correlate(od - od.mean(), od - od.mean(), "full")[len(od) - 1:]
    lags = np.arange(len(ac)) * hop / SR
    ok = (lags > 0.4) & (lags < 4.5)
    per = lags[ok][np.argmax(ac[ok])]
    rep["low pulse period"] = f"{per:.2f} s ({60 / per:.0f}/min)"
    # 3. snare-roll test: fast repeated hits in the 1.5-6 kHz band (> 6 onsets/s for 0.5 s)
    hb = bp(mono, 1500, 6000)
    eh = np.sqrt(np.convolve(hb ** 2, np.ones(220) / 220, mode="same")[::220])     # 5 ms frames
    on = np.where((eh[1:] > 2.2 * (np.convolve(eh, np.ones(40) / 40, mode="same")[1:] + 1e-6)) &
                  (eh[1:] > 0.08 * eh.max()))[0] * 220 / SR
    on = np.unique(np.round(on, 2))
    rolls = 0
    for t0 in on:
        if ((on > t0) & (on < t0 + 0.5)).sum() >= 4:
            rolls += 1
    rolls = int(rolls)
    rep["fast high-band hit runs (snare-roll test)"] = rolls
    # 4. organ test: a steady spectrum (no movement) with many exact harmonics and a flat envelope.
    #    measured as the median frame-to-frame spectral change of the 200-3000 Hz band (organ ~ near 0)
    band2 = (f > 200) & (f < 3000)
    S = np.log(P[band2] + 1e-12)
    flux = np.median(np.abs(np.diff(S, axis=1)))
    rep["spectral movement 200 Hz-3 kHz (organ ~ <0.3)"] = round(float(flux), 2)
    # 5. level shape: first and last third RMS (tension rising)
    thirds = [20 * np.log10(np.sqrt((mono[i * n // 3:(i + 1) * n // 3] ** 2).mean()) + 1e-9) for i in range(3)]
    rep["RMS by thirds (dB)"] = [round(float(v), 1) for v in thirds]
    ph = hp(mono, 200, 4)
    rep["phone check: level through a 200 Hz high-pass (dB vs full)"] = round(
        float(10 * np.log10((ph ** 2).sum() / (mono ** 2).sum())), 1)
    rep["sub share < 80 Hz"] = round(float((lp(mono, 80, 4) ** 2).sum() / (mono ** 2).sum()), 2)
    print(label, json.dumps(rep, indent=1, ensure_ascii=False, default=float))
    return rep


def to_lufs(x, target=-14.0):
    """Normalise to the target loudness (measured by ffmpeg ebur128), true peak kept below -1 dBTP."""
    import re
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, "a.wav"), os.path.join(d, "b.wav")
        wavfile.write(a, SR, (np.clip(x / (np.abs(x).max() + 1e-9) * 0.5, -1, 1) * 32767).astype(np.int16))
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", a, "-af", "ebur128", "-f", "null", "-"],
                           capture_output=True, text=True)
        li = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
        g = target - li
        lim = 10 ** (-1.5 / 20)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a, "-af",
                        f"volume={g:.2f}dB,aresample=192000,alimiter=limit={lim:.4f}:attack=3:release=80:level=false,"
                        f"aresample={SR}", b], check=True)
        _, y = wavfile.read(b)
    return y.astype(np.float32) / 32768


# ------------------------------------------------------------------ 20 s test: the whole arc, compressed
def test():
    D = 20.0
    a0 = 0.6
    plan = dict(anchor=a0,
                intensity=[(0, 0.2), (3.0, 0.3), (4.5, 0.6), (8.0, 0.7), (9.5, 0.25), (11.5, 0.3), (12.0, 0.6),
                           (14.8, 0.95), (15.6, 0.8), (18.5, 0.6), (20, 0.35)],
                beat_off=[(9.2, 12.0), (14.6, 20.1)],
                climb=(12.2, a0 + 4 * BAR),
                heart=(a0 + 4 * BAR, 20.2, 17.8),
                hits=[0.05, a0 + 4 * BAR - 0.02],
                risers=[(a0 + 4 * BAR, 2.6)],
                cuts=[4.5, 9.2], heart_ghost=[(9.3, 11.8, 0.35)])
    x, I = score(D, plan)
    fade = int(1.2 * SR)
    x[-fade:] *= np.linspace(1, 0, fade)[:, None]
    y = to_lufs(x, -14)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    p = os.path.join(HERE, "out", "exit_music_test_v5.wav")
    wavfile.write(p, SR, (y * 32767).astype(np.int16))
    print("wrote", p)
    analyse(x, I, "TEST 20 s")
    print("heart on beats from", round(a0 + 4 * BAR, 2), "s, period", round(BEAT, 3), "s (", BPM, "/min)")


# ------------------------------------------------------------------ the episode mix
def active_rms(x):
    e = np.abs(x).max(axis=1) if x.ndim > 1 else np.abs(x)
    win = int(0.05 * SR)
    sm = np.convolve(e, np.ones(win) / win, mode="same")
    act = x[sm > 1e-3]
    return float(np.sqrt((act ** 2).mean())) if len(act) else 1e-9


def build(epname):
    from exit_audio import dark_sfx
    ep = importlib.import_module(epname)
    D = ep.DURATION
    n = int(D * SR)
    plan = ep.music_plan()
    mus, I = score(D, plan)
    mus = mus[:n]
    fx = np.zeros((n + SR * 3, 2))
    for (t, name, p) in ep.sfx_list():
        place(fx, dark_sfx(name, p), t, 1.0, 0.2 * ((p % 3) - 1))
    fx = fx[:n]
    vsr, v = wavfile.read(os.path.join(HERE, "out", f"{epname}_voice.wav"))
    v = v.astype(np.float32) / 32768.0
    if vsr != SR:
        v = signal.resample_poly(v, SR, vsr).astype(np.float32)
    v = np.pad(v, (0, max(0, n - len(v))))[:n]
    voice = np.stack([v, v], axis=1)
    v_rms = active_rms(voice)
    # ducking while Relay speaks, plus dips under key lines
    e = np.abs(v)
    att, rel = int(0.04 * SR), int(0.35 * SR)
    sm = np.convolve(e, np.ones(att) / att, mode="same")
    talk = np.convolve((sm > 0.02).astype(np.float32), np.ones(rel) / rel, mode="same")
    duck = 1.0 - (1.0 - 10 ** (-DUCK_DB / 20)) * np.clip(talk * 1.5, 0, 1)
    dip = np.ones(n, np.float32)
    for (a_, b_) in ep.music_dips():
        dip[max(0, int(a_ * SR)):min(n, int(b_ * SR))] = 10 ** (-DIP_DB / 20)
    w = int(0.3 * SR)
    dip = np.convolve(dip, np.ones(w) / w, mode="same")
    mus = mus * (duck * dip)[:, None]
    mus *= (v_rms * 10 ** (-MUSIC_UNDER_VOICE_DB / 20)) / active_rms(mus)
    fx *= (v_rms * 10 ** (-SFX_UNDER_VOICE_DB / 20)) / active_rms(fx)
    mix = mus + fx + voice
    rms = float(np.sqrt((mix ** 2).mean()))
    mix *= 10 ** (-17 / 20) / max(rms, 1e-9)
    mix = np.tanh(mix / 0.9) * 0.9
    fade = int(0.03 * SR)
    mix[:fade] *= np.linspace(0, 1, fade)[:, None]
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    path = os.path.join(HERE, "out", f"{epname}_audio.wav")
    wavfile.write(path, SR, (mix * 32767).astype(np.int16))
    wavfile.write(os.path.join(HERE, "out", f"{epname}_music.wav"), SR,
                  (mus / (np.abs(mus).max() + 1e-9) * 0.8 * 32767).astype(np.int16))

    def db(x):
        return 20 * np.log10(active_rms(x) + 1e-12)
    talking = talk > 0.5
    m_sp = 20 * np.log10(np.sqrt((mus[talking] ** 2).mean()) + 1e-12)
    v_sp = 20 * np.log10(np.sqrt((voice[talking] ** 2).mean()) + 1e-12)
    print(f"wrote {path} {len(mix) / SR:.2f}s | music {db(mus) - db(voice):+.1f} dB vs voice "
          f"(during speech {m_sp - v_sp:+.1f} dB), effects {db(fx) - db(voice):+.1f} dB vs voice")
    analyse(mus, I, "EPISODE MUSIC")


if __name__ == "__main__":
    if sys.argv[1] == "--test":
        test()
    else:
        build(sys.argv[1])
