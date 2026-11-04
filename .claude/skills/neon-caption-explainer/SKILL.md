---
name: neon-caption-explainer
description: >-
  "Neon Caption Explainer": the locked edit for turning one raw talking-head or workshop clip into a punchy
  business-explainer video. Two-tier captions (a small white line plus huge yellow #FFFF00 Poppins 800 words, neon
  glow and a drop shadow, NO stroke, word-by-word pop-in), head-tracked cubic punch-ins, silences, breaths and
  stumbles cut, animated explainer B-roll that draws what is said on the word that says it (flow lines, barriers,
  meters, checklists, split cards, a screenshot with a cursor click), a tidy B&W showreel of the student's own
  videos behind the cut-out presenter, varied SFX, 16:9 first and then a rebuilt 9:16. Use whenever someone says
  "Neon Caption Explainer", "Neon Caption", "caption kuning neon", "style explainer caption kuning", or asks to edit
  a raw talking-head clip with big yellow neon captions and explainer B-roll, even without naming it. For videos
  longer than ~3 minutes with a cold-open hook, use long-form-video instead. Built with HyperFrames; renders the
  real MP4.
---

# Neon Caption Explainer

One camera, one presenter. Four things keep the viewer watching:
- tight cuts;
- head-tracked punch-ins;
- loud two-tier neon captions;
- B-roll that **draws the thing being said, on the word that says it**.

**Read in this order:**
1. `references/style-rules.md`: the locked decisions. Treat them as law.
2. `references/caption-dna.md`: the measured caption, colour and pace numbers.
3. `references/broll-animation.md`: how the B-roll must explain.
4. `references/pipeline.md`: commands, gotchas and the audit.
5. `references/sfx-music.md`.

## What a finished video contains

| Module | What it is |
|---|---|
| Opening | Start exactly where the student says. Nothing is added by default: no hook, no title card, no CTA. Design an opening only when it is asked for, for that video only |
| Captions | A small white line plus BIG yellow words, a per-word pop-in, a neon glow and a drop shadow, no stroke. Key words bold, connectors lighter |
| Counters | A big white number with a glow and a small yellow label |
| Camera | Head-tracked cubic in/out, ≥ 0.6 s each, on a low-passed head track. Wide ↔ punch ↔ split |
| Explainer B-roll | Navy overlays or right-hand cards built beat by beat (see `broll-animation.md`) |
| Showreel | One tidy row of equal panels behind the cut-out presenter: B&W background, presenter in colour with a white glow. The student's own videos only |
| 3-size frame | The same clip in 9:16, 1:1 and 16:9 playing in sync, with pill labels and equal margins. Only when the content is about sizes |
| Screenshot beat | A real app screenshot, cropped to what is safe to show, with a ring on the key control and an animated cursor click |
| Sound | Varied SFX (never the same family twice in a row) and the supplied music ducked under the voice |
| Grade | None by default. A subtle warm indoor-training grade only when asked (see the pipeline) |

## Storyboard first (must)

Make storyboard frames with the `storyboard-frames` skill (`.claude/skills/storyboard-frames/`) before any MP4 render, draft or delivery:
1. Build the composition.
2. Snapshot one still per beat onto numbered sheets.
3. Let the student refine frame by frame.
4. Render only after they reply "ok storyboard".

Every render step in the workflow below comes after that approval.

## Workflow

1. **Probe and plan** in chat. Show a beat list with the module for each beat, a sound plan, and what you need from the student. Wait for "ok".
2. **Cut:** run `edl.py`, then `cut.py`.
3. **Matte:** run `remove-background`, then `cutperson.py`.
4. **Build:** `build_gc.py` is the latest engine. Rewrite its beat list for the new clip. Then run `audio.py` and `hyperframes check`.
5. **Storyboard:** follow `storyboard-frames` until the student replies "ok storyboard".
6. **Audit and render.**
   1. Audit every beat (see `pipeline.md`).
   2. Render with the Bash tool's `run_in_background`.
   3. Verify the render, and deliver to `output/<name>_16x9.mp4`.
   4. Say plainly what you could not verify. You cannot hear the audio.

## Hard rules (short list)

- Captions have **no stroke**. Use a neon bloom in the letter's colour plus a dark drop shadow. Yellow is `#FFFF00`.
- B-roll and showreels use only the student's own videos and screenshots. No client content, other people's faces or private data. Crop app screenshots to safe rows.
- Keep the showreel tidy, never scattered. Zooms are smooth. Nothing overlaps or clips: every caption and card must fit inside 1920×1080.
- Cut silences, breaths, stumbles and fillers, so the duration may shrink. No CTA unless asked.
- B-roll must show the spoken idea (flow, barrier, meter, checklist), not decorate it.
- Reply in Bahasa Melayu.
