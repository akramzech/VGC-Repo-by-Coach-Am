---
name: orangy-blues
description: >-
  "Orangy Blues": a locked 9:16 style for a LONG talking-head clip (1-3 min) where the words, analogy animations and
  full-screen B-roll are the edit, in an orange + blue palette. Kicker words blur in one by one, a HUGE orange-gradient
  word lands BEHIND the head (cut-out layer above, no stroke), serif-italic words land BELOW the chin; every sentence is
  also visualised with a small 2D/3D analogy (kettlebell + GB counter, trash bin, search bar to app card, files into a
  folder, AI orb, moon to sun, one figure standing out of a crowd, tilted 3D hub panel); a different card composition per
  section (logo dock, vertical column, row on the chest, cascade, fan); full-screen B-roll stills and phone footage with
  circle / wipe reveals; two film-burn transitions only (rotated to portrait, screen blend); trailer-movie music whose
  hits and drop are aligned to story beats; and a final "Result & Feedback" outro where the whole scene blurs and
  screenshots of student results enter one by one, almost full screen with a margin. Calm sine camera, footage grade
  untouched, never into the platform's right-hand rail or the top 168 px. Use whenever the student says "Orangy Blues",
  "style orange biru", or asks for a long 9:16 talking-head edit with kinetic words behind
  the head, analogy animations, trailer music and a blurred results outro, even without naming it. Built with
  HyperFrames; renders the real MP4.
---

# Orangy Blues

First built for a 69 s 9:16 talking-head clip (Nov 2026). Compared with a 3 s kinetic-words hero clip, this style has to stay interesting for a minute or more, so it adds: a different composition per
section, an analogy animation per idea, full-screen B-roll, trailer-style music aligned to story beats and a closing
results scene. The identity below is locked; the script, words, assets and which modules appear change per video.
Numbers and timings: `references/rules.md`. Module recipes: `references/modules.md`. Why each rule exists:
`references/analysis.md`. Read all three before building.

## Locked identity

| Layer | Rule |
|---|---|
| Frame | Full-frame 1080x1920, 30 fps, footage 9:16 never cropped or re-ratioed. The student's cut/trimmed sequence is NEVER touched (no cuts, no retime): everything is an overlay. Grade untouched, no tint or scrim on the face. |
| Palette | Orange `#ff6a1a` (words, accents) + blue `#1f5bff` (glow, orbs, borders, rings). Gradient words: `#ffb78a` to `#ff6a1a` to `#e23d00`. Ink `#0c0c10`. White support type. Third colours only inside real logos. |
| Kicker words | 1-3 small words per phrase, Poppins 800 ~56 px, white + hard dark drop shadow, blur-in one by one on the spoken word. Never inside the top 168 px. |
| Big word | ONE per phrase on the key word. Archivo Black caps, gradient, soft drop shadow only, **no stroke**. Behind the head: box top = head.top - 92 (cut-out layer above). Blur-in scale 1.5 to 1 in 0.3 s, +5 % drift, optional sparkle. |
| Front words | Playfair Display italic 700, white, BELOW the chin (chin + 80 px), staggered, blur-in 0.3 s, a thin sweep line under the group. |
| Reframe | When the shot is too tight or the head sits too low, glide the footage + cut-out together (scale 1 to 1.15 anchored bottom, 1.5 s) so head.top ~357 and chin ~870. Close-ups with no head (phone shots) put every word in FRONT. |
| Every idea is visualised | One analogy animation per sentence that has a picture in it (heavy = kettlebell, delete = trash bin, install = search bar + app card, put inside = folder, AI = orb, sleep = moon to sun, stand out = crowd). 2D flat shapes in the palette, front layer, below the words. See `references/modules.md`. |
| Break pattern | Card compositions DIFFER between sections (dock / column / row / cascade / fan / results slides). Never the same layout twice in a row. |
| Full-screen B-roll | Where the picture deserves it, show it full screen (still or video) with a reveal (circle, wipe up, wipe left, fade) and a slow 1.0 to 1.08 push; the beat under it moves its words to the front layer. |
| Transitions | Film-burn pack clips rotated to portrait (`transpose=1`), overlaid with `mix-blend-mode: screen` at ~80 %, ONLY 2 in the whole video, on the biggest music hit. Test each clip: a white full frame means drop it. |
| Safe area | Nothing in the top 168 px. Nothing in the right rail (x > ~940 px). Elements that rise from the bottom end by ~1600 px. |
| Camera | Calm sine glides 1.0 to ~1.06, no snaps, no shake. |
| Music | Trailer-movie / action-orchestral track, low under the voice, cut into 3-4 segments so a HIT lands on the first big reveal and the DROP lands on the line that pays off the video. Riser before the drop, boom on it. |
| SFX | Varied: low hit on big words, shutter on stills, click on cuts, bubbly pop per card, glass on panels, stamp on crosses, success on the final tick. Swoosh almost never. |
| Outro | The last scene (results / feedback): the whole frame blurs, a small title + big orange word + serif word appears, and 3-4 screenshots of student results enter one by one from the right, almost full screen with margins, each replacing the last. No end card button unless asked. |
| No-go | No prompt bar chip, no coloured overlay on the face, no white flashes, no stroke on big words, no text in the top 168 px or the right rail, no other company's logo as the student's brand (tool logos shown as the topic are fine, supplied by the student). |

## Workflow (storyboard first, always)

1. Probe the footage (1080x1920, HDR or SDR; HLG phone clips need tone-mapping to BT.709 before use). Transcribe with
   whisper, then take word onsets from the voice-energy envelope: `scripts/voice_env.py footage.mov` (Whisper times
   drift 0.2-0.3 s). Save them as `onsets.json` (a list of seconds).
2. Cut-out of the presenter: `npx hyperframes remove-background raw.mov -o assets/cut.webm --quality best`
   (large file, slow render; that is expected).
3. Head geometry: `scripts/measure_head.py footage cutout 0.5` (macOS) or measure from a snapshot. Decide the
   reframe window if the shot is tight.
4. Write the plan table (time | words | visual | technique | sound) per section; one analogy per idea, a different
   composition per section, music hit/drop targets. Wait for "ok".
5. Copy `template/build_example.py` to the project, edit its config blocks, run `python3 build_example.py <project>`,
   `npx hyperframes check` (0 errors), snapshot every beat.
6. Storyboard with `storyboard-frames`: 20+ frames for a long clip, 12 per sheet. Check for overlaps in EVERY frame,
   including mid-tween ones. Render only after "ok storyboard".
7. Render `npx hyperframes render <hf> -q delivery -f 30 -o <out>.mp4` (run it in the background), verify duration,
   loudness (`ebur128`, about -16 LUFS, peak < -1 dBFS) and grab frames from the MP4 itself.

## Known gotchas

- `fromTo` that starts later in the timeline renders its start state at t=0: add `immediateRender:false`.
- Never CSS-transform AND GSAP-transform the same element; wrap one in a parent.
- Rotating text inside a spinning orb looks broken; pulse it instead.
- A bool called `front` that clobbers a list called `front` is a classic generator bug; use distinct names.
- A transition clip that renders a full white frame must be dropped, not toned down.
- If a render shows an overlap that the storyboard did not, stop, fix, re-storyboard, then render again.
- zsh arrays are 1-indexed and an unmatched glob aborts a whole `&&` chain.
- Music and SFX come from the student's own licensed library; never copy them into this skill or the repo.
- Never ship the student's screenshots or recordings with the skill: blur names and IDs in anything public.

## Files

`template/build_example.py` (the generator with the worked 69 s example), `template/style.css` (tokenised CSS),
`scripts/voice_env.py`, `scripts/measure_head.py` + `face_box.swift`, `references/rules.md`, `references/modules.md`,
`references/analysis.md`.
