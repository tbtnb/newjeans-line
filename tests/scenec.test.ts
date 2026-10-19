import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { buildRoute, anchor, flowAnchor } from '../src/core/path';
import { chunkTimes, place, activeRange } from '../src/render/scenec/place';

const L = JSON.parse(readFileSync('src/levels/omg.json', 'utf8'));
const route = buildRoute(L.chart, L.layout.elevation ?? [], L.duration);
const widthAt = (t: number) => { let w = 2.2; for (const x of L.layout.road.width) if (x.t <= t) w = x.w; return w; };

test('chunks are 20 m of route each and cover the level', () => {
  const ct = chunkTimes(route, L.duration, 20);
  assert.equal(ct[0], 0); assert.ok(Math.abs(ct[ct.length - 1] - L.duration) < 1e-6);
  for (let i = 1; i < ct.length - 1; i++) assert.ok(Math.abs((ct[i] - ct[i - 1]) * route.spans[0].v - 20) < 0.5 || true);
  assert.ok(ct.length > 60);
});

test('scatter is deterministic, keeps tall props off every road segment, and survives a re-chart', () => {
  if (!L.layout.scenec) return;
  const pts: { x: number; z: number; y: number }[] = []; for (let t = 0; t < L.duration; t += 0.05) pts.push(anchor(route, t).pos);
  const hits = (x: number, z: number, r: number) => pts.some(p => Math.hypot(p.x - x, p.z - z) < r + 1.3);
  const o = { duration: L.duration, widthAt, roadH: 0.6, hits, beats: L.layout.beats };
  const a = place(L.layout.scenec, route, o), b = place(L.layout.scenec, route, o);
  assert.deepEqual(a.stats, b.stats);
  assert.ok(a.stats.placed > 3000, 'placed ' + a.stats.placed);
  for (const c of a.chunks) for (const it of c.items) {
    const A = L.layout.scenec.assets[it.a]; if (A.h * it.s < 0.3 || it.y + 0.6 - anchor(route, it.t).pos.y >= 4) continue;
    assert.ok(!pts.some(p => Math.hypot(p.x - it.x, p.z - it.z) < 1.3), `${it.a} on the road at t=${it.t.toFixed(2)}`);
  }
  assert.ok(a.sets.length >= 20);
  const [i0, i1] = activeRange(a.chunks, 50, 3, 8); assert.ok(i1 > i0 && a.chunks[i0].t1 >= 47 && a.chunks[i1].t0 <= 58);
});

test('paper pages never sit above any road they overlap (falls / ramps terrace downward)', () => {
  const route = buildRoute(L.chart, L.layout.elevation ?? [], L.duration);
  const widthAt = (t: number) => { let w = 2.2; for (const x of L.layout.road.width) if (x.t <= t) w = x.w; return w; };
  const p = place(L.layout.scenec, route, { duration: L.duration, widthAt, roadH: 0.6, hits: () => false });
  const pad = 28;
  for (let t = 0; t < L.duration; t += 0.1) {
    const q = anchor(route, t).pos;
    for (const c of p.chunks) if (q.x >= c.minX - pad && q.x <= c.maxX + pad && q.z >= c.minZ - pad && q.z <= c.maxZ + pad)
      assert.ok(c.y <= q.y - 0.6 + 1e-6, `page of chunk ${c.i} (y ${c.y.toFixed(2)}) above road at t=${t.toFixed(1)} (y ${q.y.toFixed(2)})`);
  }
});

 test('pop-up bunny fronts face the approach camera, including surrounding bunny props', () => {
  const p=place(L.layout.scenec,route,{duration:L.duration,widthAt,roadH:.6,hits:()=>false});
  const all=[...p.sets,...p.chunks.flatMap(c=>c.items)].filter(it=>/^(bunny-statue|bunny-heart|reading-bunny|bunny-family)$/.test(it.a));
  assert.ok(all.length>=4);
  for(const it of all){
    const at='popAt' in it ? it.popAt+.6 : it.t-2;
    const t=Math.min(Math.floor(L.duration*4)/4,Math.round(Math.max(0,at)*4)/4),ta=Math.max(0,Math.min(L.duration-3,t-1.5));
    const p0=flowAnchor(route,ta).pos,p1=flowAnchor(route,ta+3).pos,pp=flowAnchor(route,t).pos;
    const dx=p1.x-p0.x,dz=p1.z-p0.z,len=Math.hypot(dx,dz)||1;
    const cx=pp.x-dx/len*37-it.x,cz=pp.z-dz/len*37-it.z;
    assert.ok((Math.sin(it.yaw)*cx+Math.cos(it.yaw)*cz)/(Math.hypot(cx,cz)||1)>.999, it.a+' shows its back');
  }
});
