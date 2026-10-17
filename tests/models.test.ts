import test from 'node:test';
import assert from 'node:assert/strict';
import { NullEngine, Scene, VertexBuffer, type TransformNode } from '@babylonjs/core';
import { WorldModels } from '../src/world-models';
import { LEVEL_ART } from '../src/level-design';

/** Regression for shared-index corruption during Babylon MergeMeshes. A model
 * must retain valid visible geometry, and rebuilding it must not grow its data. */
test('all sixteen native model profiles retain bounded valid geometry through reuse and dispose every owned resource', { timeout: 30000 }, () => {
  const engine = new NullEngine({ renderWidth: 100, renderHeight: 100, textureSize: 128, deterministicLockstep: true, lockstepMaxSteps: 4 });
  try {
    assert.equal(LEVEL_ART.length, 16);
    for (const art of LEVEL_ART) {
      const scene = new Scene(engine);
      try {
        const factory = new WorldModels(scene, art);
        const cases: Array<[string, () => TransformNode]> = [];
        for (let chapter = 0; chapter < 4; chapter++) {
          for (let variant = 0; variant < 4; variant++) cases.push([`scenery-${chapter}-${variant}`, () => factory.createScenery(variant, chapter, 17)]);
          cases.push([`landmark-${chapter}`, () => factory.createLandmark(chapter)]);
        }
        cases.push(['egg', () => factory.createEasterEgg()]);
        const baseline = new Map<string, { vertices: number; indices: number }>();
        for (let round = 0; round < 2; round++) {
          for (const [kind, create] of cases) {
            const root = create();
            factory.update(art.egg.at * 150, art.egg.at);
            const meshes = root.getChildMeshes().filter(mesh => mesh.isVisible && mesh.isEnabled());
            assert.ok(meshes.length > 0, `${art.id} ${kind} has actual visible meshes`);
            let vertices = 0, indices = 0;
            for (const mesh of meshes) {
              const count = mesh.getTotalVertices(), data = mesh.getIndices(), positions = mesh.getVerticesData(VertexBuffer.PositionKind);
              assert.ok(count > 0 && data && data.length > 0 && positions, `${art.id} ${kind} lost geometry`);
              assert.ok(mesh.material && !mesh.isDisposed(), `${art.id} ${kind} lost material/mesh`);
              for (const coordinate of positions!) assert.ok(Number.isFinite(coordinate), `${art.id} ${kind} invalid vertex`);
              for (const index of data!) assert.ok(Number.isInteger(index) && index >= 0 && index < count, `${art.id} ${kind} corrupted shared index`);
              vertices += count; indices += data!.length;
            }
            assert.ok(vertices < 250000 && indices < 1500000, `${art.id} ${kind} unbounded geometry: ${vertices} vertices/${indices} indices`);
            if (round === 0) baseline.set(kind, { vertices, indices });
            else assert.deepEqual({ vertices, indices }, baseline.get(kind), `${art.id} ${kind} geometry grew when shared templates were reused`);
            root.dispose(false, false);
            factory.update(200, 1); // Disposed animation nodes must be harmless.
          }
        }
        factory.dispose();
        factory.dispose(); // Teardown is safe when repeated by an owner.
        for (const [kind, count] of Object.entries({ meshes: scene.meshes.length, materials: scene.materials.length, geometries: scene.geometries.length, transformNodes: scene.transformNodes.length })) {
          assert.equal(count, 0, `${art.id} leaked owned ${kind}`);
        }
      } finally { scene.dispose(); }
    }
  } finally { engine.dispose(); }
});
