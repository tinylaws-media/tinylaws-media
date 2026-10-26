"""Subtitle tracks for YouTube (one .srt per language).

    python3 subtitles.py ep001                 # prints the English lines, in order, to translate
    python3 subtitles.py ep001 ep001_subs.json # writes out/subs/ep001.<lang>.srt for every language

The JSON holds {"en": [...], "fr": [...], ...}: one list per language, same order and length as the
English lines. A "/" in a line becomes a line break. TikTok and Instagram do not accept subtitle files,
so the burned-in English captions stay; these tracks are for YouTube Studio (Subtitles > Add language).
"""
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def entries(ep):
    out = []
    for cap in ep.CAPTIONS:
        words = [w for w in cap.words]
        if not words:
            continue
        start = max(0.0, words[0][0])
        text = " ".join(w[1] for w in words).replace(" / ", "\n").replace("/", "\n").strip()
        out.append((start, cap.end, text))
    for (a, b, s) in getattr(ep, "SUBTITLE_EXTRAS", []):
        out.append((a, b, s))
    out.sort(key=lambda e: e[0])
    return out


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
        srt = []
        for i, ((a, b, _), line) in enumerate(zip(ents, lines), 1):
            srt.append(f"{i}\n{ts(a)} --> {ts(b)}\n{line.replace(' / ', chr(10)).replace('/', chr(10))}\n")
        p = os.path.join(HERE, "out", "subs", f"{ep_name}.{lang}.srt")
        open(p, "w", encoding="utf-8").write("\n".join(srt))
        print("wrote", p)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        ep = importlib.import_module(sys.argv[1])
        for i, (a, b, s) in enumerate(entries(ep)):
            print(f"{i:2d}  {a:5.2f}-{b:5.2f}  {s!r}")
    else:
        write(sys.argv[1], sys.argv[2])
