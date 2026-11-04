#!/usr/bin/env /usr/bin/python3
"""Mix: voice + varied SFX + synthesized dark/energetic non-repeating music bed -> hf/assets/audio/mix.wav (stereo 48k)"""
import json, os, sys, numpy as np, scipy.io.wavfile as wf
from scipy import signal
sys.path.insert(0, 'scripts')
import sfxlib as L
from sfxlib import SR, T, nz, nrm, lp, hp, bp, tone, sweep
ev = json.load(open('build/sfx_events.json')); DUR = ev['dur']; N = int(DUR * SR); SHS = ev['sh']
sr, v = wf.read('build/voice.wav'); v = v.astype(np.float32) / 32768; v = v[:N]
assert sr == SR
def S2(name, R):
    if name == 'click':
        t = T(.16); d = hp(nz(R, .16), R.uniform(1800, 2600)) * np.exp(-t * 520) + .8 * np.sin(2 * np.pi * R.uniform(170, 230) * t) * np.exp(-t * 90)
        up = np.zeros_like(t); i = int(R.uniform(.06, .085) * SR); L_ = int(.03 * SR)
        up[i:i + L_] = hp(nz(R, .03), 2600) * np.exp(-np.arange(L_) / SR * 700) * .5
        return nrm(d + up)
    if name == 'whip':
        d = R.uniform(.26, .34); x = sweep(R, d, R.uniform(500, 900), R.uniform(5500, 7500), .35, .5, 3.5)
        pan = np.linspace(-.9, .9, len(x)) * R.choice([-1, 1]); return np.stack([x * (1 - pan) / 2 * 1.4, x * (1 + pan) / 2 * 1.4], 1)
    if name == 'shutter':
        a = hp(nz(R, .06), 1200) * np.exp(-T(.06) * 120); b = hp(nz(R, .05), 2500) * np.exp(-T(.05) * 150)
        x = np.zeros(int(.3 * SR)); x[:len(a)] += a; i = int(.06 * SR); x[i:i + len(b)] += b * .8
        x += .35 * tone(R.uniform(3200, 4200), .3, 25) ; return nrm(x)
    if name == 'burn':
        d = 1.0; t = T(d); env = np.minimum(t / .25, 1) * np.exp(-np.maximum(t - .25, 0) * 3.2)
        x = hp(nz(R, d), 2500) * env * .5 + lp(nz(R, d), 400) * env * .8
        cr = (R.random(len(t)) > .9985).astype(np.float32) * R.uniform(.4, 1, len(t)); cr = np.convolve(cr, np.exp(-np.arange(int(.004 * SR)) / (.001 * SR)), 'same')
        return nrm(x + cr * env * 2.2)
    return L.S(name, R)
def stereo(x): return np.stack([x, x], 1) if x.ndim == 1 else x
# ---- SFX bed
sf = np.zeros((N, 2), np.float32)
for i, (t, kind, db) in enumerate(ev['sfx']):
    R = np.random.default_rng(5000 + i * 6007)
    try: x = S2(kind, R)
    except ValueError: print('skip', kind); continue
    x = stereo(x).astype(np.float32); pk = np.max(np.abs(x)) + 1e-9
    x = x / pk * (10 ** (db / 20)); k = int(t * SR); e = min(N, k + len(x))
    if k < N: sf[k:e] += x[:e - k]
# ---- music: the track the student supplies (MUSIC env var), from its start
import subprocess
def load(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
trk = load(os.environ.get('MUSIC', 'input/music.mp3'))
mus = np.zeros((N, 2), np.float32); mus[:min(N, len(trk))] = trk[:N]
fade = np.ones(N); fade[:int(.4 * SR)] = np.linspace(0, 1, int(.4 * SR)); fade[-int(1.8 * SR):] = np.linspace(1, 0, int(1.8 * SR)) ** 1.5
mus *= fade[:, None]
# ---- levels: music ~22 dB under speech RMS, ducked under speech
blk = int(.01 * SR); nb = len(v) // blk; ve = np.sqrt((v[:nb * blk].reshape(nb, blk) ** 2).mean(1)); vdb = 20 * np.log10(ve + 1e-9)
sp = (vdb > -38).astype(np.float32); spm = np.convolve(sp, np.ones(12) / 12, 'same')
duck = 1 - .55 * np.clip(np.convolve(spm, np.ones(25) / 25, 'same'), 0, 1)
duck_full = np.pad(np.repeat(duck, blk), (0, max(0, N - nb * blk)), 'edge')[:N]
speech_rms = float(np.sqrt((ve[sp > 0] ** 2).mean()))
mus *= duck_full[:, None]
mrms = np.sqrt((mus ** 2).mean()); target = speech_rms * 10 ** (-22.5 / 20)
mus *= target / mrms
print('speech rms dBFS', 20 * np.log10(speech_rms), 'music rms dBFS', 20 * np.log10(np.sqrt((mus ** 2).mean())))
# ---- voice (centre) + sum + limiter
vox = np.pad(np.stack([v, v], 1), ((0, N - len(v)), (0, 0))) * 10 ** (-1.5 / 20)
mix = vox + sf + mus
pk = np.max(np.abs(mix)); print('peak before', pk)
mix = np.tanh(mix * 1.0 / 0.95) * 0.95 if pk > .95 else mix
mix = mix / max(1, np.max(np.abs(mix)) / .93)
wf.write('hf/assets/audio/mix.wav', SR, (np.clip(mix, -1, 1) * 32767).astype(np.int16))
wf.write('build/music_only.wav', SR, (np.clip(mus, -1, 1) * 32767).astype(np.int16))
print('mix ok', mix.shape)
