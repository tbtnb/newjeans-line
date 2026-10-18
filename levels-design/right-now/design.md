# Right Now — level design (worker 4)

**Concept: "Typing a message at dawn, then sending it."** The line starts at an empty chat bubble, runs a mailbox lane into a glass message greenhouse and loops up and over itself around a flower roundabout. It walks the greenhouse roof girders in the half-time bridge, jumps off into a flower field, drops onto a lamp-lit lane for the final chorus, and ends where the three typing dots have become one warm lamp. Palette: dawn lavender `#a99ad0` → peach `#ffd2c2`, petal pink `#ff9ec4`, mint glass `#e8fbff`, leaf green. Diamonds periwinkle `#a3c4f3`, crowns honey `#ffd166`.

Codex reference: none had arrived in `codex-ref/`, so the design is original. No real people are depicted.

## Route choreography (172 BPM, so the route texture changes every few bars)

| section | time | route texture | height | camera | scene / performance |
|---|---|---|---|---|---|
| Intro | 0.3–11.5 | **wide staircase** (melodic hits) | 0 | close | chat-bubble arch beside the start; its typing dots breathe every half bar; chat-sign billboard (art) |
| Verse 1 | 11.5–22.7 | **lightning bolt** | 0 | iso | mailboxes, postmark; fork 15 s |
| Verse 1b | 22.7–33.8 | **dense serpentine** (a turn on every 2nd tap): a tight wiggling corridor | 0 | iso | |
| Pre-chorus 1 | 33.8–45.0 | **staircase → switchbacks** climbing +2 between glass corridor posts | 0 → 2 | low | |
| Chorus 1 | 45.0–56.1 | **roundabout loop climbing +7 and passing over itself** (4–5 same-side turns) | 2 → 9 | **high** | greenhouse far wall unfolds; flower bed + lamp at the loop centre; fork 52 s |
| Chorus 1b | 56.1–67.3 | **tight zigzag** | 9 | iso | flower crowd nods on the beat |
| Verse 2 | 67.3–78.5 | **serpentine corridor** (turns after rests) | 9 | iso | crown 1 at 69.7; fork 72.5 s |
| Half-time bridge | 78.5–100.8 | **three-sided loop** up the greenhouse roof (+4), then a staircase along the girders | 9 → 13 | side | paper-cups EGG passing a flower on the half-time backbeat; message frame far off-road |
| Chorus 2 | 100.8–117.5 | **fall −6** (99.3 s) into the flower field, then a **bolt → serpentine** sweep | 7 | iso | giant rainbow flower in the field (sister motif to Supernatural); fork 110 s |
| Break | 117.5–123.1 | one long **turn-out** (melodic hits only) | 7 | high | crown 2 at 118.6 |
| Final chorus | 123.1–145.5 | **fall −5** (121.3 s) onto the night lane, then an **expanding spiral → staircase** | 2 | iso | petals beside the road react to the player's taps; second chat sign |
| Outro | 145.5–160.4 | staircase glide to the lamp | 2 | wide | the lamp switches on at 150 s; five-pots EGG |

There are no same-level overlaps. Both falls land ≥ 0.35 s before the next tap.

## Landmarks and eggs
- **Landmarks**: the chat-bubble arch, the greenhouse, the roundabout flower bed (inside the Chorus-1 loop), the giant flower, the lamp (finish).
- **Eggs**: two paper cups passing a flower; five pots with coloured tags; a petal that passes through the empty message frame and becomes a star.

## Fake-out forks
Visual-only stubs at 15, 52, 72.5 and 110 s, revealed together with the road.

## Art (under `art/`)
| file | use | generated-art prompt (GenerateImage asset) |
|---|---|---|
| `art/sky-dawn.jpg` | `art.backdrop` | lavender-to-peach dawn sky with light streaks (asset `86aad3ab…jpg`) |
| `art/flower-ground.jpg` | `art.ground` (scale 30) | meadow speckled with pink/white/yellow flowers (asset `7a71a02f…jpg`) |
| `art/chat-sign.jpg` | billboard image, intro + final chorus | white speech bubble with three typing dots on pink confetti (asset `b32f306e…jpg`) |

The GenerateImage outputs were stored outside this box. The committed files are procedural stand-ins from `_w4_tools/art.py`. Swap them in 1:1.

## No tap hints
The typing dots breathe on the half-bar music clock, not on taps. Petals and planks react only to the player's own taps (`react: tap`, feedback only).

## Chart summary
**411 taps**. This is the rhythmic-logic audit of the curated 419-tap chart:
- The drum layer is on the 8th grid; the intro, break and outro use melodic hits.
- Repeated sections share patterns.
- At 172 BPM a 16th is 0.087 s, which is below even the v2.5 floor of 0.105 s. So there are no 16th bursts, and the honest peak is the 8th grid at 345 CPM (0.174 s). This is the fastest sustained 8th stream of the four songs.

## Generated facts (from layout.json / chart.json)

- Road width {'width': [{'t': 0, 'w': 2.8}, {'t': 11.5, 'w': 2.3}, {'t': 44.98, 'w': 2.2}, {'t': 78.47, 'w': 2.4}, {'t': 100.79, 'w': 2.1}, {'t': 123.12, 'w': 1.8}, {'t': 145.45, 'w': 2.6}], 'height': 0.6, 'reveal': [{'t': 0, 'mode': 'static', 'lead': 3.0}, {'t': 11.5, 'mode': 'rise', 'lead': 1.8}, {'t': 44.98, 'mode': 'unfold', 'lead': 1.5}, {'t': 78.47, 'mode': 'unfold', 'lead': 2.0}, {'t': 100.79, 'mode': 'rise', 'lead': 1.4}, {'t': 117.54, 'mode': 'drop', 'lead': 1.8}, {'t': 123.12, 'mode': 'rise', 'lead': 1.3}, {'t': 145.45, 'mode': 'static', 'lead': 3.0}]}; start heading N; speed [{'t': 0, 'v': 10.5}, {'t': 78.47, 'v': 9.5}, {'t': 100.79, 'v': 10.5}, {'t': 123.12, 'v': 11.0}, {'t': 145.45, 'v': 10.0}]
- Elevation: ramp +2 @ 33.82–44.690000000000005 (pre-chorus: gentle climb into the glass greenhouse); ramp +7 @ 45.29–67.01 (chorus 1: the flower roundabout loops up and over itself); ramp +4 @ 78.47–98.01 (half-time bridge: walk up the greenhouse roof girders); fall -6 @ 99.281 (jump off the roof into the flower field at the chorus-2 downbeat); fall -5 @ 121.257 (final chorus: drop onto the lamp-lit night lane)
- Camera: 0s close; 11.5s iso; 33.82s low; 44.98s high; 56.14s iso; 67.31s iso; 78.47s side; 89.63s side; 99.4s iso; 117.54s high; 123.12s iso; 134.28s iso; 145.45s wide
- Diamonds (t): 5.916, 20.654, 37.398, 57.805, 72.632, 89.637, 108.038, 119.987, 130.365, 149.638; crowns (checkpoints): 69.666, 118.591
- Landmarks: `chat_gate` (start landmark beside the road: an empty white chat-bubble arch; three typing dots breathe on top (music clock)); `greenhouse` (the message greenhouse (glass house with mint frame); its far wall opens at Chorus 1); `big_flower` (giant rainbow flower (Supernatural cover sister) standing in the field); `lamp` (finish: the three typing dots became one warm lamp); `roundabout_bed` (round flower bed + lamp post at the centre of the chorus-1 loop)
- Easter eggs: `cups_egg` (EGG: two tiny paper cups on a roof ledge passing a flower back and forth (on the half-time snare)); `pots5_egg` (EGG: five pots with different-coloured tags; all five turn to face the direction the line leaves)
- Fake-out forks (visual only, road-coloured dead-end stubs that rise 2 s early and sink after the corner; they are revealed together with the road (same lead), so they add no timing information and only fake a straight continuation): fork0, fork1, fork2, fork3
- Objects: 39 total; events: 12
- Art wired into layout: backdrop `art/sky-dawn.jpg`, ground `art/flower-ground.jpg`, images/textures `art/chat-sign.jpg`
