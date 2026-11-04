import json,numpy as np
e=np.load('build/env.npy'); N=len(e)
es=np.convolve(e,np.ones(5)/5,'same'); esl=np.convolve(e,np.ones(11)/11,'same')
FPS=30; TH=-36; MINSIL=.30; GAP=.20
def q(t): return round(t*FPS)/FPS
def subtract(keep,a,b):
    nk=[]
    for s,t in keep:
        if b<=s or a>=t: nk.append((s,t))
        else:
            if a>s: nk.append((s,a))
            if b<t: nk.append((b,t))
    return nk
def squeeze(s,t):
    i0,i1=int(s*100),min(N,int(t*100)); low=esl[i0:i1]<TH
    out=[];cur=s;j=0
    while j<len(low):
        if low[j]:
            k=j
            while k<len(low) and low[k]: k+=1
            if (k-j)/100>MINSIL:
                a=i0/100+j/100; b=i0/100+k/100
                out.append((cur,a+GAP/2)); cur=b-GAP/2
            j=k
        else: j+=1
    out.append((cur,t)); return out
def finish(segs):
    r=[]
    for s,t in segs:
        s,t=q(s),q(t)
        if t-s<.12: continue
        i0,i1=int(s*100),int(t*100)
        if t-s<.35 and es[i0:i1].max()<-30: continue
        r.append((s,t))
    return r
REM=[(94.80,96.45,'batuk + dead air'),(101.20,103.52,'lebih kurang dalam 7, eh bukan 7'),(130.34,136.40,'adjust jalan + ulang'),
     (145.99,147.55,'so nanti kita tengok lah'),(168.93,169.55,'nafas / lip noise'),(289.28,289.78,'hmm click')]
HOOK=(193.68,201.85)
P1=(0.0,264.50)          # ... episode yang pertama
P2=(288.26,304.30)       # aku personally nak try ... tak boleh konsisten
P3=(281.30,285.82)       # anything kita jumpa esok lah untuk episode yang kedua
def part(a,b):
    keep=[(a,b)]
    for x,y,w in REM: keep=subtract(keep,x,y)
    return finish([z for s,t in keep for z in squeeze(s,t)])
hook=finish([HOOK])
main=part(*P1)+part(*P2)+part(*P3)
json.dump({'hook':hook,'main':main},open('build/edl2.json','w'))
d=lambda L:round(sum(t-s for s,t in L),2)
print('hook',hook,d(hook)); print('main segs',len(main),'dur',d(main),'total',d(hook)+d(main))
