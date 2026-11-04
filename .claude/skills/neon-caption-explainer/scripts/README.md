# Scripts

Run them from a work dir `W/` that holds `src/main_raw.mov`, `build/`, `hf/` and `scripts/`. Use a Python with numpy, scipy and faster-whisper (on macOS often `/usr/bin/python3`).

| Script | Purpose |
|---|---|
| `transcribe_words.py` | `build/voice48_raw.wav` → `build/words_raw.json` (faster-whisper large-v3, BM) |
| `edl.py` | Silence squeeze plus manual removals (`REM`, `END`, start) → `build/edl.json` |
| `cut.py` | Frame-exact cut → `main.mp4`, `voice.wav`, `person.webm`, `timemap.json`. Set `GRADE_ON = True` only if the indoor grade was asked for |
| `cutperson.py` | Eroded-edge cut-out → `person_clean.webm` (same `GRADE_ON` as `cut.py`) |
| `headtrack.py`, `words_out.py` | Head track; word onsets in the cut timeline |
| `build_gc.py` | **Latest engine**, plus a workshop beat list as the worked example: diagram, table, screenshot click, split cards, showreels, neon captions. Rewrite the beat list per clip |
| `build_first_version.py` | The first build, for reference: outline-era captions and a 3-size frame |
| `mk916.py` → `build916.py` | String-patches the first build (copied to `scripts/build.py`) into a 9:16 version. For 9:16 from `build_gc.py`, apply the same patch ideas: screen-space reels, a `#cam2` cut-out layer, a caption band at y 1360 |
| `audio.py`, `sfxlib.py` | SFX and music mix. Set `MUSIC=<path to the student's track>` and a new seed base per video |
| `storyboard_stills.html` | Headless-Chrome mock-up stills, for planning before the build |

**Hard-coded per clip (check before reuse):**
- `END`, `REM` and the start word;
- every `wt('word', after)` anchor;
- the panel file names `assets/panels/*.mp4` and `assets/projects_crop.png`;
- the music path and the seed base.
