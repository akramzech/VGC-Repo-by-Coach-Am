#!/usr/bin/env python3
"""Neon Caption Explainer engine (latest) with a workshop beat list as the worked example. Writes hf/index.html + build/sfx_events.json (16:9, 1920x1080, 30 fps)."""
import json, math, re, random
W, H = 1920, 1080
tm = json.load(open('build/timemap.json')); DUR = round(tm['dur'], 3); HD = tm['hook_dur']
WORDS = json.load(open('build/words_out.json'))      # [text, snapped_out, out, src]
HEAD = json.load(open('build/headtrack.json'))       # [t, top, cx]
LIME, WHITE, NAVY = '#FFFF00', '#FFFFFF', '#0f1224'
SH = None  # set after words are loaded (below)

SH = 0.0      # > 0 trims the start: everything before SH is dropped and the rest shifts earlier
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
 (0.0, 1.55, 0, 'set', 960), (0.1, 1.72, 3.6, 'sine', 960),
 (3.8, 1.2, .7, 'cubic', 960), (7.0, 1.0, .8, 'sine', 960), (11.4, 1.32, .7, 'cubic', 960), (14.7, 1.0, .9, 'sine', 960),
 (17.2, 1.4, .7, 'cubic', 960), (19.8, 1.0, .9, 'sine', 960), (25.8, 1.0, .8, 'sine', 960),
 (38.2, 1.45, .7, 'cubic', 960), (41.0, 1.0, .9, 'sine', 960), (43.6, 1.36, .7, 'cubic', 960), (44.9, 1.0, .8, 'sine', 960),
 (50.3, 1.4, .8, 'sine', 470), (55.2, 1.0, .8, 'sine', 960),
 (56.9, 1.5, .8, 'sine', 470), (72.0, 1.5, .8, 'sine', 960), (73.0, 1.22, .9, 'sine', 960),
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
hx = gaussian_filter1d(hx, 26, mode='nearest'); hy = gaussian_filter1d(hy, 30, mode='nearest')     # ~0.85 s / 1.0 s low-pass
TX, TY, SS = [], [], []
for i in range(NF):
    S_, sx = cam_state(i / 30); SS.append(S_)
    TX.append(sx - S_ * hx[i]); TY.append(0.42 * H - S_ * hy[i])
TX = gaussian_filter1d(np.array(TX), 2.5, mode='nearest'); TY = gaussian_filter1d(np.array(TY), 2.5, mode='nearest')
CAM = []
for i in range(NF):
    S_ = SS[i]; tx = min(0, max(W - S_ * W, TX[i])); ty = min(0, max(H - S_ * H, TY[i]))
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
POS = {
  'bl': 'left:110px;top:{y}px;text-align:left;', 'bc': 'left:0;width:1920px;top:{y}px;text-align:center;',
  'br': 'right:110px;top:{y}px;text-align:right;', 'tc': 'left:0;width:1920px;top:{y}px;text-align:center;',
  'cl': 'left:110px;top:{y}px;text-align:left;',
}
CAPSPEC = []
def cap(t0, t1, small, big, pos='bc', y=820, fs=104, times=None, hit=None, sm_t=None, sfx_on=True, sfx_db=-22, small_after=None):
    CAPSPEC.append(dict(t0=t0, t1=t1, small=small, big=big, pos=pos, y=y, fs=fs, times=times, hit=hit, sm_t=sm_t, sfx_on=sfx_on, sfx_db=sfx_db))
def emit_caps():
    S_ = sorted(CAPSPEC, key=lambda c: c['t0'])
    for i, c in enumerate(S_):
        for d in S_[i + 1:]:
            if d['t0'] >= c['t1'] + .2: break
            if abs(d['y'] - c['y']) < 260 and d['pos'] == c['pos'] or (d['pos'] != c['pos'] and abs(d['y'] - c['y']) < 150):
                c['t1'] = max(c['t0'] + .3, d['t0'] - .04); c['fade'] = .05; break
    for c in S_: emit_cap(**c)
def emit_cap(t0, t1, small, big, pos='bc', y=820, fs=104, times=None, hit=None, sm_t=None, sfx_on=True, sfx_db=-22, fade=.16):
    n = cap_n[0]; cap_n[0] += 1; cid = f'c{n}'
    sm_html = f'<div class="sm" id="{cid}s"' + (' style="font-size:1em"' if not big else '') + f'>{small}</div>' if small else ''
    bw = ''.join(('<br>' if w == '\\n' else f'<span class="bw {cl}" id="{cid}w{j}">{w}</span> ') for j, (w, c) in enumerate(big) for cl in [('y' if c == 'y' else 'w')])
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
# ---- SHOWREEL A: phone recordings behind me (20.0 -> 25.8)
A0, A1 = 20.0, 25.8
PMAT_WIN.append((A0 - .15, A1 + .1))
reel('reelA', A0, A1, [('assets/panels/r1.mp4', 0, '50% 50%'), ('assets/panels/r2.mp4', 0, '50% 50%'), ('assets/panels/r3.mp4', 0, '50% 50%'),
                       ('assets/panels/r1.mp4', 6, '50% 50%'), ('assets/panels/r2.mp4', 6, '50% 50%'), ('assets/panels/r3.mp4', 6, '50% 50%')])
sfx(A0, 'slide', -22); sfx(A0 + .45, 'swish_up', -27)
# ---- SHOWREEL B: my past ads, fast (55.3 -> 57.4)
B0, B1 = 55.3, 57.4
PMAT_WIN.append((B0 - .1, B1 + .1))
reel('reelB', B0, B1, [('assets/panels/n1.mp4', 2, '50% 50%'), ('assets/panels/n2.mp4', 4, '50% 50%'), ('assets/panels/n4.mp4', 5, '50% 50%'),
                       ('assets/panels/n5.mp4', 4, '50% 50%'), ('assets/panels/n6.mp4', 5, '50% 50%'), ('assets/panels/n7.mp4', 4, '50% 50%')], rot=-15, x0=700, x1=-560, ease='power1.inOut')
sfx(B0, 'slide', -21); sfx(B0 + 1.0, 'swish_dn', -26)

# ---- full-screen overlays ----------------------------------------------------------------
def overlay(oid, t0, t1, inner, bg=NAVY, fin='blur', fout='blur', z=30):
    HTML_SCREEN.append(f'<div id="{oid}" class="ov" style="background:{bg};z-index:{z}">{inner}</div>')
    tl_fromto(f'#{oid}', {'opacity': 0, 'scale': 1.06, 'filter': 'blur(14px)'}, {'opacity': 1, 'scale': 1, 'filter': 'blur(0px)'}, t0, .3, 'expo.out')
    tl_to(f'#{oid}', {'opacity': 0, 'scale': .96, 'filter': 'blur(12px)'}, t1 - .25, .25, 'power2.in')
    tl_set(f'#{oid}', {'opacity': 0}, t1 + .01)


# ---- icons
def cloud(x, y, s, c='#FBFF0B', ido=''):
    return f'<svg {ido} class="abs" style="left:{x}px;top:{y}px" width="{s}" height="{s*.65}" viewBox="0 0 120 78"><path d="M30 70a24 24 0 0 1-2-48 32 32 0 0 1 62 8 20 20 0 0 1 0 40z" fill="none" stroke="{c}" stroke-width="7" stroke-linejoin="round"/></svg>'
def folder(x, y, s, c='#fff', ido=''):
    return f'<svg {ido} class="abs" style="left:{x}px;top:{y}px" width="{s}" height="{s*.8}" viewBox="0 0 100 80"><path d="M6 14h30l8 10h50v50H6z" fill="none" stroke="{c}" stroke-width="6" stroke-linejoin="round"/></svg>'

# ---- DIAGRAM 1: Claude cannot reach the computer; it works through GitHub / Drive in the cloud (7.0 -> 11.3)
D0, D1 = 7.0, 11.3
dg = (f'<div class="itl2" id="dgh"><span style="color:{LIME}">KOMPUTER</span> TAK DIAKSES</div>'
      '<div class="gcard" id="dgA" style="left:110px;top:230px;width:520px;height:470px"><div class="gct">KOMPUTER</div></div>'
      + folder(285, 390, 190, '#fff', 'id="dgf"') +
      '<div id="dgbar" class="abs" style="left:690px;top:250px;width:8px;height:430px;border-radius:4px;background:repeating-linear-gradient(#ff3b3b 0 20px,transparent 20px 34px)"></div>'
      '<svg id="dgx" class="abs" style="left:632px;top:420px" width="124" height="124" viewBox="0 0 120 120"><circle cx="60" cy="60" r="46" fill="#ff3b3b"/><path d="M38 38l44 44M82 38L38 82" stroke="#fff" stroke-width="12" stroke-linecap="round"/></svg>'
      f'<div class="abs arrow" id="dga" style="left:545px;top:395px">→</div>'
      '<div class="gcard" id="dgB" style="left:790px;top:230px;width:1020px;height:470px"><div class="gct">CLOUD</div></div>'
      + cloud(830, 320, 150, LIME, 'id="dgc1"') + cloud(830, 500, 150, '#fff', 'id="dgc2"') +
      '<div class="abs" id="dgp1" style="left:1000px;top:335px"><span class="pill2">GITHUB</span></div><div class="abs" id="dgp2" style="left:1000px;top:515px"><span class="pill2" style="background:#fff">DRIVE</span></div>'
      '<svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080"><path id="dgl1" d="M1210 368 C1300 368 1330 430 1420 430" fill="none" stroke="#FFFF00" stroke-width="6" stroke-linecap="round" stroke-dasharray="16 12" opacity="0"/>'
      '<path id="dgl2" d="M1210 548 C1300 548 1330 490 1420 490" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-dasharray="16 12" opacity="0"/>'
      '<circle id="dgd1" r="11" fill="#FFFF00" opacity="0"/><circle id="dgd2" r="11" fill="#fff" opacity="0"/></svg>'
      f'<div id="dgcl" class="abs clnode" style="left:1420px;top:395px"><span>✦</span>CLAUDE</div>')
overlay('dgov', D0, D1, dg)
tl_fromto('#dgh', {'opacity': 0, 'y': -20}, {'opacity': 1, 'y': 0}, D0 + .1, .3)
tl_fromto('#dgA,#dgf', {'opacity': 0, 'x': -60}, {'opacity': 1, 'x': 0}, D0 + .2, .4, 'expo.out')
tl_fromto('#dgbar', {'opacity': 0, 'scaleY': 0}, {'opacity': 1, 'scaleY': 1}, D0 + .45, .25, 'power3.out')
# the arrow tries to cross, hits the barrier and bounces back; computer shakes; X stamps
tl_fromto('#dga', {'opacity': 0, 'x': 0}, {'opacity': 1, 'x': 120}, D0 + .6, .28, 'power2.in')
tl_to('#dga', {'x': 10, 'opacity': 0}, D0 + .9, .22, 'power2.out')
tl_fromto('#dgx', {'opacity': 0, 'scale': .2}, {'opacity': 1, 'scale': 1}, D0 + .88, .28, 'back.out(3)')
for i_, dx_ in enumerate((-12, 10, -6, 3, 0)): tl_fromto('#dgA', {'x': dx_}, {'x': 0, 'immediateRender': False}, D0 + .9 + i_ * .04, .04, 'none')
tg = wt('github', 6.5); td = wt('drive', 8.5)
tl_fromto('#dgB', {'opacity': 0, 'x': 80}, {'opacity': 1, 'x': 0}, tg - .15, .45, 'expo.out')
tl_fromto('#dgc1,#dgp1', {'opacity': 0, 'scale': .5}, {'opacity': 1, 'scale': 1}, tg + .05, .32, 'back.out(2.2)'); tl_fromto('#dgc2,#dgp2', {'opacity': 0, 'scale': .5}, {'opacity': 1, 'scale': 1}, td - .1, .32, 'back.out(2.2)')
tl_fromto('#dgcl', {'opacity': 0, 'scale': .4}, {'opacity': 1, 'scale': 1}, tg + .4, .38, 'back.out(2.4)')
# flowing dashes + travelling dots to Claude
for lid, did, t0_, c in (('dgl1', 'dgd1', tg + .75, 1), ('dgl2', 'dgd2', td + .05, 2)):
    tl_fromto(f'#{lid}', {'opacity': 0}, {'opacity': .95}, t0_, .2, 'power2.out')
    tl_fromto(f'#{lid}', {'strokeDashoffset': 0}, {'strokeDashoffset': -300, 'immediateRender': False}, t0_, D1 - t0_ - .3, 'none')
    ya, yb = (368, 430) if c == 1 else (548, 490)
    tl_fromto(f'#{did}', {'opacity': 0, 'x': 1210, 'y': ya}, {'opacity': 1, 'x': 1420, 'y': yb, 'immediateRender': False}, t0_, .7, 'power1.inOut')
    tl_to(f'#{did}', {'opacity': 0}, t0_ + .65, .1, 'none')
    tl_fromto(f'#{did}', {'opacity': 0, 'x': 1210, 'y': ya}, {'opacity': 1, 'x': 1420, 'y': yb, 'immediateRender': False}, t0_ + .9, .7, 'power1.inOut')
    tl_to(f'#{did}', {'opacity': 0}, t0_ + 1.55, .1, 'none')
sfx(D0, 'zoom_in', -22); sfx(D0 + .6, 'swish_up', -26); sfx(D0 + .88, 'stamp', -20); sfx(tg, 'click', -21); sfx(td, 'tink', -22); sfx(tg + .45, 'pop', -22)

# ---- TABLE: cloud vs local (26.0 -> 38.2)
T0, T1 = 26.0, 38.2
tb = (f'<div class="gcard" style="left:90px;top:110px;width:1740px;height:760px"></div><div class="abs" style="left:960px;top:110px;width:2px;height:760px;background:rgba(255,255,255,.2)"></div>'
      f'<div class="abs gct2" id="tbh1" style="left:90px;width:870px;top:140px;color:{LIME}">CLOUD <span style="color:#fff;font-size:40px">(ada awan)</span></div><div class="abs gct2" id="tbh2" style="left:960px;width:870px;top:140px;color:{LIME}">LOCAL <span style="color:#fff;font-size:40px">(tiada awan)</span></div>'
      + '<div id="tbr1">' + cloud(250, 300, 150) + '<div class="abs rowt" style="left:440px;top:318px">CLAUDE</div></div>'
      + '<div id="tbr2">' + cloud(250, 520, 150, '#fff') + '<div class="abs rowt" style="left:440px;top:538px">GITHUB</div></div>'
      + '<div id="tbr3">' + folder(1120, 330, 150) + '<div class="abs rowt" style="left:1300px;top:312px;line-height:1.05">FOLDER<br><span style="color:#aab3d6;font-size:34px;font-weight:600">output cloud</span></div></div>'
      + f'<div id="tbon" class="abs" style="left:90px;width:870px;top:225px;text-align:center"><span class="pill2" style="background:#25d366;color:#04210f;font-size:34px">● ONLINE</span></div><div id="tboff" class="abs" style="left:960px;width:870px;top:225px;text-align:center"><span class="pill2" style="background:#ff3b3b;color:#fff;font-size:34px">DALAM KOMPUTER</span></div>'
      + '<div id="tbr4" class="abs" style="left:960px;width:870px;top:640px;text-align:center"><span class="pill2" style="background:#ff3b3b;color:#fff;font-size:46px">TAK ADA AWAN</span></div>')
overlay('tbov', T0, T1, tb)
tl_fromto('#tbh1', {'opacity': 0, 'y': -16}, {'opacity': 1, 'y': 0}, T0 + .15, .3); tl_fromto('#tbh2', {'opacity': 0, 'y': -16}, {'opacity': 1, 'y': 0}, T0 + .3, .3)
tl_fromto('#tbr1', {'opacity': 0, 'x': -40}, {'opacity': 1, 'x': 0}, T0 + .5, .35); tl_fromto('#tbr2', {'opacity': 0, 'x': -40}, {'opacity': 1, 'x': 0}, wt('github', 25.5) - .1, .35)
tl_fromto('#tbr3', {'opacity': 0, 'x': 40}, {'opacity': 1, 'x': 0}, wt('motion', 27.5), .35); tl_fromto('#tbr4', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, wt('tak', 30.5), .3, 'back.out(2)')
tl_fromto('#tbon', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, T0 + .6, .3, 'back.out(2)'); tl_fromto('#tboff', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, T0 + .75, .3, 'back.out(2)')
sfx(T0, 'burn', -23); sfx(T0 + .5, 'click', -21); sfx(wt('github', 25.5), 'tink', -22); sfx(wt('motion', 27.5), 'pop', -22); sfx(wt('tak', 30.5), 'stamp', -21)

# ---- SCREENSHOT: the project rows of the Claude app (45.0 -> 50.4)
S0, S1 = 45.0, 50.4
sc = (f'<div class="itl2" id="sch">TEKAN <span style="color:{LIME}">+</span> &nbsp;·&nbsp; AWAN = <span style="color:{LIME}">CLAUDE ONLINE</span></div>'
      '<div class="abs shot" id="scimg" style="left:150px;top:230px;width:1110px;height:560px"><img src="assets/projects_crop.png" style="width:100%;height:100%;object-fit:cover"></div>'
      '<div class="abs ring2" id="scr1" style="left:1001px;top:265px;width:114px;height:229px"></div><div class="abs ring2" id="scr2" style="left:1095px;top:681px;width:98px;height:98px"></div>')
sc += ('<svg id="scur" class="abs" style="left:0;top:0;z-index:5" width="56" height="64" viewBox="0 0 28 32"><path d="M3 2l20 14-9 1.5 5 9-3.5 2-5-9L3 24z" fill="#fff" stroke="#0d1020" stroke-width="2" stroke-linejoin="round"/></svg>'
       '<div id="scrip" class="abs ring2" style="left:1119px;top:705px;width:50px;height:50px;border-radius:50%;opacity:0"></div>'
       f'<div class="gcard" id="scset" style="left:1330px;top:250px;width:470px;height:520px"><div class="gct" style="font-size:40px">SETTING AUTO</div>'
       + ''.join(f'<div class="srow" id="scs{i_}" style="top:{110 + i_ * 130}px"><b>✓</b>{t_}</div>' for i_, t_ in enumerate(('Repo', 'Folder', 'Environment'))) + '</div>')
overlay('scov', S0, S1, sc, bg='radial-gradient(1300px 760px at 50% 52%,#1d2350,#0d1020)')
tl_fromto('#sch', {'opacity': 0, 'y': -20}, {'opacity': 1, 'y': 0}, S0 + .1, .3)
tl_fromto('#scimg', {'opacity': 0, 'y': 50, 'rotationY': 14, 'transformPerspective': 1800, 'scale': .92}, {'opacity': 1, 'y': 0, 'rotationY': -5, 'scale': 1}, S0 + .15, .55, 'expo.out')
tl_to('#scimg', {'rotationY': -2, 'y': -8}, S0 + .7, S1 - S0 - 1.1, 'sine.inOut')
tl_fromto('#scr2', {'opacity': 0, 'scale': 1.6}, {'opacity': 1, 'scale': 1}, wt('plus', 46.0) - .1, .3, 'back.out(1.8)')
tl_fromto('#scr1', {'opacity': 0, 'scale': 1.6}, {'opacity': 1, 'scale': 1}, wt('automatic', 47.5), .3, 'back.out(1.8)')
tpl = wt('plus', 46.0); tau = wt('automatic', 47.5)
tl_fromto('#scur', {'opacity': 0, 'x': 1180, 'y': 900}, {'opacity': 1, 'x': 1128, 'y': 716, 'immediateRender': False}, tpl - .85, .75, 'power3.inOut')
tl_fromto('#scrip', {'opacity': .9, 'scale': .3}, {'opacity': 0, 'scale': 2.6, 'immediateRender': False}, tpl - .02, .5, 'power2.out')
tl_to('#scur', {'x': 1136, 'y': 722}, tpl - .08, .08, 'power1.in'); tl_to('#scur', {'x': 1128, 'y': 716}, tpl, .1, 'power1.out')
tl_fromto('#scset', {'opacity': 0, 'x': 80, 'scale': .94}, {'opacity': 1, 'x': 0, 'scale': 1}, tau - .1, .45, 'expo.out')
for i_ in range(3):
    tl_fromto(f'#scs{i_}', {'opacity': 0, 'x': 40}, {'opacity': 1, 'x': 0}, tau + .15 + i_ * .5, .3, 'back.out(2)'); sfx(tau + .15 + i_ * .5, ['tink', 'ping', 'check'][i_], -22)
sfx(S0, 'zoom_in', -22); sfx(tpl - .02, 'click', -19); sfx(tau, 'whip', -23)

# ---- SPLIT A: everything lands in the folder on my computer (50.4 -> 55.2), presenter pinned left
PA0, PA1 = 50.4, 55.2
cols_ = ('linear-gradient(135deg,#ff7a59,#ff3b6b)', 'linear-gradient(135deg,#59c3ff,#3b6bff)', 'linear-gradient(135deg,#ffd45a,#ff9a3b)', 'linear-gradient(135deg,#7dff9a,#1fb86a)', 'linear-gradient(135deg,#d08bff,#7a3bff)', 'linear-gradient(135deg,#ff8bd0,#ff3b9a)')
spa_ = ('<div class="spc2"><div class="spl2" id="sAa" style="color:' + LIME + '">KOMPUTER SAYA</div>'
        '<svg class="abs" id="sAl" style="left:110px;top:200px" width="620" height="470" viewBox="0 0 620 470"><rect x="40" y="20" width="540" height="340" rx="22" fill="#0e1230" stroke="#fff" stroke-width="6"/><path d="M10 380h600l-40 52H50z" fill="none" stroke="#fff" stroke-width="6" stroke-linejoin="round"/></svg>'
        + folder(310, 330, 220, LIME, 'id="sAf"') +
        ''.join(f'<div class="th" id="sAt{i_}" style="left:{90 + i_ * 110}px;top:128px;background:{cols_[i_]}">▶</div>' for i_ in range(6)) +
        '<div class="abs" id="sAp" style="left:0;width:100%;top:760px;text-align:center"><span class="pill2" style="font-size:42px">FOLDER · output cloud</span></div></div>')
HTML_SCREEN.append(f'<div id="splitA" style="position:absolute;left:960px;top:0;width:960px;height:1080px;z-index:30;opacity:0;background:#0b0e1c">{spa_}</div>')
tl_fromto('#splitA', {'opacity': 0, 'x': 160, 'filter': 'blur(10px)'}, {'opacity': 1, 'x': 0, 'filter': 'blur(0px)'}, PA0, .35, 'expo.out')
tl_to('#splitA', {'opacity': 0, 'x': 120, 'filter': 'blur(10px)'}, PA1 - .25, .25, 'power2.in'); tl_set('#splitA', {'opacity': 0}, PA1 + .01)
tl_fromto('#sAa', {'opacity': 0, 'y': 16}, {'opacity': 1, 'y': 0}, PA0 + .2, .3); tl_fromto('#sAl,#sAf', {'opacity': 0, 'scale': .85}, {'opacity': 1, 'scale': 1}, PA0 + .3, .45, 'back.out(1.6)')
tf_ = wt('folder', 53.0)
for i_ in range(6):
    td_ = wt('semuanya', 51.5) + i_ * .26
    tl_fromto(f'#sAt{i_}', {'opacity': 0, 'y': -30, 'scale': 1}, {'opacity': 1, 'y': 0, 'scale': 1, 'immediateRender': False}, td_ - .25, .2, 'power2.out')
    tl_to(f'#sAt{i_}', {'x': 380 - (90 + i_ * 110) + 20, 'y': 280, 'scale': .35, 'opacity': 0}, td_, .42, 'power3.in')
    sfx(td_ + .35, ['pop', 'tink', 'click'][i_ % 3], -25)
tl_fromto('#sAf', {'filter': 'drop-shadow(0 0 0 rgba(255,255,0,0))'}, {'filter': 'drop-shadow(0 0 26px rgba(255,255,0,.95))', 'immediateRender': False}, tf_, .4, 'power2.out')
tl_fromto('#sAp', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, PA0 + .9, .35, 'back.out(1.8)')
sfx(PA0, 'slide', -22); sfx(tf_, 'stamp', -21)

# ---- SPLIT: kekurangan card (56.9 -> 72.0) -- presenter pinned left (camera sx 470)
P0, P1 = 56.9, 72.0
sp = ('<div class="spc2"><div class="spl2" id="spa" style="color:' + LIME + '">KEKURANGAN</div>'
      '<div class="sprow" id="spr1" style="top:120px"><b style="color:' + LIME + '">LOCAL</b><span>usage komputer makin <u>HEAVY</u></span><div class="bar"><i id="bar1f" style="background:#ff3b3b"></i></div></div>'
      '<div class="sprow" id="spr2" style="top:380px"><b style="color:' + LIME + '">GITHUB</b><span>internet slow → makin <u>SLOW</u></span><div class="bar"><i id="bar2f" style="background:#ffb020"></i></div></div>'
      '<div class="spflow" id="spf"><i id="spf1">DRIVE</i><em>→</em><i id="spf2">GITHUB</i><em>→</em><i id="spf3" style="background:' + LIME + ';color:#0d1020">EDIT VIDEO</i></div></div>')
HTML_SCREEN.append(f'<div id="splitov" style="position:absolute;left:960px;top:0;width:960px;height:1080px;z-index:30;opacity:0;background:#0b0e1c">{sp}</div>')
tl_fromto('#splitov', {'opacity': 0, 'x': 160, 'filter': 'blur(10px)'}, {'opacity': 1, 'x': 0, 'filter': 'blur(0px)'}, P0, .35, 'expo.out')
tl_to('#splitov', {'opacity': 0, 'x': 120, 'filter': 'blur(10px)'}, P1 - .25, .25, 'power2.in'); tl_set('#splitov', {'opacity': 0}, P1 + .01)
tl_fromto('#spa', {'opacity': 0, 'y': 16}, {'opacity': 1, 'y': 0}, P0 + .15, .3)
tl_fromto('#spr1', {'opacity': 0, 'x': 50}, {'opacity': 1, 'x': 0}, wt('komputer', 57.5) - .25, .35); tl_fromto('#spr2', {'opacity': 0, 'x': 50}, {'opacity': 1, 'x': 0}, wt('internet', 63) - .3, .35)
tl_fromto('#spf', {'opacity': 0, 'y': 30}, {'opacity': 1, 'y': 0}, wt('download', 67.5) - .1, .4, 'expo.out')
th_ = wt('heavy', 58.5); ts_ = wt('internet', 63)
tl_fromto('#bar1f', {'scaleX': 0}, {'scaleX': 1}, th_ - .5, 1.0, 'power2.in')
tl_fromto('#bar2f', {'scaleX': 0}, {'scaleX': .38}, ts_, 4.2, 'none')
tl_fromto('#spf1', {'opacity': .3, 'scale': .9}, {'opacity': 1, 'scale': 1}, wt('drive', 68), .25, 'back.out(2)'); tl_fromto('#spf2', {'opacity': .3, 'scale': .9}, {'opacity': 1, 'scale': 1}, wt('github', 69.5), .25, 'back.out(2)'); tl_fromto('#spf3', {'opacity': .3, 'scale': .9}, {'opacity': 1, 'scale': 1}, wt('edit', 70.5), .25, 'back.out(2)')
sfx(wt('drive', 68), 'click', -23); sfx(wt('github', 69.5), 'tink', -23); sfx(wt('edit', 70.5), 'check', -22)
sfx(P0, 'slide', -22); sfx(wt('komputer', 57.5) - .25, 'click', -22); sfx(wt('internet', 63) - .3, 'tink', -22); sfx(wt('download', 67.5), 'swish_up', -26)

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


# ---------------------------------------------------------------- captions
t = wt
cap(0.1, 3.7, '', [('NOMBOR', 'w'), ('2', 'y')], 'bc', 800, 150, [t('nombor'), t('dua')], hit='stamp')
cap(3.75, 6.9, 'sebab kita tak nak', [('CLAUDE', 'y'), ('AKSES', 'w'), ('\\n', 'w'), ('DALAMAN', 'w'), ('KOMPUTER', 'y')], 'bc', 760, 100, [t('claude'), t('akses'), t('dalaman'), t('komputer')], hit='pop')
cap(7.0, 11.2, 'sebab tu kita buat', [('GITHUB', 'y'), ('ATAUPUN', 'w'), ('DRIVE', 'y')], 'bc', 850, 100, [t('github', 6.5), t('ataupun'), t('drive', 8.5)], hit='click')
cap(11.3, 14.9, 'kalau tengok skrin saya', [('MACAM', 'w'), ('PENING', 'y'), ('SIKIT', 'w')], 'bc', 810, 118, [t('macam'), t('pening'), t('sikit')], hit='tink')
cap(15.0, 17.2, 'fokus on', [('BELAH', 'w'), ('KIRI', 'y')], 'bc', 810, 126, [t('belah'), t('kiri')], hit='pop')
cap(17.2, 19.9, 'dan sebagainya', [('REPO', 'y')], 'bc', 810, 150, [t('repo')], hit='stamp')
cap(20.0, 22.24, 'ni edit guna', [('PHONE', 'y')], 'bc', 830, 140, [t('phone')], hit='click')
cap(22.3, 24.3, 'yang ada awan ni', [('CLAUDE', 'y')], 'bc', 830, 130, [t('claude', 22)], hit='pop')
cap(24.4, 25.9, 'ataupun masuk dekat', [('GITHUB', 'y')], 'bc', 830, 130, [t('github', 24.9)], hit='tink')
cap(26.0, 28.9, 'yang ni ada awan', [('GITHUB', 'y')], 'bc', 920, 90, [t('github', 25.5)], hit='click')
cap(29.0, 30.3, 'yang ni motion add', [('OUTPUT', 'w'), ('CLOUD', 'y')], 'bc', 920, 90, [t('output', 29), t('cloud', 29)], hit='key')
cap(30.4, 33.7, 'dia', [('TAK', 'w'), ('ADA', 'w'), ('AWAN', 'y')], 'bc', 920, 90, [t('tak', 30.5), t('ada', 31), t('awan', 31.2)], hit='stamp')
cap(33.8, 38.0, 'sebab yang ini daripada saya punya', [('FOLDER', 'y')], 'bc', 920, 100, [t('folder', 36)], hit='pop')
cap(38.2, 39.7, 'perasan tak?', [('OUTPUT', 'w'), ('CLOUD', 'y')], 'bc', 810, 126, [t('output', 38), t('cloud', 38.5)], hit='stamp')
cap(39.8, 43.46, 'apa-apa video yang saya buat', [('DALAM', 'w'), ('CHAT', 'y'), ('NI', 'w')], 'bc', 810, 118, [t('dalam', 42), t('chat', 42.3), t('ni', 42.6)], hit='click')
cap(43.5, 44.9, 'saya tak buka', [('NEW', 'w'), ('CHAT', 'y')], 'bc', 810, 130, [t('new'), t('chat', 44)], hit='tink')
cap(45.0, 47.45, 'terus tekan', [('PLUS', 'y')], 'bc', 850, 130, [t('plus')], hit='click')
cap(47.5, 50.3, 'dia akan automatic panggil', [('SETTING', 'y')], 'bc', 850, 130, [t('setting')], hit='pop')
cap(50.4, 55.2, 'semuanya masuk dalam', [('FOLDER', 'y'), ('KOMPUTER', 'w')], 'bl', 810, 90, [t('folder', 53), t('komputer', 54)], hit='stamp')
cap(55.3, 57.0, 'semua video', [('PERNAH', 'w'), ('DIBUAT', 'y')], 'bc', 840, 118, [t('pernah'), t('dibuat')], hit='click')
cap(57.0, 58.6, 'apa', [('KEKURANGAN', 'y'), ('DIA?', 'w')], 'bl', 860, 80, [t('kekurangan'), t('dia', 57.5)], hit='pop')
cap(58.7, 60.8, 'komputer makin', [('HEAVY', 'y')], 'bl', 860, 100, [t('heavy')], hit='stamp')
cap(60.9, 62.4, 'kalau', [('GITHUB', 'y'), ('TADI', 'w')], 'bl', 860, 90, [t('github', 60.5), t('tadi')], hit='tink')
cap(62.5, 66.0, 'kalau internet speed', [('SLOW', 'y')], 'bl', 860, 100, [t('slow')], hit='click')
cap(66.1, 68.0, 'dia akan', [('TAMBAH', 'w'), ('SLOW', 'y')], 'bl', 860, 90, [t('bertambahkan'), t('slow', 67)], hit='pop')
cap(68.1, 72.0, 'download daripada drive, masuk GitHub', [('BARU', 'w'), ('EDIT', 'y'), ('VIDEO', 'y')], 'bl', 860, 80, [t('baru'), t('edit', 70.5), t('video', 71)], hit='stamp')
cap(72.05, DUR + 1, 'tak faham?', [('CUBA', 'w'), ('LUKIS', 'y')], 'bc', 800, 150, [t('cuba'), t('lukis', 72.3)], hit='stamp')

emit_caps()
# ---------------------------------------------------------------- audio extras: transitions
for t_, k in ((3.8, 'zoom_in'), (7.0, 'zoom_out'), (11.4, 'swish_up'), (14.7, 'zoom_out'), (17.2, 'zoom_in'), (19.8, 'swish_dn'), (38.2, 'zoom_in'), (41.0, 'zoom_out'),
              (43.6, 'swish_up'), (50.3, 'zoom_in'), (53.4, 'zoom_out'), (56.9, 'shutter'), (72.0, 'zoom_in'), (73.0, 'zoom_out')):
    sfx(t_, k, -22)
pass  # the supplied riser (audio.py) opens the video instead of the synth boot

# ---------------------------------------------------------------- write html
CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1920px;height:1080px;overflow:hidden;background:#000;font-family:Poppins,sans-serif}}
#root{{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:hidden;background:#000}}
#cam{{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0;will-change:transform}}
#base,#pmat{{position:absolute;left:0;top:0;width:1920px;height:1080px}}
#pmat{{opacity:0;z-index:3}} #base{{z-index:1}} #wback{{position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:2}}
.pn{{position:absolute;border-radius:26px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.55);background:#000;opacity:0}}
.pn video.pv{{width:100%;height:100%;object-fit:cover;display:block;position:absolute;left:0;top:0}}
.reel{{position:absolute;opacity:0}} .rp{{position:absolute;border-radius:24px;overflow:hidden;background:#000;box-shadow:0 30px 70px rgba(0,0,0,.55)}} .rp video.pv{{width:100%;height:100%;object-fit:cover;display:block;position:absolute;left:0;top:0}}
.card3d{{background:linear-gradient(160deg,#1a2050,#0f1224);border:2px solid rgba(255,255,255,.25);box-shadow:0 30px 70px rgba(0,0,0,.6);padding:34px 36px}}
.ct{{font-weight:800;font-size:50px;color:{LIME};letter-spacing:-1px}}
.ci{{font-size:70px;color:#fff;margin-bottom:10px}}
.cs{{margin-top:18px;font-weight:600;font-size:30px;color:#dfe3ff;line-height:1.35}}
.ch{{display:inline-block;opacity:0}}
.wb{{position:absolute;bottom:90px;width:56px;height:260px;border-radius:12px;background:#2a3060;overflow:hidden}}
.wb i{{position:absolute;left:0;bottom:0;width:100%;height:100%;background:{LIME};transform-origin:50% 100%;transform:scaleY(0)}}
.wb b{{position:absolute;bottom:-40px;left:-6px;width:68px;text-align:center;font-size:18px;color:#fff;font-weight:600}}
.cn{{position:absolute;right:30px;top:34px;font-weight:800;font-size:60px;color:#fff;opacity:0;text-shadow:0 0 22px rgba(255,255,255,.5)}}
.cap{{position:absolute;z-index:100;opacity:0;font-family:Poppins,sans-serif}}
.sm{{font-weight:500;color:#fff;font-size:.42em;line-height:1.15;margin-bottom:.06em;text-transform:none;text-shadow:0 0 .1em rgba(255,255,255,.7),0 0 .35em rgba(255,255,255,.3),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}}
.bg2{{font-weight:800;line-height:1.04;text-transform:uppercase;letter-spacing:-.012em}}
.bw.y{{color:#FFFF00;text-shadow:0 0 .05em rgba(255,255,0,.95),0 0 .2em rgba(255,255,0,.6),0 0 .45em rgba(255,255,0,.35),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}}
.bw.w{{font-weight:600;color:#fff;text-shadow:0 0 .06em rgba(255,255,255,.9),0 0 .2em rgba(255,255,255,.5),0 0 .45em rgba(255,255,255,.28),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}}
.bw{{display:inline-block;transform-origin:50% 70%}}
.ov{{position:absolute;left:0;top:0;width:1920px;height:1080px;opacity:0;overflow:hidden}}
.itl{{position:absolute;left:0;width:1920px;top:70px;text-align:center;font-weight:800;font-size:110px;color:#fff;letter-spacing:-2px}}
.ring{{position:absolute;left:690px;top:190px}}
.rgl{{position:absolute;left:0;width:1920px;top:740px;text-align:center;font-weight:600;font-size:38px;color:#aab3d6;letter-spacing:2px;opacity:0}}
.wcol{{position:absolute;top:200px;width:200px;height:560px}}
.wbar{{position:absolute;left:30px;top:0;width:140px;height:440px;border-radius:24px;background:#2a3060;overflow:hidden}}
.wbar i{{position:absolute;left:0;bottom:0;width:100%;height:100%;background:{LIME};transform-origin:50% 100%;transform:scaleY(0)}}
.wcol b{{position:absolute;left:0;width:200px;top:460px;text-align:center;font-size:30px;color:#fff;font-weight:700;letter-spacing:2px}}
.lock{{position:absolute;left:0;width:1920px;top:735px;text-align:center;font-weight:800;font-size:60px;color:{LIME};opacity:0}}
.rtl{{position:absolute;left:0;width:1920px;top:110px;text-align:center;font-weight:800;font-size:150px;color:#fff;letter-spacing:-3px}}
.rc1,.rc2{{position:absolute;top:470px;width:700px;height:380px;border-radius:30px;background:#141833;border:2px solid rgba(255,255,255,.22);text-align:center;opacity:0}}
.rc1{{left:180px}} .rc2{{left:1040px}}
.rc1 b,.rc2 b{{display:block;margin-top:50px;font-size:62px;font-weight:800}} .rc1 span,.rc2 span{{display:block;margin-top:30px;font-size:130px;font-weight:800;color:#fff}}
.spc{{position:absolute;left:100px;top:170px;width:760px;height:740px;border-radius:30px;background:#141833;border:2px solid rgba(255,255,255,.22);text-align:center}}
.spl{{position:absolute;left:0;width:100%;font-weight:800;font-size:56px;opacity:0}} #spa{{top:40px}} #spe{{top:620px}}
.spn{{position:absolute;left:0;width:100%;font-weight:800;font-size:150px;color:#fff;text-shadow:0 0 28px rgba(255,255,255,.55);opacity:0}} #spb{{top:140px}} #spd{{top:420px;font-size:136px}}
.spar{{position:absolute;left:0;width:100%;top:320px;font-size:80px;color:{LIME};font-weight:800;opacity:0}}
.sbh{{position:absolute;left:0;width:1920px;top:56px;text-align:center}}
.sbh .sm{{font-size:40px;opacity:0}} .sbh .bg2{{font-size:100px;margin-top:6px;opacity:0}}
.stp{{position:absolute;border-radius:26px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.55);border:2px solid rgba(255,255,255,.18);background:#000}}
.stp video.sv{{position:absolute;object-fit:cover;max-width:none}}
.stl{{position:absolute;width:280px;text-align:center}}
.stl span{{display:inline-block;background:{LIME};color:#0d1020;font-weight:800;font-size:34px;padding:2px 26px 4px;border-radius:999px}}
.stl em{{display:block;margin-top:10px;font-style:normal;font-weight:600;font-size:28px;color:#aab3d6;letter-spacing:2px}}
.lj{{position:absolute;left:0;width:1920px;top:210px;text-align:center;font-weight:800;font-size:40px;color:{LIME};letter-spacing:4px}}
.num{{position:absolute;z-index:90;text-align:center;font-weight:800;font-size:190px;color:#fff;letter-spacing:-4px;text-shadow:0 0 30px rgba(255,255,255,.6),0 7px 0 rgba(0,0,0,.5)}}
.num small{{display:block;font-size:40px;color:{LIME};letter-spacing:6px;margin-bottom:-30px;text-shadow:0 4px 0 rgba(0,0,0,.6)}}
.chip{{display:inline-block;margin:0 14px;background:{LIME};color:#0d1020;font-weight:800;font-size:48px;padding:6px 34px 10px;border-radius:999px;opacity:0}} .chip i{{font-style:normal}}


.abs{{position:absolute}}
.clnode{{display:flex;align-items:center;gap:14px;height:110px;padding:0 34px;border-radius:30px;background:{LIME};color:#0d1020;font-weight:800;font-size:50px;box-shadow:0 0 40px rgba(255,255,0,.45)}} .clnode span{{font-size:58px}}
.srow{{position:absolute;left:36px;width:398px;height:96px;border-radius:22px;background:#222a5a;color:#fff;font-weight:700;font-size:44px;display:flex;align-items:center;gap:20px;padding:0 26px;opacity:0}} .srow b{{color:#25d366;font-size:52px}}
.th{{position:absolute;width:130px;height:78px;border-radius:14px;color:#fff;font-size:30px;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 26px rgba(0,0,0,.45);opacity:0}}
.bar{{position:absolute;left:36px;top:196px;width:688px;height:14px;border-radius:7px;background:#0f1330;overflow:hidden}} .bar i{{display:block;height:100%;width:100%;transform-origin:0 50%;transform:scaleX(0)}}
.itl2{{position:absolute;left:0;width:1920px;top:60px;text-align:center;font-weight:800;font-size:92px;color:#fff;letter-spacing:-2px;text-shadow:0 0 .06em rgba(255,255,255,.9),0 0 .25em rgba(255,255,255,.45)}} .itl2 span,.gct,.gct2,.sbh2{{text-shadow:0 0 .06em rgba(255,255,0,.9),0 0 .25em rgba(255,255,0,.5)}}
.gcard{{position:absolute;background:#171c3d;border:2px solid rgba(255,255,255,.2);border-radius:30px;opacity:1}}
.gct{{position:absolute;left:0;width:100%;top:26px;text-align:center;font-weight:800;font-size:46px;color:{LIME}}}
.gct2{{text-align:center;font-weight:800;font-size:66px}}
.arrow{{font-weight:800;font-size:110px;color:{LIME}}}
.pill2{{display:inline-block;background:{LIME};color:#0d1020;font-weight:800;font-size:44px;padding:4px 30px 8px;border-radius:999px}}
.rowt{{font-weight:800;font-size:72px;color:#fff}}
.shot{{border-radius:28px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.55);border:2px solid rgba(255,255,255,.2)}}
.ring2{{border-radius:30px;border:6px solid {LIME};box-shadow:0 0 28px {LIME}}}
.spc2{{position:absolute;left:60px;top:90px;width:840px;height:900px;border-radius:30px;background:#141833;border:2px solid rgba(255,255,255,.22)}}
.spl2{{position:absolute;left:0;width:100%;top:30px;text-align:center;font-weight:800;font-size:56px;opacity:0}}
.sprow{{color:#fff;position:absolute;left:40px;width:760px;height:230px;border-radius:24px;background:#222a5a;padding:30px 36px;opacity:0}}
.sprow b{{display:block;font-size:48px;font-weight:800}} .sprow span{{display:block;margin-top:10px;font-size:40px;white-space:nowrap;font-weight:700;line-height:1.1}} .sprow u{{text-decoration:none;color:{LIME}}}
.spflow{{position:absolute;left:30px;width:780px;top:700px;display:flex;align-items:center;justify-content:center;gap:12px;opacity:0}}
.spflow i{{font-style:normal;background:#2a3060;color:#fff;font-weight:800;font-size:40px;padding:10px 24px 14px;border-radius:999px}} .spflow em{{font-style:normal;color:{LIME};font-weight:800;font-size:44px}}

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
SFX = [[round(t - SH, 3), k, d] for t, k, d in SFX if t >= SH - 1e-6]


html = f'''<!doctype html>
<html lang="ms" data-resolution="landscape"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{NDUR}" data-width="1920" data-height="1080">
<div id="cam">
<video id="base" class="clip" src="assets/main.mp4" muted playsinline data-start="0" data-duration="{DUR}" data-media-start="0" data-track-index="1"></video>
<div id="wback">{''.join(HTML_WORLD)}</div>
<video id="pmat" class="clip" src="assets/person.webm" muted playsinline data-start="0" data-duration="{DUR}" data-media-start="0" data-track-index="2"></video>
</div>
{''.join(HTML_SCREEN)}
{''.join(CAPS)}
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{NDUR}" data-track-index="50" data-volume="1"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{paused:true}});
const CAM = {json.dumps(CAM, separators=(',', ':'))};
gsap.set('#cam',{{transformOrigin:'0 0',x:CAM[0][0],y:CAM[0][1],scale:CAM[0][2]}});
for(let i=1;i<CAM.length;i++){{const a=CAM[i-1],b=CAM[i];if(a[0]===b[0]&&a[1]===b[1]&&a[2]===b[2])continue;tl.fromTo('#cam',{{x:a[0],y:a[1],scale:a[2]}},{{x:b[0],y:b[1],scale:b[2],duration:1/30,ease:'none',immediateRender:false}},(i-1)/30);}}
{JS_ALL}
window.__timelines["main"] = tl;
</script></body></html>'''
open('hf/index.html', 'w').write(html)
json.dump({'dur': NDUR, 'sfx': sorted(SFX), 'hd': HD, 'sh': 0.0, 'hook_hit': 1.0}, open('build/sfx_events.json', 'w'))
print('html', len(html), 'sfx events', len(SFX), 'dur', NDUR)
