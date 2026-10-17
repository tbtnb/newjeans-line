import { Engine } from '@babylonjs/core/Engines/engine';
import { Scene } from '@babylonjs/core/scene';
import { FreeCamera } from '@babylonjs/core/Cameras/freeCamera';
import { Camera } from '@babylonjs/core/Cameras/camera';
import { Vector3 } from '@babylonjs/core/Maths/math.vector';
import { Color3, Color4 } from '@babylonjs/core/Maths/math.color';
import { HemisphericLight } from '@babylonjs/core/Lights/hemisphericLight';
import { DirectionalLight } from '@babylonjs/core/Lights/directionalLight';
import { TransformNode } from '@babylonjs/core/Meshes/transformNode';
import { Mesh } from '@babylonjs/core/Meshes/mesh';
import { CreateBox } from '@babylonjs/core/Meshes/Builders/boxBuilder';
import { CreateCylinder } from '@babylonjs/core/Meshes/Builders/cylinderBuilder';
import { CreatePolyhedron } from '@babylonjs/core/Meshes/Builders/polyhedronBuilder';
import { CreateTorus } from '@babylonjs/core/Meshes/Builders/torusBuilder';
import { StandardMaterial } from '@babylonjs/core/Materials/standardMaterial';
import { buildPath, positionAt, SPEED, TRACK_WIDTH } from './engine';
import { WorldModels } from './world-models';
import { getLevelArt, type LevelArt } from './level-design';
import { RoutePrism, TerrainBoxes } from './world-geometry';
import type { GameSnapshot, Level, PathPoint, Point } from './types';

const ROAD_TOP=.52,TAU=Math.PI*2;
const MENU_PATH:Point[]=[{x:-8,z:8},{x:-2.8,z:8},{x:-2.8,z:3},{x:2.8,z:3},{x:2.8,z:-2.8},{x:8,z:-2.8},{x:8,z:-8}];
const CAMERA_OFFSET=new Vector3(-18,26,23);
const clamp=(v:number,a:number,b:number)=>Math.max(a,Math.min(b,v));
const seed=(i:number)=>{const n=Math.sin(i*127.1+311.7)*43758.5453;return n-Math.floor(n);};
interface ScenerySlot {node:TransformNode;index:number;chapter:number;variant:number;}
interface Collectible {node:TransformNode;time:number;index:number;baseY:number;}
interface Particle {mesh:Mesh;velocity:Vector3;spin:Vector3;age:number;life:number;active:boolean;}

/** Native Babylon renderer. Main owns the only animation loop and audio clock. */
export class WorldRenderer {
  private engine:Engine;
  private scene:Scene;
  private camera:FreeCamera;
  private model:WorldModels|null=null;
  private level:Level|null=null;
  private art:LevelArt|null=null;
  private path:PathPoint[]=[];
  private root:TransformNode;
  private menu:TransformNode;
  private gameplay:TransformNode;
  private environment:TransformNode;
  private player:TransformNode;
  private menuPlayer:TransformNode;
  private road:RoutePrism|null=null;
  private terrain:TerrainBoxes[]=[];
  private guide:RoutePrism|null=null;
  private trail:RoutePrism|null=null;
  private marker:Mesh|null=null;
  private ground:Mesh|null=null;
  private egg:TransformNode|null=null;
  private landmarks:{node:TransformNode;time:number}[]=[];
  private scenery:ScenerySlot[]=[];
  private diamonds:Collectible[]=[];
  private crowns:Collectible[]=[];
  private menuGems:Mesh[]=[];
  private particles:Particle[]=[];
  private materials=new Map<string,StandardMaterial>();
  private cameraTarget=new Vector3();
  private desiredTarget=new Vector3();
  private trailPoints:Point[]=[];
  private windowAt=-100;
  private lastTime=-1;
  private lastElapsed=0;
  private lastStatus:GameSnapshot['status']='ready';
  private mode:'menu'|'game'='menu';
  private quality:'high'|'low'='high';
  private aspect=1;
  private height=1;
  private hasCamera=false;
  private disposed=false;
  constructor(private canvas:HTMLCanvasElement) {
    this.engine=new Engine(canvas,true,{alpha:false,stencil:false,powerPreference:'high-performance',preserveDrawingBuffer:false},false);
    this.scene=new Scene(this.engine);this.scene.useRightHandedSystem=true;
    this.scene.skipPointerMovePicking=true;this.scene.autoClear=true;
    this.camera=new FreeCamera('isometric-camera',CAMERA_OFFSET.clone(),this.scene);
    this.camera.mode=Camera.ORTHOGRAPHIC_CAMERA;this.camera.minZ=.1;this.camera.maxZ=240;
    this.camera.setTarget(Vector3.Zero());this.scene.activeCamera=this.camera;
    const ambient=new HemisphericLight('soft-sky',new Vector3(0,1,0),this.scene);ambient.intensity=.64;
    ambient.groundColor=Color3.FromHexString('#7b8b9b');
    const sun=new DirectionalLight('afternoon-sun',new Vector3(.6,-1,-.4),this.scene);sun.intensity=.40;
    this.root=new TransformNode('level-root',this.scene);
    this.menu=new TransformNode('menu-diorama',this.scene);this.menu.parent=this.root;
    this.gameplay=new TransformNode('song-world',this.scene);this.gameplay.parent=this.root;
    this.environment=new TransformNode('chapter-scenery',this.scene);this.environment.parent=this.gameplay;
    this.player=new TransformNode('player',this.scene);this.player.parent=this.gameplay;
    this.menuPlayer=new TransformNode('menu-player',this.scene);this.menuPlayer.parent=this.menu;
    this.resize();
  }
  private material(color:string,unlit=false):StandardMaterial {
    const key=color+(unlit?'u':'');let m=this.materials.get(key);
    if(!m){m=new StandardMaterial(`scene-${key}`,this.scene);m.diffuseColor=Color3.FromHexString(color);
      m.specularColor=Color3.Black();m.backFaceCulling=false;
      if(unlit){m.disableLighting=true;m.emissiveColor=m.diffuseColor.clone();}
      else m.emissiveColor=m.diffuseColor.scale(.07);
      this.materials.set(key,m);}
    return m;
  }
  private box(name:string,parent:TransformNode,x:number,y:number,z:number,w:number,h:number,d:number,color:string):Mesh {
    const m=CreateBox(name,{width:w,height:h,depth:d},this.scene);m.parent=parent;m.position.set(x,y,z);
    m.material=this.material(color);m.isPickable=false;return m;
  }
  private platform(parent:TransformNode,x:number,z:number,w:number,d:number,depth=1.8):void {
    this.box('floating-terrain',parent,x,ROAD_TOP-.28-depth/2,z,w,depth,d,this.art!.colors.ground);
    this.box('terrain-edge',parent,x,ROAD_TOP-.29-depth,z,w*.92,.2,d*.92,this.art!.colors.roadSide);
  }
  private makePlayer(parent:TransformNode):void {
    this.box('line-head',parent,0,0,0,.56,.56,.56,this.art!.colors.line);
    this.box('head-glint',parent,-.1,.285,.08,.1,.012,.1,'#fffdf4');
  }
  load(level:Level):void {
    if(this.disposed)return;this.clearLevel();this.level=level;this.art=getLevelArt(level.id);this.path=buildPath(level);
    this.model=new WorldModels(this.scene,this.art);
    const c=this.art.colors,bg=Color3.FromHexString(c.background);
    this.scene.clearColor=new Color4(bg.r,bg.g,bg.b,1);
    this.scene.fogMode=Scene.FOGMODE_LINEAR;this.scene.fogStart=76;this.scene.fogEnd=160;this.scene.fogColor=bg;
    this.ground=this.box('distant-color-field',this.root,0,-4.8,0,400,.15,400,c.background);
    this.ground.material=this.material(c.background,true);
    this.buildMenu();this.makePlayer(this.player);
    const roadMat=this.material('#ffffff');
    this.road=new RoutePrism(this.scene,'continuous-road',256,roadMat,c.road,c.roadSide);this.road.mesh.parent=this.gameplay;
    this.guide=new RoutePrism(this.scene,'route-center-guide',256,roadMat,Color3.Lerp(Color3.FromHexString(c.line),Color3.FromHexString(c.road),.63).toHexString(),c.road);this.guide.mesh.parent=this.gameplay;
    this.trail=new RoutePrism(this.scene,'raised-player-line',256,roadMat,c.line,c.line);this.trail.mesh.parent=this.gameplay;
    this.marker=CreateTorus('next-corner-halo',{diameter:.98,thickness:.055,tessellation:24},this.scene);
    this.marker.material=this.material(c.line);this.marker.parent=this.gameplay;this.marker.isPickable=false;
    this.terrain=[c.ground,c.roadSide,this.art.family==='bloom'&&this.art.dark?'#18334B':c.secondary].map((color,i)=>{const field=new TerrainBoxes(this.scene,`album-district-${i}`,this.material(color));field.mesh.parent=this.gameplay;return field;});
    this.buildScenery();this.buildCollectibles();this.buildParticles();this.updateRoad(0);
    this.lastTime=-1;this.lastElapsed=0;this.lastStatus='ready';this.hasCamera=false;this.resize();
  }
  private buildMenu():void {
    const c=this.art!.colors;
    this.platform(this.menu,0,0,23,23,2.5);
    const road=new RoutePrism(this.scene,'menu-road',MENU_PATH.length,this.material('#ffffff'),c.road,c.roadSide);
    road.mesh.parent=this.menu;road.update(MENU_PATH,TRACK_WIDTH,ROAD_TOP,.8);
    const line=new RoutePrism(this.scene,'menu-line',5,this.material('#ffffff'),c.line,c.line);
    line.mesh.parent=this.menu;line.update([...MENU_PATH.slice(0,4),{x:2.8,z:1.2}],.3,ROAD_TOP+.055,.055);
    this.makePlayer(this.menuPlayer);this.menuPlayer.position.set(2.8,ROAD_TOP+.28,1.2);
    const landmark=this.model!.createLandmark(2);landmark.parent=this.menu;landmark.position.set(-6,0,-4.4);landmark.scaling.setAll(.86);
    const poses=[[-8.5,2.7,.6,0],[7,6.9,.72,1],[1,-8.1,.63,2],[8.8,1.4,.5,3],[-.3,10.7,.45,1]];
    poses.forEach(([x,z,s,v],i)=>{const n=this.model!.createScenery(v,i%4,10+i);n.parent=this.menu;n.position.set(x,0,z);n.scaling.setAll(s);});
    const egg=this.model!.createEasterEgg();egg.name='menu-exclusive-easter-egg';egg.parent=this.menu;egg.position.set(-8.5,0,-8.6);egg.scaling.setAll(.75);
    const gate=this.createCrownGate(this.menu);gate.position.set(8,ROAD_TOP,-7.2);
    for(const [i,p] of [{x:-2.8,z:5.4},{x:1.1,z:3},{x:5.7,z:-2.8}].entries()) {
      const m=this.createGem(this.menu,i===1?c.secondary:c.accent);m.position.set(p.x,1.32,p.z);this.menuGems.push(m);
    }
    // A detached album-colored plinth gives the compact composition a floating edge.
    this.platform(this.menu,13.6,4.8,3.1,3.1,1.1);
    const detail=this.model!.createScenery(3,3,31);detail.parent=this.menu;detail.position.set(13.6,0,4.8);detail.scaling.setAll(.4);
  }
  private distanceToPath(p:Point,path:readonly Point[]=this.path):number {
    let distance=Infinity;
    for(let i=1;i<path.length;i++) {
      const a=path[i-1],b=path[i],dx=b.x-a.x,dz=b.z-a.z,l=dx*dx+dz*dz;
      const t=l?clamp(((p.x-a.x)*dx+(p.z-a.z)*dz)/l,0,1):0;
      distance=Math.min(distance,Math.hypot(p.x-a.x-t*dx,p.z-a.z-t*dz));
    }
    return distance;
  }
  private placement(time:number,extent:number,side:number):Point {
    const p=positionAt(this.level!,time),next=positionAt(this.level!,Math.min(this.level!.duration,time+.04));
    let dx=next.x-p.x,dz=next.z-p.z;const len=Math.hypot(dx,dz)||1;dx/=len;dz/=len;
    // Curated alternating tableaux stay a full road width beyond their footprint.
    for(let step=0;step<12;step++) {
      const radius=extent*Math.SQRT2;
      const distance=radius+TRACK_WIDTH*1.5+step*1.3;
      const candidate={x:p.x-dz*distance*side,z:p.z+dx*distance*side};
      if(this.distanceToPath(candidate)>radius+TRACK_WIDTH*1.5-.001)return candidate;
    }
    return {x:p.x-extent-TRACK_WIDTH*3,z:p.z+extent+TRACK_WIDTH*3};
  }
  private buildScenery():void {
    const level=this.level!;
    for(let i=0;i<14;i++) {
      const node=this.model!.createScenery(i%4,0,i);node.parent=this.environment;
      this.scenery.push({node,index:-999,chapter:0,variant:i%4});
    }
    level.sections.forEach((section,i)=>{
      const time=clamp(section.at+Math.min(3,level.duration*.02),.2,level.duration-.1);
      const p=this.placement(time,4,i%2===0?1:-1),node=this.model!.createLandmark(i);
      node.name=`chapter-${i+1}-${section.label}`;node.parent=this.environment;node.position.set(p.x,0,p.z);
      this.platform(node,0,0,8.8,8.8,2.2);this.landmarks.push({node,time});
    });
    const eggAt=this.art!.egg.at;
    const time=eggAt<=1?level.duration*eggAt:Math.min(eggAt,level.duration);
    const egg=this.model!.createEasterEgg(),p=this.placement(time,2,-1);
    egg.name=`exclusive-easter-egg-${level.id}-${this.art!.egg.type}`;egg.parent=this.environment;egg.position.set(p.x,0,p.z);
    this.platform(egg,0,0,4.8,4.8,1.6);this.egg=egg;egg.metadata={at:time,name:this.art!.egg.name};
  }
  private chapterAt(time:number):number {
    return Math.max(0,this.level!.sections.filter(s=>s.at<=time).length-1);
  }
  private updateScenery(time:number):void {
    const interval=3.8,center=Math.floor(time/interval);
    for(let i=0;i<this.scenery.length;i++) {
      const slot=this.scenery[i],first=center-3;
      const index=first+((i-first)%this.scenery.length+this.scenery.length)%this.scenery.length,at=(index+.5)*interval;
      slot.node.setEnabled(at>=0&&at<=this.level!.duration&&(this.quality==='high'||i%2===0));
      if(index===slot.index)continue;slot.index=index;
      if(at<0||at>this.level!.duration){slot.node.setEnabled(false);continue;}
      const chapter=this.chapterAt(at),variant=i%4;
      if(chapter!==slot.chapter||variant!==slot.variant) {
        slot.node.dispose(false,false);slot.node=this.model!.createScenery(variant,chapter,index);slot.node.parent=this.environment;
        slot.chapter=chapter;slot.variant=variant;
      }
      const p=this.placement(at,3,index%2===0?1:-1);slot.node.position.set(p.x,0,p.z);slot.node.rotation.y=(index%3-1)*.08;
      slot.node.setEnabled(this.quality==='high'||i%2===0);
    }
    this.landmarks.forEach(({node,time:at})=>node.setEnabled(Math.abs(at-time)<25));
    if(this.egg)this.egg.setEnabled(Math.abs((this.egg.metadata?.at??0)-time)<20);
  }
  private createGem(parent:TransformNode,color:string):Mesh {
    const gem=CreatePolyhedron('faceted-diamond',{type:1,size:.38},this.scene);gem.parent=parent;
    gem.scaling.set(.66,1.12,.66);gem.material=this.material(color);gem.isPickable=false;return gem;
  }
  private createCrownGate(parent:TransformNode):TransformNode {
    const gate=new TransformNode('crown-gate',this.scene);gate.parent=parent;
    const gold='#E7B95F',light='#FFF1B9';
    for(const x of [-1.07,1.07]) {
      this.box('gate-column',gate,x,1,0,.15,2,.16,gold);
      this.box('gate-foot',gate,x,.08,0,.34,.16,.4,light);
    }
    this.box('gate-crossbar',gate,0,2,0,2.3,.13,.17,gold);
    this.box('crown-band',gate,0,2.29,0,.9,.2,.19,gold);
    for(const [i,x] of [-.35,0,.35].entries()) {
      const spike=CreateCylinder('crown-point',{height:i===1?.5:.34,diameterBottom:.32,diameterTop:0,tessellation:4},this.scene);
      spike.parent=gate;spike.position.set(x,2.48+(i===1?.06:0),0);spike.material=this.material(light);spike.isPickable=false;
    }
    return gate;
  }
  private buildCollectibles():void {
    const level=this.level!;
    for(let i=0;i<10;i++) {
      const time=level.duration*(i+1)/10,p=positionAt(level,time);
      const node=this.createGem(this.gameplay,this.art!.colors.accent);node.position.set(p.x,1.32,p.z);
      this.diamonds.push({node,time,index:i,baseY:1.32});
    }
    [0.3,0.6,1].forEach((progress,index)=>{
      const time=level.duration*progress,p=positionAt(level,time),before=positionAt(level,time-.03),node=this.createCrownGate(this.gameplay);
      node.position.set(p.x,ROAD_TOP,p.z);node.rotation.y=Math.abs(p.x-before.x)>.01?Math.PI/2:0;
      this.crowns.push({node,time,index,baseY:ROAD_TOP});
    });
  }
  private updateRoad(time:number):void {
    const level=this.level!,start=Math.max(0,time-8),end=Math.min(level.duration,time+18);
    const points=[positionAt(level,start),...this.path.filter(p=>p.time>start+.0001&&p.time<end-.0001),positionAt(level,end)];
    if(start===0)points.unshift({x:-TRACK_WIDTH*.7,z:0});
    if(end===level.duration){const last=points[points.length-1];points.push({x:last.x+(level.turns.length%2===0?TRACK_WIDTH*.7:0),z:last.z-(level.turns.length%2===1?TRACK_WIDTH*.7:0)});}
    this.road!.update(points,TRACK_WIDTH,ROAD_TOP,.86);this.guide!.update(points,.055,ROAD_TOP+.009,.009);
    this.updateScenery(time);this.updateTerrain(points,time);this.windowAt=time;
  }
  private updateTerrain(points:Point[],time:number):void {
    if(this.terrain.length!==3)return;
    const [land,edge,detail]=this.terrain,family=this.art!.family;
    for(const field of this.terrain)field.begin();
    const strip=(field:TerrainBoxes,a:Point,b:Point,width:number,top:number,height:number)=>{
      const dx=Math.abs(b.x-a.x),dz=Math.abs(b.z-a.z);
      field.box((a.x+b.x)/2,top,(a.z+b.z)/2,dx>dz?dx+width:width,height,dz>=dx?dz+width:width);
    };
    for(let i=1;i<points.length;i++) {
      const a=points[i-1],b=points[i];
      if(family==='denim') {
        // The playable roof sits on a continuous blue architectural spine.
        strip(edge,a,b,TRACK_WIDTH+.08,ROAD_TOP-.84,5.8);
      } else if(family==='memory') {
        strip(land,a,b,13.5,-.32,2.7);
        if(i%2===0)strip(edge,a,b,5,-.31,.12);
      } else if(family==='pixel') {
        // Individual voxel piers replace the continuous stone foundation.
        if(i%2===0)edge.box(a.x,-.33,a.z,2.1,4.4,2.1);
        if(i%3===0)land.box(a.x-3,-2.2,a.z+3,7.5,1.2,5.5);
      } else if(family==='mixtape') {
        strip(land,a,b,10.5,-.32,2.7);
        strip(edge,a,b,3,-.33,3.3);
      } else {
        strip(edge,a,b,6.4,-1.05,2.8);
        strip(land,a,b,TRACK_WIDTH+.15,-.33,3.6);
      }
    }
    for(const slot of this.scenery) {
      const at=(slot.index+.5)*3.8;if(!slot.node.isEnabled()||Math.abs(at-time)>17)continue;
      const p=slot.node.position,index=slot.index;
      if(family==='denim') {
        land.box(p.x,.11,p.z,7.8,4.2+(index%3)*.5,7.6);
        detail.box(p.x+(index%2?2:-2),-.65,p.z+2.6,5.8,5.4,4.6);
        // Low white roof lips read as terraces, never as a competing path.
        detail.box(p.x-3.7,.23,p.z, .1,.12,7.6);
      } else if(family==='memory') {
        land.box(p.x,.11,p.z,9.2,3.1,8.5);
        detail.box(p.x,-.29,p.z+4.6,9.2,2.3,2.1);
      } else if(family==='pixel') {
        land.box(p.x,.11,p.z,6.8,3.2,6.2);
        detail.box(p.x+2,-1.1,p.z-2,3.8,4,3.8);
        detail.box(p.x-3.2,-2.3,p.z+1.8,4.5,.8,3.3);
      } else if(family==='mixtape') {
        land.box(p.x,.11,p.z,8.8,3.2,8.2);
        detail.box(p.x-2,-.4,p.z+3.7,8.3,2.7,5);
      } else {
        land.box(p.x,.11,p.z,7.6,3.4,7.3);
        detail.box(p.x,-.8,p.z+4.3,7.6,1.4,1.5);
      }
    }
    // Water is a single local field, with the route/coast banks raised above it.
    if(family==='mixtape'||family==='bloom') {
      const p=positionAt(this.level!,time);detail.box(p.x,-2.8,p.z,180,.2,180);
    }
    for(const field of this.terrain)field.finish();
  }
  private updateTrail(snapshot:GameSnapshot):void {
    this.trailPoints.length=0;
    const points=snapshot.trail;
    // Engine includes authored corners, including taps between two rendered frames.
    for(const p of points) {
      const last=this.trailPoints[this.trailPoints.length-1];
      if(!last||Math.hypot(last.x-p.x,last.z-p.z)>.002)this.trailPoints.push(p);
    }
    const last=this.trailPoints[this.trailPoints.length-1];
    if(!last||Math.hypot(last.x-snapshot.position.x,last.z-snapshot.position.z)>.001)this.trailPoints.push(snapshot.position);
    this.trail!.update(this.trailPoints,.30,ROAD_TOP+.055,.055);
  }
  private buildParticles():void {
    const colors=[this.art!.colors.accent,this.art!.colors.secondary,'#F5D98E','#FFF8E5'];
    for(let i=0;i<48;i++) {
      const mesh=this.box('confetti',this.gameplay,0,0,0,.1,.2,.055,colors[i%4]);mesh.setEnabled(false);
      this.particles.push({mesh,velocity:new Vector3(),spin:new Vector3(),age:0,life:1,active:false});
    }
  }
  private burst(p:Point,complete:boolean):void {
    this.particles.forEach((particle,i)=>{
      const angle=seed(i+5)*TAU,radius=complete?3:1.4;
      particle.mesh.position.set(p.x+(complete?(i%2===0?-1.4:1.4):0),ROAD_TOP+(complete?2.5:.4),p.z);
      particle.velocity.set(Math.cos(angle)*radius,(complete?4:2)+seed(i+41)*3,Math.sin(angle)*radius);
      particle.spin.set(seed(i+3)*7,seed(i+9)*7,seed(i+13)*7);
      particle.age=-i*(complete?.012:.001);particle.life=complete?3:1.2;particle.active=i<(complete?48:20);particle.mesh.setEnabled(particle.active);
    });
  }
  private updateEffects(dt:number):void {
    for(const p of this.particles)if(p.active) {
      p.age+=dt;if(p.age<0)continue;
      if(p.age>p.life){p.active=false;p.mesh.setEnabled(false);continue;}
      p.velocity.y-=dt*5.6;p.mesh.position.x+=p.velocity.x*dt;p.mesh.position.y+=p.velocity.y*dt;p.mesh.position.z+=p.velocity.z*dt;
      p.mesh.rotation.x+=p.spin.x*dt;p.mesh.rotation.y+=p.spin.y*dt;p.mesh.rotation.z+=p.spin.z*dt;
    }
  }
  render(snapshot:GameSnapshot,options:{mode:'menu'|'game';elapsed:number;quality?:'high'|'low';guide?:boolean}):void {
    if(this.disposed||!this.level||!this.model)return;
    const elapsed=options.elapsed,dt=clamp(elapsed-this.lastElapsed,0,.06),changed=options.mode!==this.mode;
    const visualTime=options.mode==='menu'?elapsed:snapshot.time;
    if(options.quality&&options.quality!==this.quality){this.quality=options.quality;this.resize();this.windowAt=-100;}
    this.mode=options.mode;this.menu.setEnabled(this.mode==='menu');this.gameplay.setEnabled(this.mode==='game');
    if(changed){this.hasCamera=false;this.resize();}
    if(this.mode==='menu') {
      this.desiredTarget.set(0,.3,0);this.menuPlayer.position.y=ROAD_TOP+.28+Math.sin(elapsed*1.8)*.025;
      this.menuGems.forEach((m,i)=>{m.rotation.y=elapsed*.5+i;m.position.y=1.32+Math.sin(elapsed*1.4+i)*.08;});
    } else {
      if(Math.abs(snapshot.time-this.windowAt)>1.6||snapshot.time<this.lastTime-.1)this.updateRoad(snapshot.time);
      this.guide!.mesh.setEnabled(options.guide!==false);this.player.position.set(snapshot.position.x,ROAD_TOP+.28,snapshot.position.z);
      this.player.setEnabled(snapshot.status!=='failed');
      if(snapshot.time!==this.lastTime||changed)this.updateTrail(snapshot);
      if(this.marker) {
        this.marker.setEnabled(options.guide!==false&&snapshot.nextTurn!==null&&snapshot.status==='playing');
        if(snapshot.nextTurn!==null){const p=positionAt(this.level,snapshot.nextTurn);this.marker.position.set(p.x,ROAD_TOP+.04,p.z);this.marker.scaling.setAll(1+Math.sin(visualTime*4)*.045);}
      }
      for(const gem of this.diamonds) {
        gem.node.setEnabled(gem.index>=snapshot.diamonds&&Math.abs(gem.time-snapshot.time)<15);
        gem.node.rotation.y=visualTime*.9+gem.index;gem.node.position.y=gem.baseY+Math.sin(visualTime*2+gem.index)*.065;
      }
      for(const crown of this.crowns)crown.node.setEnabled(Math.abs(crown.time-snapshot.time)<17);
      if(snapshot.status!==this.lastStatus) {
        if(snapshot.status==='failed')this.burst(snapshot.position,false);
        if(snapshot.status==='complete')this.burst(snapshot.position,true);
        if(snapshot.status==='ready')this.particles.forEach(p=>{p.active=false;p.mesh.setEnabled(false);});
      }
      const ahead=positionAt(this.level,Math.min(this.level.duration,snapshot.time+Math.min(1.5,9/SPEED)));
      this.desiredTarget.set(snapshot.position.x+(ahead.x-snapshot.position.x)*.45,.35,snapshot.position.z+(ahead.z-snapshot.position.z)*.45);
      this.updateEffects(snapshot.status==='paused'?0:dt);
    }
    if(!this.hasCamera){this.cameraTarget.copyFrom(this.desiredTarget);this.hasCamera=true;}
    else Vector3.LerpToRef(this.cameraTarget,this.desiredTarget,1-Math.exp(-(snapshot.status==='paused'&&this.mode==='game'?0:dt)*5.5),this.cameraTarget);
    this.camera.position.copyFrom(this.cameraTarget).addInPlace(CAMERA_OFFSET);this.camera.setTarget(this.cameraTarget);
    if(this.ground){this.ground.position.x=this.cameraTarget.x;this.ground.position.z=this.cameraTarget.z;}
    this.model.update(this.mode==='game'?snapshot.time:elapsed,snapshot.progress);
    this.scene.render();this.lastTime=snapshot.time;this.lastElapsed=elapsed;this.lastStatus=snapshot.status;
  }
  resize():void {
    if(this.disposed)return;
    const rect=this.canvas.getBoundingClientRect(),width=Math.max(1,Math.round(rect.width||window.innerWidth));
    this.height=Math.max(1,Math.round(rect.height||window.innerHeight));this.aspect=width/this.height;
    const dpr=Math.min(window.devicePixelRatio||1,this.quality==='high'?1.5:1);
    this.engine.setHardwareScalingLevel(1/dpr);this.engine.setSize(Math.round(width*dpr),Math.round(this.height*dpr),false);
    const portrait=this.aspect<.85,compact=portrait&&this.height<730;
    const visibleHeight=this.mode==='menu'?Math.max(portrait?40:57,(compact?40:35)/this.aspect):Math.max(24,19/this.aspect);
    const shift=visibleHeight*(this.mode==='menu'?-.09:.12);
    this.camera.orthoLeft=-visibleHeight*this.aspect/2;this.camera.orthoRight=visibleHeight*this.aspect/2;
    this.camera.orthoTop=visibleHeight/2+shift;this.camera.orthoBottom=-visibleHeight/2+shift;
  }
  private clearLevel():void {
    // The persistent roots and lights survive song selection; all song meshes are owned here or by the factory.
    for(const node of [this.menu,this.environment,this.player,this.menuPlayer])for(const child of node.getChildren())if(child!==this.menuPlayer)child.dispose(false,false);
    for(const child of this.gameplay.getChildren())if(child!==this.environment&&child!==this.player)child.dispose(false,false);
    this.ground?.dispose();this.ground=null;this.model?.dispose();this.model=null;
    for(const m of this.materials.values())m.dispose();this.materials.clear();
    this.terrain=[];this.road=this.guide=this.trail=null;this.marker=null;this.egg=null;this.scenery=[];this.landmarks=[];
    this.diamonds=[];this.crowns=[];this.menuGems=[];this.particles=[];
  }
  dispose():void {
    if(this.disposed)return;this.clearLevel();this.scene.dispose();this.engine.dispose();this.disposed=true;
  }
}
