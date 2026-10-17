# NewJeans Line — 关卡设计约束

设计阶段：2026-10-18。先完成歌曲研究、16 关设计和五套视觉参考，再继续代码与建模。已有初稿作为交互验证底座；其通用场景方案不作为最终美术方向。

## 已确定范围

- 精确曲目顺序：Attention、Hype Boy、Cookie、Hurt、OMG、Ditto、New Jeans、Super Shy、ETA、Cool With You、Get Up、ASAP、How Sweet、Bubble Gum、Supernatural、Right Now。
- 全部为完整演唱版。歌曲原文件不修改。网页音频单曲按需加载。
- Babylon.js 管理真实 3D 场景、模型、材质、镜头、动画和资源生命周期；最终移除 Three.js。
- 点击/触摸/空格进行一次 90° 转弯，音乐驱动连续前进；错过或过早转弯失败；暂停、重试、练习、皇冠、钻石和通关记录完整。
- 手机竖屏优先，桌面和横屏可玩。音乐、谱面和全部资产静态部署，成绩与设置在浏览器本地保存，可导入/导出。
- 新建 GitHub 仓库并部署 GitHub Pages。用户已授权，不增加确认步骤。

## 美术依据

参考图提取自用户音频内嵌的五张实际专辑封面，并与官方发行资料交叉核对。不是凭歌曲名任意挑选森林、沙漠或糖果主题。

| 作品 | 封面中的明确视觉 | 在关卡中的转化原则 |
| --- | --- | --- |
| New Jeans (2022) | 蓝白网点、兔子、丹宁色、粗大字形 | 蓝白城市与纸片建筑、网点只在远景/标识上使用、兔耳门和唱片轮廓 |
| OMG | 红白网点兔子，与首专构图呼应 | 酒红/奶白的纸片城市与记忆走廊；OMG 更活泼，Ditto 更克制、带冬日色温 |
| Get Up | 像素小人、糖果色尾迹、蓝天背景、游戏画面 | 真正 3D 的体素岛、像素星星/心形/窗口，六首分别设计动势与场景故事 |
| How Sweet | 黑色唱片包装边框、珊瑚橙字、胶片摄影、街头服饰 | 黑胶/磁带/街道/海风，奶油与牛仔蓝为底，珊瑚橙为点睛；不做字面糖果乐园 |
| Supernatural | 黑底、白色兔脸、轮廓线、彩色花瓣 | 墨蓝/黑色背景中的白路和彩色花瓣、圆形图案与 90 年代舞曲都市；避免无关的赛博霓虹堆砌 |

## 玩法视觉准则

《跳舞的线》的参考重点是：干净的低多边形世界、连续直角路线、立体细线、先可预读后到来的道路、克制的俯视跟随镜头、随音乐展开的场景段落。保留近处道路可读性，不把画面做成无止境随机方块跑道。

每首歌必须有自己的起点、展开、高潮及收束。每关至少一个特有地标和一个与歌曲有关的微小彩蛋；同专辑共享配色和材质，但不能仅换颜色。彩蛋在道路外出现，不要求误入岔路，不影响成绩；重复游玩仍可发现。

镜头不突然翻转或摇晃。拐点前约 1.5–2.5 秒的道路应可见；装饰不能遮住玩家、下个拐角或收集物。皇冠设在可辨认的检查点地标，钻石的画面位置与实际进度一致。

## 音乐和手感准则

转弯要落在听得见的节拍、清晰起音或可理解的旋律重音上。不能简单把平均 BPM 等距铺满，也不能为了增加难度乱加转弯。短曲 Get Up 保留呼吸感；快曲用重复节奏动机教会玩家后再变化。

使用音频时钟作为唯一时间依据。细化起音检测前，先用已知时间的合成瞬态标定分析工具自身的延迟；按歌曲开头/中段/末尾检查误差，区分固定偏移、累积漂移和弱起音的不确定性。不能把算法自检当作真人听感验收。

最终验证包括：16 首完整谱面确定性通关、正常与练习模式全曲浏览器实播、早/晚/重复输入失败、暂停续播、音频加载失败恢复、结尾完整播放、手机触摸、存档刷新及导入/导出。最终证据必须基于 Babylon.js 版本。

## 来源

- [Dancing Line 官方 App Store 介绍](https://apps.apple.com/us/app/dancing-line-music-game/id1177953618)
- [Dancing Line 官方 TapTap](https://www.taptap.cn/app/31429)
- [经典移动版界面截图](https://www.elespanol.com/elandroidelibre/aplicaciones/juegos/20170505/dancing-line-nuevo-musical-creadores-piano-tiles/213729439_0.html)
- [Get Up 官方 POWERPUFF GIRLS 版本](https://shop.newjeans-official.us/products/newjeans-2nd-ep-get-up-the-powerpuff-girls-x-nj-box-ver)
- [Get Up Apple Music 专辑介绍](https://music.apple.com/us/album/newjeans-2nd-ep-get-up/1695951888)
- [How Sweet 官方发行资料](https://www.newjeans.jp/news/dwmgij)
- [Supernatural 官方发行资料](https://www.newjeans.jp/discography/fqrwmw)
- [Babylon.js 官方 ES 模块文档](https://doc.babylonjs.com/setup/frameworkPackages/es6Support/)
