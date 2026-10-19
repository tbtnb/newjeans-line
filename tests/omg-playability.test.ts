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

test('OMG keeps all 361 times and accepts sustained -180 through +150 ms, with no drift off route',()=>{
  assert.equal(L.chart.taps.length,361);assert.equal(L.duration,160.637);
  for(const ms of [-180,-150,-100,-50,-20,0,20,50,100,150]){
    const g=new Game(L);g.prepare();g.start();
    for(const T of g.taps){assert.equal(g.tap(T+ms/1000),'hit',`${T} ${ms}ms`);
      const t=Math.max(T,T+ms/1000),a=linePos(g.route,g.turns,t,g.cursor),b=posAt(g.route,t);assert.ok(Math.hypot(a.x-b.x,a.z-b.z)<1e-5);}
    g.update(L.duration);assert.equal(g.status,'complete');assert.equal(g.cursor,361);
  }
});
test('early buffered turn keeps position AND heading until the chart corner',()=>{
  const g=new Game(L);g.prepare();g.start();const T=g.taps[0];g.tap(T-.15);
  assert.equal(lineHeading(g.route,g.turns,T-.05),headingAt(g.route,T-.05));
  assert.equal(lineHeading(g.route,g.turns,T+.01),headingAt(g.route,T+.01));
});
test('OMG rejects out of window and misses, but ignores bounce and accepts queued in-time input',()=>{
  for(const ms of [-181,151]){const g=new Game(L);g.prepare();g.start();assert.equal(g.tap(g.taps[0]+ms/1000),'fail');}
  const g=new Game(L);g.prepare();g.start();const T=g.taps[0];
  g.lateGrace=.4;g.update(T+.3);assert.equal(g.tap(T-.1),'hit');assert.equal(g.tap(T-.088),'ignored');assert.equal(g.cursor,1);
  const m=new Game(L);m.prepare();m.start();m.update(T+.31);assert.equal(m.failKind,'late');
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
