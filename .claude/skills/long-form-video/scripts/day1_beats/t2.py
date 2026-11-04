# ================================================================== CAPTIONS (presenter windows) ======================
grp('ramai dah start nampak', [('CLAUDE', 'y', 'cloud|claude'), ('BOLEH', 'w', 'boleh'), ('EDIT VIDEO', 'y', 'edit')], HD + .05, 1.5)
grp('sebenarnya', [('CHATGPT', 'y', 'chatgpt'), ('PUN BOLEH', 'w', 'pun')], wt('sebenarnya', HD), 1.4)
grp('gunakan code', [('SAMA JE', 'y', 'sama')], wt('gunakan', HD), 1.1)
grp('cuma hasil daripada Claude', [('LAGI BAGUS', 'y', 'bagus'), ('LAGI SMOOTH', 'y', 'smooth')], wt('cuma', HD), 1.3)
grp('saya punya social media content', [('AVERAGE', 'w', 'average'), ('VIDEO', 'y', 'video')], t_avg - .5, 1.3)
grp('sebab apa?', [('WEEKLY', 'y', 'weekly'), ('DAH HABIS', 'w', 'habis')], wt('sebab', t_tbg), 1.2)
grp('jadi mungkin pada waktu tu', [('HEAVY USE', 'y', 'heavy')], wt('mungkin', t_weekly_habis), 1.2)
grp('', [('BERBALOI', 'y', 'berbaloi'), ('KE TAK?', 'w', 'ke')], t_berbaloi - .1, 1.1)
grp('', [('MAHAL', 'y', 'mahal'), ('KE MURAH?', 'w', 'murah')], wt('mahal', t_berbaloi), 1.2)
grp('kita kena jawab satu', [('PERSOALAN', 'y', 'persoalan')], wt('persoalan', t_berbaloi), 1.2)
grp('so pada saya', [('SANGAT', 'w', 'sangat'), ('BERBALOI', 'y', 'berbaloi')], wt('so', t_daily), 1.4)
grp('video editor', [('MASIH', 'w', 'masih'), ('DIPERLUKAN', 'y', 'diperlukan')], wt('no', t_berbaloi2), 1.4)
grp('', [('NO', 'y', 'no'), ('PROBLEM', 'w', 'problem')], wt('no', t_capcut), 1.0)
grp('', [('JANGAN', 'w', 'jangan'), ('RISAU', 'y', 'risaulah')], wt('jangan', t_geng), 1.2)
grp('mungkin tu je dalam', [('EPISOD', 'w', 'episode'), ('PERTAMA', 'y', 'pertama')], wt('mungkin', t_conv), 1.5)
grp('kita rekod je, borak je', [('LEPAS TU', 'w', 'lepas'), ('CLAUDE EDIT', 'y', 'cloud|claude')], wt('lepas', t_rekod), 1.2)
grp('kita tengok', [('BOLEH', 'w', 'boleh'), ('KONSISTEN', 'y', 'konsis|consis'), ('KE?', 'w', 'ke')], wt('tengok', t_rekod), 1.7)
grp('anything', [('JUMPA', 'w', 'jumpa'), ('ESOK', 'y', 'esok')], t_anything - .1, 1.6)

# ================================================================== CAMERA ============================================
HX, HY = 950, 410
def cam_xy(S, sx=960):
    tx = min(0, max(W - S * W, sx - S * HX)); ty = min(0, max(H - S * H, 0.42 * H - S * HY)); return round(tx, 1), round(ty, 1)
blocked = [(s[0], s[1]) for s in SCENES if s[2] in ('full', 'bh')]
def in_win(t, wins, pad=0.0): return any(a - pad <= t <= b + pad for a, b in wins)
CAMK = [(h_hari - .4, 1.2, 960, .5), (h_mc - .45, 1.3, 960, .5), (h_15 - .5, 1.42, 960, .5), (HD - .5, 1.0, 960, .45)]
cyc = [1.16, 1.0, 1.28, 1.1, 1.22, 1.0]; ci = 0; last = HD; cur_S = 1.0
starts = sorted(set(round(s['s'], 2) for s in SEGS))
events = []
for t in starts:
    if t < HD + 1.2 or t > DUR - 3: continue
    if in_win(t, blocked, .9) or t - last < 4.6: continue
    S_ = cyc[ci % len(cyc)]; ci += 1
    events.append((t, S_)); last = t
for a, b in blocked:
    events.append((a - .6, 1.0))
events.sort()
cur = 1.0; planned = []
for t, S_ in events:
    if S_ == cur: continue
    if in_win(t + .5, blocked, 0) and S_ != 1.0: continue
    planned.append((t, S_, 960, .8 if S_ != 1.0 else .5)); cur = S_
CAMK += planned
CAMK.sort()
clean = []; endp = -1
for k in CAMK:
    if k[0] >= endp - 1e-6: clean.append(k); endp = k[0] + k[3]
CAMK = clean
cx, cy = cam_xy(1.1)
js(f'gsap.set("#cam",{{transformOrigin:"0 0",x:{cx},y:{cy},scale:1.1}});')
for t, S_, sx, d in CAMK:
    x_, y_ = cam_xy(S_, sx)
    js(f'tl.to("#cam",{{x:{x_},y:{y_},scale:{S_},duration:{d},ease:"sine.inOut"}},{t:.3f});')
for t, S_, sx, d in CAMK:
    if t > HD and S_ > 1.05: sfx(t, 'zoom_in', -17)
    elif t > HD and S_ <= 1.05: sfx(t, 'zoom_out', -18)
print('camera keys', len(CAMK))
emit_caps()
