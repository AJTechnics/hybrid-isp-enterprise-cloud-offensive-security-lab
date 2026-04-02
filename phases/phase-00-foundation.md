# Phase 00 — Project Foundation

## Goal

Create structure, naming, documentation, and build rules before deploying any VMs.

## Scope

This phase is purely organizational. No infrastructure is deployed.

## Components

- GitHub repository
- Obsidian vault structure
- Naming standards
- IP plan (initial)
- VM inventory (initial)
- Project journal (started)

## Tasks

- [x] Upgrade ThinkCentre to 16 GB RAM
- [x] Confirm SSD capacity
- [x] Install Proxmox
- [x] Create GitHub repository
- [x] Create Obsidian project vault/folder structure
- [x] Add README.md
- [x] Add phase files
- [ ] Add VM inventory file
- [ ] Add IP plan file
- [ ] Decide router platform: VyOS or FRRouting-based Linux routers
- [ ] Define hostname standard
- [ ] Define subnet standard
- [ ] Define phase tracker
- [ ] Define lab rules for documenting changes

## Risks / Blockers

- Hardware not yet upgraded to 32 GB RAM
- Proxmox not yet installed

## Validation

- Repository exists and is committed
- Directory structure matches blueprint
- README describes the project
- Phase tracker is readable

## Notes

- Router platform decision (VyOS vs FRRouting-based Linux) should be made before Phase 1
- Obsidian vault structure mirrors the GitHub repository structure

## Exit Criteria

- Project structure exists
- First README is committed
- Phase tracker is ready
