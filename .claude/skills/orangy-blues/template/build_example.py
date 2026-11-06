#!/usr/bin/env python3
"""Orangy Blues: worked example (a 69 s, 9:16 talking-head clip). EDIT the config blocks (B beats, BR stills, G grids, the visuals
block, the music block, the final results block), then:  python3 build_example.py <project_dir>
Reads <project_dir>/onsets.json (voice onsets, see scripts/voice_env.py) and writes <project_dir>/hf/index.html.
Assets it expects under <project_dir>/hf/assets/: raw.mov, cut.webm, broll/*, logos/* (the student's own), tele/*, music/track.mp3, sfx/*.mp3.
Reframe 1.15x anchored at the bottom from 5.5-7.0 s so head.top ~357 / chin ~870 (the geometry the style expects)."""
import json, os, re

import sys
SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # the orangy-blues skill folder
HERE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()   # the project folder
HF = os.path.join(HERE, "hf")
D = 69.38
HEAD_TOP, CHIN = 357, 870
SB, SF, BACK_TOP = 1.55, 1.9355, 130
ACC, ACC2, G0, G1, G2 = "#ff6a1a", "#1f5bff", "#ffb78a", "#ff6a1a", "#e23d00"
ONSETS = json.load(open(os.path.join(HERE, "onsets.json")))

def snap(t):
    c = [o for o in ONSETS if t - 0.12 <= o <= t + 0.2]
    return round(min(c, key=lambda o: abs(o - (t + 0.04))), 2) if c else round(t, 2)

u_back = lambda px: round((px - BACK_TOP) / SB, 1)
u_front = lambda px: round(px / SF, 1)

# ---------------------------------------------------------------- CSS
def rgba0(h):
    h = h.lstrip("#"); return "rgba(%d,%d,%d,0)" % (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
css = open(os.path.join(SKILL, "template", "style.css")).read()
for k, v in {"__ACCENT__": ACC, "__ACCENT2__": ACC2, "__G0__": G0, "__G2__": G2, "__ACCENT_0__": rgba0(ACC), "__ACCENT2_0__": rgba0(ACC2)}.items():
    css = css.replace(k, v)
css = css.replace(G0 + " 0%," + ACC + " 46%", G0 + " 0%," + G1 + " 46%")
css += """
      /* ---- long-form additions ---- */
      .rfw { position:absolute; left:0; top:0; width:1080px; height:1920px; transform-origin:50% 100%; }
      .uf .layer, .ub .layer { overflow:visible; }
      .fc video { position:absolute; left:0; top:0; width:100%; height:100%; object-fit:cover; }
      .fc.txt { background:linear-gradient(160deg, rgba(34,36,46,.94), rgba(14,15,20,.94)); }
      .fc.txt .nm { position:absolute; left:0; right:0; top:50%; margin-top:-28px; text-align:center; font-family:"Archivo Black",sans-serif; font-size:25px; line-height:1.1; color:#fff; letter-spacing:.01em; }
      .xm { position:absolute; right:12px; top:14px; width:70px; height:70px; border-radius:50%; background:__ACCENT__; color:#fff; font-weight:800; font-size:46px; line-height:68px; text-align:center; opacity:0; box-shadow:0 8px 24px rgba(0,0,0,.4); }
      .fc.tele { border-radius:20px; }
      .fc.tile { border-radius:26px; border:1.5px solid rgba(255,255,255,.5); overflow:visible; }
      .fc.tile .lgf { position:absolute; left:0; top:0; width:100%; height:100%; background-size:contain; background-repeat:no-repeat; background-position:center; border-radius:24px; }
      .fc.tile .xm { width:44px; height:44px; font-size:28px; line-height:42px; right:-12px; top:-12px; }
      .fc.col .lb, .fc.rowc .lb { font-size:18px; padding:2px 8px; left:8px; bottom:8px; }
      .trw { position:absolute; left:0; top:0; width:1080px; height:1920px; mix-blend-mode:screen; pointer-events:none; opacity:.8; }
      .fc .lg { position:absolute; left:19%; top:19%; width:62%; height:62%; }
      .fc .lgi { position:absolute; left:16%; top:16%; width:68%; height:68%; background-size:contain; background-repeat:no-repeat; background-position:center; }
      .vz { position:absolute; }
      .orbc { position:absolute; left:0; top:0; border-radius:26px; overflow:hidden; border:3px solid rgba(255,255,255,.75); box-shadow:0 24px 60px rgba(0,0,0,.5), 0 0 0 2px rgba(79,134,255,.55), 0 0 36px rgba(31,91,255,.45); background:#14151b; }
      .orbc video { position:absolute; left:0; top:0; width:100%; height:100%; object-fit:cover; }
      .pnl { background-image:url(assets/broll/hub.png); background-size:cover; background-position:center; border-radius:18px; border:2px solid rgba(255,255,255,.55); box-shadow:0 0 0 2px rgba(79,134,255,.85), 0 0 44px rgba(31,91,255,.85), 0 24px 50px rgba(0,0,0,.5); }
      .pnl.gh { box-shadow:0 0 34px rgba(31,91,255,.75); border-color:rgba(120,160,255,.6); }
      .gbn { font-family:"Archivo Black",sans-serif; font-size:44px; color:#fff; text-shadow:0 4px 0 rgba(12,12,16,.88), 0 0 18px rgba(255,106,26,.5); white-space:nowrap; }
      .zz { font-family:"Archivo Black",sans-serif; font-size:46px; color:#fff; text-shadow:0 4px 0 rgba(12,12,16,.85); }
      .okb { width:60px; height:60px; border-radius:50%; background:#22b45a; color:#fff; font-weight:800; font-size:40px; line-height:58px; text-align:center; box-shadow:0 8px 20px rgba(0,0,0,.4); }
      .srch { background:#fff; border-radius:29px; box-shadow:0 14px 34px rgba(0,0,0,.4); display:flex; align-items:center; padding:0 20px; gap:12px; }
      .stx { font-family:"Poppins",sans-serif; font-weight:600; font-size:26px; color:#1f2330; display:inline-flex; }
      .stx i { font-style:normal; opacity:0; }
      .car { display:block; width:3px; height:30px; background:#1f5bff; margin-left:-8px; opacity:0; }
      .ccard { background:rgba(255,255,255,.97); border-radius:26px; box-shadow:0 18px 44px rgba(0,0,0,.45); padding:0 20px; display:flex; align-items:center; gap:18px; }
      .clg { width:84px; height:84px; flex:none; background:#D97757; -webkit-mask:url(assets/logos/claude.svg) center/contain no-repeat; mask:url(assets/logos/claude.svg) center/contain no-repeat; }
      .ctx { flex:1; }
      .cnm { font-family:"Poppins",sans-serif; font-weight:800; font-size:34px; color:#1f2330; line-height:1.1; }
      .cds { font-family:"Poppins",sans-serif; font-weight:600; font-size:20px; color:#6a6e79; }
      .cbtn { position:relative; background:#ff6a1a; color:#fff; font-family:"Poppins",sans-serif; font-weight:800; font-size:26px; padding:12px 24px; border-radius:16px; min-width:118px; text-align:center; }
      .cbtn .b2 { position:absolute; left:0; right:0; top:12px; opacity:0; font-size:30px; }
      .fch { width:44px; height:58px; background:#fff; border-radius:7px; box-shadow:0 4px 12px rgba(0,0,0,.35); opacity:0; }
      .fch i { position:absolute; left:15px; top:19px; width:0; height:0; border-left:16px solid #ff6a1a; border-top:10px solid transparent; border-bottom:10px solid transparent; }
      .orb { width:120px; height:120px; border-radius:50%; background:radial-gradient(circle at 35% 30%, #7fa6ff, #1f5bff 55%, #0b2a8a); box-shadow:0 0 40px rgba(31,91,255,.8), inset 0 0 20px rgba(255,255,255,.4); display:flex; align-items:center; justify-content:center; }
      .orb span { font-family:"Archivo Black",sans-serif; font-size:44px; color:#fff; }
      .ring { width:120px; height:120px; border-radius:50%; border:4px solid #4f86ff; }
      .fg { width:36px; height:52px; }
      .fg .hd { position:absolute; left:10px; top:0; width:16px; height:16px; border-radius:50%; background:currentColor; }
      .fg .bd { position:absolute; left:3px; top:19px; width:30px; height:33px; border-radius:15px 15px 4px 4px; background:currentColor; }
      .brw { position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:hidden; opacity:0; }
      .bri { position:absolute; left:0; top:0; width:1080px; height:1920px; background-size:cover; background-position:50% 50%; }
      .clipcol { position:absolute; overflow:hidden; -webkit-mask-image:linear-gradient(to bottom, transparent 0, #000 10%, #000 90%, transparent 100%); mask-image:linear-gradient(to bottom, transparent 0, #000 10%, #000 90%, transparent 100%); }
      .fc.rm { background:repeating-conic-gradient(#d9dce3 0% 25%, #f4f5f8 0% 50%) 0 0 / 28px 28px; }
      .fc.rm .th { background-size:contain; background-repeat:no-repeat; background-position:50% 100%; }
      .fc .cap2 { position:absolute; left:10px; right:10px; bottom:58px; text-align:center; font-weight:800; font-size:20px; color:#fff; background:rgba(12,12,16,.78); border-radius:8px; padding:5px 8px; }
      .fc.gr .bigw { position:absolute; left:0; right:0; top:60px; text-align:center; font-family:"Archivo Black",sans-serif; font-size:50px; line-height:1; }
      .fc.gr { background:linear-gradient(160deg,#20222c,#0f1015); }
      .fc .cr { position:absolute; inset:36px 24px 78px 24px; border:3px solid rgba(255,255,255,.9); border-radius:10px; }
""".replace("__ACCENT__", ACC)

# ---------------------------------------------------------------- BEATS
# kick: [(word, t)]; big: (TEXT, t); fronts: [dict(text,t,size,dx,dy)]; zone 'low' = close-up shots (no head)
def bsize(text):  # max width ~820 px for Archivo Black caps
    return int(min(245, 820 / (0.8 * len(text))))
B = [
 dict(zone="low", kick=[("Siapa",.10),("yang",.39),("dah",.65),("biasa",.87)], fronts=[dict(text="shoot",t=1.23,size=100),dict(text="inilah perasaan dia.",t=2.13,size=44,dy=275)], sweep=2.3, out=3.15),
 dict(zone="low", kick=[("Banyak",3.24)], fronts=[dict(text="footage",t=3.68,size=100),dict(text="macam ni,",t=4.21,size=44,dy=275)], sweep=4.3, out=4.95),
 dict(kick=[("shoot",6.48),("video",6.84),("guna",7.20)], big=("DJI",7.48), spark=7.7, flayer=True, out=8.15),
 dict(kick=[("kadang-kadang",8.21),("memang",8.90)], big=("BERAT",9.23), fronts=[dict(text="bergiga-giga",t=9.61,size=84)], sweep=9.75, out=10.12),
 dict(kick=[("susun",10.40),("transfer",11.06),("editing",13.33)], big=("GILA",14.52), flayer=True, fronts=[dict(text="dah berat",t=14.04,size=70)], out=14.72),
 dict(kick=[("dah",15.52),("tak",15.69),("pakai",15.92)], big=("CAPCUT",16.14), spark=16.35, out=16.62),
 dict(kick=[("Adobe",16.68)], big=("PREMIERE",16.93), out=17.98),
 dict(kick=[("DaVinci",18.08),("Final",18.66),("Cut",18.99),("Pro",19.20)], big=("TOLAK",19.83), fronts=[dict(text="uninstall.",t=20.54,size=100)], sweep=20.7, out=21.3),
 dict(kick=[("Pergi",21.40),("dekat",21.80),("Google",22.20),("cari",22.85)], big=("CLAUDE",23.17), out=23.88),
 dict(kick=[("install",23.91),("sekarang",24.31)], big=("INSTALL",24.31), out=24.72),
 dict(kick=[("dalam",24.77),("laptop",25.05),("ataupun",25.39),("komputer",25.78)], big=("KOMPUTER",25.78), out=26.5),
 dict(kick=[("Nak",26.80),("guna",26.97),("handphone",27.19)], big=("IPAD",27.92), flayer=True, fronts=[dict(text="tak ada masalah",t=28.24,size=70)], sweep=28.4, out=29.75),
 dict(kick=[("terus",30.98),("masukkan",31.26),("dalam",31.70)], big=("FOLDER",32.20), flayer=True, fronts=[dict(text="satu",t=31.98,size=90)], out=32.75),
 dict(kick=[("satu",33.91),("skill",34.16),("editing",34.47)], big=("SKILL",34.16), out=36.1),
 dict(kick=[("masukkan",36.49),("semua",37.03)], big=("LIMA",37.37), fronts=[dict(text="video",t=37.95,size=90)], sweep=38.1, out=38.55),
 dict(kick=[("untuk",38.53)], big=("AI",38.83), fronts=[dict(text="edit kan.",t=38.97,size=90)], sweep=39.15, out=39.66),
 dict(kick=[("tutup",40.52),("laptop",40.83),("tutup",41.30),("handphone",41.60)], big=("TIDUR",42.31), flayer=True, fronts=[dict(text="dah siap.",t=43.52,size=100)], sweep=43.7, out=44.02),
 dict(kick=[("level",44.22),("editing",44.52)], big=("EDITING",44.94), fronts=[dict(text="macam ni.",t=46.20,size=96)], sweep=46.4, spark=46.5, out=46.82),
 dict(kick=[("sangat-sangat",47.24)], big=("POWERFUL",48.10), out=48.84),
 dict(kick=[("nak",48.85),("buat",49.0)], big=("MOTION",49.11), out=49.72),
 dict(kick=[("nak",49.76),("buat",50.02)], big=("ZOOM",50.37), fronts=[dict(text="in, out",t=50.72,size=84)], sweep=50.9, out=51.62),
 dict(kick=[("nak",51.69)], big=("REMOVE",51.72), fronts=[dict(text="background.",t=52.04,size=84)], sweep=52.2, out=52.58),
 dict(kick=[("Segala",52.60)], big=("SUBTITLE",52.99), fronts=[dict(text="Claude AI.",t=55.23,size=96)], sweep=55.4, out=55.92),
 dict(kick=[("belum",56.87),("ada",57.25),("dalam diri",57.47)], big=("BELAJAR",58.49), fronts=[dict(text="sekarang.",t=58.81,size=96)], sweep=59.0, out=59.32),
 dict(kick=[("orang",59.67),("lain",59.95),("lagi",60.17)], big=("STAND",60.40), fronts=[dict(text="lagi susah nak compete.",t=60.95,size=44)], sweep=61.1, out=62.0),
 dict(kick=[("Join",62.20),("panduan",62.59)], big=("VGC",63.07), spark=63.3, out=63.30),
 dict(kick=[("video",63.32),("guna",63.68)], big=("CODE",63.99), out=64.4),
]

BR = [dict(id="br1", src="assets/broll/br1.jpg", start=10.2, end=12.62, tr="circle", at="50% 62%"),
      dict(id="br2", src="assets/broll/br2.jpg", start=12.66, end=14.70, tr="up"),
      dict(id="br4", src="assets/broll/br4.jpg", start=26.8, end=29.75, tr="circle", at="82% 78%"),
      dict(id="br3", src="assets/broll/br3.jpg", start=29.8, end=32.8, tr="left"),
      dict(id="br5", src="assets/broll/br5.jpg", start=40.2, end=44.02, tr="fade")]
TR = [("trA", "assets/trans/t19.mp4", 9.75, 1.16), ("trB", "assets/trans/t6.mp4", 14.25, 1.08)]
TRHTML = "".join('<div id="%s" class="trw"><video id="%sv" class="clip" src="%s" data-start="%s" data-duration="%s" data-track-index="%d" muted playsinline style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover"></video></div>' % (i, i, src, st, du, 30 + n) for n, (i, src, st, du) in enumerate(TR))
# ---------------------------------------------------------------- GRIDS
# cards: dict(kind,label,..., w,h) ; marks = [(t, cardIndex)] for x-stamps
def card(kind, label=None, **k): return dict(kind=kind, label=label, **k)
G = [
 dict(id="gb", mode="dock", start=14.8, end=21.4, drop=14.9, cards=[
     card("logo", None, svg="assets/logos/capcut.svg", bg="#0c0c10", fg="#ffffff"),
     card("logo", None, full="assets/logos/premiere.svg", bg="transparent"),
     card("logo", None, svg="assets/logos/davinci.svg", bg="#233a51", fg="#ffffff"),
     card("logo", None, full="assets/logos/fcp.png", bg="transparent")], marks=[(16.55, 0), (17.45, 1), (18.55, 2), (19.65, 3)]),
 dict(id="gc", mode="column", start=33.0, end=39.62, drop=33.1, cards=[card("video", "VIDEO %d" % n, src="assets/broll/ad%d.mp4" % n) for n in (1, 2, 3, 4, 5)]),
 dict(id="gd", start=49.0, end=55.95, drop=49.1, cards=[card("gr", "MOTION", word="Aa"), card("zoom", "ZOOM", src="assets/broll/v41.jpg"), card("rm", "REMOVE", src="assets/broll/rm.png"), card("cap", "SUBTITLE", src="assets/broll/v33.jpg", text="Segala subtitle ni")]),
]

# ---------------------------------------------------------------- BUILD
back, front, js, grids_html, audio = [], [], [], [], []

def add_js(s): js.append(s)

for i, b in enumerate(B):
    zone_low = b.get("zone") == "low"
    kick = [(w, snap(t)) for w, t in b["kick"]]
    out_ids = []
    if not b.get("skipkick"):
        if zone_low or b.get("flayer"):
            spans = "".join('<span class="sm" data-layout-allow-overlap data-layout-allow-occlusion id="k%d_%d" style="font-size:29px">%s</span>' % (i, j, w) for j, (w, t) in enumerate(kick))
            front.append('<div class="row" id="kr%d" style="top:%spx">%s</div>' % (i, u_front(800 if zone_low else 360), spans))
        elif len(kick) < 2:
            for j, (w, t) in enumerate(kick):
                back.append('<span class="sm" data-layout-allow-overlap data-layout-allow-occlusion id="k%d_%d" style="left:%dpx;top:%spx">%s</span>' % (i, j, 150 + 142 * j, round(u_back(max(168, HEAD_TOP - 200)) + 20 * j, 1), w))
        else:
            spans = "".join('<span class="sm" data-layout-allow-overlap data-layout-allow-occlusion id="k%d_%d">%s</span>' % (i, j, w) for j, (w, t) in enumerate(kick))
            back.append('<div class="row" id="kr%d" style="top:%spx">%s</div>' % (i, u_back(max(168, HEAD_TOP - 200)), spans))
        for j, (w, t) in enumerate(kick):
            add_js('smIn("#k%d_%d", %s);' % (i, j, t)); out_ids.append("#k%d_%d" % (i, j))
    if b.get("big") and not b.get("nobig"):
        text, t = b["big"]; t = snap(t) - 0.02
        size_u = round(bsize(text) / SB)
        if b.get("flayer"):
            front.append('<div class="big" id="b%d" style="top:%spx;font-size:%spx"><div class="ds"><span class="gt">%s</span></div></div>' % (i, u_front(520), round(bsize(text) / SF), text))
        else:
            back.append('<div class="big" id="b%d" style="top:%spx;font-size:%spx"><div class="ds"><span class="gt">%s</span></div></div>' % (i, u_back(HEAD_TOP - (150 if len(text) <= 4 else 125)), size_u, text))
        add_js('bigIn("#b%d", %s);' % (i, round(t, 2)))
        add_js('tl.to("#b%d", { scale: 1.05, duration: 0.5, ease: "sine.inOut", immediateRender: false }, %s);' % (i, round(t + 0.2, 2)))
        out_ids.append("#b%d" % i)
        if b.get("spark") is not None:
            back.append('<div class="spark" id="s%d" style="left:452px;top:%spx"></div>' % (i, u_back(HEAD_TOP - 88)))
            add_js('f("#s%d", { opacity: 0, scale: 0, rotation: 0 }, { opacity: 1, scale: 1, rotation: 90, duration: 0.4, ease: "back.out(2)" }, %s);' % (i, b["spark"]))
            out_ids.append("#s%d" % i)
    fs = None
    for j, fw in enumerate(b.get("fronts", [])):
        size = fw.get("size", 96); fs = size
        base_px = 940 if zone_low else CHIN + 80
        top = round(u_front(base_px) + u_front(fw.get("dy", 0)), 1)
        front.append('<div class="ser" id="f%d_%d" style="left:%spx;top:%spx;font-size:%spx">%s</div>' % (i, j, u_front(fw.get("dx", 0)), top, size, fw["text"]))
        add_js('frIn("#f%d_%d", %s);' % (i, j, snap(fw["t"]))); out_ids.append("#f%d_%d" % (i, j))
        last_top = top
    if b.get("sweep") is not None and b.get("fronts"):
        base_px = 940 if zone_low else CHIN + 80
        sw = 360
        front.append('<div class="sweep" id="w%d" style="left:%spx;top:%spx;width:%dpx"></div>' % (i, round(279 - sw / 2, 1), round(u_front(base_px) + 1.4 * max(f.get("size", 96) for f in b["fronts"][:1]) + (u_front(b["fronts"][-1].get("dy", 0)) if zone_low else 0), 1), sw))
        add_js('sweepIn("#w%d", %s);' % (i, b["sweep"])); out_ids.append("#w%d" % i)
    if b.get("out") is not None:
        add_js('out(%s, %s);' % (json.dumps(out_ids), b["out"]))

# validate hand-offs: a beat must be gone before the next one starts
prev = None
for i, b in enumerate(B):
    starts = ([] if b.get("skipkick") else [t for _, t in b["kick"]]) + ([b["big"][1]] if b.get("big") and not b.get("nobig") else []) + [f["t"] for f in b.get("fronts", [])]
    st = min(starts)
    if prev is not None and prev[1] is not None and prev[1] > st + 0.05:
        print("OVERLAP beat %d out %.2f > beat %d start %.2f" % (prev[0], prev[1], i, st))
    prev = (i, b.get("out"))
# grids: five DIFFERENT compositions (break pattern): pair / fan / column / row / cascade
sfx = []
FINAL_TOP = u_front(CHIN + 356)
DEF = {"row": (100, 182), "pair": (190, 320), "fan": (150, 270), "dock": (96, 96), "column": (110, 196), "cascade": (190, 250), "grid2": (130, 178)}
for g in G:
    mode = g.get("mode", "row"); n = len(g["cards"]); dw, dh = DEF[mode]
    parts = []; angs = {"fan": [-27, -9, 9, 27], "pair": [14, -14], "cascade": [-5, -2, 1, 4]}.get(mode, [])
    for ci, c in enumerate(g["cards"], 1):
        cid = "%s_%d" % (g["id"], ci); k = c["kind"]; lab = c.get("label")
        cw, ch = c.get("w", dw), c.get("h", dh)
        lb = '<span class="lb" data-layout-allow-overlap data-layout-allow-occlusion>%s</span>' % lab if lab else ""
        t_in = round(g["start"] + 0.1 + (ci - 1) * (0.2 if mode in ("cascade", "column") else 0.15), 2)
        if k == "video":
            inner = '<video id="%s_v" class="clip" src="%s" data-start="%s" data-duration="%s" data-track-index="%d" muted playsinline></video>%s' % (cid, c["src"], t_in, round(min(g["end"] - t_in, 9.6), 2), 20 + ci, lb)
        elif k == "tele":
            inner = '<video id="%s_v" class="clip" src="%s" data-start="%s" data-duration="%s" data-track-index="%d" muted playsinline></video>' % (cid, c["src"], t_in, round(min(g["end"] - t_in, 8.4), 2), 20 + ci)
        elif k == "img":
            inner = '<div class="th" style="background-image:url(%s);background-size:cover;background-position:50%% 20%%"></div>%s' % (c["src"], lb)
        elif k == "logo":
            if c.get("full"):
                inner = '<div class="lgf" style="background-image:url(%s)"></div>' % c["full"]
            elif c.get("svg"):
                inner = '<div class="lg" style="-webkit-mask:url(%s) center/contain no-repeat;mask:url(%s) center/contain no-repeat;background:%s"></div>' % (c["svg"], c["svg"], c["fg"])
            else:
                inner = '<div class="lgi" style="background-image:url(%s)"></div>' % c["ico"]
        elif k == "txt":
            inner = '<div class="nm" data-layout-allow-overlap data-layout-allow-occlusion>%s</div><div class="xm" id="%s_x" data-layout-allow-overlap data-layout-allow-occlusion>&#10005;</div>' % (c["name"], cid)
        elif k == "gr":
            inner = '<div class="bigw"><div class="ds" style="display:inline-block"><span class="gt">%s</span></div></div>%s' % (c["word"], lb)
        elif k == "zoom":
            inner = '<div class="th" style="background-image:url(%s);background-size:360%% auto;background-position:38%% 14%%"></div><div class="cr"></div>%s' % (c["src"], lb)
        elif k == "rm":
            inner = '<div class="th" style="background-image:url(%s)"></div>%s' % (c["src"], lb)
        elif k == "cap":
            inner = '<div class="th" style="background-image:url(%s);background-size:cover;background-position:50%% 20%%"></div><div class="cap2">%s</div>%s' % (c["src"], c["text"], lb)
        mk = [m for m in g.get("marks", []) if m[1] == ci - 1]
        if mk and k != "txt":
            inner += '<div class="xm" id="%s_x" data-layout-allow-overlap data-layout-allow-occlusion>&#10005;</div>' % cid
        if mode == "row":
            pos = "left:%dpx;top:0px" % ((ci - 1) * (cw + 20))
        elif mode == "pair":
            pos = "left:%dpx;top:%dpx" % ([14, 330][ci - 1], [651, 690][ci - 1])
        elif mode == "fan":
            pos = "left:%dpx;top:%dpx;transform-origin:50%% 170%%" % (279 - cw // 2, 992 - ch - 6)
        elif mode == "dock":
            pos = "left:%dpx;top:%dpx" % (round(279 - (n * cw + (n - 1) * 11) / 2) + (ci - 1) * (cw + 11), round(u_front(1235)))
        elif mode == "column":
            pos = "left:0px;top:%dpx" % ((ci - 1) * (ch + 14))
        elif mode == "grid2":
            pos = "left:%dpx;top:%dpx" % (142 + ((ci - 1) % 2) * 144, round(u_front(895)) + ((ci - 1) // 2) * 192)
        else:  # cascade
            pos = "left:%dpx;top:%dpx" % (8 + (ci - 1) * 95, (n - ci) * 14)
        cls = ("fc " + {"txt": "txt", "tele": "tele", "rm": "rm", "gr": "gr", "logo": "tile"}.get(k, "") + (" col" if mode == "column" else (" rowc" if mode == "row" else ""))).strip()
        bgst = ";background:%s" % c["bg"] if k == "logo" else ""
        parts.append('<div id="%s" class="%s" style="%s;width:%dpx;height:%dpx%s">%s</div>' % (cid, cls, pos, cw, ch, bgst, inner))
        sfx.append((t_in, "bubbly", 0.14, 0.4))
        # entrance + per-mode motion
        if mode == "fan":
            add_js('f("#%s", { opacity: 0, y: 160, rotation: 0 }, { opacity: 1, y: 0, rotation: %d, duration: 0.55, ease: "back.out(1.5)" }, %s);' % (cid, angs[ci - 1], t_in))
        elif mode == "grid2":
            add_js('f("#%s", { opacity: 0, x: 330, rotation: 6 }, { opacity: 1, x: 0, rotation: 0, duration: 0.55, ease: "power3.out" }, %s);' % (cid, t_in))
        elif mode == "dock":
            add_js('f("#%s", { opacity: 0, y: 60, scale: 0.6 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, %s);' % (cid, t_in))
        elif mode == "cascade":
            add_js('gsap.set("#%s", { rotationZ: %d });' % (cid, angs[ci - 1]))
            add_js('f("#%s", { opacity: 0, x: 320 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, %s);' % (cid, t_in))
        elif mode == "column":
            add_js('f("#%s", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }, %s);' % (cid, t_in))
        elif mode == "pair":
            add_js('gsap.set("#%s", { transformPerspective: 800, rotationY: %d, rotationZ: %d });' % (cid, angs[ci - 1], -3 if ci == 1 else 3))
            add_js('f("#%s", { opacity: 0, y: 90, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.6)" }, %s);' % (cid, t_in))
            add_js('tl.to("#%s", { y: -12, duration: 0.9, ease: "sine.inOut", repeat: 3, yoyo: true, immediateRender: false }, %s);' % (cid, round(t_in + 0.6, 2)))
        else:  # row
            add_js('f("#%s", { opacity: 0, y: 70, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "power3.out" }, %s);' % (cid, t_in))
    gid = g["id"]; ex = g["end"] - 0.25
    if mode == "row":
        grids_html.append('<div id="%s" class="strip" style="top:%spx;width:%dpx">%s</div>' % (gid, round(FINAL_TOP - 88, 1), n * (dw + 20), "".join(parts)))
        slide = max(0, n * (dw + 20) - 540)
        add_js('gsap.set("#%s", { transformPerspective: 900, rotationY: -20, transformOrigin: "50%% 50%%" });' % gid)
        add_js('tl.to("#%s", { y: 88, duration: 0.4, ease: "power2.inOut" }, %s);' % (gid, g["drop"]))
        add_js('f("#%s", { x: 6 }, { x: %d, duration: %s, ease: "sine.inOut" }, %s);' % (gid, 6 - slide if slide else -60, round(g["end"] - g["start"] - 0.2, 2), g["start"] + 0.1))
    elif mode == "column":
        colh = round((1560 - 639) / SF)
        grids_html.append('<div id="%s_w" class="clipcol" style="left:34px;top:330px;width:%dpx;height:%dpx"><div id="%s" class="strip" style="left:0px;top:0px;width:%dpx">%s</div></div>' % (gid, dw, colh, gid, dw, "".join(parts)))
        add_js('gsap.set("#%s", { transformPerspective: 900, rotationY: 22, transformOrigin: "100%% 50%%" });' % gid)
        add_js('f("#%s", { y: 0 }, { y: -%d, duration: %s, ease: "sine.inOut" }, %s);' % (gid, n * (dh + 14) - colh, round(g["end"] - g["start"] - 0.5, 2), g["start"] + 0.2))
        gid = gid + "_w"
    elif mode == "cascade":
        grids_html.append('<div id="%s" class="strip" style="top:%spx;left:0px;width:556px">%s</div>' % (gid, round(u_front(1030), 1), "".join(parts)))
        add_js('f("#%s", { y: 0 }, { y: -26, duration: %s, ease: "sine.inOut" }, %s);' % (gid, round(g["end"] - g["start"] - 0.2, 2), g["start"] + 0.2))
    elif mode in ("dock", "grid2"):
        grids_html.append('<div id="%s" class="strip" style="top:0px;left:0px;width:558px;height:992px">%s</div>' % (gid, "".join(parts)))
    else:  # pair, fan: static positions inside a full-size container
        grids_html.append('<div id="%s" class="strip" style="top:0px;left:0px;width:558px;height:992px">%s</div>' % (gid, "".join(parts)))
    if g["end"] < D - 0.1:
        add_js('tl.to("#%s", { opacity: 0, duration: 0.25 }, %s);' % (gid, round(ex, 2)))
    for (tm, idx) in g.get("marks", []):
        add_js('f("#%s_%d_x", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2.4)" }, %s);' % (g["id"], idx + 1, tm))
        sfx.append((tm, "stamp", 0.5, 0.55))

# full-screen DJI B-roll (BTS): circle reveal in, quick fade out
add_js('tl.set("#djiw", { opacity: 1 }, 6.4);')
add_js('f("#djiw", { clipPath: "circle(0% at 50% 55%)" }, { clipPath: "circle(150% at 50% 55%)", duration: 0.45, ease: "power3.out" }, 6.4);')
add_js('tl.to("#djiw", { opacity: 0, duration: 0.2, ease: "power2.in" }, 8.12);')
for br in BR:
    bid = br["id"]
    if br["tr"] == "fade":
        add_js('f("#%s", { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power1.out" }, %s);' % (bid, br["start"]))
    else:
        add_js('tl.set("#%s", { opacity: 1 }, %s);' % (bid, br["start"]))
        frm = {"circle": "circle(0%% at %s)" % br.get("at", "50%% 55%%"), "up": "inset(100%% 0%% 0%% 0%%)", "left": "inset(0%% 100%% 0%% 0%%)"}[br["tr"]]
        to = {"circle": "circle(150%% at %s)" % br.get("at", "50%% 55%%"), "up": "inset(0%% 0%% 0%% 0%%)", "left": "inset(0%% 0%% 0%% 0%%)"}[br["tr"]]
        add_js('f("#%s", { clipPath: "%s" }, { clipPath: "%s", duration: 0.45, ease: "power3.out" }, %s);' % (bid, frm.replace("%%", "%"), to.replace("%%", "%"), br["start"]))
    add_js('f("#%si", { scale: 1.0 }, { scale: 1.08, duration: %s, ease: "none" }, %s);' % (bid, round(br["end"] - br["start"], 2), br["start"]))
    add_js('tl.to("#%s", { opacity: 0, duration: 0.2, ease: "power2.in" }, %s);' % (bid, round(br["end"] - 0.2, 2)))

# ---------------------------------------------------------------- ANALOGY VISUALS (2D/3D items), front layer, below the words
vis = []
def V(h): vis.append(h)
KB = '<svg viewBox="0 0 100 110" width="120" height="132"><defs><linearGradient id="kbg1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5a5e6e"/><stop offset="1" stop-color="#14151b"/></linearGradient></defs><path d="M28 40 C28 6 72 6 72 40" fill="none" stroke="url(#kbg1)" stroke-width="13" stroke-linecap="round"/><circle cx="50" cy="68" r="35" fill="url(#kbg1)"/><circle cx="37" cy="55" r="8" fill="rgba(255,255,255,.16)"/><text x="50" y="78" text-anchor="middle" font-family="Archivo Black" font-size="24" fill="#ff6a1a">GB</text></svg>'
TRASH = '<svg viewBox="0 0 100 120" width="100" height="120"><g id="tlid"><rect x="10" y="16" width="80" height="11" rx="5.5" fill="#d7dae3"/><rect x="38" y="7" width="24" height="11" rx="5" fill="#d7dae3"/></g><path d="M17 32 H83 L77 112 Q76 119 69 119 H31 Q24 119 23 112 Z" fill="#eceef4"/><rect x="36" y="44" width="6" height="62" rx="3" fill="#b4b8c6"/><rect x="47" y="44" width="6" height="62" rx="3" fill="#b4b8c6"/><rect x="58" y="44" width="6" height="62" rx="3" fill="#b4b8c6"/></svg>'
FOLDER = '<svg viewBox="0 0 120 92" width="140" height="107"><defs><linearGradient id="fgr1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb24a"/><stop offset="1" stop-color="#ff6a1a"/></linearGradient></defs><path d="M6 14 Q6 6 14 6 H44 L54 17 H106 Q114 17 114 25 V80 Q114 86 108 86 H12 Q6 86 6 80 Z" fill="#c9561a"/><path d="M6 32 Q6 26 12 26 H108 Q114 26 114 32 V80 Q114 86 108 86 H12 Q6 86 6 80 Z" fill="url(#fgr1)"/></svg>'
MOON = '<svg viewBox="0 0 100 100" width="110" height="110"><path d="M62 8 A42 42 0 1 0 92 66 A34 34 0 1 1 62 8 Z" fill="#fff1b8" stroke="rgba(255,241,184,.4)" stroke-width="2"/></svg>'
SUN = '<svg viewBox="0 0 100 100" width="110" height="110"><g id="v6r"><rect x="47" y="3" width="6" height="16" rx="3" fill="#ffc53d" transform="rotate(0 50 50)"/><rect x="47" y="3" width="6" height="16" rx="3" fill="#ffc53d" transform="rotate(30 50 50)"/><rect x="47" y="3" width="6" height="16" rx="3" fill="#ffc53d" transform="rotate(60 50 50)"/><rect x="47" y="3" width="6" height="16" rx="3" fill="#ffc53d" transform="rotate(90 50 50)"/><rect x="47" y="3" width="6" height="16" rx="3" fill="#ffc53d" transform="rotate(120 50 50)"/><rect x="47" y="3" width="6" height="16" rx="3" fill="#ffc53d" transform="rotate(150 50 50)"/><rect x="47" y="3" width="6" height="16" rx="3" fill="#ffc53d" transform="rotate(180 50 50)"/><rect x="47" y="3" width="6" height="16" rx="3" fill="#ffc53d" transform="rotate(210 50 50)"/><rect x="47" y="3" width="6" height="16" rx="3" fill="#ffc53d" transform="rotate(240 50 50)"/><rect x="47" y="3" width="6" height="16" rx="3" fill="#ffc53d" transform="rotate(270 50 50)"/><rect x="47" y="3" width="6" height="16" rx="3" fill="#ffc53d" transform="rotate(300 50 50)"/><rect x="47" y="3" width="6" height="16" rx="3" fill="#ffc53d" transform="rotate(330 50 50)"/></g><circle cx="50" cy="50" r="27" fill="#ff9d2e"/><circle cx="50" cy="50" r="27" fill="url(#sung)"/><defs><radialGradient id="sung"><stop offset="0" stop-color="#ffe27a"/><stop offset="1" stop-color="#ff6a1a"/></radialGradient></defs></svg>'
MAG = '<svg viewBox="0 0 24 24" width="30" height="30"><circle cx="10" cy="10" r="6.5" fill="none" stroke="#8a8f9e" stroke-width="2.4"/><path d="M15 15 L21 21" stroke="#8a8f9e" stroke-width="2.6" stroke-linecap="round"/></svg>'
# V1 berat, bergiga-giga: a heavy kettlebell drops and a GB counter climbs
V('<div id="v1s" class="vz" style="left:76px;top:763px;width:110px;height:16px;border-radius:50%;background:rgba(0,0,0,.4);opacity:0"></div>')
V('<div id="v1k" class="vz" style="left:70px;top:640px;width:120px;height:132px;opacity:0">' + KB + '</div>')
for i, tx in enumerate(["128 GB", "512 GB", "1 TB", "2 TB"]):
    V('<div id="v1g%d" class="vz gbn" style="left:206px;top:690px;opacity:0">%s</div>' % (i, tx))
add_js('tl.fromTo("#v1k", { opacity: 1, y: -520 }, { opacity: 1, y: 0, duration: 0.6, ease: "bounce.out", immediateRender: false }, 8.6);')
add_js('tl.set("#v1k", { opacity: 0 }, 0);')
add_js('f("#v1s", { opacity: 0, scaleX: 0.3 }, { opacity: 1, scaleX: 1, duration: 0.5, ease: "power2.out" }, 8.6);')
add_js('tl.to("#v1k", { rotation: -7, duration: 0.1, yoyo: true, repeat: 3, immediateRender: false }, 9.25);')
for i, t in enumerate([9.2, 9.45, 9.7, 9.95]):
    add_js('f("#v1g%d", { opacity: 0, y: 24, scale: 1.3 }, { opacity: 1, y: 0, scale: 1, duration: 0.16, ease: "power3.out" }, %s);' % (i, t))
    if i < 3: add_js('tl.to("#v1g%d", { opacity: 0, duration: 0.1, immediateRender: false }, %s);' % (i, round(t + 0.23, 2)))
add_js('tl.to(["#v1k", "#v1s", "#v1g3"], { opacity: 0, y: 16, duration: 0.2, immediateRender: false }, 10.0);')
# V2 tolak tepi, uninstall: the four logos fall into a bin
V('<div id="v2b" class="vz" style="left:229px;top:690px;width:100px;height:120px;opacity:0">' + TRASH + '</div>')
add_js('f("#v2b", { opacity: 0, scale: 0.6, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, 20.2);')
for i, rot in enumerate([-28, 16, -12, 30], 1):
    cx = round(279 - (4 * 96 + 33) / 2) + (i - 1) * 107 + 48
    add_js('tl.to("#gb_%d", { x: %d, y: 66, scale: 0.35, rotation: %d, opacity: 0, duration: 0.45, ease: "power2.in", immediateRender: false }, %s);' % (i, 279 - cx, rot, round(20.54 + (i - 1) * 0.1, 2)))
add_js('tl.to("#v2b", { rotation: -8, duration: 0.1, yoyo: true, repeat: 3, immediateRender: false }, 20.95);')
add_js('tl.to("#v2b", { opacity: 0, y: 20, duration: 0.25, immediateRender: false }, 21.2);')
# V3 cari Claude AI -> real Claude logo -> Install
typed = "".join('<i id="v3c%d">%s</i>' % (i, ch if ch != " " else "&nbsp;") for i, ch in enumerate("Claude AI"))
V('<div id="v3bar" class="vz srch" style="left:64px;top:662px;width:430px;height:58px;opacity:0">' + MAG + '<span class="stx">' + typed + '</span><b id="v3car" class="car"></b></div>')
V('<div id="v3card" class="vz ccard" style="left:59px;top:640px;width:440px;height:132px;opacity:0"><div class="clg"></div><div class="ctx"><div class="cnm">Claude</div><div class="cds">by Anthropic</div></div><div id="v3btn" class="cbtn"><span id="v3b1">Install</span><span id="v3b2" class="b2">&#10003;</span></div></div>')
add_js('f("#v3bar", { opacity: 0, y: 50, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.7)" }, 21.65);')
add_js('f("#v3car", { opacity: 1 }, { opacity: 0, duration: 0.18, repeat: 9, yoyo: true, ease: "steps(1)" }, 21.9);')
for i in range(9): add_js('tl.set("#v3c%d", { opacity: 1 }, %s);' % (i, round(22.85 + i * 0.08, 2)))
add_js('tl.to("#v3bar", { opacity: 0, y: -20, scale: 0.95, duration: 0.2, immediateRender: false }, 23.65);')
add_js('f("#v3card", { opacity: 0, y: 50, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.6)" }, 23.75);')
add_js('tl.to("#v3btn", { scale: 0.88, duration: 0.08, yoyo: true, repeat: 1, immediateRender: false }, 24.02);')
add_js('tl.set("#v3btn", { backgroundColor: "#22b45a" }, 24.3);')
add_js('tl.set("#v3b1", { opacity: 0 }, 24.3);')
add_js('tl.set("#v3b2", { opacity: 1 }, 24.3);')
add_js('tl.to("#v3card", { opacity: 0, y: -30, duration: 0.25, immediateRender: false }, 26.3);')
# V4 satu folder: five clips fly into a folder
for i in range(5):
    V('<div id="v4f%d" class="vz fch" style="left:257px;top:664px"><i></i></div>' % i)
V('<div id="v4d" class="vz" style="left:209px;top:640px;width:140px;height:107px;opacity:0">' + FOLDER + '</div>')
add_js('f("#v4d", { opacity: 0, scale: 0.6, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "back.out(2)" }, 29.95);')
for i, (sx, sy, rt) in enumerate([(-230, -300, -22), (-120, -360, 14), (0, -400, -8), (120, -360, 18), (230, -300, -16)]):
    t0 = round(30.1 + i * 0.3, 2)
    add_js('f("#v4f%d", { opacity: 1, x: %d, y: %d, rotation: %d, scale: 1.2 }, { opacity: 0, x: 0, y: 14, rotation: 0, scale: 0.5, duration: 0.55, ease: "power2.in" }, %s);' % (i, sx, sy, rt, t0))
    add_js('tl.set("#v4f%d", { opacity: 0 }, 0);' % i)
add_js('tl.to("#v4d", { scale: 1.08, duration: 0.12, yoyo: true, repeat: 3, immediateRender: false }, 31.7);')
add_js('tl.to("#v4d", { opacity: 0, y: 20, duration: 0.25, immediateRender: false }, 32.6);')
# V5 AI edit kan: an AI orb with expanding rings
V('<div id="v5o" class="vz orb" style="left:330px;top:610px;opacity:0"><span>AI</span></div>')
for i in range(3): V('<div id="v5r%d" class="vz ring" style="left:330px;top:610px;opacity:0"></div>' % i)
add_js('f("#v5o", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, 38.5);')
for i in range(3): add_js('tl.fromTo("#v5r%d", { opacity: 0.85, scale: 0.7 }, { opacity: 0, scale: 2.4, duration: 0.9, ease: "power2.out", immediateRender: false }, %s);' % (i, round(38.65 + i * 0.28, 2)))
add_js('tl.to("#v5o", { scale: 1.12, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }, 38.95);')
add_js('tl.to("#v5o", { opacity: 0, scale: 0.8, duration: 0.2, immediateRender: false }, 39.45);')
# V6 tidur -> esok dah siap: moon and Zs become a sunrise
V('<div id="v6m" class="vz" style="left:46px;top:430px;opacity:0">' + MOON + '</div>')
for i in range(3): V('<div id="v6z%d" class="vz zz" style="left:%dpx;top:%dpx;opacity:0">Z</div>' % (i, 150 + i * 30, 440 - i * 40))
V('<div id="v6s" class="vz" style="left:46px;top:430px;opacity:0">' + SUN + '</div>')
V('<div id="v6ok" class="vz okb" style="left:130px;top:526px;opacity:0">&#10003;</div>')
add_js('f("#v6m", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }, 41.6);')
for i, t in enumerate([42.31, 42.6, 42.9]):
    add_js('f("#v6z%d", { opacity: 0, y: 20, scale: 0.6 }, { opacity: 1, y: -34, scale: 1, duration: 0.5, ease: "power2.out" }, %s);' % (i, t))
    add_js('tl.to("#v6z%d", { opacity: 0, duration: 0.2, immediateRender: false }, %s);' % (i, round(t + 0.6, 2)))
add_js('tl.to("#v6m", { opacity: 0, y: 110, duration: 0.4, ease: "power2.in", immediateRender: false }, 43.4);')
add_js('f("#v6s", { opacity: 0, y: 110, scale: 0.7 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.8)" }, 43.45);')
add_js('f("#v6r", { rotation: 0 }, { rotation: 90, duration: 1.2, ease: "none" }, 43.45);')
add_js('f("#v6ok", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)" }, 43.71);')
add_js('tl.to(["#v6s", "#v6ok"], { opacity: 0, duration: 0.2, immediateRender: false }, 43.9);')
# V7 stand out / lagi susah nak compete: one figure rises out of a growing crowd
for i in range(9):
    V('<div id="v7a%d" class="vz fg" style="left:%dpx;top:700px;color:#aeb4c4;opacity:0"><i class="hd"></i><i class="bd"></i></div>' % (i, 40 + i * 56))
    V('<div id="v7b%d" class="vz fg" style="left:%dpx;top:752px;color:#8a90a2;opacity:0"><i class="hd"></i><i class="bd"></i></div>' % (i, 40 + i * 56))
for i in range(9): add_js('f("#v7a%d", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, %s);' % (i, round(59.75 + i * 0.04, 2)))
add_js('tl.to("#v7a4", { scale: 1.55, y: -40, color: "#ff6a1a", duration: 0.35, ease: "back.out(2)", immediateRender: false }, 60.4);')
for i in range(9): add_js('f("#v7b%d", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, %s);' % (i, round(61.0 + i * 0.05, 2)))
add_js('tl.to([%s], { opacity: 0, duration: 0.2, immediateRender: false }, 61.9);' % ", ".join('"#v7%s%d"' % (r, i) for r in "ab" for i in range(9)))

V('<div id="v8glow" class="vz" style="left:44px;top:430px;width:470px;height:390px;opacity:0;background:radial-gradient(ellipse at 50% 55%, rgba(31,91,255,.62), rgba(31,91,255,0) 66%)"></div>')
for gi in range(3): V('<div id="v8g%d" class="vz pnl gh" style="left:114px;top:470px;width:330px;height:244px;opacity:0"></div>' % gi)
V('<div id="v8m" class="vz pnl" style="left:114px;top:470px;width:330px;height:244px;opacity:0"></div>')
add_js('f("#v8glow", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power2.out" }, 62.3);')
add_js('tl.to("#v8glow", { opacity: 0, duration: 0.25, immediateRender: false }, 64.05);')
for sel in ["#v8g0", "#v8g1", "#v8g2", "#v8m"]:
    add_js('gsap.set("%s", { transformPerspective: 1000, rotationY: -18, rotationX: 8 });' % sel)
for gi, sel in enumerate(["#v8g2", "#v8g1", "#v8g0"]):
    d = 0.07 * (3 - gi)
    add_js('f("%s", { opacity: 0, x: 420, y: 160, rotationY: -55, scale: 0.8 }, { opacity: %s, x: %d, y: %d, rotationY: -18, scale: 1, duration: 0.7, ease: "power3.out" }, %s);' % (sel, round(0.34 - 0.09 * gi, 2), -22 * (3 - gi), 10 * (3 - gi), round(62.35 + d * -1 + 0.21 - 0.0, 2)))
    add_js('tl.to("%s", { opacity: 0, duration: 0.3, immediateRender: false }, 63.15);' % sel)
add_js('f("#v8m", { opacity: 0, x: 420, y: 160, rotationY: -55, scale: 0.8 }, { opacity: 1, x: 0, y: 0, rotationY: -18, scale: 1, duration: 0.7, ease: "power3.out" }, 62.35);')
add_js('tl.to("#v8m", { y: -14, rotationY: -12, duration: 0.8, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false }, 63.1);')
add_js('tl.to("#v8m", { opacity: 0, x: -50, y: 30, scale: 0.92, duration: 0.25, immediateRender: false }, 64.1);')
# V9 hasil pelajar: whole scene blurs, title, then four Telegram results enter one by one, almost full-screen with margin
FT0 = 64.3
TC = [(562, 762), (562, 858), (562, 858), (564, 826)]
CT = [64.78, 65.92, 67.06, 68.2]
cards_h = []
for i, (cw, ch) in enumerate(TC):
    H = min(1100, 860 * ch / cw); W = H * cw / ch
    cards_h.append('<div id="fc%d" class="fcard" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;opacity:0"><video id="fc%dv" class="clip" src="assets/tele/h%d.mp4" data-start="%s" data-duration="%s" data-track-index="%d" muted playsinline></video></div>' % (i, round(540 - W / 2), 480, round(W), round(H), i, i + 1, CT[i] - 0.05, round(D - CT[i] + 0.05, 2), 40 + i))
ORBB = []
ORBF = ['<div id="finblur" style="position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;backdrop-filter:blur(38px);-webkit-backdrop-filter:blur(38px)"></div>',
        '<div id="fk" class="fkick" style="opacity:0">Result &amp;</div>',
        '<div id="fbg" class="fbig" style="opacity:0"><span>FEEDBACK</span></div>',
        '<div id="fsr" class="fser" style="opacity:0">student</div>'] + cards_h
css += """
      .fcard { position:absolute; border-radius:30px; overflow:hidden; border:3px solid rgba(255,255,255,.8); box-shadow:0 28px 70px rgba(0,0,0,.45), 0 0 0 2px rgba(79,134,255,.5), 0 0 40px rgba(31,91,255,.35); background:#fff; }
      .fcard video { position:absolute; left:0; top:0; width:100%; height:100%; object-fit:cover; }
      .fkick { position:absolute; left:0; top:178px; width:1080px; text-align:center; font-family:"Poppins",sans-serif; font-weight:800; font-size:54px; color:#fff; text-shadow:0 3px 0 rgba(12,12,16,.92), 0 0 14px rgba(12,12,16,.45); }
      .fbig { position:absolute; left:0; top:226px; width:1080px; text-align:center; filter:drop-shadow(0 8px 12px rgba(12,12,16,.5)); }
      .fbig span { font-family:"Archivo Black",sans-serif; font-size:132px; line-height:1.05; background:linear-gradient(to bottom,#ffb78a,#ff6a1a,#e23d00); -webkit-background-clip:text; background-clip:text; color:transparent; }
      .fser { position:absolute; left:0; top:372px; width:1080px; text-align:center; font-family:"Playfair Display",serif; font-style:italic; font-weight:700; font-size:70px; color:#fff; text-shadow:0 5px 0 rgba(12,12,16,.88), 0 0 26px rgba(255,255,255,.32); }
"""
add_js('tl.fromTo("#finblur", { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "sine.inOut", immediateRender: false }, %s);' % FT0)
add_js('smIn("#fk", 64.58); bigIn("#fbg", 64.66); frIn("#fsr", 64.95);')
add_js('gsap.set(".fcard", { transformPerspective: 1600, transformOrigin: "50% 50%" });')
for i, t in enumerate(CT):
    sel = "#fc%d" % i
    add_js('tl.fromTo("%s", { opacity: 0, x: 980, rotationY: -22, scale: 0.94 }, { opacity: 1, x: 0, rotationY: 0, scale: 1, duration: 0.55, ease: "power3.out", immediateRender: false }, %s);' % (sel, t))
    add_js('tl.to("%s", { scale: 1.025, duration: %s, ease: "sine.inOut", immediateRender: false }, %s);' % (sel, round(1.2 if i < 3 else D - t - 0.55, 2), t + 0.55))
    if i > 0:
        add_js('tl.to("#fc%d", { opacity: 0, x: -90, scale: 0.94, duration: 0.35, ease: "power2.in", immediateRender: false }, %s);' % (i - 1, t + 0.15))
    sfx.append((round(t, 2), "bubbly", 0.14, 0.4))
# reframe + glides
add_js('f("#rf1, #rf2", { scale: 1 }, { scale: 1.15, duration: 1.5, ease: "power2.inOut" }, 5.5);')
glides = [(7, 1.04), (12, 1.0), (18, 1.05), (25, 1.0), (32, 1.05), (40, 1.0), (45, 1.06), (53, 1.0), (60, 1.04)]
for j, (t, s) in enumerate(glides):
    dur = (glides[j + 1][0] - t) if j + 1 < len(glides) else 8.0
    if j == 0: add_js('f("#zw1, #zw2", { scale: 1 }, { scale: %s, duration: %s, ease: "sine.inOut" }, %s);' % (s, dur - 0.1, t))
    else: add_js('tl.to("#zw1, #zw2", { scale: %s, duration: %s, ease: "sine.inOut" }, %s);' % (s, dur - 0.1, t))

# ---------------------------------------------------------------- AUDIO
ME = 11.79   # video time when the track starts: its first HIT (media 3.0 s) lands on 14.79 s, its DROP (media 32.25 s) on 44.04 s
audio.append('<audio id="m1" src="assets/music/track.mp3" data-start="%s" data-duration="3.0" data-media-start="0" data-track-index="5" data-volume="0.35" data-fade-in="0.8" data-fade-out="0.08"></audio>' % ME)
audio.append('<audio id="m2" src="assets/music/track.mp3" data-start="%s" data-duration="19.2" data-media-start="2.9" data-track-index="5" data-volume="0.11" data-fade-in="0.08" data-fade-out="0.15"></audio>' % round(ME + 2.9, 2))
audio.append('<audio id="m3" src="assets/music/track.mp3" data-start="%s" data-duration="10.2" data-media-start="22.0" data-track-index="5" data-volume="0.30" data-fade-in="0.15" data-fade-out="0.05"></audio>' % round(ME + 22.0, 2))
audio.append('<audio id="m4" src="assets/music/track.mp3" data-start="%s" data-duration="%s" data-media-start="32.15" data-track-index="5" data-volume="0.095" data-fade-in="0.03" data-fade-out="0.6"></audio>' % (round(ME + 32.15, 2), round(D - (ME + 32.15), 2)))
spots = [
 (1.23, "lowhit", 2.0, 0.40), (3.68, "shutter", 0.75, 0.50), (12.2, "riser_long", 3.2, 0.50), (14.70, "boom", 2.4, 0.75),
 (9.2, "lowhit", 1.5, 0.45), (20.9, "stamp", 0.5, 0.45), (20.54, "lowhit", 1.6, 0.30),
 (22.85, "key", 0.14, 0.4), (23.0, "key", 0.14, 0.4), (23.15, "key", 0.14, 0.4), (23.3, "key", 0.14, 0.4), (23.45, "key", 0.14, 0.4), (23.6, "key", 0.14, 0.4), (24.02, "click", 0.2, 0.6),
 (30.3, "bubbly", 0.14, 0.4), (30.6, "bubbly", 0.14, 0.4), (30.9, "bubbly", 0.14, 0.4), (31.2, "bubbly", 0.14, 0.4), (31.5, "bubbly", 0.14, 0.4), (38.55, "glass", 0.6, 0.5),
 (43.71, "success", 1.2, 0.40), (58.81, "lowhit", 1.5, 0.45), (60.4, "glass", 0.6, 0.5),
 (41.14, "riser_short", 2.9, 0.45), (44.04, "boom", 2.4, 0.65), (62.35, "boom", 1.6, 0.35), (6.4, "glass", 0.6, 0.55), (10.2, "shutter", 0.75, 0.5), (12.66, "click", 0.2, 0.6), (26.8, "glass", 0.6, 0.5), (29.8, "click", 0.2, 0.6), (40.2, "open14", 1.2, 0.4),
]
spots = [s for s in spots if s[3] > 0] + sfx
for n, (t, name, dur, vol) in enumerate(sorted(spots)):
    audio.append('<audio id="a%d" src="assets/sfx/%s.mp3" data-start="%s" data-duration="%s" data-track-index="%d" data-volume="%s"></audio>' % (n, name, round(t, 2), dur, 6 + n % 4, vol))

HELP = """
      const tl = gsap.timeline({ paused: true });
      const f = (s, a, b, t) => tl.fromTo(s, a, b, t);
      const smIn = (s, t) => f(s, { opacity: 0, y: 18, scale: 1.15, filter: "blur(10px)" }, { opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 0.22, ease: "power3.out" }, t);
      const bigIn = (s, t) => f(s, { opacity: 0, scale: 1.5, y: -14, filter: "blur(16px)" }, { opacity: 1, scale: 1, y: 0, filter: "blur(0px)", duration: 0.3, ease: "power4.out" }, t);
      const frIn = (s, t) => f(s, { opacity: 0, y: 34, rotation: -3, filter: "blur(12px)" }, { opacity: 1, y: 0, rotation: 0, filter: "blur(0px)", duration: 0.3, ease: "power3.out" }, t);
      const sweepIn = (s, t) => f(s, { opacity: 1, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.32, ease: "power3.out" }, t);
      const out = (sels, t) => tl.to(sels, { opacity: 0, y: -12, filter: "blur(8px)", duration: 0.16, ease: "power2.in", immediateRender: false }, t);
"""
html = """<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
%s
      .strip { position:absolute; left:28px; height:320px; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="%s" data-width="1080" data-height="1920">
      <div id="card">
        <div id="rf1" class="rfw"><div id="zw1" class="zoomwrap"><video id="v1" class="clip vid" src="assets/raw.mov" data-start="0" data-duration="%s" data-track-index="1" data-has-audio="true" playsinline></video></div></div>
        <div class="ub"><div class="layer">%s</div></div>
        %s
        <div id="rf2" class="rfw"><div id="zw2" class="zoomwrap"><video id="cut1" class="clip vid" src="assets/cut.webm" data-start="0" data-duration="%s" data-media-start="0" data-track-index="2" muted playsinline></video></div></div>
        <div id="djiw" style="position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;clip-path:circle(0%% at 50%% 55%%)"><video id="djiv" class="clip" src="assets/broll/dji_full.mp4" data-start="6.4" data-duration="1.9" data-track-index="3" muted playsinline style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover"></video></div>
        %s
        <div class="uf">%s<div class="layer">%s</div></div>
        %s
      </div>
      %s
    </div>
    <script>%s
      %s
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
""" % (css, D, D, "".join(back), "".join(ORBB), D, "".join('<div id="%s" class="brw"><div id="%si" class="bri" style="background-image:url(%s)"></div></div>' % (b["id"], b["id"], b["src"]) for b in BR) + "".join(ORBF), "".join(grids_html), "".join(vis) + "".join(front), TRHTML, "\n      ".join(audio), HELP, "\n      ".join(l for l in js if l))
open(os.path.join(HF, "index.html"), "w").write(html)
print("wrote index.html", len(html), "bytes;", len(B), "beats,", len(G), "grids,", len(audio), "audio")
