"""Subject Zero voices: several speakers per episode, each with its own Kokoro voice and processing.

    python3 szvoice.py nemo01            # -> out/nemo01_voice.wav, out/nemo01_lines.json (listen.py reads it)

Speakers (episode file, SPEAKERS dict): voice, speed, and an ffmpeg filter chain (radio for the lab, a big
pitch-down for the hero's NOPE). Lines are laid out like the Tiny Laws auto layout: each line starts at its target
or up to `pull` seconds earlier, never before the previous line ends + gap; the smallest pull that ends the
narration before DURATION - 0.3 s wins.
"""
import importlib
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf
from scipy import signal

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voice as V  # noqa: E402  (Tiny Laws voice module: Kokoro model, trim, SR)

SR = V.SR
OUT = os.path.join(HERE, "out")


def process(x, sr, chain):
    if not chain:
        return x
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, "a.wav"), os.path.join(d, "b.wav")
        sf.write(a, x, sr)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a, "-af", chain, b], check=True)
        y, ysr = sf.read(b, dtype="float32")
    if y.ndim > 1:
        y = y.mean(axis=1)
    return signal.resample_poly(y, sr, ysr).astype(np.float32) if ysr != sr else y


def synth_line(k, text, spk):
    s, sr = k.create(text, voice=spk["voice"], speed=spk.get("speed", 1.0), lang=spk.get("lang", "en-us"))
    s = np.asarray(s, np.float32)
    e = np.abs(s) > 0.01
    if e.any():
        i0, i1 = np.argmax(e), len(e) - np.argmax(e[::-1])
        s = s[max(0, i0 - int(0.01 * sr)): min(len(s), i1 + int(0.06 * sr))]
    s = signal.resample_poly(s, SR, sr).astype(np.float32)
    s = process(s, SR, spk.get("chain"))
    return s * spk.get("gain", 1.0)


def build(epname, gap=0.2, pulls=(0.0, 0.4, 0.8, 1.2, 1.6, 2.0, 3.0)):
    from kokoro_onnx import Kokoro
    V.ensure_model()
    k = Kokoro(os.path.join(V.TTS, "kokoro-v1.0.fp16.onnx"), os.path.join(V.TTS, "voices-v1.0.bin"))
    ep = importlib.import_module(epname)
    clips = []
    for row in ep.VOICE_LINES:
        key, target, who, say = row[:4]
        spk = dict(ep.SPEAKERS[who])
        opts = ep.LINE_FX.get(key, {})
        spk.update(opts)
        ref = row[4] if len(row) > 4 else say          # what the gate expects to hear (a stretched "Noooope!" is "nope")
        clips.append((key, target, who, ref, synth_line(k, say, spk), spk.get("overlap", 0.0)))
    end_max = ep.DURATION - 0.3

    def lay(pull):
        out, prev_end = [], None
        for key, target, who, say, x, ov in clips:
            t0 = target if prev_end is None else max(prev_end + gap - ov, target - pull)
            out.append((key, t0, who, say, x))
            prev_end = t0 + len(x) / SR
        return out, prev_end

    for pull in pulls:
        layout, end = lay(pull)
        if end <= end_max:
            break
    print(f"narration ends at {end:.2f}s of {ep.DURATION:.2f}s (pull {pull}s)"
          + ("" if end <= end_max else f"  !! runs {end - end_max:.2f}s past the end: shorten lines or lengthen DURATION"))
    n = int(ep.DURATION * SR) + SR
    track = np.zeros(n, np.float32)
    stems = {}
    log = []
    for key, t0, who, say, x in layout:
        a = int(t0 * SR)
        track[a:a + len(x)] += x[: max(0, n - a)]
        st = stems.setdefault(who, np.zeros(n, np.float32))
        st[a:a + len(x)] += x[: max(0, n - a)]
        log.append({"key": key, "t": round(t0, 3), "dur": round(len(x) / SR, 3), "text": say, "who": who})
    track = track[: int(ep.DURATION * SR)]
    peak = np.abs(track).max() or 1.0
    track = track / peak * 0.9
    os.makedirs(OUT, exist_ok=True)
    sf.write(os.path.join(OUT, f"{epname}_voice.wav"), (track * 32767).astype(np.int16), SR, subtype="PCM_16")
    json.dump({"voice": "multi", "lang": "en-us", "lines": log},
              open(os.path.join(OUT, f"{epname}_lines.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    hop = SR // ep.FPS
    for who, st in stems.items():
        st = st[: int(ep.DURATION * SR)] / peak * 0.9
        m = len(st) // hop
        env = np.sqrt((st[: m * hop].reshape(m, hop) ** 2).mean(axis=1))
        np.save(os.path.join(OUT, f"{epname}_env_{who}.npy"), (env / (env.max() or 1)).astype(np.float32))
    print("wrote", os.path.join(OUT, f"{epname}_voice.wav"))
    return layout


if __name__ == "__main__":
    build(sys.argv[1])
