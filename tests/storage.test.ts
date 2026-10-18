import test from 'node:test';
import assert from 'node:assert/strict';
import { parseSave, loadSave, KEY_V1, KEY_V2, mergeRecord } from '../src/storage';

const ids = ['attention', 'ditto'];
const v1 = { version: 1, selected: 'ditto', records: { ditto: { best: 0.5, diamonds: 5, crowns: 1, attempts: 3, completed: false }, contact: { best: 1 } }, settings: { volume: 0.5, offsetMs: 20, quality: 'low', vibration: false, guide: true } };

test('v1 save migrates and keeps records, settings and unknown songs', () => {
  const s = parseSave(v1, ids, 'attention');
  assert.equal(s.version, 2); assert.equal(s.migratedFrom, 1); assert.equal(s.selected, 'ditto');
  assert.equal(s.records.ditto.best, 0.5); assert.equal(s.settings.offsetMs, 20); assert.equal(s.settings.quality, 'low');
  assert.deepEqual((s.legacy as any).records.contact, { best: 1 });
});

test('loadSave prefers v2, falls back to v1 without deleting it', () => {
  const mem: Record<string, string> = { [KEY_V1]: JSON.stringify(v1) };
  const store = { getItem: (k: string) => mem[k] ?? null };
  assert.equal(loadSave(ids, 'attention', store).records.ditto.diamonds, 5);
  mem[KEY_V2] = JSON.stringify({ ...parseSave(v1, ids, 'attention'), selected: 'attention' });
  assert.equal(loadSave(ids, 'attention', store).selected, 'attention');
  assert.ok(mem[KEY_V1]);
});

test('garbage import throws', () => { assert.throws(() => parseSave({ foo: 1 }, ids, 'attention')); assert.throws(() => parseSave(null, ids, 'attention')); });

test('mergeRecord keeps bests', () => {
  const r = mergeRecord({ best: 0.8, diamonds: 7, crowns: 0, attempts: 2, completed: false }, { progress: 0.4, diamonds: 3, crowns: 0, completed: false });
  assert.equal(r.best, 0.8); assert.equal(r.attempts, 3); assert.equal(r.diamonds, 7);
});
