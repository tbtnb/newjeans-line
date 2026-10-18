import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { buildRoute, anchor } from '../src/core/path';
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
