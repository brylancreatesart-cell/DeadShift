"""Export the user's saved clubhouse without saving/modifying its Blender source."""
import bpy, json
from pathlib import Path
from mathutils import Vector
root=Path('C:/UnrealProjects/DeadShift/Art/Blender')
out=root/'Exports/GolfCourseAssets';out.mkdir(parents=True,exist_ok=True)
name='SM_Golf_Clubhouse_02'
bpy.ops.wm.open_mainfile(filepath=str(root/'Source/GolfCourseAssets'/f'{name}.blend'))
if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
col=bpy.data.collections.get('Clubhouse_02_Editable')
assert col,'Expected editable clubhouse collection is missing'
source=[o for o in col.objects if o.type in {'MESH','FONT'}]
assert source,'No architectural objects'
visual=[];hulls=[]
# Collision only on structural boxes. Tiny siding, signs and roof seams need no hulls.
collision_prefix=('Foundation','NorthWall','South_','West_','PorchRoomWall','DoorLintel','PorchPost','PorchHalfWall','PorchReturnPanel','Roof_West','Roof_East','SouthFrontWindow_Glass','WestWindow_Glass')
for src in source:
    dup=src.copy();dup.data=src.data.copy();bpy.context.scene.collection.objects.link(dup)
    dup.hide_viewport=False;dup.hide_render=False;dup.hide_set(False)
    bpy.ops.object.select_all(action='DESELECT');dup.select_set(True);bpy.context.view_layer.objects.active=dup
    if dup.type=='FONT':bpy.ops.object.convert(target='MESH');dup=bpy.context.object
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    visual.append(dup)
    if src.name.startswith(collision_prefix):
        h=dup.copy();h.data=dup.data.copy();bpy.context.scene.collection.objects.link(h)
        h.name=f'UCX_{name}_{len(hulls):03d}';hulls.append(h)
bpy.ops.object.select_all(action='DESELECT')
for o in visual:o.select_set(True)
bpy.context.view_layer.objects.active=visual[0];bpy.ops.object.join();mesh=bpy.context.object
mesh.name=name;mesh.data.name=name
bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.uv.smart_project(island_margin=.01);bpy.ops.object.mode_set(mode='OBJECT')
materials=[{'name':m.name,'color':list(m.diffuse_color)} for m in mesh.data.materials]
for h in hulls:
    bpy.ops.object.select_all(action='DESELECT');h.select_set(True);bpy.context.view_layer.objects.active=h
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT')
sockets=[]
for label,pos in [('North',(5,0,0)),('East',(0,-5,0))]:
    o=bpy.data.objects.new('SOCKET_'+name+'_'+label,None);bpy.context.scene.collection.objects.link(o);o.location=pos;sockets.append(o)
bpy.ops.object.select_all(action='DESELECT')
for o in [mesh]+hulls+sockets:o.select_set(True)
bpy.context.view_layer.objects.active=mesh
fbx=out/f'{name}.fbx'
bpy.ops.export_scene.fbx(filepath=str(fbx),use_selection=True,object_types={'MESH','EMPTY'},apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',bake_anim=False,add_leaf_bones=False)
report={'fbx':str(fbx),'source_objects':len(source),'dimensions_m':list(mesh.dimensions),'collision_hulls':len(hulls),'materials':materials,'vertices':len(mesh.data.vertices),'polygons':len(mesh.data.polygons),'source_saved':False}
(out/'export_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
