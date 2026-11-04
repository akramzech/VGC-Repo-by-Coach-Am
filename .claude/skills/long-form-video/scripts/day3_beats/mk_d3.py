import os,re
E=open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'build_engine.py')).read()
head=E[:E.index('# ================================================================== STORY ANCHORS (V2)')]
mid=E[E.index('def vclip'):E.index('def card_html')]
tail=E[E.index('# ================================================================== CAMERA'):]
tail=tail.replace("CAMK = [(h_hari - .4, 1.2, 960, .5), (h_mc - .45, 1.3, 960, .5), (h_15 - .5, 1.42, 960, .5), (HD - .5, 1.0, 960, .45)]","CAMK = [(0.2, 1.2, 960, 3.2), (4.2, 1.36, 960, 2.4), (HD - .55, 1.0, 960, .5)]")
tail=tail.replace("cyc = [1.16, 1.0, 1.28, 1.1, 1.22, 1.0]","cyc = [1.14, 1.0, 1.22, 1.08, 1.18, 1.0]")
tail=re.sub(r"for _id in \[.*?\]:\n    html = html\.replace\(.*?\)\n","",tail,flags=re.S)
open('scripts/build_d3.py','w').write(head+"\n"+mid+"\n"+open('scripts/body_d3.py').read()+"\n"+tail); print('assembled')
