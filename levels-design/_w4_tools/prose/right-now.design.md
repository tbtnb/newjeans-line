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
