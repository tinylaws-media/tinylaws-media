"""Pip's narration with a free, open-source voice (Kokoro-82M, Apache 2.0), generated offline.

    python3 voice.py ep001            # -> out/ep001_voice.wav + out/ep001_voice_env.npy

The episode lists what Pip says in NARRATION = [(time_s, "spoken text"), ...] and picks a voice
with VOICE (default "af_heart") and VOICE_SPEED (default 1.0). VOICE_FX = {"semitones": 3} pitches
Pip up as a clean cartoon voice (Rubber Band via ffmpeg, presence lift, no muffling); {} keeps it natural. Write numbers and symbols the way
they are spoken ("two times bigger", not "2× bigger"). A line that would run into the next one is
sped up a little (up to 1.25×); if it still does not fit, the script says so and you move the next line.

The model files (about 120 MB) are fetched once from the kokoro-onnx GitHub release into ./tts/.
"""
import importlib
import os
import subprocess
import sys

import numpy as np
from scipy import signal
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
TTS = os.path.join(HERE, "tts")
MODEL = os.path.join(TTS, "kokoro-v1.0.fp16.onnx")   # higher quality than the int8 build
VOICES = os.path.join(TTS, "voices-v1.0.bin")
REL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
SR = 44100
FPS = 24


def ensure_model():
    os.makedirs(TTS, exist_ok=True)
    for path in (MODEL, VOICES):
        if not os.path.exists(path):
            subprocess.run(["curl", "-sSfL", "-o", path, REL + os.path.basename(path)], check=True)


def cartoonize(x, sr, pitch=1.3, formant=1.12, expressive=1.35, lofi=True):
    """Turn the clean TTS voice into Pip's character voice with the WORLD vocoder.

    pitch      : multiplies the voice's pitch (1.3 = about +4.5 semitones)
    formant    : stretches the vocal-tract resonances upwards (smaller 'head' = younger, cartoonier)
    expressive : widens the intonation around its median (TTS speech is flat; cartoons swing)
    lofi       : a little warmth and band-limiting, like a small vintage speaker
    """
    import pyworld as pw
    x = x.astype(np.float64)
    fp = 5.0
    f0, t = pw.dio(x, sr, frame_period=fp, f0_floor=60, f0_ceil=700)
    f0 = pw.stonemask(x, f0, t, sr)
    sp = pw.cheaptrick(x, f0, t, sr)
    ap = pw.d4c(x, f0, t, sr)
    voiced = f0 > 0
    if voiced.any():
        lf = np.log(f0[voiced])
        med = np.median(lf)
        f0 = f0.copy()
        f0[voiced] = np.exp(med + (lf - med) * expressive) * pitch
    if formant != 1.0:
        bins = sp.shape[1]
        src = np.clip(np.arange(bins) / formant, 0, bins - 1)
        lo = np.floor(src).astype(int)
        hi = np.minimum(lo + 1, bins - 1)
        w = src - lo
        sp = sp[:, lo] * (1 - w) + sp[:, hi] * w
        ap = ap[:, lo] * (1 - w) + ap[:, hi] * w
    y = pw.synthesize(f0, np.ascontiguousarray(sp), np.ascontiguousarray(ap), sr, frame_period=fp)
    if lofi:
        y = signal.lfilter(*signal.butter(2, 140 / (sr / 2), "high"), y)
        y = signal.lfilter(*signal.butter(2, min(7800, sr / 2 - 200) / (sr / 2), "low"), y)
        pk = np.abs(y).max() or 1.0
        y = np.tanh(y / pk * 1.6) / np.tanh(1.6) * pk     # gentle tape-like warmth
    return y.astype(np.float32)


def brighten_shift(x, sr, semitones=0.0, presence_db=2.5):
    """Clean character voice: Rubber Band pitch shift (formants follow, the classic cartoon move),
    done at 48 kHz so no treble is lost, plus a small presence lift for clarity. No muffling filter."""
    import tempfile
    import soundfile as sf
    with tempfile.TemporaryDirectory() as d:
        src, dst = os.path.join(d, "in.wav"), os.path.join(d, "out.wav")
        sf.write(src, x, sr)
        chain = "aresample=48000"
        if semitones:
            chain += f",rubberband=pitch={2 ** (semitones / 12):.5f}:formant=shifted:transients=mixed:detector=soft"
        chain += f",highpass=f=80,equalizer=f=4000:t=o:w=1.2:g={presence_db}"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-af", chain, dst], check=True)
        y, ysr = sf.read(dst, dtype="float32")
    return signal.resample_poly(y, sr, ysr).astype(np.float32)


def synth(k, text, voice, speed, lang, fx=None):
    s, sr = k.create(text, voice=voice, speed=speed, lang=lang)
    s = np.asarray(s, np.float32)
    if fx and "semitones" in fx:
        s = brighten_shift(s, sr, **fx)
    elif fx:
        s = cartoonize(s, sr, **fx)          # legacy WORLD chain (sounded muffled: not used any more)
    # trim leading / trailing silence so lines land where they are placed
    e = np.abs(s) > 0.01
    if e.any():
        i0, i1 = np.argmax(e), len(e) - np.argmax(e[::-1])
        s = s[max(0, i0 - int(0.01 * sr)): min(len(s), i1 + int(0.05 * sr))]
    return signal.resample_poly(s, SR, sr).astype(np.float32)


def build(epname):
    from kokoro_onnx import Kokoro
    ensure_model()
    ep = importlib.import_module(epname)
    voice = getattr(ep, "VOICE", "af_heart")
    speed = getattr(ep, "VOICE_SPEED", 1.0)
    lang = getattr(ep, "VOICE_LANG", "en-us")
    fx = getattr(ep, "VOICE_FX", None)   # Pip's character voice, see cartoonize()
    k = Kokoro(MODEL, VOICES)
    # a line is (time, text) or (time, text, {"semitones": .., "speed": ..}) to vary Pip's delivery
    lines = sorted(ep.NARRATION, key=lambda l: l[0])
    track = np.zeros(int(ep.DURATION * SR) + SR * 2, np.float32)
    for i, line in enumerate(lines):
        t0, text = line[0], line[1]
        opts = line[2] if len(line) > 2 else {}
        lfx = dict(fx or {})
        if "semitones" in opts:
            lfx["semitones"] = opts["semitones"]
        nxt = lines[i + 1][0] if i + 1 < len(lines) else ep.DURATION
        room = nxt - t0 - 0.08
        sp = opts.get("speed", speed)
        clip = synth(k, text, voice, sp, lang, lfx)
        while len(clip) / SR > room and sp < 1.25:
            sp = round(sp + 0.05, 2)
            clip = synth(k, text, voice, sp, lang, lfx)
        dur = len(clip) / SR
        flag = "" if dur <= room else f"   <-- {dur - room:.2f}s too long, move the next line"
        print(f"{t0:6.2f}s  {dur:4.2f}s / {room:4.2f}s  x{sp:.2f}  {text}{flag}")
        a = int(t0 * SR)
        track[a:a + len(clip)] += clip[: len(track) - a]
    track = track[: int(ep.DURATION * SR)]
    peak = np.abs(track).max() or 1.0
    track = track / peak * 0.9
    out = os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    wavfile.write(os.path.join(out, f"{epname}_voice.wav"), SR, (track * 32767).astype(np.int16))
    # per-frame loudness envelope: drives Pip's mouth in the animation
    hop = SR // FPS
    n = len(track) // hop
    env = np.sqrt((track[: n * hop].reshape(n, hop) ** 2).mean(axis=1))
    env = env / (env.max() or 1.0)
    np.save(os.path.join(out, f"{epname}_voice_env.npy"), env.astype(np.float32))
    print("wrote", os.path.join(out, f"{epname}_voice.wav"))


if __name__ == "__main__":
    build(sys.argv[1])
