"""SLOP SHOP — narration with several Kokoro voices (one per character), built on voice.py.

    python3 slop_voice.py slop_ep002 measure   # synthesises every line once -> out/<ep>_durs.json
    python3 slop_voice.py slop_ep002           # out/<ep>_voice.wav + out/<ep>_env.npz (one mouth per character)

The episode defines:
    CAST  = {"G": ("am_michael", 1.12, {"semitones": 1}), ...}       # who -> (voice, speed, fx)
    LINES = [(who, text_or_parts, opts), ...]
    NARRATION = [(t, who, text_or_parts, opts), ...]   # LINES placed on the timeline
A line is a plain string, or a list of PARTS [(text, part_fx), ...] synthesised one by one and joined:
that is how the YouTube-Poop edits are written into the script, so the picture can sync to every part
(durs.json stores each part's start/end inside its line).

part_fx (all optional):
    stutter=n, stut=0.12   the first `stut` seconds repeated n times before the word   ("b-b-b-breaking")
    rep=n, rep_st=2.0      the whole part said n more times, each one rep_st semitones higher ("square square SQUARE")
    chip=1.4               speed AND pitch up (tape sped up)
    tempo=1.8              faster, same pitch (Rubber Band)
    st=3                   extra pitch for this part, in semitones
    gap=0.1                silence after the part
    grain=(frac, len, n)   a tiny grain at frac of the part looped n times (a digital skip)
Line opts: "speed", "semitones", "voice", "gain", "fx" (a line chain: "toaster", ("wobble", depth_st, hz)).
Every effect keeps the voice clean and in front: no distortion, no harsh highs.
"""
import importlib
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from scipy import signal
from scipy.io import wavfile

import voice as V

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
SR = V.SR


def _rb(x, tempo=1.0, semis=0.0):
    import soundfile as sf
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, "a.wav"), os.path.join(d, "b.wav")
        sf.write(a, x, SR)
        chain = f"rubberband=tempo={tempo:.4f}:pitch={2 ** (semis / 12):.5f}:formant=shifted:transients=mixed"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a, "-af", chain, b], check=True)
        y, _ = sf.read(b, dtype="float32")
    return y.astype(np.float32)


def _chip(x, k):
    """Tape sped up by k (pitch and speed together)."""
    n = int(len(x) / k)
    return np.interp(np.arange(n) * k, np.arange(len(x)), x).astype(np.float32)


def _fade(x, ms=6):
    n = min(len(x) // 2, int(ms / 1000 * SR))
    if n > 0:
        x = x.copy()
        x[:n] *= np.linspace(0, 1, n)
        x[-n:] *= np.linspace(1, 0, n)
    return x


def _sil(s):
    return np.zeros(int(max(0.0, s) * SR), np.float32)


def wobble(x, depth_st=1.5, hz=2.6):
    """Sing-song vibrato (an invented accent: the pitch rolls up and down like a slow siren)."""
    r = 2 ** (depth_st / 12) - 1
    A = r * SR / (2 * np.pi * hz)
    n = np.arange(len(x))
    d = A * (1 + np.sin(2 * np.pi * hz * n / SR))
    idx = np.clip(n - d - A, 0, len(x) - 1)
    return np.interp(idx, n, x).astype(np.float32)


def toaster(x):
    """A voice coming out of a small chrome box: band-limited, a little metallic ring, a faint crackle."""
    b, a = signal.butter(2, [260 / (SR / 2), 4200 / (SR / 2)], "band")
    y = signal.lfilter(b, a, x)
    dly = int(0.0042 * SR)
    y2 = y.copy()
    y2[dly:] += 0.35 * y[:-dly]
    rng = np.random.default_rng(9)
    crackle = (rng.random(len(x)) > 0.9993) * rng.uniform(-1, 1, len(x)) * 0.05
    y2 = y2 + signal.lfilter(*signal.butter(1, 2500 / (SR / 2), "low"), crackle)
    pk = np.abs(y2).max() or 1
    return (y2 / pk * (np.abs(x).max() or 1)).astype(np.float32)


def _part(k, text, v, sp, lang, st, pfx):
    x = V.synth(k, text, v, sp, lang, {"semitones": st + pfx.get("st", 0.0)} if (st or pfx.get("st")) else None)
    if pfx.get("tempo"):
        x = _rb(x, pfx["tempo"], 0.0)
    if pfx.get("chip"):
        x = _chip(x, pfx["chip"])
    if pfx.get("grain"):
        fr, ln, n = pfx["grain"]
        i = int(fr * len(x))
        g = _fade(x[i:i + int(ln * SR)], 3)
        x = np.concatenate([x[:i]] + [g] * n + [x[i:]])
    out = []
    if pfx.get("stutter"):
        s = _fade(x[: int(pfx.get("stut", 0.12) * SR)], 4)
        for _ in range(pfx["stutter"]):
            out += [s, _sil(pfx.get("stut_gap", 0.035))]
    if not pfx.get("stutter_only"):
        out.append(x)
    for j in range(pfx.get("rep", 0)):
        out += [_sil(pfx.get("rep_gap", 0.07)), _chip(x, 2 ** (pfx.get("rep_st", 2.0) * (j + 1) / 12))]
    out.append(_sil(pfx.get("gap", 0.0)))
    return np.concatenate(out).astype(np.float32)


def render_line(k, cast, who, text, opts):
    v, sp, fx = cast[who]
    v = opts.get("voice", v)
    sp = opts.get("speed", sp)
    st = opts.get("semitones", (fx or {}).get("semitones", 0.0))
    lang = "en-gb" if v[0] == "b" else "en-us"
    parts = [(text, {})] if isinstance(text, str) else text
    clips, spans, t = [], [], 0.0
    for (ptxt, pfx) in parts:
        x = _part(k, ptxt, v, sp, lang, st, pfx)
        spans.append((round(t, 3), round(t + len(x) / SR - pfx.get("gap", 0.0), 3)))
        t += len(x) / SR
        clips.append(x)
    x = np.concatenate(clips)
    chain = list(opts.get("fx", [])) + list(cast[who][2].get("chain", []) if cast[who][2] else [])
    for f in chain:
        if f == "toaster":
            x = toaster(x)
        elif isinstance(f, (list, tuple)) and f[0] == "wobble":
            x = wobble(x, f[1], f[2])
    return x, spans


def _sig(ep):
    return json.dumps([[l[0], l[1], l[2] if len(l) > 2 else {}] for l in ep.LINES], sort_keys=True, default=str) + \
        json.dumps(ep.CAST, sort_keys=True)


def measure(epname):
    from kokoro_onnx import Kokoro
    V.ensure_model()
    ep = importlib.import_module(epname)
    k = Kokoro(V.MODEL, V.VOICES)
    durs, spans = [], []
    for line in ep.LINES:
        who, text = line[0], line[1]
        opts = line[2] if len(line) > 2 else {}
        clip, sp = render_line(k, ep.CAST, who, text, opts)
        durs.append(round(len(clip) / SR, 3))
        spans.append(sp)
        print(f"{durs[-1]:5.2f}s  {who}  {text if isinstance(text, str) else ' | '.join(p[0] for p in text)}")
    os.makedirs(OUT, exist_ok=True)
    json.dump({"sig": _sig(ep), "durs": durs, "spans": spans}, open(os.path.join(OUT, f"{epname}_durs.json"), "w"))
    print("total speech", round(sum(durs), 2), "s")


def load_durs(epname):
    p = os.path.join(OUT, f"{epname}_durs.json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    ep = sys.modules.get(epname)
    if ep is not None and d.get("sig") != _sig(ep):
        print("[slop_voice] durs.json is stale: run measure again", file=sys.stderr)
        return None
    return d


def build(epname):
    from kokoro_onnx import Kokoro
    V.ensure_model()
    ep = importlib.import_module(epname)
    k = Kokoro(V.MODEL, V.VOICES)
    n = int(ep.DURATION * SR)
    track = np.zeros(n + SR * 2, np.float32)
    mouths = {}
    lines = sorted(ep.NARRATION, key=lambda l: l[0])
    for i, (t0, who, text, opts) in enumerate(lines):
        clip, _ = render_line(k, ep.CAST, who, text, opts)
        clip = clip * opts.get("gain", getattr(ep, "CAST_GAIN", {}).get(who, 1.0))
        nxt = lines[i + 1][0] if i + 1 < len(lines) else ep.DURATION
        dur = len(clip) / SR
        flag = "" if t0 + dur <= nxt + 0.02 else f"   <-- overlaps next line by {t0 + dur - nxt:.2f}s"
        label = text if isinstance(text, str) else " | ".join(p[0] for p in text)
        print(f"{t0:6.2f}s  {dur:4.2f}s  {who}  {label}{flag}")
        a = int(t0 * SR)
        track[a:a + len(clip)] += clip[: len(track) - a]
        m = mouths.setdefault(who, np.zeros_like(track))
        m[a:a + len(clip)] += clip[: len(track) - a]
    track = track[:n]
    peak = np.abs(track).max() or 1.0
    track = track / peak * 0.9
    wavfile.write(os.path.join(OUT, f"{epname}_voice.wav"), SR, (track * 32767).astype(np.int16))
    hop = SR // V.FPS
    envs = {}
    for who, m in mouths.items():
        m = m[:n]
        f = len(m) // hop
        e = np.sqrt((m[: f * hop].reshape(f, hop) ** 2).mean(axis=1))
        envs[who] = (e / (e.max() or 1.0)).astype(np.float32)
    np.savez(os.path.join(OUT, f"{epname}_env.npz"), **envs)
    print("wrote", os.path.join(OUT, f"{epname}_voice.wav"))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "measure":
        measure(sys.argv[1])
    else:
        build(sys.argv[1])
