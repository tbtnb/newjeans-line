# OMG 方案 C · 资产清单与建模设计稿

> 设计阶段（不改游戏代码）。每件主件/标准道具一张建模设计稿：3/4 插图 + 正/侧/俯三视图（同一比例、网格、尺寸线、比例尺）+ 细节部件 + 色板槽 + 面数预算 + 枢轴/动画；地被与小件按 7–8 件一张共享设计稿。
> 渲染：Codex（Mac mini，gpt-6.1-sol，high）；合成脚本 `build_sheets.py`；数据 `assets_c.py`；每件目录 `assets/<id>/`（sheet.jpg、hero/views/front/side/top/parts.jpg、spec.json、prompts.md）。
> 单位：游戏单位 m（路宽 ≈2.2，线头 1）。面数：主件 2–8k，道具 200–1.5k，地被 2–200。三视图一致性由脚本自动测量（正/侧高度、正/俯宽度、侧/俯深度的像素差，≤25% 记 ✓）。

## 共享色板图集

`cream #FFF3DE` `paper #FFF8EC` `gold #F7D98B` `foil #E9B949` `mint #BDEBD8` `pearl #F3F1EA` `fog #CFE3E6` `sky #5FB8F0` `sun #FFD23F` `green #6CCB5F` `coral #FF7A6B` `peach #FFC2A8` `orange #FFB056` `indigo #3A2F6B` `navy #1F2350` `pink #FF6FAE` `blush #FFC7DA` `lavender #B9A6F0` `lilac #E3D7FA` `magenta #FF4FA0` `cyan #7FE0E8` `plum #2A1640` `teal #173A4A` `moon #BFD4F5` `wardgray #B9CFC8` `wood #C99A6B` `white #FFFFFF` `lamp #FFC968`


## 主件 Hero

| 编号 | 名称 | 区域 | 尺寸 W×D×H (m) | 面数 | 动画/枢轴 | 色板槽 | 三视图 | 设计稿 |
|---|---|---|---|---|---|---|---|---|
| H01 | 弹出立体城堡 | z04,z10 | 16×10×18 | 6,000 | 整体@书页折缝(底边中线):DROP 一拍弹起：0→1 竖起 + 回弹；塔楼×5@各塔底:依次 scale-y 弹出(相差 1/8 拍)；旗帜@旗杆顶:随拍摆动 ±15°；窗@—:自发光随拍脉冲 | blush lavender cream gold lamp pink | ⚠ 34% | [sheet](H01_popup_castle/sheet.jpg) |
| H02 | 抱心巨兔 | z04 | 6×5×10 | 4,000 | 整体@底座铰接:DROP 弹起；耳朵×2@头顶耳根:每句 'Oh my god' 弹立 + 回弹；爱心@爱心中心:每拍 scale 1→1.12 | cream blush pink white gold | ✓ 10% | [sheet](H02_giant_bunny_heart/sheet.jpg) |
| H03 | 兔子旋转木马 | z08,z10 | 9×9×9 | 6,000 | 平台+顶棚@中心柱 Y 轴:匀速旋转，副歌加速；兔子座椅×6@各立杆:交替上下浮动(每拍)；灯泡@—:跑马灯随拍 | magenta gold cream pink cyan lamp | ✓ 3% | [sheet](H03_bunny_carousel/sheet.jpg) |
| H04 | 爱心摩天轮 | z08 | 10×4×13 | 6,000 | 轮框+辐条@轮毂(水平轴):慢速旋转；吊舱×8@各挂点:反向旋转保持竖直，随拍轻晃；灯泡@—:沿轮框追光随拍 | magenta gold cream cyan plum lamp | ⚠ 26% | [sheet](H04_heart_ferris_wheel/sheet.jpg) |
| H05 | 纸灯笼塔 | z04,z08 | 3×3×9 | 2,500 | 灯笼×12@各挂绳顶:随拍摆动 ±8°；灯笼发光@—:每拍换色(粉→金→青)；塔架@底:静态 | pink gold lavender cream lamp magenta | ✓ 10% | [sheet](H05_lantern_tower/sheet.jpg) |
| H06 | 书页爱心终点门 | z10 | 12×3×11 | 5,000 | 左右书页@底部铰接:入场时由平放卷起成心形；灯泡@—:依次点亮，最后一击全亮；小兔×2@底:最后一击跳起 | cream gold pink blush lamp white | ✓ 24% | [sheet](H06_heart_finish_gate/sheet.jpg) |
| H07 | 五只兔子一家 | z10 | 8×2×3 | 4,000 | 每只兔@脚底:底鼓依次跳起 0.3 m；手臂@肩部:挥手 ±30°/拍；耳朵@耳根:落地时抖动 | mint blush lavender sun sky cream | ⚠ 29% | [sheet](H07_bunny_family/sheet.jpg) |
| H08 | 纸彩带礼炮 | z04,z08,z10 | 3×2×2.5 | 1,800 | 炮管@炮耳轴:发射时后坐 0.2 m + 抬头；彩纸@炮口:粒子爆发(实例化)；底座@—:静态 | cream pink gold lavender magenta | ⚠ 30% | [sheet](H08_confetti_cannon/sheet.jpg) |
| H09 | 巨书封面 | z01 | 14×10×1.5 | 3,000 | 封面@书脊铰接:开场第一拍 0→180° 翻开；书页@书脊:翻页转场时整页翻过；徽章@—:金光扫过 | mint pearl gold cream foil | ✓ 6% | [sheet](H09_book_cover/sheet.jpg) |
| H10 | 立体纸病床+纸帘 | z03 | 3×2×2.4 | 2,000 | 纸帘@各折痕:每 4 小节展开/收起；病床@底部折缝:拉片抬起；床头灯@—:黄昏暖光闪烁 | wardgray cream coral lamp white | ✓ 15% | [sheet](H10_ward_bed_set/sheet.jpg) |
| H11 | 纸时钟塔 | z03 | 3×3×9 | 2,500 | 时针/分针@钟面中心:每拍跳一格；兔耳@耳根:小节首轻摆；窗@—:暖光 | wardgray cream gold coral lamp | ✓ 13% | [sheet](H11_clock_tower/sheet.jpg) |
| H12 | 纸艺翻盖手机 | z06,z10 | 2.5×1.5×5 | 2,000 | 上盖@铰链:随拍开合 0↔150°；屏幕@—:开盖时亮爱心；天线@顶:转场时伸长 | coral cream pink peach mint | ⚠ 40% | [sheet](H12_flip_phone_sculpture/sheet.jpg) |
| H13 | 巨型翻盖手机塔 | z06 | 5×3×12 | 4,000 | 上盖@铰链:乐句开合；天线@顶:→07 转场伸长成塔尖；电话线@—:长音时摇摆 | coral cream pink lavender gold | ⚠ 35% | [sheet](H13_phone_tower/sheet.jpg) |
| H14 | 螺旋纸塔 | z07,z10 | 4×4×14 | 3,500 | 整体@塔基一侧:pre2 最后一小节向外倒下；窗@—:随拍闪烁；顶星@—:旋转 | lilac white lavender gold indigo | ✓ 10% | [sheet](H14_spiral_paper_tower/sheet.jpg) |
| H15 | 兔子帆纸船 | z05 | 3×1.4×3 | 1,500 | 整体@船身中心:随拍上下浮动 + 横摇 ±5°；船头灯@—:hook 处亮 | pearl lilac moon lamp gold | ✓ 19% | [sheet](H15_bunny_sail_boat/sheet.jpg) |
| H16 | 湖心纸亭 | z05 | 5×5×6 | 3,000 | 灯笼@挂点:轻摆 + 柔光；整体@—:静态 | pearl moon lilac gold lamp | ✓ 6% | [sheet](H16_lake_pavilion/sheet.jpg) |
| H17 | 兔子村风车 | z02 | 4×3×9 | 3,000 | 风帆@轮毂(水平轴):匀速旋转，副歌加速；兔耳@耳根:小节首摆动 | coral cream sun green wood | ⚠ 35% | [sheet](H17_bunny_windmill/sheet.jpg) |
| H18 | 蘑菇下读书兔 | z09 | 3×3×3.5 | 2,500 | 书页@书脊:bridge 处翻页；兔耳@耳根:乐句抖动；台灯@—:暖光呼吸 | teal cream lamp mint navy | ✓ 22% | [sheet](H18_reading_bunny/sheet.jpg) |
| H19 | 纸太阳 | z10 | 8×1×8 | 2,000 | 光芒@日轮中心:慢速旋转；日轮@中心:每小节 scale 脉冲；整体@底:终章升起 | sun gold pink peach cream | ✓ 14% | [sheet](H19_paper_sun/sheet.jpg) |

## 标准道具 Props

| 编号 | 名称 | 区域 | 尺寸 W×D×H (m) | 面数 | 动画/枢轴 | 色板槽 | 三视图 | 设计稿 |
|---|---|---|---|---|---|---|---|---|
| P01 | 兔耳小屋 | z02,z10 | 3×3×4 | 1,500 | 兔耳@耳根:乐句摆动；烟囱纸云@烟囱口:底鼓冒出 | coral cream sun green | ✓ 11% | [sheet](P01_bunny_cottage/sheet.jpg) |
| P02 | 纸蘑菇屋 | z02 | 2.5×2.5×3 | 1,000 | 伞盖@菌柄顶:每拍轻压缩回弹 | coral cream sun green | ✓ 1% | [sheet](P02_mushroom_house/sheet.jpg) |
| P03 | 郁金香花圃 | z02 | 3×1.5×0.8 | 800 | 郁金香@茎底:军鼓依次弹起 | sun coral white green | ⚠ 27% | [sheet](P03_tulip_bed/sheet.jpg) |
| P04 | 圆冠纸树 | z01,z02,z04,z06,z10 | 2×2×3.5 | 600 | 整体@根部:每 4 小节一组“啪”地立起 | mint green blush wood | ✓ 5% | [sheet](P04_paper_tree_round/sheet.jpg) |
| P05 | 折纸松树 | z07,z09,z03 | 1.6×1.6×4 | 400 | 整体@根部:乐句开头依次立起 | teal mint wood | ✓ 6% | [sheet](P05_paper_pine/sheet.jpg) |
| P06 | 坐兔雕像 | z01,z02 | 1.6×1.4×2.4 | 1,200 | 耳朵@耳根:随拍轻抖 | pearl blush mint green | ✓ 6% | [sheet](P06_sitting_bunny/sheet.jpg) |
| P07 | 心形点滴架 | z03 | 0.8×0.8×2.2 | 500 | 点滴袋@挂钩:随拍轻晃+微光 | coral blush wardgray cream | ✓ 11% | [sheet](P07_heart_iv_stand/sheet.jpg) |
| P08 | 纸帘屏风 | z03 | 2×0.6×2 | 400 | 帘片@折痕:展开/收起 | wardgray cream white | ⚠ 51% | [sheet](P08_curtain_screen/sheet.jpg) |
| P09 | 拉片机关 | z03,z07 | 1.5×0.3×1.2 | 300 | 拉手@滑条:每小节拉出→场景抬起 | cream gold coral | ✓ 25% | [sheet](P09_pull_tab/sheet.jpg) |
| P10 | 纸灯笼串 | z04,z10 | 6×0.5×2 | 900 | 灯笼@挂点:轻摆；随拍明暗 | pink gold lavender lamp | ⚠ 29% | [sheet](P10_lantern_string/sheet.jpg) |
| P11 | 爱心纸雕 | z04,z08 | 1.5×0.6×1.6 | 500 | 爱心@中心:'Oh my god' 时弹出放大 | pink gold cream | ✓ 18% | [sheet](P11_heart_sculpture/sheet.jpg) |
| P12 | 纸礼盒 | z04,z08 | 0.8×0.8×0.8 | 300 | 盒盖@后边铰接:drop 时弹开 | lavender pink gold | ✓ 7% | [sheet](P12_gift_box/sheet.jpg) |
| P13 | 纸睡莲灯 | z05 | 1.2×1.2×0.8 | 500 | 莲花@中心:hook 处同时亮起 | blush pearl mint lamp | ✓ 9% | [sheet](P13_lily_lantern/sheet.jpg) |
| P14 | 吊线弯月 | z05,z03,z07 | 3×0.4×4 | 600 | 整体@吊线顶:慢摆 ±6° | gold moon cream | ⚠ 54% | [sheet](P14_crescent_moon/sheet.jpg) |
| P15 | 电话线藤蔓拱门 | z06 | 4×0.6×3.5 | 1,200 | 藤蔓@两脚:长音时摇摆；花@—:依次开放 | pink mint coral cream | ✓ 24% | [sheet](P15_phone_cord_arch/sheet.jpg) |
| P16 | 爱心花圃 | z06 | 2.5×1.5×0.9 | 800 | 花头@茎顶:依次开放 | coral pink lavender mint | ✓ 22% | [sheet](P16_heart_flower_bed/sheet.jpg) |
| P17 | 星星风铃 | z07 | 1.5×1.5×2.5 | 600 | 星星@各吊线:随拍闪+轻转 | gold lilac cream | ⚠ 35% | [sheet](P17_star_mobile/sheet.jpg) |
| P18 | 纸楼梯段 | z07 | 3×1.2×2 | 400 | 整体@—:静态 | lilac white gold | ⚠ 39% | [sheet](P18_paper_stairs/sheet.jpg) |
| P19 | 气球束 | z08,z10 | 1.2×1.2×3.5 | 500 | 气球@绳端:摇摆；部分上升离场 | magenta cyan gold pink | ✓ 7% | [sheet](P19_balloon_bunch/sheet.jpg) |
| P20 | 嘉年华小摊 | z08 | 3×2×3.2 | 1,500 | 灯串@—:随拍闪；招牌@—:脉冲 | magenta gold cream cyan | ✓ 13% | [sheet](P20_carnival_stall/sheet.jpg) |
| P21 | 三角旗串 | z08,z02 | 5×0.2×1 | 300 | 旗@挂绳:随拍摆动 | magenta gold cyan | ⚠ 92% | [sheet](P21_flag_string/sheet.jpg) |
| P22 | 萤火纸灯 | z09 | 0.6×0.6×1.4 | 200 | 灯@茎顶:随拍明灭 | lamp gold teal | ✓ 12% | [sheet](P22_firefly_lantern/sheet.jpg) |
| P23 | 树桩书堆 | z09 | 1.2×1.2×1 | 500 | 烛光@—:闪烁 | wood teal cream lamp | ✓ 4% | [sheet](P23_stump_books/sheet.jpg) |
| P24 | 纸云 | z01,z02,z06,z10 | 4×1.5×2 | 300 | 整体@中心:缓慢漂移 | white pearl fog | ⚠ 28% | [sheet](P24_paper_cloud/sheet.jpg) |
| P25 | 纸山片 | z01,z10 | 6×3×2.5 | 400 | 整体@底边:翻页时立起 | mint green pearl | ✓ 19% | [sheet](P25_paper_hill/sheet.jpg) |
| P26 | 书页墙 | z09,z10 | 8×1×5 | 800 | 书页@底边:149.3s 两侧合拢 | cream gold navy | ✓ 20% | [sheet](P26_page_wall/sheet.jpg) |
| P27 | 纸蘑菇组 | z02,z09,z01 | 1×1×0.8 | 300 | 伞盖@菌柄顶:每拍轻跳 | coral teal cream | ✓ 15% | [sheet](P27_mushroom_small/sheet.jpg) |

## 地被 / 小件 / 路面套件（共享设计稿）

| 设计稿 | 内容（≈尺寸 m / 面数） |
|---|---|
| [G1_ground_plants](G1_ground_plants/sheet.jpg) 地被·植物 | 纸草丛(0.4/60)、五瓣小纸花(0.3/80)、单支郁金香(0.4/90)、爱心小花(0.35/90)、小蘑菇(0.3/70)、三叶草片(0.4/60)、芦苇丛(0.8/120)、折纸蕨(0.6/120) |
| [G2_ground_stones](G2_ground_stones/sheet.jpg) 地被·石头与碎片 | 卵石(0.3/40)、踏石(0.6/30)、苔石(0.5/80)、岸石(1/120)、纸屑(0.2/8)、星点地贴(0.4/8)、金箔片(0.15/8)、纸波纹片(1/24) |
| [G3_sky_small_anim](G3_sky_small_anim/sheet.jpg) 天空与小动画 | 吊线星星(0.8/40)、大纸星(1.2/60)、小云朵(1.5/80)、花瓣(0.1/2)、纸蝴蝶(0.2/8)、萤火虫(0.05/2)、书页飞鸟(0.4/16)、彩纸(心/星/条)(0.08/2) |
| [G4_road_kit](G4_road_kit/sheet.jpg) 路面套件 | 纸带直路块(2.2/12)、纸带转角块(2.2/20)、金箔包边(2.2/16)、纸木板桥块(2.2/120)、浮桥块(2.2/80)、书页条路块(2.2/40)、嘉年华亮边(2.2/24) |

合计：主件 19 件、标准道具 27 件、地被/小件/路面 31 种（4 张共享稿）。
