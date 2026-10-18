"""Blender entry: blender -b --factory-startup -P tools/models/run.py -- <asset_id> <out_dir> [<spec.json>]
Builds tools/models/assets/<id>.py:build(P, spec) -> raw .glb + ortho renders (front/side/top/iso, transparent) + report json."""
import bpy, sys, json, math, importlib.util, os
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import paper as P

argv = sys.argv[sys.argv.index('--') + 1:]
aid, out = argv[0], argv[1]; spec_path = argv[2] if len(argv) > 2 else ''
spec = json.load(open(spec_path)) if spec_path and os.path.exists(spec_path) else {}
item = argv[3] if len(argv) > 3 and argv[3] != '' else None
if item is not None and 'items' in spec:   # kit sheet item: {en, cn, size_m (largest extent, m), tris} + the kit's id
    it = spec['items'][int(item)]; spec = dict(it, kit=spec['id'], item=int(item), tris_budget=it.get('tris'))
os.makedirs(out, exist_ok=True)

P.reset(); P.seed(sum(map(ord, aid)))
mod_path = os.path.join(HERE, 'assets', aid + '.py')
sp = importlib.util.spec_from_file_location('asset_' + aid.replace('-', '_'), mod_path); mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod)
mod.build(P, spec)
budget = spec.get('tris_budget') or spec.get('budget') or getattr(mod, 'BUDGET', None)
rep = P.finalize(budget=budget)
raw = os.path.join(out, aid + '.raw.glb'); P.export_glb(raw)

# ---- ortho renders (Workbench, flat lighting = exactly the baked vertex colours) ----
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading; sh.light = 'FLAT'; sh.color_type = 'VERTEX'; sh.show_object_outline = True; sh.object_outline_color = (0.25, 0.2, 0.3)
sc.render.film_transparent = True; sc.render.resolution_x = sc.render.resolution_y = 640
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
sc.view_settings.view_transform = 'Standard'
pts = [o.matrix_world @ Vector(c) for o in sc.objects if o.type == 'MESH' for c in o.bound_box]
lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts))); hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
ctr = (lo + hi) / 2; ext = hi - lo; R = max(ext) * 0.6 + 0.05
cam_d = bpy.data.cameras.new('cam'); cam_d.type = 'ORTHO'; cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam_d.clip_end = 1000
def shoot(name, direction, scale):
    d = Vector(direction).normalized(); cam.location = ctr + d * (R * 6 + 10)
    cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler(); cam_d.ortho_scale = scale
    if abs(d.z) > 0.99: cam.rotation_euler = (0, 0, 0)   # plan view: back (+Y) up, front at the bottom (design sheet convention)
    sc.render.filepath = os.path.join(out, f'{aid}-{name}.png'); bpy.ops.render.render(write_still=True)
S = max(ext) * 1.12 + 0.05
shoot('front', (0, -1, 0), S); shoot('side', (1, 0, 0), S); shoot('top', (0, 0, 1), S)
shoot('iso', (0.75, -1.0, 0.85), S * 1.15)
rep.update(id=aid, size=[round(ext.x, 3), round(ext.y, 3), round(ext.z, 3)], raw=raw)
json.dump(rep, open(os.path.join(out, aid + '.report.json'), 'w'), indent=1)
print('REPORT', json.dumps(rep))
