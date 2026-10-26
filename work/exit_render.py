"""Render a THE EXIT MANUAL episode.

    python3 exit_render.py exit_ep001                       # out/exit_ep001_video.mp4 (parallel workers)
    python3 exit_render.py exit_ep001 --sheet 0 0.5 1 ...   # out/exit_ep001_sheet.png contact sheet
    python3 exit_render.py exit_ep001 --sheet-hook          # first 8 s every 0.5 s
    python3 exit_render.py exit_ep001 --sheet-keys          # ~30 key frames incl. the last
    python3 exit_render.py exit_ep001 --frame 12.3          # out/exit_ep001_f12.30.png full size
"""
import importlib
import os
import subprocess
import sys
import time
from multiprocessing import Process

import numpy as np
import skia

from exit_engine import W, H, FPS, Assets, Ctx

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


def render_frame(ep, A, fi, surface=None):
    s = surface or skia.Surface(W, H)
    c = s.getCanvas()
    c.clear(0xFF05060A)
    X = Ctx(A, c, fi / FPS)
    ep.draw_frame(X, fi / FPS)
    return s


def worker(epname, f0, f1, path):
    ep = importlib.import_module(epname)
    A = Assets()
    s = skia.Surface(W, H)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14",
           "-pix_fmt", "yuv420p", "-x264-params", "keyint=48", path]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    for fi in range(f0, f1):
        render_frame(ep, A, fi, s)
        pr.stdin.write(s.makeImageSnapshot().toarray().tobytes())
        if (fi - f0) % 240 == 0:
            print(f"[{os.path.basename(path)}] frame {fi}/{f1}  {time.time() - t0:.0f}s", flush=True)
    pr.stdin.close()
    pr.wait()


def sheet(epname, times, cols=6, name=None):
    from PIL import Image, ImageDraw
    ep = importlib.import_module(epname)
    A = Assets()
    tw, th = 270, 480
    rows = (len(times) + cols - 1) // cols
    out = Image.new("RGB", (cols * tw, rows * (th + 24)), "white")
    d = ImageDraw.Draw(out)
    for i, t in enumerate(times):
        s = render_frame(ep, A, min(int(round(t * FPS)), int(ep.DURATION * FPS) - 1))
        a = s.makeImageSnapshot().toarray()[..., [2, 1, 0]]
        im = Image.fromarray(a).resize((tw, th), Image.LANCZOS)
        x, y = (i % cols) * tw, (i // cols) * (th + 24)
        out.paste(im, (x, y))
        d.text((x + 6, y + th + 4), f"{t:.2f}s", fill="black")
    p = f"{OUT}/{name or epname + '_sheet'}.png"
    out.save(p)
    print("saved", p)


def frame_png(epname, t):
    from PIL import Image
    ep = importlib.import_module(epname)
    s = render_frame(ep, Assets(), int(round(t * FPS)))
    p = f"{OUT}/{epname}_f{t:05.2f}.png"
    Image.fromarray(s.makeImageSnapshot().toarray()[..., [2, 1, 0]]).save(p)
    print("saved", p)


def full(epname, workers=2):
    ep = importlib.import_module(epname)
    n = int(round(ep.DURATION * FPS))
    bounds = np.linspace(0, n, workers + 1).astype(int)
    paths = [f"{OUT}/{epname}_part{i}.mp4" for i in range(workers)]
    ps = [Process(target=worker, args=(epname, bounds[i], bounds[i + 1], paths[i])) for i in range(workers)]
    t0 = time.time()
    for p in ps:
        p.start()
    for p in ps:
        p.join()
    lst = f"{OUT}/{epname}_parts.txt"
    with open(lst, "w") as f:
        for p in paths:
            f.write(f"file '{p}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    f"{OUT}/{epname}_video.mp4"], check=True)
    print("video done in", round(time.time() - t0), "s")


def key_times(ep):
    """~30 key frames: start, middle and end of every caption block, plus the last frame."""
    ts = set()
    for cap in ep.CAPTIONS:
        if cap.start < ep.DURATION:
            ts.add(round(cap.start + 0.35, 2))
    ts |= set(getattr(ep, "EXTRA_KEYS", []))
    ts = sorted(t for t in ts if t < ep.DURATION)
    if len(ts) > 29:
        idx = np.linspace(0, len(ts) - 1, 29).round().astype(int)
        ts = [ts[i] for i in idx]
    return ts + [round(ep.DURATION - 1 / FPS, 3)]


if __name__ == "__main__":
    ep = sys.argv[1]
    if "--sheet" in sys.argv:
        i = sys.argv.index("--sheet")
        sheet(ep, [float(x) for x in sys.argv[i + 1:]])
    elif "--sheet-hook" in sys.argv:
        sheet(ep, [round(0.5 * k, 2) for k in range(17)], name=f"{ep}_sheet_hook")
    elif "--sheet-keys" in sys.argv:
        sheet(ep, key_times(importlib.import_module(ep)), name=f"{ep}_sheet_keys")
    elif "--frame" in sys.argv:
        frame_png(ep, float(sys.argv[sys.argv.index("--frame") + 1]))
    else:
        full(ep)
