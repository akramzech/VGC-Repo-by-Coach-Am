# Orangy Blues: numbers and recipes

All px are on the 1080x1920 canvas. "Units" are the 558x992 layer space the generator uses
(back layer px = 130 + 1.55 u, front layer px = 1.9355 u).

## Layer order (bottom to top)

1. footage video (`#rf1`, inside a scaled wrapper)
2. back words `.ub` (kicker words, BIG word) scale 1.55, offset (107,130)
3. cut-out video `cut.webm` (`#rf2`, same reframe + glide wrappers as the footage)
4. full-screen B-roll (video `#djiw`, stills `.brw`) and the results scene (`#finblur`, title, cards)
5. front layer `.uf` (scale 1.9355): card grids, analogy visuals, front words, sweep lines
6. transitions (`mix-blend-mode: screen`, opacity 0.8)

The footage and cut-out ride the same wrappers, so reframe and glide zoom move both. Beats covered by a full-screen
still use `flayer=True` (their big word goes to the front layer so the still cannot hide it).

## Head geometry (measure once)

| Element | Rule |
|---|---|
| Kicker row | top = max(168, head.top - 200); a 2nd word sits +34 u lower and +142 u right |
| Big word | box top = head.top - 92 (short words 4 letters or fewer: head.top - 150 in u terms); font = min(245, 820 / (0.8 x letters)) |
| Front word | top = chin + 80 (+ dy); ~96 u; dx staggers left/right; long lines use 44 u |
| Sweep line | under the first front word, width 360 u |
| Phone close-up shots (no head) | `zone="low"`: kickers at y 800, front words at y 940, no big word behind the head |

Reframe used in the example: `f("#rf1, #rf2", {scale:1}, {scale:1.15, duration:1.5, ease:"power2.inOut"}, 5.5)` with
`transform-origin: 50% 100%`, giving head.top 357 and chin 870 for the rest of the clip.

## Timing recipes (seconds)

- Kicker: blur-in 0.22 s (`y 18, scale 1.15, blur 10 to 0`, power3.out) on the first-syllable onset.
- Big word: onset - 0.02, 0.30 s power4.out from `scale 1.5, y -14, blur 16`; +5 % drift 0.5 s later; sparkle 0.4 s back.out(2).
- Front word: onset, 0.30 s power3.out from `y 34, rotate -3, blur 12`; sweep 0.32 s scaleX 0 to 1.
- Phrase exit: `y -12, blur 8, opacity 0` in 0.16 s. A beat must be gone before the next one starts (the generator prints OVERLAP).
- Zoom glides: 1.0 to 1.04 to 1.0 to 1.05 ... every 5-8 s, sine.inOut, max 1.06. No snaps.
- Keep a word on screen at least 0.4 s before it leaves.

## Composition variety (the "break pattern" rule)

One card layout per section; the next section MUST use a different one. Modes in the generator (`G` list):

| mode | Where | Motion |
|---|---|---|
| `dock` | flat row of logo tiles under the chin (chin + 365) | pop in 0.15 s apart, small red cross stamps on each |
| `column` | tall strip on the LEFT edge (x 34 px), perspective `rotationY 22` | slow vertical scroll through 5 videos |
| `row` | strip on the chest, `rotationY -20`, perspective 900 | slow slide left, drops 88 u before the first front word |
| `cascade` | overlapping cards rotated -5 to 4 degrees | enter from the right, 0.2 s apart |
| `fan` | 4 cards fanned around one pivot | rise with back.out |
| `pair` | two floating cards, perspective tilt | gentle y float |
| `grid2` | 2x2 grid | enter from the right |

Card sizes (units): dock 96x96, column 110x196, row 100x182, cascade 190x250, fan 150x270, pair 190x320.
Card content kinds: `video`, `img`, `logo`, `txt`, `gr` (gradient word), `zoom` (crop with focus frame), `rm` (cut-out on
checker), `cap` (image + caption bar), `tele` (chat recording).

## Full-screen B-roll

- Phone / camera video: `#djiw` full frame with a circle reveal `circle(0% at 50% 55%)` to `150%` in 0.45 s, fade out 0.2 s.
- Stills (`BR` list): reveal one of `circle` (with `at`), `up`, `left`, `fade`; slow push 1.0 to 1.08 over the still's duration;
  0.2 s fade-out. Use different reveals back to back.
- Beats under a still: `flayer=True` so their words sit in the front layer.

## Transitions

Pack clips are 16:9; rotate with `ffmpeg -vf transpose=1`, overlay with `mix-blend-mode: screen` at 80 %. Use two:
one on the first HIT, one on the biggest moment. Check a frame from each; a clip that gives a full white frame goes.

## Music alignment (trailer track)

1. Find the track's hits and drop (look at the energy envelope, `ffmpeg -af astats` or a waveform): note `HIT` (first
   big hit), `DROP`, the breakdown length, and where it stays loud.
2. Choose the story beat that pays off the hook (HIT) and the line that pays off the video (DROP).
3. Start offset `ME = hit_video_time - hit_media_time`. Then DROP lands at `ME + drop_media_time`.
4. Cut the track into 3-4 `<audio>` segments with different volumes: intro hit loud (0.35), bed very low under speech
   (0.11), breakdown louder (0.30) into the drop, then a low tail (0.095) with a long fade-out.
5. Riser (short) 2-3 s before the drop, boom ON the drop. Never let the bed fight the voice: voice about 18-22 dB above it.
6. Final mix target about -16 LUFS integrated, true peak below -1 dBFS. Listen once end to end; if the student says it is
   not right, change the TRACK, not only the volume.

## SFX vocabulary (file names the generator expects in `assets/sfx/`)

`lowhit` (big word), `shutter` (still reveal), `click` (cut / UI), `bubbly` (card pop), `glass` (panel, orb),
`stamp` (cross mark), `key` (typing), `success` (final tick), `riser_short`, `riser_long`, `boom`. The student supplies
licensed files under these names; never commit them.

## Results outro (the last 5 s)

- From T0: `#finblur` = a full-frame div with `backdrop-filter: blur(38px)`, opacity 0 to 1 in 0.5 s (no tint, no dim).
- Title: kicker "Result &" (Poppins 800, 54 px, top 178), big "FEEDBACK" (Archivo Black 132 px, orange gradient, top 226),
  serif "student" (Playfair italic 70 px, top 372). Start them 0.3 s after the blur starts so no earlier word overlaps.
- Cards: 4 screenshots / recordings of student results, each cropped from the original at native resolution (no names or
  avatars), box = max height 1100 px, max width 860 px, top 480, centred. They enter one by one every ~1.15 s from
  x +980 with `rotationY -22, scale .94` over 0.55 s power3.out, then breathe to scale 1.025. The previous card fades out
  to x -90 in 0.35 s. The last card stays to the end. A soft pop per card.
- Remove all other words and animations after T0; the outro is a separate scene.

## Loudness and verification

`ffmpeg -i out.mp4 -af ebur128=peak=true -f null -` then read I and True peak. Grab frames from the rendered MP4 at every
module change (analogy, grid, still, outro) and compare with the storyboard.
