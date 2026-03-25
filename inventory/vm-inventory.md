# VM Inventory

## Status Key

| Status | Meaning |
|---|---|
| planned | Not yet deployed |
| deploying | In progress |
| running | Live and operational |
| stopped | Deployed but not running |
| decommissioned | Removed from lab |

## VM List

| VM | Role | vCPU | RAM | Disk | Segment | Phase | Status |
|---|---|---:|---:|---:|---|---|---|
| isp-core1 | Provider core router | 1 | 512 MB–1 GB | 8 GB | ISP-CORE | 1 | planned |
| isp-core2 | Provider core router | 1 | 512 MB–1 GB | 8 GB | ISP-CORE | 1 | planned |
| isp-edge1 | Simulated transit/edge | 1 | 512 MB–1 GB | 8 GB | ISP-EDGE | 1 | planned |
| pe1 | Provider edge router | 1 | 1 GB | 8 GB | ISP-CORE | 1 | planned |
| ce1 | Customer edge router | 1 | 512 MB–1 GB | 8 GB | CE-PE | 1 | planned |
| fw1 | Enterprise firewall | 1–2 | 1 GB | 16 GB | CE-facing | 2 | planned |
| win-ad1 | Active Directory / DNS | 2 | 4 GB | 60 GB | SERVER | 3 | planned |
| app1 | Linux application server | 1 | 1 GB | 20 GB | SERVER | 3 | planned |
| lb1 | Load balancer (HAProxy) | 1 | 1 GB | 16 GB | DMZ | 4 | planned |
| kali1 | Offensive security host | 2 | 2 GB | 30 GB | SECURITY | 5 | planned |
| vuln1 | Vulnerable target host | 1 | 1 GB | 20 GB | SECURITY | 5 | planned |
| netbox1 | NetBox SoT | 2 | 2 GB | 30 GB | AUTOMATION | 6 | planned |
| auto1 | Automation node | 1–2 | 2 GB | 20 GB | AUTOMATION | 6 | planned |
| mon1 | Monitoring node | 1–2 | 2 GB | 20 GB | AUTOMATION | 7 | planned |

## Notes

- Update status as VMs are deployed
- Track Proxmox VM IDs here once assigned
- Document OS version and image source for each VM
