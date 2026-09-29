import bpy, json, math
from pathlib import Path
from mathutils import Vector
root=Path('C:/UnrealProjects/DeadShift/Art/Blender')
p=root/'Source/GolfCourseAssets/SM_Golf_Clubhouse_02.blend'
bpy.ops.wm.open_mainfile(filepath=str(p))
s=bpy.context.scene; col=bpy.data.collections['Clubhouse_02_Editable']
prefixes=('VerticalSiding','WestSiding','SidingRib_')
def unchanged():
 return {o.name:(tuple(v for row in o.matrix_world for v in row),len(o.data.vertices) if o.type=='MESH' else o.data.body if o.type=='FONT' else o.type) for o in col.objects if not o.name.startswith(prefixes)}
before=unchanged()
for o in list(col.objects):
 if o.name.startswith(prefixes):bpy.data.objects.remove(o,do_unlink=True)
m=bpy.data.materials.get('Golf_SidingRibs')
if m is None:
 m=bpy.data.materials['Golf_CreamSiding'].copy();m.name='Golf_SidingRibs'
 for n in m.node_tree.nodes:
  if n.type=='VALTORGB':
   for e in n.color_ramp.elements:
    c=e.color;e.color=(c[0]*.88,c[1]*.88,c[2]*.88,c[3])
 m.diffuse_color=tuple(v*.88 for v in m.diffuse_color[:3])+(1,)
count=0
def rib(axis,plane,pos,low,high):
 global count
 if high-low<.04:return
 bpy.ops.mesh.primitive_cube_add(size=1)
 o=bpy.context.object;o.name='SidingRib_%03d'%count;count+=1
 o.location=(plane,pos,(low+high)/2) if axis=='x' else (pos,plane,(low+high)/2)
 o.dimensions=(.038,.045,high-low) if axis=='x' else (.045,.038,high-low)
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);o.data.materials.append(m)
def strip(axis,plane,a,b,bottom,top,holes=()):
 n=int((b-a)/.32)
 for i in range(n+1):
  t=a+(b-a)*i/n;hi=top(t) if callable(top) else top;segments=[(bottom,hi)]
  for lo_t,hi_t,lo_z,hi_z in holes:
   if lo_t<=t<=hi_t:
    result=[]
    for lo,up in segments:
     if lo_z>=up or hi_z<=lo:result.append((lo,up))
     else:
      if lo<lo_z:result.append((lo,lo_z))
      if hi_z<up:result.append((hi_z,up))
    segments=result
  for lo,up in segments:rib(axis,plane,t,lo,up)
def top(y):
 y=-y
 return (4.45-(4.45-3.45)*(-3.2-y)/6.6 if y<-3.2 else 4.45-(4.45-3.05)*(y+3.2)/13.1)-.16
strip('x',8.012,-3.02,9.4,.27,top)
strip('x',-8.012,-3.02,9.4,.27,top,[(4.48,7.52,1.08,2.63),(1.42,4.08,1.0,2.91)])
strip('y',9.617,-7.75,7.75,.27,3.37,[(-6.52,-3.48,1.08,2.63)])
strip('y',-3.215,-7.75,7.75,.27,3.37,[(-5.05,-2.95,.24,2.7)])
for a,b in [(-7.78,-4.1),(-1.9,7.78)]:strip('y',-9.446,a,b,.29,1.35)
for x in [-8.01,8.01]:strip('x',x,-9.2,-4.84,.29,1.35)
assert before==unchanged(),'Non-siding object changed'
s['SidingRevision']='Photo-based vertical metal ribs, 0.32 m nominal spacing; openings and sign kept clear.'
cam=s.camera;cam.location=(27,-32,12);cam.rotation_euler=(Vector((0,0,1.8))-cam.location).to_track_quat('-Z','Y').to_euler()
s.render.filepath=str(root/'Previews/GolfCourseAssets/Clubhouse02_NE.png')
bpy.ops.wm.save_as_mainfile(filepath=str(p));bpy.ops.render.render(write_still=True)
cam.location=(-27,32,12);cam.rotation_euler=(Vector((0,0,1.8))-cam.location).to_track_quat('-Z','Y').to_euler()
s.render.filepath=str(root/'Previews/GolfCourseAssets/Clubhouse02_SW.png');bpy.ops.render.render(write_still=True)
print(json.dumps({'siding_ribs':count,'non_siding_objects_unchanged':len(before),'saved':str(p)}))
