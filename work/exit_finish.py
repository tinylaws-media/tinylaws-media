"""Finish a THE EXIT MANUAL episode: -14 LUFS, true peak below -1 dBTP, H.264 + AAC, plus a cover PNG.

    python3 exit_finish.py exit_ep001 TheExitManual_001_FollowTheMoney
"""
import importlib
import json
import os
import re
import subprocess
import sys

import skia

from exit_engine import W, H, Assets, Ctx

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def loud(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    return json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))


def main(ep_name, name):
    ep = importlib.import_module(ep_name)
    video, wav = f"{OUT}/{ep_name}_video.mp4", f"{OUT}/{ep_name}_audio.wav"
    m = loud(wav)
    gain = -14.0 - float(m["input_i"])
    limit = 10 ** (-1.5 / 20)
    af = f"volume={gain:.2f}dB,aresample=192000,alimiter=limit={limit:.4f}:attack=3:release=80:level=false,aresample=48000"
    dst = f"{OUT}/{name}.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", video, "-i", wav, "-map", "0:v",
                    "-map", "1:a", "-af", af, "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-maxrate", "10M",
                    "-bufsize", "20M", "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "-shortest", dst], check=True)
    f = loud(dst)
    print(f"wrote {dst}: {f['input_i']} LUFS, true peak {f['input_tp']} dBTP")
    if hasattr(ep, "draw_cover"):
        s = skia.Surface(W, H)
        c = s.getCanvas()
        c.clear(0xFF05060A)
        ep.draw_cover(Ctx(Assets(), c, 0.0))
        from PIL import Image
        Image.fromarray(s.makeImageSnapshot().toarray()[..., [2, 1, 0]]).save(f"{OUT}/{name}_cover.png")
        print("wrote", f"{OUT}/{name}_cover.png")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
