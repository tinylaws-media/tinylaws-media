"""Subtitle tracks (.srt) for a THE EXIT MANUAL episode.

    python3 exit_subtitles.py exit_ep001                       # prints the English lines, in order, to translate
    python3 exit_subtitles.py exit_ep001 exit_ep001_subs.json  # writes out/subs/exit_ep001.<lang>.srt

The JSON holds {"en": [...], "fr": [...], ...}, same order and length as the English lines; "/" = line break.
"""
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def entries(ep):
    out = [(max(0.0, c.start), min(c.end, ep.DURATION), c.plain()) for c in ep.CAPTIONS if c.start < ep.DURATION]
    out += [(a, min(b, ep.DURATION), s) for (a, b, s) in getattr(ep, "SUBTITLE_EXTRAS", [])]
    return sorted(out, key=lambda e: e[0])


def ts(x):
    ms = int(round(x * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write(ep_name, path):
    ep = importlib.import_module(ep_name)
    ents = entries(ep)
    data = json.load(open(path, encoding="utf-8"))
    os.makedirs(os.path.join(HERE, "out", "subs"), exist_ok=True)
    for lang, lines in data.items():
        if len(lines) != len(ents):
            raise SystemExit(f"{lang}: {len(lines)} lines, expected {len(ents)}")
        srt = [f"{i}\n{ts(a)} --> {ts(b)}\n{line.replace(' / ', chr(10)).replace('/', chr(10))}\n"
               for i, ((a, b, _), line) in enumerate(zip(ents, lines), 1)]
        p = os.path.join(HERE, "out", "subs", f"{ep_name}.{lang}.srt")
        open(p, "w", encoding="utf-8").write("\n".join(srt))
        print("wrote", p)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        for i, (a, b, s) in enumerate(entries(importlib.import_module(sys.argv[1]))):
            print(f"{i:2d}  {a:5.2f}-{b:5.2f}  {s!r}")
    else:
        write(sys.argv[1], sys.argv[2])
