"""NOT JUST YOU — render an episode.

    python3 njy_render.py njy_ep001 --sheet 0 0.5 1 ...   # contact sheet -> out/<ep>_sheet.png
    python3 njy_render.py njy_ep001 --frame 12.3           # one full-size PNG -> out/<ep>_f12.30.png
    python3 njy_render.py njy_ep001                        # out/<ep>_video.mp4 (silent; finish.py muxes)
"""
import importlib
import os
import subprocess
import sys
import time
from multiprocessing import Process

import numpy as np
import skia

from njy_engine import W, H, FPS, NIGHT, col

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


def render(ep, t, s=None):
    s = s or skia.Surface(W, H)
    c = s.getCanvas()
    c.clear(col(NIGHT))
    ep.draw_frame(c, t)
    return s


def rgb_array(s):
    return s.makeImageSnapshot().toarray()[..., [2, 1, 0]]


def worker(epname, f0, f1, path):
    ep = importlib.import_module(epname)
    s = skia.Surface(W, H)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14",
           "-pix_fmt", "yuv420p", "-x264-params", "keyint=48", path]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    for fi in range(f0, f1):
        render(ep, fi / FPS, s)
        pr.stdin.write(s.makeImageSnapshot().toarray().tobytes())
        if (fi - f0) % 240 == 0:
            print(f"[{os.path.basename(path)}] frame {fi}/{f1}  {time.time() - t0:.0f}s", flush=True)
    pr.stdin.close()
    pr.wait()


def sheet(epname, times, cols=6, name=None):
    from PIL import Image, ImageDraw
    ep = importlib.import_module(epname)
    tw, th = 270, 480
    rows = (len(times) + cols - 1) // cols
    out = Image.new("RGB", (cols * tw, rows * (th + 24)), "white")
    d = ImageDraw.Draw(out)
    for i, t in enumerate(times):
        im = Image.fromarray(rgb_array(render(ep, t))).resize((tw, th), Image.LANCZOS)
        x, y = (i % cols) * tw, (i // cols) * (th + 24)
        out.paste(im, (x, y))
        d.text((x + 6, y + th + 4), f"{t:.2f}s", fill="black")
    p = f"{OUT}/{name or epname + '_sheet'}.png"
    out.save(p)
    print("saved", p)


def frame(epname, t):
    from PIL import Image
    ep = importlib.import_module(epname)
    p = f"{OUT}/{epname}_f{t:05.2f}.png"
    Image.fromarray(rgb_array(render(ep, t))).save(p)
    print("saved", p)


def full(epname, workers=2):
    ep = importlib.import_module(epname)
    n = int(round(ep.DURATION * FPS))
    b = np.linspace(0, n, workers + 1).astype(int)
    paths = [f"{OUT}/{epname}_part{i}.mp4" for i in range(workers)]
    ps = [Process(target=worker, args=(epname, b[i], b[i + 1], paths[i])) for i in range(workers)]
    t0 = time.time()
    [p.start() for p in ps]
    [p.join() for p in ps]
    lst = f"{OUT}/{epname}_parts.txt"
    open(lst, "w").write("".join(f"file '{p}'\n" for p in paths))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    f"{OUT}/{epname}_video.mp4"], check=True)
    print("video done in", round(time.time() - t0), "s")


if __name__ == "__main__":
    ep = sys.argv[1]
    if "--sheet" in sys.argv:
        i = sys.argv.index("--sheet")
        args = sys.argv[i + 1:]
        name = None
        if args and not args[0].replace(".", "").isdigit():
            name, args = args[0], args[1:]
        sheet(ep, [float(x) for x in args], name=name)
    elif "--frame" in sys.argv:
        frame(ep, float(sys.argv[sys.argv.index("--frame") + 1]))
    else:
        full(ep)
