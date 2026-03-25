# Hybrid ISP + Enterprise + Cloud + Offensive Security Lab

## 1. Project Goal

Build a phased homelab that simulates:

- an ISP core and edge network
- a customer enterprise environment
- load balancing and application delivery
- identity services with Active Directory
- a cloud extension into AWS
- an offensive security segment
- a Source of Truth and automation platform

The purpose of this lab is to:

- refresh and deepen high-level network engineering skills
- regain hands-on confidence in routing, switching, security, and troubleshooting
- build practical exposure to cloud networking and load balancing
- create a platform for offensive security practice
- support a future study group with shared tasks and documentation
- create a portfolio project that can be documented in Obsidian and GitHub

---

## 2. Project Principles

### Build principles

1. **Build in phases, not all at once**
2. **Prefer simple and working over complex and unfinished**
3. **Document every design decision**
4. **Treat the lab like a real customer environment**
5. **Use the lab to explain, teach, and troubleshoot**
6. **Automate only after the manual process is understood**

### Success criteria

This project is successful if I can:

- explain the end-to-end traffic path from user to application
- deploy and troubleshoot the network without guessing
- simulate provider and enterprise routing domains
- expose and protect services through firewall and load balancer layers
- extend the environment into AWS
- test attack paths from an offensive security segment
- document the design clearly enough for others to follow
- use NetBox and automation to track and change the environment

---

## 3. High-Level End State

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

---

## 4. Hardware Baseline

## Current hardware

- ThinkCentre host
- Current RAM: 8 GB
- Target RAM: 32 GB

## Recommended minimum upgrade

- 32 GB RAM
- SSD, preferably 1 TB
- Proxmox as hypervisor

## Notes

32 GB is enough to build a serious first version if VM sizing stays disciplined.
A second node can be added later for separation and realism.

---

## 5. Platform Stack

## Hypervisor

- Proxmox VE

## Network / routing

- VyOS or FRRouting-based Linux routers for ISP/core/edge/customer routing
- pfSense or OPNsense for enterprise firewall

## Load balancing

- HAProxy first
- Later map concepts to F5 terminology and design patterns

## Identity / services

- Windows Server for Active Directory, DNS, optionally DHCP
- Ubuntu or Debian Linux servers for app and utility services

## Cloud

- AWS VPC
- EC2
- Site-to-site VPN or equivalent hybrid connectivity

## Offensive security

- Kali Linux
- DVWA / Metasploitable / intentionally vulnerable hosts

## SoT / automation / monitoring

- NetBox
- PostgreSQL if required by services
- Ansible
- Python
- basic monitoring stack later

---

## 6. Logical Topology

## Routing domains

### Provider domain

- ISP-EDGE
- ISP-CORE1
- ISP-CORE2
- PE1

### Customer domain

- CE1
- Enterprise firewall
- internal VLANs and services

### Security domain

- attacker segment
- vulnerable targets

### Cloud domain

- AWS VPC
- hybrid path to enterprise or edge

---

## 7. Network Segments

Suggested initial segments:

| Segment | Purpose | Example Subnet |
|---|---|---|
| MGMT | host and device management | 10.10.0.0/24 |
| ISP-CORE | provider core links / loopbacks | 10.255.0.0/24 + P2P /31 or /30 |
| ISP-EDGE | transit/external simulation | 10.254.0.0/24 |
| CE-PE | customer/provider handoff | 172.16.0.0/30 |
| DMZ | public-facing services | 10.20.10.0/24 |
| SERVER | internal servers | 10.20.20.0/24 |
| CLIENT | user/workstation segment | 10.20.30.0/24 |
| SECURITY | attacker network | 10.20.40.0/24 |
| AUTOMATION | NetBox, Ansible, tooling | 10.20.50.0/24 |
| CLOUD | AWS VPC | 10.100.0.0/16 |

---

## 8. Initial VM Blueprint

| VM | Role | vCPU | RAM | Disk | Phase |
|---|---|---:|---:|---:|---|
| proxmox-host | hypervisor | n/a | n/a | n/a | base |
| isp-core1 | provider core router | 1 | 512 MB–1 GB | 8 GB | 1 |
| isp-core2 | provider core router | 1 | 512 MB–1 GB | 8 GB | 1 |
| isp-edge1 | simulated transit/edge | 1 | 512 MB–1 GB | 8 GB | 1 |
| pe1 | provider edge | 1 | 1 GB | 8 GB | 1 |
| ce1 | customer edge | 1 | 512 MB–1 GB | 8 GB | 1 |
| fw1 | enterprise firewall | 1–2 | 1 GB | 16 GB | 2 |
| win-ad1 | AD / DNS | 2 | 4 GB | 60 GB | 3 |
| app1 | linux application server | 1 | 1 GB | 20 GB | 3 |
| lb1 | load balancer | 1 | 1 GB | 16 GB | 4 |
| kali1 | offensive security host | 2 | 2 GB | 30 GB | 5 |
| vuln1 | vulnerable host | 1 | 1 GB | 20 GB | 5 |
| netbox1 | SoT | 2 | 2 GB | 30 GB | 6 |
| auto1 | automation node | 1–2 | 2 GB | 20 GB | 6 |
| mon1 | monitoring | 1–2 | 2 GB | 20 GB | 7 |

---

## 9. Phase Plan

## Phase 0 — Project foundation

### Goal
Create structure, naming, documentation, and build rules before deploying VMs.

### Deliverables

- GitHub repository created
- Obsidian vault structure created
- naming standards decided
- IP plan started
- VM inventory started
- project journal started

### Tasks

- create repository folders
- create markdown templates
- define hostname standard
- define subnet standard
- define phase tracker
- define lab rules for documenting changes

### Exit criteria

- project structure exists
- first README is committed
- phase tracker is ready

---

## Phase 1 — Proxmox + ISP core/edge foundation

### Goal
Build the provider side and customer handoff first.

### Components

- Proxmox installed
- Linux router templates or VyOS images ready
- ISP-CORE1
- ISP-CORE2
- ISP-EDGE1
- PE1
- CE1

### Topics

- virtual networking in Proxmox
- bridges and isolated segments
- loopbacks
- OSPF in provider core
- eBGP or static handoff between PE and CE
- route advertisement and default routing

### Deliverables

- routed provider topology
- CE can reach provider side
- routing table screenshots / notes
- traffic path documented

### Exit criteria

- routing is stable
- I can explain every advertised route
- I can trace traffic from CE to transit simulation

---

## Phase 2 — Enterprise firewall and internal segmentation

### Goal
Place a customer enterprise behind CE.

### Components

- firewall VM
- VLAN-backed or logically separated internal networks
- DMZ
- SERVER
- CLIENT
- MGMT

### Topics

- firewall zones
- NAT
- routing between CE and firewall
- segmentation
- north-south and east-west traffic

### Deliverables

- enterprise internal segments exist
- firewall policy baseline exists
- outbound path works from internal segments

### Exit criteria

- DMZ, SERVER, and CLIENT are separated
- firewall controls are tested
- path from client to outside is documented

---

## Phase 3 — Identity and core enterprise services

### Goal
Add the real enterprise backbone.

### Components

- Windows Server AD
- DNS
- optional DHCP
- Linux app server
- test client

### Topics

- domain design
- DNS dependency mapping
- domain join
- service reachability
- troubleshooting authentication and name resolution

### Deliverables

- domain created
- test client joined
- app server deployed
- DNS records documented

### Exit criteria

- client can authenticate to domain
- DNS works correctly
- app is reachable through intended path

---

## Phase 4 — Load balancing and application delivery

### Goal
Place an application behind a load-balancing layer.

### Components

- HAProxy or equivalent
- one or more backend apps
- DMZ exposure pattern

### Topics

- L4 vs L7
- health checks
- TLS termination
- reverse proxying
- persistence / stickiness

### Deliverables

- load balancer deployed
- application accessible through VIP / frontend
- health check behavior documented
- F5 concept mapping notes created

### Exit criteria

- app is reachable through LB
- failed backend behavior is validated
- I can explain the full request path

---

## Phase 5 — Offensive security segment

### Goal
Test the environment from an attacker point of view.

### Components

- Kali Linux
- vulnerable target
- optional exposed web app

### Topics

- recon
- enumeration
- HTTP inspection
- segmentation testing
- validating firewall and exposure assumptions

### Deliverables

- attack segment deployed
- recon notes created
- at least one controlled attack path tested
- hardening observations documented

### Exit criteria

- attacker-to-target path is understood
- findings are documented clearly
- defensive improvements are listed

---

## Phase 6 — NetBox and automation foundation

### Goal
Introduce Source of Truth and repeatable changes.

### Components

- NetBox
- automation node
- inventory and data model
- initial Ansible playbooks

### Topics

- device inventory
- IPAM
- interfaces and VLAN modeling
- config generation concepts
- idempotent automation

### Deliverables

- devices represented in NetBox
- prefixes and addresses documented
- first automation playbooks created
- manual-to-automated workflow documented

### Exit criteria

- NetBox reflects real lab state
- at least one change is driven from automation
- inventory is trusted enough to be useful

---

## Phase 7 — AWS hybrid extension

### Goal
Extend the enterprise into cloud.

### Components

- AWS account foundation
- VPC
- subnets
- EC2
- VPN or hybrid connectivity

### Topics

- VPC design
- cloud routing
- security groups vs firewall rules
- hybrid path troubleshooting

### Deliverables

- AWS VPC deployed
- at least one EC2 host reachable as designed
- hybrid connectivity documented
- traffic path comparison on-prem vs cloud documented

### Exit criteria

- path to AWS is working or fully understood
- enterprise-to-cloud design is documented
- key AWS networking concepts are mapped to lab topology

---

## Phase 8 — Monitoring and operations maturity

### Goal
Treat the lab like an operational environment.

### Components

- monitoring node
- logging or basic observability
- dashboards / checks

### Topics

- availability monitoring
- service checks
- route/service dependency thinking
- operational visibility

### Deliverables

- basic monitoring live
- service checks for critical nodes
- incident notes template created

### Exit criteria

- important services are monitored
- failures are visible quickly
- operational workflow is improving

---

## 10. Build Order Summary

1. Phase 0 — project foundation
2. Phase 1 — Proxmox + ISP routing
3. Phase 2 — enterprise firewall + segmentation
4. Phase 3 — AD + services
5. Phase 4 — load balancing
6. Phase 5 — offensive security
7. Phase 6 — NetBox + automation
8. Phase 7 — AWS hybrid
9. Phase 8 — monitoring

---

## 11. Repository Structure

```text
homelab-project/
├── README.md
├── docs/
│   ├── overview.md
│   ├── goals.md
│   ├── topology.md
│   ├── ip-plan.md
│   ├── naming-standards.md
│   ├── hardware.md
│   └── lessons-learned.md
├── phases/
│   ├── phase-00-foundation.md
│   ├── phase-01-isp-core-edge.md
│   ├── phase-02-enterprise-firewall.md
│   ├── phase-03-identity-services.md
│   ├── phase-04-load-balancing.md
│   ├── phase-05-offensive-security.md
│   ├── phase-06-netbox-automation.md
│   ├── phase-07-aws-hybrid.md
│   └── phase-08-monitoring.md
├── inventory/
│   ├── vm-inventory.md
│   ├── devices.md
│   ├── vlans.md
│   ├── prefixes.md
│   └── services.md
├── diagrams/
│   ├── logical-topology.md
│   └── physical-notes.md
├── build-log/
│   ├── daily-log.md
│   └── change-log.md
└── automation/
    ├── ansible/
    └── scripts/
```

---

## 12. Obsidian Vault Structure

```text
00 Inbox/
01 Project Overview/
02 Architecture/
03 Phases/
04 Inventory/
05 Build Log/
06 Troubleshooting/
07 Security Testing/
08 Automation/
09 Lessons Learned/
```

Suggested note names:

- Project Vision
- Current Topology
- IP Plan
- VM Inventory
- Phase 1 Tasks
- Phase 1 Lessons
- Build Journal
- Failure Notes
- Security Findings
- Automation Ideas

---

## 13. Naming Standard

Suggested hostname patterns:

- isp-core1
- isp-core2
- isp-edge1
- pe1
- ce1
- fw1
- win-ad1
- app1
- lb1
- kali1
- vuln1
- netbox1
- auto1
- mon1

Suggested principles:

- keep names short and obvious
- one role per VM where possible
- reflect function, not personal labels

---

## 14. Documentation Templates

## Daily build log template

```md
# Daily Log - YYYY-MM-DD

## What I worked on

## What I changed

## What worked

## What failed

## What I learned

## Next step
```

## Phase template

```md
# Phase XX - Name

## Goal

## Scope

## Components

## Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Risks / blockers

## Validation

## Notes

## Exit criteria
```

## Change log template

```md
# Change Log

## YYYY-MM-DD
- Added:
- Changed:
- Fixed:
- Broke:
```

## Troubleshooting template

```md
# Issue - Name

## Symptoms

## Scope

## Impact

## Path

## Actions taken

## Root cause

## Fix

## Prevention
```

---

## 15. Phase 0 Immediate Tasks

- [ ] Upgrade ThinkCentre to 32 GB RAM
- [ ] Confirm SSD capacity
- [ ] Install Proxmox
- [ ] Create GitHub repository
- [ ] Create Obsidian project vault/folder structure
- [ ] Add README.md
- [ ] Add phase files
- [ ] Add VM inventory file
- [ ] Add IP plan file
- [ ] Decide router platform: VyOS or FRRouting-based Linux routers

---

## 16. Phase 1 Immediate Tasks

- [ ] Create Proxmox bridges for lab segments
- [ ] Import or create router template
- [ ] Deploy isp-core1
- [ ] Deploy isp-core2
- [ ] Deploy isp-edge1
- [ ] Deploy pe1
- [ ] Deploy ce1
- [ ] Configure loopbacks
- [ ] Configure provider IGP
- [ ] Configure PE-CE handoff
- [ ] Test routing and reachability
- [ ] Document routing tables and paths

---

## 17. First Milestone

### Milestone name
**Provider to customer connectivity established**

### Definition of done

- provider core is operational
- PE and CE are exchanging routes as designed
- customer edge reaches upstream/transit simulation
- topology and IP plan are documented
- first screenshots / configs / lessons are committed

---

## 18. Project Vision Statement

This lab is a personal platform to rebuild deep technical capability across provider networking, enterprise infrastructure, cloud connectivity, offensive security, and automation. It is designed as a phased environment that grows from a routing foundation into a hybrid operational platform that can be documented, explained, tested, and eventually shared with a study group.

