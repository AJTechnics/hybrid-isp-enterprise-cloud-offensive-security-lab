# Minecraft Cutover Checklist (Selective World and Player Migration)

## Purpose

This checklist covers controlled migration from `media1` to a new Minecraft host while preserving world and player state without carrying over plugins, mods, or plugin-managed content.

Use this when creating a clean server and importing only the canonical world data, player data, and backup history.

## Scope

- Source host: `media1`
- Target host: `<newhost>`
- Migration method: build target from Ansible + selectively restore world and backup data from the latest consistent archive

## Preconditions

1. Target VM provisioned and reachable.
2. Host entry added to inventory.
3. Host vars file prepared for a clean target profile.
4. Secrets prepared (tailscale, mcweb, other vault values).
5. Maintenance window approved.
6. Target world name decided before import, for example `sib_world`.
7. Optional client-side mods communicated to players separately. Xaero's Minimap
  is client-side only and is not deployed through the Paper server plugin or
  mod automation in this repo.

## Phase 1: Build and Validate Target (No Traffic)

1. Deploy target with Ansible.

```bash
cd automation/ansible
ansible-playbook playbooks/deploy-minecraft.yml -l <newhost>
```

2. Validate target services:

```bash
ansible <newhost> -m shell -a "systemctl is-active minecraft.service" -o
ansible <newhost> -m shell -a "systemctl is-active minecraft-backup.timer" -o
ansible <newhost> -m shell -a "journalctl -u minecraft.service -n 80 --no-pager" -o
```

3. Confirm target starts cleanly before data migration.

## Phase 2: Prepare Source for Data Export

1. Confirm source health.
2. Trigger consistent manual backup on source.
3. Verify archive exists and is readable.

On source (`media1`):

```bash
sudo minecraftctl status
sudo minecraftctl manual-backup
sudo ls -1t /srv/minecraft/backups/manual-consistent-*.tar.gz | head -n 1
```

Record selected archive:
- `ARCHIVE=/srv/minecraft/backups/manual-consistent-YYYYMMDD-HHMMSS.tar.gz`

## Phase 3: Transfer Archive to Target

1. Copy archive from source to target.

Example:

```bash
scp lab@192.168.1.131:/srv/minecraft/backups/<archive>.tar.gz lab@<target_ip>:/tmp/
```

2. Verify checksum matches source and target.

## Phase 4: Selective Restore on Target

On target host:

```bash
sudo bash -lc '
set -euo pipefail
archive="/tmp/<archive>.tar.gz"
ts="$(date +%Y%m%d-%H%M%S)"
source_level="world_recovery"
target_level="sib_world"
staging="/srv/minecraft/restore-$ts"
test -f "$archive"
systemctl stop minecraft.service
mkdir -p "$staging"
tar -xzf "$archive" -C "$staging"

src_data="$staging/srv/minecraft/data"
src_backups="$staging/srv/minecraft/backups"

test -d "$src_data/$source_level"

rm -rf \
  "/srv/minecraft/data/$target_level" \
  "/srv/minecraft/data/${target_level}_nether" \
  "/srv/minecraft/data/${target_level}_the_end"

rsync -a --delete "$src_data/$source_level/" "/srv/minecraft/data/$target_level/"

if [ -d "$src_data/${source_level}_nether" ]; then
  rsync -a --delete "$src_data/${source_level}_nether/" "/srv/minecraft/data/${target_level}_nether/"
fi

if [ -d "$src_data/${source_level}_the_end" ]; then
  rsync -a --delete "$src_data/${source_level}_the_end/" "/srv/minecraft/data/${target_level}_the_end/"
fi

if [ -d "$src_backups" ]; then
  rsync -a "$src_backups/" /srv/minecraft/backups/
fi

chown -R minecraft:mcmods /srv/minecraft/data /srv/minecraft/backups
rm -rf "$staging"
systemctl start minecraft.service
systemctl is-active minecraft.service
echo "RESTORED_FROM=$archive"
echo "SOURCE_LEVEL=$source_level"
echo "TARGET_LEVEL=$target_level"
'
```

Validate:

```bash
sudo journalctl -u minecraft.service -n 120 --no-pager
sudo minecraftctl status
```

## Phase 5: Pre-Cutover Acceptance Tests

1. Confirm the imported world loads as expected under the target world name.
2. Validate sample player inventory and spawn behavior.
3. Confirm no plugins or mods were restored onto the clean target.
4. Validate backup timer on target.

Commands:

```bash
sudo systemctl is-active minecraft-backup.timer
sudo systemctl show minecraft-backup.timer -p NextElapseUSecRealtime
```

Recommended functional checks:

```bash
# Confirm the clean target has no plugin jars restored from the source host.
find /srv/minecraft/data/plugins -maxdepth 1 -type f -name '*.jar'

# Confirm the imported world/player data exists under the new world name.
find /srv/minecraft/data/sib_world -maxdepth 2 \( -name playerdata -o -name advancements -o -name stats \)
```

Client mod note:

- Xaero's Minimap should be installed by players in their own client mod loader.
- Do not try to add Xaero's Minimap to a `minecraft_paper_plugins` list on
  Paper hosts like `media2`; it is not a Bukkit/Paper plugin.
- If a server-hosted map is needed, keep using a server-compatible option such
  as BlueMap.

## Phase 6: Final Cutover (Low-Divergence)

1. Announce maintenance.
2. Freeze writes on source (stop service or block joins briefly).
3. Take final consistent backup on source.
4. Transfer final archive to target.
5. Selectively restore final archive on target.
6. Switch endpoint routing (DNS/Tailscale/public entry).
7. Open target to players.

## Rollback Plan

Trigger rollback if:
- target crashes repeatedly
- major data mismatch
- player validation fails

Rollback steps:
1. Point traffic back to source.
2. Start source service if stopped.
3. Preserve target evidence/logs.
4. Reassess and schedule second cutover window.

## Post-Cutover Tasks

1. Trigger immediate manual backup on target.
2. Confirm next nightly backup schedule on target.
3. Update inventory/docs to mark target as production.
4. Archive cutover report and commands used.
5. Record source and target world names used during migration.

## Cutover Record Template

- Source host:
- Target host:
- Window start/end (UTC):
- Archive used for pre-cutover test:
- Archive used for final cutover:
- Source world name:
- Target world name:
- Validation players:
- Outcome:
- Rollback required (yes/no):
- Follow-up tasks:
