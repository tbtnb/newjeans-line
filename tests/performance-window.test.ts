import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';
import {NullEngine} from '@babylonjs/core/Engines/nullEngine';import {Scene,Mesh} from '../src/render/bjs';
import {World} from '../src/render/world';import {Game} from '../src/core/game';import {readableRoadWidths} from '../src/core/roadwidth';import {denseWindows,inDenseWindow} from '../src/core/edgeassist';
const level=JSON.parse(readFileSync('src/levels/omg.json','utf8'));
test('late-song trail geometry stays within the rear camera window rather than growing for the whole song',()=>{
 const g=new Game(level);g.prepare(150);const e=new NullEngine(),s=new Scene(e),m=new Mesh('trail',s),w:any=Object.create(World.prototype);
 Object.assign(w,{game:g,route:g.route,cmode:true,runs:[],trailCount:0,failRun:null,trail:m});
 try{w.updateTrail(150,true);assert.ok(w.trailCount<50,`visible trail runs: ${w.trailCount}`);assert.ok(w.runs[0].a.z>g.route.spans[0].z0);assert.ok(m.getTotalVertices()<900);w.updateTrail(150.01);assert.ok(m.getTotalVertices()<900);}finally{s.dispose();e.dispose();}
});
test('only dense runs gain width, and parallel lanes retain a visible gap',()=>{
 const g=new Game(level),route=g.route,base=readableRoadWidths({...route,freeTurns:false,denseAssist:false},()=>2.6),next=readableRoadWidths(route,()=>2.6),wins=denseWindows(g.taps);
 let widened=0;
 for(let i=0;i<next.length;i++){
  if(!inDenseWindow(wins,(route.spans[i].t0+route.spans[i].t1)/2))assert.equal(next[i],base[i]);
  assert.ok(next[i]>=base[i]-1e-8);if(next[i]>base[i]+.01)widened++;
 }
 assert.ok(widened>20,`widened ${widened}`);
});
