"""COULD YOU SURVIVE? #01 — Point Nemo. Subject Zero (her) spawns at the farthest point from land.

Facts and sources: research_notes/Étude de marché chaîne IA/point_nemo_facts.md (every number below is there).
Running gags: the lab's deadpan voice ("Noted."), her NOPE in a voice far too deep for her that does more damage
each time, and the rubber duck that is never in any danger.

    python3 szvoice.py nemo01 && python3 listen.py nemo01     # voices + listening gate
    python3 nemo_render.py nemo01 [--sheet t ...]             # picture
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EPNAME = "nemo01"
FPS = 24
DURATION = 64.5
BPM = 96

SPEAKERS = {
    "N": dict(voice="am_michael", speed=1.04),
    "HERO": dict(voice="af_bella", speed=1.08, gain=1.0),
    "LAB": dict(voice="bm_george", speed=0.96, gain=0.85,
                chain="highpass=f=320,lowpass=f=3300,acompressor=threshold=-20dB:ratio=6:attack=5:release=60,"
                      "aeval='tanh(2.2*val(0))/tanh(2.2)'"),
}
# her NOPE: her own voice, pitched far down (formants follow: the joke is that this sound comes out of her)
# her NOPE (v2, 28 Oct evening: "le nope est pas ouf"): no more pitched-down robot. The deepest natural voice
# (am_onyx), a little lower still, comes out of her: L1 a dry deadpan "Nope.", L2 a punchier "Nope!", L3 a
# rapid-fire "Nope. Nope. Nope. NOPE!" that grows with each word. Echo, boom and damage go in the mix, after the
# word (an effect on top of a word masks it).
NOPE = "rubberband=pitch={p}:formant=preserved,acompressor=threshold=-18dB:ratio=4,volume={v}dB"
LINE_FX = {
    "n13": dict(voice="am_onyx", speed=0.95, chain=NOPE.format(p=0.85, v=1)),
    "n15": dict(voice="am_onyx", speed=1.0, chain=NOPE.format(p=0.85, v=4)),
    "n23": dict(voice="am_onyx", speed=1.0, chain=NOPE.format(p=0.85, v=5)),
}

# key, target start (s), speaker, what is said (numbers spelled out: the gate compares words)
VOICE_LINES = [
    ("n1", 0.0, "N", "You spawn at Point Nemo."),
    ("n2", 1.6, "N", "The farthest point from land on Earth."),
    ("n3", 3.9, "N", "Nearest land: almost 2,700 kilometers."),
    ("n4", 7.0, "N", "Two tiny islands... and one off Antarctica."),
    ("n5", 10.6, "N", "Sometimes, the nearest humans are in space."),
    ("n6", 13.6, "HERO", "Hey! Down here!"),
    ("n7", 15.0, "LAB", "Lab here. They can't hear you."),
    ("n8", 17.4, "N", "The water is around seven degrees."),
    ("n9", 19.7, "N", "In the first minute, the cold makes you gasp."),
    ("n10", 22.4, "N", "And that's not even the scariest thing out here."),
    ("n11", 25.2, "N", "Swim for it? At world-record pace, non-stop... eighteen days."),
    ("n13", 29.5, "HERO", "Nope."),
    ("n14", 30.8, "N", "Besides, after about ten minutes, your arms quit."),
    ("n15", 33.9, "HERO", "Nope!"),
    ("n16", 36.9, "N", "So how long would you last?"),
    ("n17", 40.2, "N", "In water this cold, about one to three hours."),
    ("n18", 43.4, "N", "The duck? Rubber ducks lost at sea have floated for years."),
    ("n19", 46.6, "LAB", "Noted."),
    ("n20", 47.7, "N", "Because Point Nemo is where spacecraft go to die."),
    ("n21", 50.7, "N", "More than two hundred and sixty were dropped out here."),
    ("n22", 53.7, "N", "Next, around 2030: that space station."),
    ("n23", 56.9, "HERO", "Nope. Nope. NOPE!"),
    ("n24", 58.7, "N", "Next spawn: the Sahara, Ancient Rome, or Everest?"),
    ("n25", 62.0, "LAB", "Respawning in three... two..."),
]
