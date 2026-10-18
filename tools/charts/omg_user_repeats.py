"""Repeat-consistency report on the snapped user taps (report only). Pairs of sections whose audio repeats
(chorus/post-chorus 2 are sample copies of 1 at +128 beats; each chorus/post-chorus is two 4-bar halves 16 beats apart).
Lists per 2-bar phrase the slots only in A / only in B, so single-tap slips stand out."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
s = json.load(open(ROOT / 'analysis/user/omg-user-snap.json')); P = 0.4724304864737013; B0 = 0.011; S16 = P / 4
slots = {x['slot16'] for x in s['taps']}
def t(k): return round(B0 + k * S16, 3)
def beat(sec): return round((sec - B0) / P)
PAIRS = [('Verse 1 vs Verse 2', 14.8, 29.4, 128), ('Pre-Chorus 1 vs 2', 29.4, 45.0, 128), ('Chorus 1 vs Chorus 2', 45.0, 59.4, 128),
         ('Post-Chorus 1 vs 2', 59.4, 75.2, 128), ('Chorus 1: half A vs half B', 45.0, 52.6, 16), ('Chorus 2: half A vs half B', 105.5, 113.1, 16),
         ('Post 1: half A vs half B', 59.4, 67.0, 16), ('Post 2: half A vs half B', 120.0, 127.6, 16)]
out = []
for name, a0, a1, shift_beats in PAIRS:
    k0, k1 = beat(a0) * 4, beat(a1) * 4; sh = shift_beats * 4
    A = {k - k0 for k in slots if k0 <= k < k1}; B = {k - k0 - sh for k in slots if k0 + sh <= k < k1 + sh}
    phr = []
    for p0 in range(0, k1 - k0, 32):
        a = {k for k in A if p0 <= k < p0 + 32}; b = {k for k in B if p0 <= k < p0 + 32}
        if a != b: phr.append({'phrase_at_a': t(k0 + p0), 'phrase_at_b': t(k0 + p0 + sh), 'n_a': len(a), 'n_b': len(b),
                               'only_a': [t(k0 + k) for k in sorted(a - b)], 'only_b': [t(k0 + sh + k) for k in sorted(b - a)]})
    out.append({'pair': name, 'taps_a': len(A), 'taps_b': len(B), 'same': len(A & B), 'jaccard': round(len(A & B) / max(1, len(A | B)), 2), 'diff_phrases': phr})
json.dump(out, open(ROOT / 'analysis/user/omg-user-repeats.json', 'w'), indent=1)
for o in out:
    print(f"== {o['pair']}: A {o['taps_a']} B {o['taps_b']} same {o['same']} jaccard {o['jaccard']}")
    for p in o['diff_phrases']: print(f"   phrase {p['phrase_at_a']}/{p['phrase_at_b']}: A {p['n_a']} B {p['n_b']} onlyA {p['only_a']} onlyB {p['only_b']}")
