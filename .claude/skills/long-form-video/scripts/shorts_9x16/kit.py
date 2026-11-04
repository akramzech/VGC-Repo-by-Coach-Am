"""Shared kit for 9:16 shorts (Long-Form Video style).  Each short: `from kit import *`, call beats, then assemble('SX')."""
import json, sys, os
W, H = 1080, 1920
Y = '#FFFF00'; GRN = '#3fd98a'; RED = '#FF4D4D'
JS = []; SFX = []; INIT = []; SCN = []; CAPS = []
# TikTok safe area: content between y 260 and ~1500 (orig 90..1800 mapped), x 148..932; presenter captions at y 1150, context pill at y 196
SAFE_S = .725; SAFE_TX = (1080 - 1080 * SAFE_S) / 2; SAFE_TY = 260 - 90 * SAFE_S
DUR = None
def init(name):
    global DUR, WD
    WD = name; os.chdir(name)
    DUR = round(json.load(open('timemap.json'))['dur'] + 0.35, 3)
    return DUR
def js(s): JS.append(s)
def sfx(t, kind, db=-14): SFX.append([round(float(t), 3), kind, db])
def fj(d): return json.dumps(d, separators=(',', ':'))
def A(sel, f, to, t, d=.4, ease='power3.out'):
    if 'opacity' in f and f['opacity'] == 0: INIT.append(f'gsap.set("{sel}",{fj(f)});')
    js(f'tl.fromTo("{sel}",{fj(f)},{fj({**to, "duration": d, "ease": ease, "immediateRender": False})},{t:.3f});')
def T(sel, to, t, d=.4, ease='power2.out'): js(f'tl.to("{sel}",{fj({**to, "duration": d, "ease": ease})},{t:.3f});')
def txt(i, x, y, w, t, cls='num', fs=60, align='center', extra=''):
    return f'<div class="{cls}" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;font-size:{fs}px;text-align:{align};{extra}">{t}</div>'
def big(i, y, html, fs=130, extra=''):
    return f'<div class="abs bg2" id="{i}" style="left:0;width:{W}px;top:{y}px;text-align:center;font-size:{fs}px;{extra}">{html}</div>'
def head(prefix, small, bigtxt, t, fs=130, y=150, cls='y'):
    """standard stage title (small white line + big word) + its entrance"""
    h = txt(f'{prefix}_s', 0, 90, W, small, 'sm', 50, extra='position:absolute') + big(f'{prefix}_b', y, bigtxt if '<' in bigtxt else f'<span class="{cls}">{bigtxt}</span>', fs)
    return h
def head_anim(prefix, t, sound=True):
    A(f'#{prefix}_s', {'opacity': 0}, {'opacity': 1}, t, .25)
    A(f'#{prefix}_b', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1}, t + .05, .3, 'back.out(2)')
    if sound: sfx(t + .05, 'stamp', -11)
def logo(i, kind, x, y, s=200, rot=0):
    if kind == 'openai': inner = f'<img src="assets/img/openai.svg" style="width:{s * .62:.0f}px;height:{s * .62:.0f}px">'
    else: inner = f'<img src="assets/img/{kind}.png" style="width:100%;height:100%;object-fit:cover">'
    return (f'<div class="abs" id="{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:{s * .22:.0f}px;background:#fff;box-shadow:0 24px 60px rgba(0,0,0,.55),0 0 0 3px rgba(255,255,255,.35);'
            f'display:flex;align-items:center;justify-content:center;overflow:hidden;transform:rotate({rot}deg)">{inner}</div>')
def person(i, x, y, s, col):
    return (f'<svg class="abs" id="{i}" style="left:{x}px;top:{y}px" width="{60 * s:.0f}" height="{110 * s:.0f}" viewBox="0 0 60 110">'
            f'<circle cx="30" cy="22" r="16" fill="{col}"/><path d="M6 108 C6 62 16 46 30 46 C44 46 54 62 54 108 Z" fill="{col}"/></svg>')
def chip(i, x, y, w, h, t, fs=42, col=Y):
    return f'<div class="chip abs" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;font-size:{fs}px;background:rgba(15,18,36,.92);border-color:{col};color:{col};z-index:7;box-shadow:0 0 40px {col}44">{t}</div>'

BG_PURPLE = 'radial-gradient(ellipse at 50% 38%,#4B1D96 0%,#2b1166 48%,#140a33 100%)'
BG_NAVY = 'radial-gradient(ellipse at 50% 40%,#1d2250 0%,#0F1224 70%)'
def scene(sid, t0, t1, bg, body, fade=.25, hold=False):
    SCN.append(f'<div class="ov" id="{sid}" style="background:{bg}"><div style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-origin:0 0;transform:translate({SAFE_TX:.1f}px,{SAFE_TY:.1f}px) scale({SAFE_S})">{body}</div></div>')
    INIT.append(f'gsap.set("#{sid}",{{opacity:0,display:"none"}});')
    js(f'tl.set("#{sid}",{{display:"block"}},{t0:.3f});')
    js(f'tl.fromTo("#{sid}",{{opacity:0}},{{opacity:1,duration:{fade},ease:"power1.out",immediateRender:false}},{t0:.3f});')
    if not hold:
        js(f'tl.to("#{sid}",{{opacity:0,duration:{fade},ease:"power1.in"}},{t1 - fade:.3f});')
        js(f'tl.set("#{sid}",{{display:"none"}},{t1:.3f});')
def cap(i, t0, t1, small, bigtxt=None, bt=None, cls='y', size=112):
    body = f'<div class="sm" style="font-size:46px">{small}</div>' if small else ''
    if bigtxt: body += f'<div class="bg2 {cls}" id="{i}b" style="font-size:{size}px;margin-top:6px">{bigtxt}</div>'
    CAPS.append(f'<div class="cap" id="{i}" style="left:0;top:1150px;width:{W}px;text-align:center">{body}</div>')
    INIT.append(f'gsap.set("#{i}",{{opacity:0}});')
    A(f'#{i}', {'opacity': 0, 'y': 18}, {'opacity': 1, 'y': 0}, t0, .22)
    if bigtxt and bt: A(f'#{i}b', {'opacity': 0, 'scale': .7}, {'opacity': 1, 'scale': 1}, bt, .22, 'back.out(1.8)')
    T(f'#{i}', {'opacity': 0}, t1 - .12, .12)
from contextlib import contextmanager
import re as _re
@contextmanager
def shifted(off):
    """everything authored inside the block uses its own (old) clock; shift it by `off` seconds"""
    j0, s0 = len(JS), len(SFX)
    yield
    for i in range(j0, len(JS)):
        m = _re.search(r',(-?\d+(?:\.\d+)?)\);$', JS[i])
        if m: JS[i] = JS[i][:m.start(1)] + f'{float(m.group(1)) + off:.3f}' + JS[i][m.end(1):]
    for i in range(s0, len(SFX)): SFX[i][0] = round(SFX[i][0] + off, 3)
def tag(i, t0, t1, text):
    """context pill at the top: tells the viewer what this clip is about in the first seconds"""
    CAPS.append(f'<div class="cap" id="{i}" style="left:0;top:196px;width:{W}px;text-align:center;z-index:120"><span style="display:inline-block;padding:9px 26px;border-radius:40px;background:rgba(15,18,36,.88);border:2px solid rgba(255,255,0,.75);color:#FFFF00;font:800 30px Poppins;letter-spacing:.04em">{text}</span></div>')
    INIT.append(f'gsap.set("#{i}",{{opacity:0}});')
    A(f'#{i}', {'opacity': 0, 'y': -20}, {'opacity': 1, 'y': 0}, t0, .3)
    T(f'#{i}', {'opacity': 0}, t1 - .25, .25)
def crowd(prefix, x0, y0, cols, rows, dx, dy, s, lit=(), col='#8a90b8', litcol=Y):
    h = ''
    for r in range(rows):
        for c in range(cols):
            on = (r, c) in lit
            h += person(f'{prefix}_{r}_{c}', x0 + c * dx, y0 + r * dy, s, litcol if on else col)
    return h

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
.r{color:#FF4D4D;font-weight:800;text-shadow:0 0 .05em rgba(255,77,77,.95),0 0 .2em rgba(255,77,77,.6),0 0 .45em rgba(255,77,77,.35),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}
.w{color:#fff;font-weight:600;text-shadow:0 0 .06em rgba(255,255,255,.9),0 0 .2em rgba(255,255,255,.5),0 0 .45em rgba(255,255,255,.28),0 .05em .07em rgba(0,0,0,.85),0 .1em .22em rgba(0,0,0,.7),0 .2em .55em rgba(0,0,0,.5)}
.num{position:absolute;font-weight:800;color:#fff;letter-spacing:-.02em}
.lab{position:absolute;font-weight:800;color:#FFFF00;text-transform:uppercase;text-shadow:0 0 .2em rgba(255,255,0,.6)}
.chip{position:absolute;border-radius:22px;background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.28);color:#fff;font-weight:800;display:flex;align-items:center;padding:0 34px}
.glass{position:absolute;border-radius:28px;background:linear-gradient(160deg,rgba(255,255,255,.14),rgba(255,255,255,.04));border:2px solid rgba(255,255,255,.25);box-shadow:0 30px 80px rgba(0,0,0,.5),inset 0 0 40px rgba(255,255,255,.05)}
'''
def assemble():
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
