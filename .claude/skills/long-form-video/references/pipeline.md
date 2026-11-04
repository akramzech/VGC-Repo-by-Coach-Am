# Pipeline (what worked, in order)

Work dir `W/` OUTSIDE any cloud-synced folder (Dropbox, iCloud, Google Drive): `src/main_raw.mov` (symlink to the clip), `build/`, `hf/`, `scripts/` (copy this skill's `scripts/`).
Use `/usr/bin/python3` (numpy, scipy, faster-whisper, cv2 without cascades); do NOT use `-I` (user site-packages hold numpy).

## 0. Probe
`ffprobe` frames/duration/colour; HLG needs tone-map. `df -h` (a 5 min 1080p CRF17 cut is ~400-600 MB, use `-preset veryfast -crf 18`).

## 1. Transcribe + envelope
`ffmpeg -vn -ac 1 -ar 48000 build/voice48_raw.wav` -> `transcribe_words.py ... words_raw.json "<terms>"` (large-v3, ~4-5 min for 5 min).
`build/env.npy` = 10 ms RMS dB. **Whisper times drift 0.2-0.5 s inside a run and up to ~3 s when you map between runs.** Always trust energy dips; verify by listening-by-transcript.

## 2. Raw-material review (report in BM before editing)
- Cough detector: burst candidates outside every Whisper word span (+-0.12 s) with rms > -30 dB, then spectrogram (`matplotlib specgram`, 0-8 kHz): cough = broadband noise 0-8 kHz for 0.3-0.4 s, no harmonics; held vowel = steady harmonics ("aaa"); breath = hiss 4-8 kHz.
- Dead air: runs where the 110 ms-smoothed env < -36 dB longer than 0.3 s (the old 5-frame env missed a 2.3 s gap because of tiny bumps).
- Flow notes: hook promise, jargon lines, duplicate statements, missing recap, off-message tangents, CTA lines.

## 3. Edit list (`edl2.py`)
`REM` = (from,to,why) removals; `HOOK` = (a,b) climax clip placed first; `P1/P2/P3` = reordered parts; squeeze(th -36 dB on `esl`, min 0.30 s, keep 0.20 s).
Pick every boundary on a dip (< -33 dB) found with a small env printout; a boundary on continuous speech clips syllables ("la", "se").
`cut2.py`: frame-exact `trim=start_frame/end_frame`, grade G3 + `tpad` 0.35 s tail, voice mono fold with 8 ms fades, writes `timemap.json` (`hook_dur`, `dur`).
**Re-transcribe `voice.wav` and read every junction** (found: leftover "la", "se", fragment "7"). Re-run until clean.

## 4. Anchors (`build_engine.py`, `day1_beats/a2.py`)
`wt(token|alt, after)` returns the snapped onset (`words2.py`). Chain anchors (`t_b = wt('x', t_a)`). Whisper spells numbers as words and varies per run
(`lima`, `seratus`, `tiga`, `dua`, `RM20`, `episod`, `Tim`, `cloud/Cloth` for Claude): always add aliases and re-print tokens after every re-transcription.

## 5. Scenes
- `scene(id,t0,t1,'full',bg,html)` stage; `bhscene(id,t0,t1,elements,foreground,bw=False)` behind-head (elements in `#wback` inside `#cam`, matte clip after them, text in front).
- Pop-in elements need a hidden initial state: `A()` emits `gsap.set` (INIT) because `fromTo(...immediateRender:false)` leaves them visible before their tween.
- Shake an INNER wrapper (a shake that ends at x:0 cancels a parent's x tween). Unique ids (a duplicate `z_b` silently killed a tween).
- Camera: sine tweens (0.8 s), keys only outside stage/behind-head windows, reset to 1.0 before each such window.
- `hyperframes check --json`: 0 layout errors; use `data-layout-allow-overlap` for intentionally stacked cards.

## 6. Matte (only behind-head intervals)
`matte.py` reads `build/bh_intervals.json`, trims each interval from `main.mp4` by frame, runs `npx hyperframes@0.8.216 remove-background tmp.mp4 -o hf/assets/matte/<id>.webm --quality best`
(4.8 fps on the M3 Pro: 75 s of footage = 7 min). One `<video class="clip pm">` per interval, `data-start=t0`, `data-media-start=0`.

## 7. Wall (`wall.py`)
5 strips x 22 tiles, each tile 112x199 from a different real ad (+ white 2 px border, 16 px gap), 12 s, hstack in ONE ffmpeg call per strip, ~40 s per strip when the sources are cached.

## 8. Audio (`audio2.py`) then render
`audio2.py` -> `hf/assets/audio/mix.wav` (prints speech RMS, music RMS, pre-LUFS and gain). Check voice/music/mix LUFS with `ebur128`.
Render: `cd W/hf && npx hyperframes@0.8.216 render --quality delivery --fps 30 --sdr -o renders/X.mp4` with the Bash tool's `run_in_background`, **from a non-Dropbox folder**.

## Gotchas (all hit in this build)
- Cloud-synced folders: rendering inside a Dropbox folder made `video_extract` run at 2.6 fps and time out after 15 min; the same project in /private/tmp rendered in ~4 min. Deleting/recreating folders inside a synced folder creates "conflicted copy" duplicates.
- `pkill -f script.py` leaves its ffmpeg child alive; two ffmpegs writing the same `main.mp4` corrupted it (black render, "Invalid NAL unit"). `pkill ffmpeg` too, then delete the file.
- `sed -i` on macOS needs `''`; use Python replaces. zsh does not word-split `$var` (use arrays / `$=VAR`).
- Whisper hallucination loops ("5 jam, 5 jam, ...") appear at fast speech; ignore repeated tokens.
- `hyperframes snapshot` lists "FFmpeg could not extract the frame" when the video is corrupt: it is the first sign.
- Counters must be `tl.set(textContent)` steps (onUpdate is suppressed while seeking).
- Cut-out edges: if a fringe shows, erode alpha 2 px + blur 0.7 px (see `neon-caption-explainer/scripts/cutperson.py`).

## QA lessons from a re-check ("banyak composition yg lari and error")
- **Audit the RENDERED mp4 every 2-3 s** (contact sheets of 9-12 frames with a time label), not only `hyperframes snapshot` + `check`; `check` reported 0 errors while the render still had broken beats.
- SVG `<line>` rotated by GSAP rotates around the element's box centre, not the pivot: use `svgOrigin:'cx cy'` on both from/to (stopwatch hands, refill ring hand). Same for needles drawn in HTML: set `transform-origin` explicitly.
- A scene that starts before the first thing is spoken shows an empty stage (compare beat sat empty 2 s, gauge title showed "KREDIT" alone): start the scene on the first spoken anchor minus 1 s, and reveal title words with their spoken word.
- Centre-aligned inline titles with separators ("KREDIT · TOKEN · USAGE") shift sideways as words pop in: put the separator inside the word's span.
- Absolutely-positioned children inside `.glass` cards (`.num/.lab` are `position:absolute` in the shared CSS) collapse on top of each other: give them `position:relative` + margins.
- Texts that sit in the same row as a counter (USAGE label vs 100%) overlap when the counter appears: fade the label out first.
- Big red words at the bottom-left over dark seat/door fabric lose contrast; keep the pain-red caption centred or add a stronger dark shadow.

## Day 2 lessons (2 Nov 2026)
- **Fillers ('aa', 'haa', 'okay') only show up when you re-transcribe the CUT audio** (Whisper on the raw clip drops them). Loop: cut -> transcribe cut voice -> any aa/haa/okay/eh/hmm token -> map time back to source via timemap -> add to `build/extras.json` -> recut; stop when the cut transcript has none (`day2_beats/fillfix.py`).
- Camera zoom keys that start just before a stage/behind-head scene get their reset key dropped by the overlap filter -> the zoom stays on through the scene and crops cards at the edges. Drop planned zooms within 2.4 s before a scene start and warn if a reset is missing.
- Cloudflare-protected sites (chatgpt.com, claude.ai, lovable.dev) screenshot as a "verifying" page in headless Chrome; use the student's own screenshots/logos instead. Logos: simple-icons CDN (openai, claude), favicon.ico via `Image.ico.getimage(maxsize)` for DeepSeek/Manus, apple-touch-icon.png for Claude/Lovable.
- Never drive a logged-in browser to read a private page (Facebook, banking): ask for screenshots instead.

## Remapping an approved build to a NEW cut (Day 2 V2)
When the cut changes after beats are built, do NOT retime by hand: keep the old timemap (`timemap_old.json`), write `M(t_old)` = old cut time -> source time -> new cut time (search main segments only, `_old[2:]`/`_new[2:]`, because the hook clips repeat source time), then regex-remap the trailing `,T);` of every GSAP statement, every SFX, SCENES, BHI and caption times (`day2_beats/mk_d3.py`). New beats are written with `M(old_time)` anchors. Hook length must stay identical.
The ambient layer (drifting orbs + rotating ring) that `scene()` can add is OFF for this style: stages are a plain dark gradient (see style-rules).
SFX level for the latest style: `SFX_BOOST = 7.5`, `MUSIC_GAP = 11`, final -14.6 LUFS.
