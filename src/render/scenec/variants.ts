/** v8 repetition pass: per-instance palette variants for the mass decor (merged chunk meshes only, so free in draws).
 * Each variant is a list of [sheet hex -> sheet hex] swaps; colours are matched by chroma direction (the baked paper light
 * scales the sRGB hex uniformly), so every lit / folded shade of a part follows its swap. Variant 0 is always the sheet. */
type Swap = [string, string];
const C = { coral: '#FF7A6B', pink: '#FF6FAE', magenta: '#FF4FA0', lavender: '#B9A6F0', lilac: '#E3D7FA', mint: '#BDEBD8', cyan: '#7FE0E8', moon: '#BFD4F5',
  sun: '#FFD23F', gold: '#F7D98B', blush: '#FFC7DA', teal: '#173A4A', cream: '#FFF3DE', green: '#6CCB5F', pearl: '#F3F1EA' };
const house: Swap[][] = [[], [[C.coral, C.pink]], [[C.coral, C.lavender], [C.sun, C.gold]], [[C.coral, C.cyan], [C.cream, C.pearl]], [[C.coral, C.magenta], [C.cream, C.blush]], [[C.coral, '#8FD3A6']]];
export const VARIANTS: Record<string, Swap[][]> = {
  'mushroom-house': house, 'bunny-house': house,
  'mushroom-group': [[], [[C.coral, C.pink]], [[C.coral, C.lavender]], [[C.coral, C.sun]]],
  'tulip-bed': [[], [[C.coral, C.pink]], [[C.coral, C.lavender], [C.sun, C.blush]], [[C.sun, '#FFFFFF']], [[C.coral, C.magenta]]],
  'heart-bed': [[], [[C.coral, C.lavender], [C.lavender, C.coral]], [[C.pink, C.sun], [C.coral, C.blush]], [[C.coral, C.cyan], [C.pink, C.lavender]]],
  balloons: [[], [[C.magenta, C.lavender], [C.cyan, C.mint]], [[C.magenta, C.sun], [C.pink, C.coral]], [[C.cyan, C.pink], [C.magenta, C.cyan]]],
  gift: [[], [[C.lavender, C.mint], [C.pink, C.coral]], [[C.lavender, C.pink], [C.pink, C.lavender]], [[C.lavender, C.cyan], [C.pink, C.magenta]], [[C.lavender, C.blush]]],
  'book-stack': [[], [[C.teal, C.lavender]], [[C.teal, C.coral], ['#C99A6B', C.gold]], [[C.teal, C.pink]], [[C.teal, '#2F6E73']]],
  bunting: [[], [[C.magenta, C.cyan], [C.cyan, C.magenta]], [[C.magenta, C.lavender], [C.cyan, C.mint]], [[C.cyan, C.sun]]],
  'pine-lo': [[], [[C.teal, '#21535A']], [[C.teal, '#2A4466']], [[C.mint, C.green]]],
  'tree-lo': [[], [[C.mint, C.green]], [[C.mint, C.blush], [C.green, C.pink]], [[C.mint, '#9FDCC2']], [[C.mint, C.sun]]],
  'firefly-lamp': [[], [[C.teal, '#2A4466']], [[C.teal, C.lavender], [C.gold, C.blush]], [[C.gold, C.mint]]],
  'lily-lamp': [[], [[C.blush, C.lilac]], [[C.blush, C.mint], [C.mint, C.blush]], [[C.blush, C.moon]]],
  'heart-sculpt': [[], [[C.pink, C.lavender]], [[C.pink, C.coral]], [[C.pink, C.cyan]]],
  'bunny-statue': [[], [[C.blush, C.lilac]], [[C.blush, C.mint], [C.mint, C.blush]], [[C.pearl, C.cream], [C.blush, C.sun]]],
  'pull-tab': [[], [[C.coral, C.pink]], [[C.coral, C.lavender]], [[C.coral, C.cyan]]],
  'flower-heart': [[], [[C.pink, C.lavender]], [[C.pink, C.sun]], [[C.pink, C.coral]]],
  'paper-boat': [[], [[C.lilac, C.blush]], [[C.lilac, C.mint], [C.moon, C.lilac]]],
  'forest-clump': [[], [[C.mint, C.blush]], [[C.green, '#8FD3A6']]],
  'paper-hill-lo': [[], [[C.mint, '#CBE9C4']], [[C.mint, '#C9E4F0']]],
  // repeated set pieces (z02 village: 4 windmills, 3 houses) step through these in placement order
  windmill: [[], [[C.coral, C.pink]], [[C.coral, C.lavender], [C.sun, C.gold]], [[C.coral, C.cyan]]],
  'ward-bed': [[], [[C.pink, C.lavender]], [[C.pink, C.cyan]]],
  'iv-heart': [[], [[C.pink, C.lavender]]],
  'flip-phone': [[], [[C.pink, C.lavender]], [[C.pink, C.cyan]]],
  'cord-arch': [[], [[C.pink, C.lavender]]],
  'star-chime': [[], [[C.gold, C.moon]]],
  'paper-boat-set': [],
};
for (const [a, b] of [['tree-bush-lo', 'tree-lo'], ['tree-bush', 'tree-lo'], ['tree', 'tree-lo'], ['pine', 'pine-lo']] as const) VARIANTS[a] = VARIANTS[b];
delete VARIANTS['paper-boat-set'];
/** stretched per instance (height 0.88-1.18) so rows of one kind never share a roofline */
export const STRETCH = new Set(['mushroom-house', 'bunny-house', 'pine-lo', 'tree-lo', 'tree', 'pine', 'forest-clump', 'lily-lamp', 'book-stack', 'mushroom-group', 'balloons']);

const rgb = (h: string) => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16) / 255);
const dir = (c: number[]) => { const m = Math.max(c[0], c[1], c[2], 1e-4); return [c[0] / m, c[1] / m, c[2] / m, m]; };
const cache = new Map<string, Float32Array | number[]>();
export function nVariants(a: string) { return VARIANTS[a]?.length ?? 1; }
export function variantCols(a: string, col: Float32Array | number[], v: number, cached = true): Float32Array | number[] {
  const L = VARIANTS[a]; if (!L || L.length < 2) return col; const k = ((v % L.length) + L.length) % L.length; if (k === 0) return col;
  const key = a + ':' + k; const hit = cached ? cache.get(key) : undefined; if (hit && hit.length === col.length) return hit;
  const sw = L[k].map(([f, t]) => { const F = dir(rgb(f)), T = rgb(t); return { F, T }; });
  const out = new Float32Array(col.length);
  for (let i = 0; i < col.length; i += 4) {
    const d = dir([col[i], col[i + 1], col[i + 2]]); let done = false;
    for (const { F, T } of sw) { const e = Math.abs(d[0] - F[0]) + Math.abs(d[1] - F[1]) + Math.abs(d[2] - F[2]); if (e < 0.09) { const kk = d[3] / F[3]; out[i] = T[0] * kk; out[i + 1] = T[1] * kk; out[i + 2] = T[2] * kk; done = true; break; } }
    if (!done) { out[i] = col[i]; out[i + 1] = col[i + 1]; out[i + 2] = col[i + 2]; } out[i + 3] = col[i + 3] ?? 1;
  }
  if (cached) cache.set(key, out); return out;
}
