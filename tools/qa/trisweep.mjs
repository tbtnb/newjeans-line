// v11: tris sweep over the whole song (scenec stats per second) -> per-zone max; usage: node tools/qa/trisweep.mjs <url> [--q high|low] [--step 1]
import { chromium } from '@playwright/test';
const a = process.argv.slice(2), url = a[0]; const opt = k => { const i = a.indexOf(k); return i < 0 ? null : a[i + 1]; };
const q = opt('--q') ?? 'high', step = +(opt('--step') ?? 1);
const br = await chromium.launch({ headless: true, executablePath: '/usr/bin/google-chrome', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--headless=new'] });
const page = await (await br.newContext({ viewport: { width: 540, height: 960 } })).newPage();
await page.goto(url); await page.waitForFunction(() => window.__nj, null, { timeout: 120000 });
await page.evaluate(async () => { for (let i = 0; i < 8; i++) { await window.__nj.selectLevel(i); if (window.__nj.level?.id === 'omg') return; } });
await page.waitForFunction(() => window.__nj.level && window.__nj.audio.ready, null, { timeout: 120000 });
await page.evaluate(q => window.__nj.world.setQuality(q), q);
const r = await page.evaluate(async step => { const n = window.__nj, w = n.world, Z = n.level.layout.scenec.zones, out = {};
  for (let T = 0.5; T < Z[Z.length - 1].t1; T += step) { n.preview(T); w.frame(T); w.frame(T); await new Promise(r => requestAnimationFrame(r)); const s = w.stats().scenec, z = Z.find(z => T >= z.t0 && T < z.t1)?.id ?? 'end';
    if (!out[z] || s.tris > out[z][0]) out[z] = [s.tris, +T.toFixed(1)]; } return out; }, step);
for (const [z, [t, T]] of Object.entries(r)) console.log(z, t, '@', T); await br.close();
