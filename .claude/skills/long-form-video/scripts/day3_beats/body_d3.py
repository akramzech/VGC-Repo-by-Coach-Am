# Day 3 "Buka dan tutup" - body (times are on the CUT timeline, from build/words_out.json)
HD = tm['hook_dur']
def txt(i, x, y, w, t, cls='num', fs=60, align='center', extra=''):
    return f'<div class="{cls} abs" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;text-align:{align};font-size:{fs}px;{extra}">{t}</div>'
def big(i, y, html, fs=130, extra=''):
    return f'<div class="abs bg2" id="{i}" style="left:0;width:1920px;top:{y}px;text-align:center;font-size:{fs}px;{extra}">{html}</div>'
def head(p, small, bigh, ts, tb, fs=130):
    h = txt(f'{p}_s', 0, 52, 1920, small, 'sm', 50) + big(f'{p}_b', 108, bigh, fs)
    return h
def head_in(p, ts, tb):
    A(f'#{p}_s', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, ts, .3)
    A(f'#{p}_b', {'opacity': 0, 'scale': .7, 'filter': 'blur(10px)'}, {'opacity': 1, 'scale': 1, 'filter': 'blur(0px)'}, tb, .32, 'back.out(1.8)'); sfx(tb, 'stamp', -12)
def cardico(p, x, y, w, h, label, fs=40):
    ic = '<svg class="abs" style="left:%dpx;top:16px" width="56" height="56" viewBox="0 0 64 64" fill="none" stroke="#0F1224" stroke-width="4" stroke-linejoin="round"><path d="M8 58 V14 L32 6 L56 14 V58 Z"/><path d="M20 24 h8 M36 24 h8 M20 36 h8 M36 36 h8 M26 58 V46 h12 V58"/></svg>' % (w // 2 - 28)
    return (f'<div class="abs" id="{p}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:18px;background:linear-gradient(160deg,#fff,#cfc9ff);box-shadow:0 26px 60px rgba(0,0,0,.55)">{ic}'
            f'<div class="abs" style="left:0;width:{w}px;top:84px;text-align:center;font:800 {fs}px Poppins;color:#0F1224;letter-spacing:-.01em">{label}</div>'
            f'<div class="stampr abs" id="{p}x" style="left:0;top:{h - 64}px;width:{w}px"><span style="transform:rotate(-8deg);font-size:30px;border-width:4px;padding:0 14px">CLOSED</span></div></div>')
def pdraw(i, d, stroke, sw=10, extra=''):
    return f'<path id="{i}" d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" {extra}/>'
def draw(i, t, d=1.0, ease='power2.inOut'):
    js(f'tl.to("#{i}",{{strokeDashoffset:0,duration:{d},ease:"{ease}"}},{t:.3f});')
def bulb(i, x, y, s=70):
    return (f'<svg class="abs" id="{i}" style="left:{x}px;top:{y}px" width="{s}" height="{s}" viewBox="0 0 64 64" fill="none" stroke="{Y}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M22 44 C12 36 12 14 32 10 C52 14 52 36 42 44 V50 H22 Z" fill="{Y}33" style="filter:drop-shadow(0 0 10px {Y})"/><path d="M24 56 H40 M27 61 H37"/></svg>')

def person(i, x, y, s, col):
    return (f'<svg class="abs" id="{i}" style="left:{x}px;top:{y}px" width="{60 * s:.0f}" height="{110 * s:.0f}" viewBox="0 0 60 110">'
            f'<circle cx="30" cy="22" r="16" fill="{col}"/><path d="M6 108 C6 62 16 46 30 46 C44 46 54 62 54 108 Z" fill="{col}"/></svg>')
# ================================================================== HOOK (0 - HD): kata mentor
OV.append('<div id="tg" class="abs" style="left:0;top:44px;width:1920px;text-align:center;z-index:190;opacity:0"><span style="display:inline-block;padding:10px 34px;border-radius:44px;background:rgba(15,18,36,.88);border:2px solid rgba(255,255,0,.75);color:#FFFF00;font:800 34px Poppins;letter-spacing:.05em">VLOG DAY 3 · BUKA DAN TUTUP</span></div>')
A('#tg', {'opacity': 0, 'y': -20}, {'opacity': 1, 'y': 0}, .25, .3); T('#tg', {'opacity': 0}, HD - .25, .25)
SCENES.append((0, HD, 'hook', 's_hook'))
CAPSPEC.append(dict(t0=.05, t1=2.2, small='kata mentor aku', items=[('BISNES TAK PERNAH', 'w', None), ('ADA MASALAH', 'y', None)], ts=[.1, 1.2], y=820, fs=96, pos='bc'))
CAPSPEC.append(dict(t0=2.3, t1=HD - .1, small='yang ada masalah adalah', items=[('ORANG', 'y', None), ('YANG URUS', 'w', None)], ts=[4.1, 5.5], y=820, fs=104, pos='bc'))
sfx(HD - .02, 'riser', -12); sfx(HD, 'boom', -8); sfx(HD, 'stamp', -12)

# ================================================================== INTRO captions (presenter 7.03 - 24.3)
def C(small, items, t0, t1, y=820, fs=104):
    CAPSPEC.append(dict(t0=t0, t1=t1, small=small, items=[(a, b, None) for a, b, _ in items], ts=[t for _, _, t in items], y=y, fs=fs, pos='bc'))
C('buat vlog', [('SATU HARI', 'w', 11.2), ('SATU KNOWLEDGE', 'y', 12.2)], 10.1, 13.5)
C('dia lebih kepada', [('BUKAN KNOWLEDGE', 'r', 13.8), ('SHARING', 'y', 15.7)], 13.6, 16.5)
C('sebab aku pun masih', [('BELUM BERJAYA', 'y', 18.5)], 16.8, 19.6)
C('masih banyak benda', [('NAK KENA BELAJAR', 'w', 20.3)], 19.7, 21.9)
C('cuma mungkin dalam sepanjang', [('PENGALAMAN AKU', 'y', 23.6)], 22.0, 24.3)

# ================================================================== S_BT1 buka dan tutup (24.3 - 34.9)
t0, t1 = 24.3, 34.9
b = head('bt', 'sepanjang pengalaman aku', '<span class="w">BUKA</span> <span class="w">DAN</span> <span class="r">TUTUP</span>', 24.4, 26.0)
SIGN = ('<div class="abs" id="sg" style="left:240px;top:420px;width:520px;height:340px">'
        '<div class="abs" style="left:100px;top:-70px;width:5px;height:90px;background:#ffffff99;transform:rotate(-18deg);transform-origin:50% 100%"></div>'
        '<div class="abs" style="left:415px;top:-70px;width:5px;height:90px;background:#ffffff99;transform:rotate(18deg);transform-origin:50% 100%"></div>'
        '<div class="abs" style="left:240px;top:-118px;width:40px;height:40px;border-radius:50%;background:#e0e0f0;box-shadow:0 0 0 6px #ffffff33"></div>'
        '<div class="abs" id="sgo" style="left:0;top:0;width:520px;height:340px;border-radius:34px;background:#f6f1e6;border:8px solid #ffffffcc;box-shadow:0 36px 70px rgba(0,0,0,.55);transform-origin:50% 0"><div class="abs" style="left:0;width:520px;top:70px;text-align:center;font:800 150px Poppins;color:#0F1224;letter-spacing:.02em">OPEN</div><div class="abs" style="left:0;width:520px;top:250px;text-align:center;font:700 34px Poppins;color:#7b7fa8;letter-spacing:.3em">BUKA</div></div>'
        '<div class="abs" id="sgc" style="left:0;top:0;width:520px;height:340px;border-radius:34px;background:#c0262d;border:8px solid #ffffffcc;box-shadow:0 36px 70px rgba(0,0,0,.55);transform-origin:50% 0"><div class="abs" style="left:0;width:520px;top:84px;text-align:center;font:800 118px Poppins;color:#fff;letter-spacing:.02em">CLOSED</div><div class="abs" style="left:0;width:520px;top:250px;text-align:center;font:700 34px Poppins;color:#ffd5d7;letter-spacing:.3em">TUTUP</div></div></div>')
b += SIGN
CO = [('c0', 920, 400, 'SDN BHD', None), ('c1', 1230, 400, 'SDN BHD', None), ('c2', 1540, 400, 'SDN BHD', None), ('c3', 1075, 650, 'ENTERPRISE', None), ('c4', 1385, 650, 'ENTERPRISE', None)]
# cards are 250 wide in 1920 space -> use 270x160
for (p, x, y, lb, sb) in CO:
    b += cardico('b' + p, x, y, 290, 200, lb, 40 if lb == 'SDN BHD' else 34)
b += txt('bt_n', 100, 800, 700, '<span style="text-decoration:line-through;text-decoration-color:#FF4D4D;text-decoration-thickness:6px">BUKA &amp; MASIH ADA</span>', 'lab', 44, 'center', 'color:#fff;opacity:.9')
b += txt('bt_y', 100, 868, 700, 'BUKA &amp; TUTUP', 'lab', 54, 'center')
b += big('bt_t', 944, '<span class="w">3 SDN BHD</span> <span class="y">·</span> <span class="w">2 ENTERPRISE</span>', 62)
scene('s_bt1', t0, t1, 'full', BG_PURPLE, b)
head_in('bt', 24.4, 26.1)
A('#sg', {'opacity': 0, 'y': -260}, {'opacity': 1, 'y': 0}, 24.8, .9, 'bounce.out'); sfx(25.0, 'click', -13)
js('gsap.set("#sg",{transformOrigin:"50% -118px"});')
js('tl.fromTo("#sg",{rotation:0},{rotation:6,duration:.5,ease:"sine.inOut",yoyo:true,repeat:3,immediateRender:false},25.8);')
js('gsap.set("#sgc",{scaleY:0});')
T('#sgo', {'scaleY': 0}, 26.55, .16, 'power2.in'); A('#sgc', {'scaleY': 0}, {'scaleY': 1}, 26.7, .2, 'back.out(1.6)'); sfx(26.7, 'stamp', -11); sfx(26.7, 'click', -13)
for k, (p, x, y, lb, sb) in enumerate(CO):
    tt = [27.2, 27.6, 27.95, 29.2, 29.55][k]
    A(f'#b{p}', {'opacity': 0, 'y': 90, 'scale': .85}, {'opacity': 1, 'y': 0, 'scale': 1}, tt, .4, 'back.out(1.6)'); sfx(tt, ['pop', 'click', 'pop', 'ting', 'pop'][k], -13)
    A(f'#b{p}x', {'opacity': 0, 'scale': 2.2}, {'opacity': 1, 'scale': 1}, 30.0 + k * .22, .2, 'expo.out'); sfx(30.0 + k * .22, 'stamp', -12)
A('#bt_t', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, 29.6, .3, 'back.out(1.8)')
A('#bt_n', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, 31.7, .3); sfx(31.7, 'click', -13)
A('#bt_y', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, 33.7, .3, 'back.out(1.8)'); sfx(33.7, 'ting', -12)
T('#bt_n', {'opacity': .35}, 33.6, .3)

# ================================================================== S_TU tak untung (34.9 - 37.6)
t0, t1 = 34.9, 37.6
b = head('tu', 'kenapa tutup? sebab', '<span class="r">TAK UNTUNG</span>', 35.0, 36.2, 140)
b += ('<svg class="abs" id="tu_c" style="left:300px;top:330px" width="1320" height="560" viewBox="0 0 1320 560">'
      '<path d="M20 20 V520 H1300" fill="none" stroke="#ffffff55" stroke-width="6" stroke-linecap="round"/>'
      + pdraw('tu_l', 'M40 140 L220 90 L360 200 L520 120 L700 300 L880 360 L1060 440 L1280 500', RED, 12, 'style="filter:drop-shadow(0 0 12px #FF4D4D)"')
      + '<path d="M1180 440 l100 60 l-110 24" fill="none" stroke="#FF4D4D" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" opacity="0" id="tu_a"/></svg>')
b += txt('tu_m', 360, 840, 380, 'RM', 'num', 90, 'left', 'color:#FF4D4D')
scene('s_tu', t0, t1, 'full', BG_NAVY, b)
head_in('tu', 35.0, 36.2)
A('#tu_c', {'opacity': 0}, {'opacity': 1}, 35.2, .3); draw('tu_l', 35.4, 1.6, 'power1.inOut')
T('#tu_a', {'opacity': 1}, 36.9, .2); A('#tu_m', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 36.9, .3, 'back.out(2)'); sfx(36.9, 'boom', -12)

# ================================================================== S_NT naik turun, belajar banyak (37.6 - 45.6)
t0, t1 = 37.6, 45.6
b = head('nt', 'sepanjang naik dan turun ni', '<span class="y">BELAJAR</span> <span class="w">BANYAK BENDA</span>', 37.7, 41.1, 120)
PTS = [(220, 820), (480, 600), (720, 860), (1000, 520), (1260, 880), (1520, 560), (1700, 780)]
d = 'M' + ' L'.join(f'{x} {y}' for x, y in PTS)
NTL = pdraw('nt_l', d, Y, 10, 'style="filter:drop-shadow(0 0 12px #FFFF00)"')
b += f'<svg class="abs" id="nt_c" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">{NTL}</svg>'
b += txt('nt_up', 240, 520, 220, 'NAIK', 'lab', 44) + txt('nt_dn', 600, 930, 240, 'TURUN', 'lab', 44, 'center', 'color:#FF4D4D')
for k, (x, y) in enumerate([PTS[1], PTS[3], PTS[5], PTS[6]]):
    b += bulb(f'nt_b{k}', x - 35, y - 120, 76)
scene('s_nt', t0, t1, 'full', BG_PURPLE, b)
head_in('nt', 37.7, 41.1)
draw('nt_l', 38.0, 3.6, 'none')
A('#nt_up', {'opacity': 0, 'y': 16}, {'opacity': 1, 'y': 0}, 39.6, .3); sfx(39.6, 'swish_up', -14)
A('#nt_dn', {'opacity': 0, 'y': -16}, {'opacity': 1, 'y': 0}, 40.5, .3); sfx(40.5, 'swish_dn', -14)
for k, tt in enumerate([41.7, 42.4, 43.1, 43.9]):
    A(f'#nt_b{k}', {'opacity': 0, 'scale': .2, 'y': 24}, {'opacity': 1, 'scale': 1, 'y': 0}, tt, .35, 'back.out(2.2)'); sfx(tt, ['pop', 'ting', 'pop', 'click'][k], -14)

C('benda yang paling besar', [('PALING BESAR', 'y', 47.2), ('AKU BELAJAR', 'w', 47.9)], 45.7, 49.2)

# ================================================================== S_REZ behind-head (49.2 - 69.7): rezeki
t0, t1 = 49.2, 69.7
GOLD = '#FFD76A'
els = ('<div class="abs" id="rz_beam" style="left:360px;top:-80px;width:1200px;height:900px;background:radial-gradient(ellipse at 50% 0,rgba(255,226,140,.60),rgba(255,226,140,0) 68%)"></div>')
for k in range(26):
    x = 120 + (k * 211) % 1680; y = -40 - (k * 97) % 300; s = 10 + (k * 7) % 14
    els += f'<div class="abs" id="rz_p{k}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:50%;background:{GOLD};box-shadow:0 0 18px {GOLD}"></div>'
els += ('<svg class="abs" id="rz_road" style="left:1200px;top:560px" width="640" height="480" viewBox="0 0 640 480">'
        + pdraw('rz_rd', 'M20 460 C140 380 120 300 260 280 C420 258 360 150 470 110 C540 86 580 60 610 30', GOLD, 12, 'style="filter:drop-shadow(0 0 12px #FFD76A)" stroke-dasharray="1" ') + '</svg>')
els += f'<svg class="abs" id="rz_star" style="left:1735px;top:480px" width="100" height="100" viewBox="0 0 64 64"><path d="M32 4 L38 26 L60 32 L38 38 L32 60 L26 38 L4 32 L26 26 Z" fill="{GOLD}" style="filter:drop-shadow(0 0 16px {GOLD})"/></svg>'
fg = (txt('rz_1', 90, 300, 540, 'NO.1', 'lab', 150, 'center', 'color:#FFFF00')
      + txt('rz_2', 90, 470, 540, 'TAK ADA KUASA', 'num', 78, 'center')
      + txt('rz_3', 1260, 290, 570, 'ATAS REZEKI', 'lab', 66, 'center', 'white-space:nowrap')
      + txt('rz_4', 1260, 400, 570, 'REZEKI NI<br>ALLAH YANG BAGI', 'num', 56, 'center', 'white-space:nowrap')
      + txt('rz_5', 90, 640, 540, 'BUAT YANG<br>TERBAIK', 'lab', 84, 'center')
      + txt('rz_6', 1260, 640, 570, 'APA YANG ADA<br>DEKAT TANGAN', 'num', 62, 'center')
      + txt('rz_7', 90, 300, 540, 'NIAT', 'num', 92, 'center')
      + txt('rz_8', 90, 440, 540, 'KEBERKATAN', 'lab', 80, 'center')
      + txt('rz_9', 1260, 250, 570, 'ALLAH<br>TUNJUK JALAN', 'lab', 76, 'center'))
bhscene('s_rez', t0, t1, els, fg)
A('#rz_beam', {'opacity': 0}, {'opacity': 1}, 49.4, 1.2)
A('#rz_1', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, 49.7, .35, 'back.out(1.8)'); sfx(49.7, 'stamp', -12)
A('#rz_2', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, 50.6, .35); A('#rz_3', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, 52.1, .35); sfx(52.1, 'pop', -13)
A('#rz_4', {'opacity': 0, 'scale': .8}, {'opacity': 1, 'scale': 1}, 53.6, .4, 'back.out(1.6)'); sfx(53.6, 'ting', -12)
for k in range(26):
    tt = 53.6 + (k % 13) * .3
    js(f'tl.fromTo("#rz_p{k}",{{opacity:0,y:0}},{{opacity:.9,y:{700 + (k * 37) % 220},duration:{4.0 + (k % 5) * .6},ease:"none",immediateRender:false}},{tt:.3f});')
    js(f'tl.to("#rz_p{k}",{{opacity:0,duration:.8}},{tt + 3.6 + (k % 5) * .6:.3f});')
INIT.append('gsap.set("#rz_p0,#rz_p1,#rz_p2,#rz_p3,#rz_p4,#rz_p5,#rz_p6,#rz_p7,#rz_p8,#rz_p9,#rz_p10,#rz_p11,#rz_p12,#rz_p13,#rz_p14,#rz_p15,#rz_p16,#rz_p17,#rz_p18,#rz_p19,#rz_p20,#rz_p21,#rz_p22,#rz_p23,#rz_p24,#rz_p25",{opacity:0});')
T('#rz_1,#rz_2,#rz_3,#rz_4', {'opacity': 0, 'y': -20}, 55.0, .3, 'power2.in')
A('#rz_5', {'opacity': 0, 'scale': .8}, {'opacity': 1, 'scale': 1}, 57.9, .4, 'back.out(1.7)'); sfx(57.9, 'stamp', -12)
A('#rz_6', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, 59.6, .35); sfx(59.6, 'pop', -13)
T('#rz_5,#rz_6', {'opacity': 0, 'y': -20}, 60.4, .3, 'power2.in')
A('#rz_7', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, 61.4, .35); sfx(61.4, 'click', -13)
A('#rz_8', {'opacity': 0, 'scale': .75}, {'opacity': 1, 'scale': 1}, 64.9, .45, 'back.out(1.8)'); sfx(64.9, 'ting', -11)
T('#rz_7,#rz_8', {'opacity': 0, 'y': -20}, 66.0, .3, 'power2.in')
A('#rz_road', {'opacity': 0}, {'opacity': 1}, 66.3, .3); draw('rz_rd', 66.4, 2.4, 'power1.inOut')
A('#rz_star', {'opacity': 0, 'scale': .2}, {'opacity': 1, 'scale': 1}, 68.4, .5, 'back.out(2.4)'); sfx(68.4, 'ting', -11)
A('#rz_9', {'opacity': 0, 'scale': .8}, {'opacity': 1, 'scale': 1}, 68.0, .4, 'back.out(1.7)'); sfx(68.0, 'stamp', -12)

C('bukanlah aku nak bagi', [('TAZKIRAH', 'w', 71.0)], 69.9, 72.4)

# ================================================================== S_ASB asbab personal income (72.4 - 83.6)
t0, t1 = 72.4, 83.6
b = head('as', 'aku nak cerita mungkin apa', '<span class="y">ASBAB</span>', 72.6, 74.1, 140)
b += txt('as_i', 0, 270, 1920, 'UNTUK NAIKKAN <span class="y">PERSONAL INCOME</span>', 'num', 60)
STP = [(260, 880, 260, 110), (560, 780, 260, 210), (860, 680, 260, 310), (1160, 580, 260, 410)]
for k, (x, y, w, h) in enumerate(STP):
    b += f'<div class="abs" id="as_s{k}" style="left:{x}px;top:{y + 110 - 110 + (110 - 110)}px;width:{w}px;height:{1000 - y}px;border-radius:18px 18px 0 0;background:linear-gradient(180deg,#8a5cf0,#4b2aa8);box-shadow:0 24px 50px rgba(0,0,0,.45),inset 0 6px 0 rgba(255,255,255,.28);transform-origin:50% 100%"></div>'
b += f'<div class="abs coin" id="as_c" style="left:1500px;top:380px;width:220px;height:220px;font-size:64px">RM</div>'
b += person('as_p', 316, 770, 1.4, Y)
scene('s_asb', t0, t1, 'full', BG_PURPLE, b)
head_in('as', 72.6, 74.1)
A('#as_i', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, 75.4, .4)
for k in range(4):
    A(f'#as_s{k}', {'opacity': 0, 'scaleY': 0}, {'opacity': 1, 'scaleY': 1}, 75.0 + k * .9, .45, 'back.out(1.2)'); sfx(75.0 + k * .9, ['pop', 'click', 'pop', 'ting'][k], -13)
A('#as_p', {'opacity': 0}, {'opacity': 1}, 75.0, .3)
for k in range(1, 4): js(f'tl.to("#as_p",{{x:{k * 300},y:{-k * 100},duration:.7,ease:"power2.inOut"}},{75.4 + k * .9:.3f});')
A('#as_c', {'opacity': 0, 'scale': .2, 'rotation': -90}, {'opacity': 1, 'scale': 1, 'rotation': 0}, 81.8, .55, 'back.out(2)'); sfx(81.8, 'ting', -11)
js('tl.to("#as_c",{scale:1.08,duration:.6,ease:"sine.inOut",yoyo:true,repeat:2},82.5);')
C('aku tak nak cerita pasal', [('BISNES', 'r', 84.7), ('PERSONAL INCOME', 'y', 86.3)], 83.7, 87.6)

# ================================================================== S_MEN behind-head (87.5 - 99.4): kata mentor
t0, t1 = 87.5, 99.4
els = ('<svg class="abs" id="mn_q" style="left:90px;top:40px" width="200" height="170" viewBox="0 0 64 54" opacity=".22"><path d="M4 32 C4 14 14 6 26 4 L28 10 C20 13 16 18 16 24 H28 V50 H4 Z M36 32 C36 14 46 6 58 4 L60 10 C52 13 48 18 48 24 H60 V50 H36 Z" fill="#fff"/></svg>')
els += ('<div class="abs" id="mn_bl" style="left:1210px;top:520px;width:140px;height:140px;opacity:0"><svg width="140" height="140" viewBox="0 0 64 64" fill="none" stroke="#fff" stroke-width="3.5" stroke-linejoin="round"><path d="M8 58 V14 L32 6 L56 14 V58 Z"/><path d="M20 24 h8 M36 24 h8 M20 36 h8 M36 36 h8 M26 58 V46 h12 V58"/></svg></div>')
fg = (txt('mn_1', 90, 300, 540, 'kata mentor aku', 'sm', 46, 'center')
      + txt('mn_2', 90, 360, 540, 'BISNES', 'num', 120, 'center')
      + txt('mn_3', 90, 500, 540, 'TAK PERNAH', 'num', 72, 'center')
      + txt('mn_4', 90, 600, 540, 'ADA MASALAH', 'lab', 76, 'center')
      + txt('mn_5', 1260, 330, 570, 'yang ada masalah adalah', 'sm', 46, 'center')
      + txt('mn_6', 1260, 400, 570, 'ORANG', 'lab', 140, 'center', 'color:#FF4D4D;text-shadow:0 0 .2em #FF4D4D99')
      + txt('mn_7', 1260, 560, 570, 'YANG URUS', 'num', 84, 'center'))
bhscene('s_men', t0, t1, els, fg)
A('#mn_q', {'opacity': 0, 'x': -80}, {'opacity': .22, 'x': 0}, 87.6, .8)
A('#mn_1', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, 90.2, .3)
A('#mn_2', {'opacity': 0, 'scale': .75}, {'opacity': 1, 'scale': 1}, 92.8, .35, 'back.out(1.7)'); sfx(92.8, 'stamp', -12)
A('#mn_3', {'opacity': 0, 'y': 16}, {'opacity': 1, 'y': 0}, 93.5, .3); A('#mn_4', {'opacity': 0, 'scale': .75}, {'opacity': 1, 'scale': 1}, 94.1, .35, 'back.out(1.7)'); sfx(94.1, 'ting', -12)
T('#mn_1,#mn_2,#mn_3,#mn_4', {'opacity': 0, 'y': -20}, 94.8, .3, 'power2.in')
A('#mn_5', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, 94.9, .3)
A('#mn_6', {'opacity': 0, 'scale': 1.5}, {'opacity': 1, 'scale': 1}, 96.7, .3, 'expo.out'); sfx(96.7, 'stamp', -10); shake('#mn_6', 96.95, 8)
A('#mn_7', {'opacity': 0, 'y': 16}, {'opacity': 1, 'y': 0}, 97.7, .3); sfx(97.7, 'click', -13)

# ================================================================== S_BN bisnes = nombor vs orang = emosi (99.4 - 107.6)
t0, t1 = 99.4, 107.6
b = head('bn', 'sebab bisnes ni dia', '<span class="w">BISNES</span> <span class="y">=</span> <span class="y">FACTUAL</span>', 99.5, 100.2, 120)
b += ('<svg class="abs" id="bn_c" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">'
      + pdraw('bn_l', 'M160 780 L1760 400', Y, 10, 'style="filter:drop-shadow(0 0 12px #FFFF00)"')
      + pdraw('bn_w', 'M160 880 C260 760 340 1000 460 860 C580 730 660 1000 780 860 C900 730 980 1000 1100 860 C1220 730 1300 1000 1420 860 C1540 730 1620 960 1760 860', RED, 10, 'style="filter:drop-shadow(0 0 12px #FF4D4D)"') + '</svg>')
b += txt('bn_n', 300, 560, 400, 'NUMBERS', 'lab', 48) + txt('bn_t', 1250, 620, 400, 'TREND', 'lab', 48)
b += txt('bn_e', 560, 930, 800, 'ORANG = EMOSI', 'lab', 56, 'center', 'color:#FF4D4D')
scene('s_bn', t0, t1, 'full', BG_NAVY, b)
head_in('bn', 99.5, 100.2)
draw('bn_l', 100.6, 3.0, 'power1.inOut')
A('#bn_n', {'opacity': 0, 'y': 16}, {'opacity': 1, 'y': 0}, 102.5, .3); sfx(102.5, 'click', -13)
A('#bn_t', {'opacity': 0, 'y': 16}, {'opacity': 1, 'y': 0}, 103.4, .3); sfx(103.4, 'pop', -13)
draw('bn_w', 104.3, 2.8, 'power1.inOut'); A('#bn_e', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, 106.3, .35, 'back.out(2)'); sfx(106.3, 'stamp', -11)

# ================================================================== S_RM rumah tak boleh bayar (107.6 - 113.4)
t0, t1 = 107.6, 113.4
b = head('rm', 'emosi bila', '<span class="r">RUMAH TAK BOLEH BAYAR</span>', 107.7, 110.6, 110)
HS = ('<svg class="abs" id="rm_h" style="left:240px;top:300px" width="560" height="560" viewBox="0 0 100 100" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">'
      '<path d="M8 50 L50 14 L92 50 V92 H8 Z"/><rect x="40" y="62" width="20" height="30"/><path d="M60 22 V10 h12 V32"/></svg>')
b += HS
b += ('<div class="abs" id="rm_bill" style="left:640px;top:540px;width:280px;height:340px;background:#fff;border-radius:12px;box-shadow:0 26px 60px rgba(0,0,0,.55);transform:rotate(8deg)">'
      '<div class="abs" style="left:26px;top:26px;font:800 34px Poppins;color:#0F1224">BIL</div><div class="abs" style="left:26px;top:86px;width:200px;height:12px;background:#ccd;border-radius:6px"></div><div class="abs" style="left:26px;top:116px;width:150px;height:12px;background:#ccd;border-radius:6px"></div>'
      '<div class="abs" style="left:0;top:200px;width:260px;text-align:center;font:800 62px Poppins;color:#d62828">RM!</div></div>')
b += ('<svg class="abs" id="rm_f" style="left:1000px;top:330px" width="780" height="460" viewBox="0 0 780 460">'
      '<path d="M10 230 H330" stroke="#ffffff88" stroke-width="8" fill="none" stroke-linecap="round"/>'
      + pdraw('rm_p1', 'M330 230 H560 L760 230', '#ffffff99', 8, 'stroke-dasharray="1" ')
      + pdraw('rm_p2', 'M330 230 C440 230 480 120 560 90 L760 40', RED, 10, 'style="filter:drop-shadow(0 0 10px #FF4D4D)"') + '</svg>')
b += txt('rm_k', 960, 830, 820, 'KEPUTUSAN <span class="y">JADI LAIN</span>', 'num', 64)
scene('s_rm', t0, t1, 'full', BG_NAVY, b)
head_in('rm', 107.7, 110.6)
A('#rm_h', {'opacity': 0, 'y': 40}, {'opacity': 1, 'y': 0}, 108.3, .5, 'back.out(1.4)')
A('#rm_bill', {'opacity': 0, 'y': -200, 'rotation': -20}, {'opacity': 1, 'y': 0, 'rotation': 8}, 110.7, .5, 'bounce.out'); sfx(110.8, 'stamp', -11)
A('#rm_f', {'opacity': 0}, {'opacity': 1}, 111.0, .3); draw('rm_p1', 111.3, 1.2); draw('rm_p2', 111.5, 1.4)
A('#rm_k', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, 111.8, .35, 'back.out(1.8)'); sfx(111.8, 'stamp', -12)

# ================================================================== S_GD gaduh dengan husband / wife (113.4 - 118.4)
t0, t1 = 113.4, 118.4
b = head('gd', 'emosi bila bergaduh dengan', '<span class="r">HUSBAND</span> <span class="w">/</span> <span class="r">WIFE</span>', 113.5, 114.8, 110)
b += ('<svg class="abs" id="gd_a" style="left:300px;top:380px" width="520" height="340" viewBox="0 0 130 85"><path d="M5 5 h96 a8 8 0 0 1 8 8 v34 a8 8 0 0 1 -8 8 h-60 l-20 20 v-20 h-16 a8 8 0 0 1 -8 -8 v-34 a8 8 0 0 1 8 -8z" fill="#fff"/><path d="M26 22 h56 M26 36 h40" stroke="#0F1224" stroke-width="5" stroke-linecap="round"/></svg>'
      '<svg class="abs" id="gd_b" style="left:1100px;top:440px" width="520" height="340" viewBox="0 0 130 85"><path d="M29 5 h96 a8 8 0 0 1 8 8 v34 a8 8 0 0 1 -8 8 h-16 v20 l-20 -20 h-60 a8 8 0 0 1 -8 -8 v-34 a8 8 0 0 1 8 -8z" fill="#cfc9ff"/><path d="M48 22 h56 M48 36 h36" stroke="#0F1224" stroke-width="5" stroke-linecap="round"/></svg>'
      '<svg class="abs" id="gd_z" style="left:790px;top:420px" width="340" height="340" viewBox="0 0 100 100"><path d="M52 8 L38 46 L54 46 L40 92 L72 40 L56 40 L66 8 Z" fill="#FF4D4D" style="filter:drop-shadow(0 0 16px #FF4D4D)"/></svg>')
b += txt('gd_k', 0, 820, 1920, 'KEPUTUSAN <span class="y">JADI LAIN</span>', 'num', 72)
scene('s_gd', t0, t1, 'full', BG_NAVY, b)
head_in('gd', 113.5, 114.8)
A('#gd_a', {'opacity': 0, 'x': -160}, {'opacity': 1, 'x': 0}, 114.3, .45, 'back.out(1.5)'); sfx(114.3, 'pop', -13)
A('#gd_b', {'opacity': 0, 'x': 160}, {'opacity': 1, 'x': 0}, 115.1, .45, 'back.out(1.5)'); sfx(115.1, 'pop', -13)
A('#gd_z', {'opacity': 0, 'scale': .2}, {'opacity': 1, 'scale': 1}, 115.8, .35, 'back.out(3)'); sfx(115.8, 'stamp', -11); shake('#gd_z', 116.1, 8)
A('#gd_k', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, 117.1, .35, 'back.out(1.8)'); sfx(117.1, 'stamp', -12)

# ================================================================== S_PT point: perisai + gate (118.4 - 126.5)
t0, t1 = 118.4, 126.5
b = head('pt', 'sebab itulah, urus dulu', '<span class="y">ASBAB NO.1</span>', 118.5, 118.9, 130)
b += ('<svg class="abs" id="pt_sh" style="left:760px;top:330px" width="400" height="480" viewBox="0 0 64 76"><path d="M32 4 L58 14 V38 C58 54 46 66 32 72 C18 66 6 54 6 38 V14 Z" fill="#ffffff1c" stroke="#FFFF00" stroke-width="2.5" style="filter:drop-shadow(0 0 16px #FFFF00)"/>'
      '<path d="M20 38 L29 47 L46 28" stroke="#3fd98a" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round" id="pt_ck" opacity="0"/></svg>')
b += f'<div class="chip abs" id="pt_e" style="left:150px;top:470px;width:500px;height:100px;font-size:40px;background:rgba(15,18,36,.9);border-color:{Y};color:{Y};justify-content:center">EMOSI</div>'
b += f'<div class="chip abs" id="pt_f" style="left:150px;top:610px;width:560px;height:100px;font-size:40px;background:rgba(15,18,36,.9);border-color:{Y};color:{Y};justify-content:center">FINANCIAL PERSONAL</div>'
b += ('<div class="abs" id="pt_g" style="left:1360px;top:420px;width:400px;height:440px">'
      '<div class="abs" style="left:0;top:80px;width:400px;height:360px;border-radius:200px 200px 0 0;background:linear-gradient(180deg,#2a2f66,#161a3c);border:6px solid #ffffffaa;box-shadow:0 30px 70px rgba(0,0,0,.55)"></div>'
      '<div class="abs" id="pt_l" style="left:40px;top:150px;width:150px;height:290px;background:linear-gradient(180deg,#d9b45a,#a07d2a);border-radius:120px 0 0 0;transform-origin:0 50%"></div>'
      '<div class="abs" id="pt_r" style="left:210px;top:150px;width:150px;height:290px;background:linear-gradient(180deg,#d9b45a,#a07d2a);border-radius:0 120px 0 0;transform-origin:100% 50%"></div>'
      '<div class="abs" style="left:0;top:0;width:400px;text-align:center;font:800 40px Poppins;color:#fff;letter-spacing:.06em">START BISNES</div></div>')
b += ('<svg class="abs" id="pt_ar" style="left:960px;top:610px" width="400" height="80" viewBox="0 0 400 80">' + pdraw('pt_arp', 'M10 40 H380 M340 10 L385 40 L340 70', Y, 8, 'style="filter:drop-shadow(0 0 10px #FFFF00)"') + '</svg>')
b += txt('pt_t', 0, 900, 1920, 'SEBELUM KITA NAK <span class="y">START BISNES</span>', 'num', 62)
scene('s_pt', t0, t1, 'full', BG_PURPLE, b)
head_in('pt', 118.5, 118.9)
A('#pt_sh', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 119.1, .5, 'back.out(1.6)'); sfx(119.1, 'ting', -12)
A('#pt_e', {'opacity': 0, 'x': -200}, {'opacity': 1, 'x': 0}, 119.5, .4, 'back.out(1.5)'); sfx(119.5, 'click', -13)
A('#pt_f', {'opacity': 0, 'x': -200}, {'opacity': 1, 'x': 0}, 121.0, .4, 'back.out(1.5)'); sfx(121.0, 'click', -13)
A('#pt_ck', {'opacity': 0}, {'opacity': 1}, 122.7, .3); sfx(122.7, 'ting', -11)
A('#pt_g', {'opacity': 0, 'x': 160}, {'opacity': 1, 'x': 0}, 124.0, .5, 'power3.out'); sfx(124.0, 'slide', -13)
A('#pt_t', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, 124.6, .4)
draw('pt_arp', 125.2, .7)
T('#pt_l', {'scaleX': 0}, 126.0, .4, 'power2.inOut'); T('#pt_r', {'scaleX': 0}, 126.0, .4, 'power2.inOut'); sfx(126.0, 'zoom', -14)

# ================================================================== presenter outro (126.5 - end)
C('jadi mungkin itu kot', [('POINT', 'y', 129.6), ('ASBAB NO.1', 'w', 131.1)], 127.4, 132.3)
C('boleh share pada hari ni', [('SIMPLE POINT', 'y', 132.5), ('HARI KETIGA', 'w', 135.4)], 132.4, 136.0)
C('aku shoot konten ni', [('TIGA KONTEN', 'y', 138.4), ('SEHARI', 'w', 139.7)], 136.1, 140.1)
C('cumanya aku post tu', [('DAY 1', 'w', 141.9), ('DAY 2', 'w', 142.6), ('DAY 3', 'y', 142.8)], 140.2, 144.0)
C('mungkin hari keempat', [('SETUP LAIN', 'y', 146.4), ('TAK BAWA KERETA?', 'w', 147.6)], 144.1, 150.0)
C('tapi target dia', [('SATU HARI', 'y', 152.0), ('SATU VLOG', 'y', 152.5)], 150.1, 153.5)
C('ini hari yang ketiga, kita', [('JUMPA', 'w', 154.7), ('NEXT VIDEO', 'y', 155.4)], 153.6, DUR + 1)
# in-front overlays (transparent): 3 contents per day, calendar day 1-2-3
OV.append('<div class="ov" id="ov_k" style="background:transparent">' + ''.join(
    f'<div class="abs" id="ov_k{k}" style="left:{250 + k * 190}px;top:80px;width:170px;height:100px;border-radius:14px;background:#0F1224dd;border:3px solid #ffffffaa;box-shadow:0 20px 40px rgba(0,0,0,.5)"><svg class="abs" style="left:48px;top:16px" width="76" height="68" viewBox="0 0 64 64" fill="none" stroke="#FFFF00" stroke-width="4" stroke-linejoin="round"><rect x="6" y="14" width="40" height="36" rx="6"/><path d="M46 28 L60 18 V46 L46 36"/></svg></div>' for k in range(3)) + '</div>')
A('#ov_k', {'opacity': 0}, {'opacity': 1}, 138.3, .2); T('#ov_k', {'opacity': 0}, 141.0, .3); SET('#ov_k', {'display': 'none'}, 141.4); SET('#ov_k', {'display': 'block'}, 138.2)
SCENES.append((138.3, 141.0, 'ov', 'ov_k'))
for k, tt in enumerate([138.4, 139.0, 139.4]):
    A(f'#ov_k{k}', {'opacity': 0, 'y': -60, 'scale': .6}, {'opacity': 1, 'y': 0, 'scale': 1}, tt, .35, 'back.out(1.8)'); sfx(tt, ['pop', 'click', 'ting'][k], -13)
OV.append('<div class="ov" id="ov_d" style="background:transparent">' + ''.join(
    f'<div class="abs" id="ov_d{k}" style="left:{240 + k * 190}px;top:70px;width:170px;height:140px;border-radius:14px;overflow:hidden;background:linear-gradient(160deg,#fff,#cfc9ff);box-shadow:0 20px 40px rgba(0,0,0,.5);{"outline:5px solid #FFFF00;" if k == 2 else ""}"><div style="height:44px;background:#1877f2;color:#fff;font:800 24px Poppins;text-align:center;line-height:44px">DAY</div><div style="text-align:center;font:800 78px Poppins;color:#0F1224;line-height:1.1">{k + 1}</div></div>' for k in range(3)) + '</div>')
A('#ov_d', {'opacity': 0}, {'opacity': 1}, 141.6, .2); T('#ov_d', {'opacity': 0}, 144.0, .3); SET('#ov_d', {'display': 'none'}, 144.4); SET('#ov_d', {'display': 'block'}, 141.5)
SCENES.append((141.6, 144.0, 'ov', 'ov_d'))
for k, tt in enumerate([141.9, 142.6, 142.85]):
    A(f'#ov_d{k}', {'opacity': 0, 'y': -60, 'rotation': -14}, {'opacity': 1, 'y': 0, 'rotation': -4 + k * 4}, tt, .35, 'back.out(1.8)'); sfx(tt, ['click', 'pop', 'ting'][k], -13)
