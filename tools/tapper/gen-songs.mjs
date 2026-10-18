// Writes tapper/src/songs.json: the game's 16 songs (same order as src/catalog.ts) with the known beat grid.
// Grid source: levels-src/<id>/chart.json meta (the grid the shipped chart uses) if present, else analysis/<id>.grid.json.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
const cat = readFileSync('src/catalog.ts', 'utf8');
const songs = [...cat.matchAll(/\{ id: '([^']+)', title: '([^']+)', album: '([^']+)', cover: C\('([^']+)'\), accent: '([^']+)'/g)]
  .map(([, id, title, album, cover, accent]) => ({ id, title, album, cover, accent }));
const out = songs.map(s => {
  const g = existsSync(`analysis/${s.id}.grid.json`) ? JSON.parse(readFileSync(`analysis/${s.id}.grid.json`, 'utf8')) : null;
  const a = existsSync(`analysis/${s.id}.json`) ? JSON.parse(readFileSync(`analysis/${s.id}.json`, 'utf8')) : null;
  const c = existsSync(`levels-src/${s.id}/chart.json`) ? JSON.parse(readFileSync(`levels-src/${s.id}/chart.json`, 'utf8')) : null;
  const m = c?.meta ?? {};
  let period = m.beat_period ?? (m.bpm ? 60 / m.bpm : null) ?? g?.period ?? null;
  let beat0 = m.beat0 ?? g?.beat0 ?? null; let src = m.beat_period || m.bpm ? 'chart' : g ? 'analysis' : null;
  // bar phase: first downbeat from the analysis bars (if the grid is the same), as a beat index offset 0..3
  let barBeat = 0;
  if (g?.bars?.length && period && beat0 !== null) { const b0 = typeof g.bars[0] === 'number' ? g.bars[0] : g.bars[0]?.t ?? g.bars[0]?.[0]; if (typeof b0 === 'number') barBeat = ((Math.round((b0 - beat0) / period) % 4) + 4) % 4; }
  return { ...s, duration: a?.duration ?? null, bpm: period ? +(60 / period).toFixed(3) : null, period, beat0, barBeat, gridSource: src, charted: !!c };
});
writeFileSync('tapper/src/songs.json', JSON.stringify(out, null, 1));
console.log(out.map(s => `${s.id} ${s.bpm} beat0=${s.beat0?.toFixed?.(3)} bar+${s.barBeat} (${s.gridSource})`).join('\n'));
