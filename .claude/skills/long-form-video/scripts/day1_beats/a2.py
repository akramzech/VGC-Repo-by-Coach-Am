# ================================================================== STORY ANCHORS (V2)
HD = tm['hook_dur']
# ---- hook words (inside the cold open)
h_sampai = wt('sampai', 0); h_hari = wt('hari', h_sampai); h_alasan = wt('alasan', h_hari); h_mc = wt('mc', h_alasan)
h_satu = wt('satu', h_mc); h_15 = wt('15', h_satu); h_minit = wt('minit', h_15)
# ---- compare
t_cuba = wt('cuba', HD); t_seb1 = wt('sebelah', t_cuba); t_seb2 = wt('sebelah', t_seb1 + .4); t_so_k = wt('so', t_seb2)
# ---- usage / token explainer
t_kredit = wt('kredit', HD); t_token = wt('token', t_kredit); t_adv = wt('advance', t_token); t_mesti = wt('mesti', t_adv)
t_usage = wt('usage', t_mesti); t_sama = wt('sama', t_usage); t_100 = wt('100', t_sama); t_konsep2 = wt('konsep', t_100)
t_bateri = wt('bateri', t_konsep2)
# ---- battery hero + tasks -----------------------------------------------------------
t_so_task = wt('so', t_bateri + .3); t_kompl = wt('kompleksiti', t_so_task)
t_mudah = wt('mudah', t_kompl); t_potong = wt('potongkan', t_mudah); t_sikit1 = wt('sikit', t_potong)
t_anim = wt('animation', t_sikit1); t_text = wt('text', t_anim); t_broll = wt('b', t_text)
t_efek = wt('efek', t_broll); t_banyak = wt('banyak', t_efek)
# ---- three sizes ---------------------------------------------------------------------
t_avg = wt('average', t_banyak); t_export = wt('export', t_avg); t_3 = wt('3|tiga', t_export)
t_916 = wt('9', t_3); t_169 = wt('16', wt('16', t_916 + .1) + .1); t_11 = wt('1', t_169 + .1)
t_pecah = wt('pecahkan', t_11); t_15 = wt('15', t_pecah); t_ketiga = wt('ketiga', t_15)
t_depends = wt('depends', t_ketiga); t_kompl2 = wt('kompleksiti', t_depends)
# ---- refill --------------------------------------------------------------------------
t_apa = wt('apa', t_kompl2); t_habis1 = wt('habis', t_apa); t_habis2 = wt('habis', t_habis1 + .2)
t_jangan = wt('jangan', t_habis2); t_top = wt('top', t_jangan); t_selepas = wt('selepas', t_top)
t_5jam = wt('5', t_selepas); t_after = wt('after', t_5jam); t_100b = wt('100', t_after); t_senang = wt('senang', t_100b)
# ---- modes ---------------------------------------------------------------------------
t_mode = wt('mode', t_senang); t_harian = wt('harian', t_mode); t_weekly = wt('weekly', t_harian)
t_weekly100 = wt('100', t_weekly); t_kamis = wt('kamis', t_weekly100); t_tbg = wt('boleh', t_kamis)
t_weekly_habis = wt('habis', t_tbg)
# ---- price ---------------------------------------------------------------------------
t_package = wt('package', t_weekly_habis); t_20 = wt('20', t_package); t_usd = wt('usd', t_20)
t_90 = wt('90', t_usd); t_ringgit = wt('ringgit', t_90); t_berbaloi = wt('berbaloi', t_ringgit)
# ---- team vs ai ----------------------------------------------------------------------
t_dulu = wt('dulu', wt('persoalan', t_berbaloi)); t_team = wt('team', t_dulu); t_jam1 = wt('jam', t_team)
t_heavy = wt('heavy', t_jam1); t_3jam = wt('3', t_heavy); t_hari34 = wt('hari', t_3jam + .3)
t_dengan = wt('dengan', t_hari34); t_mc = wt('mc', t_dengan); t_1520 = wt('15', t_mc); t_minit = wt('minit', t_1520)
t_sebulan = wt('sebulan', t_minit); t_100v = wt('100', t_sebulan); t_video100 = wt('video', t_100v)
t_daily = wt('daily', t_video100); t_berbaloi2 = wt('berbaloi', t_daily)
# ---- benchmark -----------------------------------------------------------------------
t_kompet = wt('kompetensi', t_berbaloi2); t_bench = wt('benchmark', t_kompet); t_dulu2 = wt('dulu', t_bench)
t_prem = wt('premiere', t_dulu2); t_after2 = wt('after', t_prem); t_capcut = wt('capcut', t_after2)
t_adapt = wt('adapt', t_capcut); t_ai = wt('ai', t_adapt); t_laju = wt('laju', t_ai)
# ---- adapt ---------------------------------------------------------------------------
t_geng = wt('geng', t_laju); t_adapt2 = wt('adapt', t_geng); t_auto = wt('automat', t_adapt2)
t_story = wt('story', t_auto); t_conv = wt('conversion', t_story); t_sendiri = wt('sendiri', t_conv)
# ---- outro (new order: pertama -> aku personally nak try -> ... -> konsisten -> anything jumpa esok)
t_episode = wt('episode', t_sendiri); t_pertama = wt('pertama', t_episode)
t_aku = wt('aku', t_pertama); t_try = wt('try', t_aku); t_vlog = wt('vlog', t_try)
t_rekod = wt('rekod', t_vlog); t_konsis = wt('konsis|consis', t_rekod); t_anything = wt('anything', t_konsis)
t_esok = wt('esok', t_anything); t_kedua = wt('kedua', t_esok)

def vclip(sid, src, t0, dur, style):
    return f'<video class="clip pv" id="{sid}" src="{src}" muted playsinline data-start="{t0:.3f}" data-duration="{dur:.3f}" data-media-start="0" data-track-index="{VT[0]}" style="{style}"></video>'
VT = [3]
def vt():
    VT[0] += 1; return VT[0]
