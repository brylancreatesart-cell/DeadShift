import unreal as u, math, json, os
l=u.get_editor_subsystem(u.LevelEditorSubsystem);l.load_level('/Game/Development/GC01/DEV_GC01_Graybox')
a=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors();b=next(x for x in a if x.get_actor_label()=='SM_Golf_Clubhouse_02');m=b.static_mesh_component.static_mesh
box=m.get_bounding_box();factor=1684.0/(box.max.x-box.min.x);b.set_actor_scale3d(u.Vector(factor,factor,factor))
names=b.static_mesh_component.get_all_socket_names();u.log('FINAL_SOCKETS '+str(names))
n=next((x for x in names if str(x).endswith('North')),None)
if n:
 p=m.find_socket(n).get_editor_property('relative_location');b.set_actor_rotation(u.Rotator(yaw=-math.degrees(math.atan2(p.y,p.x))),False)
else:
 box=m.get_bounding_box()
 if box.max.x-box.min.x>1800:b.set_actor_rotation(u.Rotator(yaw=90),False)
old=next(x for x in a if x.get_actor_label()=='Preserved_Original_NorthFacility');p=old.get_actor_location();old.set_actor_location(u.Vector(p.x,p.y,-10000),False,False);old.set_actor_enable_collision(False)
count=u.get_editor_subsystem(u.StaticMeshEditorSubsystem).get_convex_collision_count(m)
assert count==26,count
assert l.save_current_level()
u.log('FINAL_SAVED hulls='+str(count)+' rotation='+str(b.get_actor_rotation())+' bounds='+str(b.get_actor_bounds(False)))
