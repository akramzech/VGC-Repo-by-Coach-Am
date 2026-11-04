# ================================================================== DAY 2 BODY (appended to engine head) ==================
# every time below is on the CUT timeline (seconds), taken from build/words_out.json after the final cut
HD = tm['hook_dur']              # 8.07
DUR = round(tm['dur'] + 0.35, 3)
NDUR = DUR
WB = []; PM = []; BHI = []
BWF = 'grayscale(1) brightness(.55) contrast(1.1)'
def fg_fade(sid, t0, t1, fade=.35):
    A(f'#{sid}', {'opacity': 0}, {'opacity': 1}, t0, fade, 'power2.out'); T(f'#{sid}', {'opacity': 0}, t1 - fade, fade, 'power2.in')
    SET(f'#{sid}', {'opacity': 0, 'display': 'none'}, t1 + .02); SET(f'#{sid}', {'display': 'block'}, t0 - .01)
def bhscene(sid, t0, t1, els, fg, fade=.35):
    """presenter stays full screen: elements sit BEHIND the cut-out, text sits in front"""
    SCENES.append((t0, t1, 'bh', sid)); BHI.append((sid, round(t0, 3), round(t1, 3)))
    WB.append(f'<div class="bhs" id="{sid}_w">{els}</div>')
    OV.append(f'<div class="ov bhov" id="{sid}">{fg}</div>')
    PM.append(f'<video class="clip pm" id="pm_{sid}" src="assets/matte/{sid}.webm" muted playsinline data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" data-media-start="0" data-track-index="2"></video>')
    A(f'#{sid}_w', {'opacity': 0}, {'opacity': 1}, t0, fade, 'power2.out'); T(f'#{sid}_w', {'opacity': 0}, t1 - fade, fade, 'power2.in')
    SET(f'#{sid}_w', {'opacity': 0, 'display': 'none'}, t1 + .02); SET(f'#{sid}_w', {'display': 'block'}, t0 - .01)
    fg_fade(sid, t0, t1, fade)
def capx(t0, t1, small, items, y=800, fs=110, pos='bc'):
    """items: [(TEXT,'y'|'w'|'r', time)]"""
    CAPSPEC.append(dict(t0=t0, t1=t1, small=small, items=[(a, b, None) for a, b, _ in items], ts=[c for _, _, c in items], y=y, fs=fs, pos=pos))
def box(i, x, y, w, h, inner, rot=0, extra=''):
    return f'<div class="abs" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);{extra}">{inner}</div>'
def glass(i, x, y, w, h, rot=0, extra=''):
    return f'<div class="glass abs" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);{extra}"></div>'
def txt(i, x, y, w, t, cls='num', fs=60, align='center', extra=''):
    return f'<div class="{cls} abs" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;text-align:{align};font-size:{fs}px;{extra}">{t}</div>'
def person(i, x, y, s, col):
    return (f'<svg class="abs" id="{i}" style="left:{x}px;top:{y}px" width="{60 * s:.0f}" height="{110 * s:.0f}" viewBox="0 0 60 110">'
            f'<circle cx="30" cy="22" r="16" fill="{col}"/><path d="M6 108 C6 62 16 46 30 46 C44 46 54 62 54 108 Z" fill="{col}"/></svg>')
def imgcard(i, src, x, y, w, h, rot=0, ry=0, extra=''):
    return (f'<div class="abs" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:22px;overflow:hidden;border:3px solid rgba(255,255,255,.4);'
            f'box-shadow:0 40px 90px rgba(0,0,0,.6);transform:perspective(1800px) rotateY({ry}deg) rotate({rot}deg);{extra}"><img src="{src}" style="width:100%;height:100%;object-fit:cover"></div>')
def logo(i, kind, x, y, s=200, rot=0):
    if kind == 'openai': inner = f'<img src="assets/img/openai.svg" style="width:{s * .62:.0f}px;height:{s * .62:.0f}px">'; bg = '#fff'
    else: inner = f'<img src="assets/img/{kind}.png" style="width:100%;height:100%;object-fit:cover">'; bg = '#fff'
    return (f'<div class="abs" id="{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:{s * .22:.0f}px;background:{bg};box-shadow:0 24px 60px rgba(0,0,0,.55),0 0 0 3px rgba(255,255,255,.35);'
            f'display:flex;align-items:center;justify-content:center;overflow:hidden;transform:rotate({rot}deg)">{inner}</div>')

# ======================================================================= HOOK (0 - HD)
SCENES.append((0, HD, 'hook', 's_hook'))
hk = (f'<div class="abs" id="hkv" style="left:0;top:0;width:1920px;height:1080px;background:radial-gradient(620px 760px at 50% 44%,rgba(0,0,0,0),rgba(0,0,0,.9) 78%)"></div>'
      f'<div class="abs" id="hkwipe" style="left:-300px;top:0;width:300px;height:1080px;background:{Y};opacity:0;transform:skewX(-14deg)"></div>')
for i in range(9):
    hk += person(f'hkpL{i}', 40 + i * 98, 690 + ((i * 37) % 50), .85, 'rgba(120,120,150,.5)')
    hk += person(f'hkpR{i}', 1140 + i * 90, 700 + ((i * 53) % 50), .85, 'rgba(120,120,150,.5)')
for i, (x, y) in enumerate([(160, 160), (1490, 130), (300, 400), (1380, 420)]):
    hk += f'<div class="abs" id="hkq{i}" style="left:{x}px;top:{y}px;width:260px;height:260px;border-radius:50%;border:4px dashed rgba(255,255,255,.55);background:radial-gradient(circle,rgba(255,255,255,.08),rgba(255,255,255,0));display:flex;align-items:center;justify-content:center;font-size:150px;font-weight:800;color:#fff;text-shadow:0 0 30px rgba(255,255,255,.6)">?</div>'
OV.append(f'<div class="ov" id="s_hook" style="background:transparent;display:block;opacity:1">{hk}</div>')
SET('#s_hook', {'display': 'none'}, HD + .05)
A('#hkv', {'opacity': 0}, {'opacity': 1}, 0, .8, 'power2.out')
T('#hkv', {'opacity': .25}, 4.4, .5)
for i in range(9):
    A(f'#hkpL{i}', {'opacity': 0, 'y': 40}, {'opacity': 1, 'y': 0}, 0.3 + i * .05, .3); A(f'#hkpR{i}', {'opacity': 0, 'y': 40}, {'opacity': 1, 'y': 0}, 0.35 + i * .05, .3)
# the lone lit person ("dia seorang je tahu dia hebat")
hk_one = person('hkone', 905, 700, 1.0, Y)
OV[-1] = OV[-1].replace('<div class="abs" id="hkwipe"', hk_one + '<div class="abs" id="hkwipe"')
A('#hkone', {'opacity': 0, 'scale': .3}, {'opacity': 1, 'scale': 1}, 3.35, .35, 'back.out(2)')
T('#hkone', {'filter': 'drop-shadow(0 0 24px #FFFF00) drop-shadow(0 0 60px #FFFF00)'}, 3.4, .3)
T('#hkpL0,#hkpL1,#hkpL2,#hkpL3,#hkpL4,#hkpL5,#hkpL6,#hkpL7,#hkpL8,#hkpR0,#hkpR1,#hkpR2,#hkpR3,#hkpR4,#hkpR5,#hkpR6,#hkpR7,#hkpR8', {'opacity': .45}, 3.5, .4)
for i in range(4): A(f'#hkq{i}', {'opacity': 0, 'scale': .3}, {'opacity': 1, 'scale': 1}, 5.7 + i * .35, .3, 'back.out(2.2)'); sfx(5.7 + i * .35, 'pop', -13)
T('#hkq0,#hkq1,#hkq2,#hkq3', {'opacity': 0}, 7.7, .2)
capx(.2, 1.9, 'cerita ni', [('GUA', 'w', .9)], y=780, fs=0) if False else None
capx(.1, 3.3, 'belajar masuk gua bukan main, tapi last-last', [('BELAJAR', 'w', .05), ('MASUK GUA', 'y', .9)], y=800, fs=120)
capx(3.4, 4.55, '', [('DIA SEORANG JE', 'y', 3.4), ('TAHU DIA HEBAT', 'w', 3.95)], y=790, fs=112)
capx(4.7, 8.0, 'potential customer', [('TAK TAHU', 'r', 6.3), ('KAU ADA SKILL', 'w', 6.9)], y=800, fs=118)
sfx(3.4, 'riser', -12); sfx(3.4, 'boom', -9); sfx(3.4, 'shing', -12); sfx(6.3, 'stamp', -9); sfx(HD - .32, 'slide', -13); sfx(HD - .1, 'shutter', -15)
A('#hkwipe', {'opacity': 1, 'x': 0}, {'opacity': 1, 'x': 2300, 'duration': .32, 'ease': 'power2.inOut', 'immediateRender': False}, HD - .3, .32)
SET('#hkwipe', {'opacity': 0}, HD + .05)

# ======================================================================= UPGRADE SKILL (stage) 11.9 - 17.2
AIS = [('openai', 'CHATGPT'), ('claude', 'CLAUDE'), ('deepseek', 'DEEPSEEK'), ('lovable', 'LOVABLE'), ('manus', 'MANUS')]
t0, t1 = 11.9, 17.2
b = txt('up_s', 0, 50, 1920, 'ramai orang akan cakap kena', 'sm', 50) + f'<div class="abs bg2" id="up_b" style="left:0;width:1920px;top:110px;text-align:center;font-size:150px"><span class="y">UPGRADE</span> <span class="w">SKILL</span></div>'
for k, (lg, nm) in enumerate(AIS):
    x = 190 + k * 330
    b += logo(f'up_l{k}', lg, x, 380 + (k % 2) * 40, 230, -6 + k * 3) + txt(f'up_n{k}', x - 30, 640 + (k % 2) * 40, 290, nm, 'lab', 34, extra='color:#fff')
b += txt('up_r', 0, 800, 1920, '↑', 'num', 150, extra=f'color:{Y};text-shadow:0 0 40px {Y}') + txt('up_i', 0, 790, 1920, 'INCOME ↑ ?', 'bg2 y', 110, extra='white-space:nowrap')
scene('s_up', t0, t1, 'full', BG_PURPLE, b)
A('#up_s', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, t0 + .2, .3)
A('#up_b', {'opacity': 0, 'scale': .6, 'filter': 'blur(12px)'}, {'opacity': 1, 'scale': 1, 'filter': 'blur(0px)'}, 12.35, .3, 'back.out(2)'); sfx(12.35, 'stamp', -12)
for k in range(5):
    tt = 12.9 + k * .45
    A(f'#up_l{k}', {'opacity': 0, 'y': 160, 'scale': .5, 'rotation': -25}, {'opacity': 1, 'y': 0, 'scale': 1, 'rotation': -6 + k * 3}, tt, .45, 'back.out(1.8)'); A(f'#up_n{k}', {'opacity': 0}, {'opacity': 1}, tt + .2, .25)
    sfx(tt, ['pop', 'click', 'pop', 'ting', 'pop'][k], -13)
    js(f'tl.to("#up_l{k}",{{y:{(-1) ** k * 14},duration:1.2,ease:"sine.inOut",yoyo:true,repeat:3}},{tt + .5:.3f});')
A('#up_r', {'opacity': 0, 'y': 80, 'scale': .6}, {'opacity': 1, 'y': 0, 'scale': 1}, 15.55, .35, 'back.out(2)')
T('#up_r', {'opacity': 0}, 16.4, .2); A('#up_i', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 16.35, .35, 'back.out(2)'); sfx(15.6, 'swish_up', -13); sfx(16.4, 'ting', -11)

# ======================================================================= BANYAK GILA SKILL (stage) 19.3 - 31.0
t0, t1 = 19.3, 31.0
b = txt('mn_s', 0, 36, 1920, 'sekarang ni dah banyak gila skill yang kita boleh belajar', 'sm', 50) + f'<div class="abs bg2" id="mn_b" style="left:0;width:1920px;top:96px;text-align:center;font-size:120px"><span class="y">BANYAK GILA</span> <span class="w">SKILL</span></div>'
b += imgcard('mn_c0', 'assets/img/claude_site.png', 70, 330, 600, 375, -3, 22) + imgcard('mn_c1', 'assets/img/lovable_site.png', 660, 300, 600, 375, 0, 0) + imgcard('mn_c2', 'assets/img/site_deepseek.png', 1250, 330, 600, 375, 3, -22)
for k, (lg, nm) in enumerate([('claude', 'CLAUDE'), ('lovable', 'LOVABLE'), ('deepseek', 'DEEPSEEK')]):
    b += logo(f'mn_l{k}', lg, 335 + k * 590, 640, 150, 0)
b += txt('mn_w', 0, 805, 1920, 'seminggu boleh expert', 'sm', 50) + f'<div class="abs bg2" id="mn_h" style="left:0;width:1920px;top:855px;text-align:center;font-size:96px"><span class="y">2–3 SKILL HEAVY</span> <span class="w">SERENTAK</span></div>'
scene('s_many', t0, t1, 'full', BG_PURPLE, b)
A('#mn_s', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, t0 + .1, .3)
A('#mn_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 20.6, .3, 'back.out(2)'); sfx(20.7, 'stamp', -12)
for k, tt in enumerate([21.0, 21.4, 21.8]):
    A(f'#mn_c{k}', {'opacity': 0, 'y': 160, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, tt, .5, 'power3.out'); sfx(tt, ['slide', 'click', 'slide'][k], -13)
    A(f'#mn_l{k}', {'opacity': 0, 'scale': .3}, {'opacity': 1, 'scale': 1}, tt + .3, .3, 'back.out(2.2)')
    js(f'tl.to("#mn_c{k}",{{y:{(-1) ** k * 18},duration:2.2,ease:"sine.inOut",yoyo:true,repeat:4}},{tt + .6:.3f});')
A('#mn_w', {'opacity': 0}, {'opacity': 1}, 23.2, .3)
A('#mn_h', {'opacity': 0, 'scale': .6, 'filter': 'blur(12px)'}, {'opacity': 1, 'scale': 1, 'filter': 'blur(0px)'}, 26.6, .3, 'back.out(2)'); sfx(26.6, 'boom', -10); sfx(29.1, 'shing', -12)
for k in range(3): T(f'#mn_c{k}', {'boxShadow': '0 0 90px #FFFF00aa,0 40px 90px rgba(0,0,0,.6)'}, 29.1 + k * .1, .35)

# ======================================================================= EXTRA INCOME TAK ADA (stage) 37.2 - 46.9
t0, t1 = 37.2, 46.9
b = txt('st_s', 0, 36, 1920, 'dah belajar banyak, software AI & automation tahu, tapi', 'sm', 50) + f'<div class="abs bg2 r" id="st_b" style="left:0;width:1920px;top:100px;text-align:center;font-size:140px">EXTRA INCOME TAK ADA</div>'
b += glass('st_a', 210, 340, 660, 430) + glass('st_c', 1050, 340, 660, 430)
b += txt('st_at', 210, 370, 660, 'MASIH 3 ANGKA', 'lab', 44) + txt('st_ct', 1050, 370, 660, 'MASIH 4 ANGKA', 'lab', 44)
b += txt('st_an', 210, 470, 660, 'RM ###', 'num', 112, extra='white-space:nowrap') + txt('st_cn', 1050, 470, 660, 'RM #,###', 'num', 112, extra='white-space:nowrap')
b += f'<div class="abs" id="st_ab" style="left:270px;top:660px;width:540px;height:24px;border-radius:12px;background:rgba(255,255,255,.14);overflow:hidden"><div id="st_af" style="width:100%;height:24px;border-radius:12px;background:{RED};box-shadow:0 0 24px {RED};transform-origin:0 50%"></div></div>'
b += f'<div class="abs" id="st_cb" style="left:1110px;top:660px;width:540px;height:24px;border-radius:12px;background:rgba(255,255,255,.14);overflow:hidden"><div id="st_cf" style="width:100%;height:24px;border-radius:12px;background:{RED};box-shadow:0 0 24px {RED};transform-origin:0 50%"></div></div>'
b += f'<div class="abs" id="st_q" style="left:0;width:1920px;top:850px;text-align:center"><div class="sm" style="font-size:60px">silap dia <span class="y">dekat mana?</span></div></div>'
b += (f'<svg class="abs" id="st_ch" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080"><line x1="160" y1="760" x2="1760" y2="760" stroke="rgba(255,255,255,.3)" stroke-width="4"/>'
      f'<path id="st_pa" d="M160 750 H760 L1010 640 H1760" fill="none" stroke="{RED}" stroke-width="12" stroke-linecap="butt" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" style="filter:drop-shadow(0 0 14px {RED})"/></svg>'
      + txt('st_l0', 160, 690, 420, 'RM 0', 'num', 70, 'left') + txt('st_l1', 760, 520, 420, 'DAH START BUAT', 'lab', 40, 'left') + txt('st_l2', 1150, 540, 600, 'TAKAT TU JE', 'bg2 r', 64, 'left'))
scene('s_stuck', t0, t1, 'full', BG_NAVY, b)
A('#st_s', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, t0 + .1, .3)
A('#st_l0', {'opacity': 0, 'x': -40}, {'opacity': 1, 'x': 0}, 38.8, .3); A('#st_l1', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, 40.4, .3); A('#st_l2', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 41.7, .3, 'back.out(2)'); sfx(41.7, 'stamp', -11); sfx(40.4, 'swish_up', -13)
js('tl.fromTo("#st_pa",{strokeDashoffset:1},{strokeDashoffset:0,duration:4.0,ease:"none",immediateRender:false},38.2);')
T('#st_ch,#st_l0,#st_l1,#st_l2', {'opacity': 0}, 42.35, .25)
A('#st_b', {'opacity': 0, 'scale': 1.5}, {'opacity': 1, 'scale': 1}, 37.55, .25, 'expo.out'); shake('#st_b', 37.8, 10); sfx(37.55, 'boom', -9)
for sel, tt in [('#st_a,#st_at,#st_an,#st_ab', 42.6), ('#st_c,#st_ct,#st_cn,#st_cb', 43.7)]:
    A(sel, {'opacity': 0, 'y': 80, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, tt, .4, 'back.out(1.6)'); sfx(tt, 'stamp', -11)
js('tl.fromTo("#st_af",{scaleX:.05},{scaleX:.3,duration:.8,ease:"power2.out",immediateRender:false},42.9);'); js('tl.fromTo("#st_cf",{scaleX:.05},{scaleX:.52,duration:.8,ease:"power2.out",immediateRender:false},44.0);')
for sel in ('#st_af', '#st_cf'): T(sel, {'backgroundColor': '#ff7a7a'}, 45.0, .3)
A('#st_q', {'opacity': 0, 'y': 24, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, 45.0, .35, 'back.out(1.8)'); sfx(45.0, 'ting', -11)

# ======================================================================= INTRO (behind head) 51.6 - 65.4
t0, t1 = 51.6, 65.4
els = glass('in_a', 70, 150, 640, 220, -3) + txt('in_a1', 70, 185, 640, 'NAMA AKU', 'lab', 36, extra='transform:rotate(-3deg)') + txt('in_a2', 70, 250, 640, 'AKRAM ZUHAIR', 'num', 52, extra='transform:rotate(-3deg);white-space:nowrap')
els += imgcard('in_p', 'assets/img/site_profile.png', 1180, 110, 700, 438, 4, -16)
els += glass('in_b', 1280, 580, 560, 200, 4) + txt('in_b1', 1280, 610, 560, 'PANGGIL', 'lab', 34, extra='transform:rotate(4deg)') + txt('in_b2', 1280, 665, 560, 'COACH AM', 'bg2 y', 66, extra='transform:rotate(4deg);white-space:nowrap')
for k, (nm, tt) in enumerate([('KELAS', 59.0), ('PRIVATE TRAINING', 62.4), ('PRODUK COURSES', 63.9)]):
    els += f'<div class="chip abs" id="in_c{k}" style="left:{60 + k * 10}px;top:{450 + k * 100}px;width:{[300, 500, 480][k]}px;height:80px;font-size:34px">{nm}</div>'
fg = txt('in_f', 0, 850, 1920, 'AKRAM ZUHAIR · COACH AM', 'bg2 w', 74, extra='white-space:nowrap')
bhscene('s_intro', t0, t1, els, fg)
A('#in_a,#in_a1,#in_a2', {'opacity': 0, 'x': -160}, {'opacity': 1, 'x': 0}, 51.9, .45, 'power3.out'); sfx(51.9, 'slide', -13)
A('#in_p', {'opacity': 0, 'x': 200}, {'opacity': 1, 'x': 0}, 54.2, .5, 'power3.out'); sfx(54.2, 'slide', -13)
A('#in_b,#in_b1,#in_b2', {'opacity': 0, 'scale': .5}, {'opacity': 1, 'scale': 1}, 56.7, .35, 'back.out(2)'); sfx(56.7, 'stamp', -11)
for k, tt in enumerate([59.0, 62.4, 63.9]): A(f'#in_c{k}', {'opacity': 0, 'x': -120}, {'opacity': 1, 'x': 0}, tt, .35, 'back.out(1.6)'); sfx(tt, ['click', 'ting', 'pop'][k], -13)
A('#in_f', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, 52.3, .4)

# ======================================================================= GRAPHIC DESIGN / banner poster menu (stage) 75.9 - 82.2
t0, t1 = 75.9, 82.2
b = txt('dg_s', 0, 50, 1920, 'aku start dengan satu skill', 'sm', 50) + f'<div class="abs bg2" id="dg_b" style="left:0;width:1920px;top:110px;text-align:center;font-size:140px"><span class="y">GRAFIK</span> <span class="w">DESIGN</span></div>'
for k, (nm, tt) in enumerate([('BANNER', 78.6), ('POSTER', 79.8), ('MENU KEDAI MAKAN', 80.3)]):
    b += f'<div class="chip abs" id="dg_c{k}" style="left:{[200, 700, 1200][k]}px;top:{[420, 470, 420][k]}px;width:{[430, 430, 560][k]}px;height:150px;font-size:44px;transform:rotate({[-4, 2, -2][k]}deg)">{nm}</div>'
b += txt('dg_t', 0, 760, 1920, 'banyak benda boleh design', 'sm', 54)
scene('s_design', t0, t1, 'full', BG_PURPLE, b)
A('#dg_s', {'opacity': 0}, {'opacity': 1}, t0 + .1, .3); A('#dg_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 76.2, .3, 'back.out(2)'); sfx(76.2, 'stamp', -12)
for k, tt in enumerate([78.6, 79.8, 80.3]): A(f'#dg_c{k}', {'opacity': 0, 'y': 100, 'scale': .7}, {'opacity': 1, 'y': 0, 'scale': 1}, tt, .4, 'back.out(1.7)'); sfx(tt, ['click', 'pop', 'ting'][k], -13)
A('#dg_t', {'opacity': 0}, {'opacity': 1}, 77.1, .3)

# ======================================================================= NICHE JERSEY (stage) 86.4 - 99.0
t0, t1 = 86.4, 99.0
b = txt('nc_s', 0, 36, 1920, 'aku terfokus kepada satu niche sahaja', 'sm', 50) + f'<div class="abs bg2" id="nc_b" style="left:0;width:1920px;top:96px;text-align:center;font-size:110px"><span class="y">1 SKILL</span> <span class="w">·</span> <span class="y">1 NICHE</span></div>'
for k, (nm, y) in enumerate([('BANNER', 330), ('POSTER', 470), ('MENU', 610)]):
    b += f'<div class="chip abs" id="nc_x{k}" style="left:90px;top:{y}px;width:330px;height:100px;font-size:34px;opacity:.5">{nm}</div>'
b += f'<svg class="abs" id="nc_f" style="left:0;top:0" width="1920" height="1080"><g fill="none" stroke="{Y}" stroke-width="5" stroke-dasharray="14 10" style="filter:drop-shadow(0 0 8px {Y})"><path d="M430 380 C560 380 600 560 700 560"/><path d="M430 520 C560 520 600 570 700 570"/><path d="M430 660 C560 660 600 580 700 580"/></g></svg>'
b += imgcard('nc_j', 'assets/img/jersey_my.png', 700, 270, 460, 405, -2, 0) + imgcard('nc_g', 'assets/img/jersey_grid.png', 1230, 250, 270, 535, 3, -14)
b += f'<div class="abs" id="nc_t" style="left:1530px;top:300px;width:380px"><div class="bg2 y" id="nc_t0" style="font-size:66px">JERSEY</div><div class="bg2 w" id="nc_t1" style="font-size:44px;margin-top:10px">STREET APPAREL</div><div class="bg2 w" id="nc_t2" style="font-size:44px;margin-top:10px">MERCH</div></div>'
b += txt('nc_p', 0, 830, 1920, 'artwork printable · orang jual sebagai merchandise', 'sm', 50)
scene('s_niche', t0, t1, 'full', BG_PURPLE, b)
A('#nc_s', {'opacity': 0}, {'opacity': 1}, t0 + .1, .3)
A('#nc_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 87.2, .3, 'back.out(2)'); sfx(87.4, 'stamp', -12)
A('#nc_x0,#nc_x1,#nc_x2', {'opacity': 0, 'x': -80}, {'opacity': .5, 'x': 0, 'stagger': .1}, 88.2, .3); A('#nc_f', {'opacity': 0}, {'opacity': 1}, 89.0, .4)
A('#nc_j', {'opacity': 0, 'scale': .6, 'y': 100}, {'opacity': 1, 'scale': 1, 'y': 0}, 90.1, .5, 'back.out(1.6)'); sfx(90.2, 'boom', -10); sfx(90.2, 'shutter', -12)
A('#nc_t0', {'opacity': 0, 'x': 60}, {'opacity': 1, 'x': 0}, 90.5, .3); A('#nc_t1', {'opacity': 0, 'x': 60}, {'opacity': 1, 'x': 0}, 91.9, .3); sfx(91.9, 'click', -13)
A('#nc_g', {'opacity': 0, 'x': 160}, {'opacity': 1, 'x': 0}, 94.2, .5, 'power3.out'); sfx(94.2, 'slide', -13)
A('#nc_p', {'opacity': 0}, {'opacity': 1}, 95.2, .3); A('#nc_t2', {'opacity': 0, 'x': 60}, {'opacity': 1, 'x': 0}, 98.1, .3); sfx(98.1, 'ting', -12)
js('tl.to("#nc_j",{y:-14,duration:2.4,ease:"sine.inOut",yoyo:true,repeat:3},92.0);')

# ======================================================================= 5-6 OWNER BRAND (behind head) 99.2 - 108.0
t0, t1 = 99.2, 108.0
els = imgcard('ow_g', 'assets/img/gpanel.png', 80, 140, 600, 405, -4, 14) + imgcard('ow_j', 'assets/img/jersey_my2.png', 1250, 140, 520, 458, 5, -14)
fg = (txt('ow_s', 0, 690, 1920, 'dalam masa sebulan, owner brand yang buat design', 'sm', 48) +
      f'<div class="abs bg2" id="ow_n" style="left:0;width:1920px;top:740px;text-align:center;font-size:190px"><span class="y">5–6</span> <span class="w" style="font-size:90px">OWNER BRAND</span></div>')
bhscene('s_owner', t0, t1, els, fg)
A('#ow_s', {'opacity': 0}, {'opacity': 1}, 99.6, .3)
A('#ow_g', {'opacity': 0, 'x': -200}, {'opacity': 1, 'x': 0}, 100.9, .5, 'power3.out'); sfx(100.9, 'slide', -13)
A('#ow_n', {'opacity': 0, 'scale': 1.7}, {'opacity': 1, 'scale': 1}, 103.0, .25, 'expo.out'); shake('#ow_n', 103.25, 12); sfx(103.05, 'stamp', -9); sfx(103.05, 'boom', -11)
A('#ow_j', {'opacity': 0, 'x': 200}, {'opacity': 1, 'x': 0}, 104.4, .5, 'power3.out'); sfx(104.4, 'slide', -13)

# ======================================================================= FACEBOOK FEED -> TRUST (behind head) 113.4 - 123.2
t0, t1 = 113.4, 123.2
els = ''
for i in range(7): els += (f'<div class="abs" id="tr_d{i}" style="left:{60 + i * 130}px;top:{140 + (i % 3) * 36}px;width:112px;height:134px;border-radius:16px;background:#f4f1ea;box-shadow:0 14px 30px rgba(0,0,0,.5);transform:rotate({-6 + i * 2}deg)">'
                          f'<div style="height:34px;background:#1877f2;border-radius:14px 14px 0 0"></div><div style="font-size:48px;font-weight:800;color:#222;text-align:center;line-height:1.35">{i + 1}</div></div>')
els += (f'<div class="abs" id="tr_m" style="left:1400px;top:120px;width:90px;height:560px;border-radius:45px;background:rgba(255,255,255,.18);border:3px solid #fff;overflow:hidden"><div id="tr_f" style="position:absolute;left:0;bottom:0;width:100%;height:100%;background:linear-gradient(0deg,{GRN},{Y});box-shadow:0 0 40px {Y};transform-origin:50% 100%"></div></div>'
        + txt('tr_l', 1500, 260, 320, 'TRUST', 'lab', 66, 'left'))
fg = (txt('tr_s', 0, 700, 1920, 'secara tak langsung, buat posting hari-hari', 'sm', 48) +
      f'<div class="abs bg2" id="tr_b" style="left:0;width:1920px;top:750px;text-align:center;font-size:150px"><span class="y">TRUST</span> <span class="w">NAIK</span></div>')
bhscene('s_trust', t0, t1, els, fg)
A('#tr_s', {'opacity': 0}, {'opacity': 1}, 114.1, .3)
A('#tr_m,#tr_l', {'opacity': 0, 'x': 80}, {'opacity': 1, 'x': 0}, 114.3, .4)
for i in range(7): A(f'#tr_d{i}', {'opacity': 0, 'y': -120, 'rotation': -30}, {'opacity': 1, 'y': 0, 'rotation': -6 + i * 2}, 116.6 + i * .22, .45, 'bounce.out'); sfx(116.6 + i * .22, ['key', 'click'][i % 2], -14)
js('gsap.set("#tr_f",{scaleY:.12});'); js('tl.to("#tr_f",{scaleY:.5,duration:2.0,ease:"power1.out"},117.2);'); js('tl.to("#tr_f",{scaleY:.95,duration:1.0,ease:"power2.out"},121.6);')
A('#tr_b', {'opacity': 0, 'scale': 1.7}, {'opacity': 1, 'scale': 1}, 121.65, .25, 'expo.out'); shake('#tr_b', 121.9, 12); sfx(121.65, 'stamp', -9); sfx(122.4, 'ting', -11)

# ======================================================================= ZAMAN BERUBAH, TRUST SAMA (stage) 123.9 - 138.4
t0, t1 = 123.9, 138.4
b = txt('sm_s', 0, 40, 1920, 'walaupun zaman dah berubah', 'sm', 54)
b += glass('sm_a', 110, 190, 780, 650) + glass('sm_c', 1030, 190, 780, 650, 0, f'border-color:{Y};box-shadow:0 0 60px {Y}44')
b += txt('sm_at', 110, 225, 780, 'AI · TEKNOLOGI', 'lab', 48, extra='color:#fff') + txt('sm_ct', 1030, 225, 780, 'TRUST · CONVERSION', 'lab', 48)
b += f'<div class="abs" id="sm_ar" style="left:170px;top:380px;width:660px;height:12px;background:rgba(255,255,255,.2);border-radius:6px"></div><div class="abs" id="sm_ad" style="left:170px;top:350px;width:70px;height:70px;border-radius:50%;background:#fff;box-shadow:0 0 30px #fff"></div>'
b += txt('sm_an', 110, 560, 780, 'LARI LAJU', 'num', 76) + txt('sm_as', 110, 680, 780, 'untuk automate kerja kita', 'sm', 42)
b += f'<div class="abs" id="sm_cr" style="left:1090px;top:380px;width:660px;height:12px;background:rgba(255,255,255,.2);border-radius:6px"></div><div class="abs" id="sm_cd" style="left:1090px;top:350px;width:70px;height:70px;border-radius:50%;background:{Y};box-shadow:0 0 30px {Y}"></div>'
b += f'<svg class="abs" id="sm_an2" style="left:1320px;top:440px" width="120" height="120" viewBox="0 0 64 64" fill="none" stroke="{Y}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><circle cx="32" cy="12" r="6"/><path d="M32 18 V54 M18 34 H46 M12 44 C14 54 24 58 32 58 C40 58 50 54 52 44"/></svg>'
b += txt('sm_cn', 1030, 580, 780, 'TAK LARI', 'bg2 y', 76) + txt('sm_cs', 1030, 690, 780, 'fundamental masih sama', 'sm', 42)
scene('s_same', t0, t1, 'full', BG_NAVY, b)
A('#sm_s', {'opacity': 0}, {'opacity': 1}, t0 + .1, .3)
A('#sm_c,#sm_ct,#sm_cr,#sm_cd', {'opacity': 0, 'x': 120}, {'opacity': 1, 'x': 0}, 125.5, .45, 'power3.out'); sfx(125.5, 'slide', -13)
js('tl.fromTo("#sm_cd",{x:0},{x:240,duration:3.2,ease:"sine.inOut",immediateRender:false},126.0);'); js('tl.to("#sm_cd",{x:230,duration:.1},129.2);')
A('#sm_an2,#sm_cn,#sm_cs', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 130.4, .35, 'back.out(2)'); sfx(130.4, 'stamp', -10)
A('#sm_a,#sm_at,#sm_ar,#sm_ad', {'opacity': 0, 'x': -120}, {'opacity': 1, 'x': 0}, 132.5, .45, 'power3.out'); sfx(132.5, 'slide', -13)
js('tl.fromTo("#sm_ad",{x:0},{x:560,duration:.9,ease:"power3.in",immediateRender:false},133.0);'); sfx(133.0, 'swish_up', -13)
A('#sm_an,#sm_as', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 135.2, .35, 'back.out(2)'); sfx(135.2, 'ting', -11)

# ======================================================================= 3 PERKARA / PILLARS (stage) 141.2 - 149.4
t0, t1 = 141.2, 149.4
b = txt('pl_s', 0, 30, 1920, 'tiga benda · kalau dah belajar banyak gila skill', 'sm', 50) + f'<div class="abs bg2 y" id="pl_b" style="left:0;width:1920px;top:90px;text-align:center;font-size:130px">3 PERKARA</div>'
b += f'<div class="abs" id="pl_slab" style="left:300px;top:300px;width:1320px;height:110px;border-radius:20px;background:linear-gradient(180deg,#fff,#cfc9ff);box-shadow:0 30px 70px rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:56px;color:{NAVY};letter-spacing:.2em">SKILL KAU</div>'
for k, (n, tt, x) in enumerate([('1', 'TRAFFIC', 360), ('2', 'CONTENT', 780), ('3', 'CLOSING', 1200)]):
    b += (f'<div class="abs" id="pl_p{k}" style="left:{x}px;top:440px;width:360px;height:420px;border-radius:18px;background:linear-gradient(180deg,rgba(255,255,0,.28),rgba(255,255,0,.06));border:3px solid {Y};box-shadow:0 0 50px {Y}44">'
          f'<div class="num" style="position:relative;text-align:center;font-size:150px;line-height:1.1;margin-top:40px">{n}</div><div class="lab" style="position:relative;text-align:center;font-size:52px;margin-top:20px">{tt}</div></div>')
b += txt('pl_x', 0, 900, 1920, 'INCOME MASIH TAK NAIK', 'bg2 r', 70, extra='white-space:nowrap')
scene('s_pillars', t0, t1, 'full', BG_PURPLE, b)
A('#pl_s', {'opacity': 0}, {'opacity': 1}, t0 + .1, .3)
for k, tt in enumerate([141.9, 142.4, 142.9]): A(f'#pl_p{k}', {'opacity': 0, 'y': 300}, {'opacity': 1, 'y': 0}, tt, .45, 'back.out(1.5)'); sfx(tt, ['pop', 'click', 'pop'][k], -13)
A('#pl_slab', {'opacity': 0, 'y': -300}, {'opacity': 1, 'y': 0}, 144.1, .5, 'bounce.out'); sfx(144.4, 'boom', -10)
A('#pl_x', {'opacity': 0, 'scale': 1.4}, {'opacity': 1, 'scale': 1}, 145.5, .3, 'expo.out'); shake('#pl_slab', 145.6, 8); sfx(145.5, 'stamp', -10)
A('#pl_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 147.3, .3, 'back.out(2)'); sfx(147.3, 'stamp', -11)
T('#pl_x', {'opacity': 0}, 147.1, .2); T('#pl_p0', {'boxShadow': '0 0 110px #FFFF00cc'}, 148.9, .3)

# ======================================================================= TRAFFIC (stage) 149.3 - 159.8
t0, t1 = 149.3, 159.8
def crowd(prefix, lit=()):
    s = ''
    for r in range(5):
        for c in range(14):
            lit_ = (r, c) in lit
            s += person(f'{prefix}{r}_{c}', 120 + c * 125, 290 + r * 118, .75, Y if lit_ else 'rgba(130,135,170,.42)')
    return s
b = txt('tf_s', 0, 30, 1920, 'yang pertama sekali', 'sm', 50) + f'<div class="abs bg2 y" id="tf_b" style="left:0;width:1920px;top:90px;text-align:center;font-size:130px">TRAFFIC</div>' + crowd('tp', lit=[(2, 6), (2, 7), (3, 6)])
b += txt('tf_t', 0, 930, 1920, 'biar ramai orang tahu kita ada skill tu', 'sm', 50)
scene('s_traffic', t0, t1, 'full', BG_NAVY, b)
A('#tf_s', {'opacity': 0}, {'opacity': 1}, t0 + .1, .3); A('#tf_b', {'opacity': 0, 'scale': 1.7}, {'opacity': 1, 'scale': 1}, 150.6, .25, 'expo.out'); shake('#tf_b', 150.85, 10); sfx(150.6, 'stamp', -9); sfx(150.6, 'boom', -11)
for r in range(5):
    for c in range(14): A(f'#tp{r}_{c}', {'opacity': 0, 'y': 30}, {'opacity': 1, 'y': 0}, 151.0 + (r * 14 + c) * .004, .3)
tf_lit = [(r, c) for r in range(5) for c in range(14) if (r, c) not in [(2, 6), (2, 7), (3, 6)]]
import random as _r; _r.seed(4); _r.shuffle(tf_lit)
for i, (r, c) in enumerate(tf_lit):
    tt = 157.2 + i * (2.4 / len(tf_lit))
    T(f'#tp{r}_{c}', {'filter': 'drop-shadow(0 0 10px #FFFF00)'}, tt, .25)
    js(f'tl.set("#tp{r}_{c} path,#tp{r}_{c} circle",{{fill:"#FFFF00"}},{tt:.3f});')
sfx(157.2, 'riser', -14); sfx(159.5, 'shing', -11)
A('#tf_t', {'opacity': 0}, {'opacity': 1}, 154.4, .3)

# ======================================================================= GUA (behind head) 159.9 - 166.4
t0, t1 = 159.9, 166.4
els = (f'<div class="abs" id="gu_a" style="left:360px;top:60px;width:1200px;height:1100px;border-radius:600px 600px 0 0;background:radial-gradient(closest-side at 50% 70%,#000,#0b0b12 70%,rgba(0,0,0,.2));border:8px solid rgba(255,255,255,.18);box-shadow:inset 0 0 220px #000"></div>'
       + person('gu_p', 905, 650, 1.0, Y))
fg = (txt('gu_s', 0, 700, 1920, 'belajar masuk gua bukan main, tapi last-last', 'sm', 50) +
      f'<div class="abs bg2" id="gu_b" style="left:0;width:1920px;top:760px;text-align:center;font-size:130px"><span class="y">DIA SEORANG JE</span> <span class="w">TAHU</span></div>')
bhscene('s_gua', t0, t1, els, fg)
A('#gu_a', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, 160.9, .6, 'power3.out'); sfx(160.9, 'zoom', -13)
A('#gu_s', {'opacity': 0}, {'opacity': 1}, 161.7, .3)
A('#gu_p', {'opacity': 0, 'scale': .4}, {'opacity': 1, 'scale': 1}, 164.4, .35, 'back.out(2)'); T('#gu_p', {'filter': 'drop-shadow(0 0 30px #FFFF00) drop-shadow(0 0 70px #FFFF00)'}, 164.5, .3)
A('#gu_b', {'opacity': 0, 'scale': 1.6}, {'opacity': 1, 'scale': 1}, 164.6, .25, 'expo.out'); shake('#gu_b', 164.85, 10); sfx(164.6, 'stamp', -9); sfx(164.6, 'boom', -11)

# ======================================================================= ORANG AWAM TAK TAHU (stage) 166.8 - 179.0
t0, t1 = 166.8, 179.0
lit0 = [(2, 6), (2, 7), (3, 6)]
b = txt('aw_s', 0, 24, 1920, 'orang awam, target audience, potential customer', 'sm', 50) + f'<div class="abs bg2 r" id="aw_b" style="left:0;width:1920px;top:80px;text-align:center;font-size:120px">TAK TAHU PUN</div>' + crowd('ap', lit=lit0)
for k, (x, y) in enumerate([(300, 380), (700, 500), (1200, 400), (1560, 520), (950, 330)]):
    b += f'<div class="abs" id="aw_q{k}" style="left:{x}px;top:{y}px;width:150px;text-align:center;font-size:110px;font-weight:800;color:#fff;text-shadow:0 0 30px rgba(255,255,255,.6)">?</div>'
b += f'<div class="chip abs" id="aw_k" style="left:560px;top:880px;width:380px;height:90px;font-size:34px;border-color:{Y};color:{Y}">KAWAN RAPAT JE</div>' + f'<div class="abs bg2" id="aw_t" style="left:0;width:1920px;top:910px;text-align:center;font-size:80px"><span class="w">KAU ADA</span> <span class="y">SKILL</span></div>'
scene('s_awam', t0, t1, 'full', BG_NAVY, b)
A('#aw_s', {'opacity': 0}, {'opacity': 1}, 172.6, .3)
A('#aw_k', {'opacity': 0, 'y': 30, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, 167.0, .35, 'back.out(1.8)'); sfx(167.0, 'ting', -11)
T('#aw_k', {'opacity': 0}, 171.2, .3)
for r in range(5):
    for c in range(14): A(f'#ap{r}_{c}', {'opacity': 0, 'y': 30}, {'opacity': 1, 'y': 0}, t0 + .1 + (r * 14 + c) * .003, .3)
for k in range(5): A(f'#aw_q{k}', {'opacity': 0, 'scale': .3}, {'opacity': 1, 'scale': 1}, 172.9 + k * .35, .3, 'back.out(2.4)'); sfx(172.9 + k * .35, 'pop', -13)
A('#aw_b', {'opacity': 0, 'scale': 1.6}, {'opacity': 1, 'scale': 1}, 176.4, .25, 'expo.out'); shake('#aw_b', 176.65, 12); sfx(176.4, 'stamp', -9)
A('#aw_t', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, 177.5, .3); sfx(177.5, 'boom', -11)
SET('#aw_s', {'opacity': 0}, 176.3)

# ======================================================================= CONTENT (stage) 184.3 - 207.3
t0, t1 = 184.3, 207.3
b = txt('ct_s', 0, 30, 1920, 'yang kedua adalah', 'sm', 50) + f'<div class="abs bg2 y" id="ct_b" style="left:0;width:1920px;top:90px;text-align:center;font-size:130px">CONTENT</div>'
b += (f'<svg class="abs" id="ct_ar" style="left:760px;top:260px" width="400" height="130" viewBox="0 0 400 130"><path d="M20 100 C120 0 280 0 380 100 M330 60 L384 104 L318 118" fill="none" stroke="{Y}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="14 12" style="filter:drop-shadow(0 0 10px {Y})"/></svg>'
      + txt('ct_tr', 560, 400, 800, 'untuk menarik TRAFFIC tadi', 'sm', 54))
for k, nm in enumerate(['TIKTOK', 'INSTAGRAM', 'FACEBOOK', 'YOUTUBE']):
    b += f'<div class="chip abs" id="ct_pl{k}" style="left:{190 + k * 410}px;top:520px;width:370px;height:110px;font-size:42px">{nm}</div>'
b += txt('ct_pq', 0, 680, 1920, 'PLATFORM MANA?', 'bg2 y', 90, extra='white-space:nowrap')
b += txt('ct_cq', 0, 150, 1920, 'CONTENT APA?', 'bg2 w', 130, extra='white-space:nowrap')
IC = [('PENULISAN', '<path d="M10 54 L10 46 L44 12 L52 20 L18 54 Z M40 16 L48 24"/>', 130), ('VIDEO', '<rect x="6" y="14" width="40" height="36" rx="6"/><path d="M46 28 L60 18 V46 L46 36"/>', 700), ('ANIMATION', '<path d="M32 6 L38 24 L58 26 L42 38 L48 58 L32 46 L16 58 L22 38 L6 26 L26 24 Z"/>', 1270)]
for k, (nm, pth, x) in enumerate(IC):
    b += (glass(f'ct_k{k}', x, 310, 520, 390) + f'<svg class="abs" id="ct_i{k}" style="left:{x + 170}px;top:340px" width="180" height="180" viewBox="0 0 64 64" fill="none" stroke="{Y}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 14px {Y})">{pth}</svg>'
          + txt(f'ct_n{k}', x, 535, 520, nm, 'lab', 56)
          + f'<svg class="abs" id="ct_v{k}" style="left:{x + 230}px;top:605px" width="70" height="70" viewBox="0 0 64 64"><circle cx="32" cy="32" r="28" fill="none" stroke="{GRN}" stroke-width="5"/><path d="M18 33 L28 43 L47 22" fill="none" stroke="{GRN}" stroke-width="7" stroke-linecap="round"/></svg>')
b += f'<div class="abs bg2" id="ct_ai" style="left:0;width:1920px;top:770px;text-align:center;font-size:84px"><span class="w">ZAMAN AI</span> <span class="y">GUNA JE SEMUANYA</span></div>'
b += f'<div class="abs bg2" id="ct_sc" style="left:0;width:1920px;top:890px;text-align:center;font-size:76px"><span class="y">SENANG</span> <span class="w">·</span> <span class="y">CEPAT</span></div>'
scene('s_content', t0, t1, 'full', BG_PURPLE, b)
A('#ct_s', {'opacity': 0}, {'opacity': 1}, t0 + .1, .3)
A('#ct_b', {'opacity': 0, 'scale': 1.7}, {'opacity': 1, 'scale': 1}, 185.9, .25, 'expo.out'); shake('#ct_b', 186.15, 10); sfx(185.9, 'stamp', -9); sfx(185.9, 'boom', -11)
A('#ct_ar,#ct_tr', {'opacity': 0, 'y': 40}, {'opacity': 1, 'y': 0}, 188.4, .4); sfx(188.6, 'swish_up', -13)
T('#ct_ar,#ct_tr', {'opacity': 0}, 191.3, .3)
for k in range(4): A(f'#ct_pl{k}', {'opacity': 0, 'y': 80, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, 192.2 + k * .25, .35, 'back.out(1.7)'); sfx(192.2 + k * .25, ['click', 'pop', 'click', 'ting'][k], -13)
A('#ct_pq', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 192.3, .3, 'back.out(2)')
T('#ct_pl0,#ct_pl1,#ct_pl2,#ct_pl3,#ct_pq', {'opacity': 0, 'y': -30}, 194.2, .3, 'power2.in'); T('#ct_b', {'opacity': 0, 'y': -30}, 194.2, .3, 'power2.in'); T('#ct_s', {'opacity': 0}, 194.2, .2)
A('#ct_cq', {'opacity': 0, 'scale': 1.5}, {'opacity': 1, 'scale': 1}, 194.45, .25, 'expo.out'); sfx(194.45, 'stamp', -10)
for k, tt in enumerate([197.2, 198.6, 200.0]):
    A(f'#ct_k{k},#ct_i{k},#ct_n{k}', {'opacity': 0, 'y': 120, 'scale': .8}, {'opacity': 1, 'y': 0, 'scale': 1}, tt, .45, 'back.out(1.6)'); sfx(tt, ['key', 'click', 'ting'][k], -12)
    A(f'#ct_v{k}', {'opacity': 0, 'scale': 0}, {'opacity': 1, 'scale': 1}, 201.9 + k * .2, .3, 'back.out(3)'); sfx(201.9 + k * .2, 'ting', -13)
T('#ct_cq', {'y': -20, 'opacity': .35}, 197.0, .3)
A('#ct_ai', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, 201.9, .3, 'back.out(2)'); sfx(201.9, 'shing', -11)
A('#ct_sc', {'opacity': 0, 'y': 30}, {'opacity': 1, 'y': 0}, 204.6, .35, 'back.out(1.8)'); sfx(204.6, 'stamp', -10)
for k in range(3): js(f'tl.to("#ct_i{k}",{{y:{(-1) ** k * 12},duration:1.2,ease:"sine.inOut",yoyo:true,repeat:2}},{200.8 + k * .1:.3f});')

# ======================================================================= SKILL CLOSING (stage) 211.4 - 233.5
t0, t1 = 211.4, 233.5
b = txt('cl_s', 0, 30, 1920, 'yang ketiga adalah', 'sm', 50) + f'<div class="abs bg2 y" id="cl_b" style="left:0;width:1920px;top:90px;text-align:center;font-size:130px">SKILL CLOSING</div>'
for k, (nm, y, rot) in enumerate([('DM masuk · tanya service', 330, -3), ('DIJAGA dengan betul', 500, 2), ('DIRESPON dengan betul', 670, -2)]):
    b += f'<div class="abs" id="cl_m{k}" style="left:130px;top:{y}px;width:760px;height:130px;border-radius:30px 30px 30px 8px;background:linear-gradient(160deg,#fff,#e4e0ff);color:{NAVY};font-weight:700;font-size:38px;display:flex;align-items:center;padding:0 40px;box-shadow:0 20px 50px rgba(0,0,0,.5);transform:rotate({rot}deg)">{nm}</div>'
b += (f'<svg class="abs" id="cl_ar" style="left:900px;top:430px" width="200" height="200" viewBox="0 0 200 200"><path d="M20 100 H170 M120 50 L172 100 L120 150" fill="none" stroke="{Y}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 14px {Y})"/></svg>'
      + imgcard('cl_w', 'assets/img/wa_chat.png', 1130, 300, 640, 568, 3, -6)
      + txt('cl_wl', 1100, 890, 700, 'KLIEN LUAR NEGARA', 'lab', 40)
      + f'<div class="abs bg2" id="cl_sale" style="left:1440px;top:190px;width:420px;text-align:center;font-size:78px;color:{GRN};text-shadow:0 0 30px {GRN};background:rgba(15,18,36,.85);border:6px solid {GRN};border-radius:18px;transform:rotate(-8deg)">SALE ✓</div>'
      + txt('cl_tk', 0, 960, 1920, 'walaupun masuk dekat DM TikTok · DM dekat TRUST', 'sm', 46))
scene('s_closing', t0, t1, 'full', BG_NAVY, b)
A('#cl_s', {'opacity': 0}, {'opacity': 1}, t0 + .1, .3)
A('#cl_b', {'opacity': 0, 'scale': 1.7}, {'opacity': 1, 'scale': 1}, 211.75, .25, 'expo.out'); shake('#cl_b', 212.0, 10); sfx(211.75, 'stamp', -9); sfx(211.75, 'boom', -11)
for k, tt in enumerate([216.6, 224.7, 226.1]):
    A(f'#cl_m{k}', {'opacity': 0, 'x': -200}, {'opacity': 1, 'x': 0}, tt, .45, 'power3.out'); sfx(tt, ['click', 'pop', 'ting'][k], -12)
A('#cl_ar', {'opacity': 0, 'x': -60}, {'opacity': 1, 'x': 0}, 227.3, .3); A('#cl_w', {'opacity': 0, 'x': 200, 'scale': .8}, {'opacity': 1, 'x': 0, 'scale': 1}, 227.5, .5, 'power3.out'); sfx(227.5, 'slide', -12)
A('#cl_wl', {'opacity': 0}, {'opacity': 1}, 228.2, .3)
A('#cl_sale', {'opacity': 0, 'scale': 1.9}, {'opacity': 1, 'scale': 1}, 228.8, .25, 'expo.out'); shake('#cl_sale', 229.05, 12); flash(228.8, .3, .5) if 'flash' in globals() else None; sfx(228.8, 'stamp', -8); sfx(228.8, 'ting', -10)
A('#cl_tk', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, 230.6, .35); sfx(232.7, 'ting', -11)
js('tl.to("#cl_w",{y:-14,duration:2.2,ease:"sine.inOut",yoyo:true,repeat:2},229.0);')

# ======================================================================= CLOSE PROSPEK -> TRANSACTION (behind head) 233.8 - 250.4
t0, t1 = 233.8, 250.4
els = ''
chain = [('CLOSE PROSPEK', 90, 150, -4, 234.9), ('INFLUENCE', 1230, 130, 4, 242.7), ('ACTION', 90, 560, 3, 246.4), ('TRANSACTION', 1190, 560, -3, 248.3)]
for k, (nm, x, y, rot, tt) in enumerate(chain):
    els += glass(f'cc_g{k}', x, y, 600, 190, rot) + txt(f'cc_t{k}', x, y + 55, 600, nm, 'bg2 y' if k in (1, 3) else 'bg2 w', 64, extra=f'transform:rotate({rot}deg)')
els += (f'<svg class="abs" id="cc_ln" style="left:0;top:0" width="1920" height="1080"><g fill="none" stroke="{Y}" stroke-width="5" stroke-dasharray="14 10" style="filter:drop-shadow(0 0 8px {Y})">'
        '<path d="M700 250 C900 150 1000 150 1230 220"/><path d="M1530 320 C1700 440 600 440 400 560"/><path d="M700 650 C900 740 1000 740 1190 650"/></g></svg>')
fg = (txt('cc_s', 0, 700, 1920, 'orang yang boleh close prospek · ada influence buat prospek', 'sm', 46) +
      f'<div class="abs bg2" id="cc_b" style="left:0;width:1920px;top:780px;text-align:center;font-size:92px"><span class="y">BUAT ACTION</span> <span class="w">= TRANSACTION</span></div>')
bhscene('s_cc', t0, t1, els, fg)
for k, (nm, x, y, rot, tt) in enumerate(chain):
    A(f'#cc_g{k},#cc_t{k}', {'opacity': 0, 'scale': .5}, {'opacity': 1, 'scale': 1}, tt, .4, 'back.out(1.8)'); sfx(tt, ['stamp', 'click', 'ting', 'stamp'][k], -11)
A('#cc_ln', {'opacity': 0}, {'opacity': 1}, 242.6, .6)
A('#cc_s', {'opacity': 0}, {'opacity': 1}, 234.3, .3); A('#cc_b', {'opacity': 0}, {'opacity': 0}, 234.3, .01)
A('#cc_b', {'opacity': 0, 'scale': 1.6}, {'opacity': 1, 'scale': 1}, 247.0, .25, 'expo.out'); shake('#cc_b', 247.25, 12); sfx(247.0, 'boom', -9)

# ======================================================================= OPERATION SKILL + JUAL SKILL (stage) 254.8 - 262.9
t0, t1 = 254.8, 262.9
b = txt('rc_s', 0, 30, 1920, 'skill korang dah dahsyat · tu adalah', 'sm', 50) + f'<div class="abs bg2 y" id="rc_b" style="left:0;width:1920px;top:90px;text-align:center;font-size:120px">OPERATION SKILL</div>'
b += f'<div class="abs" id="rc_slab" style="left:300px;top:640px;width:1320px;height:110px;border-radius:20px;background:linear-gradient(180deg,#fff,#cfc9ff);box-shadow:0 30px 70px rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:56px;color:{NAVY};letter-spacing:.2em">SKILL KAU</div>'
for k, (nm, x) in enumerate([('TRAFFIC', 360), ('CONTENT', 780), ('CLOSING', 1200)]):
    b += f'<div class="abs" id="rc_p{k}" style="left:{x}px;top:790px;width:360px;height:160px;border-radius:14px;background:linear-gradient(180deg,rgba(255,255,0,.4),rgba(255,255,0,.1));border:3px solid {Y};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:48px;color:{Y}">{nm}</div>'
b += f'<div class="abs" id="rc_d" style="left:0;width:1920px;top:230px;text-align:center;font-size:150px;color:{Y};text-shadow:0 0 40px {Y};font-weight:800">$</div>' + f'<div class="abs bg2 y" id="rc_j" style="left:0;width:1920px;top:430px;text-align:center;font-size:130px">JUAL SKILL</div>'
scene('s_recap', t0, t1, 'full', BG_PURPLE, b)
A('#rc_s', {'opacity': 0}, {'opacity': 1}, t0 + .1, .3)
A('#rc_b', {'opacity': 0, 'scale': 1.7}, {'opacity': 1, 'scale': 1}, 255.4, .25, 'expo.out'); shake('#rc_b', 255.65, 10); sfx(255.4, 'stamp', -9); sfx(255.4, 'boom', -11)
A('#rc_slab', {'opacity': 0, 'y': -200}, {'opacity': 1, 'y': 0}, 255.9, .5, 'bounce.out')
for k, tt in enumerate([257.6, 258.0, 258.4]): A(f'#rc_p{k}', {'opacity': 0, 'y': 160}, {'opacity': 1, 'y': 0}, tt, .4, 'back.out(1.6)'); sfx(tt, ['pop', 'click', 'pop'][k], -12)
T('#rc_b', {'opacity': 0, 'y': -30}, 258.9, .25)
A('#rc_d,#rc_j', {'opacity': 0, 'scale': .5}, {'opacity': 1, 'scale': 1}, 259.4, .35, 'back.out(2)'); sfx(259.4, 'stamp', -9); sfx(259.4, 'shing', -11)
T('#rc_slab,#rc_p0,#rc_p1,#rc_p2', {'boxShadow': '0 0 90px #FFFF00aa'}, 259.6, .4)

# ======================================================================= OUTRO (behind head) 263.0 - end
t0, t1 = 263.0, DUR
els = ''
for k, (nm, x, y, rot, tt) in enumerate([('MARKETING SIKIT', 70, 150, -5, 267.2), ('FREELANCING SIKIT', 1260, 130, 5, 268.5), ('EXTRA INCOME PERSONAL', 60, 440, 3, 270.8), ('SIDE INCOME', 1330, 440, -4, 272.8)]):
    els += glass(f'ou_g{k}', x, y, 560, 150, rot) + txt(f'ou_t{k}', x, y + 42, 560, nm, 'lab', 36, extra=f'transform:rotate({rot}deg);color:#fff')
for k, (n, lab, x, y, rot, on) in enumerate([('1', 'SELESAI', 90, 620, -8, False), ('2', 'HARI INI', 340, 640, 6, True), ('3', 'ESOK', 1500, 620, 8, False)]):
    els += (f'<div class="abs" data-layout-allow-overlap id="ou_d{k}" style="left:{x}px;top:{y}px;width:170px;height:220px;border-radius:20px;background:{"rgba(255,255,0,.2)" if on else "rgba(255,255,255,.1)"};border:{"4px solid " + Y if on else "3px dashed rgba(255,255,255,.45)"};transform:rotate({rot}deg);{f"box-shadow:0 0 50px {Y}66" if on else ""}">'
            f'<div class="num" style="position:relative;text-align:center;font-size:80px;margin-top:30px">{n}</div><div class="lab" style="position:relative;text-align:center;font-size:22px;color:{Y if on else "rgba(255,255,255,.6)"}">{lab}</div></div>')
fg = (txt('ou_s', 0, 790, 1920, 'jumpa lagi pada', 'sm', 46) + f'<div class="abs bg2 y" id="ou_b" style="left:0;width:1920px;top:840px;text-align:center;font-size:140px">HARI KETIGA</div>')
bhscene('s_out', t0, t1, els, fg)
for k, tt in enumerate([267.2, 268.5, 270.8, 272.8]): A(f'#ou_g{k},#ou_t{k}', {'opacity': 0, 'scale': .5, 'y': -60}, {'opacity': 1, 'scale': 1, 'y': 0}, tt, .4, 'back.out(1.8)'); sfx(tt, ['pop', 'click', 'pop', 'ting'][k], -12)
for k, tt in enumerate([263.8, 264.2, 274.0]): A(f'#ou_d{k}', {'opacity': 0, 'y': -200, 'rotation': -40}, {'opacity': 1, 'y': 0}, tt, .55, 'bounce.out'); sfx(tt, ['pop', 'click', 'stamp'][k], -12)
A('#ou_s', {'opacity': 0}, {'opacity': 1}, 273.4, .3); A('#ou_b', {'opacity': 0, 'scale': 1.7}, {'opacity': 1, 'scale': 1}, 274.05, .25, 'expo.out'); shake('#ou_b', 274.3, 12); sfx(274.05, 'boom', -9)

# ======================================================================= CAPTIONS on presenter windows
capx(8.3, 11.5, 'bila kita fikir pasal nak cari', [('EXTRA', 'w', 9.6), ('INCOME', 'y', 9.8)], y=800, fs=118)
capx(17.3, 19.2, 'cuma persoalan dia sekarang ni', [('SKILL TU', 'y', 18.4)], y=800, fs=112)
capx(31.2, 37.0, 'dah belajar banyak-banyak skill, software AI dah banyak tahu', [('SEGALA MAK NENEK', 'w', 35.1), ('AUTOMATION', 'y', 36.2)], y=800, fs=100)
capx(47.0, 51.4, 'ini yang kita nak borak dalam content hari ni', [('SILAP DIA', 'w', 45.6), ('DEKAT MANA?', 'y', 46.5)], y=800, fs=104) if False else None
capx(47.0, 51.4, 'ini yang kita nak borak dalam', [('CONTENT', 'y', 48.6), ('HARI NI', 'w', 49.6)], y=800, fs=118)
capx(65.9, 75.7, 'aku start masuk dunia freelancing, dengan satu skill', [('GRAFIK DESIGN', 'y', 72.7)], y=800, fs=118)
capx(82.3, 86.3, 'benda ni aku buat secara tak sengaja', [('TERFOKUS', 'y', 85.8)], y=800, fs=120)
capx(108.1, 113.3, 'zaman aku start tu', [('PAID ADS', 'w', 110.6), ('AKU TAK BELAJAR', 'r', 111.7)], y=800, fs=104)
capx(123.3, 123.8, '', [('TRUST', 'y', 123.4)], y=800, fs=100) if False else None
capx(138.5, 141.1, 'strategi apa semua? itu', [('KITA YANG', 'w', 139.6), ('FIKIRKAN', 'y', 140.6)], y=800, fs=112)
capx(179.0, 184.2, 'itu nombor satu · seni untuk menarik', [('NOMBOR 1', 'w', 178.7), ('TRAFFIC', 'y', 181.6)], y=800, fs=120)
capx(207.4, 211.3, 'yang ketiga', [('NOMBOR 3', 'y', 207.9)], y=800, fs=130)
capx(250.5, 254.7, 'kalau skill korang dah dahsyat sangat', [('YANG KORANG BELAJAR', 'w', 253.8)], y=800, fs=100)
SET('#base', {'opacity': 1}, 0)

# ======================================================================= CAMERA
HX, HY = 950, 410
def cam_xy(S, sx=960):
    tx = min(0, max(W - S * W, sx - S * HX)); ty = min(0, max(H - S * H, 0.42 * H - S * HY)); return round(tx, 1), round(ty, 1)
blocked = [(s[0], s[1]) for s in SCENES if s[2] in ('full', 'bh')]
def in_win(t, wins, pad=0.0): return any(a - pad <= t <= b - 0 + pad for a, b in wins)
CAMK = [(.0, 1.18, 960, 3.2), (3.3, 1.35, 960, .45), (HD - .5, 1.0, 960, .45)]
cyc = [1.16, 1.0, 1.28, 1.1, 1.22, 1.0]; ci = 0; last = HD; cur_S = 1.0
starts = sorted(set(round(s['s'], 2) for s in SEGS))
events = []
for t in starts:
    if t < HD + 1.0 or t > DUR - 3: continue
    if in_win(t, blocked, .9) or t - last < 4.6: continue
    S_ = cyc[ci % len(cyc)]; ci += 1; events.append((t, S_)); last = t
for a, b_ in blocked: events.append((a - .6, 1.0))
events.sort(); cur = 1.0; planned = []
for t, S_ in events:
    if S_ == cur: continue
    if in_win(t + .5, blocked, 0) and S_ != 1.0: continue
    planned.append((t, S_, 960, .8 if S_ != 1.0 else .5)); cur = S_
planned = [k for k in planned if not any(a - 2.4 < k[0] < b_ for a, b_ in blocked)]
CAMK += planned
CAMK = [k for k in CAMK if not (k[0] > HD and any(a - 2.4 < k[0] < b_ for a, b_ in blocked))]
for a, b_ in blocked: CAMK.append((a - .85, 1.0, 960, .6))
CAMK.sort()
clean = []; endp = -1
for k in CAMK:
    if k[0] >= endp - 1e-6: clean.append(k); endp = k[0] + k[3]
CAMK = clean
for a, b_ in blocked:
    if not any(abs(k[0] - (a - .85)) < .01 for k in CAMK): print('WARN reset dropped at', a)
cx, cy = cam_xy(1.0)
js(f'gsap.set("#cam",{{transformOrigin:"0 0",x:{cx},y:{cy},scale:1}});')
for t, S_, sx, d in CAMK:
    x_, y_ = cam_xy(S_, sx); js(f'tl.to("#cam",{{x:{x_},y:{y_},scale:{S_},duration:{d},ease:"sine.inOut"}},{t:.3f});')
for t, S_, sx, d in CAMK:
    if t > HD and S_ > 1.05: sfx(t, 'zoom_in', -17)
    elif t > HD and S_ <= 1.05: sfx(t, 'zoom_out', -18)
print('camera keys', len(CAMK))
emit_caps()
