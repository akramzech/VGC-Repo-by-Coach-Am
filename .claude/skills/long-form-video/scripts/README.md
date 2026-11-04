# Scripts

Run them from a work dir `W/` outside any cloud-synced folder, holding `src/main_raw.mov`, `build/`, `hf/` and `scripts/`. Use a Python with numpy, scipy and faster-whisper (on macOS often `/usr/bin/python3`).

| Script | In → out |
|---|---|
| `transcribe_words.py` | `build/voice48_raw.wav` → `words_raw.json` (large-v3, BM) |
| `edl2.py` | `build/env.npy` → `build/edl2.json`. Edit `REM`, `HOOK` and `P1`–`P3` for the new clip |
| `cut2.py` | `edl2.json` + clip → `build/main.mp4` (graded), `voice.wav`, `timemap.json` |
| `words2.py` | `voice.wav` + `words_cut.json` → `words_out.json` (snapped onsets). Transcribe `voice.wav` first |
| `wall.py` | `build/wall_sources.json` (a list of `index|duration|relative path`) → `hf/assets/wall/row0-4.mp4`. Paths are relative to `WALL_ROOT` (default `input/`), the folder with the student's own finished videos |
| `build_engine.py` | Everything → `hf/index.html`, `build/sfx_events.json`, `build/bh_intervals.json`. The Day 1 vlog beat list is baked in as the worked example: copy it, then rewrite the anchors and scenes |
| `day1_beats/` | The pieces `build_engine.py` was assembled from: `a2` anchors, `n2` hook/compare/usage, `n3` price/race/wall/bench/adapt/outro, `t2` captions + camera |
| `day2_beats/` | A later build: the filler-fix loop (`fillfix.py`), new beats, remapping to a new cut (`mk_d3.py`) |
| `day3_beats/` | The latest build: `edl_d3.py` auto-shortens silences > 0.7 s to 0.5 s; `mk_d3.py` assembles the `build_engine.py` header + `body_d3.py` + the camera tail |
| `matte.py` | `bh_intervals.json` → `hf/assets/matte/<id>.webm` |
| `audio2.py` | `sfx_events.json`, `voice.wav`, `build/sfx/*.mp3` (the student's licensed SFX + `music1.mp3`, `music2.mp3`) → `hf/assets/audio/mix.wav` |
| `sfxlib.py` | Synth SFX kinds |
| `portrait/` | The engine rewritten for 1080×1920 (see its README) |
| `shorts_9x16/` | Cutting 30–55 s Shorts from the finished long-form (`prep.py` → `sN.py` → `finish.sh`) |

`template/storyboard/*.html` are headless-Chrome mock-ups (`?s=<n>` or `?s=price`), for planning before the build. They need `src/*.png|jpg` frames next to them.
