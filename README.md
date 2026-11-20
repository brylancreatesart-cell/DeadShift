# DeadShift

DeadShift is an original zombie-survival game planned for Unreal Engine 5.

## Development direction

- **Gameplay:** Third-person exploration, improvised weapons, zombie hordes, scavenging, and a story-driven outbreak.
- **Initial release:** Single-player and private cooperative play (target: 2–4 players).
- **Long-term:** Dedicated servers and persistent public survival worlds; server size depends on performance testing.
- **Architecture:** Server-authoritative gameplay, replicated state, and offline-compatible core systems.

## Current status

This repository was reset to a clean **pre-production foundation** on November 19, 2026. It is **not yet a compilable Unreal project**. Generate the actual Unreal Engine C++ project on a development PC, then commit the `.uproject`, `Config/`, `Content/`, and `Source/` files.

The previous project has been preserved in `archive/pre-rebuild-2026-11-19`.

## Documents

- [Technical architecture](Docs/ARCHITECTURE.md)
- [Milestones](Docs/MILESTONES.md)
- [First setup](Docs/SETUP.md)

Storyline content is developed separately in Codex; only approved canonical story materials should be merged into the game repository.

## Initial engineering priorities

1. Create UE5 C++ Third Person project named `DeadShift`.
2. Test an authoritative server with two clients in a small test level.
3. Implement server-authoritative health, damage, and one zombie AI.
4. Replicate pickups and inventory actions safely.
5. Test disconnect/reconnect and basic saving.
