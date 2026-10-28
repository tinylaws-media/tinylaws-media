# Subject Zero — the 2D toolkit (« estampe »)

Everything is drawn and synthesised in code: no image generator, no stock footage, nothing to license. 1080×1920,
24 fps. The template episode is **Could You Survive? #01 — Point Nemo** (`nemo01*.py`).

| File | What it does |
|---|---|
| `sz2d.py` | The look: palette (Prussian blue, cream paper, coral, her yellow hoodie), paper grain, gouache mottling, ink line that boils every 2 frames, woodblock sea (`Sea`), sky with bokashi band, mist bands, the ISS, **Subject Zero** (`draw_hero`: faces `FACES`, arm poses, squash, shiver, blink), the duck, the red seal, the HUD card, word-by-word captions |
| `szvoice.py` | Several speakers per episode (`SPEAKERS`, per-line `LINE_FX`): Kokoro voices, ffmpeg chains (radio for the lab), auto layout on targets with pull; writes `out/<ep>_voice.wav`, `out/<ep>_lines.json` and one loudness envelope per speaker (`out/<ep>_env_<WHO>.npy`, drives mouths and the intercom) |
| `voice.py` | Kokoro model download and helpers (shared with Tiny Laws) |
| `listen.py` | The listening gate: Whisper small transcribes each line; PASS = at most 8 % misheard words overall and no line over 20 % |
| `tl_audio.py` | Synth sound effects and instruments (shared with Tiny Laws): pop, tick, stamp, whoosh, sparkle, crack, glass, boing, riser, bass_note, snare… |
| `sz2render.py` | Parallel render to mp4 (`python3 sz2render.py <ep>_pic`), contact sheets (`--sheet t1 t2 …`) |
| `nemo01.py` | Episode file: speakers, voice effects, the lines (key, target second, speaker, text[, what the gate should hear]) |
| `nemo01_pic.py` | The picture, timed on `out/nemo01_lines.json`: shots, her state per second, the chart (azimuthal equidistant map from Natural Earth), the sky shot, the duck, the spacecraft graveyard, HUD, intercom, NOPE texts and punch-ins, captions, end cards, the respawn flash |
| `nemo01_audio.py` | Own music (plucked koto-like synth, woodblock, bass, a taiko section), the effects on the beats, ducking, the mix and the final mp4 at −14 LUFS |
| `make_brand.py` | Profile picture and YouTube banner |
| `fonts/` | Bagel Fat One, Bricolage Grotesque, Caveat Brush, Space Mono (Open Font License) |
| `data/` | Natural Earth 1:110 m land and countries (public domain) |

## Make an episode

```
python3 szvoice.py nemo01 && python3 listen.py nemo01            # rewrite flagged lines until PASS
python3 sz2render.py nemo01_pic --sheet 0 0.5 1 2 4 6 8 …         # look at frames before rendering
python3 sz2render.py nemo01_pic && python3 nemo01_audio.py         # -> out/SubjectZero_CYS01_PointNemo.mp4
```

Then the mix gate: copy `out/<ep>_lines.json` to `out/<ep>mix_lines.json`, write the final mix (mono) as
`out/<ep>mix_voice.wav` and run `python3 listen.py <ep>mix`: the narration must still pass over the music and effects.

## The series rules (Could You Survive?)

- Frame 0: her in the place, the question on screen ("COULD YOU SURVIVE / <PLACE>?"); the first spoken line names the
  place in 6 words or fewer.
- First number that makes you go "wow" before 8 s; a new picture every 2–3 s; re-hooks around 18–20 s and 35–38 s;
  the answer (how long you'd last) at about 60–70 %; then a bigger second payoff; the end question with three
  choices for the next spawn; the lab's "Respawning in three… two…" loops into frame 0.
- Running gags, in every episode: the lab on the intercom, deadpan ("Lab here…", "Noted."); her NOPE in a voice far
  too deep for her (am_onyx, pitched a little lower), three times, each louder and with more damage, the third a
  rapid "Nope. Nope. NOPE!"; the rubber duck that is never in danger; the respawn loop.
- Facts: every number from a fact sheet with sources; estimates said as estimates ("about", "around").
- Never graphic suffering, never combat, never a real person drawn, never a protected character or brand.
- Voices: narrator am_michael, her af_bella, her NOPE am_onyx, the lab bm_george through the radio chain.
- Captions: 1–3 words at a time, the spoken word in yellow, inside x 120–780, baseline about y 1235; the NOPE texts
  replace the caption; HUD card from (120, 290).
