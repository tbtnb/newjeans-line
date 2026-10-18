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
w(f'- 361 个点里 **{len(moved)} 个点换了格位**，都在 Verse 2 的一句人声上（77.6–78.6 s）。另外 {361 - len(moved)} 个点和 v1 完全一样：用音频起音重新判了一遍，结果相同。')
w(f'- 点数 361 → 361：没有新增、没有删除、没有合并。0.956 s 那一点照旧去掉（引擎规定第一个点 ≥ 1.0 s），v1 已经去掉了。')
w(f'- 落在真实起音上的点（证据 ≥ 0.6，见第 3 节）：v1 {R["on_onset"]["v1 ev>=0.6"]} → v2 {R["on_onset"]["ev>=0.6"]}；证据 ≥ 0.35：{R["on_onset"]["v1 ev>=0.35"]} → {R["on_onset"]["ev>=0.35"]}。'
  '剩下的点在前奏的稳拍和几处弱拍上（第 6 节），按用户的节奏保留。')
g = R['grid']; w(f'- 网格：1/4 拍 {g["quarter"]}，1/8 反拍 {g["8th_offbeat"]}，1/16 {g["16th_e"] + g["16th_a"]}（e {g["16th_e"]} / a {g["16th_a"]}），三连音 0。最小间隔 {R["min_gap"]} s（≥ 0.105 s）。')
w('- 关卡结尾（160.637 s，音乐 1.5 s 淡出）、三个下落、10 颗钻石、2 个皇冠都没变。路线用 route_forward 重跑了（这句的点距变了），布景也随之重新生成。validate：0 错误。\n')
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
w('## 4. 改动列表（相对 faa6927）\n')
w('| 原始点 (s) | v1 | v2 | 格位 | v1 证据 | v2 证据 | 原因 |'); w('|---|---|---|---|---|---|---|')
for t in moved:
    w(f'| {t["t_raw"]:.3f} | {t["v1_t"]:.3f} | {t["t"]:.3f} | {t["pos"]} | {t["v1_ev"]} {t["v1_layer"]} | {t["ev"]} {t["layer"]} | {t["reason"]} |')
w('\n这一句是 Verse 2 的 “There ain\'t nothing else that I would hold on to”。用户点的是唱出来的音节，它们大多落在 1/16 反拍上：'
  '原始点相对歌词音节分别是 −53（ain\'t）/ −6（noth）/ −20（else）/ −41（I）/ +32（would）/ −32（on）ms。用户在全曲对人声音节的平均提前量是 −25 ms，正好对得上。'
  'v1 把它们吸到了整齐的 1/8 上，这样算出来用户在这四五个点上要比平时再早 60 ms 左右（−98 ~ −146 ms），不合理。'
  '“would” 那一点同时也有 kick（1.0）。最后一个点（78.907 拍）两版一样。\n')
w('**有疑问、请试听确认的地方**：“noth-” 放在 77.608（e，音节本身）还是 77.726（&，有 kick 和 “-ing”）。'
  '原始点（77.628）几乎正好在 “noth” 的起音上，所以选了 77.608，但这样它和前一点只隔一个 1/16（0.118 s，全曲唯一这么密的地方，判定窗口 ±53 ms）。'
  '如果想要原来的感觉，把这一点改回 77.726 就行。A/B：`deliverables/omg-ab/user-v1.mp3` 和 `user-v2.mp3`，72–87 s，差别在第 5.6–6.7 秒。\n')
w('## 5. v1 的 23 个可疑点复查\n')
w('| 原始点 | v1 标记 | v2 结果 | 格位 | 证据 | 偏差 (ms) | 判断 |'); w('|---|---|---|---|---|---|---|')
for t in T:
    if t['v1_flag']:
        if t['changed']: j = '改了，见第 4 节'
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
w(f'- 路线：route_forward 重跑（这句的点距变了）。{flips} 个点的左右转向变了（77.6 s 以后几段的左右镜像），长度和最终位置基本一样，只能往前走。'
  'artkit 按新路线重新挑了几个布景件的位置和边（手机灯牌、书页墙）。validate：0 错误。\n')
w('## 9. 试玩（box 上的脚本模拟，不是真人在手机上玩）\n')
for i, p in enumerate(plays, 1):
    s = p['summary']
    w(f'- 第 {i} 次（本地 vite 构建，SwiftShader 软件渲染约 {s["fps"]:.0f} fps）：{s["status"]}，结束于 {s["time"]} s，{s["perfect"]} perfect + {s["good"]} good / {s["taps"]}，'
      f'钻石 {s["diamonds"]}/10，输入误差均值 {s["errorMeanMs"]} ms（SD {s["errorSdMs"]}，最大 {s["errorMaxAbsMs"]} ms）')
w('- 偶尔出现的 good 是软件渲染掉帧，脚本的触摸晚到了（不是谱面的问题；那些点不在这次改动的范围内）。这次没有发布，线上 /preview/ 还是 faa6927。\n')
w('## 10. 文件\n')
w('- `tools/charts/omg_user_refine.py`：精修工具，有说明和人工复核记录 → `analysis/user/omg-user-refine.json`（逐点：偏移、候选、证据、v1/v2、原因）和 `analysis/user/omg-user-taps-refined.json`')
w('- `analysis/user/omg-user-repeats-v2.json`，`analysis/user/omg-import-report-v2.json`')
w('- `levels-src/omg/chart.json`，`levels-src/omg/layout.json`，`src/levels/omg.json`')
w('- `deliverables/omg-user-clicks-v2.mp3`（歌 + 每个点一个 click，到 160.637 s 淡出）')
w('- `deliverables/omg-ab/user-v1.mp3` / `user-v2.mp3`（72–87 s，A/B）')
(ROOT / 'deliverables/omg-user-refine-report.md').write_text('\n'.join(L) + '\n')
print('ok', len(L), 'lines')
