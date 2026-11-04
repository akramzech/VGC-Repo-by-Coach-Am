import json,subprocess,os,sys
B=os.environ.get("WALL_ROOT", "input/")  # folder that holds your own finished videos
src=[B+x[2].strip() for x in json.load(open('build/wall_sources.json'))]
n=len(src); print(n,'sources')
W,H=112,199; GAP=16; COLS=22; DUR=12
def dur(p):
    r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True); return float(r.stdout.strip())
D={p:dur(p) for p in src}
for row in range(5):
    cmd=['ffmpeg','-v','error','-y']; fl=[]
    for c in range(COLS):
        p=src[(c*7+row*11)%n]; d=D[p]
        frac=0.10+(((c*37+row*53)%70)/100)
        ss=max(0,min(d*frac,d-DUR-0.5)) if d>DUR+1 else 0
        cmd+=['-ss',f'{ss:.2f}','-t',str(DUR),'-i',p]
        fl.append(f"[{c}:v]fps=30,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},tpad=stop_mode=clone:stop_duration={DUR},trim=duration={DUR},setpts=PTS-STARTPTS,pad={W+GAP}:{H}:{GAP//2}:0:color=black,drawbox=x={GAP//2}:y=0:w={W}:h={H}:color=white@0.55:t=2[t{c}]")
    fc=';'.join(fl)+';'+''.join(f'[t{c}]' for c in range(COLS))+f'hstack=inputs={COLS}[o]'
    cmd+=['-filter_complex',fc,'-map','[o]','-an','-c:v','libx264','-preset','fast','-crf','20','-g','15','-pix_fmt','yuv420p','-t',str(DUR),f'hf/assets/wall/row{row}.mp4']
    r=subprocess.run(cmd,capture_output=True,text=True)
    print('row',row,'rc',r.returncode,r.stderr[-300:] if r.returncode else '')
print('wall done')
