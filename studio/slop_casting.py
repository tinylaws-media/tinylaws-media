"""SLOP SHOP — voice casting: renders the same take with every cast the episode defines.

    python3 slop_casting.py slop_ep002            -> out/slop_cast_<name>.wav for every cast in ep.CASTS
    python3 slop_casting.py slop_ep002 A C B D    -> also out/slop_casting.wav: the takes in that order

A take = the episode's CASTING_LINES (the cold open + one line from every character), with all the
part effects (stutters, repeats, the wobble and toaster accents) applied, 0.35 s apart.
Before each take a short beep counts its rank (1 beep = first choice).
"""
import importlib
import sys

import numpy as np
from scipy.io import wavfile
from kokoro_onnx import Kokoro

import voice as V
import slop_voice as SV


def take(k, ep, cast):
    out = []
    lines = {l[0]: l for l in ep.LINES_T}
    for name in ep.CASTING_LINES:
        _, who, text, opts, _, _ = lines[name]
        clip, _ = SV.render_line(k, cast, who, text, opts)
        out += [clip * ep.CAST_GAIN.get(who, 1.0), np.zeros(int(0.35 * V.SR), np.float32)]
    x = np.concatenate(out)
    return x / (np.abs(x).max() or 1) * 0.9


def beeps(n):
    tt = np.arange(int(0.09 * V.SR)) / V.SR
    b = (np.sin(2 * np.pi * 880 * tt) * np.minimum(1, (0.09 - tt) / 0.02) * 0.25).astype(np.float32)
    g = np.zeros(int(0.12 * V.SR), np.float32)
    return np.concatenate([np.concatenate([b, g]) for _ in range(n)] + [np.zeros(int(0.4 * V.SR), np.float32)])


def main(epname, order):
    V.ensure_model()
    ep = importlib.import_module(epname)
    k = Kokoro(V.MODEL, V.VOICES)
    takes = {}
    for c, cast in ep.CASTS.items():
        takes[c] = take(k, ep, cast)
        wavfile.write(f"out/slop_cast_{c}.wav", V.SR, (takes[c] * 32767).astype(np.int16))
        print(c, {w: v[0] for w, v in cast.items()}, round(len(takes[c]) / V.SR, 2), "s")
    if order:
        gap = np.zeros(int(0.9 * V.SR), np.float32)
        parts = []
        for i, c in enumerate(order):
            parts += [beeps(i + 1), takes[c], gap]
        x = np.concatenate(parts)
        wavfile.write("out/slop_casting.wav", V.SR, (x * 32767).astype(np.int16))
        print("wrote out/slop_casting.wav", order, round(len(x) / V.SR, 1), "s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
