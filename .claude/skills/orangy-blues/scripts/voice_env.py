#!/usr/bin/env python3
"""Voice-energy envelope + syllable onset candidates for syncing words (Whisper times drift 0.2-0.3 s).
Usage: /usr/bin/python3 voice_env.py <footage.mov> [start=0] [dur=none]
Prints dB per 50 ms and the onsets (an energy minimum followed by a >= 6 dB rise within 80 ms).
Map the spoken syllables to these onsets by counting: e.g. 'Ja-ngan te-rus post kon-ten' -> 0.10 0.45 0.70 0.88 1.05 ...
Use the onset of a word's FIRST syllable for kicker/front words, and ~0.0-0.05 s earlier for the big word."""
import sys, subprocess
import numpy as np
foot = sys.argv[1]
ss = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
cmd = ["ffmpeg", "-v", "error", "-ss", str(ss)] + (["-t", sys.argv[3]] if len(sys.argv) > 3 else []) + \
      ["-i", foot, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"]
x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32)
hop = 160
n = len(x) // hop
e = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
es = np.convolve(e, np.ones(3) / 3, "same")
on = [i for i in range(2, n - 8) if es[i] <= es[i - 1] and es[i] <= es[i + 1] and es[i + 8] - es[i] >= 6]
print("envelope (t:dB):", " ".join(f"{i * 0.01 + ss:.2f}:{e[i]:.0f}" for i in range(0, n, 5)))
print("onsets:", " ".join(f"{i * 0.01 + ss:.2f}" for i in on))
