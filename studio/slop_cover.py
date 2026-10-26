"""SLOP SHOP — cover image: python3 slop_cover.py slop_ep002 out/cover.png
Uses the episode's cover(R) if it has one (#002+), else #001's host shot with the series title."""
import importlib
import sys

import skia

from slop_engine import W, H, Assets, Slop, YELLOW, RED, INK, sticker, reality_bar


def main(epname, path):
    ep = importlib.import_module(epname)
    s = skia.Surface(W, H)
    R = Slop(Assets(), s.getCanvas(), 0.0)
    if hasattr(ep, "cover"):
        ep.cover(R)
    else:
        ep.host_shot(R, 0.4, "it was thursday.", 1.0)
        reality_bar(R, 99)
        c = R.c
        c.save()
        c.translate(520, 560)
        c.rotate(-4)
        R.text("DID YOU KNOW?", 0, 0, "bungee", 96, YELLOW, INK, 16, shadow=(INK, 7, 9))
        R.text("(NO)", 0, 130, "bungee", 120, RED, INK, 16, rot=4, shadow=(INK, 7, 9))
        c.restore()
        sticker(R, "1 of these facts is real", 330, 388, size=48)
    s.makeImageSnapshot().save(path, skia.kPNG)
    print("wrote", path)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
