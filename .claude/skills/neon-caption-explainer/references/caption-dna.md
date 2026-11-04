# Caption and pace DNA (measured, not guessed)

Measured frame by frame from two long-form business YouTube videos used as references (not shipped with this skill).

## Reference 1 (10 min, 1080p/30)
- 69 cuts, median gap 5.6 s (minute 1: 15 cuts, then 4–7/min). Infographics held 20–60 s, built progressively.
- Shots: static studio medium shot, second 3/4 angle for variety; split layout (presenter left, dark list/data right); full-screen inserts (channel page, stage footage + counter, product shot with a purple progress bar); one full-frame blur punch (~2.5 s) on a topic change.
- Infographics: navy `#0F1224`-ish, white line icons, a lime headline, signposts/tables built element by element.

## Reference 2: the caption benchmark (16 min, 1080p/30, 73 cuts, median gap 7.5 s)
The first build looked flat next to it: the reference uses a little neon and, instead of a stroke, a drop shadow for depth.
- **No stroke.** Depth = a neon bloom in the letter colour (3 layers: 0.05 em, 0.2 em, 0.45–0.5 em) + a soft dark drop shadow beneath.
- **Yellow measured: RGB (254, 254, 0) = `#FFFF00`.** White text is `#FFFFFF` with a white bloom.
- **Two weights in one line**: key words Poppins ExtraBold 800, connectors 600, small line 500 (white, faint glow). e.g. "IN A **WORLD** OF **AI**".
- Stages: deep navy `#0F1224` with a soft vignette (white-text slides) and deep purple `#2B0F5C`→`#4B1D96` with glass cards and numbered badges "01 02 03" (framework slides); duotone silhouette + hand-drawn red ellipse around a word.
- Footage: cool navy curtains, warm skin; captions sit in the lower third.

## CSS recipe (latest build)
```css
.bw.y{color:#FFFF00;text-shadow:0 0 .05em rgba(255,255,0,.95),0 0 .2em rgba(255,255,0,.6),0 0 .45em rgba(255,255,0,.35),
      0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}
.bw.w{font-weight:600;color:#fff;text-shadow:0 0 .06em rgba(255,255,255,.9),0 0 .2em rgba(255,255,255,.5),0 0 .45em rgba(255,255,255,.28),/* same dark layers */}
.sm{font-weight:500;color:#fff;text-shadow:0 0 .1em rgba(255,255,255,.7),0 0 .35em rgba(255,255,255,.3),/* same dark layers */}
.bg2{font-weight:800;text-transform:uppercase;line-height:1.04;letter-spacing:-.012em}
```
The dark layers must be strong: the reference mostly sits on dark, a workshop clip sits on white projector screens and white shirts, where glow alone vanishes.

## Pace
Visual change every 3–6 s in the first 30 s, then every 5–10 s; an infographic or counter every ≈15–20 s; never > 8 s of identical framing without a caption change or camera move.

## Mapping
| Reference | Module |
|---|---|
| two-tier neon captions | `cap()` |
| counters with a label | `counter()` + `.num` |
| progressive navy infographics | `overlay()` + the patterns in `broll-animation.md` |
| split layout | `splitov` / `splitA` + camera `sx 470` |
| blur punch | `#cam` blur tween at section changes |
| thumbnail grid / channel inserts | showreel of the student's own videos |
