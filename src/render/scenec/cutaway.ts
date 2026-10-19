/**
 * Cutaway for concept-C decor: fragments inside a cone from the camera to just past the line's head are dithered out
 * (screen-door), so a tree / bunny / tower between the camera and the head never hides the line or the next road.
 * Shared state: one camera / target pair updated per frame, read by every material that carries the plugin.
 */
import { MaterialPluginBase } from '@babylonjs/core/Materials/materialPluginBase';
import type { Material } from '@babylonjs/core/Materials/material';
import type { UniformBuffer } from '@babylonjs/core/Materials/uniformBuffer';
import { Vector3 } from '@babylonjs/core/Maths/math.vector';

export const CUT = { cam: new Vector3(0, 50, -50), head: new Vector3(), radius: 6.5, on: true };

export class Cutaway extends MaterialPluginBase {
  constructor(m: Material) { super(m, 'Cutaway', 300, { CUTAWAY: false }); this._enable(true); }
  prepareDefines(defines: Record<string, unknown>) { defines.CUTAWAY = CUT.on; }
  getClassName() { return 'Cutaway'; }
  getUniforms() {
    return { ubo: [{ name: 'cutCam', size: 3, type: 'vec3' }, { name: 'cutHead', size: 3, type: 'vec3' }, { name: 'cutR', size: 1, type: 'float' }],
      fragment: '#ifdef CUTAWAY\nuniform vec3 cutCam;\nuniform vec3 cutHead;\nuniform float cutR;\n#endif\n' };
  }
  bindForSubMesh(ubo: UniformBuffer) { ubo.updateVector3('cutCam', CUT.cam); ubo.updateVector3('cutHead', CUT.head); ubo.updateFloat('cutR', CUT.radius); }
  getCustomCode(type: string) {
    if (type !== 'fragment') return null;
    // v10: fragments below ~head height (ground cover, low decor) can't hide the line from the high camera - never dithered (the near-camera fade patches)
    return { CUSTOM_FRAGMENT_MAIN_BEGIN: `
#ifdef CUTAWAY
{ vec3 ab = cutHead - cutCam; float k = clamp(dot(vPositionW - cutCam, ab) / max(dot(ab, ab), 1e-3), 0., 1.);
  if (k < 0.985 && vPositionW.y > cutHead.y - 0.25) { float d = length(vPositionW - (cutCam + ab * k)); float r = cutR * (0.25 + 0.75 * k);
    float f = 1. - smoothstep(r * 0.55, r, d);
    float n = fract(sin(dot(floor(gl_FragCoord.xy), vec2(12.9898, 78.233))) * 43758.5453);
    if (n < f) discard; } }
#endif
` };
  }
}
