"""COULD YOU SURVIVE? #02 — Everest. Subject Zero (her) spawns on the summit, 8,849 m, with no time to adapt.

Who it is for: curious 16–30s who have heard of the "death zone" and never knew what the air up there does to you.
The single promise: you will know how long you would actually keep your head on top of Everest, and the one thing
about that rock nobody told you.

Three hooks, three types (the strongest true one is kept):
  1. Statement + number (KEPT): "You spawn on top of Everest." + 8,849 m on screen, O2 "??" in the HUD. Names the place
     in 6 words, the search keyword is on screen and spoken, and the wow number (a third of the oxygen) lands by 8 s.
  2. Question: "How long would you last on Everest's summit?" (weaker: a question we answer anyway, no image of the state)
  3. Contrast: "Climbers take weeks to adapt. You get zero." (true, but needs the place named first; used as line n5)

Facts and sources: subjectzero/research/cys02_facts.md (every number below is there).
Main assumption, said in the voice: she spawns, so she has not adapted for weeks like real climbers.
Running gags: the lab's deadpan voice ("Noted."), her NOPE in a voice far too deep for her that does more damage each
time (1: a cornice of snow breaks off the ridge; 2: an avalanche runs down the next face; 3: the whole snow cap blows
off the summit and shows the fossil seabed under her boots), the rubber duck that is never in danger, the respawn.
Continuity: in #01 she was stuck in the ocean at Point Nemo; the final twist is that this summit is old seafloor.

    python3 szvoice.py cys02 && python3 listen.py cys02     # voices + listening gate
    python3 sz2render.py cys02_pic [--sheet t ...]           # picture
    python3 cys02_audio.py                                   # music, effects, mix -> out/SubjectZero_CYS02_Everest.mp4
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EPNAME = "cys02"
FPS = 24
BPM = 88
DURATION = 24 * 4 * 60 / BPM      # 24 bars of 4/4 at 88 BPM = 65.45 s

SPEAKERS = {
    "N": dict(voice="am_michael", speed=1.04),
    "HERO": dict(voice="af_bella", speed=1.08, gain=1.0),
    "LAB": dict(voice="bm_george", speed=0.96, gain=0.85,
                chain="highpass=f=320,lowpass=f=3300,acompressor=threshold=-20dB:ratio=6:attack=5:release=60,"
                      "aeval='tanh(2.2*val(0))/tanh(2.2)'"),
}
# her NOPE: the deepest natural voice (am_onyx), a little lower still, comes out of her. Each one 3 dB+ louder.
NOPE = "rubberband=pitch={p}:formant=preserved,acompressor=threshold=-18dB:ratio=4,volume={v}dB"
LINE_FX = {
    "n10": dict(voice="am_onyx", speed=0.95, chain=NOPE.format(p=0.86, v=1)),
    "n12": dict(voice="am_onyx", speed=1.0, chain=NOPE.format(p=0.86, v=4)),
    "n21": dict(voice="am_onyx", speed=1.0, chain=NOPE.format(p=0.86, v=7) + ",volume='if(gte(t,0.86),2.8,1)':eval=frame"),
}

# key, target start (s), speaker, what is said (numbers spelled out: the gate compares words)
VOICE_LINES = [
    ("n1", 0.0, "N", "You spawn on top of Everest."),
    ("n2", 1.8, "N", "Eight thousand, eight hundred forty-nine meters up."),
    ("n3", 4.6, "N", "Every breath has about a third of the oxygen you're used to."),
    ("n4", 8.3, "HERO", "Okay. Just breathe."),
    ("n5", 9.7, "N", "Real climbers adapt for weeks. You got zero."),
    ("n6", 13.2, "LAB", "Lab here. We skipped that part. Saves time."),
    ("n7", 16.4, "N", "In January, it averages minus thirty-six."),
    ("n8", 19.2, "N", "But the cold is not what gets you first."),
    ("n9", 21.4, "N", "The wind can blow over a hundred miles an hour."),
    ("n10", 24.4, "HERO", "Nope."),
    ("n11", 25.6, "N", "In that wind, bare skin can freeze in under five minutes."),
    ("n12", 29.2, "HERO", "Nope!"),
    ("n13", 30.4, "N", "The duck? It's rubber. It doesn't even need air."),
    ("n14", 33.0, "LAB", "Noted. Lucky duck."),
    ("n15", 34.6, "N", "The real clock is in your head. And wait till you see the rock."),
    ("n16", 38.8, "N", "So how long would you last?"),
    ("n17", 41.6, "N", "About one to three minutes of clear thinking."),
    ("n18", 44.6, "LAB", "Noted."),
    ("n19", 45.6, "N", "After that, you're too confused to climb down."),
    ("n20", 48.0, "N", "Last time, you escaped the ocean. This rock was sea floor."),
    ("n20b", 52.4, "N", "It still holds sea fossils, over four hundred million years old."),
    ("n21", 56.2, "HERO", "Nope. Nope. NOPE!"),
    ("n22", 58.0, "N", "Next spawn: Pompeii, the Mariana Trench, or the Moon?"),
    ("n23", 61.2, "HERO", "Anywhere with air."),
    ("n24", 62.4, "LAB", "Respawning in three... two..."),
]
