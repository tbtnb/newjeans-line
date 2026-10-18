"""Blender: render impostor sprites of shipped OMG-C models (tools/models/build.sh raw exports), iso view matching the key camera
(~36 deg down), transparent, flat baked vertex colours, no outline. usage: blender -b --factory-startup -P render.py -- <out_dir> <px> id [id...]"""
import bpy, sys, os, math, json
from mathutils import Vector
argv = sys.argv[sys.argv.index('--') + 1:]; out, px, ids = argv[0], int(argv[1]), argv[2:]
root = os.environ.get('RAW', '/tmp/omgc-build')   # uncompressed Blender exports <id>.raw.glb (the shipped glbs are meshopt-compressed)
os.makedirs(out, exist_ok=True)
for aid in ids:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=os.path.join(root, aid + '.raw.glb'))
    sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'
    sh = sc.display.shading; sh.light = 'FLAT'; sh.color_type = 'VERTEX'; sh.show_object_outline = False
    sc.render.film_transparent = True; sc.render.resolution_x = sc.render.resolution_y = px
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'; sc.view_settings.view_transform = 'Standard'
    sc.render.filter_size = 1.2
    pts = [o.matrix_world @ Vector(c) for o in sc.objects if o.type == 'MESH' for c in o.bound_box]
    lo = Vector([min(p[k] for p in pts) for k in range(3)]); hi = Vector([max(p[k] for p in pts) for k in range(3)])
    ctr = (lo + hi) / 2; ext = hi - lo
    cd = bpy.data.cameras.new('c'); cd.type = 'ORTHO'; cam = bpy.data.objects.new('c', cd); sc.collection.objects.link(cam); sc.camera = cam
    # glTF +Z (model front) imports as Blender -Y; look from the front, 36 deg above
    el = math.radians(36); d = Vector((0, -math.cos(el), math.sin(el)))
    cam.location = ctr + d * (max(ext) * 4 + 10); cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler(); cd.clip_end = 1000
    # fit: projected height = h*cos(el) + depth*sin(el); width = max(w, d)
    cd.ortho_scale = max(ext.x, ext.y * math.sin(el) + ext.z * math.cos(el)) * 1.04
    sc.render.filepath = os.path.join(out, aid + '.png'); bpy.ops.render.render(write_still=True)
    json.dump(dict(id=aid, ext=[round(x, 3) for x in ext], ortho=cd.ortho_scale, px=px), open(os.path.join(out, aid + '.json'), 'w'))
    print('IMP', aid, [round(x, 2) for x in ext])
