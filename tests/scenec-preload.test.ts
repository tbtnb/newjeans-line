import test from 'node:test';import assert from 'node:assert/strict';
import {SceneC} from '../src/render/scenec/scenec';
const mesh=()=>({on:true,setEnabled(on:boolean){this.on=on;}});
test('future chunks are prepared hidden and never duplicated',()=>{
 const c:any=Object.create(SceneC.prototype);let built=0;
 Object.assign(c,{disposed:false,prepared:new Map(),chunkMesh:new Map(),plc:{chunks:[{i:0},{i:1}]},buildChunk:()=>{built++;return{g:mesh(),m:mesh()};}});
 c.prepareChunk(1);c.prepareChunk(1);assert.equal(built,1);assert.equal(c.prepared.get(1).g.on,false);assert.equal(c.prepared.get(1).m.on,false);
 c.chunkMesh.set(0,{});c.prepareChunk(0);assert.equal(built,1);
});
test('prefetch schedules only one chunk per task within three ahead',async()=>{
 const c:any=Object.create(SceneC.prototype),calls:number[]=[];
 Object.assign(c,{disposed:false,assetsReady:true,prefetchTimer:null,prepared:new Map(),chunkMesh:new Map(),sets:[],skyT:0,range:[0,3],plc:{chunks:Array.from({length:10})},prepareChunk:(i:number)=>{calls.push(i);c.prepared.set(i,{});}});
 c.scheduleAhead(3);c.scheduleAhead(3);await new Promise(r=>setTimeout(r,10));assert.deepEqual(calls,[4]);
 c.scheduleAhead(3);await new Promise(r=>setTimeout(r,10));assert.deepEqual(calls,[4,5]);
 c.scheduleAhead(3);await new Promise(r=>setTimeout(r,10));c.scheduleAhead(3);await new Promise(r=>setTimeout(r,10));assert.deepEqual(calls,[4,5,6]);
});
test('reclaim only old chunks and passed landmarks, preserving the future preload window',()=>{
 const c:any=Object.create(SceneC.prototype);let released=0;
 const data={G:{pos:new Float32Array(3),col:new Float32Array(4),idx:new Uint32Array(3)},M:{pos:new Float32Array(),col:new Float32Array(),idx:new Uint32Array()}};
 const past={def:{t:10},on:false,far:{dispose(a:boolean,b:boolean){assert.equal(a,false);assert.equal(b,false);released++;}},near:null,nearMeshes:[],piv:[],node:{setEnabled(){}}};
 const future={...past,def:{t:80},far:{dispose(){throw Error('future preload must survive');}}};
 Object.assign(c,{baked:new Map([[1,data],[4,data],[8,data],[12,data]]),bakedBytes:160,sets:[past,future]});
 c.retireBehind(6,40,null);assert.deepEqual([...c.baked.keys()],[4,8,12]);assert.equal(c.bakedBytes,120);assert.equal(released,1);assert.equal(past.far,null);assert.ok(future.far);
});
test('a rewind invalidates queued ahead work from the previous window',async()=>{
 const c:any=Object.create(SceneC.prototype),calls:number[]=[];
 Object.assign(c,{disposed:false,assetsReady:true,prefetchTimer:null,prepared:new Map(),chunkMesh:new Map(),sets:[],skyT:30,range:[4,8],plc:{chunks:Array.from({length:20})},prepareChunk:(i:number)=>calls.push(i)});
 c.scheduleAhead(8);c.range=[0,3];c.skyT=0;await new Promise(r=>setTimeout(r,10));assert.deepEqual(calls,[]);
});
test('a recycled landmark is restored before being shown after a checkpoint rewind',()=>{
 const c:any=Object.create(SceneC.prototype);let built=0;
 const e:any={def:{t:20,popAt:15},on:false,far:null,near:null,node:{setEnabled(){}},hinge:{rotation:{}},lodFar:true};
 Object.assign(c,{tier:'high',time:16,buildSetVisual:(x:any)=>{built++;x.far={setEnabled(){}};x.lodFar=true;}});
 c.animSet(e,16,0,null);assert.equal(built,1);assert.equal(e.on,true);
});
test('landmark still intersecting the camera is not destroyed',()=>{
 const c:any=Object.create(SceneC.prototype);const e:any={def:{t:10},on:false,far:{computeWorldMatrix(){},isInFrustum(){return true;}},nearMeshes:[]};
 Object.assign(c,{baked:new Map(),bakedBytes:0,sets:[e],scene:{frustumPlanes:[]},dropSetVisual(){throw Error('visible landmark must survive');}});
 c.retireBehind(10,40,{});assert.ok(e.far);
});
