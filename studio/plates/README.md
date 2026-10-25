# NOT JUST YOU — studio

Everything in a Not Just You episode is made in code: the night bedroom, the lamp, Lumen the moth,
the diagrams, the captions, the narration (Kokoro, offline), the music and the mix.

Look (from the channel bible): a bedroom at night in cold blues, one warm light (the lamp: help,
other people). Lumen never speaks: he listens, circles the phone's cold light, and settles by the
lamp when the episode gives a way out. Palette night #0A0F1E, deep blue #18243A, amber #F2B35B,
faded rose #C9A7B8, cream #F3E9DA. Type: Instrument Serif (roman + italic). Calm: fixed rain and
grain, slow camera, no flashes, no shakes.

## Files

| File | What it does |
| --- | --- |
| `njy_engine.py` | Renderer: palette, fonts, room (window, city, lamp, bed, phone and its feed), Lumen, captions, source lines, bars, loop arrows, nodes |
| `njy_ep001.py` | Pilot "The bad-news loop". Copy it to start a new episode |
| `njy_voice.py` | Narration: `casting`, `measure` (synthesise every line, store durations), `build` (voice track on the timeline) |
| `njy_audio.py` | Night pad + felt piano + soft rain + quiet effects; mix with the voice |
| `njy_render.py` | Contact sheets, single frames, full render (2 processes) |
| `njy_cover.py` | Cover image (room + hook) |
| `njy_subtitles.py` | .srt per language from the episode's lines |
| `njy_ep001_subs.json` | French subtitles of the pilot (English comes from the captions) |
| `voice.py`, `audio.py`, `finish.py` | Unchanged copies from the Tiny Laws studio (model download, DSP helpers, -14 LUFS finish) |
| `fonts/` | Instrument Serif (SIL Open Font License, licence included) |

## Make the next episode

```bash
pip install --break-system-packages skia-python numpy scipy pillow kokoro-onnx soundfile   # ffmpeg with rubberband
cp njy_ep001.py njy_ep002.py      # set EP = "njy_ep002", rewrite LINES, SOURCES, panels, SFX
python3 njy_voice.py measure njy_ep002     # durations -> the timeline (aim for 61-66 s: DURATION prints on import)
python3 njy_render.py njy_ep002 --sheet sheet_first8 0 0.5 1 1.5 2 2.5 3 3.5 4 4.5 5 5.5 6 6.5 7 7.5 8
python3 njy_voice.py build njy_ep002 && python3 njy_audio.py njy_ep002
python3 njy_render.py njy_ep002                       # out/njy_ep002_video.mp4 (~4 min on 2 cores)
python3 finish.py njy_ep002 NotJustYou_002_<slug>     # -14 LUFS, true peak < 0 dBTP
python3 njy_cover.py njy_ep002 "hook line one" "hook *line two*"
python3 njy_subtitles.py njy_ep002 njy_ep002_subs.json
```

`LINES` is the whole script: `say` (spoken, numbers spelled out), `cap` (caption: `" / "` breaks the
line, `*word*` is amber italic, at most 5 words a line and 2 lines), `gap` (silence before the line).
The timeline comes from measured durations, so captions always land on the voice. Scene times
are written as `T(i)` (start of line i), so a script edit never breaks the animation.

## Episode rules

- 0-2 s the sensation, written from frame 0 and said at once; 2-10 s the reframe with one sourced
  number; then the mechanism with Lumen; then what helps: one path for you, one together; end on
  "it's not just you", which loops into the first line; the last 0.45 s dissolves into frame 0.
- Every figure shows its source in small type under the caption; say "a link, not proof" for
  surveys and "predicts, not proves" for longitudinal studies. No invented chart data.
- Captions mirror the voice; text between y 230 and 1450, nothing past x 900 (the engine shrinks
  captions and source lines to fit).
- Helpline on screen when the topic touches distress: "Struggling? You're not alone. Free help:
  findahelpline.com"; full country list in the pinned comment.
- Never name or credit anyone who makes the channel; never a professional title; no advice framed
  as treatment. Voice: Kokoro af_heart, speed 0.9, -1 semitone (casting: out/njy_casting.wav).
- Music 13 dB under the voice (3 dB more while it talks), effects 19 dB under, -14 LUFS.

## Review gate (every episode)

Contact sheets (first 8 s every 0.5 s, ~30 key frames) + a text timeline with sources go to a
separate reviewer agent that has not seen the work: ranked retention problems, claim-by-claim
accuracy, the bible's guardrails and safe-messaging rules, 3 alternative hooks. Apply every cheap
and right fix and every accuracy and guardrail fix; keep a list of what was rejected and why.
