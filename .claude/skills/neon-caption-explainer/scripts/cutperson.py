import json,subprocess,sys
GRADE_ON = False   # True only when the user asks for the indoor-training grade (apply to video AND cut-out)
GRADE = ("eq=contrast=1.07:saturation=0.94:gamma=0.96:brightness=-0.01,colorbalance=rm=0.035:gm=0.005:bm=-0.035:rh=0.02:bh=-0.02:rs=0.015:bs=-0.015,curves=all='0/0 0.12/0.10 0.5/0.5 0.88/0.90 1/0.97',") if GRADE_ON else ''
tm=json.load(open('build/timemap.json'))['map']
FR=[(round(s*30),round(t*30)) for s,t,o in tm]
n=len(FR)
fc=''.join(f"[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS,{GRADE}format=yuv420p[v{i}];[1:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS,alphaextract,format=gray,erosion,erosion,gblur=sigma=0.7[m{i}];" for i,(a,b) in enumerate(FR))
fc+=''.join(f"[v{i}]" for i in range(n))+f"concat=n={n}:v=1:a=0[V];"+''.join(f"[m{i}]" for i in range(n))+f"concat=n={n}:v=1:a=0[M];[V][M]alphamerge,format=yuva420p[o]"
r=subprocess.run(['ffmpeg','-v','error','-y','-i','src/main_raw.mov','-c:v','libvpx-vp9','-i','build/matte_raw.webm','-filter_complex',fc,'-map','[o]','-an','-c:v','libvpx-vp9','-pix_fmt','yuva420p','-crf','14','-b:v','0','-deadline','good','-cpu-used','4','-row-mt','1','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','build/person_clean.webm'],capture_output=True,text=True)
print(r.returncode,r.stderr[-800:])
