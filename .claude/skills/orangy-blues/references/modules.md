# Orangy Blues: module catalogue

Every module lives in the generator's `visuals` block (front layer, class `vz`, below the words) or in the grids /
B-roll / outro blocks. Flat 2D vector shapes (inline SVG) in the palette, soft shadow, small, placed mid-low (y 640-1250)
and away from the right rail. One analogy per idea. Words stay on top; the visual starts on the spoken word and is gone
before the next beat. Examples below are the worked 69 s clip; invent NEW metaphors for each new video.

| Idea said | Visual | Timing recipe |
|---|---|---|
| "heavy / many GB" | grey kettlebell drops in with `bounce.out`, shadow ellipse, a counter beside it climbs 128 GB, 512 GB, 1 TB, 2 TB | drop 0.6 s on the word; counter steps every 0.35 s |
| "uninstall / delete these apps" | four logo tiles fall into a trash bin, lid opens then shuts | tiles fall 0.15 s apart, lid rotate -25 to 0 |
| "search and install the app" | white search bar types the app name, the real logo card pops with a coral/brand mask, an orange Install button presses (`B2` text swaps "Install" to a tick) | type 0.8 s, card scale 0.5 to 1 back.out, button press scale 0.94 |
| "put everything in one folder" | small file chips fly into an orange folder, the folder lid closes | chips on curved paths 0.12 s apart |
| "AI does it" | blue orb with three expanding rings (`fromTo` with `immediateRender:false`), a pulsing label (do NOT rotate text) | rings 0.9 s loop, pulse 1.0 to 1.08 |
| "sleep, it is done tomorrow" | moon + Zzz cross-fades into a sun + tick; sun rays rotate | 1.2 s cross-fade |
| "stand out / compete" | row of grey people, one turns orange and steps forward | step y -26, scale 1.2 |
| "join the hub / community" | tilted 3D panel (real screenshot of the hub), blue glow behind, ghost trail copies, floats `y -14, rotationY -12` yoyo | enter from the right, 0.8 s float |

## Logo dock (tools being replaced)

Official marks of the tools named in the script, supplied by the student (SVG or app-icon PNG). Use the full-colour
SVG for multi-colour logos, a mask + solid fg for single-colour ones; never a favicon service that returns a generic
icon. A small red cross badge sits OUTSIDE the tile's top-right corner and stamps on the name being said
(`stamp` SFX, scale 2.4 to 1 back.out).

## Orbit (tried and replaced)

An orbit of cards around the presenter was built (4 cards on a tilted ring, back copies under the cut-out, front copies
above, keyframes every frame) and works: ring radius ~365 px, ellipse vertical 175 px, scale 0.86 +/- 0.28, `rotationY`
-sn x 26, perspective 1400, centre y 1085. The student preferred the blurred results scene for the closing, but an orbit
is a good way to show "all around me" lines. Keep the ring at a fixed centre; do not let cards wobble.

## Student results slides

See the Results outro in `rules.md`. Crop every screenshot from the ORIGINAL recording at native resolution (cropping an
already-small copy makes the near-full-screen card blurry), keep only the message bubble (no names, avatars or phone
numbers), fit by height (max 1100 px) and width (max 860 px).

## What to avoid

- The same grid layout twice in a row.
- A visual that sits behind or over the front words.
- Anything in the right rail (x > ~940 px) or in the top 168 px.
- Rotating text inside a spinning object.
- Stock-looking decoration with no meaning: every shape must be something the voice just said.
