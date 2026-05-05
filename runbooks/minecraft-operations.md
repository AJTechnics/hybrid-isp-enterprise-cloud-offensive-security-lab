# Minecraft Server Operations Runbook

## Purpose

This runbook is the operator guide for the Paper Minecraft stack on `media1`.

It covers:
- how the server is built and managed
- where all important files and services live
- backups and restore operations
- restart and day-to-day operations
- how to replicate the server or create a new server from current state
- troubleshooting workflows

The automation source of truth is Ansible. Manual changes are allowed for incident response, but should be pushed back into automation after recovery.

## Current Topology and Ownership

- Control node: `ws1` (this repo + Ansible)
- Server node: `media1` (`192.168.1.131`)
- Runtime: Podman Quadlet container running `itzg/minecraft-server:java21`
- World: `world_recovery`
- Service name: `minecraft.service`

Primary config source:
- `automation/ansible/inventories/lab/host_vars/media1.yml`

Primary deployment playbook:
- `automation/ansible/playbooks/deploy-minecraft.yml`

## Build Architecture (What, Where, Why)

### Identity and directories

- Root data path: `/srv/minecraft`
- Live game data: `/srv/minecraft/data`
- Local backup archive directory: `/srv/minecraft/backups`
- Service user/group: `minecraft:minecraft`
- Mod/admin group: `mcmods`
- Web/admin user: `mcadmin`

Why:
- `/srv/minecraft/data` is the canonical mounted state for the container.
- `/srv/minecraft/backups` stores tar archives for local restore.
- Group `mcmods` allows controlled operations access without making everything root-owned.

### Systemd units and scripts

Installed units/scripts (by Ansible):
- `/etc/containers/systemd/minecraft.container`
- `/etc/minecraft/minecraft.env`
- `/usr/local/bin/minecraftctl`
- `/usr/local/bin/minecraft-backup`
- `/usr/local/bin/minecraft-backup-manual`
- `/etc/systemd/system/minecraft-backup.service`
- `/etc/systemd/system/minecraft-backup.timer`
- `/etc/minecraft/restic.env`
- `/etc/systemd/system/mcweb.service`
- `/etc/minecraft/mcweb.env`

Why:
- `minecraft.container` + `minecraft.env` define runtime behavior.
- `minecraftctl` gives a single operational interface.
- Backup service/timer formalize scheduled protection.
- `mcweb` exposes limited admin controls for non-terminal users.

### Service behavior

- `minecraft.service` runs the container with restart policy `always`.
- BlueMap port is published when enabled.
- Backup timer is driven by `minecraft_backup_schedule` (currently `*-*-* 03:15:00`).
- Backup mode defaults to local tar archives when restic is disabled.

## Operator Modes

Use one of two modes consistently:

1. GitOps mode (preferred):
- edit inventory/playbook/templates in this repo
- deploy with Ansible

2. Incident mode (allowed):
- perform emergency commands directly on `media1`
- record actions and convert durable changes into Ansible afterwards

## Day-to-Day Operations

### Connect and baseline checks

From `ws1` (repo root):

```bash
cd automation/ansible
ansible media1 -m ping -o
ansible media1 -m shell -a "systemctl is-active minecraft.service" -o
ansible media1 -m shell -a "systemctl is-active minecraft-backup.timer" -o
```

### Use the control wrapper

On `media1`:

```bash
sudo minecraftctl status
sudo minecraftctl logs
sudo minecraftctl restart
sudo minecraftctl backup
sudo minecraftctl manual-backup
sudo minecraftctl manual-backup-live
```

`manual-backup` is consistent mode (stops service if active).
`manual-backup-live` is online mode (faster, but less crash-consistent).

### Restart server safely

Preferred:

```bash
sudo minecraftctl restart
sudo systemctl is-active minecraft.service
sudo journalctl -u minecraft.service -n 80 --no-pager
```

If applying plugin changes, always validate startup logs after restart.

## Backup Operations

### Current Backup and Snapshot Strategy (as of 2026-04-23)

Backup strategy currently in place:
- Automated nightly backup is enabled (`minecraft_backup_enabled: true`).
- Schedule is systemd timer based (`minecraft_backup_schedule: *-*-* 03:15:00`).
- Active mode is local archive backup (restic is configured but disabled).
- Archives are written to `/srv/minecraft/backups` as `nightly-live-YYYYMMDD-HHMMSS.tar.gz`.
- Local retention currently keeps 14 days of nightly archives and removes archives older than 14 days.
- Manual backups are available in two modes:
  - `manual-backup` (consistent, service stop/start)
  - `manual-backup-live` (online, lower interruption)

Repository-prepared enhancement for next deploy:
- Scheduled player-state snapshots every 15 minutes via `minecraft-playerstate-backup.timer`.
- Player-state archives written to `/srv/minecraft/backups/playerstate` as `playerstate-<label>-YYYYMMDD-HHMMSS.tar.gz`.
- Player-state scope includes `playerdata`, `advancements`, `stats`, `plugins/AxGraves/data.json`, `plugins/Essentials/userdata`, and `usercache.json`.
- Local player-state retention prepared for 7 days.
- Pre-deploy player-state checkpoint prepared in `deploy-minecraft.yml` before risky deploy actions continue.
- If `RESTIC_ENABLED=true`, the same player-state backup script is prepared to push those paths off-host with `minecraft` and `playerstate` tags.

Snapshot strategy currently in place:
- No automated VM-level snapshot policy is defined in this repository for `media1`.
- Operational safety snapshot exists at restore time via `data.pre-restore-<timestamp>` folder rollover before overwriting `/srv/minecraft/data`.
- Plugin/config/playerdata "snapshot" guidance exists in docs/checklists as procedural best practice, but not as an automated snapshot scheduler.

Implication:
- Primary recovery mechanism today is file-level tar backup/restore.
- VM snapshots must be run manually in Proxmox if desired.

### 1) Scheduled backups

- Triggered by `minecraft-backup.timer`
- Executes `minecraft-backup.service` -> `/usr/local/bin/minecraft-backup`
- Default archive format: `nightly-live-YYYYMMDD-HHMMSS.tar.gz`
- Default retention in local mode: keeps 14 days, prunes on day 15+

Check status:

```bash
sudo systemctl status minecraft-backup.timer --no-pager
sudo systemctl show minecraft-backup.timer -p LastTriggerUSec -p NextElapseUSecRealtime
sudo journalctl -u minecraft-backup.service -n 50 --no-pager
```

### 2) Manual backups

Consistent backup (recommended before risky changes):

```bash
sudo minecraftctl manual-backup
```

Live backup (minimal interruption):

```bash
sudo minecraftctl manual-backup-live
```

Manual archive names:
- `manual-consistent-YYYYMMDD-HHMMSS.tar.gz`
- `manual-live-YYYYMMDD-HHMMSS.tar.gz`

### 2b) Player-state backups

After the next deploy, the prepared player-state flows are:

Manual consistent player-state backup:

```bash
sudo minecraftctl playerstate-backup
```

Manual live player-state backup:

```bash
sudo minecraftctl playerstate-backup-live
```

Scheduled timer:
- `minecraft-playerstate-backup.timer`
- Default schedule prepared in inventory: every 15 minutes

Player-state archive contents:
- `/srv/minecraft/data/world_recovery/playerdata`
- `/srv/minecraft/data/world_recovery/advancements`
- `/srv/minecraft/data/world_recovery/stats`
- `/srv/minecraft/data/plugins/AxGraves/data.json`
- `/srv/minecraft/data/plugins/Essentials/userdata`
- `/srv/minecraft/data/usercache.json`

Archive name:
- `playerstate-<label>-YYYYMMDD-HHMMSS.tar.gz`

### 3) Verify backup artifact

```bash
sudo ls -lah /srv/minecraft/backups | tail -n 20
sudo sha256sum /srv/minecraft/backups/<archive>.tar.gz
sudo tar -tzf /srv/minecraft/backups/<archive>.tar.gz | head -n 40
```

Minimum verification criteria:
- archive exists and size is plausible
- checksum command succeeds
- archive contains expected `/srv/minecraft/data/...` tree

## Restore and Rollback

### Full restore from archive (safe pattern)

Run on `media1`:

```bash
sudo bash -lc '
set -euo pipefail
archive="/srv/minecraft/backups/<archive>.tar.gz"
ts="$(date +%Y%m%d-%H%M%S)"
test -f "$archive"
systemctl stop minecraft.service
if [ -d /srv/minecraft/data ]; then
  mv /srv/minecraft/data "/srv/minecraft/data.pre-restore-$ts"
fi
tar -xzf "$archive" -C /
chown -R minecraft:mcmods /srv/minecraft/data
systemctl start minecraft.service
systemctl is-active minecraft.service
echo "RESTORED_FROM=$archive"
echo "PREVIOUS_DATA_SAVED=/srv/minecraft/data.pre-restore-$ts"
'
```

Why this pattern:
- preserves the current state before overwrite
- enables immediate rollback to pre-restore data folder if needed

### Roll back a failed restore

```bash
sudo systemctl stop minecraft.service
sudo rm -rf /srv/minecraft/data
sudo mv /srv/minecraft/data.pre-restore-<timestamp> /srv/minecraft/data
sudo chown -R minecraft:mcmods /srv/minecraft/data
sudo systemctl start minecraft.service
```

## Player-only recovery (inventory/spawn)

When only a user's items/spawn are broken, do not always full-restore first.

Relevant files inside world directory:
- Player inventory and XP: `/srv/minecraft/data/<world>/playerdata/<uuid>.dat`
- Advancements: `/srv/minecraft/data/<world>/advancements/<uuid>.json`
- Stats: `/srv/minecraft/data/<world>/stats/<uuid>.json`

Global spawn:
- stored in world level data and set by deploy via RCON `setworldspawn`
- configured in inventory variables (`minecraft_spawn_world`, `minecraft_spawn_x`, `minecraft_spawn_y`, `minecraft_spawn_z`)

Per-player bed respawn:
- tied to player data; restoring `playerdata/<uuid>.dat` can recover it

Recommended targeted recovery flow:
1. Stop server.
2. Extract only needed player files from selected archive into temp path.
3. Replace matching files in live world.
4. Fix ownership.
5. Start server and validate with player.

## Replicate Server and Create New Server from Current State

Use one of these patterns depending on goal.

### Pattern A: Build new server from code (clean + repeatable)

Use when you want consistent infra and can accept fresh world unless migrated later.

Steps:
1. Provision new VM.
2. Add host entry in `automation/ansible/inventories/lab/hosts.yml`.
3. Add host vars file based on media1 in `automation/ansible/inventories/lab/host_vars/<newhost>.yml`.
4. Set host-specific values:
- hostname/IP/interface
- tailscale key/tag strategy
- mcweb credentials from vault
- ports if running in parallel
5. Run deploy:

```bash
cd automation/ansible
ansible-playbook playbooks/deploy-minecraft.yml -l <newhost>
```

6. Validate service, logs, backup timer.

### Pattern B: Clone current server content to new host (stateful copy)

Use when new server must match current world/player/plugin state.

Recommended process:
1. Build target host with Pattern A first.
2. On source (`media1`), create consistent manual backup.
3. Transfer selected archive to target (`scp`/`rsync`).
4. Restore archive on target with full restore pattern.
5. Adjust host-specific configs (IP, tailscale, public endpoints).
6. Start and validate target.

For lowest divergence during cutover:
- freeze writes on source briefly
- take final backup
- restore final backup on target
- switch clients/DNS/routing

### Pattern C: Fast DR from latest backup on same host

Use after accidental changes or corruption on media1.

Steps:
1. Identify latest valid archive from backup service log.
2. Run full restore pattern.
3. Validate player inventory/spawn/world.
4. Create immediate post-restore manual backup.

## Operations Map (What lives where)

Data and world:
- `/srv/minecraft/data`
- `/srv/minecraft/data/world_recovery`
- `/srv/minecraft/data/world_nether`
- `/srv/minecraft/data/world_the_end`
- `/srv/minecraft/data/plugins`
- `/srv/minecraft/data/disabled-plugins`
- `/srv/minecraft/data/mods`
- `/srv/minecraft/data/disabled-mods`

Backups:
- `/srv/minecraft/backups`

System configs and units:
- `/etc/minecraft/minecraft.env`
- `/etc/minecraft/restic.env`
- `/etc/minecraft/mcweb.env`
- `/etc/containers/systemd/minecraft.container`
- `/etc/systemd/system/minecraft-backup.service`
- `/etc/systemd/system/minecraft-backup.timer`
- `/etc/systemd/system/mcweb.service`

Operator scripts:
- `/usr/local/bin/minecraftctl`
- `/usr/local/bin/minecraft-backup`
- `/usr/local/bin/minecraft-backup-manual`

## Troubleshooting Guide

### Minecraft service will not start

Checks:

```bash
sudo systemctl status minecraft.service --no-pager
sudo journalctl -u minecraft.service -n 200 --no-pager
sudo podman ps -a --format '{{.Names}} {{.Status}}'
```

Common causes:
- bad plugin jar or plugin incompatibility
- duplicate plugin names
- mixed Quests major versions
- permissions drift in `/srv/minecraft/data`

Fixes:
- move suspect jars to `disabled-plugins`
- ensure ownership `minecraft:mcmods`
- redeploy playbook and restart

### Backup not running

Checks:

```bash
sudo systemctl status minecraft-backup.timer --no-pager
sudo systemctl list-timers --all | grep minecraft-backup
sudo journalctl -u minecraft-backup.service -n 100 --no-pager
```

Common causes:
- timer disabled
- script or env changes not reloaded
- backup path permission issues

Fixes:
- `sudo systemctl daemon-reload`
- `sudo systemctl enable --now minecraft-backup.timer`
- run one-shot backup and inspect logs

### Permission denied in backup directory

Expected mode from automation:
- `/srv/minecraft/backups` owner `minecraft`, group `mcmods`, mode `0750`

If operator needs read access:
- use sudo
- or add operator to `mcmods` and relogin

### Player lost items / spawn problems

Triage:
1. Confirm incident time.
2. Identify nearest backup before incident.
3. Prefer targeted `playerdata` restore when possible.
4. Full world restore only if scope is broad.

Post-incident:
- capture `RESTORED_FROM` and `PREVIOUS_DATA_SAVED`
- take immediate post-restore backup

### mcweb issues

Checks:

```bash
sudo systemctl status mcweb.service --no-pager
sudo journalctl -u mcweb.service -n 120 --no-pager
sudo ss -lntp | grep 8080
```

Common causes:
- missing/invalid `MC_SECRET_KEY` or `MC_PASSWORD_HASH`
- bind IP mismatch
- file access restrictions due to hardening

## Change Management Checklist

Before changes:
1. Confirm current server healthy.
2. Take `manual-backup`.
3. Verify archive exists and is readable.
4. Record intended change and rollback plan.

During changes:
1. Change one scope at a time (plugins, quests, world scripts).
2. Restart and validate logs after each scope.

After changes:
1. Validate player join, inventory, spawn, and key commands.
2. Record change in changelog/build-log.
3. Keep rollback pointer for at least one day.

## Security and Secrets Notes

- Keep secrets in vault, not plaintext host vars.
- Rotate exposed auth keys immediately if leaked.
- Use key-based access for `mcadmin` where possible.

## Canonical Commands (Quick Reference)

On media1:

```bash
sudo minecraftctl status
sudo minecraftctl logs
sudo minecraftctl restart
sudo minecraftctl backup
sudo minecraftctl manual-backup
sudo minecraftctl manual-backup-live
sudo systemctl status minecraft-backup.timer --no-pager
sudo journalctl -u minecraft-backup.service -n 50 --no-pager
```

From ws1 via Ansible:

```bash
cd automation/ansible
ansible media1 -m ping -o
ansible media1 -m shell -a "systemctl is-active minecraft.service" -o
ansible media1 -m shell -a "journalctl -u minecraft.service -n 80 --no-pager" -o
ansible-playbook playbooks/deploy-minecraft.yml -l media1
```
