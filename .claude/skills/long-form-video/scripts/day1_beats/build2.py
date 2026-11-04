#!/usr/bin/env python3
"""Long-Form Video, Day 1 vlog build (worked example). Writes hf/index.html + build/sfx_events.json (16:9, 30 fps).
Everything is anchored on spoken words (wt) so a re-cut only needs words_out.json refreshed."""
import json, math, re, random
import numpy as np
W, H = 1920, 1080
tm = json.load(open('build/timemap.json')); DUR = round(tm['dur'], 3)
WORDS = json.load(open('build/words_out.json'))       # [text, snapped_t, whisper_a, whisper_b]
SEGS = [s for s in json.load(open('build/words_cut.json'))]
Y, WH, NAVY = '#FFFF00', '#FFFFFF', '#0F1224'
RED, GRN = '#FF4D4D', '#35E08A'

# ------------------------------------------------------------------ helpers
def norm(t): return re.sub(r'[^a-z0-9%]', '', t.lower())
def wt(word, after=0.0, nth=0):
    """snapped start time of the first spoken token starting with `word` (a|b alternatives) at/after `after`"""
    alts = [norm(a) for a in word.split('|')]; c = 0
    for t, sn, a, b in WORDS:
        if sn >= after - 1e-6 and any(norm(t).startswith(x) for x in alts):
            if c == nth: return sn
            c += 1
    raise KeyError(f'{word} after {after}')
def wend(word, after=0.0):
    alts = [norm(a) for a in word.split('|')]
    for t, sn, a, b in WORDS:
        if sn >= after - 1e-6 and any(norm(t).startswith(x) for x in alts): return min(b, sn + 0.9)
    raise KeyError(word)
JS = []; SFX = []
def js(s): JS.append(s)
def sfx(t, kind, db=-20): SFX.append([round(float(t), 3), kind, db])
def fj(d): return json.dumps(d, separators=(',', ':'))
INIT = []; INIT_SEEN = set()
def A(sel, f, to, t, d=.4, ease='power3.out'):       # fromTo
    if f.get('opacity') == 0 and sel not in INIT_SEEN:
        INIT_SEEN.add(sel); INIT.append(f'gsap.set("{sel}",{fj(f)});')
    js(f'tl.fromTo("{sel}",{fj(f)},{fj({**to, "duration": d, "ease": ease, "immediateRender": False})},{t:.3f});')
def T(sel, to, t, d=.4, ease='power2.out'):          # to
    js(f'tl.to("{sel}",{fj({**to, "duration": d, "ease": ease})},{t:.3f});')
def SET(sel, to, t): js(f'tl.set("{sel}",{fj(to)},{t:.3f});')
def counter(sel, t0, d, end, n=14, start=0, fmt='{}'):
    for i in range(1, n + 1):
        u = i / n; v = round(start + (end - start) * (1 - (1 - u) ** 2))
        js(f'tl.set("{sel}",{{textContent:{json.dumps(fmt.format(v))}}},{t0 + d * u:.3f});')
def shake(sel, t, amp=14, n=5):
    for i in range(n):
        s = (-1) ** i * amp * (1 - i / n)
        js(f'tl.set("{sel}",{{x:{s:.1f}}},{t + i * .04:.3f});')
    js(f'tl.set("{sel}",{{x:0}},{t + n * .04:.3f});')

# ------------------------------------------------------------------ scenes registry
SCENES = []    # (t0, t1, kind) kind: full | split
OV = []        # overlay html
def scene(sid, t0, t1, kind, bg, body, fade=.3):
    SCENES.append((t0, t1, kind, sid))
    OV.append(f'<div class="ov" id="{sid}" style="background:{bg}">{body}</div>')
    A(f'#{sid}', {'opacity': 0}, {'opacity': 1}, t0, fade, 'power2.out')
    T(f'#{sid}', {'opacity': 0}, t1 - fade, fade, 'power2.in')
    SET(f'#{sid}', {'opacity': 0, 'display': 'none'}, t1 + .02)
    SET(f'#{sid}', {'display': 'block'}, t0 - .01)

BG_PURPLE = 'radial-gradient(1300px 800px at 50% 45%,#4B1D96 0%,#2B0F5C 45%,#140a33 100%)'
BG_NAVY = 'radial-gradient(1300px 760px at 50% 50%,#1b2350,#0F1224 70%)'
BG_SPLIT = 'linear-gradient(90deg,rgba(11,14,28,0) 0px,rgba(11,14,28,0) 930px,rgba(11,14,28,.94) 985px,#0b0e1c 1010px)'

# ------------------------------------------------------------------ battery widget
def bat(p, x, y, w, h, lv=1.0, col=Y):
    segs, gap, pad = 5, 14, 20
    iw = (w - pad * 2 - gap * (segs - 1)) / segs
    s = (f'<div class="bt" id="{p}" style="left:{x}px;top:{y}px;width:{w + 40}px;height:{h}px">'
         f'<div class="btb" id="{p}o" style="width:{w}px;height:{h}px;border-radius:{h * .16:.0f}px;border-width:{h * .035:.1f}px"></div>'
         f'<div class="btn" style="left:{w + 6}px;top:{h * .32:.0f}px;height:{h * .36:.0f}px"></div>')
    for i in range(segs):
        s += (f'<div class="btc" id="{p}c{i}" style="left:{pad + i * (iw + gap):.1f}px;top:{pad}px;width:{iw:.1f}px;height:{h - pad * 2}px;'
              f'border-radius:{h * .08:.0f}px"></div>'); js(f'gsap.set("#{p}c{i}",{{scaleX:{max(0, min(1, lv * segs - i)):.3f}}});')
    s += f'<div class="btt" id="{p}n" style="width:{w}px;height:{h}px;line-height:{h}px;font-size:{h * .55:.0f}px">{round(lv * 100)}%</div></div>'
    return s
def drain(p, a, b, t0, d, ease='none', numsteps=10, recolor=True):
    """animate battery p from level a to b over d seconds, cell by cell"""
    if abs(a - b) < 1e-6: return
    lo_, hi_ = min(a, b), max(a, b)
    for i in range(5):
        lo = max(lo_, i / 5); hi = min(hi_, (i + 1) / 5)
        if lo >= hi: continue
        frac = (a - hi) / (a - b) if b < a else (lo - a) / (b - a)
        frac2 = (a - lo) / (a - b) if b < a else (hi - a) / (b - a)
        ts = t0 + d * frac; td = d * (frac2 - frac)
        s0 = max(0, min(1, a * 5 - i)); s1 = max(0, min(1, b * 5 - i))
        A(f'#{p}c{i}', {'scaleX': s0}, {'scaleX': s1}, ts, td, 'none')
    for k in range(1, numsteps + 1):
        u = k / numsteps; v = a + (b - a) * u; tt = t0 + d * u
        pc = round(v * 100)
        st = {'textContent': f'{pc}%', 'color': (NAVY if v >= .5 else '#fff')}
        if recolor: st['color'] = NAVY if v >= .5 else '#fff'
        SET(f'#{p}n', st, tt)
def recolor_cells(p, col, t, d=.3):
    for i in range(5):
        T(f'#{p}c{i}', {'backgroundColor': col, 'boxShadow': f'0 0 36px {col}aa'}, t, d)
    T(f'#{p}o', {'boxShadow': f'0 0 60px {col}77,inset 0 0 50px rgba(255,255,255,.06)'}, t, d)

# ------------------------------------------------------------------ captions
CAPSPEC = []; CAPS = []; cap_n = [0]
FAM = ['pop', 'click', 'tink', 'blip', 'key', 'ping', 'chirp']; fam_i = [0]; last_kind = ['']
def next_fam():
    for _ in range(8):
        k = FAM[fam_i[0] % len(FAM)]; fam_i[0] += 1
        if k != last_kind[0]: last_kind[0] = k; return k
    return 'pop'
def grp(small, items, t0, hold=1.5, y=820, fs=104, pos='bc'):
    """items: [(TEXT,'y'|'w', token or None)]  token -> spoken anchor (searched from t0-.35)"""
    ts = []
    for i, (txt, c, tok) in enumerate(items):
        ts.append(wt(tok, t0 - .35) if tok else (ts[-1] + .14 if ts else t0))
    CAPSPEC.append(dict(t0=min(t0, ts[0]), t1=ts[-1] + hold, small=small, items=items, ts=ts, y=y, fs=fs, pos=pos))
POS = {'bc': 'left:0;width:1920px;top:{y}px;text-align:center;', 'bl': 'left:70px;width:880px;top:{y}px;text-align:left;',
       'br': 'right:110px;top:{y}px;text-align:right;', 'tc': 'left:0;width:1920px;top:{y}px;text-align:center;'}
def emit_caps():
    S_ = sorted(CAPSPEC, key=lambda c: c['t0'])
    # drop captions that sit inside a full-screen scene, move to the left half inside a split scene
    keep = []
    for c in S_:
        inside = [s for s in SCENES if s[0] - .05 <= c['ts'][0] <= s[1]]
        if inside and inside[0][2] in ('full', 'bh'): continue
        if inside and inside[0][2] == 'split': c['pos'] = 'bl'; c['fs'] = min(c['fs'], 84)
        keep.append(c)
    for c in keep:
        for s in SCENES:
            if s[2] in ('full', 'bh') and c['t0'] < s[1] <= c['ts'][0] + .3: c['t0'] = s[1]
    for i, c in enumerate(keep):
        for d in keep[i + 1:]:
            if d['t0'] >= c['t1'] + .2: break
            c['t1'] = max(c['t0'] + .35, d['t0'] - .12); c['fade'] = .08; break
        # never run into a full-screen scene
        for s in SCENES:
            if s[2] in ('full', 'bh') and c['t0'] < s[0] < c['t1']: c['t1'] = max(c['t0'] + .35, s[0] - .05); c['fade'] = .08
    for c in keep: emit_cap(c)
def emit_cap(c):
    n = cap_n[0]; cap_n[0] += 1; cid = f'c{n}'; fade = c.get('fade', .16)
    sm = f'<div class="sm" id="{cid}s">{c["small"]}</div>' if c['small'] else ''
    bw = ''.join(f'<span class="bw {col if col in ("y", "r") else "w"}" id="{cid}w{j}">{txt}</span> ' for j, (txt, col, tok) in enumerate(c['items']))
    CAPS.append(f'<div class="cap" id="{cid}" style="{POS[c["pos"]].format(y=c["y"])}font-size:{c["fs"]}px">{sm}<div class="bg2">{bw}</div></div>')
    t0, t1 = c['t0'], c['t1']
    SET(f'#{cid}', {'opacity': 1}, t0)
    if c['small']: A(f'#{cid}s', {'opacity': 0, 'y': 16, 'filter': 'blur(8px)'}, {'opacity': 1, 'y': 0, 'filter': 'blur(0px)'}, t0, .2)
    for j, tj in enumerate(c['ts']):
        A(f'#{cid}w{j}', {'opacity': 0, 'scale': .72, 'y': 18, 'filter': 'blur(10px)'}, {'opacity': 1, 'scale': 1, 'y': 0, 'filter': 'blur(0px)'}, tj, .17, 'back.out(1.8)')
    T(f'#{cid}', {'opacity': 0, 'filter': 'blur(6px)', 'y': -10}, t1, fade, 'power2.in')
    SET(f'#{cid}', {'opacity': 0}, t1 + fade + .01)
    sfx(c['ts'][0], next_fam(), -23)

# ================================================================== STORY ANCHORS (V2)
HD = tm['hook_dur']
# ---- hook words (inside the cold open)
h_sampai = wt('sampai', 0); h_hari = wt('hari', h_sampai); h_alasan = wt('alasan', h_hari); h_mc = wt('mc', h_alasan)
h_satu = wt('satu', h_mc); h_15 = wt('15|lima belas', h_satu); h_minit = wt('minit', h_15)
# ---- compare
t_cuba = wt('cuba', HD); t_seb1 = wt('sebelah', t_cuba); t_seb2 = wt('sebelah', t_seb1 + .4); t_so_k = wt('so', t_seb2)
# ---- usage / token explainer
t_kredit = wt('kredit', HD); t_token = wt('token', t_kredit); t_adv = wt('advance', t_token); t_mesti = wt('mesti', t_adv)
t_usage = wt('usage', t_mesti); t_sama = wt('sama', t_usage); t_100 = wt('100|seratus', t_sama); t_konsep2 = wt('konsep', t_100)
t_bateri = wt('bateri', t_konsep2)
# ---- battery hero + tasks -----------------------------------------------------------
t_so_task = wt('so', t_bateri + .3); t_kompl = wt('kompleksiti', t_so_task)
t_mudah = wt('mudah', t_kompl); t_potong = wt('potongkan', t_mudah); t_sikit1 = wt('sikit', t_potong)
t_anim = wt('animation', t_sikit1); t_text = wt('text', t_anim); t_broll = wt('b', t_text)
t_efek = wt('efek', t_broll); t_banyak = wt('banyak', t_efek)
# ---- three sizes ---------------------------------------------------------------------
t_avg = wt('average', t_banyak); t_export = wt('export', t_avg); t_3 = wt('3|tiga', t_export)
t_916 = wt('9|sembilan', t_3); t_169 = wt('16|enam belas', wt('16|enam belas', t_916 + .1) + .1); t_11 = wt('1|satu', t_169 + .1)
t_pecah = wt('pecahkan', t_11); t_15 = wt('15|lima belas', t_pecah); t_ketiga = wt('ketiga', t_15)
t_depends = wt('depends', t_ketiga); t_kompl2 = wt('kompleksiti', t_depends)
# ---- refill --------------------------------------------------------------------------
t_apa = wt('apa', t_kompl2); t_habis1 = wt('habis', t_apa); t_habis2 = wt('habis', t_habis1 + .2)
t_jangan = wt('jangan', t_habis2); t_top = wt('top', t_jangan); t_selepas = wt('selepas', t_top)
t_5jam = wt('5|lima', t_selepas); t_after = wt('after', t_5jam); t_100b = wt('100|seratus', t_after); t_senang = wt('senang', t_100b)
# ---- modes ---------------------------------------------------------------------------
t_mode = wt('mode', t_senang); t_harian = wt('harian', t_mode); t_weekly = wt('weekly', t_harian)
t_weekly100 = wt('100|seratus', t_weekly); t_kamis = wt('kamis', t_weekly100); t_tbg = wt('boleh', t_kamis)
t_weekly_habis = wt('habis', t_tbg)
# ---- price ---------------------------------------------------------------------------
t_package = wt('package', t_weekly_habis); t_20 = wt('rm20|20|dua puluh', t_package); t_usd = t_20 + .6
t_90 = wt('rm90|90', t_20 + .3); t_ringgit = wt('rm100|100', t_90); t_berbaloi = wt('berbaloi', t_ringgit)
# ---- team vs ai ----------------------------------------------------------------------
t_dulu = wt('dulu', wt('persoalan', t_berbaloi)); t_team = wt('team|tim', t_dulu); t_jam1 = wt('jam', t_team)
t_heavy = wt('heavy', t_jam1); t_3jam = wt('3|tiga', t_heavy); t_hari34 = wt('hari', t_3jam + .3)
t_dengan = wt('dengan', t_hari34); t_mc = wt('mc', t_dengan); t_1520 = wt('15|lima belas', t_mc); t_minit = wt('minit', t_1520)
t_sebulan = wt('sebulan', t_minit); t_100v = wt('100|seratus', t_sebulan); t_video100 = wt('video', t_100v)
t_daily = wt('daily', t_video100); t_berbaloi2 = wt('berbaloi', t_daily)
# ---- benchmark -----------------------------------------------------------------------
t_kompet = wt('kompetensi', t_berbaloi2); t_bench = wt('benchmark', t_kompet); t_dulu2 = wt('dulu', t_bench)
t_prem = wt('premiere', t_dulu2); t_after2 = wt('after', t_prem); t_capcut = wt('capcut', t_after2)
t_adapt = wt('adapt', t_capcut); t_ai = wt('ai', t_adapt); t_laju = wt('laju', t_ai)
# ---- adapt ---------------------------------------------------------------------------
t_geng = wt('geng', t_laju); t_adapt2 = wt('adapt', t_geng); t_auto = wt('automat', t_adapt2)
t_story = wt('story', t_auto); t_conv = wt('conversion', t_story); t_sendiri = wt('sendiri', t_conv)
# ---- outro (new order: pertama -> aku personally nak try -> ... -> konsisten -> anything jumpa esok)
t_episode = wt('episod', t_sendiri); t_pertama = wt('pertama', t_episode)
t_aku = wt('aku', t_pertama); t_try = wt('try', t_aku); t_vlog = wt('vlog', t_try)
t_rekod = wt('rekod', t_vlog); t_konsis = wt('konsis|consis', t_rekod); t_anything = wt('anything', t_konsis)
t_esok = wt('esok', t_anything); t_kedua = wt('kedua', t_esok)

def vclip(sid, src, t0, dur, style):
    return f'<video class="clip pv" id="{sid}" src="{src}" muted playsinline data-start="{t0:.3f}" data-duration="{dur:.3f}" data-media-start="0" data-track-index="{VT[0]}" style="{style}"></video>'
VT = [3]
def vt():
    VT[0] += 1; return VT[0]

# ================================================================== V2 NEW SCENES ====================================
WB = []; PM = []; BHI = []
BWF = 'grayscale(1) brightness(.55) contrast(1.1)'
def fg_fade(sid, t0, t1, fade=.35):
    A(f'#{sid}', {'opacity': 0}, {'opacity': 1}, t0, fade, 'power2.out'); T(f'#{sid}', {'opacity': 0}, t1 - fade, fade, 'power2.in')
    SET(f'#{sid}', {'opacity': 0, 'display': 'none'}, t1 + .02); SET(f'#{sid}', {'display': 'block'}, t0 - .01)
def bhscene(sid, t0, t1, els, fg, bw=False, fade=.35):
    """presenter stays full screen: elements sit BEHIND the cut-out, text sits in front"""
    SCENES.append((t0, t1, 'bh', sid)); BHI.append((sid, round(t0, 3), round(t1, 3)))
    WB.append(f'<div class="bhs" id="{sid}_w">{els}</div>')
    OV.append(f'<div class="ov bhov" id="{sid}">{fg}</div>')
    PM.append(f'<video class="clip pm{" pmglow" if bw else ""}" id="pm_{sid}" src="assets/matte/{sid}.webm" muted playsinline data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" data-media-start="0" data-track-index="2"></video>')
    A(f'#{sid}_w', {'opacity': 0}, {'opacity': 1}, t0, fade, 'power2.out'); T(f'#{sid}_w', {'opacity': 0}, t1 - fade, fade, 'power2.in')
    SET(f'#{sid}_w', {'opacity': 0, 'display': 'none'}, t1 + .02); SET(f'#{sid}_w', {'display': 'block'}, t0 - .01)
    fg_fade(sid, t0, t1, fade)
    if bw:
        T('#base', {'filter': BWF}, t0, .45, 'power2.out'); T('#base', {'filter': 'grayscale(0) brightness(1) contrast(1)'}, t1 - .45, .45, 'power2.in')

def card_html(i, n, x, y, rot, col='#f4f1ea'):
    return (f'<div class="abs" id="{{p}}cal{i}" style="left:{x}px;top:{y}px;width:280px;height:330px;border-radius:22px;background:{col};border:3px solid #cfc9bb;'
            f'box-shadow:0 18px 40px rgba(0,0,0,.45);transform:rotate({rot}deg)"><div style="height:76px;background:{RED};border-radius:19px 19px 0 0"></div>'
            f'<div style="font-size:110px;font-weight:800;color:#222;text-align:center;line-height:1.4">{n}</div></div>')

# ---------------------------------------------------------------- HOOK (cold open climax clip) ----------------------------
SCENES.append((0, HD, 'hook', 's_hook'))
hk = ''
for i in range(5):
    hk += card_html(i, [1, 2, 3, 4, 4][i], 1440 + i * 28, 70 + i * 20, -6 + i * 3).replace('{p}', 'hk')
hk += (f'<div class="abs" id="hkmc" style="left:1360px;top:70px;width:420px;height:300px;border-radius:18px;background:#fff;box-shadow:0 20px 50px rgba(0,0,0,.5);transform:rotate(-7deg)">'
       f'<div style="margin:26px 30px;font-weight:800;font-size:30px;color:#333">SIJIL CUTI SAKIT</div><div style="margin:0 30px;height:14px;background:#ddd;border-radius:7px"></div>'
       f'<div style="margin:14px 30px;height:14px;width:60%;background:#ddd;border-radius:7px"></div><div style="margin:14px 30px;height:14px;width:75%;background:#ddd;border-radius:7px"></div></div>'
       f'<div class="abs" id="hkx1" style="left:1340px;top:150px;width:460px;height:14px;background:{RED};transform:rotate(-24deg);transform-origin:0 50%;box-shadow:0 0 30px {RED}"></div>'
       f'<div class="abs" id="hkx2" style="left:1340px;top:80px;width:460px;height:14px;background:{RED};transform:rotate(24deg);transform-origin:0 50%;box-shadow:0 0 30px {RED}"></div>'
       f'<svg class="abs" id="hksw" style="left:1450px;top:70px" width="300" height="300" viewBox="0 0 300 300"><circle cx="150" cy="150" r="120" fill="rgba(15,18,36,.7)" stroke="rgba(255,255,255,.3)" stroke-width="18"/>'
       f'<circle id="hkarc" cx="150" cy="150" r="120" fill="none" stroke="{Y}" stroke-width="18" stroke-linecap="round" stroke-dasharray="754" stroke-dashoffset="754" transform="rotate(-90 150 150)" style="filter:drop-shadow(0 0 14px {Y})"/>'
       f'<line id="hkhand" x1="150" y1="150" x2="150" y2="70" stroke="#fff" stroke-width="10" stroke-linecap="round" style="transform-origin:150px 150px"/><rect x="130" y="14" width="40" height="22" rx="6" fill="#fff"/></svg>'
       f'<div class="abs" id="hkwipe" style="left:-300px;top:0;width:300px;height:1080px;background:{Y};opacity:0;transform:skewX(-14deg)"></div>')
OV.append(f'<div class="ov" id="s_hook" style="background:transparent;display:block;opacity:1">{hk}</div>')
SET('#s_hook', {'display': 'none'}, HD + .05)
# calendar flip (3-4 hari)
for i in range(5):
    A(f'#hkcal{i}', {'opacity': 0, 'rotationX': -80, 'y': -60}, {'opacity': 1, 'rotationX': 0, 'y': 0}, h_sampai - .1 + i * .13, .28, 'back.out(1.6)')
    sfx(h_sampai - .1 + i * .13, 'key', -21)
T('#hkcal0,#hkcal1,#hkcal2,#hkcal3,#hkcal4', {'opacity': 0, 'y': -40}, h_alasan - .5, .25, 'power2.in')
# MC card struck out
A('#hkmc', {'opacity': 0, 'scale': .6, 'rotation': -20}, {'opacity': 1, 'scale': 1, 'rotation': -7}, h_alasan - .2, .3, 'back.out(1.7)')
A('#hkx1', {'opacity': 0, 'scaleX': 0}, {'opacity': 1, 'scaleX': 1}, h_mc, .16, 'power3.out'); A('#hkx2', {'opacity': 0, 'scaleX': 0}, {'opacity': 1, 'scaleX': 1}, h_mc + .12, .16, 'power3.out')
sfx(h_mc, 'stamp', -16); sfx(h_mc + .12, 'stamp', -18)
T('#hkmc,#hkx1,#hkx2', {'opacity': 0, 'y': -40}, h_satu - .05, .22, 'power2.in')
# stopwatch 15-20 minit
A('#hksw', {'opacity': 0, 'scale': .4}, {'opacity': 1, 'scale': 1}, h_satu, .3, 'back.out(1.8)')
A('#hkarc', {'strokeDashoffset': 754}, {'strokeDashoffset': 200}, h_15 - .1, .5, 'power2.out'); A('#hkhand', {'rotation': 0, 'svgOrigin': '150 150'}, {'rotation': 270, 'svgOrigin': '150 150'}, h_15 - .1, .5, 'power2.out')
sfx(h_15 - .35, 'riser', -14); sfx(h_15 - .1, 'boom', -10); sfx(h_15, 'shing', -14)
# whip transition into the main video
A('#hkwipe', {'opacity': 1, 'x': 0}, {'opacity': 1, 'x': 2300, 'duration': .32, 'ease': 'power2.inOut', 'immediateRender': False}, HD - .3, .32)
SET('#hkwipe', {'opacity': 0}, HD + .05)
sfx(HD - .32, 'slide', -13); sfx(HD - .1, 'shutter', -15)
grp('ada yang sampai', [('3–4 HARI', 'r', None)], h_sampai - .15, 1.6, y=800, fs=130, pos='bl')
grp('dengan Claude, dia tak ada alasan', [('TAK ADA', 'y', 'alasan'), ('MC', 'w', 'mc')], h_alasan - .2, 1.3, y=790, fs=130, pos='bc')
grp('satu video siap dalam', [('15–20 MINIT', 'y', '15')], h_satu - .1, .9, y=790, fs=170, pos='bc')

# ---------------------------------------------------------------- COMPARE (stage, real assets) ---------------------------
tc0 = t_seb1 - 1.0; tc1 = t_so_k - .05
b = f'<div class="abs" style="left:0;width:1920px;top:50px;text-align:center"><div class="sm" id="cp_s">cuba tengok dua perbezaan ni</div></div>'
b += f'<div class="abs" id="cp_a" style="left:110px;top:200px;width:830px;height:467px;border-radius:26px;overflow:hidden;border:3px solid rgba(255,255,255,.35);box-shadow:0 40px 90px rgba(0,0,0,.6);transform:perspective(1800px) rotateY(9deg) rotate(-1.5deg)">' + vclip('cpv_a', 'assets/panels/p_gpt.mp4', tc0, tc1 - tc0, 'left:0;top:0;width:830px;height:467px;object-fit:cover') + '</div>'
b += f'<div class="abs" id="cp_b" style="left:980px;top:200px;width:830px;height:467px;border-radius:26px;overflow:hidden;border:3px solid {Y};box-shadow:0 40px 90px rgba(0,0,0,.6),0 0 60px rgba(255,255,0,.35);transform:perspective(1800px) rotateY(-9deg) rotate(1.5deg)">' + vclip('cpv_b', 'assets/panels/p_claude.mp4', tc0, tc1 - tc0, 'left:0;top:0;width:830px;height:467px;object-fit:cover') + '</div>'
VT[0] += 2
b += f'<div class="abs" id="cp_la" style="left:110px;width:830px;top:710px;text-align:center"><span class="pill" style="font-size:44px">CONTOH CHATGPT</span></div><div class="abs" id="cp_lb" style="left:980px;width:830px;top:710px;text-align:center"><span class="pill" style="font-size:44px">CONTOH CLAUDE</span></div>'
b += f'<div class="abs" id="cp_vs" style="left:900px;top:380px;width:120px;height:120px;border-radius:50%;background:{NAVY};border:5px solid {Y};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:46px;color:{Y};box-shadow:0 0 40px {Y}88">VS</div>'
scene('s_cmp', tc0, tc1, 'full', BG_PURPLE, b)
A('#cp_s', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, tc0 + .2, .3)
A('#cp_a,#cp_la', {'opacity': 0, 'x': -140}, {'opacity': 1, 'x': 0}, t_seb1 - .15, .45, 'power3.out'); sfx(t_seb1 - .15, 'slide', -14)
A('#cp_b,#cp_lb', {'opacity': 0, 'x': 140}, {'opacity': 1, 'x': 0}, t_seb2 - .15, .45, 'power3.out'); sfx(t_seb2 - .15, 'slide', -14)
A('#cp_vs', {'opacity': 0, 'scale': .3}, {'opacity': 1, 'scale': 1}, t_seb2 + .1, .35, 'back.out(2.4)'); sfx(t_seb2 + .1, 'boom', -14)

# ---------------------------------------------------------------- USAGE (stage) -----------------------------------------
tu0 = t_kredit - .6; tu1 = t_konsep2 - .2
b = f'<div class="abs" style="left:0;width:1920px;top:40px;text-align:center"><div class="sm" id="u_s">software AI yang buat benda advance</div></div>'
b += f'<div class="abs" style="left:0;width:1920px;top:100px;text-align:center"><div class="bg2" style="font-size:96px"><span class="y" id="u_k" style="display:inline-block">KREDIT</span> <span class="y" id="u_t" style="display:inline-block"><span class="w">·</span> TOKEN</span> <span class="y" id="u_u" style="display:inline-block"><span class="w">·</span> USAGE</span></div></div>'
b += f'<svg class="abs" id="u_g" style="left:620px;top:300px" width="680" height="400" viewBox="0 0 680 400"><path d="M40 360 A300 300 0 0 1 640 360" fill="none" stroke="rgba(255,255,255,.2)" stroke-width="44" stroke-linecap="round"/><path id="u_arc" d="M40 360 A300 300 0 0 1 640 360" fill="none" stroke="{Y}" stroke-width="44" stroke-linecap="round" stroke-dasharray="942" stroke-dashoffset="942" style="filter:drop-shadow(0 0 20px {Y})"/></svg>'
b += f'<div class="abs" id="u_nd" style="left:954px;top:480px;width:12px;height:230px;background:#fff;border-radius:6px;transform-origin:50% 100%;transform:rotate(-90deg)"></div><div class="abs" id="u_pv" style="left:934px;top:690px;width:52px;height:52px;border-radius:50%;background:#fff;box-shadow:0 0 30px #fff"></div>'
b += f'<div class="lab abs" id="u_gl" style="left:620px;width:680px;top:760px;text-align:center;font-size:54px;letter-spacing:6px">USAGE</div>'
b += f'<div class="abs" id="u_adv" style="left:40px;width:560px;top:520px;text-align:center"><div class="num" style="position:relative;font-size:54px">BENDA ADVANCE</div></div>'
b += f'<div class="abs" id="u_need" style="left:1290px;width:560px;top:520px;text-align:center"><div class="bg2 y" style="font-size:50px">KENA ADA USAGE</div></div>'
b += f'<div class="abs" id="u_c1" style="left:240px;top:330px">{{coin}}</div><div class="abs" id="u_c2" style="left:1480px;top:330px">{{coin}}</div>'.replace('{coin}', f'<div style="width:110px;height:110px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff7a0,{Y} 55%,#c9b800);box-shadow:0 0 40px {Y}88;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:50px;color:{NAVY}">$</div>')
b += f'<div class="glass abs" id="u_pa" style="left:200px;top:850px;width:640px;height:170px"></div><div class="glass abs" id="u_pb" style="left:1080px;top:850px;width:640px;height:170px"></div>'
b += f'<div class="num abs" id="u_ta" style="left:200px;width:640px;top:880px;text-align:center;font-size:70px">CLAUDE</div><div class="num abs" id="u_tb" style="left:1080px;width:640px;top:880px;text-align:center;font-size:70px">CHATGPT</div><div class="abs" id="u_eq" style="left:850px;top:830px;width:220px;text-align:center;font-weight:800;font-size:150px;color:{Y};text-shadow:0 0 30px {Y}">=</div>'
b += f'<div class="abs" id="u_100" style="left:0;width:1920px;top:850px;text-align:center"><div class="num" style="position:relative;font-size:150px;line-height:1">100%</div><div class="lab" style="position:relative;font-size:34px;letter-spacing:6px;margin-top:6px">MODE CODE · CODEX</div></div>'
scene('s_us', tu0, tu1, 'full', BG_PURPLE, b)
A('#u_s', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, tu0 + .3, .3)
for sel, tt in [('#u_k', t_kredit), ('#u_t', t_token)]:
    A(sel, {'opacity': 0, 'scale': .5, 'y': 20}, {'opacity': 1, 'scale': 1, 'y': 0}, tt - .1, .3, 'back.out(2.2)')
sfx(t_kredit - .1, 'click', -14); sfx(t_token - .1, 'ting', -14)
A('#u_c1', {'opacity': 0, 'y': -150, 'rotation': -90}, {'opacity': 1, 'y': 0, 'rotation': 0}, t_kredit - .1, .5, 'bounce.out'); A('#u_c2', {'opacity': 0, 'y': -150, 'rotation': 90}, {'opacity': 1, 'y': 0, 'rotation': 0}, t_token - .1, .5, 'bounce.out')
A('#u_g,#u_gl,#u_nd,#u_pv', {'opacity': 0}, {'opacity': 1}, t_token + .2, .4)
A('#u_adv', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, t_adv - .15, .3)
A('#u_need', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, t_mesti - .1, .3, 'back.out(2.2)'); sfx(t_mesti - .1, 'stamp', -13)
A('#u_u', {'opacity': 0, 'scale': .5, 'y': 20}, {'opacity': 1, 'scale': 1, 'y': 0}, t_usage - .1, .3, 'back.out(2.2)'); sfx(t_usage - .1, 'pop', -14)
A('#u_arc', {'opacity': 0}, {'opacity': 1}, t_mesti - .05, .1); A('#u_arc', {'strokeDashoffset': 942}, {'strokeDashoffset': 400}, t_mesti, .8, 'power2.out'); A('#u_nd', {'rotation': -90}, {'rotation': -8, 'duration': .8, 'ease': 'power2.out', 'immediateRender': False}, t_mesti, .8)
T('#u_adv,#u_need', {'opacity': 0}, t_sama - .45, .25)
A('#u_pa,#u_pb,#u_ta,#u_tb,#u_eq', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, t_sama - .35, .35, 'back.out(2)'); sfx(t_sama - .3, 'stamp', -13)
T('#u_pa,#u_pb,#u_ta,#u_tb,#u_eq', {'opacity': 0}, t_100 - .3, .25)
T('#u_gl', {'opacity': 0}, t_100 - .2, .2)
A('#u_100', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, t_100 - .1, .35, 'back.out(2)')
A('#u_arc', {'strokeDashoffset': 400}, {'strokeDashoffset': 0, 'duration': .7, 'ease': 'power2.out', 'immediateRender': False}, t_100 - .05, .7); T('#u_nd', {'rotation': 82}, t_100 - .05, .7, 'power2.out')
counter('#u_100 .num', t_100 - .05, .7, 100, 12, fmt='{}%'); sfx(t_100 - .05, 'ratchet', -14); sfx(t_100 + .7, 'ting', -12)

# idle life while the speaker explains (needle wobble + floating coins)
_w0 = t_token + .8; _n = max(2, 2 * int((t_mesti - .3 - _w0) / 1.4))
js(f'tl.to("#u_nd",{{rotation:-70,duration:.7,ease:"sine.inOut",yoyo:true,repeat:{_n - 1}}},{_w0:.3f});')
for _c, _s in (('#u_c1', 1), ('#u_c2', -1)):
    js(f'tl.to("{_c}",{{y:{-16 * _s},duration:1.1,ease:"sine.inOut",yoyo:true,repeat:{max(1, int((t_mesti - t_token) / 1.1))}}},{t_token + .7:.3f});')

# ================================================================== SCENE 3: battery hero + tasks (full) ===============
t3_0 = t_konsep2 - .15
t3_1 = wend('sikit', t_banyak) + 1.2
b = f'<div class="pts" id="pts"></div>'
b += f'<div class="abs" id="h1" style="left:0;width:1920px;top:60px;text-align:center"><div class="sm" id="h1s" style="font-size:50px">konsep dia lebih kurang macam</div><div class="bg2 y" id="h1b" style="font-size:170px">BATERI</div></div>'
b += f'<div class="abs" id="h2" style="left:110px;top:44px;opacity:0"><div class="sm" style="font-size:46px">bateri pakai ikut</div><div class="bg2" style="font-size:112px"><span class="y">KOMPLEKSITI</span> <span class="w">TASK</span></div></div>'
b += f'<div id="batw" class="abs" style="left:0;top:0;width:1920px;height:1080px;transform-origin:0 0"><div id="batsh" class="abs" style="left:0;top:0;width:1920px;height:1080px">' + bat('B1', 480, 360, 860, 420, 1.0) + '</div></div>'
b += f'<div class="lab" id="b1l" style="left:0;width:1920px;top:850px;text-align:center;font-size:44px;letter-spacing:6px">USAGE ANDA</div>'
rows = [('MUDAH', 'SIKIT BATERI', .2, GRN, t_mudah), ('POTONG VIDEO', 'SIKIT', .16, GRN, t_potong), ('ANIMASI', 'BANYAK', .62, RED, t_anim),
        ('TEXT', 'BANYAK', .55, RED, t_text), ('B-ROLL', 'BANYAK', .8, RED, t_broll), ('EFEK TERBANG', 'BANYAK', 1.0, RED, t_efek)]
for i, (lab, tag, wv, col, tt) in enumerate(rows):
    top = 235 + i * 118
    b += (f'<div class="chip" id="r{i}" style="left:900px;top:{top}px;width:900px;height:100px;opacity:0">'
          f'<span style="font-size:34px;letter-spacing:1px;white-space:nowrap">{lab}</span><span style="display:flex;align-items:center;gap:20px">'
          f'<span class="rb" id="r{i}b" style="width:{300 * wv:.0f}px;height:22px;background:{col};box-shadow:0 0 24px {col};transform-origin:0 50%"></span>'
          f'<span style="font-size:26px;font-weight:800;color:{col};width:215px;white-space:nowrap;text-align:right">{tag}</span></span></div>')
scene('s_bat', t3_0, t3_1, 'full', BG_PURPLE, b)
# hero: battery builds on the word 'bateri'
A('#B1o', {'scale': .7, 'opacity': 0, 'filter': 'blur(14px)'}, {'scale': 1, 'opacity': 1, 'filter': 'blur(0px)'}, t3_0 + .15, .5, 'back.out(1.6)')
A('#h1s', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, t3_0 + .2, .3)
A('#h1b', {'opacity': 0, 'scale': .6, 'filter': 'blur(14px)'}, {'opacity': 1, 'scale': 1, 'filter': 'blur(0px)'}, t_bateri - .05, .35, 'back.out(2)')
sfx(t_bateri - .05, 'boom', -19)
for i in range(5):
    A(f'#B1c{i}', {'scaleX': 0}, {'scaleX': 1}, t3_0 + .5 + i * .16, .22, 'power2.out'); sfx(t3_0 + .5 + i * .16, 'pop', -26)
A('#B1n', {'opacity': 0}, {'opacity': 1}, t3_0 + .5, .3)
js(f'tl.set("#B1n",{{textContent:"0%"}},{t3_0 + .49:.3f});')
counter('#B1n', t3_0 + .5, .9, 100, 12, fmt='{}%')
A('#b1l', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, t3_0 + 1.5, .3)
# glow pulse
for k in range(3): T('#B1o', {'boxShadow': '0 0 120px #FFFF0099,inset 0 0 50px rgba(255,255,255,.06)'}, t3_0 + 1.6 + k * .6, .3); T('#B1o', {'boxShadow': '0 0 40px #FFFF0044,inset 0 0 50px rgba(255,255,255,.06)'}, t3_0 + 1.9 + k * .6, .3)
# floating particles
for k in range(7):
    x = 150 + k * 260 + (k % 3) * 40; y0 = 900 - (k * 83) % 500
    js(f'tl.fromTo("#pt{k}",{{opacity:0,y:0}},{{opacity:.6,y:-260,duration:{t3_1 - t3_0:.2f},ease:"none"}},{t3_0:.3f});')
b_pts = ''.join(f'<div class="pt" id="pt{k}" style="left:{150 + k * 260 + (k % 3) * 40}px;top:{900 - (k * 83) % 500}px"></div>' for k in range(7))
OV[-1] = OV[-1].replace('<div class="pts" id="pts"></div>', b_pts)
# transition: header swap + battery slides left & shrinks
t_swap = t_kompl - .2
T('#h1', {'opacity': 0, 'y': -30}, t_swap, .3, 'power2.in'); T('#b1l', {'opacity': 0}, t_swap, .25, 'power2.in')
A('#h2', {'opacity': 0, 'y': 24}, {'opacity': 1, 'y': 0}, t_swap + .25, .4); sfx(t_swap + .15, 'zoom', -22)
js(f'tl.to("#batw",{{x:-264,y:19,scale:.78,duration:.7,ease:"power3.inOut"}},{t_swap + .1:.3f});')
# rows
levels = [1.0, .86, .66, .50, .34, .18]
for i, (lab, tag, wv, col, tt) in enumerate(rows):
    A(f'#r{i}', {'opacity': 0, 'x': 80}, {'opacity': 1, 'x': 0}, tt - .15, .35, 'power3.out')
    A(f'#r{i}b', {'scaleX': 0}, {'scaleX': 1}, tt + .05, .45 if col == RED else .3, 'power2.out')
    sfx(tt - .1, ['click', 'ting', 'key', 'pop', 'click', 'stamp'][i], -22 if i < 5 else -19)
# battery drain follows the tasks
tt_list = [r[4] for r in rows]
drain('B1', 1.0, .86, t_potong + .1, .5)
drain('B1', .86, .62, t_anim + .1, .6); drain('B1', .62, .44, t_text + .1, .5)
drain('B1', .44, .28, t_broll + .1, .5); drain('B1', .28, .1, t_efek + .1, .6)
recolor_cells('B1', RED, t_efek + .2, .5)
shake('#batsh', t_efek + .35, 10); sfx(t_efek + .35, 'clunk', -19)
for i, tt in enumerate([t_anim, t_text, t_broll]): shake('#batsh', tt + .2, 6, 3)

# ================================================================== SCENE 4: three sizes (full) =======================
t4_0 = t_export - .8; t4_1 = min(wend('lah', t_kompl2) + .7, t_apa - .5)
b = f'<div class="abs" style="left:0;width:1920px;top:34px;text-align:center"><div class="sm" id="z_s" style="font-size:48px">satu content terus export dalam</div><div class="bg2 y" id="z_big" style="font-size:104px">3 SIZE</div></div>'
PW = {'a': (264, 470), 'b': (440, 440), 'c': (640, 360)}
xs = {'a': 144, 'b': 552, 'c': 1136}; BASE = 740
src = {'a': 'assets/panels/p916.mp4', 'b': 'assets/panels/p11.mp4', 'c': 'assets/panels/p169.mp4'}
for k in 'abc':
    w_, h_ = PW[k]
    b += f'<div class="stp" id="z_{k}" style="left:{xs[k]}px;top:{BASE - h_}px;width:{w_}px;height:{h_}px">' + vclip(f'zv_{k}', src[k], t4_0, t4_1 - t4_0, f'left:0;top:0;width:{w_}px;height:{h_}px;object-fit:cover') + '</div>'
    lab = {'a': ('9:16', 'REELS · TIKTOK'), 'b': ('1:1', 'FEED'), 'c': ('16:9', 'YOUTUBE')}[k]
    b += f'<div class="stl" id="z_{k}l" style="left:{xs[k] + w_ / 2 - 140:.0f}px;top:{BASE + 26}px"><span>{lab[0]}</span><em>{lab[1]}</em></div>'
b += bat('B2', 470, 880, 760, 110, .84)
b += f'<div class="abs" id="z_pct" style="left:1300px;top:866px;width:520px"><div class="bg2 y" style="font-size:92px;line-height:1">15–17%</div><div class="sm" style="font-size:34px">untuk ketiga-tiga</div></div>'
b += f'<div class="tiny" id="z_dep" style="left:1300px;width:560px;top:1014px;font-size:26px;color:#aab3d6">tapi depends kepada kompleksiti</div>'
scene('s_size', t4_0, t4_1, 'full', BG_NAVY, b)
A('#z_s', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, t4_0 + .2, .3)
A('#z_big', {'opacity': 0, 'scale': .6, 'filter': 'blur(12px)'}, {'opacity': 1, 'scale': 1, 'filter': 'blur(0px)'}, t_3 - .05, .3, 'back.out(2)'); sfx(t_3 - .05, 'stamp', -21)
for k, tt in zip('abc', [t_916, t_169, t_11]):
    pass
tA, tB, tC = t_916 - .05, t_169 - .05, t_11 - .05
for k, tt in zip('abc', [tA, tC, tB]):   # spoken order 9:16, 16:9, 1:1
    pass
order = {'a': t_916 - .05, 'c': t_169 - .05, 'b': t_11 - .05}
for k, tt in order.items():
    A(f'#z_{k}', {'opacity': 0, 'y': 90, 'scale': .85}, {'opacity': 1, 'y': 0, 'scale': 1}, tt, .45, 'back.out(1.5)')
    A(f'#z_{k}l', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, tt + .25, .3)
    sfx(tt, ['shutter', 'slide', 'click'][list(order).index(k)], -20)
A('#B2', {'opacity': 0, 'y': 40}, {'opacity': 1, 'y': 0}, t_pecah - .1, .4)
A('#z_pct', {'opacity': 0, 'x': 40, 'scale': .85}, {'opacity': 1, 'x': 0, 'scale': 1}, t_15 - .1, .35, 'back.out(1.8)')
drain('B2', .84, .84, t_15, .1)
js(f'tl.set("#B2n",{{textContent:"100%"}},{t_pecah - .1:.3f});')
for i in range(5): SET(f'#B2c{i}', {'scaleX': 1}, t_pecah - .1)
drain('B2', 1.0, .84, t_15 + .05, .7); sfx(t_15 + .05, 'zoom_out', -22); sfx(t_15 + .8, 'ting', -21)
A('#z_dep', {'opacity': 0}, {'opacity': 1}, t_depends, .3)

# ================================================================== SCENE 5: refill (full) ============================
t5_0 = t_apa - .4; t5_1 = wend('senang', t_100b) + 1.0
b = f'<div class="pts"></div>'
b += f'<div class="abs" style="left:0;width:1920px;top:56px;text-align:center"><div class="sm" id="f_s" style="font-size:50px">jangan risau</div><div class="bg2" id="f_b" style="font-size:132px"><span class="y">TAK PAYAH</span> <span class="w">TOP UP</span></div></div>'
b += f'<div class="abs" id="f_q" style="left:0;width:1920px;top:56px;text-align:center"><div class="sm" style="font-size:50px">kalau usage ni</div><div class="bg2 r" style="font-size:150px">HABIS?</div></div>'
b += '<div id="f_bw" class="abs" style="left:0;top:0;width:1920px;height:1080px;transform-origin:0 0"><div id="f_bsh" class="abs" style="left:0;top:0;width:1920px;height:1080px">' + bat('B3', 530, 330, 860, 420, 1.0) + '</div></div>'
b += (f'<div class="abs" id="f_ring" style="left:700px;top:290px;width:520px;height:520px;opacity:0"><svg width="520" height="520" viewBox="0 0 520 520">'
      f'<circle cx="260" cy="260" r="210" fill="none" stroke="rgba(255,255,255,.18)" stroke-width="30"/>'
      f'<circle id="f_arc" cx="260" cy="260" r="210" fill="none" stroke="{Y}" stroke-width="30" stroke-linecap="round" stroke-dasharray="1319" stroke-dashoffset="1319" transform="rotate(-90 260 260)" style="filter:drop-shadow(0 0 16px {Y})"/>'
      f'<line id="f_hand" x1="260" y1="260" x2="260" y2="86" stroke="#fff" stroke-width="10" stroke-linecap="round" style="transform-origin:260px 260px"/></svg>'
      f'<div class="num" style="left:0;width:520px;top:146px;text-align:center;font-size:190px;line-height:1">5</div><div class="lab" style="left:0;width:520px;top:345px;text-align:center;font-size:54px;letter-spacing:6px">JAM</div></div>')
b += f'<div class="abs" id="f_arr" style="left:1250px;top:430px;font-size:100px;color:{Y};text-shadow:0 0 30px {Y};opacity:0">›</div>'
scene('s_ref', t5_0, t5_1, 'full', BG_PURPLE, b)
A('#B3', {'opacity': 0, 'scale': .8}, {'opacity': 1, 'scale': 1}, t5_0 + .15, .4)
A('#f_q', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, t5_0 + .3, .35, 'back.out(2)'); sfx(t5_0 + .3, 'pop', -22)
T('#f_q', {'opacity': 0, 'y': -24}, t_jangan - .4, .25, 'power2.in')
SET('#f_s,#f_b', {'opacity': 0}, t5_0)
drain('B3', 1.0, 0.0, t_habis1 - .1, max(.8, t_habis2 - t_habis1 + .5), 'none', 10)
recolor_cells('B3', RED, t_habis1 + .5, .5)
shake('#f_bsh', t_habis2 + .35, 16, 6); sfx(t_habis2 + .4, 'boom', -18)
A('#f_s', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, t_jangan - .05, .3)
A('#f_b', {'opacity': 0, 'scale': .7, 'filter': 'blur(12px)'}, {'opacity': 1, 'scale': 1, 'filter': 'blur(0px)'}, t_top - .15, .35, 'back.out(2)'); sfx(t_top - .1, 'stamp', -20)
# layout: battery left (0%), ring centre, battery right (refilled)  -> move 0% battery to left
t_lay = t_selepas - .2
js(f'tl.to("#f_bw",{{x:-208,y:202,scale:.6,duration:.7,ease:"power3.inOut"}},{t_lay:.3f});')
A('#f_ring', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, t_lay + .3, .4, 'back.out(1.7)'); sfx(t_lay + .3, 'zoom', -22)
sweep_t0 = t_5jam - .1; sweep_d = max(1.5, t_100b - t_5jam + .1)
A('#f_arc', {'strokeDashoffset': 1319}, {'strokeDashoffset': 0}, sweep_t0, sweep_d, 'none')
A('#f_hand', {'rotation': 0, 'svgOrigin': '260 260'}, {'rotation': 360 * 2, 'svgOrigin': '260 260'}, sweep_t0, sweep_d, 'none')
t_fill = t_100b - .1
b2 = bat('B4', 1330, 400, 480, 240, 0.0)
OV[-1] = OV[-1].replace('<div id="f_bw"', f'<div id="f_bw2" class="abs" style="left:0;top:0;width:1920px;height:1080px;opacity:0">{b2}</div><div id="f_bw"')
A('#f_arr', {'opacity': 0}, {'opacity': 1}, t_fill - .3, .3)
SET('#f_bw2', {'opacity': 1}, t_fill - .3)
for i in range(5): SET(f'#B4c{i}', {'scaleX': 0}, t_fill - .3)
SET('#B4n', {'textContent': '0%', 'color': '#fff'}, t_fill - .3)
drain('B4', 0.0, 1.0, t_fill, .9, 'none', 10); sfx(t_fill + .9, 'riser', -22); sfx(t_fill + .95, 'ting', -19)
for i in range(5): T(f'#B4c{i}', {'backgroundColor': Y}, t_fill, .01)

# ================================================================== SCENE 6: modes (full) =============================
t6_0 = t_mode - .35; t6_1 = wend('habis', t_weekly_habis) + 1.0
b = f'<div class="abs" style="left:0;width:1920px;top:40px;text-align:center"><div class="sm" id="m_s" style="font-size:50px">usage ada</div><div class="bg2 y" id="m_b" style="font-size:112px">2 MODE</div></div>'
b += '<div class="glass" id="m_cardA" style="left:140px;top:290px;width:760px;height:640px;opacity:0"></div><div class="glass" id="m_cardB" style="left:1020px;top:290px;width:760px;height:640px;opacity:0"></div>'
b += f'<div class="lab" id="m_At" style="left:140px;width:760px;top:322px;text-align:center;font-size:50px;opacity:0">HARIAN · DAILY</div><div class="lab" id="m_Bt" style="left:1020px;width:760px;top:322px;text-align:center;font-size:50px;opacity:0">WEEKLY</div>'
b += '<div id="m_bat" style="opacity:0">' + bat('B5', 230, 480, 540, 270, 1.0) + '</div>'
b += f'<div class="sm" id="m_At2" style="left:140px;width:760px;top:810px;text-align:center;position:absolute;font-size:34px;color:#cfd3ff;opacity:0">habis → penuh balik selepas 5 jam</div>'
days = ['ISN', 'SEL', 'RAB', 'KHA', 'JUM', 'SAB', 'AHD']
for i, dname in enumerate(days):
    L = 1075 + i * 95
    b += (f'<div class="wb" id="wb{i}" style="left:{L}px;top:470px;width:72px;height:320px;opacity:0"><i id="wf{i}"></i></div>'
          f'<div class="wl" id="wl{i}" style="left:{L - 8}px;top:810px;width:88px;opacity:0">{dname}</div>')
b += f'<div class="stampr" id="m_stamp" style="left:1020px;width:760px;top:470px;opacity:0"><span>TAK BOLEH GUNA</span></div>'
scene('s_mode', t6_0, t6_1, 'full', BG_PURPLE, b)
A('#m_s', {'opacity': 0}, {'opacity': 1}, t6_0 + .1, .3); A('#m_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, wt('dua|2', t_mode - .6) - .05, .3, 'back.out(2)')
sfx(wt('dua|2', t_mode - .6) - .05, 'stamp', -21)
A('#m_cardA,#m_At,#m_bat', {'opacity': 0, 'y': 40}, {'opacity': 1, 'y': 0}, t_harian - .1, .4); sfx(t_harian - .05, 'slide', -22)
A('#m_At2', {'opacity': 0}, {'opacity': 1}, t_harian + .8, .3)
drain('B5', 1.0, .6, t_harian + 1.3, 1.2); drain('B5', .6, 1.0, t_harian + 3.0, .8)
A('#m_cardB,#m_Bt', {'opacity': 0, 'y': 40}, {'opacity': 1, 'y': 0}, t_weekly - .1, .4); sfx(t_weekly - .05, 'slide', -22)
A('#wb0,#wb1,#wb2,#wb3,#wb4,#wb5,#wb6', {'opacity': 0}, {'opacity': 1, 'stagger': .06}, t_weekly + .2, .3)
A('#wl0,#wl1,#wl2,#wl3,#wl4,#wl5,#wl6', {'opacity': 0}, {'opacity': 1, 'stagger': .06}, t_weekly + .2, .3)
for i in range(7): A(f'#wf{i}', {'scaleY': 0}, {'scaleY': 1}, t_weekly100 - .05 + i * .07, .35, 'power2.out')
sfx(t_weekly100 - .05, 'ratchet', -23)
# bars die day by day, Khamis hits zero
t_use = t_weekly100 + 1.6
for i, lvl in enumerate([.72, .5, .3]):
    T(f'#wf{i}', {'scaleY': lvl}, t_use + i * .5, .5, 'power2.inOut')
T('#wf3', {'scaleY': 0, 'backgroundColor': RED}, t_kamis, .5, 'power2.in'); sfx(t_kamis, 'boom', -19)
T('#wf3', {'boxShadow': f'0 0 26px {RED}'}, t_kamis, .3)
for i in range(4, 7): T(f'#wb{i}', {'opacity': .35}, t_kamis + .3, .4)
A('#m_stamp', {'opacity': 0, 'scale': 1.6, 'rotation': -14}, {'opacity': 1, 'scale': 1, 'rotation': -6}, t_tbg - .05, .22, 'back.out(1.4)'); sfx(t_tbg - .05, 'stamp', -18)
shake('#m_cardB', t_tbg + .2, 10, 5)


# ---------------------------------------------------------------- PRICE (behind head) ------------------------------------
tp0 = t_package - .3; tp1 = wend('rm100|100', t_90) + 1.4
els = ''
for k, (x, lab, rot, d) in enumerate([(120, 'CLAUDE', -8, -1), (1280, 'CHATGPT', 7, 1)]):
    els += (f'<div class="glass abs" id="pr_c{k}" style="left:{x}px;top:{150 + k * 20}px;width:520px;height:300px;transform:rotate({rot}deg)"></div>'
            f'<div class="lab abs" id="pr_l{k}" style="left:{x}px;width:520px;top:{175 + k * 20}px;text-align:center;font-size:40px;transform:rotate({rot}deg)">{lab}</div>'
            f'<div class="num abs" id="pr_n{k}" style="left:{x}px;width:520px;top:{230 + k * 20}px;text-align:center;font-size:150px;line-height:1;transform:rotate({rot}deg)">0</div>'
            f'<div class="lab abs" id="pr_u{k}" style="left:{x}px;width:520px;top:{390 + k * 20}px;text-align:center;font-size:30px;color:#fff;transform:rotate({rot}deg)">USD / SEBULAN</div>')
for k, (x, y, r) in enumerate([(760, 60, 110), (1070, 110, 90), (560, 480, 80), (1330, 520, 100), (300, 640, 70)]):
    els += f'<div class="abs coin" id="pr_k{k}" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;font-size:{r * .45:.0f}px">$</div>'
fg = (f'<div class="abs" style="left:0;width:1920px;top:800px;text-align:center"><div class="sm" id="pr_s" style="font-size:44px">convert lebih kurang</div><div class="bg2 y" id="pr_b" style="font-size:150px">RM90–100 / BULAN</div></div>')
bhscene('s_price', tp0, tp1, els, fg)
for k in range(2):
    A(f'#pr_c{k},#pr_l{k},#pr_u{k}', {'opacity': 0, 'y': 80, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, t_package + k * .35, .45, 'back.out(1.6)')
    A(f'#pr_n{k}', {'opacity': 0}, {'opacity': 1}, t_20 - .1 + k * .2, .2)
    counter(f'#pr_n{k}', t_20 - .05 + k * .2, .6, 20, 10)
sfx(t_20 - .05, 'ratchet', -14); sfx(t_20 + .6, 'stamp', -13)
for k in range(5):
    A(f'#pr_k{k}', {'opacity': 0, 'y': 200, 'rotation': -180}, {'opacity': 1, 'y': 0, 'rotation': 0}, t_package + .1 + k * .12, .6, 'bounce.out')
    js(f'tl.to("#pr_k{k}",{{y:{(-1) ** k * 18},duration:1.4,ease:"sine.inOut",yoyo:true,repeat:3}},{t_package + .8 + k * .1:.3f});')
A('#pr_s,#pr_b', {'opacity': 0, 'y': 24, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, t_90 - .15, .4, 'back.out(1.8)'); sfx(t_90 - .15, 'ting', -12)

# ---------------------------------------------------------------- RACE team vs Claude (behind head) -----------------------
tr0 = t_team - .6; tr1 = min(wend('minit', t_1520) + 1.4, t_sebulan - .4)
els = ''
for i in range(5): els += card_html(i, [1, 2, 3, 4, '→'][i], 90 + i * 50, 120 + i * 34, -12 + i * 5).replace('{p}', 'rc')
els += (f'<div class="num abs" id="rc_t" style="left:60px;width:560px;top:735px;text-align:center;font-size:96px;color:{RED};text-shadow:0 0 30px {RED}88">1 JAM</div>'
        f'<svg class="abs" id="rc_sw" style="left:1360px;top:110px" width="400" height="400" viewBox="0 0 400 400"><circle cx="200" cy="215" r="150" fill="rgba(15,18,36,.75)" stroke="rgba(255,255,255,.3)" stroke-width="20"/>'
        f'<circle id="rc_arc" cx="200" cy="215" r="150" fill="none" stroke="{Y}" stroke-width="20" stroke-linecap="round" stroke-dasharray="942" stroke-dashoffset="942" transform="rotate(-90 200 215)" style="filter:drop-shadow(0 0 16px {Y})"/>'
        f'<line id="rc_h" x1="200" y1="215" x2="200" y2="120" stroke="#fff" stroke-width="12" stroke-linecap="round" style="transform-origin:200px 215px"/><rect x="170" y="22" width="60" height="30" rx="8" fill="#fff"/></svg>'
        f'<div class="num abs" id="rc_m" style="left:1300px;width:520px;top:520px;text-align:center;font-size:90px;color:{Y};text-shadow:0 0 30px {Y}88">15–20 MINIT</div>'
        f'<svg class="abs" id="rc_ar" style="left:690px;top:80px" width="540" height="140" viewBox="0 0 540 140"><path d="M10 70 C140 -10 400 -10 530 70" fill="none" stroke="{Y}" stroke-width="8" stroke-dasharray="16 12" style="filter:drop-shadow(0 0 10px {Y})"/><path d="M500 38 L536 72 L494 90" fill="none" stroke="{Y}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>')
fg = f'<div class="abs" style="left:0;width:1920px;top:830px;text-align:center"><div class="sm" id="rc_s" style="font-size:44px">dulu minta team · sekarang dengan Claude</div></div>'
bhscene('s_race', tr0, tr1, els, fg)
for i in range(5):
    A(f'#rccal{i}', {'opacity': 0, 'rotationX': -80, 'y': -60}, {'opacity': 1, 'rotationX': 0, 'y': 0}, t_jam1 - .1 + i * .18, .3, 'back.out(1.6)')
    sfx(t_jam1 - .1 + i * .18, ['key', 'click', 'key', 'click', 'key'][i], -15)
A('#rc_t', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, t_jam1 - .1, .3, 'back.out(2)')
js(f'tl.set("#rc_t",{{textContent:"3–4 JAM"}},{t_3jam:.3f});'); js(f'tl.set("#rc_t",{{textContent:"3–4 HARI"}},{t_hari34:.3f});')
shake('#rc_t', t_hari34, 12, 5); sfx(t_hari34, 'boom', -12)
A('#rc_ar', {'opacity': 0}, {'opacity': 1}, t_dengan - .1, .4)
A('#rc_sw', {'opacity': 0, 'scale': .4}, {'opacity': 1, 'scale': 1}, t_dengan, .35, 'back.out(1.8)')
A('#rc_arc', {'strokeDashoffset': 942}, {'strokeDashoffset': 500}, t_1520 - .1, .55, 'power2.out'); A('#rc_h', {'rotation': 0, 'svgOrigin': '200 215'}, {'rotation': 200, 'svgOrigin': '200 215'}, t_1520 - .1, .55, 'power2.out')
A('#rc_m', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, t_1520 - .05, .35, 'back.out(2)'); sfx(t_1520 - .05, 'shing', -13)
T('#rccal0,#rccal1,#rccal2,#rccal3,#rccal4,#rc_t', {'opacity': .35}, t_1520, .4)
A('#rc_s', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, t_dengan, .3)

# ---------------------------------------------------------------- 100+ VIDEO wall (behind head, B&W bg) -----------------------
tv0 = t_sebulan - .3; tv1 = wend('ni', wt('macam', t_daily)) + .7
tv1 = min(tv1, tv0 + 11.5)
els = '<div class="abs" style="left:-250px;top:-40px;width:2500px;height:1180px;transform:rotate(-7deg);transform-origin:50% 50%;background:rgba(10,8,30,.35)">'
for r in range(5):
    VT[0] += 1
    els += f'<div class="abs wallrow" id="wr{r}" style="left:{-60 - r * 90}px;top:{r * 214 + 40}px;width:2816px;height:199px">' + vclip(f'wv{r}', f'assets/wall/row{r}.mp4', tv0, tv1 - tv0, 'left:0;top:0;width:2816px;height:199px;object-fit:cover') + '</div>'
    VT[0] += 0
els += '</div>'
fg = (f'<div class="abs" style="left:0;top:0;width:1920px;height:1080px;background:linear-gradient(180deg,rgba(0,0,0,0) 55%,rgba(0,0,0,.55) 100%)"></div>'
      f'<div class="abs" style="left:0;width:1920px;top:690px;text-align:center"><div class="sm" id="wv_s" style="font-size:44px">sebulan dengan Claude, lebih</div></div>'
      f'<div class="num abs" id="wv_n" style="left:0;width:1920px;top:735px;text-align:center;font-size:250px;line-height:1">0</div>'
      f'<div class="bg2 y abs" id="wv_v" style="left:0;width:1920px;top:960px;text-align:center;font-size:84px;line-height:1">VIDEO</div>')
bhscene('s_wall', tv0, tv1, els, fg, bw=True)
for r in range(5):
    js(f'tl.fromTo("#wr{r}",{{x:0}},{{x:{(-1) ** r * 260},duration:{tv1 - tv0:.2f},ease:"none",immediateRender:false}},{tv0:.3f});')
A('#wallrows', {'opacity': 0}, {'opacity': 1}, tv0, .01) if False else None
A('#wv_s', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, tv0 + .3, .3)
A('#wv_n,#wv_v', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, t_100v - .55, .4, 'back.out(1.8)')
counter('#wv_n', t_100v - .5, .9, 100, 14, fmt='{}'); js(f'tl.set("#wv_n",{{textContent:"100+"}},{t_100v + .45:.3f});')
sfx(t_100v - .5, 'ratchet', -14); sfx(t_100v + .45, 'stamp', -11); sfx(t_100v + .45, 'boom', -13)
SET('#wv_n', {'textContent': '0'}, tv0 - .02)

# ---------------------------------------------------------------- BENCHMARK (behind head) ----------------------------------
tb0 = t_kompet - .4; tb1 = wend('video', t_laju) + 1.6
els = (f'<div class="abs" id="bk_o" style="left:60px;top:640px;width:520px;height:440px;background:linear-gradient(180deg,rgba(255,255,255,.28),rgba(255,255,255,.08));border-top:5px solid #fff;border-radius:16px 16px 0 0"></div>'
       f'<div class="abs" id="bk_n" style="left:1330px;top:230px;width:530px;height:850px;background:linear-gradient(180deg,rgba(255,255,0,.4),rgba(255,255,0,.1));border-top:6px solid {Y};border-radius:16px 16px 0 0;box-shadow:0 -20px 60px rgba(255,255,0,.3)"></div>'
       f'<div class="lab abs" id="bk_ol" style="left:80px;top:690px;font-size:34px;color:#fff">BENCHMARK LAMA</div><div class="lab abs" id="bk_nl" style="left:1350px;top:270px;font-size:34px">BENCHMARK BARU</div>')
for i, (lab, tt) in enumerate([('PREMIERE', t_prem), ('AFTER EFFECTS', t_after2), ('CAPCUT', t_capcut)]):
    els += f'<div class="chip abs" id="bk_c{i}" style="left:70px;top:{380 + i * 90}px;width:430px;height:76px;font-size:30px">{lab}</div>'
els += (f'<div class="chip abs" id="bk_ai" style="left:1350px;top:120px;width:490px;height:100px;font-size:44px;border-color:{Y};color:{Y};box-shadow:0 0 50px {Y}66">EDITOR + AI</div>'
        f'<svg class="abs" id="bk_ar" style="left:560px;top:230px" width="700" height="420" viewBox="0 0 700 420"><path d="M20 400 C220 380 420 260 620 60 M540 40 L632 52 L612 140" fill="none" stroke="{Y}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 14px {Y})"/></svg>')
fg = f'<div class="abs" style="left:0;width:1920px;top:40px;text-align:center"><div class="sm" id="bk_s" style="font-size:44px">kompetensi dia</div><div class="bg2 y" id="bk_b" style="font-size:110px">LAGI TINGGI</div></div>'
bhscene('s_bench', tb0, tb1, els, fg)
t_ting = wt('tinggi', t_kompet)
A('#bk_s', {'opacity': 0}, {'opacity': 1}, tb0 + .2, .3)
A('#bk_b', {'opacity': 0, 'scale': .6, 'filter': 'blur(12px)'}, {'opacity': 1, 'scale': 1, 'filter': 'blur(0px)'}, t_ting - .05, .35, 'back.out(2)'); sfx(t_ting - .05, 'stamp', -13)
A('#bk_o,#bk_ol', {'opacity': 0, 'y': 120}, {'opacity': 1, 'y': 0}, t_kompet + .2, .5, 'power3.out')
for i, tt in enumerate([t_prem, t_after2, t_capcut]):
    A(f'#bk_c{i}', {'opacity': 0, 'y': 30, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, tt - .1, .3, 'back.out(1.8)'); sfx(tt - .08, ['click', 'key', 'pop'][i], -14)
A('#bk_n,#bk_nl', {'opacity': 0, 'y': 400}, {'opacity': 1, 'y': 0}, t_adapt - .5, .7, 'power3.out'); sfx(t_adapt - .5, 'swish_up', -13)
A('#bk_ar', {'opacity': 0}, {'opacity': 1}, t_adapt - .35, .5)
A('#bk_ai', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, t_adapt - .05, .4, 'back.out(1.8)'); sfx(t_adapt - .05, 'shing', -12)
T('#bk_c0,#bk_c1,#bk_c2', {'opacity': .45}, t_adapt, .4)

# ---------------------------------------------------------------- ADAPT (behind head) ---------------------------------------
ta0 = t_adapt2 - .7; ta1 = wend('sendiri', t_conv) + 1.0
def svgi(p): return f'<svg width="120" height="120" viewBox="0 0 64 64" fill="none" stroke="{Y}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">{p}</svg>'
IC = [('AUTOMATE', 'kerja berulang', svgi('<path d="M52 30 A20 20 0 0 0 16 22 M12 34 A20 20 0 0 0 48 42"/><path d="M16 10 V22 H28 M48 54 V42 H36"/>'), 100, 170, -8, t_auto),
      ('FOKUS', 'story', svgi('<path d="M32 14 C24 8 14 8 6 10 V50 C14 48 24 48 32 54 C40 48 50 48 58 50 V10 C50 8 40 8 32 14 Z M32 14 V54"/>'), 1420, 150, 7, t_story),
      ('FOKUS', 'conversion', svgi('<path d="M6 10 H58 L38 34 V54 L26 48 V34 Z"/>'), 560, 60, 5, t_conv)]
els = ''
for k, (a, b_, ic, x, y, rot, tt) in enumerate(IC):
    els += f'<div class="glass abs" id="ad_t{k}" style="left:{x}px;top:{y}px;width:400px;height:320px;transform:rotate({rot}deg)"><div style="text-align:center;margin-top:26px">{ic}</div><div class="lab" style="position:relative;text-align:center;font-size:44px;margin-top:8px">{a}</div><div class="num" style="position:relative;text-align:center;font-size:30px;font-weight:600;margin-top:12px">{b_}</div></div>'
fg = f'<div class="abs" style="left:0;width:1920px;top:800px;text-align:center"><div class="sm" id="ad_s" style="font-size:44px">kita kena jadi orang yang</div><div class="bg2 y" id="ad_b" style="font-size:150px">ADAPT</div></div>'
bhscene('s_adapt', ta0, ta1, els, fg)
A('#ad_s,#ad_b', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, t_adapt2 - .15, .4, 'back.out(2)'); sfx(t_adapt2 - .15, 'stamp', -13)
for k, (a, b_, ic, x, y, rot, tt) in enumerate(IC):
    A(f'#ad_t{k}', {'opacity': 0, 'scale': .3, 'y': 200, 'rotation': rot - 30}, {'opacity': 1, 'scale': 1, 'y': 0, 'rotation': rot}, tt - .3, .5, 'back.out(1.7)'); sfx(tt - .3, ['pop', 'click', 'ting'][k], -13)
    js(f'tl.to("#ad_t{k}",{{y:{(-1) ** k * 14},rotation:{rot + (-1) ** k * 2},duration:1.3,ease:"sine.inOut",yoyo:true,repeat:3}},{tt + .4:.3f});')

# ---------------------------------------------------------------- OUTRO 1 hari 1 vlog (behind head) --------------------------
to0 = t_vlog - 1.0; to1 = min(DUR - 1.6, wend('try', t_aku) + 8.0)
to1 = min(to1, t_rekod - .2)
els = ''
for i, (x, y, rot) in enumerate([(110, 140, -9), (360, 330, 6), (1330, 160, 8), (1580, 360, -6), (860, 40, 0)]):
    first = i == 0
    els += (f'<div class="abs" id="ou_d{i}" style="left:{x}px;top:{y}px;width:200px;height:260px;border-radius:22px;background:{"rgba(255,255,0,.2)" if first else "rgba(255,255,255,.1)"};'
            f'border:{"4px solid " + Y if first else "3px dashed rgba(255,255,255,.45)"};transform:rotate({rot}deg);{f"box-shadow:0 0 50px {Y}66" if first else ""}">'
            f'<div class="num" style="position:relative;text-align:center;font-size:92px;margin-top:40px;color:{"#fff" if first else "rgba(255,255,255,.6)"}">{7 if i == 4 else i + 1}</div>'
            f'<div class="lab" style="position:relative;text-align:center;font-size:24px;color:{Y if first else "rgba(255,255,255,.55)"}">{"HARI INI" if first else ("ESOK" if i == 1 else "·")}</div></div>')
fg = f'<div class="abs" style="left:0;width:1920px;top:790px;text-align:center"><div class="sm" id="ou_s" style="font-size:44px">episod pertama</div><div class="bg2" id="ou_b" style="font-size:130px"><span class="y">1 HARI</span> <span class="w">·</span> <span class="y">1 VLOG</span></div></div>'
bhscene('s_out', to0, to1, els, fg)
A('#ou_s,#ou_b', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, wt('satu|1', t_try + .3) - .1, .4, 'back.out(2)'); sfx(wt('satu|1', t_try + .3) - .1, 'stamp', -13)
for i in range(5):
    A(f'#ou_d{i}', {'opacity': 0, 'y': -200, 'rotation': -40 + i * 7}, {'opacity': 1, 'y': 0, 'rotation': [-9, 6, 8, -6, 0][i]}, to0 + .2 + i * .22, .55, 'bounce.out'); sfx(to0 + .25 + i * .22, ['pop', 'click', 'pop', 'click', 'ting'][i], -15)

# ================================================================== CAPTIONS (presenter windows) ======================
grp('ramai dah start nampak', [('CLAUDE', 'y', 'cloud|claude'), ('BOLEH', 'w', 'boleh'), ('EDIT VIDEO', 'y', 'edit')], HD + .05, 1.5)
grp('sebenarnya', [('CHATGPT', 'y', 'chatgpt'), ('PUN BOLEH', 'w', 'pun')], wt('sebenarnya', HD), 1.4)
grp('gunakan code', [('SAMA JE', 'y', 'sama')], wt('gunakan', HD), 1.1)
grp('cuma hasil daripada Claude', [('LAGI BAGUS', 'y', 'bagus'), ('LAGI SMOOTH', 'y', 'smooth')], wt('cuma', HD), 1.3)
grp('saya punya social media content', [('AVERAGE', 'w', 'average'), ('VIDEO', 'y', 'video')], t_avg - .5, 1.3)
grp('sebab apa?', [('WEEKLY', 'y', 'weekly'), ('DAH HABIS', 'w', 'habis')], wt('sebab', t_tbg), 1.2)
grp('jadi mungkin pada waktu tu', [('HEAVY USE', 'y', 'heavy')], wt('mungkin', t_weekly_habis), 1.2)
grp('', [('BERBALOI', 'y', 'berbaloi'), ('KE TAK?', 'w', 'ke')], t_berbaloi - .1, 1.1)
grp('', [('MAHAL', 'y', 'mahal'), ('KE MURAH?', 'w', 'murah')], wt('mahal', t_berbaloi), 1.2)
grp('kita kena jawab satu', [('PERSOALAN', 'y', 'persoalan')], wt('persoalan', t_berbaloi), 1.2)
grp('so pada saya', [('SANGAT', 'w', 'sangat'), ('BERBALOI', 'y', 'berbaloi')], wt('so', t_daily), 1.4)
grp('video editor', [('MASIH', 'w', 'masih'), ('DIPERLUKAN', 'y', 'diperlukan')], wt('no', t_berbaloi2), 1.4)
grp('', [('NO', 'y', 'no'), ('PROBLEM', 'w', 'problem')], wt('no', t_capcut), 1.0)
grp('', [('JANGAN', 'w', 'jangan'), ('RISAU', 'y', 'risaulah')], wt('jangan', t_geng), 1.2)
grp('mungkin tu je dalam', [('EPISOD', 'w', 'episod'), ('PERTAMA', 'y', 'pertama')], wt('mungkin', t_conv), 1.5)
grp('kita rekod je, borak je', [('LEPAS TU', 'w', 'lepas'), ('CLAUDE EDIT', 'y', 'cloud|claude')], wt('lepas', t_rekod), 1.2)
grp('kita tengok', [('BOLEH', 'w', 'boleh'), ('KONSISTEN', 'y', 'konsis|consis'), ('KE?', 'w', 'ke')], wt('tengok', t_rekod), 1.7)
grp('anything', [('JUMPA', 'w', 'jumpa'), ('ESOK', 'y', 'esok')], t_anything - .1, 1.6)

# ================================================================== CAMERA ============================================
HX, HY = 950, 410
def cam_xy(S, sx=960):
    tx = min(0, max(W - S * W, sx - S * HX)); ty = min(0, max(H - S * H, 0.42 * H - S * HY)); return round(tx, 1), round(ty, 1)
blocked = [(s[0], s[1]) for s in SCENES if s[2] in ('full', 'bh')]
def in_win(t, wins, pad=0.0): return any(a - pad <= t <= b + pad for a, b in wins)
CAMK = [(h_hari - .4, 1.2, 960, .5), (h_mc - .45, 1.3, 960, .5), (h_15 - .5, 1.42, 960, .5), (HD - .5, 1.0, 960, .45)]
cyc = [1.16, 1.0, 1.28, 1.1, 1.22, 1.0]; ci = 0; last = HD; cur_S = 1.0
starts = sorted(set(round(s['s'], 2) for s in SEGS))
events = []
for t in starts:
    if t < HD + 1.2 or t > DUR - 3: continue
    if in_win(t, blocked, .9) or t - last < 4.6: continue
    S_ = cyc[ci % len(cyc)]; ci += 1
    events.append((t, S_)); last = t
for a, b in blocked:
    events.append((a - .6, 1.0))
events.sort()
cur = 1.0; planned = []
for t, S_ in events:
    if S_ == cur: continue
    if in_win(t + .5, blocked, 0) and S_ != 1.0: continue
    planned.append((t, S_, 960, .8 if S_ != 1.0 else .5)); cur = S_
CAMK += planned
CAMK.sort()
clean = []; endp = -1
for k in CAMK:
    if k[0] >= endp - 1e-6: clean.append(k); endp = k[0] + k[3]
CAMK = clean
cx, cy = cam_xy(1.1)
js(f'gsap.set("#cam",{{transformOrigin:"0 0",x:{cx},y:{cy},scale:1.1}});')
for t, S_, sx, d in CAMK:
    x_, y_ = cam_xy(S_, sx)
    js(f'tl.to("#cam",{{x:{x_},y:{y_},scale:{S_},duration:{d},ease:"sine.inOut"}},{t:.3f});')
for t, S_, sx, d in CAMK:
    if t > HD and S_ > 1.05: sfx(t, 'zoom_in', -17)
    elif t > HD and S_ <= 1.05: sfx(t, 'zoom_out', -18)
print('camera keys', len(CAMK))
emit_caps()

CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:#0F1224;font-family:Poppins,sans-serif}
#root{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:hidden;background:#000}
#cam{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0}
#base{position:absolute;left:0;top:0;width:1920px;height:1080px}
.abs{position:absolute}
.ov{position:absolute;left:0;top:0;width:1920px;height:1080px;opacity:0;display:none;overflow:hidden;z-index:20;font-family:Poppins,sans-serif}
.ov > *{position:absolute}
.cap{position:absolute;z-index:100;opacity:0;font-family:Poppins,sans-serif}
.sm{font-weight:500;color:#fff;line-height:1.15;font-size:.42em;text-shadow:0 0 .1em rgba(255,255,255,.7),0 0 .35em rgba(255,255,255,.3),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}
.bg2{font-weight:800;line-height:1.04;text-transform:uppercase;letter-spacing:-.012em;white-space:nowrap}
.bw{display:inline-block;transform-origin:50% 70%}
.y{color:#FFFF00;font-weight:800;text-shadow:0 0 .05em rgba(255,255,0,.95),0 0 .2em rgba(255,255,0,.6),0 0 .45em rgba(255,255,0,.35),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}
.r{color:#FF4D4D;font-weight:800;text-shadow:0 0 .05em rgba(255,77,77,.95),0 0 .2em rgba(255,77,77,.6),0 0 .45em rgba(255,77,77,.35),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}
.w{color:#fff;font-weight:600;text-shadow:0 0 .06em rgba(255,255,255,.9),0 0 .2em rgba(255,255,255,.5),0 0 .45em rgba(255,255,255,.28),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}
.ov .sm{font-size:50px}
.num{position:absolute;font-weight:800;color:#fff;letter-spacing:-.02em;text-shadow:0 0 .08em rgba(255,255,255,.9),0 0 .3em rgba(255,255,255,.45),0 .06em .1em rgba(0,0,0,.6)}
.lab{position:absolute;font-weight:800;color:#FFFF00;text-transform:uppercase;text-shadow:0 0 .2em rgba(255,255,0,.6)}
.tiny{position:absolute;font-weight:500;font-size:22px;color:#6f78a8;letter-spacing:2px}
.glass{position:absolute;border-radius:28px;background:linear-gradient(160deg,rgba(255,255,255,.14),rgba(255,255,255,.04));border:2px solid rgba(255,255,255,.25);box-shadow:0 30px 80px rgba(0,0,0,.5),inset 0 0 40px rgba(255,255,255,.05)}
.chip{position:absolute;border-radius:22px;background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.28);color:#fff;font-weight:700;display:flex;align-items:center;justify-content:space-between;padding:0 34px}
.rb{display:block;border-radius:11px;transform:scaleX(0)}
.bt{position:absolute}
.btb{position:absolute;left:0;top:0;border-style:solid;border-color:#fff;background:rgba(255,255,255,.07);box-shadow:0 0 60px #FFFF0055,inset 0 0 50px rgba(255,255,255,.06)}
.btn{position:absolute;width:34px;border-radius:0 14px 14px 0;background:#fff}
.btc{position:absolute;transform-origin:0 50%;background:linear-gradient(180deg,#FFFF00,#E6EC00);box-shadow:0 0 36px #FFFF00aa}
.btt{position:absolute;left:0;top:0;text-align:center;font-weight:800;color:#0F1224;letter-spacing:-.02em;z-index:3;text-shadow:none}
.pt{position:absolute;width:20px;height:20px;border-radius:50%;background:#FFFF00;opacity:0;box-shadow:0 0 30px #FFFF00}
.trk{position:absolute;border-radius:14px;background:rgba(255,255,255,.07);border:2px dashed rgba(255,255,255,.25)}
.dot{position:absolute;width:36px;height:36px;border-radius:50%}
.stp{position:absolute;border-radius:22px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.55);border:2px solid rgba(255,255,255,.22);background:#000}
.pv{position:absolute}
.stl{position:absolute;width:280px;text-align:center}
.stl span{display:inline-block;background:#FFFF00;color:#0F1224;font-weight:800;font-size:34px;padding:2px 26px 4px;border-radius:999px}
.stl em{display:block;margin-top:8px;font-style:normal;font-weight:600;font-size:22px;color:#aab3d6;letter-spacing:3px}
.wb{position:absolute;border-radius:14px;background:rgba(255,255,255,.16);overflow:hidden}
.wb i{position:absolute;left:0;bottom:0;width:100%;height:100%;background:#FFFF00;box-shadow:0 0 22px #FFFF00;transform-origin:50% 100%;transform:scaleY(0);border-radius:14px}
.wl{position:absolute;text-align:center;font-weight:700;font-size:24px;color:#fff}
.stampr{position:absolute;text-align:center}
.stampr span{display:inline-block;font-weight:800;font-size:44px;color:#FF4D4D;border:5px solid #FF4D4D;border-radius:12px;padding:0 22px;box-shadow:0 0 30px #FF4D4D55;background:rgba(15,18,36,.6)}
.chk{position:absolute;display:flex;align-items:center;gap:28px;border-radius:22px;background:rgba(255,255,255,.08);border:2px solid rgba(255,255,255,.22);padding:0 30px;font-weight:700;font-size:32px;color:#fff;letter-spacing:.5px;white-space:nowrap}
.bhs{position:absolute;left:0;top:0;width:1920px;height:1080px;display:none}
.bhov{background:transparent}
.pm{position:absolute;left:0;top:0;width:1920px;height:1080px}
.pmglow{filter:drop-shadow(0 0 3px rgba(255,255,255,.9)) drop-shadow(0 0 22px rgba(255,255,255,.55))}
.coin{border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff7a0,#FFFF00 55%,#c9b800);box-shadow:0 0 40px #FFFF0088;display:flex;align-items:center;justify-content:center;font-weight:800;color:#0F1224}
.wallrow{position:absolute}
.pill{display:inline-block;background:#FFFF00;color:#0F1224;font-weight:800;border-radius:999px;padding:2px 26px 4px}
#base{will-change:filter}
'''

NDUR = DUR
js_all = '\n'.join(INIT + JS)
html = f'''<!doctype html>
<html lang="ms" data-resolution="landscape"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{NDUR}" data-width="1920" data-height="1080">
<div id="cam"><video id="base" class="clip" src="assets/main.mp4" muted playsinline data-start="0" data-duration="{NDUR}" data-media-start="0" data-track-index="1"></video>
<div id="wback">{''.join(WB)}</div>{''.join(PM)}</div>
{''.join(OV)}
{''.join(CAPS)}
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{NDUR}" data-track-index="50" data-volume="1"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{paused:true}});
{js_all}
window.__timelines["main"] = tl;
</script></body></html>'''
for _id in ['hkcal%d' % i for i in range(5)] + ['rccal%d' % i for i in range(5)] + ['u_adv', 'u_100', 'pr_s', 'ad_t0', 'ad_t1', 'ad_t2', 'ou_d4']:
    html = html.replace('id="%s"' % _id, 'id="%s" data-layout-allow-overlap' % _id)
open('hf/index.html', 'w').write(html)
json.dump({'dur': NDUR, 'sfx': sorted(SFX), 'scenes': [[round(a, 2), round(b, 2), k, i] for a, b, k, i in SCENES]}, open('build/sfx_events.json', 'w'))
json.dump(BHI, open('build/bh_intervals.json', 'w'))
print('html', len(html), 'sfx events', len(SFX), 'dur', NDUR)
for a, b, k, i in sorted(SCENES): print(f'  {i:8s} {k:5s} {a:7.2f} - {b:7.2f}')
