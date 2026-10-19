---
name: nj-qa-verification
description: newjeans-line 验证与汇报：单元测试、脚本模拟全曲（含线头位置日志）、Mac GPU 截图/性能、WebKit 与 iOS Safari 音频、重复/破面/主件取景审计、设计稿对比图，以及按类别汇报的格式。每次交付/发布预览前后、给用户汇报结果时读。
---

# 验证与汇报

## 当前回归与证据等级
- a09c66f本轮61项自动测试及构建通过；Mac本机静态包的版本/主JS哈希、模型音频HTTP已验证，Chrome开局至1%及120设置/FPS显示已冒烟（约60FPS）。不是全曲或iPhone120FPS证明。Pages故障期间的发布状态见最新试玩记录，不把gh-pages上传当网站已部署。
- 前一轮运行时代码基线01cf13b：44项自动检查通过，TypeScript/Vite构建通过。没有本轮Mac GPU/iPhone帧率或最终画面验收；下方v11数字与示例不是当前结果。
- 用 `node --import tsx --test tests/*.test.ts` 可避免受限环境中tsx CLI的IPC套接字失败；与npm test执行同一测试集，记录实际命令。
- 新回归：早晚点击不吸附、实际撞墙、重开清空；连续转角顶面和UV相接、无内部封面、增量顶点更新；47%单拍、开局平路；预加载不误删、过期任务失效、检查点恢复。
- 单元通过≠脚本全曲画面通过≠真机手感通过。WebGL不可用时如实报告，不虚构截图或沿用旧GPU报告。
- 发布通过需要Pages任务success + 线上build.json + 主JS内容与本地包一致；另检查gh-pages非preview路径没有变化。技能文档提交可比线上代码更新，说明文档与运行时版本的区别。

- 统一加载新增回归：音频未解码总进度不能100%，未知长度/迟到回调不能倒退，缓存与重试正确；场景仅目标窗口+3块，检查点不先构建开局，远处地标不抢开局实例化。本轮完整测试数以最终日志为准；最终发布证据见试玩记录。

- 新增：120/60 rAF限帧、旧存档兼容、实际FPS不能用钳制dt，密集段局部宽度和双限擦边，完整361点/方向及20处微调对应，拖尾后窗纹理连续。

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
2. 通关：仅填写本轮实测设备、脚本/人工、点击数和结果；没有该测量就写未验证，不能照抄历史361完美/60帧。
3. 线头位置、性能（高/低档 tris、draws）。
4. iOS/WebKit：测了什么、结果；没测到的直说原因。
5. 和设计稿的差距（实话）+ 下一轮计划。
6. 附对比图（左设计稿、右游戏）。

## 2026-10-20 重开回归补充
只测seek(0)不足：检查点53.968、106.88、暂停回退均要检查拖尾在ready时indices=0/disabled，开始后从新起点增长；两种居中模式都覆盖。还需模拟Safari resume延迟、等待中stop及新play超越旧play，旧异步结果不能替换新音源或时钟。收集动画途中重开不得销毁可复用皇冠/钻石。自动测试不能替代用户Safari实际操作。

## 2026-10-20 01:20 通关界面与按钮回归
- 通关→返回菜单→重开不得残留白色遮罩；旧代码在flash元素设置局部CSS变量，却只清root同名变量，局部0.85永不退场。已取消全屏闪光，保留皇冠动画。
- 重试圆箭头是描边图形，不得继承播放三角的fill/currentColor与stroke:none；retry/replay/restart-p均需stroke-only且有“重新开始”可见文字。
- 按钮背景/图标必须用成对固定高对比色，不从场景dark主题的--ink借主按钮背景，否则白底白图标。文字标签使用深色小底片，夜景/亮景都清晰。
- 显式[hidden]优先于组件display，没拿皇冠时不显示复活按钮；不能只测试hidden属性存在而忽略CSS覆盖。
- tests/result-ui.test.ts覆盖结构和样式约束；截图视觉检查与Safari实机仍独立记录，不能把静态断言当浏览器渲染验收。
