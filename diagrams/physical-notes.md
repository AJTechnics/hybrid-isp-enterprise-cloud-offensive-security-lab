# Physical Notes

## Host Hardware

| Component | Current | Target |
|---|---|---|
| Machine | ThinkCentre | ThinkCentre (same) |
| RAM | 8 GB | 32 GB |
| Storage | TBD | 1 TB SSD |
| Hypervisor | None yet | Proxmox VE |
| NICs | TBD | At least 1 (MGMT + lab bridges via Proxmox) |

## Proxmox Bridge Design

Proxmox Linux bridges will be used to create isolated lab segments. Each bridge corresponds to a network segment.

| Bridge | Segment | Subnet | Notes |
|---|---|---|---|
| vmbr0 | MGMT / host uplink | 10.10.0.0/24 | Physical NIC attached |
| vmbr1 | ISP-CORE | 10.255.0.0/24 | Internal only |
| vmbr2 | ISP-EDGE | 10.254.0.0/24 | Internal only |
| vmbr3 | CE-PE | 172.16.0.0/30 | Internal only |
| vmbr4 | DMZ | 10.20.10.0/24 | Internal only |
| vmbr5 | SERVER | 10.20.20.0/24 | Internal only |
| vmbr6 | CLIENT | 10.20.30.0/24 | Internal only |
| vmbr7 | SECURITY | 10.20.40.0/24 | Internal only |
| vmbr8 | AUTOMATION | 10.20.50.0/24 | Internal only |

## Notes

- Bridge assignments above are a starting design — adjust to suit Proxmox conventions
- Proxmox host management IP to be on vmbr0
- Lab bridges (vmbr1+) should be internal only — no physical NIC attached
- All VMs attach to the bridge(s) matching their segment(s)
- Multi-homed VMs (routers) attach to multiple bridges

## Phase 0 Hardware Tasks

- [ ] Upgrade RAM to 32 GB
- [ ] Confirm SSD capacity and install if needed
- [ ] Install Proxmox VE
- [ ] Configure initial bridges before deploying VMs
- [ ] Document final bridge assignments here
