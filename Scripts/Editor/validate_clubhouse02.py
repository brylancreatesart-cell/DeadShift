import unreal as u, time, json, os, traceback
P=u.Paths.project_dir();MAP='/Game/Development/GC01/DEV_GC01_Graybox'
lev=u.get_editor_subsystem(u.LevelEditorSubsystem);ed=u.get_editor_subsystem(u.UnrealEditorSubsystem);act=u.get_editor_subsystem(u.EditorActorSubsystem)
assert lev.load_level(MAP)
world=ed.get_editor_world();allactors=act.get_all_level_actors()
building=next(a for a in allactors if a.get_actor_label()=='SM_Golf_Clubhouse_02')
mesh=building.static_mesh_component.static_mesh
count=u.get_editor_subsystem(u.StaticMeshEditorSubsystem).get_convex_collision_count(mesh)
if count<20:
    u.log('CLUBHOUSE_REPAIR_COLLISION initial_hulls='+str(count))
    mats={str(s.material_slot_name):s.material_interface for s in mesh.get_editor_property('static_materials')}
    u.SystemLibrary.execute_console_command(world,'Interchange.FeatureFlags.Import.FBX 0')
    task=u.AssetImportTask();task.filename=os.path.join(P,'Art/Blender/Exports/GolfCourseAssets/SM_Golf_Clubhouse_02.fbx');task.destination_path='/Game/GolfCourseAssets/Clubhouse';task.destination_name='SM_Golf_Clubhouse_02';task.automated=True;task.save=True;task.replace_existing=True;task.replace_existing_settings=True;task.factory=u.FbxFactory()
    options=u.FbxImportUI();options.import_mesh=True;options.import_materials=False;options.import_textures=False;options.import_as_skeletal=False;options.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH
    options.static_mesh_import_data.combine_meshes=True;options.static_mesh_import_data.auto_generate_collision=False;options.static_mesh_import_data.one_convex_hull_per_ucx=True
    task.options=options;u.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    mesh=u.load_asset('/Game/GolfCourseAssets/Clubhouse/SM_Golf_Clubhouse_02')
    for i,slot in enumerate(mesh.get_editor_property('static_materials')):
        material=mats.get(str(slot.material_slot_name))
        if material:mesh.set_material(i,material)
    u.EditorAssetLibrary.save_loaded_asset(mesh)
    building.static_mesh_component.set_static_mesh(mesh)
    count=u.get_editor_subsystem(u.StaticMeshEditorSubsystem).get_convex_collision_count(mesh)
    u.log('CLUBHOUSE_REPAIRED_HULLS '+str(count))
assert count>=20, 'Missing structural collision'
size=mesh.get_bounding_box();assert 1600<size.max.x-size.min.x<1750 and 1900<size.max.y-size.min.y<2050
origin=building.get_actor_location()
assert all(mesh.get_material(i) for i in range(mesh.get_num_sections(0)))
old=next(a for a in allactors if a.get_actor_label()=='Preserved_Original_NorthFacility')
assert not old.get_actor_enable_collision()
if old.get_actor_location().z>-9000:
    p=old.get_actor_location();old.set_actor_location(u.Vector(p.x,p.y,-10000),False,False)
nav=next((a for a in allactors if a.get_actor_label()=='Clubhouse_LocalNavigation'),None)
if not nav:
    nav=act.spawn_actor_from_class(u.NavMeshBoundsVolume,origin+u.Vector(0,0,150));nav.set_actor_label('Clubhouse_LocalNavigation');nav.set_folder_path('GolfCourseAssets/Clubhouse');nav.set_actor_scale3d(u.Vector(11,13,6))
report={'collision_hulls':count,'size_cm':[size.max.x-size.min.x,size.max.y-size.min.y,size.max.z-size.min.z],'materials_assigned':True,'tests':[]}
cases=[('Porch entrance',(-300,1150), (0,-1),400,650),('Room doorway',(-400,520),(0,-1),300,650),('North wall blocks',(600,0),(1,0),60,185)]
def vec(p,z=140):return origin+u.Vector(p[0],p[1],z)
u.EditorPythonScripting.set_keep_python_script_alive(True)
start=time.monotonic();last=start;stage='nav';index=0;player=None;position=None
def finish(ok,msg):
    report['passed']=ok;report['message']=msg
    with open(os.path.join(P,'Docs/Environment/MedfordGolfCourse/UnrealValidation.json'),'w') as f:json.dump(report,f,indent=2)
    u.log('CLUBHOUSE_TEST_'+('PASS' if ok else 'FAIL')+' '+msg)
    u.unregister_slate_post_tick_callback(handle)
    if lev.is_in_play_in_editor():lev.editor_request_end_play()
    u.EditorPythonScripting.set_keep_python_script_alive(False)
def tick(delta):
    global stage,last,index,player,position
    try:
        now=time.monotonic()
        if now-start>150:finish(False,'Timeout '+stage);return
        if stage=='nav' and now-start>2:
            u.SystemLibrary.execute_console_command(world,'RebuildNavigation');stage='navwait';last=now
        elif stage=='navwait' and now-last>6:
            path=u.NavigationSystemV1.find_path_to_location_synchronously(world,vec((-300,1150),40),vec((-400,100),40))
            if not(path and path.is_valid() and not path.is_partial()):
                if now-last>45:finish(False,'Porch-to-room navigation unavailable')
                return
            report['porch_to_room_navigation']=True
            lev.save_current_level();stage='savewait';last=now
        elif stage=='savewait' and now-last>3:lev.editor_request_begin_play();stage='pie'
        elif stage=='pie':
            game=ed.get_game_world()
            if not game:return
            player=u.GameplayStatics.get_player_pawn(game,0)
            if not player:return
            assert isinstance(player,u.Character),'Default pawn is not playable character'
            capsule=player.get_editor_property('capsule_component');report['capsule_cm']=[capsule.get_scaled_capsule_radius(),capsule.get_scaled_capsule_half_height()]
            stage='place'
        elif stage=='place':
            if index==len(cases):finish(True,'Player scale, porch entry, room doorway, wall collision, navigation and material assignments verified');return
            player.set_actor_location(vec(cases[index][1]),False,False);player.get_editor_property('character_movement').stop_movement_immediately();last=now;stage='settle'
        elif stage=='settle' and now-last>1:
            assert player.get_editor_property('character_movement').is_moving_on_ground(),'Player not grounded '+cases[index][0]
            position=player.get_actor_location();stage='walk';last=now
        elif stage=='walk':
            direction=cases[index][2];player.add_movement_input(u.Vector(*direction,0),1,True)
            if now-last>1.25:
                d=player.get_actor_location()-position;dist=d.x*direction[0]+d.y*direction[1]
                report['tests'].append({'name':cases[index][0],'distance_cm':dist})
                assert cases[index][3]<=dist<=cases[index][4],cases[index][0]+' distance '+str(dist)
                assert player.get_editor_property('character_movement').is_moving_on_ground(),'Traversal lost ground'
                index+=1;stage='place'
    except Exception:finish(False,traceback.format_exc())
handle=u.register_slate_post_tick_callback(tick)
