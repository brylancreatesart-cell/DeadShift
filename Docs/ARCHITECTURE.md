# DeadShift multiplayer architecture (v0.1)

## Design principle

Support offline single-player, private listen-server co-op, and eventually dedicated public servers with one gameplay codebase. No game-changing actions should trust the client as authority.

## Gameplay authority

- **GameMode (server only):** Rules, spawning, validation.
- **GameState (replicated):** Shared match/world state needed by clients.
- **PlayerState (replicated):** Public player state; sensitive inventories should not be indiscriminately broadcast.
- **PlayerController:** Player-owned RPC entry points; validate requests on server.
- **Character/Pawn:** Predicted movement using Unreal's CharacterMovementComponent where applicable.
- **Inventory:** Server-owned transactions, stable item instance IDs, atomic pickup/transfer logic; selectively replicate owner-facing details.
- **Combat:** Server verifies attack requests and applies authoritative damage; clients predict only appropriate visuals.
- **Zombie AI:** Server executes behavior and damage; only relevant movement/state replicated.
- **Persistence:** Local saves for offline mode; server-managed persistence for dedicated servers; version and back up saved state.

## Networking

Start with built-in UE replication and sessions. Use realistic packet-latency / loss tests early. Reassess Iris/Replication Graph only after profiling. Client cosmetic effects must never become authoritative gameplay decisions.

## Scalable hordes

Full simulation near active players; lower-frequency behavior at a distance; abstract or dormant simulation outside all active-player areas. World Partition streaming does not itself eliminate server AI costs.

## World modes

- Offline: local authority and local save.
- Private: listen-server hosted by one player; 2–4 player initial target.
- Public (later): dedicated server; persistence service; authentication; backup/recovery; anti-abuse and moderation.

## Scope guard

Do not begin with public PvP, 30-player guarantees, large persistent bases, or a complete open world. Prove a small networked gameplay loop first.

## File organization (once UE project is generated)

`Source/DeadShift/{Core,Characters,AI,Combat,Inventory,Interaction,Multiplayer,Persistence}`
`Content/{Characters,Zombies,Weapons,Vehicles,Maps,UI,Audio}`
`Config/`

These paths are proposed; Unreal-generated entry point files take precedence. Do not fabricate `.uasset` files.
