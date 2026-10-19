import { MaterialPluginBase } from '@babylonjs/core/Materials/materialPluginBase';
import type { Material } from '@babylonjs/core/Materials/material';
import type { UniformBuffer } from '@babylonjs/core/Materials/uniformBuffer';
import { Vector3 } from '@babylonjs/core/Maths/math.vector';
import { posAt, type Route } from '../../core/path';

const downward=new WeakMap<Route,Route['spans']>();
const SIGHT={cam:new Vector3(), points:Array.from({length:7},()=>new Vector3()), on:0};
/** Only the short approach/landing interval of a downward jump needs terrain cutaway. */
export function updateRoadSightline(route:Route,t:number,cam:Vector3) {
  let spans=downward.get(route);if(!spans){spans=route.spans.filter(s=>s.air&&s.y1<s.y0);downward.set(route,spans);}
  SIGHT.on=spans.some(s=>s.air && s.y1<s.y0 && s.t0<t+2.4 && s.t1>t-1.2)?1:0;
  if(!SIGHT.on)return;
  SIGHT.cam.copyFrom(cam);
  SIGHT.points.forEach((v,i)=>{const p=posAt(route,Math.min(route.duration,t+i*0.4));v.set(p.x,p.y+0.12,p.z);});
}
/** Cut only higher surfaces between the camera and upcoming road. The destination road and ground
 * stay opaque. This also covers page tops and the old upper road, excluded by the decor cutaway. */
export class RoadSightline extends MaterialPluginBase {
  constructor(m:Material){super(m,'RoadSightline',310,{});this._enable(true);}
  getClassName(){return 'RoadSightline';}
  getUniforms(){return {ubo:[{name:'sightCam',size:3,type:'vec3'},{name:'sightOn',size:1,type:'float'},...SIGHT.points.map((_,i)=>({name:`sight${i}`,size:3,type:'vec3'}))],fragment:`uniform vec3 sightCam; uniform float sightOn;\n${SIGHT.points.map((_,i)=>`uniform vec3 sight${i};`).join('\n')}`};}
  bindForSubMesh(u:UniformBuffer){u.updateVector3('sightCam',SIGHT.cam);u.updateFloat('sightOn',SIGHT.on);SIGHT.points.forEach((v,i)=>u.updateVector3(`sight${i}`,v));}
  getCustomCode(type:string){if(type!=='fragment')return null;return {CUSTOM_FRAGMENT_MAIN_BEGIN:`
    if(sightOn>0.5){float cover=0.0;
    ${SIGHT.points.map((_,i)=>`{vec3 ray=sight${i}-sightCam;float k=dot(vPositionW-sightCam,ray)/max(dot(ray,ray),0.001);
      if(k>0.0 && k<0.985 && vPositionW.y>sight${i}.y+0.35){float d=length(vPositionW-(sightCam+ray*k)); cover=max(cover,1.0-smoothstep(1.5*k,2.2*k,d));}}`).join('\n')}
    float noise=fract(sin(dot(floor(gl_FragCoord.xy),vec2(12.9898,78.233)))*43758.5453);if(noise<cover)discard;
    }`};}
}
