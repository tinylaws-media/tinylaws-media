"""COULD YOU SURVIVE? #04 — A Roman winter camp. Subject Zero (her) spawns in the snow inside Vindolanda, a timber
fort on Rome's northern frontier in Britain, around AD 100, and the army signs her up on the spot.

Who it is for: curious 16–30s who like history served as a dare ("could you hack it as a Roman soldier?") and have
never heard that we can read these soldiers' actual mail.
The single promise: you will know what a Roman winter on the frontier really asked of you, how long you'd have to
last, and why we know any of it.

Three hooks, three types (the strongest true one is kept):
  1. Statement + stakes (KEPT): "You spawn in Roman Britain." + "the army just signed you up", "YOU'D LAST ?? YEARS"
     in the HUD. Names the place in 5 words; the wow number (30 km in about 6 hours) lands by 7 s.
  2. Question: "Could you survive one winter in a Roman fort?" (weaker: a question with no picture, and longer)
  3. Contrast: "Roman soldiers wrote home for socks." (true and funny, but gives away the mid-video beat; it becomes
     the first re-hook instead)

Facts and sources: subjectzero/research/cys04_facts.md (every number below is there).
Main assumption, said in the voice: she is enrolled, so "how long would you last" is the minimum term of service
(25 years for the auxiliary soldiers who garrisoned Vindolanda). We never say she dies.
Running gags: the lab's deadpan voice ("Noted."), her NOPE in a voice far too deep for her that does more damage each
time (1: the snow on the gate tower and her drift blows off in a white burst; 2: the barrack roof's shingles rip
off and fly across the frame; 3: the whole timber rampart falls flat like dominoes and the gate tower topples, in a
wall of snow), the rubber duck that is never in danger (it found the bathhouse's warm pool), the respawn.
Continuity: in #03 she begged "Somewhere cold. Please." She got it.

    python3 szvoice.py cys04 && python3 listen.py cys04     # voices + listening gate
    python3 sz2render.py cys04_pic [--sheet t ...]           # picture
    python3 cys04_audio.py                                   # music, effects, mix -> out/SubjectZero_CYS04_RomanCamp.mp4
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EPNAME = "cys04"
FPS = 24
BPM = 100
DURATION = 27 * 4 * 60 / BPM      # 27 bars of 4/4 at 100 BPM = 64.8 s

SPEAKERS = {
    "N": dict(voice="am_michael", speed=1.06),
    "HERO": dict(voice="af_bella", speed=1.08, gain=1.0),
    "LAB": dict(voice="bm_george", speed=0.98, gain=0.85,
                chain="highpass=f=320,lowpass=f=3300,acompressor=threshold=-20dB:ratio=6:attack=5:release=60,"
                      "aeval='tanh(2.2*val(0))/tanh(2.2)'"),
}
# her NOPE: the deepest natural voice (am_onyx), a little lower still, comes out of her. Each one 3 dB+ louder.
NOPE = "rubberband=pitch={p}:formant=preserved,acompressor=threshold=-18dB:ratio=4,volume={v}dB"
LINE_FX = {
    "n16": dict(overlap=-0.45),          # 0.65 s of silence before the answer
    "n9": dict(overlap=0.1), "n10": dict(overlap=0.1), "n12": dict(overlap=0.1), "n13": dict(overlap=0.1),
    "n20": dict(overlap=0.1), "n3": dict(overlap=0.1),
    "n7": dict(voice="am_onyx", speed=0.95, chain=NOPE.format(p=0.86, v=-2)),
    "n14": dict(voice="am_onyx", speed=1.0, chain=NOPE.format(p=0.86, v=4)),
    "n18": dict(voice="am_onyx", speed=1.0, chain=NOPE.format(p=0.86, v=8) + ",volume='if(gte(t,0.86),2.8,1)':eval=frame"),
}

# key, target start (s), speaker, what is said (numbers spelled out: the gate compares words)
VOICE_LINES = [
    ("n1", 0.0, "N", "You spawn in Roman Britain."),
    ("n2", 1.6, "N", "Winter, around the year one hundred. The army signs you up."),
    ("n3", 5.2, "N", "A Roman manual: carry about twenty kilos. March thirty kilometres."),
    ("n4", 9.0, "HERO", "Thirty WHAT?", "Thirty what?"),
    ("n5", 10.0, "N", "In just over six hours."),
    ("n6", 11.6, "LAB", "Lab here. Fort sick list: thirty-one unfit. Noted."),
    ("n7", 16.0, "HERO", "Nope."),
    ("n8", 17.2, "N", "Good news: you get mail."),
    ("n9", 18.8, "N", "Someone here got socks, sandals, and two pairs of underpants."),
    ("n10", 22.8, "N", "An officer wrote: my fellow soldiers have no beer. Please order some."),
    ("n11", 27.6, "N", "The duck found the bathhouse."),
    ("n12", 29.2, "N", "The toilet? Side by side. No cubicles."),
    ("n13", 32.0, "N", "And probably a shared sponge on a stick."),
    ("n14", 34.4, "HERO", "Nope!"),
    ("n15", 35.5, "N", "How long would you last? Check your contract. The real surprise is underground."),
    ("n16", 40.6, "N", "Twenty-five years. Minimum. If you make it."),
    ("n17", 43.0, "LAB", "Noted. See you in twenty-five years."),
    ("n18", 45.9, "HERO", "Nope. Nope. NOPE!"),
    ("n19", 47.6, "N", "The twist? Those were real letters, dug out of the mud right here."),
    ("n20", 53.4, "N", "One is a birthday invitation. Probably the oldest known Latin in a woman's hand."),
    ("n21", 58.0, "N", "Next spawn: Mars, a medieval farm, or Pompeii?"),
    ("n22", 60.9, "HERO", "Anywhere with heating."),
    ("n23", 62.0, "LAB", "Respawning in three... two..."),
]
