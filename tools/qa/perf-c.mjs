// OMG concept C perf harness (render-cost measurement, not gameplay; scripted simulation, not physical-device play).
// usage: node tools/qa/perf-c.mjs <url> [--gpu] [--shots dir] [--png] [--dpr 1] [--scale 1] [--q high|low]
//   box (default): headless Chrome, SwiftShader software GL;  --gpu: real GPU (Mac: ANGLE Metal, headed-new headless)
// Per probe time (zone centres + zone boundaries): draw calls, visible tris (active meshes x thin instances), active meshes,
// GPU-synced frame time (render + 1px readPixels, median of 30) and, during real playback, rAF frame-interval p50/p95.
import { chromium } from '@playwright/test';
import { mkdirSync } from 'node:fs';
const args = process.argv.slice(2); const url = args[0];
const opt = k => { const i = args.indexOf(k); return i < 0 ? null : args[i + 1] ?? true; };
const gpu = args.includes('--gpu'), shots = opt('--shots'), scale = +(opt('--scale') ?? 1), q = opt('--q') ?? 'high', dpr = +(opt('--dpr') ?? 1), png = args.includes('--png');
const exe = process.platform === 'darwin' ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' : '/usr/bin/google-chrome';
const flags = gpu ? (process.platform === 'darwin' ? ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'] : ['--enable-gpu', '--ignore-gpu-blocklist']) : ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'];
const browser = await chromium.launch({ headless: true, executablePath: exe, args: [...flags, '--autoplay-policy=no-user-gesture-required', '--headless=new'] });
const page = await (await browser.newContext({ viewport: { width: 540, height: 960 }, deviceScaleFactor: dpr, hasTouch: true })).newPage();
page.on('pageerror', e => console.error('pageerror', e.message)); page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.error('console', m.text()); });
await page.goto(url); await page.waitForFunction(() => window.__nj);
const idx = await page.evaluate(async () => { for (let i = 0; i < 8; i++) { await window.__nj.selectLevel(i); if (window.__nj.level?.id === 'omg') return i; } return -1; });
if (idx < 0) throw new Error('omg not found');
await page.waitForFunction(() => window.__nj.level && window.__nj.audio.ready, null, { timeout: 90000 });
const info = await page.evaluate(async ([q, scale]) => {
  const w = window.__nj.world; w.setQuality(q); w.engine.setHardwareScalingLevel(scale);
  const gl = w.engine._gl; return { renderer: gl.getParameter((gl.getExtension('WEBGL_debug_renderer_info') || {}).UNMASKED_RENDERER_WEBGL ?? gl.RENDERER), w: w.engine.getRenderWidth(), h: w.engine.getRenderHeight() };
}, [q, scale]);
console.log(JSON.stringify({ url, gpu, q, ...info }));
const zones = await page.evaluate(() => window.__nj.level.layout.scenec.zones.map(z => [z.id, z.t0, z.t1]));
const probes = []; for (const [id, t0, t1] of zones) { probes.push([id + '-in', Math.max(0.6, t0 + 0.4)]); probes.push([id + '-mid', (t0 + t1) / 2]); }
// --hero: one probe per zone ~1 s before the line reaches the zone's biggest set piece (popped, in frame like the key renders)
if (args.includes('--hero')) {
  const hz = await page.evaluate(() => { const L = window.__nj.level.layout.scenec; return L.zones.map(z => { let b = null; for (const p of z.setpieces) { const tr = L.assets[p.asset]?.tris ?? 0; if (!b || tr > b.tr) b = { t: p.t, tr, a: p.asset }; } return [z.id, b ? Math.max(z.t0 + 1.3, b.t - 1.0) : (z.t0 + z.t1) / 2, b?.a]; }); });
  for (const [id, T, a] of hz) { probes.push([id + '-hero', T]); console.log(JSON.stringify({ hero: id, T, asset: a })); }
}
// let the models stream in
await page.evaluate(() => window.__nj.preview(1)); await page.waitForTimeout(4000);
const rows = [];
for (const [name, T] of probes) {
  const r = await page.evaluate(async T => {
    const n = window.__nj, w = n.world, s = w.scene, gl = w.engine._gl, px = new Uint8Array(4);
    n.preview(T); for (let i = 0; i < 6; i++) { w.frame(T); await new Promise(r => requestAnimationFrame(r)); }
    const fr = () => { s.render(); gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px); };
    fr(); const dc0 = w.engine._drawCalls?.current ?? 0; fr(); const dc = (w.engine._drawCalls?.current ?? 0) - dc0; // counter is cumulative when rendering outside the engine loop
    let tris = 0; const act = s.getActiveMeshes(); for (let i = 0; i < act.length; i++) { const m = act.data[i]; const ix = m.getTotalIndices?.() ?? 0; tris += ix / 3 * (m.hasThinInstances ? m.thinInstanceCount : 1); }
    const ts = []; for (let i = 0; i < 30; i++) { const t0 = performance.now(); fr(); ts.push(performance.now() - t0); } ts.sort((a, b) => a - b);
    const st = w.stats();
    return { T: +T.toFixed(2), drawCalls: dc, tris: Math.round(tris), active: act.length, frameMs: +ts[15].toFixed(2), frameP90: +ts[27].toFixed(2), sc: st.scenec };
  }, T);
  rows.push({ name, ...r });
  console.log(JSON.stringify({ name, ...r, sc: r.sc && { chunks: r.sc.chunks, cm: r.sc.chunkMeshes, types: r.sc.types, inst: r.sc.instances, sets: r.sc.sets, models: r.sc.models, trisAtBudget: r.sc.trisAtBudget } }));
  if (shots) { mkdirSync(shots, { recursive: true }); await page.screenshot(png ? { path: `${shots}/${name}.png` } : { path: `${shots}/${name}.jpg`, quality: 70 }); }
}
// real playback frame intervals (rAF) for 6 s from the drop
const play = await page.evaluate(async () => {
  const n = window.__nj; n.preview(44); await new Promise(r => setTimeout(r, 300));
  const g = n.game; try { await n.audio.unlock?.(); } catch {}
  document.querySelector('canvas')?.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
  const iv = []; let last = performance.now(); const t0 = last; let maxDc = 0; let prevDc = n.world.engine._drawCalls?.current ?? 0;
  await new Promise(res => { const f = () => { const now = performance.now(); iv.push(now - last); last = now; const cur = n.world.engine._drawCalls?.current ?? 0; maxDc = Math.max(maxDc, cur - prevDc); prevDc = cur; if (now - t0 < 6000) requestAnimationFrame(f); else res(); }; requestAnimationFrame(f); });
  iv.sort((a, b) => a - b); return { state: n.state, frames: iv.length, p50: +iv[iv.length >> 1].toFixed(1), p95: +iv[Math.floor(iv.length * 0.95)].toFixed(1), maxDrawCalls: maxDc, fps: n.world.fps };
});
console.log(JSON.stringify({ play }));
const max = k => Math.max(...rows.map(r => r[k] ?? 0));
console.log(JSON.stringify({ summary: { maxDrawCalls: max('drawCalls'), maxTris: max('tris'), maxTrisAtBudget: Math.max(...rows.map(r => (r.tris - (r.sc?.tris ?? 0)) + (r.sc?.trisAtBudget ?? 0))), maxFrameMs: max('frameMs'), medianFrameMs: rows.map(r => r.frameMs).sort((a, b) => a - b)[rows.length >> 1] } }));
await browser.close();
