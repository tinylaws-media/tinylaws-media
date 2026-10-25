"""NOT JUST YOU — narration (Kokoro-82M, offline), measured line by line.

    python3 njy_voice.py casting            # out/njy_casting.wav: the hook in 4 voices, ranked
    python3 njy_voice.py measure njy_ep001  # synthesise every line, write out/<ep>_lines.json (durations)
    python3 njy_voice.py build njy_ep001    # out/<ep>_voice.wav laid out on the episode's timeline

The episode's timeline is built from the measured durations (see njy_ep001.timeline()), so lines
never collide and captions land on the voice. Voice chain: Kokoro, optional Rubber Band pitch
shift, a gentle warm EQ (no muffling, no presence spike), trimmed silences.
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
from scipy.io import wavfile

import voice as tl_voice   # Tiny Laws: model download only

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
SR = 44100
FPS = 24


def warm_chain(x, sr, semitones=0.0, presence_db=1.0, low_db=1.5):
    with tempfile.TemporaryDirectory() as d:
        src, dst = os.path.join(d, "in.wav"), os.path.join(d, "out.wav")
        sf.write(src, x, sr)
        chain = "aresample=48000"
        if semitones:
            chain += f",rubberband=pitch={2 ** (semitones / 12):.5f}:formant=preserved:transients=smooth:detector=soft"
        chain += (f",highpass=f=70,equalizer=f=180:t=o:w=1.0:g={low_db},"
                  f"equalizer=f=3500:t=o:w=1.4:g={presence_db},equalizer=f=7500:t=o:w=1.0:g=-1.5")
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-af", chain, dst], check=True)
        y, ysr = sf.read(dst, dtype="float32")
    return signal.resample_poly(y, sr, ysr).astype(np.float32)


_K = None


def kokoro():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        tl_voice.ensure_model()
        _K = Kokoro(tl_voice.MODEL, tl_voice.VOICES)
    return _K


def synth(text, voice, speed=0.9, semitones=0.0, lang="en-us", **fx):
    s, sr = kokoro().create(text, voice=voice, speed=speed, lang=lang)
    s = warm_chain(np.asarray(s, np.float32), sr, semitones, **fx)
    e = np.abs(s) > 0.008
    if e.any():
        i0, i1 = np.argmax(e), len(e) - np.argmax(e[::-1])
        s = s[max(0, i0 - int(0.012 * sr)): min(len(s), i1 + int(0.08 * sr))]
    y = signal.resample_poly(s, SR, sr).astype(np.float32)
    return y / (np.abs(y).max() or 1) * 0.9


def write(path, x):
    wavfile.write(path, SR, (np.clip(x, -1, 1) * 32767).astype(np.int16))


HOOK = "Can't stop scrolling the bad news?"
CAST = [  # ranked best first: (voice, speed, semitones, why)
    ("af_heart", 0.9, -1.0, "warm, clear, lowered a semitone: most intelligible at low volume"),
    ("af_nicole", 0.92, 0.0, "close-mic whisper: most intimate, but harder to hear on a phone speaker"),
    ("bf_emma", 0.9, -0.5, "soft British, calm and grave"),
    ("bm_george", 0.9, 0.0, "deep British male, steady"),
]


def casting():
    takes = []
    for (v, sp, st, why) in CAST:
        x = synth(HOOK, v, sp, st)
        takes.append(x)
        print(f"{v:10s} speed {sp} pitch {st:+.1f} st  {len(x) / SR:.2f}s  {why}")
    gap = np.zeros(int(0.6 * SR), np.float32)
    out = np.concatenate(sum([[t, gap] for t in takes], [])[:-1])
    write(os.path.join(OUT, "njy_casting.wav"), out)
    print("wrote out/njy_casting.wav")


def measure(epname):
    ep = importlib.import_module(epname)
    d = os.path.join(OUT, f"{epname}_lines")
    os.makedirs(d, exist_ok=True)
    res = []
    for i, line in enumerate(ep.LINES):
        opts = dict(ep.VOICE_OPTS)
        opts.update(line.get("voice", {}))
        x = synth(line["say"], **opts)
        p = os.path.join(d, f"{i:02d}.wav")
        write(p, x)
        # onset of each word is unknown; store the loudness envelope for fine timing
        res.append({"i": i, "say": line["say"], "dur": round(len(x) / SR, 3)})
        print(f"{i:2d} {len(x) / SR:5.2f}s  {line['say']}")
    json.dump(res, open(os.path.join(OUT, f"{epname}_lines.json"), "w"), indent=1)
    print("total speech", round(sum(r["dur"] for r in res), 2), "s")


def build(epname):
    ep = importlib.import_module(epname)
    tl = ep.timeline()
    d = os.path.join(OUT, f"{epname}_lines")
    track = np.zeros(int(ep.DURATION * SR) + SR, np.float32)
    for i, (t0, t1) in enumerate(tl):
        sr, x = wavfile.read(os.path.join(d, f"{i:02d}.wav"))
        x = x.astype(np.float32) / 32768
        a = int(t0 * SR)
        track[a:a + len(x)] += x[: len(track) - a]
    track = track[: int(ep.DURATION * SR)]
    write(os.path.join(OUT, f"{epname}_voice.wav"), track)
    hop = SR // FPS
    n = len(track) // hop
    env = np.sqrt((track[: n * hop].reshape(n, hop) ** 2).mean(axis=1))
    np.save(os.path.join(OUT, f"{epname}_voice_env.npy"), (env / (env.max() or 1)).astype(np.float32))
    print("wrote", f"out/{epname}_voice.wav", round(len(track) / SR, 2), "s")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "casting":
        casting()
    elif cmd == "measure":
        measure(sys.argv[2])
    else:
        build(sys.argv[2])
