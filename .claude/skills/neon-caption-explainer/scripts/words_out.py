import json,numpy as np,scipy.io.wavfile as w
tm=json.load(open('build/timemap.json')); M=tm['map']; HD=tm['hook_dur']
# hook segs are first 3 (by hook duration); main = rest
acc=0;hk=[]
for s,t,o in M:
    if o+1e-6<HD: hk.append((s,t,o))
main=[m for m in M if m[2]>=HD-1e-6]
words=json.load(open('build/wordlist.json'))
sr,x=w.read('build/voice.wav');x=x.astype(np.float32)/32768
hop=sr//100;n=len(x)//hop
e=20*np.log10(np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))+1e-9);es=np.convolve(e,np.ones(3)/3,'same')
cand=np.array([i for i in range(2,n-8) if es[i]<=es[i-1] and es[i]<=es[i+1] and es[i+8]-es[i]>=6])/100
def out_of(t,segs):
    for s,u,o in segs:
        if s-0.02<=t<u: return o+max(0,t-s)
    return None
res=[]
for t,a,b in words:
    o=out_of(a,main)
    if o is None: continue
    c=cand[(cand>o-.12)&(cand<o+.3)]
    sn=float(c[np.argmin(np.abs(c-(o+.08)))]) if len(c) else o
    res.append((t,round(sn,2),round(o,2),round(a,2)))
json.dump(res,open('build/words_out.json','w'),ensure_ascii=False)
print(' '.join(f"{t}@{sn}" for t,sn,o,a in res))
