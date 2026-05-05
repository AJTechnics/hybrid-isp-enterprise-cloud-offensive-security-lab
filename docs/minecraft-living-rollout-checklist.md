# Minecraft Living World Rollout Checklist

Purpose: execute the living-world rollout in low-risk waves while preserving the existing world and player progression.

## Release 0 - Preflight and Safety
- [ ] Confirm current production world is `world_recovery`.
- [ ] Run manual backup and verify archive checksum.
- [ ] Snapshot plugin/config/playerdata directories.
- [ ] Confirm rollback path: `minecraft_disabled_plugins` can be updated quickly.
- [ ] Announce maintenance window and rollback expectation.

## Release 1 - Plugin Foundation (No Live Quests Yet)
- [ ] Keep `minecraft_living_phase1_plugins_enabled` empty.
- [ ] Add only Citizens to enabled list.
- [ ] Deploy playbook and verify startup health/TPS.
- [ ] Place 3 NPCs in one settlement (Crier, Innkeeper, Guard Captain).
- [ ] Validate NPC persistence across restart.
- [ ] Record plugin and config changes in changelog.

## Release 2 - Quest Loop Activation
- [ ] Keep Citizens enabled.
- [ ] Add Quests to enabled list.
- [ ] Deploy playbook and verify startup health/TPS.
- [ ] Enable first 3 repeatable quests only.
- [ ] Verify objective completion, reward payout, and repeat timers.
- [ ] Confirm no world edits beyond additive content.

## Release 3 - Physical Shops and Economy Progression
- [ ] Validate QuickShop stall locations in existing market.
- [ ] Convert 2 decorative stalls into active shops.
- [ ] Tie one shop upgrade to quest milestone.
- [ ] Monitor inflation and buyback loops for one week.

## Release 4 - Weekly Event Rotation
- [ ] Create event board in existing town square.
- [ ] Enable one weekly event (Caravan Arrival Day).
- [ ] Add weekly NPC dialogue variant for key NPCs.
- [ ] Validate event starts/stops cleanly with no residual state.

## Release 5 - Seasonal Layer (Autumn First)
- [ ] Add Autumn dialogue set for 6 key NPCs.
- [ ] Enable Harvestwake event hooks.
- [ ] Rotate seasonal shop stock for 2 shops.
- [ ] Apply only additive, reversible decorations.

## Release 6 - Expansion to 3 Existing Locations
- [ ] Docks/river role pack added.
- [ ] Mine/cave role pack added.
- [ ] Watchtower/ruin role pack added.
- [ ] Add inter-town deliveries and patrol loops.
- [ ] Verify travel routes reuse existing roads and landmarks.

## Operations Checklist (Each Change Window)
- [ ] Backup complete and tested.
- [ ] Single subsystem changed this window.
- [ ] Performance check passed (TPS/startup).
- [ ] Rollback instructions updated.
- [ ] Player announcement posted.
