// Repetition audit: at each zone's key-camera probe (same T as zshots / perf-c --hero), which placed assets are actually in frame.
// Counts only what is built at that moment (active chunk range, set pieces switched on). Reports per zone: visible items, distinct assets (mid+sets, ground, cards), top-asset share, and clone pairs (a visible piece >= 0.8 m tall
// whose nearest visible neighbour within 7 m is the same asset AND the same palette variant; fences excluded).
// usage: node tools/qa/repcount.mjs <url> <out.json> [--z z05,z09]
import { chromium } from '@playwright/test';
import { writeFileSync } from 'node:fs';
const a = process.argv.slice(2), url = a[0], out = a[1]; const opt = k => { const i = a.indexOf(k); return i < 0 ? null : a[i + 1]; }; const only = opt('--z')?.split(',');
const br = await chromium.launch({ headless: true, executablePath: '/usr/bin/google-chrome', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--headless=new'] });
const page = await (await br.newContext({ viewport: { width: 540, height: 960 } })).newPage();
await page.goto(url); await page.waitForFunction(() => window.__nj, null, { timeout: 120000 });
await page.evaluate(async () => { for (let i = 0; i < 8; i++) { await window.__nj.selectLevel(i); if (window.__nj.level?.id === 'omg') return; } });
await page.waitForFunction(() => window.__nj.level && window.__nj.audio.ready && window.__nj.world.sc, null, { timeout: 120000 });
const hz = await page.evaluate(() => { const L = window.__nj.level.layout.scenec; return L.zones.map(z => { let b = null; for (const p of z.setpieces) { const tr = (L.assets[p.asset]?.tris ?? 0) + (p.hero ? 1e6 : 0); if (!b || tr > b.tr) b = { tr, t: p.t }; } return [z.id, b ? Math.max(0.3, b.t - 2.2) : (z.t0 + z.t1) / 2]; }); });
await page.evaluate(() => window.__nj.preview(1)); await page.waitForTimeout(8000);
const res = {};
for (const [id, T] of hz) {
  if (only && !only.includes(id)) continue;
  res[id] = await page.evaluate(async ([T, id]) => { const n = window.__nj, w = n.world; n.preview(T); for (let i = 0; i < 6; i++) { w.frame(T); await new Promise(r => requestAnimationFrame(r)); }
    const sc = w.sc, P = sc.plc, cam = w.scene.activeCamera, m = cam.getTransformationMatrix().m, A = sc.spec.assets, zi = sc.spec.zones.findIndex(z => z.id === id);
    const vis = (x, y, z) => { const X = x * m[0] + y * m[4] + z * m[8] + m[12], Y = x * m[1] + y * m[5] + z * m[9] + m[13], W = x * m[3] + y * m[7] + z * m[11] + m[15]; return W > 0 && Math.abs(X / W) < 1.02 && Math.abs(Y / W) < 1.02; };
    const V = [];
    const rg = sc.range ?? [0, P.chunks.length - 1]; for (const c of P.chunks.slice(rg[0], rg[1] + 1)) for (const it of c.items) { if (!(sc.keep ? sc.keep(it) : true)) continue; const h = (A[it.a]?.h ?? 1) * it.s; if (vis(it.x, it.y + h * 0.5, it.z) || vis(it.x, it.y + h, it.z)) V.push({ a: it.a, g: it.layer, x: it.x, z: it.z, h, v: sc.variantOf ? sc.variantOf(it) : 0 }); }
    for (const [si, s] of P.sets.entries()) { if (sc.sets && sc.sets[si] && !sc.sets[si].on) continue; const h = (A[s.a]?.h ?? 1) * s.s; if (vis(s.x, s.y + h * 0.5, s.z) || vis(s.x, s.y + h, s.z)) V.push({ a: s.a, g: 'set', x: s.x, z: s.z, h, v: 0 }); }
    for (const c of P.chunks) for (const im of c.imp ?? []) if (vis(im.x, im.y + im.s * 0.5, im.z)) V.push({ a: 'card:' + im.k, g: 'card', x: im.x, z: im.z, h: im.s, v: 0 });
    const cnt = g => { const o = {}; for (const e of V) if (g.includes(e.g)) o[e.a] = (o[e.a] ?? 0) + 1; return Object.entries(o).sort((p, q) => q[1] - p[1]); };
    const mid = cnt(['mid', 'set']), gr = cnt(['ground']), cards = cnt(['card']);
    const tall = V.filter(e => (e.g === 'mid' || e.g === 'set') && e.h >= 0.8 && !/fence|hedge|bunting|lantern-string|cord/.test(e.a)); let clones = 0;
    for (const e of tall) { let b = null, bd = 49; for (const f of tall) { if (f === e) continue; const d = (f.x - e.x) ** 2 + (f.z - e.z) ** 2; if (d < bd) { bd = d; b = f; } } if (b && b.a === e.a && b.v === e.v) clones++; }
    const looks = new Set(V.filter(e => e.g === 'mid' || e.g === 'set').map(e => e.a + '#' + e.v)).size;
    const nMid = mid.reduce((s, x) => s + x[1], 0);
    return { T: +T.toFixed(2), visible: V.length, distinctMid: mid.length, distinctLooks: looks, distinctGround: gr.length, distinctCards: cards.length, midItems: nMid, topShare: nMid ? +(mid[0][1] / nMid).toFixed(2) : 0, clonePairs: clones, tall: tall.length, mid: mid.slice(0, 12), ground: gr.slice(0, 6), cards: cards.slice(0, 6) };
  }, [T, id]);
  const r = res[id]; console.log(id, 'T', r.T, 'distinct mid/sets', r.distinctMid, 'looks', r.distinctLooks, 'ground', r.distinctGround, 'cards', r.distinctCards, '| mid items', r.midItems, 'top', r.mid[0]?.join(':'), r.topShare, '| clone pairs', r.clonePairs, '/', r.tall);
}
writeFileSync(out, JSON.stringify(res, null, 1)); await br.close();
