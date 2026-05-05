# Minecraft Incident Response Playbook

## Purpose

This playbook is for urgent production incidents on `media1`.

Use it when you need fast containment, recovery, and clean handoff to normal operations.

## Severity Model

- `SEV-1`: Server down, corrupted world, mass data loss, inaccessible for all users
- `SEV-2`: Major gameplay degradation (inventory/spawn failures, plugin failures, repeated crashes)
- `SEV-3`: Minor issue, partial feature failure, non-critical admin issue

Escalate to `SEV-1` when data integrity is uncertain.

## Golden Rules

1. Preserve evidence first (logs + timestamps).
2. Take a manual backup before risky corrective actions.
3. Prefer smallest-scope recovery first (targeted player restore before full world restore).
4. Record exact commands executed.
5. After recovery, capture prevention tasks into Ansible/docs.

## First 10 Minutes Checklist

1. Confirm impact and start incident timeline.
2. Run quick health checks.
3. Freeze high-risk changes.
4. Create pre-fix backup.

Commands:

```bash
sudo minecraftctl status
sudo journalctl -u minecraft.service -n 120 --no-pager
sudo journalctl -u minecraft-backup.service -n 80 --no-pager
sudo minecraftctl manual-backup
```

## Incident Workflows

### A) Server will not start

Symptoms:
- `minecraft.service` inactive/failed
- crash loops in journal

Triage:

```bash
sudo systemctl status minecraft.service --no-pager
sudo journalctl -u minecraft.service -n 300 --no-pager
sudo podman ps -a --format '{{.Names}} {{.Status}}'
```

Likely causes:
- plugin incompatibility
- duplicate/conflicting plugin jars
- bad file ownership under `/srv/minecraft/data`

Recovery pattern:
1. Move suspected new plugin jars to `/srv/minecraft/data/disabled-plugins`.
2. Fix ownership.
3. Restart and re-check logs.

```bash
sudo chown -R minecraft:mcmods /srv/minecraft/data
sudo minecraftctl restart
sudo journalctl -u minecraft.service -n 200 --no-pager
```

### B) Player inventory or spawn lost

Symptoms:
- one/few players missing inventory or wrong respawn behavior

Approach:
1. Check whether `keepInventory` is still true in every vanilla dimension.
2. If any dimension is false, reapply it before further player testing.
3. Determine incident time and affected UUID(s).
4. Choose nearest backup before incident.
5. Prefer targeted restore of player files.

Quick check/remediation:

```bash
sudo podman exec -u 999 minecraft rcon-cli "mv gamerule list world_recovery --filter keepInventory"
sudo podman exec -u 999 minecraft rcon-cli "mv gamerule list world_recovery_nether --filter keepInventory"
sudo podman exec -u 999 minecraft rcon-cli "mv gamerule list world_recovery_the_end --filter keepInventory"

sudo podman exec -u 999 minecraft rcon-cli "mv gamerule set keepInventory true world_recovery"
sudo podman exec -u 999 minecraft rcon-cli "mv gamerule set keepInventory true world_recovery_nether"
sudo podman exec -u 999 minecraft rcon-cli "mv gamerule set keepInventory true world_recovery_the_end"
```

If the gamerule was false when the death happened, the inventory is already gone and must be restored from backup or recovered from a grave plugin.

Target files:
- `/srv/minecraft/data/world_recovery/playerdata/<uuid>.dat`
- `/srv/minecraft/data/world_recovery/advancements/<uuid>.json`
- `/srv/minecraft/data/world_recovery/stats/<uuid>.json`

If AxGraves is installed, also verify whether a grave was created for the death before restoring backup data.

If broad corruption, execute full restore from archive.

### C) World corruption / broad data issue

Symptoms:
- many users affected
- world chunks/state inconsistent

Recovery:
1. Stop server.
2. Save current state to `data.pre-restore-<timestamp>`.
3. Restore selected archive.
4. Start and validate.

Use canonical restore command from [runbooks/minecraft-operations.md](runbooks/minecraft-operations.md#L198).

### D) Backup pipeline failure

Symptoms:
- no new nightly archive
- timer inactive

Triage:

```bash
sudo systemctl status minecraft-backup.timer --no-pager
sudo systemctl list-timers --all | grep minecraft-backup
sudo journalctl -u minecraft-backup.service -n 150 --no-pager
```

Recovery:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now minecraft-backup.timer
sudo minecraftctl backup
sudo journalctl -u minecraft-backup.service -n 80 --no-pager
```

### E) mcweb unavailable

Triage:

```bash
sudo systemctl status mcweb.service --no-pager
sudo journalctl -u mcweb.service -n 150 --no-pager
sudo ss -lntp | grep 8080
```

Check env:
- `/etc/minecraft/mcweb.env`
- `MC_SECRET_KEY`
- `MC_PASSWORD_HASH`

## Verification Before Closure

1. Service active.
2. Affected players can join.
3. Inventory/spawn or world behavior confirmed recovered.
4. Backup timer active and a manual backup succeeds.

Commands:

```bash
sudo systemctl is-active minecraft.service
sudo systemctl is-active minecraft-backup.timer
sudo minecraftctl manual-backup
```

## Incident Record Template

- Incident ID:
- Start time (UTC):
- Severity:
- Trigger/symptom:
- Impact scope:
- Backup used (if any):
- Commands executed:
- Recovery confirmation:
- Follow-up automation/doc tasks:

## Post-Incident Hardening Tasks

1. Convert emergency manual fixes into Ansible.
2. Add/adjust pre-change backup checkpoints.
3. Update runbooks/checklists.
4. Decide whether VM snapshot policy should be automated outside Ansible (Proxmox).
