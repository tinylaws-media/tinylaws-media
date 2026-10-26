"""THE EXIT MANUAL — an epic, requiem-like layer made from a PUBLIC-DOMAIN score (v4, 26 Oct 2026).

Owner's note: "free music in the background that changes with the theme, Lacrimosa-like, epic".
Recordings can't be downloaded in the studio, so we perform the music ourselves: a public-domain composition
(Bach's chorales are centuries out of copyright; the music21 corpus ships them as scores), rendered with
FluidSynth and the FluidR3 GM soundfont (MIT licence). No recording, no performer, nothing to license.

    from exit_requiem import render
    stereo = render("bach/bwv244.54", t0=0.25, t1=62.7, intensity=[(t, 0..1), ...], D=65.5)

Arrangement: choir "aahs" on the four voices, a string section doubling them, contrabasses an octave under the
bass; above intensity 0.6 horns join the inner voices, above 0.75 trombones the tenor and bass, and timpani
mark the bass on strong beats. Fermatas are held 1.8x. Dynamics follow 'intensity' (CC11 swells, never a jump).
"""
import os
import subprocess
import tempfile

import mido
import numpy as np
import soundfile as sf
from scipy import signal

SR = 44100
SF2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
# channel: (GM program, voices doubled (0=S 1=A 2=T 3=B), octave shift, base velocity, threshold of intensity)
LAYERS = [
    (0, 52, (0, 1, 2, 3), 0, 92, 0.0),       # choir aahs
    (1, 48, (0, 1, 2, 3), 0, 80, 0.0),       # strings
    (2, 43, (3,), -12, 96, 0.0),             # contrabass
    (3, 60, (1, 2), 0, 78, 0.6),             # horns
    (4, 57, (2, 3), -12, 82, 0.75),          # trombones
]
TIMPANI = (5, 47)


def _interp(points, t):
    ts = [p[0] for p in points]
    vs = [p[1] for p in points]
    return float(np.interp(t, ts, vs))


def events(piece, transpose=0):
    """[(start_q, dur_q, midi, voice)], total quarters, set of fermata offsets (soprano)."""
    from music21 import corpus, expressions
    sc = corpus.parse(piece)
    parts = list(sc.parts)[:4]
    ev, ferm = [], []
    for vi, p in enumerate(parts):
        for n in p.flatten().notes:
            o, d = float(n.offset), float(n.quarterLength)
            for pch in n.pitches:
                ev.append((o, d, pch.midi + transpose, vi))
            if vi == 0 and any(isinstance(e, expressions.Fermata) for e in n.expressions):
                ferm.append((o, o + d))
    total = max(o + d for o, d, _, _ in ev)
    return ev, total, ferm


def time_map(total, ferm, t0, t1, hold=1.8, res=0.125):
    """Quarter position -> seconds, with fermatas held 'hold' times longer, fitted into [t0, t1]."""
    grid = np.arange(0, total + res, res)
    w = np.ones_like(grid)
    for a, b in ferm:
        w[(grid >= a) & (grid < b)] = hold
    secs = np.concatenate([[0], np.cumsum(w[:-1])]) * res
    secs = t0 + secs * (t1 - t0) / secs[-1]
    return lambda q: float(np.interp(q, grid, secs))


def write_midi(path, ev, total, ferm, t0, t1, intensity):
    tm = time_map(total, ferm, t0, t1)
    msgs = []                                         # (seconds, priority, message)
    for ch, prog, voices, octv, vel, thr in LAYERS:
        msgs.append((0.0, 0, mido.Message("program_change", channel=ch, program=prog)))
        msgs.append((0.0, 0, mido.Message("control_change", channel=ch, control=91, value=110)))   # reverb send
        msgs.append((0.0, 0, mido.Message("control_change", channel=ch, control=7, value=100)))
    ch_t, prog_t = TIMPANI
    msgs.append((0.0, 0, mido.Message("program_change", channel=ch_t, program=prog_t)))
    msgs.append((0.0, 0, mido.Message("control_change", channel=ch_t, control=91, value=90)))
    # dynamics: CC11 every 50 ms, each layer fades in above its threshold
    for x in np.arange(0, t1 + 2.0, 0.05):
        it = _interp(intensity, x)
        for ch, prog, voices, octv, vel, thr in LAYERS:
            g = np.clip((it - thr) / max(0.15, 1 - thr), 0, 1) if thr > 0 else 0.35 + 0.65 * it
            msgs.append((x, 1, mido.Message("control_change", channel=ch, control=11, value=int(127 * g))))
    for (o, d, m, v) in ev:
        a, b = tm(o), tm(o + d)
        for ch, prog, voices, octv, vel, thr in LAYERS:
            if v not in voices:
                continue
            if thr > 0 and _interp(intensity, a) < thr - 0.05:
                continue
            mm = m + octv
            msgs.append((a, 2, mido.Message("note_on", channel=ch, note=mm, velocity=vel)))
            msgs.append((b - 0.02, 0, mido.Message("note_off", channel=ch, note=mm, velocity=0)))
        if v == 3 and float(o) == int(o) and int(o) % 2 == 0:              # timpani on strong beats, epic parts
            it = _interp(intensity, a)
            if it >= 0.75:
                tn = 38 + ((m - 38) % 12)
                msgs.append((a, 2, mido.Message("note_on", channel=ch_t, note=tn, velocity=int(60 + 50 * it))))
                msgs.append((a + 0.6, 0, mido.Message("note_off", channel=ch_t, note=tn, velocity=0)))
    for (a_q, b_q) in ferm:                                                 # a soft roll under each epic fermata
        a, b = tm(a_q), tm(b_q)
        it = _interp(intensity, a)
        if it < 0.75:
            continue
        x = a
        k = 0
        while x < b - 0.1:
            vel = int(30 + 40 * (k / max(1, (b - a) / 0.09)) * it)
            msgs.append((x, 2, mido.Message("note_on", channel=ch_t, note=38, velocity=min(110, vel))))
            msgs.append((x + 0.08, 0, mido.Message("note_off", channel=ch_t, note=38, velocity=0)))
            x += 0.09
            k += 1
    msgs.sort(key=lambda z: (z[0], z[1]))
    mid = mido.MidiFile(ticks_per_beat=480)
    tr = mido.MidiTrack()
    mid.tracks.append(tr)
    tr.append(mido.MetaMessage("set_tempo", tempo=1_000_000))              # 1 beat = 1 s, ticks = s * 480
    last = 0
    for (x, _, msg) in msgs:
        tick = int(round(max(0.0, x) * 480))
        msg.time = tick - last
        last = tick
        tr.append(msg)
    mid.save(path)


def cathedral(x, seconds=2.8, mix=0.22):
    n = int(seconds * SR)
    r = np.random.default_rng(5)
    ir = r.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 2.0)[:, None]
    b, a = signal.butter(2, 3200 / (SR / 2), "low")
    ir = signal.lfilter(b, a, ir, axis=0) * 0.012
    wet = np.stack([signal.fftconvolve(x[:, c], ir[:, c])[: len(x)] for c in range(2)], axis=1)
    return x * (1 - mix) + wet * mix * 2


def render(piece, t0, t1, intensity, D, transpose=0):
    ev, total, ferm = events(piece, transpose)
    with tempfile.TemporaryDirectory() as d:
        mp, wp = os.path.join(d, "c.mid"), os.path.join(d, "c.wav")
        write_midi(mp, ev, total, ferm, t0, t1, intensity)
        subprocess.run(["fluidsynth", "-ni", "-q", "-g", "0.5", "-r", str(SR), "-R", "1", "-C", "0", "-F", wp, SF2, mp],
                       check=True, capture_output=True)
        y, sr = sf.read(wp, dtype="float32")
    if y.ndim == 1:
        y = np.stack([y, y], axis=1)
    n = int(D * SR)
    y = np.pad(y, ((0, max(0, n - len(y))), (0, 0)))[:n]
    y = cathedral(y)
    b, a = signal.butter(2, 60 / (SR / 2), "high")
    return signal.lfilter(b, a, y, axis=0)


if __name__ == "__main__":
    import sys
    y = render(sys.argv[1] if len(sys.argv) > 1 else "bach/bwv244.54", 0.5, 60.0,
               [(0, 0.3), (20, 0.6), (40, 0.9), (60, 1.0)], 62.0)
    sf.write("out/requiem_test.wav", y / (np.abs(y).max() or 1) * 0.9, SR)
    print("wrote out/requiem_test.wav")
