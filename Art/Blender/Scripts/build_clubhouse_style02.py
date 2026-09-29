"""Create a separate, editable photo-based clubhouse study; preserve original mesh."""
import bpy, math, json
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path('C:/UnrealProjects/DeadShift/Art/Blender')
DEST=ROOT/'Source/GolfCourseAssets/SM_Golf_Clubhouse_02.blend'
assert not DEST.exists(), 'Refusing to overwrite a working copy'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Source/GC01_Buildings/SM_Golf_NorthFacility_01.blend'))
s=bpy.context.scene
original=bpy.data.collections.new('Original_Preserved_DoNotEdit');s.collection.children.link(original)
for o in list(s.objects):
    for c in list(o.users_collection):c.objects.unlink(o)
    original.objects.link(o)
original.hide_render=True;original.hide_viewport=True
col=bpy.data.collections.new('Clubhouse_02_Editable');s.collection.children.link(col)
preview=bpy.data.collections.new('Preview_Only');s.collection.children.link(preview)
s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
parts=[]
def mat(name,color):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    n=m.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial')
    diffuse=n.new('ShaderNodeBsdfDiffuse');rgb=n.new('ShaderNodeShaderToRGB');ramp=n.new('ShaderNodeValToRGB');emit=n.new('ShaderNodeEmission')
    ramp.color_ramp.interpolation='CONSTANT'
    for e in list(ramp.color_ramp.elements)[2:]:ramp.color_ramp.elements.remove(e)
    ramp.color_ramp.elements[0].position=.18;ramp.color_ramp.elements[0].color=(*(v*.42 for v in color),1)
    ramp.color_ramp.elements[1].position=.7;ramp.color_ramp.elements[1].color=(*color,1)
    mid=ramp.color_ramp.elements.new(.42);mid.color=(*(v*.73 for v in color),1)
    l=m.node_tree.links;l.new(diffuse.outputs[0],rgb.inputs[0]);l.new(rgb.outputs[0],ramp.inputs[0]);l.new(ramp.outputs[0],emit.inputs[0]);l.new(emit.outputs[0],out.inputs[0])
    return m
wall=mat('Golf_CreamSiding',(.74,.72,.55));roof=mat('Golf_LightMetalRoof',(.88,.86,.71));trim=mat('Golf_DarkGreenTrim',(.055,.095,.075));glass=mat('Golf_Window',(.12,.20,.22));base=mat('Golf_Foundation',(.38,.40,.35));ink=mat('Golf_SignInk',(.025,.04,.035))
def link(o,collection):
    for c in list(o.users_collection):c.objects.unlink(o)
    collection.objects.link(o)
def box(name,loc,size,m,collection=col):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);link(o,collection)
    if collection==col:parts.append(o)
    return o
def mesh(name,verts,faces,m):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);col.objects.link(o);o.data.materials.append(m);parts.append(o);return o
# +X north, +Y east. Original 16 x 19.2 m foundation remains the sizing anchor.
box('Foundation',(0,0,.12),(16,19.2,.24),base)
# Room occupies west portion; covered porch occupies east portion.
def panel_x(name,x,a,b,z0,z1):return box(name,(x,(a+b)/2,(z0+z1)/2),(.18,b-a,z1-z0),wall)
def panel_y(name,y,a,b,z0,z1):return box(name,((a+b)/2,y,(z0+z1)/2),(b-a,.18,z1-z0),wall)
# South window y -7.4..-4.6; west window x -6.4..-3.6.
for name,fn,fixed,lo,hi,wa,wb in [('South',panel_x,-7.9,-9.5,3.1,-7.4,-4.6),('West',panel_y,-9.5,-7.9,7.9,-6.4,-3.6)]:
    fn(name+'_BelowWindow',fixed,lo,hi,.24,1.15);fn(name+'_AboveWindow',fixed,lo,hi,2.55,3.45)
    fn(name+'_WallA',fixed,lo,wa,1.15,2.55);fn(name+'_WallB',fixed,wb,hi,1.15,2.55)
panel_x('NorthWall',7.9,-9.5,3.1,.24,3.45)
panel_y('PorchRoomWall_A',3.1,-7.9,-5,.24,3.45)
panel_y('PorchRoomWall_B',3.1,-3,7.9,.24,3.45)
panel_y('DoorLintel',3.1,-5,-3,2.65,3.45)
# Low asymmetric gable: long eastern roof slope covers the porch.
ridge_y=-3.2;ridge_z=4.45
def roof_z(y):return ridge_z-(ridge_z-3.45)*(ridge_y-y)/(ridge_y+9.8) if y<ridge_y else ridge_z-(ridge_z-3.05)*(y-ridge_y)/(9.9-ridge_y)
for name,ya,yb in [('West',-9.8,ridge_y),('East',ridge_y,9.9)]:
    za,zb=roof_z(ya),roof_z(yb);angle=math.atan2(zb-za,yb-ya)
    o=box('Roof_'+name,(0,(ya+yb)/2,(za+zb)/2),(16.8,math.hypot(yb-ya,zb-za),.12),roof);o.rotation_euler.x=angle
    for i in range(29):
        rib=box('RoofSeam_'+name+'_%02d'%i,(-8.15+i*.58,(ya+yb)/2,(za+zb)/2+.075),(.025,math.hypot(yb-ya,zb-za),.025),roof);rib.rotation_euler.x=angle
    for x in [-8.35,8.35]:
        f=box('GableFascia_'+name,(x,(ya+yb)/2,(za+zb)/2-.05),(.14,math.hypot(yb-ya,zb-za),.20),trim);f.rotation_euler.x=angle
for x in [-7.9,7.9]:
    mesh('GableInfill',[(x,-9.5,3.4),(x,3.1,3.4),(x,3.1,roof_z(3.1)-.07),(x,ridge_y,4.38),(x,-9.5,roof_z(-9.5)-.07)],[(0,1,2,3,4)],wall)
for y in [-9.75,9.8]:box('EaveFascia',(0,y,roof_z(y)-.08),(16.8,.16,.24),trim)
for x in [-7.8,-4,0,4,7.8]:box('PorchPost',(x,9.35,1.63),(.20,.20,2.78),trim)
# East porch opening between x=-4 and -2. South and north return panel leave passage beside room.
for a,b in [(-7.9,-4),(-2,7.9)]:
    box('PorchHalfWall',((a+b)/2,9.35,.82),(b-a,.16,1.16),wall)
    box('PorchTopRail',((a+b)/2,9.35,1.42),(b-a,.23,.09),trim)
for x in [-7.9,7.9]:
    box('PorchReturnPanel',(x,7.05,.82),(.16,4.6,1.16),wall)
    box('PorchReturnRail',(x,7.05,1.42),(.23,4.6,.09),trim)
# Window frames with opaque stylized glazing, individual editable pieces.
def window(name,center,normal):
    x,y,z=center
    if normal=='south':
        box(name+'_Glass',(x-.02,y,z),(.045,2.68,1.28),glass)
        for q in [-1,1]:
            box(name+'_FrameV',(x-.07,y+q*1.4,z),(.16,.12,1.52),trim)
            box(name+'_FrameH',(x-.07,y,z+q*.7),(.16,2.92,.12),trim)
        box(name+'_Mullion',(x-.09,y,z),(.16,.065,1.4),trim)
    else:
        box(name+'_Glass',(x,y-.02,z),(2.68,.045,1.28),glass)
        for q in [-1,1]:
            box(name+'_FrameV',(x+q*1.4,y-.07,z),(.12,.16,1.52),trim)
            box(name+'_FrameH',(x,y-.07,z+q*.7),(2.92,.16,.12),trim)
        box(name+'_Mullion',(x,y-.09,z),(.065,.16,1.4),trim)
window('SouthFrontWindow',(-8.01,-6,1.85),'south');window('WestWindow',(-5,-9.61,1.85),'west')
# Viewed facing north, viewer-right is east (+Y): sign directly east of front window.
box('RatesSign_Frame',(-8.07,-2.75,1.95),(.16,2.5,1.8),trim)
box('RatesSign_Face',(-8.17,-2.75,1.95),(.055,2.30,1.60),roof)
for text,z,size in [('GREEN FEES',2.5,.19),('PER PERSON / 9 HOLES',2.20,.105),('RATE: TBD',1.94,.13),('CART RENTAL',1.65,.16),('PER PERSON / 9 HOLES',1.41,.105),('RATE: TBD',1.20,.12)]:
    cu=bpy.data.curves.new('RatesText','FONT');cu.body=text;cu.align_x='CENTER';cu.size=size;cu.extrude=.001
    o=bpy.data.objects.new(text,cu);col.objects.link(o);o.location=(-8.205,-2.75,z);o.rotation_euler=(math.pi/2,0,-math.pi/2);o.data.materials.append(ink)
# Readable, sparse vertical siding, cut around both windows and the front sign.
for x in [-7.95,7.95]:
    for i in range(31):
        y=-9.3+i*.4
        if x<0 and (-7.6<y<-1.4):continue
        box('VerticalSiding',(x,y,1.84),(.055,.025,3.15),wall)
for i in range(39):
    x=-7.6+i*.4
    if -6.5<x<-3.5:continue
    box('WestSiding',(x,-9.61,1.84),(.025,.035,3.15),wall)
for x in [-7.9,7.9]:
    for y in [-9.5,3.1]:box('CornerTrim',(x,y,1.85),(.18,.18,3.22),trim)
# Pack the architectural reference into this separate file.
ref=bpy.data.images.load('C:/Users/bryla/OneDrive/Pictures/clubhouse.png',check_existing=True);ref.pack()
# Blender is right-handed: use -Y east so northeast view matches the photograph.
reflection=Matrix.Diagonal((1,-1,1,1))
for o in col.objects:
    o.matrix_world=reflection @ o.matrix_world
    if o.type=='FONT':o.scale.x *= -1
s['Orientation']='+X North, -Y East in Blender; front is South (-X). East porch inferred from NE photo.'
s['DesignStatus']='Approved toon direction; footprint retained from old blockout. Heights/window sizes and hidden doorway are provisional. Prices TBD.'
s['OriginalSource']='SM_Golf_NorthFacility_01.blend preserved in hidden Original_Preserved_DoNotEdit collection'
# EEVEE identifier is stable in current Blender; use installed engine enum.
try:s.render.engine='BLENDER_EEVEE'
except TypeError:s.render.engine='BLENDER_EEVEE_NEXT'
s.world.use_nodes=True;s.world.node_tree.nodes.get('Background').inputs[0].default_value=(.5,.5,.5,1)
s.world.node_tree.nodes.get('Background').inputs[1].default_value=.6
ground=mat('PreviewGround',(.38,.44,.29));box('PreviewGround',(0,0,-.15),(200,200,.2),ground,preview)
bpy.ops.object.light_add(type='SUN',location=(15,10,30));light=bpy.context.object;link(light,preview);light.rotation_euler=(.45,-.5,-.4);light.data.energy=2.5
bpy.ops.object.camera_add(location=(27,-32,12));cam=bpy.context.object;link(cam,preview);cam.name='Camera_NE_Reference';cam.data.type='ORTHO';cam.data.ortho_scale=31
cam.rotation_euler=(Vector((0,0,1.8))-cam.location).to_track_quat('-Z','Y').to_euler();s.camera=cam
s.view_settings.view_transform='Standard';s.render.resolution_x=1200;s.render.resolution_y=800;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.filepath=str(ROOT/'Previews/GolfCourseAssets/Clubhouse02_NE.png')
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
for a in bpy.context.screen.areas:
    if a.type=='VIEW_3D':
        a.spaces.active.region_3d.view_distance=32;a.spaces.active.region_3d.view_location=(0,0,2)
bpy.ops.wm.save_as_mainfile(filepath=str(DEST))
bpy.ops.render.render(write_still=True)
cam.location=(-27,32,12);cam.rotation_euler=(Vector((0,0,1.8))-cam.location).to_track_quat('-Z','Y').to_euler()
s.render.filepath=str(ROOT/'Previews/GolfCourseAssets/Clubhouse02_SW.png');bpy.ops.render.render(write_still=True)
report={'blend':str(DEST),'editable_mesh_parts':len(parts),'original_preserved':True,'footprint_m':[16,19.2],'south_window_y':-6,'west_window_x':-5,'south_rates_sign_y':-2.75,'prices':'TBD','Unreal_integration':'Not exported or imported; modeling review only'}
(ROOT/'Previews/GolfCourseAssets/Clubhouse02_Report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
