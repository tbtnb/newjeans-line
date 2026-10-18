import math
PETALS=['#c2449a','#ff5fa8','#ff5a2c','#ff8f2a','#ffc928','#fff200','#93d14b','#00a651','#00b3a4','#00aeef','#0072bc','#5b3f9e']  # Supernatural cover, clockwise from top
def murakami_flower(r=5.0,y=0.0,face=True,petal_scale=1.0,flat=False):
    """Cover flower: 12 rainbow petals + white bunny face (upright disc facing the camera side if not flat)."""
    parts=[]
    for i,c in enumerate(PETALS):
        a=math.radians(90-i*30)
        px,py=math.cos(a)*r*0.78,math.sin(a)*r*0.78
        if flat: parts.append({'kind':'cylinder','pos':[round(px,2),y+0.15,round(py,2)],'size':[r*0.55*petal_scale,0.3,r*0.55*petal_scale],'color':c})
        else: parts.append({'kind':'sphere','pos':[round(px,2),y+r+round(py,2),0],'size':[r*0.55*petal_scale,r*0.55*petal_scale,0.35],'color':c})
    if face:
        if flat:
            parts+= [{'kind':'cylinder','pos':[0,y+0.35,0],'size':[r*1.05,0.3,r*1.0],'color':'#ffffff'},
                     {'kind':'sphere','pos':[0,y+0.45,-r*0.25],'size':[r*0.4,0.2,r*0.25],'color':'#ff6fb5'}]
        else:
            parts+= [{'kind':'cylinder','pos':[0,y+r,0.05],'size':[r*1.05,0.4,r*1.0],'rot':[90,0,0],'color':'#ffffff'},
                     {'kind':'box','pos':[0,y+r*1.45,0.1],'size':[r*0.22,r*0.5,0.3],'color':'#c2449a'},
                     {'kind':'sphere','pos':[-r*0.2,y+r*1.05,-0.25],'size':[0.35*r/3,0.5*r/3,0.1],'color':'#e8272b'},
                     {'kind':'sphere','pos':[r*0.2,y+r*1.05,-0.25],'size':[0.35*r/3,0.5*r/3,0.1],'color':'#1fae6a'},
                     {'kind':'sphere','pos':[0,y+r*0.75,-0.25],'size':[r*0.45,r*0.28,0.1],'color':'#ff6fb5'}]
    return parts
def shop(w=6,h=5,d=4,c='#f3e6cf',awn='#e8735a',sign='#111111'):
    return [{'kind':'box','pos':[0,h/2,0],'size':[w,h,d],'color':c},
            {'kind':'box','pos':[0,h*0.62,-d/2-0.6],'size':[w*0.9,0.15,1.4],'rot':[18,0,0],'color':awn},
            {'kind':'box','pos':[0,h*0.86,-d/2-0.05],'size':[w*0.7,0.8,0.1],'color':sign},
            {'kind':'box','pos':[-w*0.25,1.2,-d/2-0.05],'size':[1.4,2.4,0.1],'color':'#5b6f8f'},
            {'kind':'box','pos':[w*0.2,1.6,-d/2-0.05],'size':[1.8,1.4,0.1],'color':'#ffe9b8'}]
def balloon(c,h=6):
    return [{'kind':'sphere','pos':[0,h,0],'size':[1.6,2.0,1.6],'color':c},{'kind':'cylinder','pos':[0,h/2,0],'size':[0.05,h-1,0.05],'color':'#ffffff'}]
def palm_free_tree(c='#7cc47f'):
    return [{'kind':'cylinder','pos':[0,1,0],'size':[0.4,2,0.4],'color':'#8a6a4a'},{'kind':'sphere','pos':[0,2.8,0],'size':[2.6,2.4,2.6],'color':c}]
def pot(c,tag):
    return [{'kind':'cylinder','pos':[0,0.5,0],'size':[1.1,1.0,1.1],'color':'#d9825b'},{'kind':'sphere','pos':[0,1.6,0],'size':[1.2,1.2,1.2],'color':c},
            {'kind':'cylinder','pos':[0,1.0,0],'size':[0.08,1.0,0.08],'color':'#4c9a5b'},{'kind':'box','pos':[0.6,0.7,-0.56],'size':[0.4,0.3,0.05],'color':tag}]
