import json,subprocess,sys
E=json.load(open('build/edl2.json'))
segs=[tuple(x) for x in E['hook']]+[tuple(x) for x in E['main']]
FR=[(round(s*30),round(t*30)) for s,t in segs]
segs=[(a/30,b/30) for a,b in FR]
tm=[];o=0.0
for s,t in segs: tm.append((s,t,round(o,4))); o+=t-s
hd=sum(t-s for s,t in [tuple(x) for x in E['hook']])
TAIL=0.35
json.dump({'map':tm,'dur':round(o+TAIL,4),'hook_dur':round(sum(b-a for a,b in FR[:len(E['hook'])])/30,4)},open('build/timemap.json','w'))
print('out dur',o+TAIL)
GRADE=open('build/grade/G3.txt').read().strip()
def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
vf=''.join(f"[0:v]trim=start_frame={FR[i][0]}:end_frame={FR[i][1]},setpts=PTS-STARTPTS[v{i}];" for i in range(len(segs)))
vf+=''.join(f"[v{i}]" for i in range(len(segs)))+f"concat=n={len(segs)}:v=1:a=0,{GRADE},tpad=stop_mode=clone:stop_duration={TAIL},format=yuv420p[o]"
run(['ffmpeg','-v','error','-y','-i','src/main_raw.mov','-filter_complex',vf,'-map','[o]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-g','15','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-movflags','+faststart','build/main.mp4'])
print('main.mp4 ok')
af=''.join(f"[0:a]atrim={s:.4f}:{t:.4f},asetpts=PTS-STARTPTS,pan=mono|c0=0.5*c0+0.5*c1,afade=t=in:d=0.008,afade=t=out:st={t-s-0.008:.4f}:d=0.008[a{i}];" for i,(s,t) in enumerate(segs))
af+=''.join(f"[a{i}]" for i in range(len(segs)))+f"concat=n={len(segs)}:v=0:a=1,apad=pad_dur={TAIL}[o]"
run(['ffmpeg','-v','error','-y','-i','src/main_raw.mov','-filter_complex',af,'-map','[o]','-ar','48000','-c:a','pcm_s16le','build/voice.wav'])
print('voice ok')
