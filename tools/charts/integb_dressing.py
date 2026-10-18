"""Themed roadside dressing (schema v2.6 layout.dressing) for the integ-b levels: dense DL-style roadsides whose props
follow each level's palette and setting. Breaks/hushes thin out (sparse music -> sparse roadside); choruses thicken."""
def B(size, color, pos=(0, 0, 0)): return {'kind': 'box', 'pos': list(pos), 'size': list(size), 'color': color}
def C(size, color, pos=(0, 0, 0), kind='cylinder'): return {'kind': kind, 'pos': list(pos), 'size': list(size), 'color': color}
def house(wall, roof, w=1.6, h=1.8): return {'kind': 'group', 'parts': [B((w, h, w), wall, (0, h / 2, 0)), B((w + 0.2, 0.35, w + 0.2), roof, (0, h + 0.17, 0))]}
def tree(trunk, leaf, cone=False): return {'kind': 'group', 'parts': [C((0.28, 0.9, 0.28), trunk, (0, 0.45, 0)), (C((1.5, 2.3, 1.5), leaf, (0, 2.0, 0), 'cone') if cone else C((1.5, 1.5, 1.5), leaf, (0, 1.6, 0), 'sphere'))]}
def lamp(pole, glow, h=2.6): return {'kind': 'group', 'parts': [C((0.14, h, 0.14), pole, (0, h / 2, 0)), C((0.42, 0.42, 0.42), glow, (0, h + 0.1, 0), 'sphere')]}
def umbrella(pole, top): return {'kind': 'group', 'parts': [C((0.1, 1.9, 0.1), pole, (0, 0.95, 0)), C((1.9, 0.6, 1.9), top, (0, 2.05, 0), 'cone')]}
def w(p, weight, scale=(0.75, 1.25), scaleY=(0.8, 1.5)): return {**p, 'weight': weight, 'scale': list(scale), 'scaleY': list(scaleY)}

DRESSING = {
  # Lisbon afternoon: cream houses with coral/teal roofs, round park trees, coral parasols, lamps, five-colour pixel blocks
  'super-shy': {'density': 4.4, 'near': [0.4, 3.6], 'seed': 11, 'props': [
      w(house('#FFF3E2', '#F08C78'), 3, scaleY=(0.8, 2.0)), w(house('#F7E7D0', '#3B8A89', 1.4, 2.4), 2, scaleY=(0.8, 1.8)),
      w(tree('#8A6A4F', '#7CC795'), 3), w(umbrella('#F4F1EA', '#F27D72'), 1.5, scaleY=(0.9, 1.1)), w(lamp('#2F5F5E', '#FFF2C9'), 1, scaleY=(0.9, 1.2)),
      w(B((0.8, 0.8, 0.8), '#295BE7'), 0.7, scaleY=(0.6, 1.6)), w(B((0.8, 0.8, 0.8), '#F5C84B'), 0.7, scaleY=(0.6, 1.6))],
    'sections': [{'t': 39, 'density': 5.2}, {'t': 64.4, 'density': 2.4, 'props': [2, 3, 4]}, {'t': 70.8, 'density': 4.4}, {'t': 102.8, 'density': 2.6, 'props': [2, 4]},
                 {'t': 106, 'density': 4.4}, {'t': 115.6, 'density': 5.4}]},
  # summer seaside town: white houses with terracotta roofs, palms (sphere crowns on tall trunks), beach umbrellas, pixel cubes
  'eta': {'density': 4.6, 'near': [0.4, 3.8], 'seed': 23, 'props': [
      w(house('#FFF7EA', '#D9774B'), 3, scaleY=(0.8, 2.2)), w(house('#F6EBD9', '#C9623E', 1.3, 2.6), 2, scaleY=(0.9, 2.0)),
      w({'kind': 'group', 'parts': [C((0.25, 2.6, 0.25), '#A07A55', (0, 1.3, 0)), C((1.6, 0.7, 1.6), '#2FAE6E', (0, 2.8, 0), 'sphere')]}, 2.5),
      w(umbrella('#FFFFFF', '#F05A50'), 1.5, scaleY=(0.9, 1.1)), w(umbrella('#FFFFFF', '#FFD166'), 1, scaleY=(0.9, 1.1)),
      w(B((0.8, 0.8, 0.8), '#F05A50'), 0.8, scaleY=(0.6, 1.8)), w(B((0.8, 0.8, 0.8), '#4D9DE0'), 0.8, scaleY=(0.6, 1.8))],
    'sections': [{'t': 35.4, 'density': 5.6}, {'t': 47.9, 'density': 3.0}, {'t': 49.7, 'density': 4.6}, {'t': 78.1, 'density': 5.0}, {'t': 92.3, 'density': 5.6},
                 {'t': 104.8, 'density': 3.0}, {'t': 106.6, 'density': 6.0}, {'t': 135, 'density': 2.6, 'props': [2, 3]}]},
  # rainy night gallery city: slate blocks, tall thin towers with pale caps, street lamps, ivory pillars
  'cool-with-you': {'density': 4.2, 'near': [0.4, 3.8], 'seed': 5, 'props': [
      w(B((1.6, 2.4, 1.6), '#4A5E66'), 3, scaleY=(0.7, 2.4)), w({'kind': 'group', 'parts': [B((1.0, 4.0, 1.0), '#56707A', (0, 2.0, 0)), B((1.1, 0.25, 1.1), '#EEEADF', (0, 4.1, 0))]}, 2, scaleY=(0.7, 1.6)),
      w(lamp('#2E3B40', '#FFE7C2', 2.8), 1.6, scaleY=(0.9, 1.2)), w(C((0.6, 2.6, 0.6), '#EEEADF'), 1.4, scaleY=(0.6, 1.4)),
      w(B((1.2, 0.5, 1.2), '#AEBFC5'), 1.2, scaleY=(0.6, 1.4))],
    'sections': [{'t': 0, 'density': 3.0}, {'t': 14.6, 'density': 4.2}, {'t': 43, 'density': 3.0, 'props': [2, 3, 4]}, {'t': 57.2, 'density': 5.0}, {'t': 71.4, 'density': 4.2},
                 {'t': 85.7, 'density': 2.2, 'props': [2, 3]}, {'t': 92.8, 'density': 4.6}, {'t': 99.9, 'density': 5.4}, {'t': 128.3, 'density': 2.4, 'props': [2, 3]}]},
  # dawn after rain over shallow water: reeds, pale stones, folded white wing slabs, a few warm lamps (quiet interlude)
  'get-up': {'density': 3.4, 'near': [0.4, 3.2], 'seed': 3, 'props': [
      w({'kind': 'group', 'parts': [C((0.12, 1.4, 0.12), '#8FA98A', (0, 0.7, 0)), C((0.12, 1.9, 0.12), '#9DB596', (0.3, 0.95, 0.2)), C((0.12, 1.1, 0.12), '#8FA98A', (-0.25, 0.55, -0.2))]}, 3, scaleY=(0.7, 1.4)),
      w(C((1.2, 0.5, 1.0), '#DCD8E6', kind='sphere'), 2, scaleY=(0.6, 1.0)), w(B((0.3, 1.6, 1.4), '#FFFFFF'), 1.4, scaleY=(0.7, 1.3)),
      w(lamp('#7D7A9A', '#FFE3B8', 2.2), 0.8, scaleY=(0.9, 1.1)), w(B((1.0, 0.6, 1.0), '#B8B4D5'), 1, scaleY=(0.6, 1.6))],
    'sections': [{'t': 0, 'density': 2.6}, {'t': 8.3, 'density': 3.2}, {'t': 16.3, 'density': 3.8}, {'t': 24.3, 'density': 4.2}]},
  # emerald night forest meadow: pines, round bushes, flowers, mushrooms, stones; the hush thins out
  'asap': {'density': 4.6, 'near': [0.4, 3.8], 'seed': 17, 'props': [
      w(tree('#5B4636', '#1F5A45', cone=True), 3.5, scaleY=(0.8, 1.7)), w(tree('#5B4636', '#2E7A5A'), 2),
      w(C((1.1, 0.8, 1.1), '#3F8A63', kind='sphere'), 2, scaleY=(0.6, 1.1)),
      w({'kind': 'group', 'parts': [C((0.22, 0.6, 0.22), '#F4F1DF', (0, 0.3, 0)), C((0.8, 0.35, 0.8), '#E35D83', (0, 0.7, 0), 'sphere')]}, 1.2, scaleY=(0.8, 1.3)),
      w({'kind': 'group', 'parts': [C((0.1, 0.5, 0.1), '#4E8A5E', (0, 0.25, 0)), C((0.35, 0.35, 0.35), '#F6E7A8', (0, 0.55, 0), 'sphere')]}, 1.2, scaleY=(0.8, 1.4)),
      w(C((0.9, 0.5, 0.8), '#cfd8b8', kind='sphere'), 1, scaleY=(0.6, 1.0))],
    'sections': [{'t': 0, 'density': 3.4}, {'t': 4, 'density': 4.6}, {'t': 41, 'density': 5.0}, {'t': 55.7, 'density': 2.4}, {'t': 57.6, 'density': 4.6},
                 {'t': 72.3, 'density': 5.6}, {'t': 92.6, 'density': 5.2}, {'t': 114.8, 'density': 2.0, 'props': [0, 4]}, {'t': 120.3, 'density': 5.0}, {'t': 129.6, 'density': 2.6}]},
}
