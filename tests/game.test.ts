import test from 'node:test';
import assert from 'node:assert/strict';
import { Game, judgmentWindows, WINDOW_MIN, WINDOW_MAX } from '../src/core/game';
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
  assert.ok(Math.abs(w[0] - 0.0675) < 1e-9);
  assert.ok(w[3] <= WINDOW_MAX && w[3] >= WINDOW_MIN);
  for (const x of w) assert.ok(x >= WINDOW_MIN && x <= WINDOW_MAX);
});

test('hit within window, fail early, fail late, extra tap fails', () => {
  const g = new Game(mk([2, 4])); g.prepare(); g.start();
  g.update(1.9); assert.equal(g.tap(1.95), 'hit');
  assert.equal(g.tap(3.0), 'fail'); assert.equal(g.failKind, 'early');
  const h = new Game(mk([2, 4])); h.prepare(); h.start(); h.update(2.2); assert.equal(h.status, 'failed'); assert.equal(h.failKind, 'late');
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
test('linePos is continuous across an early and a late turn and returns to the centreline', () => {
  const lv = mk([2, 4]); const r = buildRoute(lv.chart, [], 20);
  const early = [{ index: 0, chartT: 2, tapT: 1.94 }];
  const a = linePos(r, [], 1.94 - 1e-6, 0), b = linePos(r, early, 1.94, 1);
  assert.ok(Math.hypot(a.x - b.x, a.z - b.z) < 1e-3);
  const c = linePos(r, early, 3, 1), d = posAt(r, 3);
  assert.ok(Math.hypot(c.x - d.x, c.z - d.z) < 1e-6);
  const late = [{ index: 0, chartT: 2, tapT: 2.06 }];
  const e = linePos(r, [], 2.06 - 1e-6, 0), f = linePos(r, late, 2.06, 1);
  assert.ok(Math.hypot(e.x - f.x, e.z - f.z) < 1e-3);
});
