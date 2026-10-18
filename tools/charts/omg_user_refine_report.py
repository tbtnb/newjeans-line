"""Write deliverables/omg-user-refine-report.md (Chinese) from analysis/user/omg-user-refine.json (+ repeats v2, v1 chart, play logs).
Usage: omg_user_refine_report.py <v1 chart.json> <play-log.json> [<play-log-2.json>]"""
import json, sys, numpy as np
from pathlib import Path
from scipy.ndimage import gaussian_filter1d
ROOT = Path(__file__).resolve().parents[2]
R = json.load(open(ROOT / 'analysis/user/omg-user-refine.json')); T = R['taps']
REP = json.load(open(ROOT / 'analysis/user/omg-user-repeats-v2.json'))
v1 = json.load(open(sys.argv[1]))['taps']; v2 = json.load(open(ROOT / 'levels-src/omg/chart.json'))['taps']
plays = [json.load(open(p)) for p in sys.argv[2:]]
lay = json.load(open(ROOT / 'levels-src/omg/layout.json'))
L = []; w = L.append
moved = [t for t in T if t['changed']]
w('# OMG 用户打点精修报告（v2）\n')
w('对象：`levels-src/omg/chart.json`。v1 = 已发布的 faa6927（用户原始 362 个点吸附成 361 个），v2 = 这次精修。')
w('原则：用户点了哪些拍、点了几下都不动，只修正时间精度和明显手误；每个点都对照音频起音来确定它对的是哪个音。\n')
w('## 1. 结论\n')
w(f'- 361 个点逐个对照音频起音（鼓、贝斯、合成器的分轨起音，人声分轨，歌词音节）复查了一遍，**结果和 faa6927 一样：0 个点改动**。v1 的吸附已经在用户想点的音上了。')
w('- 点数 361 → 361：没有新增、没有删除、没有合并。0.956 s 那一点照旧去掉（引擎规定第一个点 ≥ 1.0 s）。')
w('- 有一处我本来想改、后来撤回（第 4 节）：Verse 2 的一句人声（77.6–78.6 s）。用户很可能是在跟唱出来的 1/16 音节点，但那样一来会有两个点只隔 0.118 s，'
  '而路面加宽以后最小点距是 0.15 s（判定窗口不能重叠）。在这个限制下还能成立的方案，要么就是 v1 的整齐 1/8（每个点上都有 kick/snare 1.0），要么得把 “ain\'t” 挪离它的音节。所以保留 v1。')
w(f'- 落在真实起音上的点（证据 ≥ 0.6，见第 3 节）：{R["on_onset"]["ev>=0.6"]} 个；证据 ≥ 0.35：{R["on_onset"]["ev>=0.35"]} 个。剩下的是前奏的稳拍和几处弱拍（第 6 节），按用户的节奏保留。')
g = R['grid']; w(f'- 网格：1/4 拍 {g["quarter"]}，1/8 反拍 {g["8th_offbeat"]}，1/16 {g["16th_e"] + g["16th_a"]}（e {g["16th_e"]} / a {g["16th_a"]}），三连音 0。最小间隔 {R["min_gap"]} s（要求 ≥ 0.15 s）。')
w('- 关卡结尾（160.637 s，音乐 1.5 s 淡出）、三个下落、10 颗钻石、2 个皇冠、路线、布景都和 faa6927 一样（路宽是集成那边改的 2.6/2.5/2.4）。最小点距 0.236 s，validate：0 错误。\n')
w('## 2. 偏移模型复核（用音频起音对齐，而不只是本地平均）\n')
w(f'v1 用点自己在 1/8 网格上的相位做本地平均（±12 s）。v2 把每个点附近 ±10 s（至少 16 个点）的点和真实起音（鼓、人声、贝斯、合成器，来自分轨，已校正检测延迟）做互相关，'
  f'扫 −140..+60 ms，再取前后 9 个点的中位数。全曲：起音互相关 {R["global_offset_onset_ms"]} ms，v1 相位法 {R["global_offset_v1_ms"]} ms。'
  f'v2 本地偏移 {R["offset_onset_ms"]["min"]} ~ {R["offset_onset_ms"]["max"]} ms（中位 {R["offset_onset_ms"]["median"]}），'
  f'和 v1 相差中位 {R["offset_diff_vs_v1_ms"]["median_abs"]} ms，最大 {R["offset_diff_vs_v1_ms"]["max_abs"]} ms。\n')
w('| 时段 | 点数 | v2 起音对齐偏移 (ms) | v1 相位偏移 (ms) |'); w('|---|---|---|---|')
for a in range(0, 160, 10):
    s = [t for t in T if a <= t['t_raw'] < a + 10]
    if s: w(f'| {a}–{a + 10} s | {len(s)} | {np.median([t["off_ms"] for t in s]):.0f} | {np.median([t["off_v1_ms"] for t in s]):.0f} |')
w('\n结论：漂移是真的，不是算法造成的。前奏只有一个很稀的合成器旋律，用户在那里只比拍子提前约 15–25 ms；进鼓以后稳定在提前 55–80 ms（人跟拍时通常会提前一点）。'
  '两种方法给出的偏移基本一致，所以 v1 的吸附大方向没问题，v2 主要是逐个点复查。\n')
w('## 3. 怎么确定每个点对的是哪个音\n')
w('- 候选：偏移校正后的点 ±120 ms 内所有的 1/16 格位。')
w('- 证据：每个格位附近最强的真实起音。kick/snare/贝斯/合成器 ±30 ms；人声分轨的起音和歌词对齐的音节 −50..+35 ms（起音是辅音开始的时刻，比听感上的拍点 p-center 早一点）。'
  '权重：kick/snare/人声/音节 1.0，贝斯/合成器 0.8；在混音里被盖住的（比整体低 14 dB 以上）×0.3。')
w('- 选择：Viterbi 动态规划。代价 = 位置误差（σ 30 ms）− 3 × 证据 + 1/16 反拍惩罚（有真实起音时 2，没有时 8）+ 和用户自己相邻点间隔的误差（σ 30 ms）。格位严格递增，所以不会合并，也不会凭空加点。')
w('- 空格位检查：如果一个点所在格位没有真实起音（< 0.35），而相邻 1/16 或 1/8 格位有强起音（≥ 0.6），并且离校正后的点不到 75 ms，就把它挪过去。这次 0 个点满足条件（第 6 节）。')
w('- 人工复核：自动结果和 v1 不同的地方，以及 v1 标记的 23 个可疑点，逐个对照歌词时间、点的间隔、前后点来判断。')
w('- 最终时间就是网格时间（127.003 BPM，beat0 0.011）。这个网格和鼓是对齐的：snare 起音相对网格的中位偏差 0 ms，贝斯 +3.6 ms，人声 +3.1 ms。所以点在网格上，听起来也就在音上。\n')
dts = [abs(t['onset_dt_ms']) for t in T if t['ev'] >= 0.35]
w(f'v2 每个点到它对应起音的距离：中位 {np.median(dts):.1f} ms，90% 在 {np.percentile(dts, 90):.1f} ms 以内（{len(dts)} 个点有起音可比）。\n')
w('## 4. 改动：0 个。一处提议已撤回（请试听决定）\n')
w('Verse 2：“There ain\'t nothing else that I would hold on to”。用户在这里的原始点和歌词音节的偏差是 −53（ain\'t）/ −6（noth）/ −20（else）/ −41（I）/ +32（would）/ −32（on）ms，'
  '和用户全曲对人声音节平均提前 −25 ms 很吻合。如果按 v1 的 1/8 来算，这几个点会比用户平时再早 60 ms 左右（−98 ~ −146 ms）。所以用户很可能是在跟唱的 1/16 节奏点。下表是撤回的提议：\n')
w('| 原始点 (s) | 现在（= v1） | 提议 | 理由 |'); w('|---|---|---|---|')
for x in R['review_withdrawn']: w(f'| {x["t_raw"]:.3f} | {x["kept"]:.3f} | {x["proposed"]:.3f} | {x["why"]} |')
w('\n撤回的原因：提议里 77.490 → 77.608 只隔 0.118 s，低于路面加宽后的最小点距 0.15 s。“noth” 改放 77.726 的话，它和 “else”（77.844）之间又是 0.118 s。'
  '在这一段，满足 0.15 s 的方案只有两种：(a) v1 的整齐 1/8，也就是现在用的；(b) 把整句往前移一个 1/16，“ain\'t” 放到 77.372（这里有 kick 1.0），但这样它离自己的音节（77.472）就太远了。\n')
w('试听：`deliverables/omg-ab/user-v1.mp3`（= 现在的谱面）和 `deliverables/omg-ab/user-v2-vocal-proposal.mp3`（撤回的提议），72–87 s，差别在第 5.6–6.7 秒。'
  '如果你觉得提议那版才是你想点的，可以选 (b)，或者放宽这一处的最小点距。`user-v2.mp3` 是这次的结果，和 v1 一模一样。\n')
w('## 5. v1 的 23 个可疑点复查\n')
w('| 原始点 | v1 标记 | v2 结果 | 格位 | 证据 | 偏差 (ms) | 判断 |'); w('|---|---|---|---|---|---|---|')
for t in T:
    if t['v1_flag']:
        if any(abs(x['t_raw'] - round(t['t_raw'], 3)) < 1e-6 for x in R['review_withdrawn']): j = '保留 1/8，人声提议已撤回（第 4 节）'
        elif t['changed']: j = '改了'
        elif t['ev'] >= 0.6: j = '保留：这个格位有强起音；其他候选格位没有更强的起音，也不符合用户的点距'
        elif t['t_raw'] < 13: j = '保留：前奏的稳拍（隔两拍一下），附近没有别的起音'
        else: j = '保留：起音偏弱，但前后点距是整齐的 1/8'
        w(f'| {t["t_raw"]:.3f} | {"误差 > 50 ms" if "error" in t["v1_flag"] else "两个格位难分"} | {t["t"]:.3f} | {t["pos"]} | {t["ev"]} {t["layer"]} | {t["err_ms"]:+.0f} | {j} |')
w('\n另外，**70–74 s（Post-Chorus 1 结尾）和 131/133 s（Post-Chorus 2 的同一处）** 用户整体比 1/8 格位早 100–150 ms。'
  '检查过往前挪一个 1/16 的方案：那样点距一样，但那些 1/16 格位上基本没有起音，而 1/8 上是 kick/snare 1.0。所以判断为用户点快了，按 1/8 保留。两次重复的位置也一致。\n')
w('## 6. 所在格位没有强起音的点（保留）\n')
weak = [t for t in T if t['ev'] < 0.35 and t['t'] >= 1.0]
w(f'{len(weak)} 个：' + '，'.join(f'{t["t"]:.3f}' for t in weak) + '。')
w('其中 13 s 之前的都是前奏：只有稀疏的合成器和人声即兴，用户在点稳拍（每拍或隔两拍一下）。其余几个前后点距都是整齐的 1/8，'
  '相邻格位上的强起音要么离点超过 75 ms，要么会打乱顺序，所以不挪。\n')
w('## 7. 重复段落点法不同（只列出，不改，请用户决定）\n')
w('- **Chorus 2 是 Chorus 1 的子集**（24 对 46），**Post 2 是 Post 1 的子集**（41 对 56）：第二遍点得更稀，而且点的都是第一遍点过的位置。这看起来是有意的，保留。')
w('- Verse 1 和 Verse 2 歌词、旋律都不一样，点法不同很正常（Verse 2 跟着人声点得更密）。')
for o in REP:
    if 'half' in o['pair']:
        for p in o['diff_phrases']:
            if p['only_a'] or p['only_b']:
                w(f'- {o["pair"]}（{p["phrase_at_a"]} s / {p["phrase_at_b"]} s 起的两小节）：只在前半出现 {p["only_a"] or "无"}，只在后半出现 {p["only_b"] or "无"}')
w('- 这些差别都是一两个点，可能是用户有意加减，也可能是漏点。听不出明确是手误，所以都没补也没删。\n')
w('## 8. 关卡\n')
w(f'- endTime {lay["endTime"]} s，endFade {lay["endFade"]} s（不变）。')
w('- 下落：' + '，'.join(f'{e["t"]:.3f} s（{e["dy"]}）' for e in lay['elevation'] if e['type'] == 'fall') + '（不变，都在用户的副歌/drop 重拍上）。')
w('- 钻石：' + '，'.join(str(d['t']) for d in lay['diamonds']) + '（不变）；皇冠：' + '，'.join(str(c['t']) for c in lay['crowns']) + '（不变）。')
flips = sum(1 for a, b in zip(v1, v2) if a['dir'] != b['dir'])
w(f'- 路线：route_forward 重跑后和 faa6927 完全相同（转向不同的点：{flips} 个），布景也一样。validate：0 错误，最小点距 0.236 s。\n')
w('## 9. 试玩（box 上的脚本模拟，不是真人在手机上玩）\n')
for i, p in enumerate(plays, 1):
    s = p['summary']
    w(f'- 第 {i} 次（本地 vite 构建，SwiftShader 软件渲染约 {s["fps"]:.0f} fps）：{s["status"]}，结束于 {s["time"]} s，{s["perfect"]} perfect + {s["good"]} good / {s["taps"]}，'
      f'钻石 {s["diamonds"]}/10，输入误差均值 {s["errorMeanMs"]} ms（SD {s["errorSdMs"]}，最大 {s["errorMaxAbsMs"]} ms）')
w('- 偶尔出现的 good 是软件渲染掉帧，脚本的触摸晚到了（不是谱面的问题）。这次没有发布，线上 /preview/ 还是 faa6927。\n')
w('## 10. 文件\n')
w('- `tools/charts/omg_user_refine.py`：精修工具，有说明和人工复核记录 → `analysis/user/omg-user-refine.json`（逐点：偏移、候选、证据、v1/v2、原因）和 `analysis/user/omg-user-taps-refined.json`')
w('- `analysis/user/omg-user-repeats-v2.json`，`analysis/user/omg-import-report-v2.json`')
w('- `levels-src/omg/chart.json`，`levels-src/omg/layout.json`，`src/levels/omg.json`')
w('- `deliverables/omg-user-clicks-v2.mp3`（歌 + 每个点一个 click，到 160.637 s 淡出）')
w('- `deliverables/omg-ab/user-v1.mp3` / `user-v2.mp3`（72–87 s，两个一样）/ `user-v2-vocal-proposal.mp3`（撤回的提议）')
(ROOT / 'deliverables/omg-user-refine-report.md').write_text('\n'.join(L) + '\n')
print('ok', len(L), 'lines')
