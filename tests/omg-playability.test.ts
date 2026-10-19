import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {Game} from '../src/core/game';
import {linePos,lineHeading} from '../src/core/linepath';
import {posAt,headingAt} from '../src/core/path';
import {readableRoadWidths} from '../src/core/roadwidth';
import type {LevelData} from '../src/core/types';
import {AudioTransport} from '../src/audio';
const L=JSON.parse(readFileSync('src/levels/omg.json','utf8')) as LevelData;

test('OMG perfect route remains playable without changing its 361 timestamps',()=>{
  const g=new Game(L);g.prepare();g.start();
  for(const T of g.taps) { assert.equal(g.tap(T),'hit'); }
  g.update(L.duration);assert.equal(g.status,'complete');assert.equal(g.cursor,361);
});
test('early and late taps turn immediately at the current position without a centreline snap',()=>{
  for(const offset of [-.1,.1]) {
    const g=new Game(L);g.prepare();g.start();const t=g.taps[0]+offset;
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
  const g=new Game(L);g.prepare();g.start();
  assert.equal(g.tap(g.taps[0]-.7),'hit');
  g.update(g.taps[0]+.3);assert.equal(g.failKind,'wall');
  g.prepare(0);assert.equal(g.turns.length,0);assert.equal(g.cursor,0);assert.equal(g.failTime,0);assert.equal(g.failKind,null);
  assert.deepEqual(linePos(g.route,g.turns,0,0),posAt(g.route,0));
  g.start();assert.equal(g.tap(g.taps[0]),'hit');assert.equal(g.status,'playing');
});
test('bounce input does not consume the next corner',()=>{
  const g=new Game(L);g.prepare();g.start();const T=g.taps[0];
  assert.equal(g.tap(T),'hit');assert.equal(g.tap(T+.012),'ignored');assert.equal(g.cursor,1);
});
test('Safari timestamp fallback subtracts queued event age',()=>{
  const a=new AudioTransport();(a as any).ctx={currentTime:10,baseLatency:.01,outputLatency:.02};
  const now=performance.now();const t=(a as any).heardContextTime(now-200);assert.ok(Math.abs(t-9.77)<.003);
});
test('dense OMG parallel road strips have a ground gap including their gold ledges',()=>{
  const g=new Game(L),w=readableRoadWidths(g.route,()=>2.6),s=g.route.spans;
  let checked=0;
  for(let i=0;i<s.length-2;i++){
    const a=s[i],b=s[i+2];if(a.air||b.air||a.heading%2!==b.heading%2||Math.abs(a.y0-b.y0)>.001||Math.abs(a.y0-a.y1)>.001||Math.abs(b.y0-b.y1)>.001)continue;
    const d=a.heading%2?Math.abs(a.z0-b.z0):Math.abs(a.x0-b.x0);
    if(d>2 && d<2.9){assert.ok(d-(w[i]+w[i+2])/2-.32>=.299,`${i} gap`);checked++;}
  }
  assert.ok(checked>50);assert.ok(Math.min(...w)>=1.2);
});
