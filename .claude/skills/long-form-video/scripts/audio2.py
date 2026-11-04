#!/usr/bin/env /usr/bin/python3
"""V2 mix: voice + the SFX files and music tracks you supply in build/sfx/ (louder, lighter duck) -> hf/assets/audio/mix.wav"""
import json, sys, subprocess, re, numpy as np, scipy.io.wavfile as wf
sys.path.insert(0, 'scripts')
import sfxlib as L
from sfxlib import SR
ev = json.load(open('build/sfx_events.json')); DUR = ev['dur']; N = int(DUR * SR)
SFX_BOOST = 9.0; MUSIC_GAP = 13.0; DUCK = .35
def load(path, ss=0, t=None):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(ss)] + (['-t', str(t)] if t else []) + ['-i', path, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'build/voice.wav', '-af', 'highpass=f=75,acompressor=threshold=0.09:ratio=2.2:attack=8:release=120:makeup=1.6', '-ar', str(SR), 'build/voice_proc.wav'], check=True)
sr, v = wf.read('build/voice_proc.wav'); v = v.astype(np.float32) / 32768; v = np.pad(v, (0, max(0, N - len(v))))[:N]
SD = 'build/sfx/'
ES = {'shutter': ('shutter.mp3', 0, .75), 'key': ('key.mp3', 0, .2), 'click': ('click.mp3', 0, .2), 'boom': ('boom.mp3', 0, 2.4),
      'stamp': ('stamp.mp3', 0, 1.0), 'zoom': ('zoom.mp3', 0, 1.6), 'slide': ('slide.mp3', 0, 1.3), 'pop': ('pop.mp3', 0, .2),
      'ting': ('ting.mp3', 0, 1.3), 'riser': ('riser.mp3', 0, 4.38)}
cache = {}
def es(kind):
    if kind not in cache:
        f, ss, ln = ES[kind]; x = load(SD + f, ss, ln); fo = min(len(x), int(.12 * SR)); x[-fo:] *= np.linspace(1, 0, fo)[:, None]; cache[kind] = x
    return cache[kind]
sf = np.zeros((N, 2), np.float32); skipped = set()
for i, (t, kind, db) in enumerate(ev['sfx']):
    db = min(db + SFX_BOOST, -6.5)
    if kind in ES:
        x = es(kind).copy()
        if kind == 'riser': t = t - 2.95
    else:
        R = np.random.default_rng(9100 + i * 6007)
        try: x = L.S(kind, R)
        except Exception: skipped.add(kind); continue
        x = np.stack([x, x], 1) if x.ndim == 1 else x
    x = x.astype(np.float32); pk = np.max(np.abs(x)) + 1e-9; x = x / pk * (10 ** (db / 20))
    k = int(max(0, t) * SR)
    if t < 0: x = x[int(-t * SR):]; k = 0
    e = min(N, k + len(x))
    if k < N: sf[k:e] += x[:e - k]
print('skipped synth kinds', skipped)
m1 = load(SD + 'music1.mp3'); m2 = load(SD + 'music2.mp3')
XF = 6.0; sw = 150.0
mus = np.zeros((N, 2), np.float32)
a = m1[:int((sw + XF) * SR)].copy(); fo = int(XF * SR); a[-fo:] *= np.linspace(1, 0, fo)[:, None]; mus[:len(a)] += a[:N]
s0 = int(sw * SR); b = m2[:N - s0].copy(); fi = int(XF * SR); b[:fi] *= np.linspace(0, 1, fi)[:, None]; mus[s0:s0 + len(b)] += b
fade = np.ones(N); fade[:int(.5 * SR)] = np.linspace(0, 1, int(.5 * SR)); fade[-int(3.0 * SR):] = np.linspace(1, 0, int(3.0 * SR)) ** 1.5
mus *= fade[:, None]
blk = int(.01 * SR); nb = len(v) // blk; ve = np.sqrt((v[:nb * blk].reshape(nb, blk) ** 2).mean(1)); vdb = 20 * np.log10(ve + 1e-9)
sp = (vdb > -38).astype(np.float32); spm = np.convolve(sp, np.ones(12) / 12, 'same')
duck = 1 - DUCK * np.clip(np.convolve(spm, np.ones(25) / 25, 'same'), 0, 1)
duck_full = np.pad(np.repeat(duck, blk), (0, max(0, N - nb * blk)), 'edge')[:N]
speech_rms = float(np.sqrt((ve[sp > 0] ** 2).mean()))
mus *= duck_full[:, None]
mrms = np.sqrt((mus ** 2).mean()); mus *= speech_rms * 10 ** (-MUSIC_GAP / 20) / mrms
print('speech rms dBFS %.1f  music rms dBFS %.1f' % (20 * np.log10(speech_rms), 20 * np.log10(np.sqrt((mus ** 2).mean()))))
vox = np.stack([v, v], 1) * 10 ** (-1.0 / 20)
mix = vox + sf + mus
wf.write('build/mix_pre.wav', SR, (np.clip(mix / max(1, np.max(np.abs(mix)) / .98), -1, 1) * 32767).astype(np.int16))
wf.write('build/music_only.wav', SR, (np.clip(mus, -1, 1) * 32767).astype(np.int16))
r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', 'build/mix_pre.wav', '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float(re.findall(r'I:\s+(-?\d+\.\d)\s+LUFS', r)[-1]); g = -14.5 - I
print('pre LUFS', I, 'gain', g)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'build/mix_pre.wav', '-af', f'volume={g}dB,alimiter=limit=0.89:attack=3:release=60:level=disabled', '-ar', str(SR), '-c:a', 'pcm_s16le', 'hf/assets/audio/mix.wav'], check=True)
print('mix ok')
