# Right Now — chart report

> Note: the rationale below describes the curated basis chart. It was written before the 11:55 rhythmic-logic audit. Where it differs (for example, verse taps that followed vocals are now on the drum layer), the audit section and the per-section *what the taps follow* table are authoritative.


## Rationale (tied to audio events)
- 172 BPM drum & bass: kick on 1 and the "3&", snare on 2 and 4; tapping grid is the 8th note (0.174 s) — the 16th (0.087 s) is never used.
- **Intro 0.34–11.50**: piano chords only, 13 taps on chord hits (soft onsets, verified on the "other" stem).
- **Verse 1 (2.4/s)**: kick/snare skeleton (`1 . 2 2& . 3& 4 .`-type figures) with max 2-tap bursts.
- **Pre-chorus 1 (3.05/s)**: vocal pickups added, up to 4-tap bursts.
- **Choruses (3.45–3.64/s)**: full DnB pattern, bursts of up to 4 taps on the snare/ghost-kick clusters.
- **Half-time bridge 78.47–100.80 (1.9/s)**: drums switch to half-time (snare on beat 3); taps follow the snare + vocal, line slows to 9.5 u/s.
- **Break 117.55–123.13**: drums out, 5 piano taps.
- **Final chorus 123.13–145.45 (4.1/s)**: the hardest section of my four songs — **6 consecutive 8ths (0.174 s) from 135.16 s**, multiple 4-runs; road narrows to 1.8 and speed 11.
- **Outro**: piano, 12 sparse taps.


## Rhythmic-logic audit (user override 11:55) and difficulty

Rules applied by `_w4_tools/audit.py` to the curated chart (419 taps): one audible layer per section; repeated phrases get one shared pattern; 16th bursts only where the 16th figure is prominent in the **full mix** (not just a stem), starting and ending on beats; breathing room kept; no taps on faint onsets. The stem-only triplet/syncopation taps from the previous pass were dropped. Result: **411 taps**.

- removed as off-layer (no audible hit of the section's layer within ±35 ms): 0 — 
- removed as faint (full-mix onset < 0.7× median strength in both the tag band and broadband): 6 — 2.95, 53.88, 77.08, 102.20, 132.89, 148.07
- re-tagged to the section layer (they coincide with an audible hit of that layer): 54
- bars unified to a shared pattern (same phrase in another instance or 4 bars earlier, every added slot verified audible): 34
- 16th bursts: 0 (none: no prominent 16th figure in the full mix at a phrase end)

### What the taps follow, per section

| section | layer the taps follow |
|---|---|
| Intro | the melodic synth/vocal hook (melodic layer) |
| Verse 1 | kick + clap pattern on the 8th grid (172 BPM) |
| Pre-chorus 1 | kick + clap, 8th pickups |
| Chorus 1 | kick + clap (the hook drum figure) |
| Verse 2 | Verse-1 pattern (shared) |
| Half-time bridge | half-time kick + clap backbeat |
| Chorus 2 | Chorus-1 pattern (shared) |
| Break | melodic hits only, sparse |
| Final chorus | Chorus-1 pattern, densest |
| Outro | melodic stabs, sparse |

### Difficulty (soft references, not quotas)

| metric | this chart |
|---|---|
| avg CPM = taps / full audio length x 60 | **154** (411 taps / 160.4 s) |
| avg CPM over the playable span (first->last tap) | 160 |
| wiki-style avg CPM (mean of instantaneous 60/gap) | **223** (median 172) |
| peak CPM = 60 / min gap | **345** (min gap 174 ms at 129.58 s) |
| sustained 4-tap peak (3 gaps) | 344 CPM from 48.65 s |
| tightest engine judgment window | ±78 ms at 129.58 s (local gap 174 ms); half-gap rule violations: 0 |

Originals (dlfm-wiki): The Racing avg 220 / peak 440 · The Chaos 136 / 408 · Chinese Garden 148 / 296 (window ±45.8 ms) · Amusement Park peak 512 · Storm peak 460 · Winter 140 / 280 · Piano 125 / 250 · Autumn avg 96.


Audio: `public/audio/right-now.mp3`, full length 160.41 s, used as-is. Tempo 172.00 BPM (constant), grid bar0 = 0.335 s, bar = 1.3954 s.
## Counts
| | legacy v1 | new |
|---|---|---|
| taps | 216 | **411** (1.90x) |
| avg taps/s | 1.35 | 2.56 |
| min gap | 0.325 s | 0.174 s |
| fastest run (gaps <= 0.30 s) | - | 6 taps from 135.16 s |
| longest run at the minimum gap (0.174 s) | - | 6 taps from 135.16 s |

Judgment window (schema v2.5 engine rule, per tap): **PERFECT ±40 ms; window = min(0.5·g, clamp(0.45·g, 45, 110 ms))**, so the tightest is ±78 ms and sparse taps get ±110 ms (min tap gap 0.174 s -> tightest window ±78 ms (always <= half the local gap); sparse taps ±110 ms.).
Minimum tap gap: 0.174 s (one 8th note).

## Per-section density

| section | kind | start | end | taps | taps/s | max run (<=0.30 s) |
|---|---|---|---|---|---|---|
| Intro | intro | 0.34 | 11.50 | 10 | 0.90 | 1 |
| Verse 1 | verse | 11.50 | 33.82 | 53 | 2.37 | 2 |
| Pre-chorus 1 | pre | 33.82 | 44.99 | 34 | 3.05 | 4 |
| Chorus 1 | chorus | 44.99 | 67.31 | 78 | 3.49 | 4 |
| Verse 2 | verse | 67.31 | 78.47 | 28 | 2.51 | 2 |
| Half-time bridge | bridge | 78.47 | 100.80 | 40 | 1.79 | 2 |
| Chorus 2 | chorus | 100.80 | 117.55 | 64 | 3.82 | 4 |
| Break | break | 117.55 | 123.13 | 5 | 0.90 | 1 |
| Final chorus | chorus | 123.13 | 145.45 | 90 | 4.03 | 6 |
| Outro | outro | 145.45 | 160.41 | 9 | 0.60 | 1 |

## Sync measurement

For every tap the nearest transient in the **full mix** (band chosen by the tap's tag: 40–180 Hz for kick/bass, 300–3000 Hz for vocal/melody, 1.5–10 kHz for clap/hat; max-slope of the band envelope within ±60 ms) was measured. Salient transients found for 175/419 taps (the rest sit on soft vocal/synth onsets with no sharp attack). Offset = transient − tap: median -1.2 ms, median |offset| 1.5 ms, 90th percentile |offset| 11.0 ms.

| section | measured | median offset ms | median abs ms |
|---|---|---|---|
| Intro | 1 | +4.1 | 4.1 |
| Verse 1 | 21 | -0.9 | 1.4 |
| Pre-chorus 1 | 18 | -0.9 | 1.1 |
| Chorus 1 | 35 | -1.2 | 1.4 |
| Verse 2 | 11 | -1.5 | 1.8 |
| Half-time bridge | 21 | -1.4 | 2.2 |
| Chorus 2 | 24 | -1.5 | 1.5 |
| Break | 0 | – | – |
| Final chorus | 38 | -1.4 | 1.9 |
| Outro | 6 | -0.4 | 0.5 |

Cross-check on separated stems (demucs; times corrected −50 ms): 410/411 taps have a stem onset (drums/bass/vocals/other, strength > 0.35) within ±60 ms; median offset +6.0 ms, 90th pct |offset| 15.0 ms. Section-boundary taps are listed below.

## Spot checks (start / section changes / middle / end)

| tap t (s) | section | grid position | tagged event | band | measured offset ms |
|---|---|---|---|---|---|
| 1.207 | Intro | bar 0 slot 5/8 | melody | mid | n/a (soft onset) |
| 2.428 | Intro | bar 1 slot 4/8 | melody | mid | n/a (soft onset) |
| 3.125 | Intro | bar 2 slot 0/8 | melody | mid | n/a (soft onset) |
| 3.997 | Intro | bar 2 slot 5/8 | melody | mid | +4.1 |
| 11.497 | Verse 1 | bar 8 slot 0/8 | kick | mid | -2.3 |
| 11.846 | Verse 1 | bar 8 slot 2/8 | clap | hi | -0.8 |
| 34.172 | Pre-chorus 1 | bar 24 slot 2/8 | clap | hi | -0.3 |
| 34.346 | Pre-chorus 1 | bar 24 slot 3/8 | kick | lo | n/a (soft onset) |
| 44.986 | Chorus 1 | bar 32 slot 0/8 | clap | hi | -2.0 |
| 45.335 | Chorus 1 | bar 32 slot 2/8 | clap | hi | -0.4 |
| 67.312 | Verse 2 | bar 48 slot 0/8 | kick | lo | n/a (soft onset) |
| 67.661 | Verse 2 | bar 48 slot 2/8 | clap | hi | -1.0 |
| 79.172 | Half-time bridge | bar 56 slot 4/8 | clap | hi | -0.6 |
| 80.393 | Half-time bridge | bar 57 slot 3/8 | kick | lo | n/a (soft onset) |
| 80.568 | Half-time bridge | bar 57 slot 4/8 | clap | hi | -15.6 |
| 80.916 | Half-time bridge | bar 57 slot 6/8 | bass | lo | n/a (soft onset) |
| 100.800 | Chorus 2 | bar 72 slot 0/8 | clap | hi | -2.3 |
| 101.149 | Chorus 2 | bar 72 slot 2/8 | clap | hi | -1.5 |
| 117.545 | Break | bar 84 slot 0/8 | melody | mid | n/a (soft onset) |
| 119.638 | Break | bar 85 slot 4/8 | melody | mid | n/a (soft onset) |
| 123.126 | Final chorus | bar 88 slot 0/8 | kick | mid | n/a (soft onset) |
| 123.475 | Final chorus | bar 88 slot 2/8 | clap | hi | -1.1 |
| 147.545 | Outro | bar 105 slot 4/8 | melody | mid | n/a (soft onset) |
| 149.115 | Outro | bar 106 slot 5/8 | melody | mid | n/a (soft onset) |
| 154.173 | Outro | bar 110 slot 2/8 | melody | mid | n/a (soft onset) |
| 154.696 | Outro | bar 110 slot 5/8 | melody | mid | -1.9 |
| 155.045 | Outro | bar 110 slot 7/8 | melody | mid | -0.4 |
| 155.743 | Outro | bar 111 slot 3/8 | melody | mid | -0.4 |

## How this chart was made (honest method)

1. **Audio analysis** (`analysis.json`): librosa 0.11 on the untouched mp3 + demucs htdemucs stems (drums / bass / vocals / other). Constant-tempo beat grid from a DP beat tracker fitted linearly, then shifted to the measured clap/hat transient (librosa onset envelopes and demucs both lag; demucs by 25 ms). Section boundaries come from checkerboard novelty + agglomerative segmentation, cross-checked with per-bar stem levels (vocal present? drums present? bass present?).
2. **Rhythm vocabulary per section, set by hand** (`specs/<slug>.py` in `_w4_tools`): density target (taps per bar), which stems matter (e.g. vocal weight 1.6 in the Bubble Gum hook, clap/kick in the Supernatural groove), maximum burst length.
3. **Slot selection**: every 16th (8th for Right Now) is scored from the stems; for each bar the best tap set is chosen subject to the min-gap floor, the burst limit and a phrase-repetition bonus (bar 3 of a 4-bar group echoes bar 1 → call-and-response). Automatic output = candidates.
4. **Hand plans / edits**: phrase-end runs and fills (listed in the rationale) are written explicitly; first-tap rule edits.
5. **Verification**: per-tap transient offsets in the full mix + stem-onset coverage (below). I could not *listen* in this environment; tap placement is grounded in measured onsets, stem levels and the song structure, so a human listening pass is still recommended (see "open issues").


## integ-c rhythm-logic edit (2026-10-18): flagged taps removed, route repaired locally
Rule: rhythm logic comes before density. Each section follows one audible layer, and faint or off-layer taps are not used. Taps: 411 → 410.

| removed tap (s) | tag | why |
|---|---|---|
| 10.800 | vocal |  |

10.800 s (a kick hit in the melody-led intro) is removed. The 172 BPM grid is declared in chart meta, because analysis/right-now.grid.json tracks the song at 2/3 tempo.

**Route repair** (`tools/charts/integc_repair.py`). Every tap is a 90° turn, so removing one flips the heading parity of the rest of the route.
- Only a short window after each removal is re-planned. The designer's remaining route is then re-attached verbatim as a rigid copy: identical shape, rotated by k·90° and/or translated.
- Objects placed at absolute world positions that come after the join get the same transform. Objects inside the window move with the route there.
- The validator's same-level overlap rule and the air-time rule are kept, and the join is chosen to avoid new object/road intersections.

Repair log:
- group [10.8]: window 9.579-11.497 s (1 re-planned turns), remainder re-attached with rotation 90 deg, translation (7.48, 113.40); crossings 11; objects transformed 42, window-moved 0, new object/road intersections before nudge 0

Chartlogic after the edit: see docs/verification/chartlogic/right-now.md.
