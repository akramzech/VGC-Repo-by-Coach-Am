# Locked decisions: treat as law

The student usually writes Bahasa Melayu, short and blunt. Reply in BM.

## Process
1. **Plan first, storyboard second, render last.** Never build the full video before the plan is approved. Never render it before "ok storyboard".
2. **Cut:**
   - Remove silences, breaths, thinking pauses, mis-spoken lines and fillers ("Haa", repeated starts). The duration may shrink, for example 136 s → 107 s.
   - Start where the student says.
   - No CTA unless asked.
3. **Order:** deliver 16:9 first. Make 9:16 only when asked ("buat 9:16").
4. **Fixes:** when the student sends a screenshot of the exact frame to fix ("Betulkan margin kiri kanan"), fix that and re-send that frame.
5. **Audit:** before saying it is done, run the full audit in `pipeline.md`.
6. **The opening is decided per video.** Add nothing at the start by default. Build an opening only when the student asks for one for that video.

## Caption look
No stroke. A neon bloom in the letter colour plus a dark drop shadow for depth. Yellow `#FFFF00`, white `#FFFFFF`. See `caption-dna.md`.

## Showreel (floating panels behind the presenter)
- Use only the student's **own past videos and screen recordings**. Leave out:
  - client content;
  - other people's faces;
  - any recording that shows private pages, accounts or URLs. Check every frame of a recording before use.
- Scattered 3D cards look messy and were rejected. Use **one tidy row of equal-size 9:16 panels**: one shared tilt, a slow marquee, behind the cut-out presenter.
- While it runs, the **background is B&W and the presenter is in colour with a white glow** (a 3-layer drop-shadow on the cut-out). The panels stay in colour.
- When asked to replace B-roll, don't reuse the panels that were just rejected.

## 3-size frame (only when the content is about sizes)
The same clip in 9:16, 1:1 and 16:9 playing in sync:
- yellow pill labels on one baseline, with a grey platform line;
- **equal outer margins and gaps**.

## Camera and picture
- **Zoom:** smooth, because jerky zooms look like a glitch. Cubic in/out of at least 0.6 s, a low-passed head track, and no overlapping camera keys.
- **Grade:** footage grade untouched by default. The **exception** is when asked ("adjust color grading untuk indoor training vibe, tanpa nampak pelik"). Then apply the subtle grade in `pipeline.md` to the video and the cut-out identically.
- **Face:** no scrim, vignette or tint on the face. Glints on glasses come from the source; they are not bugs.
- **Captions:**
  - Captions never overlap each other. Clamp an earlier group when the next one starts.
  - Keep captions fully inside the frame.

## B-roll must carry the message
Every analogy must land visually: see `broll-animation.md`.

## Sound
- **Varied SFX:** never the same family twice in a row. Rotate mouse click, ting, keyboard, swoosh, slide, zoom, camera shutter, film burn, riser, boom and stamp.
- **Music:**
  - Dark and energetic: not cute, not corporate, no dizzying repetitive beat.
  - Always ducked under the voice.
  - Use the student's own licensed tracks. They may be cut or crossfaded.
  - Without a track, use the synthetic SFX and a simple dark bed.

## Assets from links
Before downloading, check the size (`curl -sIL "<url>&dl=1"`) and free disk (`df -h`). A shared folder can be a 20 GB zip, so ask for specific files instead.
