/**
 * Applies a SkinDef (src/skins.ts) to the player's line: head + trail materials (texture/sheen/grain via a small
 * StandardMaterial plugin, so the thin-instanced trail stays one draw call), head decoration, pooled turn-burst and
 * death particle systems. Everything is created on attach / skin change; per-frame work allocates nothing.
 */
import { MaterialPluginBase } from '@babylonjs/core/Materials/materialPluginBase';
import type { Material } from '@babylonjs/core/Materials/material';
import type { UniformBuffer } from '@babylonjs/core/Materials/uniformBuffer';
import type { MaterialDefines } from '@babylonjs/core/Materials/materialDefines';
import type { SubMesh } from '@babylonjs/core/Meshes/subMesh';
import type { AbstractEngine } from '@babylonjs/core/Engines/abstractEngine';
import {
  Color3, Color4, CreateBox, CreateCylinder, CreatePolyhedron, CreateSphere, Mesh, ParticleSystem, Scene, StandardMaterial, Texture, TransformNode, Vector3,
} from './bjs';
import { getSkin, type ParticleSpec, type SkinDef } from '../skins';

const hex3 = (h: string) => Color3.FromHexString(h.length === 7 ? h : '#ffffff');

/** Line-skin surface: local box-space UVs (across the line x stretched, along the run in world units, so a growing
 *  run never makes the pattern swim), optional iridescent sheen and animated film grain. */
class LineSkinPlugin extends MaterialPluginBase {
  tex: Texture | null = null;
  sheen = 0; grain = 0; texLen = 2; time = 0;
  private on = false; private hasMap = false;
  constructor(material: Material) {
    super(material, 'LineSkin', 200, { SKINTEX: false, SKINMAP: false });
  }
  set(on: boolean, tex: Texture | null) {
    this.tex = tex;
    if (on !== this.on || !!tex !== this.hasMap) { this.on = on; this.hasMap = !!tex; this._enable(on); this.markAllDefinesAsDirty(); }
  }
  getClassName() { return 'LineSkinPlugin'; }
  prepareDefines(defines: MaterialDefines) { (defines as any).SKINTEX = this.on; (defines as any).SKINMAP = this.on && this.hasMap; }
  getSamplers(samplers: string[]) { samplers.push('skinSampler'); }
  getUniforms() {
    return { ubo: [{ name: 'skinFx', size: 4, type: 'vec4' }], fragment: '#ifdef SKINTEX\nuniform vec4 skinFx;\n#endif\n' };
  }
  bindForSubMesh(ubo: UniformBuffer, _s: Scene, _e: AbstractEngine, _sm: SubMesh) {
    if (!this.on) return;
    ubo.updateFloat4('skinFx', this.sheen, this.grain, this.time, this.texLen);
    if (this.hasMap && this.tex) ubo.setTexture('skinSampler', this.tex);
  }
  getCustomCode(shaderType: string): { [pointName: string]: string } | null {
    if (shaderType === 'vertex') return {
      CUSTOM_VERTEX_DEFINITIONS: '#ifdef SKINTEX\nvarying vec3 vSkinL;\nvarying vec3 vSkinN;\nvarying float vSkinZ;\n#endif\n',
      CUSTOM_VERTEX_UPDATE_WORLDPOS: '#ifdef SKINTEX\nvSkinL=positionUpdated;\n#ifdef NORMAL\nvSkinN=normalUpdated;\n#else\nvSkinN=vec3(0.,1.,0.);\n#endif\nvSkinZ=(positionUpdated.z+0.5)*length(finalWorld[2].xyz);\n#endif\n',
    };
    if (shaderType === 'fragment') return {
      CUSTOM_FRAGMENT_DEFINITIONS: '#ifdef SKINTEX\nvarying vec3 vSkinL;\nvarying vec3 vSkinN;\nvarying float vSkinZ;\n#ifdef SKINMAP\nuniform sampler2D skinSampler;\n#endif\n#endif\n',
      CUSTOM_FRAGMENT_UPDATE_DIFFUSE: `#ifdef SKINMAP
vec3 skAn=abs(vSkinN);vec2 skUV;
if(skAn.y>0.5){skUV=vec2(vSkinL.x+0.5,vSkinZ/skinFx.w);}
else if(skAn.x>0.5){skUV=vec2(vSkinL.y+0.5,vSkinZ/skinFx.w);}
else{skUV=vec2(vSkinL.x+0.5,vSkinL.y+0.5);}
baseColor.rgb*=texture2D(skinSampler,skUV).rgb;
#endif
`,
      CUSTOM_FRAGMENT_BEFORE_FOG: `#ifdef SKINTEX
float skF=pow(1.0-clamp(dot(normalW,viewDirectionW),0.0,1.0),1.4);
color.rgb+=skinFx.x*(0.5+0.5*cos(6.2832*(skF*1.3+vSkinZ*0.11+skinFx.z*0.05+vec3(0.0,0.33,0.67))))*(0.3+0.9*skF);
float skG=fract(sin(dot(floor(gl_FragCoord.xy*0.5)+floor(skinFx.z*24.0)*vec2(17.0,31.0),vec2(12.9898,78.233)))*43758.5453);
color.rgb+=skinFx.y*(skG-0.5);
#endif
`,
    };
    return null;
  }
}

interface DecorPart { mesh: Mesh; role: string; base: Vector3; sign: number; }

export class LineSkin {
  def: SkinDef = getSkin(null);
  readonly glowColor = new Color3(1, 1, 1);
  private scene: Scene;
  private texCache = new Map<string, Texture>();
  private spark: Texture | null = null;
  private head: Mesh | null = null; private headMat: StandardMaterial | null = null; private trailMat: StandardMaterial | null = null;
  private headPlug: LineSkinPlugin | null = null; private trailPlug: LineSkinPlugin | null = null;
  private root: TransformNode | null = null;
  private decor: TransformNode | null = null; private parts: DecorPart[] = []; private decorMats: StandardMaterial[] = [];
  private burstPS: ParticleSystem | null = null; private deathPS: ParticleSystem | null = null;
  private burstAt = new Vector3(); private deathAt = new Vector3();
  private lastLine = ''; private lastTap = -10;

  constructor(scene: Scene, spark: Texture | null) { this.scene = scene; this.spark = spark; }

  private tex(path: string, pixel = false) {
    const key = path + (pixel ? '#px' : '');
    let t = this.texCache.get(key);
    if (!t) {
      t = new Texture('./' + path, this.scene, false, true, pixel ? Texture.NEAREST_LINEAR_MIPLINEAR : Texture.TRILINEAR_SAMPLINGMODE);
      t.wrapU = Texture.CLAMP_ADDRESSMODE; t.wrapV = Texture.WRAP_ADDRESSMODE; t.anisotropicFilteringLevel = 4;
      this.texCache.set(key, t);
    }
    return t;
  }

  /** called by World.load after the head/trail meshes and materials exist */
  attach(head: Mesh, headMat: StandardMaterial, trailMat: StandardMaterial, root: TransformNode) {
    this.detach();
    this.head = head; this.headMat = headMat; this.trailMat = trailMat; this.root = root;
    this.headPlug = new LineSkinPlugin(headMat); this.trailPlug = new LineSkinPlugin(trailMat);
    this.apply(this.def.id, true);
  }

  /** disposes everything this skin created (materials of decor are under root and die with the level anyway) */
  detach() {
    this.burstPS?.dispose(false); this.deathPS?.dispose(false); this.burstPS = this.deathPS = null;
    for (const p of this.parts) if (!p.mesh.isDisposed()) p.mesh.dispose(false, false); this.parts = [];
    for (const m of this.decorMats) m.dispose(); this.decorMats = [];
    this.decor?.dispose(); this.decor = null;
    this.head = null; this.headMat = this.trailMat = null; this.headPlug = this.trailPlug = null; this.root = null; this.lastLine = '';
  }

  apply(id: string, force = false) {
    const def = getSkin(id);
    if (def === this.def && !force) return;
    this.def = def;
    this.glowColor.copyFrom(hex3(def.glow));
    if (!this.headMat || !this.trailMat || !this.headPlug || !this.trailPlug || !this.root) return;
    const skinned = !def.levelColor;
    const map = def.tex ? this.tex(def.tex, def.pixel) : null;
    const hp = def.headTex === undefined ? def.tex : def.headTex; const hmap = hp ? this.tex(hp, def.pixel) : null;
    for (const [mat, plug, col, m] of [[this.headMat, this.headPlug, def.head, hmap], [this.trailMat, this.trailPlug, def.trail, map]] as const) {
      plug.set(skinned, m);
      plug.sheen = def.sheen ?? 0; plug.grain = def.grain ?? 0; plug.texLen = def.texLen ?? 2;
      if (skinned) {
        const c = hex3(col); mat.diffuseColor.copyFrom(c); mat.emissiveColor.copyFrom(c).scaleInPlace(def.emissive);
        mat.specularColor.set(def.specular, def.specular, def.specular); mat.specularPower = def.specPower;
      } else { mat.specularColor.set(mat === this.headMat ? 0.1 : 0.05, mat === this.headMat ? 0.1 : 0.05, mat === this.headMat ? 0.1 : 0.05); mat.specularPower = 64; }
    }
    this.lastLine = '';
    this.buildDecor();
    this.buildParticles();
  }

  private mat(color: string, emissive = 0.3, alpha = 1, spec = 0.3) {
    const m = new StandardMaterial('skinDecorM', this.scene); const c = hex3(color);
    m.diffuseColor.copyFrom(c); m.emissiveColor.copyFrom(c).scaleInPlace(emissive); m.specularColor.set(spec, spec, spec); m.alpha = alpha;
    this.decorMats.push(m); return m;
  }
  private part(mesh: Mesh, m: StandardMaterial, role: string, x: number, y: number, z: number, sign = 0) {
    mesh.material = m; mesh.parent = this.decor; mesh.position.set(x, y, z); mesh.isPickable = false;
    this.parts.push({ mesh, role, base: new Vector3(x, y, z), sign });
    return mesh;
  }

  private buildDecor() {
    for (const p of this.parts) if (!p.mesh.isDisposed()) p.mesh.dispose(false, false); this.parts = [];
    for (const m of this.decorMats) m.dispose(); this.decorMats = [];
    this.decor?.dispose(); this.decor = null;
    const d = this.def; if (d.decor === 'none' || !this.root) return;
    this.decor = new TransformNode('skinDecor', this.scene); this.decor.parent = this.root;
    const [c1, c2] = d.decorColors; const s = this.scene;
    switch (d.decor) {
      case 'ears': {
        const outer = this.mat('#eef7ff', 0.3, 1, 0.35), inner = this.mat(c1, 0.35), nose = this.mat(c2, 0.4);
        for (const sg of [-1, 1]) {
          const e = this.part(CreateSphere('ear', { diameter: 1, segments: 10 }, s), outer, 'ear', sg * 0.24, 0.78, -0.12, sg); e.scaling.set(0.26, 0.78, 0.16); e.rotation.z = -sg * 0.16;
          const i = this.part(CreateSphere('earIn', { diameter: 1, segments: 8 }, s), inner, 'ear', sg * 0.245, 0.77, -0.04, sg); i.scaling.set(0.14, 0.54, 0.06); i.rotation.z = -sg * 0.16;
        }
        this.part(CreateSphere('nose', { diameter: 0.13, segments: 8 }, s), nose, 'static', 0, 0.06, 0.5);
        this.part(CreateSphere('tail', { diameter: 0.3, segments: 8 }, s), outer, 'static', 0, -0.05, -0.55);
        break;
      }
      case 'rivets': {
        const cu = this.mat(c1, 0.25, 1, 0.9); cu.specularPower = 64;
        for (const [x, z] of [[-0.34, -0.34], [0.34, -0.34], [-0.34, 0.34], [0.34, 0.34]]) { const r = this.part(CreateCylinder('rivet', { diameter: 0.16, height: 0.05, tessellation: 12 }, s), cu, 'static', x, 0.47, z); void r; }
        const tag = this.part(CreateBox('tag', { size: 1 }, s), this.mat(c2, 0.4), 'static', 0.505, 0.12, 0); tag.scaling.set(0.03, 0.22, 0.34);
        break;
      }
      case 'bubble': {
        const b = this.part(CreateSphere('bubble', { diameter: 0.62, segments: 16 }, s), this.mat(c1, 0.35, 0.55, 1), 'bubble', 0, 0.18, 0.66);
        (b.material as StandardMaterial).specularPower = 128; (b.material as StandardMaterial).backFaceCulling = true;
        const hl = this.part(CreateSphere('bubbleHl', { diameter: 0.12, segments: 6 }, s), this.mat('#ffffff', 1), 'bubbleHl', 0.1, 0.32, 0.88); void hl;
        break;
      }
      case 'antenna': {
        const a = this.part(CreateBox('ant', { size: 1 }, s), this.mat(c1, 0.25, 1, 0.6), 'static', 0.3, 0.72, -0.3); a.scaling.set(0.07, 0.5, 0.07);
        this.part(CreateSphere('antTip', { diameter: 0.17, segments: 8 }, s), this.mat(c2, 0.9), 'blink', 0.3, 1.0, -0.3);
        break;
      }
      case 'rec': {
        this.part(CreateSphere('rec', { diameter: 0.15, segments: 8 }, s), this.mat(c1, 1), 'blink', 0.32, 0.48, 0.32);
        const vf = this.mat(c2, 0.5);
        for (const [x, z, sx, sz] of [[-0.38, 0.47, 0.18, 0.04], [-0.47, 0.38, 0.04, 0.18], [0.47, -0.38, 0.04, 0.18], [0.38, -0.47, 0.18, 0.04]]) { const m = this.part(CreateBox('vf', { size: 1 }, s), vf, 'static', x, 0.46, z); m.scaling.set(sx, 0.03, sz); }
        break;
      }
      case 'star': {
        const sm = this.mat(c1, 0.85, 1, 1);
        const a = this.part(CreatePolyhedron('starA', { type: 1, size: 1 }, s), sm, 'star', 0, 1.15, 0); a.scaling.set(0.1, 0.38, 0.05);
        const b = this.part(CreatePolyhedron('starB', { type: 1, size: 1 }, s), sm, 'star', 0, 1.15, 0); b.scaling.set(0.38, 0.1, 0.05);
        this.part(CreateSphere('starCore', { diameter: 0.12, segments: 6 }, s), this.mat(c2, 1), 'star', 0, 1.15, 0);
        break;
      }
    }
  }

  private makePS(spec: ParticleSpec, cap: number, at: Vector3) {
    const ps = new ParticleSystem('skinPS', cap, this.scene);
    ps.particleTexture = spec.sprite ? this.tex(spec.sprite, this.def.pixel) : this.spark;
    ps.emitter = at; ps.emitRate = 0; ps.manualEmitCount = 0;
    const a = hex3(spec.colors[0]), b = hex3(spec.colors[1]);
    ps.color1 = new Color4(a.r, a.g, a.b, 1); ps.color2 = new Color4(b.r, b.g, b.b, 1); ps.colorDead = new Color4(b.r, b.g, b.b, 0);
    ps.minSize = spec.size[0]; ps.maxSize = spec.size[1]; ps.minLifeTime = spec.life[0]; ps.maxLifeTime = spec.life[1];
    ps.minEmitPower = spec.power[0]; ps.maxEmitPower = spec.power[1];
    ps.direction1 = new Vector3(-1, 0.5, -1); ps.direction2 = new Vector3(1, 1.6, 1);
    ps.minEmitBox = new Vector3(-0.35, 0.2, -0.35); ps.maxEmitBox = new Vector3(0.35, 0.7, 0.35);
    ps.renderingGroupId = 1;   // drawn over the line/road so bursts read even where the trail would hide them
    ps.gravity = new Vector3(0, spec.gravity, 0);
    ps.minAngularSpeed = -(spec.spin ?? 0); ps.maxAngularSpeed = spec.spin ?? 0; ps.minInitialRotation = 0; ps.maxInitialRotation = spec.spin ? Math.PI * 2 : 0;
    ps.blendMode = spec.add ? ParticleSystem.BLENDMODE_ADD : ParticleSystem.BLENDMODE_STANDARD;
    ps.isLocal = false; ps.updateSpeed = 1 / 60;
    ps.start();
    return ps;
  }

  private buildParticles() {
    this.burstPS?.dispose(false); this.deathPS?.dispose(false); this.burstPS = this.deathPS = null;
    const d = this.def;
    if (d.burst.count > 0) this.burstPS = this.makePS(d.burst, d.burst.count * 6, this.burstAt);
    if (d.shatter.count > 0) this.deathPS = this.makePS(d.shatter, d.shatter.count + 4, this.deathAt);
  }

  get shardCount() { return this.def.shatter.shards; }

  onTurn(at: Vector3, t: number) {
    this.lastTap = t;
    if (this.burstPS) { this.burstAt.copyFrom(at); this.burstPS.manualEmitCount = this.def.burst.count; }
  }
  onShatter(at: Vector3) {
    if (this.deathPS) { this.deathAt.copyFrom(at); this.deathPS.manualEmitCount = this.def.shatter.count; }
  }
  /** reset transient state (seek / retry) */
  reset() { this.lastTap = -10; this.burstPS?.reset(); this.deathPS?.reset(); }

  /** per frame: line colour for classic, decor follow + animation, shader time. No allocations. */
  update(t: number, lineHex: string, heading: number, headVisible: boolean) {
    const def = this.def;
    if (def.levelColor && this.headMat && this.trailMat && lineHex !== this.lastLine) {
      this.lastLine = lineHex; const lc = hex3(lineHex);
      this.headMat.diffuseColor.copyFrom(lc); this.trailMat.diffuseColor.copyFrom(lc);
      this.headMat.emissiveColor.copyFrom(lc).scaleInPlace(0.25); this.trailMat.emissiveColor.copyFrom(lc).scaleInPlace(0.18);
    }
    const wall = performance.now() / 1000;
    if (this.headPlug) this.headPlug.time = wall; if (this.trailPlug) this.trailPlug.time = wall;
    if (!this.decor || !this.head) return;
    this.decor.setEnabled(headVisible && this.head.isEnabled());
    this.decor.position.copyFrom(this.head.position);
    this.decor.rotation.y = heading === 0 ? 0 : heading === 1 ? Math.PI / 2 : heading === 2 ? Math.PI : -Math.PI / 2;
    const tap = Math.exp(-Math.max(0, t - this.lastTap) * 9);
    for (const p of this.parts) {
      switch (p.role) {
        case 'ear': p.mesh.rotation.x = -0.15 - tap * 0.55; p.mesh.rotation.z = -p.sign * (0.16 + tap * 0.25); break;
        case 'bubble': { const k = Math.min(1, Math.max(0, t - this.lastTap) / 0.45); const s = (0.5 + 0.5 * k * k) * (1 + 0.06 * Math.sin(wall * 5)); p.mesh.scaling.setAll(s); p.mesh.position.z = p.base.z + 0.2 * (s - 1); break; }
        case 'bubbleHl': { const k = Math.min(1, Math.max(0, t - this.lastTap) / 0.45); p.mesh.scaling.setAll(0.5 + 0.5 * k); break; }
        case 'blink': p.mesh.setEnabled(Math.sin(wall * 6.2832) > -0.3 || tap > 0.3); break;
        case 'star': p.mesh.rotation.y = wall * 2.2; p.mesh.position.y = p.base.y + Math.sin(wall * 3) * 0.08 + tap * 0.25; break;
      }
    }
  }

  dispose() { this.detach(); for (const t of this.texCache.values()) t.dispose(); this.texCache.clear(); }
}
