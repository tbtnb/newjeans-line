"""H02 抱心巨兔 Giant pop-up bunny hugging a heart (z04 drop landmark), built to the three-view sheet
levels-design/omg/redesign-v3/C/assets/H02_giant_bunny_heart: 6.5 x 6 x 10 m incl. the closed-book base, budget 4000 tris.
Pivots (spec.json): root = base hinge (DROP pop), ears = ear roots (spring upright on each 'Oh my god'), heart = heart centre (beat 1->1.12)."""
BUDGET = 4000
K, BASE = 0.72, 0.95   # bunny scale to the 10 m sheet height; it sits on a closed book 0.95 m tall
CREAM, CREAM2, PINK, HEART, HEART2 = '#FFF3DE', '#F4E6CF', '#FFB8D2', '#FF6FAE', '#FF8DC0'
GOLD, PAGE, PAGE2 = '#F7D98B', '#FFF8EC', '#F1E6D2'

def build(P, spec):
    cream = lambda c, n: P.mix(CREAM, CREAM2, 0.5 + 0.5 * P._rng.uniform(-1, 1))   # faceted paper: each facet a slightly different cream
    body = P.ico('body', 2.5, loc=(0, 0.2, 2.6), color=cream, subdiv=2, scale=(1.0, 0.85, 1.05), jitter=0.12)
    belly = P.ico('belly', 1.6, loc=(0, -1.15, 2.3), color=cream, subdiv=1, scale=(1.0, 0.6, 1.0), jitter=0.08)
    head = P.ico('head', 2.25, loc=(0, -0.3, 6.2), color=cream, subdiv=2, scale=(1.05, 0.95, 0.95), jitter=0.1)
    cheekL = P.ico('cheekL', 0.75, loc=(-0.95, -1.5, 5.6), color=cream, subdiv=1, jitter=0.05); cheekR = P.mirror_x(cheekL, 'cheekR')
    nose = P.ico('nose', 0.18, loc=(0, -2.05, 5.95), color=PINK, subdiv=1)
    eyeL = P.ico('eyeL', 0.17, loc=(-0.65, -1.72, 6.45), color='#3A2F4A', subdiv=1, scale=(1, 0.6, 1.3)); eyeR = P.mirror_x(eyeL, 'eyeR')
    # ears: cream cut-out with a pink inner cut-out in front, tilted outwards
    earL = P.prism('earL', P.ear(2.3, 5.0, 5), 0.5, loc=(-1.05, -0.1, 7.6), color=cream, rot=(8, 0, 20))
    innL = P.prism('innL', P.ear(1.45, 3.9, 5), 0.12, loc=(-1.1, -0.42, 8.0), color=PINK, rot=(8, 0, 20))
    earR = P.mirror_x(earL, 'earR'); innR = P.mirror_x(innL, 'innR')
    # feet with pink pads, arms wrapped round the heart
    footL = P.ico('footL', 1.0, loc=(-1.5, -1.9, 0.75), color=cream, subdiv=1, scale=(0.9, 1.35, 0.75), jitter=0.05)
    padL = P.prism('padL', P.ellipse(0.45, 0.55, 8), 0.1, loc=(-1.5, -3.25, 0.8), color=PINK)
    footR = P.mirror_x(footL, 'footR'); padR = P.mirror_x(padL, 'padR')
    armL = P.ico('armL', 0.8, loc=(-2.0, -1.7, 3.3), color=cream, subdiv=1, scale=(0.75, 0.75, 1.3), rot=(0, -25, 0), jitter=0.05); armR = P.mirror_x(armL, 'armR')
    tail = P.ico('tail', 0.7, loc=(0, 2.4, 1.3), color=cream, subdiv=1, jitter=0.06)
    # heart: thick faceted cut-out, two tones (front facets lighter)
    heart = P.join([P.prism('heartA', P.heart(3.5, 18), 1.0, loc=(0, -2.4, 2.0), color=HEART, side_color=HEART),
                    P.prism('heartB', [(x * 0.72, z * 0.72 + 0.45) for x, z in P.heart(3.5, 14)], 0.5, loc=(0, -3.0, 2.0), color=lambda c, n: HEART2 if n.y < -0.5 else HEART)], 'heart')   # layered paper = puffy faceted heart
    bow = [P.prism('bowL', [(0, 0), (-0.75, 0.42), (-0.75, -0.42)], 0.25, loc=(1.55, -1.25, 4.55), color=HEART, rot=(0, 0, -35)),
           P.prism('bowR', [(0, 0), (0.75, 0.42), (0.75, -0.42)], 0.25, loc=(1.55, -1.25, 4.55), color=HEART, rot=(0, 0, -35)),
           P.ico('bowK', 0.2, loc=(1.55, -1.3, 4.55), color=HEART2, subdiv=1)]
    import bpy
    from mathutils import Matrix
    bunny = [body, belly, head, cheekL, cheekR, nose, eyeL, eyeR, footL, padL, footR, padR, armL, armR, tail, heart, earL, innL, earR, innR] + bow
    bpy.context.view_layer.update()   # matrix_world of freshly created objects is stale until the depsgraph updates
    import mathutils
    top = max((o.matrix_world @ mathutils.Vector(c)).z for o in [earL, earR, head] for c in o.bound_box)
    M = Matrix.Translation((0, 0, BASE)) @ Matrix.Scale((spec.get('size_m', {}).get('h', 10) - BASE) / top, 4)
    for o in bunny: o.matrix_world = M @ o.matrix_world
    # closed book base: cream page block with gold covers + spine notch
    BW, BD = 6.5, 6.0
    base = [P.box('coverB', (BW, BD, 0.14), loc=(0, 0, 0), color=GOLD), P.box('block', (BW - 0.25, BD - 0.3, 0.67), loc=(0.1, 0, 0.14), color=lambda c, n: PAGE if n.z > 0.5 else PAGE2),
            P.box('coverT', (BW, BD, 0.14), loc=(0, 0, 0.81), color=GOLD), P.box('topPage', (BW - 0.35, BD - 0.4, 0.02), loc=(0.05, 0, 0.95), color=PAGE)]
    for k in range(3): base.append(P.box(f'leaf{k}', (0.02, BD - 0.45, 0.6), loc=(BW / 2 - 0.13, 0, 0.17 + 0.0), color=PAGE2, rot=(0, 0, 0)) if k == 0 else None)
    base = [b for b in base if b is not None]
    hp = M @ __import__('mathutils').Vector((0, -2.6, 3.6)); ep = M @ __import__('mathutils').Vector((0, -0.2, 7.3))
    P.pivot('heart', tuple(hp), [heart])
    P.pivot('ears', tuple(ep), [earL, innL, earR, innR])
    others = [body, belly, head, cheekL, cheekR, nose, eyeL, eyeR, footL, padL, footR, padR, armL, armR, tail] + bow + base
    P.pivot('root', (0, 0, 0), others + [o for o in bpy.data.objects if o.name in ('pivot_heart', 'pivot_ears')])
