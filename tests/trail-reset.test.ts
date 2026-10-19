import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {NullEngine} from '@babylonjs/core/Engines/nullEngine';
import {Scene} from '@babylonjs/core/scene';
import {CreateBox} from '@babylonjs/core/Meshes/Builders/boxBuilder';
import {Game} from '../src/core/game';
import {World} from '../src/render/world';

test('seek to start removes old GPU trail instances and disables an empty source mesh',()=>{
  const engine=new NullEngine(),scene=new Scene(engine);
  try {
    const g=new Game(JSON.parse(readFileSync('src/levels/omg.json','utf8')));g.prepare();g.start();
    for(const t of g.taps.slice(0,4))g.tap(t);
    const w:any=Object.create(World.prototype);
    Object.assign(w,{game:g,route:g.route,road:null,dress:null,trail:CreateBox('old-trail',{},scene),trailBuf:new Float32Array(16*256),runs:[],trailCount:0,failRun:null,diamonds:[],crowns:[],fx:[],failAnim:null,head:null,skin:{reset(){}},rig:null});
    w.trail.thinInstanceSetBuffer('matrix',w.trailBuf,16,false);
    w.updateTrail(g.taps[3]+.1,true);assert.ok(w.trail.getTotalIndices()>0);assert.equal(w.trail.isEnabled(),true);
    g.prepare(0);w.seek(0);
    assert.equal(w.trailCount,0);assert.equal(w.trail.getTotalIndices(),0);assert.equal(w.trail.isEnabled(),false);
    assert.equal(w.trailBuf.some((v:number)=>v!==0),false);
    g.start();g.tap(g.taps[0]);w.updateTrail(g.taps[0]+.1);
    assert.ok(w.trail.getTotalIndices()>0);assert.equal(w.trail.isEnabled(),true);
  }finally{scene.dispose();engine.dispose();}
});

test('checkpoint and rewind start with no historical ribbon, then grow only after the new start',()=>{
 const engine=new NullEngine(),scene=new Scene(engine);
 try{for(const centerAssist of [true,false]){
  const g=new Game(JSON.parse(readFileSync('src/levels/omg.json','utf8')),{centerAssist});g.prepare(60);g.startTime=0;
  const w:any=Object.create(World.prototype);Object.assign(w,{game:g,route:g.route,road:null,dress:null,trail:CreateBox('trail',{},scene),trailBuf:new Float32Array(16),runs:[],trailCount:0,failRun:null,diamonds:[],crowns:[],fx:[],failAnim:null,head:null,skin:{reset(){}},rig:null});
  w.updateTrail(60,true);assert.ok(w.trailCount>10);
  for(const t of [53.968,106.88,0,30]){
   g.prepare(t,true,true);w.seek(t);assert.equal(w.trailCount,0);assert.equal(w.trail.getTotalIndices(),0);assert.equal(w.trail.isEnabled(),false);
   g.start();w.updateTrail(t+.01);assert.equal(w.trailCount,1);assert.ok(w.runs[0].a.subtract(w.runs[0].b).length()<.2);
  }
 }}finally{scene.dispose();engine.dispose();}
});

test('clearing attempt FX does not dispose reusable collectible meshes',()=>{
 const engine=new NullEngine(),scene=new Scene(engine);
 try{const diamond=CreateBox('diamond',{},scene),crown=CreateBox('crown',{},scene),glow=CreateBox('glow',{},scene),shard=CreateBox('shard',{},scene);
 const w:any=Object.create(World.prototype);Object.assign(w,{trail:CreateBox('trail',{},scene),trailBuf:new Float32Array(16),fx:[{kind:'collect',mesh:diamond},{kind:'crown',mesh:crown},{kind:'glow',mesh:glow}],failAnim:{pieces:[{mesh:shard}]},head:null,skin:{reset(){}},rig:null});
 w.clearAttemptVisuals();assert.equal(diamond.isDisposed(),false);assert.equal(crown.isDisposed(),false);assert.equal(glow.isDisposed(),true);assert.equal(shard.isDisposed(),true);assert.equal(w.fx.length,0);assert.equal(w.failAnim,null);
 }finally{scene.dispose();engine.dispose();}
});
