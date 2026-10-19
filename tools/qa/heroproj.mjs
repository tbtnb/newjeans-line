// v10 hero framing probe: for every hero / landmark set piece, sweep song time and project its bbox through the key camera.
// Prints per piece the best moment (largest on-screen height while fully in frame) and the frame fraction / position.
// usage: node tools/qa/heroproj.mjs <url> [--gpu] [--min 6]
import { chromium } from '@playwright/test';
const a = process.argv.slice(2), url = a[0], gpu = a.includes('--gpu'); const mi = a.indexOf('--min'), minH = mi < 0 ? 6 : +a[mi + 1];
const exe = process.platform === 'darwin' ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' : '/usr/bin/google-chrome';
const flags = gpu ? ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'] : ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'];
const br = await chromium.launch({ headless: true, executablePath: exe, args: [...flags, '--headless=new'] });
const page = await (await br.newContext({ viewport: { width: 540, height: 960 } })).newPage();
await page.goto(url); await page.waitForFunction(() => window.__nj, null, { timeout: 120000 });
await page.evaluate(async () => { for (let i = 0; i < 8; i++) { await window.__nj.selectLevel(i); if (window.__nj.level?.id === 'omg') return; } });
await page.waitForFunction(() => window.__nj.level && window.__nj.audio.ready, null, { timeout: 120000 });
const res = await page.evaluate(async minH => {
  const n = window.__nj, w = n.world, sc = w.sc, spec = n.level.layout.scenec, out = [];
  const S = sc.plc.sets.filter(e => e.hero || (spec.assets[e.a]?.h ?? 0) * e.s >= minH);
  for (const e of S) {
    const A = spec.assets[e.a], H = A.h * e.s, R = (A.w ?? A.h * 0.6) * e.s / 2; let best = null; const tr = [];
    for (let T = Math.max(0.3, e.t - 8); T <= e.t + 1.5; T += 0.5) {
      n.preview(T); w.frame(T); const cam = w.rig.cam; cam.computeWorldMatrix(true); const V = cam.getViewMatrix(true).m, P = cam.getProjectionMatrix(true).m;
      let x0 = 9, x1 = -9, y0 = 9, y1 = -9, behind = false;
      for (const [dx, dz] of [[-R, -R], [R, -R], [R, R], [-R, R]]) for (const dy of [0, H]) {
        const p = [e.x + dx, e.y + dy, e.z + dz, 1]; const v = [0, 1, 2, 3].map(j => p[0] * V[j] + p[1] * V[4 + j] + p[2] * V[8 + j] + p[3] * V[12 + j]);
        const c = [0, 1, 2, 3].map(j => v[0] * P[j] + v[1] * P[4 + j] + v[2] * P[8 + j] + v[3] * P[12 + j]); if (c[3] <= 0) { behind = true; continue; }
        const sx = c[0] / c[3] * 0.5 + 0.5, sy = 0.5 - c[1] / c[3] * 0.5; x0 = Math.min(x0, sx); x1 = Math.max(x1, sx); y0 = Math.min(y0, sy); y1 = Math.max(y1, sy); }
      if (behind) continue;
      const vis = Math.max(0, Math.min(1, x1) - Math.max(0, x0)) * Math.max(0, Math.min(1, y1) - Math.max(0, y0)) / Math.max(1e-6, (x1 - x0) * (y1 - y0));
      const hgt = Math.max(0, Math.min(1, y1) - Math.max(0, y0)); const score = hgt * (vis > 0.85 ? 1 : vis);
      tr.push([T, +hgt.toFixed(2), +vis.toFixed(2)]);
      if (!best || score > best.score) best = { T, score: +score.toFixed(2), hgt: +hgt.toFixed(2), vis: +vis.toFixed(2), cx: +((x0 + x1) / 2).toFixed(2), top: +y0.toFixed(2), bot: +y1.toFixed(2) };
    }
    out.push({ a: e.a, t: e.t, hero: !!e.hero, H: +H.toFixed(1), best, tr });
  }
  return out;
}, minH);
for (const r of res) console.log(`${r.a.padEnd(16)} t=${r.t} ${r.hero ? 'HERO' : '    '} H=${r.H} best=${JSON.stringify(r.best)}`);
await br.close();
