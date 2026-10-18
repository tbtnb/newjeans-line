# Supernatural — chart report

## Rationale (tied to audio events)
- **Intro 0.33–9.14 (bars 0–3)**: only the *Back of My Mind* sample/ad-libs and claps, no kick. Roughly two taps per bar on beat 1 / the clap — calm, readable start. First tap 2.53 s (bar-0 taps dropped: first-tap rule).
- **Groove 9.14–26.75 (bars 4–11)**: NJS drums enter, no lead vocal yet. Taps follow the kick on 1, the syncopated kick on the "2&" and the kick/clap figure on beats 3–4 (e.g. bar 4 `1 . . . | . . 2& . | . . 3& . | 4 . . .`) → 3–4 taps per bar with rests that read as long straights.
- **Verse 1 26.75–44.37**: vocal enters; vocal weight raised; beat-2 rest + 8th pairs on beats 3–4 follow the vocal phrase ends.
- **Pre-chorus 1 44.37–61.98**: density 2.3/s, ends with the bar-27 **8-tap 8th run (59.78→61.98, 0.275 s)** on the snare roll into the chorus downbeat — the densest run of the song, Dancing-Line-style "spam into the drop".
- **Chorus 1 / Chorus 2 / Final chorus**: 8th runs on beats 3–4 over the kick on 1 (patterns like `1 . 2 . 3 3& 4 4&`), the hook syllables decide where runs start; Chorus 2 opens straight out of the 7-run with another 6-tap run (bar 52: `1 . 2 2& 3 3& 4 4&`). Final chorus is the densest section (2.84/s).
- **Bridge 97.21–114.83**: drums drop to almost nothing → 1.36/s, taps on vocal phrase starts, long glides (the line also falls into the star layer here). Bar 51 drum fill (snare on 1-2-3) → **7-tap run** re-entry into Chorus 2.
- **Interlude**: vocal level low, synth stabs → 1.5/s, back-beat focused breathing room before the last chorus.
- **Outro 167.67–**: sample returns, clap on 2/4 only → sparse.


## Difficulty calibration vs. original Dancing Line (11:48 steering)

Chart change in this pass: 343 -> **348 taps** (+0 taps from 8th-triplet fill bursts tagged `fill-triplet` replacing beat interiors, 5 off-beat 16th syncopations tagged `synco-16th`).

| metric | this chart |
|---|---|
| avg CPM = taps / full audio length x 60 | **109** (348 taps / 191.0 s) |
| avg CPM over the playable span (first->last tap) | 115 |
| wiki-style avg CPM (mean of instantaneous 60/gap) | **150** (median 109) |
| peak CPM = 60 / min gap | **218** (min gap 275 ms at 148.68 s) |
| sustained 4-tap peak (3 gaps) | 218 CPM from 112.63 s |
| tightest engine judgment window | ±110 ms at 2.53 s (local gap 550 ms); half-gap rule violations: 0 |

Originals (dlfm-wiki): The Racing avg 220 / peak 440 · The Chaos 136 / 408 · Chinese Garden 148 / 296 (window ±45.8 ms) · Amusement Park peak 512 · Storm peak 460 · Winter 140 / 280 · Piano 125 / 250 · Autumn avg 96.


Audio: `public/audio/supernatural.mp3`, full length 191.00 s, used as-is. Tempo 109.00 BPM (constant), grid bar0 = 0.332 s, bar = 2.2018 s.
## Counts
| | legacy v1 | new |
|---|---|---|
| taps | 162 | **348** (2.15x) |
| avg taps/s | 0.85 | 1.82 |
| min gap | 0.468 s | 0.275 s |
| fastest run (gaps <= 0.30 s) | - | 9 taps from 59.78 s |
| longest run at the minimum gap (0.275 s) | - | 9 taps from 59.78 s |

Recommended judgment window: **perfect ±50 ms, good ±90 ms, miss beyond ±120 ms** (+/-90 ms good; min tap gap 0.275 s (eighth at 109 BPM) so windows never overlap. Validate on real touch: if late-tap bias > 30 ms, shift engine latency, not chart.).
Humanly playable floor used: no two taps closer than 0.275 s (one 8th note).

## Per-section density

| section | kind | start | end | taps | taps/s | max run (<=0.30 s) |
|---|---|---|---|---|---|---|
| Intro | intro | 0.33 | 9.14 | 6 | 0.68 | 1 |
| Groove | verse | 9.14 | 26.75 | 25 | 1.42 | 2 |
| Verse 1 | verse | 26.75 | 44.37 | 29 | 1.65 | 4 |
| Pre-chorus 1 | pre | 44.37 | 61.98 | 42 | 2.38 | 8 |
| Chorus 1 | chorus | 61.98 | 79.60 | 44 | 2.50 | 9 |
| Verse 2 | verse | 79.60 | 97.21 | 32 | 1.82 | 4 |
| Bridge | bridge | 97.21 | 114.83 | 26 | 1.48 | 7 |
| Chorus 2 | chorus | 114.83 | 132.44 | 49 | 2.78 | 9 |
| Interlude | break | 132.44 | 150.06 | 26 | 1.48 | 3 |
| Final chorus | chorus | 150.06 | 167.67 | 50 | 2.84 | 9 |
| Outro | outro | 167.67 | 191.00 | 19 | 0.81 | 1 |

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

Cross-check on separated stems (demucs; times corrected −50 ms): 341/348 taps have a stem onset (drums/bass/vocals/other, strength > 0.35) within ±60 ms; median offset +5.0 ms, 90th pct |offset| 20.0 ms. Section-boundary taps are listed below.

## Spot checks (start / section changes / middle / end)

| tap t (s) | section | grid position | tagged event | band | measured offset ms |
|---|---|---|---|---|---|
| 2.534 | Intro | bar 1 slot 0/16 | vocal | mid | +1.2 |
| 3.084 | Intro | bar 1 slot 4/16 | kick | lo | n/a (soft onset) |
| 4.736 | Intro | bar 2 slot 0/16 | vocal | mid | +1.0 |
| 5.286 | Intro | bar 2 slot 4/16 | clap | hi | -23.6 |
| 9.139 | Groove | bar 4 slot 0/16 | kick | lo | n/a (soft onset) |
| 9.965 | Groove | bar 4 slot 6/16 | kick | lo | n/a (soft onset) |
| 26.754 | Verse 1 | bar 12 slot 0/16 | clap | hi | n/a (soft onset) |
| 28.130 | Verse 1 | bar 12 slot 10/16 | kick | lo | n/a (soft onset) |
| 44.369 | Pre-chorus 1 | bar 20 slot 0/16 | clap | hi | n/a (soft onset) |
| 44.919 | Pre-chorus 1 | bar 20 slot 4/16 | vocal | mid | +0.9 |
| 61.983 | Chorus 1 | bar 28 slot 0/16 | clap | hi | n/a (soft onset) |
| 62.534 | Chorus 1 | bar 28 slot 4/16 | clap | hi | -14.6 |
| 79.598 | Verse 2 | bar 36 slot 0/16 | kick | lo | n/a (soft onset) |
| 80.974 | Verse 2 | bar 36 slot 10/16 | kick | lo | n/a (soft onset) |
| 95.011 | Verse 2 | bar 43 slot 0/16 | kick | lo | n/a (soft onset) |
| 95.837 | Verse 2 | bar 43 slot 6/16 | kick | lo | n/a (soft onset) |
| 96.112 | Verse 2 | bar 43 slot 8/16 | clap | hi | +3.7 |
| 97.763 | Bridge | bar 44 slot 4/16 | kick | lo | n/a (soft onset) |
| 98.864 | Bridge | bar 44 slot 12/16 | kick | lo | n/a (soft onset) |
| 114.828 | Chorus 2 | bar 52 slot 0/16 | vocal | mid | n/a (soft onset) |
| 115.378 | Chorus 2 | bar 52 slot 4/16 | clap | hi | +0.2 |
| 133.268 | Interlude | bar 60 slot 6/16 | melody | mid | n/a (soft onset) |
| 133.818 | Interlude | bar 60 slot 10/16 | kick | lo | n/a (soft onset) |
| 150.057 | Final chorus | bar 68 slot 0/16 | kick | lo | n/a (soft onset) |
| 150.607 | Final chorus | bar 68 slot 4/16 | clap | hi | n/a (soft onset) |
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
