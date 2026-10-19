// usage: node tools/qa/model-audit.mjs <base url (dev server)> <outdir> [ids...]   (box: SwiftShader; --gpu on the Mac)
import { chromium } from '@playwright/test'; import { readdirSync, mkdirSync, writeFileSync } from 'node:fs';
const [url, out, ...rest] = process.argv.slice(2); const gpu = rest.includes('--gpu'); const ids = rest.filter(x => !x.startsWith('--'));
const all = ids.length ? ids : readdirSync('public/models/omg-c').filter(f => f.endsWith('.glb')).map(f => f.slice(0, -4));
const br = await chromium.launch({ headless: true, executablePath: process.platform === 'darwin' ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' : '/usr/bin/google-chrome', args: gpu ? ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist', '--headless=new'] : ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--headless=new'] });
const page = await (await br.newContext({ viewport: { width: 1024, height: 512 } })).newPage(); page.on('pageerror', e => console.error(e.message));
await page.goto(url + '/tools/qa/model-audit.html'); await page.waitForFunction(() => window.auditReady, null, { timeout: 120000 });
mkdirSync(out, { recursive: true }); const rep = {};
for (const id of all) { try { rep[id] = await page.evaluate(id => window.auditModel(id), id); await page.evaluate(() => document.querySelectorAll('vite-error-overlay').forEach(e => e.remove())); await page.locator('canvas').screenshot({ path: `${out}/${id}.png` }); console.log(id, JSON.stringify(rep[id])); } catch (e) { console.log(id, 'ERR', e.message.slice(0, 120)); } }
writeFileSync(`${out}/report.json`, JSON.stringify(rep, null, 1)); await br.close();
