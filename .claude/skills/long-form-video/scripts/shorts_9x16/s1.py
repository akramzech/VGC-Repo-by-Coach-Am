import sys; sys.path.insert(0, '..')   # run from scratchpad: python3 s1.py
sys.path.insert(0, '.')
from kit import *
init('S1')
AIS = [('openai', 'CHATGPT'), ('claude', 'CLAUDE'), ('deepseek', 'DEEPSEEK'), ('lovable', 'LOVABLE'), ('manus', 'MANUS')]

# ---------------------------------------------------------------- presenter hook caption
cap('c1', 0.05, 0.95, None, 'PELIK KAN?', 0.05, size=120)

# ---------------------------------------------------------------- A: skill tower + AI logos (0.9 - 5.7)
BK = ['#7b3fe4', '#e4572e', '#2e86e4', '#e4b82e', '#3fbf7f']
b = txt('a_s', 0, 90, W, 'dah belajar banyak-banyak', 'sm', 50, extra='position:absolute') + big('a_b', 150, '<span class="y">SKILL</span> <span class="w">BANYAK</span>', 150)
for k in range(5):
    y = 1560 - k * 190
    b += (f'<div class="abs" id="a_k{k}" style="left:190px;top:{y}px;width:700px;height:170px;border-radius:16px;transform-origin:50% 100%;background:linear-gradient(180deg,{BK[k]},{BK[k]}88);'
          f'box-shadow:0 22px 46px rgba(0,0,0,.5),inset 0 -10px 0 rgba(0,0,0,.25),inset 16px 0 0 rgba(255,255,255,.16)"><div style="position:absolute;left:36px;right:36px;top:58px;height:10px;border-radius:5px;background:rgba(255,255,255,.42)"></div><div style="position:absolute;left:36px;width:300px;top:92px;height:8px;border-radius:4px;background:rgba(255,255,255,.28)"></div></div>')
    b += logo(f'a_l{k}', AIS[k][0], 720 + (k % 2) * 60, y - 60, 150, -8 + k * 4)
b += chip('a_c0', 60, 560, 480, 100, 'SOFTWARE AI', 40) + chip('a_c1', 60, 690, 500, 100, 'AUTOMATION', 40)
scene('s_a', 0.9, 5.75, BG_PURPLE, b)
head_anim('a', 1.0)
for k in range(5):
    t = 1.2 + k * .45
    A(f'#a_k{k}', {'opacity': 0, 'scaleY': 0}, {'opacity': 1, 'scaleY': 1}, t, .4, 'back.out(1.3)'); sfx(t, ['pop', 'click', 'pop', 'ting', 'pop'][k], -13)
    A(f'#a_l{k}', {'opacity': 0, 'y': -380, 'rotation': -30}, {'opacity': 1, 'y': 0, 'rotation': -8 + k * 4}, t + .1, .5, 'bounce.out')
A('#a_c0', {'opacity': 0, 'x': -160}, {'opacity': 1, 'x': 0}, 3.0, .35, 'back.out(1.8)'); sfx(3.0, 'click', -13)
A('#a_c1', {'opacity': 0, 'x': -160}, {'opacity': 1, 'x': 0}, 4.9, .35, 'back.out(1.8)'); sfx(4.9, 'ting', -13)
for k in range(5): js(f'tl.to("#a_l{k}",{{y:{(-1) ** k * 10},duration:1.3,ease:"sine.inOut",yoyo:true,repeat:2}},{3.2 + k * .08:.3f});')

# ---------------------------------------------------------------- B: extra income tak ada (5.75 - 9.0): flat line chart
b = txt('b_s', 0, 90, W, 'tapi', 'sm', 50, extra='position:absolute')
b += big('b_b', 150, '<span class="r">EXTRA INCOME</span><br><span class="r">TAK ADA</span>', 112, 'line-height:1.08')
b += ('<svg class="abs" id="b_g" style="left:60px;top:760px" width="960" height="700" viewBox="0 0 960 700"><path d="M60 30 V620 H920" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="6" stroke-linecap="round"/>'
      '<path d="M60 560 H80 C140 560 160 556 220 556 H880" fill="none" stroke="#FF4D4D" stroke-width="12" stroke-linecap="round" stroke-dasharray="900" stroke-dashoffset="900" id="b_ln" style="filter:drop-shadow(0 0 14px #FF4D4D)"/></svg>')
b += txt('b_rm', 120, 1170, 300, 'RM 0', 'num', 80, 'left', extra='color:#fff')
scene('s_b', 5.75, 9.0, BG_NAVY, b)
A('#b_s', {'opacity': 0}, {'opacity': 1}, 5.85, .2)
A('#b_b', {'opacity': 0, 'scale': 1.5}, {'opacity': 1, 'scale': 1}, 6.5, .3, 'expo.out'); sfx(6.5, 'stamp', -9); sfx(6.5, 'boom', -11)
A('#b_g', {'opacity': 0}, {'opacity': 1}, 7.0, .3)
js('tl.to("#b_ln",{strokeDashoffset:0,duration:1.3,ease:"power2.out"},7.2);')
A('#b_rm', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 8.4, .3, 'back.out(2)'); sfx(8.4, 'ting', -11)

# ---------------------------------------------------------------- C: masih 3 angka / 4 angka (9.0 - 14.1)
b = txt('c_s', 0, 90, W, 'dah start buat, cuma masih', 'sm', 50, extra='position:absolute') + big('c_b', 150, '<span class="y">TAKAT TU JE</span>', 150)
for k, (lbl, val, x, y, tt) in enumerate([('MASIH 3 ANGKA', 'RM ###', 110, 560, 11.7), ('MASIH 4 ANGKA', 'RM #,###', 110, 1060, 12.8)]):
    b += (f'<div class="glass" id="c_k{k}" style="left:{x}px;top:{y}px;width:860px;height:400px"></div>'
          + txt(f'c_l{k}', x, y + 40, 860, lbl, 'lab', 54) + txt(f'c_v{k}', x, y + 140, 860, val, 'num', 120, extra='color:#fff')
          + f'<div class="abs" style="left:{x + 70}px;top:{y + 320}px;width:720px;height:20px;border-radius:10px;background:rgba(255,255,255,.18)"></div><div class="abs" id="c_f{k}" style="left:{x + 70}px;top:{y + 320}px;width:60px;height:20px;border-radius:10px;background:{RED if k == 0 else "#ff9f4d"}"></div>')
scene('s_c', 9.0, 14.1, BG_NAVY, b)
A('#c_s', {'opacity': 0}, {'opacity': 1}, 9.1, .25)
A('#c_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 10.5, .3, 'back.out(2)'); sfx(10.5, 'stamp', -11)
for k, tt in enumerate([11.7, 12.8]):
    A(f'#c_k{k},#c_l{k},#c_v{k}', {'opacity': 0, 'y': 90, 'scale': .85}, {'opacity': 1, 'y': 0, 'scale': 1}, tt, .45, 'back.out(1.6)'); sfx(tt, ['key', 'click'][k], -12)
    js(f'tl.fromTo("#c_f{k}",{{width:60}},{{width:{[240, 400][k]},duration:1.1,ease:"power2.out",immediateRender:false}},{tt + .3:.3f});')

# ---------------------------------------------------------------- presenter: silap dekat mana
cap('c2', 14.2, 16.7, 'so persoalan dia ataupun', 'SILAP DEKAT MANA?', 15.7, size=96)

# ---------------------------------------------------------------- D: cave (16.8 - 28.6): belajar masuk gua, dia seorang je tahu
b = txt('d_s', 0, 90, W, 'ini yang ramai orang silap', 'sm', 50, extra='position:absolute') + big('d_b', 150, '<span class="y">BELAJAR</span><br><span class="w">MASUK GUA</span>', 150, 'line-height:1.02')
b += '<div class="abs" id="d_cave" style="left:90px;top:620px;width:900px;height:800px;border-radius:450px 450px 0 0;background:radial-gradient(closest-side at 50% 72%,#000,#0b0b12 72%,rgba(0,0,0,.25));border:10px solid rgba(255,255,255,.2);box-shadow:inset 0 0 240px #000"></div>'
for k in range(5):
    b += f'<div class="abs" id="d_bk{k}" style="left:{250 + k * 120}px;top:{760 + (k % 2) * 70}px;width:86px;height:62px;border-radius:8px;background:{BK[k]};box-shadow:0 0 30px {BK[k]}88;opacity:.0"></div>'
b += person('d_p', 470, 990, 3.4, Y)
b += f'<div class="abs" id="d_glow" style="left:380px;top:930px;width:320px;height:420px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,255,0,.45),rgba(255,255,0,0));filter:blur(8px)"></div>'
b += chip('d_t', 180, 1460, 720, 100, 'DIA SEORANG JE TAHU', 38) + big('d_f', 1700, '<span class="w">KAWAN RAPAT JE</span> <span class="y">TAHU</span>', 64)
for k in range(3): b += person(f'd_f{k}', 420 + k * 80, 1585, 1.1, '#9aa0c8')
scene('s_d', 16.8, 28.6, BG_NAVY, b)
head_anim('d', 16.9, False)
A('#d_cave', {'opacity': 0, 'y': 300}, {'opacity': 1, 'y': 0}, 18.2, .8, 'power3.out'); sfx(18.2, 'zoom', -13)
A('#d_p', {'opacity': 0, 'scale': .4}, {'opacity': 1, 'scale': 1}, 19.6, .5, 'back.out(2)'); A('#d_glow', {'opacity': 0}, {'opacity': 1}, 19.6, .6); sfx(19.6, 'pop', -12)
for k in range(5):
    t = 21.0 + k * .18
    A(f'#d_bk{k}', {'opacity': 0, 'y': 60, 'scale': .3}, {'opacity': 1, 'y': 0, 'scale': 1}, t, .4, 'back.out(2)'); sfx(t, ['pop', 'click', 'pop', 'ting', 'pop'][k], -14)
A('#d_t', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, 21.7, .3, 'back.out(2)'); sfx(21.7, 'stamp', -10)
A('#d_f', {'opacity': 0, 'y': 30}, {'opacity': 1, 'y': 0}, 23.7, .3)
for k in range(3): A(f'#d_f{k}', {'opacity': 0, 'y': 30}, {'opacity': 1, 'y': 0}, 23.8 + k * .2, .3)
js('tl.to("#d_glow",{scale:1.12,duration:1.2,ease:"sine.inOut",yoyo:true,repeat:3},20.0);')

# ---------------------------------------------------------------- E: orang awam tak tahu (28.6 - end)
b = txt('e_s', 0, 90, W, 'tapi orang awam, target audience', 'sm', 50, extra='position:absolute') + big('e_b', 150, '<span class="w">POTENTIAL</span><br><span class="y">CUSTOMER</span>', 150, 'line-height:1.02')
lit = [(3, 3)]
b += crowd('e', 80, 600, 7, 8, 140, 135, 1.0, lit=lit, col='#7d84b4')
for k, (r, c) in enumerate([(1, 1), (2, 5), (4, 2), (5, 6), (6, 3), (3, 0)]):
    b += txt(f'e_q{k}', 80 + c * 140 - 8, 600 + r * 135 - 70, 80, '?', 'num', 80, extra='color:#fff')
b += big('e_f', 1730, '<span class="r">TAK TAHU PUN</span>', 88)
scene('s_e', 28.6, DUR, BG_NAVY, b, hold=True)
A('#e_s', {'opacity': 0}, {'opacity': 1}, 28.7, .25)
A('#e_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 29.3, .3, 'back.out(2)'); sfx(29.3, 'stamp', -11)
for r in range(8):
    for c in range(7): A(f'#e_{r}_{c}', {'opacity': 0, 'y': 30}, {'opacity': 1, 'y': 0}, 30.0 + (r * 7 + c) * .012, .3)
sfx(30.0, 'zoom', -13)
for k in range(6):
    t = 31.8 + k * .45
    A(f'#e_q{k}', {'opacity': 0, 'scale': .2, 'rotation': -30}, {'opacity': 1, 'scale': 1, 'rotation': 0}, t, .35, 'back.out(2.4)'); sfx(t, 'pop', -13)
A('#e_f', {'opacity': 0, 'scale': 1.5}, {'opacity': 1, 'scale': 1}, 33.8, .3, 'expo.out'); sfx(33.8, 'stamp', -9)
tag('tg', 0.1, 9.0, 'EXTRA INCOME · VLOG DAY 2')
assemble()
