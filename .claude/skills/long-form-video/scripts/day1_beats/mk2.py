import re
P="scripts/build.py"  # the V1 header this was assembled from (not shipped; build_engine.py is the result)
v1=open(P).read()
def between(a,b):
    i=v1.index(a); j=v1.index(b); return v1[i:j]
head=v1[:v1.index('# ================================================================== STORY ANCHORS')]
head=head.replace("if inside and inside[0][2] == 'full': continue","if inside and inside[0][2] in ('full', 'bh'): continue")
head=head.replace("if s[2] == 'full' and c['t0'] < s[0] < c['t1']","if s[2] in ('full', 'bh') and c['t0'] < s[0] < c['t1']")
head=head.replace("if s[2] == 'full' and c['t0'] < s[1] <= c['ts'][0] + .3","if s[2] in ('full', 'bh') and c['t0'] < s[1] <= c['ts'][0] + .3")
head=head.replace("""f'<span class="bw {"y" if col == "y" else "w"}" id""","""f'<span class="bw {col if col in ("y", "r") else "w"}" id""")
assert "col in (" in head
MIDFIX=1
mid=between('# ================================================================== SCENE 3: battery hero','# ================================================================== SCENE 7: price')
mid=mid.replace("A('#f_hand', {'rotation': 0}, {'rotation': 360 * 2}, sweep_t0, sweep_d, 'none')","A('#f_hand', {'rotation': 0, 'svgOrigin': '260 260'}, {'rotation': 360 * 2, 'svgOrigin': '260 260'}, sweep_t0, sweep_d, 'none')")
assert "svgOrigin" in mid
mid=mid.replace('id="m_stamp" style="left:1020px;width:760px;top:400px;opacity:0"','id="m_stamp" style="left:1020px;width:760px;top:470px;opacity:0"')
css=v1[v1.index("CSS = '''"):v1.index("NDUR = DUR")]
css=css.replace("'''\n","""
.bhs{position:absolute;left:0;top:0;width:1920px;height:1080px;display:none}
.bhov{background:transparent}
.pm{position:absolute;left:0;top:0;width:1920px;height:1080px}
.pmglow{filter:drop-shadow(0 0 3px rgba(255,255,255,.9)) drop-shadow(0 0 22px rgba(255,255,255,.55))}
.coin{border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff7a0,#FFFF00 55%,#c9b800);box-shadow:0 0 40px #FFFF0088;display:flex;align-items:center;justify-content:center;font-weight:800;color:#0F1224}
.wallrow{position:absolute}
.pill{display:inline-block;background:#FFFF00;color:#0F1224;font-weight:800;border-radius:999px;padding:2px 26px 4px}
'''
""",1) if False else css
css=css.rstrip()
assert css.endswith("'''")
css=css[:-3]+""".bhs{position:absolute;left:0;top:0;width:1920px;height:1080px;display:none}
.bhov{background:transparent}
.pm{position:absolute;left:0;top:0;width:1920px;height:1080px}
.pmglow{filter:drop-shadow(0 0 3px rgba(255,255,255,.9)) drop-shadow(0 0 22px rgba(255,255,255,.55))}
.coin{border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff7a0,#FFFF00 55%,#c9b800);box-shadow:0 0 40px #FFFF0088;display:flex;align-items:center;justify-content:center;font-weight:800;color:#0F1224}
.wallrow{position:absolute}
.pill{display:inline-block;background:#FFFF00;color:#0F1224;font-weight:800;border-radius:999px;padding:2px 26px 4px}
#base{will-change:filter}
'''
"""
tail_html='''
NDUR = DUR
js_all = '\\n'.join(INIT + JS)
html = f\'\'\'<!doctype html>
<html lang="ms" data-resolution="landscape"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{NDUR}" data-width="1920" data-height="1080">
<div id="cam"><video id="base" class="clip" src="assets/main.mp4" muted playsinline data-start="0" data-duration="{NDUR}" data-media-start="0" data-track-index="1"></video>
<div id="wback">{''.join(WB)}</div>{''.join(PM)}</div>
{''.join(OV)}
{''.join(CAPS)}
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{NDUR}" data-track-index="50" data-volume="1"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{paused:true}});
{js_all}
window.__timelines["main"] = tl;
</script></body></html>\'\'\'
for _id in ['hkcal%d' % i for i in range(5)] + ['rccal%d' % i for i in range(5)] + ['u_adv', 'u_100', 'pr_s', 'ad_t0', 'ad_t1', 'ad_t2', 'ou_d4']:
    html = html.replace('id="%s"' % _id, 'id="%s" data-layout-allow-overlap' % _id)
open('hf/index.html', 'w').write(html)
json.dump({'dur': NDUR, 'sfx': sorted(SFX), 'scenes': [[round(a, 2), round(b, 2), k, i] for a, b, k, i in SCENES]}, open('build/sfx_events.json', 'w'))
json.dump(BHI, open('build/bh_intervals.json', 'w'))
print('html', len(html), 'sfx events', len(SFX), 'dur', NDUR)
for a, b, k, i in sorted(SCENES): print(f'  {i:8s} {k:5s} {a:7.2f} - {b:7.2f}')
'''
a2=open('a2.py').read(); n2=open('n2.py').read(); n3=open('n3.py').read(); t2=open('t2.py').read()
n3=n3.replace("""    els += f'<div class="abs wallrow" id="wr{r}" style="left:{-60 - r * 90}px;top:{r * 214 + 40}px;width:2816px;height:199px">' + vclip(""","""    VT[0] += 1
    els += f'<div class="abs wallrow" id="wr{r}" style="left:{-60 - r * 90}px;top:{r * 214 + 40}px;width:2816px;height:199px">' + vclip(""")
def alias(t):
    for a,b in [("wt('5',","wt('5|lima',"),("wt('100',","wt('100|seratus',"),("wt('3',","wt('3|tiga',"),("wt('15',","wt('15|lima belas',"),("wt('20',","wt('20|dua puluh',"),("wt('90',","wt('90|sembilan',"),("wt('1',","wt('1|satu',"),("wt('9',","wt('9|sembilan',"),("wt('16',","wt('16|enam belas',"),("wt('2',","wt('2|dua',")]:
        t=t.replace(a,b)
    return t
a2=alias(a2); n2=alias(n2); n3=alias(n3); mid=alias(mid); t2=alias(t2)
for a,b in [("t_20 = wt('20|dua puluh', t_package)","t_20 = wt('rm20|20|dua puluh', t_package)"),
            ("t_usd = wt('usd', t_20)","t_usd = t_20 + .6"),
            ("t_90 = wt('90|sembilan', t_usd)","t_90 = wt('rm90|90', t_20 + .3)"),
            ("t_ringgit = wt('ringgit', t_90)","t_ringgit = wt('rm100|100', t_90)"),
            ("t_team = wt('team', t_dulu)","t_team = wt('team|tim', t_dulu)")]:
    assert a in a2, a
    a2=a2.replace(a,b)
n3=n3.replace("wend('ringgit', t_90)","wend('rm100|100', t_90)")
a2=a2.replace("'episode'","'episod'"); t2=t2.replace("'episode'","'episod'")
out=head+a2+"\n"+n2+"\n"+mid+"\n"+n3+"\n"+t2+"\n"+css+tail_html
open('build2.py','w').write(out)
print('build2.py',len(out.splitlines()),'lines')
