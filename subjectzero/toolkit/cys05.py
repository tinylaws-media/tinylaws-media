"""COULD YOU SURVIVE? #05 — Mars, no suit. Subject Zero (her) spawns on the red plain in her hoodie, nothing else.

Who it is for: curious 16–30s who have seen a hundred "Mars colony" videos and never asked what the air there does
to a body in the first seconds.
The single promise: you will know what Mars's air (or lack of it) does to you, second by second, how long you'd
last, and one thing about Mars you did not expect.

Three hooks, three types (the strongest true one is kept):
  1. Statement + number (KEPT): "You spawn on Mars." + "No suit. Just the hoodie." + "Less than one percent of
     Earth's pressure" by ~5 s, HUD "YOU'D LAST ?? SECONDS". Names the place in 4 words; the wow number is the
     first fact.
  2. Weird physics: "On Mars, your spit boils." (true and strong, but it is the 18 s re-hook; spending it at 0 s
     leaves the middle flat)
  3. Contrast: "The red planet has blue sunsets." (true, shareable, but no danger: it becomes the second payoff)

Facts and sources: subjectzero/research/cys05_facts.md (every number below is there).
Main assumption, said in the voice: an unprotected person at Mars's average surface pressure (about 0.6 kPa,
effectively a vacuum for the body). The answer is an estimate from vacuum exposure data: about 15 s of
consciousness (NASA accident, human reports, Buckey 2006), about 90 s within which animals reliably recovered
(Brooks AFB dogs, 1965). We never show suffering: she just keeps reacting.
Running gags: the lab's deadpan voice ("Noted."), her NOPE in a voice far too deep for her that does more damage each
time (1: the red dust blows off the plain in a ring and the dust devil from frame 0 is flung away; 2: the old lander
behind her loses its dish antenna, which spins off over the horizon — after the lab says the signal takes up to
22 minutes; 3: the mesa behind her collapses and a wall of dust rolls in from both sides), the rubber duck that is
never in danger ("It doesn't breathe"), the respawn.
Continuity: #04 asked "Next spawn: Mars, a medieval farm, or Pompeii?" She got Mars.

    python3 szvoice.py cys05 && python3 listen.py cys05     # voices + listening gate
    python3 sz2render.py cys05_pic [--sheet t ...]           # picture
    python3 cys05_audio.py                                   # music, effects, mix -> out/SubjectZero_CYS05_Mars.mp4
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EPNAME = "cys05"
FPS = 24
BPM = 99
DURATION = 27 * 4 * 60 / BPM      # 27 bars of 4/4 at 99 BPM = 65.45 s

SPEAKERS = {
    "N": dict(voice="am_michael", speed=1.09),
    "HERO": dict(voice="af_bella", speed=1.08, gain=1.0),
    "LAB": dict(voice="bm_george", speed=0.99, gain=0.85,
                chain="highpass=f=320,lowpass=f=3300,acompressor=threshold=-20dB:ratio=6:attack=5:release=60,"
                      "aeval='tanh(2.2*val(0))/tanh(2.2)'"),
}
# her NOPE: the deepest natural voice (am_onyx), a little lower still, comes out of her. Each one 3 dB+ louder.
NOPE = "rubberband=pitch={p}:formant=preserved,acompressor=threshold=-18dB:ratio=4,volume={v}dB"
LINE_FX = {
    "n17": dict(overlap=-0.45),          # 0.65 s of silence before the answer
    "n8": dict(overlap=0.1), "n11": dict(overlap=0.1), "n12": dict(overlap=0.1), "n13": dict(overlap=0.1),
    "n21": dict(overlap=0.1), "n3": dict(overlap=0.1), "n2": dict(overlap=0.1),
    "n10": dict(voice="am_onyx", speed=0.95, chain=NOPE.format(p=0.86, v=-2)),
    "n15": dict(voice="am_onyx", speed=1.0, chain=NOPE.format(p=0.86, v=4)),
    "n19": dict(voice="am_onyx", speed=1.0, chain=NOPE.format(p=0.86, v=8) + ",volume='if(gte(t,0.86),2.8,1)':eval=frame"),
}

# key, target start (s), speaker, what is said (numbers spelled out: the gate compares words)
VOICE_LINES = [
    ("n1", 0.0, "N", "You spawn on Mars."),
    ("n2", 1.3, "N", "No suit. Just the hoodie."),
    ("n3", 3.0, "N", "The air? Under one percent of Earth's pressure. Mostly carbon dioxide."),
    ("n5", 7.6, "HERO", "So I hold my breath?"),
    ("n6", 9.0, "N", "Bad idea. Your lungs could tear."),
    ("n7", 11.0, "LAB", "Lab here. Breathe out. Noted."),
    ("n8", 13.4, "N", "Breathe out. Now it gets weird."),
    ("n9", 15.6, "N", "The water on your tongue starts to boil."),
    ("n10", 18.2, "HERO", "Nope."),
    ("n11", 19.4, "N", "It's not hot. The air is just too thin."),
    ("n12", 21.8, "N", "You'd need ten times more air. Even the deepest crater falls short."),
    ("n13", 26.0, "N", "The duck is fine. It doesn't breathe."),
    ("n14", 28.4, "LAB", "Lab here. Rescue is coming. Signal delay: up to twenty-two minutes."),
    ("n15", 32.6, "HERO", "Nope!"),
    ("n16", 33.8, "N", "How long would you last? Less than this video. And it's not the strangest part."),
    ("n17", 39.4, "N", "About fifteen seconds before you pass out. About ninety to get rescued."),
    ("n18", 43.8, "LAB", "Noted. Fifteen seconds."),
    ("n19", 45.4, "HERO", "Nope. Nope. NOPE!", "Nope, nope, nope!"),
    ("n20", 47.4, "N", "In the sixties, a NASA test subject felt his spit boil in a vacuum chamber. He recovered."),
    ("n21", 53.4, "N", "The strangest part? Sunsets here are blue."),
    ("n22", 56.2, "N", "The dust lets blue light through, near the sun."),
    ("n23", 59.2, "N", "Next spawn: a medieval farm, Pompeii, or the Mariana Trench?"),
    ("n24", 62.2, "HERO", "Somewhere with air."),
    ("n25", 63.2, "LAB", "Respawning in three... two..."),
]
