# Bubble Gum — chart report

> Note: the rationale below describes the curated basis chart. It was written before the 11:55 rhythmic-logic audit. Where it differs (for example, verse taps that followed vocals are now on the drum layer), the audit section and the per-section *what the taps follow* table are authoritative.


## Rationale (tied to audio events)
- **Intro 2.06–18.05**: clean guitar only; one tap per bar on the guitar accent on beat 2 (the "other" stem's strongest onset each bar) — 8 taps, wide road, a slow seaside walk.
- **Verse 1 / Verse 2 (~1.1/s)**: light kick/clap; taps on the vocal phrase rhythm and beat-3 clap, 2–3 per bar.
- **Pre-choruses (~1.55/s)**: quarter-note walk toward the chorus with a **4×8th pickup run (0.285 s) on the last bar** (bars 23 and 58: call-and-response between the two pre-choruses).
- **Choruses (1.75–1.9/s)**: kick + clap land on beats 1 and 3; the chart follows the **"bubble bubble" vocal hook** (vocal weight 1.6) so bars alternate between straight quarters and syncopated 16th-offset figures (`1001 0000 0010 1000`, `1010 0000 1000 1000`) — rhythm variety instead of a metronome.
- **Breakdown 79.76–91.19**: drums out, voice + pads → 9 taps, long floats (the road is lifted on bubbles here); the drum re-entry at 91.19 is the moment the giant bubble pops.
- **Final chorus**: densest (1.9/s), 4–5-tap 8th runs at bars 78 and 82 to finish (fastest run of the song: 5 taps at 0.285 s, 55.77→56.91 s pre-chorus pickup); outro single tap.
- Bubble Gum is intentionally the gentlest of my four songs (the song itself is the most relaxed); difficulty comes from syncopated hook figures, not speed.


## Rhythmic-logic audit (user override 11:55) and difficulty

Rules applied by `_w4_tools/audit.py` to the curated chart (269 taps): one audible layer per section; repeated phrases get one shared pattern; 16th bursts only where the 16th figure is prominent in the **full mix** (not just a stem), starting and ending on beats; breathing room kept; no taps on faint onsets. The stem-only triplet/syncopation taps from the previous pass were dropped. Result: **257 taps**.

- removed as off-layer (no audible hit of the section's layer within ±35 ms): 4 — 65.19, 135.76, 137.33, 138.33
- removed as faint (full-mix onset < 0.7× median strength in both the tag band and broadband): 2 — 4.34, 11.77
- re-tagged to the section layer (they coincide with an audible hit of that layer): 33
- bars unified to a shared pattern (same phrase in another instance or 4 bars earlier, every added slot verified audible): 43
- 16th bursts: 0 (none: no prominent 16th figure in the full mix at a phrase end)

### What the taps follow, per section

| section | layer the taps follow |
|---|---|
| Intro | melodic plucks of the intro (melodic layer) |
| Verse 1 | soft kick + clap groove |
| Pre-chorus 1 | kick + clap, 8th pairs at phrase ends |
| Chorus 1 | kick + clap backbeat with 8th pickups |
| Breakdown | vocal phrases over the drop-out (vocal layer); sparse |
| Verse 2 | Verse-1 drum pattern (shared) |
| Pre-chorus 2 | Pre-chorus-1 pattern (shared) |
| Chorus 2 | Chorus-1 pattern (shared) |
| Final chorus | Chorus-1 pattern (shared) |
| Outro | single closing clap |

### Difficulty (soft references, not quotas)

| metric | this chart |
|---|---|
| avg CPM = taps / full audio length x 60 | **77** (257 taps / 200.3 s) |
| avg CPM over the playable span (first->last tap) | 82 |
| wiki-style avg CPM (mean of instantaneous 60/gap) | **104** (median 105) |
| peak CPM = 60 / min gap | **211** (min gap 285 ms at 66.34 s) |
| sustained 4-tap peak (3 gaps) | 210 CPM from 55.77 s |
| tightest engine judgment window | ±110 ms at 2.63 s (local gap 4571 ms); half-gap rule violations: 0 |

Originals (dlfm-wiki): The Racing avg 220 / peak 440 · The Chaos 136 / 408 · Chinese Garden 148 / 296 (window ±45.8 ms) · Amusement Park peak 512 · Storm peak 460 · Winter 140 / 280 · Piano 125 / 250 · Autumn avg 96.


Audio: `public/audio/bubble-gum.mp3`, full length 200.27 s, used as-is. Tempo 105.01 BPM (constant), grid bar0 = 2.055 s, bar = 2.2856 s.
## Counts
| | legacy v1 | new |
|---|---|---|
| taps | 132 | **257** (1.95x) |
| avg taps/s | 0.66 | 1.28 |
| min gap | 1.039 s | 0.285 s |
| fastest run (gaps <= 0.30 s) | - | 7 taps from 55.77 s |
| longest run at the minimum gap (0.285 s) | - | 7 taps from 55.77 s |

Judgment window (schema v2.5 engine rule, per tap): **PERFECT ±40 ms; window = min(0.5·g, clamp(0.45·g, 45, 110 ms))**, so the tightest is ±110 ms and sparse taps get ±110 ms (min tap gap 0.285 s -> tightest window ±110 ms (always <= half the local gap); sparse taps ±110 ms.).
Minimum tap gap: 0.285 s (one 8th note).

## Per-section density

| section | kind | start | end | taps | taps/s | max run (<=0.30 s) |
|---|---|---|---|---|---|---|
| Intro | intro | 2.06 | 18.05 | 5 | 0.31 | 1 |
| Verse 1 | verse | 18.05 | 36.34 | 19 | 1.04 | 1 |
| Pre-chorus 1 | pre | 36.34 | 56.91 | 32 | 1.56 | 4 |
| Chorus 1 | chorus | 56.91 | 79.76 | 38 | 1.66 | 3 |
| Breakdown | break | 79.76 | 91.19 | 9 | 0.79 | 1 |
| Verse 2 | verse | 91.19 | 118.62 | 30 | 1.09 | 1 |
| Pre-chorus 2 | pre | 118.62 | 136.90 | 28 | 1.53 | 3 |
| Chorus 2 | chorus | 136.90 | 164.33 | 46 | 1.68 | 3 |
| Final chorus | chorus | 164.33 | 191.76 | 49 | 1.79 | 4 |
| Outro | outro | 191.76 | 200.27 | 1 | 0.12 | 1 |

## Sync measurement

For every tap the nearest transient in the **full mix** (band chosen by the tap's tag: 40–180 Hz for kick/bass, 300–3000 Hz for vocal/melody, 1.5–10 kHz for clap/hat; max-slope of the band envelope within ±60 ms) was measured. Salient transients found for 119/269 taps (the rest sit on soft vocal/synth onsets with no sharp attack). Offset = transient − tap: median -0.1 ms, median |offset| 4.2 ms, 90th percentile |offset| 23.1 ms.

| section | measured | median offset ms | median abs ms |
|---|---|---|---|
| Intro | 2 | +24.1 | 28.9 |
| Verse 1 | 13 | -3.9 | 3.9 |
| Pre-chorus 1 | 17 | -1.9 | 2.3 |
| Chorus 1 | 20 | -1.2 | 2.1 |
| Breakdown | 2 | +2.2 | 2.3 |
| Verse 2 | 14 | +1.9 | 1.9 |
| Pre-chorus 2 | 12 | +3.1 | 3.3 |
| Chorus 2 | 15 | +4.7 | 6.5 |
| Final chorus | 23 | -15.3 | 15.3 |
| Outro | 1 | -14.7 | 14.7 |

Cross-check on separated stems (demucs; times corrected −50 ms): 257/257 taps have a stem onset (drums/bass/vocals/other, strength > 0.35) within ±60 ms; median offset +5.0 ms, 90th pct |offset| 17.0 ms. Section-boundary taps are listed below.

## Spot checks (start / section changes / middle / end)

| tap t (s) | section | grid position | tagged event | band | measured offset ms |
|---|---|---|---|---|---|
| 2.627 | Intro | bar 0 slot 4/16 | melody | mid | n/a (soft onset) |
| 7.198 | Intro | bar 2 slot 4/16 | melody | mid | n/a (soft onset) |
| 9.483 | Intro | bar 3 slot 4/16 | melody | mid | -4.7 |
| 16.340 | Intro | bar 6 slot 4/16 | melody | lo | n/a (soft onset) |
| 18.626 | Verse 1 | bar 7 pos 1.00 beats | kick (burst pass) | stem bass | +4.0 (stem) |
| 19.768 | Verse 1 | bar 7 slot 12/16 | kick | lo | n/a (soft onset) |
| 36.910 | Pre-chorus 1 | bar 15 slot 4/16 | clap | hi | -2.7 |
| 37.482 | Pre-chorus 1 | bar 15 slot 8/16 | clap | mid | -5.3 |
| 56.909 | Chorus 1 | bar 24 slot 0/16 | clap | hi | -25.0 |
| 57.194 | Chorus 1 | bar 24 pos 0.50 beats | kick (burst pass) | stem bass | +5.0 (stem) |
| 79.764 | Breakdown | bar 34 slot 0/16 | melody | lo | n/a (soft onset) |
| 80.336 | Breakdown | bar 34 slot 4/16 | melody | hi | -0.1 |
| 91.764 | Verse 2 | bar 39 slot 4/16 | kick | lo | n/a (soft onset) |
| 92.906 | Verse 2 | bar 39 slot 12/16 | kick | lo | n/a (soft onset) |
| 99.192 | Verse 2 | bar 42 slot 8/16 | clap | hi | +0.8 |
| 99.763 | Verse 2 | bar 42 slot 12/16 | clap | hi | +1.5 |
| 100.906 | Verse 2 | bar 43 slot 4/16 | kick | lo | n/a (soft onset) |
| 119.190 | Pre-chorus 2 | bar 51 slot 4/16 | kick | lo | n/a (soft onset) |
| 119.762 | Pre-chorus 2 | bar 51 slot 8/16 | kick | lo | n/a (soft onset) |
| 136.903 | Chorus 2 | bar 59 slot 0/16 | kick | lo | n/a (soft onset) |
| 137.189 | Chorus 2 | bar 59 pos 0.50 beats | kick (burst pass) | stem vocal | +3.0 (stem) |
| 164.330 | Final chorus | bar 71 slot 0/16 | clap | hi | -16.2 |
| 164.616 | Final chorus | bar 71 slot 2/16 | kick | mid | n/a (soft onset) |
| 190.328 | Final chorus | bar 82 slot 6/16 | clap | hi | +8.9 |
| 190.614 | Final chorus | bar 82 slot 8/16 | clap | hi | +7.7 |
| 190.900 | Final chorus | bar 82 slot 10/16 | kick | lo | n/a (soft onset) |
| 191.757 | Outro | bar 83 slot 0/16 | clap | hi | -14.7 |

## How this chart was made (honest method)

1. **Audio analysis** (`analysis.json`): librosa 0.11 on the untouched mp3 + demucs htdemucs stems (drums / bass / vocals / other). Constant-tempo beat grid from a DP beat tracker fitted linearly, then shifted to the measured clap/hat transient (librosa onset envelopes and demucs both lag; demucs by 25 ms). Section boundaries come from checkerboard novelty + agglomerative segmentation, cross-checked with per-bar stem levels (vocal present? drums present? bass present?).
2. **Rhythm vocabulary per section, set by hand** (`specs/<slug>.py` in `_w4_tools`): density target (taps per bar), which stems matter (e.g. vocal weight 1.6 in the Bubble Gum hook, clap/kick in the Supernatural groove), maximum burst length.
3. **Slot selection**: every 16th (8th for Right Now) is scored from the stems; for each bar the best tap set is chosen subject to the min-gap floor, the burst limit and a phrase-repetition bonus (bar 3 of a 4-bar group echoes bar 1 → call-and-response). Automatic output = candidates.
4. **Hand plans / edits**: phrase-end runs and fills (listed in the rationale) are written explicitly; first-tap rule edits.
5. **Verification**: per-tap transient offsets in the full mix + stem-onset coverage (below). I could not *listen* in this environment; tap placement is grounded in measured onsets, stem levels and the song structure, so a human listening pass is still recommended (see "open issues").


## integ-c rhythm-logic edit (2026-10-18): flagged taps removed, route repaired locally
Rule: rhythm logic comes before density. Each section follows one audible layer, and faint or off-layer taps are not used. Taps: 257 → 253.

| removed tap (s) | tag | why |
|---|---|---|
| 2.627 | melody | faint intro pluck (mid 0.33, full 0.24) |
| 57.194 | kick | faint (drums 0.28, full 0.08) |
| 87.192 | vocal | faint breakdown syllable (lag-corrected vocal stem 0.33, full 0.19) |
| 183.186 | kick | faint (drums 0.33, full 0.23) |

Breakdown vocal taps, re-measured on the demucs vocals stem with its lag corrected (23 ms, measured by cross-correlation; the mp3 stems that vocal_env.py uses lag by about 46 ms, so its ±30 ms window misses the onsets):
- The vocal is clearly the lead: about 3 dB below the full mix while the drums are out, versus −16.7 dBFS for the vocal stem against about −26 dBFS for the other stems.
- 83.193 s (vocal onset 0.38), 88.907 s (0.49) and 89.478 s (1.00) are kept.
- 87.192 s (vocal 0.33, full mix 0.19) is faint and is removed. 2.627, 57.194 and 183.186 s are faint and are removed.
- The remaining flag, 'HOP 80.336', is the chorus's last snare hit (0.86 in the full mix) carried across the section line into the breakdown. It is clearly audible, so it is kept.

**Route repair** (`tools/charts/integc_repair.py`). Every tap is a 90° turn, so removing one flips the heading parity of the rest of the route.
- Only a short window after each removal is re-planned. The designer's remaining route is then re-attached verbatim as a rigid copy: identical shape, rotated by k·90° and/or translated.
- Objects placed at absolute world positions that come after the join get the same transform. Objects inside the window move with the route there.
- The validator's same-level overlap rule and the air-time rule are kept, and the join is chosen to avoid new object/road intersections.

Repair log:
- group [2.627]: window 0.000-7.198 s (1 re-planned turns), remainder re-attached with rotation 270 deg, translation (22.33, 22.33); crossings 20; objects transformed 66, window-moved 2, new object/road intersections before nudge 1
- group [57.194]: window 56.909-62.623 s (9 re-planned turns), remainder re-attached with rotation 90 deg, translation (-316.12, 34.49); crossings 40; objects transformed 51, window-moved 3, new object/road intersections before nudge 1
- group [87.192]: window 86.621-88.907 s (1 re-planned turns), remainder re-attached with rotation 270 deg, translation (12.65, 352.55); crossings 40; objects transformed 36, window-moved 0, new object/road intersections before nudge 1
- group [183.186]: window 182.900-186.043 s (4 re-planned turns), remainder re-attached with rotation 90 deg, translation (-449.73, 78.30); crossings 39; objects transformed 4, window-moved 1, new object/road intersections before nudge 1

Chartlogic after the edit: see docs/verification/chartlogic/bubble-gum.md.
