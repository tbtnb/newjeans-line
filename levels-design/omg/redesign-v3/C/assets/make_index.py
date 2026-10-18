# assets/ASSETS.md (Chinese table) + deliverables/omg-redesign/C/assets-index.jpg
import sys, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
H = Path(__file__).parent; R = H.parents[4]; sys.path.insert(0, str(H))
from assets_c import ASSETS, GROUND, ATLAS
FB = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; FR = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
f = lambda s, b=False: ImageFont.truetype(FB if b else FR, s)
def chk(id):
    p = H / id / 'spec.json'
    if not p.exists(): return None
    return json.loads(p.read_text()).get('views_check')
L = ['# OMG 方案 C · 资产清单与建模设计稿\n\n', '> 设计阶段（不改游戏代码）。每件主件/标准道具一张建模设计稿：3/4 插图 + 正/侧/俯三视图（同一比例、网格、尺寸线、比例尺）+ 细节部件 + 色板槽 + 面数预算 + 枢轴/动画；地被与小件按 7–8 件一张共享设计稿。\n',
     '> 渲染：Codex（Mac mini，gpt-6.1-sol，high）；合成脚本 `build_sheets.py`；数据 `assets_c.py`；每件目录 `assets/<id>/`（sheet.jpg、hero/views/front/side/top/parts.jpg、spec.json、prompts.md）。\n',
     '> 单位：游戏单位 m（路宽 ≈2.2，线头 1）。面数：主件 2–8k，道具 200–1.5k，地被 2–200。三视图一致性由脚本自动测量（正/侧高度、正/俯宽度、侧/俯深度的像素差，≤25% 记 ✓）。\n\n',
     '## 共享色板图集\n\n', ' '.join(f'`{k} {v}`' for k, v in ATLAS.items()), '\n\n']
for cls, title in (('hero', '## 主件 Hero'), ('prop', '## 标准道具 Props')):
    L.append(f'\n{title}\n\n| 编号 | 名称 | 区域 | 尺寸 W×D×H (m) | 面数 | 动画/枢轴 | 色板槽 | 三视图 | 设计稿 |\n|---|---|---|---|---|---|---|---|---|\n')
    for a in [x for x in ASSETS if x['cls'] == cls]:
        c = chk(a['id']); cs = '—' if not c else ('✓' if c['ok'] else '⚠') + f" {max(c['consistency'].values()):.0%}"
        an = '；'.join(f'{p}@{q}:{m}' for p, q, m in a['pivots'])
        L.append(f"| {a['id'].split('_')[0]} | {a['cn']} | {','.join(a['zones'])} | {'×'.join(f'{v:g}' for v in a['size'])} | {a['tris']:,} | {an} | {' '.join(a['colors'])} | {cs} | [sheet]({a['id']}/sheet.jpg) |\n")
L.append('\n## 地被 / 小件 / 路面套件（共享设计稿）\n\n| 设计稿 | 内容（≈尺寸 m / 面数） |\n|---|---|\n')
for g in GROUND: L.append(f"| [{g['id']}]({g['id']}/sheet.jpg) {g['cn']} | {'、'.join(f'{c}({s:g}/{t})' for e, c, s, t in g['items'])} |\n")
nh = sum(1 for a in ASSETS if a['cls'] == 'hero'); npr = len(ASSETS) - nh; ng = sum(len(g['items']) for g in GROUND)
L.append(f'\n合计：主件 {nh} 件、标准道具 {npr} 件、地被/小件/路面 {ng} 种（{len(GROUND)} 张共享稿）。\n')
(H / 'ASSETS.md').write_text(''.join(L))
# index board
items = [(a['id'], a['cn'], a['cls'], H / a['id'] / 'hero.jpg') for a in ASSETS] + [(g['id'], g['cn'], 'ground', H / g['id'] / 'kit.jpg') for g in GROUND]
cols, tw = 10, 228; th = tw + 58; W = 40 + cols * (tw + 8); rows = (len(items) + cols - 1) // cols; Hh = 150 + rows * (th + 10) + 20
img = Image.new('RGB', (W, Hh), '#1c1e2a'); d = ImageDraw.Draw(img)
d.text((30, 22), 'OMG 方案 C · 资产索引（建模设计稿）', font=f(46, True), fill='#f2f2f8')
d.text((30, 86), f'主件 {nh} · 标准道具 {npr} · 地被/小件/路面 {ng} 种（{len(GROUND)} 张共享稿）　金框=主件  蓝框=道具  绿框=地被套件　每件详见 levels-design/omg/redesign-v3/C/assets/<id>/sheet.jpg', font=f(22), fill='#aeb2c8')
col = dict(hero='#ffd27a', prop='#9fd8ff', ground='#9ed8c8')
for i, (id, cn, cls, p) in enumerate(items):
    x = 30 + (i % cols) * (tw + 8); y = 150 + (i // cols) * (th + 10)
    d.rectangle([x, y, x + tw, y + tw], fill='#2a2d3c')
    if p.exists(): im = Image.open(p).convert('RGB'); im.thumbnail((tw - 8, tw - 8)); img.paste(im, (x + (tw - im.width) // 2, y + (tw - im.height) // 2))
    d.rectangle([x, y, x + tw, y + tw], outline=col[cls], width=3)
    d.text((x + 2, y + tw + 6), id.split('_')[0], font=f(18, True), fill=col[cls]); d.text((x + 48, y + tw + 6), cn, font=f(18, True), fill='#f2f2f8')
out = R / 'deliverables/omg-redesign/C/assets-index.jpg'; img.save(out, quality=86); print(out, img.size, out.stat().st_size // 1024, 'KB')
