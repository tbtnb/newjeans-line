---
name: nj-performance
description: newjeans-line 手机性能：三角形/draw 预算、高低画质档、自适应降档、合并/thin instance/impostor/分块窗口等手段、测量工具（perf-c、trisweep）和历次实测。加场景元素、加模型、改画质档、或预算超标时读。
---

# 性能

## 统一加载与有界开局准备（2026-10-19 22:58反馈）
- 根因：2278c04把整曲CPU合并、全曲地标实例化/编译都移到开局，且warmup在音频后才开始，启动等待过长。不能把“避免途中卡顿”解释成开局构建整首歌所有实例。
- 当前 `main.ts` 同时等待音频与 `world.prepareScenery(t, onProgress)`；下载占音频任务90%，解码完成才算该项100%。统一进度按音频40/模型30/场景道路25/渲染5加权，基于实际已完成任务，非倒计时。未知下载总量显示MB，不伪造百分比；全部完成前总进度不报100%。
- `SceneC.warmup`仅下载/解码共享模板，然后准备目标时间的活动窗口+前方3块、未来16秒内地标及相关编译。其余地标不在constructor/模型到达时批量实例化；沿途沿用一任务一块/一地标的提前准备。CPU缓存按实际构建填充，上限64MiB，不再全曲预合并。
- 准备期间render loop不得重建占位块或覆盖检查点窗口；重开/失败重试释放准备锁、取消旧prefetch回调；并发音频失败后旧进度不能覆盖新加载会话。
- 回归 `tests/loading.test.ts`、`tests/scenec-preload.test.ts`：并发/缓存/未知长度/未解码/重试的进度；起点和检查点窗口有界、远处地标不创建、前方3块与回收规则继续成立。
- 这是工作量与调度优化；实际节省几秒、iPhone长帧/内存仍需实测，不从单元测试推算速度。

## 预加载与回收必须协同（2278c04 / 01cf13b基础，以上更新覆盖开局策略）
- 当前不是只在镜头内才加载：资源按路线前后窗口管理，视锥剔除另负责是否绘制。保留key镜头后方4.5秒/4秒；不能在线头经过后立刻删除仍在画面下方的景物。
- 开局前等待共享模型下载/解码（并发2）和必要窗口的地标实例、CPU/GPU块准备；每块yield，CPU缓存上限64MiB；必要窗口材料编译在播放前做。共享模板/纹理保留以供后续同款模型和重开使用。
- GPU块维持活动窗口+前方3块，未来块先隐藏。每个异步任务准备一块；进入窗口时直接启用，避免当帧重新合并大量模型。
- 普通块出窗口销毁；CPU缓存只清活动起点之前额外2块之外的旧数据。未来预热数据不能因当前在视锥外就清掉。
- 大地标过时间范围（def.t+12）、已隐藏且其整体包围盒不在镜头内，才释放far/near实例与枢轴引用；每帧最多回收一个，保留共享模板、材料、贴图、布局定义。
- 异步回调执行前重新核验当前窗口；重开/画质切换取消或丢弃旧任务。不能让旧窗口任务在回退后“复活”无用资源。
- 重开/检查点在恢复音频前 `prepareAt(t)`：从模板恢复需要的摆件并补前方窗口。不需重新下载全部素材，也不能漏模型。
- `CStats`新增 `preparedChunks`、`bakedBytes`、`residentSets` 便于跟踪资源是否随行进回落；总游戏内存还包括共享素材，不能把CPU缓存数字当总内存。
- 回归：`tests/scenec-preload.test.ts` 覆盖未来不误删、旧任务失效、回退恢复、可见地标保留。实际卡顿要在真机按长帧p95/p99、模型冒出瞬间和连续重开内存测量；44项单元测试不证明手机帧率。

## 全局掉帧与120帧（23:05/23:14新反馈）
- 用户明确开局起全局掉帧；不能仅归因后半程。移除全曲地标实例常驻、平路无用RoadSightline着色器；Cutaway先判断高度/距离，只有真正遮挡锥内才做sqrt/sin抖动，视觉公式不变。
- 高频统计移到4Hz，HUD 10Hz，同值天空CSS不重复写；模型/动作仍每次渲染更新，不得为节流统计而节流弹起动画。
- 2026-10-20 00:47：120模式仍像60。120模式移除额外时间阈值跳帧，使用rAF提供的时间戳；7.06/9.6ms交替回调必须全部绘制，不能被阈值变成60。HUD同时显示实际渲染FPS、主循环回调Hz与目标，回调Hz不是硬件刷新率证明，重负载也会降低回调。
- 120模式使用浏览器rAF，不用定时器伪造刷新；60模式只限渲染，输入/音频时钟每次rAF持续推进。帧率是实际渲染次数/未钳制墙钟时长，不能用动画dt上限伪装低帧率。
- 设置保存targetFps 60/120和showFps；旧存档默认60、记录不丢；选择120自动显示实际FPS。120模式高档DPR上限1.25，触屏60高档1.5，桌面60高档2；流畅档1。按CPU提交耗时压力继续降分辨率，不强改相机/点位；CPU提交耗时不等于GPU耗时。
- 拖尾保留后14秒、纹理累计距离连续。CPU-only NullEngine样本150秒附近：全历史345段5528顶点，对比窗口18段296顶点；不是手机FPS证据。
- 验收需要真机从开局、密集段到后半程观察实际FPS和长帧；浏览器锁60时不得宣称120已达成。

## iPhone Safari 的实测排查（2026-10-20 01:06）
- 用户确认使用Safari，随后仍反馈60帧；因此9c7ac84不能标记为iPhone120验收通过。还未确认机型、iOS版本、显示的回调Hz和系统设置。
- WebKit维护者说明：ProMotion设备可关闭Safari的“Prefer Page Rendering Updates near 60fps”功能标志以允许120Hz页面更新；来源 https://bugs.webkit.org/show_bug.cgi?id=288402#c19 。这是浏览器设置，不是网页能代改的游戏设置；不要建议批量修改实验标志。
- Apple说明ProMotion设备低电量模式限制至60Hz；来源 https://support.apple.com/en-euro/101604 。还需区分硬件是否支持120Hz、发热、辅助功能限帧及场景性能。回调只有60本身不能证明硬件只支持60，重负载也可能导致低回调。
- 先核对最新build、目标120、实际渲染FPS及回调Hz，再比较轻负载与关卡；不得用定时器重复提交冒充120，也不能将Safari历史限制笼统说成永久不支持120。

## 预算（用户：华丽但手机要流畅）
| 档 | 三角形 | draws |
|---|---|---|
| 高 | ≤ ~150k | ~45 |
| 低 | ≤ ~50k | ~30 |
- 自适应（`src/main.ts` `autoTier`，14f870c）：手机按存档画质开始（默认高）；游玩中帧 EMA > 24 ms（约 40 fps 以下）持续 4 s → 本次会话降到低档，只降一次；玩家在设置里手动选过画质（`localStorage nj-quality-picked`）就不覆盖。日志 `[nj] auto quality: high -> low`，`window.__njAutoLow`。
- v11 实测（Mac M4，脚本模拟）：高最多 144.8k / 45 draws / 中位 6.7 ms；低 32.9k / 33 draws。低档 z10 曾到约 50k（要盯）。

## 画质档（`src/render/scenec/scenec.ts` `TIERS`）
- high：density ground 1 / mid 1 / sky 1 / anim 1，ahead 8，behind 3，lod 35 m。
- low：ground 0.5 / mid 0.7 / sky 0.6 / anim 0，ahead 6，behind 2，lod 22 m。
- 带 `hi` 标记的元素低档不建；每区 `lowMul` 再稀释（z10 0.7、z08 0.35，9cbb5b9 / 67d832f）；z08 非主件布景只在高档。
- 低档：impostor 0.18、无背景带、无额外 key 窗口（dda2307）。

## 手段（都是实际用过、有效的）
- **合并**：每区一个书页网格；中景每块合并并随块弹出（996a912）；页堆/书堆/开书前景合进一个 page-stack 网格（0 额外 draw）；发光物合并到一个 glow 网格；皇冠环+尖刺合并（每个 7 → 2 draws，9a38213）。
- **静态布景**近镜头保持合并的 1-draw 网格；只有带动画的布景才有近处拷贝，且静态部分合并（城堡 6 draws → 2，9f6f3c0、248dca5）。
- **thin instance**：地被和同类型装饰。
- **impostor 卡片**：远处村庄灯塔只用 impostor（fdcbc52）；卡片按距离缩放；图集一张。
- **分块流式窗口**：key 镜头高档线头后 4.5 s / 低档 4 s（637c3b9）；路面只画后 9 s 到前 24 s（24.6k → ~5k，b6a3826）。
- **便宜的填充**：混合树林每棵 150–300 三角；把 500 三角的 book-stack 移出填充/堆的混合（637c3b9）；r11 花片用 3–5 朵 GLB 花（75 三角，6c87ace）。
- **按区按种类缩量**：重区（z09/z10、夜/黄昏区）砍 300–600 三角的散布种类；用 trisweep 找峰值区再动刀。
- 不用 GlowLayer（白化 + 2× draws，6f4737f）；柔光晕不做 bloom 复制（8975a42）；地面各向异性关闭、冻结世界矩阵、不每帧刷新 thin instance 包围盒（54d4526、cfaed39）。
- 粒子按真实秒老化（帧慢时池子不饱和，fa552c7、7a8bd01）。

## 测量
```sh
node tools/qa/perf-c.mjs <url> [--gpu] [--q high|low] [--hero] [--png --shots dir] [--dpr 1]
#   每个探针时刻：draw calls、可见三角（活动网格 × thin instance）、活动网格数、GPU 同步帧时间（render + 1px readPixels，30 次中位），播放中 rAF p50/p95
node tools/qa/trisweep.mjs <url> [--q high|low] [--step 1]   # 全曲每秒 scenec 统计 -> 每区最大值（v11 新增）
node tools/qa/prof-omg.mjs ...                               # 渲染剖析
```
- `--gpu` 在 Mac（ANGLE Metal）跑才算数；box 是 SwiftShader 软件 GL，绝对时间没有参考价值，只看 tris/draws。
- 场景统计 `CStats`：`tris`（视锥内）、`trisWindow`（整个块窗口）、`trisAtBudget`（如果每件都按预算满额建模时的三角数，用来预估）。
- perf-c `--hero`：每区探针放在该区最大布景前（v5 起 3.5 s 前），避开 0.9 s 的翻页遮罩（4c5f0d3）。
- 结果存 `deliverables/omg-c-shots/perf/perf-cNN-<box|mac>-<high|low>.txt`。

## 历次实测（commit 信息原文数据，Mac 除非注明）
| 轮 | 高 | 低 |
|---|---|---|
| 密度轮 30b8e72（box） | 44 dc / 158k | 28 / 61k |
| c10 77d174b | 40 dc / 155k，4.0 ms 中位 | 31 / 47k |
| c11 dae04ef | key 41 / 145k，3.5 ms | key 34 / 50k |
| c12 fffcba8 | 44 dc / 151k，4.4 ms 中位 7.0 最大 | 37 / 56k |
| r11 前 → 6c87ace | 158.9k → 144.8k，45 draws | — |
| v11（交接） | 144.8k / 45 / 6.7 ms | 32.9k / 33 |

## 检查清单（每次加东西后）
1. `trisweep --q high` 和 `--q low`，看每区最大值是否在预算内。
2. Mac `perf-c --gpu --hero` 看 draws 和帧时间。
3. 控制台没有 “Setting material on an instanced mesh” 警告（见 nj-lessons-learned 的 doNotInstantiate）。
4. 超预算时先砍低价值的散布，不砍主件和台地；低档优先用 `lowMul` / `hi`。
