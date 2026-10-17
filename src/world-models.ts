import {Color3} from '@babylonjs/core/Maths/math.color';
import {Vector3} from '@babylonjs/core/Maths/math.vector';
import {Mesh} from '@babylonjs/core/Meshes/mesh';
import {MeshBuilder} from '@babylonjs/core/Meshes/meshBuilder';
import {Scene} from '@babylonjs/core/scene';
import {StandardMaterial} from '@babylonjs/core/Materials/standardMaterial';
import {TransformNode} from '@babylonjs/core/Meshes/transformNode';
import type {LevelArt} from './level-design';

const TAU=Math.PI*2;
const WHITE='#F6F4EA', GOLD='#E6CA8D';
const RAINBOW=['#EF7BA8','#EDA478','#ECD36E','#A7CF76','#69C5B2','#77B7D9','#AA93D3'];
type Shape='box'|'cylinder'|'sphere'|'cone'|'ring';
type Motion={node:TransformNode;run:(elapsed:number,progress:number)=>void};
// Two complementary places per chapter, selected from the four authored motifs.
// This makes the scenery pool follow the song's spatial story rather than shuffle
// every motif indiscriminately throughout the entire track.
const STAGING:Record<string,readonly (readonly [number,number])[]>={
  'attention':[[2,0],[1,3],[2,1],[3,1]],
  'hype-boy':[[0,3],[0,2],[1,2],[3,2]],
  'cookie':[[1,0],[0,2],[1,2],[3,2]],
  'hurt':[[0,2],[1,0],[2,3],[3,2]],
  'omg':[[0,2],[1,2],[2,1],[3,0]],
  'ditto':[[1,3],[0,3],[2,0],[1,3]],
  'new-jeans':[[0,1],[0,1],[2,0],[3,2]],
  'super-shy':[[1,0],[0,1],[3,0],[2,3]],
  'eta':[[0,2],[1,2],[1,0],[3,1]],
  'cool-with-you':[[0,1],[3,0],[1,2],[0,2]],
  'get-up':[[0,1],[1,3],[3,0],[2,3]],
  'asap':[[3,1],[0,3],[1,0],[2,3]],
  'how-sweet':[[0,2],[1,0],[3,1],[3,2]],
  'bubble-gum':[[0,3],[1,0],[2,3],[2,1]],
  'supernatural':[[0,1],[1,2],[2,0],[3,1]],
  'right-now':[[2,0],[0,3],[1,3],[3,2]],
};

/**
 * Album-informed native Babylon dioramas. Geometry templates/materials are shared;
 * static pieces are merged by material at each returned root. No textures/network.
 * Local platform top is .52. Bounds: scenery +/-3, y<=5; landmarks +/-4,y<=7;
 * eggs +/-2,y<=3. All motion remains inside those envelopes.
 */
export class WorldModels {
  private readonly sources=new Map<Shape,Mesh>();
  private readonly materials=new Map<string,StandardMaterial>();
  private readonly roots=new Set<TransformNode>();
  private readonly motions=new Set<Motion>();
  private serial=0;
  private readonly c:LevelArt['colors'];
  constructor(private readonly scene:Scene,private readonly art:LevelArt) {this.c=art.colors;}

  private material(color:string,alpha=1):StandardMaterial {
    const key=`${color}:${alpha}`;let mat=this.materials.get(key);
    if(!mat){mat=new StandardMaterial(`art-${key}`,this.scene);mat.diffuseColor=Color3.FromHexString(color);mat.specularColor=Color3.Black();mat.ambientColor=Color3.FromHexString(color).scale(.22);mat.emissiveColor=Color3.FromHexString(color).scale(this.art.dark?.065:.025);mat.alpha=alpha;mat.backFaceCulling=false;this.materials.set(key,mat);}
    return mat;
  }
  private source(shape:Shape):Mesh {
    let mesh=this.sources.get(shape);if(mesh)return mesh;
    const name=`model-template-${shape}`;
    if(shape==='box')mesh=MeshBuilder.CreateBox(name,{size:1},this.scene);
    else if(shape==='cylinder')mesh=MeshBuilder.CreateCylinder(name,{diameter:1,height:1,tessellation:24},this.scene);
    else if(shape==='sphere')mesh=MeshBuilder.CreateSphere(name,{diameter:1,segments:4},this.scene);
    else if(shape==='cone')mesh=MeshBuilder.CreateCylinder(name,{diameterTop:0,diameterBottom:1,height:1,tessellation:4},this.scene);
    else mesh=MeshBuilder.CreateTorus(name,{diameter:2,thickness:.1,tessellation:16},this.scene);
    mesh.isVisible=false;mesh.isPickable=false;mesh.metadata={modelTemplate:true};this.sources.set(shape,mesh);return mesh;
  }
  private mesh(g:TransformNode,shape:Shape,color:string,x:number,y:number,z:number,sx:number,sy:number,sz:number,alpha=1):Mesh {
    const m=this.source(shape).clone(`piece-${this.serial++}`,g,true)!;m.isVisible=true;m.isPickable=false;m.material=this.material(color,alpha);m.position.set(x,y,z);m.scaling.set(sx,sy,sz);m.receiveShadows=true;return m;
  }
  private box(g:TransformNode,x:number,y:number,z:number,w:number,h:number,d:number,color=this.c.road,alpha=1):Mesh {return this.mesh(g,'box',color,x,y,z,w,h,d,alpha);}
  private cyl(g:TransformNode,x:number,y:number,z:number,r:number,h:number,color=this.c.road):Mesh {return this.mesh(g,'cylinder',color,x,y,z,r*2,h,r*2);}
  private ball(g:TransformNode,x:number,y:number,z:number,r:number,color=this.c.road,sx=1,sy=1,sz=1,alpha=1):Mesh {return this.mesh(g,'sphere',color,x,y,z,r*2*sx,r*2*sy,r*2*sz,alpha);}
  private disc(g:TransformNode,x:number,y:number,z:number,r:number,d:number,color=this.c.road):Mesh {const m=this.cyl(g,x,y,z,r,d,color);m.rotation.x=Math.PI/2;return m;}
  private ring(g:TransformNode,x:number,y:number,z:number,r:number,color=this.c.road):Mesh {const m=this.mesh(g,'ring',color,x,y,z,r,r,r);m.rotation.x=Math.PI/2;return m;}
  private node(name:string,parent:TransformNode,x=0,y=0,z=0):TransformNode {const n=new TransformNode(name,this.scene);n.parent=parent;n.position.set(x,y,z);return n;}
  private motion(node:TransformNode,run:Motion['run']):void {node.metadata={...node.metadata,moving:true};this.motions.add({node,run});}
  private begin(kind:string):{root:TransformNode;g:TransformNode} {
    const root=new TransformNode(`${this.art.id}-${kind}`,this.scene);root.metadata={artId:this.art.id,family:this.art.family,kind,footprint:kind==='landmark'?4:kind==='egg'?2:3};
    const g=this.node('platform-top',root,0,.52,0);this.roots.add(root);root.onDisposeObservable.add(()=>{this.roots.delete(root);for(const m of this.motions)if(m.node.isDisposed())this.motions.delete(m);});return {root,g};
  }
  /** Merge per material in the local space of each independently moving group. */
  private finish(root:TransformNode):TransformNode {
    const owners=new Map<TransformNode,Map<StandardMaterial,Mesh[]>>();
    for(const m of root.getChildMeshes(false)) {
      if(!(m instanceof Mesh)||!m.material||m.metadata?.moving)continue;
      let owner:TransformNode=root;let p=m.parent as TransformNode|null;
      while(p&&p!==root){if(p.metadata?.moving){owner=p;break;}p=p.parent as TransformNode|null;}
      const grouped=owners.get(owner)??new Map<StandardMaterial,Mesh[]>();
      const mat=m.material as StandardMaterial;const group=grouped.get(mat)??[];group.push(m);grouped.set(mat,group);owners.set(owner,grouped);
    }
    for(const [owner,grouped]of owners){
      // MergeMeshes bakes world transforms. Temporarily use this group's local space,
      // then restore it so animation pivots and the caller's positioning stay intact.
      const parent=owner.parent,position=owner.position.clone(),rotation=owner.rotation.clone(),scale=owner.scaling.clone(),quaternion=owner.rotationQuaternion?.clone()??null;
      owner.parent=null;owner.position.setAll(0);owner.rotation.setAll(0);owner.scaling.setAll(1);owner.rotationQuaternion=null;owner.computeWorldMatrix(true);
      for(const [mat,meshes]of grouped){
        if(meshes.length<2)continue;for(const mesh of meshes)mesh.computeWorldMatrix(true);
        // Keep inputs alive while merging: Babylon otherwise reuses a shared index
        // array. false forces copying, after which these temporary clones are freed.
        const merged=Mesh.MergeMeshes(meshes,false,true,undefined,false,false);
        if(merged){for(const mesh of meshes)mesh.dispose(false,false);merged.name=`${owner.name}-batched`;merged.parent=owner;merged.material=mat;merged.isPickable=false;merged.receiveShadows=true;}
      }
      owner.parent=parent;owner.position.copyFrom(position);owner.rotation.copyFrom(rotation);owner.scaling.copyFrom(scale);owner.rotationQuaternion=quaternion;owner.computeWorldMatrix(true);
    }
    return root;
  }
  private base(g:TransformNode,w:number,d:number,color=this.c.ground):void {this.box(g,0,-.2,0,w,.4,d,this.c.roadSide);this.box(g,0,-.035,0,w+.04,.07,d+.04,color);}
  private frame(g:TransformNode,x:number,y:number,z:number,w:number,h:number,color=this.c.road,t=.14):void {
    this.box(g,x-w/2+t/2,y+h/2,z,t,h,.2,color);this.box(g,x+w/2-t/2,y+h/2,z,t,h,.2,color);this.box(g,x,y+t/2,z,w,t,.2,color);this.box(g,x,y+h-t/2,z,w,t,.2,color);
  }
  private beam(g:TransformNode,a:Vector3,b:Vector3,width:number,color:string):Mesh {const m=this.box(g,(a.x+b.x)/2,(a.y+b.y)/2,(a.z+b.z)/2,width,Vector3.Distance(a,b),width,color);const delta=b.subtract(a).normalize();m.rotation.z=-Math.atan2(delta.x,delta.y);m.rotation.x=Math.atan2(delta.z,Math.sqrt(delta.x*delta.x+delta.y*delta.y));return m;}
  private window(g:TransformNode,x:number,y:number,z:number,w=.65,h=.9,warm=false):void {this.box(g,x,y+h/2,z,w,h,.06,warm?GOLD:this.c.secondary);this.frame(g,x,y,z+.04,w+.16,h+.16,this.c.road,.08);this.box(g,x,y+h/2,z+.15,.05,h,.04,this.c.road);}
  private building(g:TransformNode,x:number,z:number,w:number,h:number,d:number,color:string,chapter=0):TransformNode {
    const b=this.node('building',g,x,0,z);this.box(b,0,h/2,0,w,h,d,color);this.box(b,0,h+.08,0,w+.16,.16,d+.16,this.c.road);this.box(b,0,h+.18,0,w-.22,.08,d-.22,this.c.secondary);
    const count=Math.min(3,Math.max(1,Math.floor(w/.8)));for(let i=0;i<count;i++)this.window(b,(i-(count-1)/2)*.72,.45,d/2+.025,.4,Math.min(1,h-.75),chapter===3&&i===count-1);
    if(h>2.8)for(let i=0;i<count;i++)this.window(b,(i-(count-1)/2)*.72,1.85,d/2+.025,.4,.65,false);
    return b;
  }
  private bench(g:TransformNode,x:number,z:number,color=this.c.accent,scale=1):TransformNode {const b=this.node('empty-bench',g,x,0,z);b.scaling.setAll(scale);this.box(b,0,.48,0,1.75,.13,.6,color);this.box(b,0,.95,-.24,1.75,.65,.12,color);for(const a of [-.62,.62])this.box(b,a,.23,0,.12,.46,.42,this.c.ink);return b;}
  private lamp(g:TransformNode,x:number,z:number,h=2.5):void {this.box(g,x,h/2,z,.1,h,.1,this.c.ink);this.box(g,x,h+.2,z,.48,.5,.48,this.c.road);this.box(g,x,h+.2,z+.25,.32,.33,.02,GOLD);this.box(g,x,h+.51,z,.64,.1,.64,this.c.accent);}
  private envelope(g:TransformNode,x:number,y:number,z:number,scale=1,color=this.c.road):TransformNode {const n=this.node('folded-letter',g,x,y,z);n.scaling.setAll(scale);this.box(n,0,0,0,1.2,.75,.08,color);this.beam(n,new Vector3(-.58,.32,.055),new Vector3(0,-.08,.055),.025,this.c.accent);this.beam(n,new Vector3(0,-.08,.055),new Vector3(.58,.32,.055),.025,this.c.accent);return n;}
  private pixelStar(g:TransformNode,x:number,y:number,z:number,size=.6,color=GOLD):TransformNode {const n=this.node('pixel-star',g,x,y,z);this.box(n,0,0,0,size*.36,size,.16,color);this.box(n,0,0,0,size,size*.36,.16,color);this.box(n,0,0,0,size*.65,size*.65,.16,color);return n;}
  private ears(g:TransformNode,x:number,y:number,z:number,scale=1,color=this.c.road):void {for(const s of [-1,1]){this.ball(g,x+s*.28*scale,y+.42*scale,z,.28*scale,color,.75,2,.7);this.ball(g,x+s*.28*scale,y+.44*scale,z+.09*scale,.16*scale,this.c.secondary,.65,2,.5);}}
  private bunny(g:TransformNode,x:number,z:number,scale=1):{body:TransformNode;arm:TransformNode} {
    const b=this.node('geometric-bunny',g,x,0,z);b.scaling.setAll(scale);this.box(b,0,.42,0,.55,.67,.4,this.c.road);this.box(b,0,.94,.03,.68,.62,.45,this.c.road);for(const s of [-1,1]){this.box(b,s*.2,1.5,.03,.17,.63,.18,this.c.road);this.box(b,s*.2,1.53,.13,.07,.4,.02,this.c.secondary);this.box(b,s*.15,1.01,.27,.055,.065,.03,this.c.ink);this.box(b,s*.19,.09,.16,.22,.15,.38,this.c.road);}this.box(b,0,.86,.27,.08,.055,.03,this.c.accent);
    const arm=this.node('bunny-wave',b,.34,.62,0);this.box(arm,.12,.02,0,.3,.18,.22,this.c.road);return {body:b,arm};
  }
  private plant(g:TransformNode,x:number,z:number,scale=1,color=this.c.secondary):TransformNode {const p=this.node('small-plant',g,x,0,z);p.scaling.setAll(scale);this.cyl(p,0,.2,0,.3,.4,this.c.road);this.cyl(p,0,.41,0,.25,.04,this.c.ink);this.box(p,0,.78,0,.07,.75,.07,this.c.secondary);for(const s of [-1,1]){const leaf=this.ball(p,s*.18,.78+s*.12,0,.22,color,1,.5,.6);leaf.rotation.z=s*.5;}this.ball(p,0,1.2,0,.2,color,.7,1,.7);return p;}
  private record(g:TransformNode,x:number,y:number,z:number,r=.6,vertical=false,cd=false):TransformNode {const d=this.node(cd?'compact-disc':'vinyl',g,x,y,z);if(vertical)d.rotation.x=Math.PI/2;this.cyl(d,0,0,0,r,.07,cd?this.c.secondary:this.c.ink);for(const ratio of [.5,.8]){const ring=this.ring(d,0,.045,0,r*ratio,cd?this.c.road:this.c.roadSide);ring.rotation.x=0;ring.scaling.y=.16;}this.cyl(d,0,.045,0,r*.25,.03,cd?this.c.accent:this.c.accent);this.cyl(d,0,.068,0,r*.065,.035,this.c.ink);return d;}
  private cassette(g:TransformNode,x:number,y:number,z:number,w=3,h=1.8,color=this.c.accent):TransformNode {
    const n=this.node('twin-reel-cassette',g,x,y,z);this.box(n,0,0,0,w,h,.58,color);this.box(n,0,.05,.31,w*.84,h*.56,.06,this.c.road);for(const s of [-1,1]){this.disc(n,s*w*.25,.05,.38,h*.2,.07,this.c.ink);this.disc(n,s*w*.25,.05,.43,h*.09,.07,this.c.secondary);this.box(n,s*w*.25,.05,.48,h*.04,h*.22,.02,this.c.road);}this.box(n,0,.05,.4,w*.23,h*.25,.09,this.c.roadSide);this.box(n,0,-h*.36,.34,w*.52,h*.14,.04,this.c.roadSide);for(const s of [-1,1])for(const v of [-1,1])this.disc(n,s*w*.43,v*h*.39,.32,.045,.02,this.c.ink);return n;
  }
  private greenhouse(g:TransformNode,x:number,z:number,w=3,d=2.4,h=2.3):TransformNode {
    const n=this.node('glass-conservatory',g,x,0,z);this.box(n,0,.08,0,w+.3,.16,d+.3,this.c.road);for(const sx of [-1,1])for(const sz of [-1,1])this.box(n,sx*w/2,h/2,sz*d/2,.12,h,.12,this.c.road);
    for(const sz of [-1,1]){this.frame(n,0,.12,sz*d/2,w,h-.12,this.c.road,.1);this.box(n,0,h/2,sz*d/2,w-.16,h-.2,.025,this.c.secondary,.2);this.beam(n,new Vector3(-w/2,h,sz*d/2),new Vector3(0,h+.7,sz*d/2),.13,this.c.road);this.beam(n,new Vector3(0,h+.7,sz*d/2),new Vector3(w/2,h,sz*d/2),.13,this.c.road);}
    this.box(n,0,h+.7,0,.12,.12,d,this.c.road);for(const sx of [-1,1])this.box(n,sx*w/2,h/2,0,.03,h-.2,d-.18,this.c.secondary,.15);
    return n;
  }
  private flower(g:TransformNode,x:number,y:number,z:number,size=.55,multi=false):TransformNode {
    const n=this.node('cover-flower',g,x,y,z);this.box(n,0,-size*.8,0,.07,size*1.6,.07,this.c.ink);
    const count=multi?7:5;for(let i=0;i<count;i++){const a=i*TAU/count;const px=Math.cos(a)*size*.63,py=Math.sin(a)*size*.63;this.ball(n,px,py,0,size*.43,this.c.ink,.94,1.05,.4);this.ball(n,px,py,.055,size*.36,multi?RAINBOW[i]:this.c.accent,1,1.04,.4);}
    this.disc(n,0,0,.1,size*.32,.12,this.c.ink);this.disc(n,0,0,.18,size*.25,.07,GOLD);return n;
  }
  private water(g:TransformNode,w=3,d=2):void {this.box(g,0,.015,0,w,.04,d,this.c.secondary,.45);this.box(g,0,-.03,0,w+.18,.06,d+.18,this.c.roadSide);}
  private clock(g:TransformNode,x:number,y:number,z:number,r=.6,moving=false):void {
    this.disc(g,x,y,z,r,.18,this.c.ink);this.disc(g,x,y,z+.11,r*.88,.08,this.c.road);for(let i=0;i<4;i++){const a=i*Math.PI/2;this.disc(g,x+Math.sin(a)*r*.64,y+Math.cos(a)*r*.64,z+.17,r*.045,.025,this.c.accent);}
    const hands=this.node('clock-hands',g,x,y,z+.19);this.box(hands,0,r*.21,0,.045,r*.42,.04,this.c.ink);this.box(hands,r*.16,0,0,r*.32,.045,.04,this.c.accent);if(moving)this.motion(hands,t=>{hands.rotation.z=-t*.07;});
  }
  private phone(g:TransformNode,x:number,y:number,z:number,w=1.4,h=2.7):TransformNode {
    const n=this.node('telephone',g,x,y,z);this.box(n,0,h/2,0,w,h,.3,this.c.ink);this.box(n,0,h/2,.17,w-.15,h-.24,.04,this.c.road);this.box(n,0,h-.17,.2,w*.26,.07,.02,this.c.ink);this.disc(n,0,.15,.2,.065,.02,this.c.accent);
    this.box(n,0,h*.62,.22,w*.65,.42,.035,this.c.secondary);this.box(n,.12,h*.4,.22,w*.5,.3,.035,this.c.accent);this.ears(n,0,h*.78,-.18,.24,this.c.road);return n;
  }
  private umbrella(g:TransformNode,x:number,z:number,color=this.c.secondary,scale=1):TransformNode {const n=this.node('park-umbrella',g,x,0,z);n.scaling.setAll(scale);this.box(n,0,1.1,0,.08,2.2,.08,this.c.ink);const top=this.mesh(n,'cone',color,0,2.25,0,2.6,.55,2.6);top.rotation.y=Math.PI/4;this.box(n,0,2.02,0,1.84,.07,1.84,this.c.road);return n;}
  private bicycle(g:TransformNode,x:number,z:number,scale=1):void {const n=this.node('bicycle',g,x,.05,z);n.scaling.setAll(scale);for(const s of [-1,1])this.ring(n,s*.62,.42,0,.39,this.c.ink);const points=[[-.62,.42],[-.2,1.05],[.16,.42],[.5,1.05],[.62,.42]];for(let i=0;i<points.length-1;i++)this.beam(n,new Vector3(points[i][0],points[i][1],0),new Vector3(points[i+1][0],points[i+1][1],0),.06,this.c.accent);this.beam(n,new Vector3(-.62,.42,0),new Vector3(.16,.42,0),.06,this.c.accent);this.box(n,-.22,1.1,0,.35,.08,.16,this.c.ink);this.box(n,.49,1.2,0,.08,.3,.07,this.c.ink);this.box(n,.63,1.34,0,.3,.06,.07,this.c.ink);this.disc(n,.68,1.39,.04,.055,.035,GOLD);}
  private camera(g:TransformNode,x:number,y:number,z:number,scale=1):TransformNode {const n=this.node('camcorder',g,x,y,z);n.scaling.setAll(scale);this.box(n,0,.45,0,.95,.65,.52,this.c.ink);this.disc(n,.52,.45,.02,.24,.3,this.c.roadSide).rotation.y=Math.PI/2;this.box(n,-.35,.95,0,.48,.14,.16,this.c.ink);this.box(n,-.58,.51,.26,.12,.42,.55,this.c.roadSide);this.box(n,-.65,.53,.3,.02,.29,.4,this.c.secondary);this.disc(n,.2,.62,.28,.045,.025,this.c.accent);this.box(n,0,-.05,0,.08,.45,.08,this.c.ink);for(const s of [-1,1])this.beam(n,new Vector3(0,.1,0),new Vector3(s*.4,-.55,.15),.06,this.c.ink);return n;}
  private awning(g:TransformNode,x:number,y:number,z:number,w=2.5):void {const n=this.node('striped-awning',g,x,y,z);n.rotation.x=-.12;for(let i=0;i<5;i++)this.box(n,(i-2)*w/5,0,0,w/5,.13,1.1,i%2?this.c.road:this.c.accent);for(const s of [-1,1])this.box(g,x+s*w*.45,y/2,z+.42,.065,y,.065,this.c.ink);}
  private radio(g:TransformNode,x:number,y:number,z:number,scale=1,animated=false):TransformNode {const n=this.node('old-radio',g,x,y,z);n.scaling.setAll(scale);this.box(n,0,.5,0,1.9,1,.62,this.c.road);this.box(n,0,.5,.33,1.72,.82,.04,this.c.ink);this.disc(n,-.49,.5,.39,.3,.04,this.c.roadSide);for(let i=0;i<4;i++)this.box(n,-.49,.32+i*.12,.43,.45,.025,.03,this.c.road);this.box(n,.4,.64,.39,.65,.25,.03,this.c.roadSide);for(let i=0;i<5;i++)this.box(n,.14+i*.13,.64,.42,.065,.17,.03,RAINBOW[i]);const needle=this.node('bunny-tuning-pointer',n,.12,.64,.46);this.box(needle,0,0,0,.035,.23,.03,this.c.road);this.ears(needle,0,.1,0,.12,this.c.road);if(animated)this.motion(needle,(t,p)=>{needle.position.x=.14+Math.min(1,p/.85)*.52+Math.sin(t*.8)*.025;});for(const x of [.2,.65])this.disc(n,x,.27,.42,.09,.05,this.c.road);this.beam(n,new Vector3(.5,1,0),new Vector3(.88,1.85,0),.045,this.c.road);return n;}
  private boat(g:TransformNode,x:number,y:number,z:number,scale=1):TransformNode {const n=this.node('folded-paper-boat',g,x,y,z);n.scaling.setAll(scale);this.box(n,0,.1,0,.9,.12,.45,this.c.road);for(const s of [-1,1]){const side=this.box(n,0,.23,s*.2,.94,.25,.055,this.c.road);side.rotation.x=s*.42;}const sail=this.mesh(n,'cone',this.c.road,0,.56,0,.65,.6,.1);sail.rotation.y=Math.PI/4;return n;}
  private deer(g:TransformNode,x:number,z:number):TransformNode {const n=this.node('snow-deer',g,x,0,z);this.ball(n,0,.65,0,.43,'#A28B80',1.35,.8,.65);for(const a of [-.3,.3])for(const b of [-.17,.17])this.box(n,a,.28,b,.065,.55,.065,this.c.ink);const neck=this.box(n,.35,1.02,0,.19,.6,.2,'#A28B80');neck.rotation.z=-.3;const head=this.node('deer-looking-back',n,.45,1.39,0);this.ball(head,.1,0,0,.23,'#B59D8D',1.35,.7,.75);for(const s of [-1,1]){const ear=this.ball(head,-.05,.19,s*.15,.13,'#B59D8D',.6,1.2,.55);ear.rotation.x=s*.55;this.ball(head,.18,.035,s*.135,.025,this.c.ink);}this.motion(head,(t,p)=>{head.rotation.y=Math.sin(t*.25)*.14+Math.max(0,p-.5)*2;});return n;}
  private grass(g:TransformNode,x:number,z:number,scale=1):void {for(let i=0;i<3;i++){const blade=this.box(g,x+(i-1)*.11,.15*scale,z,.07*scale,.3*scale,.07*scale,this.c.secondary);blade.rotation.z=(i-1)*.3;}}
  private message(g:TransformNode,x:number,y:number,z:number,w=1.3,h=.8,color=this.c.road):void {this.box(g,x,y,z,w,h,.15,this.c.ink);this.box(g,x,y,z+.09,w-.1,h-.1,.06,color);this.box(g,x-w*.24,y-h*.5,z,.22,.24,.14,this.c.ink);this.box(g,x-w*.24,y-h*.46,z+.09,.12,.16,.06,color);for(let i=0;i<3;i++)this.disc(g,x+(i-1)*w*.2,y,z+.14,.055,.025,this.c.accent);}

  createScenery(variant:number,chapter:number,seed:number):TransformNode {
    const {root,g}=this.begin('scenery');const choice=((variant%4)+4)%4;const ch=Math.max(0,Math.min(3,chapter));const v=STAGING[this.art.id]?.[ch][choice%2]??choice;root.metadata.chapter=ch;root.metadata.motif=v;if(choice>1){g.scaling.x=.92;g.scaling.z=.92;}const jitter=(Math.sin(seed*12.9898)*.5+.5)*.15;
    switch(this.art.id){
      case 'attention':{
        this.base(g,3.8,3.1);
        if(v===0){for(let i=0;i<3;i++)this.box(g,0,.14+i*.23,-.65+i*.55,3.25,.28+i*.46,.52,i%2?this.c.road:this.c.accent);this.box(g,0,.035,1.25,2.9,.03,.045,this.c.road);}
        else if(v===1){this.building(g,0,0,2.5,2.3+ch*.22,2,this.c.accent,ch);this.box(g,-.9,3.1,.5,.05,.75,.05,this.c.ink);this.box(g,-.6,3.33,.5,.58,.34,.04,this.c.road);}
        else if(v===2){this.box(g,0,.05,0,3.3,.1,2.6,this.c.accent);for(const x of [-1.4,1.4])this.box(g,x,.11,0,.04,.025,2.3,this.c.road);this.box(g,0,.12,0,.035,.03,2.3,this.c.road);const r=this.ring(g,0,.12,0,.55,this.c.road);r.rotation.x=0;}
        else {this.bench(g,-.15,.3);for(const x of [-1.2,1.2])this.plant(g,x,-.6,.7,this.c.accent);this.frame(g,0,.1,-1,2.8,2.5,this.c.road,.15);}
        break;
      }
      case 'hype-boy':{
        this.base(g,3.7,3.3);this.box(g,0,.1,0,3.25,.2,2.8,this.c.accent);
        if(v===0){this.building(g,-.65,-.45,1.45,2.1,1.4,this.c.road,ch);this.envelope(g,.8,1.1,.9,.75);this.box(g,.8,.45,.9,.08,.9,.08,this.c.ink);}
        else if(v===1){for(const x of [-1,1]){this.box(g,x,.7,-.5,.7,1.2,.6,this.c.ink);this.disc(g,x,.72,-.16,.21,.03,this.c.secondary);}this.record(g,0,.27,.5,1,false);this.ball(g,0,2.3,-.3,.5,this.c.road);}
        else if(v===2){this.frame(g,0,.2,-.7,2.8,2.8,this.c.road);for(let i=0;i<4;i++)this.ball(g,(i-1.5)*.65,2.75,-.65,.11,i%2?GOLD:this.c.secondary);this.bench(g,0,.8,this.c.secondary,.8);}
        else {for(let i=0;i<4;i++){const e=this.envelope(g,(i-1.5)*.62,1.1+Math.sin(i)*.3,0,.6,i%2?this.c.road:this.c.secondary);e.rotation.z=(i-1.5)*.18;}this.box(g,0,.23,0,2.9,.16,1.6,this.c.road);}
        break;
      }
      case 'cookie':{
        this.base(g,4.3,3.2);
        if(v===0){this.box(g,0,.62,0,3.6,.36,1.2,this.c.road);this.box(g,0,.83,0,3.4,.06,.85,this.c.ink);for(let i=0;i<4;i++)this.record(g,-1.25+i*.82,.91,0,.32,false,ch>0);for(const x of [-1.3,1.3])this.box(g,x,.28,0,.18,.56,.7,this.c.accent);}
        else if(v===1){this.box(g,0,1.15,0,2.6,2.3,1.5,this.c.accent);this.cassette(g,0,1.55,.78,2.2,1.2,this.c.road);this.box(g,0,.58,.9,1.4,.43,.2,this.c.ink);this.record(g,0,.38,1.1,.43,false,true);}
        else if(v===2){for(const x of [-1.25,1.25])this.box(g,x,1.2,0,.12,2.4,.65,this.c.accent);for(let k=0;k<3;k++){this.box(g,0,.25+k*.8,0,2.7,.12,.82,this.c.road);for(let i=0;i<3;i++)this.record(g,-.8+i*.8,.33+k*.8,0,.3,false,true);}}
        else {this.box(g,0,.5,0,2.7,1,1.8,this.c.road);this.box(g,0,1.04,0,2.9,.08,2,this.c.accent);this.record(g,-.55,1.15,0,.68,false,true);this.envelope(g,.9,1.35,.2,.6);this.bunny(g,.95,-.65,.55);}
        break;
      }
      case 'hurt':{
        this.base(g,3.6,3);
        if(v===0){this.frame(g,0,0,-.7,2.7,2.8,this.c.road,.16);this.box(g,0,1.42,-.72,2.35,2.45,.035,this.c.secondary,.2);this.box(g,0,.82,.4,2.4,.16,1.05,this.c.roadSide);this.envelope(g,-.35,.95,.6,.5);this.lamp(g,.8,.45,1.2);}
        else if(v===1){this.greenhouse(g,0,0,2.5,2,2);this.plant(g,.55,0,.7);}
        else if(v===2){this.bench(g,-.1,0,this.c.roadSide,.9);this.plant(g,1,-.75,.8);this.water(g,2.9,2.1);}
        else {this.water(g,3,2.4);for(let i=0;i<3;i++){const n=this.plant(g,(i-1)*.85,-.65,.7);n.rotation.y=i;}this.box(g,0,.08,.9,2.6,.12,.45,this.c.road);}
        break;
      }
      case 'omg':{
        this.base(g,3.5,3.3);
        if(v===0){this.phone(g,0,.03,0,1.8,3.2);this.message(g,1.05,2.2,.35,1.1,.7);}
        else if(v===1){this.building(g,-.45,-.1,2.1,2.3,1.9,this.c.accent,ch);this.message(g,.5,2.9,.95,1.4,.85);this.box(g,1.1,.35,.7,.8,.7,.8,this.c.secondary);}
        else if(v===2){for(let i=0;i<3;i++)this.message(g,(i-1)*.72,1.1+i*.65,(i%2)*.25,1.2,.65,i%2?this.c.secondary:this.c.road);this.box(g,0,.17,0,2.8,.3,2.1,this.c.accent);}
        else {this.bench(g,0,.3,this.c.road);for(let i=0;i<3;i++)this.lamp(g,(i-1)*1.1,-.8,1.3+i*.3);}
        break;
      }
      case 'ditto':{
        this.base(g,4,3.1,this.c.road);
        if(v===0){this.building(g,0,-.3,3,2.8,1.9,this.c.accent,ch);this.box(g,0,2.97,-.3,3.3,.16,2.1,this.c.road);}
        else if(v===1){this.camera(g,-.5,.6,.2,1.3);this.box(g,.9,.5,-.1,.85,1,.68,this.c.roadSide);this.box(g,.9,.6,.26,.64,.49,.03,this.c.ink);}
        else if(v===2){this.bench(g,0,.35,this.c.accent);this.box(g,0,1.3,.09,1.86,.08,.2,this.c.road);this.lamp(g,1.3,-.6,2.2);}
        else {this.frame(g,0,.15,-.4,2.8,2.7,this.c.accent,.17);for(const x of [-.65,.65])this.window(g,x,.5,-.32,.85,1.7,ch>1);this.box(g,0,2.95,-.4,3.1,.12,.5,this.c.road);}
        break;
      }
      case 'new-jeans':{
        this.base(g,3.6,3.3,this.c.secondary);
        if(v===0){this.building(g,-.6,-.3,1.45,2.35,1.4,this.c.accent,ch);this.building(g,.85,.25,1.05,1.4,1.2,this.c.secondary,ch);this.pixelStar(g,-.45,3.1,-.2,.7);}
        else if(v===1){this.frame(g,0,.1,0,2.2,2.7,'#BBA3EE',.3);this.box(g,0,1.5,-.15,1.5,1.8,.1,this.c.secondary);this.pixelStar(g,0,1.65,.02,.8,this.c.road);}
        else if(v===2){for(let i=0;i<5;i++){this.box(g,(i-2)*.48,.28+i*.24,0,.48,.18,2.1,RAINBOW[i]);this.box(g,(i-2)*.48,.95+i*.24,-.95,.48,1.25,.2,RAINBOW[i]);}}
        else {this.cyl(g,0,.1,0,1.45,.18,this.c.ink);this.cyl(g,0,.22,0,1.33,.1,this.c.road);this.plant(g,0,0,.9);this.disc(g,.8,.65,.35,.3,.12,this.c.accent);}
        break;
      }
      case 'super-shy':{
        this.base(g,3.8,3.4,this.c.secondary);
        if(v===0){this.umbrella(g,-.3,-.4,this.c.accent,.95);this.bench(g,.1,.85,this.c.road,.8);}
        else if(v===1){this.bicycle(g,-.15,.4,1.1);this.plant(g,1.25,-.7,.8);this.box(g,0,.055,0,3.2,.08,2.7,this.c.road);}
        else if(v===2){this.box(g,0,1.05,0,3.15,1.65,1.3,this.c.road);this.box(g,0,1.82,0,3.25,.16,1.4,this.c.accent);for(let i=0;i<4;i++)this.box(g,-1.1+i*.73,1.27,.68,.56,.65,.04,RAINBOW[i+2]);for(const x of [-1,1])this.disc(g,x,.38,.63,.29,.18,this.c.ink);}
        else {this.cyl(g,0,.15,0,1.4,.3,this.c.road);this.cyl(g,0,.35,0,1.17,.1,this.c.secondary);for(let i=0;i<3;i++)this.box(g,(i-1)*.55,.65,0,.16,.6+i*.15,.16,this.c.road);this.pixelStar(g,0,1.4,0,.5);}
        break;
      }
      case 'eta':{
        this.base(g,3.7,3.2);
        if(v===0){this.phone(g,-.5,.1,0,1.6,2.8);this.message(g,.9,1.25,.6,1.2,.7);}
        else if(v===1){for(let i=0;i<3;i++)this.building(g,(i-1)*1.05,(i%2)*.45,1,1.9+i*.35,1.25,i%2?this.c.road:this.c.accent,ch);}
        else if(v===2){this.box(g,0,1.6,0,.15,3.2,.15,this.c.ink);for(let i=0;i<3;i++){this.box(g,-.85+i*.85,2.2+i*.3,0,.55,.25+i*.2,.25,this.c.accent);this.box(g,-.85+i*.85,1.5,0,.055,1.3,.055,this.c.ink);}this.message(g,0,.65,.5,2,.65);}
        else {this.bench(g,0,0,this.c.road);this.lamp(g,-1.2,-.6,1.9);this.lamp(g,1.2,-.6,1.9);}
        break;
      }
      case 'cool-with-you':{
        this.base(g,3.6,3.2);this.water(g,3.3,2.9);
        if(v===0){this.frame(g,0,0,-.3,2.5,3.1,this.c.road,.22);this.frame(g,0,.3,-.65,1.85,2.3,this.c.secondary,.1);}
        else if(v===1){for(const x of [-1,1]){this.box(g,x,1.45,-.5,.35,2.9,.4,this.c.road);this.box(g,x,2.95,-.5,.62,.15,.65,this.c.road);}this.box(g,0,.06,.6,2.7,.09,.75,this.c.road);}
        else if(v===2){for(let i=0;i<3;i++)this.window(g,(i-1)*.9,.1,-.8,.48,2.65,true);this.box(g,0,.06,-.8,3,.12,.5,this.c.roadSide);}
        else {this.bench(g,-.2,.3,this.c.roadSide,.9);this.frame(g,.7,.15,-.75,1,1.5,this.c.secondary,.1);}
        break;
      }
      case 'get-up':{
        this.base(g,3.5,3);if(v===0)this.water(g,3,2.5);else if(v===1)this.frame(g,0,0,0,2.2,2.5,this.c.road,.18);else if(v===2){for(let i=0;i<5;i++)this.grass(g,(i-2)*.45,(i%2)*.6,.8);this.box(g,0,.03,0,3,.04,2.5,this.c.secondary);}else {this.box(g,0,.12,0,1.8,.24,.8,this.c.road);this.ball(g,0,.65,-.5,.15,GOLD);}break;
      }
      case 'asap':{
        this.base(g,3.7,3.4,this.c.secondary);
        if(v===0){this.box(g,0,1.2,0,.1,2.4,.1,this.c.road);this.clock(g,0,2.25,0,.65);this.envelope(g,.9,.5,.5,.65);}
        else if(v===1){this.water(g,3,2.6);for(const x of [-1,1])this.flower(g,x,.65,-.5,.35,false);}
        else if(v===2){this.building(g,0,-.2,1.8,1.7,1.6,this.c.roadSide,ch);const roof=this.mesh(g,'cone',this.c.secondary,0,2.25,-.2,2.6,1,2.3);roof.rotation.y=Math.PI/4;this.window(g,0,.4,.63,.55,.75,ch===3);}
        else {for(let i=0;i<3;i++){this.grass(g,(i-1)*.8,0,1.4);this.flower(g,(i-1)*.8,.8,(i%2)*.4,.3,false);}this.box(g,0,.04,0,2.9,.06,2.4,this.c.roadSide);}
        break;
      }
      case 'how-sweet':{
        this.base(g,4.1,3.4);
        if(v===0){this.building(g,0,-.25,2.9,2.5,1.8,this.c.ink,ch);this.awning(g,0,2.05,.95,3);this.record(g,0,1.55,.7,.55,true);}
        else if(v===1){this.box(g,0,.8,-.5,2.8,1.6,.7,this.c.road);this.awning(g,0,2.2,.15,3.1);this.bench(g,0,.85,this.c.accent,.75);}
        else if(v===2){this.box(g,0,.6,0,2.6,1.2,1.1,this.c.ink);for(let i=0;i<3;i++){this.box(g,(i-1)*.78,1.43,0,.7,.65,.08,i%2?this.c.road:this.c.accent);this.record(g,(i-1)*.78,1.43,.075,.24,true);}}
        else {this.box(g,0,.05,0,3.4,.07,2.8,this.c.road);for(let i=0;i<4;i++)this.box(g,(i-1.5)*.78,.095,(i%2)*.85-.4,.72,.025,.8,this.c.ink);this.plant(g,1.3,-.9,.8,this.c.secondary);}
        break;
      }
      case 'bubble-gum':{
        this.base(g,4,3.4,this.c.secondary);
        if(v===0){this.box(g,0,.5,-.9,3.6,1, .6,this.c.roadSide);this.box(g,0,1.05,-.9,3.8,.12,.8,this.c.road);this.boat(g,.2,.08,.6,.9);}
        else if(v===1){this.greenhouse(g,0,0,2.8,2.25,2.05);this.plant(g,-.7,.2,.6);this.plant(g,.7,.2,.65);}
        else if(v===2){this.box(g,0,.7,0,2.6,.16,1.4,this.c.road);for(const x of [-.9,.9])this.box(g,x,.34,0,.13,.68,1.2,this.c.roadSide);this.bench(g,0,.95,this.c.secondary,.7);for(let i=0;i<3;i++){this.box(g,(i-1)*.7,1.4,-.7,.025,2.2,.025,this.c.road);this.ball(g,(i-1)*.7,2.5+jitter+i*.15,-.7,.31,RAINBOW[i+2],1,1.25,1);}}
        else {this.water(g,3.5,2.8);for(let i=0;i<3;i++)this.ball(g,(i-1)*.9,1+i*.45,0,.25+i*.08,this.c.road,1,1,1,.35);}
        break;
      }
      case 'supernatural':{
        this.base(g,3.8,3.4,this.c.ink);
        if(v===0){this.building(g,-.35,0,1.9,2.8,1.8,this.c.ink,ch);for(let i=0;i<3;i++)this.disc(g,-.35,.7+i*.8,.95,.25,.05,RAINBOW[i*2]);this.flower(g,.8,2.9,-.3,.55,true);}
        else if(v===1){this.box(g,0,.65,0,2.6,1.3,1.5,this.c.roadSide);this.radio(g,0,1.3,0,1.1);}
        else if(v===2){this.box(g,0,1.25,0,.15,2.5,.15,this.c.road);const dish=this.node('rooftop-dish',g,0,2.5,0);this.disc(dish,0,0,0,.8,.15,this.c.secondary);this.disc(dish,0,0,.11,.6,.08,this.c.ink);this.ball(dish,0,0,.25,.12,GOLD);dish.rotation.x=-.35;}
        else {this.bench(g,0,.35,this.c.road,.9);this.disc(g,0,2.25,-.8,.65,.08,GOLD);this.pixelStar(g,1.2,2.7,-.3,.25,this.c.road);}
        break;
      }
      case 'right-now':{
        this.base(g,3.7,3.4,this.c.secondary);
        if(v===0){for(let i=0;i<3;i++){const x=(i-1)*.9;this.box(g,x,.65,0,.1,1.3,.1,this.c.ink);this.box(g,x,1.4,0,.72,.55,.55,RAINBOW[i*2]);this.box(g,x,1.43,.29,.45,.055,.03,this.c.ink);this.flower(g,x,2.1,0,.33,true);}}
        else if(v===1){this.greenhouse(g,0,0,2.6,2.2,1.9);for(const x of [-.65,.65])this.flower(g,x,1.1,.25,.45,true);}
        else if(v===2){this.message(g,0,2,0,2.6,1.5,this.c.road);this.box(g,0,.7,0,.12,1.4,.12,this.c.ink);this.plant(g,-1,.4,.6);this.plant(g,1,.4,.6);}
        else {for(let i=0;i<3;i++){this.cyl(g,(i-1)*.85,.25,0,.32,.5,this.c.road);this.flower(g,(i-1)*.85,1.15,0,.48,true);}this.box(g,0,.05,0,3,.1,1.4,this.c.ink);}
        break;
      }
    }
    return this.finish(root);
  }

  createLandmark(chapter:number):TransformNode {
    const {root,g}=this.begin('landmark');const ch=Math.max(0,Math.min(3,chapter));
    switch(this.art.id){
      case 'attention':{
        this.base(g,6.4,5.4,this.c.accent);
        for(let i=0;i<4;i++)this.box(g,0,.16+i*.25,-.95+i*.7,5.6,.32+i*.5,.65,i%2?this.c.secondary:this.c.road);
        this.frame(g,0,1.1,-1.1,3.3,2.7,this.c.road,.32);this.ears(g,0,3.7,-1.1,1.8,this.c.road);
        for(const s of [-1,1]){this.box(g,s*2.5,2.1,-1.5,.08,2.6,.08,this.c.ink);this.box(g,s*2.1,3.16,-1.5,.85,.55,.05,this.c.road);}
        for(let i=0;i<5;i++)this.box(g,(i-2)*.65,.3,2, .38,.1,.5,this.c.accent);
        break;
      }
      case 'hype-boy':{
        this.base(g,6.5,5.6,this.c.accent);this.cyl(g,0,.2,0,2.45,.4,this.c.road);const disc=this.record(g,0,.43,0,2.15);this.motion(disc,t=>{disc.rotation.y=t*.07;});
        for(const x of [-2.2,2.2]){this.box(g,x,2.1,-1,.15,4.2,.15,this.c.road);this.box(g,x,.85,.55,.8,1.6,.7,this.c.ink);for(const y of [.55,1.15])this.disc(g,x,y,.93,.22,.06,this.c.secondary);}this.box(g,0,4.15,-1,4.55,.16,.18,this.c.road);
        const globe=this.node('record-mirror-ball',g,0,3.2,-1);this.ball(globe,0,0,0,.8,this.c.secondary);for(let i=0;i<8;i++){const a=i*TAU/8;const tile=this.box(globe,Math.cos(a)*.76,0,Math.sin(a)*.76,.28,.45,.035,this.c.road);tile.rotation.y=-a+Math.PI/2;}this.motion(globe,t=>{globe.rotation.y=t*.18;});
        for(let i=0;i<5;i++)this.ball(g,(i-2)*.75,4.15,-.85,.11,i%2?GOLD:this.c.secondary);break;
      }
      case 'cookie':{
        this.base(g,6.8,5.2);this.box(g,0,1.5,-.5,4.9,3,1.8,this.c.accent);this.box(g,0,2.15,.44,4.55,1.25,.14,this.c.road);
        for(const x of [-1.35,1.35]){const reel=this.record(g,x,2.15,.62,.68,true,true);this.motion(reel,t=>{reel.rotation.y=0;reel.rotation.z=t*.24;});}
        this.box(g,0,2.14,.57,1.35,.45,.15,this.c.secondary);this.box(g,0,.91,.48,2.65,.8,.12,this.c.ink);this.box(g,0,.45,1.4,4.8,.4,1.7,this.c.road);this.box(g,0,.68,1.4,4.5,.07,1.05,this.c.ink);
        for(let i=0;i<5;i++)this.record(g,(i-2)*.85,.76,1.45,.34,false,i>1||ch>1);
        this.box(g,0,3.12,-.5,5.15,.2,2.05,this.c.road);for(let i=0;i<5;i++)this.box(g,-.8+i*.4,3.35,-.2,.17,.25+(i%3)*.1,.17,this.c.secondary);this.bunny(g,2.6,1.4,.65);break;
      }
      case 'hurt':{
        this.base(g,6.3,5.4);this.greenhouse(g,0,-.55,4.2,3.5,3);this.water(g,5.6,4.7);
        this.bench(g,-1.35,.75,this.c.roadSide,.85);this.box(g,.8,.78,.8,1.6,.14,1.1,this.c.road);for(const x of [.25,1.35])this.box(g,x,.36,.8,.09,.72,.7,this.c.roadSide);const e=this.envelope(g,.8,.88,.85,.63);e.rotation.x=-1.1;
        this.lamp(g,1.55,.1,1.8);this.plant(g,-2.35,-1.2,.8);this.ears(g,-1.35,.02,1.55,.32,this.c.secondary);break;
      }
      case 'omg':{
        this.base(g,6,5.2,this.c.secondary);this.box(g,0,.16,0,4.2,.32,2.2,this.c.road);this.frame(g,0,.32,0,3.4,4.55,this.c.accent,.42);this.frame(g,0,.54,.12,2.83,3.9,this.c.ink,.12);this.box(g,0,4.65,.25,.85,.12,.06,this.c.road);this.disc(g,0,.58,.26,.17,.06,this.c.road);
        for(let i=0;i<3;i++){const msg=this.node('floating-message',g,(i-1)*1.5,2.2+i*.6,.65);this.message(msg,0,0,0,1.05,.65,i%2?this.c.secondary:this.c.road);this.motion(msg,t=>{msg.position.y=2.2+i*.6+Math.sin(t*.65+i)*.07;});}
        for(const s of [-1,1])this.lamp(g,s*2.25,1.25,1.9);this.box(g,-2.2,.4,-1,.85,.8,.85,this.c.road);break;
      }
      case 'ditto':{
        this.base(g,6.9,5.3,this.c.road);this.building(g,-1.95,-.45,1.7,2.8,2.7,this.c.accent,ch);this.building(g,1.95,-.45,1.7,2.8,2.7,this.c.accent,ch);this.box(g,0,2.6,-.45,2,5.2,2.4,this.c.accent);this.box(g,0,5.28,-.45,2.3,.18,2.7,this.c.road);const roof=this.mesh(g,'cone',this.c.road,0,5.67,-.45,2.65,.7,2.65);roof.rotation.y=Math.PI/4;
        this.clock(g,0,4.45,.82,.62);this.frame(g,0,.05,.83,1.05,2.05,this.c.road,.15);this.box(g,0,1.05,.79,.8,1.8,.04,this.c.ink);this.window(g,-1.95,.65,.94,.6,1.6,ch>1);this.window(g,1.95,.65,.94,.6,1.6,ch>1);this.camera(g,2.1,.64,1.75,.65);
        // Two physical film cards: the notch distinguishes the A/B viewpoints without UI text.
        for(const s of [-1,1]){this.box(g,s*1.2,.12,1.9,.65,.06,.85,this.c.secondary);this.box(g,s*1.2,.16,1.9,.5,.025,.55,this.c.ink);this.box(g,s*1.2+s*.14,.19,1.9,.08,.02,.3,this.c.road);}break;
      }
      case 'new-jeans':{
        this.base(g,6.3,5.5,this.c.secondary);for(let i=0;i<3;i++)this.box(g,0,.16+i*.26,0,5.7-i*.5,.32,4.7-i*.5,i%2?'#BBA3EE':this.c.road);
        this.frame(g,0,.8,0,3.55,3.25,'#BBA3EE',.45);for(const x of [-.9,.9]){this.box(g,x,4.65,0,.58,1.6,.5,this.c.road);this.box(g,x,4.67,.27,.26,1.15,.04,this.c.accent);}this.box(g,0,3.85,0,2.8,.55,.52,this.c.road);
        for(let i=0;i<5;i++)this.box(g,(i-2)*.55,.86,1.3,.55,.11,1.8,RAINBOW[i]);this.pixelStar(g,-2.25,2.3,-.5,.8,GOLD);this.plant(g,2.3,1.1,.8);break;
      }
      case 'super-shy':{
        this.base(g,6.5,5.6,this.c.secondary);this.box(g,0,.2,0,3.4,.4,3.1,this.c.road);this.box(g,0,.43,0,2.95,.08,2.6,'#8DCEDF');this.box(g,0,.65,0,1.6,.4,1.4,this.c.accent);this.box(g,0,.9,0,1.35,.12,1.16,this.c.road);
        for(let i=0;i<5;i++){const x=(i-2)*.32;this.box(g,x,1.35+Math.sin(i)*.14,0,.15,.9+Math.sin(i)*.28,.15,this.c.road);}this.pixelStar(g,0,2.25,0,.65,GOLD);
        this.bicycle(g,-2.15,1.4,.85);this.umbrella(g,2.1,-.75,this.c.accent,.85);this.bench(g,2,.6,this.c.road,.62);break;
      }
      case 'eta':{
        this.base(g,6.3,5.3);this.box(g,0,.2,0,3.2,.4,2.7,this.c.road);this.box(g,0,2.3,-.5,.2,4.6,.2,this.c.ink);
        for(let i=0;i<3;i++){this.box(g,(i-1)*1.05,4.05+i*.35,-.5,.7,.7+i*.45,.4,i%2?this.c.secondary:this.c.accent);this.box(g,(i-1)*1.05,2.9,-.5,.08,2.4,.08,this.c.ink);}this.phone(g,-2.15,.05,.8,1.2,2.5);
        for(let i=0;i<5;i++){this.window(g,-1.5+i*.73,.6+(i%2)*.4,1.2,.48,.75,true);this.box(g,-1.5+i*.73,.36,1.1,.62,.3,.5,this.c.roadSide);}this.message(g,1.7,3.2,.15,1.5,.8);break;
      }
      case 'cool-with-you':{
        this.base(g,6.2,5.8);this.water(g,5.7,5.2);
        for(let i=0;i<3;i++){this.frame(g,0,.08,-1.4+i*1.35,3.8-i*.28,3.7-i*.22,i===1?this.c.secondary:this.c.road,.23);this.box(g,0,.11,-1.4+i*1.35,4.4,.15,.62,this.c.road);}
        for(let i=0;i<5;i++)this.window(g,-2+i*.99,.15,-2.35,.42,2.1,true);this.box(g,0,.05,2.25,4.8,.08,.46,this.c.road);break;
      }
      case 'get-up':{
        this.base(g,6,5.2);this.water(g,5.5,4.7);this.frame(g,0,.08,-.75,3.4,3.6,this.c.road,.2);this.box(g,0,.06,-.75,4,.12,.65,this.c.road);for(let i=0;i<5;i++)this.window(g,-1.8+i*.9,.15,-1.9,.22,1.45,true);
        this.box(g,1.6,.04,1.1,1.7,.07,1.35,this.c.secondary);for(let i=0;i<4;i++)this.grass(g,1.1+i*.3,.9+(i%2)*.4,.7);break;
      }
      case 'asap':{
        this.base(g,6.1,5.3,this.c.secondary);this.water(g,5.4,4.6);this.box(g,-.65,1.2,-.25,.9,2.4,.65,this.c.roadSide);this.clock(g,-.65,3.25,-.22,1.05,true);this.frame(g,-.65,.4,.17,.78,1.75,this.c.road,.09);
        const pendulum=this.node('soft-pendulum',g,-.65,2.05,.28);this.box(pendulum,0,-.62,0,.045,1.25,.045,this.c.road);this.disc(pendulum,0,-1.21,0,.23,.1,GOLD);this.motion(pendulum,t=>{pendulum.rotation.z=Math.sin(t*.8)*.17;});
        this.envelope(g,-1.8,.45,1.5,.9);this.building(g,1.65,-.55,1.65,1.75,1.5,this.c.roadSide,ch);const roof=this.mesh(g,'cone',this.c.secondary,1.65,2.2,-.55,2.3,.9,2.2);roof.rotation.y=Math.PI/4;this.window(g,1.65,.45,.23,.48,.8,ch===3);this.flower(g,1.65,.7,1.2,.35,false);break;
      }
      case 'how-sweet':{
        this.base(g,6.5,5.5,this.c.ink);for(let x=0;x<4;x++)for(let z=0;z<3;z++)this.box(g,(x-1.5)*1.35,.045,(z-1)*1.45,1.3,.06,1.4,(x+z)%2?this.c.road:this.c.roadSide);
        for(const x of [-2,2])this.box(g,x,1.65,-.6,.48,3.3,.75,this.c.accent);this.cassette(g,0,3.3,-.6,5.1,2.45,this.c.accent);this.record(g,-1.15,.18,1.15,1.1,false);this.box(g,1.65,.8,1.1,1.2,1.6,.85,this.c.ink);this.record(g,1.65,1.3,1.55,.41,true);this.awning(g,-2.1,2.1,-1.6,1.25);break;
      }
      case 'bubble-gum':{
        this.base(g,6.4,5.6,this.c.secondary);this.greenhouse(g,0,-.5,4.2,3.2,2.8);for(const x of [-1.35,1.35])this.plant(g,x,-.35,.85);
        this.box(g,0,.35,2.05,5.8,.7,.65,this.c.roadSide);this.box(g,0,.76,2.05,6,.12,.85,this.c.road);for(let i=0;i<5;i++)this.box(g,(i-2)*1.05,.4,2.4,.04,.55,.03,this.c.secondary);this.boat(g,1.8,.82,2.04,.6);for(let i=0;i<3;i++)this.ball(g,-2.4+i*.35,2.7+i*.43,.8,.2+i*.05,this.c.road,1,1,1,.4);break;
      }
      case 'supernatural':{
        this.base(g,6.6,5.5,this.c.ink);this.box(g,0,.8,-.3,4,1.6,2.6,this.c.roadSide);this.box(g,0,1.64,-.3,4.25,.12,2.85,this.c.ink);this.box(g,0,2.3,-.45,.22,1.4,.22,this.c.road);
        const antenna=this.node('flower-satellite',g,0,3.8,-.5);const radius=1.75;
        for(let i=0;i<10;i++){const a=i*TAU/10;const x=Math.cos(a)*radius,y=Math.sin(a)*radius;const petal=this.ball(antenna,x,y,0,.66,this.c.ink,.85,1.25,.32);petal.rotation.z=a-Math.PI/2;const inside=this.ball(antenna,x,y,.08,.57,RAINBOW[i%7],.85,1.25,.34);inside.rotation.z=a-Math.PI/2;}
        this.disc(antenna,0,0,.12,1.18,.2,this.c.ink);this.disc(antenna,0,0,.26,1,.16,this.c.road);this.disc(antenna,0,0,.37,.31,.1,this.c.secondary);this.motion(antenna,(_t,p)=>{antenna.rotation.x=-.12-Math.max(0,p-.7)*.65;});
        this.radio(g,-1.1,1.72,.45,.7);this.bench(g,1.3,1.8,this.c.road,.7);break;
      }
      case 'right-now':{
        this.base(g,6.6,5.5,this.c.secondary);this.frame(g,0,.1,-.55,3.6,3.7,this.c.ink,.23);this.frame(g,0,.22,-.4,3.25,3.4,this.c.road,.18);
        for(let i=0;i<7;i++){const a=Math.PI*(i/6);this.flower(g,Math.cos(a)*2.1,2.6+Math.sin(a)*1.7,-.5,.6,true);}for(const x of [-2,2]){this.box(g,x,1.4,.75,.12,2.8,.12,this.c.ink);this.beam(g,new Vector3(x,2.8,.75),new Vector3(x*.5,3.5,-.6),.12,this.c.road);}
        for(let i=0;i<5;i++){this.cyl(g,(i-2)*.87,.27,1.55,.32,.54,this.c.road);this.flower(g,(i-2)*.87,1.35,1.55,.45,true);this.box(g,(i-2)*.87,.6,1.89,.16,.22,.025,RAINBOW[i]);}this.message(g,0,2.7,.1,1.7,.85);break;
      }
    }
    return this.finish(root);
  }

  createEasterEgg():TransformNode {
    const {root,g}=this.begin('egg');root.metadata.egg=this.art.egg.type;this.base(g,3.5,3.2);
    switch(this.art.id){
      case 'attention':{
        for(let i=0;i<5;i++){const w=this.node('window-turns-toward-you',g,(i-2)*.56,.3,-.5);this.frame(w,0,0,0,.49,1.15,this.c.road,.065);this.box(w,0,.57,-.035,.36,.98,.03,this.c.secondary);this.motion(w,(_t,p)=>{w.rotation.y=-.75+Math.max(0,Math.min(1,(p-.48-i*.025)*4))*.75;});}
        this.box(g,1.1,.035,1.05,.75,.035,.55,this.c.accent);this.ears(g,1.1,.1,1.06,.2,this.c.road);break;
      }
      case 'hype-boy':{
        const star=this.pixelStar(g,0,1.2,0,.8,GOLD);star.scaling.setAll(.01);
        for(let i=0;i<4;i++){const a=Math.PI/4+i*Math.PI/2;const e=this.envelope(g,Math.cos(a)*1.2,1.2+Math.sin(a)*.7,.1,.6,i%2?this.c.road:this.c.secondary);this.motion(e,(t,p)=>{const k=Math.max(0,Math.min(1,(p-.55)*2.9));e.position.x=Math.cos(a)*(1.2-k*.65);e.position.y=1.2+Math.sin(a)*(.7-k*.25)+Math.sin(t*.45+i)*.025;e.rotation.z=a-Math.PI/2;star.scaling.setAll(.01+k*.72);});}break;
      }
      case 'cookie':{
        this.box(g,0,.6,.1,2.6,.16,1.2,this.c.road);for(const x of [-.9,.9])this.box(g,x,.27,.1,.12,.54,.8,this.c.accent);for(let i=0;i<5;i++){const d=this.record(g,-.9+i*.45,.74,.1,.21,false,true);this.motion(d,(t)=>{d.rotation.y=t*.23+i;});}
        const rabbit=this.bunny(g,.95,-.85,.9);this.motion(rabbit.arm,t=>{rabbit.arm.rotation.z=.2+Math.sin(t*1.1)*.35;});this.box(g,-1.1,.28,-.9,.8,.56,.7,this.c.secondary);this.box(g,-1.1,.59,-.9,.84,.05,.74,this.c.road);break;
      }
      case 'hurt':{
        this.water(g,3.1,2.8);this.bench(g,-.55,.15,this.c.roadSide,.7);this.ears(g,-.55,.06,.85,.25,this.c.secondary);this.cyl(g,1,.24,-.3,.3,.48,this.c.road);
        const f=this.flower(g,1,1.05,-.3,.44,false);this.motion(f,(_t,p)=>{const k=Math.max(.08,Math.min(1,(p-.72)*4.2));f.scaling.set(k,k,k);});const letter=this.envelope(g,-.45,.65,.25,.42);letter.rotation.x=-.65;break;
      }
      case 'omg':{
        this.box(g,-.4,.48,0,1.4,.96,1.1,this.c.road);this.box(g,-.4,.96,0,1.48,.12,1.18,this.c.accent);
        const cat=this.node('cat-peeks-from-box',g,-.4,.85,0);this.box(cat,0,0,0,.72,.5,.55,this.c.ink);for(const s of [-1,1]){const ear=this.mesh(cat,'cone',this.c.ink,s*.24,.4,0,.4,.42,.35);ear.rotation.y=Math.PI/4;this.box(cat,s*.15,.04,.29,.05,.07,.02,GOLD);}this.motion(cat,(t,p)=>{cat.position.y=.85+Math.max(0,Math.min(.3,(p-.55)*1.1))+Math.sin(t*.55)*.035;});
        for(let i=0;i<3;i++){const s=this.pixelStar(g,.65+i*.34,1.7+i*.18,.1,.24,GOLD);this.motion(s,(t,p)=>{s.rotation.z=Math.sin(t*.5+i)*.1;s.scaling.setAll(.6+Math.min(.4,Math.max(0,p-.6)));});}break;
      }
      case 'ditto':{
        this.box(g,0,.02,0,3.1,.04,2.7,this.c.road);this.deer(g,-.35,.3);this.camera(g,1.05,.54,-.5,.6);for(const [x,z]of [[-.9,-.7],[.1,-1]]){this.box(g,x,.055,z,.5,.04,.65,this.c.secondary);this.box(g,x,.08,z,.34,.02,.37,this.c.ink);}break;
      }
      case 'new-jeans':{
        const p=this.plant(g,-.25,.05,1.15,this.c.secondary);this.motion(p,t=>{p.rotation.z=Math.sin(t*.8)*.1;});this.cyl(g,.95,.15,.7,.4,.2,this.c.ink);this.cyl(g,.95,.27,.7,.33,.04,this.c.accent);for(const x of [-.1,.1])for(const z of [-.1,.1])this.cyl(g,.95+x,.3,.7+z,.04,.025,this.c.ink);this.pixelStar(g,-1.05,1.5,-.4,.35,this.c.accent);break;
      }
      case 'super-shy':{
        this.umbrella(g,-.3,-.45,this.c.accent,.72);const b=this.bunny(g,.15,.15,.85);this.motion(b.body,(t,p)=>{b.body.position.x=.1+Math.max(0,Math.min(.65,(p-.55)*2));b.body.rotation.y=Math.sin(t*.35)*.09;});this.motion(b.arm,t=>{b.arm.rotation.z=.65+Math.sin(t*1.2)*.4;});this.disc(g,-1,.18,.85,.16,.05,GOLD);break;
      }
      case 'eta':{
        this.phone(g,0,.05,-.65,1.1,2.2);for(let i=0;i<5;i++){const n=this.node('friends-connect',g,(i-2)*.58,.2,.6);this.window(n,0,0,0,.38,.7,true);this.motion(n,(_t,p)=>{const k=Math.max(0,Math.min(1,(p-.48-i*.035)*5));n.scaling.y=.3+k*.7;});}this.ears(g,0,1.3,-.83,.22,this.c.accent);break;
      }
      case 'cool-with-you':{
        this.water(g,3.1,2.8);const feather=this.node('small-feather',g,.1,.9,0);feather.rotation.z=-.45;this.box(feather,0,0,0,.035,1.3,.035,this.c.road);for(let i=0;i<5;i++)for(const s of [-1,1]){const vane=this.box(feather,s*(.15-i*.018),-.38+i*.19,0,.3-i*.03,.11,.04,this.c.road);vane.rotation.z=s*.38;}
        const reflection=this.node('feather-reflection',g,.1,.07,.55);reflection.rotation.x=Math.PI/2;reflection.rotation.z=-.45;this.box(reflection,0,0,0,.035,1.3,.025,this.c.road,.24);for(let i=0;i<5;i++)for(const s of [-1,1]){const vane=this.box(reflection,s*(.15-i*.018),-.38+i*.19,0,.3-i*.03,.11,.025,this.c.road,.24);vane.rotation.z=s*.38;}this.motion(reflection,(_t,p)=>{reflection.scaling.setAll(Math.max(.01,Math.min(1,(p-.35)*3)));});this.motion(feather,t=>{feather.rotation.z=-.45+Math.sin(t*.4)*.05;});break;
      }
      case 'get-up':{
        this.water(g,3.1,2.8);const targets=[[-.45,1.6],[.45,1.6],[-.23,1],[.23,1],[0,.7]];
        for(let i=0;i<5;i++){const orb=this.ball(g,(i-2)*.55,.65+(i%2)*.18,0,.085,GOLD);this.motion(orb,(t,p)=>{const k=Math.max(0,1-Math.abs(p-.67)*5);orb.position.x=(i-2)*.55*(1-k)+targets[i][0]*k;orb.position.y=(.65+(i%2)*.18)*(1-k)+targets[i][1]*k+Math.sin(t*.3+i)*.025;});}break;
      }
      case 'asap':{
        this.clock(g,-.7,1.45,-.25,.52,true);this.box(g,-.7,.6,-.3,.09,1.2,.09,this.c.road);this.envelope(g,.65,.35,.25,.67);
        for(let i=0;i<5;i++){const light=this.ball(g,(i-2)*.45,1.9,.15,.065,GOLD);this.motion(light,(t,p)=>{const k=Math.max(0,1-Math.abs(p-.85)*6);light.position.x=(i-2)*.45*(1-k)+Math.sin(i*TAU/5)*.45*k;light.position.y=1.9+Math.sin(t*.35+i)*.12;});}break;
      }
      case 'how-sweet':{
        this.box(g,-.8,.45,0,1.1,.9,1.1,this.c.ink);this.ball(g,-.8,1.23,0,.37,this.c.accent,1,1.05,1);this.ball(g,-.49,1.39,.18,.18,this.c.road);this.box(g,-.8,1.62,0,.06,.22,.06,this.c.ink);this.ball(g,-.65,1.68,0,.15,this.c.secondary,1,.4,.6);
        this.frame(g,.8,0,0,1.1,2.15,this.c.ink,.09);const sign=this.node('record-shop-flips-open',g,.8,1.15,0);this.box(sign,0,0,0,.9,.65,.13,this.c.accent);this.disc(sign,0,0,.085,.23,.035,this.c.ink);this.disc(sign,0,0,.12,.08,.035,this.c.road);this.box(sign,0,0,-.085,.62,.07,.025,this.c.road);this.motion(sign,(_t,p)=>{sign.rotation.y=Math.max(0,Math.min(1,(p-.6)*3))*Math.PI;});break;
      }
      case 'bubble-gum':{
        this.water(g,3.1,2.8);for(let i=0;i<5;i++){const x=(i-2)*.53;this.ball(g,x,.2,-.85,.15,RAINBOW[i],1,1,1,.75);this.ball(g,x-.035,.27,-.78,.045,this.c.road);}this.ears(g,-.02,.04,-.8,.11,this.c.road);const boat=this.boat(g,0,.13,.4,1);this.motion(boat,(t,p)=>{boat.position.x=Math.min(.9,Math.max(0,p-.5)*2);boat.position.y=.13+Math.sin(t*.7)*.035;boat.rotation.z=Math.sin(t*.5)*.035;});break;
      }
      case 'supernatural':{
        this.radio(g,0,.2,.1,1.2,true);this.flower(g,-1,1.95,-.6,.45,true);this.box(g,0,.1,.1,3,.2,1.8,this.c.ink);break;
      }
      case 'right-now':{
        for(const s of [-1,1]){this.cyl(g,s*.65,.4,.3,.36,.8,this.c.road);this.cyl(g,s*.65,.83,.3,.29,.035,this.c.ink);for(const x of [-.1,.1])this.disc(g,s*.65+x,.47,.64,.035,.02,this.c.ink);this.box(g,s*.36,.42,.3,.3,.07,.07,this.c.ink);}
        const f=this.flower(g,-.3,1.2,.3,.32,true);this.motion(f,(t,p)=>{f.position.x=-.3+Math.max(0,Math.min(.6,(p-.5)*1.7));f.rotation.z=Math.sin(t*.5)*.08;});for(let i=0;i<5;i++){const p=this.node('turning-tagged-flowerpot',g,(i-2)*.58,0,-.85);this.cyl(p,0,.15,0,.2,.3,this.c.road);this.box(p,0,.32,.2,.12,.15,.025,RAINBOW[i]);this.flower(p,0,.75,0,.23,false);this.motion(p,(_t,progress)=>{p.rotation.y=-.5+Math.max(0,Math.min(1,(progress-.55)*3))*.75;});}break;
      }
    }
    return this.finish(root);
  }

  update(elapsed:number,progress:number):void {
    for(const motion of this.motions){if(motion.node.isDisposed()){this.motions.delete(motion);continue;}if(motion.node.isEnabled())motion.run(elapsed,Math.max(0,Math.min(1,progress)));}
  }
  dispose():void {
    for(const root of [...this.roots])if(!root.isDisposed())root.dispose(false,false);this.roots.clear();this.motions.clear();
    for(const mesh of this.sources.values())mesh.dispose(false,false);this.sources.clear();for(const material of this.materials.values())material.dispose();this.materials.clear();
  }
}
