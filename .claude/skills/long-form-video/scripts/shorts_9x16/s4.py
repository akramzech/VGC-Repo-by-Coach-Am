import sys; sys.path.insert(0, '.')
from kit import *
init('S4')
PL4 = ['joker', 'cod', 'luffy']; ROT4 = [-5, 2, 6]
GL = f'fill="none" stroke="{Y}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"'
IC = [('PENULISAN', '<path d="M10 54 L10 46 L44 12 L52 20 L18 54 Z M40 16 L48 24"/>'), ('VIDEO', '<rect x="6" y="14" width="40" height="36" rx="6"/><path d="M46 28 L60 18 V46 L46 36"/>'), ('ANIMATION', '<path d="M32 6 L38 24 L58 26 L42 38 L48 58 L32 46 L16 58 L22 38 L6 26 L26 24 Z"/>')]

# ---------------------------------------------------------------- D: untuk menarik traffic; platform mana; content apa (14.1 - 22.4)
with shifted(-11.3):
    b = txt('d_s', 0, 90, W, 'content ni untuk menarik', 'sm', 50, extra='position:absolute') + big('d_b', 150, '<span class="y">TRAFIK</span>', 150)
    b += crowd('d', 120, 420, 6, 3, 150, 170, .9, lit=[(0, 1), (1, 3), (2, 4), (0, 5)], col='#8a90b8')
    b += big('d_pq', 1000, '<span class="y">PLATFORM MANA?</span>', 100)
    for k, nm in enumerate(['TIKTOK', 'INSTAGRAM', 'FACEBOOK', 'YOUTUBE']):
        b += f'<div class="chip abs" id="d_pl{k}" style="left:160px;top:{1150 + k * 130}px;width:760px;height:108px;font-size:46px;justify-content:center">{nm}</div>'
    b += big('d_cq', 1100, '<span class="w">CONTENT APA?</span>', 120)
    b += ''.join(f'<div class="abs" id="d_po{k}" style="left:{70 + k * 320}px;top:1290px;width:300px;height:300px"><div style="width:100%;height:100%;border-radius:20px;overflow:hidden;border:3px solid rgba(255,255,255,.5);box-shadow:0 24px 50px rgba(0,0,0,.55);transform:rotate({ROT4[k]}deg)"><img src="assets/img/post_{PL4[k]}.jpg" style="width:100%;height:100%;object-fit:cover"></div></div>' for k in range(3))
    scene('s_d', 14.1, 22.4, BG_NAVY, b)
    A('#d_s', {'opacity': 0}, {'opacity': 1}, 14.2, .25)
    A('#d_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 15.2, .3, 'back.out(2)'); sfx(15.2, 'stamp', -11)
    for r in range(3):
        for c in range(6): A(f'#d_{r}_{c}', {'opacity': 0, 'y': 30}, {'opacity': 1, 'y': 0}, 15.5 + (r * 6 + c) * .03, .3)
    A('#d_pq', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 17.4, .3, 'back.out(2)'); sfx(17.4, 'pop', -11)
    for k in range(4): A(f'#d_pl{k}', {'opacity': 0, 'y': 80, 'scale': .85}, {'opacity': 1, 'y': 0, 'scale': 1}, 17.8 + k * .3, .35, 'back.out(1.7)'); sfx(17.8 + k * .3, ['click', 'pop', 'click', 'ting'][k], -13)
    T('#d_pq,#d_pl0,#d_pl1,#d_pl2,#d_pl3', {'opacity': 0, 'y': -30}, 19.5, .3, 'power2.in')
    A('#d_cq', {'opacity': 0, 'scale': 1.5}, {'opacity': 1, 'scale': 1}, 19.95, .28, 'expo.out'); sfx(19.95, 'stamp', -10)
    for k in range(3): A(f'#d_po{k}', {'opacity': 0, 'y': 120, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, 20.5 + k * .3, .45, 'back.out(1.6)'); sfx(20.5 + k * .3, ['key', 'click', 'ting'][k], -13)
# ---------------------------------------------------------------- A: penulisan / video / animation (0 - 4.9)
with shifted(11.1):
    b = txt('a_s', 0, 90, W, 'nak gunakan', 'sm', 50, extra='position:absolute') + big('a_b', 150, '<span class="y">FORMAT</span> <span class="w">APA?</span>', 118)
    for k, (nm, pth) in enumerate(IC):
        y = 480 + k * 420
        b += (f'<div class="glass" id="a_k{k}" style="left:110px;top:{y}px;width:860px;height:370px"></div>'
              f'<svg class="abs" id="a_i{k}" style="left:190px;top:{y + 70}px" width="230" height="230" viewBox="0 0 64 64" {GL}>{pth}</svg>'
              + txt(f'a_n{k}', 440, y + 130, 500, nm, 'lab', 64, 'left')
              + f'<svg class="abs" id="a_v{k}" style="left:830px;top:{y + 25}px" width="90" height="90" viewBox="0 0 64 64"><circle cx="32" cy="32" r="28" fill="none" stroke="{GRN}" stroke-width="5"/><path d="M18 33 L28 43 L47 22" fill="none" stroke="{GRN}" stroke-width="7" stroke-linecap="round"/></svg>')
    scene('s_a', 0.0, 4.95, BG_PURPLE, b, fade=.15)
    A('#a_s', {'opacity': 0}, {'opacity': 1}, .1, .25); A('#a_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, .15, .3, 'back.out(2)'); sfx(.15, 'stamp', -11)
    for k, tt in enumerate([0.5, 1.8, 3.2]):
        A(f'#a_k{k},#a_i{k},#a_n{k}', {'opacity': 0, 'y': 140, 'scale': .85}, {'opacity': 1, 'y': 0, 'scale': 1}, tt, .45, 'back.out(1.6)'); sfx(tt, ['key', 'click', 'ting'][k], -12)
        A(f'#a_v{k}', {'opacity': 0, 'scale': 0}, {'opacity': 1, 'scale': 1}, tt + .9, .3, 'back.out(3)'); sfx(tt + .9, 'ting', -14)
        js(f'tl.to("#a_i{k}",{{y:{(-1) ** k * 14},duration:1.2,ease:"sine.inOut",yoyo:true,repeat:1}},{tt + .5:.3f});')
# ---------------------------------------------------------------- B: zaman AI guna je semuanya, senang, cepat (4.95 - 11.3)
with shifted(11.0):
    b = txt('b_s', 0, 110, W, 'so,', 'sm', 54, extra='position:absolute')
    b += big('b_1', 240, '<span class="w">ZAMAN AI</span>', 170) + big('b_2', 430, '<span class="y">GUNA JE</span>', 200) + big('b_3', 650, '<span class="y">SEMUANYA</span>', 160)
    b += (f'<svg class="abs" id="b_bolt" style="overflow:visible;left:300px;top:900px" width="480" height="560" viewBox="0 0 48 56"><path d="M28 2 L8 32 H22 L18 54 L40 22 H26 Z" fill="{Y}" style="filter:drop-shadow(0 0 22px {Y})"/></svg>')
    b += chip('b_c0', 90, 1540, 420, 110, 'SENANG', 48) + chip('b_c1', 570, 1540, 420, 110, 'CEPAT', 48)
    for k in range(5): b += f'<div class="abs" id="b_sp{k}" style="left:{80 + k * 40}px;top:{1000 + k * 85}px;width:{240 - k * 20}px;height:10px;border-radius:5px;background:linear-gradient(90deg,rgba(255,255,0,0),{Y})"></div>'
    scene('s_b', 4.95, 11.3, BG_PURPLE, b)
    A('#b_s', {'opacity': 0}, {'opacity': 1}, 5.0, .2)
    A('#b_1', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 5.45, .3, 'back.out(2)'); sfx(5.45, 'stamp', -10)
    A('#b_2', {'opacity': 0, 'scale': 1.6}, {'opacity': 1, 'scale': 1}, 6.2, .28, 'expo.out'); sfx(6.2, 'stamp', -10)
    A('#b_3', {'opacity': 0, 'scale': 1.6}, {'opacity': 1, 'scale': 1}, 7.0, .28, 'expo.out'); sfx(7.0, 'boom', -11)
    A('#b_bolt', {'opacity': 0, 'scale': .3, 'rotation': -20}, {'opacity': 1, 'scale': 1, 'rotation': 0}, 7.5, .5, 'back.out(2)'); sfx(7.5, 'zoom', -12)
    A('#b_c0', {'opacity': 0, 'y': 80, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, 8.2, .35, 'back.out(1.8)'); sfx(8.2, 'click', -12)
    A('#b_c1', {'opacity': 0, 'y': 80, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, 9.8, .35, 'back.out(1.8)'); sfx(9.8, 'ting', -12)
    for k in range(5):
        INIT.append(f'gsap.set("#b_sp{k}",{{opacity:0}});')
        js(f'tl.fromTo("#b_sp{k}",{{opacity:0,x:-200}},{{opacity:.9,x:0,duration:.25,ease:"power2.out",immediateRender:false}},{9.6 + k * .1:.3f});')
    js('tl.to("#b_bolt",{scale:1.06,duration:.5,ease:"sine.inOut",yoyo:true,repeat:5},8.0);')
# ---------------------------------------------------------------- E: biar ramai orang tahu kita ada skill (22.4 - end)
with shifted(0):
    b = txt('e_s', 0, 90, W, 'kena biar', 'sm', 50, extra='position:absolute') + big('e_b', 150, '<span class="y">RAMAI ORANG</span><br><span class="w">TAHU</span>', 116, 'line-height:1.02')
    b += crowd('e', 80, 560, 7, 8, 140, 135, 1.0, lit=[], col='#7d84b4')
    b += f'<div class="abs" id="e_sk" style="left:190px;top:1690px;width:700px;height:110px;border-radius:20px;background:linear-gradient(180deg,#fff,#cfc9ff);box-shadow:0 30px 70px rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:54px;color:#0F1224;letter-spacing:.2em">SKILL KAU</div>'
    scene('s_e', 22.4, DUR, BG_NAVY, b, hold=True)
    A('#e_s', {'opacity': 0}, {'opacity': 1}, 22.5, .25)
    A('#e_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 26.9, .3, 'back.out(2)'); sfx(26.9, 'stamp', -11)
    for r in range(8):
        for c in range(7): A(f'#e_{r}_{c}', {'opacity': 0, 'y': 30}, {'opacity': 1, 'y': 0}, 23.2 + (r * 7 + c) * .012, .3)
    sfx(23.2, 'zoom', -13)
    import random
    R_ = random.Random(4); cells = [(r, c) for r in range(8) for c in range(7)]; R_.shuffle(cells)
    for i, (r, c) in enumerate(cells[:34]):
        t = 25.6 + i * .105
        js(f'tl.set("#e_{r}_{c} path,#e_{r}_{c} circle",{{fill:"{Y}"}},{t:.3f});')
        if i % 4 == 0: sfx(t, 'pop', -16)
    A('#e_sk', {'opacity': 0, 'y': 60, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, 28.9, .4, 'back.out(1.8)'); sfx(28.9, 'shing', -11)
cap('c1', 0.05, 2.65, 'yang kedua adalah', 'CONTENT', 0.8, size=130)
tag('tg', 0.1, 7.5, 'JUAL SKILL · NO.2 CONTENT')
assemble()
