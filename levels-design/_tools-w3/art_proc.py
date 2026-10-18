"""Procedural art (PIL). GenerateImage was used first, but its output files never reached the box after the
11:33 restore, so every art file the layouts reference is drawn here (flat / pixel / low-poly style, no people)."""
import os, math, random, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from paths import OUT
R=random.Random(7)
def hexc(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def grad(w,h,top,bot):
    a=np.linspace(0,1,h)[:,None,None]; t=np.array(hexc(top)); b=np.array(hexc(bot))
    return Image.fromarray(np.broadcast_to(t*(1-a)+b*a,(h,w,3)).astype('uint8'))
def save(im,slug,name,q=86):
    d=f'{OUT}/{slug}/art'; os.makedirs(d,exist_ok=True); p=f'{d}/{name}'
    if name.endswith('.jpg'): im.convert('RGB').save(p,quality=q,optimize=True)
    else: im.save(p,optimize=True)
    print(p,os.path.getsize(p)//1024,'KB')
def voxel_cloud(dr,x,y,s,col,shade):
    for dx,dy,w in [(0,0,4),(1,-1,2),(2,-1,2),(3,0,2)]:
        dr.rectangle([x+dx*s,y+dy*s,x+(dx+w)*s,y+(dy+1)*s],fill=col)
        dr.rectangle([x+dx*s,y+(dy+1)*s-s//4,x+(dx+w)*s,y+(dy+1)*s],fill=shade)
def tile_noise(w,h,base,var,scale=8,seed=1):
    rng=np.random.default_rng(seed); n=rng.random((h//scale+1,w//scale+1))
    n=np.array(Image.fromarray((n*255).astype('uint8')).resize((w,h),Image.BICUBIC))/255.0
    b=np.array(hexc(base)); v=np.array(hexc(var))
    return Image.fromarray((b*(1-n[...,None])+v*n[...,None]).astype('uint8'))
def pixel_heart(cols,bg=None,size=480):
    H=["0110110","1111111","1111111","1111111","0111110","0011100","0001000"]
    im=Image.new('RGBA',(size,size),(0,0,0,0) if bg is None else hexc(bg)+(255,)); dr=ImageDraw.Draw(im)
    c=size//9; ox=c; oy=c
    for r,row in enumerate(H):
        for k,ch in enumerate(row):
            if ch=='1':
                col=hexc(cols[min(len(cols)-1,int(r*len(cols)/len(H)))])
                dr.rectangle([ox+k*c,oy+r*c,ox+(k+1)*c-1,oy+(r+1)*c-1],fill=col+(255,))
    for i in range(14):
        x,y=R.randrange(size),R.randrange(size); col=hexc(cols[i%len(cols)])
        if 2*c<x<7*c and 1*c<y<8*c: continue
        s=c//6; dr.rectangle([x-s,y-3*s,x+s,y+3*s],fill=col+(255,)); dr.rectangle([x-3*s,y-s,x+3*s,y+s],fill=col+(255,))
    return im
def pixel_bunny(body='#ffffff',eye='#203750',inner='#F3A8C8',outline='#ffffff',eyes_glow=False,leaves=None,size=320):
    B=["00110001100","00110001100","00120002100","00120002100","00110001100","01111111110","11111111111","11311111311","11111111111","11111111111","01111111110","00111111100"]
    if leaves: B=B[:9]
    n=len(B[0]); c=size//(n+4); im=Image.new('RGBA',(size,size),(0,0,0,0)); dr=ImageDraw.Draw(im)
    ox=(size-n*c)//2; oy=c
    mp={'1':hexc(body),'2':hexc(inner),'3':hexc(eye)}
    # sticker outline
    for r,row in enumerate(B):
        for k,ch in enumerate(row):
            if ch!='0': dr.rectangle([ox+k*c-c//2,oy+r*c-c//2,ox+(k+1)*c+c//2,oy+(r+1)*c+c//2],fill=hexc(outline)+(255,))
    if leaves:
        for i in range(40):
            x=ox+R.randrange(-c,(n+1)*c); y=oy+R.randrange(7*c,11*c)
            dr.rectangle([x-c,y-c//2,x+c,y+c//2],fill=hexc(outline)+(255,))
    for r,row in enumerate(B):
        for k,ch in enumerate(row):
            if ch!='0': dr.rectangle([ox+k*c,oy+r*c,ox+(k+1)*c-1,oy+(r+1)*c-1],fill=mp[ch]+(255,))
    if leaves:
        for i in range(60):
            x=ox+R.randrange(-c//2,n*c+c//2); y=oy+R.randrange(int(7.5*c),int(10.5*c))
            dr.rectangle([x-c*0.8,y-c*0.35,x+c*0.8,y+c*0.35],fill=hexc(leaves[i%len(leaves)])+(255,))
    return im.crop(im.getbbox())
def sky_voxel(top,bot,cloud,shade,islands=None,sea=None,w=1536,h=864,seed=3):
    rng=random.Random(seed); im=grad(w,h,top,bot); dr=ImageDraw.Draw(im)
    for i in range(9):
        voxel_cloud(dr,rng.randrange(-50,w-100),rng.randrange(40,h//2),rng.choice([18,24,32]),hexc(cloud),hexc(shade))
    if sea:
        y=int(h*0.86); dr.rectangle([0,y,w,h],fill=hexc(sea))
        for i in range(30): xx=rng.randrange(w); dr.line([xx,y+rng.randrange(8,h-y),xx+rng.randrange(20,80),0],fill=None)
        if islands:
            for i in range(6):
                x=rng.randrange(40,w-120); s=rng.choice([10,14]); 
                dr.rectangle([x,y-s,x+8*s,y],fill=hexc(islands[0])); dr.rectangle([x+2*s,y-3*s,x+5*s,y-s],fill=hexc(islands[1]))
                dr.rectangle([x+6*s,y-4*s,x+6*s+3,y-s],fill=(120,90,60)); dr.ellipse([x+5*s,y-5*s,x+8*s,y-3.5*s],fill=(90,160,100))
    return im.filter(ImageFilter.GaussianBlur(0.8))
def eta():
    save(sky_voxel('#9fdbe6','#fff4e2','#ffffff','#e2f1f3',islands=['#f1e2c6','#CE785A'],sea='#7fd3d6'),'eta','sky.jpg')
    sea=tile_noise(512,512,'#2fb9bd','#7fe0de',scale=24,seed=4); d=ImageDraw.Draw(sea)
    for i in range(80): x,y=R.randrange(512),R.randrange(512); d.line([x,y,x+R.randrange(8,26),y],fill=(190,245,240),width=2)
    save(sea,'eta','sea.jpg')
    t=tile_noise(512,512,'#c96f50','#dd8a66',scale=16,seed=5); d=ImageDraw.Draw(t)
    for k in range(0,513,128): d.line([k,0,k,512],fill=(245,226,196),width=6); d.line([0,k,512,k],fill=(245,226,196),width=6)
    save(t,'eta','terracotta-tile.jpg')
    save(pixel_heart(['#77C9ED','#A5DFB5','#F3A8C8','#F8BB7D','#B1A1E3'],bg='#FFF8E8'),'eta','heart-poster.png')
    save(pixel_bunny(outline='#f4f4f4'),'eta','bunny-sticker.png')
def cwy():
    w,h=1536,864; im=grad(w,h,'#4d6672','#8aa4ad'); d=ImageDraw.Draw(im); rng=random.Random(11)
    for layer,(col,base,hmax) in enumerate([('#7fa9b4',0.62,0.22),('#9BD8E2',0.70,0.18),('#5d7b86',0.80,0.14)]):
        x=0
        while x<w:
            bw=rng.randrange(40,110); bh=int(h*rng.uniform(0.05,hmax)); y0=int(h*base)-bh
            d.rectangle([x,y0,x+bw,h],fill=hexc(col))
            for wy in range(y0+10,int(h*base)+60,18):
                for wx in range(x+8,x+bw-8,16):
                    if rng.random()<0.12: d.rectangle([wx,wy,wx+6,wy+8],fill=(255,214,150))
            x+=bw+rng.randrange(0,12)
    for i in range(500):
        x,y=rng.randrange(w),rng.randrange(h); d.line([x,y,x-3,y+18],fill=(200,220,228),width=1)
    save(im.filter(ImageFilter.GaussianBlur(1.0)),'cool-with-you','rain-city.jpg')
    st=tile_noise(512,512,'#5f7680','#8fa5ad',scale=10,seed=12); d=ImageDraw.Draw(st)
    for yy in range(0,512,64):
        off=0 if (yy//64)%2==0 else 48
        for xx in range(-48,560,96): d.rectangle([xx+off,yy,xx+off+92,yy+60],outline=(37,70,71),width=4)
    for i in range(12): x,y=R.randrange(512),R.randrange(512); d.ellipse([x,y,x+R.randrange(30,70),y+R.randrange(10,24)],fill=(150,200,212))
    save(st,'cool-with-you','wet-stone.jpg')
    # abstract painting: two ivory forms, one winged, gold frame
    P=Image.new('RGB',(600,800),hexc('#D8B86A')); d=ImageDraw.Draw(P); d.rectangle([30,30,570,770],fill=hexc('#254647'))
    d.ellipse([110,200,280,620],fill=hexc('#EEEADF')); d.ellipse([320,180,490,600],fill=hexc('#EEEADF'))
    for k in range(6): d.polygon([(280,360+k*14),(380-k*6,300+k*22),(300,400+k*14)],fill=(250,250,248))
    save(P,'cool-with-you','wings-painting.jpg')
    F=grad(600,800,'#c9eef3','#7f9ea8').convert('RGBA'); d=ImageDraw.Draw(F)
    for i in range(26):
        x,y=R.randrange(40,560),R.randrange(40,760); L_=R.randrange(40,110); a=math.radians(R.randrange(20,70))
        dx,dy=math.cos(a)*L_/2,math.sin(a)*L_/2
        d.line([x-dx,y-dy,x+dx,y+dy],fill=(255,255,255,255),width=2)
        d.polygon([(x-dx,y-dy),(x+dx,y+dy),(x+dx*0.6-dy*0.25,y+dy*0.6+dx*0.25),(x-dx*0.8-dy*0.2,y-dy*0.8+dx*0.2)],fill=(255,255,255,210))
    for i in range(20): x,y=R.randrange(600),R.randrange(800); d.ellipse([x,y,x+7,y+7],fill=(240,139,120,255))
    save(F.convert('RGB'),'cool-with-you','feather-poster.jpg')
def getup():
    w,h=1536,864; im=grad(w,h,'#a8c8d1','#e9d6e4'); d=ImageDraw.Draw(im)
    y=int(h*0.62); d.rectangle([0,y-6,w,y+6],fill=(247,205,214))
    refl=grad(w,h-y,'#d9cfe6','#a8c8d1'); im.paste(refl,(0,y))
    for x,s in [(120,180),(520,120),(980,220),(1300,140)]:
        d.polygon([(x,y),(x+s,y),(x+s*0.85,y-s*0.12),(x+s*0.15,y-s*0.1)],fill=(184,180,213))
    save(im.filter(ImageFilter.GaussianBlur(1.2)),'get-up','dawn.jpg')
    g=tile_noise(512,512,'#8fae86','#b4cfa0',scale=6,seed=21); d=ImageDraw.Draw(g)
    for i in range(500): x,y=R.randrange(512),R.randrange(512); d.line([x,y,x+R.randrange(-2,3),y-R.randrange(4,9)],fill=(170,200,150))
    for i in range(18): x,y=R.randrange(512),R.randrange(512); d.ellipse([x,y,x+5,y+5],fill=(250,250,240))
    save(g,'get-up','grass.jpg')
    M=grad(960,540,'#a8d4cf','#cfe7e2').convert('RGB'); d=ImageDraw.Draw(M); d.rectangle([0,400,960,540],fill=hexc('#F5F1E8'))
    for i,col in enumerate(['#4B9EDF','#93CF9B','#F1A9C9','#E9BC83','#B39AD7']):
        x=160+i*150
        for yy in range(130,420,14): d.rectangle([x+int(8*math.sin(yy/40+i)),yy,x+40+int(8*math.sin(yy/40+i)),yy+12],fill=hexc(col))
    d.polygon([(480,90),(380,40),(420,95)],fill=(250,248,240)); d.polygon([(480,90),(580,40),(540,95)],fill=(250,248,240))
    save(M,'get-up','five-lights.jpg')
def asap():
    w,h=1536,864; im=grad(w,h,'#0f2f2a','#2c5a4b'); d=ImageDraw.Draw(im); rng=random.Random(31)
    d.ellipse([980,120,1180,320],fill=(226,232,200))
    for layer,(col,base) in enumerate([('#1d4a3e',0.55),('#163d34',0.68),('#0f2e27',0.82)]):
        for i in range(26):
            x=rng.randrange(-60,w); s=rng.randrange(50,120); yb=int(h*base)+rng.randrange(-20,20)
            d.polygon([(x,yb),(x+s,yb),(x+s/2,yb-s*1.8)],fill=hexc(col))
    d.rectangle([0,int(h*0.82),w,h],fill=hexc('#0f2e27'))
    for i in range(90): x,y=rng.randrange(w),rng.randrange(int(h*0.3),h); d.ellipse([x,y,x+4,y+4],fill=(255,226,120))
    save(im.filter(ImageFilter.GaussianBlur(0.9)),'asap','forest.jpg')
    g=tile_noise(512,512,'#9fb88c','#bcd0a3',scale=7,seed=33); d=ImageDraw.Draw(g)
    for i in range(30):
        x,y=R.randrange(512),R.randrange(512); col=[(241,184,203),(244,241,223),(234,184,140)][i%3]
        for a in range(5): d.ellipse([x+5*math.cos(a*1.256)-3,y+5*math.sin(a*1.256)-3,x+5*math.cos(a*1.256)+3,y+5*math.sin(a*1.256)+3],fill=col)
    save(g,'asap','meadow.jpg')
    S=Image.new('RGB',(600,600),hexc('#A8BE94')); d=ImageDraw.Draw(S)
    d.line([300,0,300,190],fill=hexc('#E2BD65'),width=6); d.ellipse([170,190,430,450],fill=hexc('#F4F1DF'),outline=hexc('#E2BD65'),width=10)
    d.line([300,320,300,230],fill=hexc('#315C4C'),width=8); d.line([300,320,360,350],fill=hexc('#315C4C'),width=6)
    for sgn in (-1,1):
        for k in range(4): d.ellipse([300+sgn*(150+k*30)-40,240+k*40-18,300+sgn*(150+k*30)+40,240+k*40+18],fill=(250,250,245))
    for i in range(16): x,y=R.randrange(600),R.randrange(600); d.ellipse([x,y,x+10,y+10],fill=(241,184,203))
    save(S,'asap','pendulum-sign.jpg')
    save(pixel_bunny(body='#1b1b1b',eye='#e8323a',inner='#7a4a55',outline='#f4f4f4',leaves=['#1f5a2c','#2c7a3c','#174a22']),'asap','bunny-eyes.png')
if __name__=='__main__':
    eta(); cwy(); getup(); asap()
