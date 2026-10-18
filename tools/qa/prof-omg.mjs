// Render-cost profiler (box, software GL): times scene.render() with feature groups toggled. Not gameplay.
import { chromium } from '@playwright/test';
const url = process.argv[2], T = +(process.argv[3] ?? 30);
const browser = await chromium.launch({ headless: true, executablePath: '/usr/bin/google-chrome', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required'] });
const ctx = await browser.newContext({ viewport: { width: 540, height: 960 }, hasTouch: true });
const page = await ctx.newPage();
await page.goto(url); await page.waitForFunction(() => window.__nj);
await page.evaluate(() => window.__nj.selectLevel(4));
await page.waitForFunction(() => window.__nj.level && window.__nj.audio.ready, null, { timeout: 60000 });
const r = await page.evaluate(async T => {
  const w = window.__nj.world; w.setQuality('high'); w.engine.setHardwareScalingLevel(1.5);
  window.__nj.preview(T); await new Promise(r => setTimeout(r, 1500));
  const s = w.scene; const gl = w.engine._gl; const px = new Uint8Array(4); const fr = () => { s.render(); gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px); };
  const time = n => { fr(); const t0 = performance.now(); for (let i = 0; i < n; i++) fr(); return +((performance.now() - t0) / n).toFixed(1); };
  const out = { meshes: s.meshes.length, active: (s.render(), s.getActiveMeshes().length), mats: s.materials.length, tex: s.textures.length, ps: s.particleSystems.length, layers: s.effectLayers?.length };
  out.all = time(8);
  const groups = {
    objects: s.meshes.filter(m => /^(obj|art|lm)/i.test(m.name) || (w.objects || []).some(o => m.isDescendantOf?.(o.node))),
    dressing: s.meshes.filter(m => /dress/i.test(m.name)),
    ground: w.ground ? [w.ground] : [],
    fx: s.meshes.filter(m => /^fx/i.test(m.name)),
    beams: s.meshes.filter(m => /^fxBeam/i.test(m.name)),
    trims: s.meshes.filter(m => /^fxTrim/i.test(m.name)),
  };
  for (const [k, ms] of Object.entries(groups)) { ms.forEach(m => m.setEnabled(false)); out['no_' + k + '(' + ms.length + ')'] = time(8); ms.forEach(m => m.setEnabled(true)); }
  const ps = s.particleSystems.slice(); ps.forEach(p => p.stop()); s.particlesEnabled = false; out.no_particles = time(8); s.particlesEnabled = true;
  const gls = s.effectLayers?.slice() || []; gls.forEach(g => g.isEnabled = false); out.no_glow = time(8); s.meshes.filter(m => /^fxBeam/i.test(m.name)).forEach(m => m.setEnabled(false)); out.no_glow_beams = time(8); s.meshes.filter(m => /^fxBeam/i.test(m.name)).forEach(m => m.setEnabled(true)); gls.forEach(g => g.isEnabled = true);
  s.shadowsEnabled = false; out.no_shadows = time(8); s.shadowsEnabled = true;
  s.imageProcessingConfiguration.isEnabled = false; out.no_ip = time(8); s.imageProcessingConfiguration.isEnabled = true;
  const tr = s.getMeshByName('fxTrim'); const rt = s.getMeshByName('roadTop'); const rb = s.getMeshByName('roadBody');
  out.N = rt?.thinInstanceCount; out.trimCount = tr?.thinInstanceCount;
  gls.forEach(g => g.isEnabled = false); if (tr) tr.setEnabled(false); out.no_glow_trim = time(8); if (tr) tr.setEnabled(true); gls.forEach(g => g.isEnabled = true);
  if (rt) { rt.setEnabled(false); out.no_roadTop = time(8); rt.setEnabled(true); }
  if (rb) { rb.setEnabled(false); out.no_roadBody = time(8); rb.setEnabled(true); }
  if (tr) { const n = tr.thinInstanceCount; tr.thinInstanceCount = Math.min(n, 300); out.trim300 = time(8); tr.thinInstanceCount = n; }
  out.names = [...new Set(s.meshes.map(m => m.name.replace(/[\d_.-]+$/, '')))].slice(0, 80).join(',');
  return out;
}, T);
console.log(JSON.stringify(r)); await browser.close();
