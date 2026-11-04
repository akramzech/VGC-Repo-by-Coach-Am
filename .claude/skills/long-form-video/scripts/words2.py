import json,numpy as np,scipy.io.wavfile as w
sr,x=w.read('build/voice.wav'); x=x.astype(np.float32)/32768
hop=sr//100; n=len(x)//hop
e=20*np.log10(np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))+1e-9); es=np.convolve(e,np.ones(3)/3,'same')
cand=np.array([i for i in range(2,n-8) if es[i]<=es[i-1] and es[i]<=es[i+1] and es[i+8]-es[i]>=6])/100
S=json.load(open('build/words_cut.json')); res=[]
for s in S:
    for t,a,b in s['w']:
        c=cand[(cand>a-.12)&(cand<a+.3)]
        sn=float(c[np.argmin(np.abs(c-(a+.08)))]) if len(c) else a
        res.append((t,round(sn,2),a,b))
json.dump(res,open('build/words_out.json','w'),ensure_ascii=False)
print(len(res),'words')
