---
name: nj-performance
description: newjeans-line 手机性能：三角形/draw 预算、高低画质档、自适应降档、合并/thin instance/impostor/分块窗口等手段、测量工具（perf-c、trisweep）和历次实测。加场景元素、加模型、改画质档、或预算超标时读。
---

# 性能

## 预加载与回收必须协同（2278c04 / 01cf13b）
- 当前不是只在镜头内才加载：资源按路线前后窗口管理，视锥剔除另负责是否绘制。保留key镜头后方4.5秒/4秒；不能在线头经过后立刻删除仍在画面下方的景物。
- 开局前等待模型下载/解码/地标实例准备（并发2），合并CPU数据分块yield预热，缓存上限64MiB；初始材料编译在播放前做。共享模板/纹理保留以供后续同款模型和重开使用。
- GPU块维持活动窗口+前方3块，未来块先隐藏。每个异步任务准备一块；进入窗口时直接启用，避免当帧重新合并大量模型。
- 普通块出窗口销毁；CPU缓存只清活动起点之前额外2块之外的旧数据。未来预热数据不能因当前在视锥外就清掉。
- 大地标过时间范围（def.t+12）、已隐藏且其整体包围盒不在镜头内，才释放far/near实例与枢轴引用；每帧最多回收一个，保留共享模板、材料、贴图、布局定义。
- 异步回调执行前重新核验当前窗口；重开/画质切换取消或丢弃旧任务。不能让旧窗口任务在回退后“复活”无用资源。
- 重开/检查点在恢复音频前 `prepareAt(t)`：从模板恢复需要的摆件并补前方窗口。不需重新下载全部素材，也不能漏模型。
- `CStats`新增 `preparedChunks`、`bakedBytes`、`residentSets` 便于跟踪资源是否随行进回落；总游戏内存还包括共享素材，不能把CPU缓存数字当总内存。
- 回归：`tests/scenec-preload.test.ts` 覆盖未来不误删、旧任务失效、回退恢复、可见地标保留。实际卡顿要在真机按长帧p95/p99、模型冒出瞬间和连续重开内存测量；44项单元测试不证明手机帧率。

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
