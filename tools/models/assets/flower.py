"""Ground cover: small paper flower (5 tilted petal cards + gold centre card, <=30 tris)."""
BUDGET = 30
def build(P, spec):
    import math
    pet = []
    for i in range(5):
        a = 2 * math.pi * i / 5
        pet.append(P.card(f'p{i}', P.ellipse(0.06, 0.1, 6, cz=0.1), loc=(0, 0, 0.12), color='#FFB8D2', rot=(90 - 22, 0, math.degrees(a) + 180)))
    c = P.card('c', P.ellipse(0.045, 0.045, 5), loc=(0, 0, 0.135), color='#F7C948', rot=(90, 0, 0))
    stem = P.blade('leaf', 0.12, 0.12, loc=(0, 0, 0), color='#9ACB8E', bend=0.2)
    P.join(pet + [c, stem], 'flower')
