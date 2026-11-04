import json,numpy as np
e=np.load('build/env.npy'); N=len(e)
es=np.convolve(e,np.ones(5)/5,'same'); esl=np.convolve(e,np.ones(11)/11,'same')
FPS=30; TH=-36; MINSIL=.30; GAP=.20
def q(t): return round(t*FPS)/FPS
def snap(t,rad=.12):
    i=int(t*100); lo=max(0,i-int(rad*100)); hi=min(N-1,i+int(rad*100)); return (lo+int(np.argmin(es[lo:hi+1])))/100
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
                a=i0/100+j/100; b=i0/100+k/100; out.append((cur,a+GAP/2)); cur=b-GAP/2
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
# removals (from, to, why): fillers, held vowels 'aaaa', stumbles, CTA, muddled lines
REM=[(115.05,115.52,'aaaa held vowel before "buat posting"'),
     (141.00,141.58,'Okay,'),
     (144.30,147.80,'So yang ni saya nak share / sekejap saya sekejap aku / Okay'),
     (160.36,160.88,'Okay.'),
     (218.80,219.45,'Okay.'),
     (224.98,225.27,'aaa after closing'),
     (236.85,237.58,'aaaa held vowel before "kalau"'),
     (252.38,253.18,'sesuatu eh, (restart)'),
     (262.48,263.12,'Haa,'),
     (273.04,280.24,'Haa, ataupun ... permata (muddled)'),
     (285.86,290.84,'Haa, macam dapat tak ... berjela-jela / Haa, cuma'),
     (301.00,301.40,'Haa,'),
     (303.10,315.00,'CTA: what do you think / komen / follow subscribe')]
EXTRA=[(94.87, 95.37, 'aa filler'), (95.93, 96.63, 'aa filler'), (100.11, 100.51, 'aa filler'), (114.33, 115.05, 'aa filler'), (117.04, 117.58, 'aa filler'), (119.28, 119.98, 'aa filler'), (121.74, 122.18, 'aa filler'), (130.94, 131.6, 'aa filler'), (132.94, 133.22, 'aa filler'), (137.04, 137.68, 'aa filler'), (142.65, 142.81, 'aa filler'), (148.71, 149.35, 'aa filler'), (183.56, 184.33, 'aa filler'), (187.79, 188.41, 'aa filler'), (190.79, 191.63, 'aa filler')]
REM+=EXTRA
import os
if os.path.exists('build/extras.json'): REM+=[tuple(x) for x in json.load(open('build/extras.json'))]
HOOK=[(170.86-.06,175.30),(184.42,187.85)]
keep=[(0.0,315.94)]
REM.sort()
for a,b,w in REM:
    sa,sb=(a,b) if (w=='aa filler' or w.startswith('filler')) else (snap(a),snap(b)); print(f'REM {a:7.2f}->{sa:7.2f}  {b:7.2f}->{sb:7.2f}  dB {es[int(sa*100)]:.0f}/{es[int(sb*100)]:.0f}  {w}')
    keep=subtract(keep,sa,sb)
main=finish([x for s,t in keep for x in squeeze(s,t)])
hook=finish([(snap(a,.1),snap(b,.1)) for a,b in HOOK])
json.dump({'hook':hook,'main':main},open('build/edl_d2.json','w'))
d=lambda L:round(sum(t-s for s,t in L),2)
print('hook',hook,d(hook)); print('main segs',len(main),'dur',d(main),'total',d(hook)+d(main))
