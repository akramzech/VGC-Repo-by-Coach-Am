import re
s = open('scripts/build.py').read()
def R(old, new, count=1):
    global s
    assert old in s, 'MISSING: ' + old[:70]
    s = s.replace(old, new, count)

R("W, H = 1920, 1080\n", "W, H = 1080, 1920\nWW, WH = 1920, 1080\n")
# ---- camera
a = s.index("NF = int(DUR * 30) + 1"); b = s.index("# fast-forward fix")
s = s[:a] + '''NF = int(DUR * 30) + 1
tt_ = np.arange(NF) / 30
hx = np.interp(tt_, [h[0] for h in ht], [h[2] for h in ht]); hy = np.interp(tt_, [h[0] for h in ht], [h[1] for h in ht])
hx = gaussian_filter1d(hx, 26, mode='nearest'); hy = gaussian_filter1d(hy, 30, mode='nearest')
TX, TY, SS = [], [], []
for i in range(NF):
    S_, sx = cam_state(i / 30)
    Zp = 1 + (S_ - 1) * 0.42            # gentler punch-ins: the 1080p source is already enlarged 1.78x for 9:16
    Sc = (H / WH) * Zp; SS.append(Sc)
    f = min(1.0, max(0.0, (sx - 470) / 490.0)); pin_y = (0.27 + 0.13 * f) * H
    TX.append(W / 2 - Sc * hx[i]); TY.append(pin_y - Sc * hy[i])
TX = gaussian_filter1d(np.array(TX), 2.5, mode='nearest'); TY = gaussian_filter1d(np.array(TY), 2.5, mode='nearest')
CAM = []
for i in range(NF):
    S_ = SS[i]; tx = min(0, max(W - S_ * WW, TX[i])); ty = min(0, max(H - S_ * WH, TY[i]))
    CAM.append([round(float(tx), 2), round(float(ty), 2), round(float(S_), 4)])
d2 = np.abs(np.diff(np.array(CAM), 2, axis=0)); print('max 2nd diff tx,ty,S', d2.max(0).round(3))
''' + s[b:]
# ---- captions: single centred lower-third band
R("""POS = {
  'bl': 'left:110px;top:{y}px;text-align:left;', 'bc': 'left:0;width:1920px;top:{y}px;text-align:center;',
  'br': 'right:110px;top:{y}px;text-align:right;', 'tc': 'left:0;width:1920px;top:{y}px;text-align:center;',
  'cl': 'left:110px;top:{y}px;text-align:left;',
}""", """POS = {k: 'left:0;width:1080px;padding:0 44px;top:{y}px;text-align:center;' for k in ('bl', 'bc', 'br', 'tc', 'cl')}""")
R("""    CAPSPEC.append(dict(t0=t0, t1=t1, small=small, big=big, pos=pos, y=y, fs=fs, times=times, hit=hit, sm_t=sm_t, sfx_on=sfx_on, sfx_db=sfx_db))""",
"""    y2 = 230 if pos == 'tc' else (930 if (not big and pos == 'bl') else 1360)
    fs2 = fs if fs < 70 else min(112, round(fs * .8))
    CAPSPEC.append(dict(t0=t0, t1=t1, small=small, big=big, pos='bc', y=y2, fs=fs2, times=times, hit=hit, sm_t=sm_t, sfx_on=sfx_on, sfx_db=sfx_db))""")
# ---- reels (screen space)
R("('assets/panels/n3.mp4', 0, '50% 50%')])\nsfx(A0", "('assets/panels/n3.mp4', 0, '50% 50%')], y=430, w=400, h=711, gap=30, x0=785, x1=85)\nsfx(A0")
R("rot=-15, x0=700, x1=-560, ease='power1.inOut')", "rot=-15, y=430, w=400, h=711, gap=30, x0=785, x1=-115, ease='power1.inOut')")
# ---- weekly card behind me
R("left:{40 + i * 70}px", "left:{28 + i * 56}px")
R("left:1270px;top:210px;width:560px;height:470px", "left:610px;top:300px;width:440px;height:380px")
# ---- prompt cards
R('id="cv" class="pn card3d" style="left:20px;top:210px;width:520px;height:400px', 'id="cv" class="pn card3d" style="left:30px;top:330px;width:420px;height:340px')
R('id="cp" class="pn card3d" style="left:1330px;top:180px;width:520px;height:400px', 'id="cp" class="pn card3d" style="left:630px;top:640px;width:420px;height:340px')
R("PMAT_WIN.append((tt - .4, C1 + .1))", "PMAT_WIN.append((tv - .45, C1 + .1))")
# ---- stage (3 sizes) stacked
R("def stcol(sid, cx, w, h, ry, label, sub, bgpos, bgsize, t_in):\n    L, Tp = cx - w / 2, BASEY - h", "def stcol(sid, cx, w, h, ry, label, sub, bgpos, bgsize, t_in, by=830):\n    L, Tp = cx - w / 2, by - h")
R("top:{BASEY + 44}px;z-index:34;opacity:0\"><span>", "top:{by + 26}px;z-index:34;opacity:0\"><span>")
R("stcol('sz2', 1501, 540, 304, -14, '16:9', 'YOUTUBE', (0, 0), (600, 338), t169)", "stcol('sz2', 540, 800, 450, -5, '16:9', 'YOUTUBE', (0, 0), (600, 338), t169, by=790)")
R("stcol('sz1', 301, 304, 540, 14, '9:16', 'REELS · TIKTOK', (-387, 0), (1067, 600), t916)", "stcol('sz1', 830.5, 281, 500, 8, '9:16', 'REELS · TIKTOK', (-387, 0), (1067, 600), t916, by=1440)")
R("stcol('sz3', 842, 480, 480, 0, '1:1', 'FEED', (-230, 0), (960, 540), t11)", "stcol('sz3', 360, 500, 500, -6, '1:1', 'FEED', (-230, 0), (960, 540), t11, by=1440)")
# ---- split card -> bottom half
R("""f'<div id="splitov" style="position:absolute;left:960px;top:0;width:960px;height:1080px;z-index:30;opacity:0;background:#0b0e1c">{split}</div>'""", """f'<div id="splitov" style="position:absolute;left:0;top:1010px;width:1080px;height:910px;z-index:30;opacity:0;background:#0b0e1c">{split}</div>'""")
R("tl_fromto('#splitov', {'opacity': 0, 'x': 160, 'filter': 'blur(10px)'}, {'opacity': 1, 'x': 0, 'filter': 'blur(0px)'}", "tl_fromto('#splitov', {'opacity': 0, 'y': 220, 'filter': 'blur(10px)'}, {'opacity': 1, 'y': 0, 'filter': 'blur(0px)'}")
R("tl_to('#splitov', {'opacity': 0, 'x': 120, 'filter': 'blur(10px)'}", "tl_to('#splitov', {'opacity': 0, 'y': 160, 'filter': 'blur(10px)'}")
# ---- ring / weekly / recap geometry in markup
R("left:{140 + i * 240}px", "left:{60 + i * 137}px")
R("""<div class="itl" style="top:50px">""", """<div class="itl" style="top:250px">""")
# ---- counters + chips
R('class="num" style="left:0;width:1920px;top:760px;opacity:0"', 'class="num" style="left:0;width:1080px;top:1090px;opacity:0"')
R('class="num" style="left:0;width:1920px;top:690px;opacity:0"', 'class="num" style="left:0;width:1080px;top:1040px;opacity:0"')
R('style="position:absolute;left:0;width:1920px;top:800px;text-align:center;z-index:60"', 'style="position:absolute;left:0;width:1080px;top:1580px;text-align:center;z-index:60"')
# ---- CSS (full 9:16 version)
a = s.index("CSS = f'''"); b = s.index("'''\nNDUR")
CSS916 = r"""CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000;font-family:Poppins,sans-serif}}
#root{{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden;background:#000}}
#cam,#cam2{{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0;will-change:transform}}
#cam{{z-index:1}} #cam2{{z-index:3}}
#base,#pmat{{position:absolute;left:0;top:0;width:1920px;height:1080px}}
#pmat{{opacity:0}} #wback{{position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:2}}
.pn{{position:absolute;border-radius:26px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.55);background:#000;opacity:0}}
.pn video.pv{{width:100%;height:100%;object-fit:cover;display:block;position:absolute;left:0;top:0}}
.reel{{position:absolute;opacity:0}} .rp{{position:absolute;border-radius:24px;overflow:hidden;background:#000;box-shadow:0 30px 70px rgba(0,0,0,.55)}} .rp video.pv{{width:100%;height:100%;object-fit:cover;display:block;position:absolute;left:0;top:0}}
.card3d{{background:linear-gradient(160deg,#1a2050,#0f1224);border:2px solid rgba(255,255,255,.25);box-shadow:0 30px 70px rgba(0,0,0,.6);padding:28px 30px}}
.ct{{font-weight:800;font-size:40px;color:{LIME};letter-spacing:-1px}}
.ci{{font-size:56px;color:#fff;margin-bottom:8px}}
.cs{{margin-top:14px;font-weight:600;font-size:26px;color:#dfe3ff;line-height:1.35}}
.ch{{display:inline-block;opacity:0}}
.wb{{position:absolute;bottom:80px;width:44px;height:200px;border-radius:12px;background:#2a3060;overflow:hidden}}
.wb i{{position:absolute;left:0;bottom:0;width:100%;height:100%;background:{LIME};transform-origin:50% 100%;transform:scaleY(0)}}
.wb b{{position:absolute;bottom:-34px;left:-8px;width:60px;text-align:center;font-size:15px;color:#fff;font-weight:600}}
.cn{{position:absolute;right:24px;top:28px;font-weight:800;font-size:44px;color:#fff;opacity:0;text-shadow:0 0 22px rgba(255,255,255,.5)}}
.cap{{position:absolute;z-index:100;opacity:0;font-family:Poppins,sans-serif}}
.sm{{font-weight:500;color:#fff;font-size:.42em;line-height:1.15;text-shadow:.06em 0 0 #0b0b0d,-.06em 0 0 #0b0b0d,0 .06em 0 #0b0b0d,0 -.06em 0 #0b0b0d,.045em .045em 0 #0b0b0d,-.045em .045em 0 #0b0b0d,.045em -.045em 0 #0b0b0d,-.045em -.045em 0 #0b0b0d,0 .1em .22em rgba(0,0,0,.6);margin-bottom:.04em;text-transform:none}}
.bg2{{font-weight:800;line-height:1.02;text-transform:uppercase;letter-spacing:-.01em;text-shadow:.035em 0 0 #0b0b0d,-.035em 0 0 #0b0b0d,0 .035em 0 #0b0b0d,0 -.035em 0 #0b0b0d,.025em .025em 0 #0b0b0d,-.025em .025em 0 #0b0b0d,.025em -.025em 0 #0b0b0d,-.025em -.025em 0 #0b0b0d,0 .07em 0 #0b0b0d,0 .1em .22em rgba(0,0,0,.65)}}
.bw{{display:inline-block;transform-origin:50% 70%}}
.ov{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;overflow:hidden}}
.itl{{position:absolute;left:0;width:1080px;top:300px;text-align:center;font-weight:800;font-size:84px;color:#fff;letter-spacing:-2px}}
.ring{{position:absolute;left:270px;top:560px}}
.rgl{{position:absolute;left:0;width:1080px;top:1150px;text-align:center;font-weight:600;font-size:34px;color:#aab3d6;letter-spacing:2px;opacity:0}}
.wcol{{position:absolute;top:470px;width:137px;height:700px}}
.wbar{{position:absolute;left:18px;top:0;width:101px;height:560px;border-radius:24px;background:#2a3060;overflow:hidden}}
.wbar i{{position:absolute;left:0;bottom:0;width:100%;height:100%;background:{LIME};transform-origin:50% 100%;transform:scaleY(0)}}
.wcol b{{position:absolute;left:0;width:137px;top:590px;text-align:center;font-size:19px;color:#fff;font-weight:700;letter-spacing:1px}}
.lock{{position:absolute;left:0;width:1080px;top:1200px;text-align:center;font-weight:800;font-size:52px;color:{LIME};opacity:0}}
.rtl{{position:absolute;left:0;width:1080px;top:330px;text-align:center;font-weight:800;font-size:118px;color:#fff;letter-spacing:-3px}}
.rc1,.rc2{{position:absolute;left:140px;width:800px;height:300px;border-radius:30px;background:#141833;border:2px solid rgba(255,255,255,.22);text-align:center;opacity:0}}
.rc1{{top:700px}} .rc2{{top:1060px}}
.rc1 b,.rc2 b{{display:block;margin-top:34px;font-size:54px;font-weight:800}} .rc1 span,.rc2 span{{display:block;margin-top:14px;font-size:112px;font-weight:800;color:#fff}}
.spc{{position:absolute;left:90px;top:40px;width:900px;height:800px;border-radius:30px;background:#141833;border:2px solid rgba(255,255,255,.22);text-align:center}}
.spl{{position:absolute;left:0;width:100%;font-weight:800;font-size:52px;opacity:0}} #spa{{top:30px}} #spe{{top:670px}}
.spn{{position:absolute;left:0;width:100%;font-weight:800;font-size:130px;color:#fff;text-shadow:0 0 28px rgba(255,255,255,.55);opacity:0}} #spb{{top:110px}} #spd{{top:400px;font-size:120px}}
.spar{{position:absolute;left:0;width:100%;top:290px;font-size:70px;color:{LIME};font-weight:800;opacity:0}}
.sbh{{position:absolute;left:0;width:1080px;top:110px;text-align:center}}
.sbh .sm{{font-size:34px;opacity:0}} .sbh .bg2{{font-size:78px;margin-top:6px;opacity:0}}
.stp{{position:absolute;border-radius:26px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.55);border:2px solid rgba(255,255,255,.18);background:#000}}
.stp video.sv{{position:absolute;object-fit:cover;max-width:none}}
.stl{{position:absolute;width:280px;text-align:center}}
.stl span{{display:inline-block;background:{LIME};color:#0d1020;font-weight:800;font-size:34px;padding:2px 26px 4px;border-radius:999px}}
.stl em{{display:block;margin-top:10px;font-style:normal;font-weight:600;font-size:26px;color:#aab3d6;letter-spacing:2px}}
.lj{{position:absolute;left:0;width:1080px;top:1620px;text-align:center;font-weight:800;font-size:40px;color:{LIME};letter-spacing:4px}}
.num{{position:absolute;z-index:90;text-align:center;font-weight:800;font-size:150px;color:#fff;letter-spacing:-4px;text-shadow:0 0 30px rgba(255,255,255,.6),0 7px 0 rgba(0,0,0,.5)}}
.num small{{display:block;font-size:36px;color:{LIME};letter-spacing:6px;margin-bottom:-24px;text-shadow:0 4px 0 rgba(0,0,0,.6)}}
.chip{{display:inline-block;margin:0 8px;background:{LIME};color:#0d1020;font-weight:800;font-size:40px;padding:6px 28px 10px;border-radius:999px;opacity:0}} .chip i{{font-style:normal}}
"""
s = s[:a] + CSS916 + s[b:]
# ---- HTML template
R('data-resolution="landscape"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">', 'data-resolution="portrait"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">')
R('data-duration="{NDUR}" data-width="1920" data-height="1080">', 'data-duration="{NDUR}" data-width="1080" data-height="1920">')
R('''<div id="cam">
<video id="base" class="clip" src="assets/main.mp4" muted playsinline data-start="0" data-duration="{NDUR}" data-media-start="{SH}" data-track-index="1"></video>
<div id="wback">{''.join(HTML_WORLD)}</div>
<video id="pmat" class="clip" src="assets/person.webm" muted playsinline data-start="0" data-duration="{NDUR}" data-media-start="{SH}" data-track-index="2"></video>
</div>''', '''<div id="cam"><video id="base" class="clip" src="assets/main.mp4" muted playsinline data-start="0" data-duration="{NDUR}" data-media-start="{SH}" data-track-index="1"></video></div>
<div id="wback">{''.join(HTML_WORLD)}</div>
<div id="cam2"><video id="pmat" class="clip" src="assets/person.webm" muted playsinline data-start="0" data-duration="{NDUR}" data-media-start="{SH}" data-track-index="2"></video></div>''')
R("gsap.set('#cam',{{transformOrigin:'0 0'", "gsap.set('#cam,#cam2',{{transformOrigin:'0 0'")
R("tl.fromTo('#cam',{{x:a[0]", "tl.fromTo('#cam,#cam2',{{x:a[0]")
R("open('hf/index.html', 'w')", "open('hf916/index.html', 'w')")
R("open('build/sfx_events.json', 'w')", "open('build/sfx_events_916.json', 'w')")
open('scripts/build916.py', 'w').write(s)
print('ok')
