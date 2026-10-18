# 人声 / 伴奏 卡点研究 + OMG v4 重谱

> 起因：用户反馈 v3「卡点怎么样都不对劲」。本文 = 业界规则调研 → v3 量化诊断 → 新规则 → v4 结果。
> 数据脚本：`tools/research/omg_diag_v3.py`（诊断）、`tools/research/omg_v4_chart.py`（v4 生成器，规则写在文件头）。
> 试听：`deliverables/omg-clicks-v4.mp3`（整首），`deliverables/omg-ab/`（主歌 / 预副歌 / 副歌各约 15 秒，v3 与 v4 对比）。
> 点击音：**高音“嘀” = 跟人声的点**，**低音“咚” = 跟鼓的点**，中音 = 无鼓段的乐器脉冲点。

## 1. 调研结论（带出处）

| # | 规则 | 出处与原文 |
|---|---|---|
| 1 | **所有音符都必须落在节拍网格上。人声唱得不准时，谱师不能为了跟人声而偏离网格** | osu! 论坛（unsnapped notes）：“If the vocals are off, that's just tough luck for the mapper. They can't unsnap any notes to follow the vocals… all notes must follow the timing that comes from the music” https://osu.ppy.sh/community/forums/topics/80040 ；osu! 上架标准：“All circles and slider heads should be snapped to distinct sounds” https://osu.ppy.sh/wiki/en/Ranking_criteria/osu%21 |
| 2 | **要么能用一个稳定、可预测的分音表达，要么就简化** | osu!mania 上架标准：声音若 “would be effectively represented with a consistent, predictable snap” 就应简化成那个分音 https://osu.ppy.sh/wiki/en/Ranking_criteria/osu%21mania |
| 3 | **跟人声时只取重要的重音；人声拉长音的地方用伴奏节奏补上；8 分为主，16 分只用来给强调处加料** | 太鼓达人官方博客《三瀬川乱舞》谱面解说：“歌の伸びにあたる部分には、リズムにあわせた音符を配置”（人声拖长的部分按节奏放音符）；“ボーカルに合わせた音符は８分音符や１６分音符が主”；同一首歌一段跟歌、一段跟乐器时，要把两种写法明确分开 https://taiko-ch.net/blog/?p=1815 。Yamaha 对太鼓谱师的访谈（歌合わせ / ドラム合わせ 按段落区分）https://member.jp.yamaha.com/topics/myujin/2024/wm-79103 |
| 4 | **密度不要突然跳**（A 段以 8 分为主 → B 段出现 16 分 → 副歌以 16 分为主） | 同上太鼓博客：“急激な密度変化をなるべく避ける” |
| 5 | **低难度只跟主旋律，长音用 hold 代替“刷点”** | Project Sekai 谱面指南：“HARD levels generally focus on the main melody… Any underlying pattern may be replaced with hold note” https://sekai-guide.tootiejin.com/charting-guide/making-charts-in-different-difficulties |
| 6 | 跟人声时的点在**声调转折 / 元音起点**，不在辅音起点 | Phigros「音押」帖：“他的采音点在于人声的声调转换点 … ā→á 刚刚要说出来的时候” https://www.taptap.cn/moment/570328126907745294 |
| 7 | 跳舞的线官方唯一有歌词的关卡（All About Us）：**同一句歌词每次出现都用同一个点法**，并且点法是可以记住的 | https://www.taptap.cn/moment/15204677620597264 ；赛车关的分析：最后一段只跟旋律、跳过重拍，让玩家困惑 https://www.233leyuan.com/post-detail/1966480825598370516 |
| 8 | 人声起音**本来就不在网格上**：流行歌手在 1、3 拍平均**提前**，16 分强位（N/+）平均**拖后**，弱位（e/a）更准。数字修音让人声越来越贴网格。听感上的节拍由伴奏决定 | Georgieva 等，TISMIR 2026，88,357 条人声：“singers tend to anticipate the beat, especially on beats 1 and 3”“Stronger metrical positions… were more likely to be delayed” https://transactions.ismir.net/articles/10.5334/tismir.278 |
| 9 | 听感上“这个字在哪个拍点”（P-center）≈ **元音起点**，不是辅音起点；擦音开头的字感知更晚 | 伴奏者对齐歌手的元音起点 https://www.jvoice.org/article/S0892-1997(06)00005-1/abstract ；P-center = 预期中的元音起点 https://pubs.aip.org/asa/jasa/article-abstract/155/4/2698/3283278 ；拍点落在韵母前约 25% 处 https://doi.org/10.31219/osf.io/3xdjw ；英语 52.9% / 普通话 66.7% 的拍点落在元音上 https://pubs.aip.org/asa/jasa/article/148/4_Supplement/2699/645226 |
| 10 | 人声故意晚 70–90 ms 进是一种“groove”，**不能拿来当点的时机** | 安室奈美惠分析 http://acoustics.asn.au/conference_proceedings/ICA2010/cdrom-ICA2010/papers/p908.pdf |

**一句话总结：** 音游里“跟人声”的意思，是**跟人声的节奏型**（它落在哪些 8 分 / 16 分格子上），不是跟人声的**实际起音时间**。时间永远以伴奏的网格为准。人声的切分可以保留，但必须吸附到网格。孤立的 16 分弱位和三连音不写。

## 2. v3 哪里不对（量化诊断，`analysis/research/omg-diag-v3.json`）

v3 共 553 个点，其中人声点 444 个。

| 问题 | 数字 | 为什么听起来“不对劲” |
|---|---|---|
| 不在 16 分网格上的点（三连音 + 原始起音 + 鼓的原始起音） | **113 / 553**（人声：三连音 56，原始起音 29） | 对网格的偏移中位数约 40 ms，听起来像“抢拍 / 拖拍”。规则 1 明确禁止 |
| 人声点落在 16 分弱位（e / a） | **117**，其中 **101 个是孤立的**（前后 1/16 都没有点） | 每个点都是一次转弯。孤立的弱位转弯 = 随机感最强的来源 |
| 只有 **54.5%** 的人声点在 8 分格子 ±15 ms 内 | — | 节奏型读不出来 |
| 强鼓拍（kick 或 snare ≥ 0.8）没点 | **112 / 267** | 律动的骨架缺了 |
| 其中强鼓拍旁 30–160 ms 处有一个人声点 | **100 拍** | 最糟的情况：点“差一点”落在鼓上，像一记“闪音”（flam），手感上觉得自己点错了 |
| 每小节点数 | 1 – 9，标准差 1.45，相邻小节差 ≥4 的有 8 处 | 密度忽高忽低 |
| 时间参考：P-center（80–1000 Hz 人声包络上升最快的时刻）− 我们检测到的起音 | 中位数 **+27.5 ms**（四分位 −4 到 +73） | 起音检测抓到的是辅音 / 起音，元音还要再晚一些 |
| 人声起音相对 16 分网格的偏移 | 带符号中位数 +3.7 ms，绝对值中位数 16.8 ms。P-center 分别为 +11.9 / 19.9 ms | 两种参考都散布在网格周围，**网格才是最稳的参考**。把点放在网格上，比放在辅音起点（早）或 P-center（散）都准 |

结论：「不对劲」不是“没跟歌词”，而是 **v3 跟得太“真实”**。它把歌手的微小时差（三连音、原始起音、孤立 16 分）原样写成了转弯，同时漏掉了 100 个就在旁边的强鼓拍。

## 3. 新规则（v4，全曲一套，`omg_v4_chart.py` 文件头）

- **G 网格：** 所有点都在 127.003 BPM 网格上，默认 1/8。**没有三连音，也没有原始起音。**
- **D 脉冲：** 每个强鼓四分拍（kick 或 snare/clap ≥ 0.8）都点，全曲都适用。无鼓小节（强鼓拍少于 2 个）改用乐器 / 贝斯在四分拍上的起音（≥ 0.6）作脉冲。
- **V 人声：** 音节的起音**或** P-center 若在某个 1/8 点 ±45 ms 内，就在**那个网格点**加一个点。优先级：句首 > 副歌钩子词（oh / my / god / baby…）> 词首 > 强度。每小节最多 4 个人声点（句首和 16 分连唱不受此限）。
  - 1/16 只用于**清楚的连唱**（≥ 3 个连续 16 分音节，强度都 ≥ 0.5）。**孤立的 16 分音节不点。**
  - 切分保留，只要它落在 1/8 反拍上。
- **H 长音：** 人声拉长音（≥ 1 拍）期间没有人声点，D 脉冲照常继续，所以律动不会断（对应太鼓“歌の伸び”的做法）。
- **S 一致：** 同一句歌词用同一种点法（多数投票）。副歌 / 后副歌的复制段完全照抄母段。
- 人声点和鼓拍重合时只算一个点（103 个人声点同时就在强鼓拍上）。

## 4. v4 结果

| 指标 | v3 | v4 |
|---|---|---|
| 总点数 | 553 | **516**（2.43 个/秒，1 秒内峰值 7 个，最小间隔 0.118 s） |
| 不在网格上的点 | 113 | **0** |
| 16 分弱位点 | 117（孤立的 101） | **8（全部在连唱里，孤立的 0）** |
| 四分 / 8 分反拍 | 207 / 116 | 345 / 163 |
| 人声点 | 444 | 336（其中 103 个同时在鼓拍上）+ 鼓 164 + 乐器 16 |
| 人声点在 1/8 格子 ±15 ms 内的比例 | 54.5% | **97.6%** |
| 强鼓拍没点 / 强鼓拍旁边是“差一点”的人声点 | 112 / 100 | **0 / 0** |
| 每小节点数 | 1–9 | 1–10，中位数 5 |

- 路线：仍用 `route_forward.py`（只往前走的 N/E/W 阶梯）。
- 布局：用 `omg_layout_fix.py` 调整钻石；第二个皇冠移到 129.05 s，让它后面有一段平静的直线。
- 校验：`validate.py` 结果为 **0 错误 0 警告**（含 FORWARD 规则）。
- 脚本试玩：complete，514 perfect + 2 good / 516，钻石 10/10（`deliverables/omg-v4-play.json`）。

**代价（如实说明）：** 被点到的人声音节从 444 降到 336，少了 24%，删掉的主要是三连音、原始起音和孤立 16 分。如果用户反过来觉得“歌词跟得少了”，可以调高每小节人声点上限 `--vb 5`。网格规则不应该放松。

**A/B 片段**（`deliverables/omg-ab/`，各 15 秒）：

| 片段 | 文件 | v3 点数 | v4 点数 |
|---|---|---|---|
| 主歌（15.0 s 起） | `1-verse-v3/v4.mp3` | 42，其中 10 个不在网格、7 个 16 分 | 34，全部在 1/4 或 1/8 |
| 预副歌（29.6 s 起） | `2-prechorus-v3/v4.mp3` | 45，其中 10 个不在网格、10 个 16 分 | 42，只有 3 个 16 分（连唱） |
| 副歌（45.2 s 起） | `3-chorus-v3/v4.mp3` | 39，其中 10 个不在网格、8 个 16 分 | 40，全部在 1/4 或 1/8 |
