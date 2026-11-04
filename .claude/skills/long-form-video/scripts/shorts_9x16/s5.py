import sys; sys.path.insert(0, '.')
from kit import *
init('S5')

def bubble(i, x, y, w, h, t, mine=False, fs=40):
    bg = '#1877f2' if mine else '#e9ebee'; col = '#fff' if mine else '#0F1224'
    return f'<div class="abs" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:30px;background:{bg};color:{col};font:700 {fs}px Poppins;display:flex;align-items:center;padding:0 30px;box-shadow:0 12px 26px rgba(0,0,0,.35)">{t}</div>'

# ---------------------------------------------------------------- C: DM masuk dekat social media (8.4 - 16.8)
with shifted(-6.5):
    b = txt('c_s', 0, 90, W, 'bila DM-DM masuk dekat social media', 'sm', 46, extra='position:absolute') + big('c_b', 150, '<span class="y">DM</span> <span class="w">MASUK</span>', 150)
    for k, (nm, col) in enumerate([('TIKTOK', '#111'), ('INSTAGRAM', '#c13584'), ('FACEBOOK', '#1877f2')]):
        b += f'<div class="abs" id="c_ic{k}" style="left:{110 + k * 300}px;top:420px;width:200px;height:200px;border-radius:44px;background:{col};border:4px solid rgba(255,255,255,.35);box-shadow:0 24px 50px rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;color:#fff;font:800 34px Poppins">{nm[:2]}</div>'
        b += f'<div class="abs" id="c_bd{k}" style="left:{250 + k * 300}px;top:398px;width:66px;height:66px;border-radius:50%;background:#ff3b30;color:#fff;font:800 36px Poppins;display:flex;align-items:center;justify-content:center;box-shadow:0 0 24px #ff3b3088">{k + 1}</div>'
    for k, (t_, mine) in enumerate([('Boleh tanya pasal service?', False), ('Harga berapa ya?', False), ('Boleh buat untuk kedai saya?', False), ('Ada contoh design?', False)]):
        b += bubble(f'c_m{k}', 120 + (k % 2) * 130, 720 + k * 160, 760, 120, t_, False, 40)
    b += chip('c_t', 140, 1500, 800, 110, 'ORANG TANYA SERVICE', 44)
    scene('s_c', 8.4, 16.85, BG_PURPLE, b)
    A('#c_s', {'opacity': 0}, {'opacity': 1}, 8.5, .25)
    A('#c_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 9.6, .3, 'back.out(2)'); sfx(9.6, 'stamp', -11)
    for k, tt in enumerate([10.2, 10.5, 10.8]):
        A(f'#c_ic{k}', {'opacity': 0, 'y': -120, 'scale': .6}, {'opacity': 1, 'y': 0, 'scale': 1}, tt, .45, 'bounce.out'); sfx(tt, ['click', 'pop', 'ting'][k], -13)
        A(f'#c_bd{k}', {'opacity': 0, 'scale': 0}, {'opacity': 1, 'scale': 1}, tt + .5, .3, 'back.out(3)')
    for k, tt in enumerate([11.6, 12.4, 13.2, 14.0]):
        A(f'#c_m{k}', {'opacity': 0, 'x': -120 if k % 2 == 0 else 120, 'scale': .85}, {'opacity': 1, 'x': 0, 'scale': 1}, tt, .35, 'back.out(1.6)'); sfx(tt, 'pop', -13)
    A('#c_t', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, 12.0, .35, 'back.out(2)'); sfx(12.0, 'ting', -12)
# ---------------------------------------------------------------- A: dijaga + di-respond betul -> convert sale (0 - 6.4)
with shifted(10.3):
    b = txt('a_s', 0, 90, W, 'kalau dijaga dengan betul', 'sm', 50, extra='position:absolute') + big('a_b', 150, '<span class="y">DM</span> <span class="w">DIJAGA</span>', 150)
    b += (f'<div class="abs" id="a_ph" style="left:150px;top:420px;width:780px;height:1180px"><div style="width:100%;height:100%;border-radius:70px;background:#111;border:8px solid #444;box-shadow:0 40px 90px rgba(0,0,0,.65),0 0 0 3px rgba(255,255,255,.2);overflow:hidden;transform:perspective(1800px) rotateY(-10deg) rotateZ(1.5deg)">'
          f'<div style="position:absolute;left:18px;top:34px;right:18px;bottom:28px;border-radius:50px;background:#fff;overflow:hidden"><div style="position:absolute;left:0;top:0;right:0;height:96px;background:#f4f5f7;border-bottom:2px solid #dde0e4;font:800 36px Poppins;color:#0F1224;display:flex;align-items:center;padding-left:34px">Client baru</div></div></div></div>')
    b += bubble('a_m0', 230, 600, 560, 100, 'Boleh tanya pasal service?', False, 34)
    b += bubble('a_m1', 320, 760, 500, 100, 'Boleh! Ni harga & contoh', True, 34)
    b += bubble('a_m2', 230, 920, 470, 100, 'Okay, saya nak buat', False, 34)
    b += bubble('a_m3', 320, 1080, 500, 100, 'Jom, saya mula sekarang', True, 34)
    b += f'<div class="abs bg2" id="a_sale" style="left:0;width:{W}px;top:1700px;text-align:center;font-size:118px"><span class="y">CONVERT SALE ✓</span></div>'
    scene('s_a', 0.0, 6.4, BG_NAVY, b, fade=.15)
    A('#a_s', {'opacity': 0}, {'opacity': 1}, .1, .25); A('#a_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, .2, .3, 'back.out(2)'); sfx(.2, 'stamp', -11)
    A('#a_ph', {'opacity': 0, 'y': 300}, {'opacity': 1, 'y': 0}, .4, .6, 'power3.out'); sfx(.4, 'slide', -13)
    for k, tt in enumerate([1.0, 2.1, 3.4, 4.3]):
        A(f'#a_m{k}', {'opacity': 0, 'y': 40, 'scale': .85}, {'opacity': 1, 'y': 0, 'scale': 1}, tt, .3, 'back.out(1.7)'); sfx(tt, ['pop', 'click', 'pop', 'click'][k], -13)
    A('#a_sale', {'opacity': 0, 'scale': 1.6}, {'opacity': 1, 'scale': 1}, 5.7, .3, 'expo.out'); sfx(5.7, 'stamp', -9); sfx(5.7, 'boom', -11)
# ---------------------------------------------------------------- D: DM TikTok semata-mata, DM dekat trust (16.85 - 21.45)
with shifted(-0.45):
    b = txt('d_s', 0, 90, W, 'walaupun masuk dekat DM TikTok', 'sm', 50, extra='position:absolute') + big('d_b', 150, '<span class="y">DM</span> <span class="w">DEKAT</span><br><span class="y">TRUST</span>', 150, 'line-height:1.02')
    b += '<div class="abs" id="d_tk" style="left:110px;top:760px;width:300px;height:300px;border-radius:64px;background:#111;border:4px solid rgba(255,255,255,.4);box-shadow:0 24px 60px rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;color:#fff;font:800 56px Poppins">TikTok</div>'
    b += f'<svg class="abs" id="d_ar" style="left:430px;top:850px" width="220" height="120" viewBox="0 0 220 120"><path d="M10 60 H190 M150 20 L196 60 L150 100" fill="none" stroke="{Y}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 12px {Y})"/></svg>'
    b += f'<div class="abs" id="d_m" style="left:700px;top:600px;width:100px;height:700px;border-radius:50px;background:rgba(255,255,255,.18);border:3px solid #fff;overflow:hidden"><div id="d_f" style="position:absolute;left:0;bottom:0;width:100%;height:100%;background:linear-gradient(0deg,{GRN},{Y});box-shadow:0 0 40px {Y};transform-origin:50% 100%"></div></div>'
    b += txt('d_l', 600, 1330, 300, 'TRUST', 'lab', 54)
    scene('s_d', 16.85, 21.45, BG_NAVY, b)
    A('#d_s', {'opacity': 0}, {'opacity': 1}, 16.95, .25)
    A('#d_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 17.9, .3, 'back.out(2)'); sfx(17.9, 'stamp', -11)
    A('#d_tk', {'opacity': 0, 'x': -200}, {'opacity': 1, 'x': 0}, 18.3, .45, 'back.out(1.6)'); sfx(18.3, 'slide', -13)
    A('#d_ar', {'opacity': 0, 'x': -60}, {'opacity': 1, 'x': 0}, 19.0, .35); A('#d_m,#d_l', {'opacity': 0}, {'opacity': 1}, 19.2, .3)
    js('gsap.set("#d_f",{scaleY:.08});'); js('tl.to("#d_f",{scaleY:1,duration:1.8,ease:"power2.out"},19.4);'); sfx(19.4, 'swish_up', -13); sfx(20.5, 'ting', -11)
# ---------------------------------------------------------------- E: funnel: close prospek, influence, buat action (21.45 - 36.2)
with shifted(-0.2):
    b = txt('e_s', 0, 90, W, 'orang yang boleh', 'sm', 50, extra='position:absolute') + big('e_b', 150, '<span class="y">CLOSE</span> <span class="w">PROSPEK</span>', 110)
    LV = [(960, 'PROSPEK', '#6a2cc9'), (700, 'CLOSE', '#2e86e4'), (440, 'ACTION', '#3fbf7f')]
    for k, (wd, nm, col) in enumerate(LV):
        b += f'<div class="abs" id="e_l{k}" style="left:{(W - wd) // 2}px;top:{470 + k * 250}px;width:{wd}px;height:210px;border-radius:30px;background:linear-gradient(180deg,{col},{col}99);box-shadow:0 24px 50px rgba(0,0,0,.45);display:flex;align-items:center;justify-content:center;font:800 62px Poppins;color:#fff;letter-spacing:.06em">{nm}</div>'
    for k in range(6): b += person(f'e_p{k}', 270 + k * 100, 330, .7, Y)
    b += chip('e_i', 170, 1300, 740, 100, 'ADA INFLUENCE', 44)
    b += f'<svg class="abs" id="e_coin" style="left:410px;top:1420px" width="260" height="260" viewBox="0 0 64 64"><circle cx="32" cy="32" r="28" fill="{Y}" stroke="#e6c200" stroke-width="3"/><text x="32" y="43" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="30" fill="#7a5c00">RM</text></svg>'
    scene('s_e', 21.45, 36.25, BG_NAVY, b)
    A('#e_s', {'opacity': 0}, {'opacity': 1}, 21.55, .25)
    A('#e_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 22.5, .3, 'back.out(2)'); sfx(22.5, 'stamp', -11)
    for k, tt in enumerate([23.0, 26.2, 28.6]):
        A(f'#e_l{k}', {'opacity': 0, 'y': 90, 'scale': .85}, {'opacity': 1, 'y': 0, 'scale': 1}, tt, .45, 'back.out(1.6)'); sfx(tt, ['key', 'click', 'ting'][k], -12)
    for k in range(6):
        INIT.append(f'gsap.set("#e_p{k}",{{opacity:0}});')
        t = 24.0 + k * .5
        js(f'tl.fromTo("#e_p{k}",{{opacity:0,y:0}},{{opacity:1,y:{[130, 380, 690, 130, 380, 690][k]},duration:1.1,ease:"power1.inOut",immediateRender:false}},{t:.3f});')
    A('#e_i', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, 29.6, .35, 'back.out(2)'); sfx(29.6, 'ting', -11)
    A('#e_coin', {'opacity': 0, 'scale': 0, 'rotation': -90}, {'opacity': 1, 'scale': 1, 'rotation': 0}, 34.4, .5, 'back.out(2)'); sfx(34.4, 'shing', -10)
# ---------------------------------------------------------------- F: buat action = transaction (36.25 - end)
with shifted(0.05):
    b = txt('f_s', 0, 110, W, 'buat action ni maksudnya', 'sm', 54, extra='position:absolute')
    b += big('f_1', 300, '<span class="w">ADA</span>', 200) + big('f_2', 520, '<span class="y">TRANSACTION</span>', 128)
    b += '<div class="abs" id="f_coin" style="left:80px;top:760px;width:520px;height:520px"><div style="width:100%;height:100%;border-radius:24px;overflow:hidden;border:3px solid rgba(255,255,255,.5);box-shadow:0 30px 70px rgba(0,0,0,.6);transform:rotate(-4deg)"><img src="assets/img/post_uschat.jpg" style="width:100%;height:100%;object-fit:cover"></div></div>'
    b += '<div class="abs" id="f_c2" style="left:520px;top:860px;width:470px;height:470px"><div style="width:100%;height:100%;border-radius:24px;overflow:hidden;border:3px solid rgba(255,255,255,.5);box-shadow:0 30px 70px rgba(0,0,0,.6);transform:rotate(5deg)"><img src="assets/img/post_bao.jpg" style="width:100%;height:100%;object-fit:cover"></div></div>'
    b += chip('f_cp', 140, 1370, 800, 100, 'KLIEN LUAR NEGARA · FULL PAYMENT DULU', 34)
    b += big('f_t', 1540, '<span class="y">DM</span> <span class="w">=</span> <span class="y">DUIT</span>', 150)
    scene('s_f', 36.25, DUR, BG_PURPLE, b, hold=True)
    A('#f_s', {'opacity': 0}, {'opacity': 1}, 36.35, .25)
    A('#f_1', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 37.4, .3, 'back.out(2)'); sfx(37.4, 'stamp', -10)
    A('#f_2', {'opacity': 0, 'scale': 1.5}, {'opacity': 1, 'scale': 1}, 37.95, .3, 'expo.out'); sfx(37.95, 'stamp', -9); sfx(37.95, 'boom', -11)
    A('#f_coin', {'opacity': 0, 'x': -200, 'scale': .8}, {'opacity': 1, 'x': 0, 'scale': 1}, 38.3, .5, 'power3.out'); sfx(38.3, 'shing', -10)
    A('#f_t', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 39.6, .3, 'back.out(2)'); sfx(39.6, 'ting', -10)
    A('#f_c2', {'opacity': 0, 'x': 200, 'scale': .8}, {'opacity': 1, 'x': 0, 'scale': 1}, 38.8, .5, 'power3.out'); sfx(38.8, 'click', -13)
    A('#f_cp', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, 39.3, .35, 'back.out(2)'); sfx(39.3, 'ting', -12)
cap('c1', 0.05, 1.85, 'ini yang ramai', 'TAK PERASAN', 0.6, size=118)
tag('tg', 0.1, 8.0, 'JUAL SKILL · NO.3 CLOSING')
assemble()
