"""COULD YOU SURVIVE? #03 — Death Valley. Subject Zero (her) spawns on the Badwater salt flat in July, one bottle of
water in her hand.

Who it is for: curious 16–30s who know Death Valley is "the hottest place on Earth" and have never pictured a day there.
The single promise: you will know how long one bottle of water actually buys you in Death Valley in July, and the
real story behind the name.

Three hooks, three types (the strongest true one is kept):
  1. Statement + number (KEPT): "You spawn in Death Valley." + 134°F coming on screen, "YOU'D LAST ?? DAYS" in the HUD.
     Names the place in 5 words, the search keyword is on screen and spoken, the wow number lands by 5 s.
  2. Question: "How long would one bottle of water last you in Death Valley?" (weaker: long, and gives away the bottle)
  3. Contrast: "The ground here gets hotter than your coffee." (true-ish but needs care: coffee is served 160–185°F; cut)

Facts and sources: subjectzero/research/cys03_facts.md (every number below is there).
Main assumption, said in the voice: she rests in shade (the military estimate's condition), one litre of water.
Running gags: the lab's deadpan voice ("Noted."), her NOPE in a voice far too deep for her that does more damage each
time (1: the salt crust cracks in a ring around her boots; 2: a dust devil spins up beside her and rips across
the flat, flinging salt plates; 3: the whole salt flat shatters into hexagon plates that flip up and the heat haze
breaks like glass), the rubber duck that is never in
danger (it floats on the mirage lake, the only "water" around), the respawn.
Continuity: in #02 she was on the roof of the world; now she is 86 m below sea level.

    python3 szvoice.py cys03 && python3 listen.py cys03     # voices + listening gate
    python3 sz2render.py cys03_pic [--sheet t ...]           # picture
    python3 cys03_audio.py                                   # music, effects, mix -> out/SubjectZero_CYS03_DeathValley.mp4
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EPNAME = "cys03"
FPS = 24
BPM = 96
DURATION = 26 * 4 * 60 / BPM      # 26 bars of 4/4 at 96 BPM = 65.0 s

SPEAKERS = {
    "N": dict(voice="am_michael", speed=1.05),
    "HERO": dict(voice="af_bella", speed=1.08, gain=1.0),
    "LAB": dict(voice="bm_george", speed=0.96, gain=0.85,
                chain="highpass=f=320,lowpass=f=3300,acompressor=threshold=-20dB:ratio=6:attack=5:release=60,"
                      "aeval='tanh(2.2*val(0))/tanh(2.2)'"),
}
# her NOPE: the deepest natural voice (am_onyx), a little lower still, comes out of her. Each one 3 dB+ louder.
NOPE = "rubberband=pitch={p}:formant=preserved,acompressor=threshold=-18dB:ratio=4,volume={v}dB"
LINE_FX = {
    "n16": dict(overlap=-0.45),          # 0.65 s of silence before the answer
    "n7": dict(voice="am_onyx", speed=0.95, chain=NOPE.format(p=0.86, v=1)),
    "n11": dict(voice="am_onyx", speed=1.0, chain=NOPE.format(p=0.86, v=4)),
    "n19": dict(voice="am_onyx", speed=1.0, chain=NOPE.format(p=0.86, v=7) + ",volume='if(gte(t,0.86),2.8,1)':eval=frame"),
}

# key, target start (s), speaker, what is said (numbers spelled out: the gate compares words)
VOICE_LINES = [
    ("n1", 0.0, "N", "You spawn in Death Valley."),
    ("n2", 1.6, "N", "July. The air here once hit a hundred thirty-four degrees."),
    ("n3", 5.0, "N", "The hottest air ever officially recorded on Earth."),
    ("n4", 7.9, "HERO", "It's fine. I brought water!"),
    ("n5", 9.6, "N", "One litre. Above a hundred degrees, the army says drink that every hour."),
    ("n6", 14.0, "LAB", "Lab here. That was breakfast."),
    ("n7", 16.9, "HERO", "Nope."),
    ("n8", 18.2, "N", "But the air isn't the hottest thing here."),
    ("n9", 20.3, "N", "The ground once hit two hundred one degrees."),
    ("n10", 23.0, "N", "Eleven degrees short of boiling water."),
    ("n11", 25.3, "HERO", "Nope!"),
    ("n12", 26.4, "N", "The duck found the only lake for miles."),
    ("n13", 28.7, "LAB", "That lake is a mirage. The duck doesn't care."),
    ("n14", 32.1, "N", "Even at night, it can stay over a hundred."),
    ("n15", 34.9, "N", "So how long would you last? The answer is weird. The name is weirder."),
    ("n16", 39.7, "N", "About two days."),
    ("n17", 41.0, "N", "With the bottle or without. And only resting in shade."),
    ("n18", 44.4, "LAB", "Noted. There is no shade."),
    ("n19", 46.5, "HERO", "Nope. Nope. NOPE!"),
    ("n20", 48.3, "N", "The twist? In eighteen forty-nine, lost travelers crossed this valley.",
     "The twist? In 1849, lost travelers crossed this valley."),
    ("n21", 52.0, "N", "Leaving, one said: goodbye, Death Valley. Only one had died."),
    ("n22", 56.6, "N", "Next spawn: Roman winter camp, Mars, or a medieval farm?"),
    ("n23", 60.6, "HERO", "Somewhere cold. Please."),
    ("n24", 62.0, "LAB", "Respawning in three... two..."),
]
