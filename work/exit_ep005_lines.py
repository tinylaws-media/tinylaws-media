"""Script of TRANSMISSION 001 v5 · EXIT ("Forty days a year"). Imported by exit_ep004.py.

v4 (26 Oct 2026, owner: "a bit more human; the story must be clear or we get lost; fewer numbers, emotion first;
sources can live in the description"). One spine, said simply: we give the feed our nights -> someone sells them
-> it's designed that way -> some places are built the other way: a commons -> step one -> build the commons.
Numbers kept to one in the voice (forty days); the rest is felt ("a few cents", "billions") and shown on screen.
"""
LINES = [
    ("hook", "Forty days a year.", 0.45),
    ("added", "That's what we give our feeds. | Hour after hour, without even noticing.", 0.5),
    ("look", "Now look at it from Meta's side of the screen.", 0.4),
    ("slot", "Every time your thumb moves, | there's a little more space to sell.", 0.5),
    ("name", "Meta says it in its own annual report: | its results depend on keeping us engaged.", 0.45),
    ("us", "Us. Our evenings. Our nights.", 0.7),
    ("cents", "To them, each of us is worth | a few cents a day. | Now multiply that by billions.", 0.9),
    ("nolast", "The feed never ends. | Our night does.", 0.7),
    ("tired", "And in the morning, we wake up tired, | wondering where the evening went.", 0.6),
    ("design", "None of this is an accident. | Endless is a design choice. | And choices can be changed.", 0.55),
    ("other", "Mastodon is built the other way. | No ads, by design. No single owner.", 0.45),
    ("commons", "Nothing there is built | to keep you up at night. | That's a commons: | something we run together, for us.", 0.65),
    ("step", "So here's step one. Tonight, | the phone sleeps outside your room.", 0.6),
    ("stop", "Stop scrolling. | Go to sleep.", 0.9),
    ("world", "We need you awake. | We build what comes next, together.", 0.5),
    ("sign", "build the commons.", 0.6),
    ("loop", "Or next year, it takes another...", 0.0),
]

CAPS = {
    "hook": [None],
    "added": ["That's what we / give *our feeds.*", "Hour after hour, / *without even noticing.*"],
    "look": ["Now look from / *Meta's* side of the screen."],
    "slot": ["Every time / your thumb moves,", "a little more space / *to sell.*"],
    "name": ["Meta says it in / its own annual report:", "its results depend on / *keeping us engaged.*"],
    "us": ["*Us.* Our *evenings.* / Our *nights.*"],
    "cents": ["To them, each / of us is worth", "*a few cents* / a day.", "Now multiply that / by *billions.*"],
    "nolast": ["The feed / *never ends.*", "Our *night* does."],
    "tired": ["And in the morning, / we wake up *tired,*", "wondering where / *the evening went.*"],
    "design": ["None of this / is an *accident.*", "Endless is a / *design choice.*", "And choices / *can be changed.*"],
    "other": ["Mastodon is built / *the other way.*", "*No ads,* by design. / *No single owner.*"],
    "commons": ["Nothing there / is built", "to keep you / *up at night.*", "That's a *commons:*", "something we run / *together, for us.*"],
    "step": ["So here's *step one.* / Tonight,", "the phone sleeps / *outside your room.*"],
    "stop": ["*Stop scrolling.*", "*Go to sleep.*"],
    "world": ["We need you *awake.*", "We build what comes / next, *together.*"],
    "sign": [None],
    "loop": ["Or next year, / it takes another..."],
}
