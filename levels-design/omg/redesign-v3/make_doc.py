import sys
from pathlib import Path
H = Path(__file__).parent; sys.path.insert(0, str(H))
from zones_v3 import ZONES, TEXT
head = r'''# OMG 地图重设计 v3（设计稿，待确认）

> 状态：**仅设计，不改游戏代码**。确认方案后再进入建模/实现。
> 路线：origin/rebuild 当前谱面（你的点击，361 拍点，160.6 s 结束，前进式折线路线，路宽 2.2→2.0→1.8 m ≈ 2.2–2.5 倍线宽）。
> 所有渲染图均由 Codex（Mac mini，gpt-6.1-sol，high）生成；是**设计效果图**，不是最终贴图——实现时用真正的低多边形 3D 网格搭建。

交付物：
- 总览板：`deliverables/omg-redesign/board.jpg`（三个概念 + 推荐方案的十个区域）
- 区域设计稿：`deliverables/omg-redesign/zones-z01-intro.jpg` … `zones-z10-finale.jpg`
- 路线蓝图：`deliverables/omg-redesign/blueprint.png`
- 原始渲染：`levels-design/omg/redesign-v3/renders/`（Codex 提示词见 `prompts/`）
- 数据/脚本：`zones_v3.py`（区域、色板、布景点）、`blueprint.py`、`sheets.py`、`make_doc.py`

---

## 1. 调研：原版跳舞的线为什么好看

1. **低多边形“微缩模型”世界**：场景基本由方块和少量定制模型拼成，平涂/少量渐变材质、无复杂贴图，靠清晰轮廓和体积取胜（参考：Unity 论坛对其制作方式的分析 [1]；低多边形美术要点：干净剪影、有限色板、简单方向光 [3]）。
2. **一关一个完整主题世界**：每首歌对应一个原型场景（冬天、农田、天空、海洋、钢琴…），所有物件都服务于这个主题，所以看起来“统一”而不是“堆贴纸”[2][5]。
3. **随音乐分段换景、换色**：到达检查点/乐段时，颜色、灯光、物件形状和氛围一起变化；《The Earth》从明亮绿野转向被砍伐的工地，音乐同时变暗，叙事感很强 [2][4]。
4. **路本身就是世界的一部分**：路会变成桥、栈道、石阶、屋顶、悬崖边；在后段甚至变色/变窄来提示难度（如《混沌》The Chaos 60% 处路由黄变砖红并变窄 [6]）。
5. **布景动画=音乐可视化**：物件从地下升起、倒下、塌落、翻开、发光、随拍跳动；关键鼓点有大动作（drop 爆发），安静段落只有少量轻动作。
6. **光与雾**：单一主方向光 + 柔和阴影 + 远景雾/渐变底色，把视线集中到路与线头上；前景路面亮度/饱和度永远最高。
7. **克制的密度**：近处干净、远处有大轮廓；“华丽”来自大型主件与整体色调变化，而不是满屏小物件。

参考：
[1] Unity Discussions “How do they make this?” https://discussions.unity.com/t/how-do-they-make-this/652016
[2] Reading Eagle, “Graphics and music morph into tricky ‘Dancing Line’” (2017) https://www.readingeagle.com/2017/08/29/graphics-and-music-morph-into-tricky-dancing-line/
[3] RetroStyle Games, “Low Poly Game Art: An Ultimate Guide” https://retrostylegames.com/blog/low-poly-game-art-an-ultimate-guide/
[4] NoobFeed, Dancing Line Review https://www.noobfeed.com/reviews/dancing-line-review
[5] Baidu Baike (EN), Dancing Line 关卡列表 https://baike.baidu.com/en/item/Dancing%20Line/1460178
[6] NamuWiki, 혼돈(Dancing Line) 条目 https://en.namu.wiki/w/%ED%98%BC%EB%8F%88(Dancing%20Line)

**由此得出的设计原则**（v3 全部遵守）：
- 立体雕刻感低多边形网格（圆角倒角、平面着色），**不用平面贴纸立牌**。
- 每区 3–5 色的限定色板；区与区之间做“颜色+地形+路面材质”三重变化。
- 路面始终是最亮、最干净的元素；布景只在路两侧，近路 2 m 内不放高物件，远处放大主件。
- 每区 1 个“主件”（hero set piece）+ 2–3 种重复配件，宁少勿乱。
- 音乐同步：drop 有一个大动作，乐句有中动作，拍子只做小动作（亮灯/轻跳）。

---

## 2. 三个整体概念

| 方案 | 一句话 | 优点 | 风险 |
|---|---|---|---|
| **A 粉彩病院·五个白日梦（推荐）** | 以粉彩低多边形病院为底色，沿路墙板像立体书一样翻开，依次进入病人们的白日梦：黑兔舞台、玻璃鞋宫殿、猫咪屋顶、翻盖手机桥、Y2K 屏幕城、童话书页，最后五面主题墙在日出舞台合体。 | 直接对应 MV（精神病院喜剧、每人一个幻想、手机、玻璃鞋、猫、书）；十个区域变化最丰富又有统一母题“病院→幻想”；路面材质每区可变（地砖→T台→玻璃桥→屋脊→手机桥→屏幕砖→书页） | 资产量最大，需要严格控制每区资产数（每区 1 主件 + 2–3 配件） |
| B 翻盖手机宇宙 | 整关在一部 Y2K 翻盖手机内部：电路板地形、按键广场、电容塔、屏幕天空；路是发光电路走线。 | 风格极统一，实现简单（几何感强） | 十个区域容易“长得一样”；与 MV 病院叙事关系弱 |
| C 兔子立体童话书 | 从巨大书页中弹出的纸艺低多边形花园：纸山、纸树、兔子雕像、纸月亮，路是奶油色纸带。 | 温柔、漂亮、低多边形折纸感天然适合 | 偏安静，副歌不够“炸”；与病院/手机主题关联弱 |

推荐 **A**：它把 MV 的核心梗（病房里的每个人都活在自己的幻想里）变成关卡结构——每到一个乐段，“病房墙板翻开”就是换景动画本身，非常像原版跳舞的线“随音乐整块变换世界”的做法。B 的手机元素与 C 的书页/猫元素都被吸收进 A 的单独区域里。

统一规则（方案 A）：
- 母题：白色/薄荷色病院地砖 + 金色细边，在每个区域都以某种形式出现（墙板、地砖边、终点五面墙之一）。
- 两次副歌（黑兔舞台、屏幕城）是全关最亮、最饱和的两段；中间区域（玻璃鞋、屋顶、书页）降低对比，给耳朵与眼睛休息。
- 线头/路面：路面为浅色高亮材质 + 发光包边，所有区域路面亮度高于地面至少 2 档。

---

## 3. 区域设计（方案 A）

区间与谱面对应（谱面原分段标签在括号内）：
intro 0–15.1（病房走廊）· verse1 15.1–30.3（治疗桌与五椅）· pre1 30.3–45.4（墙板外折）· chorus1 45.4–60.5（黑兔舞台）· post1 60.5–75.6（玻璃鞋）· verse2 75.6–90.7（双折长短路）· pre2 90.7–105.8（手机桥）· chorus2 105.8–121.0（屏幕块）· post2 121.0–151.2（错列直角 + 书页墙与猫 + 书页合拢）· finale 151.2–160.6（舞台五墙）。
'''
parts = [head]
for Z in ZONES:
    T = TEXT[Z['id']]
    parts.append(f"""
### {Z['id'][1:]} · {Z['cn']}（{Z['en']}）— {Z['key']}，{Z['t0']:.1f}–{Z['t1']:.1f} s

![](../../../deliverables/omg-redesign/zones-{Z['id']}-{Z['key']}.jpg)

- **色板**：{' '.join('`' + c + '`' for c in Z['pal'])}
- **路面**：{T['road']}
- **灯光/氛围**：{T['light']}
- **主要布景（细节渲染）**：{'、'.join(T['assets'])}
- **蓝图布景点**：{'；'.join(f"{t:.1f}s {'路左' if s < 0 else '路右' if s > 0 else '全场/路面'} {n}" for t, s, n in Z['pieces'])}
- **音乐同步**：{T['sync']}
- **过渡**：{T['trans']}
""")
parts.append(r'''
---

## 4. 路线蓝图

![](../../../deliverables/omg-redesign/blueprint.png)

俯视全路线（800 m，按 200 m 分四行，前进方向向右）。底色=区域；粉色圆点=路侧主件（距路中心约 12 m，实现时按 RoadGrid 推开保证不压路）；金色三角=音乐同步时刻/路面变化；蓝色菱形=钻石；金冠=皇冠检查点。布景点全部按时间 t + 左右侧定义，**相对路线生成**，换谱后自动重算。

## 5. 实现备注（确认后再做）

- 每区：1 个主件（可动画的低多边形模型）+ 2–3 种配件实例化（thin instance），配件沿路两侧按节拍间距重复。
- 材质：平面着色 StandardMaterial/PBR 低光泽，少量自发光（霓虹、屏幕、灯）；色板驱动。
- 换景：沿用 reveal（rise/unfold/drop）+ 区域边界的“墙板翻开”动画；颜色通过雾/环境光/地面渐变过渡 1–2 s。
- 性能：每区同屏不超过 ~12 个主件实例 + 配件，静态网格冻结；不遮挡路面（沿用前方路线遮挡回避）。
- 待你确认：① 选 A/B/C；② 十个区域主题是否要替换某几个（例如屋顶猫 ↔ 别的 MV 元素）；③ 色调整体偏亮(白天) 还是偏夜景。
''')
(H / 'DESIGN.md').write_text(''.join(parts))
print('ok')
