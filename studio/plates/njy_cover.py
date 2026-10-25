"""Cover image: python3 njy_cover.py njy_ep001 'line one' 'line *two*' -> out/<ep>_cover.png (1080x1920)"""
import importlib
import sys

import skia
from PIL import Image

from njy_engine import *

ep = importlib.import_module(sys.argv[1])
s = skia.Surface(W, H)
c = s.getCanvas()
c.clear(col(NIGHT))
ep.draw_world(c, float(sys.argv[4]) if len(sys.argv) > 4 else 1.2)
lines = sys.argv[2:4]
size = 112
while max(rich_width(parse_rich(l), size) for l in lines) > 2 * (SAFE_RIGHT - 540) - 10:
    size -= 2
for i, l in enumerate(lines):
    draw_rich(c, l, 540, 420 + i * size * 1.1, size)
text(c, "it's not just you.", 540, 420 + 2 * size * 1.1 + 40, 60, ROSE, 0.95, italic=True)
draw_grain(c, 0.06)
Image.fromarray(s.makeImageSnapshot().toarray()[..., [2, 1, 0]]).save(f"out/{sys.argv[1]}_cover.png")
print("saved", f"out/{sys.argv[1]}_cover.png")
