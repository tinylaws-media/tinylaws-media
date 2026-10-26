# THE EXIT MANUAL — studio

Code for the channel's shorts. Everything is made in code (skia + Kokoro TTS + synthesised music); nothing to license.
Channel bible: Claude Docs 7adc0a97-b49c-4479-be53-963ffafc0403 (its "Retours de direction" section decides).

## v2 (25-26 Oct 2026) — the demo remade after the owner's notes

- **Episode:** `exit_ep002.py` + `exit_ep002_lines.py` = TRANSMISSION 001 v2 · EXIT, "Forty days a year" (65.5 s).
  The v1 pilot (`exit_ep001.py`, Follow the money) stays as it was.
- **Look:** `exit_look2.py`. No synthwave grid, no RGB offset on every word. One meaning per colour (green = our time,
  magenta = their money, cyan = data). IBM Plex Sans Condensed for captions, IBM Plex Mono for documents.
  Building blocks: year grid (365 days, slivers that stack), phone + endless feed with ad slots, eye that turns
  into pixels, dot-field zoom, document highlighter.
- **Voice:** natural Kokoro voice, speed 1.0, no pitch shift; pace comes from pauses. `exit_voice.py` adds a very
  light `warm` colour (no band-limit). Casting v2: `python3 exit_voice.py --casting "text"` -> out/exit_casting.wav,
  ranked am_fenrir, am_michael, am_puck, bm_george.

## Files

| File | What it does |
| --- | --- |
| `exit_look2.py` | v2 look and building blocks (imports `exit_engine.py`) |
| `exit_engine.py` | v1 look; still provides Relay, paints, arrows |
| `exit_voice.py` | Voice, timeline from measured line lengths, casting |
| `exit_audio.py` | Music bed and effects; music ~13 dB under the voice, effects ~19 dB under |
| `exit_render.py` | Parallel render, `--sheet-hook`, `--sheet-keys`, `--frame t` |
| `exit_finish.py` | -14 LUFS, true peak below -1 dBTP, MP4 + cover |
| `exit_subtitles.py` | .srt per language |
| `exit_ep002.py`, `exit_ep002_lines.py`, `exit_ep002_subs.json` | the v2 episode (facts + sources in the docstring) |
| `fonts/` | VT323, Major Mono Display, IBM Plex (SIL OFL, licences included) |

Needs `voice.py` and `audio.py` from the Tiny Laws studio, unchanged, next to these.

## Make an episode

```bash
pip install --break-system-packages skia-python numpy scipy pillow kokoro-onnx soundfile   # ffmpeg with rubberband
python3 exit_voice.py exit_ep002                 # voice + timing (run twice)
python3 exit_render.py exit_ep002 --sheet-hook && python3 exit_render.py exit_ep002 --sheet-keys
python3 exit_audio.py exit_ep002
python3 exit_render.py exit_ep002
python3 exit_finish.py exit_ep002 TheExitManual_001v2_FortyDays
python3 exit_subtitles.py exit_ep002 exit_ep002_subs.json
```

## Rules learnt at the v2 review gate

- Quote documents exactly *and* in context (a phrase qualifying "products" is not a name for people).
- Every spoken line is captioned; documents on screen are short excerpts at >= 48 px.
- No unsourced comparison ("more than our holidays"), no announced both-sides line: show it in the content.
- Name the company, never an unnamed "they". Label illustrations as illustrations.
- Studies: say what they measured (any screen in bed) and that a link is not a cause.
- Preliminary decisions are said as preliminary ("may break EU law").
