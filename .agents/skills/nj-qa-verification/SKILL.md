---
name: nj-qa-verification
description: newjeans-line 验证与汇报：单元测试、脚本模拟全曲（含线头位置日志）、Mac GPU 截图/性能、WebKit 与 iOS Safari 音频、重复/破面/主件取景审计、设计稿对比图，以及按类别汇报的格式。每次交付/发布预览前后、给用户汇报结果时读。
---

# 验证与汇报

## 用户规则
- 脚本模拟可以当测试，但**必须标明“脚本模拟”**，不是真机，也不能证明音画同步。
- 按类别汇报：每类写结果，并**直说哪些没验证**（例：“这次没在真的 iPhone 模拟器上测到，因为模拟器卡住了，所以你的手机是第一次真机测试”）。
- 每轮给对比图（设计稿 vs 游戏）。

## 每次交付的验证清单（交接文档第 8 节）
| 类别 | 怎么测 | 合格 |
|---|---|---|
| 单元测试 | `npm test` | 全过（交接时 23/23） |
| 谱面/路线 | `python3 levels-design/validate.py <slug> --dir levels-src` | 0 errors |
| 全曲通关（脚本模拟） | `play.mjs` 跑到结算画面 | OMG 361/361，结束于 160.637 s |
| 线头位置 | `play.mjs --headlog` | 竖屏 y 约 0.42，全程不往下掉 |
| 帧率/预算 | Mac `perf-c.mjs --gpu`、`trisweep.mjs` | 见 nj-performance |
| iOS 音频 | WebKit（iPhone 配置）/ iOS 模拟器：加载、点一下出声 | 能加载、点后有声 |
| 控制台 | 浏览器 console | 无新警告（尤其 “Setting material on an instanced mesh”） |
| 场景质量 | repcount、heroproj、model-audit、对比图 | 克隆对 0–3、主件入画、0 破面 |

## 命令
```sh
# 脚本模拟（CDP touch 事件，按谱面时间点击）
DISPLAY=:99 node tools/qa/play.mjs --url URL --level 5 --w 540 --h 960 [--from 0] [--to 999] \
   [--log out.json] [--headlog head.json] [--shots 20,45,90 --shotdir DIR] [--quality low] [--scale 1.5] [--record out.mp4]
#   --jitter/--miss/--double/--extra/--pauseAt 用来测容错和暂停
node tools/qa/zshots.mjs <url> <outdir> --gpu [--q high|low] [--z z05,z09] [--t ...]   # 每区关键时刻（静态渲染，不是游玩）
node tools/qa/snap.mjs --url URL --level 5 --times 10,40,80 --out DIR    # ?debug 预览帧（静态，不证明动态）
node tools/qa/repcount.mjs <url> out.json [--z z05,z09]                  # 每区可见资产、头部占比、克隆对
node tools/qa/heroproj.mjs <url> [--gpu] [--min 6]                       # 主件入画
node tools/qa/model-audit.mjs <dev url> <outdir> [ids...]                # 破面
npm run test:webkit                                                      # WebKit 冒烟（服务生产包到 4175）
node tools/qa/tapper-audio.mjs [URL] [chromium|webkit] [out.json]        # 打点工具音频解锁（Mac: PW_MODULE=playwright-core）
node tools/qa/tapper-layout.mjs [URL] / tapper-e2e.mjs [URL]             # 打点工具布局 / 端到端（合成输入）
python3 tools/qa/design-vs-game.py <renders(zNN-key.jpg)> <shots(zNN.png)> out.jpg [title]
python3 tools/qa/progress-board.py <renders> <shots> out.jpg "<title>" z01 z04 ...
```
- box 上重任务加 `flock /workspace/.nj-heavy.lock`；box 的 SwiftShader 很慢（OMG v2 低档在 box 上只有约 11 fps 并在 105.4 s 失败，1d3d9e3），所以**通关和截图以 Mac GPU 为准**（zshots/perf-c/heroproj 的 `--gpu` 用 `--use-angle=metal`）。
- Mac 上没有 dev server 时：`npx vite build --config tools/qa/vite.audit.config.mjs --outDir <dir>` 出静态包再起本地服务（交接时 Mac 上 4611 端口开过一个本地预览服务）。
- 对已发布的预览直接测线上 URL（`https://tbtnb.github.io/newjeans-line/preview/?level=omg`），确认测的是新 build（看 build.json）。
- 脚本模拟偶尔会卡顿（OMG 有过“one scripted stall”、Mac 被别的任务占着时两个点慢约 70 ms）→ 重跑一遍，两次都报。

## iOS 专项（用户在 iPhone 上玩）
- 游戏音频（d2c9e15、e9680d7、dda41b6）：audioSession 'playback'（静音键）、每个手势同步解锁（touchend/click/keydown；pointerdown 不算），恢复 iOS 'interrupted'；在 OfflineAudioContext 上解码（绝不在挂起的 live ctx 上）；load() 里仍创建 live ctx（歌曲时钟要走）；加载画面有下载进度；卡住/解码超时给提示，不无限加载。
- 关卡结束：play() 总是恢复增益（之前的结束/失败淡出会让增益停在低位，faa6927）。
- stale-build 守卫（`src/main.ts`）：读 `build.json?t=...`（no-store），若 `preview_of` 的 hash 和包内 `__BUILD__` 不同，用 `?v=<hash>` 重载一次（sessionStorage 防循环）。发布后告诉用户“打开还是旧版就刷新一次”。
- 音画同步工具：`tools/qa/avcal/`（蜂鸣+闪光采集标定）、`syncan.py`（?syncprobe 录屏分析）。

## 对比图与进度图
- 每轮把 Mac GPU 的线头定位截图和 key 图并排：`deliverables/omg-c-shots/progress-morning.jpg`（挑 5–6 个区）、`design-vs-game.jpg`（全部区），旧版保留为 `*-vN.jpg`，截图放 `vN/`。
- `evolution.jpg`：同一时刻（如 z04/z08 的 49.8 s / 108 s）v1…vN 的演变（95426b2）。
- 修模型/去重复时出修复前后特写板：`broken-fix-board.jpg`、`repetition-board.jpg`（fix-boards.py）。

## 汇报模板（中文）
1. 一句话结论 + 预览链接 + “刷新一下就是新版”。
2. 通关：“我在 Mac 上用脚本模拟打完了全曲：361 个点全部完美，一直 60 帧”。
3. 线头位置、性能（高/低档 tris、draws）。
4. iOS/WebKit：测了什么、结果；没测到的直说原因。
5. 和设计稿的差距（实话）+ 下一轮计划。
6. 附对比图（左设计稿、右游戏）。
