# GC-01 northern facility — first exterior pass

Created with Blender 5.2.1. The project source is Art/Blender/Source/GC01_Buildings/SM_Golf_NorthFacility_01.blend; export is Art/Blender/Exports/GC01_Buildings/SM_Golf_NorthFacility_01.fbx. Copies accompany this note.

The foundation follows the existing 16 x 19.2 meter blockout footprint. Overall height is 4.48 meters. The entrance canopy increases the overall X extent to about 17.11 meters. The roof, doors, windows and trim are provisional designs; only aerial references were available. Exterior only, no working doors or interior.

The source contains an editable joined building mesh with separate material slots, UVs, simple UCX collision, and a studio camera/light setup. The FBX contains only the building and collision, not the studio. The pivot is at ground level at the center of the footprint. Scale is applied. An FBX reimport into Blender retained dimensions and UVs; Unreal import, materials and player collision remain untested.

## Next Unreal step

Save the current level before integrating. Import the FBX as a static mesh into a GC01 Buildings folder. Use import scale 1 and the supplied UCX collision. Verify that the footprint reads approximately 1600 x 1920 centimeters; check orientation before placement. Simple material colors may need adjustment in Unreal.

Place the mesh with its ground pivot at X=80, Y=0, Z=0 centimeters, rotation zero, scale 1. Add the actor tag DeadShift_GC01_Replacement_NorthFacility. This exact tag tells the revised generator to preserve that actor and skip the NorthFacility placeholder on the next rebuild. Do not add the tag to an empty actor: it must identify the finished replacement. Save the level, then rerun the generator to replace its old placeholder. Test player collision around the walls and entry canopy.

Preservation logic was checked with generated, finished and manual actors; actual editor regeneration with the imported asset still needs verification. The existing map has not been changed during this modeling pass.