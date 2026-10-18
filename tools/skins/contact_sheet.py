#!/usr/bin/env python3
"""deliverables/skins-contact.png from tools/qa/skin-shots.mjs output (deliverables/skins/)."""
import os, json
from PIL import Image, ImageDraw, ImageFont
D = 'deliverables/skins'
rep = json.load(open(f'{D}/report.json'))
fp = [p for p in ['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc'] if os.path.exists(p)]
F = ImageFont.truetype(fp[0], 22) if fp else ImageFont.load_default(); Fs = ImageFont.truetype(fp[0], 16) if fp else F
names = {'classic': '经典 Classic', 'bunny': '兔兔 Bunny', 'denim': 'Y2K 牛仔 Denim', 'bubble-gum': '泡泡糖 Bubble Gum', 'phoning': '翻盖机 Phoning', 'film': 'Ditto 胶片 Film', 'supernatural': '超自然铬 Supernatural'}
w, h = 270, 480; cw = w + 8; cs = w
play = rep['play']
top = Image.new('RGB', (cw * len(play) + 8, 40 + 2 * (cs + 30) + (h + 30) + 10), '#f4f1ea'); d = ImageDraw.Draw(top)
for i, r in enumerate(play):
    x = 8 + i * cw
    d.text((x, 8), names.get(r['skin'], r['skin']), fill='#2c2a28', font=F)
    for j, (k, c, lab) in enumerate([('turnShot', 'turnClip', '转弯 turn +0.16s (head crop)'), ('deathShot', 'deathClip', '死亡 shatter (head crop)')]):
        y = 40 + j * (cs + 30); b = r[c]; im = Image.open(r[k]).convert('RGB').crop((b['x'], b['y'], b['x'] + b['width'], b['y'] + b['height']))
        im.save(r[k].replace('.png', '-head.png'))
        top.paste(im.resize((cs, cs)), (x, y + 22)); d.text((x, y), lab, fill='#77706a', font=Fs)
    y = 40 + 2 * (cs + 30)
    top.paste(Image.open(r['turnShot']).convert('RGB').resize((w, h)), (x, y + 22)); d.text((x, y), '全屏 full frame (turn)', fill='#77706a', font=Fs)
pk = rep['picker']; ph = 360
ims = [Image.open(p['path']).convert('RGB') for p in pk]; ims = [im.resize((int(im.width * ph / im.height), ph)) for im in ims]
bw = sum(im.width + 12 for im in ims) + 8
bot = Image.new('RGB', (max(bw, top.width), ph + 50), '#f4f1ea'); d2 = ImageDraw.Draw(bot); x = 8
for p, im in zip(pk, ims):
    d2.text((x, 8), f"picker {p['name']} {p['w']}x{p['h']}", fill='#2c2a28', font=Fs); bot.paste(im, (x, 36)); x += im.width + 12
S = Image.new('RGB', (max(top.width, bot.width), top.height + bot.height), '#f4f1ea'); S.paste(top, (0, 0)); S.paste(bot, (0, top.height))
S.save('deliverables/skins-contact.png', optimize=True); print(S.size)
