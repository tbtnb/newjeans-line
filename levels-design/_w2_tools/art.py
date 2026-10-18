"""copy generated art into <slug>/art/: art.py slug src name [alpha]  (alpha: near-white -> transparent PNG)"""
import sys
from PIL import Image
slug,src,name=sys.argv[1:4]; alpha=len(sys.argv)>4
from pathlib import Path
d=Path(f'/workspace/newjeans-line-designs/{slug}/art'); d.mkdir(parents=True,exist_ok=True)
im=Image.open(src).convert('RGB'); im.thumbnail((1536,1536))
if alpha:
    im=im.convert('RGBA'); px=im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r,g,b,a=px[x,y]; m=min(r,g,b)
            if m>238: px[x,y]=(r,g,b,int(max(0,(255-m)*255/17)))
    im.save(d/f'{name}.png',optimize=True)
else: im.save(d/f'{name}.jpg',quality=86,optimize=True)
print(d, im.size)
