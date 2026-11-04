# Portrait (1080×1920) adaptation

First built for a 30 s walking selfie.

## `build_p.py`
`build_engine` rewritten for 1080×1920:
- captions at y=1000, below the face and above the 1330 UI line;
- a 30-character limit per big-word line;
- stages at 1080×1920;
- behind-head beats with a matte only for their intervals (`BHI`);
- an fg-only overlay kind `'fg'` (no matte), for when the head would hide the element;
- half-strength camera (max 1.12), only in free windows.

## `audio_p.py`
`audio2` with `SFX_BOOST 7.5`, `MUSIC_GAP 11` and a single music track (offset 8 s). Final target −14.6 LUFS.

## Run order from `W/`
`cut2.py` → `transcribe_words.py` → `words2.py` → `build_p.py` → `matte.py` → `audio_p.py` → `hyperframes check` → storyboard → render.
