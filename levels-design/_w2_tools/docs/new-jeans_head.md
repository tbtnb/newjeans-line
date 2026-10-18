# New Jeans — 城市换新 City Unfolded · level design (worker w2, v3)

Files: `chart.json` (162 taps) · `layout.json` (v2.5 + `path.nodes`) · `route.png` · `route-sections.png` · `chart-report.md` · `analysis.json` / `analysis-notes.md` · `art/` (5 images).
**Aligned with codex-ref** (`/workspace/nj-refs/new-jeans/`): a pink solid line through a light-blue city that keeps unfolding; streets → rooftops → the five flight trails become the skyline. Cover = **Get Up EP digital cover** (pale-blue pixel city, five Powerpuff-style members, five colour trails, small bunny icon top-left). The blueprint shapes are mood only; the route choreography is ours.

## Concept
- **Song:** a 1:49 opener with a Baltimore/UK-garage club beat at 134 BPM. The MV is the Powerpuff Girls collaboration. Theme: renewing yourself, showing a new style, inviting others along. The mood is light, confident and bouncy.
- **Level:**
  - the pink line starts on a blank city plan (graph-paper ground);
  - blocks unfold;
  - the line wraps round the **Bunny Gate**;
  - it climbs an alley ramp onto L1, where a horseshoe of staircases wraps the **sunken city courtyard** while five **flight fins** rise;
  - it drops under the chorus deck (E1 bunny shadow);
  - the city re-rises;
  - the line spirals up the courtyard tower;
  - it flies on L2 above everything;
  - the five trails freeze into the **cover tableau**.
- **Palette** (codex-ref):

  | use | colour |
  |---|---|
  | sky | `#DDF5FF` |
  | ivory road | `#FFF9ED` |
  | city | `#73D5EB` |
  | denim sides | `#397FC0` |
  | ink / road side | `#164A63` |
  | player line | `#F36BA5` |
  | crown | `#F5CA63` |
  | five trail colours | `#F36BA5 #397FC0 #8FDFB7 #F5CA63 #B7A0EA` (mint/peach/lavender from the fins) |

  Diamonds are pink and the crown is gold (`collectibleColors`).

## Core numbers
- **Speed and width:** 10.2 u/s. Width 2.2 → 2.0 (Chorus 1) → 1.8 (Chorus 2) → 2.2 (outro).
- **Taps: old 68 → new 162 (×2.38)**, averaging 1.49/s. The re-audit removed 4 faint synth taps in the intro and 1 in the break. Still above 2× because the old chart was very sparse (0.62/s).
- **Fastest run:** 6 × 8th (224 ms) at 63.3 s (Rebuild). Minimum 8th gap 222 ms.
- **Difficulty (moderate tier, EP opener):** avg CPM 89 (taps ÷ length) / 123 wiki-style. **Peak CPM 300** (validator style), 270 instantaneous. There are no bursts: the only candidate (rapid vocal syllables at 89.3 s) is not clearly audible as a 16th figure in the full mix. Charting rules (user override): one audible layer per section, the same pattern on every repeat of a phrase, bursts only where the 16th figure is audible in the full mix and starts or ends on a beat, breaks stay sparse, no taps on faint or ghost onsets. CPM numbers are references, not quotas. See the per-section 'What the taps follow' table in `chart-report.md`.
- **Judgment:** the engine rule (v2.5, per tap) gives min ±100 ms and median ±110 ms.
- **Levels** (codex L0/L1/L2 = 0/+4/+8): 0 → **alley ramp +4** (31.7–35.8 s, L1) → **fall −4** at the break (50.8 s, L0, under the chorus deck) → **spiral ramp +4** round the courtyard tower (79–83 s, L1) → **ramp +4** into Chorus 2 (86–92 s, L2), and it stays on top to the finish.
- **Checks:** the validator reports 0 same-level overlaps.

## Route choreography (each section has its own texture)
Planner: beam search over per-section motifs plus a drift bearing, using the exact v2.4 overlap rule. The table is computed from the built path.
