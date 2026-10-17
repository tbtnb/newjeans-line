import test from 'node:test';
import assert from 'node:assert/strict';
import { defaultSettings, emptyRecord, loadSave, persistSave, validateSave } from '../src/storage';
import type { SaveData } from '../src/types';

const ids = ['new-jeans', 'get-up'];
const save: SaveData = {
  version: 1, selected: 'get-up', settings: { ...defaultSettings, volume: 0.42, quality: 'low' },
  records: { 'get-up': { best: 1, crowns: 3, diamonds: 10, completed: true, attempts: 4 } },
};

function withStorage(run: (values: Map<string, string>) => void) {
  const descriptor = Object.getOwnPropertyDescriptor(globalThis, 'localStorage');
  const values = new Map<string, string>();
  Object.defineProperty(globalThis, 'localStorage', { configurable: true, value: {
    getItem: (key: string) => values.get(key) ?? null,
    setItem: (key: string, value: string) => values.set(key, value),
  } });
  try { run(values); }
  finally {
    if (descriptor) Object.defineProperty(globalThis, 'localStorage', descriptor);
    else Reflect.deleteProperty(globalThis, 'localStorage');
  }
}

test('settings, selected song and a completed record survive a storage round trip', () => withStorage(() => {
  assert.equal(persistSave(save), true);
  assert.deepEqual(loadSave(ids, ids[0]), save);
  const validated = validateSave(JSON.parse(JSON.stringify(save)), ids);
  validated.records['get-up'].attempts = 99;
  assert.equal(save.records['get-up'].attempts, 4, 'validation returns independent records');
}));

test('corrupt import is rejected before the existing save can be replaced', () => withStorage(values => {
  persistSave(save);
  const previous = values.get('newjeans-line.save.v1');
  const invalid = { ...save, records: { 'get-up': { ...save.records['get-up'], best: 0.6 } } };
  assert.throws(() => persistSave(validateSave(invalid, ids)), /不一致/);
  assert.equal(values.get('newjeans-line.save.v1'), previous);
  assert.deepEqual(loadSave(ids, ids[0]), save);
}));

test('unknown songs, nonfinite settings and fractional collectibles are rejected', () => {
  assert.throws(() => validateSave({ ...save, selected: 'missing' }, ids));
  assert.throws(() => validateSave({ ...save, settings: { ...save.settings, volume: NaN } }, ids));
  assert.throws(() => validateSave({ ...save, records: { 'get-up': { ...emptyRecord(), diamonds: 1.5 } } }, ids));
});

test('unreadable stored JSON falls back to a fresh save without throwing', () => withStorage(values => {
  values.set('newjeans-line.save.v1', '{broken');
  assert.deepEqual(loadSave(ids, ids[0]), { version: 1, selected: ids[0], settings: defaultSettings, records: {} });
}));
