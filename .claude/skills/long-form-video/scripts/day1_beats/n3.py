# ---------------------------------------------------------------- PRICE (behind head) ------------------------------------
tp0 = t_package - .3; tp1 = wend('ringgit', t_90) + 1.4
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
