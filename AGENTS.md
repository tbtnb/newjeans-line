# AGENTS.md — newjeans-line

跳舞的线（Dancing Line）网页复刻，16 首 NewJeans。Babylon.js + TypeScript + Vite + Playwright，游戏时钟 = AudioContext 时间。
- 仓库 https://github.com/tbtnb/newjeans-line ｜ 正式版 https://tbtnb.github.io/newjeans-line/（不要动）
- 预览 https://tbtnb.github.io/newjeans-line/preview/?level=omg ｜ 打点工具 https://tbtnb.github.io/newjeans-line/tapper/
- 当前重点：OMG 方案 C「兔子立体童话书」（分支 `omg-c`，设计稿在 `omg-design-v3`）。其余 15 首之后按 OMG 模板重审。

## 硬规则（违反任何一条都会被用户否）
1. 正式版（main / gh-pages 根目录）和 `/tapper/` 不动；预览只发 gh-pages `preview/`；普通 commit，**永不 force-push**。
2. 完整音频：不剪、不加速、不循环（唯一例外：OMG 用用户 361 点谱，结束于 160.637 s；**不要改这个谱**）。16 首固定顺序。
3. 竖屏/横屏/电脑都能玩；存档可导入导出，旧存档兼容；iOS Safari 音频要能用。
4. 没有点击提示；路宽、容错高；线头朴素（无描边、无光晕）。
5. 路线永远往前（之字形前进），不盘旋、不回头。
6. 线头在屏幕 42%（竖屏）/ 47%（横屏）高度，绝不在下方被手指挡住；任何东西不能挡线头。
7. 每首歌一种一致的点法；人声/歌词为主层，没人声才跟鼓；节奏逻辑 > 密度。
8. 画面华丽、密集，但手机流畅：高 ≤ ~150k 三角 / ~45 draws，低 ≤ ~50k / ~30 draws。
9. 不重复克隆、不破碎模型；每个建筑先有细节插图 + 三视图，模型要像（bunny-heart BH2 是标准）。
10. 改地图前先出 Codex 设计稿给用户批；Codex（Mac mini）出美术，agent 写代码。
11. 脚本模拟要标明是模拟；按类别汇报验证结果，说清没验证的部分；每轮给设计稿 vs 游戏对比图。
12. 能并行就并行；用户说停就立刻全停。另一个 AI 可能在 `omg-c` 上工作：只在自己的分支上改。

## Skills 索引（`.agents/skills/<name>/SKILL.md`）
| Skill | 什么时候读 |
|---|---|
| [nj-project-overview](.agents/skills/nj-project-overview/SKILL.md) | 第一次接手；找分支、目录、命令、机器（box / Mac mini）分工、当前进度 |
| [nj-user-preferences](.agents/skills/nj-user-preferences/SKILL.md) | **任何改动或汇报之前**；用户全部规则与反馈原话、时间、原因、未回答的问题 |
| [nj-chart-design](.agents/skills/nj-chart-design/SKILL.md) | 做/审谱面：tapper 打点导入、偏移、Viterbi 吸附、精修、判定窗口、点击音轨、打点调研 |
| [nj-route-design](.agents/skills/nj-route-design/SKILL.md) | 生成/改路线、路宽、方角、下落、路面渲染；FORWARD 规则 |
| [nj-camera](.agents/skills/nj-camera/SKILL.md) | 改镜头/运镜/天际线；线头定位 42%/47%；视线规则和 cutaway；线头被挡或主件出画 |
| [nj-scene-design](.agents/skills/nj-scene-design/SKILL.md) | 场景/地图：区域、五层布景、书页台地与花圃、主件表、密度、去克隆、夜景发光、逐区打磨 |
| [nj-design-sheets-codex](.agents/skills/nj-design-sheets-codex/SKILL.md) | 地图重设计、新建筑/布景、贴图：Mac Codex 出概念/区域/三视图设计稿 + 提示词模板 + 审批流程 |
| [nj-3d-models](.agents/skills/nj-3d-models/SKILL.md) | 建/修模型：Blender bpy 管线、paper.finalize、gltfpack、compare IoU、model-audit、LOD/impostor |
| [nj-performance](.agents/skills/nj-performance/SKILL.md) | 加元素/模型、画质档、预算超标；合并/实例/impostor/窗口手段与测量工具 |
| [nj-qa-verification](.agents/skills/nj-qa-verification/SKILL.md) | 交付前后验证：测试、脚本模拟通关、headlog、Mac GPU、WebKit/iOS、审计、对比图、汇报模板 |
| [nj-deploy-preview](.agents/skills/nj-deploy-preview/SKILL.md) | 发布 /preview/ 或 /tapper/、核对 build.json、推送被拦截、回滚 |
| [nj-lessons-learned](.agents/skills/nj-lessons-learned/SKILL.md) | 遇到奇怪 bug 或改 scenec/place/camera 前；逐轮历史在 `references/rounds.md` |

其它就近文档：`tools/models/AGENTS.md`（建模 worker brief）、`docs/research/charting-logic.md`、`levels-design/REFERENCE.md`、`levels-design/SCHEMA.md`、`docs/SHOW_FX.md`、`docs/ART_PROPS.md`、`docs/SKINS.md`。

## 快速命令
```sh
npm install && npm run dev       # 开发
npm test                         # 单元测试
npm run build                    # build-levels + tsc + vite build
node tools/build-levels.mjs      # 重新生成 src/levels/*.json
python3 tools/omgc/make_spec.py  # levels-src/omg/scene-c.json
tools/models/build.sh <id>       # 建模
tools/publish-preview.sh         # 只发 gh-pages /preview/
```
