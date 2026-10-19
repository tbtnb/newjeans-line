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
 Object.assign(c,{disposed:false,assetsReady:true,prefetchTimer:null,prepared:new Map(),chunkMesh:new Map(),plc:{chunks:Array.from({length:10})},prepareChunk:(i:number)=>{calls.push(i);c.prepared.set(i,{});}});
 c.scheduleAhead(3);c.scheduleAhead(3);await new Promise(r=>setTimeout(r,10));assert.deepEqual(calls,[4]);
 c.scheduleAhead(3);await new Promise(r=>setTimeout(r,10));assert.deepEqual(calls,[4,5]);
 c.scheduleAhead(3);await new Promise(r=>setTimeout(r,10));c.scheduleAhead(3);await new Promise(r=>setTimeout(r,10));assert.deepEqual(calls,[4,5,6]);
});
