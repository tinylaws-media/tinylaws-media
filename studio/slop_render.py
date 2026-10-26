"""Render a Slop Shop episode: python3 slop_render.py slop_ep001 [--sheet t1 t2 ...] [--name sheetname]"""
import importlib
import os
import subprocess
import sys
import time
from multiprocessing import Process

import numpy as np
import skia

from slop_engine import W, H, FPS, Assets, Slop

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


def render_frame(ep, A, fi, surface=None):
    s = surface or skia.Surface(W, H)
    c = s.getCanvas()
    c.clear(skia.ColorBLACK)
    ep.draw_frame(Slop(A, c, fi / FPS), fi / FPS)
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
        pr.stdin.write(s.makeImageSnapshot().toarray().tobytes())
        if (fi - f0) % 240 == 0:
            print(f"[{os.path.basename(path)}] frame {fi}/{f1}  {time.time() - t0:.0f}s", flush=True)
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
    p = f"{OUT}/{name}.png"
    out.save(p)
    print("saved", p)


def frame_png(epname, t, path):
    ep = importlib.import_module(epname)
    s = render_frame(ep, Assets(), int(round(t * FPS)))
    s.makeImageSnapshot().save(path, skia.kPNG)


def full(epname, workers=None):
    ep = importlib.import_module(epname)
    workers = workers or max(1, min(8, os.cpu_count() or 2))
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
    for p in paths:
        os.remove(p)
    print("video done in", round(time.time() - t0), "s")


if __name__ == "__main__":
    ep = sys.argv[1]
    if "--sheet" in sys.argv:
        i = sys.argv.index("--sheet")
        name = f"{ep}_sheet"
        args = sys.argv[i + 1:]
        if "--name" in args:
            j = args.index("--name")
            name = args[j + 1]
            args = args[:j]
        sheet(ep, [float(x) for x in args], name=name)
    elif "--frame" in sys.argv:
        i = sys.argv.index("--frame")
        frame_png(ep, float(sys.argv[i + 1]), sys.argv[i + 2])
    else:
        full(ep)
