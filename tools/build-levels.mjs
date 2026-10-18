// Merge levels-src/<slug>/{chart,layout}.json + analysis into src/levels/<slug>.json (runtime format).
import { readFileSync, writeFileSync, existsSync, mkdirSync, cpSync, rmSync } from 'node:fs';
const SONGS = ['attention', 'hype-boy', 'cookie', 'hurt', 'omg', 'ditto', 'new-jeans', 'super-shy', 'eta', 'cool-with-you', 'get-up', 'asap', 'how-sweet', 'bubble-gum', 'supernatural', 'right-now'];
const META = Object.fromEntries((await import('./song-meta.mjs')).default.map(m => [m.id, m]));
mkdirSync('src/levels', { recursive: true });
const only = process.argv.slice(2);
for (const id of SONGS) {
  if (only.length && !only.includes(id)) continue;
  const dir = `levels-src/${id}`;
  if (!existsSync(`${dir}/chart.json`) || !existsSync(`${dir}/layout.json`)) { console.log(`skip ${id} (no source)`); continue; }
  const chart = JSON.parse(readFileSync(`${dir}/chart.json`, 'utf8'));
  const layout = JSON.parse(readFileSync(`${dir}/layout.json`, 'utf8'));
  const an = JSON.parse(readFileSync(`analysis/${id}.json`, 'utf8'));
  const grid = existsSync(`analysis/${id}.grid.json`) ? JSON.parse(readFileSync(`analysis/${id}.grid.json`, 'utf8')) : null;
  const duration = an.duration;
  let beats = an.beats;
  if (grid) { beats = []; for (let t = grid.beat0; t < duration; t += grid.period) beats.push(Math.round(t * 1000) / 1000); }
  const kicks = an.kick.filter(([, s]) => s >= 0.45).map(([t]) => t);
  const taps = chart.taps.map(t => t.t);
  const density = taps.length / duration;
  let minRun = Infinity; for (let i = 3; i < taps.length; i++) minRun = Math.min(minRun, (taps[i] - taps[i - 3]) / 3);
  const difficulty = Math.max(1, Math.min(5, Math.round(density * 1.2 + (minRun < 0.24 ? 1 : 0))));
  const m = META[id];
  const out = { id, title: m.title, album: m.album, duration, bpm: grid ? Math.round(grid.bpm * 100) / 100 : an.tempo, audio: `./audio/${id}.mp3`, cover: m.cover, difficulty, accent: m.accent,
    chart, layout: { ...layout, beats: layout.beats ?? beats, kicks: layout.kicks ?? kicks } };
  writeFileSync(`src/levels/${id}.json`, JSON.stringify(out));
  // level art (schema v2.4): levels-src/<id>/art -> public/levels/<id>/art (served at ./levels/<id>/art/...)
  rmSync(`public/levels/${id}`, { recursive: true, force: true });
  if (existsSync(`${dir}/art`)) { mkdirSync(`public/levels/${id}`, { recursive: true }); cpSync(`${dir}/art`, `public/levels/${id}/art`, { recursive: true }); }
  console.log(`${id}: ${taps.length} taps (legacy ${m.legacyTaps}, x${(taps.length / m.legacyTaps).toFixed(2)}), ${density.toFixed(2)}/s, difficulty ${difficulty}`);
}
