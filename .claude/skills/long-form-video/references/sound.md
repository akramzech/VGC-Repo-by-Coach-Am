# Sound (long form)

## `scripts/audio2.py` constants
- **SFX:** `SFX_BOOST = 9` dB over the per-event dB in the beat code, capped at −6.5. A later build used 7.5.
- **Music:** `MUSIC_GAP = 13` dB under the speech RMS (a later build used 11), and `DUCK = .35`.
- **Tracks:** `music1.mp3` cross-faded over 6 s into `music2.mp3`. Both are tracks the student supplies in `build/sfx/`. Fade in over 0.5 s and out over 3 s.
- **Master:** final gain to −14.5 LUFS, plus `alimiter 0.89`.

**Measured stems from a good build:**
- voice −20.5 LUFS;
- music −32.6 LUFS, a 12 LU gap. A gap of 21.6 LU was too quiet to hear;
- final −14.6 LUFS.

## SFX
- **Licensed files:** put them in `build/sfx/`: shutter, key, click, boom, stamp, zoom, slide (tech whoosh), pop, ting and riser. The riser climaxes at the event time, so it starts 2.95 s earlier.
- **Synth fallbacks** from `sfxlib.py`: ratchet, shing, swish_up, zoom_in/out, check, clunk, tink, blip, ping, chirp.
- **Caption starts** rotate pop, click, tink, blip, key, ping and chirp, never the same twice in a row.
- **Accents:** stamps on numbers, a boom on hero words, a riser into the hook slam, a ting on refill.

You can't hear the result. Report the LUFS and gap numbers, and say the by-ear check is the student's.
