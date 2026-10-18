"""Blender: decimate a built raw glb into a low-poly filler variant (vertex colours kept). Used for mass / far-ring decor only.
usage: blender -b --factory-startup -P tools/models/lod.py -- <in.raw.glb> <out.raw.glb> <ratio>"""
import bpy, sys
a = sys.argv[sys.argv.index('--') + 1:]; src, out, ratio = a[0], a[1], float(a[2])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
n0 = n1 = 0
for o in [o for o in bpy.context.scene.objects if o.type == 'MESH']:
    n0 += sum(len(p.vertices) - 2 for p in o.data.polygons)
    bpy.context.view_layer.objects.active = o; m = o.modifiers.new('lod', 'DECIMATE'); m.ratio = ratio; m.use_collapse_triangulate = True
    bpy.ops.object.modifier_apply(modifier=m.name)
    n1 += sum(len(p.vertices) - 2 for p in o.data.polygons)
kw = dict(filepath=out, export_format='GLB', export_yup=True, export_apply=True, export_extras=True)
try: bpy.ops.export_scene.gltf(**kw, export_vertex_color='ACTIVE')
except TypeError: bpy.ops.export_scene.gltf(**kw, export_colors=True)
print('LOD', src, n0, '->', n1)
