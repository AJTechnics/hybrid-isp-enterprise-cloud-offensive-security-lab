# Phase 06 — NetBox and Automation Foundation

## Goal

Introduce Source of Truth and repeatable, documented change processes.

## Scope

AUTOMATION segment: netbox1, auto1. Model existing lab in NetBox. Build initial Ansible playbooks.

## Components

- netbox1 — NetBox instance (SoT)
- auto1 — Automation node (Ansible)
- Inventory and data model
- Initial Ansible playbooks

## Tasks

- [ ] Deploy netbox1
- [ ] Configure NetBox with lab site, tenant, and roles
- [ ] Add all devices to NetBox inventory
- [ ] Add all interfaces and IP addresses
- [ ] Add VLANs and prefixes
- [ ] Add cable/connectivity model where relevant
- [ ] Deploy auto1 (Ansible control node)
- [ ] Configure Ansible inventory from NetBox (dynamic or static)
- [ ] Write first Ansible playbook (connectivity check or config backup)
- [ ] Drive at least one change through automation
- [ ] Document manual-to-automated workflow

## Topics

- Device inventory in NetBox
- IPAM (prefixes, IP addresses, VLANs)
- Interface and connectivity modelling
- Config generation concepts
- Idempotent automation with Ansible

## Risks / Blockers

- NetBox requires PostgreSQL and Redis — plan resource allocation accordingly
- All previous phases should be complete so NetBox reflects a real state

## Validation

- NetBox reflects real lab state (devices, interfaces, IPs match actual config)
- At least one change is driven by automation
- Inventory is trusted and useful

## Notes

- Use NetBox as the source of truth from this point forward
- Any new device added to the lab should be added to NetBox first
- Ansible should be idempotent — running twice should not cause errors

## Exit Criteria

- NetBox reflects real lab state
- At least one change is driven from automation
- Inventory is trusted enough to be useful
