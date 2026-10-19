import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { NullEngine } from '@babylonjs/core/Engines/nullEngine';
import { Scene } from '@babylonjs/core/scene';
import { CameraRig } from '../src/render/camera';
import { Game } from '../src/core/game';
import { posAt } from '../src/core/path';

test('key gameplay camera ignores beat punch, zoom cues and event shake at 15/60 fps', () => {
  const level = JSON.parse(readFileSync('src/levels/omg.json', 'utf8'));
  const route = new Game(level).route;
  const engine = new NullEngine();
  const scene = new Scene(engine);
  try {
    for (const fps of [15, 60]) {
      const neutral = new CameraRig(scene, route, [{t:0, punch:0, zoom:1, shake:0}], [], [], false);
      const effects = new CameraRig(scene, route, [{t:0, punch:.15, zoom:1.3, shake:2}, {t:43, blend:.3, zoom:.8, punch:.2, shake:3}], [], level.chart.taps, false);
      neutral.keyMode = effects.keyMode = true;
      neutral.aspect = effects.aspect = 390 / 844;
      for (let frame = 0; frame <= Math.ceil(level.duration * fps); frame++) {
        const t = Math.min(level.duration, frame / fps), head = posAt(route, t);
        effects.shakeBoost = 4;
        neutral.update(t, head, 1 / fps);
        effects.update(t, head, 1 / fps);
        assert.ok(neutral.cam.position.subtract(effects.cam.position).length() < 1e-7, `position at ${t}`);
        assert.ok(neutral.cam.getTarget().subtract(effects.cam.getTarget()).length() < 1e-7, `target at ${t}`);
        assert.ok(Number.isFinite(effects.lastFx) && Number.isFinite(effects.lastFy));
      }
      neutral.cam.dispose(); effects.cam.dispose();
    }
  } finally { scene.dispose(); engine.dispose(); }
});
