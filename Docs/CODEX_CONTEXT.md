# DeadShift — Durable Project Context

- DeadShift is a stylized 3D third-person zombie survival game.
- Permanent art direction: **DEADSHIFT STYLIZED TOON**. [ART_DIRECTION.md](Art/ART_DIRECTION.md) is authoritative for production art. All future Blender and environment work must follow it; document the reason for any required deviation.
- Develop the world geographically in small sections, starting with the Medford, Oklahoma golf-course area and progressing toward the airport and industrial areas later.
- Unreal owns landscape/terrain, large-scale ground materials, foliage placement, splines, PCG where useful, lighting, and gameplay placement. Blender supplies reusable static meshes, golf-course props, infrastructure, recognizable structures, and modular environment pieces.
- Keep Blender scripts in `Art/Blender/Scripts/`, editable sources in `Art/Blender/Source/`, and exports in `Art/Blender/Exports/`; group future sources/exports by package. Golf-course planning lives in `Docs/Environment/MedfordGolfCourse/`.
- The first planned custom Blender package is `DeadShift_GolfCourse_Pack01`; its scope is the seven reusable assets in the golf-course manifest. No asset library has been generated. Do not create a generic test asset pack.
- Static mesh naming: `SM_Golf_[AssetName]_[Variant]`, with PascalCase asset names and two-digit variants. Match mesh object, mesh data, and export stems.
- Blender authoring uses Metric, Unit Scale `1.0` (one unit = one meter). Unreal uses centimeters. Preserve `1 m = 100 cm`, apply rotation/scale, and validate a known dimension before batch export. Target Z-up/+X-forward and use placement-appropriate pivots.
- Real-world golf-course layout is not verified. Verify references before construction; do not guess course geometry, hole/building positions, elevations, or exact dimensions.
- Cost efficiency is mandatory: build small verified sections, prioritize reusable pieces, start with one variant, and validate blockouts before detailed modeling. Expand asset scope only when the section requires it.
