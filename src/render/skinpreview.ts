/** The picker renders the same meshes/materials/decor as gameplay, never a PNG head billboard. */
import {Engine,Scene,FreeCamera,HemisphericLight,DirectionalLight,Vector3,Color4,CreateBox,StandardMaterial,TransformNode,DynamicTexture,Mesh} from './bjs';
import {LineSkin} from './lineskin';
import {updateTrailMesh,type TrailRun} from './trailmesh';
import type {SkinDef} from '../skins';
export class SkinPreview {
  private engine:Engine|null=null; private scene:Scene|null=null; private skin:LineSkin|null=null;
  private head:any; private ribbon!:Mesh; private cam:any; private running=false; private startAt=0; private lastSegment=-1;
  private selected:SkinDef|null=null; private color='#ffffff'; private size='';
  private lens=[3,2,4,1.5,2.5,3.5,2,1.5];
  constructor(private canvas:HTMLCanvasElement) {}
  set(skin:SkinDef,color:string){this.selected=skin;this.color=color;this.skin?.apply(skin.id);this.skin?.reset();this.lastSegment=-1;}
  private setup(){
    if(this.engine)return;
    const engine=new Engine(this.canvas,true,{alpha:true,stencil:false,powerPreference:'low-power'},false);this.engine=engine;
    engine.setHardwareScalingLevel(1/Math.min(1.5,window.devicePixelRatio||1));
    const scene=new Scene(engine);this.scene=scene;scene.clearColor=new Color4(0,0,0,0);scene.skipPointerMovePicking=true;
    const hemi=new HemisphericLight('preview-light',new Vector3(.2,1,-.3),scene);hemi.intensity=.85;
    const sun=new DirectionalLight('preview-sun',new Vector3(-.55,-1,.35),scene);sun.intensity=.5;
    this.cam=new FreeCamera('preview-camera',new Vector3(9,9,-9),scene);this.cam.inputs.clear();this.cam.fov=.6;
    const root=new TransformNode('preview-line',scene),hm=new StandardMaterial('preview-head',scene),tm=new StandardMaterial('preview-trail',scene);
    this.head=CreateBox('preview-head',{size:1},scene);this.head.scaling.set(1,.9,1);this.head.parent=root;this.head.material=hm;
    this.ribbon=new Mesh('preview-ribbon',scene);this.ribbon.material=tm;this.ribbon.parent=root;this.ribbon.setEnabled(false);
    const spark=new DynamicTexture('preview-spark',{width:32,height:32},scene,false),ctx=spark.getContext();
    const g=ctx.createRadialGradient(16,16,0,16,16,16);g.addColorStop(0,'white');g.addColorStop(1,'rgba(255,255,255,0)');ctx.fillStyle=g;ctx.fillRect(0,0,32,32);spark.hasAlpha=true;spark.update();
    this.skin=new LineSkin(scene,spark);this.skin.attach(this.head,hm,tm,root);if(this.selected)this.skin.apply(this.selected.id);
  }
  private at(d:number){let x=0,z=0,i=0,rem=d;for(;;i++){const n=this.lens[i%this.lens.length];if(rem<=n)break;rem-=n;if(i%2===0)x+=n;else z+=n;}if(i%2===0)x+=rem;else z+=rem;return{x,z,i};}
  start(){if(this.running)return;try{this.setup();}catch{this.canvas.setAttribute('aria-label','此浏览器无法显示立体皮肤预览');return;}this.running=true;this.startAt=performance.now();this.lastSegment=-1;this.engine!.runRenderLoop(()=>this.draw());}
  stop(){this.running=false;this.engine?.stopRenderLoop();this.skin?.reset();}
  private draw(){
    if(!this.running||!this.skin||!this.scene)return;
    const size=`${this.canvas.clientWidth}:${this.canvas.clientHeight}`;if(size!==this.size){this.size=size;this.engine!.resize();}
    const t=(performance.now()-this.startAt)/1000,D=t*2.6,head=this.at(D);this.head.position.set(head.x,.45,head.z);
    let d=Math.max(0,D-16),p=this.at(d),n=0;const runs:TrailRun[]=[];
    while(d<D-1e-6&&n<24){let end=0;for(let i=0;i<=p.i;i++)end+=this.lens[i%this.lens.length];end=Math.min(end,D);const q=this.at(end-1e-8);const h=p.i%2===0?1:0,dx=h?1:0,dz=h?0:1;
      runs.push({a:new Vector3(p.x,.45,p.z),b:new Vector3(q.x,.45,q.z)});n++;
      if(end>=D)break;d=end+1e-8;p=this.at(d);
    }
    updateTrailMesh(this.ribbon,runs);
    this.head.visibility=n?0:1;
    if(head.i!==this.lastSegment){if(this.lastSegment>=0)this.skin.onTurn(this.head.position,t);this.lastSegment=head.i;}
    this.skin.update(t,this.color,head.i%2===0?1:0,true);
    this.cam.position.set(head.x+9,10,head.z-9);this.cam.setTarget(new Vector3(head.x-1,.3,head.z-1));this.scene.render();
  }
}
