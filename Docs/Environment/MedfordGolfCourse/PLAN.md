> Scope update — September 27, 2026: The user authorized expanding GC-01 to a full-course reference blockout with corrected pond placement and southern building footprints. This supersedes the earlier small-slice/no-complete-map restrictions below. See GC01.md for the current implementation and limitations. Gameplay and Blender work remain out of scope.

# Medford Golf Course — Phase 001

DeadShift is a third-person zombie survival game. World development begins with the Medford, Oklahoma golf-course area and will progress geographically toward the airport and industrial areas later.

GC-01 establishes a small provisional graybox of the southern facilities and immediate course area, using the supplied directional relationships. It does not establish exact real-world geometry. See `GC01.md` for parameters and Editor generation steps.

## Environment ownership

| Category | Unreal-native work | Blender work |
| --- | --- | --- |
| Terrain | Landscape and terrain shaping | None |
| Fairways | Landscape layers and large-scale ground materials | None |
| Greens | Landscape shaping and surface materials | Flag pin and cup |
| Rough | Ground materials and foliage placement | None initially |
| Trees/vegetation | Foliage placement; PCG where useful | No foliage library in this phase |
| Cart paths | Splines and surface materials | Special modular pieces only if later needed |
| Roads | Splines and ground materials | Infrastructure pieces later |
| Fencing | Spline/instance placement | Reusable posts and panels later |
| Utilities | Placement and cable splines | Poles and cabinets later |
| Drainage | Terrain channels and splines | Culverts and grates later |
| Course signage | Placement and eventual text/material setup | Reusable sign post and panel |
| Golf-course props | Placement | Tee marker, flag pin, cup, bench, trash can |
| Maintenance equipment | Placement | Equipment meshes later |
| Buildings/structures | Eventual blockout and placement | Reference-verified recognizable structures later |
| Parking | Ground surfaces and markings | Modular stops/bollards later |
| Vehicles | Placement | Vehicle meshes later |
| Environmental clutter | Decals and instance placement | Reusable clutter later |
| Zombie-survival dressing | Eventual dressing and gameplay placement | Modular dressing later |

Unreal also owns lighting and gameplay placement. This task makes no gameplay changes.

## Blender pipeline

- Scripts: `Art/Blender/Scripts/`; editable sources: `Art/Blender/Source/`; exports: `Art/Blender/Exports/`. Group future source/export files by package.
- First planned package: `DeadShift_GolfCourse_Pack01`, limited to the seven meshes in `ASSET_MANIFEST.md`. Do not generate it yet. No existing DeadShift Blender asset library is assumed; do not create a generic test pack.
- Name static meshes `SM_Golf_[AssetName]_[Variant]`, using PascalCase names and two-digit variants. Match object, mesh data, and export file stems.
- Author Blender in Metric, Unit Scale `1.0`: one Blender unit equals one meter. Unreal uses centimeters; preserve `1 m = 100 cm` through export/import. Apply rotation/scale and verify a known one-meter dimension before batch export; imported scale should be `(1,1,1)`.
- Target Z-up and Unreal +X-forward. Use useful placement pivots: bottom center for freestanding props, ground surface for cups, attachment points for modular pieces.

## Scope and cost controls

Reuse instances and one initial variant per mesh. Use `Scripts/Editor/generate_gc01.py` to rebuild primitive GC-01 geometry in the dedicated `/Game/Development/GC01/DEV_GC01_Graybox` map. Preserve the existing third-person implementation. Keep west open toward future Airport-01 and north toward GC-02. Verify measurements before detailed world construction and model only what the slice needs. No complete map, detailed buildings, final textures, foliage libraries, zombies, weapons, unrelated gameplay systems, Blender assets, or Unreal build in this phase.

## References required before construction

The exact real-world layout is unverified. GC-01 dimensions and placements are explicitly provisional design estimates. Do not represent them as actual course geometry, hole/building positions, elevations, or measured dimensions.

Two supplied aerial views guide the southern cluster's relative arrangement: a larger northern footprint, several smaller southern footprints, a narrow western structure, and a nearby green to the west. Building functions, measured spacing, elevations, and the annotated property boundary remain unverified.

Obtain confirmed course location, dated/scaled aerial imagery, a marked boundary for the first playable section, elevation/contour references, and ground-level photos with measured prop dimensions. Verify relevant paths, roads, structures, vegetation, and drainage within that boundary before world construction.
