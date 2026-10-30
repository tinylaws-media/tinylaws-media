# Subject Zero — the 2D toolkit (« estampe »)

Everything is drawn and synthesised in code: no image generator, no stock footage, nothing to license. 1080×1920,
24 fps. The template episode is **Could You Survive? #01 — Point Nemo** (`nemo01*.py`).

| File | What it does |
|---|---|
| `sz2d.py` | The look: palette (Prussian blue, cream paper, coral, her yellow hoodie), paper grain, gouache mottling, wood grain (`woodgrain`), ink line that boils every 2 frames, woodblock sea (`Sea`), sky with bokashi band, mist bands, the ISS (long truss, eight gold wings), **Subject Zero** (`draw_hero`: faces `FACES`, arm poses, squash, shiver, blink), the duck, the red seal, the HUD cartouche (`hud_card`), word-by-word captions |
| `cys02*.py` | Episode #02, Everest: same machinery; new in `sz2d.py`: `alpine_sky`, `peak` (woodblock mountain with snow mantle, shadow side, carved hatching), `snow_plume`, `snowfall`, `trilobite`, `crinoid`, `shell_fossil`, `thermometer` |
| `cys03*.py` | Episode #03, Death Valley; new in `sz2d.py`: `desert_sky`, `heat_haze`, `mirage`, `SaltFlat` (perspective polygon crust with `crack` and `shatter`), `dust_devil`, `water_bottle`, `draw_legs` (she stands on dry ground), `covered_wagon`, arm modes `raise` and `fan`, `thermometer(col=…)` |
| `szvoice.py` | Several speakers per episode (`SPEAKERS`, per-line `LINE_FX`): Kokoro voices, ffmpeg chains (radio for the lab), auto layout on targets with pull; writes `out/<ep>_voice.wav`, `out/<ep>_lines.json` and one loudness envelope per speaker (`out/<ep>_env_<WHO>.npy`, drives mouths and the intercom) |
| `voice.py` | Kokoro model download and helpers (shared with Tiny Laws) |
| `listen.py` | The listening gate: Whisper small transcribes each line; PASS = at most 8 % misheard words overall and no line over 20 % |
| `tl_audio.py` | Synth sound effects and instruments (shared with Tiny Laws): pop, tick, stamp, whoosh, sparkle, crack, glass, boing, riser, bass_note, snare… |
| `sz2render.py` | Parallel render to mp4 (`python3 sz2render.py <ep>_pic`), contact sheets (`--sheet t1 t2 …`) |
| `nemo01.py` | Episode file: speakers, voice effects, the lines (key, target second, speaker, text[, what the gate should hear]) |
| `nemo01_pic.py` | The picture, timed on `out/nemo01_lines.json`: named shots, her state per second, the chart (azimuthal equidistant map from Natural Earth), the sky shot, the swim on the chart (% there, day counter), the half-underwater shot (legs over 4 km of water, the ON STRIKE sign), the big survival clock (seigaiha background, cracked glass), the duck, the spacecraft graveyard, the impact zone, HUD, intercom with the "Noted" tick, NOPE texts and punch-ins, captions, end cards, the respawn flash |
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

## Lessons from the review of #01 (apply to every episode)

- **Shot list:** no camera setup held longer than 8 s. Name the shots (`shot_start("clock")`), never index them.
  Point Nemo cuts close → chart → sky → close → swim on the chart → close (NOPE 1) → half underwater → close (NOPE 2)
  → big clock → duck → graveyard → close.
- **Text:** one story number on screen at a time. HUD labels ≥ 32 px, values ≥ 46 px, nothing smaller than 30 px.
  A stamp is drawn after the HUD, never under it. Check every label fits its card (long labels overlap the value).
- **Safe zone:** every text and every face inside x 120–780, y 230–1450 (the right column and the bottom belong to
  the app's buttons and caption). Big words are centred on x 450, not 540, and capped at 680 px wide pop included.
- **NOPEs:** the word goes above her head (y ≈ 600), never over her face; the HUD hides while she says it; the word
  never spills into the next shot. Each NOPE at least 3 dB louder than the one before, its damage landing just after
  the word, its boom short enough not to sit under the next line. Rings only in front of her. Vary the climax set
  piece from one episode to the next.
- **Mute viewers:** a sound gag carries a tag at the caption line ("[comically deep voice]").
- **Her:** she gets 2–3 lines of her own (the lab and the narrator are not the only voices), and a reaction to the
  end question.
- **Hook:** frame 0 has the question, her, and the number to come as "????" in the HUD; something moving in the sky
  from frame 0 (paid off later); the seal arrives at 3 s; a slow push-out over the first line; no "0" flash when a
  count starts.
- **Ending:** no title at the loop end, no seal on the flash, the end cards clear before the flash.
- **Facts:** a figure is written the same way in the voice, the captions and the HUD (2,688 everywhere).

## Lessons from the review of #02

- **A progress bar must not spoil or contradict the answer:** hide the answer's marks until it is said; if the story
  jumps in time ("after that…"), make the clock jump too.
- **One HUD card at a time** in a close shot, never a card + the bar + the lab chip + a caption.
- **Captions end before the next line starts** and never sit under a NOPE.
- **Leave 0.5 s of silence before the answer** and give the answer its own line.
- **Each NOPE's damage must be visible in its own shot** (start it on the word if the cut comes soon).
- **Word the facts at their honest edge:** "under five minutes" (not "about five") when the source gives 5 min typical
  and 1 min in storms; "still holds fossils", not "packed".

## Lessons from the review of #03

- **Never zoom a shot out below 1.0**: the frame edge shows (black bands). Push in, or draw the background oversize.
- **A HUD count must land when the number is said** (the caption lights the figure at that moment); put the count in
  its own insert shot so the hook is not one setup held for 6 s.
- **Hide the HUD while the lab chip is on screen**; never a stamp + a note + the chip + a caption together.
- **Clamp every NOPE word to end 0.15 s before the next line**, and write what she says ("NOPE!", not "NOOOPE!").
- **Damage must be big and in front**: a dust devil behind her in sand colours disappears into the background.
- **NOPE levels are measured on the final mix** (mean over the word): the limiter eats the last one, so add gain to it
  in the mix, not only in the voice chain.
- **The end shot is a setup too** (≤ 8 s): cut to her close-up for her reaction, clear the end cards first.
- **Hedge reported speech** ("supposedly said") even when a park page tells the story.

## Lessons from the review of #04

- **Say what the number is.** "YOU'D LAST 25 YEARS" read as a survival time when it was a term of service: the HUD
  now says "YOU'RE IN FOR", and the voice adds "If you make it". A HUD label is a claim too.
- **Don't spend the twist early.** Saying "a letter found here" at 18 s spoiled "their letters survived" at 47 s.
  Keep the source of a mid-video fact vague until the payoff that reveals it.
- **The wow number must be impressive on its own**: 30 km in 6 h is walking pace; lead with the load (20 kg).
- **Give the lab real stakes** (a real document: the fort's sick list) rather than filler.
- **Keep the damage of NOPE 3 on screen for at least 1 s** before the cut (speed up the collapse, cut later).
- **The end choice stays on screen** as a one-line strip until 0.3 s before the flash.
- **The mix gate can flip on a short line**: cut the music and the bed under a 2-word line ("Thirty WHAT?").
