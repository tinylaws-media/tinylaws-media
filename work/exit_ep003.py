"""THE EXIT MANUAL — TRANSMISSION 001 (v3) · EXIT: "Forty days a year."
Demo episode, v3 after the owner's notes of 26 Oct 2026: back to a dark, cryptic, whistleblower atmosphere
(disguised voice, dark score), animation pushed further (camera through space, depth, data streams, kinetic type,
the eye that glitches into pixels and swallows the camera), and "build the commons." as the way out the whole
episode climbs to. Topic and core facts kept from v2.

Facts (checked 25-26 Oct 2026, primary sources):
- Time: DataReportal / Kepios with GWI, "Digital 2026 Global Overview Report" (Oct 2025): online adults spend on
  average 18 h 36 min a week on social and video platforms (YouTube and TikTok included).
  18.6 h / 7 = 2.66 h a day = 11.07 % of each day; x 52.14 weeks = 970 h = 40.4 days of 24 h a year.
  https://datareportal.com/reports/digital-2026-global-overview-report
- Meta, Form 10-K for fiscal 2025 (filed Jan 2026), verbatim excerpts: "...significantly determined by our success in
  adding, retaining, and engaging active users..." and the risk-factor heading "...if our users decrease their level
  of engagement with our products, our revenue, financial results, and business may be significantly harmed."
  https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm
- Meta Q4 & full-year 2025 results (28 Jan 2026): revenue $200.97 bn (advertising $196.18 bn); 3.58 bn daily
  active people (Dec 2025); ad impressions +12 % in 2025. ARPP $12.36 + $13.65 + $14.46 + $16.56 = $57.03 in 2025,
  i.e. 16 cents a day (worldwide average).
  https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Fourth-Quarter-and-Full-Year-2025-Results-2026.pdf
- Sleep: Hjetland et al., Frontiers in Psychiatry (31 Mar 2025), 45,202 students aged 18-28, Norway (SHoT 2022):
  each extra hour of screen use after going to bed = 59 % higher odds of insomnia symptoms and 24 min less sleep.
  "This study cannot determine causality." https://doi.org/10.3389/fpsyt.2025.1548273
- EU: European Commission, 6 Feb 2026, PRELIMINARY findings that TikTok's addictive design (infinite scroll,
  autoplay, push notifications, recommender) breaches the Digital Services Act; TikTok disputes them.
  https://digital-strategy.ec.europa.eu/en/news/commission-preliminarily-finds-tiktoks-addictive-design-breach-digital-services-act
- Mastodon (new in v3): joinmastodon.org (read 26 Oct 2026): "No algorithms or ads to waste your time", "We will
  never serve ads", "too important to belong to one company", each server "a completely independent entity",
  "developed by a non-profit organization", speaks ActivityPub. ActivityPub = W3C Recommendation, 23 Jan 2018.
  https://joinmastodon.org/  ·  https://www.w3.org/TR/activitypub/
Guardrails: no real person drawn, no logo (company names as text only), illustrations labelled, legal action only.
"""
import json
import math
import os

import numpy as np
import skia

from exit_look3 import *            # noqa: F401,F403
from exit_look3 import (Cam, plane, tilt_quad, data_rain, vignette, hud, glitch, offscreen, streams, bezier,
                        kin_text, typed_mono, count, Caption3, Assets3, smooth, quad_matrix)
from exit_look2 import (Ctx2, Assets2, CAP_CX, phone, feed, feed_card, is_ad, eye, pixelated, year_grid, cell_xy,
                        GRID_X0, GRID_Y0, GRID_PITCH, GRID_CELL, GRID_COLS, PHONE_W, PHONE_H, CARD_H, CARD_GAP, tag,
                        doc_lines, ease_io5)
from exit_engine import W, H, FPS, clamp01, prog, lerp, ease_out, ease_in_out, relay
from exit_ep003_lines import LINES, CAPS

EPISODE = "001"
SERIES = "EXIT"
VOICE = "am_fenrir"            # casting v3, take 1 (out/exit_casting_v3.wav)
VOICE_SPEED = 1.0
VOICE_FX = {"disguise": True, "semitones": -3.0, "lo": 150, "hi": 5800, "drive": 1.6, "room": 0.22}
START = 0.08
TAIL = 0.4

# ------------------------------------------------------------------ timing
_HERE = os.path.dirname(os.path.abspath(__file__))
_TP = os.path.join(_HERE, "out", "exit_ep003_timing.json")
TIM = json.load(open(_TP)) if os.path.exists(_TP) else None
if TIM and [(l[0], " ".join(p.strip() for p in l[1].split("|"))) for l in LINES] != \
        [(k, v["text"]) for k, v in TIM.items() if not k.startswith("_")]:
    TIM = None
DURATION = round(TIM["_end"] + TAIL, 2) if TIM else None


def T(i):
    return TIM[i]["start"]


def E(i):
    return TIM[i]["end"]


def CH(i, k):
    return TIM[i]["chunks"][k]


def nxt(i):
    ids = [l[0] for l in LINES]
    j = ids.index(i)
    return T(ids[j + 1]) if j + 1 < len(ids) else DURATION


CAP_STYLE = {"stop": dict(size=116, y=1190, hi="white"), "warn": dict(hi="magenta"), "times": dict(hi="magenta"),
             "dollar": dict(hi="magenta"), "slot": dict(hi="magenta"), "eu": dict(hi="cyan")}
CAPTIONS = []
if TIM:
    for (lid, _, _, *r) in LINES:
        blocks = CAPS[lid]
        ch = TIM[lid]["chunks"]
        assert len(blocks) == len(ch), lid
        for k, txt in enumerate(blocks):
            if txt is None:
                continue
            a = ch[k] - 0.04
            se = ch[k + 1] - 0.04 if k + 1 < len(blocks) else E(lid)
            b = ch[k + 1] - 0.04 if k + 1 < len(blocks) else (DURATION + 1 if lid == "loop" else nxt(lid) - 0.04)
            CAPTIONS.append(Caption3(a, b, txt, speak_end=se, **CAP_STYLE.get(lid, {})))

_EP = os.path.join(_HERE, "out", "exit_ep003_voice_env.npy")
VOICE_ENV = np.load(_EP) if os.path.exists(_EP) else None


def level(t):
    if VOICE_ENV is None:
        return 0.0
    i = int(t * FPS)
    return float(VOICE_ENV[i]) if 0 <= i < len(VOICE_ENV) else 0.0


# ------------------------------------------------------------------ shared pieces
SRC = {
    "time": "source: DataReportal / GWI, Digital 2026 (Oct 2025)",
    "meta": "source: Meta, full-year 2025 results (Jan 2026)",
    "10k": "source: Meta, annual report (Form 10-K), 2025",
    "sleep": "source: Hjetland et al., Frontiers in Psychiatry, 2025",
    "eu": "source: European Commission, 6 Feb 2026 (preliminary)",
    "masto": "source: joinmastodon.org (Oct 2026) · W3C ActivityPub, 2018",
}


SRC2 = {"time": "18 h 36 min a week · average online adult", "meta": "worldwide averages"}


def source(X, key, alpha=1.0):
    if alpha > 0:
        X.text(SRC[key], 80, 376, 27, "grey", kind="mono", align="left", alpha=alpha)
        if key in SRC2:
            X.text(SRC2[key], 80, 408, 24, "grey", kind="mono", align="left", alpha=0.85 * alpha)


def fade_in(t, a, d=0.25):
    return prog(t, a, a + d)


def bump(t, a, d=0.4):
    """0 -> 1 -> 0 over d seconds starting at a (smooth)."""
    u = prog(t, a, a + d)
    return math.sin(math.pi * u) ** 2


# ------------------------------------------------------------------ 1 · the year
def title40(X, alpha=1.0):
    X.text("40 DAYS", CAP_CX, 560, 220, "green", kind="sans", alpha=alpha, glow=0.3)
    X.text("A YEAR. GONE INTO OUR FEEDS.", CAP_CX, 638, 50, "white", kind="sansm", alpha=alpha)


GBOX = (CAP_CX - 400, 640, 800, 560)          # content box of the grid plane (x, y, w, h)


def grid_plane(X, cam, u, hi, others, pitch, zc, alpha=1.0):
    gx, gy, gw, gh = GBOX

    def draw(Y):
        Y.c.translate(-gx, -gy)
        year_grid(Y, u, alpha=1.0, block_hi=hi, others=others)
    plane(X, cam, tilt_quad(gx + gw / 2, gy + gh / 2, gw, gh, pitch=pitch, z=zc), gw, gh, draw, alpha=alpha)


def scene_year(X, t):
    t_add = 0.3
    u = clamp01((t - t_add) / 1.35)                       # the slivers fly together into 40 whole days
    hi = prog(t, t_add + 1.2, t_add + 1.6)
    t_out = CH("added", 1) - 0.1
    k = smooth(prog(t, t_out, T("look") - 0.1))            # the year tilts away and we fly over it
    cam = Cam(z=lerp(0, 700, k), y=lerp(800, 700, k))
    title40(X, alpha=1 - prog(t, t_out, t_out + 0.5))
    grid_plane(X, cam, u, hi * (1 - k), 1 - 0.7 * k, pitch=lerp(0, 1.15, k), zc=1100 + 300 * k,
               alpha=1 - prog(t, T("look") - 0.9, T("look") - 0.5))
    a = hi * (1 - prog(t, t_out - 0.2, t_out + 0.2))
    if a > 0:
        X.text("= 40 full days, 24 h each", CAP_CX, GRID_Y0 + 2 * GRID_PITCH + 62, 50, "green", kind="sansm", alpha=a)
        X.text("365 days × 2 h 39 min", CAP_CX, GRID_Y0 + 2 * GRID_PITCH + 114, 38, "grey", kind="mono", alpha=a)
    pa = prog(t, T("look") - 0.7, T("look") - 0.2)        # the phone rises out of the dark
    if pa > 0:
        X.c.saveLayerAlpha(None, int(255 * pa))
        phone(X, CAP_CX, 760, scroll=0, clock="23:12", glow=pa)
        X.c.restore()
    source(X, "time", 1 - prog(t, t_out, t_out + 0.4))


# ------------------------------------------------------------------ 2 · the machine behind the glass
RIB_W = PHONE_W - 32 - 28
RIB_X = CAP_CX - RIB_W / 2
PH_CY = 760
FEED_TOP = PH_CY - PHONE_H / 2 + 16 + 70
PBOX = (CAP_CX - 240, PH_CY - 1650, 480, 3300)       # content box of the phone plane


def flick_scroll(t, t0, every=0.62, dist=CARD_H + CARD_GAP):
    if t < t0:
        return 0.0
    n = (t - t0) / every
    k = math.floor(n)
    f = n - k
    return (k + ease_out(clamp01(f / 0.55), 4)) * dist


ADV = (690, 560)
META = (690, 1040)


def scene_machine(X, t):
    t_look = T("look")
    k = smooth(prog(t, t_look + 0.05, t_look + 1.6))
    scroll = flick_scroll(t, t_look - 0.2)
    ext = prog(t, t_look + 0.3, t_look + 1.3)
    cam = Cam(z=lerp(0, -650, k))
    px, py, pw, ph = PBOX

    def draw(Y):
        Y.c.translate(-px, -py)
        if ext > 0:
            feed(Y, RIB_X, FEED_TOP, RIB_W, scroll, i0=-14, i1=60, alpha=0.6 * ext)
        phone(Y, CAP_CX, PH_CY, scroll=scroll, clock="23:12", glow=1.0)
    corners = tilt_quad(lerp(CAP_CX, 250, k), PH_CY, pw, ph, yaw=lerp(0, 0.62, k), pitch=lerp(0, -0.12, k), z=1100)
    plane(X, cam, corners, pw, ph, draw)
    quad = [cam.p(*c)[:2] for c in corners]
    m = quad_matrix(pw, ph, quad)
    mm = prog(t, t_look + 1.1, t_look + 1.7)
    if mm > 0 and m is not None:
        # every ad slot that passes is wired to the buyers; the money flows on to Meta
        step = CARD_H + CARD_GAP
        paths = []
        for i in range(-14, 60):
            if not is_ad(i):
                continue
            yc = FEED_TOP + i * step - scroll + CARD_H / 2
            if not (PH_CY - 1500 < yc < PH_CY + 1500):
                continue
            p = m.mapXY(RIB_X + RIB_W - px, yc - py)
            if not (300 < p.fY < 1180):
                continue
            inside = PH_CY - PHONE_H / 2 < yc < PH_CY + PHONE_H / 2
            pts = bezier((p.fX, p.fY), (p.fX + 120, p.fY), (ADV[0] - 260, ADV[1] + 40), (ADV[0] - 190, ADV[1]))
            X.c.drawPath(_poly(pts), X.paint("magenta", (0.55 if inside else 0.22) * mm, stroke=2.5))
            if inside:
                paths.append(pts)
        streams(X, paths, t, "magenta", n=3, speed=0.9, r=6, alpha=mm, seed=2)
        a = mm
        X.neon_rect(ADV[0] - 190, ADV[1] - 100, 380, 200, "magenta", width=4, r=20, glow=0.5, fill=0xFF12040C,
                    fill_alpha=0.95, alpha=a)
        kin_text(X, "ADVERTISERS", ADV[0], ADV[1] - 6, 54, t_look + 1.2, "white", kind="sans", dur=0.45)
        kin_text(X, "buy the slots", ADV[0], ADV[1] + 58, 46, t_look + 1.4, "magenta", kind="sansm", dur=0.4)
        mp = [(ADV[0], ADV[1] + 104), (META[0], META[1] - 134)]
        X.arrow(mp, "magenta", u=prog(t, t_look + 1.5, t_look + 2.0), width=6, head=26, alpha=a)
        streams(X, [mp], t, "magenta", n=4, speed=0.7, r=8, alpha=a * prog(t, t_look + 2.0, t_look + 2.3), seed=5)
        X.neon_rect(META[0] - 190, META[1] - 130, 380, 260, "magenta", width=4, r=20, glow=0.7, fill=0xFF12040C,
                    fill_alpha=0.95, alpha=a)
        kin_text(X, "META", META[0], META[1] - 50, 84, t_look + 1.6, "white", kind="sans", dur=0.4)
        kin_text(X, "$196 B", META[0], META[1] + 34, 76, t_look + 1.8, "magenta", kind="sans", dur=0.5, glow=0.4)
        kin_text(X, "from ads, 2025", META[0], META[1] + 92, 40, t_look + 2.0, "grey", kind="sansm", dur=0.4)
        if t >= CH("slot", 1):
            kin_text(X, "+12 % ads shown", META[0], META[1] + 196, 56, CH("slot", 1), "white", kind="sans", dur=0.5)
            kin_text(X, "in one year", META[0], META[1] + 246, 40, CH("slot", 1) + 0.2, "grey", kind="sansm", dur=0.4)
        X.text("illustration · ads shown 1 card in 4", 80, 440, 26, "grey", kind="mono", align="left", alpha=a)
        g = fade_in(t, t_look + 1.3)
        X.text("OUR TIME", 250, 1140, 46, "green", kind="sans", alpha=g)
        X.text("goes in here", 250, 1182, 32, "grey", kind="sansm", alpha=g)
    source(X, "meta", mm)


def _poly(pts):
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    return p


# ------------------------------------------------------------------ 3 · the eye swallows the camera
def _q_index(words, phrase):
    w = " ".join(words).split(" ")
    p = phrase.split(" ")
    for i in range(len(w) - len(p) + 1):
        if [x.strip(",.“”") for x in w[i:i + len(p)]] == p:
            return (i, i + len(p) - 1)
    raise ValueError(phrase)


Q1 = ["“...significantly determined by our success in adding, retaining, and engaging active users...”"]
Q2 = ["“...if our users decrease their level of engagement with our products, our revenue, financial results, "
      "and business may be significantly harmed.”"]
Q1_HI = _q_index(Q1, "engaging active users")
Q2_HI = [_q_index(Q2, "if our users decrease their level of engagement"), _q_index(Q2, "may be significantly harmed")]
DBOX = (70, 410, 830, 770)


def doc_page(X, t, alpha):
    x0, y0 = DBOX[0], DBOX[1]
    X.panel(x0, y0, DBOX[2], DBOX[3], alpha=0.97 * alpha, r=16, border="cyan", border_alpha=0.4)
    X.text("META PLATFORMS, INC.", 110, 478, 34, "cyan", kind="mono", align="left", alpha=alpha)
    X.text("ANNUAL REPORT (FORM 10-K) · 2025", 110, 520, 30, "grey", kind="mono", align="left", alpha=alpha)
    t_warn = T("warn")
    sw = prog(t, t_warn - 0.3, t_warn)
    X.text("our financial performance:", 110, 578, 30, "grey", kind="mono", align="left", alpha=alpha * (1 - sw))
    X.text("risk factors:", 110, 578, 30, "grey", kind="mono", align="left", alpha=alpha * sw)
    sc = ease_io5(prog(t, t_warn - 0.3, t_warn + 0.5))
    X.c.save()
    X.c.clipRect(skia.Rect(70, 600, 900, 1176))
    yy = 680 - 450 * sc
    u1 = clamp01((t - CH("name", 1)) / 0.8)
    y1 = doc_lines(X, Q1, 110, yy, size=50, hi=[Q1_HI], hi_u=[u1], alpha=alpha * (1 - 0.6 * sc), maxw=750)
    if t >= CH("name", 2) - 0.05 and sc < 0.5:
        kin_text(X, "= US.", 860, y1 + 34, 110, CH("name", 2) - 0.05, "green", kind="sans", align="right", dur=0.35,
                 glow=0.5, alpha=1 - 2 * sc, rise=40)
    u2 = clamp01((t - CH("warn", 1)) / 0.9)
    u3 = clamp01((t - CH("warn", 2)) / 1.4)
    doc_lines(X, Q2, 110, y1 + 170, size=48, hi=Q2_HI, hi_u=[u2, u3], alpha=alpha * (0.35 + 0.65 * sc), maxw=750)
    X.c.restore()


_TUN = np.random.default_rng(21)
TUNNEL = [(_TUN.uniform(-900, 900), _TUN.uniform(-1100, 1100), _TUN.uniform(0, 1), int(_TUN.integers(0, 10)))
          for _ in range(260)]


def tunnel(X, t, t0, alpha):
    """Digits rushing past the camera: we are inside the numbers."""
    cam = Cam(cx=CAP_CX, cy=790, x=0, y=0)
    for (x, y, ph, d) in TUNNEL:
        z = 60 + ((ph - (t - t0) * 0.9) % 1.0) * 4200
        sx, sy, k = cam.p(x, y, z)
        if not (-100 < sx < W + 100 and 150 < sy < 1500):
            continue
        a = alpha * clamp01((4200 - z) / 1500) * clamp01((z - 60) / 300) * 0.8
        size = min(260, 70 * k)
        X.text(str(d), sx, sy, size, "green", kind="mono", alpha=a)


def scene_eye(X, t):
    t0 = T("name") - 0.2
    t_px = T("name") + 0.75                 # the eye starts to break into pixels
    t_dive = T("name") + 1.25               # the camera falls into the pupil
    t_in = T("name") + 2.0                  # inside: digits rush past
    t_doc = CH("name", 1) - 0.75            # the report flies in from the depth
    if t < t_in + 0.4:
        block = 1 + 40 * ease_in_out(prog(t, t_px, t_in))
        z = 1 + 9 * ease_io5(prog(t, t_dive, t_in + 0.4))
        a = 1 - prog(t, t_in, t_in + 0.4)
        open_ = ease_out(prog(t, t0, t0 + 0.6))

        def draw(Y):
            Y.c.save()
            Y.c.translate(CAP_CX, 760)
            Y.c.scale(z, z)
            Y.c.translate(-CAP_CX, -760)
            Y.c.drawCircle(CAP_CX, 760, 520, Y.paint(0xFF9FC4FF, 0.06, blur=80))
            eye(Y, CAP_CX, 760, 1.25, lid=lerp(0.12, 1.0, open_))
            Y.c.restore()
        X.c.saveLayerAlpha(None, int(255 * a))
        if block > 1.5:
            img = offscreen(X, lambda Y: pixelated(Y, draw, block))
            glitch(X, img, 0.55 * prog(t, t_px, t_dive + 0.2) * (1 - prog(t, t_in - 0.2, t_in + 0.2)), t, seed=3)
        else:
            draw(X)
        X.c.restore()
    ta = prog(t, t_dive + 0.2, t_in) * (1 - prog(t, t_doc + 0.6, t_doc + 1.1))
    if ta > 0:
        X.c.save()
        X.c.clipRect(skia.Rect(0, 400, W, 1220))
        tunnel(X, t, t_dive, ta)
        X.c.restore()
    if t >= t_doc - 0.05:
        k = smooth(prog(t, t_doc, t_doc + 0.75))
        cam = Cam()
        bx, by, bw, bh = DBOX

        def draw_doc(Y):
            Y.c.translate(-bx, -by)
            doc_page(Y, t, 1.0)
        plane(X, cam, tilt_quad(bx + bw / 2, by + bh / 2, bw, bh, yaw=lerp(0.9, 0, k), pitch=lerp(-0.35, 0, k),
                                z=lerp(4200, 1100, k)), bw, bh, draw_doc, alpha=prog(t, t_doc, t_doc + 0.3))
    source(X, "10k", prog(t, t_doc + 0.5, t_doc + 0.8))


# ------------------------------------------------------------------ 4 · one person, then billions
def person(X, x, y, r, color="green", alpha=1.0):
    X.c.drawCircle(x, y - r * 1.25, r * 0.55, X.paint(color, alpha))
    X.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - r * 0.9, y - r * 0.55, x + r * 0.9, y + r * 0.9), r * 0.6,
                                        r * 0.6), X.paint(color, alpha))


FBOX = 2400.0                                   # size of the crowd plane's content box


def crowd(Y, lz, a_scene):
    """Lattices of people at successive powers of ten (a seamless zoom out), centred in the FBOX box."""
    c0 = FBOX / 2
    d0 = 260.0
    for lvl in range(0, 6):
        dd = d0 * 10 ** (lvl - lz / 2.0)
        if dd < 4 or dd > 2000:
            continue
        a = clamp01((dd - 4) / 12) * clamp01((900 - dd) / 600) * a_scene
        r = max(1.2, dd * 0.18)
        n = int(min(90, 1150 / dd)) + 1
        for iy in range(-n, n + 1):
            for ix in range(-n, n + 1):
                xx, yy = c0 + ix * dd, c0 + iy * dd
                fall = clamp01(1 - math.hypot(ix * dd, iy * dd) / 1150)
                if fall <= 0:
                    continue
                if r > 6:
                    person(Y, xx, yy, r, "green", a * fall)
                else:
                    Y.c.drawCircle(xx, yy, r, Y.paint("green", a * fall))


def scene_money(X, t):
    t_d = T("dollar")
    t_x = T("times") - 0.1
    t_b = T("times") + 1.3
    t_y = t_b + 0.15                  # the total lands right after "billion" and holds
    k = ease_in_out(prog(t, t_x, t_b))
    lz = lerp(0.0, 9.55, k)
    tilt = smooth(prog(t, t_x + 0.2, t_b + 0.3))
    a_scene = 1 - 0.8 * prog(t, t_y + 0.1, t_y + 0.6)
    if t >= t_x:
        cam = Cam(z=lerp(0, -300, tilt), y=lerp(800, 900, tilt))

        def draw(Y):
            crowd(Y, lz, a_scene)
        X.c.save()
        X.c.clipRect(skia.Rect(0, 560, W, 1200))
        plane(X, cam, tilt_quad(CAP_CX, 800, FBOX, FBOX, pitch=lerp(0, 1.12, tilt), z=1100), FBOX, FBOX, draw)
        X.c.restore()
        # the money rises out of the crowd into one point
        mr = prog(t, t_y - 0.4, t_y + 0.4) * (1 - prog(t, t_y + 1.4, t_y + 2.0))
        if mr > 0:
            rr = np.random.default_rng(8)
            paths = []
            for _ in range(26):
                sx, sy = rr.uniform(120, 860), rr.uniform(880, 1160)
                paths.append(bezier((sx, sy), (sx, sy - 200), (CAP_CX, 760), (CAP_CX, 690), 16))
            streams(X, paths, t, "magenta", n=2, speed=1.1, r=5, alpha=mr, seed=4)
    if lz < 0.25:
        a = fade_in(t, t_d - 0.1, 0.3)
        cy = 800
        person(X, CAP_CX, cy, 50, "green", a)
        kin_text(X, "16¢", CAP_CX, cy - 196, 170, CH("dollar", 1) - 0.05, "magenta", kind="sans", dur=0.4, glow=0.4)
        kin_text(X, "a day, to Meta", CAP_CX, cy - 126, 46, CH("dollar", 1) + 0.15, "white", kind="sansm", dur=0.4)
        X.text("revenue per daily user: $57 in 2025", CAP_CX, cy + 160, 38, "grey", kind="mono",
               alpha=fade_in(t, CH("dollar", 1) + 0.4))
        X.text("worldwide average", CAP_CX, cy + 206, 34, "grey", kind="mono", alpha=fade_in(t, CH("dollar", 1) + 0.4))
    if t >= t_x:
        n = 10 ** min(lz, math.log10(3.58e9))
        if t >= t_b:
            n = 3.58e9
        s = f"× {int(round(n)):,}" if n < 3.5e9 else "× 3,580,000,000"
        X.text(s, CAP_CX, 486, 76, "white", kind="mono", alpha=fade_in(t, t_x) * a_scene)
        X.text("daily users, Dec 2025", CAP_CX, 540, 36, "grey", kind="mono", alpha=fade_in(t, t_x) * a_scene)
    if t >= t_y - 0.1:
        a = fade_in(t, t_y - 0.1, 0.35)
        X.c.drawCircle(CAP_CX, 690, 240, X.paint(0xFF000000, 0.75 * a, blur=60))
        kin_text(X, "$201 B", CAP_CX, 760, 220, t_y - 0.1, "magenta", kind="sans", dur=0.5, glow=0.5, track0=0.6)
        kin_text(X, "Meta's revenue in 2025", CAP_CX, 840, 46, t_y + 0.15, "white", kind="sansm", dur=0.45)
    source(X, "meta")


# ------------------------------------------------------------------ 5 · no last page
def clock_at(t):
    t0, t1 = T("nolast") - 0.2, CH("nolast", 1) + 0.5
    u = clamp01((t - t0) / (t1 - t0)) ** 1.7
    m = int(23 * 60 + 12 + u * 155)
    return f"{(m // 60) % 24:02d}:{m % 60:02d}"


def scene_night(X, t):
    t0 = T("nolast") - 0.2
    t_stop = CH("nolast", 1) + 0.5
    tt = min(t, t_stop)
    u = clamp01((tt - t0) / (t_stop - t0))
    sp = (CARD_H + CARD_GAP) / 0.55 * (tt - t0) * (1 + 1.6 * u)        # faster and faster
    n_cards = 6 + sp / (CARD_H + CARD_GAP)
    clk = clock_at(t)
    last = prog(t, CH("nolast", 1) - 0.1, CH("nolast", 1) + 0.6)

    def content(Y, rect):
        sx0, sy0, sx1, sy1 = rect
        feed(Y, sx0 + 14, sy0 + 70, sx1 - sx0 - 28, sp, i0=-2, i1=int(n_cards) + 8)
        Y.c.drawRect(skia.Rect(sx0, sy0, sx1, sy0 + 58), Y.paint(0xFF07090D, 0.92))
        Y.text(clk, sx0 + 40, sy0 + 42, 30, "white", kind="sansm", align="left")
        if last > 0:
            Y.c.drawRect(skia.Rect(sx0, sy0, sx1, sy1), Y.paint(0xFF020306, last))
            Y.text(clk, (sx0 + sx1) / 2, (sy0 + sy1) / 2 + 30, 120, "white", kind="sans", alpha=last)
            Y.text("night's over", (sx0 + sx1) / 2, (sy0 + sy1) / 2 + 100, 34, "grey", kind="mono", alpha=last)
    k = smooth(prog(t, t0, t_stop + 0.6))
    cam = Cam(z=lerp(-250, 120, k))                                      # a slow dolly towards the screen
    px, py, pw, ph = (380 - 220, 760 - 420, 440, 840)

    def draw(Y):
        Y.c.translate(-px, -py)
        phone(Y, 380, 760, content=content, glow=1.0)
    plane(X, cam, tilt_quad(380, 760, pw, ph, yaw=lerp(-0.32, -0.12, k), pitch=0.05, z=1100), pw, ph, draw)
    X.text(clk, 892, 560, 88, "white", kind="mono", align="right", alpha=1 - last)
    X.text("illustration", 892, 690, 26, "grey", kind="mono", align="right", alpha=1 - last)
    if t < CH("nolast", 1):
        X.text("no end", 892, 624, 44, "grey", kind="mono", align="right", alpha=fade_in(t, CH("nolast", 0) + 0.8))


# ------------------------------------------------------------------ 6 · the study, and its limit
def ring(X, cx, cy, r, u0, u1, color, width=34, alpha=1.0):
    if u1 <= u0:
        return
    p = skia.Path()
    p.addArc(skia.Rect(cx - r, cy - r, cx + r, cy + r), -90 + 360 * u0, 360 * (u1 - u0))
    X.c.drawPath(p, X.paint(color, alpha, stroke=width, cap_round=False))


def scene_study(X, t):
    t0 = T("study")
    drift = 14 * math.sin((t - t0) * 0.6)
    tag(X, "THE STUDY", 110, 456, "cyan", alpha=fade_in(t, t0 - 0.2))
    n = 45202 * ease_out(prog(t, t0 + 0.5, t0 + 1.6), 3)
    count(X, n, 110 + drift * 0.3, 596, 132, "white", align="left", alpha=fade_in(t, t0 + 0.4))
    X.text("students, aged 18–28, Norway", 110, 656, 42, "grey", kind="sansm", align="left", alpha=fade_in(t, t0 + 1.0))
    cx, cy, r = 320 + drift, 930, 150
    a1 = fade_in(t, CH("study", 1) - 0.1)
    if a1 > 0:
        X.c.drawCircle(cx, cy, r, X.paint(0xFF1A2030, a1, stroke=34))
        ring(X, cx, cy, r, 0, ease_in_out(prog(t, CH("study", 1), CH("study", 1) + 1.3)), "cyan", alpha=a1)
        X.text("+1 h", cx, cy + 22, 74, "cyan", kind="sans", alpha=a1)
        kin_text(X, "screen in bed", 560 - drift * 0.5, 890, 44, CH("study", 1), "cyan", kind="sansm", align="left",
                 dur=0.4)
    a2 = fade_in(t, CH("study", 2) - 0.05)
    if a2 > 0:
        ring(X, cx, cy, r + 2, 0, ease_in_out(prog(t, CH("study", 2), CH("study", 2) + 1.1)) * 0.4, "magenta",
             width=40, alpha=a2)
        kin_text(X, "−24 min", 560 - drift * 0.5, 990, 78, CH("study", 2), "magenta", kind="sans", align="left",
                 dur=0.4, glow=0.3)
        X.text("of sleep, on average", 560 - drift * 0.5, 1040, 40, "white", kind="sansm", align="left", alpha=a2)
    X.text("any screen use, not only social media", 80, 1170, 30, "grey", kind="mono", align="left",
           alpha=fade_in(t, CH("study", 2) + 0.5))
    source(X, "sleep")


def scene_check(X, t):
    t0 = T("check")
    tag(X, "CHECK THE CLAIM", 110, 456, "green", alpha=fade_in(t, t0 - 0.2))
    a = fade_in(t, t0 - 0.15)
    for (lab, y) in (("SCREEN IN BED", 620), ("BAD SLEEP", 960)):
        X.neon_rect(190, y - 70, 590, 130, "white", width=3, r=18, glow=0.0, fill=0xFF0C0F18, fill_alpha=0.95, alpha=a)
        X.text(lab, CAP_CX, y + 18, 62, "white", kind="sans", alpha=a)
    X.arrow([(400, 692), (400, 880)], "white", u=prog(t, t0, t0 + 0.4), width=6, head=24, alpha=a)
    X.arrow([(570, 880), (570, 692)], "green", u=prog(t, t0 + 0.5, t0 + 0.9), width=6, head=24)
    X.text("causes?", 380, 800, 42, "grey", kind="sansm", align="right", alpha=prog(t, t0 + 0.3, t0 + 0.6))
    X.text("or the reverse:", 600, 784, 40, "green", kind="sansm", align="left", alpha=prog(t, t0 + 0.8, t0 + 1.1))
    X.text("tired people", 600, 828, 40, "green", kind="sansm", align="left", alpha=prog(t, t0 + 0.9, t0 + 1.2))
    X.text("may scroll more", 600, 872, 40, "green", kind="sansm", align="left", alpha=prog(t, t0 + 1.0, t0 + 1.3))
    X.text("the authors say it can't show cause", CAP_CX, 1124, 34, "grey", kind="mono", alpha=fade_in(t, t0 + 1.1))
    source(X, "sleep")


# ------------------------------------------------------------------ 7 · the rules are written somewhere
def scene_eu(X, t):
    t0 = T("eu")
    a = fade_in(t, t0 - 0.2)
    k = smooth(prog(t, t0 - 0.2, t0 + 0.6))
    cam = Cam()
    bx, by, bw, bh = (90, 420, 790, 540)

    def draw(Y):
        Y.c.translate(-bx, -by)
        Y.panel(90, 420, 790, 540, alpha=0.96, border="cyan", border_alpha=0.4)
        Y.text("EUROPEAN COMMISSION", 130, 490, 40, "cyan", kind="mono", align="left")
        Y.text("6 February 2026 · preliminary findings", 130, 538, 32, "grey", kind="mono", align="left")
        b = fade_in(t, CH("eu", 1) - 0.1)
        Y.text("TikTok's design:", 130, 620, 44, "white", kind="sansm", align="left", alpha=b)
        for i, s in enumerate(["infinite scroll", "autoplay", "push notifications"]):
            Y.text("— " + s, 150, 690 + i * 60, 46, "white" if i else "cyan", kind="sansm", align="left",
                   alpha=fade_in(t, CH("eu", 1) + i * 0.15))
        c = fade_in(t, CH("eu", 1) + 1.0)
        Y.text("may breach the Digital", 130, 884, 46, "cyan", kind="sans", align="left", alpha=c)
        Y.text("Services Act · not a final decision", 130, 930, 38, "grey", kind="sansm", align="left", alpha=c)
    plane(X, cam, tilt_quad(bx + bw / 2, by + bh / 2, bw, bh, yaw=lerp(-0.6, 0, k), z=lerp(2600, 1100, k)), bw, bh,
          draw, alpha=a)
    X.text("TikTok disputes the findings", CAP_CX, 1030, 34, "grey", kind="mono", alpha=fade_in(t, CH("eu", 1) + 1.3))
    source(X, "eu")


def scene_design(X, t):
    t0 = T("design")
    X.panel(110, 520, 750, 330, alpha=0.96, border="green", border_alpha=0.35)
    X.text("illustration", 140, 572, 28, "grey", kind="mono", align="left")
    typed_mono(X, "feed.settings", 140, 640, 44, t0 - 0.35, cps=40, color="grey", cursor=False)
    typed_mono(X, "infinite_scroll = ", 140, 730, 52, t0 - 0.1, cps=40, color="white", cursor=False)
    xw = 140 + X.width("infinite_scroll = ", 52, "mono")
    v = prog(t, t0 + 0.55, t0 + 0.9)
    X.text("true", xw, 730, 52, "magenta", kind="mono", align="left", alpha=fade_in(t, t0 + 0.4, 0.15) * (1 - v))
    X.text("false", xw, 730, 52, "green", kind="mono", align="left", alpha=v, glow=0.4 * v)
    X.c.drawRect(skia.Rect(xw, 748, xw + X.width("false", 52, "mono") * v, 752), X.paint("green", v))
    kin_text(X, "A DESIGN CHOICE.", CAP_CX, 990, 88, t0 + 0.6, "white", kind="sans", dur=0.45, glow=0.15)
    X.text("someone wrote it. someone can change it.", CAP_CX, 1060, 32, "grey", kind="mono", alpha=fade_in(t, t0 + 1.1))


# ------------------------------------------------------------------ 8 · built the other way: the commons
_NR = np.random.default_rng(31)
NODES = []
for _ in range(70):
    th, ph = _NR.uniform(0, 2 * math.pi), math.acos(_NR.uniform(-1, 1))
    rad = _NR.uniform(250, 380)
    NODES.append((rad * math.sin(ph) * math.cos(th), rad * math.cos(ph) * 0.9, rad * math.sin(ph) * math.sin(th)))
SERVERS = []
for i in range(9):
    th = i / 9 * 2 * math.pi
    SERVERS.append((300 * math.cos(th), 120 * math.sin(th * 2), 300 * math.sin(th)))
HOME = [min(range(9), key=lambda j: math.dist(n, SERVERS[j])) for n in NODES]
FED = [(i, j) for i in range(9) for j in range(i + 1, 9) if (j - i) in (1, 2, 4)]


def net_points(t, yaw, cam_z, cx=CAP_CX, cy=780):
    cam = Cam(cx=cx, cy=cy, x=0, y=0, z=cam_z)
    cs, sn = math.cos(yaw), math.sin(yaw)

    def P(p):
        x, y, z = p
        return cam.p(x * cs + z * sn, y, -x * sn + z * cs + 1100)
    return P


def scene_net(X, t):
    t0 = T("other")
    t_flip = CH("other", 0) + 0.9                  # "...the other way": the centre lets go
    k = smooth(prog(t, t_flip, t_flip + 1.4))
    yaw = (t - t0) * 0.32
    P = net_points(t, yaw, lerp(-150, -350, smooth(prog(t, T("commons"), T("commons") + 2.5))))
    hub = (0, 0, 0)
    hp_ = P(hub)
    # links
    for i, n in enumerate(NODES):
        a = P(n)
        s = P(SERVERS[HOME[i]])
        if k < 1:
            X.c.drawLine(a[0], a[1], hp_[0], hp_[1], X.paint("magenta", 0.32 * (1 - k), stroke=2))
        if k > 0:
            X.c.drawLine(a[0], a[1], s[0], s[1], X.paint("green", 0.35 * k, stroke=2))
    if k > 0:
        for (i, j) in FED:
            a, b = P(SERVERS[i]), P(SERVERS[j])
            X.c.drawLine(a[0], a[1], b[0], b[1], X.paint("cyan", 0.4 * k, stroke=2.5))
    # flows: before, everything drains into the centre; after, it moves between equals
    if k < 0.9:
        paths = [[P(n)[:2], hp_[:2]] for n in NODES[::3]]
        streams(X, paths, t, "magenta", n=1, speed=0.8, r=5, alpha=(1 - k), seed=6, trail=4)
    if k > 0.2:
        paths = [[P(SERVERS[i])[:2], P(SERVERS[j])[:2]] for (i, j) in FED]
        streams(X, paths, t, "green", n=1, speed=0.5, r=5, alpha=k, seed=7, trail=4)
    # nodes, far first
    pts = sorted([(P(n), "white", 9) for n in NODES] + [(P(s), "green", 16 + 6 * k) for s in SERVERS],
                 key=lambda q: q[0][2])
    for (sx, sy, sc), colr, r in pts:
        X.c.drawCircle(sx, sy, r * sc, X.paint(colr, 0.9 if colr == "green" and k > 0.3 else 0.75))
        if colr == "green" and k > 0.3:
            X.c.drawCircle(sx, sy, r * sc * 2.2, X.paint("green", 0.25 * k, blur=10))
    if k < 1:
        X.c.drawCircle(hp_[0], hp_[1], 60 * hp_[2] * (1 - k) + 1, X.paint("magenta", 0.95 * (1 - k)))
        X.c.drawCircle(hp_[0], hp_[1], 120 * hp_[2] * (1 - k) + 1, X.paint("magenta", 0.3 * (1 - k), blur=20))
        X.text("ONE OWNER", hp_[0], hp_[1] - 90, 44, "white", kind="sans", alpha=(1 - k) * fade_in(t, t0 - 0.1))
    X.text("illustration", 80, 420, 26, "grey", kind="mono", align="left", alpha=fade_in(t, t0 - 0.1))
    kin_text(X, "NO ADS", CAP_CX, 520, 96, CH("other", 1) - 0.05, "green", kind="sans", dur=0.4, glow=0.3,
             out_t=T("commons") - 0.3)
    X.text("by design", CAP_CX, 566, 32, "grey", kind="mono",
           alpha=fade_in(t, CH("other", 1) + 0.3) * (1 - prog(t, T("commons") - 0.3, T("commons"))))
    kin_text(X, "NO SINGLE OWNER", CAP_CX, 1100, 66, CH("other", 2) - 0.05, "white", kind="sans", dur=0.45,
             out_t=T("commons") - 0.3)
    X.text("independent servers, one open standard", CAP_CX, 1160, 30, "grey", kind="mono",
           alpha=fade_in(t, CH("other", 2) + 0.3) * (1 - prog(t, T("commons") - 0.3, T("commons"))))
    kin_text(X, "COMMONS", CAP_CX, 540, 150, CH("commons", 1) - 0.1, "green", kind="sans", dur=0.6, glow=0.5,
             track0=0.8)
    X.text("what we run together, for ourselves", CAP_CX, 1120, 34, "grey", kind="mono",
           alpha=fade_in(t, CH("commons", 1) + 0.4))
    source(X, "masto", fade_in(t, t0 - 0.1))


# ------------------------------------------------------------------ 9 · step one
def scene_step(X, t):
    t0 = T("step")
    tag(X, "STEP ONE · TONIGHT", 110, 456, "green", alpha=fade_in(t, t0 - 0.2))
    a = fade_in(t, t0 - 0.1)
    c = X.c
    k0 = smooth(prog(t, t0 - 0.2, nxt("step")))
    c.save()
    c.translate(CAP_CX, 1000)
    c.scale(lerp(0.96, 1.05, k0), lerp(0.96, 1.05, k0))           # a slow push in
    c.translate(-CAP_CX, -1000)
    wall = X.paint(0xFF2A3040, a, stroke=4)
    c.drawLine(90, 1120, 880, 1120, wall)
    door_x = 700
    c.drawRect(skia.Rect(door_x, 600, door_x + 160, 1120), wall)
    close = ease_in_out(prog(t, CH("step", 1) + 1.15, CH("step", 1) + 1.6))
    dp = skia.Path()
    dw = 160 * lerp(0.25, 1.0, close)
    dp.addRect(skia.Rect(door_x, 600, door_x + dw, 1120))
    c.drawPath(dp, X.paint(0xFF12161F, a))
    c.drawPath(dp, X.paint(0xFF3A4458, a, stroke=3))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(110, 980, 520, 1120), 18, 18), X.paint(0xFF141A26, a))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(110, 940, 230, 1000), 22, 22), X.paint(0xFF2A3346, a))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(110, 980, 520, 1120), 18, 18), X.paint(0xFF2A3040, a, stroke=4))
    c.drawRect(skia.Rect(540, 1010, 650, 1120), X.paint(0xFF141A26, a))
    c.drawRect(skia.Rect(540, 1010, 650, 1120), X.paint(0xFF2A3040, a, stroke=4))
    ca = fade_in(t, CH("step", 1) + 1.5, 0.4)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(552, 950, 640, 1006), 10, 10), X.paint(0xFF0A0C11, ca))
    X.text("07:00", 596, 990, 34, "amber", kind="mono", alpha=ca, glow=0.6)
    k = ease_in_out(prog(t, CH("step", 1), CH("step", 1) + 1.2))
    px = lerp(330, door_x + 240, k)
    py = lerp(940, 860, k) - math.sin(math.pi * k) * 120
    if px < door_x + 160 or close < 0.9:
        c.save()
        if k > 0.6:
            c.clipRect(skia.Rect(0, 0, door_x + dw + 2, H))
        c.translate(px, py)
        c.rotate(lerp(-8, 10, k))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-34, -64, 34, 64), 12, 12), X.paint(0xFF9FC4FF, 0.25 * a, blur=22))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-34, -64, 34, 64), 12, 12), X.paint(0xFF0A0C11, a))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-28, -56, 28, 56), 8, 8), X.paint(0xFF6F8BC0, a))
        c.restore()
    c.restore()
    X.text("out of reach, it can't pull you back", CAP_CX, 566, 38, "grey", kind="sansm",
           alpha=fade_in(t, CH("step", 1) + 1.6))
    X.text("an old alarm clock", 596, 920, 30, "amber", kind="sansm", alpha=fade_in(t, CH("step", 1) + 1.7))


# ------------------------------------------------------------------ 10 · stop scrolling, go to sleep
STARS = [(x, y, r_, a_) for x, y, r_, a_ in zip(*[np.random.default_rng(3).uniform(lo, hi, 40) for lo, hi in
                                                    ((60, 900), (380, 1120), (1.2, 2.6), (0.25, 0.7))])]


def scene_stop(X, t):
    t0 = T("stop")
    on = 1 - ease_in_out(prog(t, t0 + 0.1, CH("stop", 1) + 0.5))       # slow dimming, never a flash
    sc = flick_scroll(min(t, t0 + 0.2), t0 - 2.0, every=0.9)
    phone(X, CAP_CX, 700, scroll=sc, clock="01:47", screen_on=on, glow=on)
    s = prog(t, CH("stop", 1) + 0.3, CH("stop", 1) + 1.0)
    for (x, y, r_, a_) in STARS:
        X.c.drawCircle(x, y, r_, X.paint("white", s * a_))


def scene_world(X, t):
    t0 = T("world") - 0.25
    a = ease_in_out(prog(t, t0, t0 + 1.2))
    for (x, y, r_, a_) in STARS:
        X.c.drawCircle(x, y, r_, X.paint("white", (1 - a * 0.6) * a_))
    # the servers of the commons drift in and settle into Relay's three nodes
    k = smooth(prog(t, t0, T("sign")))
    tgt = [(0, -62), (-76, 70), (76, 70)]
    s = 0.62
    rr = np.random.default_rng(12)
    for i in range(9):
        sx, sy = rr.uniform(120, 860), rr.uniform(420, 1100)
        tx, ty = tgt[i % 3]
        x = lerp(sx, CAP_CX + tx * s, k)
        y = lerp(sy, 760 + ty * s, k)
        X.c.drawCircle(x, y, 10, X.paint("green", (1 - prog(t, T("sign") - 0.4, T("sign"))) * 0.9))
        X.c.drawCircle(x, y, 24, X.paint("green", 0.25 * (1 - prog(t, T("sign") - 0.4, T("sign"))), blur=8))
    relay(X, CAP_CX, 760, s, alpha=prog(t, T("sign") - 0.9, T("sign") - 0.1), rim=0.6)
    sa = prog(t, T("sign") - 0.05, T("sign") + 0.3)
    if sa > 0:
        X.panel(110, 1190, 750, 200, alpha=0.8 * sa, border=None)
        kin_text(X, "build the commons.", CAP_CX, 1290, 64, T("sign") - 0.05, "green", kind="sign", dur=0.7, glow=0.5,
                 track0=0.5)
        X.text("THE EXIT MANUAL", CAP_CX, 1358, 40, "white", kind="sansm", alpha=0.8 * prog(t, T("sign") + 0.3,
                                                                                            T("sign") + 0.6))


# ------------------------------------------------------------------ 11 · loop (ends on frame 0)
def scene_loop(X, t):
    a = ease_in_out(prog(t, T("loop") - 0.2, T("loop") + 0.8))
    X.c.saveLayerAlpha(None, int(255 * a))
    year_grid(X, 0.0, alpha=1.0)
    X.c.restore()
    title40(X, alpha=ease_in_out(prog(t, E("loop") - 0.45, DURATION - 0.05)))


def scenes():
    return [
        (0.0, T("look") - 0.2, scene_year),
        (T("look") - 0.2, T("name") - 0.2, scene_machine),
        (T("name") - 0.2, T("dollar") - 0.2, scene_eye),
        (T("dollar") - 0.2, T("nolast") - 0.2, scene_money),
        (T("nolast") - 0.2, T("study") - 0.25, scene_night),
        (T("study") - 0.25, T("check") - 0.2, scene_study),
        (T("check") - 0.2, T("eu") - 0.2, scene_check),
        (T("eu") - 0.2, T("design") - 0.2, scene_eu),
        (T("design") - 0.2, T("other") - 0.2, scene_design),
        (T("other") - 0.2, T("step") - 0.2, scene_net),
        (T("step") - 0.2, T("stop") - 0.2, scene_step),
        (T("stop") - 0.2, T("world") - 0.25, scene_stop),
        (T("world") - 0.25, T("loop") - 0.2, scene_world),
        (T("loop") - 0.2, DURATION + 1, scene_loop),
    ]


# short glitch bursts on some cuts (smooth sideways slices, constant brightness)
def cut_glitches():
    return [T("name") - 0.2, T("dollar") - 0.2, T("nolast") - 0.2, T("eu") - 0.2, T("other") - 0.2]


def rain_alpha(t):
    if t < T("stop") - 0.2:
        return 1.0 if t > 0.0 else 1.0
    return 1 - 0.7 * prog(t, T("stop") - 0.2, T("stop") + 1.0) + 0.5 * prog(t, T("loop") - 0.2, T("loop") + 0.8)


_SC = None


def _scene(X, t):
    for a, b, fn in _SC:
        if a <= t < b:
            fn(X, t)
            break


def draw_frame(X, t):
    global _SC
    _SC = _SC or scenes()
    if not isinstance(X, Ctx2):
        X.__class__ = Ctx2
    if not hasattr(X.A, "rain"):
        X.A.__class__ = Assets3
        Assets3.__init__(X.A)
    X.level = level(t)
    X.bg()
    data_rain(X, t, rain_alpha(t))
    g = max([bump(t, c - 0.12, 0.34) for c in cut_glitches()] + [0.0])
    if g > 0.01:
        img = offscreen(X, lambda Y: _scene(Y, t))
        glitch(X, img, 0.45 * g, t, seed=int(t * 3) % 7)
    else:
        _scene(X, t)
    vignette(X)
    hud(X, t, ep=EPISODE, series=SERIES)
    for cap in CAPTIONS:
        cap.draw(X)
    X.finish()


# ------------------------------------------------------------------ sound (exit_audio.py, SCORE = "dark")
SCORE = "dark"
BPM = 50                        # the slow pulse: 50 per minute, like a resting heart in the dark


def music_dips():
    """Lines the score dips under (extra -6 dB): the numbers and the turn."""
    if not TIM:
        return []
    return [(T(i) - 0.1, E(i) + 0.2) for i in ("hook", "name", "warn", "dollar", "times", "study", "other", "commons",
                                                "step", "sign")]


def music_sections():
    """(start, end, state) — state: 'hush' (drone only), 'pulse' (drone + pulse), 'build' (+ textures, rising),
    'void' (almost nothing), 'resolve' (warmer chord for the sign)."""
    return [
        (0.0, T("look") - 0.2, "hush"),
        (T("look") - 0.2, T("nolast") - 0.2, "pulse"),
        (T("nolast") - 0.2, T("study") - 0.25, "void"),
        (T("study") - 0.25, T("other") - 0.2, "pulse"),
        (T("other") - 0.2, T("step") - 0.2, "build"),
        (T("step") - 0.2, T("world") - 0.25, "void"),
        (T("world") - 0.25, T("loop") - 0.2, "resolve"),
        (T("loop") - 0.2, DURATION + 5, "hush"),
    ]


def sfx_list():
    s = [(0.02, "static", 0), (0.3, "sub_drop", 0)]
    s += [(T("look") - 0.25, "whoosh_low", 1), (T("look") + 1.15, "low_hit", 0)]
    for j in range(4):
        s.append((T("look") + 1.7 + j * 0.62 * 2, "data", j))
    for c in cut_glitches():
        s.append((c - 0.12, "static", int(c * 10) % 5))
    s += [
        (T("name") + 0.75, "glitch", 0),
        (T("name") + 1.25, "sub_drop", 1),
        (CH("name", 1) - 0.75, "whoosh_low", 2),
        (CH("name", 2) - 0.05, "low_hit", 1),
        (T("warn"), "data", 5),
        (CH("dollar", 1) - 0.05, "coin", 0),
        (T("times"), "rise", 2),
        (T("times") + 1.45, "sub_drop", 2),
        (CH("nolast", 1) + 0.5, "clunk", 0),
        (T("study") - 0.2, "data", 6),
        (T("design") + 0.55, "data", 7),
        (CH("other", 0) + 0.9, "sub_drop", 3),
        (CH("commons", 1) - 0.1, "low_hit", 2),
        (CH("step", 1) + 1.3, "clunk", 1),
        (T("sign") - 0.05, "low_hit", 3),
        (T("loop") - 0.2, "static", 4),
    ]
    return s


SUBTITLE_EXTRAS = []
EXTRA_KEYS = []
if TIM:
    SUBTITLE_EXTRAS = [(0.0, T("added") - 0.04, "Forty days a year."),
                       (T("sign") - 0.04, T("loop") - 0.04, "build the commons.")]
    EXTRA_KEYS = [0.9, 1.6, round(T("look") - 0.5, 2), round(T("look") + 1.9, 2), round(T("name") + 1.0, 2),
                  round(T("name") + 1.6, 2), round(T("name") + 2.2, 2), round(CH("name", 2) + 0.4, 2),
                  round(CH("warn", 2) + 1.2, 2), round(T("times") + 0.8, 2), round(E("times") + 0.5, 2),
                  round(CH("nolast", 1) + 0.6, 2), round(CH("study", 2) + 1.0, 2), round(T("check") + 1.3, 2),
                  round(CH("eu", 1) + 1.4, 2), round(T("design") + 1.0, 2), round(T("other") + 0.5, 2),
                  round(CH("other", 0) + 1.6, 2), round(CH("commons", 1) + 0.6, 2), round(CH("step", 1) + 1.8, 2),
                  round(CH("stop", 1) + 1.0, 2), round(T("sign") + 0.6, 2)]


def draw_cover(X):
    """Cover: the 40 stacked days and the intercepted header. No person, no logo."""
    if not isinstance(X, Ctx2):
        X.__class__ = Ctx2
    if not hasattr(X.A, "rain"):
        X.A.__class__ = Assets3
        Assets3.__init__(X.A)
    X.t = 0.0
    X.bg()
    data_rain(X, 7.0, 1.4)
    title40(X)
    year_grid(X, 1.0, block_hi=1.0)
    vignette(X)
    hud(X, 0.0, ep=EPISODE, series=SERIES)
    X.text("every hour on our feeds, added up", CAP_CX, 1250, 50, "white", kind="sansm")
    X.text("18 h 36 min a week · DataReportal / GWI, 2026", CAP_CX, 1316, 32, "grey", kind="mono")
    X.finish()
