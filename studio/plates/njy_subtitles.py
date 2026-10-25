"""Subtitle files: python3 njy_subtitles.py njy_ep001 njy_ep001_subs.json -> out/subs/<ep>.<lang>.srt

The JSON holds {"en": [...], "fr": [...]} with one line per narration line (same order as LINES);
" / " is a line break. Without a JSON, the English comes from the captions (stars removed)."""
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def ts(x):
    ms = int(round(x * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main(epname, path=None):
    ep = importlib.import_module(epname)
    data = json.load(open(path, encoding="utf-8")) if path else {}
    data.setdefault("en", [ln["cap"].replace("*", "") for ln in ep.LINES])
    os.makedirs(os.path.join(HERE, "out", "subs"), exist_ok=True)
    for lang, lines in data.items():
        assert len(lines) == len(ep.LINES), (lang, len(lines))
        out = []
        for i, ((a, b), txt) in enumerate(zip(ep.TL, lines)):
            end = ep.TL[i + 1][0] - 0.05 if i + 1 < len(ep.TL) else ep.DURATION
            out.append(f"{i + 1}\n{ts(0.0 if i == 0 else a)} --> {ts(end)}\n{txt.replace(' / ', chr(10))}\n")
        p = os.path.join(HERE, "out", "subs", f"{epname}.{lang}.srt")
        open(p, "w", encoding="utf-8").write("\n".join(out))
        print("wrote", p)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
