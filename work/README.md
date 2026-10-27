# THE EXIT MANUAL — studio

Code for the channel's shorts. Everything is made in code (skia + Kokoro TTS + synthesised music); nothing to license.
Channel bible: Claude Docs 7adc0a97-b49c-4479-be53-963ffafc0403 (its "Retours de direction" section decides).

## The signature ending — LOCKED (26 Oct 2026)

Owner: "the logo animation exactly as in v5, at the end of every video, always the same animation."
`exit_outro.py` holds the v5 ending, frozen: the 12 fragments fly in from far away and converge (4.35 s), lock
0.25 s before "build the commons.", the logo beats like a heart (64/min, lub-dub, ripple rings) under the
"build the commons." / THE EXIT MANUAL panel, then keeps beating as it falls back into the depth. Same fragments,
paths, timing, camera drift and music cues (climb, downbeat + hit + riser on the word, heartbeat) in every episode.
Everything hangs on one time, `t_sign` (when the voice starts "build the commons."). Never edit its numbers:
change what comes before the ending instead.

An episode uses it like `exit_ep005.py` (refactored onto it; 18 frames from 56.9 s to 65.4 s and the whole sound
plan checked identical to the approved v5 render):
- LINES end with `("sign", "build the commons.", 0.6)` (+ an optional short loop line); `CAPS["sign"] = [None]`.
- scenes: its last own scene ends at `outro.start(ts)`; then `(outro.start(ts), outro.fall_at(ts) - 0.2, scene_world)`
  where `scene_world` calls `outro.scene(X, t, ts)`, and a last scene that calls `outro.fall(X, t, ts)` before its
  own loop image (`ts = T("sign")`).
- `cam_move` returns `outro.cam(t, ts, "world" | "loop")` in those two scenes; `outro.rain_level` and
  `outro.dust_level` drive the background layers; `music_plan()` returns `outro.plan(ep_plan, ts, DURATION)`;
  `music_dips()` adds `outro.dip(ts, E("sign"))`; `SUBTITLE_EXTRAS` adds `outro.subtitle(ts)`.

## v5 (26 Oct 2026) — original dark-epic score, the logo's heartbeat as signature, more camera

- **Episode:** `exit_ep005.py` + `exit_ep005_lines.py` (same script as v4) + `exit_ep005_subs.json` (65.46 s). Owner on v4:
  keep script, story and voice; the Bach chorale sounded like church, the earlier score like a march; make the
  music dark and epic (Lacrimosa / old Anonymous-era dark electronic); animate the Build the Commons logo at the end.
- **Score:** `exit_score5.py`, all synthesised in numpy (no samples, no recordings). D minor, 64/min, 12/8 sway,
  Dm | Bb | Gm | A. Drones, sub-bass, detuned filtered pads, glassy bit-crushed falling "sighs" + a cello-like synth
  line (Lacrimosa-like gestures written from scratch), triplet arp, half-time beat (kick on 1, ghost kick, one deep
  impact on 3: no snare, no rolls), crushed ticks, stutter glitches at the cuts, braams, risers, a chromatic climb
  A3 -> D5 landing on "build the commons.", then a lub-dub heartbeat (a faint one also under the night scene).
  Low hits get a 100-250 Hz body and a 2-4 kHz click so phones hear them. Music 13 dB under the voice (active RMS,
  after 4 dB ducking under speech and 3 dB dips under key lines); effects 17 dB under.
  `python3 exit_score5.py --test` -> `out/exit_music_test_v5.wav` + analysis (key, pulse period, snare-roll test,
  organ test, phone check through a 200 Hz high-pass).
- **Logo:** (now frozen in `exit_outro.py`, see above) `exit_logo.py` parses `logo/btc_logo_final.svg` (paths + matrix transforms) into 12 fragment paths and
  the centre star. In the episode, `draw_logo()`: fragments fly in one by one from far away/off-screen (spin, motion
  trail, depth fade), lock in clockwise, the ring, halo and star appear, then the logo beats (lub +9.5 %, dub
  0.30 s later, ripple ring, glow; no flash) on the score's beat grid anchored on "build the commons."; it keeps
  beating through the loop line, recedes to a point and the 40-day grid returns (last frame = first frame).
- **Camera everywhere:** slow push-in, drift and tiny roll on every scene; parallax on the data rain; a near layer
  of out-of-focus dust; 0.42 s push-through crossfades between scenes; lighter glitch on cuts.
- **Review gate fixes:** phone-audible thumps; longer, bigger heartbeat payoff; fragments start as "go to sleep"
  ends (no dead stretch), first two close to the camera; "check your screen time · comment your number" during step
  one; "ARPP" in the 16¢ label; the wordmark appears whole.

- **27 Oct 2026, owner's note:** Mastodon must not sound like an ad. The "other" and "commons" lines now say
  "Some places are built the other way. No ads. No owner selling your nights. / Wikipedia. Open networks. Run by
  the people who use them. That's a commons..." On screen: WIKIPEDIA (non-profit · no ads · written by volunteers),
  then MASTODON · PEERTUBE (open networks · servers run by communities), shown like evidence. 65.93 s; the locked
  ending (exit_outro.py) is untouched. Rule: the commons is the idea; examples stay plural and secondary, never one
  product, no absolute claim.

### Make v5
```bash
python3 exit_voice.py exit_ep005
python3 exit_score5.py --test
python3 sheets5.py exit_ep005                      # hook, keys, end sheets
python3 exit_score5.py exit_ep005                  # score + effects + voice -> out/exit_ep005_audio.wav
python3 exit_render.py exit_ep005
python3 exit_finish.py exit_ep005 TheExitManual_001v5_FortyDays
python3 exit_subtitles.py exit_ep005 exit_ep005_subs.json
```

## v4 (26 Oct 2026) — more human, clearer, fewer numbers, epic public-domain music

- **Episode:** `exit_ep004.py` + `exit_ep004_lines.py` + `exit_ep004_subs.json` (65.46 s). Owner: "a bit more
  human; the story must be clear; fewer numbers, emotion first; sources in the description; free music that fits
  the theme (Lacrimosa-like, epic)". One spine: we give the feed our nights -> Meta sells them, says so in its
  report -> it's designed that way -> Mastodon is built the other way: a commons -> step one -> build the commons.
  Only one number is spoken (forty days); the rest is felt ("a few cents", "billions") and shown small on screen.
  Sources: `out/TheExitManual_001v4_description.txt`.
- **Voice:** lighter disguise (fenrir -2 st, band 100 Hz-7.5 kHz, drive 1.25, room 0.14), longer pauses.
- **Music:** `exit_requiem.py` performs a public-domain score in software: Bach, "O Haupt voll Blut und Wunden"
  (St Matthew Passion BWV 244 no. 54, D minor) from the music21 corpus, FluidSynth + FluidR3 GM (MIT): choir aahs,
  strings, contrabass, horns above intensity 0.6, trombones and timpani above 0.75, fermatas held, cathedral
  reverb. The episode's `requiem()` gives start/end and an intensity curve; `exit_audio.py` puts the chorale
  11 dB under the voice (ducked, -4 dB dips under key lines) and the v3 dark textures 20 dB under, as a floor.
  Recordings can't be downloaded from the studio sandbox; any other public-domain score in the music21 corpus
  works the same way (`corpus.search(...)`). Needs `apt install fluidsynth fluid-soundfont-gm`, `pip install
  music21 mido`.

## v3 (26 Oct 2026) — dark transmission, deeper animation, the commons as the way out

- **Episode:** `exit_ep003.py` + `exit_ep003_lines.py` + `exit_ep003_subs.json` = TRANSMISSION 001 v3 · EXIT,
  "Forty days a year" (65.96 s). Same topic and core facts as v2; darker writing; new Mastodon beat
  (joinmastodon.org, W3C ActivityPub 2018) so the episode climbs to "build the commons." as the way out.
- **Look:** `exit_look3.py` (on top of `exit_look2.py`): perspective camera (`Cam`), any drawing on a 3D plane
  (`plane`, `tilt_quad`), data rain in 3 depth layers, particle streams, smooth slice glitch (constant brightness,
  no flash), kinetic letters (`kin_text`), word-by-word captions (`Caption3`), "INTERCEPTED" HUD with a steady dot.
- **"Oh, I get it" moments:** slivers of each day fly into 40 whole days; the phone turns in 3D and its ad slots
  are wired to advertisers and Meta; the eye breaks into pixels and swallows the camera into the 10-K; one person
  pulls back to a floor of 3.58 billion while money rises to $201 B; `infinite_scroll = true -> false`;
  a network drained into one owner rewires into federated servers = a commons, which become Relay's three nodes.
- **Voice:** disguised `am_fenrir`, -3 st (Rubber Band, formants preserved), band-pass 150 Hz-5.8 kHz, +3 dB at
  2.2 kHz, light saturation, short bare room (`disguise_fx` in `exit_voice.py`).
  Casting: `python3 exit_voice.py --casting-v3 "text"` -> out/exit_casting_v3.wav, ranked (1) fenrir -3 st,
  (2) fenrir -4 st + more room, (3) onyx -2 st narrow band (thinnest consonants).
- **Score:** `SCORE = "dark"` in the episode -> `build_dark()` in `exit_audio.py`: A1/E2 saw drones with a slow
  breathing filter, sub-bass, a heavy double pulse at 50/min, crushed digital ticks, static bursts on cuts,
  an A-major colour for the ending. Music 15 dB under the voice + 4 dB ducking + 6 dB dips under key lines
  (`music_dips()`), states per section (`music_sections()`: hush / pulse / void / build / resolve).

### Make v3
```bash
python3 exit_voice.py exit_ep003
python3 exit_render.py exit_ep003 --sheet-hook && python3 exit_render.py exit_ep003 --sheet-keys
python3 exit_audio.py exit_ep003
python3 exit_render.py exit_ep003
python3 exit_finish.py exit_ep003 TheExitManual_001v3_FortyDays
python3 exit_subtitles.py exit_ep003 exit_ep003_subs.json
```

### Rules learnt at the v3 review gate
- Never put words in a document's mouth: "if we engage less" (the 10-K says "decrease their level of
  engagement"), not "if we look away".
- Say the rounded number that matches the screen (3.6 billion for 3.58 bn).
- Preliminary decisions said as such in the voice too ("the EU's first finding").
- Mastodon: "no ads, by design", "no single owner" (the software has a non-profit steward; servers are independent).
- Label every illustration (ad ratio, clocks, the settings panel, the network). HUD says "staged · public sources only".
- The platforms' AI-voice / altered-content label is switched on at upload (synthetic voice).

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
| `exit_outro.py` | the signature ending (logo convergence + heartbeat), locked: the same in every episode |
| `exit_ep005.py`, `exit_ep005_lines.py`, `exit_ep005_subs.json` | the v5 episode (current), built on `exit_outro.py` |
| `exit_score5.py` | v5 original dark-epic score, music test, episode mix |
| `exit_logo.py` | the owner's logo as 12 fragment paths + centre star |
| `sheets5.py` | contact sheets (hook, keys, last 8 s) |
| `logo/` | the owner's Build the Commons logo files |
| `exit_requiem.py` | v4 epic layer: a public-domain chorale arranged and performed with FluidSynth |
| `exit_ep004.py`, `exit_ep004_lines.py`, `exit_ep004_subs.json` | the v4 episode |
| `exit_look3.py` | v3 look: camera, 3D planes, data rain, streams, glitch, kinetic type, HUD |
| `exit_look2.py` | v2 look and building blocks (imports `exit_engine.py`) |
| `exit_engine.py` | v1 look; still provides Relay, paints, arrows |
| `exit_voice.py` | Voice, timeline from measured line lengths, casting |
| `exit_audio.py` | Music bed and effects; music ~13 dB under the voice, effects ~19 dB under |
| `exit_render.py` | Parallel render, `--sheet-hook`, `--sheet-keys`, `--frame t` |
| `exit_finish.py` | -14 LUFS, true peak below -1 dBTP, MP4 + cover |
| `exit_subtitles.py` | .srt per language |
| `exit_ep003.py`, `exit_ep003_lines.py`, `exit_ep003_subs.json` | the v3 episode (facts + sources in the docstring) |
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
