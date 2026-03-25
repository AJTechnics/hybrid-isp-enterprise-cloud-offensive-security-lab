# Prefixes

Document all IP prefixes allocated in the lab.

## Prefix Allocations

| Prefix | Description | Segment | Assigned To | Phase |
|---|---|---|---|---|
| 10.10.0.0/24 | Management network | MGMT | Proxmox host, OOB | base |
| 10.20.10.0/24 | DMZ | DMZ | fw1, lb1, web app | 2 |
| 10.20.20.0/24 | Server segment | SERVER | win-ad1, app1 | 2 |
| 10.20.30.0/24 | Client segment | CLIENT | Test client VMs | 2 |
| 10.20.40.0/24 | Security/attacker segment | SECURITY | kali1, vuln1 | 5 |
| 10.20.50.0/24 | Automation segment | AUTOMATION | netbox1, auto1, mon1 | 6 |
| 10.254.0.0/24 | ISP-EDGE / transit simulation | ISP-EDGE | isp-edge1 | 1 |
| 10.255.0.0/24 | Provider core loopbacks | ISP-CORE | isp-core1, isp-core2, isp-edge1, pe1 | 1 |
| 10.255.1.0/24 | Provider core P2P links | ISP-CORE | Core router interfaces | 1 |
| 172.16.0.0/30 | CE-PE handoff | CE-PE | pe1, ce1 | 1 |
| 10.100.0.0/16 | AWS VPC | CLOUD | AWS VPC | 7 |
| 10.100.1.0/24 | AWS public subnet | CLOUD | NAT GW, bastion | 7 |
| 10.100.2.0/24 | AWS private subnet | CLOUD | EC2 workloads | 7 |

## Notes

- Loopback /32s to be allocated from 10.255.0.0/24 and documented here
- P2P /31 links to be allocated from 10.255.1.0/24 and documented here
- All addresses to be tracked in NetBox from Phase 6 onwards
