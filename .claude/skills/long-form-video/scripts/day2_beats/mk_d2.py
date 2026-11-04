s=open('scripts/build2_d1.py').read()
i=s.index('# ================================================================== STORY ANCHORS')
head=s[:i]
j=s.index("CSS = '''")
tail=s[j:]
body=open('scripts/body_d2.py').read()
helpers='''
def flash(t, d=.22, a=.85):
    A('#flash', {'opacity': a}, {'opacity': 0}, t, d, 'power2.out')
'''
tail=tail.replace("</div>\n{''.join(OV)}","</div>\n{''.join(OV)}<div id=\"flash\"></div>")
tail=tail.replace("json.dump({'dur': NDUR,","json.dump(BHI, open('build/bh_intervals.json', 'w'))\njson.dump({'dur': NDUR,",1)
tail=tail.replace("#base{will-change:filter}","#base{will-change:filter}\n#flash{position:absolute;left:0;top:0;width:1920px;height:1080px;background:#fff;opacity:0;z-index:180;pointer-events:none}")
open('scripts/build_d2.py','w').write(head+helpers+body+'\n'+tail)
print('ok')
