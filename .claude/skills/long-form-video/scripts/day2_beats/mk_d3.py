import re
s=open('scripts/build2_d1.py').read()
head=s[:s.index('# ================================================================== STORY ANCHORS')]
tail=s[s.index("CSS = '''"):]
body=open('scripts/body_d2.py').read()
def cut(txt,start_marker,end_marker=None):
    a=txt.index(start_marker)
    b=txt.index(end_marker,a+10) if end_marker else len(txt)
    return txt[:a]+txt[b:], txt[a:b]
H='# ======================================================================='
body,_=cut(body,H+' UPGRADE SKILL',H+' BANYAK GILA')
body,_=cut(body,H+' INTRO',H+' GRAPHIC DESIGN')
body,_=cut(body,H+' GRAPHIC DESIGN',H+' NICHE JERSEY')
body,_=cut(body,H+' FACEBOOK FEED',H+' ZAMAN BERUBAH')
body,camera=cut(body,H+' CAMERA')
# camera block uses 'CAMK' etc; keep as-is (it also calls emit_caps)
pre='''
def flash(t, d=.22, a=.85):
    A('#flash', {'opacity': a}, {'opacity': 0}, t, d, 'power2.out')
import json as _j, re as _re
_old = _j.load(open('build/timemap_old.json'))['map']; _new = tm['map']
def M(t, _HD=None):
    _HD = tm['hook_dur'] if _HD is None else _HD
    if t < _HD: return t
    src = None
    for s_, e_, o_ in _old[2:]:
        if o_ <= t < o_ + (e_ - s_): src = s_ + t - o_; break
    if src is None: src = _old[-1][1] if t >= _old[-1][2] else _old[2][0]
    _mn = _new[2:]
    for s_, e_, o_ in _mn:
        if s_ <= src < e_: return o_ + src - s_
    for s_, e_, o_ in _mn:
        if s_ > src: return o_
    return _new[-1][2] + _new[-1][1] - _new[-1][0]

import random as _rr
_scene_orig = scene
def scene(sid, t0, t1, kind, bg, body, fade=.3):
    r = _rr.Random(sid); h = ''; tw = []
    for k in range(12):
        sz = r.choice([18, 26, 40, 70, 110]); x = r.randint(30, 1860); y = r.randint(60, 1000); col = r.choice(['255,255,0', '255,255,255', '176,122,255', '120,160,255'])
        sh = r.choice(['50%', '50%', '8px'])
        h += f'<div class="abs" id="{sid}_o{k}" style="left:{x}px;top:{y}px;width:{sz}px;height:{sz}px;border-radius:{sh};background:rgba({col},{r.choice([.10, .16, .22])});box-shadow:0 0 {sz}px rgba({col},.35);transform:rotate({r.randint(0, 80)}deg)"></div>'
        dur = r.uniform(3.2, 5.5); rep = max(1, int((t1 - t0) / dur)) ; dx = r.randint(-120, 120); dy = r.randint(-110, 110)
        tw.append(f'tl.to("#{sid}_o{k}",{{x:{dx},y:{dy},rotation:{r.randint(-60, 60)},duration:{dur:.2f},ease:"sine.inOut",yoyo:true,repeat:{rep}}},{t0:.3f});')
    h += f'<svg class="abs" id="{sid}_ring" style="left:620px;top:240px" width="680" height="680" viewBox="0 0 680 680" opacity=".16"><circle cx="340" cy="340" r="320" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="6 22"/><circle cx="340" cy="340" r="240" fill="none" stroke="#ffe600" stroke-width="2" stroke-dasharray="30 40"/></svg>'
    tw.append(f'tl.fromTo("#{sid}_ring",{{rotation:0,transformOrigin:"340px 340px"}},{{rotation:120,duration:{max(1, t1 - t0):.2f},ease:"none",immediateRender:false}},{t0:.3f});')
    _scene_orig(sid, t0, t1, kind, bg, h + body, fade)
    for x in tw: JS.append(x)

# user (Day 2 V2 r3): no geometric ambient layer, plain smooth dark gradient like Day 1
scene = _scene_orig

AIS = [('openai', 'CHATGPT'), ('claude', 'CLAUDE'), ('deepseek', 'DEEPSEEK'), ('lovable', 'LOVABLE'), ('manus', 'MANUS')]
'''
remap='''
# ---- remap every statement of the OLD body from the old cut timeline to the new one
def _rj(st):
    m = _re.search(r',(-?\\d+(?:\\.\\d+)?)\\);$', st)
    return st if not m else st[:m.start(1)] + f'{M(float(m.group(1))):.3f}' + st[m.end(1):]
JS[:] = [_rj(x) for x in JS]
SFX[:] = [[round(M(t), 3), k, d_] for t, k, d_ in SFX]
SCENES[:] = [(M(a), M(b), k, i) for a, b, k, i in SCENES]
BHI[:] = [(i, round(M(a), 3), round(M(b), 3)) for i, a, b in BHI]
PM[:] = [f'<video class="clip pm" id="pm_{i}" src="assets/matte/{i}.webm" muted playsinline data-start="{a:.3f}" data-duration="{b - a:.3f}" data-media-start="0" data-track-index="2"></video>' for i, a, b in BHI]
for c in CAPSPEC:
    c['t0'] = M(c['t0']); c['t1'] = M(c['t1']); c['ts'] = [M(x) for x in c['ts']]
'''
new=open('scripts/new_beats.py').read()
open('scripts/build_d3.py','w').write(head+pre+body+remap+new+'\n'+camera+'\n'+tail.replace("</div>\n{''.join(OV)}","</div>\n{''.join(OV)}<div id=\"flash\"></div>").replace("json.dump({'dur': NDUR,","json.dump(BHI, open('build/bh_intervals.json', 'w'))\njson.dump({'dur': NDUR,",1).replace("#base{will-change:filter}","#base{will-change:filter}\n#flash{position:absolute;left:0;top:0;width:1920px;height:1080px;background:#fff;opacity:0;z-index:180;pointer-events:none}"))
print('ok')
