# Synthesised SFX library (from the Editor Pupus NV build). S(kind, rng) -> mono or stereo float array.
import numpy as np
from scipy import signal
SR=48000
def T(d):return np.arange(int(d*SR))/SR
def sos(kind,f,order=2):return signal.butter(order,f,kind,fs=SR,output='sos')
def bp(x,lo,hi):return signal.sosfilt(sos('band',[max(30,lo),min(SR/2-200,hi)]),x)
def lp(x,f):return signal.sosfilt(sos('low',min(f,SR/2-200)),x)
def hp(x,f):return signal.sosfilt(sos('high',max(20,f)),x)
def nz(R,d):return R.standard_normal(int(d*SR)).astype(np.float32)
def nrm(x):return (x/(np.max(np.abs(x))+1e-9)).astype(np.float32)
def adsr(N,a,dcy,sh=1.):
    t=np.linspace(0,1,N);return np.minimum(t/max(a,1e-4),1)*np.exp(-np.maximum(t-a,0)*dcy)**sh
def sweep(R,d,f0,f1,q=.35,att=.3,dcy=3.):
    x=nz(R,d);N=len(x);out=np.zeros_like(x);B=28;bl=max(1,N//B)
    for b in range(B):
        f=f0*(f1/f0)**(b/(B-1));seg=bp(x[b*bl:(b+1)*bl+bl//2],f*(1-q),f*(1+q))[:bl];out[b*bl:b*bl+len(seg)]=seg
    return nrm(out*adsr(N,att,dcy))
def tone(f,d,dec,harm=((1,1),),fm=0,fmr=2.0,glide=1.0):
    t=T(d);ph=2*np.pi*np.cumsum(f*(glide**(t/d)))/SR;x=sum(a*np.sin(h*ph+fm*np.sin(2*np.pi*f*fmr*t)) for h,a in harm);return nrm(x*np.exp(-t*dec))
lib={}
def S(name,R):
    k=name
    if k=='boot':
        t=T(1.3);x=.8*np.sin(2*np.pi*(38+20*t)*t)*np.minimum(t/.5,1)*np.exp(-t*2)+.35*hp(nz(R,1.3),6000)*np.exp(-t*4)+.3*tone(1760*R.uniform(.98,1.02),1.3,3.5,((1,1),(2,.3)))
        return nrm(x)
    if k=='tink':return tone(R.uniform(2400,2800),.5,9,((1,1),(2.76,.4),(5.4,.15)))
    if k=='swish_up':return sweep(R,R.uniform(.3,.42),R.uniform(500,800),R.uniform(3500,5200),.4,.55,3)
    if k=='swish_dn':return sweep(R,R.uniform(.3,.42),R.uniform(4000,5200),R.uniform(500,800),.4,.15,3)
    if k=='key':
        d=.035;x=hp(nz(R,d),R.uniform(1800,3500))*np.exp(-T(d)*R.uniform(120,220))+.4*tone(R.uniform(900,1500),d,160);return nrm(x)
    if k=='zoom_in':
        t=T(.75);wh=np.sin(2*np.pi*np.cumsum(220+900*(t/.75)**1.6)/SR)*.35*(t/.75);x=wh+sweep(R,.75,400,4200,.3,.7,2.5)*.8;return nrm(x*np.minimum(t/.05,1))
    if k=='zoom_out':
        t=T(.7);wh=np.sin(2*np.pi*np.cumsum(1100-850*(t/.7)**.7)/SR)*.35*(1-t/.7);x=wh+sweep(R,.7,4200,350,.3,.15,2.5)*.8;return nrm(x)
    if k=='ping':
        f=R.uniform(1100,1500);return tone(f,.55,7,((1,1),(1.5,.5),(2,.25)))
    if k=='slide':return sweep(R,.35,R.uniform(300,500),R.uniform(1600,2400),.5,.4,4)
    if k=='pop':
        f=R.uniform(500,1500);t=T(.11);x=np.sin(2*np.pi*f*(1+.7*np.exp(-t*55))*t)*np.exp(-t*R.uniform(35,60));return nrm(x)
    if k=='slam':
        t=T(.9);x=np.sin(2*np.pi*(48+120*np.exp(-t*16))*t)*np.exp(-t*5)+.4*lp(nz(R,.9),900)*np.exp(-t*12)+.25*hp(nz(R,.9),7000)*np.exp(-t*6);return nrm(x)
    if k=='rewind':
        t=T(1.75);car=np.sin(2*np.pi*np.cumsum(2400*(1-.75*t/1.75)+180*np.sin(2*np.pi*7*t))/SR);x=car*.4+bp(nz(R,1.75),900,5000)*.6;return nrm(x*np.minimum(t/.1,1)*np.exp(-t*.8))
    if k=='bell':return tone(R.uniform(780,800),1.2,3.2,((1,1),(2.0,.5),(3.01,.3),(4.17,.15)))
    if k=='check':return tone(R.uniform(1000,1700),.35,11,((1,1),(3,.2)),fm=.6,fmr=R.uniform(1.4,2.2))
    if k=='riser':
        t=T(3.3);x=sweep(R,3.3,180,3600,.5,.98,.2)*.6+.4*np.sin(2*np.pi*np.cumsum(90+300*(t/3.3)**2)/SR)*(t/3.3)**1.5;return nrm(x)
    if k=='boom':
        t=T(1.4);x=np.sin(2*np.pi*(40+90*np.exp(-t*10))*t)*np.exp(-t*3)+.5*lp(nz(R,1.4),700)*np.exp(-t*7)+.3*hp(nz(R,1.4),3000)*np.exp(-t*9);return nrm(x)
    if k=='portal':
        f0=R.uniform(300,700);x=sweep(R,.5,f0,f0*R.uniform(4,7),.3,.45,3.5)+.25*tone(R.uniform(600,1200),.5,6,glide=R.uniform(1.5,2.2));return nrm(x)
    if k=='whoomp':
        t=T(.9);x=np.sin(2*np.pi*(70-30*t)*t)*np.minimum(t/.08,1)*np.exp(-t*4)+.3*sweep(R,.9,200,900,.5,.3,3);return nrm(x)
    if k=='suction':
        t=T(1.3);x=sweep(R,1.3,5000,600,.4,.95,.3)*.7+.3*np.sin(2*np.pi*np.cumsum(900-500*t/1.3)/SR)*(t/1.3);return nrm(x)
    if k=='hum':
        t=T(1.6);x=(np.sin(2*np.pi*110*t)+.5*np.sin(2*np.pi*165.5*t)+.2*np.sin(2*np.pi*331*t))*(1+.3*np.sin(2*np.pi*6*t))*np.minimum(t/.3,1)*np.minimum((1.6-t)/.2,1);return nrm(lp(x,1200))
    if k=='wub':
        t=T(.4);x=np.sin(2*np.pi*(90+60*np.sin(np.pi*t/.4))*t)*np.sin(np.pi*t/.4);return nrm(x)
    if k=='throw':return sweep(R,.6,350,4800,.35,.8,2.5)
    if k=='implode':
        t=T(1.0);suck=sweep(R,.22,5200,300,.35,.98,.2);burst=np.sin(2*np.pi*(55+200*np.exp(-t*20))*t)*np.exp(-t*4)+.5*hp(nz(R,1.0),4500)*np.exp(-t*5)
        sp=sum(tone(R.uniform(2500,6000),1.0,R.uniform(5,9))*R.uniform(.1,.25) for _ in range(6));x=np.concatenate([suck,nrm(burst+sp)]);return nrm(x)
    if k=='zap':
        t=T(.55);x=hp(nz(R,.55),2500)*(np.abs(np.sin(2*np.pi*R.uniform(40,70)*t))>.6)*np.exp(-t*7)+.5*np.sin(2*np.pi*np.cumsum(3000*np.exp(-t*8)+200)/SR)*np.exp(-t*9);return nrm(x)
    if k=='thunder':
        t=T(1.3);x=hp(nz(R,1.3),1500)*np.exp(-t*9)*.8+lp(nz(R,1.3),300)*np.exp(-t*2.5)*.9+np.sin(2*np.pi*(45+60*np.exp(-t*8))*t)*np.exp(-t*3)*.7;return nrm(x)
    if k=='airdown':return sweep(R,.8,3000,400,.5,.3,1.5)
    if k=='knock':
        t=T(.18);x=bp(nz(R,.18),600,1800)*np.exp(-t*45)+.6*np.sin(2*np.pi*R.uniform(180,240)*t)*np.exp(-t*30);return nrm(x)
    if k=='blip':return tone(R.uniform(1800,2400),.12,30,((1,1),(2,.3)))
    if k=='chirp':
        t=T(.3);x=np.sin(2*np.pi*np.cumsum(np.where((t*30).astype(int)%2==0,1600,2300)*1.0)/SR)*np.exp(-t*9);return nrm(x)
    if k=='chord':
        base=R.uniform(520,560);x=sum(tone(base*r,.9,3.5,((1,1),(2,.25))) for r in (1,1.26,1.5,2));return nrm(x)
    if k=='ratchet':
        d=.03;x=hp(nz(R,d),R.uniform(2000,4000))*np.exp(-T(d)*R.uniform(150,260))+.5*np.sin(2*np.pi*R.uniform(600,1100)*T(d))*np.exp(-T(d)*140);return nrm(x)
    if k=='clunk':
        t=T(.4);x=lp(nz(R,.4),1200)*np.exp(-t*20)+np.sin(2*np.pi*95*t)*np.exp(-t*14);return nrm(x)
    if k=='stab':
        t=T(.6);f=R.uniform(440,470);x=sum(signal.sawtooth(2*np.pi*f*r*t)*a for r,a in ((1,1),(1.5,.6),(2,.5)));return nrm(lp(x,4200)*np.exp(-t*6))
    if k=='buzz':
        t=T(.35);x=signal.square(2*np.pi*110*t)*.5+signal.square(2*np.pi*116*t)*.5;return nrm(lp(x,900)*np.exp(-t*7))
    if k=='bigwhoosh':
        t=T(1.0);x=sweep(R,1.0,200,6000,.3,.6,2.2);pan=np.linspace(-.8,.8,len(x));return np.stack([x*(1-pan)/2*1.4,x*(1+pan)/2*1.4],1)
    if k=='shimmer':return nrm(sum(tone(R.uniform(3000,7000),.8,R.uniform(4,8))*R.uniform(.2,.5) for _ in range(8)))
    if k=='revwhoosh':return sweep(R,.6,5000,300,.35,.2,2.5)
    if k=='drone':
        t=T(3.4);x=(signal.sawtooth(2*np.pi*55*t)*.5+signal.sawtooth(2*np.pi*55.6*t)*.5+.4*np.sin(2*np.pi*82.4*t));return nrm((lp(x,320)*(1-t/3.4)+lp(x,850)*(t/3.4))*np.minimum(t/1.2,1))
    if k=='lowboom':
        t=T(1.0);x=np.sin(2*np.pi*(36+40*np.exp(-t*6))*t)*np.minimum(t/.04,1)*np.exp(-t*2.6);return nrm(x)
    if k=='shing':
        t=T(.5);x=hp(nz(R,.5),5000)*np.exp(-t*8)+.5*tone(R.uniform(3500,4200),.5,6,((1,1),(1.41,.6)));return nrm(x)
    if k=='stamp':
        t=T(.6);x=np.sin(2*np.pi*(60+140*np.exp(-t*25))*t)*np.exp(-t*7)+.6*lp(nz(R,.6),1500)*np.exp(-t*25);return nrm(x)
    if k=='pad':
        t=T(1.6);x=sum(np.sin(2*np.pi*f*t+R.uniform(0,6)) for f in (261.6,329.6,392,523.3))*np.minimum(t/.9,1)*np.minimum((1.6-t)/.5,1);return nrm(lp(x,2200))
    if k=='confetti':
        t=T(1.0);x=sum(tone(R.uniform(900,4000),1.0,R.uniform(8,16))*R.uniform(.1,.3)*np.roll(np.ones(len(t)),0) for _ in range(10))+hp(nz(R,1.0),3000)*np.exp(-t*12)*.6
        pops=np.zeros(len(t))
        for _ in range(14):
            i=int(R.uniform(0,.5)*SR);L=int(.04*SR);pops[i:i+L]+=np.sin(2*np.pi*R.uniform(700,1600)*np.arange(L)/SR)*np.exp(-np.arange(L)/SR*60)
        return nrm(x+pops*.7)
    if k=='sand':
        d=1.1;t=T(d);x=nz(R,d);g=(R.random(len(x))>.985).astype(np.float32)*R.uniform(.5,1,len(x));gr=np.convolve(g,np.exp(-np.arange(int(.004*SR))/(.0012*SR)),'same')
        x=hp(gr*bp(x,2500,9000)*3+bp(nz(R,d),3000,8000)*.25,1800)*np.minimum(t/.15,1)*np.exp(-t*1.6);x=np.tanh(4*nrm(x))/np.tanh(4)*.7;pan=np.linspace(-.7,.7,len(x));return np.stack([x*(1-pan),x*(1+pan)],1)
    if k=='zip':
        t=T(.5);x=np.sin(2*np.pi*np.cumsum(500+2600*(t/.5)**1.4)/SR)*np.sin(np.pi*t/.5)*.5+bp(nz(R,.5),1500,4000)*.15*np.sin(np.pi*t/.5);return nrm(x)
    if k=='switch':
        t=T(.5);x=bp(nz(R,.5),1500,6000)*np.exp(-t*90)+.7*np.sin(2*np.pi*R.uniform(160,190)*t)*np.exp(-t*40)+.25*lp(nz(R,.5),400)*np.exp(-t*18);return nrm(x)
    if k=='rattle':
        d=.7;t=T(d);x=np.zeros(len(t))
        for j in range(int(d*24)):
            i=int(j/24*SR);L=int(.012*SR);x[i:i+L]+=hp(nz(R,.012),R.uniform(1500,2600))[:L]*np.exp(-np.arange(L)/SR*300)
        return nrm(x*np.minimum(t/.1,1)*np.minimum((d-t)/.2,1))
    raise ValueError(k)
