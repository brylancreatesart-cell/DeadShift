import bpy, math, json
from pathlib import Path
from mathutils import Vector

ROOT=Path(r'C:\UnrealProjects\DeadShift\Art\Blender')
OUT=Path(r'C:\Users\bryla\Documents\Codex\2026-09-27\referenced-chatgpt-conversation-this-is-an\outputs')
NAME='SM_Golf_NorthFacility_01'
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'
scene.unit_settings.scale_length=1.0

def material(name,color,metal=0,rough=.65):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Metallic'].default_value=metal; bs.inputs['Roughness'].default_value=rough
    return m
wall=material('Painted warm gray siding',(.52,.53,.48))
roof=material('Light metal roofing',(.7,.72,.69),.45,.4)
trim=material('Dark fascia and frames',(.16,.20,.18),.2)
glass=material('Opaque blue gray glazing',(.12,.22,.25),.35,.25)
concrete=material('Concrete base',(.4,.41,.38))
parts=[]
def box(name,loc,size,mat,bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mat)
    if bevel:
        mod=o.modifiers.new('Edge highlights','BEVEL');mod.width=bevel;mod.segments=2
        bpy.ops.object.modifier_apply(modifier=mod.name)
    parts.append(o);return o
# Match the blockout's 16m X / 19.2m Y footprint and 4.5m maximum height.
box('Foundation',(0,0,.12),(16,19.2,.24),concrete,.03)
box('Exterior shell',(0,0,1.95),(15.8,19,3.5),wall,.025)
# Closed gable volume; ridge along Y. Facades and roof profile are provisional.
verts=[(-7.9,-9.5,3.7),(7.9,-9.5,3.7),(0,-9.5,4.35),
       (-7.9,9.5,3.7),(7.9,9.5,3.7),(0,9.5,4.35)]
mesh=bpy.data.meshes.new('GableMesh');mesh.from_pydata(verts,[],[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)]);mesh.update()
o=bpy.data.objects.new('Gable ends',mesh);scene.collection.objects.link(o);o.data.materials.append(wall);parts.append(o)
slope=math.atan2(.65,7.9)
for side in (-1,1):
    o=box('Roof panel',(side*4,0,4.06),(8.08,19.2,.10),roof)
    o.rotation_euler[1]=side*slope
    # Raised standing seams running down the slope; one every 80cm along ridge.
    for j in range(24):
        seam=box('Roof seam',(side*4,-9.2+j*.8,4.12),(8.07,.025,.025),roof)
        seam.rotation_euler[1]=side*slope
box('Ridge cap',(0,0,4.43),(.18,19.2,.10),roof,.015)
for side in (-1,1):
    box('Eave fascia',(side*7.92,0,3.70),(.12,19.2,.18),trim)
    for y in (-9.46,9.46):
        box('Corner trim',(side*7.88,y,1.98),(.10,.10,3.45),trim)
# South-facing entry (-X): shallow surface details, no interior or working doors.
box('Entry frame',(-7.93,-4,1.4),(.10,1.55,2.5),trim,.02)
box('Entry door',(-8.0,-4,1.4),(.06,1.32,2.25),wall,.01)
box('Door glazing',(-8.04,-4,1.85),(.025,.93,.9),glass)
box('Door handle',(-8.075,-3.53,1.28),(.07,.035,.25),trim,.008)
for y in (0,4.2):
    box('Window frame',(-7.96,y,2.1),(.12,2.5,1.5),trim,.02)
    box('Window glass',(-8.035,y,2.1),(.035,2.28,1.28),glass)
    box('Window mullion',(-8.06,y,2.1),(.03,.05,1.3),trim)
box('Entry canopy',(-8.5,-4,2.85),(1.15,2.1,.12),roof,.025)
for x in (-4,3.5):
    box('Side window frame',(x,-9.54,2.1),(2.4,.12,1.5),trim,.02)
    box('Side window glass',(x,-9.615,2.1),(2.18,.03,1.28),glass)

# Join the exterior into a single game mesh with ground-centered pivot and UVs.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
bpy.ops.object.join();building=bpy.context.object;building.name=NAME;building.data.name=NAME
scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.uv.smart_project(island_margin=.015)
bpy.ops.object.mode_set(mode='OBJECT')
building['reference_status']='Approximate exterior: blockout footprint; roof and facades inferred, not surveyed.'
building['unreal_location_cm']='80, 0, 0'
building['replacement_tag']='DeadShift_GC01_Replacement_NorthFacility'
parts=[]
collision=box('UCX_'+NAME+'_00',(0,0,2.25),(16,19.2,4.5),concrete)
collision.display_type='WIRE';collision.hide_render=True
# Export only mesh and simple convex collision. FBX unit metadata converts meters to cm.
bpy.ops.object.select_all(action='DESELECT')
building.select_set(True);collision.select_set(True);bpy.context.view_layer.objects.active=building
fbx=ROOT/'Exports/GC01_Buildings'/f'{NAME}.fbx'
bpy.ops.export_scene.fbx(filepath=str(fbx),use_selection=True,object_types={'MESH'},
    apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',
    bake_anim=False,add_leaf_bones=False)
collision.hide_set(True)
# Studio preview, excluded from exported asset.
floor=box('Preview ground',(0,0,-.11),(200,200,.2),material('Studio ground',(.13,.17,.16)))
floor.hide_select=True
world=scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.32,.39,.46,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.5
for loc,power,size in [((-15,-12,22),3500,12),((10,6,15),2400,10)]:
    bpy.ops.object.light_add(type='AREA',location=loc)
    lamp=bpy.context.object;lamp.data.energy=power;lamp.data.shape='DISK';lamp.data.size=size
    lamp.rotation_euler=(Vector((0,0,2))-lamp.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(-28,-30,22))
cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,1.8))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=33;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=24
scene.render.resolution_x=1280;scene.render.resolution_y=960;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.filepath=str(OUT/'NorthFacility-preview.png')
bpy.ops.object.select_all(action='DESELECT');building.select_set(True);bpy.context.view_layer.objects.active=building
blend=ROOT/'Source/GC01_Buildings'/f'{NAME}.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
bpy.ops.render.render(write_still=True)
report={'name':NAME,'vertices':len(building.data.vertices),'polygons':len(building.data.polygons),
        'dimensions_m':list(building.dimensions),'scale':list(building.scale),'uv_layers':len(building.data.uv_layers),
        'source':str(blend),'export':str(fbx),'status':'Unreal import and in-game collision not yet tested'}
(OUT/'NorthFacility-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
