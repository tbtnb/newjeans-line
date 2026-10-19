---
name: nj-3d-models
description: newjeans-line 低多边形纸艺 3D 模型管线：Blender 4.5 headless bpy 每件一个脚本、paper.finalize（去共面/去重/翻面/烘焙光）、gltfpack meshopt、compare.py 三视图 IoU 还原度、model-audit 破面检查、LOD/impostor。新建/修改/修复任何模型，或用户说“模型丑/不像/破/重复”时读。
---

# 3D 模型

## 当前执行边界与展示
- 本轮用户要求不派云端Codex、不派subagent；文末并行建模只保留历史方法，不自动执行。
- 兔子立牌/摆件朝向按实际接近镜头核对；导出模板正面+Z，不能把建模坐标−Y直接当运行时yaw。
- 皮肤演示里的线头使用真正3D几何和装饰，不能拿选择器图标贴在头上充当模型；其接续与UV见 `nj-line-skins`。

## 标准（用户）
- 模型必须像设计稿：**bunny-heart（BH2）是标准**——尖锐的纸艺切面、精确色板、耳朵有厚度和折叠。糊成一团（blobby）的会被否（“这个兔子太丑了，和参考图完全不像啊”）。
- 不能有破面：z-fight 闪烁、重复面、翻面、减面碎片、悬空件、穿插。
- 详细规范：`tools/models/AGENTS.md`（给建模 worker 的 brief，必读）、`tools/models/README.md`。

## 管线
```
design: omg-design-v3 levels-design/omg/redesign-v3/C/assets/<design>/ (front/side/top.jpg, hero.jpg, spec.json)
tools/models/catalog.json            # 77 条：engine id -> design 目录 (+ kit item 序号)、cls、budget、size
tools/models/assets/<id>.py          # build(P, spec)，每件一个
tools/models/paper.py                # 建模工具：box/cyl/ico/prism/card/lathe/blade、heart/star/ear/ellipse 轮廓、pivot、mirror_x、paint
tools/models/run.py                  # Blender 入口：build -> finalize -> raw glb + 正交 front/side/top + iso 渲染 + report json
tools/models/build.sh <id>...        # run.py -> gltfpack -cc -kn -km -> public/models/omg-c/<id>.glb -> compare.py -> deliverables/omg-c-models/<id>-compare.jpg
tools/models/compare.py              # 设计视图 vs 模型渲染 + 洋红色设计轮廓叠加，指标：每视图 IoU、长宽比差、平均色差、尺寸差
tools/models/index.py <build> out.jpg  # 全部模型的总览图（iso + tris/budget + IoU）
tools/models/lod.py                  # 减面做填充用低模（只用于团块/远环，见下面的坑）
```
- Blender：box `/workspace/tools/blender`；Mac `~/tools/Blender.app`（build.sh 自动找）。设计目录默认 `/workspace/nj-design-v3/levels-design/omg/redesign-v3/C`（omg-design-v3 的工作树），可用 `DESIGN=` 覆盖；`TMP_DIR` 默认 `/tmp/omgc-build`。
- Python 要有 numpy：Mac 上 `~/miniconda3/envs/comfyui-3.11/bin/python`（build.sh 会用 `PY`）。
- 离线构建：`npm_config_offline=true tools/models/build.sh <id>`（gltfpack@1.3.0 已缓存）。

## 约定（AGENTS.md）
- Blender Z 朝上、米；正面朝 −Y；底在 z=0、足迹居中；严格按 spec `size_m`（w=X，d=Y，h=Z）。
- 每个脚本开头 docstring：设计 id+名字、尺寸、预算、枢轴、`SIMPLIFICATIONS:`。
- 枢轴：spec `pivots` 里的动画部件建空物体 `pivot_<kind><index>`（`P.pivot(...)`）。引擎会动的种类：root（必须顶层，在原点）、heart/pulse、ears、gate/lid、flag、tower、bob、spin、wheel、swing、hand。主件 ≤12 组（每组一个 draw），道具 ≤3，套件只有 root。
- 颜色：spec `colors` 的 hex **原样使用**；平面每面一色；切面变化只靠同部件两档色交替（cream #FFF3DE / paper #FFF8EC）；**不要自己加暗/染色/做旧**——管线烘焙柔光（受光面 = 精确 hex，背光面 ≥0.88×；bake v2 `lo=0.80, ao=0.07`）。
- 面数：主件用预算的 60–90%，道具 50–90%，套件 50–100%，绝不超预算。三角形花在轮廓上：有机形用 ico subdiv 2–3、lathe 10–16 段、倒角；耳朵要有厚度和折叠，不是平片。

## 验收
- IoU：正、侧 ≥ 0.85，俯 ≥ 0.80；尺寸 ±5%；compare 表头任一轴差 >15% 标红。
- 设计稿自己的视图互相矛盾时，以正视 + hero 为准并写明（例：BH2 的俯视图耳朵位置与侧视矛盾）。
- 薄物件（P08 纸帘、P21 旗串）侧/俯 IoU 不可靠；H12 俯视带俯角 → 以正/侧为准；P24 云俯视画扁 → 俯视只作参考。
- **每次迭代都要打开 compare.jpg 用眼睛看**，再读 metrics.json；每件最多约 8 轮。
- BH2 参考结果：3515/4000 tris（87.9%），IoU 0.950/0.922/0.927，尺寸差 0/0/0（`deliverables/omg-c-models/summaries/summary-BH2.md`，每轮迭代表格是好范例）。
- 完成后写 `build/summary-<worker>.md`：每件一行 tris/budget、IoU、尺寸差、简化项。

## compare.py 的公平性（踩过的坑）
- v3：设计图前景阈值 8 + 形态学闭运算（奶油色纸和灰底只差约 10 级，v2 阈值 14 会丢掉整只耳朵/脸颊/脚）。
- v9：设计图的封闭孔洞被填充（分不出孔和奶油纸）→ 模型的 mask **也同样填孔**，否则开放的拱/辐条/柱间会被算成缺失（凉亭、摊位因此被低估）。

## 破面审计（v8，用户反馈“破碎的建模很多”之后）
```sh
node tools/qa/model-audit.mjs <dev server url> <outdir> [ids...]     # box SwiftShader；Mac 加 --gpu
npx vite build --config tools/qa/vite.audit.config.mjs --outDir <dir>  # Mac GPU 审计的静态包（无需 dev server）
python3 tools/qa/fix-boards.py ...                                   # 修复前后对比板（broken-fix-board.jpg / repetition-board.jpg）
```
- 加载**最终** glb（gltfpack 之后），4 个视角开背面剔除渲染（翻面显示为洞），报告：degen、dupes、floating（离地且 bbox 不碰任何其它岛）、inverted（封闭岛体积符号反）、openIslands、zfight（+ 位置 zfAt）。
- `paper.finalize()` 自动修：`_join_by_parent`（每个枢轴组合一个网格）→ `fix_closed`（向内的封闭件翻面、零面积面溶解）→ `decoplanar`（不同岛同平面同朝向重叠面沿法线推开约模型高 0.25%（≥2 mm），同件重复面删除；最多迭代 10 次）→ `bake_light`。
- 交接时仍有：castle 11 个、heart-gate 6 个闪烁三角；lantern-tower、gift、stall 的 floating 标记和 hanging-star、reading-bunny 的翻面要复查；cloud 侧/俯 0.78（目标 0.85）。

## LOD / 低模
- **不要用减面做可见低模**：tree/pine 减面产生碎片和颜色分裂，paper-hill 减面出现破洞 → 改成单独 bpy 写的 `tree-lo`、`pine-lo`、`paper-hill-lo`（2f0d408、83b38c4）。
- 远处用 impostor：`tools/impostors/render.py`（Blender 36° 等距，平涂烘焙色，无描边）+ `pack.py` 图集（36 张 2048×1024 WebP 220 KB，bfa501d）。
- 一个 glb 可以被多个模型 id 共用（GLB 别名，7dd9297）。

## 并行建模（Mac Codex worker）
- 按 AGENTS.md 的边界分配：worker 只写自己的 `assets/<ids>.py`、`build/`、自己的 glb/compare/summary；不改 paper.py/run.py/compare.py/build.sh/catalog.json/设计目录；不装软件、不联网、不杀进程。
- 第一轮 77 件由 7 个并行 Codex worker 在 Mac 上完成（95419c2）；后续 F1–F5、W1–W9、R1–R3、BH/BH2、FA/FB 轮次的总结在 `deliverables/omg-c-models/summaries/`。
- worker 交回后在 box 上用同一 compare 版本全量重建一次，确保指标一致（3c53220：box 与 Mac 指标一致）。
