# Phase 01 — Proxmox + ISP Core/Edge Foundation

## Goal

Build the provider side and customer handoff first. Establish a working routed provider topology before adding enterprise components.

## Scope

Provider domain only: ISP-CORE1, ISP-CORE2, ISP-EDGE1, PE1, CE1.

## Components

- Proxmox installed and bridges configured
- Linux router templates or VyOS images ready
- ISP-CORE1
- ISP-CORE2
- ISP-EDGE1
- PE1
- CE1

## Tasks

- [ ] Create Proxmox bridges for lab segments
- [ ] Import or create router template
- [ ] Deploy isp-core1
- [ ] Deploy isp-core2
- [ ] Deploy isp-edge1
- [ ] Deploy pe1
- [ ] Deploy ce1
- [ ] Configure loopbacks on all routers
- [ ] Configure provider IGP (OSPF)
- [ ] Configure PE-CE handoff (eBGP or static)
- [ ] Test routing and reachability
- [ ] Document routing tables and paths

## Topics

- Virtual networking in Proxmox
- Bridges and isolated segments
- Loopback addressing
- OSPF in provider core
- eBGP or static handoff between PE and CE
- Route advertisement and default routing

## Risks / Blockers

- Hardware upgrade (Phase 0) must be complete
- Proxmox must be installed before VMs can be deployed
- Router platform choice must be made

## Validation

- All routers have loopbacks configured and reachable within the provider domain
- OSPF is stable with all expected prefixes
- CE1 can reach simulated transit/upstream
- Routing tables match design
- Traffic path can be traced and explained

## Notes

- Document all routing table outputs with timestamps
- Capture configs for every router at this phase
- Take screenshots of reachability tests for the build log

## Exit Criteria

- Routing is stable
- Every advertised route can be explained
- Traffic from CE to transit simulation can be traced
