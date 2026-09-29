"""Run in Unreal Editor Python. Provisional dimensions in cm; no surveyed layout."""
import unreal

MAP = "/Game/Development/GC01/DEV_GC01_Graybox"
MATERIAL_DIR = "/Game/Development/GC01/Materials"
TAG = "DeadShift_GC01_Generated"
GAME_MODE = "/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode"

# Full-course visual blockout traced from supplied medfprd golf course.png.
# Reference coordinates are pixels in the 1007 x 685 image. Image-up is
# planning north (+X); image-right is east (+Y). This is NOT georeferenced.
# 0.8 m/pixel is an adjustable visual estimate, not a measured scale.
CM_PER_PIXEL = 80.0
ORIGIN_PX = (460, 575)
def xy(point):
    return ((ORIGIN_PX[1] - point[1]) * CM_PER_PIXEL,
            (point[0] - ORIGIN_PX[0]) * CM_PER_PIXEL)

OUTLINE_PX = [(9, 5), (991, 35), (997, 45), (626, 652),
              (615, 668), (315, 657), (15, 342), (14, 211),
              (4, 145), (11, 91), (5, 45)]
# Neutral footprint names: use and height cannot be established from aerials.
# label, pixel center, pixel width/height, provisional height in centimeters.
BUILDINGS_PX = [
    ('NorthFacility', (460, 574), (24, 20), 450),
    ('LongNarrowStructure', (402, 617), (45, 10), 300),
    ('WestSouth_Main', (369, 630), (11, 13), 300),
    ('WestSouth_EastWing', (378, 634), (8, 9), 270),
    ('MiddleSouth_Main', (410, 630), (11, 13), 300),
    ('MiddleSouth_EastWing', (419, 634), (8, 9), 270),
    ('EastSouth_Main', (450, 631), (11, 13), 300),
    ('EastSouth_EastWing', (459, 635), (8, 9), 270),
    ('SoutheastBuilding', (499, 632), (25, 14), 450),
]
GREENS_PX = [(60, 81, 35, 36), (37, 142, 28, 32),
             (134, 205, 41, 44), (463, 57, 30, 25),
             (564, 95, 29, 33), (571, 319, 32, 29),
             (457, 427, 34, 32), (258, 501, 26, 27),
             (350, 580, 41, 41), (485, 552, 31, 26),
             (635, 572, 34, 28), (574, 627, 40, 52)]
POND_PX = (547, 256, 22, 35)
WOODS_PX = [(658, 230), (687, 168), (782, 137), (887, 54),
            (953, 36), (908, 120), (849, 228), (791, 330),
            (750, 365), (681, 335)]
TREE_PIXELS = [(33,112),(87,113),(161,145),(116,171),(178,209),
               (222,257),(307,332),(331,378),(340,399),(391,407),
               (299,449),(309,462),(326,482),(428,573),(434,585),
               (377,554),(286,570),(365,604),(488,582),(501,585),
               (516,588),(537,612),(540,631),(547,650),(586,653),
               (607,636),(624,608),(646,589),(604,546),(602,514),
               (602,490),(601,463),(595,440),(593,416),(587,395),
               (576,378),(537,556),(535,528),(536,503),(540,478),
               (557,432),(529,453),(449,452),(485,449),(410,496),
               (444,542),(491,293),(507,299),(498,321),(510,340),
               (528,350),(548,363),(578,347),(599,343),(587,306),
               (565,279),(589,234),(637,144),(601,85),(506,45),
               (455,42),(369,49),(307,107),(288,106),(254,102),
               (101,47),(221,462),(235,477)]

def inside(point, polygon):
    x, y = point
    result = False
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        if (a[1] > y) != (b[1] > y):
            crossing = a[0] + (y-a[1]) * (b[0]-a[0]) / (b[1]-a[1])
            if x < crossing:
                result = not result
    return result

# Random forest scatter, repeatable across regeneration. Positions are estimates.
# Change the seed for a different arrangement; density matches the previous grove.
FOREST_SEED = 270926
FOREST_TREE_COUNT = 127
FOREST_MIN_SPACING_PX = 12.0

def scatter_forest():
    import random
    rng = random.Random(FOREST_SEED)
    points = []
    min_u = min(p[0] for p in WOODS_PX)
    max_u = max(p[0] for p in WOODS_PX)
    min_v = min(p[1] for p in WOODS_PX)
    max_v = max(p[1] for p in WOODS_PX)
    for _ in range(FOREST_TREE_COUNT * 1000):
        point = (rng.uniform(min_u, max_u), rng.uniform(min_v, max_v))
        if not inside(point, WOODS_PX) or not inside(point, OUTLINE_PX):
            continue
        if any((point[0]-other[0])**2 + (point[1]-other[1])**2
               < FOREST_MIN_SPACING_PX**2 for other in TREE_PIXELS + points):
            continue
        points.append(point)
        if len(points) == FOREST_TREE_COUNT:
            return points
    raise ValueError('Forest scatter could not fit the requested density; no map changed.')

FOREST_PIXELS = scatter_forest()
TREE_PIXELS.extend(FOREST_PIXELS)
TREE_POSITIONS = [xy(p) for p in TREE_PIXELS]
TREE = {'trunk_diameter': 60, 'trunk_height': 500,
        'canopy_diameter': 850, 'canopy_height': 500}

BOXES = []
# Narrow contiguous ground bands approximate the traced irregular boundary.
# No terrain sculpting or surveyed elevation is implied.
for v in range(5, 668, 3):
    height = min(3, 668-v)
    mid = v + height/2
    crossings = []
    for a, b in zip(OUTLINE_PX, OUTLINE_PX[1:] + OUTLINE_PX[:1]):
        if (a[1] > mid) != (b[1] > mid):
            crossings.append(a[0] + (mid-a[1])*(b[0]-a[0])/(b[1]-a[1]))
    crossings.sort()
    for j in range(0, len(crossings), 2):
        left, right = crossings[j:j+2]
        BOXES.append(('GroundBand_%03d_%d' % (v,j), xy(((left+right)/2,mid)),
                      (height*CM_PER_PIXEL,(right-left)*CM_PER_PIXEL,100),
                      -100,'grass',True))
for label, center, size, height in BUILDINGS_PX:
    BOXES.append((label, xy(center),
                  (size[1]*CM_PER_PIXEL,size[0]*CM_PER_PIXEL,height),0,'building',True))

# Access route and apron follow the visible southern cluster, in reference pixels.
PATH_PX = [(318,657),(367,658),(420,660),(473,662),(527,664),
           (539,645),(536,620),(523,603),(494,596),(461,595),(444,583)]
PLAYER_START = (*xy((472,650)),120)
COLORS = {'grass': (0.26,0.29,0.17), 'green': (0.28,0.48,0.23),
          'path': (0.38,0.35,0.29), 'building': (0.48,0.49,0.50),
          'trunk': (0.22,0.15,0.09), 'canopy': (0.12,0.22,0.12),
          'pond_water_v2': (0.10,0.23,0.24), 'pond_bank_v2': (0.36,0.33,0.23)}


def generate():
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    levels = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    assets = unreal.EditorAssetLibrary
    meshes = {name: unreal.load_asset("/Engine/BasicShapes/" + name)
              for name in ("Cube", "Cylinder", "Sphere")}
    game_mode = assets.load_blueprint_class(GAME_MODE)
    if not all(meshes.values()) or game_mode is None:
        raise RuntimeError("Missing engine primitives or existing third-person game mode; no map changed.")
    for row in BOXES:
        if min(row[2]) <= 0:
            raise ValueError("Box dimensions must be positive: " + row[0])

    # Finished actors opt in with a per-building replacement tag.
    replacement_prefix = 'DeadShift_GC01_Replacement_'
    replacements = set()
    # Save prompts precede any map switch. Existing GC01 maps must be opened explicitly.
    exists = assets.does_asset_exist(MAP)
    if exists:
        current = levels.get_current_level().get_outer().get_path_name().split(".")[0]
        if current != MAP:
            raise RuntimeError("Open " + MAP + " explicitly, then rerun. No map changed.")
        owned = []
        for actor in actors.get_all_level_actors():
            tags = [str(t) for t in actor.tags]
            finished = [t[len(replacement_prefix):] for t in tags
                        if t.startswith(replacement_prefix)]
            replacements.update(finished)
            if TAG in tags and not finished:
                owned.append(actor)
        if not owned:
            raise RuntimeError("Existing map has no GC01 ownership tags; refusing to overwrite it.")
        if not unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True):
            raise RuntimeError("Save cancelled; generation stopped.")
    else:
        if not unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True):
            raise RuntimeError("Save cancelled; generation stopped.")
        assets.make_directory("/Game/Development/GC01")
        if not levels.new_level(MAP):
            raise RuntimeError("Could not create dedicated GC01 map.")
        owned = []

    materials = {}
    assets.make_directory(MATERIAL_DIR)
    for name, rgb in COLORS.items():
        asset_name = "M_GC01_" + name
        mat = unreal.load_asset(MATERIAL_DIR + "/" + asset_name)
        if mat is None:
            mat = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
                asset_name, MATERIAL_DIR, unreal.Material, unreal.MaterialFactoryNew())
            if mat is None:
                raise RuntimeError("Could not create " + asset_name)
            color = unreal.MaterialEditingLibrary.create_material_expression(
                mat, unreal.MaterialExpressionConstant3Vector, -200, 0)
            color.set_editor_property("constant", unreal.LinearColor(*rgb, 1.0))
            unreal.MaterialEditingLibrary.connect_material_property(
                color, "", unreal.MaterialProperty.MP_BASE_COLOR)
            unreal.MaterialEditingLibrary.recompile_material(mat)
            assets.save_loaded_asset(mat)
        materials[name] = mat

    # Only generated actors are rebuilt; manual untagged additions survive.
    for actor in owned:
        if not actors.destroy_actor(actor):
            raise RuntimeError("Could not remove generated actor; stopped.")

    def spawn(cls, label, location, rotation=unreal.Rotator()):
        actor = actors.spawn_actor_from_class(cls, unreal.Vector(*location), rotation)
        if actor is None:
            raise RuntimeError("Could not spawn " + label)
        actor.set_actor_label("GC01_" + label)
        actor.set_editor_property("tags", [unreal.Name(TAG)])
        actor.set_folder_path("GC01_Generated")
        return actor

    def shape(label, mesh, xy, size, bottom, color, collision=True):
        actor = spawn(unreal.StaticMeshActor, label, (xy[0], xy[1], bottom + size[2] / 2))
        component = actor.static_mesh_component
        component.set_static_mesh(meshes[mesh])
        component.set_material(0, materials[color])
        component.set_collision_profile_name("BlockAll" if collision else "NoCollision")
        # Engine basic primitives have 100 cm bounds at unit scale.
        actor.set_actor_scale3d(unreal.Vector(*(d / 100.0 for d in size)))
        return actor

    for label, center, size, bottom, color, collision in BOXES:
        if label in replacements:
            continue
        shape(label, "Cube", center, size, bottom, color, collision)
    for i, (u, v, width, height) in enumerate(GREENS_PX, 1):
        shape('Green_%02d' % i, 'Cylinder', xy((u,v)),
              (height*CM_PER_PIXEL,width*CM_PER_PIXEL,8),0,'green',False)
    u, v, width, height = POND_PX
    shape('PondBank', 'Cylinder', xy((u,v)),
          ((height+8)*CM_PER_PIXEL,(width+8)*CM_PER_PIXEL,10),0,'pond_bank_v2',False)
    shape('PondWater', 'Cylinder', xy((u,v)),
          (height*CM_PER_PIXEL,width*CM_PER_PIXEL,4),11,'pond_water_v2',False)
    # Flat visual water placeholder over solid ground, not a swimming volume.
    import math
    for i, (a,b) in enumerate(zip(PATH_PX, PATH_PX[1:]),1):
        ax, ay = xy(a)
        bx, by = xy(b)
        length = math.hypot(bx-ax,by-ay)
        road = shape('AccessRoute_%02d' % i,'Cube',((ax+bx)/2,(ay+by)/2),
                     (length+100,500,8),0,'path',True)
        road.set_actor_rotation(unreal.Rotator(roll=0.0, pitch=0.0, yaw=math.degrees(math.atan2(by-ay,bx-ax))),False)
    for i, center in enumerate(TREE_POSITIONS, 1):
        shape("TreeTrunk_%02d" % i, "Cylinder", center,
              (TREE["trunk_diameter"], TREE["trunk_diameter"], TREE["trunk_height"]), 0, "trunk")
        shape("TreeCanopy_%02d" % i, "Sphere", center,
              (TREE["canopy_diameter"], TREE["canopy_diameter"], TREE["canopy_height"]),
              TREE["trunk_height"] - 100, "canopy", False)
    spawn(unreal.PlayerStart, "ThirdPersonStart", PLAYER_START)
    sun = spawn(unreal.DirectionalLight, "WorkLight", (0, 0, 10000), unreal.Rotator(-55, -35, 0))
    sun.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    sun.light_component.set_editor_property("intensity", 3.0)
    fill = spawn(unreal.DirectionalLight, "WorkFill", (0, 0, 9000), unreal.Rotator(-35, 145, 0))
    fill.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    fill.light_component.set_editor_property("intensity", 1.0)
    fill.light_component.set_editor_property("cast_shadows", False)
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    world.get_world_settings().set_editor_property("default_game_mode", game_mode)
    if not levels.save_current_level():
        raise RuntimeError("GC01 generated but map save failed; save manually.")
    unreal.log("GC01 full-course reference blockout ready: " + MAP + ". Play using Default Player Start; +X north, +Y east.")


if __name__ == "__main__":
    generate()
