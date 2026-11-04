import json,numpy as np
e=np.load('build/env.npy'); N=len(e); es=np.convolve(e,np.ones(5)/5,'same'); FPS=30; SIL=-34
def q(t): return round(t*FPS)/FPS
def runs(lo,hi):
    i0,i1=int(lo*100),int(hi*100); m=es[i0:i1]<SIL; r=[];j=0
    while j<len(m):
        if m[j]:
            k=j
            while k<len(m) and m[k]: k+=1
            r.append(((i0+j)/100,(i0+k)/100)); j=k
        else: j+=1
    return r
END_RAW=155.60
rs=runs(END_RAW-.2,END_RAW+.6); END=min(rs[0][0]+.25,END_RAW+.35) if rs else END_RAW+.1
# 1) manual removal: held vowel / noise 135.15-137.15 (re-checked by re-transcription)
REM=[(135.15,137.15,'held vowel / noise')]
# 2) every silent run > 0.7 s is shortened to 0.5 s (0.25 s kept each side)
es9=np.convolve(e,np.ones(9)/9,'same'); m9=es9<-32; allruns=[]; j=0
while j<len(m9):
    if m9[j]:
        k=j
        while k<len(m9) and m9[k]: k+=1
        if (k-j)>=70 and j>100 and k/100<END: allruns.append((j/100,k/100))
        j=k
    else: j+=1
for a,b in allruns:
    if any(x<=a and b<=y+0.01 for x,y,_ in REM): continue
    REM.append((a+.25,b-.25,'long pause'))
REM.sort()
keep=[(0.0,END)]
def subtract(keep,a,b):
    nk=[]
    for s,t in keep:
        if b<=s or a>=t: nk.append((s,t))
        else:
            if a>s: nk.append((s,a))
            if b<t: nk.append((b,t))
    return nk
for a,b,w in REM:
    print(f'REM {a:7.2f}-{b:7.2f} {b-a:4.2f}s {w}'); keep=subtract(keep,a,b)
main=[(q(s),q(t)) for s,t in keep if t-s>.12]
# hook: silence before 'Bisnes tak pernah ada masalah' (87.14) .. after 'bisnes tu' (~94.1)
r=runs(86.3,87.3); hs=max(r[-1][1]-.10,86.5) if r else 87.0
r=runs(93.9,94.7); he=(r[0][0]+.12) if r else 94.2
hook=[(q(hs),q(he))]
json.dump({'hook':hook,'main':main},open('build/edl_d3.json','w'))
d=lambda L:round(sum(t-s for s,t in L),2)
print('END',round(END,2),'hook',hook,d(hook),'main segs',len(main),'dur',d(main),'total',d(hook)+d(main))
