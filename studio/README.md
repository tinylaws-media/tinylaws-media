# SLOP SHOP — studio

Everything in a Slop Shop episode is made in code: Glorp, the penguins, the glossy "AI image" look,
the captions, the jingle and the effects. Voices are Kokoro-82M (Apache 2.0, offline). Fonts: Anton,
Comic Neue, Bungee (SIL OFL, licences in `slop_fonts/`). No stock, no image generator, nothing to license.

## Files

| File | What it does |
| --- | --- |
| `slop_engine.py` | Renderer: saturated gradients, glossy plastic shading, lens flares, Glorp (misaligned eyes, too many teeth, any finger count, sweat, melt), the penguin with protest signs, Sun, Moon, shark, sapling, melting text, fact cards, SYSTEM box, reality bar, watermark, stickers |
| `slop_ep001.py` | Episode #001 "Did You Know? (No)" |
| `slop_ep002.py` | Episode #002 "SLOP NEWS: The Moon Has Been Sold" (YouTube-Poop cut). Copy it to start a new episode |
| `slop_ytp.py` | The YTP layer (punch zooms, crash zooms, shakes, visual stutters and freezes, RGB split, saturated look, bad morphs) and the SLOP NEWS cast: desk, window, ticker, lower thirds, the Moon (square, premium, arms), tech boss (USB stick), Minister of Night (bread), Thursday, influencer (ring light), toaster, werewolf, SOLD stickers, price tags |
| `slop_audio.py` | Soundtrack for YTP episodes: the jingle + synthesised gags (sub boom, scratch, slide whistle, cash register, squeak, howl, skip, rewind, wah-wah, creak, crackle, mic tap), tape stops and beat repeats |
| `slop_voice.py` | Multi-voice narration (one Kokoro voice per character) with YTP parts per line (stutter, repeat pitched up, sped-up tape, tempo, digital grain) and line accents (vibrato "wobble", "toaster" filter); a mouth envelope per character; `measure` times every line and part |
| `slop_render.py` | Parallel render + contact sheets (`--sheet t1 t2 ... --name x`) and single frames (`--frame t out.png`) |
| `slop_cover.py` | Cover image (`cover(R)` in the episode, or #001's host shot) |
| `slop_casting.py` | `python3 slop_casting.py slop_ep002 A C B D`: every cast in `CASTS`, ranked into `out/slop_casting.wav` (beeps = rank) |
| `slop_ep002_subs.json` | EN + FR subtitle lines for #002 |
| `slop_ep001_subs.json` | EN + FR subtitle lines for #001 |
| `audio.py`, `voice.py`, `finish.py`, `subtitles.py` | Unchanged copies from the Tiny Laws studio (music + mix, Kokoro helpers, -14 LUFS finish, .srt) |

## Make the next episode

```bash
pip install --break-system-packages skia-python numpy scipy pillow kokoro-onnx soundfile   # + ffmpeg with rubberband
cp slop_ep001.py slop_ep002.py      # rewrite LINES_T (who, text, opts, gap), CAPTIONS, beats, scenes, SFX
python3 slop_voice.py slop_ep002 measure      # times every line -> out/slop_ep002_durs.json (timeline follows it)
python3 slop_render.py slop_ep002 --sheet 0 0.5 1 1.5 2 2.5 3 3.5 4 4.5 5 5.5 6 6.5 7 7.5 8 --name first8
python3 slop_voice.py slop_ep002              # out/slop_ep002_voice.wav (+ mouth envelope)
python3 audio.py slop_ep001                   # #001: music 13 dB and effects 19 dB under the voice
python3 slop_audio.py slop_ep002              # #002+: YTP gags 15 dB under the voice, music ducks
python3 slop_render.py slop_ep002             # out/slop_ep002_video.mp4
python3 finish.py slop_ep002 SlopShop_002_<slug>   # -14 LUFS, peaks limited at -2 dB
python3 slop_cover.py slop_ep002 out/SlopShop_002_cover.png
python3 subtitles.py slop_ep002 slop_ep002_subs.json   # out/subs/*.srt
```

The timeline is laid out from the measured line lengths: each line gets its GAP, and all gaps are scaled
so the episode fills exactly `DURATION` (32 bars at 124 BPM = 61.94 s, over TikTok's 1-minute mark).
If the scale factor printed by `python3 -c "import slop_ep002 as e; print(e._k)"` is above ~1.3,
the episode has dead air: add a joke, don't stretch pauses.

## Rules learned on #001 (independent review, 25 Oct 2026)

- Frame 0 = the full gag: the FACT card + the picture that disproves it + the game sticker
  ("1 of these facts is real"). The last frame is identical to frame 0; the last line leads into the first.
- The picture must *contradict* the fact, not just deny it (the penguin's sign corrects with another
  absurd fact: "it was thursday.").
- Escalate what disagrees: an object, then his own body, then the whole picture, then reality agrees with
  him and that breaks him. The busiest frame comes late.
- Text melts within 0.4 s after a lie, more each time. A true fact never melts.
- Numbers of a real fact go on screen, not in the voice (no lecture). Every real fact is sourced in the
  episode docstring and in the post description.
- Glorp's hand and every sign stay inside x 60-880; text between y 230 and 1450; nothing under the
  app's caption overlay that matters.
- Comment prompt: invite *fake* facts ("Comment a fake fact. I'll make it real."), never fact-checks of real claims.
- Nothing yellow dripping from Glorp (reads as a pee joke). Adult deadpan, no kid codes.
- Calm image: pops and eases only, no flashes. Music 13 dB under the voice, effects 19 dB under.

## Rules learned on #002 (YTP cut, independent review, 26 Oct 2026)

- The YTP edits live in the script: a line is a list of parts with effects, so the picture syncs to every stutter and repeat.
- One premise, and every scene is caused by the one before it. No anchor bridges ("X has responded") with no joke in them.
- Never tell the same joke twice (the werewolf: fine print, then a silent cutaway).
- The ticker shows only jokes already told, plus one future headline as a hidden detail.
- Invented accents only: all voices use the US-English Kokoro locale, and the accent is a vibrato or a filter.
- No archetype close to a real person's trademark look (no egg avatar, no bird, no rocket). The tech boss is a USB stick.
- Lower thirds and captions stay outside the camera so punch zooms never push text out of the safe zone.
- No strobe: at most one hard light/dark change a second, the RGB split keeps the frame's brightness, saturated looks are held, never pulsed. Check: `ffmpeg ... scale=54:96,format=gray` and diff the mean luminance per frame.
- Finish at -14 LUFS, true peak about -1.5 dBTP (measured with `ebur128=peak=true`).
