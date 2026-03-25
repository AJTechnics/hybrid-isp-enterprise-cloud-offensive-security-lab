# IP Plan

## Summary

All lab addressing uses RFC 1918 private space. Provider simulation uses 10.255.x and 10.254.x ranges. Enterprise uses 10.20.x. Cloud extends into 10.100.0.0/16.

## Network Segments

| Segment | Purpose | Subnet | Notes |
|---|---|---|---|
| MGMT | Host and device management | 10.10.0.0/24 | Proxmox host, OOB access |
| ISP-CORE | Provider core loopbacks | 10.255.0.0/24 | Loopback /32s allocated here |
| ISP-CORE P2P | Provider core point-to-point links | /31 or /30 from 10.255.1.0/24 | Between core routers |
| ISP-EDGE | Transit/external simulation | 10.254.0.0/24 | Simulates upstream/internet |
| CE-PE | Customer/provider handoff | 172.16.0.0/30 | eBGP or static peering |
| DMZ | Public-facing services | 10.20.10.0/24 | Load balancer, web app |
| SERVER | Internal servers | 10.20.20.0/24 | AD, DNS, app servers |
| CLIENT | User/workstation segment | 10.20.30.0/24 | Test client VMs |
| SECURITY | Attacker network | 10.20.40.0/24 | Kali, vulnerable hosts |
| AUTOMATION | NetBox, Ansible, tooling | 10.20.50.0/24 | SoT and automation node |
| CLOUD | AWS VPC | 10.100.0.0/16 | Split into public/private subnets |

## Loopback Assignments (Provider Domain)

| Device | Loopback | Address |
|---|---|---|
| isp-core1 | lo | TBD |
| isp-core2 | lo | TBD |
| isp-edge1 | lo | TBD |
| pe1 | lo | TBD |

## Point-to-Point Links (Provider Domain)

| Link | Interface A | Interface B | Subnet |
|---|---|---|---|
| isp-core1 ↔ isp-core2 | TBD | TBD | TBD |
| isp-core1 ↔ isp-edge1 | TBD | TBD | TBD |
| isp-core2 ↔ isp-edge1 | TBD | TBD | TBD |
| isp-core1 ↔ pe1 | TBD | TBD | TBD |
| isp-core2 ↔ pe1 | TBD | TBD | TBD |

## Customer Domain Addressing

| Device | Interface | Address | Notes |
|---|---|---|---|
| pe1 | CE-facing | 172.16.0.1/30 | TBD |
| ce1 | PE-facing | 172.16.0.2/30 | TBD |
| fw1 | CE-facing | TBD | |
| fw1 | DMZ | 10.20.10.1/24 | Gateway |
| fw1 | SERVER | 10.20.20.1/24 | Gateway |
| fw1 | CLIENT | 10.20.30.1/24 | Gateway |
| fw1 | SECURITY | 10.20.40.1/24 | Gateway |
| fw1 | AUTOMATION | 10.20.50.1/24 | Gateway |

## AWS VPC (Phase 7)

| Subnet | CIDR | AZ | Purpose |
|---|---|---|---|
| Public | 10.100.1.0/24 | TBD | NAT GW, bastion |
| Private | 10.100.2.0/24 | TBD | EC2 workloads |

## Notes

- All TBD entries to be filled in during Phase 1 build
- Document final addressing in NetBox during Phase 6
- Use /31 for all point-to-point links (RFC 3021)
