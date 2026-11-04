#!/usr/bin/env python3
"""Neon Caption Explainer, first build (worked example). Writes hf/index.html + build/sfx_events.json (16:9, 1920x1080, 30 fps)."""
import json, math, re, random
W, H = 1080, 1920
WW, WH = 1920, 1080
tm = json.load(open('build/timemap.json')); DUR = round(tm['dur'], 3); HD = tm['hook_dur']
WORDS = json.load(open('build/words_out.json'))      # [text, snapped_out, out, src]
HEAD = json.load(open('build/headtrack.json'))       # [t, top, cx]
LIME, WHITE, NAVY = '#EAFF00', '#FFFFFF', '#0f1224'
SH = None  # set after words are loaded (below)

SH = round((min(sn for t, sn, o, a in WORDS if re.sub(r'[^a-z]', '', t.lower()) == 'setiap') - .12) * 30) / 30
print('start offset SH =', SH)
# ---------------------------------------------------------------- helpers
def wt(word, after=0.0, nth=0):
    """snapped out-time of the first spoken word starting with `word` at/after `after`"""
    w = word.lower(); c = 0
    for t, sn, o, a in WORDS:
        tt = re.sub(r'[^a-z0-9%\-]', '', t.lower())
        if sn >= after - 1e-6 and tt.startswith(w):
            if c == nth: return sn
            c += 1
    raise KeyError(f'{word} after {after}')
JS = []            # gsap statements on the root timeline
SFX = []           # [t, kind, db]
def js(s): JS.append(s)
def sfx(t, kind, db=-20): SFX.append([round(t, 3), kind, db])
def counter(sel,t0,d,end,n=12):
    for i in range(1,n+1):
        u=i/n; v=round(end*(1-(1-u)**2)); js(f'tl.set("{sel}",{{textContent:"{v}"}},{t0+d*u:.3f});')
def esc(s): return s.replace('"', '\\"')
def tl_fromto(sel, f, to, t, d, ease='power3.out'):
    js(f'tl.fromTo("{sel}",{json.dumps(f)},{json.dumps({**to, "duration": d, "ease": ease})},{t:.3f});')
def tl_to(sel, to, t, d, ease='power2.out'):
    js(f'tl.to("{sel}",{json.dumps({**to, "duration": d, "ease": ease})},{t:.3f});')
def tl_set(sel, to, t):
    js(f'tl.set("{sel}",{json.dumps(to)},{t:.3f});')

# ---------------------------------------------------------------- camera plan (out seconds)
# (t, S, dur, ease, sx)   S = zoom, sx = screen x the head is pinned to
CAMK = [
 (0.0, 1.55, 0, 'set', 960), (0.1, 1.72, 4.1, 'sine', 960),
 (4.27, 1.22, .32, 'expo', 960), (6.35, 1.0, .9, 'sine', 960), (7.35, 1.36, .30, 'expo', 960),
 (9.7, 1.0, .9, 'sine', 960), (11.9, 1.3, .5, 'expo', 960), (12.9, 1.0, 1.0, 'sine', 960),
 (22.25, 1.42, .3, 'expo', 960), (26.0, 1.0, .8, 'sine', 960),
 (37.45, 1.58, .28, 'expo', 960), (39.1, 1.25, .9, 'sine', 960), (40.55, 1.52, .3, 'expo', 960),
 (43.3, 1.0, .9, 'sine', 960), (45.5, 1.4, .3, 'expo', 960), (47.9, 1.62, .25, 'expo', 960),
 (49.7, 1.2, .9, 'sine', 960), (51.1, 1.46, .3, 'expo', 960),
 (58.85, 1.0, .5, 'sine', 960),
 (76.6, 1.5, .3, 'expo', 960), (79.15, 1.66, .3, 'expo', 960), 
 (80.7, 1.5, .8, 'sine', 470),
 (88.05, 1.28, .5, 'expo', 960), (90.3, 1.0, .9, 'sine', 960), (98.0, 1.62, .3, 'expo', 960),
 (100.4, 1.3, .8, 'sine', 960), (102.3, 1.0, 1.0, 'sine', 960),
 (111.2, 1.36, .4, 'expo', 960), (112.8, 1.56, .3, 'expo', 960), (114.8, 1.2, .8, 'sine', 960), (116.2, 1.0, .8, 'sine', 960),
]
def ease_fn(name, u):
    u = max(0.0, min(1.0, u))
    if name == 'cubic': return 4 * u ** 3 if u < .5 else 1 - (-2 * u + 2) ** 3 / 2
    if name == 'sine': return -(math.cos(math.pi * u) - 1) / 2
    return 1.0
import numpy as np
from scipy.ndimage import gaussian_filter1d
ht = [(t, top + 80, cx) for t, top, cx in HEAD]
# every punch is now a smooth cubic in/out (>= .6 s); overlapping keys continue from the truncated value (no jumps)
CAMK = [(k, S_, (max(d, .6) if e in ('expo', 'cubic') else d), ('cubic' if e == 'expo' else e), x) for (k, S_, d, e, x) in CAMK]
KSEG = []   # (t_start, S0, sx0, S1, sx1, dur, ease)
cS, cX = CAMK[0][1], CAMK[0][4]
def seg_val(sg, t):
    k, S0, X0, S1, X1, d, e = sg
    if e == 'set' or d <= 0: return S1, X1
    f = ease_fn(e, (t - k) / d); return S0 + (S1 - S0) * f, X0 + (X1 - X0) * f
for i, (k, S1, d, e, X1) in enumerate(CAMK):
    if i == 0: S0, X0 = S1, X1
    else: S0, X0 = seg_val(KSEG[-1], k)
    KSEG.append((k, S0, X0, S1, X1, d, e))
def cam_state(t):
    sg = KSEG[0]
    for g in KSEG:
        if g[0] <= t: sg = g
        else: break
    return seg_val(sg, t)
NF = int(DUR * 30) + 1
tt_ = np.arange(NF) / 30
hx = np.interp(tt_, [h[0] for h in ht], [h[2] for h in ht]); hy = np.interp(tt_, [h[0] for h in ht], [h[1] for h in ht])
hx = gaussian_filter1d(hx, 26, mode='nearest'); hy = gaussian_filter1d(hy, 30, mode='nearest')
TX, TY, SS = [], [], []
for i in range(NF):
    S_, sx = cam_state(i / 30)
    Zp = 1 + (S_ - 1) * 0.42            # gentler punch-ins: the 1080p source is already enlarged 1.78x for 9:16
    Sc = (H / WH) * Zp; SS.append(Sc)
    f = min(1.0, max(0.0, (sx - 470) / 490.0)); pin_y = (0.27 + 0.13 * f) * H
    TX.append(W / 2 - Sc * hx[i]); TY.append(pin_y - Sc * hy[i])
TX = gaussian_filter1d(np.array(TX), 2.5, mode='nearest'); TY = gaussian_filter1d(np.array(TY), 2.5, mode='nearest')
CAM = []
for i in range(NF):
    S_ = SS[i]; tx = min(0, max(W - S_ * WW, TX[i])); ty = min(0, max(H - S_ * WH, TY[i]))
    CAM.append([round(float(tx), 2), round(float(ty), 2), round(float(S_), 4)])
d2 = np.abs(np.diff(np.array(CAM), 2, axis=0)); print('max 2nd diff tx,ty,S', d2.max(0).round(3))
# fast-forward fix: CAMK processed sequentially above (prev_S carries); verify range
print('cam S range', min(c[2] for c in CAM), max(c[2] for c in CAM))

# ---------------------------------------------------------------- captions
CAPS = []     # html
cap_n = [0]
FAM = ['pop', 'click', 'tink', 'blip', 'key', 'ping', 'switch', 'chirp']
random.seed(7); fam_i = [0]
last_kind = ['']
def next_fam():
    for _ in range(8):
        k = FAM[fam_i[0] % len(FAM)]; fam_i[0] += 1
        if k != last_kind[0]: last_kind[0] = k; return k
    return 'pop'
POS = {k: 'left:0;width:1080px;padding:0 44px;top:{y}px;text-align:center;' for k in ('bl', 'bc', 'br', 'tc', 'cl')}
CAPSPEC = []
t100 = wt('%', 8.0)
def cap(t0, t1, small, big, pos='bc', y=820, fs=104, times=None, hit=None, sm_t=None, sfx_on=True, sfx_db=-22, small_after=None):
    y2 = 230 if pos == 'tc' else (930 if (not big and pos == 'bl') else 1360)
    fs2 = fs if fs < 70 else min(112, round(fs * .8))
    CAPSPEC.append(dict(t0=t0, t1=t1, small=small, big=big, pos='bc', y=y2, fs=fs2, times=times, hit=hit, sm_t=sm_t, sfx_on=sfx_on, sfx_db=sfx_db))
def emit_caps():
    S_ = sorted(CAPSPEC, key=lambda c: c['t0'])
    for i, c in enumerate(S_):
        for d in S_[i + 1:]:
            if d['t0'] >= c['t1'] + .2: break
            if abs(d['y'] - c['y']) < 260 and d['pos'] == c['pos'] or (d['pos'] != c['pos'] and abs(d['y'] - c['y']) < 150):
                c['t1'] = max(c['t0'] + .3, d['t0'] - .1); c['fade'] = .08; break
    for c in S_: emit_cap(**c)
def emit_cap(t0, t1, small, big, pos='bc', y=820, fs=104, times=None, hit=None, sm_t=None, sfx_on=True, sfx_db=-22, fade=.16):
    n = cap_n[0]; cap_n[0] += 1; cid = f'c{n}'
    sm_html = f'<div class="sm" id="{cid}s"' + (' style="font-size:1em"' if not big else '') + f'>{small}</div>' if small else ''
    bw = ''.join(('<br>' if w == '\\n' else f'<span class="bw" id="{cid}w{j}" style="color:{LIME if c == "y" else WHITE}">{w}</span> ') for j, (w, c) in enumerate(big))
    CAPS.append(f'<div class="cap" id="{cid}" style="{POS[pos].format(y=y)}font-size:{fs}px">{sm_html}<div class="bg2">{bw}</div></div>')
    big_ = [b for b in big if b[0] != '\\n']; ts = times or [t0 + 0.12 * j for j in range(len(big_))]
    st = sm_t if sm_t is not None else (min(t0, ts[0] - 0.12) if small else None)
    js(f'tl.set("#{cid}",{{opacity:1}},{t0:.3f});')
    if small:
        tl_fromto(f'#{cid}s', {'opacity': 0, 'y': 16, 'filter': 'blur(8px)'}, {'opacity': 1, 'y': 0, 'filter': 'blur(0px)'}, st, .2)
    idx = [j for j, b in enumerate(big) if b[0] != '\\n']
    for jj, tj in enumerate(ts):
        j = idx[jj]
        tl_fromto(f'#{cid}w{j}', {'opacity': 0, 'scale': .72, 'y': 18, 'filter': 'blur(10px)'}, {'opacity': 1, 'scale': 1, 'y': 0, 'filter': 'blur(0px)'}, tj, .17, 'back.out(1.8)')
    tl_to(f'#{cid}', {'opacity': 0, 'filter': 'blur(6px)', 'y': -10}, t1, fade, 'power2.in')
    js(f'tl.set("#{cid}",{{opacity:0}},{t1 + fade + .01:.3f});')
    if sfx_on:
        sfx(ts[0] if ts else st, hit or next_fam(), sfx_db)
    return cid

# ---------------------------------------------------------------- scene builders
HTML_WORLD = []      # inside #cam, behind presenter
HTML_SCREEN = []     # overlays above #cam
VID = [0]
def vclip(src, start, dur, media_start=0, cls='', style='', mid=None):
    VID[0] += 1; vid = mid or f'v{VID[0]}'
    return vid, (f'<video id="{vid}" class="clip {cls}" src="{src}" muted playsinline data-start="{max(0, start - SH):.3f}" data-duration="{dur + VID[0] * .013:.3f}" '
                 f'data-media-start="{media_start:.3f}" data-track-index="{VID[0] + 4}" style="{style}"></video>')

def panel_world(pid, src, t0, t1, l, tp, w, h, ry, rx, rz, enter_from, mstart=0, hold_dy=-14, crop=None, z=2):
    vid, v = vclip(src, t0, t1 - t0 + .3, mstart, 'pv', 'object-position:%s;' % (crop or '50% 50%'), mid=pid + 'v')
    HTML_WORLD.append(f'<div id="{pid}" class="pn" style="left:{l}px;top:{tp}px;width:{w}px;height:{h}px;z-index:{z}">{v}</div>')
    ex, ey = enter_from
    tl_fromto(f'#{pid}', {'opacity': 0, 'x': ex, 'y': ey, 'rotationY': ry * 2.3, 'rotationX': rx * 2, 'rotationZ': rz * 2.2, 'scale': .86, 'transformPerspective': 1700, 'filter': 'blur(14px)'},
              {'opacity': 1, 'x': 0, 'y': 0, 'rotationY': ry, 'rotationX': rx, 'rotationZ': rz, 'scale': 1, 'filter': 'blur(0px)'}, t0, .62, 'expo.out')
    tl_to(f'#{pid}', {'y': hold_dy, 'rotationY': ry * .55, 'rotationZ': rz * .4, 'scale': 1.03}, t0 + .62, max(.4, t1 - t0 - .62 - .3), 'sine.inOut')
    tl_to(f'#{pid}', {'opacity': 0, 'x': -ex * .6, 'y': -ey * .6 - 30, 'rotationY': ry * 1.8, 'scale': .9, 'filter': 'blur(10px)'}, t1 - .3, .3, 'power2.in')
    js(f'tl.set("#{pid}",{{opacity:0}},{t1 + .02:.3f});')

PMAT_WIN = []   # windows where cut-out is on

# ---- SHOWREEL strips (tidy row of equal panels, one shared tilt, slow marquee) behind me
def reel(rid, t0, t1, items, y=190, w=360, h=640, gap=28, rot=-15, x0=380, x1=-340, ease='sine.inOut'):
    n = len(items); tot = n * w + (n - 1) * gap; ps = []
    for i, (src, ms, crop) in enumerate(items):
        vid, v = vclip(src, t0, t1 - t0 + .3, ms, 'pv', 'object-position:%s;' % crop, mid=f'{rid}v{i}')
        ps.append(f'<div class="rp" style="left:{i * (w + gap)}px;top:0;width:{w}px;height:{h}px">{v}</div>')
    left = (W - tot) / 2
    HTML_WORLD.append(f'<div id="{rid}" class="reel" style="left:{left}px;top:{y}px;width:{tot}px;height:{h}px;z-index:2">{"".join(ps)}</div>')
    tl_fromto(f'#{rid}', {'opacity': 0, 'x': x0 + 220, 'rotationY': rot, 'transformPerspective': 1900, 'filter': 'blur(12px)'}, {'opacity': 1, 'x': x0, 'rotationY': rot, 'filter': 'blur(0px)'}, t0, .5, 'expo.out')
    tl_fromto(f'#{rid}', {'x': x0}, {'x': x1, 'immediateRender': False}, t0 + .5, max(.5, t1 - t0 - .8), ease)
    tl_to(f'#{rid}', {'opacity': 0, 'x': x1 - 200, 'filter': 'blur(10px)'}, t1 - .3, .3, 'power2.in')
    tl_set(f'#{rid}', {'opacity': 0}, t1 + .02)
# ---- GROUP A: showreel behind me (13.0 -> 22.4)
A0, A1 = wt('saya', 12.5) - 0.35, 22.4
PMAT_WIN.append((A0 - .15, A1 + .1))
reel('reelA', A0, A1, [('assets/panels/n2.mp4', 0, '50% 50%'), ('assets/panels/n5.mp4', 0, '50% 50%'), ('assets/panels/n6.mp4', 0, '50% 50%'),
                       ('assets/panels/n4.mp4', 0, '50% 50%'), ('assets/panels/n7.mp4', 0, '50% 50%'), ('assets/panels/n3.mp4', 0, '50% 50%')], y=430, w=400, h=711, gap=30, x0=785, x1=85)
sfx(A0, 'slide', -22); sfx(A0 + .5, 'swish_up', -27)
# ---- GROUP B: faster showreel slide behind me (58.9 -> 61.4)
B0, B1 = 58.85, 61.45
PMAT_WIN.append((B0 - .1, B1 + .1))
reel('reelB', B0, B1, [('assets/panels/n1.mp4', 2, '50% 50%'), ('assets/panels/n3.mp4', 4, '50% 50%'), ('assets/panels/n6.mp4', 5, '50% 50%'),
                       ('assets/panels/n2.mp4', 4, '50% 50%'), ('assets/panels/n4.mp4', 5, '50% 50%'), ('assets/panels/n7.mp4', 4, '50% 50%')], rot=-15, y=430, w=400, h=711, gap=30, x0=785, x1=-115, ease='power1.inOut')
sfx(B0, 'slide', -21); sfx(B0 + 1.1, 'swish_dn', -26)

# ---- GROUP D: floating weekly card behind me (90.9 -> 97.9)
D0, D1 = wt('maksudnya', 89.5) - .1, wt('balik', 96.3) + .9
PMAT_WIN.append((D0 - .1, D1 + .1))
bars = ''.join(f'<div class="wb" id="dw{i}" style="left:{28 + i * 56}px"><i id="dwf{i}"></i><b>{d}</b></div>' for i, d in enumerate(['ISN', 'SEL', 'RAB', 'KHA', 'JUM', 'SAB', 'AHD']))
HTML_WORLD.append(f'<div id="dcard" class="pn card3d" style="left:610px;top:300px;width:440px;height:380px;z-index:2;opacity:0"><div class="ct">WEEKLY</div>{bars}<div class="cn" id="dnum">3 HARI</div></div>')
tl_fromto('#dcard', {'opacity': 0, 'x': 420, 'rotationY': -60, 'transformPerspective': 1700, 'filter': 'blur(12px)'}, {'opacity': 1, 'x': 0, 'rotationY': -22, 'rotationX': 5, 'filter': 'blur(0px)'}, D0, .6, 'expo.out')
tl_to('#dcard', {'y': -16, 'rotationY': -12}, D0 + .6, D1 - D0 - .9, 'sine.inOut')
tl_to('#dcard', {'opacity': 0, 'x': 260, 'filter': 'blur(10px)'}, D1 - .3, .3, 'power2.in'); tl_set('#dcard', {'opacity': 0}, D1 + .02)
for i in range(7): tl_fromto(f'#dwf{i}', {'scaleY': 0}, {'scaleY': 1 if i < 4 else .12}, D0 + .5 + i * .05, .3, 'power3.out')
t_tiga = wt('tiga', D0)
tl_fromto('#dnum', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, t_tiga, .25, 'back.out(2)')
for i in range(4, 7): tl_to(f'#dwf{i}', {'scaleY': 1}, wt('tambah', D0) + (i - 4) * .12, .3, 'power3.out')
sfx(D0, 'portal', -23); sfx(t_tiga, 'stamp', -22); sfx(wt('tambah', D0), 'check', -22)

# ---- GROUP C: prompt cards behind me (102.4 -> 111.4)
C0, C1 = wt('rasa', 102.5) - .45, wt('semua', 110.2) + .6
def typed(sel_prefix, text, t0, per=.05, sfxdb=-27, every=3):
    out = ''
    for i, ch in enumerate(text):
        out += f'<span id="{sel_prefix}{i}" class="ch">{ch if ch != " " else "&nbsp;"}</span>'
        tl_fromto(f'#{sel_prefix}{i}', {'opacity': 0}, {'opacity': 1}, t0 + i * per, .02, 'none')
        if i % every == 0: sfx(t0 + i * per, 'key', sfxdb)
    return out
tv = wt('vault', C0)
tt = wt('template', tv)
PMAT_WIN.append((tv - .45, C1 + .1))
HTML_WORLD.append(f'<div id="cv" class="pn card3d" style="left:30px;top:330px;width:420px;height:340px;z-index:2;opacity:0"><div class="ci">⛁</div><div class="ct">PROMPT VAULT</div><div class="cs">{typed("cvt", "senarai prompt siap pakai", tv - .1, .045)}</div></div>')
HTML_WORLD.append(f'<div id="cp" class="pn card3d" style="left:630px;top:640px;width:420px;height:340px;z-index:2;opacity:0"><div class="ci">❏</div><div class="ct">PROMPT TEMPLATE</div><div class="cs">{typed("cpt", "ikut format, terus jalan", tt - .1, .045)}</div></div>')
tl_fromto('#cv', {'opacity': 0, 'x': -460, 'rotationY': 62, 'transformPerspective': 1700, 'filter': 'blur(12px)'}, {'opacity': 1, 'x': 0, 'rotationY': 24, 'rotationX': 5, 'filter': 'blur(0px)'}, tv - .35, .6, 'expo.out')
tl_fromto('#cp', {'opacity': 0, 'x': 460, 'rotationY': -62, 'transformPerspective': 1700, 'filter': 'blur(12px)'}, {'opacity': 1, 'x': 0, 'rotationY': -24, 'rotationX': 5, 'filter': 'blur(0px)'}, tt - .35, .6, 'expo.out')
tl_to('#cv', {'y': -14, 'rotationY': 13}, tv + .3, C1 - tv - .6, 'sine.inOut'); tl_to('#cp', {'y': -14, 'rotationY': -13}, tt + .3, C1 - tt - .6, 'sine.inOut')
for s in ('#cv', '#cp'): tl_to(s, {'opacity': 0, 'filter': 'blur(10px)'}, C1 - .25, .3, 'power2.in'); tl_set(s, {'opacity': 0}, C1 + .06)
sfx(tv - .35, 'slide', -22); sfx(tt - .35, 'swish_up', -23); sfx(tv + .05, 'click', -21); sfx(tt + .05, 'click', -22)

# ---- full-screen overlays ----------------------------------------------------------------
def overlay(oid, t0, t1, inner, bg=NAVY, fin='blur', fout='blur', z=30):
    HTML_SCREEN.append(f'<div id="{oid}" class="ov" style="background:{bg};z-index:{z}">{inner}</div>')
    tl_fromto(f'#{oid}', {'opacity': 0, 'scale': 1.06, 'filter': 'blur(14px)'}, {'opacity': 1, 'scale': 1, 'filter': 'blur(0px)'}, t0, .3, 'expo.out')
    tl_to(f'#{oid}', {'opacity': 0, 'scale': .96, 'filter': 'blur(12px)'}, t1 - .25, .25, 'power2.in')
    tl_set(f'#{oid}', {'opacity': 0}, t1 + .01)

# STAGE: same video, 3 sizes (28.2 -> 37.3)
S0 = wt('contohnya', 27.5) - .15; S1 = wt('siap', 36.0) + .2
BASEY = 830
def stcol(sid, cx, w, h, ry, label, sub, bgpos, bgsize, t_in, by=830):
    L, Tp = cx - w / 2, by - h
    vid, v = vclip('assets/panels/stage.mp4', S0, S1 - S0 + .3, 0, 'sv', 'width:100%;height:100%;left:0;top:0;object-fit:cover;object-position:50% 40%;', mid=sid + 'v')
    HTML_SCREEN.append(f'<div id="{sid}" class="stp" style="left:{L}px;top:{Tp}px;width:{w}px;height:{h}px;z-index:34;opacity:0">{v}</div>')
    HTML_SCREEN.append(f'<div id="{sid}l" class="stl" style="left:{cx - 140}px;top:{by + 26}px;z-index:34;opacity:0"><span>{label}</span><em>{sub}</em></div>')
    tl_fromto(f'#{sid}', {'opacity': 0, 'y': 90, 'rotationY': ry * 2.2, 'transformPerspective': 1800, 'filter': 'blur(12px)', 'scale': .9}, {'opacity': 1, 'y': 0, 'rotationY': ry, 'filter': 'blur(0px)', 'scale': 1}, t_in, .5, 'expo.out')
    tl_fromto(f'#{sid}l', {'opacity': 0, 'y': 22, 'scale': .7}, {'opacity': 1, 'y': 0, 'scale': 1}, t_in + .25, .28, 'back.out(2.2)')
    tl_to(f'#{sid}', {'y': -10}, t_in + .5, S1 - t_in - 1.0, 'sine.inOut')
    for s in (f'#{sid}', f'#{sid}l'):
        tl_to(s, {'opacity': 0, 'filter': 'blur(10px)'}, S1 - .25, .25, 'power2.in'); tl_set(s, {'opacity': 0}, S1 + .01)
    sfx(t_in, 'click', -21); sfx(t_in + .22, 'tink', -23)
stage_bg = f'<div class="sbh"><div class="sm" id="sth1">satu video, satu minit setengah ke bawah</div><div class="bg2" id="sth2"><span style="color:{LIME}">MACAM-MACAM</span> <span style="color:#fff">SIZE</span></div></div>'
overlay('stage', S0, S1, stage_bg, bg='radial-gradient(1300px 760px at 50% 52%,#1d2350,#0d1020)')
tl_fromto('#sth1', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, S0 + .12, .25)
tl_fromto('#sth2', {'opacity': 0, 'scale': .82, 'filter': 'blur(10px)'}, {'opacity': 1, 'scale': 1, 'filter': 'blur(0px)'}, S0 + .2, .3, 'back.out(1.8)')
t169 = wt('siap', S0) - .12; t916 = wt('menegak', S0) - .25; t11 = wt('petak', S0) - .2
stcol('sz2', 540, 800, 450, -5, '16:9', 'YOUTUBE', (0, 0), (600, 338), t169, by=790)
stcol('sz1', 830.5, 281, 500, 8, '9:16', 'REELS · TIKTOK', (-387, 0), (1067, 600), t916, by=1440)
stcol('sz3', 360, 500, 500, -6, '1:1', 'FEED', (-230, 0), (960, 540), t11, by=1440)
sfx(S0, 'burn', -22)
# 'LAJU' burst on "terus laju"
tl_laju = wt('laju', S0)
HTML_SCREEN.append(f'<div id="laju" class="lj" style="z-index:36;opacity:0">SEMUA SERENTAK</div>')
tl_fromto('#laju', {'opacity': 0, 'scale': .7, 'y': 20}, {'opacity': 1, 'scale': 1, 'y': 0}, tl_laju - .05, .22, 'back.out(2)'); tl_to('#laju', {'opacity': 0}, S1 - .3, .2, 'power2.in'); tl_set('#laju', {'opacity': 0}, S1 + .01)
sfx(tl_laju, 'zoom_in', -22)

# SESSION ring (infographic) 53.0 -> 58.9
R0, R1 = wt('ibarat', 52.0) - .15, wt('so,', 57.5) if False else 58.85
ring = (f'<div class="itl"><span style="color:{LIME}">SESSION</span> <span>= 5 JAM</span></div>'
        '<svg class="ring" width="540" height="540" viewBox="0 0 620 620"><circle cx="310" cy="310" r="250" fill="none" stroke="#2a3060" stroke-width="40"/>'
        f'<circle id="rg" cx="310" cy="310" r="250" fill="none" stroke="{LIME}" stroke-width="40" stroke-linecap="round" stroke-dasharray="1571" stroke-dashoffset="0" transform="rotate(-90 310 310)"/>'
        f'<text id="rgt" x="310" y="345" text-anchor="middle" fill="#fff" font-family="Poppins" font-weight="800" font-size="118">5 JAM</text></svg>'
        '<div class="rgl" id="rgl">tidur dulu → bagi balik</div>')
overlay('ringov', R0, R1, ring)
t_staff = wt('ibarat', R0); t_tidur = wt('tidur', R0); t_lima = wt('lima', R0); t_balik = wt('balik', t_lima)
tl_fromto('#rg', {'strokeDashoffset': 0}, {'strokeDashoffset': 1571}, t_tidur, t_lima - t_tidur + .5, 'power1.inOut')
tl_fromto('#rg', {'strokeDashoffset': 1571}, {'strokeDashoffset': 0, 'immediateRender': False}, t_balik - .55, .9, 'power2.inOut')
tl_fromto('#rgl', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, t_tidur, .3)
sfx(R0, 'swish_up', -22); sfx(t_tidur, 'zoom_out', -23); sfx(t_balik - .5, 'riser', -26); sfx(t_balik + .35, 'shing', -22)

# WEEKLY infographic 61.4 -> 75.6
K0, K1 = B1 - .05, 75.65
wk = ''.join(f'<div class="wcol" style="left:{60 + i * 137}px"><div class="wbar" id="kw{i}"><i id="kwf{i}"></i></div><b>{d}</b></div>' for i, d in enumerate(['ISNIN', 'SELASA', 'RABU', 'KHAMIS', 'JUMAAT', 'SABTU', 'AHAD']))
week = (f'<div class="itl" style="top:250px"><span style="color:{LIME}">WEEKLY</span> <span>= 7 HARI</span></div>{wk}'
        '<div class="lock" id="lock">🔒 TUNGGU</div>')
overlay('weekov', K0, K1, week)
days = [wt('isnin', K0), wt('isnin', K0) + .3, wt('hari', wt('isnin', K0)) + .0, wt('kamis', K0)]
for i, tday in enumerate([wt('isnin', K0), wt('isnin', K0) + .45, wt('sampai', wt('isnin', K0)) + .4, wt('kamis', K0)]):
    tl_fromto(f'#kwf{i}', {'scaleY': 0}, {'scaleY': 1}, tday - .05, .38, 'power3.out'); sfx(tday - .05, ['click', 'pop', 'tink', 'stamp'][i], -21)
tl_fromto('#kwf4', {'scaleY': 0}, {'scaleY': .1}, K0 + .3, .3); tl_fromto('#kwf5', {'scaleY': 0}, {'scaleY': .1}, K0 + .38, .3); tl_fromto('#kwf6', {'scaleY': 0}, {'scaleY': .1}, K0 + .46, .3)
t_gila = wt('guna', K0); t_hab = wt('habis', t_gila)
tl_to('#kw0,#kw1,#kw2,#kw3', {'x': 0}, t_gila, .01)
js(f'tl.to(["#kwf0","#kwf1","#kwf2","#kwf3"],{{backgroundColor:"#ff3b3b",duration:.4,ease:"power2.out"}},{t_hab - .05:.3f});')
t_tgg = wt('tunggu', t_hab)
tl_fromto('#lock', {'opacity': 0, 'scale': .6, 'y': 20}, {'opacity': 1, 'scale': 1, 'y': 0}, t_tgg - .1, .3, 'back.out(2)'); sfx(t_tgg - .1, 'stamp', -21)
t_naik = wt('naik', t_tgg)
tl_to('#lock', {'opacity': 0}, t_naik - .5, .2)
for i in range(7): tl_to(f'#kwf{i}', {'scaleY': 1, 'backgroundColor': LIME}, t_naik - .3 + i * .06, .35, 'power3.out')
sfx(t_naik - .3, 'riser', -26); sfx(t_naik + .1, 'shing', -22); sfx(K0, 'burn', -23); sfx(t_hab - .05, 'boom', -21)

# RECAP "2 JENIS USAGE" 75.65 -> 77.6
Q0, Q1 = K1 - .05, 77.55
recap = (f'<div class="rtl"><span style="color:{LIME}">2 JENIS</span> USAGE</div><div class="rc1"><b style="color:{LIME}">SESSION</b><span>5 JAM</span></div><div class="rc2"><b style="color:{LIME}">WEEKLY</b><span>7 HARI</span></div>')
overlay('recapov', Q0, Q1, recap)
tl_fromto('#recapov .rtl', {'scale': .8, 'opacity': 0}, {'scale': 1, 'opacity': 1}, Q0 + .1, .3, 'back.out(1.8)')
tl_fromto('#recapov .rc1', {'x': -80, 'opacity': 0}, {'x': 0, 'opacity': 1}, Q0 + .25, .3); tl_fromto('#recapov .rc2', {'x': 80, 'opacity': 0}, {'x': 0, 'opacity': 1}, Q0 + .4, .3)
sfx(Q0, 'zoom_in', -22); sfx(Q0 + .3, 'click', -22); sfx(Q0 + .45, 'tink', -23)

# SPLIT (81.2 -> 88.0): right card over camera pinned left
P0, P1 = wt('rm90', 80.5) - .2, wt('panjang', 85.5) + .75
split = (f'<div class="spc"><div class="spl" style="color:{LIME}" id="spa">SEBULAN</div><div class="spn" id="spb">RM<span id="rm">0</span></div>'
         f'<div class="spar" id="spc2">↓</div><div class="spn" id="spd"><span id="vn">0</span>–<span id="vm">0</span></div><div class="spl" style="color:{LIME}" id="spe">VIDEO</div></div>')
HTML_SCREEN.append(f'<div id="splitov" style="position:absolute;left:0;top:1010px;width:1080px;height:910px;z-index:30;opacity:0;background:#0b0e1c">{split}</div>')
tl_fromto('#splitov', {'opacity': 0, 'y': 220, 'filter': 'blur(10px)'}, {'opacity': 1, 'y': 0, 'filter': 'blur(0px)'}, P0, .35, 'expo.out')
tl_to('#splitov', {'opacity': 0, 'y': 160, 'filter': 'blur(10px)'}, P1 - .25, .25, 'power2.in'); tl_set('#splitov', {'opacity': 0}, P1 + .01)
t_rm = wt('rm90', 80.5); t_30 = wt('30', t_rm); t_50 = wt('50', t_30); t_vid = wt('video', t_50)
for sel, tt_, fr in (('#spa', P0 + .15, {'y': 16}), ('#spb', t_rm - .05, {'scale': .7}), ('#spc2', t_30 - .3, {'y': -20}), ('#spd', t_30 - .05, {'scale': .7}), ('#spe', t_vid - .08, {'scale': .7})):
    tl_fromto(sel, {'opacity': 0, **fr}, {'opacity': 1, 'y': 0, 'scale': 1}, tt_, .26, 'back.out(1.8)')
counter('#rm',t_rm,.5,90); counter('#vn',t_30,.4,30); counter('#vm',t_50-.1,.4,50)
sfx(P0, 'slide', -22); sfx(t_rm, 'ratchet', -23); sfx(t_30, 'ratchet', -24); sfx(t_vid, 'stamp', -21)

GLOW0 = 'drop-shadow(0px 0px 0px rgba(255,255,255,0)) drop-shadow(0px 0px 0px rgba(255,255,255,0)) drop-shadow(0px 0px 0px rgba(255,255,255,0))'
GLOW1 = 'drop-shadow(0px 0px 3px rgba(255,255,255,1)) drop-shadow(0px 0px 14px rgba(255,255,255,.95)) drop-shadow(0px 0px 38px rgba(255,255,255,.7))'
GLOW_JS = f'gsap.set("#pmat",{{filter:"{GLOW0}"}});'
for (ga, gb) in ((A0 - .15, A1 + .1), (B0 - .1, B1 + .1)):
    GLOW_JS += (f'tl.fromTo("#pmat",{{filter:"{GLOW0}"}},{{filter:"{GLOW1}",duration:.45,ease:"power2.out",immediateRender:false}},{ga:.3f});'
                f'tl.to("#pmat",{{filter:"{GLOW0}",duration:.3,ease:"power2.in"}},{gb - .3:.3f});')
GLOW_JS += 'gsap.set("#base",{filter:"grayscale(0)"});'
for (ga, gb) in ((A0 - .15, A1 + .1), (B0 - .1, B1 + .1)):
    GLOW_JS += (f'tl.fromTo("#base",{{filter:"grayscale(0)"}},{{filter:"grayscale(1)",duration:.45,ease:"power2.out",immediateRender:false}},{ga:.3f});'
                f'tl.to("#base",{{filter:"grayscale(0)",duration:.35,ease:"power2.in"}},{gb - .3:.3f});')
PMAT_JS = GLOW_JS + ''.join(f'tl.set("#pmat",{{opacity:1}},{a:.3f});tl.set("#pmat",{{opacity:0}},{b:.3f});' for a, b in PMAT_WIN)

# ---------------------------------------------------------------- HOOK + main captions
t_rm_h = 0.05
# hook (0 -> 4.27): small + big
hk_a = 0.05; hk_b = HD - 0.12
cap(hk_a, HD - .02, 'RM90 tu, memang almost', [('30', 'y'), ('–', 'w'), ('50', 'y'), ('VIDEO', 'w')], 'bl', 650, 150, [2.45, 2.75, 2.95, 3.5], hit='stamp', sm_t=0.12)
# whip into main
js(f'tl.fromTo("#cam",{{filter:"blur(0px)"}},{{filter:"blur(22px)",duration:.14,ease:"power2.in"}},{HD - .16:.3f});tl.to("#cam",{{filter:"blur(0px)",duration:.3,ease:"power2.out"}},{HD:.3f});')
sfx(HD - .16, 'whip', -19); sfx(HD, 'shutter', -21)

M = HD  # main start
cap(wt('checkgpt', 0) - .1, 6.4, 'ChatGPT pun', [('SAMA', 'y'), ('JUGA', 'w')], 'bc', 800, 110, [wt('sama', 0), wt('juga', 0)])
cap(wt('konsep', 0) - .05, 6.4, 'konsep dia', [('SAMA', 'y')], 'bc', 800, 120, [wt('sama', wt('konsep', 0))])
cap(wt('kedua', 0) - .1, t100 - .5, 'yang kedua adalah', [('WEEKLY', 'y')], 'bc', 790, 140, [wt('weekly', 0)], hit='stamp')
# 100% counter
HTML_SCREEN.append(f'<div id="n100" class="num" style="left:0;width:1080px;top:1090px;opacity:0"><small id="n100s">juga</small><span id="n100v">0</span>%</div>')
tl_fromto('#n100', {'opacity': 0, 'scale': .8}, {'opacity': 1, 'scale': 1}, t100 - .4, .25, 'back.out(1.8)'); tl_to('#n100', {'opacity': 0, 'filter': 'blur(6px)'}, wt('setiap', 9) - .1, .16, 'power2.in'); tl_set('#n100', {'opacity': 0}, wt('setiap', 9) + .1)
counter('#n100v',t100-.35,.55,100)
sfx(t100 - .35, 'ratchet', -23); sfx(t100 + .22, 'stamp', -21)

# 10-22: floating panels beat
cap(wt('setiap', 9) - .05, wt('contoh', 11) + .2, 'setiap hari bila kita', [('BUAT', 'w'), ('VIDEO', 'y')], 'bc', 820, 112, [wt('buat', 10), wt('video', 11)])
cap(wt('saya', 12.5) + .0, wt('agak', 15.5) - .05, 'video aku dekat social media', [], 'bc', 868, 52, None, hit='click', sm_t=wt('saya', 12.5) + .0)
cap(wt('agak', 15.5), wt('soundtrack', 17.5) - .05, '', [('HEAVY', 'y'), ('EDITING', 'y'), ('\\n', 'w'), ('BANYAK', 'w'), ('B-ROLL', 'y')], 'bc', 770, 104, [wt('heavy', 15.5), wt('editing', 16), wt('banyak', 16.5), wt('-roll', 16.5)], hit='stamp')
cap(wt('soundtrack', 17.5) - .05, wt('sound', 20.9) - .1, 'soundtrack pun memang ada', [('UBAH', 'y')], 'bc', 810, 128, [wt('ubah', 19.5)], hit='tink')
cap(wt('sound', 20.9) - .05, 22.25, 'sound effect pun', [('UBAH', 'y')], 'bc', 810, 128, [wt('ubah', 21.2)], hit='pop')
# 22.3: 1.5 minit
cap(wt('biasanya', 21.5) - .05, wt('boleh', 25.5) - .05, 'satu video', [('1½', 'y'), ('MINIT', 'w'), ('KE BAWAH', 'y')], 'bc', 790, 120, [wt('satu', wt('video', 22)) , wt('minit', 23), wt('ke', 25.2)], hit='click')
cap(wt('boleh', 25.5) - .05, S0 + .1, 'buat', [('MACAM-MACAM', 'y'), ('SIZE', 'w')], 'bc', 800, 116, [wt('macam', 26.5), wt('size', 26.9)], hit='pop')
# 37.4 question + 15%
tb = wt('berapa', 36.8)
cap(tb - .05, wt('biasanya', tb) - .12, '', [('BERAPA', 'w'), ('MAKAN', 'w'), ('MASA?', 'y')], 'bc', 800, 130, [tb, wt('makan', tb), wt('masa', tb)], hit='chirp')
t15 = wt('15', 38.8)
HTML_SCREEN.append(f'<div id="n15" class="num" style="left:0;width:1080px;top:1040px;opacity:0"><small>MASA EDIT</small><span id="n15v">0</span>%</div>')
tl_fromto('#n15', {'opacity': 0, 'scale': .8}, {'opacity': 1, 'scale': 1}, t15 - .35, .25, 'back.out(1.8)'); tl_to('#n15', {'opacity': 0, 'filter': 'blur(6px)'}, wt('ke', t15) + .0, .16, 'power2.in'); tl_set('#n15', {'opacity': 0}, wt('ke', t15) + .3)
counter('#n15v',t15-.3,.5,15)
sfx(t15 - .3, 'ratchet', -23); sfx(t15 + .3, 'stamp', -21)
cap(wt('ke', t15) - .02, wt('apa', 42.5) - .1, 'lebih kurang', [('15%', 'y'), ('KE BAWAH', 'w')], 'bc', 810, 120, [wt('ke', t15) + .05, wt('bawah', t15)], hit='click')
# credit -> usage -> habis
tcr = wt('credit', 44)
cap(wt('apa', 42.5) - .05, wt('credit', 44) - .05, 'apa jadi kalau kita punya', [('CREDIT', 'w')], 'bc', 810, 108, [tcr], hit='pop')
cid_u = cap(wt('bukan', 45) - .1, wt('dia', 48.6) - .05, 'bukan credit,', [('USAGE', 'y'), ('HABIS', 'w')], 'bc', 810, 122, [wt('usage', 46), wt('habis', 47)], hit='tink')
cap(wt('dia', 48.6) - .02, R0 + .1, 'bila habis, kita panggil', [('OPEN', 'y'), ('WINDOW', 'y'), ('TIME', 'w')], 'bc', 790, 118, [wt('open', 49), wt('window', 50), wt('time', 51)], hit='stamp')

# ring-overlay captions (screen space above overlay)
cap(wt('dia', R0 + .4) , wt('setiap', 55) - .1, '', [('TIDUR', 'w'), ('LIMA', 'y'), ('JAM', 'y')], 'bc', 850, 96, [wt('tidur', R0), wt('lima', R0), wt('jam', R0)], hit='pop')
cap(wt('setiap', 55) - .02, R1 - .1, 'setiap lima jam, bagi balik', [('100%', 'y')], 'bc', 860, 130, [wt('100', R0)], hit='shing')
# 58.9 weekly sama
cap(wt('untuk', 57.5) - .1, B1 + .0, 'untuk', [('WEEKLY', 'y'), ('PUN', 'w'), ('SAMA', 'w')], 'bc', 800, 126, [wt('weekly', 58.5), wt('pun', 59), wt('sama', 59)], hit='click')
# weekly infographic captions
cap(wt('boleh', 60.9) - .02, wt('memang', 65.5) - .1, 'dalam tempoh satu minggu', [('ISNIN', 'y'), ('→', 'w'), ('KHAMIS', 'y')], 'bc', 850, 96, [wt('isnin', 63), wt('sampai', 63), wt('kamis', 64)], hit='tink')
cap(wt('memang', 65.5) - .02, wt('weekly', 68.5) - .05, '', [('GUNA', 'w'), ('GILA-GILA', 'y')], 'bc', 850, 112, [wt('guna', 66), wt('gila', 66.5)], hit='stamp')
cap(wt('weekly', 68.5) - .02, K1 - .8, 'sampai weekly pun', [('HABIS', 'y')], 'bc', 850, 124, [wt('habis', 70)], hit='boom', sfx_db=-20)
cap(t_tgg - .2, wt('supaya', t_tgg) - .05, 'kita kena', [('TUNGGU', 'y'), ('MINGGU', 'w'), ('LAGI', 'w')], 'bc', 850, 100, [wt('tunggu', t_tgg), wt('minggu', t_tgg), wt('lagi', t_tgg)], hit='click')
cap(wt('supaya', t_tgg) - .02, K1 - .05, 'supaya weekly ni', [('NAIK', 'y'), ('BALIK', 'w')], 'bc', 850, 118, [wt('naik', t_tgg), wt('balik', wt('naik', t_tgg))], hit='ping')
# 77.6+ heavy
cap(wt('tapi', 76.0) + .35, wt('rm90', 80.5) - .2, 'as of saya rasa saya agak', [('HEAVY', 'y')], 'bl', 800, 150, [wt('heavy', 78)], hit='stamp')
# split: small bottom-left caption
cap(wt('termasuklah', 84.5) - .02, P1, 'termasuk tutorial panjang-panjang', [], 'bl', 880, 54, None, hit='click', sm_t=wt('termasuklah', 84.5))
# 88.2 sebulan
cap(wt('tak', 87.5) - .2, wt('saya', 88.7) - .05, 'eh tak tak,', [('SEBULAN', 'y')], 'bc', 800, 140, [wt('sebulan', 87.8)], hit='stamp')
cap(wt('saya', 88.7) - .02, wt('maksudnya', 89.5) - .08, 'saya sempat buat benda tu', [], 'bc', 860, 56, None, hit='tink', sm_t=wt('saya', 88.7))
# 90.6 weekly back-card captions
cap(wt('seminggu', 91) - .05, wt('saya', 93) - .02, 'seminggu dah', [('HABIS', 'y')], 'bl', 800, 130, [wt('habis', 92.5)], hit='click')
cap(wt('saya', 93) - .02, wt('limit', 94.8) - .02, 'saya kena tunggu dalam', [('3 HARI', 'y')], 'bl', 800, 140, [t_tiga if False else t_tiga], hit='stamp')
cap(wt('limit', 94.8) - .02, wt('hasilnya', 96) - .02, 'limit weekly ni tambah', [('BALIK', 'y')], 'bl', 800, 130, [wt('balik', 96.6)], hit='ping')
# 98+
cap(wt('hasilnya', 96) - .02, wt('heavy', 99.8) - .06, 'hasilnya', [('30', 'y'), ('–', 'w'), ('50', 'y'), ('VIDEO', 'w')], 'bc', 790, 130, [wt('30', 98.5), wt('30', 98.5) + .12, wt('50', 98.8), wt('50', 98.8) + .3], hit='stamp')
cap(wt('heavy', 99.8) - .02, wt('termasuk', 100.8) + .2, '', [('HEAVY', 'y'), ('EDITING', 'w')], 'bc', 800, 140, [wt('heavy', 99.8), wt('editing', 99.8)], hit='pop')
cap(wt('termasuk', 100.8) + .2, tv - .5, 'termasuk', [('TESTING', 'y')], 'bc', 840, 112, [wt('testing', 100.8)], hit='click')
# prompt vault / template captions
cap(tv - .45, tt - .38, 'kalau kita dah follow', [('PROMPT VAULT', 'y')], 'bc', 840, 96, [tv - .05], hit='stamp')
cap(tt - .38, wt('dia', tt) + .0, 'ataupun', [('PROMPT TEMPLATE', 'y')], 'bc', 840, 96, [tt - .05], hit='stamp')
tj = wt('jimatkan', tt)
cap(wt('dia', tt) + .02, wt('okay', tj) - .02 if False else wt('semua', tj) + .35, 'dia akan', [('JIMAT', 'y'), ('USAGE', 'w')], 'bc', 840, 128, [tj, wt('usage', tj)], hit='shing')
# ending checklist
tin = wt('install', 111); tl2 = wt('login', tin); tsi = wt('siap', tl2); tse = wt('selesai', tsi)
chips = [('INSTALL', tin), ('LOGIN', tl2), ('SIAP', tsi)]
HTML_SCREEN.append('<div id="chk" style="position:absolute;left:0;width:1080px;top:1580px;text-align:center;z-index:60">' + ''.join(f'<span class="chip" id="ck{i}">{n} <i>✓</i></span>' for i, (n, _) in enumerate(chips)) + '</div>')
for i, (n, tc) in enumerate(chips):
    tl_fromto(f'#ck{i}', {'opacity': 0, 'y': 30, 'scale': .6}, {'opacity': 1, 'y': 0, 'scale': 1}, tc - .12, .26, 'back.out(2.2)')
    sfx(tc - .12, ['click', 'tink', 'check'][i], -21)
tl_to('#chk', {'opacity': 0, 'filter': 'blur(8px)'}, tse + .25, .2); tl_set('#chk', {'opacity': 0}, tse + .5)
cap(tse - .02, DUR + 1, '', [('SELESAI', 'y')], 'bc', 820, 150, [tse], hit='stamp')

emit_caps()
# ---------------------------------------------------------------- audio extras: transitions
for t, k in ((22.25, 'zoom_in'), (37.45, 'zoom_in'), (47.9, 'zoom_in'), (79.15, 'zoom_in'), (98.0, 'zoom_in'), (112.8, 'zoom_in'),
             (7.35, 'swish_up'), (45.5, 'zoom_in'), (51.1, 'swish_dn'), (76.6, 'swish_up'), (88.05, 'shutter'), (6.35, 'zoom_out'), (26.0, 'zoom_out'),
             (43.3, 'zoom_out'), (102.3, 'zoom_out'), (116.2, 'zoom_out'), (90.3, 'swish_dn'), (40.55, 'swish_up'), (111.2, 'zoom_in'), (11.9, 'swish_up')):
    sfx(t, k, -22)
pass  # the supplied riser (audio.py) opens the video instead of the synth boot

# ---------------------------------------------------------------- write html
CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000;font-family:Poppins,sans-serif}}
#root{{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden;background:#000}}
#cam,#cam2{{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0;will-change:transform}}
#cam{{z-index:1}} #cam2{{z-index:3}}
#base,#pmat{{position:absolute;left:0;top:0;width:1920px;height:1080px}}
#pmat{{opacity:0}} #wback{{position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:2}}
.pn{{position:absolute;border-radius:26px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.55);background:#000;opacity:0}}
.pn video.pv{{width:100%;height:100%;object-fit:cover;display:block;position:absolute;left:0;top:0}}
.reel{{position:absolute;opacity:0}} .rp{{position:absolute;border-radius:24px;overflow:hidden;background:#000;box-shadow:0 30px 70px rgba(0,0,0,.55)}} .rp video.pv{{width:100%;height:100%;object-fit:cover;display:block;position:absolute;left:0;top:0}}
.card3d{{background:linear-gradient(160deg,#1a2050,#0f1224);border:2px solid rgba(255,255,255,.25);box-shadow:0 30px 70px rgba(0,0,0,.6);padding:28px 30px}}
.ct{{font-weight:800;font-size:40px;color:{LIME};letter-spacing:-1px}}
.ci{{font-size:56px;color:#fff;margin-bottom:8px}}
.cs{{margin-top:14px;font-weight:600;font-size:26px;color:#dfe3ff;line-height:1.35}}
.ch{{display:inline-block;opacity:0}}
.wb{{position:absolute;bottom:80px;width:44px;height:200px;border-radius:12px;background:#2a3060;overflow:hidden}}
.wb i{{position:absolute;left:0;bottom:0;width:100%;height:100%;background:{LIME};transform-origin:50% 100%;transform:scaleY(0)}}
.wb b{{position:absolute;bottom:-34px;left:-8px;width:60px;text-align:center;font-size:15px;color:#fff;font-weight:600}}
.cn{{position:absolute;right:24px;top:28px;font-weight:800;font-size:44px;color:#fff;opacity:0;text-shadow:0 0 22px rgba(255,255,255,.5)}}
.cap{{position:absolute;z-index:100;opacity:0;font-family:Poppins,sans-serif}}
.sm{{font-weight:500;color:#fff;font-size:.42em;line-height:1.15;text-shadow:.06em 0 0 #0b0b0d,-.06em 0 0 #0b0b0d,0 .06em 0 #0b0b0d,0 -.06em 0 #0b0b0d,.045em .045em 0 #0b0b0d,-.045em .045em 0 #0b0b0d,.045em -.045em 0 #0b0b0d,-.045em -.045em 0 #0b0b0d,0 .1em .22em rgba(0,0,0,.6);margin-bottom:.04em;text-transform:none}}
.bg2{{font-weight:800;line-height:1.02;text-transform:uppercase;letter-spacing:-.01em;text-shadow:.035em 0 0 #0b0b0d,-.035em 0 0 #0b0b0d,0 .035em 0 #0b0b0d,0 -.035em 0 #0b0b0d,.025em .025em 0 #0b0b0d,-.025em .025em 0 #0b0b0d,.025em -.025em 0 #0b0b0d,-.025em -.025em 0 #0b0b0d,0 .07em 0 #0b0b0d,0 .1em .22em rgba(0,0,0,.65)}}
.bw{{display:inline-block;transform-origin:50% 70%}}
.ov{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;overflow:hidden}}
.itl{{position:absolute;left:0;width:1080px;top:300px;text-align:center;font-weight:800;font-size:84px;color:#fff;letter-spacing:-2px}}
.ring{{position:absolute;left:270px;top:560px}}
.rgl{{position:absolute;left:0;width:1080px;top:1150px;text-align:center;font-weight:600;font-size:34px;color:#aab3d6;letter-spacing:2px;opacity:0}}
.wcol{{position:absolute;top:470px;width:137px;height:700px}}
.wbar{{position:absolute;left:18px;top:0;width:101px;height:560px;border-radius:24px;background:#2a3060;overflow:hidden}}
.wbar i{{position:absolute;left:0;bottom:0;width:100%;height:100%;background:{LIME};transform-origin:50% 100%;transform:scaleY(0)}}
.wcol b{{position:absolute;left:0;width:137px;top:590px;text-align:center;font-size:19px;color:#fff;font-weight:700;letter-spacing:1px}}
.lock{{position:absolute;left:0;width:1080px;top:1200px;text-align:center;font-weight:800;font-size:52px;color:{LIME};opacity:0}}
.rtl{{position:absolute;left:0;width:1080px;top:330px;text-align:center;font-weight:800;font-size:118px;color:#fff;letter-spacing:-3px}}
.rc1,.rc2{{position:absolute;left:140px;width:800px;height:300px;border-radius:30px;background:#141833;border:2px solid rgba(255,255,255,.22);text-align:center;opacity:0}}
.rc1{{top:700px}} .rc2{{top:1060px}}
.rc1 b,.rc2 b{{display:block;margin-top:34px;font-size:54px;font-weight:800}} .rc1 span,.rc2 span{{display:block;margin-top:14px;font-size:112px;font-weight:800;color:#fff}}
.spc{{position:absolute;left:90px;top:40px;width:900px;height:800px;border-radius:30px;background:#141833;border:2px solid rgba(255,255,255,.22);text-align:center}}
.spl{{position:absolute;left:0;width:100%;font-weight:800;font-size:52px;opacity:0}} #spa{{top:30px}} #spe{{top:670px}}
.spn{{position:absolute;left:0;width:100%;font-weight:800;font-size:130px;color:#fff;text-shadow:0 0 28px rgba(255,255,255,.55);opacity:0}} #spb{{top:110px}} #spd{{top:400px;font-size:120px}}
.spar{{position:absolute;left:0;width:100%;top:290px;font-size:70px;color:{LIME};font-weight:800;opacity:0}}
.sbh{{position:absolute;left:0;width:1080px;top:110px;text-align:center}}
.sbh .sm{{font-size:34px;opacity:0}} .sbh .bg2{{font-size:78px;margin-top:6px;opacity:0}}
.stp{{position:absolute;border-radius:26px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.55);border:2px solid rgba(255,255,255,.18);background:#000}}
.stp video.sv{{position:absolute;object-fit:cover;max-width:none}}
.stl{{position:absolute;width:280px;text-align:center}}
.stl span{{display:inline-block;background:{LIME};color:#0d1020;font-weight:800;font-size:34px;padding:2px 26px 4px;border-radius:999px}}
.stl em{{display:block;margin-top:10px;font-style:normal;font-weight:600;font-size:26px;color:#aab3d6;letter-spacing:2px}}
.lj{{position:absolute;left:0;width:1080px;top:1620px;text-align:center;font-weight:800;font-size:40px;color:{LIME};letter-spacing:4px}}
.num{{position:absolute;z-index:90;text-align:center;font-weight:800;font-size:150px;color:#fff;letter-spacing:-4px;text-shadow:0 0 30px rgba(255,255,255,.6),0 7px 0 rgba(0,0,0,.5)}}
.num small{{display:block;font-size:36px;color:{LIME};letter-spacing:6px;margin-bottom:-24px;text-shadow:0 4px 0 rgba(0,0,0,.6)}}
.chip{{display:inline-block;margin:0 8px;background:{LIME};color:#0d1020;font-weight:800;font-size:40px;padding:6px 28px 10px;border-radius:999px;opacity:0}} .chip i{{font-style:normal}}
'''
NDUR = round(DUR - SH, 3)
def shift_js(txt):
    parts = re.split(r'(?<=\);)\s*(?=(?:tl|gsap)\.)', txt)
    out = []
    for st in parts:
        st = st.strip()
        if not st: continue
        m = re.search(r'\},(-?\d+(?:\.\d+)?)\);$', st)
        if m:
            t = float(m.group(1))
            if t < SH - 1e-6: continue
            st = st[:m.start(1)] + f'{max(0.0, t - SH):.3f}' + st[m.end(1):]
        out.append(st)
    return '\n'.join(out)
JS_ALL = shift_js(PMAT_JS + '\n' + '\n'.join(JS))
CAM = CAM[int(round(SH * 30)):]
SFX = [[round(t - SH, 3), k, d] for t, k, d in SFX if t >= SH - 1e-6]
html = f'''<!doctype html>
<html lang="ms" data-resolution="portrait"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{NDUR}" data-width="1080" data-height="1920">
<div id="cam"><video id="base" class="clip" src="assets/main.mp4" muted playsinline data-start="0" data-duration="{NDUR}" data-media-start="{SH}" data-track-index="1"></video></div>
<div id="wback">{''.join(HTML_WORLD)}</div>
<div id="cam2"><video id="pmat" class="clip" src="assets/person.webm" muted playsinline data-start="0" data-duration="{NDUR}" data-media-start="{SH}" data-track-index="2"></video></div>
{''.join(HTML_SCREEN)}
{''.join(CAPS)}
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{NDUR}" data-track-index="50" data-volume="1"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{paused:true}});
const CAM = {json.dumps(CAM, separators=(',', ':'))};
gsap.set('#cam,#cam2',{{transformOrigin:'0 0',x:CAM[0][0],y:CAM[0][1],scale:CAM[0][2]}});
for(let i=1;i<CAM.length;i++){{const a=CAM[i-1],b=CAM[i];if(a[0]===b[0]&&a[1]===b[1]&&a[2]===b[2])continue;tl.fromTo('#cam,#cam2',{{x:a[0],y:a[1],scale:a[2]}},{{x:b[0],y:b[1],scale:b[2],duration:1/30,ease:'none',immediateRender:false}},(i-1)/30);}}
{JS_ALL}
window.__timelines["main"] = tl;
</script></body></html>'''
open('hf916/index.html', 'w').write(html)
json.dump({'dur': NDUR, 'sfx': sorted(SFX), 'hd': HD, 'sh': SH, 'hook_hit': round(wt('buat', 10) - SH, 3)}, open('build/sfx_events_916.json', 'w'))
print('html', len(html), 'sfx events', len(SFX), 'dur', NDUR)
