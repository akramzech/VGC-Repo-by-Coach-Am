import json,subprocess
E=json.load(open('build/edl_d2.json')); segs=E['hook']+E['main']
FR=[(round(s*30),round(t*30)) for s,t in segs]; segs=[(a/30,b/30) for a,b in FR]
tm=[];o=0.0
for s,t in segs: tm.append((s,t,round(o,4))); o+=t-s
json.dump({'map':tm,'dur':round(o,3),'hook_dur':round(sum(b-a for a,b in FR[:len(E['hook'])])/30,3)},open('build/timemap.json','w'))
af=''.join(f"[0:a]atrim={s:.4f}:{t:.4f},asetpts=PTS-STARTPTS,pan=mono|c0=0.5*c0+0.5*c1,afade=t=in:d=0.008,afade=t=out:st={t-s-0.008:.4f}:d=0.008[a{i}];" for i,(s,t) in enumerate(segs))
af+=''.join(f"[a{i}]" for i in range(len(segs)))+f"concat=n={len(segs)}:v=0:a=1[o]"
subprocess.run(['ffmpeg','-v','error','-y','-i','src/main_raw.mov','-filter_complex',af,'-map','[o]','-ar','48000','-c:a','pcm_s16le','build/voice.wav'],check=True); print('dur',o)
