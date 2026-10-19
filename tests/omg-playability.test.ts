import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {Game} from '../src/core/game';
import {linePos,lineHeading} from '../src/core/linepath';
import {posAt,headingAt} from '../src/core/path';
import {denseWindows,inDenseWindow} from '../src/core/edgeassist';
import {readableRoadWidths} from '../src/core/roadwidth';
import type {LevelData} from '../src/core/types';
import {AudioTransport} from '../src/audio';
const L=JSON.parse(readFileSync('src/levels/omg.json','utf8')) as LevelData;

test('OMG perfect route remains playable with all 361 inputs',()=>{
  const g=new Game(L,{centerAssist:false});g.prepare();g.start();
  for(const T of g.taps) { assert.equal(g.tap(T),'hit'); }
  g.update(L.duration);assert.equal(g.status,'complete');assert.equal(g.cursor,361);
});
test('early and late taps turn immediately at the current position without a centreline snap',()=>{
  for(const offset of [-.1,.1]) {
    const g=new Game(L,{centerAssist:false});g.prepare();g.start();const t=g.taps[0]+offset;
    const before=linePos(g.route,g.turns,t,g.cursor);
    assert.equal(g.tap(t),'hit');
    const after=linePos(g.route,g.turns,t,g.cursor);
    assert.ok(Math.hypot(after.x-before.x,after.z-before.z)<1e-8);
    assert.equal(lineHeading(g.route,g.turns,t+.001),g.route.headingAfter[0]);
    const future=linePos(g.route,g.turns,g.taps[0]+.2,g.cursor),centre=posAt(g.route,g.taps[0]+.2);
    assert.ok(Math.hypot(future.x-centre.x,future.z-centre.z)>.5,'input offset must remain, not pull to centre');
  }
});
test('OMG fails when its actual line leaves the visible road, and restart clears all attempt state',()=>{
  const g=new Game(L,{centerAssist:false});g.prepare();g.start();
  assert.equal(g.tap(g.taps[0]-.7),'hit');
  g.update(g.taps[0]+.3);assert.equal(g.failKind,'wall');
  g.prepare(0);assert.equal(g.turns.length,0);assert.equal(g.cursor,0);assert.equal(g.failTime,0);assert.equal(g.failKind,null);
  assert.deepEqual(linePos(g.route,g.turns,0,0),posAt(g.route,0));
  g.start();assert.equal(g.tap(g.taps[0]),'hit');assert.equal(g.status,'playing');
});
test('bounce input does not consume the next corner',()=>{
  const g=new Game(L,{centerAssist:false});g.prepare();g.start();const T=g.taps[0];
  assert.equal(g.tap(T),'hit');assert.equal(g.tap(T+.012),'ignored');assert.equal(g.cursor,1);
});
test('Safari timestamp fallback subtracts queued event age',()=>{
  const a=new AudioTransport();(a as any).ctx={currentTime:10,baseLatency:.01,outputLatency:.02};
  const now=performance.now();const t=(a as any).heardContextTime(now-200);assert.ok(Math.abs(t-9.77)<.003);
});
test('dense OMG parallel road strips have a ground gap including their gold ledges',()=>{
  const g=new Game(L,{centerAssist:false}),w=readableRoadWidths(g.route,()=>2.6),s=g.route.spans;
  let checked=0;
  for(let i=0;i<s.length-2;i++){
    const a=s[i],b=s[i+2];if(a.air||b.air||a.heading%2!==b.heading%2||Math.abs(a.y0-b.y0)>.001||Math.abs(a.y0-a.y1)>.001||Math.abs(b.y0-b.y1)>.001)continue;
    const d=a.heading%2?Math.abs(a.z0-b.z0):Math.abs(a.x0-b.x0);
    if(d>2 && d<2.9){assert.ok(d-(w[i]+w[i+2])/2-.32>=.179,`${i} gap`);checked++;}
  }
  assert.ok(checked>50);assert.ok(Math.min(...w)>=1.2);
});

test('47 percent phrase keeps a steady quarter-note pulse',()=>{
  const taps=L.chart.taps.map(x=>x.t).filter(t=>t>=75.1 && t<=77.1);
  assert.equal(taps.length,5);
  for(let i=1;i<taps.length;i++)assert.ok(Math.abs(taps[i]-taps[i-1]-.47243)<.002);
});
test('jumps only occur in long straight input-free windows, never dense phrases',()=>{
  const g=new Game(L,{centerAssist:false});
  for(const s of g.route.spans.filter(s=>s.air)){
    const before=g.taps.filter(t=>t<s.t0).at(-1)??0;
    const after=g.taps.find(t=>t>s.t1)??L.duration;
    assert.ok(after-before>=1.8);
    assert.ok(!g.taps.some(t=>t>=s.t0-.3&&t<=s.t1+.3));
  }
  assert.equal(g.route.spans.some(s=>s.air&&s.t0>2&&s.t0<157.8),false);
});
test('OMG opening road is connected and flat with no opening jump',()=>{
 const g=new Game(L,{centerAssist:false});assert.equal(g.route.spans.some(s=>s.t0<2&&s.air),false);
});

test('audio correction preserves every intended tap and direction, and runtime geometry uses corrected times',()=>{
 const old=JSON.parse(readFileSync('analysis/user/omg-timing-20261019-baseline.json','utf8'));
 const audit=JSON.parse(readFileSync('analysis/user/omg-timing-20261019.json','utf8'));
 assert.equal(L.chart.taps.length,361);assert.equal(audit.changed,20);assert.ok(audit.saved_full_mix_correlation>.999);assert.equal(audit.saved_full_lag_samples,0);
 const g=new Game(L,{centerAssist:false});let changed=0;
 for(let i=0;i<361;i++){assert.equal(L.chart.taps[i].dir,old.taps[i].dir);const d=Math.abs(L.chart.taps[i].t-old.taps[i].t);assert.ok(d<=.025001);if(d>.001)changed++;assert.equal(g.route.tapTimes[i],L.chart.taps[i].t);}
 assert.equal(changed,20);assert.equal(L.duration,160.637);
});

test('dense edge grace rescues a brief 100ms-early skim without teleporting the line',()=>{
 const run=(assist:boolean)=>{const g=new Game(L,{centerAssist:false}),idx=127;g.prepare(g.taps[idx-1]+.001);
  if(!assist)(g as any).edgeGrace={reset(){},survives(_t:number,d:number){return d<=1e-6;}};
  g.start();const t=g.taps[idx]-.1,before=linePos(g.route,g.turns,t,g.cursor);g.tap(t);
  const after=linePos(g.route,g.turns,t,g.cursor);assert.ok(Math.hypot(after.x-before.x,after.z-before.z)<1e-8);
  for(let j=idx+1;j<idx+10&&g.status==='playing';j++)g.tap(g.taps[j]);return g.status;
 };
 assert.equal(run(true),'playing');assert.equal(run(false),'failed');
});

test('centering defaults on, toggles off, and never changes dense road widths',()=>{
 const centered=new Game(L),free=new Game(L,{centerAssist:false});
 assert.equal(centered.route.freeTurns,false);assert.equal(free.route.freeTurns,true);
 for(const T of centered.taps)assert.equal(centered.roadWidth(T),free.roadWidth(T));
 for(const offset of [-.08,.08]){
  const g=new Game(L);g.prepare();g.start();const T=g.taps[0];assert.equal(g.tap(T+offset),'hit');
  const p=linePos(g.route,g.turns,T+.2,g.cursor),c=posAt(g.route,T+.2);assert.deepEqual(p,c);
 }
 centered.prepare();centered.start();for(const t of centered.taps)assert.equal(centered.tap(t),'hit');centered.update(L.duration);assert.equal(centered.status,'complete');
 centered.setCenterAssist(false);centered.prepare();assert.equal(centered.route.freeTurns,true);
});

test('checkpoint revival discards previous free-turn offsets without resetting earned score',()=>{
 const g=new Game(L,{centerAssist:false});g.prepare();g.start();g.tap(g.taps[0]-.08);const score=g.good;g.checkpointsUsed.add(0);
 g.prepare(53.968,true,true);assert.equal(g.good,score);assert.ok(g.checkpointsUsed.has(0));
 const p=linePos(g.route,g.turns,g.time,g.cursor),c=posAt(g.route,g.time);assert.ok(Math.hypot(p.x-c.x,p.z-c.z)<1e-6);
 g.start();g.update(54.05);assert.equal(g.status,'playing');g.prepare(0);g.start();g.update(1);assert.equal(g.status,'playing');assert.equal(g.cursor,0);
});
