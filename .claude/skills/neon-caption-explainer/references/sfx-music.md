# SFX and music

## Synthetic SFX (`scripts/sfxlib.py` + `S2()` in `audio.py`)
- **Events:** `[time, kind, peak dBFS]`, written by `sfx(t, kind, db)`.
- **Seeds:** each event renders with its own seed. Use a NEW seed base per video, for example `default_rng(5000 + i*6007)` and then `1000 + i*7919` for the next one, so videos don't sound alike.

| Use | Kinds (rotate; never the same twice in a row) |
|---|---|
| caption start | `pop`, `click`, `tink`, `blip`, `key`, `ping`, `switch`, `chirp` |
| key word / hit | `stamp`, `boom`, `shing`, `knock` |
| counters | `ratchet` then `stamp` |
| typing | `key` every 3rd character, −27 dB |
| camera punch | `zoom_in` / `zoom_out`, `swish_up` / `swish_dn` |
| scene in/out | `slide`, `whip`, `portal`, `burn`, `shutter` |
| climax | `riser` (−20…−26 dB) into `shing` / `stamp` |
| cursor click | `click` at −19 dB exactly on the click frame |

- **Kinds added in `audio.py`:** `click` (down/up), `whip` (stereo), `shutter` and `burn`.
- **Levels:** −19…−27 dB peak against speech RMS of −17 dBFS.
- **Count:** about 60–110 events per clip.

Licensed SFX files work too. Put them in `build/sfx/` and map them by kind.

## Music
- **Source:** use the track the student supplies, from a library they hold a licence for. Set its path with the `MUSIC` env var for `audio.py`. It may be cut or crossfaded, and doesn't have to run the whole way.
- **No track:** use a simple dark synthetic bed. Never cute, never corporate.
- **Level:** music RMS = speech RMS − 22.5 dB, plus an extra duck of `1 − 0.55·speech` (smoothed over 0.25 s). Fade in over 0.4 s and out over 1.8 s.
- **A loud track** (≈ 112 BPM, dense) sits ≈ 22 dB under the speech RMS.
- Don't slow the track down for this style.
