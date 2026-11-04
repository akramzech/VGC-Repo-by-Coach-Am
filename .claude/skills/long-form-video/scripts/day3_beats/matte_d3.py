import json,subprocess,sys,os
iv=json.load(open('build/bh_intervals.json'))
for sid,t0,t1 in iv:
    out=f'hf/assets/matte/{sid}.webm'
    if os.path.exists(out): print('skip',sid); continue
    a=round(t0*30); b=round(t1*30); tmp=f'build/mtmp/{sid}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-i','build/main.mp4','-vf',f'trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS','-an','-c:v','libx264','-preset','veryfast','-crf','12','-pix_fmt','yuv420p',tmp],check=True)
    r=subprocess.run(['npx','--yes','hyperframes@0.8.216','remove-background',tmp,'-o',out,'--quality','best'],capture_output=True,text=True)
    print(sid,a,b,'rc',r.returncode,r.stdout[-200:].strip().splitlines()[-1:],flush=True)
print('matte done')
