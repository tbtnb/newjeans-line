---
name: nj-chart-design
description: newjeans-line 打点/谱面设计：用户在 /tapper/ 打点导出 → 导入、偏移校正、Viterbi 吸附、按音频起音复查 → 验证。新做或重审任何一首歌的谱（包括其余 15 首按 OMG 模板重审）、改判定窗口、出点击音轨时读。
---

# 打点（谱面）设计

## 23:04全谱时间复核（覆盖之前仅局部修正的权限范围）
- 用户现有谱已经做过网格量化，不能假装仍是未处理的原始手点；当前点型以四分/八分脉冲为主、保留用户选择的停顿和密度。卡点感还受全局掉帧影响，谱面微调不能代替性能修复。
- `omg_audio_microalign.py`重新解码同一MP3，重新检测全混起音，与已校准的分轨证据交叉确认。全混包络相关>0.999999、滞后0样本，音频SHA未变。
- 保留361点、方向、所属拍位、160.637结束；20处只改10–24ms，需强kick/snare且新全混起音在9ms内支持。47%已修规则乐句及有歧义的人声快速段保持，不盲目把整首吸到最强鼓点。
- 证据/原始基线保存在 `analysis/user/omg-timing-20261019*.json`；运行时地图转角由新chart时间重新生成，不能只改评分时间不改道路。
- 这次是信号分析验证，不是人工听感或iPhone音画同步验收；不据此声称所有用户意图已完美识别。

## 之前局部节奏修正与输入边界
- 用户说47%而非47秒。结合关卡160.637秒终点定位至75–77秒乐句。
- `7260c29` 仅将 tap索引182由76.663改至76.545秒（提前118ms），邻接间隔从约.591/.354恢复约.473/.472；保留361点、方向及结束时间。此为针对反馈的规则化处理，不能声称已获用户听感确认。
- 依据：`analysis/omg.json`、歌词/用户refine分析、相邻拍间隔。测试：`tests/omg-playability.test.ts` 的47%拍距断言。
- 音乐节奏和输入容错分开：不移动音符来掩盖碰撞问题；OMG不再用旧时间窗吸附位置，见 `nj-input-tolerance`。

## 先记住的规则（用户定的，见 nj-user-preferences B 节）
1. 每首歌一种一致的点法，全曲一套规则。
2. 人声/歌词是主层；没有人声的地方才跟鼓（再没有才跟钢琴/中频）。
3. 重复的副歌/hook 用同一套点型（镜像）。
4. 节奏逻辑 > 密度；不要为了 CPM 加点，不要打不存在的音。
5. 用户自己打的谱：只修手的误差（整体偏移 + 抖动），**不增、不删、不合并、不改点法**；每一处非吸附改动都写进报告。
6. OMG保留361点和160.637秒结束时间。23:04用户授权全谱复核手动偏差；记录时间、证据和原值，仍不改变其点法/增删点。

## 调研依据（docs/research/charting-logic.md，已逐条读过原网页）
- 跳舞的线：一次点击 = 一次 90° 转弯；线匀速，所以点距 = 路段长度。
- 赛车关：110 BPM、357 点、平均 220 CPM、峰值 440；最后一段只打旋律，漏掉小节强拍和弦，“引起了一些玩家的困惑” → **强拍要有点**。
- 钢琴关：平均 125 CPM、峰值 250；安静关约 2 点/秒。
- osu!/BSMG/Cytus/晨峦：每个物件要对准一个清楚的声音；一次跟一个层，换层要有意图；重复段一致；不要 overmap。
- P-centre：音节的感知拍点在元音起始附近 → 人声按网格位置吸附，鼓按真实起音。
- 规则集 10 条（同步优先、每段一个主层、强拍/反拍锚定、转弯=重音、默认 8 分、16 分只在听得到的地方、时间来源、乐句一致、相对强调、密度预算约 2–2.5 点/秒、峰值约 3/秒）——全文见该文件。

## 工作流：用户打点 → 可玩谱
1. **用户打点**：https://tbtnb.github.io/newjeans-line/tapper/（源码 `tapper/`，发布用 `tools/publish-tapper.sh`，只改 gh-pages `/tapper/`）。
   - 功能：选歌、延迟校准、按输出时钟录音、时间线编辑、A–B 段重录、导出/导入（f6516ba）。
   - 布局要求：手机单屏 100dvh、无文档滚动、安全区、无缩放/选中/长按菜单/点击高亮，录音时空格不触发聚焦的按钮（9550bd8）。
   - iOS 音频：audioSession 'playback'（静音键下也响）、手势解锁含 'interrupted' 与可见性、慢速播放用手势里启动的 `<audio>`（d2c9e15）。
2. **导入**：
   ```sh
   python3 tools/charts/import_taps.py <export.json> --song omg [--fit-offset] [--allow-16] [--report r.json] [--dry-run]
   ```
   步骤：校准 → 偏移检查 → 60 ms 内去重 → 吸附（默认 1/8，1/16 只在 ≥3 点的快串里）→ 离格 >60 ms 列为 QUESTIONABLE → 同格合并 → 可玩性（最小点距 0.105 s、首点 ≥1 s、末点 ≤ 时长−1 s、下落/跳跃后 0.35 s 内无点）。
3. **偏移**：人跟拍会提前（负平均异步）。OMG 实测整体提前约 55 ms（1/8 相位圆周平均 −55.5 ms，起音互相关 −52.5 ms），且分段漂移（前奏约 −16 ms，进鼓后 −54..−71 ms）→ 用**局部偏移**（±12 s 窗口），不用一个全局值。
   - 排除“滞后一个 1/8”的解释：那会让 262 个点落在反拍上。
4. **吸附**（`tools/charts/omg_user_snap.py`）：候选 1/16 格位上做 Viterbi。代价 = 位置误差（σ 25 ms）+ 与用户自己相邻间隔的误差（σ 30 ms）+ 1/16 反拍罚分 − 真实起音小加分（只用来决胜）。格位严格递增 → 不会合并/删除/凭空加点。
   - 结果（OMG v1）：277 个四分拍、84 个 8 分反拍、1 个 1/16；吸附移动中位 15.9 ms。
5. **精修 v2**（`tools/charts/omg_user_refine.py`）：每个点 ±10 s 窗口和分轨起音（kick/snare/vocal/bass/synth，已校正检测延迟）互相关求局部偏移，再逐格看起音证据。OMG 结果：361 点 0 改动（v1 已在用户想点的音上）。
6. **结尾**：用户谱提前结束时用 `layout.endTime/endFade`（路线、终点、进度、通关都按关卡长度；音乐淡出 1.5 s 后停），validator/router 都认 endTime（fef26b4）。
7. **验证**：
   ```sh
   python3 levels-design/validate.py <slug> --dir levels-src     # 0 errors（含 FORWARD 规则）
   python3 tools/charts/chartlogic.py <slug> --md docs/verification/chartlogic/<slug>.md
   python3 tools/research/click_track.py public/audio/<slug>.mp3 levels-src/<slug>/chart.json out.mp3 [--two]
   node tools/build-levels.mjs <slug>
   ```
   然后脚本模拟全曲（nj-qa-verification），听点击音轨（`--two` 用不同音色区分人声/鼓/乐器点）。

## 历史判定窗口和最小点距（OMG已改为几何容错）
- 判定窗口 = (路宽/2)/速度，上限 150 ms，且不超过相邻点距的一半（窗口相接不重叠）；PERFECT 仍是 40 ms。
- 加宽路面后最小点距按 0.15 s 处理。OMG 曾想把 Verse 2（77.6–78.6 s）改成 1/16 人声读法，但需要 0.118 s 的点距（77.49 s 处）→ **撤回**，A/B 留在 `deliverables/omg-ab/user-v2-vocal-proposal.mp3`。这件事用户还没回答，不要自己改。

## 同步第一（规则 1 的细节）
- 网格和偏移必须在游戏实际播放的同一解码上测：Chrome `decodeAudioData` 与 ffmpeg/librosa 无缝解码逐样本一致。
- demucs 分轨保留了 mp3 编码延迟，比混音晚 25 ms → 分轨必须先和混音互相关对齐（vocal_env 对齐，25c658c）。
- right-now 的分析网格是 2/3 速度（114.79 BPM，实际 172）→ 用 chart.json `meta: {bpm, beat0}` 覆盖（integ-c-issues.md）。

## 规则生成谱（用户打点之前的方法，仍可用于其余 15 首的初稿）
- `f9a0a4b` OMG v3：人声为骨架 + 0.2 s 内无人声点且无长音时补每个 kick/snare + 两者都没有时才用钢琴 → 553 点 = 444 人声 + 83 鼓 + 26 钢琴，规则偏离 0。
- `1f3b671` 歌词谱：Genius 歌词 + whisper large-v3 词先验 + 校准过的人声分轨起音，副歌联合对齐（06767e1，`analysis/omg.lyrics.json`）。
- `integrate.py` 的修剪阈值：faint（层 <0.35 且全混 <0.35 且无其它频段 ≥0.5）、off-layer（层 <0.35 而别的频段 ≥0.6）、weak burst（间隔 <0.15 s 且层和全混都 <0.6）。
- 其余 15 首现有谱是初稿（integ-a/b/c 等），都要按上面规则重审，以 OMG 为模板（交接文档第 7 节第 5 条）。

## 报告格式
- 中文；写清偏移模型、吸附分布、被标记需要听的点（表格：原始 t / 选中 / 误差 / 备选 / 原因）、任何撤回的提议和原因。参考 `deliverables/omg-user-import-report.md`、`deliverables/omg-user-refine-report.md`。
