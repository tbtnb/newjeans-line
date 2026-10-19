---
name: nj-design-sheets-codex
description: 设计先行流程：在 Mac mini 上用 Codex 出概念图、区域 key/detail 渲染、每个建筑的 3/4 插图 + 正侧俯三视图 + 部件图 + spec.json，给用户批准后再改游戏。任何地图重设计、新增建筑/布景、给其它 15 首做场景、出地面/背景贴图时读。
---

# 设计稿与 Codex 工作流

## 规则（用户）
- 改地图之前**先出设计稿/渲染图给用户批**，批了再动游戏代码。设计包的 DESIGN.md 开头写明“仅设计，不改游戏代码”。
- 每个建筑/大布景：细节插图 + 三视图，模型必须照它做（nj-3d-models）。
- Codex 在 Mac mini 上出所有美术和插图；agent 写代码、写合成脚本、做测量。

## Codex 怎么跑（Mac mini，machineId 见 nj-project-overview）
- 命令：`codex exec -m gpt-6.1-sol -c model_reasoning_effort=high`，用内置 image_gen，一次调用一张图。
- 工作区：`~/nj-level-art/omgc-mac/omgc-mac`（非 git），`build/` 里有启动脚本；早期设计在 `/Users/bit_1/nj-level-art/omg-v3/wc/`（`cam-ref.png` 在这里）。
- 参考图：`style-ref.jpg`（已批准的风格）、`cam-ref.png`（**只**管镜头角度、路与方块比例、直角之字形；风格全忽略）、资产图用自己的 `hero.png` 作权威参考。
- 并行：多个 Codex worker 同时跑（模型第一轮是 7 个并行 worker，95419c2）。
- 每张图的**精确提示词**都存进同目录 `prompts.md`（重出的存 `prompts-views2.md`、`prompts-views3.md`）。

## 设计包结构（omg-design-v3 分支）
```
levels-design/omg/redesign-v3/
  DESIGN.md              # 原作调研 + 三个概念 A/B/C + 方案 A 区域
  prompts/c.md, zNN.md   # 概念图 / 区域渲染提示词
  C/DESIGN.md            # 选定方案 C：世界观、DROP 设计、五层布景、区域速览（实例/三角估算）、每区稿
  C/zones_c.py           # 区域、色板、布景点、分层元素与实例数（make_spec.py 读它）
  C/blueprint.py sheets.py make_doc.py
  C/prompts/zNN.md, zNN-r2.md
  C/renders/             # 原始渲染
  C/assets/ASSETS.md     # 共享色板 + 主件/道具/地被清单（尺寸、面数、枢轴/动画、色板槽、三视图一致性）
  C/assets/<id>/         # sheet.jpg hero.jpg views.jpg front/side/top.jpg parts.jpg spec.json prompts.md
deliverables/omg-redesign/C/board.jpg, zones-zNN-*.jpg, blueprint.png
```

## 流程
1. **调研**原作（为什么好看），写进 DESIGN.md 第 1 节，附来源链接。
2. **概念**：出 2–3 个方向的 key 渲染（竖屏 2:3），表格写优点/风险，给推荐。OMG 时推荐 A，用户选了 C → 以用户选择为准。
3. **区域稿**：每区 1 张 key（游戏镜头）+ 3–4 张 detail（单件展示），写色板、路面、灯光、主件、分层元素与实例/三角估算、蓝图布景点（时间+侧）、音乐同步、过渡。拼成 `zones-*.jpg` 和总览 `board.jpg`。
   - 用户觉得相邻区太像时要拉开（4c9283b：z01 薄荷珍珠黎明 / z02 饱和正午村 / z03 珊瑚到靛蓝黄昏病房）。
4. **发给用户批**（图 + 简短中文说明），等确认。
5. **资产设计稿**（批了之后）：每件主件/标准道具一张：3/4 插图 + 正/侧/俯三视图（同比例）+ 部件特写 + 色板槽 + 面数预算 + 枢轴/动画；地被小件 7–8 件一张共享稿（4×2 网格）。
   - 三视图一致性脚本自动量（正/侧高度、正/俯宽度、侧/俯深度像素差 ≤25% 记 ✓）；不一致的重出 views2/views3，自动挑最好的（ae37a1d）。
   - 薄物件（纸帘 P08、旗串 P21）深度只有几像素 → 人工复核写进 `views_check.note`；俯视带俯角（H12 翻盖手机）或画扁（P24 纸云）→ 以正/侧为准。
   - 面数：主件 2–8k，道具 200–1.5k，地被 2–200。
6. **贴图类**（地面、背景全景）：同样 Codex 出，提示词强调双向无缝、无暗角、无文字；接缝不行就 seam-correction 重出（`deliverables/omg-c-paint/prompts.md`）。

## 提示词要点（模板见 references/prompt-templates.md）
- 开头 `Use case: stylized-concept.` + `Asset type:`（IN-GAME KEY RENDER / DETAIL RENDER / ORTHOGRAPHIC THREE-VIEW MODELING PLATE / DETAIL CALLOUT PLATE / seamless ground texture / panoramic backdrop）。
- 风格段固定复用：雕刻感低多边形纸艺、平面着色切面、软倒角、纸有厚度和折痕、**不是平面贴纸**。
- 硬约束固定复用：无人、无人脸、无真人肖像；兔子是无五官切面脸；**无文字/字母/数字/logo/水印/UI**；无写实。
- key 渲染写清镜头和路：高 3/4 俯视约 60°、单条连续直角之字形路、路宽约线头 2.3 倍、路是最亮元素、路边 1–2 个路宽内无高物件、地标在路侧。
- 三视图：真正正交、三等分、同一比例、写明 W:D:H、俯视图不要放大填满、浅灰 #E6E6E6 平底无阴影、色板 hex。
- 写死精确色值（ASSETS.md 共享色板），不要让模型“自由发挥”色调。

## 交付和汇报
- 图发给用户时用中文简述每张图是什么、对应哪个区/哪个时间点，问“可以吗”；用户批准的原话记进 nj-user-preferences。
- 设计包提交到 `omg-design-v3`（或同名新分支），游戏分支只读不写设计目录。
