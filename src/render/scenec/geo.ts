/**
 * Tiny flat-shaded geometry builder for concept C placeholders (pure, no Babylon). Every triangle gets its own vertices with
 * a baked paper light (ambient + one sun + a little height AO), so unlit materials still read as folded paper.
 * Unit convention: y up, the prop stands on y=0, height ~1; the front faces +Z.
 */
export interface Geo { pos: number[]; col: number[]; idx: number[] }
const SUN = (() => { const v = [-0.45, 0.62, 0.65]; const l = Math.hypot(...v); return v.map(x => x / l); })();

export function geo(): Geo { return { pos: [], col: [], idx: [] }; }

export function tri(g: Geo, a: number[], b: number[], c: number[], shade: number) {
  const ux = b[0] - a[0], uy = b[1] - a[1], uz = b[2] - a[2], vx = c[0] - a[0], vy = c[1] - a[1], vz = c[2] - a[2];
  let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx; const l = Math.hypot(nx, ny, nz) || 1; nx /= l; ny /= l; nz /= l;
  // double-sided paper: light the side facing the sun
  const d = Math.abs(nx * SUN[0] + ny * SUN[1] + nz * SUN[2]);
  const i0 = g.pos.length / 3;
  for (const p of [a, b, c]) {
    const ao = 0.82 + 0.18 * Math.min(1, Math.max(0, p[1]));
    const k = Math.min(1, (0.74 + 0.3 * d) * ao) * shade;
    g.pos.push(p[0], p[1], p[2]); g.col.push(k, k, k, 1);
  }
  g.idx.push(i0, i0 + 1, i0 + 2);
}
export function quad(g: Geo, a: number[], b: number[], c: number[], d: number[], s: number) { tri(g, a, b, c, s); tri(g, a, c, d, s); }

export function box(g: Geo, cx: number, y0: number, cz: number, sx: number, sy: number, sz: number, s = 1) {
  const x0 = cx - sx / 2, x1 = cx + sx / 2, z0 = cz - sz / 2, z1 = cz + sz / 2, y1 = y0 + sy;
  quad(g, [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1], s); quad(g, [x1, y0, z0], [x0, y0, z0], [x0, y1, z0], [x1, y1, z0], s * 0.92);
  quad(g, [x1, y0, z1], [x1, y0, z0], [x1, y1, z0], [x1, y1, z1], s * 0.96); quad(g, [x0, y0, z0], [x0, y0, z1], [x0, y1, z1], [x0, y1, z0], s * 0.96);
  quad(g, [x0, y1, z1], [x1, y1, z1], [x1, y1, z0], [x0, y1, z0], s);
}
/** cylinder / cone (r1 bottom, r2 top), seg sides, no bottom cap */
export function cyl(g: Geo, cx: number, y0: number, cz: number, r1: number, r2: number, h: number, seg = 6, s = 1, cap = true) {
  for (let i = 0; i < seg; i++) {
    const a = i / seg * Math.PI * 2, b = (i + 1) / seg * Math.PI * 2;
    const p = (r: number, t: number, y: number) => [cx + Math.sin(t) * r, y, cz + Math.cos(t) * r];
    if (r2 > 0) quad(g, p(r1, a, y0), p(r1, b, y0), p(r2, b, y0 + h), p(r2, a, y0 + h), s); else tri(g, p(r1, a, y0), p(r1, b, y0), [cx, y0 + h, cz], s);
    if (cap && r2 > 0) tri(g, p(r2, a, y0 + h), p(r2, b, y0 + h), [cx, y0 + h, cz], s);
  }
}
/** squashed octahedron "blob" (pebbles, clouds, bunny bodies) */
export function blob(g: Geo, cx: number, cy: number, cz: number, rx: number, ry: number, rz: number, s = 1) {
  const seg = 6; const ring = (k: number, y: number, r: number) => [cx + Math.sin(k / seg * Math.PI * 2) * rx * r, cy + y * ry, cz + Math.cos(k / seg * Math.PI * 2) * rz * r];
  for (let i = 0; i < seg; i++) {
    const top = [cx, cy + ry, cz], bot = [cx, cy - ry, cz];
    tri(g, ring(i, 0.5, 0.87), ring(i + 1, 0.5, 0.87), top, s); tri(g, ring(i + 1, -0.5, 0.87), ring(i, -0.5, 0.87), bot, s * 0.9);
    quad(g, ring(i, -0.5, 0.87), ring(i + 1, -0.5, 0.87), ring(i + 1, 0.5, 0.87), ring(i, 0.5, 0.87), s);
  }
}
/** upright card from an outline in the XY plane (fan triangulated; convex-ish outlines), at depth z */
export function card(g: Geo, pts: number[][], z = 0, s = 1, ox = 0, oy = 0) {
  const c = pts.reduce((a, p) => [a[0] + p[0] / pts.length, a[1] + p[1] / pts.length], [0, 0]);
  for (let i = 0; i < pts.length; i++) { const p = pts[i], q = pts[(i + 1) % pts.length]; tri(g, [ox + c[0], oy + c[1], z], [ox + p[0], oy + p[1], z], [ox + q[0], oy + q[1], z], s); }
}
/** flat card lying in XZ at height y */
export function flat(g: Geo, pts: number[][], y: number, s = 1) {
  const c = pts.reduce((a, p) => [a[0] + p[0] / pts.length, a[1] + p[1] / pts.length], [0, 0]);
  for (let i = 0; i < pts.length; i++) { const p = pts[i], q = pts[(i + 1) % pts.length]; tri(g, [c[0], y, c[1]], [p[0], y, p[1]], [q[0], y, q[1]], s); }
}
export const star = (r: number, n = 5, k = 0.45) => Array.from({ length: n * 2 }, (_, i) => { const a = i / (n * 2) * Math.PI * 2; const rr = i % 2 ? r * k : r; return [Math.sin(a) * rr, Math.cos(a) * rr]; });
export const heart = (r: number) => Array.from({ length: 12 }, (_, i) => { const t = i / 12 * Math.PI * 2; return [r * 0.06 * 16 * Math.pow(Math.sin(t), 3), r * 0.06 * (13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t))]; });
const ngon = (r: number, n: number, ry = r) => Array.from({ length: n }, (_, i) => [Math.sin(i / n * Math.PI * 2) * r, Math.cos(i / n * Math.PI * 2) * ry]);

/** placeholder by shape; returns unit-height geometry (y 0..~1) */
export function placeholder(shape: string): Geo {
  const g = geo();
  switch (shape) {
    case 'tuft': for (let i = 0; i < 3; i++) { const a = i * 2.1; tri(g, [Math.sin(a) * 0.12, 0, Math.cos(a) * 0.12], [Math.sin(a + 0.5) * 0.12, 0, Math.cos(a + 0.5) * 0.12], [Math.sin(a) * 0.3, 1, Math.cos(a) * 0.3], 1); } break;
    case 'flower': tri(g, [-0.03, 0, 0], [0.03, 0, 0], [0, 0.75, 0], 0.8); card(g, star(0.35, 5, 0.6), 0, 1, 0, 0.75); break;
    case 'ico': blob(g, 0, 0.5, 0, 0.8, 0.5, 0.65); break;
    case 'mushroom': cyl(g, 0, 0, 0, 0.12, 0.1, 0.55, 5, 0.95); cyl(g, 0, 0.5, 0, 0.45, 0, 0.5, 6, 1); break;
    case 'tree': cyl(g, 0, 0, 0, 0.07, 0.06, 0.3, 4, 0.7); cyl(g, 0, 0.25, 0, 0.36, 0, 0.45, 6); cyl(g, 0, 0.55, 0, 0.27, 0, 0.45, 6); break;
    case 'bunny': blob(g, 0, 0.28, 0, 0.26, 0.28, 0.22); blob(g, 0, 0.66, 0.02, 0.18, 0.16, 0.16); box(g, -0.07, 0.78, 0, 0.06, 0.24, 0.03); box(g, 0.07, 0.78, 0, 0.06, 0.24, 0.03); break;
    case 'card': card(g, [[-0.6, 0], [-0.35, 0.55], [-0.1, 0.8], [0.15, 1], [0.4, 0.6], [0.6, 0]]); break;
    case 'book': box(g, 0, 0, 0, 1.4, 0.08, 1, 0.95); for (const sx of [-1, 1]) quad(g, [0, 0.08, -0.5], [0, 0.08, 0.5], [sx * 0.62, 1, 0.5], [sx * 0.62, 1, -0.5], 1); break;
    case 'star': card(g, star(0.5), 0, 1, 0, 0.5); break;
    case 'far': card(g, [[-2, 0], [-1.6, 0.55], [-1.1, 0.35], [-0.5, 1], [0.2, 0.5], [0.8, 0.85], [1.4, 0.3], [2, 0]]); break;
    case 'bird': tri(g, [0, 0.5, 0.2], [-0.5, 0.65, 0], [0, 0.5, -0.2], 1); tri(g, [0, 0.5, 0.2], [0, 0.5, -0.2], [0.5, 0.65, 0], 1); break;
    case 'box': box(g, 0, 0, 0, 0.9, 0.9, 0.9); break;
    case 'house': box(g, 0, 0, 0, 0.8, 0.55, 0.7); cyl(g, 0, 0.55, 0, 0.62, 0, 0.45, 4, 0.9); break;
    case 'tower': cyl(g, 0, 0, 0, 0.16, 0.13, 0.78, 6); cyl(g, 0, 0.78, 0, 0.21, 0, 0.22, 6, 0.9); break;
    case 'castle': box(g, 0, 0, 0, 0.9, 0.4, 0.4); box(g, 0, 0, -0.1, 0.36, 0.7, 0.3, 0.95); for (const x of [-0.45, 0.45]) { cyl(g, x, 0, 0.1, 0.1, 0.1, 0.6, 6); cyl(g, x, 0.6, 0.1, 0.13, 0, 0.2, 6, 0.9); } cyl(g, 0, 0.7, -0.1, 0.17, 0, 0.3, 6, 0.9); break;
    case 'arch': box(g, -0.4, 0, 0, 0.12, 0.8, 0.12); box(g, 0.4, 0, 0, 0.12, 0.8, 0.12); card(g, heart(0.35), 0, 1, 0, 0.82); break;
    case 'balloons': for (const [x, y] of [[-0.15, 0.8], [0.15, 0.85], [0, 0.65]]) { blob(g, x, y, 0, 0.12, 0.15, 0.12); tri(g, [x, y - 0.15, 0], [x + 0.01, y - 0.15, 0], [0, 0, 0], 0.8); } break;
    case 'bed': box(g, 0, 0.15, 0, 0.6, 0.18, 1); box(g, 0, 0, -0.48, 0.6, 0.6, 0.06, 0.95); box(g, 0, 0.33, -0.35, 0.4, 0.08, 0.2); break;
    case 'boat': quad(g, [-0.5, 0.25, 0], [0.5, 0.25, 0], [0.35, 0, 0.15], [-0.35, 0, 0.15], 1); quad(g, [0.5, 0.25, 0], [-0.5, 0.25, 0], [-0.35, 0, -0.15], [0.35, 0, -0.15], 0.95); card(g, [[0, 0.25], [0, 1], [0.35, 0.3]], 0); break;
    case 'carousel': cyl(g, 0, 0, 0, 0.5, 0.5, 0.08, 8); for (let i = 0; i < 6; i++) { const a = i / 6 * Math.PI * 2; box(g, Math.sin(a) * 0.4, 0.08, Math.cos(a) * 0.4, 0.03, 0.62, 0.03, 0.9); } cyl(g, 0, 0.7, 0, 0.55, 0, 0.3, 8, 0.95); break;
    case 'cloud': blob(g, -0.25, 0.4, 0, 0.3, 0.2, 0.2); blob(g, 0.15, 0.45, 0, 0.35, 0.25, 0.22); blob(g, 0.45, 0.38, 0, 0.2, 0.15, 0.15); break;
    case 'cyl': cyl(g, 0, 0, 0, 0.35, 0.35, 1, 8); break;
    case 'moon': card(g, ngon(0.45, 10), 0, 1, 0, 0.5); break;
    case 'pole': cyl(g, 0, 0, 0, 0.04, 0.03, 0.9, 4, 0.85); box(g, 0, 0.85, 0, 0.18, 0.15, 0.18); break;
    case 'wheel': { const n = 12; for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2, b = (i + 1) / n * Math.PI * 2; quad(g, [Math.sin(a) * 0.45, 0.52 + Math.cos(a) * 0.45, 0], [Math.sin(b) * 0.45, 0.52 + Math.cos(b) * 0.45, 0], [Math.sin(b) * 0.4, 0.52 + Math.cos(b) * 0.4, 0], [Math.sin(a) * 0.4, 0.52 + Math.cos(a) * 0.4, 0], 1); box(g, Math.sin(a) * 0.45, 0.47 + Math.cos(a) * 0.45, 0, 0.07, 0.07, 0.07, 0.95); } quad(g, [-0.2, 0, 0.05], [-0.17, 0, 0.05], [0, 0.52, 0.05], [-0.03, 0.52, 0.05], 0.9); quad(g, [0.17, 0, 0.05], [0.2, 0, 0.05], [0.03, 0.52, 0.05], [0, 0.52, 0.05], 0.9); break; }
    default: box(g, 0, 0, 0, 0.7, 1, 0.7);
  }
  return g;
}
export const triCount = (g: Geo) => g.idx.length / 3;
