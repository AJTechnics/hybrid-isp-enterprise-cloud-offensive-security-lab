# Logical Topology

## High-Level Diagram

```text
                [ Internet / Transit Simulation ]
                           |
                      [ ISP-EDGE ]
                      /         \
               [ ISP-CORE1 ] [ ISP-CORE2 ]
                      \         /
                        [ PE1 ]
                          |
                        [ CE1 ]
                          |
                [ Enterprise Firewall (fw1) ]
                          |
       ------------------------------------------------
       |                      |                       |
     [ DMZ ]              [ Server ]              [ Client ]
     10.20.10.0/24        10.20.20.0/24           10.20.30.0/24
       |                      |                       |
 [ lb1 (HAProxy) ]      [ win-ad1 / app1 ]       [ Test Client ]
       |
   [ Web App ]

Parallel / out-of-band domains:
- AWS VPC (10.100.0.0/16) via VPN tunnel
- Kali / offensive security (10.20.40.0/24)
- NetBox + automation + monitoring (10.20.50.0/24)
- MGMT (10.10.0.0/24) — Proxmox and OOB access
```

## Routing Domain Boundaries

```text
[ Provider Domain ]                 [ Customer Domain ]
ISP-EDGE                            CE1
ISP-CORE1  ←— OSPF —→  PE1         |
ISP-CORE2                           fw1 (firewall boundary)
                        |           |
                      CE-PE       Internal zones
                    (172.16.0.0/30)
```

## Key Traffic Paths

| Flow | Path |
|---|---|
| Client → Internet | Client → fw1 → CE1 → PE1 → ISP-CORE → ISP-EDGE |
| Client → DMZ App | Client → fw1 → lb1 (VIP) → app1 |
| Attacker → Target | kali1 → (firewall) → vuln1 / DMZ services |
| On-Prem → AWS | fw1 or CE1 → VPN → AWS VGW → VPC → EC2 |
| MGMT Access | Proxmox host → MGMT segment → All VMs |

## Notes

- Detailed per-phase topology evolution will be documented in the phases directory
- ASCII diagram to be supplemented with drawn diagrams (e.g., draw.io) as the lab grows
- Provider domain P2P addressing documented in [`../docs/ip-plan.md`](../docs/ip-plan.md)
