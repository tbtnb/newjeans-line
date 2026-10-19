"""Papercraft low-poly modelling kit for Blender (bpy, headless). Units: metres, Blender Z-up; models face -Y (front view).
Every primitive gets a flat per-face colour (colour attribute 'Col'); finalize() bakes a fixed paper-light (sun + sky + height AO)
into the colours, flat-shades, counts triangles and exports a .glb. Animated parts hang under empties named 'pivot_<name>'.
"""
import bpy, bmesh, math, random
from mathutils import Vector, Matrix, Euler

_rng = random.Random(7)

def seed(s):
    global _rng; _rng = random.Random(s)

def hexc(h, a=1.0):
    h = h.lstrip('#'); return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)

def mix(c1, c2, k):
    a, b = hexc(c1) if isinstance(c1, str) else c1, hexc(c2) if isinstance(c2, str) else c2
    return tuple(a[i] * (1 - k) + b[i] * k for i in range(4))

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for c in list(bpy.data.collections): bpy.data.collections.remove(c)

def _obj_from_bm(bm, name, color, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), jitter=0.0):
    if jitter > 0:
        for v in bm.verts: v.co += Vector((_rng.uniform(-1, 1), _rng.uniform(-1, 1), _rng.uniform(-1, 1))) * jitter
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = loc; ob.rotation_euler = Euler([math.radians(a) for a in rot]); ob.scale = scale
    paint(ob, color)
    return ob

def paint(ob, color, faces=None):
    """flat colour per face (colour may be a hex, an rgba tuple, or a callable(face_center_local, normal) -> colour)"""
    me = ob.data
    attr = me.color_attributes.get('Col') or me.color_attributes.new('Col', 'BYTE_COLOR', 'CORNER')
    me.color_attributes.active_color = attr
    for p in me.polygons:
        if faces is not None and p.index not in faces: continue
        c = color(p.center, p.normal) if callable(color) else color
        if isinstance(c, str): c = hexc(c)
        for li in p.loop_indices: attr.data[li].color_srgb = c
    return ob

# ---------------- primitives ----------------
def box(name, size, loc=(0, 0, 0), color='#ffffff', rot=(0, 0, 0), base=True, jitter=0.0):
    """box; base=True puts its bottom at loc.z (paper props stand on the page)"""
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    if base: bmesh.ops.translate(bm, vec=Vector((0, 0, size[2] / 2)), verts=bm.verts)
    return _obj_from_bm(bm, name, color, loc, rot, jitter=jitter)

def cyl(name, r, h, segs=8, loc=(0, 0, 0), color='#ffffff', r2=None, rot=(0, 0, 0), cap=True, jitter=0.0):
    """frustum/cylinder/cone standing on loc (r2 = top radius; 0 = cone)"""
    bm = bmesh.new(); r2 = r if r2 is None else r2
    bmesh.ops.create_cone(bm, cap_ends=cap, cap_tris=False, segments=segs, radius1=r, radius2=max(r2, 1e-5) if r2 > 0 else 0, depth=h)
    bmesh.ops.translate(bm, vec=Vector((0, 0, h / 2)), verts=bm.verts)
    if r2 == 0: bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    return _obj_from_bm(bm, name, color, loc, rot, jitter=jitter)

def ico(name, r, loc=(0, 0, 0), color='#ffffff', subdiv=1, scale=(1, 1, 1), rot=(0, 0, 0), jitter=0.0):
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=r)
    bmesh.ops.scale(bm, vec=Vector(scale), verts=bm.verts)
    return _obj_from_bm(bm, name, color, loc, rot, jitter=jitter)

def prism(name, outline, depth, loc=(0, 0, 0), color='#ffffff', rot=(0, 0, 0), side_color=None):
    """paper cut-out: 2D outline in the XZ plane (front view), extruded along Y by depth (centred). side_color tints the rim."""
    bm = bmesh.new()
    vs = [bm.verts.new((x, -depth / 2, z)) for x, z in outline]
    f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, vec=Vector((0, depth, 0)), verts=[e for e in ext['geom'] if isinstance(e, bmesh.types.BMVert)])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = _obj_from_bm(bm, name, color, loc, rot)
    if side_color: paint(ob, side_color, faces={p.index for p in ob.data.polygons if abs(p.normal.y) < 0.5})
    return ob

def card(name, outline, loc=(0, 0, 0), color='#ffffff', rot=(0, 0, 0)):
    """single paper face (n-gon) in the XZ plane, facing -Y; rotate it to lie flat (rot=(90,0,0) faces up)"""
    bm = bmesh.new(); bm.faces.new([bm.verts.new((x, 0, z)) for x, z in outline])
    return _obj_from_bm(bm, name, color, loc, rot)

def lathe(name, profile, segs=8, loc=(0, 0, 0), color='#ffffff', rot=(0, 0, 0), jitter=0.0):
    """surface of revolution around Z from [(r, z), ...] bottom->top (r=0 ends close the shape)"""
    bm = bmesh.new(); rings = []
    for r, z in profile:
        if r <= 1e-6: rings.append([bm.verts.new((0, 0, z))]); continue
        rings.append([bm.verts.new((r * math.cos(2 * math.pi * i / segs), r * math.sin(2 * math.pi * i / segs), z)) for i in range(segs)])
    for a, b in zip(rings, rings[1:]):
        for i in range(segs):
            if len(a) == 1 and len(b) == 1: continue
            if len(a) == 1: bm.faces.new((a[0], b[(i + 1) % segs], b[i]))
            elif len(b) == 1: bm.faces.new((a[i], a[(i + 1) % segs], b[0]))
            else: bm.faces.new((a[i], a[(i + 1) % segs], b[(i + 1) % segs], b[i]))
    if len(rings[0]) > 1: bm.faces.new(list(reversed(rings[0])))
    if len(rings[-1]) > 1: bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj_from_bm(bm, name, color, loc, rot, jitter=jitter)

def blade(name, w, h, loc=(0, 0, 0), color='#7fbf7f', rot=(0, 0, 0), bend=0.15, depth=0.0):
    """folded paper leaf/grass blade: a creased diamond (2 tris per side), optionally with a little thickness"""
    bm = bmesh.new()
    a, b, c, d = bm.verts.new((-w / 2, 0, 0)), bm.verts.new((0, -bend * w, h * 0.45)), bm.verts.new((w / 2, 0, 0)), bm.verts.new((0, bend * h, h))
    m = bm.verts.new((0, -bend * w * 0.6, 0.02))
    bm.faces.new((a, m, b)); bm.faces.new((m, c, b)); bm.faces.new((a, b, d)); bm.faces.new((b, c, d))
    return _obj_from_bm(bm, name, color, loc, rot)

# ---------------- outlines (XZ) ----------------
def ellipse(rx, rz, n=10, cx=0, cz=0, a0=0.0):
    return [(cx + rx * math.cos(a0 + 2 * math.pi * i / n), cz + rz * math.sin(a0 + 2 * math.pi * i / n)) for i in range(n)]

def heart(s=1.0, n=14):
    pts = []
    for i in range(n):
        t = math.pi * 2 * i / n
        x = 16 * math.sin(t) ** 3; z = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((x / 17 * s, (z + 5) / 17 * s))
    return pts[::-1]

def star(r1, r2, n=5, a0=math.pi / 2):
    return [((r1 if i % 2 == 0 else r2) * math.cos(a0 + math.pi * i / n), (r1 if i % 2 == 0 else r2) * math.sin(a0 + math.pi * i / n)) for i in range(2 * n)][::-1]

def ear(w, h, n=5):
    """pointed bunny-ear / leaf outline, base at z=0"""
    left = [(-w / 2 * math.sin(math.pi * k / (2 * n) + 0.3) * (1 - (k / n) ** 3), h * k / n) for k in range(n + 1)]
    right = [(-x, z) for x, z in left[::-1]]
    return left + right[1:-1]

# ---------------- structure ----------------
def pivot(name, loc, children):
    """empty 'pivot_<name>' at loc; children keep their world transform (animated part rotates/scales about loc)"""
    e = bpy.data.objects.new('pivot_' + name, None); bpy.context.scene.collection.objects.link(e); e.location = loc
    bpy.context.view_layer.update()
    for c in children:
        mw = c.matrix_world.copy(); c.parent = e; c.matrix_parent_inverse = e.matrix_world.inverted(); c.matrix_world = mw
    return e

def join(objs, name):
    objs = [o for o in objs if o is not None]
    if len(objs) == 1: objs[0].name = name; objs[0].data.name = name; return objs[0]
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join(); ob = bpy.context.view_layer.objects.active; ob.name = name; ob.data.name = name
    return ob

def mirror_x(ob, name=None):
    c = ob.copy(); c.data = ob.data.copy(); bpy.context.scene.collection.objects.link(c)
    c.location.x = -ob.location.x; c.rotation_euler = Euler((ob.rotation_euler.x, -ob.rotation_euler.y, -ob.rotation_euler.z))
    c.scale = ob.scale.copy(); c.scale.x *= -1
    bpy.context.view_layer.update()
    # apply the mirror so normals stay outward
    bpy.ops.object.select_all(action='DESELECT'); c.select_set(True); bpy.context.view_layer.objects.active = c
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    me = c.data; me.flip_normals()
    if name: c.name = name
    return c

# ---------------- finish ----------------
SUN = Vector((-0.4, -0.75, 0.55)).normalized()   # key light from the front-left-top (the game camera side)

def bake_light(objs, height=None, lo=0.80, ao=0.07):   # v2: deeper fold shading so facets read at the gameplay camera (lit faces stay exact hex)
    """palette-preserving paper light baked into vertex colours: faces turned to the key light keep the EXACT palette hex
    (k = 1), faces turned away fall to `lo` (crisp folds, never muddy), plus a faint height AO at the page. No tint."""
    zs = [(o.matrix_world @ v.co).z for o in objs for v in o.data.vertices]
    z0 = min(zs) if zs else 0; H = height or max(1e-3, (max(zs) - z0) if zs else 1)
    for o in objs:
        me = o.data; attr = me.color_attributes['Col']; mw = o.matrix_world; nm = mw.to_3x3().inverted().transposed()
        for p in me.polygons:
            n = (nm @ p.normal).normalized(); lam = max(0.0, n.dot(SUN)); up = max(0.0, n.z)
            k_face = min(1.0, lo + (1 - lo) * min(1.0, 1.25 * lam + 0.35 * up))
            for li in p.loop_indices:
                v = me.vertices[me.loops[li].vertex_index]; z = (mw @ v.co).z
                k = k_face * (1 - ao * (1 - min(1.0, max(0.0, (z - z0) / (0.25 * H)))))
                c = attr.data[li].color_srgb
                attr.data[li].color_srgb = (c[0] * k, c[1] * k, c[2] * k, c[3])

def tris(objs):
    n = 0
    for o in objs:
        if o.type != 'MESH': continue
        o.data.calc_loop_triangles(); n += len(o.data.loop_triangles)
    return n

def _join_by_parent():
    """one mesh per pivot group (fewer draw calls / nodes in-engine): meshes with the same parent are joined, named
    '<pivot>_mesh' (or 'static' at the top level); pivots stay as empties."""
    groups = {}
    for o in bpy.context.scene.objects:
        if o.type == 'MESH': groups.setdefault(o.parent.name if o.parent else '', []).append(o)
    for par, objs in groups.items():
        if len(objs) < 2 and objs and objs[0].name.endswith('_mesh'): continue
        name = (par[len('pivot_'):] if par.startswith('pivot_') else 'static') + '_mesh'
        j = join(objs, name)

def fix_closed(meshes):
    """v8 audit fix: closed parts whose faces point inward (negative signed volume) are flipped; zero-area faces are dissolved."""
    import bmesh
    flipped = degen = 0
    for o in meshes:
        bm = bmesh.new(); bm.from_mesh(o.data)
        dg = [f for f in bm.faces if f.calc_area() < 1e-9]
        if dg:
            n0 = len(bm.faces); bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=list(bm.edges)); degen += n0 - len(bm.faces)
        bm.faces.ensure_lookup_table(); seen = set()
        for f in bm.faces:
            if f.index in seen: continue
            isl = []; st = [f]; seen.add(f.index)
            while st:
                g = st.pop(); isl.append(g)
                for e in g.edges:
                    for h in e.link_faces:
                        if h.index not in seen: seen.add(h.index); st.append(h)
            es = {e for g in isl for e in g.edges}
            if len(isl) < 4 or any(len(e.link_faces) != 2 for e in es): continue
            vol = 0.0
            for g in isl:
                vs = [v.co for v in g.verts]
                for k in range(1, len(vs) - 1): vol += vs[0].dot(vs[k].cross(vs[k + 1])) / 6
            if o.matrix_world.to_3x3().determinant() < 0: vol = -vol
            if vol < 0: bmesh.ops.reverse_faces(bm, faces=isl); flipped += 1
        bm.to_mesh(o.data); o.data.update(); bm.free()
    return flipped, degen

def decoplanar(meshes, eps_rel=0.0025):
    """v8 audit fix: z-fighting. Faces of DIFFERENT parts (islands) lying in the same plane, facing the same way and overlapping
    flicker in the game. The smaller part's conflicting faces are nudged out along their normal by ~0.25% of the model height
    (min 2 mm); exact duplicate faces inside one part are deleted. Returns (nudged faces, removed duplicates)."""
    import bmesh
    from mathutils import Vector
    pts = [o.matrix_world @ v.co for o in meshes for v in o.data.vertices]
    if not pts: return 0, 0
    H = max(p.z for p in pts) - min(p.z for p in pts); eps = max(0.002, H * eps_rel); tol = max(0.0008, H * 0.0013)
    F = []   # (obj index, face index, island id, normal, d, area, centroid, verts world)
    bms = []; removed = 0
    for oi, o in enumerate(meshes):
        bm = bmesh.new(); bm.from_mesh(o.data); bm.faces.ensure_lookup_table()
        seen = {}; dup = []
        for f in bm.faces:
            k = tuple(sorted((round(v.co.x, 4), round(v.co.y, 4), round(v.co.z, 4)) for v in f.verts))
            if k in seen: dup.append(f)
            else: seen[k] = f
        if dup: bmesh.ops.delete(bm, geom=dup, context='FACES_ONLY'); removed += len(dup)
        bm.faces.ensure_lookup_table(); bm.verts.ensure_lookup_table()
        isl = {}; nid = 0   # islands by linked faces
        for f in bm.faces:
            if f.index in isl: continue
            st = [f]; isl[f.index] = nid
            while st:
                g = st.pop()
                for e in g.edges:
                    for h in e.link_faces:
                        if h.index not in isl: isl[h.index] = nid; st.append(h)
            nid += 1
        M = o.matrix_world; N3 = M.to_3x3().inverted().transposed()
        for f in bm.faces:
            if f.calc_area() < 1e-8: continue
            n = (N3 @ f.normal).normalized(); W = [M @ v.co for v in f.verts]; c = sum(W, Vector()) / len(W)
            F.append((oi, f.index, (oi, isl[f.index]), n, n.dot(c), f.calc_area() * (M.to_3x3().determinant() ** (2 / 3)), c, W))
        bms.append(bm)
    isz = {}
    for x in F: isz[x[2]] = isz.get(x[2], 0) + x[5]
    B = {}
    for i, x in enumerate(F):
        n = x[3]; B.setdefault((round(n.x * 40), round(n.y * 40), round(n.z * 40), round(x[4] / (tol * 4))), []).append(i)
    def inside(p, W, n):
        ax = max(range(3), key=lambda k: abs(n[k])); i, j = [k for k in range(3) if k != ax]; sgn = 0
        for a in range(len(W)):
            A, Bv = W[a], W[(a + 1) % len(W)]; cr = (Bv[i] - A[i]) * (p[j] - A[j]) - (Bv[j] - A[j]) * (p[i] - A[i])
            if abs(cr) < 1e-12: continue
            s = 1 if cr > 0 else -1
            if sgn == 0: sgn = s
            elif s != sgn: return False
        return True
    move = {}   # (obj, vert index) -> world offset
    nud = 0
    for arr in B.values():
        if len(arr) < 2: continue
        for a in range(len(arr)):
            for b in range(a + 1, len(arr)):
                x, y = F[arr[a]], F[arr[b]]
                if x[2] == y[2] or x[3].dot(y[3]) < 0.999 or abs(x[4] - y[4]) > tol: continue
                px = [x[6]] + [(x[7][0] + x[7][k] + x[7][k + 1]) / 3 for k in range(1, len(x[7]) - 1)]
                py = [y[6]] + [(y[7][0] + y[7][k] + y[7][k + 1]) / 3 for k in range(1, len(y[7]) - 1)]
                if not (any(inside(p, y[7], y[3]) for p in px) or any(inside(p, x[7], x[3]) for p in py)): continue
                sm = x if isz[x[2]] <= isz[y[2]] else y; nud += 1
                for v in bms[sm[0]].faces[sm[1]].verts:
                    k = (sm[0], v.index); off = move.get(k, Vector()); add = sm[3] * eps
                    move[k] = Vector(tuple(max(off[q], add[q]) if add[q] > 0 else min(off[q], add[q]) for q in range(3)))
    for oi, o in enumerate(meshes):
        bm = bms[oi]; bm.verts.ensure_lookup_table(); Mi = o.matrix_world.to_3x3().inverted()
        for (o2, vi), off in move.items():
            if o2 == oi: bm.verts[vi].co += Mi @ off
        bm.to_mesh(o.data); o.data.update(); bm.free()
    return nud, removed

def finalize(budget=None, bake=True):
    _join_by_parent()
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    for o in meshes:
        bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
        if o.parent is None: bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        for p in o.data.polygons: p.use_smooth = False
    fc = fix_closed(meshes)
    zf = [0, 0]
    for _ in range(5):
        a, b = decoplanar(meshes); zf[0] += a; zf[1] += b
        if a == 0: break
    if bake: bake_light(meshes)
    mat = bpy.data.materials.get('paper') or bpy.data.materials.new('paper'); mat.use_nodes = True
    nt = mat.node_tree; bsdf = nt.nodes.get('Principled BSDF'); ca = nt.nodes.new('ShaderNodeVertexColor'); ca.layer_name = 'Col'
    nt.links.new(ca.outputs['Color'], bsdf.inputs['Base Color']); bsdf.inputs['Roughness'].default_value = 0.9
    for o in meshes: o.data.materials.clear(); o.data.materials.append(mat)
    n = tris(meshes)
    return dict(tris=n, budget=budget, ok=(budget is None or n <= budget), decoplanar=list(zf), fixclosed=list(fc), meshes=[o.name for o in meshes],
                pivots=[o.name for o in bpy.context.scene.objects if o.type == 'EMPTY' and o.name.startswith('pivot_')])

def export_glb(path):
    bpy.ops.object.select_all(action='DESELECT')
    kw = dict(filepath=path, export_format='GLB', export_yup=True, export_apply=True, use_selection=False, export_extras=True)
    try: bpy.ops.export_scene.gltf(**kw, export_vertex_color='ACTIVE')
    except TypeError: bpy.ops.export_scene.gltf(**kw, export_colors=True)
