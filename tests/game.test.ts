import test from 'node:test';
import assert from 'node:assert/strict';
import { Game, judgmentWindows, geometricWindow, WINDOW_MIN, WINDOW_MAX } from '../src/core/game';
import { buildRoute, posAt, anchor } from '../src/core/path';
import type { LevelData } from '../src/core/types';

const mk = (taps: number[], extra: Partial<LevelData['layout']> = {}, dirs?: ('L'|'R')[]): LevelData => ({
  id: 't', title: 't', album: '', duration: 20, bpm: 120, audio: '', cover: '', difficulty: 1, accent: '#fff',
  chart: { id: 't', taps: taps.map((t, i) => ({ t, dir: dirs?.[i] })), sections: [{ t: 0, label: 'a', kind: 'intro' }] },
  layout: { id: 't', palette: {} as never, road: { width: [{ t: 0, w: 2 }], reveal: [] }, diamonds: [{ t: 1.5 }], crowns: [{ t: 5 }], ...extra },
});

test('route alternates R/L by default and integrates speed', () => {
  const r = buildRoute(mk([1, 2]).chart, [], 20);
  assert.deepEqual(r.dirs, ['R', 'L']);
  const p = posAt(r, 1.5);
  assert.ok(Math.abs(p.z - 9) < 1e-9 && Math.abs(p.x - 4.5) < 1e-9);
  const q = posAt(r, 3);
  assert.ok(Math.abs(q.x - 9) < 1e-9 && Math.abs(q.z - 18) < 1e-9);
});

test('explicit R,R makes a U-turn', () => {
  const r = buildRoute(mk([1, 2], {}, ['R', 'R']).chart, [], 20);
  const p = posAt(r, 3);
  assert.ok(Math.abs(p.x - 9) < 1e-9 && Math.abs(p.z - 0) < 1e-9);
});

test('anchor side is to the right of travel', () => {
  const r = buildRoute(mk([5]).chart, [], 20);
  const a = anchor(r, 1, 3);
  assert.ok(Math.abs(a.pos.x - 3) < 1e-9);
});

test('fall lowers the road after air time', () => {
  const r = buildRoute(mk([5]).chart, [{ type: 'fall', t: 2, dy: -4 }], 20);
  assert.ok(Math.abs(posAt(r, 4).y + 4) < 1e-9);
  assert.ok(posAt(r, 2.2).y > -4);
});

test('windows shrink with dense gaps but stay within bounds', () => {
  const w = judgmentWindows([1, 1.15, 1.3, 3]);
  assert.ok(Math.abs(w[0] - 0.075) < 1e-9, 'half the 0.15 s gap');
  assert.ok(w[3] <= WINDOW_MAX && w[3] >= WINDOW_MIN);
  for (const x of w) assert.ok(x >= WINDOW_MIN && x <= WINDOW_MAX);
});

test('window follows the road: late tap survives while the head centre is on the road', () => {
  const w = judgmentWindows([2, 4, 6], i => geometricWindow([2.6, 1.8, 6][i], 9));
  assert.ok(Math.abs(w[0] - 1.3 / 9) < 1e-9); assert.ok(Math.abs(w[1] - 0.9 / 9) < 1e-9); assert.equal(w[2], WINDOW_MAX);
});

test('hit within window, fail early, fail late, extra tap fails', () => {
  const g = new Game(mk([2, 4])); g.prepare(); g.start();
  g.update(1.9); assert.equal(g.tap(1.95), 'hit');
  assert.equal(g.tap(3.0), 'fail'); assert.equal(g.failKind, 'early');
  const h = new Game(mk([2, 4])); h.prepare(); h.start(); h.update(2.2); assert.equal(h.status, 'playing', 'grace for queued input');
  assert.equal(h.tap(2.105), 'hit', 'event stamped inside the window but delivered late still counts');
  const h2 = new Game(mk([2, 4])); h2.prepare(); h2.start(); h2.update(2.3); assert.equal(h2.status, 'failed'); assert.equal(h2.failKind, 'late'); assert.ok(Math.abs(h2.failTime - (2 + h2.windows[0])) < 1e-9);
  const h3 = new Game(mk([2, 4])); h3.prepare(); h3.start(); h3.update(2.2); assert.equal(h3.tap(2.18), 'fail'); assert.equal(h3.failKind, 'late');
  const k = new Game(mk([2])); k.prepare(); k.start(); k.tap(2); assert.equal(k.tap(10), 'fail'); assert.equal(k.failKind, 'extra');
});

test('duplicate events within debounce are ignored, a real second tap is judged', () => {
  const g = new Game(mk([2, 2.2])); g.prepare(); g.start();
  assert.equal(g.tap(2.0), 'hit'); assert.equal(g.tap(2.02), 'ignored'); assert.equal(g.tap(2.21), 'hit');
});

test('missing an end tap is not required; completes at duration and collects', () => {
  const g = new Game(mk([2])); g.prepare(); g.start(); g.tap(2.01); g.update(20);
  assert.equal(g.status, 'complete'); assert.equal(g.diamondsTaken.size, 1); assert.equal(g.crownsEarned(), 3);
});

test('checkpoint prepare keeps earlier diamonds and drops later ones', () => {
  const g = new Game(mk([2, 8], { diamonds: [{ t: 1.5 }, { t: 6 }] })); g.prepare(); g.start(); g.tap(2); g.update(7.9);
  assert.equal(g.diamondsTaken.size, 2); g.prepare(5, true); assert.deepEqual([...g.diamondsTaken], [0]); assert.equal(g.cursor, 1);
});

import { linePos } from '../src/core/linepath';
test('linePos keeps square corners: early taps turn exactly at the corner, late taps overshoot then snap back', () => {
  const lv = mk([2, 4]); const r = buildRoute(lv.chart, [], 20);
  const early = [{ index: 0, chartT: 2, tapT: 1.94 }];
  for (const t of [1.94, 1.99, 2.0, 2.3, 3]) { const p = linePos(r, early, t, 1), q = posAt(r, t); assert.ok(Math.hypot(p.x - q.x, p.z - q.z) < 1e-6, 'on centreline at ' + t); }
  // late: before the tap is accepted the line goes straight past the corner
  const c = posAt(r, 2 - 1e-6), e = linePos(r, [], 2.06, 0); const h0 = r.spans[0].heading;
  assert.ok(Math.abs(Math.hypot(e.x - c.x, e.z - c.z) - 0.06 * r.spans[0].v) < 1e-3);
  assert.equal(r.spans[0].heading, h0);
  const late = [{ index: 0, chartT: 2, tapT: 2.06 }];
  const f = linePos(r, late, 2.06, 1), g = posAt(r, 2.06); assert.ok(Math.hypot(f.x - g.x, f.z - g.z) < 1e-6, 'snaps back to the centreline');
});

test('falls/jumps land before the next tap (no turning in mid-air)', async () => {
  const { buildRoute } = await import('../src/core/path');
  const chart = { id: 'x', taps: [{ t: 2 }, { t: 5.3 }, { t: 9 }], sections: [] } as any;
  const r = buildRoute(chart, [{ type: 'fall', t: 5.0, dy: -4 }, { type: 'jump', t: 8.7, dy: 3 }], 12);
  for (const s of r.spans) if (s.air) assert.ok(s.turnIndex < 0, 'no tap ends an airborne span');
  const airEnd = Math.max(...r.spans.filter(s => s.air && s.t0 >= 5 && s.t0 < 6).map(s => s.t1));
  assert.ok(airEnd <= 5.3 - 0.04, 'fall shortened to land before tap at 5.3, got ' + airEnd);
  const landY = r.spans.find(s => s.t0 >= airEnd - 1e-6 && !s.air)!.y0;
  assert.ok(Math.abs(landY + 4) < 1e-6, 'lands at -4, got ' + landY);
});

test('16th bursts at 0.11 s: per-tap windows never overlap; every real tap lands, duplicates are ignored', () => {
  const burst = [2, 2.11, 2.22, 2.33, 2.44, 2.55];
  const g = new Game(mk(burst)); g.prepare(); g.start();
  const w = g.windows;
  for (let i = 0; i + 1 < burst.length; i++) assert.ok(burst[i] + w[i] <= burst[i + 1] - w[i + 1] + 1e-9, 'windows never overlap');
  assert.ok(Math.abs(w[2] - 0.055) < 1e-9);
  for (const [i, t] of burst.entries()) {
    assert.equal(g.tap(t + (i % 2 ? 0.03 : -0.03)), 'hit', 'tap ' + i);
    assert.equal(g.tap(t + (i % 2 ? 0.03 : -0.03) + 0.008), 'ignored', 'double-trigger ' + i);
  }
  assert.equal(g.cursor, burst.length);
  const h = new Game(mk(burst)); h.prepare(); h.start();
  assert.equal(h.tap(2.0), 'hit'); assert.equal(h.tap(2.164), 'hit', 'a tap at the boundary goes to the pending corner once'); assert.equal(h.cursor, 2);
  assert.equal(h.tap(2.30), 'fail', 'a tap beyond the window is a fail, never a double count'); assert.equal(h.failKind, 'late');
});

test('level that ends before the audio (layout.endTime): route, progress and completion use the level length', () => {
  const lv = { ...mk([2, 4]), duration: 12, audioDuration: 30, endFade: 1.5 };
  const g = new Game(lv); g.prepare(); g.start(); g.tap(2); g.tap(4);
  g.update(6); assert.ok(Math.abs(g.progress - 0.5) < 1e-9);
  g.update(12); assert.equal(g.status, 'complete');
  assert.equal(g.route.duration, 12);
});
