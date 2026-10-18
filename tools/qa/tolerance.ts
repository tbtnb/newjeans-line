// Effective tap tolerance per level: the judgment window (early = late = window; a tap with |err| <= window survives).
// usage: npx tsx tools/qa/tolerance.ts [slug]   (reads src/levels/<slug>.json built by tools/build-levels.mjs)
import { readFileSync } from 'node:fs';
import { Game, PERFECT } from '../../src/core/game';
const slug = process.argv[2] ?? 'omg';
const L = JSON.parse(readFileSync(`src/levels/${slug}.json`, 'utf8'));
const g = new Game(L); const w = [...g.windows].map(x => x * 1000).sort((a, b) => a - b);
const q = (p: number) => w[Math.min(w.length - 1, Math.floor(p * w.length))];
const at = (ms: number) => (100 * w.filter(x => x >= ms - 1e-6).length / w.length).toFixed(0) + '%';
const widths = (L.layout.road.width as { t: number; w: number }[]).map(x => x.w);
console.log(JSON.stringify({ slug, taps: w.length, roadWidth: widths, perfectMs: PERFECT * 1000, windowMs: { min: +q(0).toFixed(1), p10: +q(0.1).toFixed(1), median: +q(0.5).toFixed(1), max: +w[w.length - 1].toFixed(1) }, share_ge_100ms: at(100), share_ge_120ms: at(120) }));
