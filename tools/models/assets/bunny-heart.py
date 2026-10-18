"""Giant pop-up bunny hugging a heart (z04 landmark, ~9 m). Pivots: root (pop-up spring), ears (wiggle), heart (beat pulse)."""
BUDGET = 6000
CREAM, CREAM2, PINK, HEART, HEART2 = '#FFF3DE', '#F4E6CF', '#FFB8D2', '#FF6FAE', '#FF8DC0'

def build(P, spec):
    cream = lambda c, n: P.mix(CREAM, CREAM2, 0.5 + 0.5 * P._rng.uniform(-1, 1))   # faceted paper: each facet a slightly different cream
    body = P.ico('body', 2.5, loc=(0, 0.2, 2.6), color=cream, subdiv=2, scale=(1.0, 0.85, 1.05), jitter=0.12)
    belly = P.ico('belly', 1.6, loc=(0, -1.15, 2.3), color=cream, subdiv=1, scale=(1.0, 0.6, 1.0), jitter=0.08)
    head = P.ico('head', 2.0, loc=(0, -0.3, 6.1), color=cream, subdiv=2, scale=(1.05, 0.95, 0.95), jitter=0.1)
    cheekL = P.ico('cheekL', 0.75, loc=(-0.95, -1.5, 5.6), color=cream, subdiv=1, jitter=0.05); cheekR = P.mirror_x(cheekL, 'cheekR')
    nose = P.ico('nose', 0.18, loc=(0, -2.05, 5.95), color=PINK, subdiv=1)
    eyeL = P.ico('eyeL', 0.17, loc=(-0.65, -1.72, 6.45), color='#3A2F4A', subdiv=1, scale=(1, 0.6, 1.3)); eyeR = P.mirror_x(eyeL, 'eyeR')
    # ears: cream cut-out with a pink inner cut-out in front, tilted outwards
    earL = P.prism('earL', P.ear(1.5, 4.6, 5), 0.35, loc=(-0.9, -0.1, 7.4), color=cream, rot=(8, 0, 16))
    innL = P.prism('innL', P.ear(0.9, 3.6, 5), 0.12, loc=(-0.95, -0.33, 7.75), color=PINK, rot=(8, 0, 16))
    earR = P.mirror_x(earL, 'earR'); innR = P.mirror_x(innL, 'innR')
    # feet with pink pads, arms wrapped round the heart
    footL = P.ico('footL', 1.0, loc=(-1.5, -1.9, 0.75), color=cream, subdiv=1, scale=(0.9, 1.35, 0.75), jitter=0.05)
    padL = P.prism('padL', P.ellipse(0.45, 0.55, 8), 0.1, loc=(-1.5, -3.25, 0.8), color=PINK)
    footR = P.mirror_x(footL, 'footR'); padR = P.mirror_x(padL, 'padR')
    armL = P.ico('armL', 0.8, loc=(-2.0, -1.7, 3.3), color=cream, subdiv=1, scale=(0.75, 0.75, 1.3), rot=(0, -25, 0), jitter=0.05); armR = P.mirror_x(armL, 'armR')
    tail = P.ico('tail', 0.7, loc=(0, 2.4, 1.3), color=cream, subdiv=1, jitter=0.06)
    # heart: thick faceted cut-out, two tones (front facets lighter)
    heart = P.prism('heart', P.heart(2.7, 18), 0.9, loc=(0, -2.35, 2.5), color=lambda c, n: HEART2 if n.y < -0.5 else HEART, side_color=HEART)
    P.pivot('heart', (0, -2.35, 3.7), [heart])
    P.pivot('ears', (0, -0.2, 7.3), [earL, innL, earR, innR])
    others = [body, belly, head, cheekL, cheekR, nose, eyeL, eyeR, footL, padL, footR, padR, armL, armR, tail]
    P.pivot('root', (0, 0, 0), others + [o for o in __import__('bpy').data.objects if o.name in ('pivot_heart', 'pivot_ears')])
