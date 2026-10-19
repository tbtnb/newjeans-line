---
name: nj-lessons-learned
description: newjeans-line 踩过的坑和修法（Babylon 实例化、z-fight、雾、发光、impostor、放置、线头定位后的连锁问题、音频、合并回退等），按类别列出并附 commit。遇到奇怪的渲染/放置/音频 bug、或改 scenec/place/camera 之前读；逐轮历史见 references/rounds.md。
---

# 经验教训（按类别）

> 每条：现象 → 原因 → 修法（commit）。改相关代码前先搜一下这里。

## 最新试玩修复
本轮反馈、原因、实现、测试和仍未实测的内容见 [2026-10-19试玩回归](references/playtest-2026-10-19.md)。旧记录中“每段盒子”“吸附到转角”“密集段下落”“默认并行”已经被后续明确反馈覆盖，不要复用为当前方案。

## Babylon / 渲染
- **布景近处拷贝必须 `doNotInstantiate: true`**（`scenec.ts` buildSetVisual 的 `instantiateModelsToScene(..., { doNotInstantiate: true })`）。v8 改成 `vi > 0` 后，没变体的模型变成容器网格（不在场景里）的 InstancedMesh：133 个孤儿实例、134 条 BJS 警告，bunny-house / flip-phone / page-wall 的动画近处部件不显示（109cfe7）。验收：控制台没有 “Setting material on an instanced mesh”。
- 色板变体的布景近处拷贝要 clone 不能 instance：`makeGeometryUnique` 让凉亭/风车近处拷贝崩溃（97c9d7a）。
- 不用 GlowLayer：它把所有 unlit 自发光白材质都当发光 → 发白、draws 翻倍；改为合并发光网格里的淡光晕复制（6f4737f）。
- impostor：alpha test 需要 `useAlphaFromDiffuseTexture`（b5f4e92）；图集 `invertY=false`、卡片高度上限 11 m、卡片别挡 key 镜头路径（1910265）；歌曲两端的镜头路径方向要固定，否则 z10 出现细条（dda2307）。
- 页面的区归属 alpha 要到 shader 必须 `hasVertexAlpha`（否则 z07 页盖住 z06，f8c9e89）。
- 一行材质设置被吞掉 → `backFaceCulling = false` 实际没生效，纸卡片要双面（2f4adcb）。
- 布景跳过雾，否则主件奶油/粉色发灰（2f4adcb）；夜区装饰不受雾并提亮（996a912）。
- z-fight：书页 3 cm 台阶（2f4adcb）；每区一个书页网格 + 固定 polygon offset 顺序（后面的区在上），替代每块的页面方片（区边界出现阶梯，ca8a1e5）；旧地面放到 C 书页下 4 m（下落后出现藏青/桃色条纹，78af431）；线头不能和拖尾共面 + 阴影视锥按 texel 对齐（线头闪烁，c70b3fd）。
- 模型在首次放置前或地面刷新后流式到达 → 块窗口无效，需要 refill 守卫（9eb982a）。

## 放置 / 场景
- 放置点落在别的路段上就丢 → 丢了约 70% 中景 / 45% 地被；改为换位置重试（996a912）。
- v5 的近景带拒绝规则把所有房子/塔都拒了；v7 只对绿色团块生效（c98b772）。
- tree-bush / paper-hill 作为布景在镜头近处是大块薄荷色团 → 删掉，团块改由簇提供（1a389b1）。
- 爬坡时装饰在路下 8 m → 加坡道书页，装饰坐在路面高度（fe86dcf）。
- 栅栏曾是占位方块（fe86dcf 才建模）——上线前检查有没有占位几何。
- 淡紫条纹的页边在 ~99 s / ~146 s 看起来是平板 → 改成一叠合上的书（560cd78）。
- 页边卷曲在线头定位镜头下像一堵墙 → 降低卷曲（a57c8ee）。
- 随从不在占用网格里 → 兔子雕像穿进树林（a917493）。
- 装饰压在页卷下面 → 清掉页卷下的装饰（e50622e）。

## 镜头 / 线头定位的连锁问题
- 线头上移到 42% 后，画面下三分之一是线头后方，之前根本没建 → 块窗口保留后方约 6 s（7876efe），后按预算调为 4.5/4 s（637c3b9）。
- 近景带要重新对准画面底部（约后方 20 m），impostor 卡片不进近景带（532dca0）；高物件不进画面底部带（a917493）。
- 约 40 s 钟楼挡线头 → 放置时加镜头→线头视线规则，cutaway 半径 4.5→6.5 m（09935de）。
- cutaway 在镜头近处抖出补丁 → 线头高度以下不消隐（3194ee2）。
- 天空带在夜景吃掉画面顶部的路 → 深度跟随远处路面（09935de）。
- 主件靠路后被画面边缘裁掉 → 用 heroproj 找最佳时刻/侧/缩放（城堡缩放 1.9 → 1.6 → 1.15 → 0.8，2f887d0、248dca5、ba18863、aaa9813）。

## 模型
- 减面 LOD 产生碎片/破洞/颜色分裂 → 单独 bpy 写低模（2f0d408、83b38c4）。
- compare 的 mask 不公平 → v3 阈值 8 + 闭运算，v9 两边都填孔（940d86f、de7fee7）。
- 第一版兔子“太丑、不像参考图” → 尖锐切面 + 精确色板（BH1 940d86f → BH2 ce9e03f）。

## 音频 / 同步 / 输入
- 结束或失败淡出会把增益留在低位 → play() 总是恢复增益（faa6927）。
- iOS：绝不在挂起/interrupted 的 live ctx 上解码，用 OfflineAudioContext；audioSession 只在第一次手势时设置（e9680d7）；但 load() 里仍要创建 live ctx（歌曲时钟要走，dda41b6）。
- 慢帧时晚点击被误判 → 晚判宽限随帧时间放宽（输入每帧才到一次，f22e1b3）。
- demucs 分轨晚 25 ms（保留了 mp3 编码延迟）→ 先和混音互相关对齐（25c658c）。
- right-now 分析网格是 2/3 速度 → chart.json `meta` 覆盖（docs/verification/integ-c-issues.md）。
- 录屏用墙钟时间戳的改动造成问题被 revert（f205c42）——录屏不能证明同步。
- Chrome 翻译栏会弹出 → notranslate meta + 录制参数（cb6bb09）。

## 合并 / 构建 / 流程
- 合并时旧 layout 覆盖新值：refine 把路边裁切从 6% 改回 11%（31fd69a 修回）→ 合并后检查 layout 关键字段（路宽、裁切、endTime）。
- `src/levels/*.json` 冲突时直接 `node tools/build-levels.mjs` 重新生成。
- `public/levels/<slug>/art` 不进 git，发布前必须 build-levels。
- box SwiftShader 太慢，低档通关都会失败（OMG v2 在 105.4 s，1d3d9e3）→ 通关和截图以 Mac GPU 为准。
- perf/截图探针别落在 0.9 s 翻页遮罩里（4c5f0d3、209d090）。
- 两个 AI 同时改同一分支会冲突 → 交接前停下、推干净、写明 hash；新工作开新分支。

## 设计层面的教训
- “华丽”不等于满屏小物件：设计调研结论是近处干净、远处大轮廓、主件 + 整体色调；但用户也否了稀疏 → 解法是有结构的密度（台地、花圃、书堆、成排、主件靠路、天际线），而不是均匀撒点。
- 和 key 图比，差距主要在“立体书结构”（厚书页、台地、大主件靠近镜头、天际线），只加数量没用（v9 后的结论，见 references/rounds.md）。
