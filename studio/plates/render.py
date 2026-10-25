"""Render an episode: python3 render.py ep001 [--sheet] [--frames a b]"""
import importlib
import os
import subprocess
import sys
import time
from multiprocessing import Process

import numpy as np
import skia

import engine
from engine import W, H, FPS, Assets, Riso

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


def grain_pass(R):
    g = R.A.grains[R.boil % len(R.A.grains)]
    p = skia.Paint(BlendMode=skia.BlendMode.kMultiply)
    p.setAlphaf(0.28)
    R.c.drawImageRect(g, skia.Rect(0, 0, W, H), skia.SamplingOptions(skia.FilterMode.kLinear), p)


def render_frame(ep, A, fi, surface=None):
    s = surface or skia.Surface(W, H)
    c = s.getCanvas()
    c.clear(skia.ColorWHITE)
    R = Riso(A, c, fi)
    ep.draw_frame(R, fi / FPS)
    grain_pass(R)
    return s


def worker(epname, f0, f1, path):
    ep = importlib.import_module(epname)
    A = Assets()
    s = skia.Surface(W, H)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "15",
           "-pix_fmt", "yuv420p", "-x264-params", "keyint=48", path]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    for fi in range(f0, f1):
        render_frame(ep, A, fi, s)
        arr = s.makeImageSnapshot().toarray()
        pr.stdin.write(arr.tobytes())
        if (fi - f0) % 120 == 0:
            print(f"[{path[-12:]}] frame {fi}/{f1}  {time.time() - t0:.0f}s", flush=True)
    pr.stdin.close()
    pr.wait()


def sheet(epname, times, cols=6, name="sheet"):
    ep = importlib.import_module(epname)
    A = Assets()
    from PIL import Image, ImageDraw
    tw, th = 270, 480
    rows = (len(times) + cols - 1) // cols
    out = Image.new("RGB", (cols * tw, rows * (th + 24)), "white")
    d = ImageDraw.Draw(out)
    for i, t in enumerate(times):
        s = render_frame(ep, A, int(round(t * FPS)))
        a = s.makeImageSnapshot().toarray()[..., [2, 1, 0]]
        im = Image.fromarray(a).resize((tw, th), Image.LANCZOS)
        x, y = (i % cols) * tw, (i // cols) * (th + 24)
        out.paste(im, (x, y))
        d.text((x + 6, y + th + 4), f"{t:.2f}s", fill="black")
    out.save(f"{OUT}/{name}.png")
    print("saved", f"{OUT}/{name}.png")


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


if __name__ == "__main__":
    ep = sys.argv[1]
    if "--sheet" in sys.argv:
        i = sys.argv.index("--sheet")
        ts = [float(x) for x in sys.argv[i + 1:]]
        sheet(ep, ts, name=f"{ep}_sheet")
    else:
        full(ep)
