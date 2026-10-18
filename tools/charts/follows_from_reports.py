#!/usr/bin/env python3
"""Attach a `follows` layer to each chart section from the worker's chart-report.md 'what the taps follow' table.
The report text is mapped to an analysis band: drums (kick+snare), kick, snare, hat, mid (vocal/melody/synth), full.
Sections with no matching row keep no `follows` (chartlogic.py then infers one and marks it '(inferred)').
Usage: follows_from_reports.py <slug> [...]  (edits levels-src/<slug>/chart.json in place)"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def layer(txt):
    t = txt.lower()
    if re.search(r'kick ?(\+|/|and) ?(snare|clap)|drum groove|drums\b|backbeat and|full kit|kick pattern \+ clap', t): return 'drums'
    if any(w in t for w in ['vocal', 'syllable', 'voice', 'lyric', 'sung', 'chop', 'rap']): return 'vocal'
    for k, words in [('mid', ['melody', 'synth', 'piano', 'guitar', 'arp', 'choir', 'chop', 'voice', 'lyric', 'stab', 'lead', 'chord']),
                     ('snare', ['snare', 'clap', 'backbeat', 'rim']), ('kick', ['kick', '808', 'bass drum', 'four-on-the-floor', 'bass']),
                     ('hat', ['hat', 'shaker', 'cymbal'])]:
        if any(w in t for w in words): return k
    if 'full' in t or 'fill' in t or 'hit' in t or 'accent' in t: return 'full'
    return None
def norm(s): return re.sub(r'[^a-z0-9\u4e00-\u9fff]+', '', s.lower())
for slug in sys.argv[1:]:
    rep = (ROOT / f'levels-design/{slug}/chart-report.md').read_text() if (ROOT / f'levels-design/{slug}/chart-report.md').exists() else ''
    rows = []
    for line in rep.splitlines():
        if line.startswith('|') and not re.match(r'^\|[\s\-:|]+\|$', line):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if len(cells) >= 2: rows.append(cells)
    p = ROOT / f'levels-src/{slug}/chart.json'; c = json.loads(p.read_text())
    n = 0
    for s in c['sections']:
        lab = norm(s['label'].split('·')[0]); lab_full = norm(s['label'])
        best = None
        for cells in rows:
            k = norm(cells[0])
            if not k or k in ('section', 'level'): continue
            if k == lab or k == lab_full or (len(k) > 3 and (lab_full.startswith(k) or k.startswith(lab))):
                txt = ' '.join(cells[1:]); L = layer(txt)
                if L: best = (L, txt); break
        if best:
            s['follows'] = best[0]; s['follows_note'] = best[1][:160]; n += 1
    p.write_text(json.dumps(c, indent=1, ensure_ascii=False))
    print(f'{slug}: follows set on {n}/{len(c["sections"])} sections')
