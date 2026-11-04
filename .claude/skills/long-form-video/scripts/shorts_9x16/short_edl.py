import json,sys,numpy as np
# usage: short_edl.py out.json  "a:b" "c:d" ...   (FINAL-video times of first/last word of each segment, in the order wanted)
out=sys.argv[1]; spans=[tuple(map(float,x.split(':'))) for x in sys.argv[2:]]
tm=json.load(open('build/timemap.json'))['map'][2:]
env=np.load('build/env.npy'); es=np.convolve(env,np.ones(5)/5,'same'); SIL=-34
def src(f):
    for s,e,o in tm:
        if o<=f<o+(e-s): return s+f-o
    return tm[-1][1]
def runs(lo,hi):
    i0,i1=int(lo*100),int(hi*100); m=es[i0:i1]<SIL; r=[];j=0
    while j<len(m):
        if m[j]:
            k=j
            while k<len(m) and m[k]: k+=1
            r.append(((i0+j)/100,(i0+k)/100)); j=k
        else: j+=1
    return r
segs=[]
for a,b in spans:
    sa,sb=src(a),src(b)
    r=[x for x in runs(sa-.45,sa+.2)]
    st=None
    if r:
        run=min(r,key=lambda x:abs(x[1]-sa)); st=max(run[0],run[1]-.10)
    if st is None: st=sa-.05
    r=[x for x in runs(sb-.2,sb+.6)]
    if r:
        run=min(r,key=lambda x:abs(x[0]-sb)); en=min(run[1],run[0]+.12)
    else: en=sb+.1
    # honour the V2 cuts (fillers, long pauses) inside the span: split on final-timeline segments
    pcs=[]
    for s_,e_,o_ in tm:
        lo=max(a,o_); hi=min(b,o_+e_-s_)
        if hi>lo+.05: pcs.append([s_+lo-o_, s_+hi-o_])
    pcs[0][0]=st; pcs[-1][1]=en
    for p_ in pcs: segs.append([round(p_[0]*30)/30,round(p_[1]*30)/30])
    print(f'final {a:.1f}-{b:.1f} -> pieces {[(round(x,2),round(y,2)) for x,y in pcs]}  startEnv {es[int(pcs[0][0]*100)]:.1f} endEnv {es[int(pcs[-1][1]*100)]:.1f}')
json.dump(segs,open(out,'w'))
