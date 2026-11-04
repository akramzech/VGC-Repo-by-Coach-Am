# Locked decisions: treat as law

These rules come from the first builds of this style (a daily-vlog series). The student usually writes Bahasa Melayu, blunt, and often by voice, so the text can be garbled. Extract the intent, say it back in one line, and ask only when the answer changes the work.

## Process
1. **Order:** plan → "ok" → build → storyboard → "ok storyboard" → render.
2. **Collecting feedback:** improvements arrive point by point. Understand them all first, and make no edits until the student says to proceed.
3. **Raw review:** give an honest review of the raw material before editing: coughs, transcript flow ("flow, storytelling, point") and what is off-message.
4. **Time estimates**, when asked, are a range with the biggest steps: cut + transcribe ~10 min, scenes ~20 min, matte ~10 min, render 5–8 min, checks ~10 min.

## Look
- **Captions:** yellow `#FFFF00` neon, no stroke. Red only for pain ("3-4 HARI", "HABIS?", "TAK BOLEH GUNA"). Green only for "sikit"/"ok".
- **Grade:** very light (`G3`). No darkening and no crushed blacks; a harsher grade raised shadow noise. The goal is no visible noise.
- **No split-screen:** no blue split-screen or side card. Use either a full-screen stage, or the presenter full screen with elements flying behind the head.
- **Mix stage and behind-head beats ("Campur"):**
  - Behind-head suits claims about the speaker's own world: their 100+ videos, price, race, benchmark, adapt, outro.
  - Stage suits explanations: battery, tasks, refill, two modes, three sizes, compare, usage.
- **All-out HyperFrames animation:** the visual must carry the message about three times better than the words alone. Draw the analogy literally.

## Hook
- 5–10 s at the very start, taken from the most climactic moment in the content, like a clip shot. This overrides the no-opening default of `neon-caption-explainer`.
- Example: "ada yang sampai 3-4 hari... dengan Claude... satu video siap dalam 15-20 minit" (8.2 s, pulled from the middle of the video).

## Real footage
- **When the speaker talks about their own output** ("Sebulan dengan 100 lebih video"), show REAL videos from the student's own folders, as a wall behind the head.
- **Screen every thumbnail before use** and exclude:
  - client work;
  - other people's faces;
  - other creators' content;
  - testimonials and student feedback;
  - screen recordings with account data.
- **Example clips for the compare beat:** cut off their CTA or end card.
- **The 3-size beat:** use the student's real 16:9 and 9:16 finals. The 1:1 is a centre crop of the 16:9.

## Sound
- **Make it clearly audible.** The first build, with music 21.6 LU under the voice and SFX peaks around −22 dBFS, was "tak dengar langsung".
- **Working values:**
  - music ~12–13 dB under the speech RMS, ducked 35 %;
  - SFX peaks −7…−14 dBFS (a later build went 10–15 % lower);
  - final −14.5 LUFS.
- **Licences:** use music and SFX the student holds a licence for. Check that the licence covers social media and sponsored content.

## Content decisions
- **Cut:** false starts ("7, eh bukan 7"), driving asides, "so nanti kita tengok lah", comment-question CTAs, coughs and dead air, breath or lip noise, "hmm" clicks.
- **Ending:** no CTA and no "subscribe" line. Reorder the outro so nothing is said twice, and end on the natural sign-off.
- **Optional beats:** if a recap beat has nothing in the speech to hang on, suggest it; don't force it.

## Latest rules (treat as law)
- **Minimal cutting.** Only long breaths, coughs, held fillers, pauses > 0.7 s and the CTA. Squeezing every silence and deleting short fillers made the speech hard to follow. Restore lines the student likes.
- **Graphics, not boxes.** No beat is just boxes and text: use 2D or 3D visuals that fit the theme, so the viewer can picture the situation. Check composition, animation and elements twice, with a frame audit every 1.5–3 s.
- **Use the student's own assets:**
  - logos of the AIs they name (ChatGPT, Claude, DeepSeek, Lovable, Manus);
  - their screenshots of those pages;
  - their own photos for a coach or about-me beat;
  - their own finished videos for training moments.
  Crop off burned-in captions.
- **Design wall:** the student's own design screenshots or inspiration boards, when given as FILES. Images pasted into chat are not saved to disk. Ask for the files, or draw synthetic 2D panels (menu, banner, poster, billboard) in CSS. Crop out sponsored ads and thumbnails with people.
- **Logo sources:** Cloudflare blocks headless screenshots of chatgpt.com, claude.ai and lovable.dev. Use the simple-icons CDN, favicon.ico, apple-touch-icon.png, or the student's own screenshots.
- **Mid-build messages:** each message the student sends during a build adds to the same plan. When they say "bagi plan dulu", reply with a plan first.
- **Margins:** keep ≥ 70 px from every frame edge, and ≥ 40 px between stacked blocks (slab to cards, cards to caption, caption to caption). Audit every stage beat for touching blocks, not just overlaps.
- **No geometric ambient layer** (orbs, rotating dotted rings, drifting squares) on dark stages. Stages are a plain smooth dark gradient.
- **Platform B-roll is full screen.** When AI platforms are mentioned, each platform's own screenshot fills 100 % of the frame:
  - a perspective tilt and a slow drift;
  - slide-left cuts;
  - a logo + name pill bottom-left.
  Then comes the stage beat. If a platform is missing, draw a simple chat screen and flag it to the student.
- **Cut edges sit in true silence** (envelope < −34 dB). Keep fillers glued to words with no silence on either side; cutting them clips words. Verify by transcribing the cut and reading the text at every junction.
