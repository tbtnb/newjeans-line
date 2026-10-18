# Super Shy — 害羞也能带动整座广场 · level design (worker w2)

Files: `chart.json` (388 taps) · `layout.json` (+ `path.nodes`) · `route.png` · `chart-report.md` · `analysis.json` / `analysis-notes.md`.
Cover: Get Up EP (pixel characters + colour trails). No `codex-ref/` existed for this song when written; palette is my own.

## Concept / grounding
- Song: 150 BPM, breakbeat/jersey-club drums under a shy, airy vocal. Haerin (GRAMMY): she relates to the lyric and notes the contrast between shy words and strong, dynamic choreography. ELLE shoot interview: Portugal location, parks, buses, local dancers, synchronised group dance.
- Level: a small shy signal on a mint street corner gets answered by the neighbourhood — cobblestone alleys, park parasols opening on the kick, a sunken fountain plaza, a Lisbon-style stairway, a hillside tram line, a viewpoint over the whole town, then a big plaza where distant geometric dancers move in sync and a colourful bus leaves. Tension comes from rhythm; the scenery stays sunny.
- Palette: mint sky `#A8E6D8`, cream `#FFF8E8`, road `#FFFDF6` with sand sides `#E2C79E`, line `#FF5C8A`, azulejo blue `#5AA8D8`, tram yellow `#FFD23F`, parasols pink/mint/yellow/blue/peach.

## Core numbers
- Speed 11.0 u/s (8th at 150 BPM = 200 ms = 2.2 u), width 2.0 → 1.9 → 1.8 (verse 2) → 1.9 → **1.7 (final chorus b/c)**.
- **Taps: old 176 → new 388 (×2.20)**, 2.51/s (highest of my four). Densest: Final chorus b 3.44/s, c 3.26/s (4.5/s peak). **Fastest run: 6 consecutive 8ths (200 ms = 5 taps/s) at 142.5, 145.7 and 148.9 s**; the validator's looser definition (gaps ≤ 0.30 s) finds a 10-tap run at 142.2–144.4 s. Min gap 191 ms (snapped 8th).
- Judgment: perfect ±55, **accept ±95 ms** (must stay < 100 ms so 200 ms 8ths never have overlapping windows).
- Levels: 0 → **fall −4** into the sunken fountain plaza (64.4 s) → **ramp +6** up the stairway (70.9–77.0) → ramp −2 downhill (106–115) → **jump +3** onto the final plaza stage (115.6) → fall −3 (141.2). Real overpass: the viewpoint (Break 2, y +2, 103 s) is directly **above** the sunken fountain plaza path (y −4, 67 s) — from the viewpoint you look down on where you were.

## Section plan
| t | section | route / space | camera | performance |
|---|---|---|---|---|
| 0–13.2 | Intro · 薄荷街角 | short staircase from a mint corner; kick on 2 and 3+ | `low` | small bike; flags only half visible |
| 13.2–38.8 | Verse 1 · 石砖小巷 | **meander** through narrow cobblestone alleys between tiled facades (skippy kick 4/7/10/14) | iso, yaw 60 at bar 16 | azulejo facades (row, `react: tap`) rise on the verse downbeat |
| 38.8–64.4 | Chorus 1 · 公园遮阳伞 | park opens, long staircase, jersey kick + 8th kick rolls closing each 4 bars | `high` | 10 parasols **unfold** 1.2 s ahead and bounce on the kick; petals |
| 64.4–70.8 | Break · 下沉喷泉广场 | **fall −4**, meander around the fountain, vocal-only taps | `wide` | fountain rises, bubbles on the beat; crown 1 at 66.0 s |
| 70.8–77.2 | Build · 里斯本阶梯 | **ramp +6** stairway, kick on 2/4 densifying to 8ths | `side` | stair railing |
| 77.2–102.8 | Verse 2 · 山坡电车 | meander along the hillside; yellow tram runs parallel off-road | `side` → iso | warm afternoon palette |
| 102.8–106.0 | Break 2 · 观景台 | viewpoint above the plaza; whole town (5×5 blocks) below | `wide` dist 34 | crown 2 at 103.5 s |
| 106.0–115.6 | Verse 3 · 下坡 | ramp −2 downhill, staircase | iso | — |
| 115.6–128.4 | Final chorus · 广场集体舞 | **jump +3** onto the plaza | `high`, shake 0.1 | five distant dancers pop in and move on the beat (≥ 14 u off-road); confetti |
| 128.4–141.2 | Final chorus b · 喷泉 | width 1.7, 6-tap kick rolls | iso | big fountain pulses every half note |
| 141.2–154.7 | Final chorus c · 巴士 | fall −3, alternating 5- and 7-tap bars (hardest) | `wide` → `close` → `high` | colourful bus appears; greeting card flips face-up at the end |

## Landmarks & eggs
Landmarks: corner bike, azulejo alleys, parasol park, sunken fountain, stairway, yellow tram, viewpoint town, synchronised dancers, plaza fountain, rainbow-window bus, greeting card.
Eggs: **E1** a mini bunny hiding behind a parasol (≈43 s) returns at the end waving openly (≈151 s); **E2** the bike bell wobbles silently with the player's taps on the final straight (no sound, so it never disturbs the beat).

## Collectibles
Diamonds: 5.0, 22.6, 47.8, 67.3, 74.6, 86.4, 104.3, 112.4, 124.6, 127.8 s. Crowns: 66.0 s, 103.5 s.

## Readability
No hints. Parasols/dancers/fountains react to kick/beat; facades & bell to real taps. Reveal lead ≥ 1.3 s (drop reveal in the final chorus is 1.3 s — the hardest readability point, kept ≥ 1.2 s rule). Widest gaps (breaks) are vocal-led and ≥ 0.4 s.
