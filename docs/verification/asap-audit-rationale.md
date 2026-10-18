# ASAP: why 201 → 162 taps (integ-b rhythm-logic audit)

ASAP is the softest track on *Get Up*: a pad-led, swung 130 BPM groove whose first chorus and pre-chorus have no full drum kit. W3 charted it before the rule *rhythm logic beats density* and placed many taps on the 16th grid where the full mix has no onset. Strengths below are per-band onset strengths (0–1.5, normalised to the song's 99.5th percentile; < 0.35 = faint, ≥ 0.6 = clear), max within ±30 ms of the tap.

**Result:** 39 taps removed, 4 re-timed by one 16th onto the clear hit of the same layer, **0 added**. That gives 162 taps: 2.0× the legacy 83 and 72 CPM on average (peak 360 CPM in the dance break).

**Is it over-pruned?** No tap that lands on a clear hit of its section's layer was removed. The losses are concentrated where the music is genuinely sparse:

- Chorus 1 (41–56 s): 12 of 26 removed. In the full mix this chorus has almost no clear onsets: median full-mix strength 0.19, and only 3 cells per bar reach 0.6, all at other positions. It is a breathing chorus, so it stays sparse. Chorus 2, which brings the kit in, keeps 32 taps.
- Pre (26–41 s): 8 of 16 removed (7 faint hat taps, 1 weak burst). The pre is a soft vocal call-and-response.
- Final hook (120–130 s): 7 of 17 removed. The sustained chords there leave few hits.

The difficulty comes from the dance break (36 taps in 14.8 s, 9-tap 8th runs) and Chorus 2. Where the song is calm, the level is calm too, as in the original game's slow levels; The Autumn averages about 96 CPM. Raising ASAP further would mean tapping on silence. If a human listening pass hears hits that the envelopes miss (for example the soft vocal "ASAP" chops in Chorus 1), those can be re-charted on the vocal layer.

| t (s) | section | tag | decision | followed layer | layer str. | full str. | why |
|---|---|---|---|---|---|---|---|
| 5.187 | Verse 1 · moon-green meadow | kick | re-timed to 5.302 | drums | 0.31 | 0.16 | faint: the intended hit is one 16th away (clear onset of the same layer), so the tap was moved onto it |
| 14.186 | Verse 1b · clock in the sky | kick | removed | drums | 0.10 | 0.05 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 25.493 | Verse 1b · clock in the sky | vocal | removed | drums | 0.28 | 0.05 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 29.877 | Pre · letters behind trees | vocal | removed | hat | 0.27 | 0.27 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 30.800 | Pre · letters behind trees | vocal | re-timed to 30.684 | hat | 0.22 | 0.14 | faint: the intended hit is one 16th away (clear onset of the same layer), so the tap was moved onto it |
| 34.723 | Pre · letters behind trees | bass | removed | hat | 0.30 | 0.12 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 34.838 | Pre · letters behind trees | snare | removed | hat | 0.42 | 0.49 | weak-burst: 16th-note burst tap on an onset that is not clear in the full mix (a burst must be audible) |
| 35.415 | Pre · letters behind trees | vocal | removed | hat | 0.25 | 0.23 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 37.261 | Pre · letters behind trees | bass | removed | hat | 0.23 | 0.26 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 38.184 | Pre · letters behind trees | kick | removed | hat | 0.28 | 0.13 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 39.107 | Pre · letters behind trees | bass | removed | hat | 0.23 | 0.08 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 42.107 | Chorus 1 · swing of pendulums | vocal | removed | drums | 0.31 | 0.12 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 42.799 | Chorus 1 · swing of pendulums | bass | removed | drums | 0.32 | 0.32 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 47.183 | Chorus 1 · swing of pendulums | vocal | removed | drums | 0.23 | 0.18 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 48.337 | Chorus 1 · swing of pendulums | kick | removed | drums | 0.31 | 0.30 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 49.491 | Chorus 1 · swing of pendulums | vocal | removed | drums | 0.29 | 0.13 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 50.183 | Chorus 1 · swing of pendulums | bass | removed | drums | 0.32 | 0.26 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 52.952 | Chorus 1 · swing of pendulums | vocal | removed | drums | 0.26 | 0.17 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 54.567 | Chorus 1 · swing of pendulums | vocal | removed | drums | 0.22 | 0.16 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 54.798 | Chorus 1 · swing of pendulums | vocal | removed | drums | 0.18 | 0.11 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 55.028 | Chorus 1 · swing of pendulums | bass | removed | drums | 0.21 | 0.11 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 55.259 | Chorus 1 · swing of pendulums | bass | removed | drums | 0.21 | 0.06 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 55.490 | Chorus 1 · swing of pendulums | bass | removed | drums | 0.33 | 0.06 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 71.412 | Verse 2 · water garden | bass | removed | drums | 0.30 | 0.23 | off-layer: the followed layer is silent here; the hit belongs to another instrument, so the tap would hop layers |
| 75.565 | Dance break · stars in groups | hat | removed | drums | 0.34 | 0.52 | off-layer: the followed layer is silent here; the hit belongs to another instrument, so the tap would hop layers |
| 81.103 | Dance break · stars in groups | vocal | re-timed to 80.987 | drums | 0.27 | 0.04 | faint: the intended hit is one 16th away (clear onset of the same layer), so the tap was moved onto it |
| 82.949 | Dance break · stars in groups | hat | removed | drums | 0.33 | 0.24 | off-layer: the followed layer is silent here; the hit belongs to another instrument, so the tap would hop layers |
| 90.333 | Turnaround | vocal | removed | mid | 0.17 | 0.13 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 91.371 | Turnaround | hat | re-timed to 91.486 | mid | 0.12 | 0.54 | off-layer: the intended hit is one 16th away (clear onset of the same layer), so the tap was moved onto it |
| 99.332 | Chorus 2 · the small house | bass | removed | drums | 0.26 | 0.21 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 106.716 | Chorus 2 · the small house | vocal | removed | drums | 0.59 | 0.14 | weak-burst: 16th-note burst tap on an onset that is not clear in the full mix (a burst must be audible) |
| 106.831 | Chorus 2 · the small house | hat | removed | drums | 0.44 | 0.11 | weak-burst: 16th-note burst tap on an onset that is not clear in the full mix (a burst must be audible) |
| 114.100 | Chorus 2 · the small house | vocal | removed | drums | 0.24 | 0.07 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 114.215 | Chorus 2 · the small house | hat | removed | drums | 0.32 | 0.14 | off-layer: the followed layer is silent here; the hit belongs to another instrument, so the tap would hop layers |
| 114.331 | Chorus 2 · the small house | vocal | removed | drums | 0.49 | 0.06 | weak-burst: 16th-note burst tap on an onset that is not clear in the full mix (a burst must be audible) |
| 114.792 | Hush · lamp flickers | bass | removed | drums | 0.34 | 0.07 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 121.715 | Final hook · lamp lights | vocal | removed | drums | 0.16 | 0.06 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 123.330 | Final hook · lamp lights | snare | removed | drums | 0.49 | 0.58 | weak-burst: 16th-note burst tap on an onset that is not clear in the full mix (a burst must be audible) |
| 123.445 | Final hook · lamp lights | hat | removed | drums | 0.29 | 0.12 | weak-burst: 16th-note burst tap on an onset that is not clear in the full mix (a burst must be audible) |
| 125.868 | Final hook · lamp lights | bass | removed | drums | 0.28 | 0.22 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 126.791 | Final hook · lamp lights | vocal | removed | drums | 0.30 | 0.24 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 127.022 | Final hook · lamp lights | vocal | removed | drums | 0.27 | 0.11 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
| 127.483 | Final hook · lamp lights | vocal | removed | drums | 0.33 | 0.16 | faint: no audible hit: every band is quiet at this instant (the tap would land between sounds) |
