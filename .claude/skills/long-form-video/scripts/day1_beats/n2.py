# ================================================================== V2 NEW SCENES ====================================
WB = []; PM = []; BHI = []
BWF = 'grayscale(1) brightness(.55) contrast(1.1)'
def fg_fade(sid, t0, t1, fade=.35):
    A(f'#{sid}', {'opacity': 0}, {'opacity': 1}, t0, fade, 'power2.out'); T(f'#{sid}', {'opacity': 0}, t1 - fade, fade, 'power2.in')
    SET(f'#{sid}', {'opacity': 0, 'display': 'none'}, t1 + .02); SET(f'#{sid}', {'display': 'block'}, t0 - .01)
def bhscene(sid, t0, t1, els, fg, bw=False, fade=.35):
    """presenter stays full screen: elements sit BEHIND the cut-out, text sits in front"""
    SCENES.append((t0, t1, 'bh', sid)); BHI.append((sid, round(t0, 3), round(t1, 3)))
    WB.append(f'<div class="bhs" id="{sid}_w">{els}</div>')
    OV.append(f'<div class="ov bhov" id="{sid}">{fg}</div>')
    PM.append(f'<video class="clip pm{" pmglow" if bw else ""}" id="pm_{sid}" src="assets/matte/{sid}.webm" muted playsinline data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" data-media-start="0" data-track-index="2"></video>')
    A(f'#{sid}_w', {'opacity': 0}, {'opacity': 1}, t0, fade, 'power2.out'); T(f'#{sid}_w', {'opacity': 0}, t1 - fade, fade, 'power2.in')
    SET(f'#{sid}_w', {'opacity': 0, 'display': 'none'}, t1 + .02); SET(f'#{sid}_w', {'display': 'block'}, t0 - .01)
    fg_fade(sid, t0, t1, fade)
    if bw:
        T('#base', {'filter': BWF}, t0, .45, 'power2.out'); T('#base', {'filter': 'grayscale(0) brightness(1) contrast(1)'}, t1 - .45, .45, 'power2.in')

def card_html(i, n, x, y, rot, col='#f4f1ea'):
    return (f'<div class="abs" id="{{p}}cal{i}" style="left:{x}px;top:{y}px;width:280px;height:330px;border-radius:22px;background:{col};border:3px solid #cfc9bb;'
            f'box-shadow:0 18px 40px rgba(0,0,0,.45);transform:rotate({rot}deg)"><div style="height:76px;background:{RED};border-radius:19px 19px 0 0"></div>'
            f'<div style="font-size:110px;font-weight:800;color:#222;text-align:center;line-height:1.4">{n}</div></div>')

# ---------------------------------------------------------------- HOOK (cold open climax clip) ----------------------------
SCENES.append((0, HD, 'hook', 's_hook'))
hk = ''
for i in range(5):
    hk += card_html(i, [1, 2, 3, 4, 4][i], 1440 + i * 28, 70 + i * 20, -6 + i * 3).replace('{p}', 'hk')
hk += (f'<div class="abs" id="hkmc" style="left:1360px;top:70px;width:420px;height:300px;border-radius:18px;background:#fff;box-shadow:0 20px 50px rgba(0,0,0,.5);transform:rotate(-7deg)">'
       f'<div style="margin:26px 30px;font-weight:800;font-size:30px;color:#333">SIJIL CUTI SAKIT</div><div style="margin:0 30px;height:14px;background:#ddd;border-radius:7px"></div>'
       f'<div style="margin:14px 30px;height:14px;width:60%;background:#ddd;border-radius:7px"></div><div style="margin:14px 30px;height:14px;width:75%;background:#ddd;border-radius:7px"></div></div>'
       f'<div class="abs" id="hkx1" style="left:1340px;top:150px;width:460px;height:14px;background:{RED};transform:rotate(-24deg);transform-origin:0 50%;box-shadow:0 0 30px {RED}"></div>'
       f'<div class="abs" id="hkx2" style="left:1340px;top:80px;width:460px;height:14px;background:{RED};transform:rotate(24deg);transform-origin:0 50%;box-shadow:0 0 30px {RED}"></div>'
       f'<svg class="abs" id="hksw" style="left:1450px;top:70px" width="300" height="300" viewBox="0 0 300 300"><circle cx="150" cy="150" r="120" fill="rgba(15,18,36,.7)" stroke="rgba(255,255,255,.3)" stroke-width="18"/>'
       f'<circle id="hkarc" cx="150" cy="150" r="120" fill="none" stroke="{Y}" stroke-width="18" stroke-linecap="round" stroke-dasharray="754" stroke-dashoffset="754" transform="rotate(-90 150 150)" style="filter:drop-shadow(0 0 14px {Y})"/>'
       f'<line id="hkhand" x1="150" y1="150" x2="150" y2="70" stroke="#fff" stroke-width="10" stroke-linecap="round" style="transform-origin:150px 150px"/><rect x="130" y="14" width="40" height="22" rx="6" fill="#fff"/></svg>'
       f'<div class="abs" id="hkwipe" style="left:-300px;top:0;width:300px;height:1080px;background:{Y};opacity:0;transform:skewX(-14deg)"></div>')
OV.append(f'<div class="ov" id="s_hook" style="background:transparent;display:block;opacity:1">{hk}</div>')
SET('#s_hook', {'display': 'none'}, HD + .05)
# calendar flip (3-4 hari)
for i in range(5):
    A(f'#hkcal{i}', {'opacity': 0, 'rotationX': -80, 'y': -60}, {'opacity': 1, 'rotationX': 0, 'y': 0}, h_sampai - .1 + i * .13, .28, 'back.out(1.6)')
    sfx(h_sampai - .1 + i * .13, 'key', -21)
T('#hkcal0,#hkcal1,#hkcal2,#hkcal3,#hkcal4', {'opacity': 0, 'y': -40}, h_alasan - .5, .25, 'power2.in')
# MC card struck out
A('#hkmc', {'opacity': 0, 'scale': .6, 'rotation': -20}, {'opacity': 1, 'scale': 1, 'rotation': -7}, h_alasan - .2, .3, 'back.out(1.7)')
A('#hkx1', {'opacity': 0, 'scaleX': 0}, {'opacity': 1, 'scaleX': 1}, h_mc, .16, 'power3.out'); A('#hkx2', {'opacity': 0, 'scaleX': 0}, {'opacity': 1, 'scaleX': 1}, h_mc + .12, .16, 'power3.out')
sfx(h_mc, 'stamp', -16); sfx(h_mc + .12, 'stamp', -18)
T('#hkmc,#hkx1,#hkx2', {'opacity': 0, 'y': -40}, h_satu - .05, .22, 'power2.in')
# stopwatch 15-20 minit
A('#hksw', {'opacity': 0, 'scale': .4}, {'opacity': 1, 'scale': 1}, h_satu, .3, 'back.out(1.8)')
A('#hkarc', {'strokeDashoffset': 754}, {'strokeDashoffset': 200}, h_15 - .1, .5, 'power2.out'); A('#hkhand', {'rotation': 0, 'svgOrigin': '150 150'}, {'rotation': 270, 'svgOrigin': '150 150'}, h_15 - .1, .5, 'power2.out')
sfx(h_15 - .35, 'riser', -14); sfx(h_15 - .1, 'boom', -10); sfx(h_15, 'shing', -14)
# whip transition into the main video
A('#hkwipe', {'opacity': 1, 'x': 0}, {'opacity': 1, 'x': 2300, 'duration': .32, 'ease': 'power2.inOut', 'immediateRender': False}, HD - .3, .32)
SET('#hkwipe', {'opacity': 0}, HD + .05)
sfx(HD - .32, 'slide', -13); sfx(HD - .1, 'shutter', -15)
grp('ada yang sampai', [('3–4 HARI', 'r', None)], h_sampai - .15, 1.6, y=800, fs=130, pos='bl')
grp('dengan Claude, dia tak ada alasan', [('TAK ADA', 'y', 'alasan'), ('MC', 'w', 'mc')], h_alasan - .2, 1.3, y=790, fs=130, pos='bc')
grp('satu video siap dalam', [('15–20 MINIT', 'y', '15')], h_satu - .1, .9, y=790, fs=170, pos='bc')

# ---------------------------------------------------------------- COMPARE (stage, real assets) ---------------------------
tc0 = t_seb1 - 1.0; tc1 = t_so_k - .05
b = f'<div class="abs" style="left:0;width:1920px;top:50px;text-align:center"><div class="sm" id="cp_s">cuba tengok dua perbezaan ni</div></div>'
b += f'<div class="abs" id="cp_a" style="left:110px;top:200px;width:830px;height:467px;border-radius:26px;overflow:hidden;border:3px solid rgba(255,255,255,.35);box-shadow:0 40px 90px rgba(0,0,0,.6);transform:perspective(1800px) rotateY(9deg) rotate(-1.5deg)">' + vclip('cpv_a', 'assets/panels/p_gpt.mp4', tc0, tc1 - tc0, 'left:0;top:0;width:830px;height:467px;object-fit:cover') + '</div>'
b += f'<div class="abs" id="cp_b" style="left:980px;top:200px;width:830px;height:467px;border-radius:26px;overflow:hidden;border:3px solid {Y};box-shadow:0 40px 90px rgba(0,0,0,.6),0 0 60px rgba(255,255,0,.35);transform:perspective(1800px) rotateY(-9deg) rotate(1.5deg)">' + vclip('cpv_b', 'assets/panels/p_claude.mp4', tc0, tc1 - tc0, 'left:0;top:0;width:830px;height:467px;object-fit:cover') + '</div>'
VT[0] += 2
b += f'<div class="abs" id="cp_la" style="left:110px;width:830px;top:710px;text-align:center"><span class="pill" style="font-size:44px">CONTOH CHATGPT</span></div><div class="abs" id="cp_lb" style="left:980px;width:830px;top:710px;text-align:center"><span class="pill" style="font-size:44px">CONTOH CLAUDE</span></div>'
b += f'<div class="abs" id="cp_vs" style="left:900px;top:380px;width:120px;height:120px;border-radius:50%;background:{NAVY};border:5px solid {Y};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:46px;color:{Y};box-shadow:0 0 40px {Y}88">VS</div>'
scene('s_cmp', tc0, tc1, 'full', BG_PURPLE, b)
A('#cp_s', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, tc0 + .2, .3)
A('#cp_a,#cp_la', {'opacity': 0, 'x': -140}, {'opacity': 1, 'x': 0}, t_seb1 - .15, .45, 'power3.out'); sfx(t_seb1 - .15, 'slide', -14)
A('#cp_b,#cp_lb', {'opacity': 0, 'x': 140}, {'opacity': 1, 'x': 0}, t_seb2 - .15, .45, 'power3.out'); sfx(t_seb2 - .15, 'slide', -14)
A('#cp_vs', {'opacity': 0, 'scale': .3}, {'opacity': 1, 'scale': 1}, t_seb2 + .1, .35, 'back.out(2.4)'); sfx(t_seb2 + .1, 'boom', -14)

# ---------------------------------------------------------------- USAGE (stage) -----------------------------------------
tu0 = t_kredit - .6; tu1 = t_konsep2 - .2
b = f'<div class="abs" style="left:0;width:1920px;top:40px;text-align:center"><div class="sm" id="u_s">software AI yang buat benda advance</div></div>'
b += f'<div class="abs" style="left:0;width:1920px;top:100px;text-align:center"><div class="bg2" style="font-size:96px"><span class="y" id="u_k" style="display:inline-block">KREDIT</span> <span class="y" id="u_t" style="display:inline-block"><span class="w">·</span> TOKEN</span> <span class="y" id="u_u" style="display:inline-block"><span class="w">·</span> USAGE</span></div></div>'
b += f'<svg class="abs" id="u_g" style="left:620px;top:300px" width="680" height="400" viewBox="0 0 680 400"><path d="M40 360 A300 300 0 0 1 640 360" fill="none" stroke="rgba(255,255,255,.2)" stroke-width="44" stroke-linecap="round"/><path id="u_arc" d="M40 360 A300 300 0 0 1 640 360" fill="none" stroke="{Y}" stroke-width="44" stroke-linecap="round" stroke-dasharray="942" stroke-dashoffset="942" style="filter:drop-shadow(0 0 20px {Y})"/></svg>'
b += f'<div class="abs" id="u_nd" style="left:954px;top:480px;width:12px;height:230px;background:#fff;border-radius:6px;transform-origin:50% 100%;transform:rotate(-90deg)"></div><div class="abs" id="u_pv" style="left:934px;top:690px;width:52px;height:52px;border-radius:50%;background:#fff;box-shadow:0 0 30px #fff"></div>'
b += f'<div class="lab abs" id="u_gl" style="left:620px;width:680px;top:760px;text-align:center;font-size:54px;letter-spacing:6px">USAGE</div>'
b += f'<div class="abs" id="u_adv" style="left:40px;width:560px;top:520px;text-align:center"><div class="num" style="position:relative;font-size:54px">BENDA ADVANCE</div></div>'
b += f'<div class="abs" id="u_need" style="left:1290px;width:560px;top:520px;text-align:center"><div class="bg2 y" style="font-size:50px">KENA ADA USAGE</div></div>'
b += f'<div class="abs" id="u_c1" style="left:240px;top:330px">{{coin}}</div><div class="abs" id="u_c2" style="left:1480px;top:330px">{{coin}}</div>'.replace('{coin}', f'<div style="width:110px;height:110px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff7a0,{Y} 55%,#c9b800);box-shadow:0 0 40px {Y}88;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:50px;color:{NAVY}">$</div>')
b += f'<div class="glass abs" id="u_pa" style="left:200px;top:850px;width:640px;height:170px"></div><div class="glass abs" id="u_pb" style="left:1080px;top:850px;width:640px;height:170px"></div>'
b += f'<div class="num abs" id="u_ta" style="left:200px;width:640px;top:880px;text-align:center;font-size:70px">CLAUDE</div><div class="num abs" id="u_tb" style="left:1080px;width:640px;top:880px;text-align:center;font-size:70px">CHATGPT</div><div class="abs" id="u_eq" style="left:850px;top:830px;width:220px;text-align:center;font-weight:800;font-size:150px;color:{Y};text-shadow:0 0 30px {Y}">=</div>'
b += f'<div class="abs" id="u_100" style="left:0;width:1920px;top:850px;text-align:center"><div class="num" style="position:relative;font-size:150px;line-height:1">100%</div><div class="lab" style="position:relative;font-size:34px;letter-spacing:6px;margin-top:6px">MODE CODE · CODEX</div></div>'
scene('s_us', tu0, tu1, 'full', BG_PURPLE, b)
A('#u_s', {'opacity': 0, 'y': 14}, {'opacity': 1, 'y': 0}, tu0 + .3, .3)
for sel, tt in [('#u_k', t_kredit), ('#u_t', t_token)]:
    A(sel, {'opacity': 0, 'scale': .5, 'y': 20}, {'opacity': 1, 'scale': 1, 'y': 0}, tt - .1, .3, 'back.out(2.2)')
sfx(t_kredit - .1, 'click', -14); sfx(t_token - .1, 'ting', -14)
A('#u_c1', {'opacity': 0, 'y': -150, 'rotation': -90}, {'opacity': 1, 'y': 0, 'rotation': 0}, t_kredit - .1, .5, 'bounce.out'); A('#u_c2', {'opacity': 0, 'y': -150, 'rotation': 90}, {'opacity': 1, 'y': 0, 'rotation': 0}, t_token - .1, .5, 'bounce.out')
A('#u_g,#u_gl,#u_nd,#u_pv', {'opacity': 0}, {'opacity': 1}, t_token + .2, .4)
A('#u_adv', {'opacity': 0, 'y': 20}, {'opacity': 1, 'y': 0}, t_adv - .15, .3)
A('#u_need', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, t_mesti - .1, .3, 'back.out(2.2)'); sfx(t_mesti - .1, 'stamp', -13)
A('#u_u', {'opacity': 0, 'scale': .5, 'y': 20}, {'opacity': 1, 'scale': 1, 'y': 0}, t_usage - .1, .3, 'back.out(2.2)'); sfx(t_usage - .1, 'pop', -14)
A('#u_arc', {'opacity': 0}, {'opacity': 1}, t_mesti - .05, .1); A('#u_arc', {'strokeDashoffset': 942}, {'strokeDashoffset': 400}, t_mesti, .8, 'power2.out'); A('#u_nd', {'rotation': -90}, {'rotation': -8, 'duration': .8, 'ease': 'power2.out', 'immediateRender': False}, t_mesti, .8)
T('#u_adv,#u_need', {'opacity': 0}, t_sama - .45, .25)
A('#u_pa,#u_pb,#u_ta,#u_tb,#u_eq', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, t_sama - .35, .35, 'back.out(2)'); sfx(t_sama - .3, 'stamp', -13)
T('#u_pa,#u_pb,#u_ta,#u_tb,#u_eq', {'opacity': 0}, t_100 - .3, .25)
T('#u_gl', {'opacity': 0}, t_100 - .2, .2)
A('#u_100', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, t_100 - .1, .35, 'back.out(2)')
A('#u_arc', {'strokeDashoffset': 400}, {'strokeDashoffset': 0, 'duration': .7, 'ease': 'power2.out', 'immediateRender': False}, t_100 - .05, .7); T('#u_nd', {'rotation': 82}, t_100 - .05, .7, 'power2.out')
counter('#u_100 .num', t_100 - .05, .7, 100, 12, fmt='{}%'); sfx(t_100 - .05, 'ratchet', -14); sfx(t_100 + .7, 'ting', -12)

# idle life while the speaker explains (needle wobble + floating coins)
_w0 = t_token + .8; _n = max(2, 2 * int((t_mesti - .3 - _w0) / 1.4))
js(f'tl.to("#u_nd",{{rotation:-70,duration:.7,ease:"sine.inOut",yoyo:true,repeat:{_n - 1}}},{_w0:.3f});')
for _c, _s in (('#u_c1', 1), ('#u_c2', -1)):
    js(f'tl.to("{_c}",{{y:{-16 * _s},duration:1.1,ease:"sine.inOut",yoyo:true,repeat:{max(1, int((t_mesti - t_token) / 1.1))}}},{t_token + .7:.3f});')
