#!/usr/bin/env /usr/bin/python3
"""Short S2 (9:16): "5-6 owner brand sebulan" - resequenced from Day 2. Writes hf/index.html + sfx_events.json"""
import json
DUR = round(json.load(open('timemap.json'))['dur'] + 0.35, 3)
W, H = 1080, 1920
Y = '#FFFF00'; GRN = '#3fd98a'
SAFE_S = .725; SAFE_TX = (1080 - 1080 * SAFE_S) / 2; SAFE_TY = 260 - 90 * SAFE_S
JS = []; SFX = []; INIT = []
def js(s): JS.append(s)
def sfx(t, kind, db=-14): SFX.append([round(float(t), 3), kind, db])
def fj(d): return json.dumps(d, separators=(',', ':'))
def A(sel, f, to, t, d=.4, ease='power3.out'):
    if 'opacity' in f and f['opacity'] == 0: INIT.append(f'gsap.set("{sel}",{fj(f)});')
    js(f'tl.fromTo("{sel}",{fj(f)},{fj({**to, "duration": d, "ease": ease, "immediateRender": False})},{t:.3f});')
def T(sel, to, t, d=.4, ease='power2.out'): js(f'tl.to("{sel}",{fj({**to, "duration": d, "ease": ease})},{t:.3f});')
def txt(i, x, y, w, t, cls='num', fs=60, align='center', extra=''):
    return f'<div class="{cls}" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;font-size:{fs}px;text-align:{align};{extra}">{t}</div>'

BG_PURPLE = 'radial-gradient(ellipse at 50% 38%,#4B1D96 0%,#2b1166 48%,#140a33 100%)'
BG_NAVY = 'radial-gradient(ellipse at 50% 40%,#1d2250 0%,#0F1224 70%)'
SCN = []
def scene(sid, t0, t1, bg, body, fade=.25, hold=False):
    SCN.append(f'<div class="ov" id="{sid}" style="background:{bg}"><div style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-origin:0 0;transform:translate({SAFE_TX:.1f}px,{SAFE_TY:.1f}px) scale({SAFE_S})">{body}</div></div>')
    INIT.append(f'gsap.set("#{sid}",{{opacity:0,display:"none"}});')
    js(f'tl.set("#{sid}",{{display:"block"}},{t0:.3f});')
    js(f'tl.fromTo("#{sid}",{{opacity:0}},{{opacity:1,duration:{fade},ease:"power1.out",immediateRender:false}},{t0:.3f});')
    if not hold:
        js(f'tl.to("#{sid}",{{opacity:0,duration:{fade},ease:"power1.in"}},{t1 - fade:.3f});')
        js(f'tl.set("#{sid}",{{display:"none"}},{t1:.3f});')

# ------------------------------------------------------------------ captions on the presenter shots
CAPS = []   # (id, t0, t1, small, big_html or None, big_t)
def cap(i, t0, t1, small, big=None, bt=None, cls='y', size=112):
    body = f'<div class="sm" style="font-size:46px">{small}</div>' if small else ''
    if big: body += f'<div class="bg2 {cls}" id="{i}b" style="font-size:{size}px;margin-top:6px">{big}</div>'
    CAPS.append(f'<div class="cap" id="{i}" style="left:0;top:1150px;width:{W}px;text-align:center">{body}</div>')
    INIT.append(f'gsap.set("#{i}",{{opacity:0}});')
    A(f'#{i}', {'opacity': 0, 'y': 18}, {'opacity': 1, 'y': 0}, t0, .22)
    if big and bt: A(f'#{i}b', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, bt, .22, 'back.out(1.8)')
    T(f'#{i}', {'opacity': 0}, t1 - .12, .12)

# ================================================================== S0 hook stage: 5-6 owner brand
PO = ['1', '2', '3', '4', '5']  # assets/img/post_1..5.jpg = the student's own design work
SH = ['#d62828', '#6a2cc9', '#0b6e4f', '#f77f00', '#0077b6', '#e4b82e']
def shirt(i, x, y, col, s=250):
    return (f'<div class="abs" id="{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px"><svg width="{s}" height="{s}" viewBox="0 0 100 100"><defs><linearGradient id="{i}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col}"/><stop offset="1" stop-color="{col}" stop-opacity=".62"/></linearGradient></defs>'
            f'<path d="M20 12 L38 5 Q50 17 62 5 L80 12 L97 34 L83 44 L76 37 L76 93 L24 93 L24 37 L17 44 L3 34 Z" fill="url(#{i}g)" stroke="rgba(255,255,255,.55)" stroke-width="1.6"/><path d="M24 62 L76 62 M24 72 L76 72" stroke="rgba(255,255,255,.4)" stroke-width="3"/></svg>'
            f'<svg class="abs" id="{i}c" style="left:{s*.55:.0f}px;top:{s*.62:.0f}px" width="{s*.42:.0f}" height="{s*.42:.0f}" viewBox="0 0 64 64"><circle cx="32" cy="32" r="29" fill="#0F1224" stroke="{GRN}" stroke-width="5"/><path d="M18 33 L28 43 L47 22" fill="none" stroke="{GRN}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
b = txt('h_s', 0, 150, W, 'dalam masa sebulan', 'sm', 54, extra='position:absolute')
b += f'<div class="abs bg2 y" id="h_n" style="left:0;width:{W}px;top:215px;text-align:center;font-size:400px;line-height:1">5–6</div>'
b += f'<div class="abs bg2 w" id="h_o" style="left:0;width:{W}px;top:640px;text-align:center;font-size:130px">OWNER BRAND</div>'
for k in range(6):
    b += shirt(f'h_t{k}', 60 + (k % 3) * 330, 880 + (k // 3) * 330, SH[k], 300 if False else 270)
b += f'<div class="abs bg2 y" id="h_i" style="left:0;width:{W}px;top:1560px;text-align:center;font-size:104px">INSYAALLAH ADA</div>'
scene('s_hook', 3.95, 9.15, BG_PURPLE, b)
A('#h_s', {'opacity': 0}, {'opacity': 1}, 4.05, .25)
A('#h_n', {'opacity': 0, 'scale': 1.6}, {'opacity': 1, 'scale': 1}, 4.1, .3, 'expo.out'); sfx(4.1, 'stamp', -10); sfx(4.1, 'boom', -12)
A('#h_o', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, 5.75, .28, 'back.out(2)'); sfx(5.75, 'pop', -12)
for k in range(6):
    t = 6.1 + k * .4
    A(f'#h_t{k}', {'opacity': 0, 'y': 160, 'scale': .6}, {'opacity': 1, 'y': 0, 'scale': 1}, t, .4, 'back.out(1.7)'); sfx(t, ['click', 'pop', 'click', 'ting', 'pop', 'click'][k], -13)
    A(f'#h_t{k}c', {'opacity': 0, 'scale': 0}, {'opacity': 1, 'scale': 1}, t + .22, .25, 'back.out(3)')
A('#h_i', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 8.5, .3, 'back.out(2)'); sfx(8.5, 'shing', -11)
for k in range(6): js(f'tl.to("#h_t{k}",{{y:{(-1) ** k * 12},duration:1.2,ease:"sine.inOut",yoyo:true,repeat:1}},{6.8 + k * .1:.3f});')

# ================================================================== presenter captions 0-4.3, 9.5-16.4
cap('c1', 0.1, 2.85, 'Jadi,', 'DALAM SEBULAN', 1.6)
cap('c2', 2.9, 3.95, 'kalau nak dapat')
cap('c3', 9.25, 11.5, 'So, aku ingat balik dulu,', None)
cap('c4', 11.5, 14.4, 'waktu aku start masuk dunia', 'FREELANCING', 13.5)
cap('c5', 14.45, 16.2, 'aku start dengan satu skill iaitu')

# ================================================================== S1 design-inspiration wall (portrait, full-bleed)
cols = ''.join(f'<div class="abs" style="left:{-28 + c * 286}px;top:0;width:270px;height:1500px;overflow:hidden;border-radius:18px;box-shadow:0 18px 40px rgba(0,0,0,.55)"><img id="w_c{c}" src="assets/img/pin_col{c}.jpg" style="position:absolute;left:0;top:0;width:270px;height:2706px"></div>' for c in range(4))
b = f'<div class="abs" id="w_wall" data-layout-allow-overflow style="left:0;top:470px;width:{W}px;height:1500px;transform:perspective(1700px) rotateX(20deg) rotateZ(-4deg) scale(1.12);transform-origin:50% 0"><div class="abs" style="left:0;top:0;width:{W}px;height:1500px">{cols}</div></div>'
b += txt('w_s', 0, 90, W, 'aku start dengan satu skill', 'sm', 50, extra='position:absolute;z-index:6')
b += f'<div class="abs bg2" id="w_b" style="left:0;width:{W}px;top:150px;text-align:center;font-size:150px;z-index:6;line-height:1.02"><span class="y">GRAFIK</span><br><span class="w">DESIGN</span></div>'
for k, (nm, tt) in enumerate([('BANNER', 22.1), ('POSTER', 23.4), ('MENU KEDAI MAKAN', 24.0)]):
    b += f'<div class="chip abs" id="w_k{k}" style="left:90px;top:{1330 + k * 125}px;width:{[430, 430, 760][k]}px;height:104px;font-size:44px;background:rgba(15,18,36,.92);border-color:{Y};color:{Y};z-index:7;box-shadow:0 0 40px {Y}55">{nm}</div>'
scene('s_wall', 16.2, 25.0, BG_PURPLE, b)
A('#w_s', {'opacity': 0}, {'opacity': 1}, 16.25, .25)
A('#w_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 16.25, .3, 'back.out(2)'); sfx(16.25, 'stamp', -11)
A('#w_wall', {'opacity': 0, 'y': 260}, {'opacity': 1, 'y': 0}, 16.6, .8, 'power3.out'); sfx(16.6, 'zoom', -13)
for c in range(4): js(f'tl.fromTo("#w_c{c}",{{y:{-80 if c % 2 == 0 else -820}}},{{y:{-700 if c % 2 == 0 else -160},duration:8.8,ease:"none",immediateRender:false}},16.2);')
for k, tt in enumerate([22.1, 23.4, 24.0]): A(f'#w_k{k}', {'opacity': 0, 'x': -160, 'scale': .8}, {'opacity': 1, 'x': 0, 'scale': 1}, tt, .35, 'back.out(1.8)'); sfx(tt, ['click', 'pop', 'ting'][k], -13)

# ================================================================== presenter captions 25.4-32.7
cap('c6', 25.1, 29.0, 'aku perasan benda ni aku buat secara', 'TAK SENGAJA', 27.9)
cap('c7', 29.1, 32.2, 'aku terfokus kepada', 'SATU NICHE SAHAJA', 30.9, size=88)

# ================================================================== S2 niche jersey
b = txt('n_s', 0, 90, W, 'aku fokus kepada satu niche', 'sm', 50, extra='position:absolute')
b += f'<div class="abs bg2 y" id="n_b" style="left:0;width:{W}px;top:150px;text-align:center;font-size:130px">1 SKILL · 1 NICHE</div>'
b += f'<div class="abs" id="n_card" style="left:240px;top:400px;width:600px;height:600px"><div style="width:100%;height:100%;border-radius:26px;overflow:hidden;border:3px solid rgba(255,255,255,.5);box-shadow:0 40px 90px rgba(0,0,0,.6);transform:perspective(1700px) rotateY(-10deg) rotate(-3deg)"><img src="assets/img/post_marquez.jpg" style="width:100%;height:100%;object-fit:cover"></div></div>'
b += f'<div class="abs" id="n_c2" style="left:570px;top:780px;width:380px;height:335px"><div style="width:100%;height:100%;border-radius:22px;overflow:hidden;border:3px solid rgba(255,255,255,.5);box-shadow:0 30px 70px rgba(0,0,0,.6);transform:rotate(5deg)"><img src="assets/img/post_cod.jpg" style="width:100%;height:100%;object-fit:cover"></div></div>'
b += f'<div class="abs" id="n_c3" style="left:110px;top:810px;width:400px;height:324px"><div style="width:100%;height:100%;border-radius:22px;overflow:hidden;border:3px solid rgba(255,255,255,.5);box-shadow:0 30px 70px rgba(0,0,0,.6);transform:rotate(-6deg)"><img src="assets/img/post_joker.jpg" style="width:100%;height:100%;object-fit:cover"></div></div>'
tags = [('JERSEY', 34.4, 120, 1230), ('STREET APPAREL', 35.8, 120, 1340), ('ARTWORK PRINTABLE', 38.8, 120, 1450)]
for k, (nm, tt, x, y) in enumerate(tags):
    b += f'<div class="chip abs" id="n_t{k}" style="left:{x}px;top:{y}px;width:{[380, 560, 800][k]}px;height:96px;font-size:42px;background:rgba(15,18,36,.92);border-color:{Y};color:{Y}">{nm}</div>'
b += f'<div class="abs bg2" id="n_m" style="left:0;width:{W}px;top:1580px;text-align:center;font-size:96px"><span class="w">jual sebagai</span> <span class="y">MERCH</span></div>'
scene('s_niche', 32.3, 43.6, BG_PURPLE, b)
A('#n_s', {'opacity': 0}, {'opacity': 1}, 32.4, .25)
A('#n_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 32.5, .3, 'back.out(2)'); sfx(32.5, 'stamp', -11)
A('#n_card', {'opacity': 0, 'x': 260, 'scale': .85}, {'opacity': 1, 'x': 0, 'scale': 1}, 33.3, .6, 'power3.out'); sfx(33.3, 'slide', -13)
for k, (nm, tt, x, y) in enumerate(tags): A(f'#n_t{k}', {'opacity': 0, 'x': -140, 'scale': .8}, {'opacity': 1, 'x': 0, 'scale': 1}, tt, .35, 'back.out(1.8)'); sfx(tt, ['click', 'pop', 'ting'][k], -13)
A('#n_m', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 42.0, .3, 'back.out(2)'); sfx(42.0, 'stamp', -10)
js('tl.to("#n_card",{y:-14,duration:2.4,ease:"sine.inOut",yoyo:true,repeat:3},33.9);')
A('#n_c3', {'opacity': 0, 'x': -240, 'scale': .8}, {'opacity': 1, 'x': 0, 'scale': 1}, 34.0, .5, 'power3.out'); sfx(34.0, 'click', -13)
A('#n_c2', {'opacity': 0, 'x': 240, 'scale': .8}, {'opacity': 1, 'x': 0, 'scale': 1}, 34.5, .5, 'power3.out'); sfx(34.5, 'pop', -13)

# ================================================================== S3 trust: Facebook feed phone + days + meter
cards = ''
cc = [('#d62828', '#fcbf49'), ('#6a2cc9', '#ffd166'), ('#0b6e4f', '#f4f1de'), ('#f77f00', '#fff3e0'), ('#0077b6', '#caf0f8'), ('#222', '#ffd60a')]
for k in range(8):
    a_, b_ = cc[k % 6]
    cards += (f'<div style="position:absolute;left:18px;top:{k * 330 + 12}px;width:{480 - 36}px;height:310px;border-radius:18px;background:#fff;overflow:hidden"><div style="height:60px;display:flex;align-items:center;padding:0 16px;gap:12px"><div style="width:38px;height:38px;border-radius:50%;background:#1877f2"></div><div style="width:170px;height:12px;border-radius:6px;background:#ccd0d5"></div></div>'
              f'<div style="height:190px;background:url(assets/img/post_{PO[k % 5]}.jpg) center/cover"></div><div style="height:60px;display:flex;align-items:center;padding:0 16px;gap:10px"><div style="width:28px;height:28px;border-radius:50%;background:#1877f2"></div><div style="width:28px;height:28px;border-radius:50%;background:#f33e58"></div><div style="width:90px;height:10px;border-radius:5px;background:#ccd0d5"></div></div></div>')
b = txt('t_s', 0, 90, W, '100% menggunakan', 'sm', 50, extra='position:absolute')
b += f'<div class="abs bg2 y" id="t_b" style="left:0;width:{W}px;top:150px;text-align:center;font-size:122px">FACEBOOK FEED</div>'
b += (f'<div class="abs" id="t_ph" style="left:300px;top:400px;width:560px;height:1080px"><div style="width:100%;height:100%;border-radius:62px;background:#111;border:7px solid #444;box-shadow:0 40px 90px rgba(0,0,0,.65),0 0 0 3px rgba(255,255,255,.2);overflow:hidden;transform:perspective(1800px) rotateY(-14deg) rotateZ(2deg)">'
      f'<div style="position:absolute;left:16px;top:30px;right:16px;bottom:24px;border-radius:44px;background:#e9ebee;overflow:hidden"><div style="position:absolute;left:0;top:0;right:0;height:74px;background:#1877f2;color:#fff;font:800 32px Poppins;display:flex;align-items:center;padding-left:24px;z-index:3">facebook</div>'
      f'<div id="t_feed" style="position:absolute;left:0;top:74px;width:100%;height:2700px">{cards}</div></div></div></div>')
b += f'<div class="abs" id="t_m" style="left:130px;top:470px;width:84px;height:850px;border-radius:42px;background:rgba(255,255,255,.18);border:3px solid #fff;overflow:hidden"><div id="t_f" style="position:absolute;left:0;bottom:0;width:100%;height:100%;background:linear-gradient(0deg,{GRN},{Y});box-shadow:0 0 40px {Y};transform-origin:50% 100%"></div></div>'
b += txt('t_l', 40, 1345, 270, 'TRUST', 'lab', 44, 'center')
for i in range(7):
    b += f'<div class="abs" id="t_d{i}" style="left:{82 + i * 136}px;top:290px;width:112px;height:108px;border-radius:14px;background:#fff;overflow:hidden;box-shadow:0 14px 30px rgba(0,0,0,.45)"><div style="height:34px;background:#1877f2"></div><div style="text-align:center;font:800 54px Poppins;color:#0F1224;line-height:1.1">{i + 1}</div></div>'
for i in range(5):
    b += f'<svg class="abs" id="t_h{i}" style="left:{650 + (i % 3) * 110}px;top:1270px" width="70" height="64" viewBox="0 0 24 22"><path d="M12 21 C-6 9 4 -3 12 5 C20 -3 30 9 12 21Z" fill="{["#f33e58", "#ff5d73", "#ff2d55"][i % 3]}"/></svg>'
b += txt('t_c', 0, 1590, W, 'buat posting hari-hari', 'sm', 50, extra='position:absolute')
b += f'<div class="abs bg2" id="t_n" style="left:0;width:{W}px;top:1540px;text-align:center;font-size:132px"><span class="y">TRUST</span> <span class="w">NAIK</span></div>'
scene('s_trust', 43.6, DUR, BG_NAVY, b, hold=True)
A('#t_s', {'opacity': 0}, {'opacity': 1}, 43.7, .25)
A('#t_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 45.7, .3, 'back.out(2)'); sfx(45.7, 'stamp', -11)
A('#t_ph', {'opacity': 0, 'x': 300, 'rotation': 8}, {'opacity': 1, 'x': 0, 'rotation': 0}, 46.4, .6, 'power3.out'); sfx(46.4, 'slide', -13)
js('tl.to("#t_feed",{y:-1400,duration:8,ease:"none"},46.8);')
A('#t_m', {'opacity': 0}, {'opacity': 1}, 47.3, .3); A('#t_l', {'opacity': 0}, {'opacity': 1}, 47.3, .3)
js('gsap.set("#t_f",{scaleY:.06});')
js('tl.to("#t_f",{scaleY:1,duration:5.6,ease:"power1.inOut"},47.9);')
for i in range(7): A(f'#t_d{i}', {'opacity': 0, 'y': -80, 'rotation': -12}, {'opacity': 1, 'y': 0, 'rotation': -4 + i * 1.3}, 47.8 + i * .26, .35, 'back.out(1.8)'); sfx(47.8 + i * .26, ['click', 'pop', 'click', 'pop', 'click', 'pop', 'ting'][i], -14)
A('#t_c', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, 47.6, .3)
for i in range(5): A(f'#t_h{i}', {'opacity': 0, 'y': 40, 'scale': .3}, {'opacity': 1, 'y': -60, 'scale': 1}, 49.6 + i * .45, .5, 'back.out(2)')
T('#t_c', {'opacity': 0}, 52.3, .2)
A('#t_n', {'opacity': 0, 'scale': 1.5}, {'opacity': 1, 'scale': 1}, 52.5, .3, 'expo.out'); sfx(52.5, 'stamp', -9); sfx(52.5, 'boom', -11)

# context pill (first seconds): what this clip is about
CAPS.append(f'<div class="cap" id="tg" style="left:0;top:196px;width:{W}px;text-align:center;z-index:120"><span style="display:inline-block;padding:9px 26px;border-radius:40px;background:rgba(15,18,36,.88);border:2px solid rgba(255,255,0,.75);color:#FFFF00;font:800 30px Poppins;letter-spacing:.04em">PENGALAMAN AKU · FREELANCE GRAFIK DESIGN</span></div>')
INIT.append('gsap.set("#tg",{opacity:0});')
A('#tg', {'opacity': 0, 'y': -20}, {'opacity': 1, 'y': 0}, 0.1, .3); T('#tg', {'opacity': 0}, 8.9, .25)
# ------------------------------------------------------------------ assemble
CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0F1224;font-family:Poppins,sans-serif}
#root{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden;background:#000}
#base{position:absolute;left:0;top:0;width:1080px;height:1920px}
.abs{position:absolute}
.ov{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;display:none;overflow:hidden;z-index:20;font-family:Poppins,sans-serif}
.cap{position:absolute;z-index:100;opacity:0;font-family:Poppins,sans-serif}
.sm{font-weight:500;color:#fff;line-height:1.15;text-align:center;text-shadow:0 0 .1em rgba(255,255,255,.7),0 0 .35em rgba(255,255,255,.3),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}
.ov .sm{position:absolute}
.bg2{font-weight:800;line-height:1.04;text-transform:uppercase;letter-spacing:-.012em;white-space:nowrap}
.y{color:#FFFF00;font-weight:800;text-shadow:0 0 .05em rgba(255,255,0,.95),0 0 .2em rgba(255,255,0,.6),0 0 .45em rgba(255,255,0,.35),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}
.w{color:#fff;font-weight:600;text-shadow:0 0 .06em rgba(255,255,255,.9),0 0 .2em rgba(255,255,255,.5),0 0 .45em rgba(255,255,255,.28),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}
.num{position:absolute;font-weight:800;color:#fff;letter-spacing:-.02em}
.lab{position:absolute;font-weight:800;color:#FFFF00;text-transform:uppercase;text-shadow:0 0 .2em rgba(255,255,0,.6)}
.chip{position:absolute;border-radius:22px;background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.28);color:#fff;font-weight:800;display:flex;align-items:center;padding:0 34px}
'''
html = f'''<!doctype html>
<html lang="ms" data-resolution="portrait"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
<video id="base" class="clip" src="assets/main.mp4" muted playsinline data-start="0" data-duration="{DUR}" data-media-start="0" data-track-index="1"></video>
{''.join(SCN)}
{''.join(CAPS)}
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{DUR}" data-track-index="50" data-volume="1"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{paused:true}});
{chr(10).join(INIT)}
{chr(10).join(JS)}
window.__timelines["main"] = tl;
</script></body></html>'''
open('hf/index.html', 'w').write(html)
json.dump({'dur': DUR, 'sfx': sorted(SFX)}, open('sfx_events.json', 'w'))
print('html', len(html), 'sfx', len(SFX), 'dur', DUR)
