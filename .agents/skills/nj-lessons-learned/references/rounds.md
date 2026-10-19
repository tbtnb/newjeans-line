# OMG 方案 C 逐轮记录（来自 omg-c 的 git log）

> 数字均摘自 commit 信息；perf 为当时的测量（box = SwiftShader，Mac = M4 GPU）。

## 方案 C 之前（OMG v1/v2，同一天 2026-10-18）
- 规则谱 451 → v3 553 点 → 歌词谱 478 → 用户自打 361 点（fef26b4）；路线改为前进式（2961ddc，用户“地图还是往前走的”）。
- OMG v2 场景（omg-visual）：Codex 概念 3 个方向、歌词触发事件（“God”时手机亮、drop 46.427/106.898 s 兔子升起）；corridor 布景：会挡线头或未来约 3 s 路的物件下沉（9cde34f）。
- 加宽路面、朴素线头（f37b6d1）；iOS 音频加固（d2c9e15、e9680d7）。

## 设计阶段（omg-design-v3）
- 7e02b42 三概念（推荐 A）→ 用户选 C → 2b92476 C 设计包 → 4c9283b 拉开 z01–z03 → 48fe498/032638b/5772498 资产设计稿 → ae37a1d 三视图重出与人工复核。

## 引擎与模型
- 4daa560 建模管线；ba143d7 放置 spec；317ff9b 流式分块引擎；8ff05f1 城堡/兔子/树按设计稿。
- 模型 round 1（95419c2，77 件，7 个并行 Codex worker）→ round 2（3c53220）→ BH1（940d86f，用户嫌兔子丑后）→ round 3 + BH2（ce9e03f，用户“可以的”）→ round 4 兔脸（a2050bf）→ W8/W9 弱模型（fe86dcf）→ round 8 Codex 还原度（b1d3c8d）→ v8 审计修复（2f0d408）。

## 场景轮次
| 轮 | 主要内容 | 代表 commit |
|---|---|---|
| 密度 1/2 | 3D 套件替代贴片、远环、放置重试、夜景灯晕 | 30b8e72、996a912、bf905eb |
| v3 | 簇团、纸带路、key 镜头变体（pitch 31→36）、cutaway | 78b8de5、09d8ee5、ebe2837 |
| v4 | Codex 绘制地面/背景、impostor 地毯、去 GlowLayer、暖色曲线+暗角 | 3b21c5b、8e89cd3、6f4737f |
| v5 | 每区主件表 + 随从、近景带、页堆边/纸悬崖、静态布景 1 draw | 1a389b1、085d0ea、9f6f3c0 |
| v6 | 夜村、主件取景运镜（?focus）、预算 | 416f3f7、db70a99 |
| v7 | 夜空条、贴路改为按层开启 | 4e08ca1、d2152da |
| v8 | 'view' 层、开书前景、天空条、去重复轮、破面审计、线头定位合并、视线规则 | e228ad7、2947b43、e50622e、2f0d408、60ba8ba、09935de |
| v9 | 混合团/树林/堆、填充网格、窗口后方、compare 填孔、低档 lowMul、doNotInstantiate 回退修复 | 532dca0、7876efe、de7fee7、9cbb5b9、109cfe7 |
| r10 | 书页台地、主件就近、pitch 33 + 天际线、书堆页边、cutaway 不消隐低处、clone pass、路面窗口 | 5d46e34、ba18863、0eaa85e、560cd78、3194ee2、7b768b0、b6a3826 |
| r11 | 台地花圃、城堡/z07 高塔完整入画、z05 纸船主件、z01/z03/z10 更茂盛、预算回到 144.8k | 467d186、aaa9813、328ade4、6c87ace |

## 每轮交付物
- `deliverables/omg-c-shots/`：`progress-morning.jpg`、`design-vs-game.jpg`、`evolution.jpg`（旧版 `-vN` 保留）、`vN/` 截图、`perf/perf-cNN-*.txt`。
- `deliverables/omg-c-models/`：`<id>-compare.jpg`、`summaries/summary-*.md`。
