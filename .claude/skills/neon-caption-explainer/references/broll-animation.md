# B-roll that carries the message

The rule: every B-roll beat
must **draw the idea as it is spoken**, element by element, on the word that names it. Decoration does not count.

## Patterns that worked (workshop example) — all in `scripts/build_gc.py`

| Idea in the speech | Visual | Key motion |
|---|---|---|
| "Claude must not reach inside the computer" | computer card ← red dashed barrier → cloud card | arrow runs at the barrier, bounces back, red ✕ stamps, card shakes (5 × 40 ms offsets) |
| "so we use GitHub or Drive" | two clouds (GitHub yellow, Drive white) joined to a lime CLAUDE node | dashed lines flow (animate `strokeDashoffset`), dots travel along the lines on the word |
| "cloud vs local" | two-column table, ONLINE (green) / DALAM KOMPUTER (red) pills | rows slide in on "Claude", "GitHub", "folder"; red "TAK ADA AWAN" pill stamps |
| "press + and it calls the setting" | real screenshot of the project rows, tilted | cursor glides in, ring pulses on "+", ripple on the click, settings card slides in and ticks Repo / Folder / Environment one by one |
| "everything lands in the folder on my computer" | laptop outline with a folder; six video thumbnails drop in | thumbnails fall into the folder on the words, folder glows on "folder" |
| "computer gets heavier / internet slow" | row cards with a red bar that fills fast (heavy) and a yellow bar that crawls (slow) | `scaleX` tweens, linear for the crawl so it feels slow |
| "download from Drive, into GitHub, then edit" | DRIVE → GITHUB → EDIT VIDEO chips | each chip lights on its own spoken word |
| "all my past videos" (the student's own) | showreel row behind the presenter | B&W background, white glow on presenter |

## Rules
1. One idea per beat, the picture is complete when the sentence ends.
2. Time every element from the word list (`wt('word', after)`), never from guesses; hold each caption ≥ the readability floor
   (`hyperframes check` warns `line_unread`; ~0.5 s + 0.3 s per word).
3. Use the presenter's side: when a card sits on the right, pin the camera left (`sx 470`) and put captions on the left.
4. Always leave the bottom ≈ 230 px for captions: overlays end by y ≈ 790; a caption of font 130 needs y ≤ 850.
5. Card text must fit its card: `white-space:nowrap` plus a font size measured at 1920 wide (a 46 px line wrapped and a
   bar covered the second line: `text_occluded` error).
6. Real screenshots only for apps; crop them (project rows only). Mock UI only if no file exists, labelled as mock.
7. Keep each icon simple (stroke SVG, 6–7 px); one yellow accent, red only for "blocked/slow/heavy", green only for "online/ok".
