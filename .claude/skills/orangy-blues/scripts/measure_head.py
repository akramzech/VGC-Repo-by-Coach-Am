#!/usr/bin/env python3
"""Measure where the head sits in a 1080x1920 portrait clip so words can be placed relative to it.
Usage: /usr/bin/python3 measure_head.py <footage.mov> <cutout.webm> [t=0.5]
Prints JSON {"top":..,"chin":..,"face":[x,y,w,h]}:
  top  = highest opaque row of the cut-out (the hat / hair top)  -> big words sit ~92 px above it (hidden behind the head)
  chin = Vision face-box bottom minus 5 % of its height          -> front words sit ~80 px below it
Needs ffmpeg, swiftc (macOS), PIL + numpy (/usr/bin/python3 has them). Always sanity-check with a snapshot."""
import sys, subprocess, json, os, tempfile
from PIL import Image
import numpy as np
foot, cut = sys.argv[1], sys.argv[2]
t = sys.argv[3] if len(sys.argv) > 3 else "0.5"
d = tempfile.mkdtemp()
f, c = f"{d}/f.png", f"{d}/c.png"
subprocess.run(["ffmpeg","-v","error","-y","-ss",t,"-i",foot,"-frames:v","1",f],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-c:v","libvpx-vp9","-ss",t,"-i",cut,"-frames:v","1","-vf","format=rgba",c],check=True)
a = np.array(Image.open(c))[:, :, 3]
top = int(np.where((a > 128).sum(1) > 20)[0].min())
here = os.path.dirname(os.path.abspath(__file__))
exe = "/private/tmp/face_box"
if not os.path.exists(exe):
    subprocess.run(["swiftc","-O",f"{here}/face_box.swift","-o",exe],check=True)
x, y, w, h = map(int, subprocess.run([exe, f],capture_output=True,text=True,check=True).stdout.split())
print(json.dumps({"top": top, "chin": int(y + h - 0.05 * h), "face": [x, y, w, h]}))
