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

test('skin setting: old saves default to classic, skin round-trips, bad values fall back', () => {
  // v1 and v2 saves written before skins existed have no settings.skin
  assert.equal(parseSave(v1, ids, 'attention').settings.skin, 'classic');
  const oldV2 = { version: 2, selected: 'ditto', records: { ditto: { best: 1, diamonds: 10, crowns: 3, attempts: 9, completed: true } }, settings: { volume: 0.3, offsetMs: -15, quality: 'high', vibration: true } };
  const s = parseSave(oldV2, ids, 'attention');
  assert.equal(s.settings.skin, 'classic');
  // everything else in the old save is unchanged
  assert.deepEqual({ ...s.settings, skin: undefined }, { ...oldV2.settings, skin: undefined, targetFps:60, showFps:false });
  assert.deepEqual(s.records.ditto, oldV2.records.ditto);
  // a chosen skin survives export -> import and persist -> load
  const withSkin = { ...s, settings: { ...s.settings, skin: 'bubble-gum' } };
  assert.equal(parseSave(JSON.parse(JSON.stringify(withSkin)), ids, 'attention').settings.skin, 'bubble-gum');
  const mem: Record<string, string> = { [KEY_V2]: JSON.stringify(withSkin) };
  assert.equal(loadSave(ids, 'attention', { getItem: (k: string) => mem[k] ?? null }).settings.skin, 'bubble-gum');
  // unknown future skin ids are kept (rendered as classic by the game); junk falls back
  assert.equal(parseSave({ ...oldV2, settings: { ...oldV2.settings, skin: 'future-skin' } }, ids, 'a').settings.skin, 'future-skin');
  for (const bad of [42, null, '', '<script>', 'x'.repeat(40), { id: 'denim' }]) assert.equal(parseSave({ ...oldV2, settings: { ...oldV2.settings, skin: bad } }, ids, 'a').settings.skin, 'classic');
  // a fresh profile defaults to classic
  assert.equal(loadSave(ids, 'attention', { getItem: () => null }).settings.skin, 'classic');
});


test('frame-rate settings migrate safely and round-trip without changing old progress',()=>{
 const old=parseSave(v1,ids,'attention');assert.equal(old.settings.targetFps,60);assert.equal(old.settings.showFps,false);
 const updated={...old,settings:{...old.settings,targetFps:120,showFps:true}};
 const imported=parseSave(JSON.parse(JSON.stringify(updated)),ids,'attention');assert.equal(imported.settings.targetFps,120);assert.equal(imported.settings.showFps,true);assert.deepEqual(imported.records,old.records);
 assert.equal(parseSave({...updated,settings:{targetFps:999}},ids,'attention').settings.targetFps,60);
});
