import json,subprocess,sys
GRADE_ON = False   # True only when the user asks for the indoor-training grade (apply to video AND cut-out)
GRADE = ("eq=contrast=1.07:saturation=0.94:gamma=0.96:brightness=-0.01,colorbalance=rm=0.035:gm=0.005:bm=-0.035:rh=0.02:bh=-0.02:rs=0.015:bs=-0.015,curves=all='0/0 0.12/0.10 0.5/0.5 0.88/0.90 1/0.97',") if GRADE_ON else ''
E=json.load(open('build/edl.json'))
segs=[tuple(x) for x in E['hook']]+[tuple(x) for x in E['main']]
FR=[(round(s*30),round(t*30)) for s,t in segs]
segs=[(a/30,b/30) for a,b in FR]
tm=[];o=0.0
for s,t in segs: tm.append((s,t,round(o,4))); o+=t-s
json.dump({'map':tm,'dur':round(o,4),'hook_dur':round(sum(t-s for s,t in E['hook']),4)},open('build/timemap.json','w'))
print('out dur',o)
def run(cmd): 
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
# 1) video (no audio)
vf=''.join(f"[0:v]trim=start_frame={FR[i][0]}:end_frame={FR[i][1]},setpts=PTS-STARTPTS,{GRADE}format=yuv420p[v{i}];" for i,(s,t) in enumerate(segs))
vf+=''.join(f"[v{i}]" for i in range(len(segs)))+f"concat=n={len(segs)}:v=1:a=0[o]"
run(['ffmpeg','-v','error','-y','-i','src/main_raw.mov','-filter_complex',vf,'-map','[o]','-an','-c:v','libx264','-preset','slow','-crf','17','-g','15','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-movflags','+faststart','build/main.mp4'])
print('main.mp4 ok')
# 2) voice (mono fold of L+R, fades 8ms)
af=''.join(f"[0:a]atrim={s:.4f}:{t:.4f},asetpts=PTS-STARTPTS,pan=mono|c0=0.5*c0+0.5*c1,afade=t=in:d=0.008,afade=t=out:st={t-s-0.008:.4f}:d=0.008[a{i}];" for i,(s,t) in enumerate(segs))
af+=''.join(f"[a{i}]" for i in range(len(segs)))+f"concat=n={len(segs)}:v=0:a=1[o]"
run(['ffmpeg','-v','error','-y','-i','src/main_raw.mov','-filter_complex',af,'-map','[o]','-ar','48000','-c:a','pcm_s16le','build/voice.wav'])
print('voice ok')
# 3) exact cut-out: source YUV + matte alpha
fc=''.join(f"[0:v]trim=start_frame={FR[i][0]}:end_frame={FR[i][1]},setpts=PTS-STARTPTS,{GRADE}format=yuv420p[v{i}];[1:v]trim=start_frame={FR[i][0]}:end_frame={FR[i][1]},setpts=PTS-STARTPTS,alphaextract,format=gray[m{i}];" for i,(s,t) in enumerate(segs))
fc+=''.join(f"[v{i}]" for i in range(len(segs)))+f"concat=n={len(segs)}:v=1:a=0[V];"+''.join(f"[m{i}]" for i in range(len(segs)))+f"concat=n={len(segs)}:v=1:a=0[M];[V][M]alphamerge,format=yuva420p[o]"
run(['ffmpeg','-v','error','-y','-i','src/main_raw.mov','-c:v','libvpx-vp9','-i','build/matte_raw.webm','-filter_complex',fc,'-map','[o]','-an','-c:v','libvpx-vp9','-pix_fmt','yuva420p','-crf','14','-b:v','0','-deadline','good','-cpu-used','4','-row-mt','1','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','build/person.webm'])
print('person ok')
