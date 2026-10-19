// Quick zone hero shots (box SwiftShader or Mac --gpu): same probe times as perf-c.mjs --hero. Scripted render, not gameplay.
// usage: node tools/qa/zshots.mjs <url> <outdir> [--gpu] [--q high|low] [--z z05,z09] [--dt 0] [--dpr 1]
import { chromium } from '@playwright/test';
import { mkdirSync } from 'node:fs';
const a = process.argv.slice(2), url = a[0], out = a[1]; const opt = k => { const i = a.indexOf(k); return i < 0 ? null : a[i + 1]; };
const gpu = a.includes('--gpu'), q = opt('--q') ?? 'high', only = opt('--z')?.split(','), dt = +(opt('--dt') ?? 0), dpr = +(opt('--dpr') ?? 1);
const exe = process.platform === 'darwin' ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' : '/usr/bin/google-chrome';
const flags = gpu ? ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'] : ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'];
const br = await chromium.launch({ headless: true, executablePath: exe, args: [...flags, '--autoplay-policy=no-user-gesture-required', '--headless=new'] });
const page = await (await br.newContext({ viewport: { width: 540, height: 960 }, deviceScaleFactor: dpr })).newPage();
page.on('pageerror', e => console.error('pageerror', e.message));
await page.goto(url); await page.waitForFunction(() => window.__nj, null, { timeout: 120000 });
await page.evaluate(async () => { for (let i = 0; i < 8; i++) { await window.__nj.selectLevel(i); if (window.__nj.level?.id === 'omg') return; } });
await page.waitForFunction(() => window.__nj.level && window.__nj.audio.ready, null, { timeout: 120000 });
await page.evaluate(q => window.__nj.world.setQuality(q), q);
const at = opt('--at'); const hz = at === 'in' ? await page.evaluate(() => window.__nj.level.layout.scenec.zones.map(z => { const L = z.t1 - z.t0; return [z.id, Math.max(0.3, z.t0 - 0.8)]; })) : await page.evaluate(() => { const L = window.__nj.level.layout.scenec; return L.zones.map(z => { let b = null; for (const p of z.setpieces) { const tr = (L.assets[p.asset]?.tris ?? 0) + (p.hero ? 1e6 : 0); if (!b || tr > b.tr) b = { t: p.t, tr }; } return [z.id, b ? Math.max(z.t0 + 1.3, b.t - 2.2) : (z.t0 + z.t1) / 2]; }); });
await page.evaluate(() => window.__nj.preview(1)); await page.waitForTimeout(gpu ? 4000 : 15000);
mkdirSync(out, { recursive: true });
for (const [id, T0] of hz) {
  if (only && !only.includes(id)) continue; const T = T0 + dt;
  const st = await page.evaluate(async T => { const n = window.__nj, w = n.world; n.preview(T); for (let i = 0; i < 6; i++) { w.frame(T); await new Promise(r => requestAnimationFrame(r)); } return w.stats().scenec; }, T);
  await page.waitForTimeout(gpu ? 300 : 1500);
  await page.screenshot({ path: `${out}/${id}.png` }); console.log(id, T.toFixed(2), JSON.stringify(st && { tris: st.tris, sets: st.sets, inst: st.instances }));
}
await br.close();
