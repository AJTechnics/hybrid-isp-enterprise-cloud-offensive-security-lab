# Topology

## High-Level End State

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
                [ Enterprise Firewall ]
                          |
       ------------------------------------------------
       |                      |                       |
     [ DMZ ]              [ Server ]              [ Client ]
       |                      |                       |
 [ Load Balancer ]       [ AD / DNS ]            [ User VM ]
       |
   [ Web App ]

Parallel domains:
- AWS VPC via VPN
- Kali / offensive security segment
- NetBox + automation + monitoring
```

```
## Current active topology
## Mikrotik integration is planned later
[ Desktop / Laptop ]
        |
      SSH
        |
      [ ws1 ]
        |
   [ Proxmox host ]
        |
   [ USW8-Lite ]


```

## Routing Domains

### Provider Domain

| Device | Role |
|---|---|
| ISP-EDGE | Simulated transit/edge |
| ISP-CORE1 | Provider core router |
| ISP-CORE2 | Provider core router |
| PE1 | Provider edge router |

### Customer Domain

| Device | Role |
|---|---|
| CE1 | Customer edge router |
| fw1 | Enterprise firewall |
| Internal VLANs | DMZ, SERVER, CLIENT, MGMT |

### Security Domain

| Device | Role |
|---|---|
| kali1 | Attacker / offensive host |
| vuln1 | Vulnerable target |

### Cloud Domain

| Component | Role |
|---|---|
| AWS VPC | Cloud extension |
| EC2 instances | Cloud-hosted services |
| VPN / hybrid path | Connectivity to on-prem |

## Network Segments

| Segment | Purpose | Subnet |
|---|---|---|
| MGMT | Host and device management | 10.10.0.0/24 |
| ISP-CORE | Provider core links / loopbacks | 10.255.0.0/24 + P2P /31 or /30 |
| ISP-EDGE | Transit/external simulation | 10.254.0.0/24 |
| CE-PE | Customer/provider handoff | 172.16.0.0/30 |
| DMZ | Public-facing services | 10.20.10.0/24 |
| SERVER | Internal servers | 10.20.20.0/24 |
| CLIENT | User/workstation segment | 10.20.30.0/24 |
| SECURITY | Attacker network | 10.20.40.0/24 |
| AUTOMATION | NetBox, Ansible, tooling | 10.20.50.0/24 |
| CLOUD | AWS VPC | 10.100.0.0/16 |

## Traffic Paths

### Client to Internet (North-South)
```
Client VM → fw1 (CLIENT zone) → CE1 → PE1 → ISP-CORE → ISP-EDGE → Transit
```

### Client to DMZ App via Load Balancer
```
Client VM → fw1 → DMZ → lb1 (VIP) → app1 (backend)
```

### Offensive Segment to Target
```
kali1 (SECURITY segment) → fw1 (or direct L2) → vuln1 / DMZ services
```

### On-Prem to AWS
```
fw1 or CE1 → VPN tunnel → AWS VGW → VPC → EC2
```
