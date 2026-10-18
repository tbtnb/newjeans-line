# How Sweet — chart report

## Rationale (tied to audio events)
- The Miami-bass backbone is a **tresillo at bar scale** (16th slots 0 / 6 / 12 = 3+3+2 dotted quarters) with the clap on beat 4 of the bar; verses and choruses use it as the default figure, so the route has a recognisable long-long-short gait.
- **Intro 0.34–8.02**: synth arpeggio only, taps on the arp downbeats (5 taps).
- **Verse 1 / Verse 2 (~1.0/s)**: sparse drums (clap every bar on 4, kick fragments); taps on the vocal phrase starts + clap → plenty of breathing.
- **Pre-chorus 1 38.74–46.42**: drums thin, kick on 2/4 → 2/s, bar 23 pickup **4×8th run into the chorus**.
- **Choruses**: full drums; tresillo + vocal "how sweet" figures, every 4th bar ends in an **8th-note run on beats 3–4** (`1 . 2 . 3 3& 4 4&`), matching the synth 8th figure heard in the "other" stem.
- **Bridge 138.58–153.94**: bass drops out, half-time kick on 2 & 4 → exactly the back-beat (1.1/s).
- **Build 153.94–169.29**: drum break at bar 86 (left empty: 2 bars of almost nothing), then a run into the final chorus.
- **Final chorus 169.29–200.01** (2.15/s): runs on bars 91/95/99 and the **8-tap run 198.09→199.78 (0.24 s)** as the climax before the outro.
- **Outro**: synth only, 7 taps.


## Difficulty calibration vs. original Dancing Line (11:48 steering)

Chart change in this pass: 295 -> **323 taps** (+17 taps from 8th-triplet fill bursts tagged `fill-triplet` replacing beat interiors, 12 off-beat 16th syncopations tagged `synco-16th`).

| metric | this chart |
|---|---|
| avg CPM = taps / full audio length x 60 | **88** (323 taps / 219.0 s) |
| avg CPM over the playable span (first->last tap) | 94 |
| wiki-style avg CPM (mean of instantaneous 60/gap) | **145** (median 125) |
| peak CPM = 60 / min gap | **375** (min gap 160 ms at 76.66 s) |
| sustained 4-tap peak (3 gaps) | 375 CPM from 138.10 s |
| tightest engine judgment window | ±72 ms at 76.66 s (local gap 160 ms); half-gap rule violations: 0 |

Originals (dlfm-wiki): The Racing avg 220 / peak 440 · The Chaos 136 / 408 · Chinese Garden 148 / 296 (window ±45.8 ms) · Amusement Park peak 512 · Storm peak 460 · Winter 140 / 280 · Piano 125 / 250 · Autumn avg 96.


Audio: `public/audio/how-sweet.mp3`, full length 219.03 s, used as-is. Tempo 125.00 BPM (constant), grid bar0 = 0.339 s, bar = 1.9200 s.
## Counts
| | legacy v1 | new |
|---|---|---|
| taps | 133 | **323** (2.43x) |
| avg taps/s | 0.61 | 1.47 |
| min gap | 0.893 s | 0.160 s |
| fastest run (gaps <= 0.30 s) | - | 8 taps from 198.09 s |
| longest run at the minimum gap (0.160 s) | - | 4 taps from 76.66 s |

Recommended judgment window: **perfect ±45 ms, good ±85 ms, miss beyond ±110 ms** (min gap 0.239 s (8th at 125 BPM); good window +/-85 ms keeps neighbouring taps unambiguous).
Humanly playable floor used: no two taps closer than 0.160 s (one 8th note).

## Per-section density

| section | kind | start | end | taps | taps/s | max run (<=0.30 s) |
|---|---|---|---|---|---|---|
| Intro | intro | 0.34 | 8.02 | 5 | 0.65 | 1 |
| Verse 1 | verse | 8.02 | 38.74 | 32 | 1.04 | 2 |
| Pre-chorus 1 | pre | 38.74 | 46.42 | 16 | 2.08 | 4 |
| Chorus 1 | chorus | 46.42 | 77.14 | 52 | 1.69 | 5 |
| Verse 2 | verse | 77.14 | 107.86 | 29 | 0.94 | 2 |
| Chorus 2 | chorus | 107.86 | 138.58 | 55 | 1.79 | 5 |
| Bridge | bridge | 138.58 | 153.94 | 18 | 1.17 | 2 |
| Build | pre | 153.94 | 169.29 | 38 | 2.47 | 5 |
| Final chorus | chorus | 169.29 | 200.01 | 71 | 2.31 | 8 |
| Outro | outro | 200.01 | 219.03 | 7 | 0.37 | 1 |

## Sync measurement

For every tap the nearest transient in the **full mix** (band chosen by the tap's tag: 40–180 Hz for kick/bass, 300–3000 Hz for vocal/melody, 1.5–10 kHz for clap/hat; max-slope of the band envelope within ±60 ms) was measured. Salient transients found for 122/295 taps (the rest sit on soft vocal/synth onsets with no sharp attack). Offset = transient − tap: median -4.3 ms, median |offset| 4.8 ms, 90th percentile |offset| 15.1 ms.

| section | measured | median offset ms | median abs ms |
|---|---|---|---|
| Intro | 2 | -6.0 | 6.0 |
| Verse 1 | 11 | +0.5 | 1.5 |
| Pre-chorus 1 | 4 | -10.2 | 10.2 |
| Chorus 1 | 20 | -9.6 | 9.6 |
| Verse 2 | 10 | -0.3 | 1.4 |
| Chorus 2 | 24 | -5.1 | 5.1 |
| Bridge | 9 | +4.3 | 13.0 |
| Build | 14 | -2.4 | 6.8 |
| Final chorus | 27 | -9.2 | 9.2 |
| Outro | 1 | -18.9 | 18.9 |

Cross-check on separated stems (demucs; times corrected −50 ms): 318/323 taps have a stem onset (drums/bass/vocals/other, strength > 0.35) within ±60 ms; median offset +2.0 ms, 90th pct |offset| 13.3 ms. Section-boundary taps are listed below.

## Spot checks (start / section changes / middle / end)

| tap t (s) | section | grid position | tagged event | band | measured offset ms |
|---|---|---|---|---|---|
| 2.259 | Intro | bar 1 slot 0/16 | bass | lo | n/a (soft onset) |
| 3.699 | Intro | bar 1 slot 12/16 | melody | mid | -5.9 |
| 4.179 | Intro | bar 2 slot 0/16 | bass | lo | n/a (soft onset) |
| 5.619 | Intro | bar 2 slot 12/16 | kick | lo | n/a (soft onset) |
| 8.019 | Verse 1 | bar 4 slot 0/16 | kick | lo | n/a (soft onset) |
| 9.939 | Verse 1 | bar 5 slot 0/16 | kick | lo | n/a (soft onset) |
| 38.738 | Pre-chorus 1 | bar 20 slot 0/16 | vocal | mid | -0.1 |
| 39.218 | Pre-chorus 1 | bar 20 slot 4/16 | vocal | mid | -15.6 |
| 46.418 | Chorus 1 | bar 24 slot 0/16 | kick | lo | n/a (soft onset) |
| 46.778 | Chorus 1 | bar 24 pos 0.75 beats | synco-16th (burst pass) | stem snare | +18.0 (stem) |
| 77.138 | Verse 2 | bar 40 slot 0/16 | melody | mid | -2.0 |
| 77.858 | Verse 2 | bar 40 slot 6/16 | kick | lo | n/a (soft onset) |
| 107.857 | Chorus 2 | bar 56 slot 0/16 | kick | lo | n/a (soft onset) |
| 108.577 | Chorus 2 | bar 56 slot 6/16 | kick | lo | n/a (soft onset) |
| 109.777 | Chorus 2 | bar 57 slot 0/16 | kick | lo | n/a (soft onset) |
| 110.977 | Chorus 2 | bar 57 slot 10/16 | kick | lo | n/a (soft onset) |
| 138.576 | Bridge | bar 71 pos 4.00 beats | accent (burst pass) | stem bass | +44.0 (stem) |
| 139.056 | Bridge | bar 72 slot 4/16 | kick | lo | n/a (soft onset) |
| 153.936 | Build | bar 80 slot 0/16 | kick | lo | n/a (soft onset) |
| 154.656 | Build | bar 80 slot 6/16 | kick | lo | n/a (soft onset) |
| 169.295 | Final chorus | bar 88 slot 0/16 | kick | lo | n/a (soft onset) |
| 170.015 | Final chorus | bar 88 slot 6/16 | kick | lo | n/a (soft onset) |
| 201.455 | Outro | bar 104 slot 12/16 | vocal | mid | n/a (soft onset) |
| 203.375 | Outro | bar 105 slot 12/16 | melody | mid | n/a (soft onset) |
| 205.295 | Outro | bar 106 slot 12/16 | melody | mid | n/a (soft onset) |
| 205.775 | Outro | bar 107 slot 0/16 | melody | mid | n/a (soft onset) |
| 206.255 | Outro | bar 107 slot 4/16 | melody | mid | n/a (soft onset) |
| 209.135 | Outro | bar 108 slot 12/16 | vocal | mid | -18.9 |

## How this chart was made (honest method)

1. **Audio analysis** (`analysis.json`): librosa 0.11 on the untouched mp3 + demucs htdemucs stems (drums / bass / vocals / other). Constant-tempo beat grid from a DP beat tracker fitted linearly, then shifted to the measured clap/hat transient (librosa onset envelopes and demucs both lag; demucs by 25 ms). Section boundaries come from checkerboard novelty + agglomerative segmentation, cross-checked with per-bar stem levels (vocal present? drums present? bass present?).
2. **Rhythm vocabulary per section, set by hand** (`specs/<slug>.py` in `_w4_tools`): density target (taps per bar), which stems matter (e.g. vocal weight 1.6 in the Bubble Gum hook, clap/kick in the Supernatural groove), maximum burst length.
3. **Slot selection**: every 16th (8th for Right Now) is scored from the stems; for each bar the best tap set is chosen subject to the min-gap floor, the burst limit and a phrase-repetition bonus (bar 3 of a 4-bar group echoes bar 1 → call-and-response). Automatic output = candidates.
4. **Hand plans / edits**: phrase-end runs and fills (listed in the rationale) are written explicitly; first-tap rule edits.
5. **Verification**: per-tap transient offsets in the full mix + stem-onset coverage (below). I could not *listen* in this environment; tap placement is grounded in measured onsets, stem levels and the song structure, so a human listening pass is still recommended (see "open issues").
