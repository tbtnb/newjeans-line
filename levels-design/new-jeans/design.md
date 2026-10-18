# New Jeans — 新的我，从方格纸出发 · level design (worker w2)

Files: `chart.json` (167 taps) · `layout.json` (+ `path.nodes`) · `route.png` · `chart-report.md` · `analysis.json` / `analysis-notes.md`.
Cover: this track opens the **Get Up** EP — use the Get Up cover (five pixel Powerpuff-style characters with colour trails), *not* the 2022 New Jeans EP bunny. No `codex-ref/` existed for this song when written; palette below is my own and should be re-aligned if one appears.

## Concept / grounding
- Song: 1:49 opener, Baltimore/UK-garage club beat at 134 BPM; MV is the Powerpuff Girls collaboration (members become animated characters, talk about superpowers). Theme "discovering a new me" (Hyein, GRAMMY interview); the superpower adventure here is our own story.
- Level: a tiny pixel dot wakes on graph paper → paper houses pop up → five colour trails launch like superpower streaks → the flat pixel plane → the city rebuilds in 3D → flight → camera pulls back: the whole city was a badge on a denim jacket.
- Palette: paper `#F8F9FB`/`#FDFCF7`, sky `#CFE6FF`, road white with `#9EC3E6` sides, line `#1F6FD1`; five trail colours `#FF7EB6 #5AA8FF #5AD69A #FFD23F #A98BFF`; outro denim `#3D5F8F` with gold stitching `#F2C94C`.

## Core numbers
- Speed 10.2 u/s, width 2.2 → 2.0 (chorus 1) → 1.8 (chorus 2) → 2.2 (outro).
- **Taps: old 68 → new 167 (×2.46)**, 1.53/s. The old chart was anomalously sparse (0.62 taps/s, first tap at 7.96 s, difficulty 1/5) relative to an energetic club track, so this one goes past 2× — verses still sit at only 2–3 taps per bar; if the integrator wants ≤ 2×, drop the snare taps on beat 2 in the verses (−12) and the downbeat snares in chorus 2 (−4) → ~150.
- Densest: Chorus 2 2.3/s, Rebuild 2.2/s (3.5/s peaks). **Fastest run: 6 consecutive 8ths (224 ms) at 63.3–64.4 s**, 5-tap kick roll at 99.7 s. Min gap 222 ms. Judgment: perfect ±60, accept ±115 ms.
- Levels: 0 → **jump +3** at chorus 1 (36.2 s) → **fall −6** at the break (50.5 s, onto the pixel plane at −3) → ramp +3 → **jump +4** at chorus 2 (86.3 s, flight) → fall −4 into the outro. Real overpasses: the break/rebuild path on the pixel plane (y −3, 48–63 s) runs **underneath** the Verse 1 paper-house route (y 0) — the paper city literally sits on top of the flat plane.

## Section plan
| t | section | route / space | camera | performance |
|---|---|---|---|---|
| 0–7.5 | Intro · 方格纸 | **meander** with long segments = a pixel-step blueprint line on graph paper; 8 taps on synth stabs | `top` (flat, paper-like) | road `fade` in, pencil-grey palette, grid lines on the paper, giant pencil prop |
| 7.5–14.7 | Beat in · 蓝图线 | staircase, snare accents | → `iso` | road turns white and the line blue on the downbeat (colour event) |
| 14.7–36.2 | Verse 1 · 纸片房屋 | meander through a block of paper houses (2-step kick 0/10) | iso | houses **unfold** up from the page 1.5 s ahead and bounce on the kick |
| 36.2–50.5 | Chorus 1 · 五色尾迹 | **jump +3**, staircase on the jersey kick | `high`, then yaw 60 | five colour trails grow into the sky on successive beats (bodies ≥ 7 u above road) and fade at the break; pixel particles burst |
| 50.5–57.7 | Break · 像素平面 | **fall −6** onto the flat pixel plane; off-beat claps | `top` | big pixel heart pops and beats; road `static` (fully visible – readability during syncopation) |
| 57.7–64.8 | Rebuild · 重新立起 | meander, "..s.k" call/response, 6-tap 8th run | iso | — |
| 64.8–86.3 | Verse 2 · 立体城市 | ramp +3, meander between rising towers | `side` → iso | 6 towers rise 1.8 s ahead; "toy city" landmark |
| 86.3–100.6 | Chorus 2 · 飞行 | **jump +4**, width 1.8 | `wide` then `low` | confetti burst |
| 100.6–109.0 | Outro · 牛仔徽章 | fall −4, last straight | `high` dist 34 slow pull-back | ground turns denim, a huge badge disc under the area, gold stitch rows both sides |

## Landmarks & eggs
Landmarks: pencil, paper houses (5 colours), five superpower trails, pixel heart, toy city core, denim badge.
Eggs: **E1** a small potted plant that "nods" to the player's taps (MV talk about speaking to plants), 31 s; **E2** a bunny-ear glint in the badge reflection at the very end (107 s).

## Collectibles
Diamonds: 4.3, 11.0, 17.9, 28.7, 45.6, 53.8, 70.7, 80.6, 93.6, 101.9 s. Crowns: 34.9 s (breather before chorus 1) and 81.5 s (before chorus 2).

## Readability
No hints. Paper houses/towers react to kick/beat only; the plant reacts to real taps. Reveal lead ≥ 1.5 s; the break uses a static fully-visible road because every tap there is off-beat.
