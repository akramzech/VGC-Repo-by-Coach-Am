import json,re
S=json.load(open('build/words_cut.json')); tm=json.load(open('build/timemap.json'))['map']
def src(o):
    for s,e,oo in tm:
        if oo<=o<oo+(e-s): return round(s+o-oo,3)
try: ex=json.load(open('build/extras.json'))
except Exception: ex=[]
new=[]
for s in S:
    for w,a,b in s['w']:
        k=re.sub(r'[^a-z]','',w.lower())
        if k in ('aa','aaa','haa','ha','eh','hmm','um','uh','er','erm','ah','okay','ok'):
            sa,sb=src(a+0.01),src(b-0.01)
            if sa is None or sb is None: continue
            new.append((round(sa-0.03,2),round(sb+0.03,2),f'filler {w}'))
print('found',len(new),new)
ex+=new; json.dump(ex,open('build/extras.json','w'))
