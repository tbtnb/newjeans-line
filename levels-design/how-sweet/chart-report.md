# How Sweet — chart report

> Note: the rationale below describes the curated basis chart. It was written before the 11:55 rhythmic-logic audit. Where it differs (for example, verse taps that followed vocals are now on the drum layer), the audit section and the per-section *what the taps follow* table are authoritative.


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


## Rhythmic-logic audit (user override 11:55) and difficulty

Rules applied by `_w4_tools/audit.py` to the curated chart (295 taps): one audible layer per section; repeated phrases get one shared pattern; 16th bursts only where the 16th figure is prominent in the **full mix** (not just a stem), starting and ending on beats; breathing room kept; no taps on faint onsets. The stem-only triplet/syncopation taps from the previous pass were dropped. Result: **307 taps**.

- removed as off-layer (no audible hit of the section's layer within ±35 ms): 3 — 60.82, 76.18, 122.26
- removed as faint (full-mix onset < 0.7× median strength in both the tag band and broadband): 6 — 134.74, 137.62, 168.34, 176.01, 183.69, 199.06
- re-tagged to the section layer (they coincide with an audible hit of that layer): 25
- bars unified to a shared pattern (same phrase in another instance or 4 bars earlier, every added slot verified audible): 70
- 16th bursts: 4 at 38.26 s (Verse 1, full-mix strength 1.15× median); 45.94 s (Pre-chorus 1, full-mix strength 1.06× median); 153.46 s (Bridge, full-mix strength 1.07× median); 161.14 s (Build, full-mix strength 1.16× median)

### What the taps follow, per section

| section | layer the taps follow |
|---|---|
| Intro | the synth-bass/melody stabs of the intro (one per bar) |
| Verse 1 | kick pattern + clap; ends with a full-mix 16th hat/snare fill into the pre-chorus |
| Pre-chorus 1 | kick on the beat, clap answer; a 16th fill on the last beat into the chorus |
| Chorus 1 | kick + clap backbeat |
| Verse 2 | Verse-1 drum pattern (shared) |
| Chorus 2 | Chorus-1 pattern (shared bar for bar where audible) |
| Bridge | half-density clap/kick; 16th fill at the end into the build |
| Build | kick + clap, rising; one 16th fill at the 4-bar phrase end |
| Final chorus | Chorus-1 pattern again, densest |
| Outro | melody stabs only, sparse |

### Difficulty (soft references, not quotas)

| metric | this chart |
|---|---|
| avg CPM = taps / full audio length x 60 | **84** (307 taps / 219.0 s) |
| avg CPM over the playable span (first->last tap) | 88 |
| wiki-style avg CPM (mean of instantaneous 60/gap) | **137** (median 83) |
| peak CPM = 60 / min gap | **500** (min gap 120 ms at 38.26 s) |
| sustained 4-tap peak (3 gaps) | 500 CPM from 38.26 s |
| tightest engine judgment window | ±54 ms at 38.26 s (local gap 120 ms); half-gap rule violations: 0 |

Originals (dlfm-wiki): The Racing avg 220 / peak 440 · The Chaos 136 / 408 · Chinese Garden 148 / 296 (window ±45.8 ms) · Amusement Park peak 512 · Storm peak 460 · Winter 140 / 280 · Piano 125 / 250 · Autumn avg 96.


Audio: `public/audio/how-sweet.mp3`, full length 219.03 s, used as-is. Tempo 125.00 BPM (constant), grid bar0 = 0.339 s, bar = 1.9200 s.
## Counts
| | legacy v1 | new |
|---|---|---|
| taps | 133 | **307** (2.31x) |
| avg taps/s | 0.61 | 1.40 |
| min gap | 0.893 s | 0.120 s |
| fastest run (gaps <= 0.30 s) | - | 7 taps from 45.46 s |
| longest run at the minimum gap (0.120 s) | - | 5 taps from 38.26 s |

Judgment window (schema v2.5 engine rule, per tap): **PERFECT ±40 ms; window = min(0.5·g, clamp(0.45·g, 45, 110 ms))**, so the tightest is ±54 ms and sparse taps get ±110 ms (min tap gap 0.120 s -> tightest window ±54 ms (always <= half the local gap); sparse taps ±110 ms.).
Minimum tap gap: 0.120 s (a 16th-note fill).

## Per-section density

| section | kind | start | end | taps | taps/s | max run (<=0.30 s) |
|---|---|---|---|---|---|---|
| Intro | intro | 0.34 | 8.02 | 5 | 0.65 | 1 |
| Verse 1 | verse | 8.02 | 38.74 | 38 | 1.24 | 5 |
| Pre-chorus 1 | pre | 38.74 | 46.42 | 17 | 2.21 | 6 |
| Chorus 1 | chorus | 46.42 | 77.14 | 49 | 1.60 | 4 |
| Verse 2 | verse | 77.14 | 107.86 | 33 | 1.07 | 2 |
| Chorus 2 | chorus | 107.86 | 138.58 | 51 | 1.66 | 4 |
| Bridge | bridge | 138.58 | 153.94 | 19 | 1.24 | 4 |
| Build | pre | 153.94 | 169.29 | 27 | 1.76 | 6 |
| Final chorus | chorus | 169.29 | 200.01 | 60 | 1.95 | 4 |
| Outro | outro | 200.01 | 219.03 | 8 | 0.42 | 1 |

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

Cross-check on separated stems (demucs; times corrected −50 ms): 306/307 taps have a stem onset (drums/bass/vocals/other, strength > 0.35) within ±60 ms; median offset +2.0 ms, 90th pct |offset| 10.0 ms. Section-boundary taps are listed below.

## Spot checks (start / section changes / middle / end)

| tap t (s) | section | grid position | tagged event | band | measured offset ms |
|---|---|---|---|---|---|
| 2.259 | Intro | bar 1 slot 0/16 | bass | lo | n/a (soft onset) |
| 3.699 | Intro | bar 1 slot 12/16 | kick | mid | -5.9 |
| 4.179 | Intro | bar 2 slot 0/16 | bass | lo | n/a (soft onset) |
| 5.619 | Intro | bar 2 slot 12/16 | kick | lo | n/a (soft onset) |
| 8.019 | Verse 1 | bar 4 slot 0/16 | kick | lo | n/a (soft onset) |
| 8.739 | Verse 1 | bar 4 pos 1.50 beats | kick (burst pass) | stem other | -0.0 (stem) |
| 38.738 | Pre-chorus 1 | bar 20 slot 0/16 | kick | mid | -0.1 |
| 39.218 | Pre-chorus 1 | bar 20 slot 4/16 | kick | mid | -15.6 |
| 46.418 | Chorus 1 | bar 24 slot 0/16 | kick | lo | n/a (soft onset) |
| 47.138 | Chorus 1 | bar 24 slot 6/16 | kick | lo | n/a (soft onset) |
| 77.138 | Verse 2 | bar 40 slot 0/16 | kick | mid | -2.0 |
| 77.858 | Verse 2 | bar 40 slot 6/16 | kick | lo | n/a (soft onset) |
| 107.857 | Chorus 2 | bar 56 slot 0/16 | kick | lo | n/a (soft onset) |
| 108.577 | Chorus 2 | bar 56 slot 6/16 | kick | lo | n/a (soft onset) |
| 109.297 | Chorus 2 | bar 56 pos 3.00 beats | clap (burst pass) | stem snare | -4.0 (stem) |
| 109.777 | Chorus 2 | bar 57 slot 0/16 | kick | lo | n/a (soft onset) |
| 139.056 | Bridge | bar 72 slot 4/16 | kick | lo | n/a (soft onset) |
| 140.016 | Bridge | bar 72 slot 12/16 | kick | lo | n/a (soft onset) |
| 153.936 | Build | bar 80 slot 0/16 | kick | lo | n/a (soft onset) |
| 154.656 | Build | bar 80 slot 6/16 | kick | lo | n/a (soft onset) |
| 169.295 | Final chorus | bar 88 slot 0/16 | kick | lo | n/a (soft onset) |
| 170.015 | Final chorus | bar 88 slot 6/16 | kick | lo | n/a (soft onset) |
| 201.455 | Outro | bar 104 slot 12/16 | vocal | mid | n/a (soft onset) |
| 203.375 | Outro | bar 105 slot 12/16 | melody | mid | n/a (soft onset) |
| 205.775 | Outro | bar 107 slot 0/16 | melody | mid | n/a (soft onset) |
| 206.255 | Outro | bar 107 slot 4/16 | melody | mid | n/a (soft onset) |
| 209.135 | Outro | bar 108 slot 12/16 | vocal | mid | -18.9 |
| 211.055 | Outro | bar 109 pos 3.00 beats | melody (burst pass) | stem other | +11.0 (stem) |

## How this chart was made (honest method)

1. **Audio analysis** (`analysis.json`): librosa 0.11 on the untouched mp3 + demucs htdemucs stems (drums / bass / vocals / other). Constant-tempo beat grid from a DP beat tracker fitted linearly, then shifted to the measured clap/hat transient (librosa onset envelopes and demucs both lag; demucs by 25 ms). Section boundaries come from checkerboard novelty + agglomerative segmentation, cross-checked with per-bar stem levels (vocal present? drums present? bass present?).
2. **Rhythm vocabulary per section, set by hand** (`specs/<slug>.py` in `_w4_tools`): density target (taps per bar), which stems matter (e.g. vocal weight 1.6 in the Bubble Gum hook, clap/kick in the Supernatural groove), maximum burst length.
3. **Slot selection**: every 16th (8th for Right Now) is scored from the stems; for each bar the best tap set is chosen subject to the min-gap floor, the burst limit and a phrase-repetition bonus (bar 3 of a 4-bar group echoes bar 1 → call-and-response). Automatic output = candidates.
4. **Hand plans / edits**: phrase-end runs and fills (listed in the rationale) are written explicitly; first-tap rule edits.
5. **Verification**: per-tap transient offsets in the full mix + stem-onset coverage (below). I could not *listen* in this environment; tap placement is grounded in measured onsets, stem levels and the song structure, so a human listening pass is still recommended (see "open issues").
