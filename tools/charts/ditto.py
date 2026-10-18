"""Ditto (NewJeans, 133.98 BPM). Hand-authored chart on the fitted grid (bar = 1.791 s, beat0 = 0.293 s).
Section map derived from tools/audio/grid.py ditto (kick/snare/mid/full 16th rows) + loudness.
Every pattern below names the musical event it follows."""
from common import Grid, Chart
g = Grid('ditto'); c = Chart('ditto', g)

# --- Intro: choir 'woo-ooh', sporadic low kick. Long straights, one tap per bar on the bar's kick.
c.section(0, 'Intro · 雪原', 'intro')
for b in [2, 3, 4, 5, 6]: c.bar(b, [0], 'kick')
c.bar(4, [8], 'melody'); c.bar(6, [8], 'melody')
c.bar(7, [0, 8, 12], 'kick')                      # 7: 'O....   O..' + hat pickup at 12

# --- Hook A: Baltimore-club beat enters (bar 8). Kick accents at steps 3/6/12/15 (dotted-8th feel).
c.section(8, 'Hook · 雪林', 'verse')
for b in [8, 9, 10, 11]: c.bar(b, [0, 6, 12], 'kick')          # 1, a-of-2, 4
for b in [12, 13, 14]: c.bar(b, [0, 3, 6, 12], 'kick')        # add the 'e-and' syncopation
c.bar(15, [0, 2, 4, 6, 8, 10, 12], 'snare')                  # bar 15: full-band 8th fill (### row)

# --- Verse: kick on beats, snare/vocal on 8ths.
c.section(16, 'Verse · 校舍', 'verse')
for b in [16, 17, 18, 20, 22]: c.bar(b, [0, 4, 11], 'kick')   # '#...#......#' (11 = 'a' of 3)
for b in [19, 21]: c.bar(b, [0, 4, 8, 11, 14], 'kick')
c.bar(23, [4, 8, 11, 14], 'kick')
c.section(24, 'Verse b · 走廊', 'verse')
for b in [24, 26]: c.bar(b, [0, 3, 6, 8, 12], 'snare')
for b in [25, 27]: c.bar(b, [0, 3, 6, 9, 12], 'kick')        # dotted-8th chain (3-step spacing) on the kick
c.bar(28, [0, 3, 6, 12, 14], 'kick'); c.bar(29, [0, 4, 8, 10, 12], 'snare'); c.bar(30, [0, 3, 6, 9, 12], 'kick')

# --- Pre-chorus: band drops out, kick on beats only -> breathing room, long lines.
c.section(31, 'Pre · 体育馆', 'pre')
c.bar(31, [0, 12], 'kick'); c.bar(32, [0, 8], 'kick'); c.bar(33, [0, 8, 11], 'kick'); c.bar(34, [4, 8], 'kick')
c.bar(35, [0, 4, 8], 'kick'); c.bar(36, [0, 8, 11], 'kick'); c.bar(37, [4, 8, 11, 14], 'kick'); c.bar(38, [0, 4, 8], 'kick')
c.bar(39, [0, 4, 8, 10, 12, 14], 'snare')                   # build: 8th run into the drop

# --- Chorus 1: 'I got no time to lose' — vocal 8ths + kick.
c.section(40, 'Chorus · 雪桥', 'chorus')
for b in range(40, 48):
    if b % 2 == 0: c.bar(b, [0, 4, 6, 10, 12, 14], 'vocal')
    else: c.bar(b, [0, 3, 6, 8, 12], 'kick')

# --- Post-chorus: 'Stay in the middle' groove, kick 0/11/15 snare 6/11. Four 4-bar phrases with variation.
c.section(48, 'Post · Stay in the middle', 'post')
P = [[0, 6, 11], [0, 6, 11, 14], [0, 6, 11], [0, 4, 6, 8, 11, 14],
     [0, 3, 6, 11], [0, 6, 11, 14], [0, 3, 6, 11], [0, 6, 8, 10, 12, 14],
     [0, 6, 11, 14], [0, 6, 11, 14], [0, 6, 11, 14], [0, 2, 4, 6, 11, 14],
     [0, 3, 6, 9, 12], [0, 6, 11, 14], [0, 3, 6, 9, 12], [0, 4, 6, 8, 10, 12]]
for i, steps in enumerate(P): c.bar(48 + i, steps, 'kick' if i % 4 != 3 else 'fill')

# --- Verse 2 / bridge: thinner groove, snare 8ths soft.
c.section(64, 'Bridge · 冰湖', 'bridge')
for b in [64, 66, 68]: c.bar(b, [0, 6, 12], 'kick')
for b in [65, 67, 69]: c.bar(b, [0, 8], 'snare')
c.bar(70, [0, 6, 12], 'kick')
c.section(71, 'Break · 夜', 'break')
c.bar(71, [0], 'kick'); c.bar(72, [0, 12], 'snare'); c.bar(73, [0], 'kick'); c.bar(74, [4, 12], 'snare')
c.bar(75, [4, 15], 'melody'); c.bar(76, [3, 8], 'fx'); c.bar(77, [3, 12], 'melody')
c.bar(78, [0, 4, 8, 10, 12], 'snare')                    # 'o   o .ooooo#' build into the last chorus

# --- Final chorus: heaviest kick section; density peak with two 8-tap 8th runs.
c.section(79, 'Final · 黎明', 'chorus')
F = [[0, 4, 6, 8, 11, 14], [0, 4, 8, 11, 14], [0, 3, 6, 8, 12, 14], [0, 4, 8, 11, 14],
     [0, 4, 6, 8, 11, 14], [0, 4, 8, 11, 14], [0, 3, 6, 8, 12, 14], [0, 2, 4, 6, 8, 10, 12, 14],
     [0, 4, 6, 8, 11, 14], [0, 4, 8, 11, 14], [0, 3, 6, 8, 12, 14], [0, 2, 4, 6, 8, 10, 12, 14],
     [0, 4, 6, 8, 11, 14], [0, 4, 8, 11, 14], [0, 3, 6, 9, 12], [0, 4, 8, 12], [0, 2, 4, 6, 8, 10, 12, 14]]
for i, steps in enumerate(F): c.bar(79 + i, steps, 'kick' if len(steps) < 8 else 'run')

# --- Outro: choir chords on half-bars, thinning out.
c.section(96, 'Outro · 光', 'outro')
for b in [96, 97, 98, 99]: c.bar(b, [0, 8], 'melody')
c.bar(100, [0], 'melody'); c.bar(101, [0], 'melody')
for bar, way in [(8, 'cw'), (16, 'ccw'), (24, 'ccw'), (31, 'cw'), (40, 'cw'), (48, 'ccw'), (56, 'ccw'), (60, 'cw'),
                 (64, 'cw'), (71, 'ccw'), (79, 'ccw'), (87, 'cw'), (91, 'cw'), (96, 'ccw')]:
    c.rotate(bar, way)
c.save(notes='Hand-authored on fitted grid; see docs/design/levels/ditto.md')
