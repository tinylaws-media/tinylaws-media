"""THE EXIT MANUAL — Relay's voice: Kokoro-82M (Apache 2.0, offline), pitched down, light radio colour.

    python3 exit_voice.py exit_ep001          # -> out/exit_ep001_voice.wav + out/exit_ep001_voice_env.npy
    python3 exit_voice.py --casting "text"    # -> out/exit_casting.wav (4 ranked takes, 0.6 s apart)

The episode sets NARRATION = [(t, "text"), ...] or [(t, "text", {"speed": .., "semitones": ..}), ...],
VOICE, VOICE_SPEED, VOICE_FX = {"semitones": -2.5, "radio": 0.6}. Numbers are written as spoken.
The radio colour is a gentle band-limit (90 Hz - 7.5 kHz), a small 1.8 kHz presence bump and a touch of
saturation: it must stay perfectly intelligible (bible: "léger effet radio").
Reuses the Tiny Laws model files (./tts) and voice.ensure_model().
"""
import importlib
import os
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf
from scipy import signal
from scipy.io import wavfile

import voice as tl_voice           # Tiny Laws voice.py: model download only

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 44100
FPS = 24


def relay_fx(x, sr, semitones=-2.5, radio=0.6, warm=0.0):
    """Pitch down with Rubber Band (formants preserved, so it stays a human voice, only deeper),
    then the radio colour. radio = 0 keeps it clean.
    warm (v2, owner feedback 25 Oct 2026: natural voice, at most a very light effect): a close-mic
    night colour, no band-limit: +warm*2 dB at 180 Hz, -warm*1.5 dB at 6.5 kHz, soft 2:1 compression."""
    with tempfile.TemporaryDirectory() as d:
        src, dst = os.path.join(d, "in.wav"), os.path.join(d, "out.wav")
        sf.write(src, x, sr)
        chain = "aresample=48000"
        if warm > 0:
            chain += (f",highpass=f=65:poles=2,equalizer=f=180:t=o:w=1.2:g={2.0 * warm:.1f}"
                      f",equalizer=f=6500:t=o:w=1.5:g={-1.5 * warm:.1f}"
                      ",acompressor=threshold=0.12:ratio=2:attack=15:release=180:makeup=1")
        if semitones:
            chain += (f",rubberband=pitch={2 ** (semitones / 12):.5f}:formant=preserved"
                      ":transients=smooth:detector=soft:window=standard")
        if radio > 0:
            lo = 70 + 50 * radio
            hi = 9000 - 2500 * radio
            chain += (f",highpass=f={lo:.0f}:poles=2,lowpass=f={hi:.0f}:poles=2"
                      f",equalizer=f=1800:t=o:w=1.0:g={2.5 * radio:.1f}"
                      f",equalizer=f=220:t=o:w=1.0:g={1.5 * radio:.1f}")
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-af", chain, dst], check=True)
        y, ysr = sf.read(dst, dtype="float32")
    if radio > 0:
        pk = np.abs(y).max() or 1.0
        drive = 1.0 + 1.2 * radio
        y = np.tanh(y / pk * drive) / np.tanh(drive) * pk       # light, warm saturation
    return signal.resample_poly(y, SR, ysr).astype(np.float32)


def synth(k, text, voice, speed, fx, lang="en-us"):
    s, sr = k.create(text, voice=voice, speed=speed, lang=lang)
    s = np.asarray(s, np.float32)
    s = relay_fx(s, sr, **(fx or {}))
    e = np.abs(s) > 0.01
    if e.any():
        i0, i1 = np.argmax(e), len(e) - np.argmax(e[::-1])
        s = s[max(0, i0 - int(0.01 * SR)): min(len(s), i1 + int(0.06 * SR))]
    return s


def kokoro():
    from kokoro_onnx import Kokoro
    tl_voice.ensure_model()
    return Kokoro(tl_voice.MODEL, tl_voice.VOICES)


def build(epname):
    ep = importlib.import_module(epname)
    voice = getattr(ep, "VOICE", "am_onyx")
    speed = getattr(ep, "VOICE_SPEED", 1.0)
    fx = getattr(ep, "VOICE_FX", {"semitones": -2.5, "radio": 0.6})
    k = kokoro()
    lines = sorted(ep.NARRATION, key=lambda l: l[0])
    track = np.zeros(int(ep.DURATION * SR) + SR * 2, np.float32)
    report = []
    for i, line in enumerate(lines):
        t0, text = line[0], line[1]
        opts = line[2] if len(line) > 2 else {}
        lfx = dict(fx)
        if "semitones" in opts:
            lfx["semitones"] = opts["semitones"]
        nxt = lines[i + 1][0] if i + 1 < len(lines) else ep.DURATION
        room = nxt - t0 - 0.12
        sp = opts.get("speed", speed)
        clip = synth(k, text, voice, sp, lfx)
        while len(clip) / SR > room and sp < 1.15:
            sp = round(sp + 0.03, 2)
            clip = synth(k, text, voice, sp, lfx)
        dur = len(clip) / SR
        flag = "" if dur <= room else f"   <-- {dur - room:.2f}s too long"
        print(f"{t0:6.2f}s  {dur:4.2f}s / {room:4.2f}s  x{sp:.2f}  {text}{flag}")
        report.append((t0, dur))
        a = int(t0 * SR)
        track[a:a + len(clip)] += clip[: len(track) - a]
    track = track[: int(ep.DURATION * SR)]
    track = track / (np.abs(track).max() or 1.0) * 0.9
    out = os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    wavfile.write(os.path.join(out, f"{epname}_voice.wav"), SR, (track * 32767).astype(np.int16))
    hop = SR // FPS
    n = len(track) // hop
    env = np.sqrt((track[: n * hop].reshape(n, hop) ** 2).mean(axis=1))
    np.save(os.path.join(out, f"{epname}_voice_env.npy"), (env / (env.max() or 1)).astype(np.float32))
    print("wrote", os.path.join(out, f"{epname}_voice.wav"))
    return report


def _pauses(clip, min_len=0.07, thr=0.035):
    """Centres (s) of the pauses inside a spoken clip."""
    hop = int(0.01 * SR)
    n = len(clip) // hop
    e = np.sqrt((clip[: n * hop].reshape(n, hop) ** 2).mean(axis=1))
    e = e / (e.max() or 1)
    quiet = e < thr
    out, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if (j - i) * 0.01 >= min_len and i > 0 and j < n:
                out.append((i + j) / 2 * 0.01)
            i = j
        else:
            i += 1
    return out


def layout(epname):
    """Timing from measured line lengths. The episode lists LINES = [(id, "spoken | chunk | chunk", gap_after,
    opts), ...]; '|' marks where a caption block changes. Each line starts gap seconds after the previous one ends.
    Chunk times: proportional to letters, snapped to a real pause in the audio within 0.35 s.
    Writes out/<ep>_voice.wav, out/<ep>_voice_env.npy and out/<ep>_timing.json."""
    import json
    ep = importlib.import_module(epname)
    voice = getattr(ep, "VOICE", "am_fenrir")
    speed = getattr(ep, "VOICE_SPEED", 0.95)
    fx = getattr(ep, "VOICE_FX", {"semitones": -3.0, "radio": 0.55})
    k = kokoro()
    t = getattr(ep, "START", 0.1)
    clips, timing = [], {}
    for (lid, say, gap, *rest) in ep.LINES:
        opts = rest[0] if rest else {}
        parts = [p.strip() for p in say.split("|")]
        text = " ".join(parts)
        lfx = dict(fx)
        lfx.update({k_: v for k_, v in opts.items() if k_ in ("semitones", "radio")})
        clip = synth(k, text, voice, opts.get("speed", speed), lfx)
        dur = len(clip) / SR
        letters = [sum(ch.isalnum() for ch in p) for p in parts]
        tot = sum(letters) or 1
        pauses = _pauses(clip)
        chunks, acc = [0.0], 0
        for L in letters[:-1]:
            acc += L
            est = dur * acc / tot
            near = [p for p in pauses if abs(p - est) < 0.35]
            chunks.append(min(near, key=lambda p: abs(p - est)) if near else est)
        timing[lid] = {"start": round(t, 3), "dur": round(dur, 3), "end": round(t + dur, 3),
                       "chunks": [round(t + c, 3) for c in chunks], "text": text}
        clips.append((t, clip))
        print(f"{lid:>6} {t:6.2f}s +{dur:4.2f}s  {text}")
        t += dur + gap
    D = getattr(ep, "DURATION", None) or t
    track = np.zeros(int((D + 2) * SR), np.float32)
    for (t0, clip) in clips:
        a = int(t0 * SR)
        track[a:a + len(clip)] += clip[: len(track) - a]
    track = track[: int(D * SR)]
    track = track / (np.abs(track).max() or 1.0) * 0.9
    out = os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    wavfile.write(os.path.join(out, f"{epname}_voice.wav"), SR, (track * 32767).astype(np.int16))
    hop = SR // FPS
    n = len(track) // hop
    env = np.sqrt((track[: n * hop].reshape(n, hop) ** 2).mean(axis=1))
    np.save(os.path.join(out, f"{epname}_voice_env.npy"), (env / (env.max() or 1)).astype(np.float32))
    timing["_end"] = round(t, 3)
    json.dump(timing, open(os.path.join(out, f"{epname}_timing.json"), "w"), indent=1)
    print(f"speech ends {t:.2f}s; DURATION {D:.2f}s")


def measure(texts, voice, speed, fx):
    """Spoken length of each text (s): lay the timeline out on these before writing times."""
    k = kokoro()
    return [round(len(synth(k, t, voice, speed, fx)) / SR, 2) for t in texts]


CASTING = [  # v2 casting, 25 Oct 2026: natural voices only, speed 1.0, no pitch shift, very light "warm" colour
    # 1. am_fenrir: the widest natural intonation (~15 st swing on the test text), clear, warm at 137 Hz
    ("am_fenrir", 1.0, {"semitones": 0, "radio": 0, "warm": 0.5}),
    # 2. am_michael: the calmest and warmest (116 Hz), steady; less swing (~9 st), a touch slower
    ("am_michael", 1.0, {"semitones": 0, "radio": 0, "warm": 0.5}),
    # 3. am_puck: deep (109 Hz) and lively, but a slightly brighter, younger colour
    ("am_puck", 1.0, {"semitones": 0, "radio": 0, "warm": 0.5}),
    # 4. bm_george: British, clean and grave, the most formal and the least intimate
    ("bm_george", 1.0, {"semitones": 0, "radio": 0, "warm": 0.5}),
]


def casting(text, takes=CASTING, path=None):
    k = kokoro()
    gap = np.zeros(int(0.6 * SR), np.float32)
    parts = []
    for v, sp, fx in takes:
        c = synth(k, text, v, sp, fx)
        c = c / (np.abs(c).max() or 1) * 0.85
        parts += [c, gap]
        print(v, sp, fx, round(len(c) / SR, 2), "s")
    y = np.concatenate(parts[:-1])
    path = path or os.path.join(HERE, "out", "exit_casting.wav")
    wavfile.write(path, SR, (y * 32767).astype(np.int16))
    print("wrote", path)


if __name__ == "__main__":
    if sys.argv[1] == "--casting":
        casting(sys.argv[2])
    elif hasattr(importlib.import_module(sys.argv[1]), "LINES"):
        layout(sys.argv[1])
    else:
        build(sys.argv[1])
