"""Writes chart-report.md + design.md for a song and patches chart.json notes. Usage: report3.py <slug>"""
import sys, json, importlib, os, re, numpy as np
sys.path.insert(0, '/workspace/nj-w1-work'); sys.path.insert(0, '/workspace/nj-w1-work/v3')
s = sys.argv[1]; mod = s.replace('-', '_')
OUT = f'/workspace/newjeans-line-designs/{s}'
c = json.load(open(f'{OUT}/chart.json')); L = json.load(open(f'{OUT}/layout.json'))
A = json.load(open(f'/workspace/nj-w1-work/{s}.analysis.json')); AU = json.load(open(f'{s}.audited.json'))
PRE = json.load(open(f'{s}.preaudit.chart.json'))
S3 = importlib.import_module('spec3_' + mod)
LEGACY = {'attention': 139, 'hype-boy': 140, 'cookie': 357, 'hurt': 64}[s]
TITLE = L.get('title', s); dur = A['duration']; P = A['beat_period']; bpm = 60 / P
T = np.array([x['t'] for x in c['taps']]); g = np.diff(T)
def win(gg): return min(0.5 * gg, min(max(0.45 * gg, 0.045), 0.11))
lg = np.r_[g[:1], np.minimum(g[:-1], g[1:]), g[-1:]] if len(g) > 1 else g
W = np.array([win(x) for x in lg])
avg_total = len(T) / dur * 60
inst = 60 / g; avg_wiki_mean = float(np.mean(inst)); avg_wiki_med = float(60 / np.median(g))
peak_inst = 60 / g.min()
peak_win = max(((T >= t) & (T < t + 1.0)).sum() for t in T) * 60
runs, cur, st = [], 1, 0
for i, x in enumerate(g):
    if x <= 0.30 - 1e-6: cur += 1
    else:
        runs.append((cur, T[st], T[i])); cur, st = 1, i + 1
runs.append((cur, T[st], T[-1])); fr = max(runs)
b16 = c['meta'].get('bursts16', [])
secs = c['sections']; ends = [x['t'] for x in secs[1:]] + [dur]
FOLLOW = {
 'attention': {'drums': 'kick/snare backbeat and its syncopated pickups (the dotted/off-beat claps of the hook)', 'vocal': 'vocal syllables - one tap per sung syllable onset, held notes left open'},
 'hype-boy': {'drums': 'moombahton kick/snare (3+3+2 dembow syncopation)', 'vocal': 'vocal call-and-response phrase onsets', 'synth': 'the lead synth riff notes (one per beat)'},
 'cookie': {'drums': 'half-time kick/snare groove (8th doubles only where the kick really doubles)', 'vocal': 'vocal syllables of the rising/falling phrase'},
 'hurt': {'drums': 'the bass/chord hits that open each bar (about one per bar)', 'vocal': 'vocal phrase onsets and held-note releases (sung syllables only, no drum fills)'},
}[s]
rows = []
for x, e in zip(secs, ends):
    k = T[(T >= x['t']) & (T < e)]; gg = np.diff(k)
    lay = AU['report'].get(x['label'], {}).get('layer', '?')
    nb = sum(1 for t in b16 if x['t'] <= t < e)
    rows.append((x['label'], x['t'], e, len(k), len(k) / (e - x['t']), (gg.min() if len(gg) else float('nan')), lay, AU['report'].get(x['label'], {}).get('before', 0), nb))
REF = [('The Racing (hardest)', '357 / 2:24', 149, 220, 440), ('The Chaos', '-', None, 136, 408), ('Chinese Garden', '-', None, 148, 296),
       ('Winter', '-', None, 140, 280), ('Piano', '-', None, 125, 250), ('Autumn', '-', None, 96, None)]
tier = 'moderate (ballad)' if s == 'hurt' else 'hard (title track)'
honest = ''
if peak_inst < 400:
    honest = (f'Honest peak {peak_inst:.0f} CPM is below the 400-460 "title track" reference. That is deliberate (user override: rhythmic logic beats density): '
              + ('the song\'s 16th grid (0.096 s at 157 BPM) is below the 0.105 s gap floor, so no 16th bursts are possible; the hardest figures are the 8th-note club-kick runs.' if s == 'cookie' else
                 'there are no 16th figures prominent enough in the full mix to justify bursts.' if not b16 else
                 'only the few 16th figures that are clearly audible in the full mix carry bursts.'))
moves = c['meta'].get('route_moves', [])
lines = [f'# {TITLE} - chart report (designs-w1, v3, rhythm-logic audit)', '',
 f'- Audio: `public/audio/{s}.mp3`, full track {dur:.2f} s, untouched. Tempo grid measured from audio: **{bpm:.2f} BPM**, beat {P:.4f} s, downbeat phase {A["grid_phase"]:.3f} s. htdemucs stem envelopes shifted -25.03 ms before use.',
 f'- **Taps: legacy {LEGACY} -> previous designs-w1 chart {len(PRE["taps"])} -> now {len(T)}** ({len(T) / LEGACY:.2f}x legacy). Difficulty tier: {tier}.',
 f'- Audit vs the override rules: {len(AU["removed"])} off-layer / faint taps removed, {len(AU["dropped"])} one-off taps dropped and {len(AU["added"])} taps added so repeated phrases share one pattern (each added slot had clear evidence in every repeat). 16th bursts: {len(b16)} inserted tap(s) at {", ".join(f"{t:.3f}" for t in b16) or "none"}.',
 f'- Gaps: min **{g.min():.3f} s**, median {np.median(g):.3f} s (floor 0.105 s).',
 f'- Fastest run (validator definition, gaps <= 0.30 s): **{fr[0]} taps**, {fr[1]:.2f}-{fr[2]:.2f} s.',
 f'- Judgment window (engine rule min(0.5g, clamp(0.45g, 45, 110 ms)), g = local min gap): **min ±{W.min() * 1000:.0f} ms, median ±{np.median(W) * 1000:.0f} ms** - always <= half the local gap.',
 '', '## Difficulty vs original Dancing Line', '',
 '| Level | Taps / length | avg CPM (total taps / duration) | avg CPM (wiki-style) | peak CPM |', '|---|---|---|---|---|',
 f'| **{TITLE} (this chart)** | {len(T)} / {int(dur // 60)}:{int(dur % 60):02d} | **{avg_total:.0f}** | **{avg_wiki_med:.0f}** (60/median gap; mean of 60/gap = {avg_wiki_mean:.0f}) | **{peak_inst:.0f}** (60/min gap); {peak_win:.0f} as taps-in-1 s x60 |']
for n, tl, at, aw, pk in REF:
    lines.append(f'| {n} | {tl} | {at if at else "-"} | {aw} | {pk if pk else "-"} |')
lines += ['', 'Wiki-style avg CPM is approximated as 60 / median tap gap (the wiki does not publish its formula; for The Racing total/duration gives 149 while the wiki says 220, so it is clearly a playing-tempo measure rather than taps per minute of audio). Peak CPM = 60 / shortest gap, which reproduces the wiki numbers (Racing 16ths at 110 BPM = 0.136 s = 440).',
 *( [ '', honest ] if honest else [] ),
 '', '## Per-section density and what the taps follow', '',
 '| Section | Start | End | Taps (before audit -> now) | Taps/s | Min gap | Layer | What the taps follow |', '|---|---|---|---|---|---|---|---|']
for (lab, a0, e, n, d, mg, lay, before, nb) in rows:
    f = FOLLOW.get(lay, lay)
    if n <= 2: f += '; deliberately near-empty (break / held notes - breathing room)'
    if nb: f += f'; {nb} 16th burst tap(s) on an audible fill, starting and ending on 8th/beat positions'
    lines.append(f'| {lab} | {a0:.2f} | {e:.2f} | {before} -> {n} | {d:.2f} | {mg:.3f} | {lay} | {f} |')
lines += ['', '## Rules applied (user override, 11:55)', '',
 '1. One layer per section (table above). Taps whose own-layer envelope was weak at the tap (another layer drove it) were removed, even when the full mix was loud there.',
 '2. Repeated sections (' + '; '.join(' / '.join(gp) for gp in importlib.import_module('audit_groups').G[s]) + ') were aligned bar-by-bar on the 16th-slot grid: a slot is kept/added if most repeats have it and every repeat shows evidence; one-off slots were dropped unless very strong.',
 '3. 16th bursts only where the onset of the FULL MIX (not a stem) is in the top percentile at the 16th off-position, with both neighbours on 8th positions and at least one on a beat - so a burst starts and ends on strong grid points (3-tap figures).',
 '4. Held notes, breaks and outros keep their long gaps; no fills were added to reach CPM targets.',
 '5. Faint onsets (layer < 0.22 or mix < 0.10 at the tap) removed unless they anchor a section start.',
 '', '## Route (summary)', '', 'Route textures per section are listed in design.md; moves: ' + ', '.join(f'{m["name"]} ({m["kind"]})' for m in moves) + '.',
 '', 'Not tested in the engine on a device; touch latency still needs confirming.']
open(f'{OUT}/chart-report.md', 'w').write('\n'.join(lines) + '\n')
notes = (f'{TITLE} {bpm:.2f} BPM (beat {P:.4f} s). {len(T)} taps (legacy {LEGACY}). Each section follows one audible layer (see chart-report.md); repeated phrases share one tap pattern; '
         f'{len(b16)} 16th burst tap(s) only on fills clearly audible in the full mix; min gap {g.min():.3f} s, honest peak {peak_inst:.0f} CPM, avg {avg_total:.0f} CPM (total) / {avg_wiki_med:.0f} (wiki-style). '
         f'Engine judgment window ±{W.min() * 1000:.0f}..±110 ms.')
c['notes'] = notes; json.dump(c, open(f'{OUT}/chart.json', 'w'), indent=1)
open(f'{s}.notes.txt', 'w').write(notes)
# design.md
r = L.get('route', {}); objs = L.get('objects', [])
lm = [o for o in objs if o.get('landmark')]; eggs = [o for o in objs if o.get('egg')]
D = [f'# {TITLE} - level design (designs-w1, v3)', '',
 f'Codex concept/blueprint (codex-ref/) is used as a loose mood/palette reference only; the route choreography is our own. {len(T)} taps, speed {c["speed"][0]["v"] if isinstance(c.get("speed"), list) else c.get("speed")} u/s, start heading {c.get("startHeading")}.', '',
 '## Route textures per section', '']
for x in L['sections']:
    D.append(f'- **{x["label"]}** ({x["t"]:.2f} s): {x.get("note", "")}')
D += ['', '## Structure', '',
 f'- Multi-level crossings: {len(r.get("crossings", []))} (over/under passes, piers added automatically under raised road; camera goes "high" over underpasses).',
 f'- Fake-out forks (visual only, a stub of road continuing straight that ends in a broken edge; no hint): {", ".join(f"{f["t"] if isinstance(f, dict) else f}" for f in r.get("fake_forks", []))} s.',
 '- Arcades / wraps through buildings: ' + '; '.join(f'{a[2]} ({a[0]:.1f}-{a[1]:.1f} s)' for a in S3.arcades) + '.',
 '- Elevation: ' + '; '.join(f'{e["type"]} {e.get("dy"):+g} at {e.get("t", e.get("t0"))}' + (f'-{e["t1"]}' for _ in [0]).__next__() if 't1' in e else f'{e["type"]} {e.get("dy"):+g} at {e.get("t")}' for e in L.get('elevation', [])) + '.',
 f'- Landmarks: ' + '; '.join(o.get('name', o['id']) for o in lm) + '.',
 f'- Eggs: ' + ('; '.join(o.get('name', o['id']) for o in eggs) or 'none') + '.',
 f'- Diamonds ({len(L["diamonds"])}): ' + ', '.join(f'{d["t"]:.2f}' for d in L['diamonds']) + f' s. Crowns ({len(L["crowns"])}): ' + ', '.join(f'{d["t"]:.2f}' for d in L['crowns']) + ' s.',
 '- Camera: ' + ', '.join(f'{k["t"]:.1f}s {k.get("preset")}' for k in L['camera']) + '.',
 '- No tap hints anywhere (the engine adds the % markers itself).', '',
 '## Art (engine files under art/)', '',
 'All art is procedural (PIL, `_w1_tools/v3/artgen.py`): the image-generation tool\'s outputs could not be reached from the box shell in this session, so they could not be copied into the level folder. No real people\'s faces - only cartoon bunnies, shapes and album motifs.', '']
for k, v in S3.art['files'].items():
    D.append(f'- `art/{k}` - {v}')
D += ['', f'layout.json `art`: backdrop `{L["art"].get("backdrop")}`, ground `{L["art"].get("ground", {}).get("src")}`; section backdrops: ' +
      (', '.join(f'{x["label"]} -> {x["backdrop"]}' for x in L['sections'] if x.get('backdrop')) or 'none') + '; image objects (posters/stickers): ' + str(sum(1 for o in objs if o.get('kind') == 'image')) + '.']
open(f'{OUT}/design.md', 'w').write('\n'.join(D) + '\n')
print(s, len(T), f'avg {avg_total:.0f}/{avg_wiki_med:.0f} peak {peak_inst:.0f} win {W.min()*1000:.0f} run {fr[0]}')
