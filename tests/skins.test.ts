import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import { SKINS, DEFAULT_SKIN, getSkin, isSkinId } from '../src/skins';

test('skin registry is well formed', () => {
  assert.equal(SKINS[0].id, DEFAULT_SKIN); assert.ok(SKINS[0].levelColor);
  const ids = new Set<string>();
  for (const s of SKINS) {
    assert.ok(isSkinId(s.id), s.id); assert.ok(!ids.has(s.id)); ids.add(s.id);
    for (const c of [s.head, s.trail, s.glow, s.ui, ...s.decorColors, ...s.burst.colors, ...s.shatter.colors]) assert.match(c, /^#[0-9a-f]{6}$/i, `${s.id} ${c}`);
    for (const f of [s.tex, s.burst.sprite, s.shatter.sprite]) if (f) assert.ok(existsSync(`public/${f}`), `${s.id}: missing public/${f}`);
    if (s.id !== DEFAULT_SKIN) assert.ok(existsSync(`public/skins/${s.id}/icon.png`), `${s.id}: missing icon`);
  }
  assert.ok(SKINS.length >= 6);
  assert.equal(getSkin('nope').id, DEFAULT_SKIN); assert.equal(getSkin(undefined).id, DEFAULT_SKIN); assert.equal(getSkin('denim').id, 'denim');
});
