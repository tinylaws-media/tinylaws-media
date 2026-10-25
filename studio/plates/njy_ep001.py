"""NOT JUST YOU #001 — "The bad-news loop".

Hook (frame 0, said at once): "Can't stop scrolling the bad news?"
Payoff by ~10 s: after the Boston Marathon bombing, 6+ hours a day of coverage was linked to more
acute stress than being there (Holman, Garfin & Silver, PNAS 2014, doi:10.1073/pnas.1316265110).
Mechanism: a 3-year study found a loop: coverage -> stress -> worry -> more watching
(Thompson et al., Sci Adv 2019, doi:10.1126/sciadv.aav3502).
What helps: keep the key updates, skip repetitive coverage; media should drop sensational and
graphic images (Garfin, Silver & Holman, Health Psychol 2020, doi:10.1037/hea0000875); graphic
images and sharing them (Holman, Garfin & Silver, PNAS 2024, doi:10.1073/pnas.2318465121).
Loop: the last line "...it's not just you" runs into the first "Can't stop scrolling the bad news?"
"""
import json
import math
import os

from njy_engine import *

EP = "njy_ep001"
VOICE_OPTS = {"voice": "af_heart", "speed": 0.9, "semitones": -1.0}

# say: what the voice says (numbers spelled as spoken). cap: the caption ('/' = line break,
# *word* = amber italic). gap: silence before the line (s). src: source line under the caption.
LINES = [
    dict(say="Can't look away from terrible news?", cap="Can't look away / from *terrible news*?", gap=0.10),
    dict(say="It's not weakness. It's a loop.", cap="Not weakness. / A *loop*.", gap=0.35),
    dict(say="In twenty thirteen, after the Boston bombing,", cap="In 2013, after / the Boston bombing...", gap=0.45),
    dict(say="six or more hours a day of coverage, that first week,", cap="6+ hours a day / of coverage, week one...", gap=0.20),
    dict(say="went with more stress symptoms than being there.", cap="...more stress symptoms / than *being there*.", gap=0.15),
    dict(say="One survey: a link, not proof.", cap="One survey: / a *link*, not proof.", gap=0.55),
    dict(say="So the same team followed over four thousand people for three years.", cap="The same team followed / 4,165 people, 3 years.", gap=0.45),
    dict(say="More watching came before more lasting stress.", cap="More watching... / more *lasting stress*.", gap=0.35),
    dict(say="More stress, before more worry about the future.", cap="More stress... / more *worry*.", gap=0.30),
    dict(say="Years later, after another attack, worry went with more watching.", cap="Years later: more worry, / more *watching*.", gap=0.30),
    dict(say="The more it hurts, the more we look.", cap="The more it hurts, / the more we *look*.", gap=0.50),
    dict(say="Wanting news when you're scared makes sense.", cap="Scared? Wanting news / makes *sense*.", gap=0.40),
    dict(say="And a twenty-four seven feed never runs out.", cap="And a 24/7 feed / never *runs out*.", gap=0.40),
    dict(say="What helps? The researchers suggest: keep the key updates,", cap="What helps? / Keep the *key updates*...", gap=0.50),
    dict(say="and cut the replays that add nothing new.", cap="...cut the replays / that add *nothing new*.", gap=0.20),
    dict(say="Graphic images were linked to more stress, six months later.", cap="Graphic images: / more stress *6 months on*.", gap=0.40),
    dict(say="So, together: share the facts, not the footage.", cap="Together: share / the facts, not the *footage*.", gap=0.40),
    dict(say="And ask newsrooms to hold back graphic images.", cap="Ask newsrooms to / hold back *graphic images*.", gap=0.30),
    dict(say="If it's heavy, tell someone: a friend, a helpline. Not the feed.", cap="Heavy? Tell someone: / a friend, a *helpline*.", gap=0.50),
    dict(say="Be honest: how many hours today?", cap="Be honest: / how many hours *today*?", gap=0.50),
    dict(say="Whatever the number... it's not just you.", cap="Whatever the number... / it's *not just you*.", gap=0.50),
]
TAIL = 0.55        # after the last word, before the loop seam


def _lines_json():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", f"{EP}_lines.json")
    return json.load(open(p)) if os.path.exists(p) else None


def timeline():
    """[(start, end)] per line, from the measured durations (njy_voice.py measure)."""
    m = _lines_json()
    t, out = 0.0, []
    for i, ln in enumerate(LINES):
        d = m[i]["dur"] if (m and i < len(m) and m[i]["say"] == ln["say"]) else 0.36 * len(ln["say"].split())
        t += ln["gap"]
        out.append((round(t, 3), round(t + d, 3)))
        t += d
    return out


TL = timeline()
DURATION = round(TL[-1][1] + TAIL, 2)


# ================================================================== scenes
def T(i):
    return TL[i][0]


def E(i):
    return TL[i][1]


CAPTIONS = [Caption(0.0 if i == 0 else TL[i][0], (TL[i + 1][0] if i + 1 < len(TL) else DURATION + 1), ln["cap"])
            for i, ln in enumerate(LINES)]

# source shown under the caption (bible: every figure shows its source)
SOURCES = [
    (T(2), T(5), "Holman, Garfin & Silver, PNAS (2014)"),
    (T(5), T(6), "4,675 US adults, 2-4 weeks after: one survey"),
    (T(6), T(10) - 0.3, "Thompson et al., Science Advances (2019): predicts, not proves"),
    (T(13), T(15), "Garfin, Silver & Holman, Health Psychology (2020)"),
    (T(15), T(16), "Holman et al., Clinical Psychological Science (2020)"),
    (T(16), T(17), "Holman, Garfin & Silver, PNAS (2024)"),
    (T(17), T(18), "Garfin, Silver & Holman, Health Psychology (2020)"),
]


def key(t, pts):
    """Smoothly interpolated keyframes [(t, v), ...]."""
    if t <= pts[0][0]:
        return pts[0][1]
    for (a, va), (b, vb) in zip(pts, pts[1:]):
        if t <= b:
            return lerp(va, vb, smooth(prog(t, a, b)))
    return pts[-1][1]


S_BOSTON, S_LOOP, S_FEED, S_HELP, S_SHARE, S_HUMAN = T(3) - 0.5, T(6), T(10), T(13), T(16), T(18)
F = 0.7   # crossfade length (s)


def room_dim(t):
    return key(t, [(S_BOSTON - 0.3, 0.0), (S_BOSTON + 0.4, 0.86), (S_LOOP - 0.2, 0.86), (S_LOOP + 0.5, 0.88),
                   (S_FEED - 0.3, 0.88), (S_FEED + 0.4, 0.0), (S_HELP - 0.1, 0.0), (S_HELP + 0.5, 0.55),
                   (S_HUMAN - 0.2, 0.55), (S_HUMAN + 0.6, 0.0)])


def lamp_power(t):
    return key(t, [(S_HELP, 1.0), (S_HELP + 1.0, 1.15), (S_HUMAN + 0.8, 1.15), (S_HUMAN + 2.4, 1.5)])


def phone_light(t):
    return key(t, [(S_HELP, 1.0), (S_HELP + 3, 0.75), (S_HUMAN + 0.4, 0.75), (S_HUMAN + 1.6, 0.18)])


def phone_down(t):
    return 0.0   # the review: dim the phone, don't flip it ('keep the key updates')


def feed_pos(t):
    """Scroll offset (px): steady, slower and slower once 'what helps' starts, still after."""
    v0, ts = 38.0, S_HELP + 0.5
    if t < ts:
        return v0 * t
    k = 2.2   # decay time
    return v0 * ts + v0 * k * (1 - math.exp(-(t - ts) / k))


def city_lit(t):
    return key(t, [(T(20) + 0.4, 0.0), (E(20), 0.62)])


def zoom(t):
    """Slow camera: a gentle push on the phone during the feed line, otherwise a slow drift."""
    return key(t, [(0, 1.32), (4.2, 1.0), (S_BOSTON, 1.02), (S_FEED, 1.0), (S_FEED + 3.0, 1.12), (S_HELP + 1.0, 1.0),
                   (DURATION, 1.035)])


# ------------------------------------------------------------------ Lumen's path
LOOP_C, LOOP_R = (500, 960), 265


def moth_pose(t):
    """(x, y, scale, flap, spread, lit). Poses per scene, blended over F seconds at each change."""
    def orbit_phone(tt, r=95, period=5.0):
        a = tt * 2 * math.pi / period
        return (PHONE[0] + r * math.cos(a), PHONE[1] - 85 + 0.45 * r * math.sin(a), 0.9, 1.0, 1.0, 0.0)

    def pose(scene, tt):
        if scene == "phone":
            return orbit_phone(tt)
        if scene == "bars":       # perched on the 'being there' bar, listening (slow wing breathing)
            hl = BAR_H * 5.69 / 15.61 * ease_out(prog(tt, T(3) + 0.2, T(3) + 1.4))
            return (290, BAR_BASE - hl - 46, 0.8, 0.0, 0.85 + 0.08 * math.sin(tt * 1.3), 0.0)
        if scene == "loop":       # Lumen flies the loop itself
            a = math.radians(-90 + (tt - S_LOOP) * 360 / 7.0)
            r = LOOP_R - 115     # inside the circle, so he never covers a word
            return (LOOP_C[0] + r * math.cos(a), LOOP_C[1] + r * math.sin(a), 0.7, 1.0, 1.0, 0.0)
        if scene == "help":       # hovering between the phone and the lamp, undecided
            return (190 + 30 * math.sin(tt * 0.7), 1320 + 18 * math.sin(tt * 1.1), 0.9, 1.0, 1.0, 0.0)
        if scene == "lamp":       # settles by the lamp, wings open, warmed
            return (300, 1138, 0.95, 0.0, 1.15 + 0.05 * math.sin(tt * 1.0), 1.0)
        raise ValueError(scene)

    seq = [(0, "phone"), (S_BOSTON, "bars"), (S_LOOP, "loop"), (S_FEED, "phone"),
           (S_HELP, "help"), (S_HUMAN + 0.6, "lamp")]
    cur = 0
    for i, (ts, _) in enumerate(seq):
        if t >= ts:
            cur = i
    p1 = pose(seq[cur][1], t)
    if cur > 0:
        ts = seq[cur][0]
        dur = 1.6 if seq[cur][1] == "lamp" else F + 0.3
        u = smooth(prog(t, ts, ts + dur))
        if u < 1:
            p0 = pose(seq[cur - 1][1], ts)
            return tuple(lerp(a, b, u) for a, b in zip(p0, p1))
    return p1


# ------------------------------------------------------------------ panels
BAR_H = 520
BAR_BASE = 1130


def boston_panel(c, t):
    a = smooth(prog(t, S_BOSTON, S_BOSTON + F)) * (1 - smooth(prog(t, S_LOOP - 0.2, S_LOOP + 0.4)))
    if a <= 0:
        return
    # 'being there' first, then the news bar overtakes it on "...than being there"
    hl = BAR_H * 5.69 / 15.61 * ease_out(prog(t, T(3) + 0.2, T(3) + 1.4))
    hr = BAR_H * ease_out(prog(t, T(4) + 0.1, T(4) + 1.9))
    c.drawLine(150, BAR_BASE, 880, BAR_BASE, paint(CREAM, 0.5 * a, stroke=3))
    bar(c, 290, BAR_BASE, 190, hl, ROSE, a, label="being there", sub="at or near it")
    bar(c, 690, BAR_BASE, 190, hr, COLD, a, label="6+ hours a day", sub="of coverage")
    text(c, "extra stress symptoms (adjusted)", 540, 1330, 42, ROSE, 0.9 * a, italic=True)
    text(c, "one survey", 540, 1382, 42, ROSE, 0.9 * a, italic=True)


def loop_panel(c, t):
    a = smooth(prog(t, S_LOOP, S_LOOP + F)) * (1 - smooth(prog(t, S_FEED - 0.4, S_FEED + 0.3)))
    if a <= 0:
        return
    cx, cy = LOOP_C
    soft = 1.0
    c.drawCircle(cx, cy, LOOP_R, paint(CREAM, 0.12 * a, stroke=3))
    # the phone in the middle of the loop
    draw_phone(c, t, 0.8 * a, 0, x=cx, y=cy + 10, scale=1.0, screen=feed_screen_at(feed_pos(t)))
    a1 = ease_out(prog(t, T(7) + 0.2, T(7) + 1.4))
    a2 = ease_out(prog(t, T(8) + 0.2, T(8) + 1.4))
    a3 = ease_out(prog(t, T(9) + 0.6, T(9) + 2.0))
    arc_arrow(c, cx, cy, LOOP_R, -72, 14, a1, CREAM, a * soft)
    arc_arrow(c, cx, cy, LOOP_R, 46, 134, a2, CREAM, a * soft)
    arc_arrow(c, cx, cy, LOOP_R, 166, 252, a3, AMBER, a * soft)
    sw = smooth(prog(t, T(9) + 1.4, T(9) + 2.1))
    node(c, cx, cy - LOOP_R, "watching", a * smooth(prog(t, T(7), T(7) + 0.5)) * (1 - sw))
    node(c, cx, cy - LOOP_R, "more watching", a * sw * soft, color=AMBER, ring=AMBER)
    node(c, cx + LOOP_R * math.cos(math.radians(30)) - 10, cy + LOOP_R * 0.5 + 10, "stress",
         a * smooth(prog(t, T(7) + 1.0, T(7) + 1.5)))
    node(c, cx - LOOP_R * math.cos(math.radians(30)) + 10, cy + LOOP_R * 0.5 + 10, "worry",
         a * smooth(prog(t, T(8) + 1.0, T(8) + 1.5)))
    text(c, "2013  to  2016", cx, cy + LOOP_R + 150, 46, ROSE, 0.85 * a * smooth(prog(t, T(6) + 0.5, T(6) + 1.2)),
         italic=True)


def feed_screen_at(pos):
    def scr(c, r, t, a):
        hcard = 74
        off = pos % hcard
        for k in range(-1, 5):
            yy = r.top() + 8 + k * hcard - off
            c.drawRoundRect(skia.Rect.MakeXYWH(r.left() + 7, yy, r.width() - 14, hcard - 10), 8, 8,
                            paint(CREAM, 0.80 * a))
            c.drawRect(skia.Rect.MakeXYWH(r.left() + 14, yy + 8, 34, 9), paint(ROSE, 0.95 * a))
            c.drawRect(skia.Rect.MakeXYWH(r.left() + 14, yy + 24, r.width() - 34, 7), paint(DEEP, 0.45 * a))
            c.drawRect(skia.Rect.MakeXYWH(r.left() + 14, yy + 37, r.width() - 50, 7), paint(DEEP, 0.35 * a))
    return scr


def card(c, x, y, w, h, a, kind="text", check=False, veil=False, strike=False):
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), 22, 22)
    c.drawRRect(rr, paint(CREAM, 0.92 * a))
    if kind == "text":
        c.drawRect(skia.Rect.MakeXYWH(x - w / 2 + 26, y - h / 2 + 26, 70, 14), paint(ROSE, a))
        for k in range(3):
            c.drawRect(skia.Rect.MakeXYWH(x - w / 2 + 26, y - h / 2 + 58 + k * 26, w - 52 - 40 * (k == 2), 11),
                       paint(DEEP, 0.55 * a))
    elif kind == "video":
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2 + 16, y - h / 2 + 16, w - 32, h - 32), 14, 14),
                    paint(DEEP, 0.8 * a))
        tri = skia.Path()
        tri.moveTo(x - 18, y - 26)
        tri.lineTo(x + 26, y)
        tri.lineTo(x - 18, y + 26)
        tri.close()
        c.drawPath(tri, paint(CREAM, 0.8 * a))
    if veil:     # a soft cover: nothing graphic is ever shown
        p = paint(ROSE, 0.85 * a)
        c.drawRRect(rr, p)
        text(c, "graphic", x, y + 16, 50, NIGHT, a, italic=True)
    if check:
        q = skia.Path()
        q.moveTo(x + w / 2 - 60, y + h / 2 - 50)
        q.lineTo(x + w / 2 - 40, y + h / 2 - 30)
        q.lineTo(x + w / 2 - 6, y + h / 2 - 72)
        c.drawCircle(x + w / 2 - 34, y + h / 2 - 48, 38, paint(AMBER, a))
        c.drawPath(q, paint(NIGHT, a, stroke=7))
    if strike:
        c.drawLine(x - w / 2 - 10, y + h / 2 + 6, x + w / 2 + 10, y - h / 2 - 6, paint(CREAM, 0.7 * a, stroke=5))


def help_panel(c, t):
    a = smooth(prog(t, S_HELP + 0.2, S_HELP + F)) * (1 - smooth(prog(t, S_SHARE - 0.3, S_SHARE + 0.3)))
    if a <= 0:
        return
    k1 = ease_out(prog(t, T(13) + 1.9, T(13) + 2.7))
    card(c, 300, 860 + 30 * (1 - k1), 320, 200, a * k1, "text", check=t > T(13) + 2.6)
    text(c, "key updates", 300, 1020, 52, CREAM, a * k1, italic=True)
    k2 = ease_out(prog(t, T(14) + 0.2, T(14) + 1.0))
    fade = 1 - 0.55 * smooth(prog(t, T(14) + 1.2, T(14) + 2.0))
    for j in range(3):
        card(c, 690 + 14 * j, 840 + 22 * j, 300, 190, a * k2 * fade * (0.55 + 0.15 * j), "text")
    text(c, "replays", 720, 1020, 52, CREAM, a * k2 * fade, italic=True)
    k3 = smooth(prog(t, T(15), T(15) + 0.8))
    card(c, 540, 1200, 300, 190, a * k3, "video", veil=True)


def share_panel(c, t):
    a = smooth(prog(t, S_SHARE, S_SHARE + F)) * (1 - smooth(prog(t, S_HUMAN - 0.2, S_HUMAN + 0.5)))
    if a <= 0:
        return
    k1 = ease_out(prog(t, T(16) + 0.3, T(16) + 1.1))
    # a message bubble with words: the facts
    x, y = 310, 800
    bub = skia.Path()
    bub.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 170, y - 110, 340, 220), 40, 40))
    bub.moveTo(x - 120, y + 100)
    bub.lineTo(x - 150, y + 160)
    bub.lineTo(x - 70, y + 108)
    c.drawPath(bub, paint(CREAM, 0.92 * a * k1))
    for j in range(3):
        c.drawRect(skia.Rect.MakeXYWH(x - 125, y - 60 + j * 44, 250 - 60 * (j == 2), 16), paint(DEEP, 0.6 * a * k1))
    text(c, "the facts", x, y - 140, 56, AMBER, a * k1, italic=True)
    k2 = ease_out(prog(t, T(16) + 1.4, T(16) + 2.1))
    veil = smooth(prog(t, T(17) + 0.3, T(17) + 1.0))
    card(c, 720, 800, 290, 200, a * k2 * (0.6 + 0.4 * veil), "video", strike=t > T(16) + 1.9 and veil < 0.5,
         veil=veil > 0.5)
    text(c, "the footage", 720, 660, 56, CREAM, 0.7 * a * k2 * (1 - veil), italic=True)
    text(c, "held back", 720, 660, 56, AMBER, a * veil, italic=True)


def helpline(c, t):
    a = smooth(prog(t, T(18) + 0.4, T(18) + 1.2))
    if a > 0:
        text(c, "Struggling? You're not alone.", 540, 1352, 46, CREAM, 0.9 * a, italic=True)
        text(c, "Free help: findahelpline.com", 540, 1408, 46, CREAM, 0.9 * a, italic=True)


# ------------------------------------------------------------------ the frame
def draw_world(c, t):
    z = zoom(t)
    c.save()
    focus = PHONE if (S_FEED - 0.5 < t < S_HELP + 1.2 or t < S_BOSTON) else (540, 960)
    c.translate(focus[0], focus[1])
    c.scale(z, z)
    c.translate(-focus[0], -focus[1])
    scr = feed_screen_at(feed_pos(t))
    draw_room(c, t, lamp_power(t), phone_light(t), phone_down(t), city_lit(t), screen=scr)
    # "It's a loop": a thin amber orbit around the phone, the motif the loop diagram pays off later
    lp_ = ease_out(prog(t, T(1) + 0.9, T(1) + 2.2)) * (1 - smooth(prog(t, S_BOSTON - 0.4, S_BOSTON + 0.2)))
    if lp_ > 0:
        r = skia.Rect.MakeLTRB(PHONE[0] - 110, PHONE[1] - 85 - 50, PHONE[0] + 110, PHONE[1] - 85 + 50)
        pth = skia.Path()
        pth.addArc(r, -90, 359 * lp_)
        c.drawPath(pth, paint(AMBER, 0.75, stroke=4))
    c.restore()
    dim(c, room_dim(t))
    boston_panel(c, t)
    loop_panel(c, t)
    help_panel(c, t)
    share_panel(c, t)
    x, y, s, fl, sp, lt = moth_pose(t)
    c.save()     # Lumen lives in the room: same camera as the room
    c.translate(focus[0], focus[1])
    c.scale(z, z)
    c.translate(-focus[0], -focus[1])
    if lt > 0.3:
        glow(c, x, y, 120, AMBER, 0.12 * lt)
    draw_moth(c, x, y, t, s, fl, sp, lit=lt)
    c.restore()
    vignette(c, 0.5)


def draw_frame(c, t):
    draw_world(c, t)
    for k, cap in enumerate(CAPTIONS):
        cap.draw(c, t, y=360, first=(k == 0))
    for (a, b, s) in SOURCES:
        if a <= t < b:
            al = smooth(prog(t, a, a + 0.3)) * (1 - smooth(prog(t, b - 0.15, b)))
            source_line(c, s, 568, al)
    helpline(c, t)
    # loop seam: the last moment dissolves into frame 0
    u = smooth(prog(t, DURATION - 0.45, DURATION))
    if u > 0:
        c.saveLayerAlpha(None, int(255 * u))
        draw_world(c, 0.0)
        CAPTIONS[0].draw(c, 0.0, y=360, first=True)
        c.restore()
    draw_grain(c, 0.06)


# ================================================================== sound
MUSIC_KEYS = [(0, "minor"), (S_HELP - 0.5, "major")]
SFX = [
    (T(3) + 0.2, "rise"), (T(4) + 0.1, "rise"),
    (T(7) + 0.0, "tone"), (T(7) + 1.0, "tone_low"), (T(8) + 1.0, "tone_low"), (T(9) + 1.4, "tone"),
    (T(13) + 1.9, "slide"), (T(13) + 2.6, "tone"), (T(14) + 0.2, "slide"), (T(15) + 0.1, "slide"),
    (T(16) + 0.3, "slide"), (T(16) + 1.4, "slide"), (T(17) + 0.4, "tone_low"),
    (S_HUMAN + 1.6, "warm"),
    (T(20) + 0.9, "window"), (T(20) + 1.5, "window"), (T(20) + 2.2, "window"),
]
