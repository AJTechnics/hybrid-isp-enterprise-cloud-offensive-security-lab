# Minecraft Living Blueprint Execution

Purpose: convert the living-world blueprint into practical phased execution steps for this repository.

## Current status snapshot
- World policy: additive only, no resets.
- Oakcross content skeleton: present.
- Citizens + Quests runtime: active.
- LuckPerms command-group automation: active in deploy.

## Phase 1 - Foundation
- Confirm backups before each release window.
- Keep one active plugin jar per plugin family.
- Validate startup health and reachability after deploy.
- Keep rollback list updated in host vars.

## Phase 2 - Oakcross MVP
- NPC minimum set: 3 to 5 active NPCs in central loop.
- Shops: smithy and tavern first, market stall second.
- Quests: enable 3 to 5 repeatables with short completion loops.
- Weekly event: run Market Day first as low-risk baseline.

## Phase 3 - Local expansion
- Reuse nearby road, farm, and ruin landmarks.
- Add patrol + exploration quest links across those points.
- Keep travel loop under 5 minutes for early content.

## Phase 4 - Seasonal layer
- Activate one seasonal profile at a time.
- Tie season state to dialogue and shop stock first.
- Add gameplay modifiers only after one full season cycle is stable.

## Release guardrails
- No destructive world edits.
- No replacement of player builds.
- No mass NPC expansion without performance checks.
- Validate one subsystem per deploy window.

## Next implementation targets
1. Move from Quests content to NotQuests-compatible format in a staged branch while preserving current live quests.
2. Re-enable Shopkeepers only after confirming server-version compatibility.
3. Add seasonal state driver (plugin or scheduler) with reversible toggles.
