// Ground truth without video capture: record the sink monitor with parec (low latency) stamped by wall clock, and
// have the page report the wall-clock time at which getOutputTimestamp says each beep is heard.
import { chromium } from '@playwright/test'; import { spawn } from 'node:child_process'; import { writeFileSync } from 'node:fs';
const b = await chromium.launch({ headless: true, executablePath: '/usr/bin/google-chrome', args: ['--autoplay-policy=no-user-gesture-required'] });
const page = await b.newPage(); await page.setContent('<html><body></body></html>');
const rec = spawn('parec', ['-d', 'rec.monitor', '--latency-msec=5', '--format=s16le', '--rate=44100', '--channels=1', '--raw'], { stdio: ['ignore', 'pipe', 'inherit'] });
const chunks = []; let firstWall = 0; rec.stdout.on('data', c => { if (!firstWall) firstWall = Date.now(); chunks.push(c); });
await new Promise(r => setTimeout(r, 1500));
const res = await page.evaluate(async () => {
  const c = new AudioContext({ latencyHint: 'interactive' }); await c.resume();
  await new Promise(r => setTimeout(r, 500));
  const t0 = c.currentTime + 0.5, N = 10, P = 0.9; const claims = [];
  for (let i = 0; i < N; i++) { const o = c.createOscillator(); const g = c.createGain(); o.frequency.value = 1000; o.connect(g); g.connect(c.destination); g.gain.value = 0.8; o.start(t0 + i * P); o.stop(t0 + i * P + 0.04); }
  // map context time -> wall clock using the output timestamp (exactly what the game does)
  await new Promise(r => setTimeout(r, 300));
  for (let k = 0; k < 20; k++) { const ts = c.getOutputTimestamp(); claims.push(performance.timeOrigin + ts.performanceTime + (t0 - ts.contextTime) * 1000); await new Promise(r => setTimeout(r, 200)); }
  await new Promise(r => setTimeout(r, N * P * 1000));
  return { claimBeep0Wall: claims.reduce((a, b) => a + b, 0) / claims.length, spread: Math.max(...claims) - Math.min(...claims), P, N, out: c.outputLatency, base: c.baseLatency };
});
rec.kill(); await b.close();
const buf = Buffer.concat(chunks); const s = new Int16Array(buf.buffer, buf.byteOffset, buf.length >> 1);
let first = -1; for (let i = 0; i < s.length; i++) if (Math.abs(s[i]) > 8000) { first = i; break; }
// parec delivers the first chunk ~latency after capture began; wall time of sample i ~ firstWall - chunkLen + i/sr
const firstChunkSamples = chunks[0].length >> 1; const wall0 = firstWall - firstChunkSamples / 44.1;
const beepWall = wall0 + first / 44.1;
console.log(JSON.stringify({ ...res, measuredBeep0Wall: beepWall, heardMinusClaimMs: +(beepWall - res.claimBeep0Wall).toFixed(1) }));
