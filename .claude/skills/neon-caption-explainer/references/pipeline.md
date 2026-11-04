# Pipeline (what actually worked)

Work dir `W/`: `src/main_raw.mov`, `build/`, `hf/`, `scripts/` (copy this skill's `scripts/`). Use `/usr/bin/python3` (it has numpy, scipy, faster-whisper; Homebrew python does not).

## 0. Probe
`ffprobe` frames/duration; HLG (`arib-std-b67`) must be tone-mapped first, or HyperFrames renders HDR. 4K camera source: make a 1080p 30 fps working copy (`scale=1920:1080:flags=lanczos`, CRF 12, `-g 15`) and keep the 4K for a 9:16 crop. Check free disk (`df -h`).

## 1. Transcribe
`ffmpeg -vn -ac 1 -ar 48000` → `scripts/transcribe_words.py … words_raw.json "<term prompt>"` (large-v3). Fix terms by hand in captions. Build `env.npy` (10 ms RMS dB) and `wordlist.json`; **cut and sync on the envelope, not Whisper times** (`words_out.py` snaps words to onsets).

## 2. Cut (`edl.py` → `cut.py`)
Silence > 0.26 s at < −40 dB keeps 0.16 s; `REM` = manual removals (fillers, stumbles); `END` = last source second; the first `keep` start = where the video begins. `cut.py` trims **by frame** (`trim=start_frame/end_frame`; time-based trims lost frames) and writes `main.mp4`, `voice.wav`, `person.webm`, `timemap.json`.

## 3. Cut-out
`npx hyperframes remove-background src/main_raw.mov -o build/matte_raw.webm --quality best` (run via the Bash tool's `run_in_background`, 4 min per 1,000 frames) → `cutperson.py` (alpha eroded 2 px + 0.7 px blur removes the red fringe) → `build/person_clean.webm`; `headtrack.py` → `headtrack.json`.

## 4. Build
`scripts/build_gc.py` = latest engine. The beat list (captions, overlays, SFX) is clip-specific: rewrite it, keep the engine (`cap()`, `emit_caps()`, `reel()`, `overlay()`, `counter()`, camera, `shift_js()`). `SH` > 0 trims the start (everything earlier is dropped and shifted). 9:16: `mk916.py` patches the first build into `build916.py` (see the note in `scripts/README.md`).

## 5. Audio
`audio.py` reads `sfx_events.json` + `voice.wav` → `mix.wav`. Check the voice-vs-music gap per 0.5 s window (median ≈ 21–25 dB; the few windows under 12 dB are pause edges).

## 6. Audit (always, before saying "done")
1. `npx hyperframes check --json`: zero errors; read every `line_unread` (hold ≥ ~0.5 s + 0.3 s/word), `text_box_overflow`, `text_occluded`, `content_overlap`. Contrast warnings on small white text over a bright projector are expected; the drop shadow handles them.
2. `npx hyperframes snapshot --at <30 times, every ~2.5 s> -o ../snaps --no-end` and open every contact sheet: look for clipped text (captions with 2 lines need y ≤ 850 at font 130), text crossing card edges, overlays colliding with captions, empty half-cards.
3. Re-snapshot the specific beats you changed.
4. Render, then pull frames **from the MP4** (`ffmpeg -ss t -i out.mp4`), plus `ffprobe` (h264 yuv420p bt709 30 fps) and `ebur128` (≈ −16.6 LUFS, peak ≈ −2 dBFS).
5. Say what you did not verify: you cannot hear the audio.

## 7. Render
`cd hf && npx hyperframes render --quality delivery --fps 30 --sdr -o renders/X.mp4` via the Bash tool with `run_in_background: true` (a `nohup … &` shell dies with `render_cancelled_parent_exited`). ≈ 2 min per 80–117 s of 1080p.

## Indoor training-room grade (only when the student asks)
Applied to BOTH the video and the cut-out inside `cut.py` and `cutperson.py`, after `setpts` and before `format=yuv420p` (set `GRADE_ON`):
`eq=contrast=1.07:saturation=0.94:gamma=0.96:brightness=-0.01,colorbalance=rm=0.035:gm=0.005:bm=-0.035:rh=0.02:bh=-0.02:rs=0.015:bs=-0.015,curves=all='0/0 0.12/0.10 0.5/0.5 0.88/0.90 1/0.97'`
Effect: warmer mids/skin, red banner a touch deeper, projector highlights pulled in. Compare before/after side by side first. Otherwise do not grade.

## Gotchas
- GSAP `onUpdate` callbacks are suppressed while the renderer seeks → counters = `tl.set(textContent)` steps; the camera = one `fromTo` per frame on `#cam`.
- Camera keys must continue from the truncated value of the previous key (no jumps); smooth the 5 Hz head track (σ ≈ 0.85 s).
- `fromTo` second tween on the same property needs `immediateRender:false`; unique durations for videos sharing a source (`duplicate_media_discovery_risk`).
- Any SFX added after the time shift must already be in final-timeline seconds (a stale offset put events at negative times, silently).
- Define a `.abs{position:absolute}` rule in the composition CSS if scenes use that class (the storyboard HTML had it, the composition did not: overlay content collapsed).
- CSS `drop-shadow` glow and `grayscale()` on `#pmat/#base` pass `hyperframes check`.
- zsh does not split `$E` variables for ffmpeg options: use `bash -c` with arrays.
- Hard-link big assets into `hf/assets` (`ln`); `ffmpeg -y` overwrites the same inode, so linked copies update too.
