"""Script of TRANSMISSION 001 v2 · EXIT ("Forty days a year"). Imported by exit_ep002.py.

(id, spoken text with '|' where the caption block changes, pause after (s))
Numbers are written as spoken. Pace comes from the pauses, never from speed (speed 1.0, no pitch shift).
Revised after the independent review (25 Oct 2026): exact 10-K wording, no unsourced lines, every line captioned.
"""
LINES = [
    ("hook", "Forty days a year.", 0.35),
    ("added", "On our feeds. | Every hour, added up.", 0.6),
    ("look", "Now look from Meta's side.", 0.45),
    ("slot", "Each flick of your thumb | loads more space to sell.", 0.7),
    ("name", "Their annual report says their results depend on | engaging active users. | That's us.", 0.6),
    ("warn", "And it warns: | if we look away, | their revenue may be significantly harmed.", 0.7),
    ("dollar", "On average, each of us brings Meta | sixteen cents a day.", 0.3),
    ("times", "Times three and a half billion of us.", 0.85),
    ("nolast", "The feed never ends. | Our night does.", 0.9),
    ("study", "In Norway, among forty-five thousand students, | each extra hour on a screen in bed | came with twenty-four minutes less sleep.", 0.5),
    ("check", "A link, not proof. | Tired people may just scroll more.", 0.55),
    ("dont", "So don't take my word for it. | Test it.", 0.75),
    ("eu", "In February, EU regulators said | TikTok's endless scroll may break EU law.", 0.5),
    ("design", "Endless scroll is a design choice. | Choices can change.", 0.75),
    ("step", "Step one, tonight: | the phone sleeps outside your room.", 0.75),
    ("stop", "Stop scrolling. | Go to sleep.", 0.9),
    ("world", "We need you awake tomorrow.", 0.8),
    ("sign", "build the commons.", 0.6),
    ("loop", "Or next year, our feeds take another...", 0.0),
]

# caption blocks, one per '|' chunk; *word* = accent colour; '/' = line break. Every spoken line is captioned.
CAPS = {
    "hook": [None],
    "added": ["On our *feeds.*", "Every hour, / *added up.*"],
    "look": ["Now look from / *Meta's* side."],
    "slot": ["Each flick of / your thumb", "loads more space / to *sell.*"],
    "name": ["Their annual report says / their results depend on", "*engaging active users.*", "That's *us.*"],
    "warn": ["And it warns:", "if we *look away,*", "their revenue may be / *significantly harmed.*"],
    "dollar": ["On average, each of / us brings Meta", "*sixteen cents* / a day."],
    "times": ["Times *3.5 billion* / of us."],
    "nolast": ["The feed / *never ends.*", "Our *night* does."],
    "study": ["In Norway, among / *45,000 students,*", "each extra hour / on a screen in bed", "came with *24 minutes* / less sleep."],
    "check": ["A *link,* not proof.", "Tired people may / just scroll more."],
    "dont": ["So don't take / my word for it.", "*Test it.*"],
    "eu": ["In February, EU / regulators said", "TikTok's endless scroll / *may break EU law.*"],
    "design": ["Endless scroll is / a *design choice.*", "Choices *can change.*"],
    "step": ["*Step one,* tonight:", "the phone sleeps / *outside your room.*"],
    "stop": ["*Stop scrolling.*", "*Go to sleep.*"],
    "world": ["We need you / *awake* tomorrow."],
    "sign": [None],
    "loop": ["Or next year, our / feeds take another..."],
}
