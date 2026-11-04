# ====================================================================== NEW 2D/3D BEATS (times already on the NEW cut: use M(old_time))
def vclip(sid, src, t0, dur, style, mstart=0, tr=None):
    VT[0] += 1
    return f'<video class="clip pv" id="{sid}" src="{src}" muted playsinline data-start="{t0:.3f}" data-duration="{dur:.3f}" data-media-start="{mstart}" data-track-index="{VT[0]}" style="{style}"></video>'
VT = [10]

# ---------------------------------------------------------------- UPGRADE SKILL: skill tower grows, income does not (stage)
t0, t1 = M(11.9), M(17.4)
b = txt('up_s', 0, 50, 1920, 'ramai orang akan cakap kena', 'sm', 50) + f'<div class="abs bg2" id="up_b" style="left:0;width:1920px;top:105px;text-align:center;font-size:150px"><span class="y">UPGRADE</span> <span class="w">SKILL</span></div>'
# FULL-SCREEN staircase: five skill "blocks" climb across the whole frame, each topped by a big AI logo; the income line below stays flat
BK = [('#7b3fe4', 'CHATGPT'), ('#e4572e', 'CLAUDE'), ('#2e86e4', 'DEEPSEEK'), ('#e4b82e', 'LOVABLE'), ('#3fbf7f', 'MANUS')]
for k, (col, nm) in enumerate(BK):
    x = 90 + k * 350; h_ = 150 + k * 80; y = 880 - h_
    b += (f'<div class="abs" id="up_k{k}" style="left:{x}px;top:{y}px;width:320px;height:{h_}px;border-radius:16px 16px 6px 6px;transform-origin:50% 100%;background:linear-gradient(180deg,{col},{col}88);'
          f'box-shadow:0 24px 50px rgba(0,0,0,.5),inset 0 -10px 0 rgba(0,0,0,.25),inset 16px 0 0 rgba(255,255,255,.16)"><div style="position:absolute;left:30px;right:30px;top:{h_ - 70}px;height:8px;border-radius:4px;background:rgba(255,255,255,.4)"></div>'
          f'<div style="position:absolute;left:30px;width:{140 + k * 20}px;top:{h_ - 48}px;height:6px;border-radius:3px;background:rgba(255,255,255,.28)"></div></div>')
    b += logo(f'up_l{k}', AIS[k][0], x + 75, y - 190, 170, -6 + k * 3) + txt(f'up_n{k}', x, y + 22, 320, nm, 'lab', 34, extra='color:#fff')
b += (f'<div class="abs" id="up_m" style="left:90px;top:975px;width:1740px;height:10px;border-radius:5px;background:rgba(255,255,255,.2)"></div>'
      f'<div class="abs" id="up_mf" style="left:90px;top:975px;width:150px;height:10px;border-radius:5px;background:{Y};box-shadow:0 0 22px {Y}"></div>'
      + txt('up_i', 90, 915, 400, 'INCOME', 'lab', 44, 'left') + txt('up_q', 700, 895, 90, '?', 'num', 100))
# full-screen platform plates (the user's own screenshots, perspective-tilted, filling 100 % of the frame); ChatGPT has no screenshot -> drawn chat screen
SHOT = [None, 'assets/img/claude_site.png', 'assets/img/site_deepseek.png', 'assets/img/lovable_site.png', 'assets/img/site_manus.png']
for k in range(5):
    if SHOT[k]:
        inner = f'<img src="{SHOT[k]}" style="position:absolute;left:-60px;top:-60px;width:2040px;height:1275px;object-fit:cover;transform:perspective(2200px) rotateY({-7 if k % 2 else 7}deg) rotateX(3deg) scale(1.1)">'
    else:
        inner = ('<div style="position:absolute;inset:0;background:linear-gradient(180deg,#2a2a2a,#171717)"></div>'
                 '<div style="position:absolute;left:0;right:0;top:330px;text-align:center;font:600 78px Poppins;color:#ececec">Apa yang boleh saya bantu?</div>'
                 '<div style="position:absolute;left:330px;top:500px;width:1260px;height:130px;border-radius:65px;background:#2f2f2f;box-shadow:0 20px 60px rgba(0,0,0,.5);transform:perspective(2200px) rotateX(3deg) rotateY(7deg)"><div style="position:absolute;left:56px;top:38px;font:500 44px Poppins;color:#8e8e8e">Tanya apa-apa...</div></div>')
    badge = (f'<div class="abs" style="left:70px;top:800px;width:600px;height:170px;border-radius:30px;background:rgba(10,8,30,.84);box-shadow:0 20px 50px rgba(0,0,0,.5)"></div>'
             + logo(f'up_pb{k}', AIS[k][0], 100, 820, 130, 0) + txt(f'up_pn{k}', 250, 850, 400, AIS[k][1], 'bg2 w', 60, 'left'))
    b += f'<div class="abs" id="up_p{k}" data-layout-allow-overlap style="left:0;top:0;width:1920px;height:1080px;overflow:hidden;background:#0b0820;z-index:{20 + k}"><div class="abs" id="up_pw{k}" style="left:0;top:0;width:1920px;height:1080px">{inner}</div>{badge}</div>'
scene('s_up', t0, t1, 'full', BG_PURPLE, b)
A('#up_s', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, t0 + .2, .3)
A('#up_b', {'opacity': 0, 'scale': .6, 'filter': 'blur(12px)'}, {'opacity': 1, 'scale': 1, 'filter': 'blur(0px)'}, M(12.35), .3, 'back.out(2)'); sfx(M(12.35), 'stamp', -12)
for k in range(5):
    tp_ = M(12.95 + k * .5)
    A(f'#up_p{k}', {'opacity': 0, 'x': 1920}, {'opacity': 1, 'x': 0}, tp_, .22, 'power3.out'); sfx(tp_, ['click', 'pop', 'click', 'ting', 'pop'][k], -13)
    js(f'tl.fromTo("#up_pw{k}",{{scale:1}},{{scale:1.07,duration:.6,ease:"none",immediateRender:false}},{tp_:.3f});')
T('#up_p0,#up_p1,#up_p2,#up_p3,#up_p4', {'x': -1920}, M(15.45), .3, 'power2.in'); sfx(M(15.45), 'slide', -14)
for k in range(5):
    tt = M(15.55 + k * .1)
    A(f'#up_k{k}', {'opacity': 0, 'scaleY': 0}, {'opacity': 1, 'scaleY': 1}, tt, .4, 'back.out(1.3)')
    A(f'#up_n{k}', {'opacity': 0}, {'opacity': 1}, tt + .2, .25)
    A(f'#up_l{k}', {'opacity': 0, 'y': -260, 'rotation': -30, 'scale': .6}, {'opacity': 1, 'y': 0, 'rotation': -6 + k * 3, 'scale': 1}, tt + .1, .45, 'bounce.out')
sfx(M(15.55), 'pop', -13); sfx(M(15.75), 'click', -13); sfx(M(15.95), 'pop', -13)
A('#up_m,#up_mf', {'opacity': 0}, {'opacity': 1}, M(15.55), .3)
js(f'tl.to("#up_mf",{{width:560,duration:1.2,ease:"sine.out"}},{M(15.75):.3f});')
A('#up_i', {'opacity': 0}, {'opacity': 1}, M(15.7), .3); A('#up_q', {'opacity': 0, 'scale': .3, 'rotation': -30}, {'opacity': 1, 'scale': 1, 'rotation': 0}, M(16.3), .35, 'back.out(2.4)'); sfx(M(16.3), 'ting', -11)
for k in range(5): js(f'tl.to("#up_l{k}",{{y:{(-1) ** k * 10},duration:1.2,ease:"sine.inOut",yoyo:true,repeat:1}},{M(16.2) + k * .08:.3f});')

# ---------------------------------------------------------------- INTRO behind head: workshop photos + real training clips
t0, t1 = M(51.6), M(65.4)
els = f'<div class="abs" id="in_amA" style="left:70px;top:90px;width:560px;height:373px;border-radius:20px;overflow:hidden;border:3px solid rgba(255,255,255,.5);box-shadow:0 30px 70px rgba(0,0,0,.6);transform:perspective(1600px) rotateY(18deg) rotate(-3deg)"><img src="assets/photos/am1.jpg" style="width:100%;height:100%;object-fit:cover"></div>'
els += txt('in_a1', 70, 480, 560, 'NAMA AKU', 'lab', 34, extra='transform:rotate(-3deg)') + txt('in_a2', 70, 525, 560, 'AKRAM ZUHAIR', 'num', 50, extra='transform:rotate(-3deg);white-space:nowrap')
els += imgcard('in_p', 'assets/img/site_profile.png', 1240, 90, 600, 375, 4, -16)
els += f'<div class="abs" id="in_amB" style="left:1280px;top:520px;width:540px;height:360px;border-radius:20px;overflow:hidden;border:3px solid {Y};box-shadow:0 0 60px {Y}55,0 30px 70px rgba(0,0,0,.6);transform:perspective(1600px) rotateY(-16deg) rotate(3deg)"><img src="assets/photos/am5.jpg" style="width:100%;height:100%;object-fit:cover"></div>'
els += txt('in_b1', 1280, 890, 540, 'PANGGIL', 'lab', 28, extra='transform:rotate(3deg)') + txt('in_b2', 1280, 925, 540, 'COACH AM', 'bg2 y', 62, extra='white-space:nowrap;transform:rotate(3deg)')
tk, tp = M(59.0), M(62.4)
els += f'<div class="abs" id="in_ck" style="left:70px;top:625px;width:250px;height:360px;border-radius:20px;overflow:hidden;border:3px solid rgba(255,255,255,.5);box-shadow:0 30px 70px rgba(0,0,0,.6);transform:rotate(-5deg)">' + vclip('in_vk', 'assets/clips/epic.mp4', tk, t1 - tk, 'left:0;top:-20px;width:250px;height:445px;object-fit:cover') + '</div>'
els += f'<div class="chip abs" id="in_ckl" style="left:50px;top:990px;width:290px;height:46px;font-size:24px;transform:rotate(-5deg)">KELAS · TRAINING</div>'
els += f'<div class="abs" id="in_cp" style="left:380px;top:640px;width:430px;height:250px;border-radius:20px;overflow:hidden;border:3px solid rgba(255,255,255,.5);box-shadow:0 30px 70px rgba(0,0,0,.6);transform:perspective(1600px) rotateY(14deg) rotate(3deg)">' + vclip('in_vp', 'assets/clips/dji.mp4', tp, t1 - tp, 'left:0;top:-8px;width:430px;height:260px;object-fit:cover', mstart=11) + '</div>'
fg = txt('in_f', 0, 850, 1920, 'AKRAM ZUHAIR · COACH AM', 'bg2 w', 70, extra='white-space:nowrap')
bhscene('s_intro', t0, t1, els, fg)
A('#in_amA,#in_a1,#in_a2', {'opacity': 0, 'x': -200}, {'opacity': 1, 'x': 0}, M(51.9), .5, 'power3.out'); sfx(M(51.9), 'slide', -13)
A('#in_p', {'opacity': 0, 'x': 220}, {'opacity': 1, 'x': 0}, M(54.2), .5, 'power3.out'); sfx(M(54.2), 'slide', -13)
A('#in_amB,#in_b1,#in_b2', {'opacity': 0, 'scale': .5, 'y': 80}, {'opacity': 1, 'scale': 1, 'y': 0}, M(56.7), .45, 'back.out(1.8)'); sfx(M(56.7), 'stamp', -11)
A('#in_ck,#in_ckl', {'opacity': 0, 'y': 160, 'rotation': -20}, {'opacity': 1, 'y': 0, 'rotation': -5}, tk, .45, 'back.out(1.7)'); sfx(tk, 'click', -12)
A('#in_cp', {'opacity': 0, 'x': -160}, {'opacity': 1, 'x': 0}, tp, .45, 'power3.out'); sfx(tp, 'ting', -12)
A('#in_f', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, M(52.3), .4)

# ---------------------------------------------------------------- DESIGN WALL (stage): many panels, drawn 2D designs sliding in tilted rows
def dp(kind, i, x, w, h):
    pal = [('#d62828', '#fcbf49'), ('#0b6e4f', '#f4f1de'), ('#6a2cc9', '#ffd166'), ('#0077b6', '#caf0f8'), ('#f77f00', '#fff3e0'), ('#222', '#ffd60a')][i % 6]
    base = f'position:absolute;left:{x}px;top:0;width:{w}px;height:{h}px;border-radius:14px;overflow:hidden;box-shadow:0 16px 36px rgba(0,0,0,.5);background:{pal[0]}'
    if kind == 'menu':
        inner = (f'<div style="position:absolute;left:0;top:0;width:100%;height:56px;background:{pal[1]};display:flex;align-items:center;justify-content:center;font:800 30px Poppins;color:{pal[0]}">MENU</div>'
                 + ''.join(f'<div style="position:absolute;left:{24 + (j % 2) * (w // 2 - 6)}px;top:{76 + (j // 2) * 62}px;width:{w // 2 - 40}px;height:46px;border-radius:23px;background:rgba(255,255,255,.18)"></div><div style="position:absolute;left:{36 + (j % 2) * (w // 2 - 6)}px;top:{88 + (j // 2) * 62}px;width:{w // 4}px;height:8px;border-radius:4px;background:{pal[1]}"></div>' for j in range(6))
                 + f'<div style="position:absolute;right:20px;bottom:14px;width:70px;height:70px;border-radius:50%;background:{pal[1]}"></div>')
    elif kind == 'banner':
        inner = (f'<div style="position:absolute;left:24px;top:26px;font:800 {h * .24:.0f}px Poppins;line-height:1;color:{pal[1]}">PROMO<br>HARI INI</div><div style="position:absolute;right:-30px;bottom:-40px;width:{h * .9:.0f}px;height:{h * .9:.0f}px;border-radius:50%;background:{pal[1]}"></div>'
                 f'<div style="position:absolute;left:24px;bottom:22px;width:{w * .3:.0f}px;height:34px;border-radius:17px;background:#fff"></div>')
    elif kind == 'poster':
        inner = (f'<div style="position:absolute;left:50%;top:{h * .14:.0f}px;margin-left:-{h * .17:.0f}px;width:{h * .34:.0f}px;height:{h * .34:.0f}px;border-radius:50%;background:{pal[1]}"></div>'
                 f'<div style="position:absolute;left:0;right:0;top:{h * .56:.0f}px;text-align:center;font:800 {h * .13:.0f}px Poppins;color:#fff;line-height:1">LIVE<br>SHOW</div><div style="position:absolute;left:20%;right:20%;bottom:{h * .08:.0f}px;height:8px;border-radius:4px;background:{pal[1]}"></div>')
    elif kind == 'billboard':
        inner = (f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,#8ecae6,#e0f4ff)"></div><div style="position:absolute;left:12%;right:12%;top:14%;height:46%;border:6px solid #333;background:{pal[0]};display:flex;align-items:center;justify-content:center;font:800 {h * .15:.0f}px Poppins;color:{pal[1]}">SALE 50%</div>'
                 f'<div style="position:absolute;left:49%;width:5%;top:60%;height:40%;background:#333"></div>')
    else:
        inner = f'<img src="assets/img/jersey_my.png" style="width:100%;height:100%;object-fit:cover">'
    return f'<div style="{base}">{inner}</div>'
t0, t1 = M(75.9), M(82.2)
KINDS = ['menu', 'banner', 'poster', 'billboard', 'jersey', 'banner', 'menu', 'poster', 'billboard', 'banner']
rows = ''.join(f'<div class="abs" style="left:{20 + c * 316}px;top:0;width:300px;height:760px;overflow:hidden;border-radius:16px;box-shadow:0 18px 40px rgba(0,0,0,.55)"><img id="dw_c{c}" src="assets/img/pin_col{c}.jpg" style="position:absolute;left:0;top:0;width:300px;height:3007px"></div>' for c in range(6))
b = (txt('dg_s', 0, 44, 1920, 'aku start dengan satu skill', 'sm', 50) + f'<div class="abs bg2" id="dg_b" style="left:0;width:1920px;top:100px;text-align:center;font-size:130px;z-index:5"><span class="y">GRAFIK</span> <span class="w">DESIGN</span></div>'
     + f'<div class="abs" id="dg_wall" style="left:0;top:300px;width:1920px;height:760px;transform:perspective(1800px) rotateX(24deg) rotateZ(-3deg) scale(1.08);transform-origin:50% 0"><div class="abs" style="left:0;top:0;width:1920px;height:760px">{rows}</div></div>')
for k, (nm, tt) in enumerate([('BANNER', 78.6), ('POSTER', 79.8), ('MENU KEDAI MAKAN', 80.3)]):
    b += f'<div class="chip abs" id="dg_c{k}" style="left:{[100, 600, 1100][k]}px;top:930px;width:{[440, 440, 700][k]}px;height:110px;font-size:42px;background:rgba(15,18,36,.9);border-color:{Y};color:{Y};z-index:6;box-shadow:0 0 40px {Y}55">{nm}</div>'
scene('s_design', t0, t1, 'full', BG_PURPLE, b)
A('#dg_s', {'opacity': 0}, {'opacity': 1}, t0 + .1, .3); A('#dg_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, M(76.2), .3, 'back.out(2)'); sfx(M(76.2), 'stamp', -12)
A('#dg_wall', {'opacity': 0, 'y': 300}, {'opacity': 1, 'y': 0}, M(76.5), .8, 'power3.out'); sfx(M(76.5), 'zoom', -13)
for c in range(6): js(f'tl.fromTo("#dw_c{c}",{{y:{-100 if c % 2 == 0 else -820}}},{{y:{-840 if c % 2 == 0 else -100},duration:{t1 - t0:.2f},ease:"none",immediateRender:false}},{t0:.3f});')
for k, tt in enumerate([78.6, 79.8, 80.3]): A(f'#dg_c{k}', {'opacity': 0, 'y': 120, 'scale': .6}, {'opacity': 1, 'y': 0, 'scale': 1}, M(tt), .4, 'back.out(1.8)'); sfx(M(tt), ['click', 'pop', 'ting'][k], -13)

# ---------------------------------------------------------------- TRUST: phone with Facebook-style feed, hearts, calendar + meter (behind head)
t0, t1 = M(113.4), M(123.2)
cards = ''
for k in range(6):
    cards += (f'<div style="position:absolute;left:14px;top:{k * 250 + 10}px;width:332px;height:236px;border-radius:14px;background:#fff;overflow:hidden"><div style="height:46px;background:#fff;display:flex;align-items:center;padding:0 12px;gap:10px"><div style="width:30px;height:30px;border-radius:50%;background:#1877f2"></div><div style="width:120px;height:9px;border-radius:5px;background:#ccd0d5"></div></div>'
              f'<div style="height:150px;background:linear-gradient(135deg,{["#d62828", "#6a2cc9", "#0b6e4f", "#f77f00", "#0077b6", "#222"][k]},{["#fcbf49", "#ffd166", "#f4f1de", "#fff3e0", "#caf0f8", "#ffd60a"][k]})"></div>'
              f'<div style="height:40px;display:flex;align-items:center;padding:0 12px;gap:8px"><div style="width:22px;height:22px;border-radius:50%;background:#1877f2"></div><div style="width:22px;height:22px;border-radius:50%;background:#f33e58"></div><div style="width:60px;height:8px;border-radius:4px;background:#ccd0d5"></div></div></div>')
els = (f'<div class="abs" id="tr_ph" style="left:1420px;top:90px;width:390px;height:780px;border-radius:52px;background:#111;border:6px solid #444;box-shadow:0 40px 90px rgba(0,0,0,.65),0 0 0 3px rgba(255,255,255,.2);transform:perspective(1600px) rotateY(-18deg) rotateZ(3deg);overflow:hidden">'
       f'<div style="position:absolute;left:14px;top:26px;right:14px;bottom:20px;border-radius:38px;background:#e9ebee;overflow:hidden"><div style="position:absolute;left:0;top:0;right:0;height:62px;background:#1877f2;color:#fff;font:800 28px Poppins;display:flex;align-items:center;padding-left:20px">facebook</div>'
       f'<div id="tr_feed" style="position:absolute;left:0;top:72px;width:360px;height:1500px">{cards}</div></div></div>')
for i in range(7): els += (f'<div class="abs" id="tr_d{i}" style="left:{50 + i * 118}px;top:{150 + (i % 3) * 36}px;width:104px;height:124px;border-radius:14px;background:#f4f1ea;box-shadow:0 14px 30px rgba(0,0,0,.5);transform:rotate({-6 + i * 2}deg)"><div style="height:32px;background:#1877f2;border-radius:12px 12px 0 0"></div><div style="font:800 44px Poppins;color:#222;text-align:center;line-height:1.35">{i + 1}</div></div>')
for i in range(6):
    els += f'<svg class="abs" id="tr_h{i}" style="left:{1360 + (i % 3) * 120}px;top:620px" width="60" height="56" viewBox="0 0 24 22"><path d="M12 21 C-6 9 4 -3 12 5 C20 -3 30 9 12 21Z" fill="{["#f33e58", "#ff5d73", "#ff2d55"][i % 3]}"/></svg>'
els += (f'<div class="abs" id="tr_m" style="left:1290px;top:120px;width:80px;height:560px;border-radius:40px;background:rgba(255,255,255,.18);border:3px solid #fff;overflow:hidden"><div id="tr_f" style="position:absolute;left:0;bottom:0;width:100%;height:100%;background:linear-gradient(0deg,{GRN},{Y});box-shadow:0 0 40px {Y};transform-origin:50% 100%"></div></div>' + txt('tr_l', 1150, 360, 130, 'TRUST', 'lab', 40, 'right'))
fg = (txt('tr_s', 0, 700, 1920, 'secara tak langsung, buat posting hari-hari', 'sm', 48) + f'<div class="abs bg2" id="tr_b" style="left:0;width:1920px;top:750px;text-align:center;font-size:150px"><span class="y">TRUST</span> <span class="w">NAIK</span></div>')
bhscene('s_trust', t0, t1, els, fg)
A('#tr_s', {'opacity': 0}, {'opacity': 1}, M(114.1), .3)
A('#tr_ph', {'opacity': 0, 'x': 240, 'rotation': 8}, {'opacity': 1, 'x': 0, 'rotation': 3}, M(114.3), .6, 'power3.out'); sfx(M(114.3), 'slide', -13)
A('#tr_m,#tr_l', {'opacity': 0, 'x': 60}, {'opacity': 1, 'x': 0}, M(114.6), .4)
js(f'tl.to("#tr_feed",{{y:-760,duration:{M(121.5) - M(114.8):.2f},ease:"sine.inOut"}},{M(114.8):.3f});')
for i in range(7): A(f'#tr_d{i}', {'opacity': 0, 'y': -140, 'rotation': -30}, {'opacity': 1, 'y': 0, 'rotation': -6 + i * 2}, M(116.6 + i * .22), .45, 'bounce.out'); sfx(M(116.6 + i * .22), ['key', 'click'][i % 2], -14)
for i in range(6):
    tt = M(116.9 + i * .55)
    A(f'#tr_h{i}', {'opacity': 0, 'y': 40, 'scale': .3}, {'opacity': 1, 'y': 0, 'scale': 1}, tt, .3, 'back.out(2.5)'); js(f'tl.to("#tr_h{i}",{{y:-260,opacity:0,duration:1.3,ease:"power1.in"}},{tt + .4:.3f});'); sfx(tt, 'pop', -15)
js('gsap.set("#tr_f",{scaleY:.12});'); js(f'tl.to("#tr_f",{{scaleY:.5,duration:2.0,ease:"power1.out"}},{M(117.2):.3f});'); js(f'tl.to("#tr_f",{{scaleY:.95,duration:1.0,ease:"power2.out"}},{M(121.6):.3f});')
A('#tr_b', {'opacity': 0, 'scale': 1.7}, {'opacity': 1, 'scale': 1}, M(121.65), .25, 'expo.out'); shake('#tr_b', M(121.9), 12); sfx(M(121.65), 'stamp', -9); sfx(M(122.4), 'ting', -11)

# ---------------------------------------------------------------- HOOK: cave frame (2D rock silhouettes + stalactites) around the crowd
cave = ('<svg class="abs" id="hkcave" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080"><defs><linearGradient id="rk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050509"/><stop offset="1" stop-color="#17141f"/></linearGradient></defs>'
        '<path d="M0 0 H1920 V120 L1840 190 L1790 120 L1700 260 L1650 150 L1560 230 L1500 120 L1400 180 L1330 90 L1250 150 L1180 70 L1100 130 L1020 60 L940 150 L860 80 L780 170 L700 90 L620 190 L560 100 L470 220 L400 120 L320 250 L250 130 L170 200 L100 120 L0 190 Z" fill="url(#rk)"/>'
        '<path d="M0 1080 V240 L90 330 L60 520 L150 640 L100 820 L200 960 L180 1080 Z" fill="url(#rk)"/><path d="M1920 1080 V260 L1830 340 L1860 520 L1770 650 L1830 830 L1720 970 L1750 1080 Z" fill="url(#rk)"/></svg>')
OV[0] = OV[0].replace('<div class="abs" id="hkwipe"', cave + '<div class="abs" id="hkwipe"', 1)
A('#hkcave', {'opacity': 0, 'y': -120}, {'opacity': 1, 'y': 0}, .05, .9, 'power3.out')
T('#hkcave', {'opacity': .35}, 3.4, .5); T('#hkcave', {'opacity': .0}, 7.0, .4)
