# Spawn Town Implementation Pack

Purpose: turn the current village at world spawn into Oakcross without changing player bed respawns and without needing exact coordinates ahead of time.

## Anchor Rule
- Use the existing world spawn as the town-square anchor.
- Current configured world spawn anchor:
  - world: `world_recovery`
  - x: `1293`
  - z: `-455`
- Keep player bed spawnpoints unchanged.
- Use relative offsets from the world spawn square for first-pass NPC placement.

## Placement Workflow
1. Stand at the current world spawn square.
2. Face the main road or most obvious village street.
3. Use the offsets below to select buildings or stalls already present.
4. If a required building does not exist, use the fallback footprint for a small additive build.

## Starter NPC Placements

### 1. Mira Vale, Town Crier
- Role: notice board keeper, event intro, seasonal announcements
- Preferred placement: directly on or beside the spawn square
- Relative offset from spawn: `+2 east`, `+1 south`
- Required structure: notice board kiosk or square-side canopy

### 2. Elira Thorn, Innkeeper
- Role: rumors, food quests, social entry point
- Preferred placement: existing largest house with beds, tavern, or central lodge
- Relative offset from spawn: `-6 west`, `+4 south`
- Required structure: tavern or inn with 4-8 beds, hearth, storage, and front counter

### 3. Bram Coalhand, Blacksmith
- Role: ore turn-ins, tool stock, repair progression
- Preferred placement: existing smithy building or furnace workshop
- Relative offset from spawn: `+8 east`, `-5 north`
- Required structure: smithy with furnaces, anvils, barrels, and small stock room

### 4. Captain Rowan Pike, Guard Captain
- Role: patrol contracts, road warnings, defense event anchor
- Preferred placement: road-facing gate, watch post, or edge building near village entrance
- Relative offset from spawn: `+12 east`, `+10 south`
- Required structure: guard post with map wall, weapon rack, and alarm bell

### 5. Sella Reed, Market Trader
- Role: rotating stock, weekly trade loop, event merchant
- Preferred placement: existing market stall or square-edge booth
- Relative offset from spawn: `-4 west`, `-3 north`
- Required structure: market stall with chest/barrel storage and display counter

### 6. Old Fen Gray, Ranger Scout
- Role: exploration hints, route safety, ruin/forest hooks
- Preferred placement: village edge house facing forest, ruins, or outbound road
- Relative offset from spawn: `-12 west`, `+8 south`
- Required structure: scout hut or edge-house office with maps, table, and supply chest

## Required Buildings

### Spawn square notice board
- Owner: Mira Vale
- Use existing square if present.
- If missing, add:
  - footprint: `5x5`
  - style: wood canopy, board wall, lanterns
  - props: 2 barrels, 1 bell, 1 message board wall

### Tavern / inn
- Owner: Elira Thorn
- Reuse existing multi-bed house first.
- If missing, add:
  - footprint: `9x11`
  - spaces: counter, hearth, 4 beds, 3 tables, upstairs or rear bunkroom
  - nearby use: food shop and Bread for the Tavern quest turn-in

### Smithy
- Owner: Bram Coalhand
- Reuse any furnace/workshop building first.
- If missing, add:
  - footprint: `7x9`
  - props: 2 furnaces, 1 blast furnace, 1 anvil, 2 barrels, ore yard

### Guard post
- Owner: Captain Rowan Pike
- Reuse a road-facing edge building first.
- If missing, add:
  - footprint: `5x7`
  - props: wall map, 2 beds, weapon rack, bell or banner marker

### Market stall
- Owner: Sella Reed
- Reuse any decorative stall first.
- If missing, add:
  - footprint: `3x5`
  - props: chest/barrel storage, awning, counter block

### Scout hut
- Owner: Old Fen Gray
- Reuse edge house first.
- If missing, add:
  - footprint: `5x7`
  - props: cartography table, barrel, campfire or lantern, waypoint board

## Minimal Build Order
1. Notice board kiosk
2. Tavern / inn
3. Smithy
4. Guard post
5. Market stall
6. Scout hut

## Bed Spawn Safety
- Do not run commands that clear player spawnpoints.
- Do not replace occupied player houses if they already serve as bedspawn anchors.
- Prefer unused or public buildings for NPC roles.
- If a needed role building is player-owned, build a small public version nearby instead of overwriting it.

## First Town Loop
- Spawn square -> tavern -> smithy -> market stall -> guard post -> east road -> scout hut -> return to square
- This loop should stay walkable in under 3 minutes.