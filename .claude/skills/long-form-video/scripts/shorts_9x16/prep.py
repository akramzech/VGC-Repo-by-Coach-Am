#!/usr/bin/env /usr/bin/python3
"""prep.py NAME span... : EDL (silence-snapped) -> voice.wav -> words.json -> 9:16 graded video.  Run from scratchpad/. spans = FINAL-video first:last word times"""
import sys,json,subprocess,os,shutil
name=sys.argv[1]; spans=sys.argv[2:]; D=f'{name}'; os.makedirs(f'{D}/hf/assets/audio',exist_ok=True); os.makedirs(f'{D}/hf/assets/img',exist_ok=True)
r=subprocess.run(['/usr/bin/python3','scripts/short_edl.py',f'../{D}/edl.json']+spans,cwd='day2',capture_output=True,text=True); print(r.stdout,r.stderr[-300:])
segs=json.load(open(f'{D}/edl.json')); FR=[(round(s*30),round(t*30)) for s,t in segs]; segs=[(a/30,b/30) for a,b in FR]
tm=[];o=0
for s,t in segs: tm.append((s,t,o)); o+=t-s
json.dump({'map':tm,'dur':o},open(f'{D}/timemap.json','w')); print('dur',o)
af=''.join(f"[0:a]atrim={s:.4f}:{t:.4f},asetpts=PTS-STARTPTS,pan=mono|c0=0.5*c0+0.5*c1,afade=t=in:d=0.008,afade=t=out:st={t-s-0.008:.4f}:d=0.008[a{i}];" for i,(s,t) in enumerate(segs))
af+=''.join(f"[a{i}]" for i in range(len(segs)))+f"concat=n={len(segs)}:v=0:a=1[o]"
subprocess.run(['ffmpeg','-v','error','-y','-i','day2/src/main_raw.mov','-filter_complex',af,'-map','[o]','-ar','48000','-c:a','pcm_s16le',f'{D}/voice.wav'],check=True)
for f in ['jersey_my.png','jersey_grid.png','pin_col0.jpg','pin_col1.jpg','pin_col2.jpg','pin_col3.jpg','openai.svg','claude.png','deepseek.png','lovable.png','manus.png']:
    shutil.copy(f'day2/hf/assets/img/{f}',f'{D}/hf/assets/img/{f}')
for f in ['hyperframes.json','meta.json','package.json']: shutil.copy(f'day2/hf/{f}',f'{D}/hf/{f}')
G=open('day2/build/G3.txt').read().strip()
vf=''.join(f"[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS,crop=608:1080:600:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6:5:5:0.0[v{i}];" for i,(a,b) in enumerate(FR))
vf+=''.join(f"[v{i}]" for i in range(len(FR)))+f"concat=n={len(FR)}:v=1:a=0,{G},tpad=stop_mode=clone:stop_duration=0.35,format=yuv420p[o]"
rr=subprocess.run(['ffmpeg','-v','error','-y','-i','day2/src/main_raw.mov','-filter_complex',vf,'-map','[o]','-an','-c:v','libx264','-preset','veryfast','-crf','17','-g','15','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-movflags','+faststart',f'{D}/hf/assets/main.mp4'],capture_output=True,text=True); print('video rc',rr.returncode,rr.stderr[-200:])
subprocess.run(['/usr/bin/python3','day2/scripts/transcribe_words.py',f'{D}/voice.wav',f'{D}/words.json'],capture_output=True)
w=json.load(open(f'{D}/words.json')); print(' '.join(f'{a}@{s:.1f}' for x in w for a,s,e in x['w']))
for x in w: print(f"{x['s']:5.1f} {x['t']}")
