import sys; sys.path.insert(0, '.')
from kit import *
init('S3')
PO = ['1', '2', '3', '4', '5']  # assets/img/post_1..5.jpg = the student's own design work
AIS = [('openai', 'CHATGPT'), ('claude', 'CLAUDE'), ('deepseek', 'DEEPSEEK'), ('lovable', 'LOVABLE'), ('manus', 'MANUS')]
CC = [('#d62828', '#fcbf49'), ('#6a2cc9', '#ffd166'), ('#0b6e4f', '#f4f1de'), ('#f77f00', '#fff3e0'), ('#0077b6', '#caf0f8'), ('#e4b82e', '#fff')]

# ---------------------------------------------------------------- B: paid ads ada, aku yang tak belajar (6.9 - 12.2)
with shifted(-6.9):
    b = txt('b_s', 0, 90, W, 'waktu zaman aku start', 'sm', 50, extra='position:absolute') + big('b_b', 150, '<span class="w">PAID ADS</span>', 160)
    b += ('<svg class="abs" id="b_m" style="left:240px;top:520px" width="600" height="600" viewBox="0 0 64 64" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M10 26 V38 H20 L40 50 V14 L20 26 Z"/><path d="M46 22 C50 27 50 37 46 42"/><path d="M52 16 C59 25 59 39 52 48"/></svg>')
    b += f'<div class="abs bg2 r" id="b_x" style="left:60px;width:960px;top:1250px;text-align:center;font-size:130px;transform-origin:50% 50%"><span style="display:inline-block;border:10px solid #FF4D4D;border-radius:26px;padding:6px 40px;background:rgba(15,18,36,.85)">TAK BELAJAR</span></div>'
    b += txt('b_a', 0, 1530, W, 'aku yang tak belanja kan', 'sm', 52, extra='position:absolute')
    scene('s_b', 9.5, 12.2, BG_NAVY, b)
    A('#b_s', {'opacity': 0}, {'opacity': 1}, 7.0, .25)
    A('#b_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 9.7, .3, 'back.out(2)'); sfx(9.7, 'stamp', -11)
    A('#b_m', {'opacity': 0, 'x': -200, 'rotation': -20}, {'opacity': 1, 'x': 0, 'rotation': 0}, 9.9, .5, 'back.out(1.6)'); sfx(9.9, 'swish_up', -13)
    A('#b_x', {'opacity': 0, 'scale': 2.2, 'rotation': -14}, {'opacity': 1, 'scale': 1, 'rotation': -6}, 11.2, .3, 'expo.out'); sfx(11.2, 'stamp', -9); sfx(11.2, 'boom', -12)
    A('#b_a', {'opacity': 0}, {'opacity': 1}, 11.1, .25)
    js('tl.to("#b_m",{opacity:.35,duration:.4},11.3);')
# ---------------------------------------------------------------- C: 100% Facebook feed (12.2 - 16.2)
with shifted(-7.0):
    cards = ''
    for k in range(8):
        a_, b_ = CC[k % 6]
        cards += (f'<div style="position:absolute;left:18px;top:{k * 330 + 12}px;width:{480 - 36}px;height:310px;border-radius:18px;background:#fff;overflow:hidden"><div style="height:60px;display:flex;align-items:center;padding:0 16px;gap:12px"><div style="width:38px;height:38px;border-radius:50%;background:#1877f2"></div><div style="width:170px;height:12px;border-radius:6px;background:#ccd0d5"></div></div>'
                  f'<div style="height:190px;background:url(assets/img/post_{PO[k % 5]}.jpg) center/cover"></div><div style="height:60px;display:flex;align-items:center;padding:0 16px;gap:10px"><div style="width:28px;height:28px;border-radius:50%;background:#1877f2"></div><div style="width:28px;height:28px;border-radius:50%;background:#f33e58"></div><div style="width:90px;height:10px;border-radius:5px;background:#ccd0d5"></div></div></div>')
    b = txt('c_s', 0, 90, W, 'waktu tu menggunakan', 'sm', 50, extra='position:absolute') + big('c_b', 150, '<span class="y">100%</span> <span class="w">FACEBOOK</span>', 112)
    b += (f'<div class="abs" id="c_ph" style="left:270px;top:420px;width:560px;height:1100px"><div style="width:100%;height:100%;border-radius:62px;background:#111;border:7px solid #444;box-shadow:0 40px 90px rgba(0,0,0,.65),0 0 0 3px rgba(255,255,255,.2);overflow:hidden;transform:perspective(1800px) rotateY(14deg) rotateZ(-2deg)">'
          f'<div style="position:absolute;left:16px;top:30px;right:16px;bottom:24px;border-radius:44px;background:#e9ebee;overflow:hidden"><div style="position:absolute;left:0;top:0;right:0;height:74px;background:#1877f2;color:#fff;font:800 32px Poppins;display:flex;align-items:center;padding-left:24px;z-index:3">facebook</div>'
          f'<div id="c_feed" style="position:absolute;left:0;top:74px;width:100%;height:2700px">{cards}</div></div></div></div>')
    b += big('c_f', 1640, '<span class="y">FEED SAHAJA</span>', 110)
    scene('s_c', 12.2, 16.25, BG_NAVY, b)
    A('#c_s', {'opacity': 0}, {'opacity': 1}, 12.3, .25)
    A('#c_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 13.6, .3, 'back.out(2)'); sfx(13.6, 'stamp', -11)
    A('#c_ph', {'opacity': 0, 'y': 400}, {'opacity': 1, 'y': 0}, 12.7, .6, 'power3.out'); sfx(12.7, 'slide', -13)
    js('tl.to("#c_feed",{y:-1300,duration:3.8,ease:"none"},12.5);')
    A('#c_f', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 14.9, .3, 'back.out(2)'); sfx(14.9, 'pop', -11)
# ---------------------------------------------------------------- A: posting hari-hari -> jar of trust fills (0 - 6.8)
with shifted(9.0):
    b = txt('a_s', 0, 90, W, 'buat posting hari-hari', 'sm', 50, extra='position:absolute') + big('a_b', 150, '<span class="y">POSTING</span><br><span class="w">HARI-HARI</span>', 150, 'line-height:1.02')
    b += ('<div class="abs" id="a_jar" style="left:240px;top:620px;width:600px;height:900px;border-radius:70px 70px 110px 110px;border:10px solid rgba(255,255,255,.5);background:rgba(255,255,255,.07);overflow:hidden;box-shadow:0 0 80px rgba(255,255,0,.15)">'
          f'<div id="a_fill" style="position:absolute;left:0;bottom:0;width:100%;height:100%;background:linear-gradient(0deg,{GRN},{Y});transform-origin:50% 100%;box-shadow:0 0 60px {Y}"></div></div>')
    b += txt('a_t', 240, 1560, 600, 'TRUST', 'lab', 80)
    for k in range(6):
        a_, b_ = CC[k]
        b += f'<div class="abs" id="a_p{k}" style="left:{340 + (k % 2) * 90}px;top:380px;width:220px;height:170px;border-radius:16px;background:#fff;overflow:hidden;box-shadow:0 14px 30px rgba(0,0,0,.45)"><div style="height:36px;display:flex;align-items:center;padding:0 12px;gap:8px"><div style="width:22px;height:22px;border-radius:50%;background:#1877f2"></div><div style="width:90px;height:8px;border-radius:4px;background:#ccd0d5"></div></div><div style="height:134px;background:url(assets/img/post_{PO[k % 5]}.jpg) center/cover"></div></div>'
    b += big('a_n', 1700, '<span class="y">TRUST</span> <span class="w">NAIK</span>', 120)
    scene('s_a', 0.0, 6.9, BG_PURPLE, b, fade=.15)
    A('#a_s', {'opacity': 0}, {'opacity': 1}, .15, .25); A('#a_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, .2, .3, 'back.out(2)'); sfx(.2, 'stamp', -11)
    A('#a_jar', {'opacity': 0, 'y': 200}, {'opacity': 1, 'y': 0}, .7, .6, 'power3.out'); A('#a_t', {'opacity': 0}, {'opacity': 1}, 1.0, .3)
    js('gsap.set("#a_fill",{scaleY:.05});')
    js('tl.to("#a_fill",{scaleY:1,duration:5.0,ease:"power1.inOut"},1.2);')
    for k in range(6):
        t = 1.4 + k * .8
        js(f'tl.fromTo("#a_p{k}",{{opacity:0,y:-120,scale:.7}},{{opacity:1,y:520,scale:.8,duration:.7,ease:"power2.in",immediateRender:false}},{t:.3f});')
        js(f'tl.to("#a_p{k}",{{opacity:0,duration:.15}},{t + .72:.3f});'); sfx(t + .68, ['pop', 'click', 'pop', 'ting', 'click', 'pop'][k], -14)
    INIT.append('gsap.set("#a_p0,#a_p1,#a_p2,#a_p3,#a_p4,#a_p5",{opacity:0});')
    A('#a_n', {'opacity': 0, 'scale': 1.5}, {'opacity': 1, 'scale': 1}, 5.4, .3, 'expo.out'); sfx(5.4, 'stamp', -9); sfx(5.4, 'boom', -11)
# ---------------------------------------------------------------- D: zaman berubah, fundamental masih sama (16.3 - 24.8)
with shifted(-0.4):
    b = txt('d_s', 0, 90, W, 'walaupun zaman dah berubah', 'sm', 50, extra='position:absolute') + big('d_b', 150, '<span class="y">TRUST</span> <span class="w">NAIK</span>', 140)
    b += (f'<div class="glass" id="d_k0" style="left:90px;top:560px;width:900px;height:340px"></div>' + txt('d_l0', 90, 590, 900, 'AI · TEKNOLOGI', 'lab', 52)
          + '<div class="abs" style="left:170px;top:760px;width:740px;height:8px;border-radius:4px;background:rgba(255,255,255,.3)"></div><div class="abs" id="d_dot0" style="left:150px;top:738px;width:50px;height:50px;border-radius:50%;background:#fff;box-shadow:0 0 30px #fff"></div>')
    b += (f'<div class="glass" id="d_k1" style="left:90px;top:1000px;width:900px;height:520px;border-color:{Y};box-shadow:0 0 60px {Y}33"></div>' + txt('d_l1', 90, 1030, 900, 'TRUST · CONVERSION', 'lab', 52)
          + f'<div class="abs" style="left:170px;top:1200px;width:740px;height:8px;border-radius:4px;background:rgba(255,255,255,.3)"></div><div class="abs" id="d_dot1" style="left:495px;top:1178px;width:50px;height:50px;border-radius:50%;background:{Y};box-shadow:0 0 30px {Y}"></div>'
          + f'<svg class="abs" id="d_anc" style="left:480px;top:1260px" width="120" height="120" viewBox="0 0 64 64" fill="none" stroke="{Y}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><circle cx="32" cy="12" r="6"/><path d="M32 18 V54 M18 34 H46 M10 40 C12 52 22 56 32 56 C42 56 52 52 54 40"/></svg>')
    b += big('d_m', 1620, '<span class="y">MASIH SAMA</span>', 120)
    scene('s_d', 16.3, 24.9, BG_NAVY, b)
    A('#d_s', {'opacity': 0}, {'opacity': 1}, 16.4, .25)
    A('#d_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 19.1, .3, 'back.out(2)'); sfx(19.1, 'stamp', -11)
    A('#d_k0,#d_l0,#d_dot0', {'opacity': 0, 'y': 80}, {'opacity': 1, 'y': 0}, 17.0, .45, 'back.out(1.5)'); sfx(17.0, 'click', -13)
    js('tl.fromTo("#d_dot0",{x:0},{x:640,duration:.9,ease:"power3.in",immediateRender:false},17.9);')
    js('tl.to("#d_dot0",{x:0,duration:.9,ease:"power3.inOut"},19.0);')
    js('tl.to("#d_dot0",{x:640,duration:.9,ease:"power3.inOut"},20.2);')
    A('#d_k1,#d_l1,#d_dot1,#d_anc', {'opacity': 0, 'y': 80}, {'opacity': 1, 'y': 0}, 20.0, .45, 'back.out(1.5)'); sfx(20.0, 'ting', -13)
    js('tl.to("#d_dot1",{x:14,duration:.5,ease:"sine.inOut",yoyo:true,repeat:5},21.0);')
    A('#d_m', {'opacity': 0, 'scale': 1.5}, {'opacity': 1, 'scale': 1}, 23.9, .3, 'expo.out'); sfx(23.9, 'stamp', -9); sfx(23.9, 'boom', -11)
# ---------------------------------------------------------------- E: AI automate kerja (24.9 - 32.9): conveyor
with shifted(-0.5):
    b = txt('e_s', 0, 90, W, 'AI datang, teknologi datang', 'sm', 50, extra='position:absolute') + big('e_b', 150, '<span class="w">AI =</span> <span class="y">AUTOMATE</span>', 104)
    b += '<div class="abs" style="left:60px;top:1000px;width:960px;height:26px;border-radius:13px;background:rgba(255,255,255,.22)"></div>'
    b += logo('e_ai', 'claude', 400, 560, 280, 0)
    b += f'<div class="abs" id="e_gate" style="left:380px;top:850px;width:320px;height:200px;border-radius:30px;border:6px solid {Y};background:rgba(255,255,0,.06);box-shadow:0 0 50px {Y}55"></div>'
    for k in range(4):
        b += (f'<div class="abs" id="e_t{k}" style="left:-300px;top:830px;width:230px;height:150px;border-radius:18px;background:linear-gradient(160deg,#fff,#cfc9ff);box-shadow:0 14px 30px rgba(0,0,0,.45);overflow:hidden"><div style="margin:30px 22px 0;height:12px;border-radius:6px;background:#0F1224;opacity:.7"></div><div style="margin:14px 22px 0;width:120px;height:10px;border-radius:5px;background:#0F1224;opacity:.35"></div>'
              f'<svg class="abs" id="e_c{k}" style="left:150px;top:80px" width="64" height="64" viewBox="0 0 64 64"><circle cx="32" cy="32" r="28" fill="{GRN}"/><path d="M18 33 L28 43 L47 22" fill="none" stroke="#0F1224" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
    b += big('e_f', 1300, '<span class="w">KERJA</span> <span class="y">JADI CEPAT</span>', 100)
    scene('s_e', 24.9, 33.1, BG_PURPLE, b)
    A('#e_s', {'opacity': 0}, {'opacity': 1}, 25.0, .25)
    A('#e_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 26.7, .3, 'back.out(2)'); sfx(26.7, 'stamp', -11)
    A('#e_ai', {'opacity': 0, 'y': -200, 'scale': .6}, {'opacity': 1, 'y': 0, 'scale': 1}, 27.6, .5, 'back.out(1.7)'); sfx(27.6, 'pop', -12)
    A('#e_gate', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, 28.2, .35, 'back.out(1.7)')
    for k in range(4):
        t = 28.6 + k * 1.0
        INIT.append(f'gsap.set("#e_c{k}",{{opacity:0,scale:0}});')
        js(f'tl.fromTo("#e_t{k}",{{x:0}},{{x:1400,duration:2.6,ease:"none",immediateRender:false}},{t:.3f});')
        js(f'tl.fromTo("#e_c{k}",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{t + .85:.3f});'); sfx(t + .85, ['click', 'ting', 'click', 'ting'][k], -13)
    A('#e_f', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 31.5, .3, 'back.out(2)'); sfx(31.5, 'stamp', -10)
# ---------------------------------------------------------------- F: strategi kita yang fikir (presenter)
with shifted(-0.5):
    cap('c1', 33.0, 36.1, 'strategi apa semua, itu', 'KITA YANG FIKIR', 34.6, size=96)
cap('c0', 0.05, 2.6, 'waktu zaman aku start tu', None)
tag('tg', 0.1, 6.0, 'TANPA PAID ADS · KISAH AKU')
assemble()
