"""THE EXIT MANUAL — soundtrack: a dark, calm synth bed, soft terminal effects, Relay's voice on top.

    python3 exit_audio.py exit_ep001     # -> out/exit_ep001_audio.wav  (run exit_voice.py first)

Mix rules (owner's standing feedback): music 13 dB under the voice, ducking 4 dB more while Relay speaks;
effects 19 dB under the voice; nothing sharp or loud. Reuses the Tiny Laws synthesis helpers (audio.py).
The episode gives BPM, optional TRANSPOSE / CHORDS, and sfx_list() -> [(t, name, variant), ...].
"""
import importlib
import os
import sys

import numpy as np
from scipy import signal
from scipy.io import wavfile

from audio import SR, place, lp, hp, bp, noise, env, midi, t_, kick2, hat

HERE = os.path.dirname(os.path.abspath(__file__))
MUSIC_UNDER_VOICE_DB = 13.0
SFX_UNDER_VOICE_DB = 19.0
DUCK_DB = 4.0

# A minor: Am - F - Dm - Em (one chord per bar), low and wide
CHORDS = [([57, 60, 64, 69], 45), ([53, 57, 60, 65], 41), ([50, 57, 62, 65], 38), ([52, 55, 59, 64], 40)]
ARP = [0, 2, 1, 3, 2, 1, 3, 2]   # chord-tone order for the 8th-note arpeggio


def pad(ms, d, v=1.0):
    tt = t_(d)
    x = np.zeros_like(tt)
    for m in ms:
        f = midi(m)
        for det in (-0.006, 0.0, 0.0055):
            x += signal.sawtooth(2 * np.pi * np.cumsum(np.full_like(tt, f * (1 + det))) / SR) * 0.3
    x = lp(x, 1100, 2)
    e = np.minimum(1, tt / 0.6) * np.clip((d - tt) / 0.5, 0, 1)
    return x * e * v / len(ms)


def pluck(m, d=0.5, v=1.0):
    tt = t_(d)
    f = midi(m)
    x = signal.square(2 * np.pi * f * tt, 0.3) * 0.5 + np.sin(2 * np.pi * f * tt) * 0.5
    x = lp(x, 1800, 2)
    return x * np.minimum(1, tt / 0.004) * np.exp(-tt * 7) * v


def sub(m, d, v=1.0):
    tt = t_(d)
    x = np.sin(2 * np.pi * midi(m) * tt)
    return x * np.minimum(1, tt / 0.01) * np.clip((d - tt) / 0.05, 0, 1) * np.exp(-tt * 1.2) * v


def music(D, bpm, transpose=0, chords=CHORDS, quiet=()):
    beat = 60.0 / bpm
    bar = 4 * beat
    n = int((D + 3) * SR)
    bus = {k: np.zeros((n, 2)) for k in ("pad", "bass", "arp", "drums")}
    nb = int(np.ceil(D / bar)) + 1
    for b in range(nb):
        t0 = b * bar
        ch, root = chords[b % len(chords)]
        ch = [m + transpose for m in ch]
        root += transpose
        in_quiet = any(a <= t0 < z for a, z in quiet)
        place(bus["pad"], pad(ch, bar + 0.6, 0.9), t0, 1, -0.2)
        place(bus["pad"], pad([m + 12 for m in ch[1:3]], bar + 0.6, 0.25), t0, 1, 0.3)
        for k in range(4):
            place(bus["bass"], sub(root, beat * 0.95, 0.8), t0 + k * beat, 1)
        if not in_quiet:
            for k in range(8):
                m = ch[ARP[k] % len(ch)] + 12
                place(bus["arp"], pluck(m, 0.45, 0.35 if k % 2 else 0.45), t0 + k * beat / 2, 1, 0.35 if k % 2 else -0.35)
            place(bus["drums"], kick2(0.55), t0, 1)
            place(bus["drums"], kick2(0.45), t0 + 2 * beat, 1)
            for k in range(4):
                place(bus["drums"], hat(0.12), t0 + k * beat + beat / 2, 1, 0.2)
    mix = bus["pad"] * 0.9 + bus["bass"] * 0.7 + bus["arp"] * 0.45 + bus["drums"] * 0.5
    # a long, dark room
    ir_n = int(1.4 * SR)
    ir = np.random.default_rng(4).standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 4)
    ir = lp(ir, 3500) * 0.03
    wet = np.stack([signal.fftconvolve(mix[:, c], ir)[:n] for c in range(2)], axis=1)
    mix = mix + wet * 0.6
    return np.tanh(mix * 0.8)[: int(D * SR)]


# ------------------------------------------------------------------ soft effects (always low)
def sfx(name, p=0):
    r = np.random.default_rng(p + 7)
    if name == "whoosh_low":
        d = 0.6
        x = noise(d)
        out = np.zeros_like(x)
        f = np.geomspace(300, 1600, len(x))
        hop = 512
        for i in range(0, len(x), hop):
            seg = x[max(0, i - 256): i + hop]
            yb = bp(seg, f[i] * 0.7, f[i] * 1.4)
            out[i:i + hop] = yb[-min(hop, len(x) - i):]
        return out * np.sin(np.pi * np.arange(len(x)) / len(x)) ** 2 * 0.7
    if name == "rise":
        d = 0.8
        tt = t_(d)
        f = 220 * (2.0 ** (tt / d))
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) * 0.35
    if name == "blip":
        f = midi([76, 79, 81, 84, 88][p % 5])
        tt = t_(0.18)
        return (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 22) * 0.5
    if name == "keys":                    # a short burst of soft terminal key clicks
        d = 0.7
        out = np.zeros(int(d * SR))
        for k in range(9):
            i = int((k * 0.07 + r.uniform(0, 0.02)) * SR)
            c = hp(noise(0.012), 2500) * env(int(0.012 * SR), 0.0005, 0.012, 5) * r.uniform(0.3, 0.6)
            out[i:i + len(c)] += c[: len(out) - i]
        return out
    if name == "coin":
        f = midi(84 + (p % 3) * 2)
        tt = t_(0.12)
        return np.sin(2 * np.pi * f * tt) * np.exp(-tt * 40) * 0.35
    if name == "clunk":
        tt = t_(0.3)
        f = 90 + 80 * np.exp(-tt * 30)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 14) * 0.8
    if name == "low_hit":
        tt = t_(1.2)
        f = 55 + 40 * np.exp(-tt * 12)
        return np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 3) * 1.5) * 0.7
    raise ValueError(name)


def active_rms(x):
    e = np.abs(x).max(axis=1) if x.ndim > 1 else np.abs(x)
    win = int(0.05 * SR)
    sm = np.convolve(e, np.ones(win) / win, mode="same")
    act = x[sm > 1e-3]
    return float(np.sqrt((act ** 2).mean())) if len(act) else 1e-9


def build(epname):
    ep = importlib.import_module(epname)
    D = ep.DURATION
    n = int(D * SR)
    mus = music(D, ep.BPM, getattr(ep, "TRANSPOSE", 0), getattr(ep, "CHORDS", CHORDS), getattr(ep, "MUSIC_QUIET", ()))
    fx = np.zeros((n + SR * 3, 2))
    for (t, name, p) in ep.sfx_list():
        place(fx, sfx(name, p), t, 1.0)
    fx = fx[:n]
    vsr, v = wavfile.read(os.path.join(HERE, "out", f"{epname}_voice.wav"))
    v = v.astype(np.float32) / 32768.0
    if vsr != SR:
        v = signal.resample_poly(v, SR, vsr).astype(np.float32)
    v = np.pad(v, (0, max(0, n - len(v))))[:n]
    voice = np.stack([v, v], axis=1)
    v_rms = active_rms(voice)
    mus *= (v_rms * 10 ** (-MUSIC_UNDER_VOICE_DB / 20)) / active_rms(mus)
    fx *= (v_rms * 10 ** (-SFX_UNDER_VOICE_DB / 20)) / active_rms(fx)
    e = np.abs(v)
    att, rel = int(0.04 * SR), int(0.35 * SR)
    sm = np.convolve(e, np.ones(att) / att, mode="same")
    talk = np.convolve((sm > 0.02).astype(np.float32), np.ones(rel) / rel, mode="same")
    duck = 1.0 - (1.0 - 10 ** (-DUCK_DB / 20)) * np.clip(talk * 1.5, 0, 1)
    mus *= duck[:, None]
    mix = mus + fx + voice
    rms = float(np.sqrt((mix ** 2).mean()))
    mix *= 10 ** (-17 / 20) / max(rms, 1e-9)
    mix = np.tanh(mix / 0.9) * 0.9
    fade = int(0.03 * SR)                          # loop seam
    mix[:fade] *= np.linspace(0, 1, fade)[:, None]
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    path = os.path.join(HERE, "out", f"{epname}_audio.wav")
    wavfile.write(path, SR, (mix * 32767).astype(np.int16))
    # report the real levels (active RMS) so the mix rules can be checked
    def db(x):
        return 20 * np.log10(active_rms(x) + 1e-12)
    print(f"wrote {path} {len(mix) / SR:.2f}s | music {db(mus) - db(voice):+.1f} dB vs voice, "
          f"effects {db(fx) - db(voice):+.1f} dB vs voice")


# ------------------------------------------------------------------ v3 dark score (owner notes, 26 Oct 2026)
# Low drones, a slow pulse, digital textures, sub-bass, short bursts of static as punctuation. No melody to hum,
# nothing bright. The episode gives SCORE = "dark", BPM (the pulse), music_sections() -> [(a, b, state)],
# music_dips() -> [(a, b)] (extra dip under key lines) and sfx_list().
DARK_UNDER_VOICE_DB = 15.0
REQUIEM_UNDER_VOICE_DB = 11.0   # v4: the chorale is the music; still well under the voice
REQUIEM_DIP_DB = 4.0
TEXTURE_UNDER_VOICE_DB = 20.0   # v4: drones, pulse and static sit lower, as a dark floor under the chorale
DIP_DB = 6.0
STATE_GAIN = {   # drone, sub, pulse, texture, high pad, warm third
    "hush": (0.75, 0.6, 0.0, 0.25, 0.0, 0.0),
    "pulse": (0.8, 0.8, 1.0, 0.7, 0.0, 0.0),
    "build": (1.0, 0.9, 1.0, 0.9, 0.8, 0.0),
    "void": (0.3, 0.45, 0.0, 0.1, 0.0, 0.0),
    "resolve": (0.7, 0.8, 0.35, 0.2, 0.6, 0.8),
}


def _ramp(D, sections, idx, fade=0.6):
    n = int(D * SR)
    g = np.zeros(n, np.float32)
    for (a, b, st) in sections:
        ia, ib = max(0, int(a * SR)), min(n, int(b * SR))
        if ib > ia:
            g[ia:ib] = STATE_GAIN[st][idx]
    w = int(fade * SR)
    return np.convolve(g, np.ones(w) / w, mode="same")


def _saw_drone(midis, D, cutoff=320, lfo=0.06, seed=0):
    tt = t_(D)
    r = np.random.default_rng(seed)
    x = np.zeros_like(tt)
    for m in midis:
        for det in (-0.004, 0.0, 0.0037):
            ph = 2 * np.pi * np.cumsum(np.full_like(tt, midi(m) * (1 + det))) / SR + r.uniform(0, 6)
            x += signal.sawtooth(ph) * 0.3
    # slow breathing filter: two passes, cut-off swept by a slow LFO
    lo = lp(x, cutoff * 0.7, 2)
    hi = lp(x, cutoff * 1.6, 2)
    m = 0.5 + 0.5 * np.sin(2 * np.pi * lfo * tt)
    return (lo * (1 - m) + hi * m) / len(midis)


def dark_music(D, bpm, sections, dips):
    n = int(D * SR)
    tt = t_(D)
    drone = _saw_drone([33, 40, 45], D, 300, 0.05, 1)            # A1, E2, A2
    drone += _saw_drone([48], D, 600, 0.031, 2) * 0.35            # a C3 above: minor colour
    sub = np.sin(2 * np.pi * 41.2 * tt) * 0.6 + np.sin(2 * np.pi * 55 * tt) * 0.25
    pulse = np.zeros(n)
    beat = 60.0 / bpm
    k = 0
    while k * beat < D:
        for (dt, v) in ((0.0, 1.0), (0.27, 0.55)):                 # a slow, heavy double beat
            i = int((k * beat + dt) * SR)
            d = int(0.5 * SR)
            u = np.arange(d) / SR
            f = 44 + 50 * np.exp(-u * 30)
            hit = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-u * 7) * v
            pulse[i:i + d] += hit[: max(0, n - i)]
        k += 1
    tex = np.zeros(n)                                              # data: tiny crushed ticks, sparse
    r = np.random.default_rng(17)
    tpos = 0.0
    while tpos < D:
        tpos += r.uniform(0.12, 0.6)
        i = int(tpos * SR)
        d = int(r.uniform(0.01, 0.05) * SR)
        g = bp(r.uniform(-1, 1, d), r.uniform(1800, 3500), 7000) * np.exp(-np.arange(d) / d * 3)
        g = np.round(g * 6) / 6                                    # bit-crushed
        tex[i:i + d] += g[: max(0, n - i)] * r.uniform(0.15, 0.5)
    tex += lp(hp(RNG_DARK.standard_normal(n), 3000), 9000) * 0.03  # faint digital air
    pad = _saw_drone([57, 60, 64], D, 900, 0.08, 3)               # Am, higher, for the build
    third = _saw_drone([61, 64, 69], D, 1100, 0.05, 4)            # A major colour for the way out
    parts = [drone, sub, pulse, tex, pad, third]
    vol = (1.0, 0.55, 0.9, 0.8, 0.5, 0.45)
    mono = sum(p[:n] * v * _ramp(D, sections, j) for j, (p, v) in enumerate(zip(parts, vol)))
    left = mono + 0.15 * tex[:n] * _ramp(D, sections, 3)
    right = mono - 0.15 * tex[:n] * _ramp(D, sections, 3)
    mix = np.stack([left, right], axis=1)
    ir_n = int(2.2 * SR)
    ir = np.random.default_rng(4).standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 2.6)
    ir = lp(ir, 2500) * 0.02
    wet = np.stack([signal.fftconvolve(mix[:, c], ir)[:n] for c in range(2)], axis=1)
    mix = mix + wet * 0.7
    dip = np.ones(n, np.float32)
    for (a, b) in dips:
        dip[max(0, int(a * SR)):min(n, int(b * SR))] = 10 ** (-DIP_DB / 20)
    w = int(0.25 * SR)
    dip = np.convolve(dip, np.ones(w) / w, mode="same")
    return np.tanh(mix * 0.9) * dip[:, None]


RNG_DARK = np.random.default_rng(23)


def dark_sfx(name, p=0):
    r = np.random.default_rng(p + 31)
    if name == "static":                       # a short burst of radio static (punctuation), band-limited
        d = 0.22 + 0.08 * (p % 3)
        x = bp(r.uniform(-1, 1, int(d * SR)), 900, 6500)
        crackle = (r.random(len(x)) < 0.004) * r.uniform(-1, 1, len(x)) * 3
        e = np.minimum(1, np.arange(len(x)) / (0.01 * SR)) * np.clip((len(x) - np.arange(len(x))) / (0.06 * SR), 0, 1)
        return (x + crackle) * e * 0.6
    if name == "sub_drop":
        tt = t_(1.6)
        f = 70 * np.exp(-tt * 1.2) + 30
        return np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.2) * 1.6) * 0.8
    if name == "glitch":                       # stuttered digital grain, no high squeal
        d = 0.5
        out = np.zeros(int(d * SR))
        for k in range(10):
            i = int(r.uniform(0, d - 0.04) * SR)
            g = bp(r.uniform(-1, 1, int(0.03 * SR)), 600, 4000)
            g = np.round(g * 4) / 4
            out[i:i + len(g)] += g[: len(out) - i] * r.uniform(0.3, 0.8)
        return out * 0.6
    if name == "data":                         # a short run of soft digital ticks
        d = 0.6
        out = np.zeros(int(d * SR))
        for k in range(12):
            i = int((k * 0.045 + r.uniform(0, 0.01)) * SR)
            f = r.choice([1760, 2093, 2349, 2637])
            tk = np.sin(2 * np.pi * f * t_(0.02)) * np.exp(-t_(0.02) * 200)
            out[i:i + len(tk)] += tk[: len(out) - i] * r.uniform(0.2, 0.5)
        return out
    return sfx(name, p)


def build_dark(ep, epname):
    D = ep.DURATION
    n = int(D * SR)
    mus = dark_music(D, ep.BPM, ep.music_sections(), ep.music_dips())
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
    req = getattr(ep, "requiem", lambda: None)()
    if req:                                    # v4: an epic layer from a public-domain score (exit_requiem.py)
        from exit_requiem import render
        r = render(req["piece"], req["t0"], req["t1"], req["intensity"], D, req.get("transpose", 0))[:n]
        r *= (v_rms * 10 ** (-REQUIEM_UNDER_VOICE_DB / 20)) / active_rms(r)
        dip = np.ones(n, np.float32)
        for (a_, b_) in ep.music_dips():
            dip[max(0, int(a_ * SR)):min(n, int(b_ * SR))] = 10 ** (-REQUIEM_DIP_DB / 20)
        w = int(0.3 * SR)
        r *= np.convolve(dip, np.ones(w) / w, mode="same")[:, None]
        mus *= (v_rms * 10 ** (-TEXTURE_UNDER_VOICE_DB / 20)) / active_rms(mus)
        mus = mus + r
    else:
        mus *= (v_rms * 10 ** (-DARK_UNDER_VOICE_DB / 20)) / active_rms(mus)
    fx *= (v_rms * 10 ** (-SFX_UNDER_VOICE_DB / 20 + 2 / 20)) / active_rms(fx)
    e = np.abs(v)
    att, rel = int(0.04 * SR), int(0.35 * SR)
    sm = np.convolve(e, np.ones(att) / att, mode="same")
    talk = np.convolve((sm > 0.02).astype(np.float32), np.ones(rel) / rel, mode="same")
    duck = 1.0 - (1.0 - 10 ** (-DUCK_DB / 20)) * np.clip(talk * 1.5, 0, 1)
    mus *= duck[:, None]
    mix = mus + fx + voice
    rms = float(np.sqrt((mix ** 2).mean()))
    mix *= 10 ** (-17 / 20) / max(rms, 1e-9)
    mix = np.tanh(mix / 0.9) * 0.9
    fade = int(0.03 * SR)
    mix[:fade] *= np.linspace(0, 1, fade)[:, None]
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    path = os.path.join(HERE, "out", f"{epname}_audio.wav")
    wavfile.write(path, SR, (mix * 32767).astype(np.int16))

    def db(x):
        return 20 * np.log10(active_rms(x) + 1e-12)
    print(f"wrote {path} {len(mix) / SR:.2f}s | music {db(mus) - db(voice):+.1f} dB vs voice, "
          f"effects {db(fx) - db(voice):+.1f} dB vs voice")


if __name__ == "__main__":
    _ep = importlib.import_module(sys.argv[1])
    if getattr(_ep, "SCORE", None) == "dark":
        build_dark(_ep, sys.argv[1])
    else:
        build(sys.argv[1])
