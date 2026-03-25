# Hardware

## Current Hardware

| Component | Details |
|---|---|
| Host | ThinkCentre |
| RAM | 8 GB (current) → 32 GB (target) |
| Storage | SSD preferred, 1 TB target |
| Hypervisor | Proxmox VE |

## Recommended Minimum Upgrade

- 32 GB RAM
- SSD, preferably 1 TB
- Proxmox as hypervisor

## Notes

32 GB is enough to build a serious first version if VM sizing stays disciplined. A second node can be added later for separation and realism.

## VM Sizing Summary

Total estimated RAM for all VMs (all phases):

| VM | RAM |
|---|---|
| isp-core1 | 512 MB–1 GB |
| isp-core2 | 512 MB–1 GB |
| isp-edge1 | 512 MB–1 GB |
| pe1 | 1 GB |
| ce1 | 512 MB–1 GB |
| fw1 | 1 GB |
| win-ad1 | 4 GB |
| app1 | 1 GB |
| lb1 | 1 GB |
| kali1 | 2 GB |
| vuln1 | 1 GB |
| netbox1 | 2 GB |
| auto1 | 2 GB |
| mon1 | 2 GB |
| **Total (max)** | **~22 GB** |

Running all VMs simultaneously at max sizing requires ~22 GB. 32 GB provides comfortable headroom.

## Phase 0 Hardware Tasks

- [ ] Upgrade ThinkCentre to 32 GB RAM
- [ ] Confirm SSD capacity (target 1 TB)
- [ ] Install Proxmox VE
