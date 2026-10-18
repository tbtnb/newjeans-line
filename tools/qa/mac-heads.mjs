// GPU (Metal) head-colour check: deterministic preview frames, several skins/times; prints head screen position for crops.
import { chromium } from 'playwright-core';
const [url, out, skins, ...ts] = process.argv.slice(2);
const b = await chromium.launch({ headless: true, executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', args: ['--use-angle=metal', '--enable-gpu-rasterization', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'] });
const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 }); const errs = []; p.on('pageerror', e => errs.push(String(e)));
await p.goto(url); await p.waitForFunction(() => window.__nj && window.__nj.level, null, { timeout: 60000 }); await p.waitForTimeout(3000);
const gl = await p.evaluate(() => { const c = document.createElement('canvas').getContext('webgl2'); const d = c.getExtension('WEBGL_debug_renderer_info'); return d ? c.getParameter(d.UNMASKED_RENDERER_WEBGL) : 'n/a'; });
const res = [];
for (const sk of skins.split(',')) {
  await p.evaluate(s => window.__nj.world.setSkin(s), sk);
  for (const t of ts) {
    await p.evaluate(t => window.__nj.preview(+t), t); await p.waitForTimeout(1800);
    await p.evaluate(() => document.querySelector('#ready-hint')?.style.setProperty('display', 'none'));
    const pos = await p.evaluate(() => { const w = window.__nj.world, v = w.head.getAbsolutePosition(), m = w.scene.getTransformMatrix().m;
      const x = v.x*m[0]+v.y*m[4]+v.z*m[8]+m[12], y = v.x*m[1]+v.y*m[5]+v.z*m[9]+m[13], ww = v.x*m[3]+v.y*m[7]+v.z*m[11]+m[15];
      return { sx: Math.round((x/ww*0.5+0.5)*innerWidth), sy: Math.round((1-(y/ww*0.5+0.5))*innerHeight), heads: w.scene.meshes.filter(q => q.name === 'head').length, mat: w.head.material?.name }; });
    await p.screenshot({ path: `${out}/${sk}-t${t}.png` }); res.push({ sk, t, ...pos });
  }
}
console.log(JSON.stringify({ gl, errs, res })); await b.close();
