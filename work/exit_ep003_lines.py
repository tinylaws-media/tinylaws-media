"""Script of TRANSMISSION 001 v3 · EXIT ("Forty days a year"). Imported by exit_ep003.py.

(id, spoken text with '|' where the caption block changes, pause after (s), optional voice opts)
v3 (26 Oct 2026): same topic and facts as v2, written darker (a leaked message, not a lesson), and built so the
episode climbs to "build the commons." as the way out: their feed (owned, endless) -> a network built the other
way (Mastodon, no single owner) -> what that is: a commons -> step one tonight -> build the commons.
Numbers are written as spoken.
"""
LINES = [
    ("hook", "Forty days a year.", 0.4),
    ("added", "Every hour we give the feed. | Added up.", 0.45),
    ("look", "Now look from Meta's side.", 0.35),
    ("slot", "Each flick of your thumb | loads more space to sell.", 0.45),
    ("name", "Their annual report ties their results to | engaging active users. | That's us.", 0.45),
    ("warn", "It warns: | if we engage less, | revenue may be significantly harmed.", 0.45),
    ("dollar", "On average, we each bring Meta | sixteen cents a day.", 0.25),
    ("times", "Times three point six billion of us.", 0.55),
    ("nolast", "The feed never ends. | Our night does.", 0.6),
    ("study", "In Norway, forty-five thousand students. | One more hour of screen in bed: | twenty-four minutes less sleep.", 0.35),
    ("check", "A link, not proof.", 0.45),
    ("eu", "The EU's first finding: | TikTok's endless scroll may break the law.", 0.35),
    ("design", "Endless is a design choice.", 0.45),
    ("other", "Mastodon is built the other way. | No ads, by design. | No single owner.", 0.4),
    ("commons", "Nothing there is built to sell your night. | That's a commons.", 0.5),
    ("step", "Step one, tonight: | the phone sleeps outside your room.", 0.5),
    ("stop", "Stop scrolling. | Go to sleep.", 0.7),
    ("world", "We need you awake. | We build what comes next.", 0.45),
    ("sign", "build the commons.", 0.6),
    ("loop", "Or next year, it takes another...", 0.0),
]

CAPS = {
    "hook": [None],
    "added": ["Every hour we / give *the feed.*", "*Added up.*"],
    "look": ["Now look from / *Meta's* side."],
    "slot": ["Each flick of / your thumb", "loads more space / to *sell.*"],
    "name": ["Their annual report ties / their results to", "*engaging active users.*", "That's *us.*"],
    "warn": ["It warns:", "if we *engage less,*", "revenue may be / *significantly harmed.*"],
    "dollar": ["On average, we each / bring Meta", "*sixteen cents* / a day."],
    "times": ["Times *3.6 billion* / of us."],
    "nolast": ["The feed / *never ends.*", "Our *night* does."],
    "study": ["In Norway, / *45,000 students.*", "One more hour of / screen in bed:", "*24 minutes* / less sleep."],
    "check": ["A *link,* not proof."],
    "eu": ["The EU's / *first finding:*", "TikTok's endless scroll / *may break the law.*"],
    "design": ["Endless is a / *design choice.*"],
    "other": ["Mastodon is built / *the other way.*", "*No ads,* by design.", "*No single owner.*"],
    "commons": ["Nothing there is built / to sell *your night.*", "That's a *commons.*"],
    "step": ["*Step one,* tonight:", "the phone sleeps / *outside your room.*"],
    "stop": ["*Stop scrolling.*", "*Go to sleep.*"],
    "world": ["We need you *awake.*", "We *build* what / comes next."],
    "sign": [None],
    "loop": ["Or next year, / it takes another..."],
}
