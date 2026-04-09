# Hybrid ISP + Enterprise + Cloud + Offensive Security Lab

Hybrid ISP & enterprise homelab simulating provider networking, load balancing, cloud integration, offensive security, and automation.

## Overview

This lab is built in phases on Proxmox and covers:

- **ISP/Provider networking** — core routers, edge, PE/CE handoff, OSPF, BGP
- **Enterprise infrastructure** — firewall, segmentation, Active Directory, DNS
- **Load balancing** — HAProxy with L4/L7, health checks, TLS, F5 concept mapping
- **Cloud hybrid** — AWS VPC with site-to-site VPN extension
- **Offensive security** — Kali Linux, vulnerable hosts, segmentation validation
- **Automation & SoT** — NetBox, Ansible, Python
- **Monitoring** — availability checks and operational visibility

## Tech Stack

### Core Platform
- Proxmox — hypervisor platform
- Ubuntu Server 24.04 LTS — base OS for general-purpose Linux VMs
- Podman — container runtime for tooling and workspace execution

### Infrastructure as Code
- OpenTofu — VM provisioning and infrastructure lifecycle management
- Proxmox templates — repeatable VM cloning baseline
- Reusable OpenTofu modules — scalable infrastructure definitions

### Configuration and Automation
- Ansible — post-provisioning configuration and validation
- Python — helper scripts, inventory generation, validation, and documentation glue

### Networking and Security
- VyOS (planned) — router platform for provider/core-edge phases
- HAProxy (planned) — load balancing and application delivery
- Kali Linux (planned) — offensive security validation

### Source of Truth and Operations
- NetBox (planned) — inventory, IPAM, topology relationships, and live documentation
- GitHub — version control and engineering history
- Markdown — project documentation and runbooks
- IDE-based workflow — daily coding, refactoring, and structured development

### Platform and Orchestration (Planned)
- Kubernetes — container orchestration platform for services and applications
- GitLab — source control, CI/CD pipelines, and automation platform

## Implementation Approach

The lab is built in layers rather than all at once.

1. Foundation first
   - Proxmox
   - storage
   - workspace VM
   - containerized tooling

2. Infrastructure as Code
   - OpenTofu environments and modules
   - template-based VM deployment
   - Git-tracked changes

3. Core network build-out
   - provider/core-edge nodes
   - multi-interface topology
   - routing validation

4. Configuration as Code
   - Ansible-based host and network configuration
   - reusable automation patterns

5. Source of Truth and observability
   - inventory, IPAM, diagrams, and monitoring

## Daily Working Model

- IDE for editing, refactoring, and project navigation
- Terminal for execution, validation, and Git operations
- Podman toolbox container for OpenTofu and other tooling
- Build logs for implementation history
- GitHub for version control and progress tracking

See [`homelab_lab_blueprint.md`](homelab_lab_blueprint.md) for the full project blueprint.

## Repository Structure

```text
├── homelab_lab_blueprint.md   # Full project blueprint

├── docs/                      # High-level documentation
│   ├── overview.md
│   ├── goals.md
│   ├── topology.md
│   ├── ip-plan.md
│   ├── naming-standards.md
│   ├── hardware.md
│   └── lessons-learned.md

├── phases/                    # Phase definitions + progress tracking
│   ├── phase-00-foundation.md
│   ├── phase-01-isp-core-edge.md
│   ├── phase-02-enterprise-firewall.md
│   ├── phase-03-identity-services.md
│   ├── phase-04-load-balancing.md
│   ├── phase-05-offensive-security.md
│   ├── phase-06-netbox-automation.md
│   ├── phase-07-aws-hybrid.md
│   └── phase-08-monitoring.md

├── build-log/                 # Detailed engineering logs
│   ├── daily-log.md
│   ├── change-log.md
│   ├── 2026-04-07-opentofu-first-vm.md   # ← (NEW) 

├── architecture/              # System-level design (NEW)
│   ├── core-network.md

├── runbooks/                  # Operational knowledge (NEW)
│   ├── opentofu.md

├── opentofu/                  # Infrastructure as Code (NEW CORE)
│   ├── environments/
│   │   └── lab-core/
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       ├── terraform.tfvars (ignored)
│   │       └── .gitignore
│   └── modules/               # (next step)

├── inventory/                 # Tracking of deployed assets
│   ├── vm-inventory.md
│   ├── devices.md
│   ├── vlans.md
│   ├── prefixes.md
│   └── services.md

├── diagrams/                  # Visual topology
│   ├── logical-topology.md
│   └── physical-notes.md

└── automation/                # Config management layer
    ├── ansible/
    └── scripts/
```

## Current Phase

- **Phase 00 — Project Foundation** (Done)
- **Phase 01 - ISP-Core-Edge** (In progress)

## Current status


### Completed foundation
- Proxmox reinstalled
- secondary SSD configured as `vmdata`
- Ubuntu Server 24.04 workspace VM (`ws1`) deployed
- SSH access working
- Podman installed
- toolbox container baseline built

### Current note
- Proxmox is currently connected through the UniFi switch
- MikroTik integration will come later as a separate network realism phase

## Build Principles

1. Build in phases, not all at once
2. Prefer simple and working over complex and unfinished
3. Document every design decision
4. Treat the lab like a real customer environment
5. Use the lab to explain, teach, and troubleshoot
6. Automate only after the manual process is understood
