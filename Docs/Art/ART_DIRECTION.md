# DeadShift — Art Direction

## Authority and identity

**Internal style name: DEADSHIFT STYLIZED TOON**

DeadShift is a stylized 3D third-person zombie survival game. Its visual inspiration is clean adult animated television/cartoon artwork translated into a fully 3D playable world, with an original visual identity of its own.

This document is the permanent, authoritative visual direction for all production art. Every future production asset and all future Blender/environment work must follow it. Do not silently change the established visual language. If a future task requires a deviation, document the reason.

Do not directly copy Futurama characters, props, architecture, logos, or copyrighted designs. Inspiration must be translated into original DeadShift designs.

## 1. Geometry

- Use simplified, clean, readable geometry with strong silhouettes.
- Keep geometric complexity low to moderate.
- Favor large intentional forms over tiny realistic details.
- Use bevels and chamfers where they improve cartoon readability.
- Slightly exaggerate proportions.
- Avoid photorealistic modeling.

## 2. Environments

- Real-world locations may inspire layout and recognizable structure, but convert them into stylized fictionalized versions.
- Preserve major proportions and layout landmarks where useful.
- Simplify architectural details.
- Avoid real-world corporate branding unless explicitly requested.
- Buildings must remain believable and navigable despite stylization.

## 3. Props and vehicles

- Preserve recognizable real-world function.
- Use slight caricature and exaggeration, chunkier forms, and readable silhouettes.
- Avoid unnecessary micro-detail.
- Vehicles should generally remain believable enough for gameplay.

## 4. Characters and zombies

- Use stylized human proportions with slightly exaggerated heads, hands, feet, and major features.
- Maintain strong silhouette differentiation.
- Zombies must support visual variety and readable damage states.
- Gore can be more graphic and exaggerated than the environment while remaining consistent with the toon style.

## 5. Materials

- Use graphic, simple surface treatment and controlled color blocks.
- Avoid noisy photorealistic textures.
- Target a toon/cel-shaded presentation.
- Use reusable Unreal master materials and material instances wherever practical.
- Materials must remain readable under different lighting conditions.

## 6. Outlines

- Dark stylized outlines are part of the final rendering language.
- Favor silhouette and important crease readability.
- Avoid excessively thick outlines that obscure small objects.
- Test outline implementation in Unreal before standardizing the technique. This document establishes the visual target; implementation remains pending.

## 7. Color

- Use color that is more saturated and intentional than reality.
- Avoid random neon coloration.
- Maintain distinct material and color families.
- Environment colors must support zombie and enemy readability.

## 8. Vegetation

- Use simplified graphic foliage with strong silhouettes.
- Favor clustered, readable leaf and branch masses over photorealistic individual detail.
- Optimize vegetation for large outdoor environments.

## 9. Lighting

- Stylized rendering does not mean flat atmosphere: retain a strong survival/horror atmosphere.
- Support day and night conditions.
- Fog, fires, emergency lights, flashlights, moonlight, and dramatic shadows may contrast against the colorful toon world.
- Maintain gameplay readability.

## 10. Blender pipeline

- Blender creates reusable stylized static meshes and, later, appropriate character and prop assets.
- Prefer parameterized Python generators when practical.
- Use consistent scale, naming, origins, and material slots, following the project's established pipeline conventions.
- Avoid unnecessary topology and detail.
- Unreal remains responsible for landscape, world assembly, lighting, foliage systems, materials, and gameplay integration.

## 11. Performance

- Stylization should help performance.
- Favor efficient geometry and reusable materials.
- Avoid unnecessary unique high-resolution textures.
- Design for large outdoor areas and substantial zombie counts.

## 12. Consistency and production review

Evaluate every future production asset against this document: silhouette and form, stylization, color and material readability, atmosphere, pipeline consistency, and performance must support DEADSHIFT STYLIZED TOON.

Do not silently change the established visual language. Document the reason for any required deviation in the relevant task or asset documentation.
