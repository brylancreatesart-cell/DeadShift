import bpy
from mathutils import Matrix,Vector
p='C:/UnrealProjects/DeadShift/Art/Blender/'
bpy.ops.wm.open_mainfile(filepath=p+'Source/GolfCourseAssets/SM_Golf_Clubhouse_02.blend')
s=bpy.context.scene
for o in bpy.data.collections['Clubhouse_02_Editable'].objects:
 o.matrix_world=Matrix.Diagonal((1,-1,1,1)) @ o.matrix_world
 if o.type=='FONT':o.scale.x *= -1
s['Orientation']='+X North, -Y East in Blender; front South (-X). East porch inferred from NE photo.'
cam=s.camera
cam.location=(27,-32,12);cam.rotation_euler=(Vector((0,0,1.8))-cam.location).to_track_quat('-Z','Y').to_euler()
s.render.filepath=p+'Previews/GolfCourseAssets/Clubhouse02_NE.png'
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
bpy.ops.render.render(write_still=True)
cam.location=(-27,32,12);cam.rotation_euler=(Vector((0,0,1.8))-cam.location).to_track_quat('-Z','Y').to_euler()
s.render.filepath=p+'Previews/GolfCourseAssets/Clubhouse02_SW.png'
bpy.ops.render.render(write_still=True)
