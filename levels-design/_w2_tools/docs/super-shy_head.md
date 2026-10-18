# Super Shy — 把心事跳成一座城 · Lisbon afternoon · level design (worker w2, v3/v4)

Files: `chart.json` · `layout.json` (v2.4 + `path.nodes`) · `route.png` · `route-sections.png` · `chart-report.md` · `analysis.json` / `analysis-notes.md` · `art/` (6 images).
**Aligned with codex-ref** (`/workspace/nj-refs/super-shy/`): a blue line hops through a pastel Lisbon-style hill town on a sunny afternoon, the shy feeling turned into a whole city. The blueprint is mood only; the route choreography is ours.

## Concept
- **Song:** the Get Up title track, 2:35, a skippy jersey-club / drum-and-bass-lite beat at 150 BPM. Shy crush, light, bouncy, a little breathless.
- **Level:**
  - the line passes the red bike and bench (A);
  - it zigzags through cobbled alleys and cut-away courtyard walls;
  - it spirals up round the green courtyard (B) to +3 for Chorus 1 under parasols;
  - it drops into the sunken fountain plaza, then spirals up the Lisbon stairway to the +6 market terrace;
  - it wraps through the coral market arcade (D), where the E1 bunny tile sits under a bench;
  - it steps down to the viewpoint and runs downhill to L0;
  - it jumps onto Bridge B over the five-dancer plaza (C), climbs past the teal stepped wall with the five-colour pixel relief (E), then drops to the bus street for the finish.
- **Palette** (codex-ref):

  | use | colour |
  |---|---|
  | sky | `#CDEDF1` |
  | park / ground | `#BEE9C9` |
  | road | `#FFF8ED` |
  | road side wall | `#3B8A89` |
  | player line | `#295BE7` |
  | market roofs / sunlit walls | `#F4A39B` |
  | annotations | `#B1A6E8` |
  | diamonds | `#FF82D0` |
  | crown | `#F7CE63` |

## Core numbers
- **Speed and width:** 11.0 u/s. Width 2.0 → 1.9 (Chorus 1) → 1.8 (Verse 2) → 1.9 (final chorus) → 1.7 (final chorus b).
- **Taps: old 176 → new 396 (×2.25)**, 2.56 taps/s. Avg CPM 154 (taps ÷ length), 192 wiki-style; **peak CPM 395** (min gap 152 ms). 11 fast bursts at fills, build-up and final choruses; 96 dotted-8th gaps. Full comparison with the original levels is in `chart-report.md`.
- **Fastest 8th run:** 6 × 200 ms at 137.1 s; fastest burst 4 taps at 137.56 s (395 CPM).
- **Judgment:** the engine rule (v2.4) gives min ±68 ms (inside bursts) and median ±110 ms, i.e. ≤ half the local minimum gap everywhere.
- **Levels** (codex L0 / +3W / +6W = 0 / +3 / +6): spiral ramp +3 round courtyard B (32.7–38.1 s) → fall −3 into the fountain plaza (64.4 s) → stairway spiral +6 (71.1–76.5 s) → fall −3 to the viewpoint (103.0 s) → downhill ramp −3 (106.3–114.6 s) → jump +3 onto Bridge B (115.0 s) → ramp +3 past the relief wall (128.7–133.2 s) → big fall −6 to the bus street (140.0 s).
- **Checks:** the validator reports 0 same-level overlaps.

## Route choreography (each section has its own texture)
Planner: beam search over per-section motifs plus a drift bearing, using the exact v2.4 overlap rule. The table is computed from the built path.
