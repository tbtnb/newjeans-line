"""Procedural level art (PIL) for w2 songs. usage: artgen.py slug   -> /workspace/newjeans-line-designs/<slug>/art/*
Flat / halftone / pixel illustrations in each level's palette. No text, no faces, no arrows (nothing that can read as a tap hint)."""
import sys, math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
slug=sys.argv[1]; OUT=Path(f'/workspace/newjeans-line-designs/{slug}/art'); OUT.mkdir(parents=True,exist_ok=True)
R=random.Random(7)
def hx(c): c=c.lstrip('#'); return tuple(int(c[i:i+2],16) for i in (0,2,4))
def lerp(a,b,f): return tuple(int(a[i]+(b[i]-a[i])*f) for i in range(3))
def grad(w,h,top,bot,glow=None):
    im=Image.new('RGB',(w,h)); d=ImageDraw.Draw(im); t,b=hx(top),hx(bot)
    for y in range(h): d.line([(0,y),(w,y)],fill=lerp(t,b,y/(h-1)))
    if glow:
        g=Image.new('L',(w,h),0); gd=ImageDraw.Draw(g); gd.ellipse([w*0.2,h*0.72,w*0.8,h*0.9],fill=110); g=g.filter(ImageFilter.GaussianBlur(60))
        im=Image.composite(Image.new('RGB',(w,h),hx(glow)),im,g)
    return im
def halftone_blob(im,cx,cy,rx,ry,col,step=10,maxr=3.6,alpha=1.0):
    d=ImageDraw.Draw(im)
    for y in range(int(cy-ry),int(cy+ry),step):
        for x in range(int(cx-rx),int(cx+rx),step):
            q=((x-cx)/rx)**2+((y-cy)/ry)**2
            if q<1:
                r=maxr*(1-q)**0.5*alpha
                if r>0.4: d.ellipse([x-r,y-r,x+r,y+r],fill=col)
def save(im,name,png=False):
    if png: im.save(OUT/f'{name}.png',optimize=True)
    else: im.convert('RGB').save(OUT/f'{name}.jpg',quality=88,optimize=True)
    print(' art', name, im.size)
def tile_halftone(bg,dot,n=512,step=16,amp=0.35):
    im=Image.new('RGB',(n,n),hx(bg)); d=ImageDraw.Draw(im)
    for y in range(0,n,step):
        for x in range(0,n,step):
            f=0.5+0.5*math.sin(2*math.pi*x/n)*math.cos(2*math.pi*y/n)
            r=1.2+amp*step*0.25*f; xo=(step/2 if (y//step)%2 else 0)
            for dx in (0,-n):
                d.ellipse([x+xo+dx-r,y-r,x+xo+dx+r,y+r],fill=hx(dot))
    return im
def grid_tile(bg,line,n=512,cell=32,major=4):
    im=Image.new('RGB',(n,n),hx(bg)); d=ImageDraw.Draw(im)
    for i in range(0,n,cell):
        w=2 if (i//cell)%major==0 else 1
        d.line([(i,0),(i,n)],fill=hx(line),width=w); d.line([(0,i),(n,i)],fill=hx(line),width=w)
    return im
def pixel_cloud(d,x,y,s,col):
    for (cx,cy,w,h) in [(0,1,6,2),(1,0,3,1),(4,0,1,1)]:
        d.rectangle([x+cx*s,y+cy*s,x+(cx+w)*s-1,y+(cy+h)*s-1],fill=col)
def bunny_shape(d,cx,cy,s,col,face=None):
    d.ellipse([cx-1.1*s,cy-0.6*s,cx+1.1*s,cy+1.6*s],fill=col)          # body
    d.ellipse([cx-0.8*s,cy-1.5*s,cx+0.8*s,cy-0.1*s],fill=col)          # head
    d.ellipse([cx-0.7*s,cy-3.3*s,cx-0.25*s,cy-1.1*s],fill=col)         # ears
    d.ellipse([cx+0.25*s,cy-3.3*s,cx+0.7*s,cy-1.1*s],fill=col)
    if face: d.ellipse([cx-0.5*s,cy-1.1*s,cx+0.5*s,cy-0.35*s],fill=face)   # blank mask, no facial features
def pixel_bunny(d,x,y,s,col):
    rows=["..X...X..","..X...X..","..X...X..",".XXXXXXX.","XXXXXXXXX","XXXXXXXXX",".XXXXXXX.","..XX.XX.."]
    for j,r in enumerate(rows):
        for i,c in enumerate(r):
            if c=='X': d.rectangle([x+i*s,y+j*s,x+(i+1)*s-1,y+(j+1)*s-1],fill=col)
def pixel_flyer(d,x,y,s,col,trail):
    # abstract pixel 'flyer' (a rounded pixel blob with a colour trail) - no face
    for k in range(10): d.rectangle([x-(k+2)*s*1.6,y+s*0.5,x-(k+1)*s*1.6,y+s*1.5],fill=lerp(hx(trail),(255,255,255),k/11))
    blob=[".XXX.","XXXXX","XXXXX",".XXX."]
    for j,r in enumerate(blob):
        for i,c in enumerate(r):
            if c=='X': d.rectangle([x+i*s,y+(j-1)*s,x+(i+1)*s-1,y+j*s-1],fill=hx(col))
def alpha_from_white(im,thr=245):
    im=im.convert('RGBA'); px=im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r,g,b,a=px[x,y]
            if min(r,g,b)>=thr: px[x,y]=(r,g,b,0)
    return im

if slug=='omg':
    im=grad(1536,864,'#CFDCD0','#F3F0E8',glow='#EFA6B1')
    for k in range(6): halftone_blob(im,R.randint(100,1436),R.randint(80,420),R.randint(120,240),R.randint(40,80),hx('#BCCBBE'),step=12,maxr=3.2)
    save(im,'sky')
    save(tile_halftone('#B8C8BC','#9DB0A3'),'ground-halftone')
    im=Image.new('RGB',(768,1024),hx('#F3F0E8')); halftone_blob(im,384,520,330,330,hx('#E7DFCF'),step=14,maxr=5)
    m=Image.new('L',(768,1024),0); bunny_shape(ImageDraw.Draw(m),384,560,150,255)
    dots=Image.new('RGB',(768,1024),hx('#F3F0E8')); dd=ImageDraw.Draw(dots)
    for y in range(0,1024,9):
        for x in range(0,768,9):
            if m.getpixel((x,y)): r=4.2-1.8*(y/1024); dd.ellipse([x-r,y-r,x+r,y+r],fill=hx('#25282B'))
    im=Image.composite(dots,im,m); d=ImageDraw.Draw(im); d.ellipse([384-72,560-165,384+72,560-55],fill=hx('#F3F0E8')); d.polygon([(370,525),(398,525),(384,540)],fill=hx('#EFA6B1'))
    save(im,'bunny-poster')
    im=Image.new('RGB',(576,1024),hx('#25282B')); d=ImageDraw.Draw(im)
    d.polygon([(0,0),(576,0),(576,90),(0,260)],fill=(52,56,60))
    for j,(side,col) in enumerate([(0,'#F3F0E8'),(1,'#EFA6B1'),(0,'#F3F0E8'),(1,'#EFA6B1'),(0,'#F3F0E8')]):
        y=170+j*150; x=60 if side==0 else 236; d.rounded_rectangle([x,y,x+280,y+92],radius=40,fill=hx(col))
    d.rounded_rectangle([200,930,376,990],radius=30,fill=(60,64,68))
    for k in range(3): d.ellipse([238+k*40,950,258+k*40,970],fill=hx('#F3F0E8'))
    save(im,'phone-screen')
    im=Image.new('RGB',(1024,768),(255,255,255)); d=ImageDraw.Draw(im)
    d.polygon([(140,600),(470,600),(520,520),(430,330),(390,330),(330,470),(170,520)],fill=hx('#BFE3EA'),outline=hx('#25282B'))
    d.polygon([(330,470),(390,330),(430,330),(400,470)],fill=hx('#E6F6F8')); d.rectangle([455,520,475,640],fill=hx('#BFE3EA'),outline=hx('#25282B'))
    d.polygon([(560,640),(960,640),(930,700),(590,700)],fill=hx('#F3F0E8'),outline=hx('#788A80'))
    d.ellipse([700,420,860,640],fill=hx('#25282B')); d.ellipse([720,330,830,440],fill=hx('#25282B'))
    d.polygon([(730,350),(745,295),(765,345)],fill=hx('#25282B')); d.polygon([(790,345),(810,295),(825,350)],fill=hx('#25282B'))
    d.line([(850,620),(930,600),(950,560)],fill=hx('#25282B'),width=18)
    save(alpha_from_white(im),'slipper-cat-decal',png=True)
elif slug=='ditto':
    im=grad(1536,864,'#C9D3CF','#EEF0EA',glow='#D8BE93')
    d=ImageDraw.Draw(im)
    for k in range(700): x,y=R.randint(0,1535),R.randint(0,863); r=R.choice([1,1,2]); d.ellipse([x-r,y-r,x+r,y+r],fill=(250,250,248))
    for k in range(14):  # far pine silhouettes, low contrast
        x=R.randint(0,1536); h=R.randint(60,140); d.polygon([(x,780),(x-h*0.35,780),(x,780-h),(x+h*0.35,780)],fill=(196,206,201))
    save(im.filter(ImageFilter.GaussianBlur(1.2)),'sky')
    im=Image.new('RGB',(512,512),hx('#F2F0E7')); d=ImageDraw.Draw(im)
    for k in range(2600): x,y=R.randint(0,511),R.randint(0,511); c=R.randint(222,236); d.point((x,y),fill=(c,c+2,c))
    save(im,'ground-snow')
    im=Image.new('RGB',(1024,640),hx('#272D32')); d=ImageDraw.Draw(im)   # cassette label (no text)
    d.rounded_rectangle([60,60,964,580],radius=30,fill=hx('#F2F0E7')); d.rectangle([60,150,964,230],fill=hx('#C85F65')); d.rectangle([60,230,964,262],fill=hx('#788A80'))
    d.rounded_rectangle([250,300,774,470],radius=80,fill=hx('#272D32'))
    for cx in (370,654): d.ellipse([cx-60,325,cx+60,445],fill=hx('#AEB7BA')); d.ellipse([cx-22,363,cx+22,407],fill=hx('#272D32'))
    save(im,'cassette-label')
    im=Image.new('RGB',(1024,640),hx('#9FB3C6')); d=ImageDraw.Draw(im)   # camcorder flip-screen: rooftop with SIX chairs (egg)
    d.rectangle([0,380,1024,640],fill=hx('#DCE3DF'))
    for k in range(6):
        x=120+k*140; c=hx('#272D32') if k<5 else hx('#C85F65')
        d.rectangle([x,380,x+70,400],fill=c); d.rectangle([x,300,x+12,400],fill=c); d.rectangle([x+58,400,x+66,460],fill=c); d.rectangle([x+4,400,x+12,460],fill=c)
    for y in range(0,640,4): d.line([(0,y),(1024,y)],fill=(255,255,255) if (y//4)%2 else (230,236,240))
    im=Image.blend(im,Image.new('RGB',im.size,hx('#D8BE93')),0.12)
    d=ImageDraw.Draw(im); d.ellipse([940,40,980,80],fill=(220,60,60))
    save(im,'camcorder-screen')
    im=Image.new('RGB',(900,900),(255,255,255)); d=ImageDraw.Draw(im)   # deer silhouette decal
    c=hx('#788A80'); d.ellipse([260,380,660,600],fill=c); d.rectangle([300,560,330,800],fill=c); d.rectangle([590,560,620,800],fill=c); d.rectangle([380,570,405,790],fill=c); d.rectangle([520,570,545,790],fill=c)
    d.polygon([(600,420),(650,260),(700,250),(690,300),(640,440)],fill=c); d.ellipse([650,210,760,290],fill=c)
    for s in (-1,1):
        x0=690+s*10; d.line([(x0,220),(x0+s*40,130),(x0+s*80,100)],fill=c,width=12); d.line([(x0+s*30,150),(x0+s*70,160)],fill=c,width=10)
    save(alpha_from_white(im),'deer-decal',png=True)
    im=Image.new('RGB',(1024,1024),hx('#F2F0E7'))   # halftone bunny relief (OMG cover motif, used as wall relief)
    m=Image.new('L',im.size,0); bunny_shape(ImageDraw.Draw(m),512,580,170,255)
    dd=ImageDraw.Draw(im)
    for y in range(0,1024,11):
        for x in range(0,1024,11):
            r=4.6 if m.getpixel((x,y)) else 1.3
            dd.ellipse([x-r,y-r,x+r,y+r],fill=hx('#272D32') if m.getpixel((x,y)) else hx('#C9CFC9'))
    save(im,'halftone-bunny-relief')
elif slug=='new-jeans':
    im=grad(1536,864,'#BFE9FA','#F3FBFF'); d=ImageDraw.Draw(im)
    for k in range(9): pixel_cloud(d,R.randint(0,1400),R.randint(40,500),R.choice([14,18,22]),(250,253,255))
    save(im,'sky')
    save(grid_tile('#E9F7FD','#BFE3F2'),'ground-graph-paper')
    im=Image.new('RGB',(1280,720),hx('#73D5EB')); d=ImageDraw.Draw(im)   # pixel billboard: five abstract pixel flyers with colour trails
    for i in range(0,1280,40):
        for j in range(0,720,40):
            if (i//40+j//40)%7==0: d.rectangle([i,j,i+39,j+39],fill=(124,218,238))
    cols=[('#F36BA5','#FFB3D2'),('#397FC0','#9CC7EE'),('#8FDFB7','#C9F1DD'),('#F5CA63','#FBE3A6'),('#B7A0EA','#DACFF6')]
    for k,(c,t) in enumerate(cols): pixel_flyer(d,700+k*90,140+k*100,26,c,t)
    pixel_bunny(d,60,40,10,(255,255,255))
    save(im,'pixel-billboard')
    im=Image.new('RGB',(512,512),hx('#FFF9ED')); d=ImageDraw.Draw(im)   # bunny-gate face
    d.rectangle([0,0,511,511],outline=hx('#397FC0'),width=24); pixel_bunny(d,166,150,20,hx('#164A63'))
    save(im,'bunny-gate-face')
    im=Image.new('RGB',(1600,400),(255,255,255)); d=ImageDraw.Draw(im)   # five-colour trail decal (flat on ground)
    for k,(c,t) in enumerate(cols):
        y=40+k*70
        for s in range(40): d.rectangle([40+s*38,y,40+s*38+30,y+44],fill=lerp(hx(c),(255,255,255),s/44))
    save(alpha_from_white(im,250),'five-trails-decal',png=True)
elif slug=='super-shy':
    im=grad(1536,864,'#B9E4EA','#EAF8F6'); d=ImageDraw.Draw(im)
    for k in range(7): pixel_cloud(d,R.randint(0,1400),R.randint(40,420),R.choice([14,18]),(248,253,253))
    for k in range(22):   # far city, low contrast
        x=k*72+R.randint(-10,10); h=R.randint(60,170); d.rectangle([x,864-h,x+60,864],fill=(196,226,228))
    save(im,'sky')
    im=Image.new('RGB',(512,512),hx('#BEE9C9')); d=ImageDraw.Draw(im)   # park cobbles
    for j in range(0,512,32):
        for i in range(0,512,32):
            o=16 if (j//32)%2 else 0; c=lerp(hx('#BEE9C9'),hx('#A9DDB7'),R.random()*0.8)
            d.rounded_rectangle([i+o-14,j+2,i+o+14,j+30],radius=8,fill=c)
            d.rounded_rectangle([i+o-14+512,j+2,i+o+14+512,j+30],radius=8,fill=c)
    save(im,'ground-park')
    im=Image.new('RGB',(512,512),hx('#FFF8ED')); d=ImageDraw.Draw(im)  # market awning stripes
    for i in range(0,512,64): d.rectangle([i,0,i+31,511],fill=hx('#F4A39B'))
    for i in range(0,512,64): d.pieslice([i-0,470,i+64,560],180,360,fill=hx('#F4A39B') if (i//64)%2==0 else hx('#FFF8ED'))
    save(im,'awning-stripes')
    im=Image.new('RGB',(1280,640),hx('#3B8A89')); d=ImageDraw.Draw(im)  # five-colour pixel relief (cover motif)
    for i in range(0,1280,32):
        for j in range(0,640,32):
            if (i//32*3+j//32)%5==0: d.rectangle([i,j,i+31,j+31],fill=(70,150,149))
    cols=[('#295BE7','#9DB4F4'),('#8FDFB7','#CBF2DE'),('#FF82D0','#FFC6EA'),('#F7CE63','#FBE6AE'),('#B1A6E8','#DAD4F5')]
    for k,(c,t) in enumerate(cols): pixel_flyer(d,520+k*120,110+k*95,22,c,t)
    pixel_cloud(d,80,80,18,(232,248,248)); pixel_cloud(d,900,520,14,(232,248,248))
    save(im,'pixel-relief')
    im=Image.new('RGB',(1024,640),(255,255,255)); d=ImageDraw.Draw(im)   # red bike decal
    c=hx('#E0473C'); k=hx('#2B2B2B')
    for cx in (280,740): d.ellipse([cx-150,310,cx+150,610],outline=k,width=16); d.ellipse([cx-12,448,cx+12,472],fill=k)
    d.line([(280,460),(450,460),(600,250),(380,250),(280,460)],fill=c,width=20); d.line([(450,460),(380,250)],fill=c,width=18)
    d.line([(600,250),(740,460)],fill=c,width=18); d.line([(370,250),(350,210)],fill=c,width=14); d.rectangle([310,195,410,215],fill=k)
    d.line([(600,250),(590,200),(650,190)],fill=k,width=12); d.rectangle([600,170,700,250],outline=hx('#F7CE63'),width=10)
    save(alpha_from_white(im),'red-bike-decal',png=True)
    im=Image.new('RGB',(512,512),hx('#F4F0E6')); d=ImageDraw.Draw(im)   # E1 bunny tile (flips to show five colour squares)
    d.rectangle([0,0,511,511],outline=hx('#3B8A89'),width=16); pixel_bunny(d,166,150,20,(255,255,255))
    for k,(c,_) in enumerate(cols): d.rectangle([96+k*68,420,96+k*68+48,468],fill=hx(c))
    save(im,'bunny-tile')
