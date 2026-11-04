---
name: long-form-video
description: >-
  "Long-Form Video": the locked long-form edit (3–10 min, 16:9) of one single-camera vlog or talking-head clip. A
  5–10 s cold-open HOOK cut from the video's most climactic line, two-tier yellow #FFFF00 neon captions (no stroke),
  minimal cuts (only long breaths, coughs, held fillers, long pauses, tangents), a very light grade, and every idea
  illustrated: full-screen HyperFrames stages that draw the analogy on the spoken word (battery = usage, gauge, race,
  price) and behind-the-head scenes where the cut-out presenter stays full screen while elements or a wall of the
  student's own videos fly behind the head. No split-screen, audible music and SFX, plus 9:16 Shorts cut from the
  finished video. Use whenever someone says "Long-Form Video", "Long Form", "video panjang YouTube", "edit vlog
  panjang", "vlog harian", or gives a raw single-camera clip over ~3 min to turn into a YouTube video. For short 9:16
  ads use neon-caption-explainer. Built with HyperFrames; renders the real MP4.
---

# Long-Form Video

One camera, one presenter, 3–10 minutes. The edit must:
1. hook in the first 5–10 s with the video's own climax;
2. never leave a spoken idea un-illustrated;
3. feel loud and alive without hurting the eyes.

**Read first:**
1. `references/style-rules.md`
2. `references/pipeline.md`
3. `references/broll-patterns.md`
4. `references/sound.md`

The caption look matches `neon-caption-explainer` (see its `references/caption-dna.md`).

## What a finished video contains

| Module | What it is | Where |
|---|---|---|
| Cold-open hook | A 5–10 s **climax clip** cut from later in the video (the strongest claim plus a number). It has its own graphics (calendar flip, struck-out card, stopwatch), a riser into a boom, and a whip into the real start | `n2.py` HOOK block, `edl2.py` `HOOK` |
| Captions | A small white line plus BIG words: yellow `#FFFF00`, red `#FF4D4D` only for pain or blocked. Neon bloom and a dark drop shadow, **no stroke**, a per-word pop-in on the spoken word | `grp()` / `emit_caps()` |
| Stage beats (full screen) | A purple `#4B1D96→#140a33` or navy `#0F1224` stage. Examples: a hero battery, gauge, task cards, 3-size export, refill, daily/weekly | `build_engine.py` scene blocks |
| Behind-head beats | The presenter full screen (a cut-out via `remove-background`, only for these intervals), with elements and text behind or in front. On the wall beat: B&W background and a white glow | `bhscene()` |
| Real-video wall | 5 rows × 22 tiles (112×199) of the student's own finished videos: marquee, tilted, behind the head | `wall.py` + `s_wall` |
| Compare beat | Two of the student's real example videos (muted) side by side, with pills | `s_cmp` |
| Camera | Slow sine punch-ins between 1.0 and 1.28, never during stage or behind-head scenes. The hook ramps to 1.42 | `t2.py` CAMERA |
| Grade | Very light: `hqdn3d=1.0:0.8:2.5:2.0`, `eq` contrast 1.03 and saturation 1.04, tiny warm mids. Median luma unchanged | `cut2.py` `G3.txt` |
| Sound | Two music tracks the student supplies, cross-faded ~12 LU under speech. SFX clearly audible. Final ~ −14.5 LUFS | `audio2.py` |

## Storyboard first (must)

Make storyboard frames with the `storyboard-frames` skill (`.claude/skills/storyboard-frames/`) before any MP4 render, draft or delivery:
1. Build the composition.
2. Snapshot one still per beat onto numbered sheets.
3. Let the student refine frame by frame.
4. Render only after they reply "ok storyboard".

Every render step in the workflow below comes after that approval.

## Workflow

1. **Probe and transcribe.**
   1. Transcribe with large-v3 (`transcribe_words.py`).
   2. Build `env.npy` (10 ms RMS dB).
   3. Fix Whisper's number words ("lima", "seratus", "tiga", "RM20") with aliases in the anchors.
2. **Analyse before editing**, and report in BM:
   - coughs, breaths and dead air (spectrogram plus the burst detector, see the pipeline);
   - transcript flow and storytelling: hook, concept order, duplicates, a missing recap;
   - off-message tangents and CTA lines to cut.
3. **Choose the hook:** the most climactic 5–10 s (a claim plus a number). **Verify its boundaries by re-transcribing the cut audio.** Whisper times drift up to 3 s between runs, so trust the envelope dips, then check the text.
4. **Plan.** Show the beat list: which beats are stage and which are behind-head. Ask only the one real decision. Wait for "ok".
5. **Cut.**
   1. Run `edl2.py`, then `cut2.py`.
   2. Re-transcribe the cut voice and check that every junction reads cleanly.
   3. Run `words2.py`.
6. **Assets.**
   - The student's example clips, with any CTA or end cards cut off.
   - Wall strips (`wall.py`), after screening out client work, other people and other creators' content.
   - SFX and two music tracks the student supplies.
7. **Build.**
   1. Build the composition (`build_engine.py`; clip-specific beats live in a folder like `scripts/day1_beats/`).
   2. Run `hyperframes check` (0 layout errors).
   3. Snapshot every ~5 s, plus an extra frame at every beat change. Fix overlaps and clipping.
8. **Storyboard:** follow `storyboard-frames` until the student replies "ok storyboard".
9. **Matte, audio, render.**
   1. Matte only the behind-head intervals (`matte.py`, about 8 min per 75 s of footage).
   2. Mix the audio (`audio2.py`).
   3. **Render from a local folder that is not cloud-synced** (`run_in_background`).
   4. Pull frames from the MP4, and check it with `ffprobe` and `ebur128`.
10. **Deliver** to `output/<name>_16x9.mp4`. Say what you could not verify; you cannot hear the audio.

## Hard rules (short list; details in `references/style-rules.md`)

- **Hook first:** a 5–10 s climax clip at 0:00. Not a title card. No logo and no CTA anywhere.
- **No split-screen or side card.** Use either a full-screen stage beat, or the presenter full screen with elements behind the head.
- **B-roll is real 2D/3D graphics that fit the theme, never just boxes and text.** Use:
  - drawn illustrations;
  - perspective-tilted screenshots, photos and clips;
  - falling, stacking and filling motion.
  Stages sit on a plain smooth dark gradient, with no geometric ambient layer. Don't use `preserve-3d` (it renders black); use perspective transforms on flat planes.
- **Draw the idea on the word that says it:** battery = usage, calendar pages = days, stopwatch = minutes. Never invent numbers the speaker didn't say; use relative bars only.
- **Cut MINIMALLY.**
  - Remove ONLY long breaths, coughs, held fillers (aa/haa/okay > ~0.45 s), pauses > 0.7 s (trim them to 0.5 s) and the CTA.
  - Keep every full sentence, the normal pauses and the short fillers glued to words.
  - Cut edges only in true silence.
  - Verify by re-transcribing and listing every missing word.
- **Wall and B-roll sources** are the student's OWN finished videos only. Exclude client work, other people, other creators, testimonials and screen recordings with private data.
- **Music and SFX must be audible.**
  - Music sits ~11–13 dB under the speech RMS.
  - SFX peaks around −9…−16 dBFS.
  - Never use the same SFX family twice in a row.
- **Platform mentions** (ChatGPT, Claude, …) get full-screen screenshots of each platform, from the student's own screenshots.
- **Margins:** ≥ 70 px to the frame edges and ≥ 40 px between stacked blocks.
- **Grade:** stays light and must not raise noise.
- **Processes:** never leave orphan ffmpeg processes. Kill the child processes too.
- Reply in Bahasa Melayu: short and blunt.

## Shorts from the long-form (9:16, 30–55 s)
- **Order:** resequence; never copy one contiguous chunk. The hook is the strongest sentence, then the problem, then the payoff. Every junction falls at a sentence end, in true silence.
- **Mapping:** map spans from the FINAL long-form timeline back to the source with `short_edl.py`. **Keep the long-form's own cuts inside each span**, or the cut fillers come back.
- **Verify:** transcribe the short and read every junction. If Whisper hallucinates "Terima kasih", pass it a topical prompt.
- **Crop:** 608×1080 around the face → 1080×1920.
- **Beats:** full-screen portrait B-roll, from the kit in `scripts/shorts_9x16/kit.py`. Captions go in the lower third on presenter shots. Titles ≤ 116 px. Keep the bottom 200 px free.
- **Tools:** `prep.py NAME spans...` → `sN.py` (beats) → `finish.sh NAME DROP_AT` (mix + check) → `hyperframes render`.
- **TikTok safe area:** all stage content lives between y 260 and ~1500, and x 148–932 (the kit's `SAFE_S=.725` wrapper). The context pill sits at y 196, presenter captions at y 1150. Check with a contact sheet that draws guide lines at y 170 / 1500 and x 940.
- **Clarity in the first 10 s:** the short says what it is about (a context pill) before or with the hook. Never open mid-sentence. Every hook claim is paid off in the same clip.

The 9:16 adaptation of the whole long-form engine is in `scripts/portrait/`.
