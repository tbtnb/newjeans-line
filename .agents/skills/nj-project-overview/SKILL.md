---
name: nj-project-overview
description: newjeans-line 项目总览。第一次接手这个仓库、需要知道分支/目录/命令/机器分工/当前进度时先读它，再按 AGENTS.md 索引去读具体 skill。
---

# newjeans-line 项目总览

## 当前实现基线（2026-10-19）
- 工作分支 `omg-c-fix-20261019`；运行时发布基线 `01cf13b`。以下 v11/Mac 指标是历史，不能当当前验收。
- `966f72e`：OMG 实际位置转向、几何容错、重开清线、3D皮肤展示、透明层顺序修复。
- `7260c29`：47%单点调整，密集段移除高差，兔子朝接近视角。
- `2278c04`：连续斜接拖尾与连续UV、开局无跳跃、场景预热与前方三块准备。
- `01cf13b`：后方实例/旧CPU缓存回收、预加载保护、重开/检查点恢复。44项自动检查通过；当前版本无手机GPU/真实帧率验收。
- 新入口：`src/core/travel.ts`（实际轨迹），`src/render/trailmesh.ts`（连续线几何），`src/render/skinpreview.ts`（真实3D展示）。
- 本轮自己完成，不启动云端Codex或subagent。历史机器路径仅为线索，使用前核实连接与当前授权。

## 是什么
- 跳舞的线（Dancing Line）的网页复刻，16 首 NewJeans 歌。Babylon.js + TypeScript + Vite + Playwright。
- 游戏时钟 = AudioContext 时间（OMG自由转向使用当前 songTime，不用未来预测位置拉扯轨迹；其它模式见代码）。
- 仓库：https://github.com/tbtnb/newjeans-line
- 正式版（不要动）：https://tbtnb.github.io/newjeans-line/
- 预览版（用户用 iPhone 试玩）：https://tbtnb.github.io/newjeans-line/preview/?level=omg
- 打点工具：https://tbtnb.github.io/newjeans-line/tapper/
- 歌曲顺序固定：Attention, Hype Boy, Cookie, Hurt, OMG, Ditto, New Jeans, Super Shy, ETA, Cool With You, Get Up, ASAP, How Sweet, Bubble Gum, Supernatural, Right Now。

## 分支
| 分支 | 用途 |
|---|---|
| `main` / gh-pages 根目录 | 正式版，**不改** |
| `omg-c` / `omg-c-preview` | 历史v11基线（e3ad9be），不是本轮发布分支 |
| `omg-c-fix-20261019` | 当前游戏修复与合并后的skills |
| `omg-design-v3` | 设计稿：`levels-design/omg/redesign-v3/C/`（区域稿、`assets/<id>/` 三视图 sheet.jpg + spec.json + prompts.md） |
| `gh-pages` | 部署；只改 `preview/`（和 `tapper/` 由专用脚本改） |
| `level-design-skills` | 本 skills 文档分支 |
| 旧：`rebuild`, `chart-research`, `omg-visual`, `integ-a/b/c`, `skins`, `art-props`, `tapper`, `designs-w1..w4`, `art-codex` | 历史工作分支（commit 信息里有大量理由） |

## 目录速查
- `src/render/scenec/`：方案 C 场景引擎（流式分块、合并装饰、impostor 图集、书页台地、天际线带、高/低画质档）。
  - `scenec.ts`（主体，TIERS、clone pass、buildSetVisual 的 `doNotInstantiate: true`）、`place.ts`（确定性放置器、视线规则、台地、填充网格）、`cutaway.ts`（镜头→线头锥内抖动消隐）、`variants.ts`（色板变体）、`paint.ts`（绘制地面）、`pageturn.ts`、`geo.ts`、`assets.ts`。
- `src/render/camera.ts`：镜头（KEY_PITCH 33、`pinHead()` 竖屏 42% / 横屏 47%）。
- `src/main.ts`：自适应画质、stale-build 守卫（读 `build.json`）。
- `tools/omgc/make_spec.py`：由设计数据 `zones_c.py`（omg-design-v3）生成 `levels-src/omg/scene-c.json`；`sky_day.py`、`sky_strip.py`。
- `tools/models/`：Blender bpy 建模管线（catalog.json、assets/<id>.py、paper.py、run.py、build.sh、compare.py、index.py、lod.py、AGENTS.md）。
- `tools/impostors/`：Blender 等距精灵渲染 + 图集打包。
- `tools/qa/`：perf-c、play、zshots、repcount、heroproj、trisweep、model-audit、design-vs-game.py、progress-board.py、fix-boards.py、tapper-*.mjs、avcal/。
- `tools/charts/`：import_taps.py、omg_user_*.py、chartlogic.py、integrate.py、route.py。
- `tools/research/`：route_forward.py、onsets/barmap/audit 工具。
- `docs/research/charting-logic.md`（打点调研 + 规则）、`levels-design/REFERENCE.md`（原作调研）、`levels-design/SCHEMA.md`、`levels-design/validate.py`。
- `deliverables/`：报告与对比图（`omg-c-shots/progress-morning.jpg`、`evolution.jpg`、`omg-c-models/*-compare.jpg`、summaries）。

## 常用命令
```sh
npm install
npm run dev            # 本地开发
npm run build          # build-levels + tsc + vite build
npm test               # 单元测试（交接时 23/23）
npm run test:webkit    # WebKit 检查
node tools/build-levels.mjs           # 重新生成 src/levels/*.json（合并冲突时直接重跑）
python3 tools/omgc/make_spec.py       # scene-c.json
tools/models/build.sh <id> ...        # 建模
tools/publish-preview.sh              # 只发布到 gh-pages /preview/
```
- 重任务在 box 上用 `flock /workspace/.nj-heavy.lock <cmd>` 串行（box 是 SwiftShader 软件渲染，很慢）。

## 历史机器分工（本轮不自动沿用）
- box（Linux）：代码、构建、Blender 4.5（`/workspace/tools/blender`）、SwiftShader 截图（慢，只作参考）。
- Mac mini（Apple M4）：GPU 截图、性能、iOS 模拟器、Codex 出图/出设计稿。
  - Codex：`codex exec -m gpt-6.1-sol -c model_reasoning_effort=high`
  - 临时工作区（非 git）：`~/nj-level-art/omgc-mac/omgc-mac`，`build/` 里有 Codex 启动脚本。
  - Blender 在 `~/tools`（build.sh 会找 `~/tools/Blender.app`）；numpy Python：`~/miniconda3/envs/comfyui-3.11/bin/python`。
- 分工原则：**Codex 出美术和设计图，agent 写代码**（见 nj-user-preferences）。

## 历史状态（v11，e3ad9be）与待重新核查事项
见 `/workspace/handoff/newjeans-line-handoff.md` 第 6–7 节（若不在本机，内容摘要）：
- 已完成：83 个模型的破面修复、克隆对清零、线头定位、钟楼不挡线头（视线规则）、两侧书页台地、主件靠路、天际线、路面三角形 24.6k→~5k；v11 加台地花园、卷页边、z04 城堡和 z07 高塔完整入画、z05 兔帆纸船主件。
- 性能（Mac M4，脚本模拟）：高 144.8k tris / 45 draws / 中位 6.7 ms；低 32.9k / 33 draws。
- 剩余：场景离设计稿仍远（z03 地面偏橘粉、z08 旋转木马/摩天轮被裁、z05 船偏低偏淡、台地顶色差太弱、天际线只有设计稿一半高、整体偏平）；cloud 侧/俯 IoU 0.78（目标 0.85）；castle 11 / heart-gate 6 个闪烁三角；其余 15 首按 OMG 模板重审。
- 未回答的问题：Cloudflare 托管或压缩音频；77.6–78.6 s 人声 1/16 方案（已撤回，见 nj-chart-design）。

## 读完之后
按任务类型去读：打点 → nj-chart-design；路线 → nj-route-design；镜头 → nj-camera；场景 → nj-scene-design；设计稿 → nj-design-sheets-codex；模型 → nj-3d-models；性能 → nj-performance；验证 → nj-qa-verification；发布 → nj-deploy-preview；踩坑 → nj-lessons-learned。**任何改动前先读 nj-user-preferences。**
