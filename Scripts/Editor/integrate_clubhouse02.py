"""Import saved clubhouse, replace only identified northern facility, preserve course."""
import unreal as u, json, os
P=u.Paths.project_dir()
ROOT='/Game/GolfCourseAssets/Clubhouse'
MAP='/Game/Development/GC01/DEV_GC01_Graybox'
report=json.load(open(os.path.join(P,'Art/Blender/Exports/GolfCourseAssets/export_report.json')))
level=u.get_editor_subsystem(u.LevelEditorSubsystem);actors=u.get_editor_subsystem(u.EditorActorSubsystem)
assert level.load_level(MAP)
allactors=actors.get_all_level_actors()
before=[{'label':a.get_actor_label(),'class':a.get_class().get_name(),'location':str(a.get_actor_location()),'scale':str(a.get_actor_scale3d())} for a in allactors if any(w in a.get_actor_label().lower() for w in ['facility','club','north','player'])]
u.log('CLUBHOUSE_EXISTING '+json.dumps(before))
target=[a for a in allactors if a.get_actor_label() in ['GC01_NorthFacility','NorthFacility','SM_Golf_NorthFacility_01']]
assert len(target)==1, 'Ambiguous original facility; inspect CLUBHOUSE_EXISTING before making map changes'
old=target[0]
task=u.AssetImportTask();task.filename=report['fbx'];task.destination_path=ROOT;task.destination_name='SM_Golf_Clubhouse_02';task.automated=True;task.save=True;task.replace_existing=False
options=u.FbxImportUI();options.import_mesh=True;options.import_materials=False;options.import_textures=False;options.import_as_skeletal=False
options.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH
options.static_mesh_import_data.combine_meshes=True;options.static_mesh_import_data.auto_generate_collision=False
options.static_mesh_import_data.one_convex_hull_per_ucx=True
task.options=options
task.factory=u.FbxFactory()
u.SystemLibrary.execute_console_command(u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
if not u.EditorAssetLibrary.does_asset_exist(ROOT+'/SM_Golf_Clubhouse_02'):
    u.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
u.log('CLUBHOUSE_IMPORTED '+str(task.imported_object_paths))
mesh=u.load_asset(ROOT+'/SM_Golf_Clubhouse_02');assert isinstance(mesh,u.StaticMesh)
u.log('CLUBHOUSE_BOUNDS '+str(mesh.get_bounding_box()))
for socket_name in ['North','East','SM_Golf_Clubhouse_02_North','SM_Golf_Clubhouse_02_East']:
    socket=mesh.find_socket(socket_name)
    if socket:u.log('CLUBHOUSE_SOCKET '+socket_name+' '+str(socket.get_editor_property('relative_location')))
matlib=u.MaterialEditingLibrary
byname={r['name']:r['color'] for r in report['materials']}
for i,slot in enumerate(mesh.get_editor_property('static_materials')):
    name=str(slot.material_slot_name);color=byname.get(name)
    if color is None:
        matches=[v for k,v in byname.items() if k.replace(' ','_').replace('.','_')==name]
        color=matches[0] if matches else [.55,.55,.5,1]
    path=ROOT+'/Materials';assetname='M_'+name.replace('.','_').replace(' ','_')
    mat=u.load_asset(path+'/'+assetname) or u.AssetToolsHelpers.get_asset_tools().create_asset(assetname,path,u.Material,u.MaterialFactoryNew())
    rgb=matlib.create_material_expression(mat,u.MaterialExpressionConstant3Vector,-200,0);rgb.set_editor_property('constant',u.LinearColor(*color))
    matlib.connect_material_property(rgb,'',u.MaterialProperty.MP_BASE_COLOR)
    rough=matlib.create_material_expression(mat,u.MaterialExpressionConstant,-200,150);rough.set_editor_property('r',.85);matlib.connect_material_property(rough,'',u.MaterialProperty.MP_ROUGHNESS)
    matlib.recompile_material(mat);u.EditorAssetLibrary.save_loaded_asset(mat);mesh.set_material(i,mat)
u.EditorAssetLibrary.save_loaded_asset(mesh)
# Original ground-centered building footprint is X=80,Y=0 and 16x19.2 metres.
b=old.get_actor_bounds(False);u.log('CLUBHOUSE_OLD_BOUNDS '+str(b))
loc=old.get_actor_location()
origin=u.Vector(loc.x,loc.y,b[0].z-b[1].z)
actor=actors.spawn_actor_from_class(u.StaticMeshActor,origin)
actor.set_actor_label('SM_Golf_Clubhouse_02');actor.set_folder_path('GolfCourseAssets/Clubhouse')
actor.static_mesh_component.set_static_mesh(mesh);actor.static_mesh_component.set_collision_profile_name('BlockAll')
actor.tags=[u.Name('DeadShift_GC01_Replacement_NorthFacility')]
# Preserve the old placeholder hidden in the level for reversal.
old.set_actor_hidden_in_game(True);old.set_is_temporarily_hidden_in_editor(True);old.set_actor_enable_collision(False)
old.set_actor_label('Preserved_Original_NorthFacility');old.set_folder_path('Preserved/PreClubhouseIntegration')
old.set_actor_location(u.Vector(loc.x,loc.y,-10000),False,False) # Keep it out of view after editor reload too.
old.tags=[t for t in old.tags if str(t)!='DeadShift_GC01_Generated']
u.log('CLUBHOUSE_NEW_BOUNDS '+str(actor.get_actor_bounds(False)))
u.log('CLUBHOUSE_COLLISION '+str(mesh.get_editor_property('body_setup')))
assert level.save_current_level()
out={'map':MAP,'asset':mesh.get_path_name(),'old':before,'origin_cm':[origin.x,origin.y,origin.z],'new_bounds':str(actor.get_actor_bounds(False)),'material_slots':len(mesh.get_editor_property('static_materials')),'other_actors_preserved':len(allactors)-1}
with open(os.path.join(P,'Docs/Environment/MedfordGolfCourse/UnrealIntegration.json'),'w') as f:json.dump(out,f,indent=2)
u.log('CLUBHOUSE_INTEGRATION_SAVED')

