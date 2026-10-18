def box(pos,size,color,rot=None): 
    d={'kind':'box','pos':pos,'size':size,'color':color}
    if rot: d['rot']=rot
    return d
def part(kind,pos,size,color,rot=None):
    d={'kind':kind,'pos':pos,'size':size,'color':color}
    if rot: d['rot']=rot
    return d
def obj(id,t,side,kind,size=None,color=None,**kw):
    d={'id':id,'t':t,'side':side,'kind':kind}
    if size: d['size']=size
    if color: d['color']=color
    d.update(kw); return d
def appear(t,mode='rise',dur=0.8): return {'t':round(t,3),'mode':mode,'dur':dur}
def exitm(t,mode='sink',dur=0.8): return {'t':round(t,3),'mode':mode,'dur':dur}
def bunny_relief(id,t,side,wall,ink,scale=1.0,**kw):
    """2022 EP cover bunny as block relief: wall + white face, ears, eyes, arms."""
    s=scale
    parts=[part('box',[0,6*s,0],[16*s,12*s,1.2*s],wall),
           part('box',[0,6.5*s,-0.8*s],[7*s,5.5*s,0.6*s],ink),          # face
           part('box',[-2*s,11*s,-0.8*s],[1.6*s,5*s,0.6*s],ink),        # ears
           part('box',[2*s,11*s,-0.8*s],[1.6*s,5*s,0.6*s],ink),
           part('box',[-1.4*s,7.2*s,-1.2*s],[1.0*s,1.2*s,0.3*s],wall),  # eyes
           part('box',[1.4*s,7.2*s,-1.2*s],[1.0*s,1.2*s,0.3*s],wall),
           part('box',[0,5.6*s,-1.2*s],[1.2*s,0.5*s,0.3*s],'#E8A0A8'),  # mouth/cheek
           part('box',[-5.5*s,4.5*s,-0.8*s],[4*s,1.4*s,0.6*s],ink,[0,0,20]),  # arms
           part('box',[5.5*s,4.5*s,-0.8*s],[4*s,1.4*s,0.6*s],ink,[0,0,-20])]
    d={'id':id,'t':t,'side':side,'kind':'group','parts':parts,'radius':9*s}
    d.update(kw); return d
