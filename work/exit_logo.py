"""THE EXIT MANUAL — the Build the Commons logo as 12 separate fragments (owner's SVGs in logo/).

    python3 exit_logo.py            # -> out/logo_check.png (grouped, semi-expanded, final; fragments numbered)

Each top-level <g> of the layer is one fragment (two flattened pentagons). Paths and nested matrix() transforms are
parsed here (the files only use M/L/Z polygons and matrix()), so every fragment is a skia.Path in a common frame
centred on the logo's centre, in "logo units" (1 unit = 1 SVG mm). LOGO_R is the radius of the formed logo.
The small star in the centre of btc_logo_final.svg is kept as STAR (drawn last, after the fragments meet).
"""
import math
import os
import re
import xml.etree.ElementTree as ET

import skia

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "logo")
NS = "{http://www.w3.org/2000/svg}"


def _mat(s):
    if not s:
        return (1, 0, 0, 1, 0, 0)
    m = re.match(r"\s*matrix\(([^)]*)\)", s)
    if m:
        return tuple(float(v) for v in re.split(r"[ ,]+", m.group(1).strip()))
    m = re.match(r"\s*translate\(([^)]*)\)", s)
    if m:
        v = [float(x) for x in re.split(r"[ ,]+", m.group(1).strip())]
        return (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
    raise ValueError(s)


def _mul(a, b):            # a ∘ b (apply b first)
    return (a[0] * b[0] + a[2] * b[1], a[1] * b[0] + a[3] * b[1], a[0] * b[2] + a[2] * b[3],
            a[1] * b[2] + a[3] * b[3], a[0] * b[4] + a[2] * b[5] + a[4], a[1] * b[4] + a[3] * b[5] + a[5])


def _app(m, x, y):
    return (m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5])


def _poly(d):
    """Polygons from an M/L/Z path (absolute or relative)."""
    toks = re.findall(r"[MmLlZzHhVv]|-?\d*\.?\d+(?:e-?\d+)?", d)
    polys, cur, cmd, x, y, i = [], [], "M", 0.0, 0.0, 0
    while i < len(toks):
        tk = toks[i]
        if tk in "MmLlZzHhVv":
            cmd = tk
            i += 1
            if cmd in "Zz":
                if cur:
                    polys.append(cur)
                cur = []
            continue
        if cmd in "Hh":
            x = float(tk) + (x if cmd == "h" else 0)
            i += 1
        elif cmd in "Vv":
            y = float(tk) + (y if cmd == "v" else 0)
            i += 1
        else:
            a, b = float(toks[i]), float(toks[i + 1])
            i += 2
            if cmd in "ml" and cur:
                x, y = x + a, y + b
            elif cmd == "m":
                x, y = x + a, y + b
            else:
                x, y = a, b
            if cmd in "Mm":
                if cur:
                    polys.append(cur)
                cur = []
                cmd = "l" if cmd == "m" else "L"
        cur.append((x, y))
    if cur:
        polys.append(cur)
    return polys


def fragments(name="btc_logo_grouped_bw.svg"):
    """[[polygon, ...], ...] one list per fragment, in SVG user units, plus the star polygons (final file)."""
    root = ET.parse(os.path.join(LOGO, name)).getroot()
    layer = [g for g in root.iter(NS + "g") if g.get("id") == "layer1"][0]
    frags, star = [], []

    def walk(el, m, out):
        m = _mul(m, _mat(el.get("transform")))
        if el.tag == NS + "path":
            for p in _poly(el.get("d")):
                out.append([_app(m, *q) for q in p])
        for ch in el:
            walk(ch, m, out)

    for el in layer:
        if el.tag == NS + "g":
            out = []
            walk(el, (1, 0, 0, 1, 0, 0), out)
            frags.append(out)
        elif el.tag == NS + "path":
            out = []
            walk(el, (1, 0, 0, 1, 0, 0), out)
            star += out
    return frags, star


class Logo:
    """Fragments centred on the logo centre. pieces[i] = (path, (cx, cy) centroid, angle of centroid)."""

    def __init__(self):
        frf, star = fragments("btc_logo_final.svg")
        fr = frf                       # the formed logo = the owner's final logo (fragments + centre star)
        allp = [q for f in fr for p in f for q in p]
        xs, ys = [q[0] for q in allp], [q[1] for q in allp]
        self.c0 = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
        self.R = max(math.hypot(q[0] - self.c0[0], q[1] - self.c0[1]) for q in allp)
        self.pieces = []
        for f in fr:
            path = skia.Path()
            pts = []
            for poly in f:
                path.moveTo(poly[0][0] - self.c0[0], poly[0][1] - self.c0[1])
                for q in poly[1:]:
                    path.lineTo(q[0] - self.c0[0], q[1] - self.c0[1])
                path.close()
                pts += poly
            cx = sum(q[0] for q in pts) / len(pts) - self.c0[0]
            cy = sum(q[1] for q in pts) / len(pts) - self.c0[1]
            self.pieces.append((path, (cx, cy), math.atan2(cy, cx)))
        # arrival order: clockwise from the top, so the logo closes like a ring
        self.order = sorted(range(len(self.pieces)), key=lambda i: (self.pieces[i][2] + math.pi / 2) % (2 * math.pi))
        # the centre star of the final logo, in the same frame (the final file uses the same coordinates)
        self.star = None
        sp = [p for p in star if len(p) >= 4]
        if sp and frf:
            fp = [q for f in frf for p in f for q in p]
            fx, fy = [q[0] for q in fp], [q[1] for q in fp]
            c0f = ((min(fx) + max(fx)) / 2, (min(fy) + max(fy)) / 2)
            kf = self.R / max(math.hypot(q[0] - c0f[0], q[1] - c0f[1]) for q in fp)
            path = skia.Path()
            for poly in sp:
                path.moveTo((poly[0][0] - c0f[0]) * kf, (poly[0][1] - c0f[1]) * kf)
                for q in poly[1:]:
                    path.lineTo((q[0] - c0f[0]) * kf, (q[1] - c0f[1]) * kf)
                path.close()
            b = path.getBounds()
            if b.width() < self.R * 0.6:          # only keep it if it really is the small centre star
                self.star = path


if __name__ == "__main__":
    from PIL import Image
    L = Logo()
    print(len(L.pieces), "fragments, R =", round(L.R, 2), "centre", [round(v, 2) for v in L.c0],
          "star", L.star.getBounds() if L.star else None)
    s = skia.Surface(1200, 1200)
    c = s.getCanvas()
    c.clear(0xFF05060A)
    c.translate(600, 600)
    k = 520 / L.R
    c.scale(k, k)
    f = skia.Font(skia.Typeface.MakeFromFile(os.path.join(HERE, "fonts", "IBMPlexMono-Medium.ttf")), 6)
    for n, i in enumerate(L.order):
        p, (cx, cy), _ = L.pieces[i]
        c.drawPath(p, skia.Paint(AntiAlias=True, Color=0xFFE8ECEF))
        c.drawString(str(n), cx, cy, f, skia.Paint(AntiAlias=True, Color=0xFFFF2E88))
    if L.star:
        c.drawPath(L.star, skia.Paint(AntiAlias=True, Color=0xFF39FF88))
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    Image.fromarray(s.makeImageSnapshot().toarray()[..., [2, 1, 0]]).save(os.path.join(HERE, "out", "logo_check.png"))
    # reference: what the owner's final logo looks like (rendered by skia's SVG module, for comparison only)
    try:
        st = skia.Stream.MakeFromFile(os.path.join(LOGO, "btc_logo_final.svg"))
        dom = skia.SVGDOM.MakeFromStream(st)
        s2 = skia.Surface(600, 600)
        c2 = s2.getCanvas()
        c2.scale(1.5, 1.5)
        c2.translate(-105 * 3.7795 + 200, -148.5 * 3.7795 + 200)
        dom.render(c2)
        Image.fromarray(s2.makeImageSnapshot().toarray()[..., [2, 1, 0]]).save(os.path.join(HERE, "out", "logo_ref.png"))
    except Exception as e:  # noqa: BLE001
        print("svgdom:", e)
