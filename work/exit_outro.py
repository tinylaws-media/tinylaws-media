"""THE EXIT MANUAL — the signature ending, LOCKED (owner, 26 Oct 2026: "the logo animation exactly as in v5, at the end
of every video, always the same animation").

Taken from exit_ep005.py (Transmission 001, v5, approved) and frozen here. Every episode ends with this module,
unchanged: the 12 fragments of the Build the Commons logo (exit_logo.py, owner's SVGs in logo/) fly in one by one
from far away and converge, lock 0.25 s before the voice says "build the commons.", then the logo beats like a heart
(lub-dub at 64/min, in sync with the heartbeat in the score) under "build the commons." / THE EXIT MANUAL; then it
keeps beating while it falls back into the depth, to a point. Same fragments, same paths, same timing, same camera,
same music cues in every episode. Do not edit the numbers below: change what comes BEFORE the ending instead.

Everything is placed relative to ONE time, t_sign = when the narrator starts "build the commons." An episode:
- ends its LINES with ("sign", "build the commons.", 0.6) and, if it loops, one short last line after it
  (the loop line starts FALL_LEAD = 1.667 s after t_sign, which the 0.6 s pause gives with the usual voice);
  CAPS["sign"] = [None] (the panel shows the words);
- ends its last own scene at start(t_sign) and adds scenes():  (start(t_sign), fall_at(t_sign) - 0.2, outro.scene)
  and (fall_at(t_sign) - 0.2, end, <its own loop scene that calls outro.fall(X, t, t_sign) first>);
- uses cam(t, t_sign, part) for the camera in those two scenes, rain_level / dust_level for the background layers,
  plan(...) to merge the music cues into its music_plan(), dip(...) for music_dips() and subtitle(...) for the
  "build the commons." subtitle.
The lines spoken during the 4.35 s fly-in (v5: "We need you awake. We build what comes next, together.") are the
episode's closing words; they change, the picture does not.
"""
import math

import numpy as np

from exit_engine import clamp01, prog, lerp, ease_out, ease_in_out
from exit_look2 import CAP_CX
from exit_look3 import Cam, kin_text, smooth
from exit_logo import Logo

# ------------------------------------------------------------------ frozen numbers (v5, seconds from t_sign)
V5_SIGN = 61.579              # t_sign in v5: the camera drift is replayed from v5's clock, so it is identical
FLY_LEAD = 4.352              # the first fragment leaves 4.352 s before "build the commons." (v5: end of "stop" + 0.05)
LOCK_LEAD = 0.25              # every fragment has locked 0.25 s before the word
FLY = 1.05                    # each fragment's flight (s)
FALL_LEAD = 1.667             # the fall into the depth is timed from t_sign + 1.667 (v5: start of the loop line)
CLIMB_LEAD = 3.352            # the chromatic climb in the score starts 3.352 s before the word, lands on it
BEAT_BACK = 3.302             # the half-time beat comes back 3.302 s before the word and stops 0.35 s before it
INTENS_LEAD = 3.802           # the score swells from 3.802 s before the word (intensity 0.45 -> 0.98)
DUST_IN = (3.802, 2.702)      # the near dust comes back between these leads
CAM_K = {"world": 9, "loop": 10}   # v5 scene indices (the camera drift's phase)
LOOP_END = 4.881              # v5 last scene's end, from t_sign (DURATION + 1)
HEART_BPM = 64                # the logo's heartbeat = the score's tempo (exit_score5.BPM)
HEART = 60.0 / HEART_BPM
LOGO = Logo()
LOGO_CX, LOGO_CY, LOGO_PX = CAP_CX, 750, 300  # centre and radius (px) of the formed logo: x 185..785, y 450..1050
_LR = np.random.default_rng(55)
# each fragment's far starting point: outward along its own direction, swung round, far in depth
FRAG_FROM = [(LOGO.pieces[i][2] + _LR.uniform(-0.7, 0.7), _LR.uniform(2600, 4200), _LR.uniform(4200, 6800),
              _LR.uniform(-2.6, 2.6)) for i in range(len(LOGO.pieces))]
for _k in LOGO.order[:2]:                     # the first two come in close to the camera: big, visible at once
    FRAG_FROM[_k] = (FRAG_FROM[_k][0], 1500.0, 2300.0, FRAG_FROM[_k][3])
STARS = [(x, y, r_, a_) for x, y, r_, a_ in zip(*[np.random.default_rng(3).uniform(lo, hi, 40) for lo, hi in
                                                    ((60, 900), (380, 1120), (1.2, 2.6), (0.25, 0.7))])]


def start(t_sign):
    """When the ending takes over the picture (the first fragment leaves)."""
    return t_sign - FLY_LEAD


def fall_at(t_sign):
    return t_sign + FALL_LEAD


def _bump(t, a, d=0.4):
    u = prog(t, a, a + d)
    return math.sin(math.pi * u) ** 2


def frag_times(t_sign):
    """When each fragment (in arrival order) leaves and locks in. All locked 0.25 s before 'build the commons.'"""
    t0, t_lock = start(t_sign), t_sign - LOCK_LEAD
    st = (t_lock - FLY - t0) / (len(LOGO.pieces) - 1)
    return [(t0 + k * st, t0 + k * st + FLY) for k in range(len(LOGO.pieces))]


def heart_pulse(t, t_sign):
    """0..1 lub-dub envelope: a strong beat then a softer one 0.30 s later, every HEART s from t_sign."""
    if t < t_sign - 0.05:
        return 0.0
    k = math.floor((t - t_sign) / HEART)
    x = t - (t_sign + k * HEART)

    def bump_(u):                               # fast smooth rise (40 ms), soft fall (no flash)
        if u < 0:
            return 0.0
        return (1 - math.exp(-u / 0.018)) * math.exp(-u / 0.13)
    return clamp01(bump_(x) * 1.25 + 0.55 * bump_(x - 0.30) * 1.25)


def draw_logo(X, t, t_sign, alpha=1.0, scale=1.0):
    """The fragments arrive one by one from depth and converge; once formed, the logo beats like a heart."""
    if alpha <= 0:
        return
    c = X.c
    times = frag_times(t_sign)
    cam = Cam(cx=LOGO_CX, cy=LOGO_CY, x=0, y=0, z=0)
    k_unit = LOGO_PX / LOGO.R * scale
    formed = prog(t, times[-1][1], times[-1][1] + 0.2)
    hp_ = heart_pulse(t, t_sign)
    beat_s = 1 + 0.095 * hp_
    # the camera eases in as the logo forms, and rolls very slightly back to level
    roll = 0.06 * (1 - smooth(prog(t, times[0][0], times[-1][1])))
    c.save()
    c.translate(LOGO_CX, LOGO_CY)
    c.rotate(math.degrees(roll))
    c.translate(-LOGO_CX, -LOGO_CY)
    # soft green halo behind the logo: grows as it forms, breathes with the heart (alpha change is small)
    halo = 0.10 * formed + 0.10 * hp_ * formed
    if halo > 0:
        c.drawCircle(LOGO_CX, LOGO_CY, LOGO_PX * 1.15 * beat_s, X.paint("green", halo * alpha, blur=90))
    # a thin ring (the owner's white disc, reduced to its outline in our palette)
    ring_a = 0.35 * formed * alpha
    if ring_a > 0:
        c.drawCircle(LOGO_CX, LOGO_CY, LOGO_PX * 1.12 * beat_s, X.paint("white", ring_a * 0.6, stroke=2.5))
        c.drawCircle(LOGO_CX, LOGO_CY, LOGO_PX * 1.12 * beat_s, X.paint("green", ring_a * 0.5, stroke=6, blur=6))
    # a thin ring ripples outward on each beat (a shape moving out, not a brightness flash)
    if t >= t_sign:
        kb = math.floor((t - t_sign) / HEART)
        for dk, (dt, g) in enumerate(((0.0, 1.0), (0.30, 0.6))):
            x = t - (t_sign + kb * HEART) - dt
            if 0 <= x < 0.9:
                u = x / 0.9
                c.drawCircle(LOGO_CX, LOGO_CY, LOGO_PX * (1.15 + 0.45 * ease_out(u, 2)),
                             X.paint("green", 0.28 * g * (1 - u) * alpha * formed, stroke=3))
    for n_, i in enumerate(LOGO.order):
        path, (fx, fy), ang = LOGO.pieces[i]
        ta, tb = times[n_]
        if t < ta:
            continue
        u = clamp01((t - ta) / (tb - ta))
        e = 1 - (1 - u) ** 3.2                                 # fast from far, gentle landing
        th, rad, z0, spin = FRAG_FROM[i]
        tx, ty = fx * k_unit * beat_s, fy * k_unit * beat_s
        trail = [0.0] if u >= 1 else [0.0, 0.05, 0.1, 0.16]   # motion trail while flying (ghosts, dim)
        for j, dt in enumerate(trail):
            ee = 1 - (1 - clamp01(u - dt * 1.4)) ** 3.2
            wx = lerp(tx + math.cos(th) * rad, tx, ee)
            wy = lerp(ty + math.sin(th) * rad, ty, ee)
            wz = lerp(z0, 1100, ee)
            sx, sy, kk = cam.p(wx, wy, wz)
            fade = clamp01((7600 - wz) / 2500)
            a = alpha * fade * (1.0 if j == 0 else 0.22 * (1 - j / len(trail)))
            if a <= 0.01:
                continue
            c.save()
            c.translate(sx, sy)
            c.scale(kk * k_unit * beat_s, kk * k_unit * beat_s)
            c.rotate(math.degrees(spin * (1 - ee)))
            c.translate(-fx, -fy)
            if j == 0:
                lock = _bump(t, tb - 0.05, 0.5) if u >= 0.95 else 0.0
                c.drawPath(path, X.paint("green", (0.30 + 0.25 * lock + 0.25 * hp_ * formed) * a, blur=3.5 / kk / k_unit))
            c.drawPath(path, X.paint("white", a))
            c.restore()
    # the centre star appears once the ring of fragments is closed
    if LOGO.star is not None and formed > 0:
        sa = alpha * formed
        c.save()
        c.translate(LOGO_CX, LOGO_CY)
        ss = k_unit * beat_s * (0.6 + 0.4 * smooth(formed)) * (1 + 0.08 * hp_)
        c.scale(ss, ss)
        c.rotate(25 * (1 - smooth(formed)))
        c.drawPath(LOGO.star, X.paint("green", 0.7 * sa, blur=2.5 / ss * 3))
        c.drawPath(LOGO.star, X.paint("green", sa))
        c.restore()
    c.restore()


def scene(X, t, t_sign):
    """From start(t_sign) to fall_at(t_sign) - 0.2: night stars dim, the fragments converge, the logo beats under
    the signature panel."""
    t0 = start(t_sign) - 0.05                    # v5: the stars start dimming 0.05 s before the first fragment
    a = ease_in_out(prog(t, t0, t0 + 1.2))
    for (x, y, r_, a_) in STARS:
        X.c.drawCircle(x, y, r_, X.paint("white", (1 - a * 0.6) * a_))
    draw_logo(X, t, t_sign)
    fa = fall_at(t_sign)
    sa = prog(t, t_sign - 0.05, t_sign + 0.3) * (1 - prog(t, fa - 0.55, fa - 0.22))
    if sa > 0:
        X.panel(110, 1190, 750, 200, alpha=0.8 * sa, border=None)
        kin_text(X, "build the commons.", CAP_CX, 1290, 64, t_sign - 0.05, "green", kind="sign", dur=0.45, glow=0.5,
                 track0=0.12, rise=14)
        X.text("THE EXIT MANUAL", CAP_CX, 1358, 40, "white", kind="sansm", alpha=0.8 * prog(t, t_sign + 0.3,
                                                                                            t_sign + 0.6))


def fall(X, t, t_sign):
    """The logo keeps beating while it falls back into the depth, to a point (gone at fall_at + 1.4 s). Call it
    first in the episode's last scene; the episode then draws its own loop-back image."""
    fa = fall_at(t_sign)
    u = ease_in_out(prog(t, fa + 0.7, fa + 1.4))
    la = 1 - prog(t, fa + 1.05, fa + 1.4)
    if la > 0:
        X.c.save()
        X.c.translate(LOGO_CX, LOGO_CY)
        z = lerp(1.0, 0.12, u)
        X.c.scale(z, z)
        X.c.translate(-LOGO_CX, -LOGO_CY)
        draw_logo(X, t, t_sign, alpha=la)
        X.c.restore()


def cam(t, t_sign, part):
    """v5's slow camera for the two ending scenes ("world": the convergence, "loop": the fall), replayed on v5's
    clock so the drift is the same in every episode. Returns (zoom, dx, dy, roll) like the episode's cam_move."""
    if part == "world":
        a, b = start(t_sign), fall_at(t_sign) - 0.2
    else:
        a, b = fall_at(t_sign) - 0.2, t_sign + LOOP_END
    k = CAM_K[part]
    t5 = t - t_sign + V5_SIGN
    u = smooth(prog(t, a, b))
    z = 1.0 + 0.035 * u
    dx = 10 * math.sin(t5 * 0.21 + k * 1.3)
    dy = 7 * math.sin(t5 * 0.17 + k * 0.7)
    roll = 0.35 * math.sin(t5 * 0.13 + k)
    return z, dx, dy, roll


def rain_level(t, t_sign, before):
    """Data-rain alpha during the ending: settles at 0.3 (from the episode's level `before` at start), then comes
    back up by 0.5 as the logo falls."""
    t0, fa = start(t_sign), fall_at(t_sign)
    return lerp(before, 0.3, prog(t, t0, t0 + 1.2)) + 0.5 * prog(t, fa - 0.2, fa + 0.8)


def dust_level(t, t_sign, before):
    """Near-dust alpha during the ending: from the episode's level `before` back to 1.0 as the fragments arrive."""
    return before + (1.0 - before) * prog(t, t_sign - DUST_IN[0], t_sign - DUST_IN[1])


def plan(ep_plan, t_sign, duration):
    """Merge the ending's music cues into an episode's music plan (exit_score5.score): the episode's intensity
    points and beat-off spans stop where the ending's begin; anchor, climb and heart are the ending's."""
    fa = fall_at(t_sign)
    p = dict(ep_plan)
    p["anchor"] = t_sign                                     # a downbeat lands on "build the commons."
    p["intensity"] = [q for q in ep_plan.get("intensity", []) if q[0] < t_sign - INTENS_LEAD] + [
        (t_sign - INTENS_LEAD, 0.45), (t_sign - 0.1, 0.98), (t_sign + 0.6, 0.6), (fa, 0.45), (duration, 0.3)]
    p["beat_off"] = [(a, min(b, t_sign - BEAT_BACK)) for (a, b) in ep_plan.get("beat_off", [])
                     if a < t_sign - BEAT_BACK] + [(t_sign - 0.35, duration + 1)]
    p["climb"] = (t_sign - CLIMB_LEAD, t_sign)
    p["heart"] = (t_sign, duration + 0.6, fa + 0.9)
    p["hits"] = list(ep_plan.get("hits", [])) + [t_sign]
    p["risers"] = list(ep_plan.get("risers", [])) + [(t_sign, 3.0)]
    return p


def dip(t_sign, t_sign_end):
    """The music dips a further 3 dB under the signature line."""
    return (t_sign - 0.1, t_sign_end + 0.2)


def subtitle(t_sign):
    return (t_sign - 0.04, fall_at(t_sign) - 0.04, "build the commons.")
