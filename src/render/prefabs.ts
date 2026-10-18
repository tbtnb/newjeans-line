import { Texture, Color3, CreateBox, CreateCylinder, CreateDisc, CreateIcoSphere, CreatePlane, CreatePolyhedron, CreateSphere, CreateTorus, DynamicTexture, ExtrudeShape, Mesh, Scene, StandardMaterial, TransformNode, Vector3 } from './bjs';
import type { Part, SceneObject } from '../core/types';

export const hex = (c: string | undefined, d = '#ffffff') => Color3.FromHexString(/^#[0-9a-fA-F]{6}$/.test(c ?? '') ? c! : d);

export class Materials {
  private cache = new Map<string, StandardMaterial>();
  constructor(private scene: Scene) {}
  get(color: string, opts: { alpha?: number; emissive?: number; key?: string } = {}): StandardMaterial {
    const key = `${color}|${opts.alpha ?? 1}|${opts.emissive ?? 0}`;
    let m = this.cache.get(key);
    if (!m) {
      m = new StandardMaterial('m' + key, this.scene);
      const c = hex(color);
      m.diffuseColor = c;
      m.specularColor = new Color3(0.06, 0.06, 0.06);
      m.emissiveColor = c.scale(0.1 + (opts.emissive ?? 0));
      if (opts.alpha !== undefined && opts.alpha < 1) { m.alpha = opts.alpha; m.backFaceCulling = false; }
      this.cache.set(key, m);
    }
    return m;
  }
  /** base URL for level art (e.g. ./levels/ditto/) */
  artBase = './';
  textured(src: string, opts: { alpha?: boolean; emissive?: number } = {}): StandardMaterial {
    const key = `tex|${this.artBase}${src}|${opts.alpha ? 1 : 0}|${opts.emissive ?? 0.35}`;
    let m = this.cache.get(key);
    if (!m) {
      m = new StandardMaterial('m' + key, this.scene);
      const t = new Texture(this.artBase + src, this.scene, false, true, Texture.TRILINEAR_SAMPLINGMODE);
      if (opts.alpha) { t.hasAlpha = true; m.useAlphaFromDiffuseTexture = true; }
      m.diffuseTexture = t; m.diffuseColor = new Color3(1, 1, 1); m.specularColor = new Color3(0.03, 0.03, 0.03);
      m.emissiveColor = new Color3(1, 1, 1).scale(opts.emissive ?? 0.35); m.backFaceCulling = false;
      this.cache.set(key, m);
    }
    return m;
  }
  dispose() { for (const m of this.cache.values()) m.dispose(); this.cache.clear(); }
}

const DEF: Record<string, number[]> = {
  box: [1, 1, 1], cylinder: [1, 1, 1], cone: [1, 1.5, 1], sphere: [1, 1, 1], torus: [2, 0.4, 2], plane: [4, 0, 4], disc: [4, 0, 4],
  tree: [2, 4, 2], pine: [2, 5, 2], cloud: [5, 2, 3], building: [4, 10, 4], tower: [3, 16, 3], arch: [6, 6, 1], pillar: [1, 6, 1],
  lamp: [0.4, 4, 0.4], flower: [1, 1.6, 1], heart: [2, 2, 0.6], star: [2, 2, 0.5], note: [1.2, 2.4, 0.4], bubble: [2, 2, 2],
  rock: [2, 1.4, 2], bridge: [3, 1, 10], stairs: [3, 3, 4], water: [60, 0, 60], moon: [6, 6, 6], sun: [8, 8, 8], ring: [4, 0.4, 4],
  crystal: [1, 3, 1], cassette: [4, 2.5, 0.6], phone: [2, 4, 0.3], bench: [2.4, 1, 0.8], pyramid: [5, 5, 5], text: [6, 0, 1.6], image: [4, 0, 4],
};

function starShape(points: number, rO: number, rI: number) { const s: Vector3[] = []; for (let i = 0; i < points * 2; i++) { const r = i % 2 ? rI : rO; const a = Math.PI / 2 + i * Math.PI / points; s.push(new Vector3(Math.cos(a) * r, Math.sin(a) * r, 0)); } s.push(s[0].clone()); return s; }
function heartShape() { const s: Vector3[] = []; for (let i = 0; i <= 40; i++) { const t = (i / 40) * Math.PI * 2; const x = 16 * Math.sin(t) ** 3; const y = 13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t); s.push(new Vector3(x / 17, y / 17 + 0.1, 0)); } return s; }
function extrudeFlat(name: string, shape: Vector3[], depth: number, scene: Scene) {
  return ExtrudeShape(name, { shape, path: [new Vector3(0, 0, -depth / 2), new Vector3(0, 0, depth / 2)], cap: Mesh.CAP_ALL, sideOrientation: Mesh.DOUBLESIDE }, scene);
}

export function textPlane(scene: Scene, text: string, color: string, size: number[], mats?: Materials): Mesh {
  const w = size[0] || 6, h = size[2] || 1.6;
  const px = 512, py = Math.max(64, Math.round(512 * h / w));
  const tex = new DynamicTexture('txt' + text, { width: px, height: py }, scene, true);
  const ctx = tex.getContext() as unknown as CanvasRenderingContext2D;
  ctx.clearRect(0, 0, px, py);
  ctx.fillStyle = color; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.font = `300 ${Math.round(py * 0.72)}px "Avenir Next", "Futura", "Helvetica Neue", "PingFang SC", sans-serif`;
  ctx.fillText(text, px / 2, py / 2 + 2);
  tex.hasAlpha = true; tex.update();
  const m = new StandardMaterial('txtm' + text, scene);
  m.diffuseTexture = tex; m.useAlphaFromDiffuseTexture = true; m.emissiveColor = new Color3(0.6, 0.6, 0.6); m.specularColor = Color3.Black(); m.backFaceCulling = false;
  const p = CreatePlane('txt', { width: w, height: h }, scene);
  p.material = m; p.rotation.x = Math.PI / 2;
  void mats;
  return p;
}

/** Build a prefab/primitive. The node's local frame: x right, y up, z forward. Origin at the base centre. */
export function buildKind(scene: Scene, mats: Materials, o: SceneObject | Part, parent: TransformNode): TransformNode {
  const kind = o.kind;
  const size = (o.size && o.size.length === 3 ? o.size : DEF[kind] ?? [1, 1, 1]) as number[];
  const [sx, sy, sz] = size;
  const color = o.color ?? '#ffffff';
  const color2 = o.color2 ?? shade(color, -0.25);
  const node = new TransformNode(kind, scene);
  node.parent = parent;
  const add = (m: Mesh, mat: StandardMaterial, x = 0, y = 0, z = 0) => { m.parent = node; m.position.set(x, y, z); m.material = mat; m.isPickable = false; return m; };
  const M = (c: string, alpha?: number, emissive?: number) => mats.get(c, { alpha, emissive });
  switch (kind) {
    case 'box': add(CreateBox('b', { width: sx, height: sy, depth: sz }, scene), M(color), 0, sy / 2); break;
    case 'cylinder': add(CreateCylinder('c', { diameterTop: sx, diameterBottom: sx, height: sy, tessellation: 18 }, scene), M(color), 0, sy / 2).scaling.z = sz / sx; break;
    case 'cone': add(CreateCylinder('c', { diameterTop: 0, diameterBottom: sx, height: sy, tessellation: 18 }, scene), M(color), 0, sy / 2).scaling.z = sz / sx; break;
    case 'pyramid': add(CreateCylinder('p', { diameterTop: 0, diameterBottom: sx * 1.41, height: sy, tessellation: 4 }, scene), M(color, undefined, 0.1), 0, sy / 2).rotation.y = Math.PI / 4; break;
    case 'sphere': { const m = add(CreateSphere('s', { diameter: 1, segments: 12 }, scene), M(color), 0, sy / 2); m.scaling.set(sx, sy, sz); break; }
    case 'torus': case 'ring': add(CreateTorus('t', { diameter: sx, thickness: sy, tessellation: 32 }, scene), M(color, undefined, kind === 'ring' ? 0.3 : 0), 0, sy / 2); break;
    case 'plane': case 'water': { const m = add(CreatePlane('pl', { width: sx, height: sz }, scene), M(color, kind === 'water' ? 0.78 : undefined, kind === 'water' ? 0.1 : 0)); m.rotation.x = Math.PI / 2; break; }
    case 'disc': { const m = add(CreateDisc('d', { radius: sx / 2, tessellation: 40 }, scene), M(color)); m.rotation.x = Math.PI / 2; m.scaling.y = sz / sx; break; }
    case 'tree': {
      add(CreateCylinder('tr', { diameterTop: sx * 0.12, diameterBottom: sx * 0.18, height: sy * 0.45, tessellation: 6 }, scene), M(color2), 0, sy * 0.225);
      const c = add(CreateIcoSphere('cn', { radius: 0.5, subdivisions: 1, flat: true }, scene), M(color), 0, sy * 0.66); c.scaling.set(sx, sy * 0.62, sz); break;
    }
    case 'pine': {
      add(CreateCylinder('tr', { diameter: sx * 0.15, height: sy * 0.3, tessellation: 6 }, scene), M(color2), 0, sy * 0.15);
      for (let i = 0; i < 3; i++) add(CreateCylinder('cn', { diameterTop: 0, diameterBottom: sx * (1 - i * 0.22), height: sy * 0.38, tessellation: 7 }, scene), M(color), 0, sy * (0.38 + i * 0.2));
      break;
    }
    case 'cloud': { for (const [x, y, s] of [[-0.3, 0.4, 0.55], [0.05, 0.55, 0.7], [0.35, 0.4, 0.5], [0, 0.3, 0.6]]) { const m = add(CreateSphere('cl', { diameter: 1, segments: 8 }, scene), M(color, 0.95, 0.35), x * sx, y * sy, 0); m.scaling.set(s * sx * 0.8, s * sy, s * sz); } break; }
    case 'building': {
      add(CreateBox('bd', { width: sx, height: sy, depth: sz }, scene), M(color), 0, sy / 2);
      const floors = Math.max(2, Math.floor(sy / 1.6));
      for (let i = 1; i < floors; i++) { add(CreateBox('w', { width: sx * 1.01, height: sy / floors * 0.28, depth: sz * 1.01 }, scene), M(color2), 0, i * sy / floors); }
      add(CreateBox('rf', { width: sx * 1.08, height: 0.3, depth: sz * 1.08 }, scene), M(color2), 0, sy + 0.15);
      break;
    }
    case 'tower': {
      add(CreateCylinder('tw', { diameterTop: sx * 0.8, diameterBottom: sx, height: sy * 0.82, tessellation: 8 }, scene), M(color), 0, sy * 0.41);
      add(CreateCylinder('tp', { diameterTop: 0, diameterBottom: sx * 1.1, height: sy * 0.18, tessellation: 8 }, scene), M(color2), 0, sy * 0.91);
      break;
    }
    case 'arch': {
      const pw = Math.max(0.5, sx * 0.12);
      add(CreateBox('a1', { width: pw, height: sy, depth: sz }, scene), M(color), -sx / 2 + pw / 2, sy / 2);
      add(CreateBox('a2', { width: pw, height: sy, depth: sz }, scene), M(color), sx / 2 - pw / 2, sy / 2);
      add(CreateBox('a3', { width: sx, height: pw, depth: sz }, scene), M(color2), 0, sy - pw / 2);
      break;
    }
    case 'pillar': {
      add(CreateCylinder('pl', { diameter: sx, height: sy, tessellation: 12 }, scene), M(color), 0, sy / 2);
      add(CreateBox('cap', { width: sx * 1.4, height: sx * 0.3, depth: sx * 1.4 }, scene), M(color2), 0, sy);
      add(CreateBox('base', { width: sx * 1.4, height: sx * 0.3, depth: sx * 1.4 }, scene), M(color2), 0, sx * 0.15);
      break;
    }
    case 'lamp': {
      add(CreateCylinder('lp', { diameter: sx * 0.35, height: sy, tessellation: 6 }, scene), M(color2), 0, sy / 2);
      add(CreateSphere('lb', { diameter: sx * 1.6, segments: 8 }, scene), M(color, undefined, 0.8), 0, sy);
      break;
    }
    case 'flower': {
      add(CreateCylinder('st', { diameter: sx * 0.08, height: sy * 0.75, tessellation: 5 }, scene), M('#6aa874'), 0, sy * 0.375);
      for (let i = 0; i < 5; i++) { const a = i / 5 * Math.PI * 2; const p = add(CreateSphere('pt', { diameter: sx * 0.45, segments: 6 }, scene), M(color), Math.cos(a) * sx * 0.25, sy * 0.82, Math.sin(a) * sx * 0.25); p.scaling.y = 0.5; }
      add(CreateSphere('ct', { diameter: sx * 0.3, segments: 6 }, scene), M(color2), 0, sy * 0.85);
      break;
    }
    case 'heart': { const m = add(extrudeFlat('h', heartShape(), sz, scene), M(color, undefined, 0.2), 0, sy / 2); m.scaling.set(sx, sy, 1); break; }
    case 'star': { const m = add(extrudeFlat('s', starShape(5, 0.5, 0.22), sz, scene), M(color, undefined, 0.35), 0, sy / 2); m.scaling.set(sx, sy, 1); break; }
    case 'note': {
      const h = add(CreateSphere('nh', { diameter: sx * 0.55, segments: 8 }, scene), M(color), -sx * 0.15, sx * 0.25); h.scaling.set(1.3, 1, 0.6);
      add(CreateBox('ns', { width: sx * 0.08, height: sy * 0.85, depth: sz * 0.4 }, scene), M(color), sx * 0.1, sy * 0.5);
      add(CreateBox('nf', { width: sx * 0.4, height: sy * 0.12, depth: sz * 0.4 }, scene), M(color), sx * 0.28, sy * 0.88).rotation.z = -0.5;
      break;
    }
    case 'bubble': {
      add(CreateSphere('bb', { diameter: 1, segments: 16 }, scene), M(color, 0.35, 0.4), 0, sy / 2).scaling.set(sx, sy, sz);
      add(CreateSphere('hl', { diameter: sx * 0.18, segments: 6 }, scene), M('#ffffff', 0.9, 1), -sx * 0.22, sy * 0.72, -sz * 0.3);
      break;
    }
    case 'rock': { const m = add(CreateIcoSphere('rk', { radius: 0.5, subdivisions: 1, flat: true }, scene), M(color), 0, sy * 0.4); m.scaling.set(sx, sy, sz); m.rotation.y = (sx * 7.3) % 3; break; }
    case 'crystal': { const m = add(CreatePolyhedron('cr', { type: 1, size: 0.5 }, scene), M(color, 0.85, 0.5), 0, sy / 2); m.scaling.set(sx, sy, sz); break; }
    case 'moon': case 'sun': {
      add(CreateSphere('mn', { diameter: sx, segments: 20 }, scene), M(color, undefined, 0.9), 0, sy / 2);
      if (kind === 'sun') add(CreateTorus('hal', { diameter: sx * 1.5, thickness: sx * 0.05, tessellation: 40 }, scene), M(color2, 0.6, 0.9), 0, sy / 2).rotation.x = Math.PI / 2;
      break;
    }
    case 'bridge': {
      add(CreateBox('dk', { width: sx, height: sy * 0.25, depth: sz }, scene), M(color), 0, -sy * 0.125);
      for (const s of [-1, 1]) {
        add(CreateBox('rl', { width: 0.12, height: 0.12, depth: sz }, scene), M(color2), s * sx / 2, sy);
        for (let z = -sz / 2; z <= sz / 2 + 0.01; z += 2) add(CreateBox('pst', { width: 0.12, height: sy, depth: 0.12 }, scene), M(color2), s * sx / 2, sy / 2, z);
      }
      break;
    }
    case 'stairs': { const n = Math.max(3, Math.round(sy / 0.5)); for (let i = 0; i < n; i++) add(CreateBox('st', { width: sx, height: sy / n * (i + 1), depth: sz / n }, scene), M(i % 2 ? color : color2), 0, sy / n * (i + 1) / 2, -sz / 2 + sz / n * (i + 0.5)); break; }
    case 'cassette': {
      add(CreateBox('cb', { width: sx, height: sy, depth: sz }, scene), M(color), 0, sy / 2);
      add(CreateBox('lbl', { width: sx * 0.8, height: sy * 0.45, depth: sz * 1.02 }, scene), M(color2), 0, sy * 0.62);
      for (const s of [-1, 1]) add(CreateCylinder('rl', { diameter: sy * 0.32, height: sz * 1.05, tessellation: 12 }, scene), M('#333333'), s * sx * 0.22, sy * 0.55).rotation.x = Math.PI / 2;
      break;
    }
    case 'phone': {
      add(CreateBox('ph', { width: sx, height: sy, depth: sz }, scene), M(color), 0, sy / 2);
      add(CreateBox('sc', { width: sx * 0.86, height: sy * 0.86, depth: sz * 1.05 }, scene), M(color2, undefined, 0.7), 0, sy / 2);
      break;
    }
    case 'bench': {
      add(CreateBox('seat', { width: sx, height: sy * 0.12, depth: sz }, scene), M(color), 0, sy * 0.5);
      add(CreateBox('back', { width: sx, height: sy * 0.5, depth: sz * 0.12 }, scene), M(color), 0, sy * 0.8, sz * 0.45);
      for (const s of [-1, 1]) add(CreateBox('leg', { width: 0.1, height: sy * 0.5, depth: sz }, scene), M(color2), s * sx * 0.42, sy * 0.25);
      break;
    }
    case 'image': {
      const im = o as SceneObject; const w = im.size?.[0] ?? 4, h = im.size?.[2] || im.size?.[1] || 4;
      const p = CreatePlane('img', { width: w, height: h, sideOrientation: Mesh.DOUBLESIDE }, scene);
      p.material = mats.textured(im.src ?? '', { alpha: im.alpha !== false });
      p.parent = node;
      if (im.mode === 'flat') { p.rotation.x = Math.PI / 2; p.position.y = 0.03; }
      else { p.position.y = h / 2; if (im.mode === 'billboard') p.billboardMode = Mesh.BILLBOARDMODE_Y; }
      break;
    }
    case 'text': { const p = textPlane(scene, (o as SceneObject).name ?? '', color, size); p.parent = node; p.position.y = 0.02; break; }
    case 'group': {
      for (const part of (o as SceneObject).parts ?? []) {
        const child = buildKind(scene, mats, part, node);
        const pos = part.pos ?? [0, 0, 0]; child.position.set(pos[0], pos[1], pos[2]);
        const r = part.rot ?? [0, 0, 0]; child.rotation.set(r[0] * Math.PI / 180, r[1] * Math.PI / 180, r[2] * Math.PI / 180);
      }
      break;
    }
    default: add(CreateBox('b', { width: sx, height: sy, depth: sz }, scene), M(color), 0, sy / 2);
  }
  const tex = (o as Part).texture;
  if (tex && kind !== 'image') { const m = mats.textured(tex, { alpha: false, emissive: 0.2 }); for (const c of node.getChildMeshes(true)) c.material = m; }
  return node;
}

export function shade(c: string, amt: number): string {
  const col = hex(c);
  const f = (v: number) => Math.max(0, Math.min(255, Math.round((amt < 0 ? v * (1 + amt) : v + (1 - v) * amt) * 255)));
  return '#' + [col.r, col.g, col.b].map(v => f(v).toString(16).padStart(2, '0')).join('');
}
