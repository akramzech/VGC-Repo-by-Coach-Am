import json,numpy as np
e=np.load('build/env.npy'); N=len(e)
es=np.convolve(e,np.ones(5)/5,'same')
END=105.5; FPS=30
TH=-40; MINSIL=.26; GAP=.16
def snap(t,rad=.12):
    i=int(t*100); lo=max(0,i-int(rad*100)); hi=min(N-1,i+int(rad*100))
    return (lo+int(np.argmin(es[lo:hi+1])))/100
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
    i0,i1=int(s*100),min(N,int(t*100)); low=es[i0:i1]<TH
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
REM=[(48.60,51.25),(52.70,54.68),(96.95,102.78)]
keep=[(snap(1.68-0.12,.1),END)]
for a,b in REM: keep=subtract(keep,snap(a),snap(b))
main=finish([x for s,t in keep for x in squeeze(s,t)])
hook=[]
json.dump({'hook':hook,'main':main},open('build/edl.json','w'))
d=lambda L:round(sum(t-s for s,t in L),2)
print('hook',hook,d(hook)); print('main',len(main),d(main),'total',d(hook)+d(main))
