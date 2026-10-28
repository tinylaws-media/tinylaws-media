"""Render a 2D Subject Zero episode (24 fps): python3 sz2render.py nemo01_pic [--sheet t1 t2 ...] [--procs 2]"""
import importlib
import os
import subprocess
import sys
import time
from multiprocessing import Process

import skia

from sz2d import W, H, FPS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def worker(mod, f0, f1, path):
    ep = importlib.import_module(mod)
    s = skia.Surface(W, H)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", path]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    for fi in range(f0, f1):
        c = s.getCanvas()
        c.clear(skia.ColorBLACK)
        ep.draw_frame(c, fi / FPS)
        pr.stdin.write(s.makeImageSnapshot().toarray().tobytes())
        if (fi - f0) % 120 == 0:
            print(f"[{os.path.basename(path)}] {fi}/{f1} {time.time() - t0:.0f}s", flush=True)
    pr.stdin.close()
    pr.wait()


def render(mod, procs=2):
    ep = importlib.import_module(mod)
    n = int(round(ep.DURATION * FPS))
    parts, ps = [], []
    for i in range(procs):
        a, b = n * i // procs, n * (i + 1) // procs
        p = os.path.join(OUT, f"{mod}_part{i}.mp4")
        parts.append(p)
        ps.append(Process(target=worker, args=(mod, a, b, p)))
    t0 = time.time()
    for p in ps:
        p.start()
    for p in ps:
        p.join()
    lst = os.path.join(OUT, f"{mod}_parts.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    os.path.join(OUT, f"{mod}_video.mp4")], check=True)
    print(f"video done in {time.time() - t0:.0f} s")


def sheet(mod, times, cols=6, name=None):
    from PIL import Image, ImageDraw
    ep = importlib.import_module(mod)
    tw, th = 270, 480
    rows = (len(times) + cols - 1) // cols
    sh = Image.new("RGB", (cols * tw, rows * (th + 26)), (20, 20, 20))
    d = ImageDraw.Draw(sh)
    s = skia.Surface(W, H)
    for i, t in enumerate(times):
        c = s.getCanvas()
        c.clear(skia.ColorBLACK)
        ep.draw_frame(c, t)
        img = s.makeImageSnapshot().toarray()[:, :, [2, 1, 0]]
        im = Image.fromarray(img).resize((tw, th))
        x, y = (i % cols) * tw, (i // cols) * (th + 26)
        sh.paste(im, (x, y))
        d.text((x + 6, y + th + 4), f"{t:.2f}s", fill=(230, 230, 230))
    p = os.path.join(OUT, f"{name or mod}_sheet.png")
    sh.save(p)
    print("saved", p)


if __name__ == "__main__":
    mod = sys.argv[1]
    if "--sheet" in sys.argv:
        i = sys.argv.index("--sheet")
        ts = [float(x) for x in sys.argv[i + 1:] if not x.startswith("--")]
        sheet(mod, ts)
    else:
        procs = int(sys.argv[sys.argv.index("--procs") + 1]) if "--procs" in sys.argv else 2
        render(mod, procs)
