# Device Inventory

Track physical and virtual devices here. Update as devices are deployed.

## Devices

| Hostname | Type | Platform | Role | Segment | Phase | Management IP | Status |
|---|---|---|---|---|---|---|---|
| proxmox-host | Physical | Proxmox VE | Hypervisor | MGMT | base | TBD | planned |
| isp-core1 | VM | VyOS / FRR | Provider core router | ISP-CORE | 1 | TBD | planned |
| isp-core2 | VM | VyOS / FRR | Provider core router | ISP-CORE | 1 | TBD | planned |
| isp-edge1 | VM | VyOS / FRR | Transit/edge router | ISP-EDGE | 1 | TBD | planned |
| pe1 | VM | VyOS / FRR | Provider edge | ISP-CORE | 1 | TBD | planned |
| ce1 | VM | VyOS / FRR | Customer edge | CE-PE | 1 | TBD | planned |
| fw1 | VM | pfSense / OPNsense | Enterprise firewall | CE-facing | 2 | TBD | planned |
| win-ad1 | VM | Windows Server | AD / DNS | SERVER | 3 | TBD | planned |
| app1 | VM | Ubuntu / Debian | Application server | SERVER | 3 | TBD | planned |
| lb1 | VM | Ubuntu + HAProxy | Load balancer | DMZ | 4 | TBD | planned |
| kali1 | VM | Kali Linux | Offensive host | SECURITY | 5 | TBD | planned |
| vuln1 | VM | DVWA / Metasploitable | Vulnerable target | SECURITY | 5 | TBD | planned |
| netbox1 | VM | Ubuntu + NetBox | Source of Truth | AUTOMATION | 6 | TBD | planned |
| auto1 | VM | Ubuntu + Ansible | Automation node | AUTOMATION | 6 | TBD | planned |
| mon1 | VM | Ubuntu + monitoring | Monitoring | AUTOMATION | 7 | TBD | planned |

## Notes

- Platform column to be updated when images are confirmed
- Management IPs from MGMT 10.10.0.0/24 range
- Proxmox VM IDs to be added when assigned
