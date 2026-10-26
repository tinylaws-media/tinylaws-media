"""THE EXIT MANUAL — TRANSMISSION 001 (v2) · EXIT: "Forty days a year."
Demo episode, remade after the owner's direction notes of 25 Oct 2026 (manifesto writing, "mental boom" animation,
natural voice, "stop scrolling, go to sleep").

Facts (checked 25 Oct 2026, primary sources):
- Time: DataReportal / Kepios with GWI, "Digital 2026 Global Overview Report" (Oct 2025): online adults spend on
  average 18 h 36 min a week on social and video platforms (YouTube and TikTok included).
  18.6 h / 7 = 2.66 h a day = 11.07 % of each day; x 52.14 weeks = 970 h = 40.4 days of 24 h a year.
  https://datareportal.com/reports/digital-2026-global-overview-report
- Meta, Form 10-K for fiscal 2025 (filed Jan 2026), verbatim excerpts: "...significantly determined by our success in
  adding, retaining, and engaging active users..." and the risk-factor heading "...if our users decrease their level
  of engagement with our products, our revenue, financial results, and business may be significantly harmed."
  (Review gate: "that deliver ad impressions" qualifies the products, not people; it is NOT used.)
  https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm
- Meta Q4 & full-year 2025 results (28 Jan 2026): revenue $200.97 bn (advertising $196.18 bn); 3.58 bn daily
  active people (Dec 2025); ad impressions +12 % in 2025. Earnings slides: ARPP (revenue per daily active person)
  $12.36 + $13.65 + $14.46 + $16.56 = $57.03 in 2025, i.e. 16 cents a day (worldwide average).
  https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Fourth-Quarter-and-Full-Year-2025-Results-2026.pdf
- Sleep: Hjetland et al., Frontiers in Psychiatry (31 Mar 2025), 45,202 students aged 18-28, Norway (SHoT 2022
  survey): each extra hour of screen use after going to bed = 59 % higher odds of insomnia symptoms and 24 min less
  sleep. "This study cannot determine causality." https://doi.org/10.3389/fpsyt.2025.1548273
- EU: European Commission, 6 Feb 2026, PRELIMINARY findings that TikTok's addictive design (infinite scroll,
  autoplay, push notifications, recommender) breaches the Digital Services Act; TikTok disputes them.
  https://digital-strategy.ec.europa.eu/en/news/commission-preliminarily-finds-tiktoks-addictive-design-breach-digital-services-act
Guardrails: no real person drawn, no brand logo, no organisation imagery (text only), legal action only.
"""
import json
import math
import os

import numpy as np
import skia

from exit_look2 import *
from exit_ep002_lines import LINES, CAPS

EPISODE = "001"
SERIES = "EXIT"
VOICE = "am_fenrir"            # casting v2, take 1 (out/exit_casting.wav)
VOICE_SPEED = 1.0
VOICE_FX = {"semitones": 0, "radio": 0, "warm": 0.5}
START = 0.08

# ------------------------------------------------------------------ timing
_HERE = os.path.dirname(os.path.abspath(__file__))
_TP = os.path.join(_HERE, "out", "exit_ep002_timing.json")
TIM = json.load(open(_TP)) if os.path.exists(_TP) else None
if TIM and [(l[0], " ".join(p.strip() for p in l[1].split("|"))) for l in LINES] != \
        [(k, v["text"]) for k, v in TIM.items() if not k.startswith("_")]:
    TIM = None
DURATION = round(TIM["_end"] + 0.75, 2) if TIM else None


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


CAP_STYLE = {"stop": dict(size=118, y=1180, hi="white"), "warn": dict(hi="magenta"), "times": dict(hi="magenta"),
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
            b = ch[k + 1] - 0.04 if k + 1 < len(blocks) else (DURATION + 1 if lid == "loop" else nxt(lid) - 0.04)
            CAPTIONS.append(Caption2(a, b, txt, **CAP_STYLE.get(lid, {})))

_EP = os.path.join(_HERE, "out", "exit_ep002_voice_env.npy")
VOICE_ENV = np.load(_EP) if os.path.exists(_EP) else None


def level(t):
    if VOICE_ENV is None:
        return 0.0
    i = int(t * FPS)
    return float(VOICE_ENV[i]) if 0 <= i < len(VOICE_ENV) else 0.0


# ------------------------------------------------------------------ shared pieces
SRC = {
    "time": "source: DataReportal / GWI survey, Digital 2026 (Oct 2025)",
    "meta": "source: Meta, Q4 & full-year 2025 results (Jan 2026)",
    "10k": "source: Meta, annual report (Form 10-K) for 2025",
    "sleep": "source: Hjetland et al., Frontiers in Psychiatry, 2025",
    "eu": "source: European Commission, 6 Feb 2026 (preliminary)",
}


def header(X, alpha=1.0):
    relay_icon(X, 96, 272, 24, alpha)
    X.text("THE EXIT MANUAL", 134, 286, 36, "white", kind="sansm", align="left", alpha=0.85 * alpha)
    X.text(f"{EPISODE} · {SERIES}", 892, 286, 30, "grey", kind="mono", align="right", alpha=alpha)


def source(X, key, alpha=1.0):
    if alpha > 0:
        X.text(SRC[key], 80, 340, 28, "grey", kind="mono", align="left", alpha=alpha)


def fade_in(t, a, d=0.25):
    return prog(t, a, a + d)


def fade_io(t, a, b, d=0.25):
    return prog(t, a, a + d) * (1 - prog(t, b - d, b))


# ------------------------------------------------------------------ 1 · the year (0 -> look)
def title40(X, alpha=1.0, sub_alpha=1.0):
    X.text("40 DAYS", CAP_CX, 560, 210, "green", kind="sans", alpha=alpha, glow=0.25)
    X.text("A YEAR ON OUR FEEDS", CAP_CX, 636, 52, "white", kind="sansm", alpha=sub_alpha * alpha)


def scene_year(X, t):
    t_add = 0.3                                        # the slivers stack while "forty days a year" is said
    u = clamp01((t - t_add) / 1.35)
    hi = prog(t, t_add + 1.2, t_add + 1.6)
    t_out = CH("added", 1) + 0.25                      # the stacked days are pulled into a phone
    k = ease_io5(prog(t, t_out, T("look") - 0.1))
    a_grid = 1 - prog(t, t_out, t_out + 0.9)
    title40(X, alpha=1 - prog(t, t_out, t_out + 0.6))
    if k < 1:
        X.c.save()
        # the grid shrinks towards the phone's screen as the phone appears
        z = lerp(1.0, 0.36, k)
        gy = GRID_Y0 + 7.5 * GRID_PITCH
        X.c.translate(CAP_CX, lerp(gy, 760, k))
        X.c.scale(z, z)
        X.c.translate(-CAP_CX, -gy)
        year_grid(X, u, alpha=1.0, block_hi=hi * (1 - k), others=a_grid)
        X.c.restore()
    if hi > 0 and k < 0.2:
        x1, y1 = cell_xy(24)
        a = hi * (1 - prog(t, t_out - 0.3, t_out))
        X.text("= 40 full days, 24 h each", CAP_CX, GRID_Y0 + 2 * GRID_PITCH + 60, 50, "green", kind="sansm", alpha=a)
        X.text("365 days × 2 h 39 min", CAP_CX, GRID_Y0 + 2 * GRID_PITCH + 112, 38, "grey", kind="mono", alpha=a)
    if t < 0:
        a = 0
        X.text("each square = one day · green = time on feeds", CAP_CX, GRID_Y0 + 15 * GRID_PITCH + 40, 32,
               "grey", kind="mono", alpha=a)
    pa = prog(t, t_out + 0.3, T("look") - 0.25)        # the phone forms around the stacked days
    if pa > 0:
        X.c.saveLayerAlpha(None, int(255 * pa))
        phone(X, CAP_CX, 760, scroll=0, clock="23:12", glow=pa)
        X.c.restore()
    source(X, "time", 1 - prog(t, t_out, t_out + 0.5))


# ------------------------------------------------------------------ 2 · the machine behind the screen (look -> name)
RIB_X = CAP_CX - (PHONE_W - 32 - 28) / 2          # x of the feed column (same as inside the phone)
RIB_W = PHONE_W - 32 - 28
PH_CY = 760
FEED_TOP = PH_CY - PHONE_H / 2 + 16 + 70


def flick_scroll(t, t0, every=0.62, dist=CARD_H + CARD_GAP):
    """The feed moves one card per flick of the thumb (fast start, soft stop)."""
    if t < t0:
        return 0.0
    n = (t - t0) / every
    k = math.floor(n)
    f = n - k
    return (k + ease_out(clamp01(f / 0.55), 4)) * dist


def scene_machine(X, t):
    t_look = T("look")
    kz = ease_io5(prog(t, t_look + 0.15, t_look + 1.7))
    z = lerp(1.0, 0.62, kz)
    scroll = flick_scroll(t, T("look") - 0.2)
    X.cam(CAP_CX, 760, z, fx=lerp(CAP_CX, 300, kz), fy=lerp(760, 790, kz))
    # the feed doesn't stop at the edge of the screen: it runs off into the dark, both ways
    ext = prog(t, t_look + 0.3, t_look + 1.4)
    if ext > 0:
        feed(X, RIB_X, FEED_TOP, RIB_W, scroll, i0=-14, i1=60, alpha=0.55 * ext)
    phone(X, CAP_CX, PH_CY, scroll=scroll, clock="23:12", glow=1.0)
    # the machine
    m = prog(t, t_look + 1.2, t_look + 1.8)
    if m > 0:
        bx, by = 1000, 330                               # advertisers (world)
        mx, my = 1000, 1060                              # Meta's revenue (world)
        X.neon_rect(bx - 220, by - 120, 440, 240, "magenta", width=5, r=24, glow=0.6, fill=0xFF16060F, fill_alpha=0.95,
                    alpha=m)
        X.text("ADVERTISERS", bx, by - 4, 80, "white", kind="sans", alpha=m)
        X.text("buy the slots", bx, by + 76, 64, "magenta", kind="sansm", alpha=m)
        X.neon_rect(mx - 220, my - 150, 440, 300, "magenta", width=5, r=24, glow=0.8, fill=0xFF16060F,
                    fill_alpha=0.95, alpha=m)
        X.text("META", mx, my - 52, 96, "white", kind="sans", alpha=m)
        X.text("$196 B", mx, my + 40, 84, "magenta", kind="sans", alpha=m, glow=0.4)
        X.text("from ads, 2025", mx, my + 108, 58, "grey", kind="sansm", alpha=m)
        X.arrow([(bx, by + 124), (bx, my - 156)], "magenta", u=prog(t, t_look + 1.5, t_look + 2.1), width=7, head=30,
                alpha=m)
        a12 = prog(t, CH("slot", 1), CH("slot", 1) + 0.3) * m
        X.text("+12 % ads shown", mx, my + 240, 70, "white", kind="sans", alpha=a12)
        X.text("in one year", mx, my + 312, 58, "grey", kind="sansm", alpha=a12)
        # every ad slot that scrolls through the screen is wired to the buyers
        step = CARD_H + CARD_GAP
        for i in range(-14, 60):
            if not is_ad(i):
                continue
            y = FEED_TOP + i * step - scroll + CARD_H / 2
            if not (-900 < y < 2400):
                continue
            inside = PH_CY - PHONE_H / 2 < y < PH_CY + PHONE_H / 2
            a = m * (1.0 if inside else 0.45)
            X.neon_line(RIB_X + RIB_W + 4, y, bx - 152, by + (y - by) * 0.18, "magenta", width=3 if inside else 2,
                        glow=0.6 if inside else 0.2, alpha=a)
            if inside:                                      # a coin travels to the buyers while the ad is on screen
                ph = ((y - (PH_CY - PHONE_H / 2)) / PHONE_H)
                cx = lerp(RIB_X + RIB_W + 4, bx - 152, 1 - ph)
                cy = lerp(y, by + (y - by) * 0.18, 1 - ph)
                X.c.drawCircle(cx, cy, 14, X.paint("magenta", m))
                X.c.drawCircle(cx, cy, 26, X.paint("magenta", 0.35 * m, blur=10))
    X.c.restore()
    if m > 0:
        X.text("illustration: ad slots shown 1 in 4", 80, 384, 28, "grey", kind="mono", align="left", alpha=m)
        X.panel(190, 420, 220, 110, alpha=0.9 * m, border=None)
        X.text("OUR TIME", 300, 470, 48, "green", kind="sans", alpha=m)
        X.text("goes in here", 300, 512, 34, "grey", kind="sansm", alpha=m)
    source(X, "meta", m)


# ------------------------------------------------------------------ 3 · the eye opens onto the numbers (name -> dollar)
Q1 = ["“...significantly determined by our success in adding, retaining, and engaging active users...”"]
Q1_HI = (17, 24)          # "active users of our products that deliver ad impressions,"
Q2 = ["“...if our users decrease their level of engagement with our products, our revenue, financial results, "
      "and business may be significantly harmed.”"]
Q2_HI = [(15, 22), (29, 32)]   # "if our users decrease their level of engagement" / "may be significantly harmed."


def _q_index(words, phrase):
    w = " ".join(words).split(" ")
    p = phrase.split(" ")
    for i in range(len(w) - len(p) + 1):
        if [x.strip(",.“”") for x in w[i:i + len(p)]] == p:
            return (i, i + len(p) - 1)
    raise ValueError(phrase)


Q1_HI = _q_index(Q1, "engaging active users")
Q2_HI = [_q_index(Q2, "if our users decrease their level of engagement"), _q_index(Q2, "may be significantly harmed")]


def doc_page(X, t, alpha):
    X.panel(70, 410, 830, 760, alpha=0.96 * alpha, r=16, border="cyan", border_alpha=0.35)
    X.text("META PLATFORMS, INC.", 110, 478, 34, "cyan", kind="mono", align="left", alpha=alpha)
    X.text("ANNUAL REPORT (FORM 10-K) · 2025", 110, 520, 30, "grey", kind="mono", align="left", alpha=alpha)
    X.text("our financial performance:", 110, 578, 30, "grey", kind="mono", align="left", alpha=alpha * (1 - prog(t, T("warn") - 0.3, T("warn"))))
    X.text("risk factors:", 110, 578, 30, "grey", kind="mono", align="left", alpha=alpha * prog(t, T("warn") - 0.3, T("warn")))
    t_warn = T("warn")
    sc = ease_io5(prog(t, t_warn - 0.3, t_warn + 0.5))          # the page moves to the second passage
    X.c.save()
    X.c.clipRect(skia.Rect(70, 600, 900, 1166))
    y0 = 680 - 450 * sc
    u1 = clamp01((t - CH("name", 1)) / 0.8)
    y1 = doc_lines(X, Q1, 110, y0, size=50, hi=[Q1_HI], hi_u=[u1], alpha=alpha * (1 - 0.6 * sc), maxw=750)
    us = prog(t, CH("name", 2) - 0.05, CH("name", 2) + 0.25) * (1 - sc)
    if us > 0:
        X.text("= us.", 860, y1 + 20, 84, "green", kind="sans", align="right", alpha=us, glow=0.4)
    u2 = clamp01((t - CH("warn", 1)) / 0.9)
    u3 = clamp01((t - CH("warn", 2)) / 1.4)
    doc_lines(X, Q2, 110, y1 + 150, size=48, hi=Q2_HI, hi_u=[u2, u3], alpha=alpha * (0.35 + 0.65 * sc), maxw=750)
    X.c.restore()


def scene_eye(X, t):
    t0 = T("name") - 0.2
    t_px = T("name") + 0.8                     # the eye starts turning into pixels
    t_dive = T("name") + 1.4
    t_doc = T("name") + 2.3
    if t < t_doc + 0.35:
        block = 1 + 46 * ease_in_out(prog(t, t_px, t_doc))
        z = 1 + 7 * ease_io5(prog(t, t_dive, t_doc + 0.35))
        a = 1 - prog(t, t_doc, t_doc + 0.35)
        open_ = ease_out(prog(t, t0, t0 + 0.5))

        def draw(Y):
            Y.c.save()
            Y.c.translate(CAP_CX, 760)
            Y.c.scale(z, z)
            Y.c.translate(-CAP_CX, -760)
            # the feed's light on the face (soft)
            Y.c.drawCircle(CAP_CX, 760, 520, Y.paint(0xFF9FC4FF, 0.06, blur=80))
            eye(Y, CAP_CX, 760, 1.25, lid=lerp(0.15, 1.0, open_))
            Y.c.restore()
        X.c.save()
        X.c.saveLayerAlpha(None, int(255 * a))
        pixelated(X, draw, block)
        # inside the pixels: the numbers behind the façade
        if block > 14:
            r = np.random.default_rng(5)
            na = prog(t, t_px + 0.3, t_doc) * a
            for gy in range(int(block * 4), 1200, int(block)):
                for gx in range(int(block * 2), 900, int(block * 2)):
                    if r.random() < 0.33:
                        X.text(str(r.integers(0, 10)), gx + block / 2, gy - block * 0.25, block * 0.62, "green",
                               kind="mono", alpha=0.55 * na)
        X.c.restore()
        X.c.restore()
    if t >= t_doc:
        doc_page(X, t, prog(t, t_doc, t_doc + 0.35))
    source(X, "10k", prog(t, t_doc, t_doc + 0.3))


# ------------------------------------------------------------------ 4 · one dollar, times billions (dollar -> nolast)
def person(X, x, y, r, color="green", alpha=1.0):
    X.c.drawCircle(x, y - r * 1.25, r * 0.55, X.paint(color, alpha))
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect(x - r * 0.9, y - r * 0.55, x + r * 0.9, y + r * 0.9), r * 0.6, r * 0.6))
    X.c.drawPath(p, X.paint(color, alpha))


def scene_money(X, t):
    t_d = T("dollar")
    t_x = T("times") - 0.1
    t_b = CH("times", 0) + 1.25                  # "...billion": the count lands on the word
    t_y = E("times") + 0.05
    # zoom out from one person to 3.58 billion
    k = ease_in_out(prog(t, t_x, t_b))
    lz = lerp(0.0, 9.55, k)                       # log10 of the number of people in view
    d0 = 260.0
    a_scene = 1 - 0.75 * prog(t, t_y, t_y + 0.4)
    cy = 790
    # lattices at successive powers of ten fade in and out (a seamless zoom)
    for lvl in range(0, 6 if t >= t_x else 0):
        dd = d0 * 10 ** (lvl - lz / 2.0)          # screen spacing of this lattice
        if dd < 3 or dd > 2000:
            continue
        a = clamp01((dd - 3) / 12) * clamp01((900 - dd) / 600) * a_scene
        r = max(0.9, dd * 0.18)
        n = int(min(70, 520 / dd)) + 1
        for iy in range(-n, n + 1):
            yy = cy + iy * dd
            if yy < 590 or yy > 1160:
                continue
            for ix in range(-n, n + 1):
                xx = CAP_CX + ix * dd
                if xx < 60 or xx > 910:
                    continue
                if r > 6:
                    person(X, xx, yy, r, "green", a)
                else:
                    X.c.drawCircle(xx, yy, r, X.paint("green", a))
    if lz < 0.2:                                  # the one person, and their dollar
        a = fade_in(t, t_d - 0.1, 0.3)
        person(X, CAP_CX, cy, 46, "green", a)
        X.text("16¢", CAP_CX, cy - 190, 150, "magenta", kind="sans", alpha=fade_in(t, CH("dollar", 1) - 0.1), glow=0.4)
        X.text("a day, to Meta", CAP_CX, cy - 128, 44, "white", kind="sansm", alpha=fade_in(t, CH("dollar", 1) - 0.1))
        X.text("$57 a year per daily user, 2025", CAP_CX, cy + 150, 38, "grey", kind="mono", alpha=fade_in(t, CH("dollar", 1) + 0.3))
        X.text("worldwide average", CAP_CX, cy + 196, 34, "grey", kind="mono", alpha=fade_in(t, CH("dollar", 1) + 0.3))
    if t >= t_x:
        n = 10 ** min(lz, math.log10(3.58e9))
        if t >= t_b:
            n = 3.58e9
        s = f"× {int(round(n)):,}" if n < 3.5e9 else "× 3,580,000,000"
        X.text(s, CAP_CX, 470, 76, "white", kind="mono", alpha=fade_in(t, t_x) * a_scene)
        X.text("daily users, Dec 2025", CAP_CX, 530, 38, "grey", kind="mono", alpha=fade_in(t, t_x) * a_scene)
    if t >= t_y - 0.1:
        a = fade_in(t, t_y - 0.1, 0.35)
        sc = 1 + 0.06 * (1 - ease_out(prog(t, t_y - 0.1, t_y + 0.4)))
        X.panel(110, 610, 750, 380, alpha=0.88 * a, border=None)
        X.text("$201 B", CAP_CX, 850, 230, "magenta", kind="sans", alpha=a, glow=0.5, scale=sc)
        X.text("Meta's revenue in 2025", CAP_CX, 930, 46, "white", kind="sansm", alpha=a)
    source(X, "meta")


# ------------------------------------------------------------------ 5 · no last page (nolast -> study)
def clock_at(t):
    """23:12 -> 01:47 over the scene, faster and faster."""
    t0, t1 = T("nolast") - 0.2, CH("nolast", 1) + 0.5
    u = clamp01((t - t0) / (t1 - t0)) ** 1.7
    m = int(23 * 60 + 12 + u * (155))
    return f"{(m // 60) % 24:02d}:{m % 60:02d}"


def scene_night(X, t):
    t0 = T("nolast") - 0.2
    t_stop = CH("nolast", 1) + 0.5
    tint = 1 - prog(t, t0, t_stop)
    X.bg(tint=0xFF1A2A55, tint_a=0.35 * tint)
    # the flicks get faster as the night goes on, then stop
    tt = min(t, t_stop)
    sp = 0.0
    every = 0.55
    for i in range(int(max(0, tt - t0) / 0.02)):
        sp += 0.02 * (CARD_H + CARD_GAP) / every * (1 + 1.2 * i * 0.02 / (t_stop - t0))
    if t > t_stop:
        sp += (CARD_H + CARD_GAP) * 0.5 * ease_out(prog(t, t_stop, t_stop + 0.6))
    n_cards = 6 + sp / (CARD_H + CARD_GAP)
    clk = clock_at(t)
    last = prog(t, CH("nolast", 1) - 0.1, CH("nolast", 1) + 0.5)

    def content(Y, rect):
        sx0, sy0, sx1, sy1 = rect
        feed(Y, sx0 + 14, sy0 + 70, sx1 - sx0 - 28, sp, i0=-2, i1=int(n_cards) + 8)
        Y.c.drawRect(skia.Rect(sx0, sy0, sx1, sy0 + 58), Y.paint(0xFF07090D, 0.92))
        Y.text(clk, sx0 + 40, sy0 + 42, 30, "white", kind="sansm", align="left")
        frac = 6 / n_cards
        th = max(10, (sy1 - sy0 - 100) * frac)
        Y.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(sx1 - 12, sy0 + 70 + (sy1 - sy0 - 100 - th) * 0.92, sx1 - 6,
                                                      sy0 + 70 + (sy1 - sy0 - 100 - th) * 0.92 + th), 3, 3),
                      Y.paint(0xFFAAB2C0, 0.8))
        if last > 0:                           # the last page is the night itself
            Y.c.drawRect(skia.Rect(sx0, sy0, sx1, sy1), Y.paint(0xFF020306, last))
            Y.text(clk, (sx0 + sx1) / 2, (sy0 + sy1) / 2 + 30, 120, "white", kind="sans", alpha=last)
            Y.text("night's over", (sx0 + sx1) / 2, (sy0 + sy1) / 2 + 100, 34, "grey", kind="mono", alpha=last)
    phone(X, 380, 760, content=content, glow=1.0)
    # the time, big, beside the phone
    X.text(clk, 890, 560, 84, "white", kind="mono", align="right", alpha=1 - last)
    if t < CH("nolast", 1):
        X.text("no end", 890, 624, 44, "grey", kind="mono", align="right", alpha=fade_in(t, CH("nolast", 0) + 0.8))


# ------------------------------------------------------------------ 6 · the study, then check it (study -> eu)
def ring(X, cx, cy, r, u0, u1, color, width=34, alpha=1.0):
    if u1 <= u0:
        return
    p = skia.Path()
    p.addArc(skia.Rect(cx - r, cy - r, cx + r, cy + r), -90 + 360 * u0, 360 * (u1 - u0))
    X.c.drawPath(p, X.paint(color, alpha, stroke=width, cap_round=False))


def scene_study(X, t):
    t0 = T("study")
    tag(X, "THE STUDY", 110, 450, "cyan", alpha=fade_in(t, t0 - 0.2))
    X.text("45,202", 110, 590, 128, "white", kind="sans", align="left", alpha=fade_in(t, t0 + 0.8))
    X.text("students, aged 18–28, Norway", 110, 650, 42, "grey", kind="sansm", align="left",
           alpha=fade_in(t, t0 + 1.0))
    # one hour on a screen in bed = a full ring; 24 minutes of sleep lost = 40 % of it
    cx, cy, r = 330, 940, 150
    a1 = fade_in(t, CH("study", 1) - 0.1)
    if a1 > 0:
        X.c.drawCircle(cx, cy, r, X.paint(0xFF1A2030, a1, stroke=34))
        ring(X, cx, cy, r, 0, ease_in_out(prog(t, CH("study", 1), CH("study", 1) + 1.4)), "cyan", alpha=a1)
        X.text("+1 h", cx, cy + 22, 74, "cyan", kind="sans", alpha=a1)
        X.text("screen in bed", 560, 900, 44, "cyan", kind="sansm", align="left", alpha=a1)
    a2 = fade_in(t, CH("study", 2) + 0.2)
    if a2 > 0:
        u = ease_in_out(prog(t, CH("study", 2) + 0.2, CH("study", 2) + 1.4)) * 0.4
        ring(X, cx, cy, r + 2, 0, u, "magenta", width=40, alpha=a2)
        X.text("−24 min", 560, 990, 74, "magenta", kind="sans", align="left", alpha=a2)
        X.text("of sleep", 560, 1040, 44, "white", kind="sansm", align="left", alpha=a2)
    X.text("any screen use, not only social media", 80, 1170, 30, "grey", kind="mono", align="left",
           alpha=fade_in(t, CH("study", 2) + 0.6))
    source(X, "sleep")


def scene_check(X, t):
    t0 = T("check")
    tag(X, "CHECK THE CLAIM", 110, 450, "green", alpha=fade_in(t, t0 - 0.2))
    a = fade_in(t, t0)
    for (lab, y) in (("SCREEN IN BED", 600), ("BAD SLEEP", 960)):
        X.neon_rect(190, y - 70, 590, 130, "white", width=3, r=18, glow=0.0, fill=0xFF0C0F18, fill_alpha=0.95, alpha=a)
        X.text(lab, CAP_CX, y + 18, 62, "white", kind="sans", alpha=a)
    X.arrow([(400, 672), (400, 880)], "white", u=prog(t, t0 + 0.2, t0 + 0.6), width=6, head=24, alpha=a)
    X.text("causes?", 380, 790, 42, "grey", kind="sansm", align="right", alpha=prog(t, t0 + 0.5, t0 + 0.8))
    b = prog(t, CH("check", 1) - 0.05, CH("check", 1) + 0.5)
    X.arrow([(570, 880), (570, 672)], "green", u=b, width=6, head=24)
    X.text("or the reverse", 600, 790, 42, "green", kind="sansm", align="left", alpha=prog(t, CH("check", 1) + 0.3,
                                                                                            CH("check", 1) + 0.6))
    ta = fade_in(t, CH("dont", 1) - 0.05, 0.2)
    ga = prog(t, CH("check", 1) + 0.9, CH("check", 1) + 1.2) * (1 - prog(t, CH("dont", 1) - 0.25, CH("dont", 1) - 0.05))
    X.text("a survey shows a link, not a cause.", CAP_CX, 1118, 36, "grey", kind="mono", alpha=ga)
    X.text("its authors say so.", CAP_CX, 1160, 36, "grey", kind="mono", alpha=ga)
    if ta > 0:
        X.panel(190, 1060, 590, 130, alpha=0.97 * ta, border="green", border_alpha=0.6)
        X.text("TEST IT: ONE NIGHT", CAP_CX, 1145, 60, "green", kind="sans", alpha=ta, glow=0.3)
    source(X, "sleep")


# ------------------------------------------------------------------ 7 · rules can change (eu -> step)
def scene_eu(X, t):
    t0 = T("eu")
    a = fade_in(t, t0 - 0.2)
    X.panel(90, 420, 790, 520, alpha=0.95 * a, border="cyan", border_alpha=0.4)
    X.text("EUROPEAN COMMISSION", 130, 490, 40, "cyan", kind="mono", align="left", alpha=a)
    X.text("6 February 2026 · preliminary findings", 130, 538, 32, "grey", kind="mono", align="left", alpha=a)
    items = ["infinite scroll", "autoplay", "push notifications"]
    b = fade_in(t, CH("eu", 1) - 0.1)
    X.text("TikTok's design:", 130, 620, 44, "white", kind="sansm", align="left", alpha=b)
    for i, s in enumerate(items):
        X.text("— " + s, 150, 690 + i * 60, 46, "white", kind="sansm", align="left", alpha=b)
    c = fade_in(t, CH("eu", 1) + 1.0)
    X.text("may breach the Digital", 130, 880, 46, "cyan", kind="sans", align="left", alpha=c)
    X.text("Services Act · not a final decision", 130, 926, 38, "grey", kind="sansm", align="left", alpha=c)
    d = fade_in(t, T("design") - 0.1)
    if d > 0:
        X.text("a design choice", CAP_CX, 1040, 64, "white", kind="sans", alpha=d)
        X.text("↓", CAP_CX, 1095, 50, "grey", kind="sans", alpha=fade_in(t, CH("design", 1) - 0.1))
        X.text("can be changed.", CAP_CX, 1160, 64, "green", kind="sans", alpha=fade_in(t, CH("design", 1) - 0.1), glow=0.3)
    source(X, "eu")


# ------------------------------------------------------------------ 8 · step one (step -> stop)
def scene_step(X, t):
    t0 = T("step")
    tag(X, "STEP ONE · TONIGHT", 110, 450, "green", alpha=fade_in(t, t0 - 0.2))
    a = fade_in(t, t0)
    c = X.c
    # a bedroom, in a few lines
    wall = X.paint(0xFF2A3040, a, stroke=4)
    c.drawLine(90, 1120, 880, 1120, wall)
    door_x = 700
    c.drawRect(skia.Rect(door_x, 600, door_x + 160, 1120), wall)
    close = ease_in_out(prog(t, CH("step", 1) + 1.15, CH("step", 1) + 1.6))
    dp = skia.Path()                                   # the door swings shut
    dw = 160 * lerp(0.25, 1.0, close)
    dp.addRect(skia.Rect(door_x, 600, door_x + dw, 1120))
    c.drawPath(dp, X.paint(0xFF12161F, a))
    c.drawPath(dp, X.paint(0xFF3A4458, a, stroke=3))
    # bed
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(110, 980, 520, 1120), 18, 18), X.paint(0xFF141A26, a))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(110, 940, 230, 1000), 22, 22), X.paint(0xFF2A3346, a))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(110, 980, 520, 1120), 18, 18), X.paint(0xFF2A3040, a, stroke=4))
    # nightstand + alarm clock
    c.drawRect(skia.Rect(540, 1010, 650, 1120), X.paint(0xFF141A26, a))
    c.drawRect(skia.Rect(540, 1010, 650, 1120), X.paint(0xFF2A3040, a, stroke=4))
    ca = fade_in(t, CH("step", 1) + 1.5, 0.4)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(552, 950, 640, 1006), 10, 10), X.paint(0xFF0A0C11, ca))
    X.text("07:00", 596, 990, 34, "amber", kind="mono", alpha=ca, glow=0.6)
    # the phone leaves the room
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
    X.text("in the next room, it can't call you back", CAP_CX, 560, 38, "grey", kind="sansm",
           alpha=fade_in(t, CH("step", 1) + 1.6))
    X.text("old alarm clock", 596, 920, 30, "amber", kind="sansm", alpha=fade_in(t, CH("step", 1) + 1.7))


# ------------------------------------------------------------------ 9 · stop scrolling, go to sleep (stop -> world)
def scene_stop(X, t):
    t0 = T("stop")
    on = 1 - ease_in_out(prog(t, t0 + 0.1, CH("stop", 1) + 0.4))          # slow, smooth dimming (never a flash)
    sc = flick_scroll(t, t0 - 2.0, every=0.9) if t < t0 + 0.2 else flick_scroll(t0 + 0.2, t0 - 2.0, every=0.9)
    phone(X, CAP_CX, 700, scroll=sc, clock="01:47", screen_on=on, glow=on)
    # after the screen is off: a few still stars over the dark
    s = prog(t, CH("stop", 1) + 0.3, CH("stop", 1) + 1.0)
    if s > 0:
        r = np.random.default_rng(3)
        for _ in range(40):
            x, y = r.uniform(60, 900), r.uniform(380, 1120)
            X.c.drawCircle(x, y, r.uniform(1.2, 2.6), X.paint("white", s * r.uniform(0.25, 0.7)))


def scene_world(X, t):
    t0 = T("world") - 0.25
    a = ease_in_out(prog(t, t0, t0 + 1.2))
    r = np.random.default_rng(3)
    for _ in range(40):
        x, y = r.uniform(60, 900), r.uniform(380, 1120)
        X.c.drawCircle(x, y, r.uniform(1.2, 2.6), X.paint("white", (1 - a * 0.6) * r.uniform(0.25, 0.7)))
    relay(X, CAP_CX, 760, 0.62, alpha=a, rim=0.6)
    sa = prog(t, T("sign") - 0.05, T("sign") + 0.3)
    if sa > 0:
        X.panel(110, 1200, 750, 190, alpha=0.75 * sa, border=None)
        X.text("build the commons.", CAP_CX, 1290, 62, "green", kind="sign", alpha=sa, glow=0.5)
        X.text("THE EXIT MANUAL", CAP_CX, 1356, 40, "white", kind="sansm", alpha=0.8 * sa)


# ------------------------------------------------------------------ 10 · loop (loop -> end == frame 0)
def scene_loop(X, t):
    a = ease_in_out(prog(t, T("loop") - 0.2, T("loop") + 0.8))
    year_grid(X, 0.0, alpha=a)
    title40(X, alpha=ease_in_out(prog(t, E("loop") - 0.3, DURATION - 0.05)))
    source(X, "time", a)


def scenes():
    return [
        (0.0, T("look") - 0.2, scene_year),
        (T("look") - 0.2, T("name") - 0.2, scene_machine),
        (T("name") - 0.2, T("dollar") - 0.2, scene_eye),
        (T("dollar") - 0.2, T("nolast") - 0.2, scene_money),
        (T("nolast") - 0.2, T("study") - 0.25, scene_night),
        (T("study") - 0.25, T("check") - 0.2, scene_study),
        (T("check") - 0.2, T("eu") - 0.2, scene_check),
        (T("eu") - 0.2, T("step") - 0.2, scene_eu),
        (T("step") - 0.2, T("stop") - 0.2, scene_step),
        (T("stop") - 0.2, T("world") - 0.25, scene_stop),
        (T("world") - 0.25, T("loop") - 0.2, scene_world),
        (T("loop") - 0.2, DURATION + 1, scene_loop),
    ]


_SC = None


def draw_frame(X, t):
    global _SC
    _SC = _SC or scenes()
    if not isinstance(X, Ctx2):
        X.__class__ = Ctx2
    if not hasattr(X.A, "bg2"):
        X.A.__class__ = Assets2
        Assets2.__init__(X.A)
    X.level = level(t)
    X.bg()
    for a, b, fn in _SC:
        if a <= t < b:
            fn(X, t)
            break
    header(X)
    for cap in CAPTIONS:
        cap.draw(X)
    X.finish()


# ------------------------------------------------------------------ sound (exit_audio.py)
BPM = 76
TRANSPOSE = -2
# Fmaj7 - Am7 - G6 - Em7 (A-minor colour, more open and human than v1's loop)
CHORDS = [([53, 57, 60, 64], 41), ([57, 60, 64, 67], 45), ([55, 59, 62, 64], 43), ([52, 55, 59, 62], 40)]
MUSIC_QUIET = ((0, 3.8), (25.7, 28.8), (56.6, 70))


def sfx_list():
    s = [(0.35 + k * 0.22, "blip", k) for k in range(5)]
    s += [
        (CH("added", 1) + 0.3, "whoosh_low", 1),
        (T("look") + 0.15, "rise", 0),
        (T("look") + 1.3, "low_hit", 0),
    ]
    for j in range(4):
        s.append((T("look") + 1.6 + j * 0.62 * 4, "coin", j))
    s += [
        (T("name") + 0.9, "rise", 1),
        (CH("name", 1) - 0.15, "whoosh_low", 2),
        (CH("name", 1), "keys", 0),
        (T("warn"), "keys", 1),
        (T("dollar") + 1.0, "coin", 0),
        (T("times"), "rise", 2),
        (E("times") + 0.05, "low_hit", 1),
        (T("nolast") - 0.2, "whoosh_low", 3),
        (CH("nolast", 1) + 0.5, "clunk", 0),
        (T("study") - 0.2, "keys", 2),
        (CH("study", 2) + 0.2, "blip", 3),
        (CH("check", 1), "blip", 4),
        (CH("dont", 1), "blip", 2),
        (T("eu") - 0.2, "keys", 3),
        (CH("step", 1) + 1.3, "clunk", 1),
        (T("world") - 0.2, "low_hit", 2),
        (T("loop") - 0.2, "whoosh_low", 4),
    ]
    return s


SUBTITLE_EXTRAS = []
EXTRA_KEYS = []
if TIM:
    SUBTITLE_EXTRAS = [(0.0, T("added") - 0.04, "Forty days a year."),
                       (T("sign") - 0.04, T("loop") - 0.04, "build the commons.")]
    EXTRA_KEYS = [0.9, 1.5, round(T("look") + 1.9, 2), round(T("name") + 1.2, 2), round(CH("name", 2) + 0.4, 2),
                  round(CH("warn", 2) + 1.2, 2), round(T("times") + 0.8, 2), round(E("times") + 0.5, 2),
                  round(CH("nolast", 1) + 0.6, 2), round(CH("study", 2) + 1.4, 2), round(CH("dont", 1) + 0.3, 2),
                  round(CH("design", 1) + 0.4, 2), round(CH("step", 1) + 1.8, 2), round(CH("stop", 1) + 1.0, 2),
                  round(T("sign") + 0.5, 2)]


def draw_cover(X):
    """Cover / thumbnail: the 40 days, the year grid stacked. No byline."""
    if not isinstance(X, Ctx2):
        X.__class__ = Ctx2
    if not hasattr(X.A, "bg2"):
        X.A.__class__ = Assets2
        Assets2.__init__(X.A)
    X.t = 0.0
    X.bg()
    header(X)
    X.text("WE GIVE", CAP_CX, 380, 76, "white", kind="sans")
    title40(X)
    year_grid(X, 1.0, block_hi=1.0)
    X.text("every hour, added up", CAP_CX, 1250, 64, "white", kind="sansm")
    X.text("18 h 36 min a week · DataReportal / GWI, 2026", CAP_CX, 1320, 32, "grey", kind="mono")
    X.finish()
