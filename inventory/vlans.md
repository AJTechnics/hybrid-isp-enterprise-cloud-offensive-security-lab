# VLANs

Document VLAN assignments here as they are configured.

## VLAN Table

| VLAN ID | Name | Segment | Subnet | Purpose | Phase |
|---|---|---|---|---|---|
| TBD | MGMT | MGMT | 10.10.0.0/24 | Host and device management | base |
| TBD | DMZ | DMZ | 10.20.10.0/24 | Public-facing services | 2 |
| TBD | SERVER | SERVER | 10.20.20.0/24 | Internal servers | 2 |
| TBD | CLIENT | CLIENT | 10.20.30.0/24 | User/workstation segment | 2 |
| TBD | SECURITY | SECURITY | 10.20.40.0/24 | Attacker network | 5 |
| TBD | AUTOMATION | AUTOMATION | 10.20.50.0/24 | NetBox, Ansible, tooling | 6 |

## Notes

- VLAN IDs to be assigned during Phase 2 (firewall and segmentation)
- Proxmox bridges map to VLANs — document bridge names here
- Provider domain (ISP-CORE, ISP-EDGE, CE-PE) uses point-to-point links, not VLANs
