# Clubhouse 02 — editable style study

Saved separately as Art/Blender/Source/GolfCourseAssets/SM_Golf_Clubhouse_02.blend.
Original source file is untouched; its objects are also retained in the hidden Original_Preserved_DoNotEdit collection.

Photo-based low metal roof, covered east porch, cream siding and dark green trim. Southwest corner has west and south windows. The rates sign is immediately to the viewer's right of the south/front window, with greens fees and cart rental per person per nine holes; prices remain TBD.

Blender orientation: +X north, -Y east, +Z up. Foundation retains the prior provisional 16 x 19.2 m footprint. Dimensions, doorway and unseen details require review; this is an editable modeling study, not a surveyed reconstruction or finished production asset. Toon materials use Blender EEVEE and need Unreal equivalents. No Unreal map was modified or export performed.

NE and SW previews were rendered and inspected. The original open Blender session was not overwritten. New working copy is opened separately for review.

September 29 siding-only revision: photo-based vertical metal ribs added to exterior walls and porch panels, with clearances for windows, doorway and rates sign. Both previews inspected; all 118 non-siding objects retained their transforms and geometry counts. Run update_clubhouse02_siding.py after the initial builder to reproduce this revision.

Unreal integration: clubhouse placed in existing DEV_GC01_Graybox at the original northern facility position. Legacy FBX import required actor scale correction; 26 convex collision hulls present. Original placeholder retained below the map with collision disabled. Materials assigned. Interactive player traversal and final visual/material review remain UNVERIFIED; automated validation did not complete. User requested no further retries.
