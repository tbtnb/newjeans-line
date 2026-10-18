# How rhythm games place taps (charting logic) — research notes

Collected 2026-10-18 for newjeans-line. Every URL below was opened and read. A search on X found nothing useful, so no X posts are cited.

## Sources

### Dancing Line (跳舞的线) itself
- dlfm-wiki, 游戏机制: https://dlfm-wiki.top/wiki/%E6%B8%B8%E6%88%8F%E6%9C%BA%E5%88%B6
  - One tap = one 90° turn. The line moves at a constant speed, so the time between taps is the length of the segment.
- dlfm-wiki, 赛车 (Racing) level page: https://dlfm-wiki.top/wiki/%E8%B5%9B%E8%BD%A6
  - Stats: 110 BPM, 357 taps, average 220 CPM, peak 440 CPM.
  - The wiki calls its dotted-8th and displaced-8th rhythms "极其诡异" (extremely weird).
  - In the last stretch the level charts only the melody. That leaves a half-beat gap on every bar's downbeat chord, which "引起了一些玩家的困惑" (confused some players).
  - Takeaway: players expect the downbeat to be a tap. Leaving it out reads as an off-beat chart.
- dlfm-wiki, 钢琴 (Piano): https://dlfm-wiki.top/wiki/%E9%92%A2%E7%90%B4
  - 125 CPM average, 250 CPM peak. A calm level sits around 2 taps/s.
- Xiaomi game review: https://game.xiaomi.com/viewpoint/51374283_1558963702786_12
  - Turns are synced to the beat, and the music is the timing cue.
- TapTap, 迷宫 (Maze) strategy: https://www.taptap.cn/moment/15229160397998145
  - Tapping early or late shifts the whole line, so picture and audio drift apart. You correct it on the following turns.
  - Takeaway: in this genre any chart or offset error builds up visibly along the route.
- Dancing Line fan-made template: https://github.com/LAM0578/Dancing-Line-Fanmade-Template
  - Fan levels are built from a beatline display plus a global audio-offset calibration. Taps go on the beat grid; latency is a separate setting.

### General rhythm-game charting
- osu! wiki, 乐理 Music theory (zh): https://osu.ppy.sh/wiki/zh/Music_theory
  - Downbeats carry the most weight.
  - Putting long or important objects on upbeats/off-beats is "dangerous" unless the music clearly stresses them.
- osu! Ranking criteria: https://osu.ppy.sh/wiki/en/Ranking_criteria/osu%21
  - Every object must be snapped to a distinct sound in the song.
  - Avoid difficulty spikes the music doesn't justify.
- osu! Rhythm techniques: https://osu.ppy.sh/wiki/en/Beatmapping/Mapping_techniques/Rhythm
  - Follow one rhythm layer at a time and switch layers on purpose.
- BSMG Basic mapping: https://bsmg.wiki/mapping/basic-mapping.html
  - Get the timing (BPM/offset) right first, and only place notes where there is sound.
- BSMG Intermediate mapping: https://bsmg.wiki/mapping/intermediate-mapping.html
  - Pick one instrument (or a few) to follow, and don't jump between them abruptly.
  - Emphasis is relative: a strong sound in a quiet part deserves a note even if the same loudness wouldn't elsewhere.
  - Keep repeated sections consistent and respect the song's structure.
  - For vocals, map the intended rhythm with simple precision rather than every micro-timing.
  - Don't overmap.
- 晨峦, 制谱乐理基础 (music theory for charting): https://chen-luan.github.io/essay/music-theory-foundation-for-charting/
  - Strong beat versus secondary beat.
  - Phrases are usually 4 bars, with a fill (加花) in the last bar.
  - Keep your note choices consistent within a phrase.
- Cytus II charting guide: https://cytus2-charting-guide.kyreflection.com/Basic/Adagietto/
  - Beginner charts follow the main pulse and add subdivisions only where the music clearly plays them.
- Ace of Arrows, ITG/StepMania how-to: http://aceofarrows.weebly.com/how-to-guide.html
  - Set offset and BPM first.
  - Check sync with assist ticks (a click track) before charting.

### Perception (where "the beat" of a sound is)
- "Where is the beat in that note?" (P-centre study, J. Exp. Psychol.: Human Perception & Performance): https://doi.org/10.1037/xhp0000611
- P-centre research paper (ZAS Papers in Linguistics 7, 1996): https://doi.org/10.21248/zaspil.7.1996.743
  - The perceived beat of a syllable sits near the vowel onset, not the consonant.
  - Sounds with a slow attack are heard later than their acoustic onset.
  - So snap vocals to the intended grid position, and put drums on their real (sharp) onset.

## Rule set used for newjeans-line

1. **Sync first.** Grid and offset are measured on the same decoding the game plays. Chrome's `decodeAudioData` matches a gapless ffmpeg/librosa decode sample for sample. Stems must be aligned to the mix by cross-correlation: the demucs stems here kept the mp3 encoder delay and were 25 ms late. Check by ear with a click track.
2. **One prominent layer per section.** Each section names the layer it follows (drums, vocal, mid/piano, bass/kick), and taps come from that layer. Switch layers only at section boundaries.
3. **Anchor the pulse.**
   - Downbeats (step 0) and backbeats (steps 4/12, the clap/snare) are tapped whenever they sound strong.
   - A bar made only of off-beat taps is not allowed unless nothing sounds on the beats (Racing-style confusion).
4. **A turn means an accent.** A tap needs an audible onset at that moment, with a gate on the full mix as well as the stem.
   - Long sustains and silences become straight segments, not filler taps.
5. **Simple snaps.**
   - 8th notes by default.
   - 16ths only where an audible 16th figure exists (fills, bridge figure).
   - No dotted or displaced rhythms that the music doesn't play.
6. **Timing source.**
   - Drums: the real transient (calibrated onset).
   - Vocals and soft attacks: the grid position (P-centre).
   - In our tool a tap uses the onset time if it is within 20 ms of the grid, otherwise the grid time.
7. **Phrase consistency.** Repeated sections (all choruses, verse A/B bars) use the same pattern, voted across every repetition. Fills go only in the last bar of a 4- or 8-bar phrase.
8. **Relative emphasis.** Quiet intro/outro/breakdown parts use sparse taps on their loudest events, with thresholds relative to the section.
9. **Density budget.**
   - About 2–2.5 taps/s in normal sections; about 3/s at the peak (dance break, bridge).
   - Minimum gap 0.105 s (validator).
   - Bursts only on audible 16ths.
10. **Verify mechanically and by ear.**
    - Run chartlogic and the validator (0 errors) and a scripted playthrough.
    - Render a click track over the song and listen to it.
