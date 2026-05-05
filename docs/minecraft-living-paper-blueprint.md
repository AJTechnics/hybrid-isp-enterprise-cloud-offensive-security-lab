# Living Paper Minecraft Server Blueprint (World-Preserving)

## Objective
Layer seasons, recurring events, dynamic NPCs, quests, and physical shops on top of the existing Paper survival world without replacing terrain, wiping builds, or resetting player progression.

## Non-Negotiable World Policy
- Keep the current world as canonical (`minecraft_level_name: world_recovery`).
- No terrain regeneration and no world swap.
- Keep player structures, inventories, and progression unless explicitly approved.
- Reuse existing roads, towns, farms, mines, docks, and landmarks as gameplay anchors.
- Apply all changes additively and reversibly.

## 1) Plugin Architecture Plan

### Current foundation already in place
- Core economy and utility: EssentialsX, Vault, EssentialsXSpawn.
- Quality of life and safety: CoreProtect, AxGraves, OnePlayerSleep+.
- Immersive economy base: QuickShop-Hikari.
- Mapping and planning visibility: BlueMap.
- Managed delivery path: Ansible vars in `minecraft_paper_plugins` and `deploy-minecraft.yml`.

### Recommended phased plugin roles

#### NPC plugin role
- Primary: Citizens (named NPCs, pathing, role placement in existing buildings).
- Role in design:
  - Ambient NPCs for settlement life.
  - Functional NPCs for shops, rumors, and services.
  - Progression NPCs with dialogue state changes by quest/reputation/season.
- Integration notes:
  - Keep active NPC count low per chunk/town center.
  - Prioritize static or short-radius pathing in high-traffic areas.
  - Place NPCs only in existing built spaces.

#### Quest plugin role
- Primary: Quests (or BetonQuest if deeper branching is required later).
- Role in design:
  - Tiered quest packs (short repeatables first, then chains).
  - Prerequisites and unlocks tied to settlement reputation and event flags.
  - Location-scoped objectives on existing roads, docks, farms, caves, and ruins.
- Integration notes:
  - Keep first release to 5-10 starter quests.
  - Favor delivery, patrol, gather, and exploration objectives over kill-only loops.
  - Use Citizens NPC IDs as quest givers/completion targets.

#### Shop plugin role
- Primary baseline: QuickShop-Hikari for physical, location-bound shops.
- Secondary immersive NPC shops: Shopkeepers after confirming Paper compatibility.
- Role in design:
  - Convert existing decorative stalls/buildings into active shops.
  - Seasonal rotation by item category and limited-time event offers.
  - Unlock higher stock via quest milestones/reputation.
- Integration notes:
  - Keep market identity local (no forced global GUI economy at launch).
  - Maintain Vault as single economy API.

#### Seasons plugin role
- Primary approach: lightweight season-state scheduler with config flags and event hooks.
- Implementation options:
  - Option A: dedicated seasons plugin that supports Paper and command hooks.
  - Option B: scheduled command rotation (weekly/monthly) plus quest/shop/NPC state toggles.
- Role in design:
  - Season tag drives dialogue sets, quest availability, event board rotation, and shop stock profiles.
  - Town decorations are additive and removable.
- Integration notes:
  - Do not apply destructive crop/weather rules globally.
  - Start with mood and content rotation, then add optional mechanics later.

### Integration model (single source of truth)
- `SeasonState` (spring/summer/autumn/winter) controls:
  - event board text
  - enabled quest sets
  - NPC dialogue pool
  - seasonal shop stock
- `WeeklyEventState` controls one rotating weekly activity.
- `TownReputation` gates advanced stock and quest chains.
- Keep each subsystem decoupled so rollback is granular.

### Compatibility and rollout controls
- Pin plugin versions explicitly in Ansible inventory before production rollout.
- Add new jars to a staged plugin list, then promote to live after validation.
- Keep `minecraft_disabled_plugins` policy for immediate rollback on incompatibility.
- Preserve `CoreProtect` logging for all initial content changes.

## 2) World Preservation Checklist

### Backup steps (before each major change)
- Trigger manual backup of world and server data.
- Snapshot plugin and config directories separately.
- Archive playerdata and advancement data before quest/plugin migrations.
- Record active plugin set and version manifest in changelog.

### Backup runbook (current stack aligned)
- Use existing backup wrapper on host:
  - `minecraft-backup-manual`
- Verify backup artifact and checksum in `/srv/minecraft/backups`.
- Validate archive includes:
  - `/srv/minecraft/data/world*`
  - `/srv/minecraft/data/plugins`
  - `/srv/minecraft/data/playerdata`
  - `/srv/minecraft/data/*.yml` and plugin subconfigs

### Staging steps
- Clone current world data into a staging instance/profile.
- Test new plugins and config there first.
- Validate:
  - startup time and TPS impact
  - NPC pathing in populated settlements
  - quest completion and reset behavior
  - shop transactions and economy balance
- Run at least one full season state switch in staging.

### Deployment safety steps
- Deploy in maintenance window with rollback checkpoint.
- Enable only one major subsystem per change window:
  - wave 1 NPCs
  - wave 2 quests
  - wave 3 seasonal hooks
  - wave 4 expanded shops
- Keep a disable list ready (`minecraft_disabled_plugins`) for bad plugin rollback.
- Announce player-facing changes and known limits before enabling.

## 3) Starter Settlement Pack

### Settlement profile
- Name: Oakcross
- Theme: farming crossroads and river checkpoint
- Physical anchor: the current village at world spawn becomes Oakcross, the first living town
- Spawn policy: keep world spawn in the village for orientation and NPC access, but preserve each player's bed spawnpoint for respawns
- Core economy: crops, bread, fish, ore resupply
- Nearby anchors to map onto existing world:
  - spawn square/notice board
  - tavern
  - smithy
  - east road to bridge/watchtower
  - docks or river landing
- Main risks: route disruption, supply loss, cellar pests, road monsters

### NPC roster (6 named NPCs)
- Mira Vale, Town Crier (event board and seasonal announcements)
- Elira Thorn, Innkeeper (rumors, intro quests, food supply)
- Bram Coalhand, Blacksmith (ore turn-ins, tool stock progression)
- Captain Rowan Pike, Guard Captain (patrol contracts and threat alerts)
- Sella Reed, Market Trader (rotating stock and event merchant role)
- Old Fen Gray, Ranger Scout (exploration hints and route safety tasks)

### Shops (2 starter)
- Oakcross Smithy
  - sells: basic tools, repair mats, starter armor
  - unlock rank 2 stock: after ore support quest chain
- Hearthlight Provisions (Inn)
  - sells: bread, cooked foods, torches, travel rations
  - seasonal rotation: soups/stews in winter, fishing meals in summer

### Starter quests (5)
- `oakcross_bread_tavern`: Bread for the Tavern
  - giver: Elira Thorn
  - objective: deliver wheat/bread bundle
  - repeatable: daily
  - reward: currency + small reputation
- `oakcross_east_road_patrol`: Check the East Road
  - giver: Captain Rowan Pike
  - objective: patrol gate -> bridge -> return report
  - repeatable: every 2 days
  - reward: currency + guard reputation
- `oakcross_missing_crate`: Missing Crate
  - giver: Sella Reed
  - objective: locate and recover shipment near road/dock marker
  - repeatable: weekly
  - reward: currency + market discount token
- `oakcross_smith_ore`: Smith Needs Ore
  - giver: Bram Coalhand
  - objective: deliver iron/coal quota
  - repeatable: weekly
  - reward: currency + smith stock progress
- `oakcross_ruin_scout`: Scout the Old Ruin
  - giver: Old Fen Gray
  - objective: visit known ruin and report
  - repeatable: weekly
  - reward: reputation + exploration token

### Event hooks
- Weekly event: Caravan Arrival Day
  - active loop: escort-lite deliveries, market bonus offers, road patrol bonus
- Seasonal event: Harvestwake (Autumn)
  - location: square + farm district
  - activities: crop turn-ins, cooking submissions, temporary feast vendor

### Spawn behavior rule
- Keep the current `setworldspawn` location in the village so new players and spawn travel still land in town.
- Do not clear or overwrite bed respawn points.
- Bed-based player respawns remain the default personal spawn mechanic.
- NPC placement must stay inside the current village footprint so the town grows out of the existing map instead of replacing it.

## 4) Expansion Framework (3 More Existing Locations)

## Expansion rule
Do not invent disconnected hubs. Assign gameplay roles to existing landmarks and settlements.

### Location A: Existing docks or river port
- Role set:
  - dockmaster NPC
  - fisherman quest giver
  - import trader (rotating goods)
- Quest patterns:
  - shipment recovery
  - fish quota
  - crate delivery to tavern/market
- Event hook:
  - summer fishing contest and river market day

### Location B: Existing mine/cave district
- Role set:
  - mining foreman
  - safety marshal/guard
  - salvage broker
- Quest patterns:
  - ore quota
  - lost tools recovery
  - infestation clear path
- Event hook:
  - winter supply pressure contracts

### Location C: Existing watchtower/ruin corridor
- Role set:
  - ranger post captain
  - historian/lore keeper
  - traveling merchant stop
- Quest patterns:
  - patrol checkpoint runs
  - ruin scouting reports
  - route repair material runs
- Event hook:
  - weekly patrol contract week

### Inter-location progression model
- Create simple route triangles between Oakcross and the 3 expansions.
- Unlock cross-settlement discounts at reputation thresholds.
- Rotate one weekly event focus among the four locations.

## 5) Content Authoring Rules

### Dialogue style rules
- Keep lines short (1-3 lines each), practical, and location-aware.
- Include one local anchor per key line (bridge, tavern, dock road, old ruin).
- Avoid lore dumps at quest handoff points.
- Provide changed dialogue states for:
  - pre-quest
  - in-progress
  - post-completion
  - seasonal variant

### Quest writing rules
- Use this structure for every quest:
  - id, title, giver, location, prerequisites, objectives, repeatability, season tags, rewards, follow-up dialogue state
- Favor 5-12 minute tasks for repeatables.
- Use chain quests only for progression milestones.
- Keep at least 60 percent of early quests non-combat.
- Tie objectives to existing roads and structures, not artificial arenas.

### Event design rules
- Weekly events should modify normal play, not replace it.
- Monthly/seasonal events should be town-centered and additive.
- Every event must have:
  - start/end window
  - clear objective list
  - small participation reward and one premium tier reward
  - rollback/cleanup checklist
- No event should require world edits that overwrite player builds.

### Economy balance rules
- Keep Vault as economy backbone.
- Use local physical shops first; avoid global menu economy dominance.
- Lock advanced stock behind reputation/quest milestones.
- Cap buyback loops and monitor inflation weekly.
- Keep event currencies seasonal and auto-expire or convert at season end.

## Recommended Phased Rollout

### Phase 1: Foundation (minimal disruption)
- Backup baseline.
- Add NPC plugin and place 3-5 core NPCs in one town.
- Enable 2 shops and first 5 quests.
- Activate one weekly event cycle.

### Phase 2: First living town
- Expand to full 6+ NPC roster.
- Add seasonal dialogue variants.
- Run first seasonal event (Harvestwake or Bloomfair).
- Tie first shop stock upgrade to reputation.

### Phase 3: Expansion
- Adapt 3 existing locations with role packs.
- Add inter-town deliveries and patrol loops.
- Introduce one traveling merchant route.

### Phase 4: Persistent world reactivity
- Full seasonal loop active.
- Reputation tracks affect trade and quest tiers.
- Rare world requests/town needs rotate monthly.

## Success Metrics
- No world reset and no terrain regeneration.
- Stable TPS and startup after each release wave.
- Players repeatedly return to settlement hubs for content.
- At least one active weekly loop and one active seasonal loop at all times.
- Existing roads, towns, and landmarks see measurable player traffic growth.

## Implementation Assets In This Repo
- Rollout task cards: `docs/minecraft-living-rollout-checklist.md`
- Spawn-relative town pack: `docs/minecraft-spawn-town-pack.md`
- Citizens starter NPC commands: `automation/ansible/files/minecraft/living-content/citizens/oakcross-npcs.commands`
- Building requirements pack: `automation/ansible/files/minecraft/living-content/buildings/oakcross-buildings.yml`
- Quests authoring skeleton: `automation/ansible/files/minecraft/living-content/quests/oakcross-quests.skeleton.yml`
- Plugin-ready Oakcross Quests pack: `automation/ansible/files/minecraft/living-content/quests/quests-plugin/`
- Phase-1 plugin pinning and staged enablement vars: `automation/ansible/inventories/lab/host_vars/media1.yml`
