#!/usr/bin/env python3
"""'Siapa dekat sini banyak video tak edit' - Long-Form Video style adapted to 9:16 (1080x1920, 30 fps).
Writes hf/index.html + build/sfx_events.json + build/bh_intervals.json. Anchors come from words_out.json (cut time)."""
import json, math, re, random
W, H = 1080, 1920
tm = json.load(open('build/timemap.json')); DUR = round(tm['dur'], 3); HD = tm['hook_dur']
WORDS = json.load(open('build/words_out.json'))
Y, WH, NAVY = '#FFFF00', '#FFFFFF', '#0F1224'
RED, GRN, CLC = '#FF4D4D', '#35E08A', '#D97757'

def norm(t): return re.sub(r'[^a-z0-9%]', '', t.lower())
def wt(word, after=0.0, nth=0):
    alts = [norm(a) for a in word.split('|')]; c = 0
    for t, sn, a, b in WORDS:
        if sn >= after - 1e-6 and any(norm(t).startswith(x) for x in alts):
            if c == nth: return sn
            c += 1
    raise KeyError(f'{word} after {after}')
JS = []; SFX = []
def js(s): JS.append(s)
def sfx(t, kind, db=-20): SFX.append([round(float(t), 3), kind, db])
def fj(d): return json.dumps(d, separators=(',', ':'))
INIT = []; INIT_SEEN = set()
def A(sel, f, to, t, d=.4, ease='power3.out'):
    if f.get('opacity') == 0 and sel not in INIT_SEEN:
        INIT_SEEN.add(sel); INIT.append(f'gsap.set("{sel}",{fj({k: v for k, v in f.items()})});')
    js(f'tl.fromTo("{sel}",{fj(f)},{fj({**to, "duration": d, "ease": ease, "immediateRender": False})},{t:.3f});')
def T(sel, to, t, d=.4, ease='power2.out'): js(f'tl.to("{sel}",{fj({**to, "duration": d, "ease": ease})},{t:.3f});')
def SET(sel, to, t): js(f'tl.set("{sel}",{fj(to)},{t:.3f});')
def G0(sel, st): INIT.append(f'gsap.set("{sel}",{fj(st)});')
def shake(sel, t, amp=14, n=5):
    for i in range(n): js(f'tl.set("{sel}",{{x:{(-1) ** i * amp * (1 - i / n):.1f}}},{t + i * .04:.3f});')
    js(f'tl.set("{sel}",{{x:0}},{t + n * .04:.3f});')
def typed(sel, text, t0, t1, key=True):
    n = len(text)
    for i in range(1, n + 1):
        tt = t0 + (t1 - t0) * i / n
        js(f'tl.set("{sel}",{{textContent:{json.dumps(text[:i])}}},{tt:.3f});')
        if key and i % 3 == 0: sfx(tt, 'key' if (i // 3) % 2 else 'click', -30)

# ------------------------------------------------------------------ scene registry
SCENES = []; OV = []; WB = []; PM = []; BHI = []
BG_PURPLE = 'radial-gradient(900px 1100px at 50% 42%,#4B1D96 0%,#2B0F5C 48%,#140a33 100%)'
BG_NAVY = 'radial-gradient(900px 1100px at 50% 45%,#1b2350,#0F1224 72%)'
rng = random.Random(11)
def ambient(sid, t0, t1):
    s = ''
    for i in range(9):
        x = rng.randint(30, 980); y = rng.randint(200, 1700); r = rng.randint(70, 190); o = rng.choice([.07, .09, .12])
        s += f'<div id="{sid}_o{i}" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,0,{o}),rgba(255,255,0,0) 70%)"></div>'
        d = rng.uniform(2.2, 3.2); n = max(1, int((t1 - t0) / d))
        js(f'tl.to("#{sid}_o{i}",{{y:{rng.choice([-1, 1]) * rng.randint(60, 140)},x:{rng.choice([-1, 1]) * rng.randint(30, 90)},duration:{d:.2f},ease:"sine.inOut",repeat:{n},yoyo:true}},{t0:.3f});')
    s += (f'<svg id="{sid}_rg" width="1500" height="1500" viewBox="0 0 100 100" style="left:-210px;top:210px"><circle cx="50" cy="50" r="48" fill="none" '
          f'stroke="rgba(255,255,255,.10)" stroke-width=".18" stroke-dasharray="0.6 1.4"/></svg>')
    js(f'tl.to("#{sid}_rg",{{rotation:90,duration:{t1 - t0:.2f},ease:"none"}},{t0:.3f});')
    return s
def scene(sid, t0, t1, bg, body, fade=.28):
    SCENES.append((t0, t1, 'full', sid))
    OV.append(f'<div class="ov" id="{sid}" style="background:{bg}">{ambient(sid, t0, t1)}{body}</div>')
    A(f'#{sid}', {'opacity': 0}, {'opacity': 1}, t0, fade, 'power2.out')
    T(f'#{sid}', {'opacity': 0}, t1 - fade, fade, 'power2.in')
    SET(f'#{sid}', {'opacity': 0, 'display': 'none'}, t1 + .02); SET(f'#{sid}', {'display': 'block'}, t0 - .01)
def fg_fade(sid, t0, t1, fade=.3):
    A(f'#{sid}', {'opacity': 0}, {'opacity': 1}, t0, fade, 'power2.out'); T(f'#{sid}', {'opacity': 0}, t1 - fade, fade, 'power2.in')
    SET(f'#{sid}', {'opacity': 0, 'display': 'none'}, t1 + .02); SET(f'#{sid}', {'display': 'block'}, t0 - .01)
def bhscene(sid, t0, t1, els, fg='', fade=.3):
    SCENES.append((t0, t1, 'bh', sid)); BHI.append((sid, round(t0, 3), round(t1, 3)))
    WB.append(f'<div class="bhs" id="{sid}_w">{els}</div>')
    if fg: OV.append(f'<div class="ov bhov" id="{sid}">{fg}</div>')
    PM.append(f'<video class="clip pm" id="pm_{sid}" src="assets/matte/{sid}.webm" muted playsinline data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" data-media-start="0" data-track-index="2"></video>')
    A(f'#{sid}_w', {'opacity': 0}, {'opacity': 1}, t0, fade, 'power2.out'); T(f'#{sid}_w', {'opacity': 0}, t1 - fade, fade, 'power2.in')
    SET(f'#{sid}_w', {'opacity': 0, 'display': 'none'}, t1 + .02); SET(f'#{sid}_w', {'display': 'block'}, t0 - .01)
    if fg: fg_fade(sid, t0, t1, fade)

# ------------------------------------------------------------------ captions (two-tier, portrait)
CAPSPEC = []; CAPS = []; cap_n = [0]
FAM = ['pop', 'click', 'tink', 'blip', 'key', 'ping', 'chirp']; fam_i = [0]; last_kind = ['']
def next_fam():
    for _ in range(8):
        k = FAM[fam_i[0] % len(FAM)]; fam_i[0] += 1
        if k != last_kind[0]: last_kind[0] = k; return k
    return 'pop'
def grp(small, items, t0, hold=1.3, y=1000, fs=112, after=0.0):
    ts = []
    for i, (txt, c, tok) in enumerate(items):
        ts.append(wt(tok, max(after, t0 - .35)) if tok else (ts[-1] + .14 if ts else t0))
    CAPSPEC.append(dict(t0=min(t0, ts[0]), t1=ts[-1] + hold, small=small, items=items, ts=ts, y=y, fs=fs))
def emit_caps():
    S_ = sorted(CAPSPEC, key=lambda c: c['t0']); keep = []
    for c in S_:
        inside = [s for s in SCENES if s[2] == 'full' and s[0] - .05 <= c['ts'][0] <= s[1]]
        if inside: continue
        keep.append(c)
    for c in keep:
        for s in SCENES:
            if s[2] == 'full' and c['t0'] < s[1] <= c['ts'][0] + .3: c['t0'] = s[1]
    for i, c in enumerate(keep):
        for d in keep[i + 1:]:
            if d['t0'] >= c['t1'] + .2: break
            c['t1'] = max(c['t0'] + .35, d['t0'] - .12); c['fade'] = .08; break
        for s in SCENES:
            if s[2] == 'full' and c['t0'] < s[0] < c['t1']: c['t1'] = max(c['t0'] + .35, s[0] - .05); c['fade'] = .08
    for c in keep: emit_cap(c)
def emit_cap(c):
    n = cap_n[0]; cap_n[0] += 1; cid = f'c{n}'; fade = c.get('fade', .16)
    sm = f'<div class="sm" id="{cid}s">{c["small"]}</div>' if c['small'] else ''
    bw = ''.join(f'<span class="bw {col if col in ("y", "r") else "w"}" id="{cid}w{j}">{txt}</span> ' for j, (txt, col, tok) in enumerate(c['items']))
    CAPS.append(f'<div class="cap" id="{cid}" style="left:0;width:{W}px;top:{c["y"]}px;text-align:center;font-size:{c["fs"]}px">{sm}<div class="bg2">{bw}</div></div>')
    t0, t1 = c['t0'], c['t1']
    SET(f'#{cid}', {'opacity': 1}, t0)
    if c['small']: A(f'#{cid}s', {'opacity': 0, 'y': 16, 'filter': 'blur(8px)'}, {'opacity': 1, 'y': 0, 'filter': 'blur(0px)'}, t0, .2)
    for j, tj in enumerate(c['ts']):
        A(f'#{cid}w{j}', {'opacity': 0, 'scale': .72, 'y': 18, 'filter': 'blur(10px)'}, {'opacity': 1, 'scale': 1, 'y': 0, 'filter': 'blur(0px)'}, tj, .17, 'back.out(1.8)')
    T(f'#{cid}', {'opacity': 0, 'filter': 'blur(6px)', 'y': -10}, t1, fade, 'power2.in')
    SET(f'#{cid}', {'opacity': 0}, t1 + fade + .01)
    sfx(c['ts'][0], next_fam(), -23)

# ------------------------------------------------------------------ SVG icons
def claude_svg(sz, bid, rounded=True):
    lens = [.43, .30, .45, .28, .41, .33, .46, .29, .42, .31, .44, .27]; s = ''
    for i, l in enumerate(lens):
        a = 2 * math.pi * i / 12 + .15
        s += f'<line x1="50" y1="50" x2="{50 + l * 100 * math.cos(a):.1f}" y2="{50 + l * 100 * math.sin(a):.1f}" stroke="#FFF1E6" stroke-width="7.5" stroke-linecap="round"/>'
    bg = f'<rect width="100" height="100" rx="23" fill="{CLC}"/>' if rounded else ''
    return f'<svg id="{bid}" width="{sz}" height="{sz}" viewBox="0 0 100 100">{bg}{s}</svg>'
DRIVE_P = ('M12.01 1.485c-2.082 0-3.754.02-3.743.047.01.02 1.708 3.001 3.774 6.62l3.76 6.574h3.76c2.081 0 3.753-.02 3.742-.047-.01-.02-1.708-3.001-3.775-6.62l-3.76-6.574zm-4.76 1.73a789.828 789.861 0 0 0-3.63 6.319L0 15.868l1.89 3.298 1.885 3.297 3.62-6.335 3.63-6.334-1.88-3.287C8.1 4.704 7.255 3.22 7.25 3.214zm2.259 12.653-.203.348c-.114.198-.96 1.672-1.88 3.287a423.93 423.93 0 0 1-1.698 2.97c-.01.026 3.24.042 7.222.042h7.244l1.796-3.157c.992-1.734 1.85-3.23 1.906-3.323l.104-.167h-7.249z')
def drive_svg(sz, bid):
    return (f'<svg id="{bid}" width="{sz}" height="{sz}" viewBox="0 0 24 24"><path d="{DRIVE_P}" fill="#FFFFFF"/></svg>')
def ring_svg(i, r=56):
    c = 2 * math.pi * r
    return (f'<svg class="rg" id="rg{i}" width="150" height="150" viewBox="0 0 150 150"><circle cx="75" cy="75" r="{r}" fill="rgba(15,18,36,.55)" stroke="rgba(255,255,255,.28)" stroke-width="9"/>'
            f'<circle id="rga{i}" cx="75" cy="75" r="{r}" fill="none" stroke="{Y}" stroke-width="9" stroke-linecap="round" stroke-dasharray="{c:.1f}" stroke-dashoffset="{c:.1f}" transform="rotate(-90 75 75)"/>'
            f'<path id="rgc{i}" d="M48 77 L67 96 L103 56" fill="none" stroke="{Y}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="120" stroke-dashoffset="120"/></svg>')

# ================================================================== ANCHORS
t_sambil = wt('sambil', 0); t_jalan = wt('jalan', 0); t_dekat0 = wt('dekat', 0); t_hp0 = wt('handphone', 0)
t_dah0 = wt('dah', 0); t_proses0 = wt('proses', 0); t_3a = wt('3', 0); t_video0 = wt('video', t_3a); t_untuk0 = wt('untuk', t_video0); t_edit0 = wt('edit', t_untuk0)
t_siapa = wt('siapa', HD); t_aku = wt('aku', t_siapa)
t_banyak = wt('banyak', HD); t_gila = wt('gila', t_banyak); t_footage = wt('footage', t_gila); t_hp1 = wt('handphone', t_footage)
t_tapi = wt('tapi', t_hp1); t_tak = wt('tak', t_tapi); t_ada = wt('ada', t_tak); t_masa = wt('masa', t_ada)
t_bukan = wt('bukannya', t_masa); t_pandai = wt('pandai', t_bukan); t_tapi2 = wt('tapi', t_pandai); t_masa2 = wt('masa', t_tapi2)
t_tak2 = wt('tak', t_masa2); t_ada2 = wt('ada', t_tak2)
t_kita = wt('kita', t_ada2); t_editing = wt('editing', t_kita); t_cantik = wt('cantik', t_editing); t_suka = wt('suka', t_cantik)
t_dengan = wt('dengan', t_suka); t_branding = wt('branding', t_dengan); t_kita2 = wt('kita', t_branding)
t_sebab = wt('sebab', t_kita2); t_nasib = wt('nasib', t_sebab); t_baik = wt('baik', t_nasib); t_ada3 = wt('ada', t_baik); t_cloud = wt('cloud|claude', t_ada3)
t_dengan2 = wt('dengan', t_cloud); t_semua = wt('semua', t_dengan2); t_footage2 = wt('footage', t_semua); t_tadi = wt('tadi', t_footage2)
t_google = wt('google', t_tadi); t_drive = wt('drive', t_google); t_dulu = wt('dulu', t_drive)
t_lepas = wt('lepas', t_dulu); t_baru = wt('baru', t_lepas); t_masuk2 = wt('masuk', t_baru); t_cloud2 = wt('cloud|claude', t_masuk2); t_ai = wt('ai', t_cloud2)
t_cloud3 = wt('cloud|claude', t_ai + .05); t_install = wt('install', t_cloud3); t_hp2 = wt('handphone', t_install)
t_lepas2 = wt('lepas', t_hp2); t_terus = wt('terus', t_lepas2); t_boleh = wt('boleh', t_terus); t_prompt = wt('prompt', t_boleh)
t_untuk1 = wt('untuk', t_prompt); t_masukkan = wt('masukkan', t_untuk1); t_video1 = wt('video', t_masukkan)
t_sambil2 = wt('sambil', t_video1); t_jalan2 = wt('jalan', t_sambil2); t_hp3 = wt('handphone', t_jalan2)
t_dah1 = wt('dah', t_hp3); t_proses1 = wt('proses', t_dah1); t_3b = wt('3', t_proses1); t_video2 = wt('video', t_3b); t_untuk2 = wt('untuk', t_video2); t_editing2 = wt('editing', t_untuk2)
t_macam = wt('macam', t_editing2); t_best = wt('best', t_macam); t_ke = wt('ke', t_best); t_tak3 = wt('tak', t_ke); t_best2 = wt('best', t_tak3 + .05)
t_nak = wt('nak', t_best2); t_belajar = wt('belajar', t_nak); t_tak4 = wt('tak', t_belajar)
print('anchors ok')

# ================================================================== VIDEO CARDS (hook + BH3)
VT = [3]
def vcard(pref, i, src, x, y, w, h, rot, t0, t1):
    VT[0] += 1; G0(f'#{pref}{i}', {'rotation': rot})
    return (f'<div class="vc" id="{pref}{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<video class="clip pv" id="{pref}v{i}" src="{src}" muted playsinline data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" data-media-start="0" data-track-index="{VT[0]}" style="width:{w}px;height:{h}px"></video>'
            f'<div class="vcs" id="{pref}s{i}" style="width:{w}px;height:{h}px"></div>'
            f'<div class="rgw" style="left:{(w - 150) // 2}px;top:{(h - 150) // 2}px">{ring_svg(pref + str(i))}</div></div>')
def cards_beat(pref, cards, t_start, step, fill, counter_id):
    """cards: [(x,y,w,h,rot,src)]; pop at t_start+k*step, ring fills for `fill` s, check pops, counter ticks"""
    c = 2 * math.pi * 56; done = []
    for k, (x, y, w, h, rot, src) in enumerate(cards):
        tp = t_start + k * step; td = tp + fill + k * .12
        A(f'#{pref}{k}', {'opacity': 0, 'scale': .55, 'y': 90, 'filter': 'blur(12px)'}, {'opacity': 1, 'scale': 1, 'y': 0, 'filter': 'blur(0px)'}, tp, .38, 'back.out(1.6)')
        A(f'#rga{pref}{k}', {'strokeDashoffset': c}, {'strokeDashoffset': 0}, tp + .12, fill, 'power1.inOut')
        T(f'#rga{pref}{k}', {'opacity': 0}, td, .08)
        A(f'#rgc{pref}{k}', {'strokeDashoffset': 120}, {'strokeDashoffset': 0}, td, .22, 'power2.out')
        T(f'#{pref}s{k}', {'backgroundColor': 'rgba(53,224,138,.12)'}, td, .2)
        T(f'#rg{pref}{k}', {'scale': 1.25}, td, .12, 'power2.out'); T(f'#rg{pref}{k}', {'scale': 1}, td + .12, .2, 'power2.in')
        T(f'#rg{pref}{k}', {'opacity': 0}, td + .9, .3)
        done.append(td)
    return done

# ================================================================== SCENE 0: HOOK (behind head, matte 1.95 -> HD)
hk_t0 = t_proses0 - .22
hk_cards = [(24, 470, 300, 534, -8, 'assets/vid/ex1.mp4'), (756, 430, 300, 534, 7, 'assets/vid/ex2.mp4'), (390, 150, 300, 534, 0, 'assets/vid/ex3.mp4')]
els = ''.join(vcard('hk', i, s, x, y, w, h, r, hk_t0, HD) for i, (x, y, w, h, r, s) in enumerate(hk_cards))
fg = ('<div class="badge" id="hkb" style="left:300px;top:196px;width:480px"><span id="hkbn">0</span><em>/3 VIDEO</em><b id="hkbc">&#10003;</b></div>')
bhscene('s_hook', hk_t0, HD, els, fg, fade=.2)
dn = cards_beat('hk', hk_cards, t_proses0, .2, .85, 'hkbn')
A('#hkb', {'opacity': 0, 'y': -30, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, t_proses0, .3, 'back.out(1.6)')
for k, td in enumerate(dn):
    SET('#hkbn', {'textContent': str(k + 1)}, td + .05); T('#hkb', {'scale': 1.12}, td, .08); T('#hkb', {'scale': 1}, td + .08, .18)
    sfx(td, ['ting', 'tink', 'ting'][k], -22)
T('#hkb', {'color': Y, 'boxShadow': f'0 0 50px {Y}aa'}, dn[-1], .2)
A('#hkbc', {'opacity': 0, 'scale': 0}, {'opacity': 1, 'scale': 1}, dn[-1] + .05, .25, 'back.out(2.2)')
G0('#hkbc', {'opacity': 0})
sfx(t_3a + .15, 'boom', -14); sfx(HD - .1, 'zoom', -18)
for k in range(3): sfx(t_proses0 + k * .2, ['pop', 'click', 'blip'][k], -24)
shake('#cam', t_3a, 10, 4)

# ================================================================== BH1: wall of footage + clock ('banyak gila footage ... tak ada masa')
w1_t0 = t_banyak - .12; w1_t1 = t_bukan - .1
tiles = ''; thumbs = [f't{n:02d}' for n in range(1, 22)]
dur_lab = ['0:42', '1:07', '0:18', '2:31', '0:55', '0:12', '3:04', '0:37', '1:48', '0:26']
ti = 0
for r in range(5):
    row = ''
    for c in range(8):
        badge = '' if r in (2, 3) else '<i>' + dur_lab[(r * 2 + c) % 10] + '</i>'
        row += (f'<div class="wt" style="left:{c * 214}px"><img src="assets/thumbs_dim/{thumbs[(r * 3 + c * 2) % 21]}.jpg">{badge}<b></b></div>'); ti += 1
    tiles += f'<div class="wrow" id="wr{r}" style="top:{r * 372 + 20}px;left:{-120 - r * 70}px">{row}</div>'
ck = (f'<div class="clk" id="clk" style="left:800px;top:230px"><svg width="250" height="250" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="rgba(15,18,36,.88)" stroke="{RED}" stroke-width="3.5"/>'
      + ''.join(f'<line x1="50" y1="9" x2="50" y2="{15 if k % 3 else 19}" stroke="#fff" stroke-width="{2.2 if k % 3 == 0 else 1.2}" transform="rotate({k * 30} 50 50)"/>' for k in range(12))
      + f'<line id="clh1" x1="50" y1="50" x2="50" y2="22" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/><line id="clh2" x1="50" y1="50" x2="50" y2="34" stroke="{RED}" stroke-width="4.6" stroke-linecap="round"/><circle cx="50" cy="50" r="3.6" fill="#fff"/></svg></div>')
bhscene('s_wall', w1_t0, w1_t1, f'<div id="wallwrap">{tiles}</div>{ck}', '', fade=.3)
js('gsap.set("#wallwrap",{transformOrigin:"540px 960px",rotation:-5,scale:1.2});')
for r, tt in enumerate([t_banyak, t_gila, t_footage, t_footage + .22, t_hp1]):
    A(f'#wr{r}', {'opacity': 0, 'scale': .8, 'x': 60 if r % 2 else -60}, {'opacity': 1, 'scale': 1, 'x': 0}, tt, .35, 'back.out(1.4)')
    T(f'#wr{r}', {'x': (-1) ** r * 200}, tt + .37, w1_t1 - tt, 'none')
sfx(t_banyak, 'shutter', -20)
A('#clk', {'opacity': 0, 'scale': .3, 'rotation': -40}, {'opacity': 1, 'scale': 1, 'rotation': 0}, t_masa - .1, .4, 'back.out(1.7)')
js(f'tl.to("#clh1",{{rotation:1080,svgOrigin:"50 50",duration:{w1_t1 - t_masa:.2f},ease:"power1.in"}},{t_masa:.3f});')
js(f'tl.to("#clh2",{{rotation:90,svgOrigin:"50 50",duration:{w1_t1 - t_masa:.2f},ease:"power1.in"}},{t_masa:.3f});')
T('#clk', {'filter': f'drop-shadow(0 0 30px {RED})'}, t_masa, .3); sfx(t_masa, 'tink', -20); sfx(t_masa + .15, 'ratchet', -26)

# ================================================================== S3 stage: pandai edit vs masa tak ada
s3_t0 = t_bukan - .1; s3_t1 = t_kita - .22
blocks = ''
cols = [Y, '#fff', '#8E7CFF', Y, '#fff']
for tr in range(3):
    x = 40
    for b in range(5):
        wv = [150, 90, 200, 120, 160][(b + tr * 2) % 5]
        blocks += f'<div class="tb" style="left:{x}px;top:{70 + tr * 96}px;width:{wv}px;background:{cols[(b + tr) % 5]};opacity:{.95 if (b + tr) % 2 else .75}"></div>'; x += wv + 22
body = ('<div class="glass" id="tlc" style="left:60px;top:230px;width:960px;height:420px"><div class="tdots"><i></i><i></i><i></i></div>' + blocks +
        '<div id="phd" style="position:absolute;left:44px;top:46px;width:5px;height:340px;background:#FFFF00;box-shadow:0 0 22px #FFFF00;border-radius:3px"></div></div>'
        '<div class="okp" id="okp" style="left:200px;top:700px;width:680px"><b>&#10003;</b>PANDAI EDIT</div>'
        f'<div class="clk2" id="ck2" style="left:340px;top:790px"><svg width="400" height="400" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="rgba(15,18,36,.6)" stroke="rgba(255,255,255,.25)" stroke-width="3"/>'
        f'<circle id="ck2a" cx="50" cy="50" r="46" fill="none" stroke="{RED}" stroke-width="4" stroke-linecap="round" stroke-dasharray="289" stroke-dashoffset="0" transform="rotate(-90 50 50)"/>'
        + ''.join(f'<line x1="50" y1="9" x2="50" y2="14" stroke="#fff" stroke-width="1.4" transform="rotate({k * 30} 50 50)"/>' for k in range(12))
        + f'<line id="ck2h" x1="50" y1="50" x2="50" y2="20" stroke="#fff" stroke-width="3" stroke-linecap="round"/><circle cx="50" cy="50" r="3.4" fill="#fff"/></svg></div>'
        '<div class="xw" id="mtk" style="left:0;top:1215px;width:1080px"><span class="r2">MASA</span> <span class="r2">TAK ADA</span></div>')
scene('s_tl', s3_t0, s3_t1, BG_PURPLE, body)
A('#tlc', {'opacity': 0, 'y': 80, 'scale': .9}, {'opacity': 1, 'y': 0, 'scale': 1}, s3_t0 + .05, .4)
js(f'tl.fromTo("#phd",{{x:0}},{{x:870,duration:.85,ease:"power1.inOut",immediateRender:false}},{t_pandai - .25:.3f});')
A('#okp', {'opacity': 0, 'scale': .6, 'y': 30}, {'opacity': 1, 'scale': 1, 'y': 0}, t_pandai, .3, 'back.out(1.8)'); sfx(t_pandai, 'ting', -22); sfx(t_pandai - .25, 'key', -28)
T('#tlc', {'opacity': .22, 'scale': .86, 'y': -40}, t_tapi2 - .05, .35, 'power2.inOut'); T('#okp', {'opacity': 0, 'y': -40}, t_tapi2, .3, 'power2.in')
A('#ck2', {'opacity': 0, 'scale': .4, 'rotation': -60}, {'opacity': 1, 'scale': 1, 'rotation': 0}, t_masa2 - .12, .45, 'back.out(1.5)')
A('#ck2a', {'strokeDashoffset': 0}, {'strokeDashoffset': 289}, t_masa2, t_ada2 - t_masa2 + .1, 'power1.in')
js(f'tl.to("#ck2h",{{rotation:1260,svgOrigin:"50 50",duration:{t_ada2 - t_masa2 + .2:.2f},ease:"power1.in"}},{t_masa2:.3f});')
A('#mtk', {'opacity': 0, 'scale': 1.4, 'filter': 'blur(14px)'}, {'opacity': 1, 'scale': 1, 'filter': 'blur(0px)'}, t_tak2 - .05, .22, 'power4.out')
shake('#mtk', t_tak2, 12, 4); sfx(t_tak2, 'boom', -16); sfx(s3_t0, 'slide', -24); sfx(t_masa2, 'ratchet', -26)

# ================================================================== BH2 branding tiles
b_t0 = t_kita - .1; b_t1 = t_nasib - .08
ic_pal = ('<div class="sw"><i style="background:#FFFF00"></i><i style="background:#fff"></i><i style="background:#8E7CFF"></i></div>')
ic_aa = '<div class="aa">Aa</div>'
ic_logo = f'<svg width="120" height="120" viewBox="0 0 100 100"><polygon points="50,8 88,29 88,71 50,92 12,71 12,29" fill="none" stroke="{Y}" stroke-width="7" stroke-linejoin="round"/><circle cx="50" cy="50" r="14" fill="{Y}"/></svg>'
ic_cap = '<div class="cp"><span>TEKS</span><em>NEON</em></div>'
tl4 = [('bt0', ic_pal, -30, 300, 'PALET', t_editing), ('bt1', ic_aa, 870, 270, 'FONT', t_cantik), ('bt2', ic_logo, -30, 610, 'LOGO', t_dengan), ('bt3', ic_cap, 870, 600, 'CAPTION', t_branding)]
els = ''.join(f'<div class="glass bt" id="{i}" style="left:{x}px;top:{y}px;width:230px;height:250px"><div class="btin">{ic}</div><div class="btl">{lb}</div></div>' for i, ic, x, y, lb, _ in tl4)
bhscene('s_brand', b_t0, b_t1, els, '', fade=.3)
for k, (i, ic, x, y, lb, tt) in enumerate(tl4):
    A(f'#{i}', {'opacity': 0, 'scale': .4, 'y': 60, 'rotation': -10 + 6 * k}, {'opacity': 1, 'scale': 1, 'y': 0, 'rotation': (-4 if k % 2 == 0 else 4)}, tt - .02, .4, 'back.out(1.7)')
    js(f'tl.to("#{i}",{{y:{-18 if k % 2 else 18},duration:1.1,ease:"sine.inOut",repeat:2,yoyo:true}},{tt + .45:.3f});')
    sfx(tt, ['blip', 'ping', 'chirp', 'tink'][k], -23)

# ================================================================== STAGE: Claude hero + Google Drive
cl_t0 = t_baik + .1; cl_t1 = t_lepas - .08
body = (f'<div class="rays" id="rays"></div><div id="ic1" style="left:350px;top:470px">{claude_svg(380, "ic1s")}</div>'
        '<div class="xw sm2" id="nb" style="left:0;top:380px;width:1080px">sekarang ni, ada</div>'
        '<div class="xw" id="adc" style="left:0;top:940px;width:1080px"><span class="y2">CLAUDE</span></div>'
        '<div class="plane" id="pl1" style="left:110px;top:300px;width:860px"><img src="assets/img/drive1.jpg" style="width:860px"></div>'
        '<div class="plane" id="pl2" style="left:150px;top:760px;width:780px"><img src="assets/img/drive2.jpg" style="width:780px"></div>'
        f'<div class="dlab" id="dlab" style="left:0;top:196px;width:1080px">{drive_svg(54, "dlg")}<span>GOOGLE DRIVE</span></div>'
        + ''.join(f'<img class="ft" id="ft{k}" src="assets/thumbs/t{k + 1:02d}.jpg" style="left:{[80, 380, 700, 240, 560][k]}px;top:1500px">' for k in range(5))
        + '<div class="pulse" id="pul" style="left:100px;top:380px"></div>')
scene('s_cl', cl_t0, cl_t1, BG_PURPLE, body)
G0('#rays', {'opacity': 0})
A('#ic1', {'opacity': 0, 'scale': .2, 'rotation': -70}, {'opacity': 1, 'scale': 1, 'rotation': 0}, t_ada3 - .1, .55, 'back.out(1.5)')
A('#nb', {'opacity': 0, 'y': 20, 'filter': 'blur(8px)'}, {'opacity': 1, 'y': 0, 'filter': 'blur(0px)'}, cl_t0 + .1, .25)
A('#rays', {'opacity': 0, 'scale': .5}, {'opacity': .9, 'scale': 1}, t_ada3, .5)
js(f'tl.to("#rays",{{rotation:50,duration:{t_dengan2 - t_ada3:.2f},ease:"none"}},{t_ada3:.3f});')
A('#adc', {'opacity': 0, 'scale': 1.6, 'filter': 'blur(16px)'}, {'opacity': 1, 'scale': 1, 'filter': 'blur(0px)'}, t_cloud - .05, .22, 'power4.out')
shake('#adc', t_cloud, 10, 4); sfx(t_cloud - .02, 'boom', -12); sfx(t_ada3 - .1, 'shing', -24)
for sel in ('#ic1', '#adc', '#nb', '#rays'):
    T(sel, {'opacity': 0, 'scale': 1.25, 'filter': 'blur(14px)'}, t_dengan2 - .02, .3, 'power2.in')
A('#pl1', {'opacity': 0, 'rotationX': 40, 'rotationY': -35, 'y': 200, 'scale': .8}, {'opacity': 1, 'rotationX': 10, 'rotationY': -12, 'y': 0, 'scale': 1}, t_dengan2 + .05, .6, 'power3.out')
A('#pl2', {'opacity': 0, 'rotationX': 40, 'rotationY': 30, 'y': 260, 'scale': .8}, {'opacity': 1, 'rotationX': 10, 'rotationY': 10, 'y': 0, 'scale': 1}, t_dengan2 + .3, .6, 'power3.out')
G0('#pl1', {'transformPerspective': 1500, 'rotationZ': 2}); G0('#pl2', {'transformPerspective': 1500, 'rotationZ': -2})
T('#pl1', {'rotationY': -4, 'x': 14}, t_dengan2 + .7, t_dulu - t_dengan2, 'sine.inOut'); T('#pl2', {'rotationY': 4, 'x': -14}, t_dengan2 + .9, t_dulu - t_dengan2, 'sine.inOut')
sfx(t_dengan2, 'slide', -22)
for k, tt in enumerate([t_semua, t_footage2, t_footage2 + .16, t_tadi, t_tadi + .12]):
    A(f'#ft{k}', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, tt - .02, .12)
    js(f'tl.to("#ft{k}",{{x:{[15, -285, -605, -145, -465][k]},y:-1060,scale:.16,opacity:0,duration:.55,ease:"power2.in"}},{tt + .1:.3f});')
    sfx(tt + .55, ['pop', 'click', 'blip', 'pop', 'tink'][k], -26)
A('#pul', {'opacity': 0, 'scale': .3}, {'opacity': .9, 'scale': 1.6}, t_semua + .5, .5)
T('#pul', {'opacity': 0}, t_semua + 1.1, .4)
A('#dlab', {'opacity': 0, 'y': -30, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, t_google - .05, .3, 'back.out(1.7)'); sfx(t_google, 'ting', -22)

# ================================================================== BH: Drive -> Claude flow
f_t0 = t_lepas - .05; f_t1 = t_cloud3 - .12
P0, P1, P2 = (190, 560), (540, 120), (890, 560)
def bez(u): return ((1 - u) ** 2 * P0[0] + 2 * (1 - u) * u * P1[0] + u * u * P2[0], (1 - u) ** 2 * P0[1] + 2 * (1 - u) * u * P1[1] + u * u * P2[1])
els = (f'<svg id="flsv" width="1080" height="1000" viewBox="0 0 1080 1000" style="left:0;top:0"><path id="flp" d="M{P0[0]} {P0[1]} Q{P1[0]} {P1[1]} {P2[0]} {P2[1]}" fill="none" stroke="{Y}" stroke-width="7" stroke-linecap="round" stroke-dasharray="14 18"/></svg>'
       f'<div class="glass ic" id="fdr" style="left:60px;top:470px;width:260px;height:260px;display:flex;align-items:center;justify-content:center;background:rgba(15,18,36,.78)">{drive_svg(150, "fdrs")}</div>'
       f'<div id="fcl" style="left:760px;top:470px">{claude_svg(260, "fcls")}</div>'
       + ''.join(f'<img class="fc" id="fc{k}" src="assets/thumbs/t{k + 6:02d}.jpg">' for k in range(4)))
bhscene('s_flow', f_t0, f_t1, els, '', fade=.25)
A('#fdr', {'opacity': 0, 'scale': .4}, {'opacity': 1, 'scale': 1}, t_lepas - .02, .35, 'back.out(1.7)')
A('#flsv', {'opacity': 0}, {'opacity': 1}, t_baru - .05, .3)
A('#fcl', {'opacity': 0, 'scale': .3, 'rotation': -60}, {'opacity': 1, 'scale': 1, 'rotation': 0}, t_cloud2 - .2, .45, 'back.out(1.6)')
for k in range(4):
    ts = t_masuk2 - .05 + k * .2
    kf = [{'x': round(bez(u / 6)[0] - 60 - 0), 'y': round(bez(u / 6)[1] - 107 - (0)), 'duration': .1, 'ease': 'none'} for u in range(1, 7)]
    G0(f'#fc{k}', {'opacity': 0, 'x': round(P0[0] - 60), 'y': round(P0[1] - 107), 'scale': .6})
    js(f'tl.to("#fc{k}",{{opacity:1,duration:.1}},{ts:.3f});'); js(f'tl.to("#fc{k}",{{keyframes:{fj(kf)}}},{ts:.3f});'); js(f'tl.to("#fc{k}",{{opacity:0,scale:.2,duration:.12}},{ts + .6:.3f});')
    sfx(ts + .65, ['pop', 'click', 'tink', 'blip'][k], -28)
sfx(t_baru, 'swish_up', -24); sfx(t_cloud2, 'ping', -22)
T('#fcl', {'scale': 1.14}, t_ai + .08, .15); T('#fcl', {'scale': 1}, t_ai + .23, .25)

# ================================================================== BH: install (real phone stays in footage)
i_t0 = t_cloud3 - .08; i_t1 = t_lepas2 - .1
import math as _m
_c = 2 * _m.pi * 118
els = ('<svg id="isv" width="300" height="300" viewBox="0 0 300 300" style="left:770px;top:190px"><circle cx="150" cy="150" r="118" fill="rgba(15,18,36,.55)" stroke="rgba(255,255,255,.28)" stroke-width="10"/>'
       f'<circle id="ipg" cx="150" cy="150" r="118" fill="none" stroke="{Y}" stroke-width="10" stroke-linecap="round" stroke-dasharray="{_c:.1f}" stroke-dashoffset="{_c:.1f}" transform="rotate(-90 150 150)"/></svg>'
       f'<div id="icf" style="left:820px;top:240px">{claude_svg(200, "icfs")}</div>'
       '<div class="ph-ok" id="phok" style="left:985px;top:235px;width:64px;height:64px;line-height:64px;font-size:40px">&#10003;</div>'
       '<div class="glass" id="ichip" style="left:740px;top:495px;width:300px;height:96px;border-radius:999px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:44px;color:#fff;letter-spacing:3px;background:rgba(15,18,36,.7)">INSTALL</div>')
SCENES.append((i_t0, i_t1, 'fg', 's_inst')); OV.append(f'<div class="ov bhov" id="s_inst">{els}</div>'); fg_fade('s_inst', i_t0, i_t1, .25)
A('#isv', {'opacity': 0, 'scale': .4}, {'opacity': 1, 'scale': 1}, t_cloud3 - .02, .35, 'back.out(1.7)')
A('#icf', {'opacity': 0, 'scale': .3, 'rotation': -50}, {'opacity': 1, 'scale': 1, 'rotation': 0}, t_cloud3 - .02, .4, 'back.out(1.7)')
A('#ichip', {'opacity': 0, 'x': -60}, {'opacity': 1, 'x': 0}, t_install - .05, .3, 'back.out(1.5)')
A('#ipg', {'strokeDashoffset': _c}, {'strokeDashoffset': 0}, t_install, t_hp2 - t_install + .1, 'power1.inOut')
A('#phok', {'opacity': 0, 'scale': 0}, {'opacity': 1, 'scale': 1}, t_hp2 + .12, .25, 'back.out(2.4)')
T('#ichip', {'backgroundColor': 'rgba(53,224,138,.35)'}, t_hp2 + .12, .2)
sfx(t_install, 'pop', -24); sfx(t_hp2 + .1, 'ting', -20)

# ================================================================== STAGE: prompt
p_t0 = t_lepas2 - .06; p_t1 = t_sambil2 - .1
body = (f'<div id="pic" style="left:445px;top:236px">{claude_svg(190, "pics")}</div>'
        '<div class="xw sm2" id="pl_a" style="left:0;top:470px;width:1080px">terus boleh</div>'
        '<div class="xw" id="pl_b" style="left:0;top:535px;width:1080px"><span class="y2">PROMPT</span></div>'
        '<div class="glass cmp" id="cmp" style="left:60px;top:860px;width:960px;height:230px"><div class="ph" id="cph" data-layout-allow-overlap>Tanya Claude apa-apa…</div><div class="tx" id="ctx" data-layout-allow-overlap></div><div class="snd" id="snd">&#10148;</div></div>'
        '<div class="att" id="att" style="left:60px;top:1130px;width:960px"></div>'
        + ''.join(f'<img class="ft2" id="at{k}" src="assets/thumbs/t{k + 12:02d}.jpg" style="left:{[120, 420, 720][k]}px;top:1560px">' for k in range(3))
        + ''.join(f'<div class="chp" id="chp{k}" style="left:{70 + k * 190}px;top:1135px"><img src="assets/thumbs/t{k + 12:02d}.jpg"><span>VIDEO {k + 1}</span></div>' for k in range(3)))
scene('s_pr', p_t0, p_t1, BG_NAVY, body)
A('#pic', {'opacity': 0, 'scale': .3, 'y': 40}, {'opacity': 1, 'scale': 1, 'y': 0}, p_t0 + .12, .45, 'back.out(1.6)')
A('#cmp', {'opacity': 0, 'y': 120}, {'opacity': 1, 'y': 0}, p_t0 + .2, .45)
A('#pl_a', {'opacity': 0, 'y': 20, 'filter': 'blur(8px)'}, {'opacity': 1, 'y': 0, 'filter': 'blur(0px)'}, t_terus - .05, .25)
A('#pl_b', {'opacity': 0, 'scale': 1.6, 'filter': 'blur(14px)'}, {'opacity': 1, 'scale': 1, 'filter': 'blur(0px)'}, t_prompt - .05, .22, 'power4.out')
shake('#pl_b', t_prompt, 10, 4); sfx(t_prompt - .02, 'boom', -16)
T('#cph', {'opacity': 0}, t_boleh - .1, .15)
typed('#ctx', 'Edit semua footage ni ikut branding aku', t_boleh + .05, t_untuk1 + .05)
for k in range(3):
    tt = t_masukkan - .05 + k * .2
    A(f'#at{k}', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, tt, .12)
    js(f'tl.to("#at{k}",{{x:{[-30, -140, -250][k] + 0},y:-420,scale:.5,opacity:0,duration:.4,ease:"power2.in"}},{tt + .14:.3f});')
    A(f'#chp{k}', {'opacity': 0, 'scale': .4}, {'opacity': 1, 'scale': 1}, tt + .45, .25, 'back.out(1.8)'); sfx(tt + .5, ['pop', 'click', 'blip'][k], -26)
T('#snd', {'scale': 1.3, 'backgroundColor': '#FFFF00'}, t_video1, .15); T('#snd', {'scale': 1}, t_video1 + .15, .25); sfx(t_video1, 'chirp', -22); sfx(p_t0, 'slide', -24)

# ================================================================== BH3: 3 videos while walking
c_t0 = t_proses1 - .2
c_cards = [(20, 520, 330, 586, -7, 'assets/vid/ex1.mp4'), (730, 470, 330, 586, 7, 'assets/vid/ex2.mp4'), (375, 130, 330, 586, 0, 'assets/vid/ex3.mp4')]
c_t1 = t_macam - .14
els = ''.join(vcard('bc', i, s, x, y, w, h, r, c_t0, c_t1) for i, (x, y, w, h, r, s) in enumerate(c_cards))
fg = ('<div class="badge" id="bcb" style="left:300px;top:196px;width:480px"><span id="bcbn">0</span><em>/3 VIDEO</em><b id="bcbc">&#10003;</b></div>')
bhscene('s_3v', c_t0, c_t1, els, fg, fade=.25)
dn2 = cards_beat('bc', c_cards, t_proses1, .22, .7, 'bcbn')
A('#bcb', {'opacity': 0, 'y': -30, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, t_proses1, .3, 'back.out(1.6)')
for k, td in enumerate(dn2):
    SET('#bcbn', {'textContent': str(k + 1)}, td + .05); T('#bcb', {'scale': 1.12}, td, .08); T('#bcb', {'scale': 1}, td + .08, .18)
    sfx(td, ['ting', 'tink', 'ting'][k], -22)
T('#bcb', {'color': Y, 'boxShadow': f'0 0 50px {Y}aa'}, dn2[-1], .2)
A('#bcbc', {'opacity': 0, 'scale': 0}, {'opacity': 1, 'scale': 1}, dn2[-1] + .05, .25, 'back.out(2.2)')
G0('#bcbc', {'opacity': 0})
sfx(t_3b, 'stamp', -14); sfx(t_3b, 'boom', -16)
for k in range(3): sfx(t_proses1 + k * .22, ['pop', 'click', 'blip'][k], -24)

# ================================================================== CAPTIONS
grp('sambil', [('JALAN', 'y', 'jalan')], t_sambil - .02, 0.9, fs=140)
grp('macam ni, dekat dalam', [('HANDPHONE', 'y', 'handphone')], t_dekat0 - .2, 0.55, fs=116)
grp('dah proses', [('3', 'y', '3'), ('VIDEO', 'w', 'video')], t_dah0, 1.0, fs=150)
grp('untuk', [('EDITING', 'y', 'edit')], t_untuk0, 0.8, fs=128)
grp('siapa dekat sini yang', [('MACAM', 'w', 'macam'), ('AKU?', 'y', None)], t_siapa, 1.0, fs=128, after=HD)
grp('footage dalam handphone', [('BANYAK', 'w', 'banyak'), ('GILA', 'y', 'gila')], t_banyak, 1.8, fs=124, after=HD)
grp('tapi', [('TAK ADA', 'r', 'tak'), ('MASA', 'r', 'masa')], t_tapi, 0.9, fs=112, after=t_hp1)
grp('kita nak editing yang', [('CANTIK', 'y', 'cantik')], t_kita, 1.0, fs=140, after=t_ada2)
grp('dah suka dengan', [('BRANDING', 'y', 'branding'), ('KITA', 'w', 'kita')], t_suka, 1.0, fs=100, after=t_cantik)
grp('sebab tu', [('NASIB', 'y', 'nasib'), ('BAIK', 'w', 'baik')], t_sebab, 0.9, fs=124)
grp('lepas tu baru masuk dalam', [('CLAUDE', 'y', 'cloud|claude'), ('AI', 'w', 'ai')], t_lepas, 1.6, fs=124, after=t_dulu)
grp('install dekat dalam', [('HANDPHONE', 'y', 'handphone')], t_install, 1.0, fs=116, after=t_cloud3)
grp('sambil jalan macam ni, dekat dalam', [('HANDPHONE', 'y', 'handphone')], t_sambil2, 1.5, fs=116, after=t_video1)
grp('dah proses', [('3', 'y', '3'), ('VIDEO', 'w', 'video')], t_dah1, 1.4, fs=150, after=t_hp3)
grp('untuk', [('EDITING', 'y', 'editing')], t_untuk2, 0.9, fs=128, after=t_video2)
grp('macam, best ke', [('TAK BEST?', 'y', 'tak')], t_macam, 0.9, fs=124, after=t_editing2)
grp('nak', [('BELAJAR TAK?', 'y', 'belajar')], t_nak - .05, 1.4, fs=116, after=t_best2)
emit_caps()

# ================================================================== CAMERA (portrait: half-strength, only in free windows)
blocked = [(s[0], s[1]) for s in SCENES]
js(f'gsap.set("#cam",{{transformOrigin:"540px 620px",scale:1}});')
cam = [(0.0, 1.0, 1.10, 1.9, 'sine.inOut'), (1.9, 1.10, 1.22, t_3a - 1.9, 'power2.in'), (t_3a + .1, 1.22, 1.22, .001, 'none'),
       (t_3a + .15, 1.22, 1.0, HD - .05 - t_3a - .15, 'sine.inOut'),
       (HD + .05, 1.0, 1.08, .8, 'sine.inOut'), (HD + .9, 1.08, 1.0, .3, 'sine.inOut'),
       (b_t1 + .05, 1.0, 1.06, cl_t0 - b_t1 - .1, 'sine.inOut'),
       (t_sambil2, 1.0, 1.06, .9, 'sine.inOut'), (t_sambil2 + .95, 1.06, 1.0, c_t0 - .05 - t_sambil2 - .95, 'sine.inOut'),
       (t_macam - .02, 1.0, 1.12, DUR - t_macam, 'sine.inOut')]
for t, a, b, d, e in cam:
    js(f'tl.fromTo("#cam",{{scale:{a}}},{{scale:{b},duration:{max(d, .001):.3f},ease:"{e}",immediateRender:false}},{t:.3f});')
js(f'tl.set("#cam",{{scale:1}},{cl_t0 + .02:.3f});')
sfx(HD + .05, 'zoom_in', -22)
print('captions', cap_n[0])

# ================================================================== CSS + HTML
CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0F1224;font-family:Poppins,sans-serif}
#root{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden;background:#000}
#cam{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0}
#base{position:absolute;left:0;top:0;width:1080px;height:1920px}
.ov{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;display:none;overflow:hidden;z-index:20;font-family:Poppins,sans-serif}
.ov > *{position:absolute}
.cap{position:absolute;z-index:100;opacity:0;font-family:Poppins,sans-serif}
.sm{font-weight:500;color:#fff;line-height:1.15;font-size:.42em;text-shadow:0 0 .1em rgba(255,255,255,.7),0 0 .35em rgba(255,255,255,.3),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}
.bg2{font-weight:800;line-height:1.04;text-transform:uppercase;letter-spacing:-.012em;white-space:nowrap}
.bw{display:inline-block;transform-origin:50% 70%}
.y{color:#FFFF00;font-weight:800;text-shadow:0 0 .05em rgba(255,255,0,.95),0 0 .2em rgba(255,255,0,.6),0 0 .45em rgba(255,255,0,.35),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}
.r{color:#FF4D4D;font-weight:800;text-shadow:0 0 .05em rgba(255,77,77,.95),0 0 .2em rgba(255,77,77,.6),0 0 .45em rgba(255,77,77,.35),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}
.w{color:#fff;font-weight:600;text-shadow:0 0 .06em rgba(255,255,255,.9),0 0 .2em rgba(255,255,255,.5),0 0 .45em rgba(255,255,255,.28),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}
.xw{position:absolute;text-align:center;font-weight:800;text-transform:uppercase;font-size:130px;line-height:1.05;white-space:nowrap}
.xw.sm2{font-size:56px;font-weight:500;text-transform:none;color:#fff;text-shadow:0 0 .2em rgba(255,255,255,.5)}
.y2{color:#FFFF00;text-shadow:0 0 .05em rgba(255,255,0,.95),0 0 .2em rgba(255,255,0,.6),0 0 .45em rgba(255,255,0,.35),0 .06em .1em rgba(0,0,0,.6)}
.r2{color:#FF4D4D;font-size:110px;text-shadow:0 0 .05em rgba(255,77,77,.95),0 0 .2em rgba(255,77,77,.6),0 .06em .1em rgba(0,0,0,.6)}
.glass{position:absolute;border-radius:36px;background:linear-gradient(160deg,rgba(255,255,255,.14),rgba(255,255,255,.04));border:2px solid rgba(255,255,255,.25);box-shadow:0 30px 80px rgba(0,0,0,.5),inset 0 0 40px rgba(255,255,255,.05)}
.bhs{position:absolute;left:0;top:0;width:1080px;height:1920px;display:none}
.bhs > *{position:absolute}
.bhov{background:transparent}
.pm{position:absolute;left:0;top:0;width:1080px;height:1920px}
.vc{position:absolute;border-radius:30px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.6),0 0 0 3px rgba(255,255,255,.35)}
.pv{position:absolute;left:0;top:0;object-fit:cover}
.vcs{position:absolute;left:0;top:0;border-radius:30px;background:rgba(10,12,28,.18)}
.rgw{position:absolute;width:150px;height:150px}
.rg{position:absolute;left:0;top:0}
.badge{position:absolute;display:flex;align-items:baseline;justify-content:center;gap:10px;height:96px;border-radius:999px;background:rgba(15,18,36,.82);border:3px solid rgba(255,255,255,.35);color:#fff;font-weight:800;font-size:50px;line-height:96px;text-shadow:0 0 .2em rgba(255,255,255,.4)}
.badge span{font-size:62px;color:#FFFF00}.badge em{font-style:normal;font-size:44px}.badge b{color:#35E08A;font-size:50px;margin-left:8px}
.wrow{position:absolute;width:1760px;height:346px}
.wt{position:absolute;top:0;width:194px;height:346px;border-radius:18px;overflow:hidden;border:3px solid rgba(255,255,255,.7);background:#222}
.wt img{width:194px;height:346px;object-fit:cover;display:block}
.wt i{position:absolute;right:10px;bottom:10px;font-style:normal;font-weight:600;font-size:22px;color:#fff;background:rgba(0,0,0,.65);padding:2px 10px;border-radius:8px}
.wt b{position:absolute;left:10px;top:10px;width:0;height:0;border-left:20px solid #fff;border-top:12px solid transparent;border-bottom:12px solid transparent;opacity:.9}
#wallwrap{position:absolute;left:0;top:0;width:1080px;height:1920px}
.clk{position:absolute;filter:drop-shadow(0 20px 30px rgba(0,0,0,.6))}
.tb{position:absolute;height:70px;border-radius:14px}
.tdots{position:absolute;left:24px;top:14px}.tdots i{display:inline-block;width:14px;height:14px;border-radius:50%;background:rgba(255,255,255,.4);margin-right:8px}
.okp{position:absolute;display:flex;align-items:center;justify-content:center;gap:22px;height:100px;border-radius:999px;background:rgba(53,224,138,.18);border:3px solid #35E08A;color:#fff;font-weight:800;font-size:54px;box-shadow:0 0 40px rgba(53,224,138,.4)}
.okp b{color:#35E08A;font-size:62px}
.clk2{position:absolute}
.bt{position:absolute}
.btin{position:absolute;left:0;top:0;width:230px;height:190px;display:flex;align-items:center;justify-content:center}
.btl{position:absolute;left:0;bottom:16px;width:230px;text-align:center;font-weight:700;font-size:26px;letter-spacing:4px;color:#FFFF00}
.sw i{display:inline-block;width:52px;height:52px;border-radius:50%;margin:0 6px;border:3px solid rgba(255,255,255,.7)}
.aa{font-weight:800;font-size:112px;color:#fff;text-shadow:0 0 30px rgba(255,255,255,.4)}
.cp{text-align:center;font-weight:800;line-height:1.1}.cp span{display:block;font-size:50px;color:#fff}.cp em{display:block;font-style:normal;font-size:50px;color:#FFFF00;text-shadow:0 0 24px #FFFF00}
.rays{position:absolute;left:90px;top:210px;width:900px;height:900px;border-radius:50%;background:repeating-conic-gradient(from 0deg,rgba(255,235,200,.20) 0deg 6deg,rgba(255,235,200,0) 6deg 24deg);-webkit-mask-image:radial-gradient(circle,#000 30%,transparent 70%);mask-image:radial-gradient(circle,#000 30%,transparent 70%)}
.plane{position:absolute;border-radius:26px;overflow:hidden;box-shadow:0 40px 90px rgba(0,0,0,.6);border:2px solid rgba(255,255,255,.4);background:#fff}
.plane img{display:block}
.dlab{position:absolute;display:flex;align-items:center;justify-content:center;gap:18px;font-weight:800;font-size:56px;color:#FFFF00;letter-spacing:3px;text-shadow:0 0 30px rgba(255,255,0,.6)}
.ft{position:absolute;width:150px;height:267px;border-radius:16px;object-fit:cover;border:3px solid #fff;box-shadow:0 14px 30px rgba(0,0,0,.5)}
.ft2{position:absolute;width:150px;height:267px;border-radius:16px;object-fit:cover;border:3px solid #fff;box-shadow:0 14px 30px rgba(0,0,0,.5)}
.pulse{position:absolute;width:140px;height:140px;border-radius:50%;border:6px solid #FFFF00;box-shadow:0 0 40px #FFFF00}
.fc{position:absolute;left:0;top:0;width:120px;height:214px;border-radius:14px;object-fit:cover;border:3px solid #fff;box-shadow:0 10px 24px rgba(0,0,0,.5)}
.ic{border-radius:50px}
.phn{position:absolute;width:420px;height:760px;border-radius:64px;background:#0b0d1c;border:10px solid #2a2e4a;box-shadow:0 40px 90px rgba(0,0,0,.6)}
.phs{position:absolute;left:0;top:0;width:400px;height:740px}
.ap{position:absolute;width:64px;height:64px;border-radius:16px;display:block}
.slot{position:absolute;width:64px;height:64px;border-radius:16px;border:3px dashed rgba(255,255,0,.7);display:block}
.ph-ok{position:absolute;width:40px;height:40px;border-radius:50%;background:#35E08A;color:#0F1224;font-weight:800;font-size:26px;text-align:center;line-height:40px}
.cmp{position:absolute}
.cmp .ph{position:absolute;left:44px;top:44px;font-size:42px;color:rgba(255,255,255,.55);font-weight:500}
.cmp .tx{position:absolute;left:44px;top:44px;width:760px;font-size:42px;color:#fff;font-weight:600;line-height:1.25}
.cmp .snd{position:absolute;right:30px;bottom:30px;width:92px;height:92px;border-radius:50%;background:#8E7CFF;color:#fff;font-size:48px;text-align:center;line-height:92px;transform:rotate(-90deg)}
.chp{position:absolute;width:180px;height:90px;border-radius:18px;background:rgba(255,255,255,.12);border:2px solid rgba(255,255,255,.3);display:flex;align-items:center;gap:10px;padding:8px}
.chp img{width:50px;height:74px;border-radius:8px;object-fit:cover}.chp span{font-weight:700;font-size:19px;color:#fff}
#base{will-change:filter}
'''
js_all = '\n'.join(INIT + JS)
html = f'''<!doctype html>
<html lang="ms" data-resolution="portrait"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
<div id="cam"><video id="base" class="clip" src="assets/main.mp4" muted playsinline data-start="0" data-duration="{DUR}" data-media-start="0" data-track-index="1"></video>
<div id="wback">{''.join(WB)}</div>{''.join(PM)}</div>
{''.join(OV)}
{''.join(CAPS)}
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{DUR}" data-track-index="50" data-volume="1"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{paused:true}});
{js_all}
window.__timelines["main"] = tl;
</script></body></html>'''
open('hf/index.html', 'w').write(html)
json.dump({'dur': DUR, 'sfx': sorted(SFX), 'scenes': [[round(a, 2), round(b, 2), k, i] for a, b, k, i in SCENES]}, open('build/sfx_events.json', 'w'))
json.dump(BHI, open('build/bh_intervals.json', 'w'))
print('html', len(html), 'sfx', len(SFX), 'dur', DUR)
for a, b, k, i in sorted(SCENES): print(f'  {i:9s} {k:5s} {a:7.2f} - {b:7.2f}')
