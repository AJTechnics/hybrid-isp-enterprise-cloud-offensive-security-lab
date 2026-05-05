# Minecraft Dynamic NPCs

This server now has two dynamic layers for Oakcross:

1. Scheduled dialogue profile rotation.
2. Per-player reactive NPC dialogue via Denizen.

## Scheduled world-state rotation

Profile packs are still stored in `automation/ansible/files/minecraft/living-content/citizens/dialogue-profiles/` and deployed to `/srv/minecraft/data/living-world/dialogue-profiles/`.

The timer applies them automatically using:

- `minecraft_dialogue_schedule_calendar`
- `minecraft_dialogue_weekday_profiles`
- `minecraft_dialogue_season_month_map`

Current precedence is:

1. Weekday profile for the current day.
2. Seasonal profile for the current month.
3. `minecraft_dialogue_schedule_default_profile`.

Manual commands on the host:

```sh
sudo minecraftctl oakcross-dialogue-schedule
sudo minecraftctl oakcross-dialogue-default
```

## Reactive NPC dialogue

Denizen is now part of the managed plugin set and Oakcross scripts are seeded to:

`/srv/minecraft/data/plugins/Denizen/scripts/oakcross_reactive_npcs.dsc`

Reactive assignments are applied by:

```sh
sudo minecraftctl oakcross-reactive-apply
```

The apply command depends on the generated Oakcross NPC ID map:

`/srv/minecraft/data/living-world/state/oakcross-npcs.env`

That file is refreshed automatically by the Oakcross NPC bootstrap script. If the map is missing or stale, rerun the NPC bootstrap once and then re-apply reactive assignments.

## Operational flow

For a clean refresh after changing reactive NPC scripts:

```sh
cd /home/lab/workspace/hybrid-isp-enterprise-cloud-offensive-security-lab/automation/ansible
./scripts/deploy-media1.sh
```

If NPC IDs changed because of a rebuild, then run:

```sh
sudo minecraftctl oakcross-npcs
sudo minecraftctl oakcross-reactive-apply
```

## Behavior model

The scheduled profile apply script sets Denizen server flags such as:

- `oakcross.profile.market_day`
- `oakcross.profile.road_patrol`
- `oakcross.season.autumn`

Reactive scripts use those flags together with per-player flags like `oakcross.met_mira` to branch lines based on both current world state and that player's prior interactions.