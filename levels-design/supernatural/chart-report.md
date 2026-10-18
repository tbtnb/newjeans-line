# Supernatural — chart report

> Note: the rationale below describes the curated basis chart. It was written before the 11:55 rhythmic-logic audit. Where it differs (for example, verse taps that followed vocals are now on the drum layer), the audit section and the per-section *what the taps follow* table are authoritative.


## Rationale (tied to audio events)
- **Intro 0.33–9.14 (bars 0–3)**: only the *Back of My Mind* sample/ad-libs and claps, no kick. Roughly two taps per bar on beat 1 / the clap — calm, readable start. First tap 2.53 s (bar-0 taps dropped: first-tap rule).
- **Groove 9.14–26.75 (bars 4–11)**: NJS drums enter, no lead vocal yet. Taps follow the kick on 1, the syncopated kick on the "2&" and the kick/clap figure on beats 3–4 (e.g. bar 4 `1 . . . | . . 2& . | . . 3& . | 4 . . .`) → 3–4 taps per bar with rests that read as long straights.
- **Verse 1 26.75–44.37**: vocal enters; vocal weight raised; beat-2 rest + 8th pairs on beats 3–4 follow the vocal phrase ends.
- **Pre-chorus 1 44.37–61.98**: density 2.3/s, ends with the bar-27 **8-tap 8th run (59.78→61.98, 0.275 s)** on the snare roll into the chorus downbeat — the densest run of the song, Dancing-Line-style "spam into the drop".
- **Chorus 1 / Chorus 2 / Final chorus**: 8th runs on beats 3–4 over the kick on 1 (patterns like `1 . 2 . 3 3& 4 4&`), the hook syllables decide where runs start; Chorus 2 opens straight out of the 7-run with another 6-tap run (bar 52: `1 . 2 2& 3 3& 4 4&`). Final chorus is the densest section (2.84/s).
- **Bridge 97.21–114.83**: drums drop to almost nothing → 1.36/s, taps on vocal phrase starts, long glides (the line also falls into the star layer here). Bar 51 drum fill (snare on 1-2-3) → **7-tap run** re-entry into Chorus 2.
- **Interlude**: vocal level low, synth stabs → 1.5/s, back-beat focused breathing room before the last chorus.
- **Outro 167.67–**: sample returns, clap on 2/4 only → sparse.


## Rhythmic-logic audit (user override 11:55) and difficulty

Rules applied by `_w4_tools/audit.py` to the curated chart (343 taps): one audible layer per section; repeated phrases get one shared pattern; 16th bursts only where the 16th figure is prominent in the **full mix** (not just a stem), starting and ending on beats; breathing room kept; no taps on faint onsets. The stem-only triplet/syncopation taps from the previous pass were dropped. Result: **320 taps**.

- removed as off-layer (no audible hit of the section's layer within ±35 ms): 15 — 51.25, 56.75, 61.43, 63.08, 65.29, 78.77, 79.32, 82.90, 88.13, 96.66, 111.53, 115.93, 118.13, 129.97, 155.29
- removed as faint (full-mix onset < 0.7× median strength in both the tag band and broadband): 6 — 61.98, 67.76, 70.52, 129.41, 153.36, 158.86
- re-tagged to the section layer (they coincide with an audible hit of that layer): 42
- bars unified to a shared pattern (same phrase in another instance or 4 bars earlier, every added slot verified audible): 31
- 16th bursts: 0 (none: no prominent 16th figure in the full mix at a phrase end)

### What the taps follow, per section

| section | layer the taps follow |
|---|---|
| Intro | the 'Back of My Mind' sample hits and ad-libs (two per bar); no drums yet |
| Groove | NJS drum kit: kick on 1, syncopated kick on 2&, clap on the backbeat |
| Verse 1 | same drum figure as the Groove, so the verse can be learned from the groove; vocal phrases sit on top without taps of their own |
| Pre-chorus 1 | kick + clap, with 8th pairs on beats 3–4; the snare roll into the chorus becomes an 8-tap 8th run |
| Chorus 1 | kick + clap backbeat, with 8th runs on beats 3–4 (the hook drum figure) |
| Verse 2 | drum figure from Verse 1 (shared pattern) |
| Bridge | sparse kick hits under the held vocals; long glides; the bar-51 snare fill re-enters as an 8th run |
| Chorus 2 | same tap pattern as Chorus 1 (unified bar for bar where audible) |
| Interlude | backbeat claps and kick, sparse |
| Final chorus | Chorus-1 pattern again, densest because the drums are fullest |
| Outro | clap on 2 and 4 only |

### Difficulty (soft references, not quotas)

| metric | this chart |
|---|---|
| avg CPM = taps / full audio length x 60 | **101** (320 taps / 191.0 s) |
| avg CPM over the playable span (first->last tap) | 105 |
| wiki-style avg CPM (mean of instantaneous 60/gap) | **140** (median 109) |
| peak CPM = 60 / min gap | **218** (min gap 275 ms at 144.00 s) |
| sustained 4-tap peak (3 gaps) | 218 CPM from 112.63 s |
| tightest engine judgment window | ±110 ms at 2.53 s (local gap 550 ms); half-gap rule violations: 0 |

Originals (dlfm-wiki): The Racing avg 220 / peak 440 · The Chaos 136 / 408 · Chinese Garden 148 / 296 (window ±45.8 ms) · Amusement Park peak 512 · Storm peak 460 · Winter 140 / 280 · Piano 125 / 250 · Autumn avg 96.


Audio: `public/audio/supernatural.mp3`, full length 191.00 s, used as-is. Tempo 109.00 BPM (constant), grid bar0 = 0.332 s, bar = 2.2018 s.
## Counts
| | legacy v1 | new |
|---|---|---|
| taps | 162 | **320** (1.98x) |
| avg taps/s | 0.85 | 1.68 |
| min gap | 0.468 s | 0.275 s |
| fastest run (gaps <= 0.30 s) | - | 9 taps from 58.96 s |
| longest run at the minimum gap (0.275 s) | - | 9 taps from 58.96 s |

Judgment window (schema v2.5 engine rule, per tap): **PERFECT ±40 ms; window = min(0.5·g, clamp(0.45·g, 45, 110 ms))**, so the tightest is ±110 ms and sparse taps get ±110 ms (min tap gap 0.275 s -> tightest window ±110 ms (always <= half the local gap); sparse taps ±110 ms.).
Minimum tap gap: 0.275 s (one 8th note).

## Per-section density

| section | kind | start | end | taps | taps/s | max run (<=0.30 s) |
|---|---|---|---|---|---|---|
| Intro | intro | 0.33 | 9.14 | 6 | 0.68 | 1 |
| Groove | verse | 9.14 | 26.75 | 30 | 1.70 | 4 |
| Verse 1 | verse | 26.75 | 44.37 | 29 | 1.65 | 4 |
| Pre-chorus 1 | pre | 44.37 | 61.98 | 38 | 2.16 | 9 |
| Chorus 1 | chorus | 61.98 | 79.60 | 36 | 2.04 | 7 |
| Verse 2 | verse | 79.60 | 97.21 | 31 | 1.76 | 4 |
| Bridge | bridge | 97.21 | 114.83 | 23 | 1.31 | 7 |
| Chorus 2 | chorus | 114.83 | 132.44 | 42 | 2.38 | 9 |
| Interlude | break | 132.44 | 150.06 | 26 | 1.48 | 3 |
| Final chorus | chorus | 150.06 | 167.67 | 41 | 2.33 | 6 |
| Outro | outro | 167.67 | 191.00 | 18 | 0.77 | 1 |

## Sync measurement

For every tap the nearest transient in the **full mix** (band chosen by the tap's tag: 40–180 Hz for kick/bass, 300–3000 Hz for vocal/melody, 1.5–10 kHz for clap/hat; max-slope of the band envelope within ±60 ms) was measured. Salient transients found for 140/343 taps (the rest sit on soft vocal/synth onsets with no sharp attack). Offset = transient − tap: median -9.2 ms, median |offset| 14.1 ms, 90th percentile |offset| 24.1 ms.

| section | measured | median offset ms | median abs ms |
|---|---|---|---|
| Intro | 4 | +1.1 | 1.5 |
| Groove | 10 | -10.4 | 11.9 |
| Verse 1 | 12 | -6.8 | 15.0 |
| Pre-chorus 1 | 19 | +0.3 | 1.6 |
| Chorus 1 | 14 | -14.2 | 14.2 |
| Verse 2 | 15 | -9.0 | 23.5 |
| Bridge | 8 | -11.8 | 11.8 |
| Chorus 2 | 16 | -9.8 | 12.2 |
| Interlude | 10 | +0.2 | 4.0 |
| Final chorus | 18 | -3.2 | 5.7 |
| Outro | 14 | -23.8 | 23.9 |

Cross-check on separated stems (demucs; times corrected −50 ms): 313/320 taps have a stem onset (drums/bass/vocals/other, strength > 0.35) within ±60 ms; median offset +4.0 ms, 90th pct |offset| 18.8 ms. Section-boundary taps are listed below.

## Spot checks (start / section changes / middle / end)

| tap t (s) | section | grid position | tagged event | band | measured offset ms |
|---|---|---|---|---|---|
| 2.534 | Intro | bar 1 slot 0/16 | kick | mid | +1.2 |
| 3.084 | Intro | bar 1 slot 4/16 | kick | lo | n/a (soft onset) |
| 4.736 | Intro | bar 2 slot 0/16 | kick | mid | +1.0 |
| 5.286 | Intro | bar 2 slot 4/16 | clap | hi | -23.6 |
| 9.139 | Groove | bar 4 slot 0/16 | kick | lo | n/a (soft onset) |
| 9.965 | Groove | bar 4 slot 6/16 | kick | lo | n/a (soft onset) |
| 26.754 | Verse 1 | bar 12 slot 0/16 | clap | hi | n/a (soft onset) |
| 27.580 | Verse 1 | bar 12 pos 1.50 beats | kick (burst pass) | stem other | +13.0 (stem) |
| 44.369 | Pre-chorus 1 | bar 20 slot 0/16 | clap | hi | n/a (soft onset) |
| 44.919 | Pre-chorus 1 | bar 20 slot 4/16 | clap | mid | +0.9 |
| 62.534 | Chorus 1 | bar 28 slot 4/16 | clap | hi | -14.6 |
| 63.360 | Chorus 1 | bar 28 slot 10/16 | kick | lo | n/a (soft onset) |
| 79.598 | Verse 2 | bar 36 slot 0/16 | kick | lo | n/a (soft onset) |
| 80.424 | Verse 2 | bar 36 pos 1.50 beats | kick (burst pass) | stem other | +6.0 (stem) |
| 95.011 | Verse 2 | bar 43 slot 0/16 | kick | lo | n/a (soft onset) |
| 95.837 | Verse 2 | bar 43 slot 6/16 | kick | lo | n/a (soft onset) |
| 96.112 | Verse 2 | bar 43 slot 8/16 | clap | hi | +3.7 |
| 97.763 | Bridge | bar 44 slot 4/16 | kick | lo | n/a (soft onset) |
| 98.864 | Bridge | bar 44 slot 12/16 | kick | lo | n/a (soft onset) |
| 115.378 | Chorus 2 | bar 52 slot 4/16 | clap | hi | +0.2 |
| 116.204 | Chorus 2 | bar 52 slot 10/16 | kick | lo | n/a (soft onset) |
| 133.268 | Interlude | bar 60 slot 6/16 | kick | mid | n/a (soft onset) |
| 133.818 | Interlude | bar 60 slot 10/16 | kick | lo | n/a (soft onset) |
| 150.607 | Final chorus | bar 68 slot 4/16 | clap | hi | n/a (soft onset) |
| 151.433 | Final chorus | bar 68 slot 10/16 | kick | lo | n/a (soft onset) |
| 169.323 | Outro | bar 76 slot 12/16 | clap | hi | -24.0 |
| 169.873 | Outro | bar 77 slot 0/16 | clap | hi | +0.4 |
| 181.433 | Outro | bar 82 slot 4/16 | clap | hi | -23.9 |
| 182.534 | Outro | bar 82 slot 12/16 | clap | hi | -19.8 |
| 183.635 | Outro | bar 83 slot 4/16 | clap | hi | -24.0 |
| 184.736 | Outro | bar 83 slot 12/16 | clap | hi | -19.4 |

## How this chart was made (honest method)

1. **Audio analysis** (`analysis.json`): librosa 0.11 on the untouched mp3 + demucs htdemucs stems (drums / bass / vocals / other). Constant-tempo beat grid from a DP beat tracker fitted linearly, then shifted to the measured clap/hat transient (librosa onset envelopes and demucs both lag; demucs by 25 ms). Section boundaries come from checkerboard novelty + agglomerative segmentation, cross-checked with per-bar stem levels (vocal present? drums present? bass present?).
2. **Rhythm vocabulary per section, set by hand** (`specs/<slug>.py` in `_w4_tools`): density target (taps per bar), which stems matter (e.g. vocal weight 1.6 in the Bubble Gum hook, clap/kick in the Supernatural groove), maximum burst length.
3. **Slot selection**: every 16th (8th for Right Now) is scored from the stems; for each bar the best tap set is chosen subject to the min-gap floor, the burst limit and a phrase-repetition bonus (bar 3 of a 4-bar group echoes bar 1 → call-and-response). Automatic output = candidates.
4. **Hand plans / edits**: phrase-end runs and fills (listed in the rationale) are written explicitly; first-tap rule edits.
5. **Verification**: per-tap transient offsets in the full mix + stem-onset coverage (below). I could not *listen* in this environment; tap placement is grounded in measured onsets, stem levels and the song structure, so a human listening pass is still recommended (see "open issues").
