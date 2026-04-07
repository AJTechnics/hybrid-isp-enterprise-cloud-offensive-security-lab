# Phase 00 - Foundation

## Goal

Create the project structure, workspace foundation, storage policy, and documentation baseline before deeper automation and network deployment.

## Completed

- [x] Proxmox reinstalled
- [x] secondary SSD detected
- [x] secondary SSD configured as `vmdata`
- [x] Ubuntu Server 24.04 VM installed as `ws1`
- [x] SSH access to `ws1` working
- [x] Podman installed on `ws1`
- [x] toolbox container baseline built
- [x] documentation baseline started
- [x] OpenTofu Initialized
- [x] Podman toolbox working
- [x] Proxmox rebuilt
- [x] `vmdata` storage configured
- [x] `ws1` workspace VM deployed
- [x] First VM successfully deployed via OpenTofu

## Remaining

- [ ] commit and push updated documentation
- [ ] connect OpenTofu to Proxmox
- [ ] define first automated VM deployment

## Exit criteria

- documentation reflects actual state
- workspace is stable
- storage policy is documented
- ready to begin OpenTofu integration
